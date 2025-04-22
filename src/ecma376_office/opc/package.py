"""
提供用于操作开放打包约定 (OPC) 包的 API。
"""

from __future__ import annotations

import logging
import weakref
from typing import (
    TYPE_CHECKING,
    Any,
    BinaryIO,
    Optional,
    Self,
    TypeAlias,
    TypeVar,
)

from ecma376_office.descriptor import lazyproperty
from ecma376_office.opc.constants import CONTENT_TYPE as OCT
from ecma376_office.opc.constants import RELATIONSHIP_TYPE as ORT
from ecma376_office.opc.pkg_reader import PackageReader
from ecma376_office.packuri import PACKAGE_URI, PackURI
from ecma376_office.part import PartFactory, SpecificPart
from ecma376_office.relationship import RelationshipCollection
from ecma376_office.utils import DMLPartFinder, PMLPartFinder, SharedPartFinder, WMLPartFinder

if TYPE_CHECKING:
    from collections.abc import Callable, Generator

    from ecma376_office.opc.parts import CorePropertiesPart
    from ecma376_office.oxml.xsd_types import XSD_ID, XSD_AnyURI

# 泛型
T = TypeVar('T')

AnyURI = str
AnyContentType: TypeAlias = str

logger = logging.getLogger(__name__)


class PackageBase:
    """
    包基类

    主要提供解析包，加载包所有部件的方法

    主要 API 类。 通过调用 open 类方法以及包含包文件或类文件对象的路径来构造新实例。
    """

    def __init__(self, pkg_reader: PackageReader):
        """整个包的关系，/_res/.res"""

        self._relationship_collect = RelationshipCollection(PACKAGE_URI.baseURI)
        self.pkg_reader = pkg_reader
        self.all_parts: Optional[dict] = None

    def __del__(self):
        """清除OPC包"""

        # for uri, part in self.all_parts.items():
        #     logger.info(
        #         f"{uri = } {sys.getrefcount(part)} - {weakref.getweakrefcount(part)}"
        #     )

        del self.all_parts  # 删除唯一保留的强引用.
        logger.info('清除OPC包....')

    @classmethod
    def open(cls: type[Self], pkg_file: str | BinaryIO):
        """
        返回 |OpcPackage| 实例加载了 *pkg_file* 的内容。
        """
        pkg_reader = PackageReader.from_file(pkg_file)
        opc_pkg = cls(pkg_reader)

        logger.info('解组 opc 包 的 部件')

        # 保持1个强引用
        opc_pkg.all_parts = Unmarshaller.unmarshal(pkg_reader, opc_pkg, PartFactory)
        return opc_pkg

    @property
    def parts(self):
        """
        返回一个不可变序列（元组），其中包含对此OPC包中每个部件的引用。
        """
        return tuple(p for p in self._walk_parts(self._relationship_collect))

    @property
    def rels(self):
        """
        返回对 |RelationshipCollection| 的引用 保存此包的关系。
        """
        return self._relationship_collect

    def _add_relationship(
        self,
        reltype: XSD_AnyURI,
        target: SpecificPart | PackURI,
        rId: XSD_ID,
        external: bool = False,
    ):
        """
        返回新添加的 | Relationship| 此包与带有键 *rId* 的部件 *target* 之间的 *reltype* 实例。

        如果 *external* 为 |True|，则目标模式设置为“RTM.EXTERNAL”。

        target: 为Part的实例时表示是包的内部资源，为AnyURI的实例时表示是外部资源。
        """
        return self._relationship_collect.add_relationship(reltype, target, rId, external)

    @staticmethod
    def _walk_parts(rels: RelationshipCollection, parts: list[SpecificPart] | None = None) -> Generator[SpecificPart, Any, Any]:
        """
        通过执行 rels 图的深度优先遍历，准确生成对包中每个部件的一个引用。
        """
        if parts is None:
            parts = []
        visited_parts: list[SpecificPart] = parts or []

        for rel in rels:  # type: ignore
            if rel.is_external:
                continue
            part = rel.target_part

            if part in visited_parts:
                continue

            visited_parts.append(part)  # type: ignore

            yield part  # type: ignore

            for part in OpcPackage._walk_parts(
                part._relationship_collect,
                visited_parts,  # type: ignore
            ):
                yield part


AnyPackage = TypeVar('AnyPackage', bound=PackageBase)


