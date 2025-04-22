"""
opc 包所需的常量值
"""

from enum import StrEnum

from ecma376_office.constants import RELATIONSHIP_TYPE_BASE


class CONTENT_TYPE(StrEnum):  # noqa: N801
    """
    各个部件的内容类型
    """

    # ===========================================================================================
    # OPC 标准的内容类型
    # https://hellowac.github.io/ecma-376-zh-cn/ecma-part2-refrence/#annex-e-normative-标准命名空间和媒体类型
    # ===========================================================================================

    # 核心属性部件
    CORE_PROPERTIES = 'application/vnd.openxmlformats-package.coreproperties+xml'

    # 数字签名证书部件
    DIGITAL_SIGNATURE_CERTIFICATE = 'application/vnd.openxmlformats-package.digitalsignature-certificate'

    # 数字签名起源部件
    DIGITAL_SIGNATURE_ORIGIN = 'application/vnd.openxmlformats-package.digitalsignature-origin'

    # 数字签名 XML 签名部件
    DIGITAL_SIGNATURE_XML_SIGNATURE = 'application/vnd.openxmlformats-package.digitalsignature-xmlsignature+xml'

    # 关系部件
    RELATIONSHIP = 'application/vnd.openxmlformatspackage.relationships+xml'

    # ===========================================================================================
    # PresentationML 包的内容类型(媒体类型)
    # https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-13/#131-presentationml-特定术语词汇表

    # ===========================================================================================
    # 演示文稿部件 https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-13/#1336-演示部件
    # §11.3.10

    PRESONTAION = 'application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml'
    PRESONTAION1 = 'application/vnd.openxmlformats-officedocument.presentationml.slideshow.main+xml'
    PRESONTAION2 = 'application/vnd.openxmlformats-officedocument.presentationml.template.main+xml'

    # ===========================================================================================
    # WordprocessingML 包的内容类型(媒体类型)
    # https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-11/#11310-主文档部件
    # ===========================================================================================

    WORDPROCESSING = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml'
    WORDPROCESSING1 = 'application/vnd.openxmlformats-officedocument.wordprocessingml.template.main+xml'

    # ===========================================================================================
    # SpreadsheetML 包的内容类型(媒体类型)
    # https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-12/#12-spreadsheetml
    # ===========================================================================================
    # §12.3.23

    WORKBOOK = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml'
    WORKBOOK1 = 'application/vnd.openxmlformats-officedocument.spreadsheetml.template.main+xml'

    # ===========================================================================================
    # 公共的媒体类型
    # https://www.iana.org/assignments/media-types/media-types.xhtml
    # ===========================================================================================

    JPEG = 'image/jpeg'  # jpeg
    JPG = 'image/.jpg'  # JPG
    VML = 'application/vnd.openxmlformats-officedocument.vmlDrawing'  # vml
    BIN = 'application/vnd.openxmlformats-officedocument.oleObject'  # bin
    EMF = 'image/x-emf'  # emf
    WMF = 'image/x-wmf'  # wmf
    PNG = 'image/png'  # png
    GIF = 'image/gif'  # gif
    RELS = 'application/vnd.openxmlformats-package.relationships+xml'  # rels
    XML = 'application/xml'  # xml


class NAMESPACE(StrEnum):
    """OPC XML 命名空间的常量值"""

    # ===========================================================================================
    # https://hellowac.github.io/ecma-376-zh-cn/ecma-part2-refrence/#annex-e-normative-标准命名空间和媒体类型
    # ===========================================================================================
    # 媒体类型流(内容类型)
    MEDIA_TYPES_STREAM = 'http://schemas.openxmlformats.org/package/2006/content-types'

    # 核心属性
    CORE_PROPERTIES = 'http://schemas.openxmlformats.org/package/2006/metadata/core-properties'

    # 数字签名
    DIGITAL_SIGNATURES = 'http://schemas.openxmlformats.org/package/2006/digitalsignature'

    # 关系
    RELATIONSHIP = 'http://schemas.openxmlformats.org/package/2006/relationships'


class RELATIONSHIP_TYPE(str, RELATIONSHIP_TYPE_BASE):  # noqa: N801
    """OPC 关系类型"""

    # ===========================================================================================
    # https://hellowac.github.io/ecma-376-zh-cn/ecma-part2-refrence/#annex-e-normative-标准命名空间和媒体类型
    # ===========================================================================================

    # 核心属性
    CORE_PROPERTIES = 'http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties'

    # 数字签名
    DIGITAL_SIGNATURES = 'http://schemas.openxmlformats.org/package/2006/relationships/digital-signature/signature'

    # 数字签名证书
    DIGITAL_SIGNATURE_CERTIFICATE = (
        'http://schemas.openxmlformats.org/package/2006/relationships/digital-signature/certificate'
    )

    # 数字签名起源
    DIGITAL_SIGNATURE_ORIGIN = 'http://schemas.openxmlformats.org/package/2006/relationships/digital-signature/origin'

    # 缩略图
    THUMBNAIL = 'http://schemas.openxmlformats.org/package/2006/relationships/metadata/thumbnail'

    # 参考文档: OpenXML-White-Paper.pdf
    # 包级别的主要文档关系
    OFFICE_DOCUMENT = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument'
