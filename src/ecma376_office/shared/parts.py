"""
DrawingML 部件概览

参考: https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-14/#142-概览
"""

from typing import TYPE_CHECKING

from ecma376_office.opc.parts import CorePropertiesPart as OPC_CorePropertiesPart
from ecma376_office.opc.parts import ImagePart as OPC_ImagePart
from ecma376_office.part import Part

if TYPE_CHECKING:
    from ecma376_office.oxml.dml.main import CT_OfficeStyleSheet
    from ecma376_office.oxml.shared.additional_characteristics import CT_AdditionalCharacteristics
    from ecma376_office.oxml.shared.custom_xml_data_pr import CT_DatastoreItem
    from ecma376_office.oxml.shared.doc_custom_pr import CT_Properties
    from ecma376_office.oxml.shared.doc_pr_extended import CT_Properties


class AdditionalCharacteristicsPart(Part):
    """15.2.1 Characteristics

    根节点: Characteristics

    可能是以下部件的 关系目标部件

    大量的 PresentationML， SpreadsheetML， WordprocessingML 部件
    """

    @property
    def oxml(self):
        """
        经过lxml解析过后的对象化的xml文档
        """

        oxml: CT_AdditionalCharacteristics = super().oxml

        return oxml


class AudioPart(Part):
    """15.2.2 音频部件

    根节点: 不适用, 任何支持的音频部件都可以

    可能是以下部件的 关系目标部件

    大量的 PresentationML， SpreadsheetML， WordprocessingML 部件
    """

    # @property
    # def oxml(self):
    #     """
    #     经过lxml解析过后的对象化的xml文档
    #     """
    #     from ..oxml.pml.core import CT_CommentAuthorList

    #     oxml: CT_CommentAuthorList = super().oxml

    #     return oxml



class BibliographyPart(Part):
    """15.2.3 参考文献部件

    根节点: Sources

    可能是以下部件的 关系目标部件

    大量的 PresentationML， SpreadsheetML， WordprocessingML 部件
    """

    # @property
    # def oxml(self):
    #     """
    #     经过lxml解析过后的对象化的xml文档
    #     """
    #     from ..oxml.pml.core import CT_CommentAuthorList

    #     oxml: CT_CommentAuthorList = super().oxml

    #     return oxml



class ContentPart(Part):
    """15.2.4 内容部件

    根节点: 多种多样，由所使用的内容类型定义。

    可能是以下部件的 关系目标部件

    大量的 PresentationML， SpreadsheetML， WordprocessingML 部件
    """

    # @property
    # def oxml(self):
    #     """
    #     经过lxml解析过后的对象化的xml文档
    #     """
    #     from ..oxml.pml.core import CT_CommentAuthorList

    #     oxml: CT_CommentAuthorList = super().oxml

    #     return oxml



class CustomXMLDataStoragePart(Part):
    """15.2.5 自定义XML数据存储部件

    根节点: 不适用， 任何支持的xml部件都可以

    可能是以下部件的 关系目标部件

    大量的 PresentationML， SpreadsheetML， WordprocessingML 部件
    """

    # @property
    # def oxml(self):
    #     """
    #     经过lxml解析过后的对象化的xml文档
    #     """
    #     from ..oxml.pml.core import CT_CommentAuthorList

    #     oxml: CT_CommentAuthorList = super().oxml

    #     return oxml



class CustomXMLDataStoragePropertiesPart(Part):
    """15.2.6 自定义 XML 数据存储属性部件

    根节点: datastoreItem

    可能是以下部件的 关系目标部件

    Custom XML Data Storage
    """

    @property
    def oxml(self):
        """
        经过lxml解析过后的对象化的xml文档
        """

        oxml: CT_DatastoreItem = super().oxml

        return oxml


class DigitalSignatureOriginPart(Part):
    """15.2.7 数字签名起源部件

    根节点: 不适用

    可能是以下部件的 关系目标部件

    PresentationML， SpreadsheetML， WordprocessingML 的包部件
    """

    # @property
    # def oxml(self):
    #     """
    #     经过lxml解析过后的对象化的xml文档
    #     """
    #     from ..oxml.pml.core import CT_CommentAuthorList

    #     oxml: CT_CommentAuthorList = super().oxml

    #     return oxml



