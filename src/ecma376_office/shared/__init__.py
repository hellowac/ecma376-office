# DML 相关的部件注册

from ecma376_office.part import PART_TYPE_MAP
from ecma376_office.shared.constants import CONTENT_TYPE as CT
from ecma376_office.shared.parts import (
    AdditionalCharacteristicsPart,
    AudioPart,
    BibliographyPart,
    ContentPart,
    CustomXMLDataStoragePart,
    CustomXMLDataStoragePropertiesPart,
    DigitalSignatureCertificatePart,
    DigitalSignatureOriginPart,
    DigitalSignatureXMLSignaturePart,
    EmbeddedControlPersistencePart,
    EmbeddedObjectPart,
    EmbeddedPackagePart,
    FilePropertiesCorePart,
    FilePropertiesCustomPart,
    FilePropertiesExtendedPart,
    FontPart,
    ImagePart,
    PrinterSettingsPart,
    ThumbnailPart,
    VideoPart,
)

PART_TYPE_MAP.update({
    # 附加特性相关
    CT.AdditionalCharacteristics: AdditionalCharacteristicsPart,
    # 音频相关
    CT.Audio: AudioPart,  # 多种多样
    CT.Audio1: AudioPart,  # 多种多样
    CT.Audio2: AudioPart,  # 多种多样
    CT.Audio3: AudioPart,  # 多种多样
    # 引用文献相关
    CT.Bibliography: BibliographyPart,
    # 内容类型相关
    CT.Content: ContentPart,  # 多种多样
    CT.Content1: ContentPart,  # 多种多样
    CT.Content2: ContentPart,  # 多种多样
    # 自定义xml数据相关
    CT.CustomXMLDataStorage: CustomXMLDataStoragePart,
    CT.CustomXMLDataStorageProperties: CustomXMLDataStoragePropertiesPart,
    # 签名证书相关
    CT.DigitalSignatureOrigin: DigitalSignatureOriginPart,
    CT.DigitalSignatureXMLSignature: DigitalSignatureXMLSignaturePart,
    CT.DigitalSignatureCertificate: DigitalSignatureCertificatePart,
    # 嵌入对象相关
    CT.EmbeddedControlPersistence: EmbeddedControlPersistencePart,
    CT.EmbeddedObject: EmbeddedObjectPart,
    CT.EmbeddedPackage: EmbeddedPackagePart,
    # 文档属性相关
    CT.ExtendedFileProperties: FilePropertiesExtendedPart,
    CT.ExtendedFileProperties1: FilePropertiesExtendedPart,
    CT.CoreFileProperties: FilePropertiesCorePart,
    CT.CustomFileProperties: FilePropertiesCustomPart,
    # 字体相关
    CT.Font: FontPart,  # 多种多样
    CT.Font1: FontPart,  # 多种多样
    CT.Font2: FontPart,  # 多种多样
    # 图片相关
    CT.Image: ImagePart,  # 多种多样
    CT.Image1: ImagePart,  # 多种多样
    CT.Image2: ImagePart,  # 多种多样
    CT.Image3: ImagePart,  # 多种多样
    CT.Image4: ImagePart,  # 多种多样
    # 打印设置相关
    CT.PrinterSettings: PrinterSettingsPart,  # 多种多样
    CT.PrinterSettings1: PrinterSettingsPart,  # 多种多样
    CT.PrinterSettings2: PrinterSettingsPart,  # 多种多样
    # 缩略图相关
    CT.Thumbnail: ThumbnailPart,  # 多种多样
    CT.Thumbnail1: ThumbnailPart,  # 多种多样
    CT.Thumbnail2: ThumbnailPart,  # 多种多样
    CT.Thumbnail3: ThumbnailPart,  # 多种多样
    CT.Thumbnail4: ThumbnailPart,  # 多种多样
    # 视频相关
    CT.Video: VideoPart,  # 多种多样
    CT.Video1: VideoPart,  # 多种多样
    CT.Video2: VideoPart,  # 多种多样
    CT.Video3: VideoPart,  # 多种多样
    CT.Video4: VideoPart,  # 多种多样
    CT.Video5: VideoPart,  # 多种多样
})