class OpcPackage(PackageBase):
    """
    对应 ML 中的 Shared 中共享部件
    """

    @lazyproperty
    def main_document(self):
        """

        返回对此包的主文档部分的引用。

        示例包括:

        WordprocessingML 包的文档部件、 --> word 文档

        PresentationML 包的演示部件、 --> pptx 文档

        SpreadsheetML 包的工作簿部件。--> xlst 文档
        """
        part = SharedPartFinder._part_by_rt(ORT.OFFICE_DOCUMENT, self.rels)

        if part is not None:
            content_type = part.content_type

            if content_type in {OCT.PRESONTAION, OCT.PRESONTAION1, OCT.PRESONTAION2}:
                logger.info('zip文件为pptex文件包')
                return part

            if content_type in {OCT.WORDPROCESSING, OCT.WORDPROCESSING1}:
                logger.info('zip文件为wordx文件包')
                return part

            if content_type in {OCT.WORKBOOK, OCT.WORKBOOK1}:
                logger.info('zip文件为xlsx文件包')
                return part
            msg = f'未知的主文档内容(媒体)类型:{content_type}'
            raise ValueError(msg)

        msg = '获取主文档失败！'
        raise ValueError(msg)

    @property
    def additional_characteristics(self):
        """
        包级别的附加特性部件

        主要针对xlsx包的一些支持特性说明
        """

        return SharedPartFinder.additional_characteristics(self.rels)

    @property
    def content(self):
        """15.2.4 内容部件

        此部件类型的实例可以包含 ECMA-376 未定义的格式的 XML 标记。

        包允许包含零个或多个内容部件，并且每个此类部件应成为

        - 注释 ([§11.3.2])、
        - 尾注 ([§11.3.4])、
        - 页脚 ([§11.3.6])、
        - 脚注（[§11.3.7]）、
        - 术语表文档（[§11.3.8]）、
        - 标题([§11.3.9]), 或

        WordprocessingML 包中主文档（[§11.3.10]）部件、

        SpreadsheetML 包中的绘图 ([§12.3.8]) 部件； 或

        - 讲义母版 ([§13.3.3])、
        - 笔记幻灯片 ([§13.3.5])、
        - 笔记母版 ([§13.3.4])、
        - 幻灯片 ([§13.3.8])、
        - 幻灯片布局([§ 13.3.9])，或

        PresentationML包中的幻灯片母版（[§13.3.10]）

        等等这些部件的显式关系的目标
        """

        return SharedPartFinder.content(self.rels)

    @property
    def custom_xml_data_storate(self):
        """15.2.5 自定义XML数据存储部件

        该部件类型的实例可以包含任意 XML。 因此，此部件的实例可用于通过此包往返任意自定义 XML 数据。
        """

        return SharedPartFinder.custom_xml_data_storage(self.rels)

    @property
    def custom_xml_data_storate_pr(self):
        """15.2.6 自定义 XML 数据存储属性部件

        此部件类型的实例包含为此自定义 XML 数据指定的属性集。 这些属性由存储的唯一 ID 以及有关此自定义 XML 数据存储所使用的 XML Schema 集的信息组成。
        """

        return SharedPartFinder.custom_xml_data_storage_pr(self.rels)

    @property
    def digital_signature_origin(self):
        """15.2.7 数字签名起源部件

        该部件内容设计数字签名，目前未涉及，且章节应为第二部分的§10.4.2 节，详细信息参考原文档/文件.
        """

        SharedPartFinder.digital_signature_origin(self.rels)

    @property
    def digital_signature_xml_signature(self):
        """15.2.8 数字签名 XML 签名部件

        该部件内容设计数字签名，目前未涉及，且章节应为第二部分的§10.4.3 节，详细信息参考原文档/文件.
        """

        SharedPartFinder.digital_signature_origin(self.rels)

    @property
    def embedded_control_persistence(self):
        """15.2.9 嵌入式控制持久化部件

        该部件的实例包含有关包中嵌入控件的信息。 当要求保留时，此信息由指定的控件提供。

        一个包允许包含一个或多个嵌入式控制持久性部件
        """

        SharedPartFinder.embedded_control_persistence(self.rels)

    @property
    def embedded_object(self):
        """15.2.10 嵌入对象部件

        此部件类型的实例可以包含由任何嵌入对象服务器生成的嵌入对象.

        包允许包含零个或多个嵌入式对象部件
        """

        SharedPartFinder.embedded_object(self.rels)

    @property
    def embedded_package(self):
        """15.2.11 嵌入包部件

        包允许包含零个或多个嵌入式包部件
        """

        SharedPartFinder.embedded_package(self.rels)

    @property
    def core_properties(self):
        """
        15.2.12.1 核心文件属性部件

        该部件和相关的 OPC 部件在 ECMA-376-2 的第 11 节 “核心属性” 中定义。

        较新版的关于核心属性的内容在第二部分的第8章中定义。
        """
        # logger.info(f"{self._relationship_collect =}")

        part: CorePropertiesPart = SharedPartFinder._part_require_by_rt(ORT.CORE_PROPERTIES, self.rels)

        return part

    @property
    def file_custom_pr(self):
        """15.2.12.2 自定义文件属性部件

        此部件的实例包含适用于包的自定义文件属性的名称、它们的值以及这些值的类型。 自定义文件属性可能是为其准备文档的客户的名称、发生某些事件的日期/时间、文档编号或某些布尔状态标志。

        一个包最多应包含一个自定义文件属性部件，并且该部件应是文档的包关系项中关系的目标。
        """

        return SharedPartFinder.file_custom_pr(self.rels)


    @property
    def file_extended_pr(self):
        """15.2.12.3 扩展文件属性部件

        该部件的实例包含特定于 Office Open XML 文档的属性。

        一个包最多应包含一个扩展文件属性部件，并且该部件应是文档的包关系项(/_rels/.rels)中关系的目标。

        该内容类型的部件的根元素应是Properties。
        """

        return SharedPartFinder.file_extended_pr(self.rels)


    @property
    def font(self):
        """15.2.13 字体部件

        此部件类型的实例包含直接嵌入到文档中的给定字体。 （当使用自定义字体或未广泛分发的字体时，这非常有用。）
        """

        SharedPartFinder.font(self.rels)

    @property
    def image(self):
        """15.2.14 图片部件

        图像可以作为 ZIP 项存储在包中。 图像 ZIP 项应通过图像部件关系和适当的内容类型来标识。

        一个包允许包含零个或多个图像部件，并且每个此类部件应成为以下部件的显示关系目录, 如下:
        """

        SharedPartFinder.image(self.rels)

    @property
    def printer_settings(self):
        """15.2.15 打印机设置部件

        此部件类型的实例包含有关打印机或显示设备的初始化和环境的信息。 该信息的布局是应用程序定义的。
        """

        SharedPartFinder.printer_settings(self.rels)

    @property
    def thumbnail(self):
        """返回此OPC包的缩略图

        一个包只能有一个缩略图
        """

        return SharedPartFinder.thumbnail(self.rels)


    @property
    def vedio(self):
        """15.2.17 视频部件

        包允许包含零个或多个视频部件
        """

        SharedPartFinder.video(self.rels)

    @property
    def hyperlinks(self):
        """15.3 超链接

        超链接可以作为关系存储在包中。 超链接应通过包含指定给定超链接的目的地的目标来标识。
        """

        SharedPartFinder.hyperlinks(self.rels)


