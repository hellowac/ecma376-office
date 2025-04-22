"""
为序列化开放打包约定 (OPC) 包提供低级只读 API。
"""

import logging
from collections.abc import Generator
from typing import (
    TYPE_CHECKING,
    Any,
    BinaryIO,
    NamedTuple,
    Optional,
    TypeAlias,
)

from ecma376_office.opc.zip_pkg import ZipPkgReader
from ecma376_office.oxml.base import oxml_fromstring
from ecma376_office.oxml.opc.relationships import CT_Relationship, CT_Relationships, ST_TargetMode
from ecma376_office.oxml.xsd_types import XSD_AnyURI
from ecma376_office.packuri import PACKAGE_URI, PackURI

if TYPE_CHECKING:
    from ecma376_office.oxml.opc.content_types import CT_Types

logger = logging.getLogger(__name__)

AnyURI: TypeAlias = str
AnyExtension: TypeAlias = str
AnyContentType: TypeAlias = str


class PackageReader:
    """
    通过其 Serialized_parts 和 pkg_srels 属性提供对 zip 格式 OPC 包内容的访问。
    """

    def __init__(
        self,
        pkg_content_type: 'PackageContentType',
        pkg_srels: 'SerializedRelationshipCollection',
        all_parts: tuple['SerializedPart', ...],
    ):
        super().__init__()
        self._pkg_srels = pkg_srels
        self._serialiazed_all_parts = all_parts

    def __del__(self):
        logger.info('清除PackageReade...')

    @staticmethod
    def from_file(pkg_file: str | BinaryIO):
        """
        返回 |PackageReader| 实例加载了 *pkg_file* 的内容。
        """
        zip_reader = ZipPkgReader(pkg_file)

        logger.info(f'{zip_reader = }')
        # logger.info(f"{zip_reader.content_types_xml = }")

        pkg_content_type = PackageContentType.from_xml(zip_reader.content_types_xml)
        pkg_srels = PackageReader._seriazlied_relationship_collect_for(zip_reader, PACKAGE_URI)
        all_parts = PackageReader._load_all_serialized_parts(zip_reader, pkg_srels, pkg_content_type)

        # logger.info(f"{pkg_srels = }")
        logger.info(f'所有部件数量: {len(all_parts) = }')

        zip_reader.close()
        return PackageReader(pkg_content_type, pkg_srels, all_parts)

    def iter_serialized_parts(self):
        """
        为包中的每个序列化部分生成一个 4 元组 “(partname, content_type, part_blob, serialized_relationships_blob)”。
        """
        yield from self._serialiazed_all_parts

    def iter_serialized_relationships(self):
        """
        为包中的每个关系生成一个 2 元组 “(source_uri, srel)”。
        """
        for srel in self._pkg_srels:
            yield (PACKAGE_URI, srel)

        for spart in self._serialiazed_all_parts:
            for srel in spart.srels:
                yield (spart.part_name, srel)

    @staticmethod
    def _load_all_serialized_parts(
        zip_reader: ZipPkgReader,
        pkg_srels: 'SerializedRelationshipCollection',
        content_types: 'PackageContentType',
    ):
        """
        返回 | SerializedPart| 的列表 与 *zip_reader* 中的部件相对应的实例可以通过遍历以 *pkg_srels* 开头的关系图来访问。
        """
        sparts: list[SerializedPart] = []
        part_walker = PackageReader._walk_zip_all_parts(zip_reader, pkg_srels)
        for part_name, blob, srels, is_external in part_walker:
            # logger.info(f"求部件: {part_name} {part_name.ext} 的内容类型")
            content_type = content_types.get(part_name, 'unkonw')
            # logger.info(f"部件: {part_name }, 内容类型: {content_type } 有关系数量: {len(srels) }")
            spart = SerializedPart(part_name, content_type, blob, srels, is_external)
            sparts.append(spart)

        return tuple(sparts)

    @staticmethod
    def _seriazlied_relationship_collect_for(zip_reader: ZipPkgReader, source_uri: PackURI):
        """
        返回 |SerializedRelationshipCollection| 实例填充了由 *source_uri* 标识的源的关系。
        """

        # logger.info(f"源URI: {source_uri = }")

        # 有一些部件的关系部件不存在, 忽略,比如: xxx.bin 等嵌入式文件
        try:
            # 获取某个部件URI所标识的部件的 *.rel xml文件，即该部件的关系xml
            rels_xml = zip_reader.rels_xml_for(source_uri)
        except KeyError:
            # logger.info(f"部件: {source_uri} 的关系文件(.rels)不存在")
            rels_xml = None

        # logger.info(f"源URI {source_uri = }, {rels_xml = }")

        return SerializedRelationshipCollection.load_from_xml(source_uri.baseURI, rels_xml)

    @staticmethod
    def _walk_zip_all_parts(
        zip_reader: ZipPkgReader,
        srels: 'SerializedRelationshipCollection',
        visited_part_names: Optional[list[PackURI | XSD_AnyURI]] = None,
    ) -> Generator[tuple[PackURI, bytes, 'SerializedRelationshipCollection', bool], Any, None]:
        """
        通过遍历以 srels 为根的关系图，为 *zip_reader* 中的每个部件生成一个 3 元组“(partname, blob, srels)”。
        """
        if visited_part_names is None:
            visited_part_names = []

        for srel in srels:
            # 外部资源, 继续下一次遍历
            # if srel.is_external:
            # logger.info(f"外部部件: {srel.target_part_name = } {srel.target}")
            # continue

            if srel.target_part_name is None:
                continue

            part_name = srel.target_part_name

            # 已经遍历过的部件，继续
            if part_name in visited_part_names:
                continue

            visited_part_names.append(part_name)

            if not isinstance(part_name, PackURI):
                # logger.info(f"部件:{part_name} 的类型不是 PackURI, 是外部资源")
                continue

            # part_relationship_type = srel.reltype

            # logger.info(
            #     f"获取部件:{part_name} - 关系类型: {part_relationship_type} 的序列化的 xxx.rels 文件内容"
            # )

            # 有一些部件的关系部件不存在, 忽略,比如: xxx.bin 等嵌入式文件
            part_srels = PackageReader._seriazlied_relationship_collect_for(zip_reader, part_name)

            if not srel.is_external and zip_reader.exists(part_name.member_name):
                blob = zip_reader.blob_for(part_name)

            else:
                blob = b''
                logger.info(f'部件名称: {part_name.member_name} 不存在!!!')
                # continue

            yield (part_name, blob, part_srels, srel.is_external)

            for (
                part_name,
                blob,
                srels,
                is_external,
            ) in PackageReader._walk_zip_all_parts(zip_reader, part_srels, visited_part_names):
                yield (part_name, blob, srels, is_external)