class DigitalSignatureCertificatePart(Part):
    """第二部分文档 10.4.4 数字签名证书部件

    根节点: 不适用

    可能是以下部件的 关系目标部件

    PresentationML， SpreadsheetML， WordprocessingML 的包部件
    """



class DigitalSignatureXMLSignaturePart(Part):
    """15.2.8 数字签名 XML 签名部件

    根节点: Signature

    可能是以下部件的 关系目标部件

    Digital Signature Origin
    """

    @property
    def oxml(self):
        """
        经过lxml解析过后的对象化的xml文档
        """

        oxml: CT_OfficeStyleSheet = super().oxml

        return oxml


class EmbeddedControlPersistencePart(Part):
    """15.2.9 嵌入式控制持久化部件

    根节点: 适用

    可能是以下部件的 关系目标部件

    PresentationML， SpreadsheetML， WordprocessingML 的包部件
    """

    # @property
    # def oxml(self):
    #     """
    #     经过lxml解析过后的对象化的xml文档
    #     """
    #     from ..oxml.dml.main import CT_BaseStylesOverride

    #     oxml: CT_BaseStylesOverride = super().oxml

    #     return oxml


class EmbeddedObjectPart(Part):
    """15.2.10 嵌入对象部件

    根节点: 不适用

    可能是以下部件的 关系目标部件

    PresentationML， SpreadsheetML， WordprocessingML 的包部件
    """


class EmbeddedPackagePart(Part):
    """15.2.11 嵌入包部件

    根节点: 不适用

    可能是以下部件的 关系目标部件

    PresentationML， SpreadsheetML， WordprocessingML 的包部件

    """


class FilePropertiesExtendedPart(Part):
    """15.2.12.3 扩展文件属性部件

    根节点: Properties

    可能是以下部件的 关系目标部件

    PresentationML， SpreadsheetML， WordprocessingML 的包部件

    """

    @property
    def oxml(self):
        """
        经过lxml解析过后的对象化的xml文档
        """

        oxml: CT_Properties = super().oxml

        return oxml


FilePropertiesCorePart = OPC_CorePropertiesPart
"""15.2.12.1 核心文件属性部件

根节点: coreProperties

可能是以下部件的 关系目标部件

PresentationML， SpreadsheetML， WordprocessingML 的包部件

此部件在Opc包中定义
"""


class FilePropertiesCustomPart(Part):
    """15.2.12.2 自定义文件属性部件

    根节点: properties

    可能是以下部件的 关系目标部件

    PresentationML， SpreadsheetML， WordprocessingML 的包部件
    """

    @property
    def oxml(self):
        """
        经过lxml解析过后的对象化的xml文档
        """

        oxml: CT_Properties = super().oxml

        return oxml


class FontPart(Part):
    """15.2.13 字体部件

    根节点: 不适用

    可能是以下部件的 关系目标部件

    PresentationML， SpreadsheetML， WordprocessingML 的包部件

    """


ImagePart = OPC_ImagePart
# """15.2.14 图片部件

# 根节点: 不适用

# 可能是以下部件的 关系目标部件

# PresentationML， SpreadsheetML， WordprocessingML 的包部件

# """


class PrinterSettingsPart(Part):
    """15.2.15 打印机设置部件

    根节点: 不适用

    可能是以下部件的 关系目标部件

    SpreadsheetML Chartsheet, Dialogsheet, Worksheet parts,
    WordprocessingML Main Document 或 Glossary Document parts

    """


# class ThumbnailPart(Part):
ThumbnailPart = OPC_ImagePart
"""15.2.16 缩略图部件

根节点: 不适用

可能是以下部件的 关系目标部件

PresentationML， SpreadsheetML， WordprocessingML 的包部件
"""


class VideoPart(Part):
    """15.2.10 嵌入对象部件

    根节点: 不适用

    大量 PresentationML，WordprocessingML 的部件
    """



# class HyperlinksPart(Part):
class HyperlinksPartTargetStr(str):
    """15.3 超链接

    根节点: 不适用
    """