class DMLPackage(OpcPackage):
    """
    aaa
    """

    @property
    def chart(self):
        """
        14.2.1 图表部件
        """

        return DMLPartFinder.chart(self.rels)

    @property
    def chart_drawing(self):
        """
        14.2.2 图表绘制部件
        """

        return DMLPartFinder.chart_drawing(self.rels)

    @property
    def diagrame_colors(self):
        """
        14.2.3 绘制颜色部件
        """

        return DMLPartFinder.diagrame_colors(self.rels)

    @property
    def chart_data(self):
        """
        14.2.4 图表数据部件
        """

        return DMLPartFinder.diagrame_data(self.rels)

    @property
    def diagrame_layout_definition(self):
        """
        14.2.5 绘制布局定义部件
        """

        return DMLPartFinder.diagrame_layout_definition(self.rels)

    @property
    def diagrame_style(self):
        """
        14.2.6 绘制样式部件
        """

        return DMLPartFinder.diagrame_style(self.rels)

    @property
    def theme(self):
        """
        14.2.7 主题部件
        """

        return DMLPartFinder.theme(self.rels)

    @property
    def theme_override(self):
        """
        14.2.8 主题覆盖部件
        """

        return DMLPartFinder.theme_override(self.rels)

    @property
    def table_style(self):
        """
        14.2.9 表格样式部件
        """

        return DMLPartFinder.table_style(self.rels)


class PPTxPackage(DMLPackage):
    """
    解析pptx文件的OPC包的封装
    """

    @property
    def presentation_part(self):
        """
        演示文稿部件
        """

        return PMLPartFinder.presentation(self.rels)


        # raise OPCError(f"获取演示文稿部件失败（presentation.xml）")


class WordPackage(DMLPackage):
    """
    ...
    """

    @property
    def docx_main_part(self):
        """
        文字处理部件
        """

        return WMLPartFinder.main_document(self.rels)


        # raise OPCError(f"获取演示文稿部件失败（presentation.xml）")


