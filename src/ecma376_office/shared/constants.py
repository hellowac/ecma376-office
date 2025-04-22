"""
PML 包所需的常量值
"""

from enum import StrEnum

from ecma376_office.constants import RELATIONSHIP_TYPE_BASE


class CONTENT_TYPE(StrEnum):
    """
    各个部件的内容类型
    """

    # -------------------------------------------------------------------------------------------
    # https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-15/#152-部件概览

    # 15.2.1 附加特性部件
    AdditionalCharacteristics = 'application/xml'

    # 15.2.2 音频部件
    Audio = 'audio/aiff'  # 不支持, 多种多样
    Audio1 = 'audio/midi'
    Audio2 = 'audio/ogg'
    Audio3 = 'audio/mpeg'

    # 15.2.3 参考文献部件
    Bibliography = 'application/xml'

    # 15.2.4 内容部件
    Content = 'image/svg+xml'  # 多种多样
    Content1 = 'application/smil'
    Content2 = 'text/xml'

    # 15.2.5 自定义XML数据存储部件
    CustomXMLDataStorage = 'application/xml'

    # 15.2.6 自定义 XML 数据存储属性部件
    CustomXMLDataStorageProperties = 'application/vnd.openxmlformats-officedocument.customXmlProperties+xml'

    # 15.2.7 数字签名起源部件
    # 在opc包中定义 附录E  - OPC 包级别
    DigitalSignatureOrigin = 'application/vnd.openxmlformats-package.digitalsignature-origin'

    # 15.2.8 数字签名 XML 签名部件
    # 在opc包中定义 附录E - OPC 包级别
    DigitalSignatureXMLSignature = 'application/vnd.openxmlformats-package.digitalsignature-xmlsignature+xml'

    # 第二部分文档, 10.4.4 数字签名 XML 签名证书部件 - OPC 包级别
    DigitalSignatureCertificate = 'application/vnd.openxmlformats-package.digitalsignature-certificate'

    # 15.2.9 嵌入式控制持久化部件
    EmbeddedControlPersistence = 'application/vnd.ms-office.activeX+xml'  # 多种多样

    # 15.2.10 嵌入对象部件
    EmbeddedObject = None  # 多种多样, 任何支持的音频类型.

    # 15.2.11 嵌入包部件
    EmbeddedPackage = None  # 任何内容类型都被允许

    # 15.2.12 文件属性部件
    # 15.2.12.1 核心文件属性部件
    # 在opc包中定义 附录E
    CoreFileProperties = 'application/vnd.openxmlformats-package.coreproperties+xml'

    # 15.2.12.2 自定义文件属性部件
    CustomFileProperties = 'application/vnd.openxmlformats-officedocument.custom-properties+xml'

    # 15.2.12.3 扩展文件属性部件
    ExtendedFileProperties = 'application/vnd.openxmlformats-officedocument.custom-properties+xml'
    ExtendedFileProperties1 = 'application/vnd.openxmlformats-officedocument.extended-properties+xml'

    # 15.2.13 字体部件
    Font = 'application/x-fontdata'
    Font1 = 'application/x-font-ttf'
    Font2 = 'application/vnd.openxmlformats-officedocument.obfuscatedFont'

    # 15.2.14 图片部件, # 受支持的任何图片类型
    Image = 'image/gif'  # http://www.w3.org/Graphics/GIF/spec-gif89a.txt
    Image1 = 'image/png'  # ISO/IEC 15948:2003 http://www.libpng.org/pub/png/spec/
    Image2 = 'image/tiff'  # http://partners.adobe.com/public/developer/tiff/index.html#spec
    Image3 = 'image/pict'  # http://developer.apple.com/documentation/mac/QuickDraw/QuickDraw2.html
    Image4 = 'image/jpeg'  # http://www.w3.org/Graphics/JPEG/

    # 15.2.15 打印机设置部件
    PrinterSettings = (
        'application/vnd.openxmlformats-officedocument.spreadsheetml.printerSettings'  # 在 SpreadsheetML 文档中
    )
    PrinterSettings1 = (
        'application/vnd.openxmlformats-officedocument.wordprocessingml.printerSettings'  # 在 WordprocessingML 文档中
    )
    PrinterSettings2 = (
        'application/vnd.openxmlformats-officedocument.presentationml.printerSettings'  # 在 PresentationML 文档中
    )

    # 15.2.16 缩略图部件, # 受支持的任何图片类型
    Thumbnail = 'image/gif'
    Thumbnail1 = 'image/png'
    Thumbnail2 = 'image/tiff'
    Thumbnail3 = 'image/pict'
    Thumbnail4 = 'image/jpeg'

    # 15.2.17 视频部件, # 受支持的任何视频类型
    Video = 'video/avi'  # http://www.the-labs.com/Video/odmlff2-avidef.pdf
    Video1 = 'video/mpg'  # ISO/IEC 13818
    Video2 = 'video/mpeg'  # ISO/IEC 13818
    Video3 = 'video/ogg'  # http://www.theora.org/doc/Theora.pdf
    Video4 = 'video/quicktime'  # http://developer.apple.com/documentation/QuickTime/
    Video5 = 'video/vc1'  # http://tools.ietf.org/html/rfc4425
    # -------------------------------------------------------------------------------------------


