"""
DML 包所需的常量值
"""

from enum import StrEnum

from ecma376_office.constants import RELATIONSHIP_TYPE_BASE


class CONTENT_TYPE(StrEnum):
    """
    各个部件的内容类型
    """

    # -------------------------------------------------------------------------------------------
    # https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-15/#152-部件概览

    # 11.3.1 替代格式导入部件
    AlternativeFormatImport = '*'

    # 11.3.2 注释部件
    Comments = 'application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml'

    # 11.3.3 文档设置部件
    DocumentSettings = 'application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml'

    # 11.3.4 尾注部件
    Endnotes = 'application/vnd.openxmlformats-officedocument.wordprocessingml.endnotes+xml'

    # 11.3.5 字体表部件
    FontTable = 'application/vnd.openxmlformats-officedocument.wordprocessingml.fontTable+xml'

    # 11.3.6 页脚部件
    Footer = 'application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml'

    # 11.3.7 脚注部件
    Footnotes = 'application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml'

    # 11.3.8 术语表部件
    GlossaryDocument = 'application/vnd.openxmlformats-officedocument.wordprocessingml.glossary+xml'

    # 11.3.9 头部部件
    Header = 'application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml'

    # 11.3.10 主文档部件
    MainDocument = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml'

    # 11.3.10 主文档部件
    MainDocument1 = 'application/vnd.openxmlformats-officedocument.wordprocessingml.template.main+xml'

    # 11.3.11 编号定义部件
    NumberingDefinitions = 'application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml'

    # 11.3.12 样式定义部件
    StyleDefinitions = 'application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml'

    # 11.3.13 web设置部件
    WebSettings = 'application/vnd.openxmlformats-officedocument.wordprocessingml.webSettings+xml'
    # -------------------------------------------------------------------------------------------


class NAMESPACE(StrEnum):
    """OPC XML 命名空间的常量值"""

    # -------------------------------------------------------------------------------------------
    # https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-11/#113-部件概览


class RELATIONSHIP_TYPE(str, RELATIONSHIP_TYPE_BASE):
    """OPC 关系类型"""

    # -------------------------------------------------------------------------------------------
    # https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-11/#113-部件概览

    # 11.3.1 替代格式导入部件
    # AlternativeFormatImport = (
    #     "http://purl.oclc.org/ooxml/officeDocument/relationships/aFChunk"
    # )
    AlternativeFormatImport = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/aFChunk'

    # 11.3.2 注释部件
    # Comments = "http://purl.oclc.org/ooxml/officeDocument/relationships/comments"
    Comments = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments'

    # 11.3.3 文档设置部件
    # DocumentSettings = (
    #     "http://purl.oclc.org/ooxml/officeDocument/relationships/settings"
    # )

    # 11.3.3 文档设置部件
    DocumentSettings = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings'

    # 11.3.4 尾注部件
    # Endnotes = "http://purl.oclc.org/ooxml/officeDocument/relationships/endnotes"
    Endnotes = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/endnotes'

    # 11.3.5 字体表部件
    # FontTable = "http://purl.oclc.org/ooxml/officeDocument/relationships/fontTable"
    FontTable = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/fontTable'

    # 11.3.6 页脚部件
    # Footer = "http://purl.oclc.org/ooxml/officeDocument/relationships/footer"
    Footer = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer'

    # 11.3.7 脚注部件
    # Footnotes = "http://purl.oclc.org/ooxml/officeDocument/relationships/footnotes"
    Footnotes = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/footnotes'

    # 11.3.8 术语表部件
    # GlossaryDocument = (
    #     "http://purl.oclc.org/ooxml/officeDocument/relationships/glossaryDocument"
    # )
    GlossaryDocument = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/glossaryDocument'

    # 11.3.9 头部部件
    # Header = "http://purl.oclc.org/ooxml/officeDocument/relationships/header"
    Header = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/header'

    # 11.3.10 主文档部件
    # MainDocument = (
    #     "http://purl.oclc.org/ooxml/officeDocument/relationships/officeDocument"
    # )
    MainDocument = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument'

    # 11.3.11 编号定义部件
    # NumberingDefinitions = (
    #     "http://purl.oclc.org/ooxml/officeDocument/relationships/numbering"
    # )
    NumberingDefinitions = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering'

    # 11.3.12 样式定义部件
    # StyleDefinitions = "http://purl.oclc.org/ooxml/officeDocument/relationships/styles"
    StyleDefinitions = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles'

    # 11.3.13 web设置部件
    # WebSettings = "http://purl.oclc.org/ooxml/officeDocument/relationships/webSettings"
    WebSettings = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/webSettings'

    # 11.4 文档模板
    # DocumentTemplate = (
    #     "http://purl.oclc.org/ooxml/officeDocument/relationships/attachedTemplate"
    # )
    DocumentTemplate = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/attachedTemplate'

    # 11.5 框架集
    # Framesets = "http://purl.oclc.org/ooxml/officeDocument/relationships/frame"
    Framesets = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/frame'

    # 11.6 主文档和子文档
    # Subdocuments = "http://purl.oclc.org/ooxml/officeDocument/relationships/subDocument"
    Subdocuments = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/subDocument'

    # 11.7 邮件合并数据源
    # MailMergeDataSource = (
    #     "http://purl.oclc.org/ooxml/officeDocument/relationships/mailMergeSource"
    # )
    MailMergeDataSource = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/mailMergeSource'

    # 11.8 邮件合并标头数据源
    # MailMergeHeaderDataSource = (
    #     "http://purl.oclc.org/ooxml/officeDocument/relationships/mailMergeHeaderSource"
    # )
    MailMergeHeaderDataSource = (
        'http://schemas.openxmlformats.org/officeDocument/2006/relationships/mailMergeHeaderSource'
    )

    # 11.9 XSL 转换
    # XSLTransformation = (
    #     "http://purl.oclc.org/ooxml/officeDocument/relationships/transform"
    # )
    XSLTransformation = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/transform'
    # -------------------------------------------------------------------------------------------