class PackageContentType:
    """
    用于按部件名称查找内容类型，

    例如 content_type = cti['/ppt/presentation.xml']。
    """

    def __init__(self):
        super().__init__()

        # 比如: /ppt/slideLayouts/slideLayout1.xml : application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml
        self._overrides: dict[AnyURI, AnyContentType] = {}

        # 比如: .vml: application/vnd.openxmlformats-officedocument.vmlDrawing
        self._defaults: dict[AnyExtension, AnyContentType] = {}

    def __getitem__(self, part_name: PackURI):
        """
        返回由 *part_name* 标识的部件的内容类型。
        """

        # logger.info(f"{self._overrides = }")
        # logger.info(f"{self._defaults = }")

        if not isinstance(part_name, PackURI):
            tmpl = "ContentTypeMap 键必须是 <type 'PackURI'>, 得到 %s"
            raise KeyError(tmpl % type(part_name))

        lower_part_name = part_name.lower()

        if lower_part_name in self._overrides:
            return self._overrides[lower_part_name]

        lower_ext = part_name.ext.lower()

        if lower_ext in self._defaults:
            return self._defaults[lower_ext]

        tmpl = f'[Content_Types].xml 中没有为部件名称为“{part_name}”对应的内容类型(ContentType)'

        raise KeyError(tmpl)

    @staticmethod
    def from_xml(content_types_xml):
        """
        返回一个新的 |PackageContentType| 使用 *content_types_xml* 的内容填充的实例。
        """
        types_elm: CT_Types = oxml_fromstring(content_types_xml)
        ctmap = PackageContentType()
        ctmap._overrides = {o.part_name.lower(): o.content_type for o in types_elm.overrides}

        ctmap._defaults = {f'.{d.extension}'.lower(): d.content_type for d in types_elm.defaults}
        return ctmap

    def get(self, key, default: Optional[Any] = None):
        try:
            return self[key]
        except KeyError:
            return default


