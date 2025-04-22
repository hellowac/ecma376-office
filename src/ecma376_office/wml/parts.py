"""
PrensentationML 部件概览

参考: https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-16/#163-presentationml-概览
"""

from typing import TYPE_CHECKING

from ecma376_office.part import Part

if TYPE_CHECKING:
    from ecma376_office.oxml.wml.main import (
        CT_Comments,
        CT_Document,
        CT_Endnotes,
        CT_FontsList,
        CT_Footnotes,
        CT_GlossaryDocument,
        CT_HdrFtr,
        CT_Numbering,
        CT_Settings,
        CT_Styles,
        CT_WebSettings,
    )


class AlternativeFormatImportPart(Part):
    """11.3.1 替代格式导入部件

    根节点: 不适用

    任何基于文本的内容，其支持方式由应用程序定义。

    [注：可能支持的格式示例包括：

    - Text = text/plain
    - HTML = text/html
    - WordprocessingML=application/vnd.openxmlformats-officedocument.wordprocessingml.document
    - XHTML = application/xhtml+xml
    """

    @property
    def content(self):
        """
        文件原内容
        """

        return self.blob.decode()


class CommentsPart(Part):
    """11.3.2 注释部件

    根节点: comments
    """

    @property
    def oxml(self):
        """
        经过lxml解析过后的对象化的xml文档
        """

        oxml: CT_Comments = super().oxml

        return oxml


class DocumentSettingsPart(Part):
    """11.3.3 文档设置部件

    根节点: settings
    """

    @property
    def oxml(self):
        """
        经过lxml解析过后的对象化的xml文档
        """

        oxml: CT_Settings = super().oxml

        return oxml


class EndnotesPart(Part):
    """11.3.4 尾注部件

    根节点: endnotes
    """

    @property
    def oxml(self):
        """
        经过lxml解析过后的对象化的xml文档
        """

        oxml: CT_Endnotes = super().oxml

        return oxml


class FontTablePart(Part):
    """11.3.5 字体表部件

    根节点: fonts
    """

    @property
    def oxml(self):
        """
        经过lxml解析过后的对象化的xml文档
        """

        oxml: CT_FontsList = super().oxml

        return oxml


class FooterPart(Part):
    """11.3.6 页脚部件

    根节点: ftr
    """

    @property
    def oxml(self):
        """
        经过lxml解析过后的对象化的xml文档
        """

        oxml: CT_HdrFtr = super().oxml

        return oxml


class FootnotesPart(Part):
    """11.3.7 脚注部件

    根节点: footnotes
    """

    @property
    def oxml(self):
        """
        经过lxml解析过后的对象化的xml文档
        """

        oxml: CT_Footnotes = super().oxml

        return oxml


class GlossaryDocumentPart(Part):
    """11.3.8 术语表部件

    根节点: glossaryDocument
    """

    @property
    def oxml(self):
        """
        经过lxml解析过后的对象化的xml文档
        """

        oxml: CT_GlossaryDocument = super().oxml

        return oxml


class HeaderPart(Part):
    """11.3.9 头部部件

    根节点: hdr
    """

    @property
    def oxml(self):
        """
        经过lxml解析过后的对象化的xml文档
        """

        oxml: CT_HdrFtr = super().oxml

        return oxml


class MainDocumentPart(Part):
    """11.3.10 主文档部件

    根节点: document
    """

    @property
    def oxml(self):
        """
        经过lxml解析过后的对象化的xml文档
        """

        oxml: CT_Document = super().oxml

        return oxml


class NumberingDefinitionsPart(Part):
    """11.3.11 编号定义部件

    根节点: numbering
    """

    @property
    def oxml(self):
        """
        经过lxml解析过后的对象化的xml文档
        """

        oxml: CT_Numbering = super().oxml

        return oxml


class StyleDefinitionsPart(Part):
    """11.3.12 样式定义部件

    根节点: styles
    """

    @property
    def oxml(self):
        """
        经过lxml解析过后的对象化的xml文档
        """

        oxml: CT_Styles = super().oxml

        return oxml


class WebSettingsPart(Part):
    """11.3.13 web设置部件

    根节点: webSettings
    """

    @property
    def oxml(self):
        """
        经过lxml解析过后的对象化的xml文档
        """

        oxml: CT_WebSettings = super().oxml

        return oxml


class DocumentTemplatePart(Part):
    """11.4 文档模板

    文档模板可以通过WordprocessingML包的一个实例来表示，其中包含了样式、编号定义等元素，这些元素在基于该模板编辑文档时可供使用。WordprocessingML文档可以通过包含一个文档设置部件（[§11.3.3]）来引用另一个文档作为其文档模板，该部件使用附加模板元素的id属性显式指定了所需文档模板的文件位置。
    """



class FramesetsPart(Part):
    """11.5 框架集

    框架集(frameset)是一个WordprocessingML文档，用于指定其他WordprocessingML文档（在该上下文中称为框架）的位置和布局。框架集应由一个WordprocessingML文档的实例表示，该文档包含一个网页设置(Web Settings)部件（[§11.3.13]），其关系项指向该框架集的每个框架。
    """



class SubdocumentsPart(Part):
    """11.6 主文档和子文档

    主文档(master document)应由一个WordprocessingML文档的实例表示，其主文档（[§11.3.10]）部件指向该主文档的每个子文档。

    [理由：有时，将文档作为一系列片段来处理会比较方便，特别是当这些片段可能由协作组中的不同作者编辑时。也许将一本书视为章节的集合而不是一个大文档更有意义。通过拥有一个或多个子文档的主文档来将文档拆分成这样的片段是可以实现的。理由结束]
    """



class MailMergeDataSourcePart(Part):
    """11.7 邮件合并数据源

    一个存储有关邮件合并操作信息的文档可以包含一个文档设置部件（[§11.3.3]），其关系项使用此关系目标指向所需数据源的文件位置。
    """



class MailMergeHeaderDataSourcePart(Part):
    """11.8 邮件合并标头数据源

    一个存储有关邮件合并操作信息的文档可以包含一个文档设置部件（[§11.3.3]），其关系项通过此关系指向必要标题数据源的文件位置。
    """



class XSLTransformationPart(Part):
    """11.9 XSL 转换

    文档可以存储关于XSL转换的信息，该转换可能在文档以单个文件格式输出时（例如，作为XML或HTML）应用。这些信息存储在一个文档设置部件（[§11.3.3]）中，其部件关系项包含使用此关系到XSL转换文件位置的显式关系。[注意：关于此关系如何使用（结合saveThroughXslt元素）的完整描述，请参阅§17.15.1.76。]
    """