class NAMESPACE(StrEnum):
    """OPC XML 命名空间的常量值"""

    # -------------------------------------------------------------------------------------------
    # https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-15/#152-部件概览

    # 15.2.1 附加特性部件
    AdditionalCharacteristics = 'http://schemas.openxmlformats.org/officeDocument/2006/additionalCharacteristics'

    # 15.2.2 音频部件
    Audio = None  # 不支持, 多种多样

    # 15.2.3 参考文献部件
    Bibliography = 'http://purl.oclc.org/ooxml/officeDocument/bibliography'

    # 15.2.4 内容部件
    Content = None  # 不支持,多种多样

    # 15.2.5 自定义XML数据存储部件
    CustomXMLDataStorage = None  # 不支持,多种多样

    # 15.2.6 自定义 XML 数据存储属性部件
    CustomXMLDataStorageProperties = 'http://purl.oclc.org/ooxml/officeDocument/customXmlDataProps'

    # 15.2.7 数字签名起源部件
    # 忽略

    # 15.2.8 数字签名 XML 签名部件
    # 忽略

    # 第二部分文档, 附录E - OPC 包级别
    # 证书签名
    DigitalSignatures = 'http://schemas.openxmlformats.org/package/2006/digitalsignature'
    # 媒体类型
    MediaTypesStream = 'http://schemas.openxmlformats.org/package/2006/content-types'

    # 15.2.9 嵌入式控制持久化部件
    EmbeddedControlPersistence = None  # 不支持

    # 15.2.10 嵌入对象部件
    EmbeddedObject = None  # 不适用

    # 15.2.11 嵌入包部件
    EmbeddedPackage = None  # 不适用

    # 15.2.12 文件属性部件
    # 15.2.12.1 核心文件属性部件
    # 在opc包中定义 附录E
    CoreFileProperties = 'http://schemas.openxmlformats.org/package/2006/metadata/core-properties'

    # 15.2.12.2 自定义文件属性部件
    CustomFileProperties = 'http://purl.oclc.org/ooxml/officeDocument/customProperties'

    # 15.2.12.3 扩展文件属性部件
    ExtendedFileProperties = 'http://purl.oclc.org/ooxml/officeDocument/extendedProperties'

    # 15.2.13 字体部件
    Font = None  # 不适用

    # 15.2.14 图片部件
    Image = None  # 不适用

    # 15.2.15 打印机设置部件
    PrinterSettings = None  # 不适用

    # 15.2.16 缩略图部件
    Thumbnail = None  # 不适用

    # 15.2.17 视频部件
    Video = None  # 不适用
    # -------------------------------------------------------------------------------------------