class SerializedPart(NamedTuple):
    """
    OPC 包部件的值对象。 提供对部件的部件名称、内容类型、blob 和序列化关系的访问。
    """

    part_name: PackURI
    content_type: AnyContentType
    blob: bytes
    srels: 'SerializedRelationshipCollection'
    is_external: bool


class SerializedRelationship:
    """
    表示 OPC 包中序列化关系的值对象。 在这种情况下，序列化意味着任何目标部分都通过其部件名称引用，而不是直接链接到内存中 |Part| 目标。
    """

    def __init__(self, baseURI: PackURI, rel_elm: CT_Relationship):
        super().__init__()
        self._baseURI = baseURI
        self._rel_elm = rel_elm

    @property
    def base_uri(self):
        return self._baseURI

    @property
    def oxml(self):
        return self._rel_elm

    @property
    def is_external(self):
        """
        是否为OPC包内部资源
        """
        return self._rel_elm.target_mode == ST_TargetMode.External

    @property
    def reltype(self):
        """关系类型, 例如: ``RT.OFFICE_DOCUMENT``"""
        return self._rel_elm.reltype

    @property
    def rId(self):
        """
        关系id, 例如: 'rId9', 对应于 “CT_Relationship” 元素上的 “Id” 属性。
        """
        return self._rel_elm.rId

    @property
    def target_mode(self):
        """
        “CT_Relationship” 元素的 “TargetMode” 属性中的字符串，“RTM.INTERNAL” 或 “RTM.EXTERNAL” 之一。
        """
        return self._rel_elm.target_mode

    @property
    def target(self):
        """
        “CT_Relationship” 元素的 “Target” 属性中的字符串，内部目标模式或任意 URI 的相对部分引用，例如 HTTP URL，用于外部目标模式。
        """
        return self._rel_elm.target

    @property
    def target_part_name(self):
        """
        |PackURI| 包含此关系所针对的部件名的实例。 如果 target_mode 是 ``'External'``，则在引用时引发 ``ValueError``。

        在引用之前使用 target_mode 进行检查。
        """

        # 目标可能为Null
        if self.target == 'NULL':
            return None

        if self.is_external:
            # msg = "Relationship 上的 PartName 属性未定义，其中 TargetMode == 'External' "
            # logger.warn(f"关系目标: {self.target} 的关系模式(TargetMode)为 'External'")
            # raise ValueError(msg)
            return self.target
        # 懒加载 _target_partname 属性
        # 目标部件URI
        if not hasattr(self, '_target_partname'):
            self._target_part_name = PackURI.from_rel_ref(self._baseURI, self.target or '')

        return self._target_part_name


class SerializedRelationshipCollection:
    """
    | SerializedRelationship| 的只读序列 与传递给构造函数的关系项 XML 相对应的实例。
    """

    def __init__(self, xml_blob: Optional[bytes]):
        super().__init__()
        self._srels: list[SerializedRelationship] = []
        self._xml_blob = xml_blob  # 有的部件没有关系文件

    def __iter__(self):
        """支持迭代，例如 'for x in srels:'"""
        return self._srels.__iter__()

    def __len__(self):
        """支持迭代，例如 'for x in srels:'"""
        return self._srels.__len__()

    @staticmethod
    def load_from_xml(baseURI: PackURI, rels_item_xml: Optional[bytes]):
        """
        返回 | SerializedRelationshipCollection | 加载了 *rels_item_xml* 中包含的关系的实例。

        如果 *rels_item_xml* 为 |None|，则返回空集合。
        """

        srels = SerializedRelationshipCollection(rels_item_xml)
        if rels_item_xml is not None:
            rels_elm: CT_Relationships = oxml_fromstring(rels_item_xml)

            # logger.info(f"部件: {baseURI = } 的 关系xml为: {rels_elm.xml = }")

            # logger.info(f"部件: {baseURI = } 的 关系xml为: {rels_elm = }")

            for rel_elm in rels_elm.relationships:
                srels._srels.append(SerializedRelationship(baseURI, rel_elm))

        # logger.info(f"部件关系目录: {baseURI = } 的(.rels)关系有: {len(srels._srels)}")

        return srels
