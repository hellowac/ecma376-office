"""
对应xsd: shared-documentPropertiesExtended.xsd

<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
    xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"
    targetNamespace="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
    elementFormDefault="qualified" blockDefault="#all">
    <xsd:import namespace="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"
        schemaLocation="shared-documentPropertiesVariantTypes.xsd"/>
    ...
</xsd:schema>

"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional, TypeVar

from ecma376_office.oxml.base import OxmlBaseElement, lookup
from ecma376_office.oxml.xsd_types import CT_XSD_Base64, CT_XSD_Boolean, CT_XSD_Int, CT_XSD_String

if TYPE_CHECKING:
    from ecma376_office.oxml.shared.doc_pr_variant_types import CT_Vector as vt_CT_Vector

# namespace_ep = "http://purl.oclc.org/ooxml/officeDocument/extendedProperties"
namespace_ep = 'http://schemas.openxmlformats.org/officeDocument/2006/extended-properties'
# namespace_vt = "http://purl.oclc.org/ooxml/officeDocument/docPropsVTypes"
namespace_vt = 'http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes'

logger = logging.getLogger(__name__)

ns_map = {
    'ep': namespace_ep,  # 当前命名空间
    'vt': namespace_vt,
}


def qn(tag: str):
    """将 dc:creator 这种的标签,转换为 {http://purl.org/dc/elements/1.1/}creator 这样的形式"""

    global ns_map

    if ':' not in tag:
        return tag

    ns_prefix, ns = tag.split(':')

    return f'{{{ns_map[ns_prefix]}}}{ns}'


SubBaseElement = TypeVar('SubBaseElement', bound=OxmlBaseElement)


class CT_VectorVariant(OxmlBaseElement):
    """矢量变体"""

    @property
    def vector(self) -> vt_CT_Vector:
        """矢量"""

        return self.find(qn('vt:vector'))  # type: ignore


class CT_VectorLpstr(OxmlBaseElement):
    """
    矢量标题对
    """

    @property
    def vector(self) -> vt_CT_Vector:
        """
        矢量
        """

        return self.find(qn('vt:vector'))  # type: ignore


class CT_DigSigBlob(OxmlBaseElement):
    """
    数字签名块
    """

    @property
    def blob(self) -> CT_XSD_Base64:
        """
        块数据
        """

        return getattr(self, qn('vt:blob'))


class CT_Properties(OxmlBaseElement):
    """
    属性
    """

    @property
    def template(self) -> Optional[CT_XSD_String]:
        """文档模板名称

        此元素指定外部文档模板的名称，该模板包含用于创建当前文档的格式和样式信息。
        """

        return getattr(self, qn('ep:Template'), None)

    @property
    def manager(self) -> Optional[CT_XSD_String]:
        """主管姓名

        该元素指定与文档关联的主管的姓名。
        """

        return getattr(self, qn('ep:Manager'), None)

    @property
    def company(self) -> Optional[CT_XSD_String]:
        """公司名称

        该元素指定与文档关联的公司名称。
        """

        return getattr(self, qn('ep:Company'), None)

    @property
    def pages(self) -> Optional[CT_XSD_Int]:
        """总页数

        该元素指定文档的总页数（如果适用）。
        """

        return getattr(self, qn('ep:Pages'), None)

    @property
    def words(self) -> Optional[CT_XSD_Int]:
        """字数

        该元素指定上次保存时文档中包含的总字数。
        """

        return getattr(self, qn('ep:Words'), None)

    @property
    def characters(self) -> Optional[CT_XSD_Int]:
        """字符总数

        该元素指定文档中的字符总数。
        """

        return getattr(self, qn('ep:Characters'), None)

    @property
    def presentation_format(self) -> Optional[CT_XSD_String]:
        """演示文稿的预期格式

        该元素指定演示文稿文档的预期格式。 例如，打算在视频上显示的演示具有 PresentationFormat “Vedio”。
        """

        return getattr(self, qn('ep:PresentationFormat'), None)

    @property
    def lines(self) -> Optional[CT_XSD_Int]:
        """行数

        Number of Lines

        该元素指定合格生产者最后一次保存文档时的总行数（如果适用）。
        """

        return getattr(self, qn('ep:Lines'), None)

    @property
    def paragraphs(self) -> Optional[CT_XSD_Int]:
        """段落总数

        Total Number of Paragraphs

        该元素指定文档中找到的段落总数（如果适用）。
        """

        return getattr(self, qn('ep:paragraphs'), None)

    @property
    def slides(self) -> Optional[CT_XSD_Int]:
        """幻灯片元数据元素

        Slides Metadata Element

        此元素指定演示文档中幻灯片的总数。
        """

        return getattr(self, qn('ep:Slides'), None)

    @property
    def notes(self) -> Optional[CT_XSD_Int]:
        """包含注释/笔记的幻灯片数量

        Number of Slides Containing Notes

        此元素指定演示文稿中包含注释的幻灯片的数量。
        """

        return getattr(self, qn('ep:Notes'), None)

    @property
    def total_time(self) -> Optional[CT_XSD_Int]:
        """总编辑时间元数据元素

        Total Edit Time Metadata Element

        编辑文档的总时间。 默认时间单位是分钟。
        """

        return getattr(self, qn('ep:TotalTime'), None)

    @property
    def hidden_slides(self) -> Optional[CT_XSD_Int]:
        """隐藏幻灯片数量

        此元素指定演示文稿文档中隐藏幻灯片的数量。
        """

        return getattr(self, qn('ep:HiddenSlides'), None)

    @property
    def mm_clips(self) -> Optional[CT_XSD_Int]:
        """多媒体剪辑总数

        Total Number of Multimedia Clips

        此元素指定文档中存在的声音或视频剪辑的总数。
        """

        return getattr(self, qn('ep:MMClips'), None)

    @property
    def scale_crop(self) -> Optional[CT_XSD_Boolean]:
        """缩略图显示模式

        Thumbnail Display Mode

        该元素指示文档缩略图的显示模式。 将此元素设置为 TRUE 可缩放文档缩略图以适应显示。
        将此元素设置为 FALSE 可以裁剪文档缩略图，从而仅显示适合显示屏的部分。
        """

        return getattr(self, qn('ep:ScaleCrop'), None)

    @property
    def heading_pairs(self) -> Optional[CT_VectorVariant]:
        """标题对

        标题对(Heading pairs)指示文档部件的分组以及每组中的部件数量。
        这些部件不是文档部件，而是文档部件的概念表示。
        """

        return getattr(self, qn('ep:HeadingPairs'), None)

    @property
    def titles_of_parts(self) -> Optional[CT_VectorLpstr]:
        """部件标题

        该元素指定每个文档的标题。 这些部件不是文档部件，而是文档部件的概念表示。
        """

        return getattr(self, qn('ep:TitlesOfParts'), None)

    @property
    def links_up_to_date(self) -> Optional[CT_XSD_Boolean]:
        """最新链接

        该元素指示文档中的超链接是否是最新的。 将此元素设置为 TRUE 以指示超链接已更新。 将此元素设置为 FALSE 以指示超链接已过时。
        """

        return getattr(self, qn('ep:LinksUpToDate'), None)

    @property
    def characters_with_spaces(self) -> Optional[CT_XSD_Int]:
        """字符数（带空格）

        该元素指定本文档中字符数（包括空格）的最后计数。
        """

        return getattr(self, qn('ep:CharactersWithSpaces'), None)

    @property
    def shared_doc(self) -> Optional[CT_XSD_Boolean]:
        """共享文档

        该元素指示该文档当前是否在多个生产者之间共享。 如果此元素设置为 TRUE，则生产者在更新文档时应小心。
        """

        return getattr(self, qn('ep:SharedDoc'), None)

    @property
    def hyperlink_base(self) -> Optional[CT_XSD_String]:
        """相对超链接基础

        Relative Hyperlink Base

        该元素指定用于评估本文档中的相对超链接的基本字符串。
        """

        return getattr(self, qn('ep:HyperlinkBase'), None)

    @property
    def hyperlinks(self) -> Optional[CT_VectorVariant]:
        """超链接列表

        该元素指定上次保存时文档中的超链接集。
        """

        return getattr(self, qn('ep:HLinks'), None)

    @property
    def hyperlink_changed(self) -> Optional[CT_XSD_Boolean]:
        """超链接已更改

        该元素指定该部件中的一个或多个超链接是由生产者在该部件中专门更新的。
        下一个打开本文档的制作者应使用本部件规定的新超链接来更新超链接关系。
        """

        return getattr(self, qn('ep:HyperlinksChanged'), None)

    @property
    def dig_sig(self) -> Optional[CT_DigSigBlob]:
        """数字签名

        该元素包含数字签名文档的签名。

        注意:

            此属性是遗留文档用来存储其二进制表示的数字签名的机制，应避免使用第 2 部分中定义的明确定义的机制。此属性的任何使用都应仅用于遗留兼容性，并且是 应用程序定义的。
        """

        return getattr(self, qn('ep:DigSig'), None)

    @property
    def application(self) -> Optional[CT_XSD_String]:
        """应用名称

        Application Name

        该元素指定创建该文档的应用程序的名称。
        """

        return getattr(self, qn('ep:Application'), None)

    @property
    def app_version(self) -> Optional[CT_XSD_String]:
        """应用版本

        该元素指定生成该文档的应用程序的版本。

        该元素的内容应采用 XX.YYYY 的形式，其中 X 和 Y 代表数值，否则该文档应被视为不合格。

        注意:

            该元素的内容并不代表绝对值，而是限定Application元素的内容以区分同一生产者的不同版本。 应用程序应仅以提供信息的方式使用此信息（作为文档元数据）。
        """

        return getattr(self, qn('ep:AppVersion'), None)

    @property
    def doc_security(self) -> Optional[CT_XSD_Int]:
        """文档安全

        该元数据元素将文档的安全级别指定为数值。 文档安全性定义为：

        - 1: 文档受密码保护。
        - 2: 建议以只读方式打开文档。
        - 3: 文档强制以只读方式打开。
        - 4: 文档已锁定以进行注释。
        """

        return getattr(self, qn('ep:DocSecurity'), None)


shared_doc_pr_extended_namespace = lookup.get_namespace(namespace_ep)
shared_doc_pr_extended_namespace[None] = OxmlBaseElement
shared_doc_pr_extended_namespace['Properties'] = CT_Properties
shared_doc_pr_extended_namespace['Template'] = OxmlBaseElement
shared_doc_pr_extended_namespace['Manager'] = CT_XSD_String
shared_doc_pr_extended_namespace['Company'] = CT_XSD_String
shared_doc_pr_extended_namespace['Pages'] = CT_XSD_Int
shared_doc_pr_extended_namespace['Words'] = CT_XSD_Int
shared_doc_pr_extended_namespace['Characters'] = CT_XSD_Int
shared_doc_pr_extended_namespace['PresentationFormat'] = CT_XSD_String
shared_doc_pr_extended_namespace['Lines'] = CT_XSD_Int
shared_doc_pr_extended_namespace['Paragraphs'] = CT_XSD_Int
shared_doc_pr_extended_namespace['Slides'] = CT_XSD_Int
shared_doc_pr_extended_namespace['Notes'] = CT_XSD_Int
shared_doc_pr_extended_namespace['TotalTime'] = CT_XSD_Int
shared_doc_pr_extended_namespace['HiddenSlides'] = CT_XSD_Int
shared_doc_pr_extended_namespace['MMClips'] = CT_XSD_Int
shared_doc_pr_extended_namespace['ScaleCrop'] = CT_XSD_Boolean
shared_doc_pr_extended_namespace['HeadingPairs'] = CT_VectorVariant
shared_doc_pr_extended_namespace['TitlesOfParts'] = CT_VectorLpstr
shared_doc_pr_extended_namespace['LinksUpToDate'] = CT_XSD_Boolean
shared_doc_pr_extended_namespace['CharactersWithSpaces'] = CT_XSD_Int
shared_doc_pr_extended_namespace['SharedDoc'] = CT_XSD_Boolean
shared_doc_pr_extended_namespace['HyperlinkBase'] = CT_XSD_String
shared_doc_pr_extended_namespace['HLinks'] = CT_VectorVariant
shared_doc_pr_extended_namespace['HyperlinksChanged'] = CT_XSD_Boolean
shared_doc_pr_extended_namespace['DigSig'] = CT_DigSigBlob
shared_doc_pr_extended_namespace['Application'] = CT_XSD_String
shared_doc_pr_extended_namespace['AppVersion'] = CT_XSD_String
shared_doc_pr_extended_namespace['DocSecurity'] = CT_XSD_Int