class RELATIONSHIP_TYPE(str, RELATIONSHIP_TYPE_BASE):
    """OPC 关系类型"""

    # -------------------------------------------------------------------------------------------
    # https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-15/#152-部件概览

    # 15.2.1 附加特性部件
    AdditionalCharacteristics = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/customXml'

    # 15.2.2 音频部件
    # Audio = "http://purl.oclc.org/ooxml/officeDocument/relationships/audio"
    Audio = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/audio'

    # 15.2.3 参考文献部件
    Bibliography = 'http://purl.oclc.org/ooxml/officeDocument/relationships/customXml'

    # 15.2.4 内容部件
    Content = 'http://purl.oclc.org/ooxml/officeDocument/relationships/customXml'

    # 15.2.5 自定义XML数据存储部件
    CustomXMLDataStorage = 'http://purl.oclc.org/ooxml/officeDocument/relationships/customXml'

    # 15.2.6 自定义 XML 数据存储属性部件
    CustomXMLDataStorageProperties = 'http://purl.oclc.org/ooxml/officeDocument/relationships/customXmlProps'

    # 15.2.7 数字签名起源部件
    # 在opc包中定义 附录E  - OPC 包级别
    DigitalSignatureOrigin = 'http://schemas.openxmlformats.org/package/2006/relationships/digital-signature/signature'

    # 15.2.8 数字签名 XML 签名部件
    # 在opc包中定义 附录E - OPC 包级别
    DigitalSignatureXMLSignature = (
        'http://schemas.openxmlformats.org/package/2006/relationships/digital-signature/origin'
    )

    # 第二部分文档, 10.4.4 数字签名 XML 签名证书部件 - OPC 包级别
    DigitalSignatureCertificate = (
        'http://schemas.openxmlformats.org/package/2006/relationships/digital-signature/certificate'
    )

    # 15.2.9 嵌入式控制持久化部件
    EmbeddedControlPersistence = 'http://purl.oclc.org/ooxml/officeDocument/relationships/control'

    # 15.2.10 嵌入对象部件
    EmbeddedObject = 'http://purl.oclc.org/ooxml/officeDocument/relationships/oleObject'  # 不适用

    # 15.2.11 嵌入包部件
    EmbeddedPackage = 'http://purl.oclc.org/ooxml/officeDocument/relationships/package'  # 不适用

    # 15.2.12 文件属性部件
    # 15.2.12.1 核心文件属性部件
    # 在opc包中定义 附录E
    CoreFileProperties = 'http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties'

    # 15.2.12.2 自定义文件属性部件
    CustomFileProperties = 'http://purl.oclc.org/ooxml/officeDocument/relationships/customProperties'
    CustomFileProperties1 = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/custom-properties'

    # 15.2.12.3 扩展文件属性部件
    ExtendedFileProperties = 'http://purl.oclc.org/ooxml/officeDocument/relationships/extendedProperties'
    ExtendedFileProperties1 = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties'

    # 15.2.13 字体部件
    # Font = "http://purl.oclc.org/ooxml/officeDocument/relationships/font"
    Font = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/font'

    # Font_table = (
    #     "http://schemas.openxmlformats.org/officeDocument/2006/relationships/fontTable"
    # )

    # 15.2.14 图片部件
    # Image = "http://purl.oclc.org/ooxml/officeDocument/relationships/image"
    Image = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image'

    # 15.2.15 打印机设置部件
    PrinterSettings = 'http://purl.oclc.org/ooxml/officeDocument/relationships/printerSettings'  # 不适用

    # 15.2.16 缩略图部件
    Thumbnail = 'http://purl.oclc.org/ooxml/officeDocument/relationships/metadata/thumbnail'
    Thumbnail1 = 'http://schemas.openxmlformats.org/package/2006/relationships/metadata/thumbnail'

    # 15.2.17 视频部件
    # Video = "http://purl.oclc.org/ooxml/officeDocument/relationships/video"
    Video = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/video'

    # 15.3 超链接
    # Hyperlinks = "http://purl.oclc.org/ooxml/officeDocument/relationships/hyperlink"
    Hyperlinks = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink'

    # -------------------------------------------------------------------------------------------