class XlsxPackage(DMLPackage):
    """
    ...
    """


class Unmarshaller:
    """提取 PackageReader 中的包的内容的静态方法组合， 数据解组器,解包器(Unmarshaller)"""

    @staticmethod
    def unmarshal(
        pkg_reader: PackageReader,
        opc_pkg: AnyPackage,
        part_factory: Callable[[PackURI, AnyContentType, bytes, Optional[bytes], bool], SpecificPart],
    ):
        """
        根据 *pkg_reader* 的内容构建部件图并实现关系，
        将每个部件的构建委托给 *part_factory*。
        包关系已添加到 *opc_pkg*。
        """

        # 1个强引用，在解析期间一直存活,
        # 1个若引用字典，在解析期间一直使用，不创建新的强引用，防止内存泄漏（循环引用），
        pkg_all_parts, weakref_parts = Unmarshaller._unmarshal_parts(pkg_reader, part_factory)

        logger.info(f'包部件总数为: {len(pkg_all_parts) = }')

        Unmarshaller._unmarshal_relationships(pkg_reader, opc_pkg, weakref_parts)
        for part in weakref_parts.values():
            part._after_unmarshal()

        return pkg_all_parts

    @staticmethod
    def _unmarshal_parts(
        pkg_reader: PackageReader,
        part_factory: Callable[[PackURI, AnyContentType, bytes, Optional[bytes], bool], SpecificPart],
    ):
        """
        返回 |Part| 的字典 从 *pkg_reader* 解组的实例，按部件名称键入。

        副作用是 *pkg_reader* 中的每个部件都是使用 *part_factory* 构造的。
        """
        logger.info('遍历所有部件:')
        parts: dict[PackURI, SpecificPart] = {}
        weakref_parts = {}
        for spart in pkg_reader.iter_serialized_parts():
            # logger.info(f"遍历部件: {partname} -> {content_type}")

            # 构建具体的部件对象
            # 1个强引用，在解析期间一直存活,
            parts[spart.part_name] = part_factory(
                spart.part_name,
                spart.content_type,
                spart.blob,
                spart.blob,
                spart.is_external,
            )

            # 1个若引用字典，在解析期间一直使用，不创建新的强引用，防止内存泄漏（循环引用），
            weakref_parts[spart.part_name] = weakref.proxy(parts[spart.part_name])

        return parts, weakref_parts

    @staticmethod
    def _unmarshal_relationships(
        pkg_reader: PackageReader,
        opc_pkg: AnyPackage,
        parts: dict[PackURI, SpecificPart],
    ):
        """
        将关系添加到与 *pkg_reader* 中的每个关系相对应的源对象，并将其 target_part 设置为 *parts* 中的实际目标部件。
        """

        # logger.info(f"原始所有的部件: {parts}")

        for (
            source_uri,
            serialized_relationship,
        ) in pkg_reader.iter_serialized_relationships():
            # if source_uri == "/":
            #     logger.info(
            #         f"{source_uri = } {serialized_relationship.target_part_name =}"
            #     )

            source: AnyPackage | SpecificPart

            if source_uri == '/':
                source = opc_pkg

                # "/_rels/.rels" 部件的 xml源码
                source.rels._rels_blob = pkg_reader._pkg_srels._xml_blob
            else:
                source = parts[source_uri]  # type: ignore
                source._rels_blob = pkg_reader._pkg_srels._xml_blob  # "" type: ignore

            if serialized_relationship.is_external:
                # logger.info(f"{serialized_relationship.target = } 外部部件")
                try:
                    target = PackURI(serialized_relationship.target)
                except ValueError:
                    # 说明为外部部件且不是以'/'开头.
                    target = serialized_relationship.target

            elif serialized_relationship.target_part_name in parts:
                # logger.info(f"{serialized_relationship.target = } 内部部件")
                target = parts[serialized_relationship.target_part_name]  # type: ignore

            # 有一些部件找不到对应的物理部件，故此忽略，比如缩略图
            else:
                # logger.info(
                #     f"{source_uri =} {serialized_relationship.target_part_name =} 不存在, 忽略"
                # )
                continue

            # if source_uri == "/":
            # logger.info(
            #     f"{source_uri} 添加关系: {serialized_relationship.reltype} {target.part_name} {serialized_relationship.rId} "
            # )
            # logger.info(
            #     f"{source_uri} 添加关系: {target.part_name} - {serialized_relationship.rId} - {type(target)}"
            # )

            source._add_relationship(
                serialized_relationship.reltype,
                target,  # type: ignore
                serialized_relationship.rId,
                serialized_relationship.is_external,
            )
