from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Optional

from ecma376_office.dml.constants import RELATIONSHIP_TYPE as DRT
from ecma376_office.pml.constants import RELATIONSHIP_TYPE as PRT
from ecma376_office.shared.constants import RELATIONSHIP_TYPE as SRT
from ecma376_office.wml.constants import RELATIONSHIP_TYPE as WRT

if TYPE_CHECKING:
    from ecma376_office.constants import RELATIONSHIP_TYPE_BASE as RT_BASE
    from ecma376_office.dml.parts import (
        ChartDrawingPart,
        ChartPart,
        DiagramColorsPart,
        DiagramDataPart,
        DiagrameStylePart,
        DiagramLayoutDefinitionPart,
        TableStylesPart,
        ThemeOverridePart,
        ThemePart,
    )
    from ecma376_office.pml.parts import (
        CommentAuthorsPart,
        CommentsPart,
        HandoutMasterPart,
        HTMLPublishLocation,
        NotesMasterPart,
        NotesSlidePart,
        PresentaionPart,
        PresentationPropertiesPart,
        SlideLayoutPart,
        SlideMasterPart,
        SlidePart,
        SlideSynchronizationDataPart,
        SlideSynchronizationServerLocation,
        UserDefinedTagsPart,
        ViewProperitesPart,
    )
    from ecma376_office.relationship import RelationshipCollection
    from ecma376_office.shared.parts import (
        AdditionalCharacteristicsPart,
        AudioPart,
        BibliographyPart,
        ContentPart,
        CustomXMLDataStoragePart,
        CustomXMLDataStoragePropertiesPart,
        EmbeddedControlPersistencePart,
        EmbeddedObjectPart,
        FilePropertiesCustomPart,
        FilePropertiesExtendedPart,
        FontPart,
        HyperlinksPartTargetStr,
        ImagePart,
        PrinterSettingsPart,
        ThumbnailPart,
        VideoPart,
    )
    from ecma376_office.wml.parts import (
        AlternativeFormatImportPart,
        DocumentSettingsPart,
        DocumentTemplatePart,
        EndnotesPart,
        FontTablePart,
        FooterPart,
        FootnotesPart,
        GlossaryDocumentPart,
        HeaderPart,
        MailMergeDataSourcePart,
        MailMergeHeaderDataSourcePart,
        MainDocumentPart,
        NumberingDefinitionsPart,
        StyleDefinitionsPart,
        SubdocumentsPart,
        WebSettingsPart,
        XSLTransformationPart,
    )

logger = logging.getLogger(__name__)


class PartFinder:
    """
    部件加载查找类
    """

    @classmethod
    def _part_by_rt(cls, rt: RT_BASE, rels: RelationshipCollection) -> Optional[Any]:
        """
        根据关系类型获取部件(单个)
        """

        relationship = rels.get_rel_by_type(rt)

        if relationship is not None:
            return relationship.target_part

        return None

    @classmethod
    def _part_by_rt_id(cls, rt: RT_BASE, rels: RelationshipCollection, rid: str) -> Optional[str | Any]:
        """
        根据关系类型和ID获取单个部件
        """

        relationship = rels.get_rel_by_type_and_id(rt, rid)

        if relationship is not None:
            if relationship.is_external:
                # logger.warning(f"外部资源: {relationship.target_part}")
                return relationship.target

            return relationship.target_part

        return None

    @classmethod
    def _part_require_by_rt(cls, rt: RT_BASE, rels: RelationshipCollection, rid: Optional[str] = None) -> Any:
        """
        根据关系类型获取部件(单个) 必须
        """

        part = cls._part_by_rt_id(rt, rels, rid) if rid is not None else cls._part_by_rt(rt, rels)

        if part is None:
            msg = f'获取部件失败: {rt = }'
            raise ValueError(msg)

        return part

    @classmethod
    def _parts_by_rt(cls, rt: RT_BASE, rels: RelationshipCollection) -> list[Any]:
        """
        根据关系类型获取部件(多个)
        """

        relationships = rels.get_rels_by_type(rt)

        return [relationship.target_part for relationship in relationships]


class SharedPartFinder(PartFinder):
    """
    15章 贡献部件的集合

    其中主要包括:

    - Additional Characteristics 附加特性部件
    - Bibliography 参考文献部件
    - Custom XML Data Storage Properties 自定义xml数据存储属性
    - File Properties, Extended 文件的扩展属性【这里文件指xxx.pptx/word/xlsx文件】
    - File Properties, Core 文件的核心属性【这里文件指xxx.pptx/word/xlsx文件】
    - File Properties, Custom 文件的自定义属性【这里文件指xxx.pptx/word/xlsx文件】
    """

    @classmethod
    def additional_characteristics(cls, rels: RelationshipCollection):
        """
        15.2.1 附加特性部件

        当无法使用 ECMA-376 定义的元素指定特征信息时，
        此部件类型的实例包含有关生成文档的生产者的附加特征的信息。

        包允许包含零个或一个附加特征部件
        """
        # logger.info(f"{self._relationship_collect =}")

        part: Optional[AdditionalCharacteristicsPart] = PartFinder._part_by_rt(SRT.AdditionalCharacteristics, rels)

        return part

    @classmethod
    def audio(cls, rels: RelationshipCollection):
        """
        15.2.2 音频部件

        此部件类型的实例应包含一个音频文件。

        一些示例内容类型是:

        - audio/aiff http://developer.apple.com/documentation/QuickTime/INMAC/SOUND/imsoundmgr.30.htm
        - audio/midi http://www.midi.org/about-midi/specinfo.shtml
        - audio/ogg http://xiph.org/vorbis/doc/Vorbis_I_spec.html
        - audio/mpeg ISO/IEC 11172-3

        允许 PresentationML 包包含零个或多个音频部件，每个部件都应是讲义母版（[§13.3.3]）、笔记幻灯片（[§13.3.5]）、笔记母版（[§13.3.4]）中关系的目标、幻灯片 ([§13.3.8])、幻灯片布局 ([§13.3.9]) 或幻灯片母版 ([§13.3.10]) 部件的关系项。
        """

        part: list[AudioPart] = cls._parts_by_rt(SRT.Audio, rels)

        return part

    @classmethod
    def audio_one(cls, rels: RelationshipCollection, rid: str):
        """
        15.2.2 音频部件

        此部件类型的实例应包含一个音频文件。

        一些示例内容类型是:

        - audio/aiff http://developer.apple.com/documentation/QuickTime/INMAC/SOUND/imsoundmgr.30.htm
        - audio/midi http://www.midi.org/about-midi/specinfo.shtml
        - audio/ogg http://xiph.org/vorbis/doc/Vorbis_I_spec.html
        - audio/mpeg ISO/IEC 11172-3

        允许 PresentationML 包包含零个或多个音频部件，每个部件都应是讲义母版（[§13.3.3]）、笔记幻灯片（[§13.3.5]）、笔记母版（[§13.3.4]）中关系的目标、幻灯片 ([§13.3.8])、幻灯片布局 ([§13.3.9]) 或幻灯片母版 ([§13.3.10]) 部件的关系项。
        """

        part: Optional[str | AudioPart] = cls._part_by_rt_id(SRT.Audio, rels, rid)

        return part

    @classmethod
    def bibliography(cls, rels: RelationshipCollection):
        """
        15.2.3 参考文献部件

        此部件类型的实例包含当前包的书目数据。

        一个包允许包含零个或一个参考书目部件，并且每个此类部件应是 WordprocessingML 包中主文档 ([§11.3.10]) 部件中隐式关系的目标；

        SpreadsheetML 包中的工作簿 ([§12.3.23]) 部件； 或讲义母版 ([§13.3.3])、笔记母版 ([§13.3.4])、笔记幻灯片 ([§13.3.5])、幻灯片 ([§13.3.8])、幻灯片布局 ([§ 13.3.9])，或PresentationML包中的幻灯片母版（[§13.3.10]）部件。
        """

        part: Optional[BibliographyPart] = cls._part_by_rt(SRT.Bibliography, rels)

        return part

    @classmethod
    def content(cls, rels: RelationshipCollection):
        """
        15.2.4 内容部件

        此部件类型的实例可以包含 ECMA-376 未定义的格式的 XML 标记。

        包允许包含零个或多个内容部件，并且每个此类部件应成为

        - 注释 ([§11.3.2])、
        - 尾注 ([§11.3.4])、
        - 页脚 ([§11.3.6])、
        - 脚注（[§11.3.7]）、
        - 术语表文档（[§11.3.8]）、
        - 标题([§11.3.9]), 或
        - WordprocessingML 包中主文档（[§11.3.10]）部件、
        - SpreadsheetML 包中的绘图 ([§12.3.8]) 部件； 或
        - 讲义母版 ([§13.3.3])、
        - 笔记幻灯片 ([§13.3.5])、
        - 笔记母版 ([§13.3.4])、
        - 幻灯片 ([§13.3.8])、
        - 幻灯片布局([§ 13.3.9])，或
        - PresentationML包中的幻灯片母版（[§13.3.10]）

        等等这些部件的显式关系的目标
        """

        part: list[ContentPart] = cls._parts_by_rt(SRT.Content, rels)

        return part

    @classmethod
    def custom_xml_data_storage(cls, rels: RelationshipCollection):
        """
        15.2.5 自定义XML数据存储部件

        该部件类型的实例可以包含任意 XML。 因此，此部件的实例可用于通过此包往返任意自定义 XML 数据。

        包允许包含一个或多个自定义 XML 数据存储部件，

        并且每个此类部件应是 WordprocessingML 包中主文档 ([§11.3.10]) 部件中隐式关系的目标； SpreadsheetML 包中的工作簿 ([§12.3.23]) 部件； 或讲义母版 ([§13.3.3])、笔记母版 ([§13.3.4])、笔记幻灯片 ([§13.3.5])、演示文稿 ([§13.3.6])、幻灯片([§13.3.8])、幻灯片布局（[§13.3.9]）或 PresentationML 包中的幻灯片母版（[§13.3.10]）部件。
        """

        part: list[CustomXMLDataStoragePart] = cls._parts_by_rt(SRT.CustomXMLDataStorage, rels)

        return part

    @classmethod
    def custom_xml_data_storage_pr(cls, rels: RelationshipCollection):
        """
        15.2.6 自定义 XML 数据存储属性部件

        此部件类型的实例包含为此自定义 XML 数据指定的属性集。
        这些属性由存储的唯一 ID 以及有关此自定义 XML 数据存储所使用的 XML Schema 集的信息组成。

        包允许包含零个或多个自定义 XML 数据存储属性部件，并且每个此类部件应是自定义 XML 数据存储（[§15.2.4]）部件的隐式关系的目标。
        """

        part: list[CustomXMLDataStoragePropertiesPart] = cls._parts_by_rt(SRT.CustomXMLDataStorageProperties, rels)

        return part

    @classmethod
    def digital_signature_origin(cls, rels: RelationshipCollection):
        """
        15.2.7 数字签名源部件

        该部件内容设计数字签名，目前未涉及，且章节应为第二部分的 §10.4.2 节，详细信息参考原文档/文件.
        """

        return None

    @classmethod
    def digital_signature_xml_signature(cls, rels: RelationshipCollection):
        """
        15.2.8 数字签名 XML 签名部件

        该部件内容设计数字签名，目前未涉及，且章节应为第二部分的§10.4.3 节，详细信息参考原文档/文件.
        """

        return None

    @classmethod
    def embedded_control_persistence(cls, rels: RelationshipCollection):
        """
        15.2.9 嵌入式控制持久化部件

        该部件的实例包含有关包中嵌入控件的信息。 当要求保留时，此信息由指定的控件提供。

        例如:

        应用程序可以利用嵌入式对象服务器技术 KParts 或 Bonobo 来使用该部件存储嵌入式对象。

        一个包允许包含一个或多个嵌入式控制持久性部件，并且每个此类部件应成为 WordprocessingML 包中的

        - 尾注 ([§11.3.4])、
        - 页脚 ([§11.3.6])、
        - 脚注 ([§11.3.7])、
        - 标题 ([§11.3.9]) 或
        - 主文档 ([§11.3.10]) 等等部件中显式关系项的目标；

        或者 SpreadsheetML 包中的

        - 工作表部件 ([§12.3.24])；

        或者 PresentationML 包中的

        - 讲义母版 ([§13.3.3])、
        - 笔记幻灯片 ([§13.3.5])、
        - 笔记母版 ([§13.3.4])、
        - 幻灯片 ([§13.3.8])、
        - 幻灯片布局 ([§13.3.9])、
        - 幻灯片母版 ([§13.3.10]) 等等部件的关系项。

        该部件的内容类型决定了嵌入控件的格式和内容。
        """


        part: list[EmbeddedControlPersistencePart] = cls._parts_by_rt(SRT.EmbeddedControlPersistence, rels)

        return part

    @classmethod
    def embedded_object(cls, rels: RelationshipCollection):
        """
        此部件类型的实例可以包含由任何嵌入对象服务器生成的嵌入对象.

        包允许包含零个或多个嵌入式对象部件，并且每个此类部件可能是 WordprocessingML 包中

        -注释 ([§11.3.2])、
        -尾注 ([§11.3.4])、
        -页脚 ([§11.3.6])、
        -脚注 ([§11.3.7])、
        -页眉 ([§11.3.9])、
        -主文档 ([§11.3.10]) 等等部件；

        或 SpreadsheetML 包中的

        -工作表 ([§12.3.24])部件；

        或 PresentationML 包中的

        - 讲义母版 ([§13.3.3])、
        - 笔记幻灯片 ([§13.3.5])、
        - 笔记母版 ([§13.3.4])、
        - 幻灯片 ([§13.3.8])、
        - 幻灯片布局 ([§13.3.9])、
        - 幻灯片母版 ([§13.3.10])部件。

        等的显示关系目标（target of an explicit relationship）。

        WordprocessingML 文档包允许包含零个或多个嵌入对象部件，每个部件都应是主文档部件关系项中关系的目标。 每个嵌入对象部件应有一个关联的图像，该图像作为相应嵌入对象的占位符出现在文档中。
        """


        part: list[EmbeddedObjectPart] = cls._parts_by_rt(SRT.EmbeddedObject, rels)

        return part

    @classmethod
    def embedded_package(cls, rels: RelationshipCollection):
        """
        15.2.11 嵌入包部件

        此部件类型的实例包含完整的包。 例如，WordprocessingML 文档可能包含 SpreadsheetML 或PresentationML 文档，在这种情况下，WordprocessingML 文档包将包含定义该 SpreadsheetML 或 PresentationML 文档的嵌入包部件。

        包允许包含零个或多个嵌入式包部件，并且每个此类部件应是如下部件的显式关系的目标，包括：

        WordprocessingML 包中的

        - Chart ([§14.2.1]),
        - Comments ([§11.3.2]),
        - Endnotes ([§11.3.4]),
        - Footer ([§11.3.6]),
        - Footnotes ([§11.3.7]),
        - Header ([§11.3.9]), 或
        - Main Document ([§11.3.10]) 部件；

        SpreadsheetML 包中的

        - Chart ([§14.2.1])
        - Worksheet ([§12.3.24]) 部件;

        PresentationML 包中的

        - Chart ([§14.2.1]),
        - Handout Master ([§13.3.3]),
        - Notes Slide ([§13.3.5]),
        - Notes Master ([§13.3.4]),
        - Slide ([§13.3.8]),
        - Slide Layout ([§13.3.9]),
        - Slide Master ([§13.3.10]) 部件;
        """


        part: list[EmbeddedObjectPart] = cls._parts_by_rt(SRT.EmbeddedObject, rels)

        return part

    @classmethod
    def file_custom_pr(cls, rels: RelationshipCollection):
        """
        15.2.12.2 自定义文件属性部件

        此部件的实例包含适用于包的自定义文件属性的名称、它们的值以及这些值的类型。 自定义文件属性可能是为其准备文档的客户的名称、发生某些事件的日期/时间、文档编号或某些布尔状态标志。

        一个包最多应包含一个自定义文件属性部件，并且该部件应是文档的包关系项中关系的目标。
        """


        part: Optional[FilePropertiesCustomPart] = cls._part_by_rt(SRT.CustomFileProperties, rels)

        if part is None:
            part = cls._part_by_rt(SRT.CustomFileProperties1, rels)

        return part

    @classmethod
    def file_extended_pr(cls, rels: RelationshipCollection):
        """
        15.2.12.3 扩展文件属性部件

        该部件的实例包含特定于 Office Open XML 文档的属性。

        一个包最多应包含一个扩展文件属性部件，并且该部件应是文档的包关系项(/_rels/.rels)中关系的目标。
        """


        part: Optional[FilePropertiesExtendedPart] = cls._part_by_rt(SRT.ExtendedFileProperties, rels)

        if part is None:
            part = cls._part_by_rt(SRT.ExtendedFileProperties1, rels)

        if part is None:
            msg = '获取扩展属性失败, 请检查关系类型(relationship type)'
            raise ValueError(msg)

        return part

    @classmethod
    def font(cls, rels: RelationshipCollection):
        """
        15.2.13 字体部件

        此部件类型的实例包含直接嵌入到文档中的给定字体。 （当使用自定义字体或未广泛分发的字体时，这非常有用。）

        包应包含零个或多个字体部件，对于每个存在的部件，该部件应是字体表(Font Table)（[§11.3.5]）或演示（[§13.3.6]）部件中显式关系的目标 。
        """


        parts: list[FontPart] = cls._parts_by_rt(SRT.Font, rels)

        return parts

    @classmethod
    def image(cls, rels: RelationshipCollection):
        """
        15.2.14 图片部件

        图像可以作为 ZIP 项存储在包中。 图像 ZIP 项应通过图像部件关系和适当的内容类型来标识。

        一个包允许包含零个或多个图像部件，并且每个此类部件应成为以下部件的显示关系目录, 如下:

        WordprocessingML 包中的

        - Comments ([§11.3.2]),
        - Endnotes ([§11.3.4]),
        - Footer ([§11.3.6]),
        - Footnotes ([§11.3.7]),
        - Header ([§11.3.9]),
        - Drawing ([§12.3.8]),
        - Main Document ([§11.3.10])

        PresentationML 包中的

        - Handout Master ([§13.3.3]),
        - Notes Slide ([§13.3.5]),
        - Notes Master ([§13.3.4]),
        - Slide ([§13.3.8]),
        - Slide Layout ([§13.3.9]),
        - Slide Master ([§13.3.10]).

        """


        part: list[ImagePart] = cls._parts_by_rt(SRT.Image, rels)

        return part

    @classmethod
    def image_one(cls, rels: RelationshipCollection, rid: str):
        """
        15.2.14 图片部件

        图像可以作为 ZIP 项存储在包中。 图像 ZIP 项应通过图像部件关系和适当的内容类型来标识。

        一个包允许包含零个或多个图像部件，并且每个此类部件应成为以下部件的显示关系目录, 如下:

        WordprocessingML 包中的

        - Comments ([§11.3.2]),
        - Endnotes ([§11.3.4]),
        - Footer ([§11.3.6]),
        - Footnotes ([§11.3.7]),
        - Header ([§11.3.9]),
        - Drawing ([§12.3.8]),
        - Main Document ([§11.3.10])

        PresentationML 包中的

        - Handout Master ([§13.3.3]),
        - Notes Slide ([§13.3.5]),
        - Notes Master ([§13.3.4]),
        - Slide ([§13.3.8]),
        - Slide Layout ([§13.3.9]),
        - Slide Master ([§13.3.10]).

        """


        part: Optional[str | ImagePart] = cls._part_by_rt_id(SRT.Image, rels, rid)

        return part

    @classmethod
    def printer_settings(cls, rels: RelationshipCollection):
        """
        15.2.15 打印机设置部件

        此部件类型的实例包含有关打印机或显示设备的初始化和环境的信息。 该信息的布局是应用程序定义的。

        SpreadsheetML 包允许每个图表(Chartsheet)、对话框表(Dialogsheet)或工作表(Worksheet)部件最多包含一个打印机设置部件，并且该部件应是图表(Chartsheet) ([§12.3.2])、、对话框表(Dialogsheet) ([§12.3.7]) 或工作表(Worksheet) ([§12.3.24]) 部件中隐式关系的目标。

        WordprocessingML 包允许包含零个或多个打印机设置部件，每个 sectPr 元素(Element)一个，每个部件都是来自主文档 ([§11.3.10]) 或词汇表文档 ([§11.3.8]) 部件的显式关系的目标 。

        一个 PresentationML 包最多允许包含一个打印机设置部件，并且该部件应是来自 Presentation ([§13.3.6]) 部件的隐式关系的目标。
        """


        part: list[PrinterSettingsPart] = cls._parts_by_rt(SRT.Image, rels)

        return part

    @classmethod
    def thumbnail(cls, rels: RelationshipCollection):
        """
        15.2.16 缩略图部件

        为了帮助最终用户识别包的各个部件或整个包，可以将称为缩略图的图像存储在该包中。 每个缩略图图像均由包制作者生成，并作为 ZIP 项目存储在包中。 生成的缩略图的大小没有限制，应用程序可以根据需要自由缩放图像。

        缩略图 ZIP 项应由包关系项目或部件关系项来标识。 包不得包含多个与整个包关联的缩略图关系，或者每个包部件不得包含多个缩略图关系。
        """


        part: Optional[ThumbnailPart] = cls._part_by_rt(SRT.Thumbnail, rels)

        if part is None:
            part = cls._part_by_rt(SRT.Thumbnail1, rels)

        if part is None:
            msg = '获取缩略图失败, 检查关系类型(relationship type)'
            raise ValueError(msg)

        return part

    @classmethod
    def video(cls, rels: RelationshipCollection):
        """
        15.2.17 视频部件

        此部件类型的实例包含视频文件。

        PresentationML 包允许包含零个或多个视频部件，每个部件都应是

        - Handout Master ([§13.3.3]),
        - Notes Slide ([§13.3.5]),
        - Notes Master ([§13.3.4]),
        - Slide ([§13.3.8]),
        - Slide Layout ([§13.3.9]),
        - Slide Master ([§13.3.10])

        等等部件的显式关系的目标.

        WordprocessingML 包允许包含零个或多个视频部件，每个部件都应是

        - Comments ([§11.3.2]),
        - Endnotes ([§11.3.4]),
        - Footer ([§11.3.6]),
        - Footnotes ([§11.3.7]),
        - Header ([§11.3.9]),
        - Main Document ([§11.3.10])

        等等部件的显式关系的目标.
        """


        parts: list[VideoPart] = cls._parts_by_rt(SRT.Video, rels)

        return parts

    @classmethod
    def video_one(cls, rels: RelationshipCollection, rid: str):
        """
        15.2.17 视频部件

        此部件类型的实例包含视频文件。

        PresentationML 包允许包含零个或多个视频部件，每个部件都应是

        - Handout Master ([§13.3.3]),
        - Notes Slide ([§13.3.5]),
        - Notes Master ([§13.3.4]),
        - Slide ([§13.3.8]),
        - Slide Layout ([§13.3.9]),
        - Slide Master ([§13.3.10])

        等等部件的显式关系的目标.

        WordprocessingML 包允许包含零个或多个视频部件，每个部件都应是

        - Comments ([§11.3.2]),
        - Endnotes ([§11.3.4]),
        - Footer ([§11.3.6]),
        - Footnotes ([§11.3.7]),
        - Header ([§11.3.9]),
        - Main Document ([§11.3.10])

        等等部件的显式关系的目标.
        """

        part: Optional[VideoPart | str] = cls._part_by_rt_id(SRT.Video, rels, rid)

        return part

    @classmethod
    def hyperlinks(cls, rels: RelationshipCollection):
        """
        15.3 超链接

        超链接可以作为关系存储在包中。 超链接应通过包含指定给定超链接的目的地的目标来标识。

        超链接目标可以位于包含关系部件的包内部或外部（从语法上表达，关系元素的 TargetMode 属性可以是Internal或External）。
        """


        part: list[HyperlinksPartTargetStr] = cls._parts_by_rt(SRT.Hyperlinks, rels)

        return part

    @classmethod
    def hyperlink_one(cls, rels: RelationshipCollection, rid: str):
        """
        15.3 超链接

        超链接可以作为关系存储在包中。 超链接应通过包含指定给定超链接的目的地的目标来标识。

        超链接目标可以位于包含关系部件的包内部或外部（从语法上表达，关系元素的 TargetMode 属性可以是Internal或External）。
        """


        target_str: Optional[str | HyperlinksPartTargetStr] = cls._part_by_rt_id(SRT.Hyperlinks, rels, rid)

        return target_str


class DMLPartFinder(PartFinder):
    """
    8.7.1 DrawingML

    该Finder 查找与元素绘制、定位、外观相关的部件以及定义。

    - DrawingML 指定包中绘图元素的位置和外观。
    - DrawingML 还指定包中图表的位置和外观。 图表部件的根元素是图表，并指定图表在文档中此位置的外观。
    - 此外，DrawingML 指定包范围的外观特征，例如包的主题。 文档的主题指定配色方案、字体和效果，文档的各个部件（例如文本、绘图、图表和图表）可以引用这些主题，以创建一致的视觉表示。

    以及 14章 部件概览

    本节中定义的关系项和部件由 WordprocessingML ([§11])、SpreadsheetML ([§12]) 和PresentationML ([§13]) 环境中的一个或多个使用。

    其中主要包括:

    - Chart 图表
    - Chart Drawing 图表绘制
    - Diagram Colors 图表颜色
    - Diagram Data 图表数据
    - Diagram Layout Definition 图表布局定义
    - Diagram Style 图表样式
    - Theme 主题
    - Theme Override 主题覆盖
    - Table Styles 表格样式
    """

    @classmethod
    def chart(cls, rels: RelationshipCollection):
        """
        14.2.1 图表部件

        此部件类型的实例描述了一个图表。

        包应包含文档中每个图表的图表部件。

        在 WordprocessingML 文档中，每个此类部件应是主文档 ([§11.3.10]) 部件中显式关系的目标。

        在 SpreadsheetML 文档中，每个此类部件应是绘图 ([§12.3.8]) 部件中显式关系的目标。

        在 PresentationML 文档中，每个这样的部件应是讲义母版（[§13.3.3]）、注释母版（[§13.3.4]）、注释幻灯片（[§13.3.5]）中显式关系的目标 、幻灯片 ([§13.3.8])、幻灯片布局 ([§13.3.9]) 或幻灯片母版 ([§13.3.10]) 部件。

        如果指向此图表绘图部件的图表是图表表部件中关系的目标，则也允许此部件作为图表绘图 ([§14.2.2]) 部件中显式关系的目标。 换句话说，图表可以嵌入另一个图表, 唯一的限制是父级图表需是 chartsheet 的部件。
        """


        part: list[ChartPart] = PartFinder._parts_by_rt(DRT.Chart, rels)

        return part

    @classmethod
    def chart_one(cls, rels: RelationshipCollection, rid: str):
        """
        14.2.1 图表部件

        此部件类型的实例描述了一个图表。

        包应包含文档中每个图表的图表部件。

        在 WordprocessingML 文档中，每个此类部件应是主文档 ([§11.3.10]) 部件中显式关系的目标。

        在 SpreadsheetML 文档中，每个此类部件应是绘图 ([§12.3.8]) 部件中显式关系的目标。

        在 PresentationML 文档中，每个这样的部件应是讲义母版（[§13.3.3]）、注释母版（[§13.3.4]）、注释幻灯片（[§13.3.5]）中显式关系的目标 、幻灯片 ([§13.3.8])、幻灯片布局 ([§13.3.9]) 或幻灯片母版 ([§13.3.10]) 部件。

        如果指向此图表绘图部件的图表是图表表部件中关系的目标，则也允许此部件作为图表绘图 ([§14.2.2]) 部件中显式关系的目标。 换句话说，图表可以嵌入另一个图表, 唯一的限制是父级图表需是 chartsheet 的部件。
        """


        part: ChartPart = PartFinder._part_require_by_rt(DRT.Chart, rels, rid)

        return part

    @classmethod
    def chart_drawing(cls, rels: RelationshipCollection):
        """
        14.2.2 图表绘制部件

        此部件类型的实例包含与此图表显式关联的所有基本绘图元素（形状）。 当移动图表时，这些绘图元素会自动随图表一起移动，并在调整图表大小时调整其大小。

        包允许每个图表部件包含一个图表绘图部件，并且每个此类部件应是图表 ([§14.2.1]) 部件的显式关系的目标。
        """


        parts: list[ChartDrawingPart] = PartFinder._parts_by_rt(DRT.ChartDrawing, rels)

        return parts

    @classmethod
    def diagrame_colors(cls, rels: RelationshipCollection):
        """
        14.2.3 绘制颜色部件

        此部件类型的实例包含图表的颜色信息。

        包中每个图表应包含一个图表颜色部件。

        每个图表颜色部件应是 WordprocessingML 主文档 ([§11.3.10])、SpreadsheetML 绘图 ([§12.3.8]) 或PresentationML Slide ([§13.3.8]) 部件中显式关系的目标。
        """


        parts: list[DiagramColorsPart] = PartFinder._parts_by_rt(DRT.DiagramColors, rels)

        return parts

    @classmethod
    def diagrame_colors_one(cls, rels: RelationshipCollection, rid: str):
        """
        14.2.3 绘制颜色部件

        此部件类型的实例包含图表的颜色信息。

        包中每个图表应包含一个图表颜色部件。

        每个图表颜色部件应是 WordprocessingML 主文档 ([§11.3.10])、SpreadsheetML 绘图 ([§12.3.8]) 或PresentationML Slide ([§13.3.8]) 部件中显式关系的目标。
        """


        part: DiagramColorsPart = PartFinder._part_require_by_rt(DRT.DiagramColors, rels)

        return part

    @classmethod
    def diagrame_data(cls, rels: RelationshipCollection):
        """
        14.2.4 绘制数据部件

        此部件类型的实例包含图表的语义数据。

        包中每个图表应包含一个图表数据部件。

        每个图表数据部件应是 WordprocessingML 主文档 ([§11.3.10]) 中显式关系的目标；

        SpreadsheetML 绘图部件（[§12.3.8]）； 或 PresentationML Handout Master ([§13.3.3])、Notes Master ([§13.3.4])、Notes Slide ([§13.3.5])、Slide ([§13.3.8])、Slide Layout （[ §13.3.9]），或幻灯片母版（[§13.3.10]）部件。
        """


        parts: list[DiagramDataPart] = PartFinder._parts_by_rt(DRT.DiagramData, rels)

        return parts

    @classmethod
    def diagrame_data_one(cls, rels: RelationshipCollection, rid: str):
        """
        14.2.4 绘制数据部件

        此部件类型的实例包含图表的语义数据。

        包中每个图表应包含一个图表数据部件。

        每个图表数据部件应是 WordprocessingML 主文档 ([§11.3.10]) 中显式关系的目标；

        SpreadsheetML 绘图部件（[§12.3.8]）； 或 PresentationML Handout Master ([§13.3.3])、Notes Master ([§13.3.4])、Notes Slide ([§13.3.5])、Slide ([§13.3.8])、Slide Layout （[ §13.3.9]），或幻灯片母版（[§13.3.10]）部件。
        """


        part: DiagramDataPart = PartFinder._part_require_by_rt(DRT.DiagramData, rels, rid)

        return part

    @classmethod
    def diagrame_layout_definition(cls, rels: RelationshipCollection):
        """
        14.2.5 绘制布局定义部件

        此部件类型的一个实例是一个模板，用于描述如何将与图表相关的数据映射到形状。

        包中的每个图表应包含一个图表布局定义部件。

        每个布局定义部件应是 WordprocessingML 主文档 ([§11.3.10]) 中显式关系的目标；
        SpreadsheetML 绘图部件（[§12.3.8]）；
        或 PresentationML Handout Master ([§13.3.3])、Notes Master (§13.3.4)、Notes Slide ([§13.3.5])、Slide ([§13.3.8])、Slide Layout (§13.3)。 9) 或幻灯片母版 ([§13.3.10]) 部件。

        如果文档包含多个具有相同图形布局定义的图表，则每个图表都应具有其自己的该图表布局定义部件的副本。
        """


        parts: list[DiagramLayoutDefinitionPart] = PartFinder._parts_by_rt(DRT.DiagramLayoutDefinition, rels)

        return parts

    @classmethod
    def diagrame_layout_definition_one(cls, rels: RelationshipCollection, rid: str):
        """
        14.2.5 绘制布局定义部件

        此部件类型的一个实例是一个模板，用于描述如何将与图表相关的数据映射到形状。

        包中的每个图表应包含一个图表布局定义部件。

        每个布局定义部件应是 WordprocessingML 主文档 ([§11.3.10]) 中显式关系的目标；
        SpreadsheetML 绘图部件（[§12.3.8]）；
        或 PresentationML Handout Master ([§13.3.3])、Notes Master (§13.3.4)、Notes Slide ([§13.3.5])、Slide ([§13.3.8])、Slide Layout (§13.3)。 9) 或幻灯片母版 ([§13.3.10]) 部件。

        如果文档包含多个具有相同图形布局定义的图表，则每个图表都应具有其自己的该图表布局定义部件的副本。
        """


        part: DiagramLayoutDefinitionPart = PartFinder._part_require_by_rt(DRT.DiagramLayoutDefinition, rels, rid)

        return part

    @classmethod
    def diagrame_style(cls, rels: RelationshipCollection):
        """
        14.2.6 绘制样式部件

        此部件类型的实例将图表语义信息映射到文档的主题。

        包中每个图表应包含一个图表样式部件。

        每个样式部件应是 WordprocessingML 主文档 ([§11.3.10]) 中显式关系的目标；
        SpreadsheetML 绘图部件（[§12.3.8]）； 或 PresentationML Handout Master ([§13.3.3])、Notes Master ([§13.3.4])、Notes Slide ([§13.3.5])、Slide ([§13.3.8])、Slide Layout ([ §13.3.9])，或幻灯片母版（[§13.3.10]）部件。
        """


        parts: list[DiagrameStylePart] = PartFinder._parts_by_rt(DRT.DiagrameStyle, rels)

        return parts

    @classmethod
    def diagrame_style_one(cls, rels: RelationshipCollection, rid: str):
        """
        14.2.6 绘制样式部件

        此部件类型的实例将图表语义信息映射到文档的主题。

        包中每个图表应包含一个图表样式部件。

        每个样式部件应是 WordprocessingML 主文档 ([§11.3.10]) 中显式关系的目标；
        SpreadsheetML 绘图部件（[§12.3.8]）； 或 PresentationML Handout Master ([§13.3.3])、Notes Master ([§13.3.4])、Notes Slide ([§13.3.5])、Slide ([§13.3.8])、Slide Layout ([ §13.3.9])，或幻灯片母版（[§13.3.10]）部件。
        """


        part: DiagrameStylePart = PartFinder._part_require_by_rt(DRT.DiagrameStyle, rels, rid)

        return part

    @classmethod
    def theme(cls, rels: RelationshipCollection):
        """
        14.2.7 主题部件

        此部件类型的实例包含有关文档主题的信息，该主题是配色方案、字体方案和格式方案（后者也称为效果）的组合。

        对于 WordprocessingML 文档，主题的选择会影响标题的颜色和样式等。

        对于 SpreadsheetML 文档，主题的选择会影响单元格内容和图表的颜色和样式等。

        对于 PresentationML 文档，主题的选择会通过关联的母版影响幻灯片、讲义和笔记的格式等。

        WordprocessingML 或 SpreadsheetML 包应包含零个或一个主题部件，该部件应是主文档 (§11.3.10) 或工作簿 ([§12.3.23]) 部件中隐式关系的目标。

        每个讲义母版 ([§13.3.3])、笔记母版 ([§13.3.4])、幻灯片母版 ([§13.3.10]) 或演示文稿 (§13.3.6) 的 PresentationML 包应通过隐式关系包含零个或一个主题部件 ）部件。
        """


        parts: list[ThemePart] = PartFinder._parts_by_rt(DRT.Theme, rels)

        return parts

    @classmethod
    def theme_one(cls, rels: RelationshipCollection):
        """
        14.2.7 主题部件

        此部件类型的实例包含有关文档主题的信息，该主题是配色方案、字体方案和格式方案（后者也称为效果）的组合。

        对于 WordprocessingML 文档，主题的选择会影响标题的颜色和样式等。

        对于 SpreadsheetML 文档，主题的选择会影响单元格内容和图表的颜色和样式等。

        对于 PresentationML 文档，主题的选择会通过关联的母版影响幻灯片、讲义和笔记的格式等。

        WordprocessingML 或 SpreadsheetML 包应包含零个或一个主题部件，该部件应是主文档 (§11.3.10) 或工作簿 ([§12.3.23]) 部件中隐式关系的目标。

        每个讲义母版 ([§13.3.3])、笔记母版 ([§13.3.4])、幻灯片母版 ([§13.3.10]) 或演示文稿 (§13.3.6) 的 PresentationML 包应通过隐式关系包含零个或一个主题部件 ）部件。
        """


        part: Optional[ThemePart] = PartFinder._part_by_rt(DRT.Theme, rels)

        return part

    @classmethod
    def theme_override(cls, rels: RelationshipCollection):
        """
        14.2.8 主题覆盖部件

        此部件类型的实例包含有关对象主题覆盖的信息，这些信息覆盖特定幻灯片、笔记幻灯片或讲义的配色方案、字体方案和格式方案（后者也称为效果）。

        PresentationML 包应通过隐式关系为每个 Notes Slide ([§13.3.5])、Slide ([§13.3.8]) 或 Slide Layout ([§13.3.9]) 部件包含零个或一个主题覆盖部件。
        """


        parts: list[ThemeOverridePart] = PartFinder._parts_by_rt(DRT.ThemeOverride, rels)

        return parts

    @classmethod
    def theme_override_one(cls, rels: RelationshipCollection):
        """从相关rels中获取一个主题覆盖部件

        14.2.8 主题覆盖部件

        此部件类型的实例包含有关对象主题覆盖的信息，这些信息覆盖特定幻灯片、笔记幻灯片或讲义的配色方案、字体方案和格式方案（后者也称为效果）。

        PresentationML 包应通过隐式关系为每个 Notes Slide ([§13.3.5])、Slide ([§13.3.8]) 或 Slide Layout ([§13.3.9]) 部件包含零个或一个主题覆盖部件。
        """


        parts: Optional[ThemeOverridePart] = PartFinder._part_by_rt(DRT.ThemeOverride, rels)

        return parts

    @classmethod
    def table_style(cls, rels: RelationshipCollection):
        """
        14.2.8 主题覆盖部件

        此部件类型的实例包含有关此演示文稿中的表格所使用的表格样式的信息。 表格样式定义行和列颜色、标题行颜色和文本等特征。

        通过隐式关系，PresentationML 包中的每个演示文稿 ([§13.3.6]) 部件不得包含超过一个表格样式部件。
        """


        part: Optional[TableStylesPart] = PartFinder._part_by_rt(DRT.TableStyles, rels)

        return part


class WMLPartFinder(PartFinder):
    """
    11. WordprocessingML

    该Finder 查找与word包相关的部件

    - Alternative Format Import （替代格式导入）
    - Comments （注解/注释）
    - Document Settings（文档设置）
    - Endnotes (尾注 )
    - Font Table (字体表 )
    - Footer (页脚)
    - Footnotes (脚注)
    - Glossary Document (术语表文档 )
    - Header (标头)
    - Main Document (主文档 )
    - Numbering Definitions (编号定义 )
    - Style Definitions (样式定义 )
    - Web Settings (网页设置 )
    """

    @classmethod
    def alternative_format_import(cls, rels: RelationshipCollection):
        """
        11.3.1 替代格式导入部件

        替代格式导入部件允许将在上述指定的替代格式中指定的内容直接嵌入到WordprocessingML文档中，以便将该内容迁移到WordprocessingML格式。

        任何允许包含p元素的文档部件也可以包含一个altChunk元素，其id属性引用一个关系。该关系应指向包中的一个部件，该部件包含要导入到此WordprocessingML文档中的内容。
        """


        part: Optional[AlternativeFormatImportPart] = PartFinder._part_by_rt(WRT.AlternativeFormatImport, rels)

        return part

    @classmethod
    def comments(cls, rels: RelationshipCollection):
        """
        11.3.2 注释/注解部件

        该部件类型的一个实例包含文档中每个注释的信息。

        一个包不应包含超过两个注释部件。如果存在，该部件的一个实例应是主文档（[§11.3.10]）部件的隐式关系对象，另一个部件应是词汇表文档（[§11.3.8]）部件的隐式关系对象。
        """


        part: Optional[CommentsPart] = PartFinder._part_by_rt(WRT.Comments, rels)

        return part

    @classmethod
    def document_settings(cls, rels: RelationshipCollection):
        """
        11.3.3 文档设置部件

        该部件类型的实例包含了文档的所有属性设置。

        一个包中不得包含超过两个文档设置部件。如果存在，其中一个实例应该是主文档（[§11.3.10]）部件隐式关系的目标，另一个实例应该是词汇表文档（[§11.3.8]）部件隐式关系的目标。
        """


        part: Optional[DocumentSettingsPart] = PartFinder._part_by_rt(WRT.DocumentSettings, rels)

        return part

    @classmethod
    def endnotes(cls, rels: RelationshipCollection):
        """
        11.3.4 尾注部件

        该部件类型的实例包含了文档中的所有尾注。

        一个包中不得包含超过两个尾注部件。如果存在，其中一个实例应该是主文档（[§11.3.10]）部件隐式关系的目标，另一个实例应该是词汇表文档（[§11.3.8]）部件隐式关系的目标。
        """


        part: Optional[EndnotesPart] = PartFinder._part_by_rt(WRT.Endnotes, rels)

        return part

    @classmethod
    def font_table(cls, rels: RelationshipCollection):
        """
        11.3.5 字体表部件

        此部件类型的一个实例包含文档中每个使用的字体的信息。当使用者阅读一个 WordprocessingML 文档时，应该使用此信息来确定在消费者的系统上指定的字体不可用时，要使用哪些字体来显示文档。

        一个包不应包含多于两个 Font Table 部件。如果存在，该部件的一个实例应该成为 Main Document（[§11.3.10]）部件中隐式关系的目标，而另一个实例应该成为 Glossary Document（[§11.3.8]）部件的隐式关系的目标。

        包应包含零个或多个字体部件，对于每个存在的部件，该部件应是字体表(Font Table)（[§11.3.5]）或演示（§13.3.6）部件中显式关系的目标 。

        Font 部件应位于包含关系部件的包内（从语法上表达，Relationship 元素的 TargetMode 属性应为 Internal）。

        字体部件不应与 ECMA-376 定义的其他部件有隐式或显式的关系。
        """


        part: Optional[FontTablePart] = PartFinder._part_by_rt(WRT.FontTable, rels)

        return part

    @classmethod
    def footer(cls, rels: RelationshipCollection):
        """
        11.3.6 页脚部件

        此部件类型的一个实例包含一个或多个部件所显示的页脚的信息。一个包允许为文档中每个部件的每种类型的页脚（第一页、奇数页或偶数页）包含零个或一个页脚部件。

        每个页脚部件应该是 Main Document（[§11.3.10]）部件或 Glossary Document（[§11.3.8]）部件的 part-relationship 项中的一个显式关系的目标。
        """


        part: Optional[FooterPart] = PartFinder._part_by_rt(WRT.Footer, rels)

        return part

    @classmethod
    def footnotes(cls, rels: RelationshipCollection):
        """
        11.3.7 脚注部件

        此部件类型的一个实例包含文档中的所有脚注。

        一个包不应包含多于两个 Footnotes 部件。如果存在，该部件的一个实例应该成为 Main Document（[§11.3.10]）部件的隐式关系的目标，而另一个实例应该成为 Glossary Document（[§11.3.8]）部件的隐式关系的目标。
        """


        part: Optional[FootnotesPart] = PartFinder._part_by_rt(WRT.Footnotes, rels)

        return part

    @classmethod
    def glossary_document(cls, rels: RelationshipCollection):
        """
        11.3.8 术语表部件

        此部件类型的一个实例是一个附加文档存储位置，用于存储将来要插入和/或使用的内容的定义和内容，但这些内容不应在主文档内容中可见。[示例：一个法律合同模板可能包含一个或多个可选条款，在用户操作明确插入这些条款之前，这些条款不会出现在文档中。为了存储这些可选条款直到被插入，它们的内容被放置在词汇表文档部件中。结束示例]
        """


        part: Optional[GlossaryDocumentPart] = PartFinder._part_by_rt(WRT.GlossaryDocument, rels)

        return part

    @classmethod
    def header(cls, rels: RelationshipCollection):
        """
        11.3.9 页眉部件

        此部件类型的一个实例包含关于一个或多个章节显示的页眉的信息。一个包应该对于文档中每个部件的每种类型的页眉（第一页、奇数页或偶数页）包含零个或一个 Header 部件。每个 Header 部件应该是来自 Main Document（[§11.3.10]）部件或 Glossary Document（[§11.3.8]）部件的显式关系的目标。
        """


        part: Optional[HeaderPart] = PartFinder._part_by_rt(WRT.Header, rels)

        return part

    @classmethod
    def main_document(cls, rels: RelationshipCollection):
        """
        11.3.10 主文档部件

        该部件类型的一个实例包含文档的正文。

        一个包应该包含一个 Main Document（[§11.3.10]）部件。Main Document 部件应该是 package-relationship 项中的一个关系的目标。

        这种内容类型的部件的根元素应该是 document。
        """


        part: MainDocumentPart = PartFinder._part_require_by_rt(WRT.MainDocument, rels)

        return part

    @classmethod
    def numbering_definitions(cls, rels: RelationshipCollection):
        """
        11.3.11 编号定义部件

        该部件类型的一个实例包含该文档中每个唯一编号定义的结构定义。
        """


        part: list[NumberingDefinitionsPart] = PartFinder._parts_by_rt(WRT.NumberingDefinitions, rels)

        return part

    @classmethod
    def numbering_definition_one(cls, rels: RelationshipCollection):
        """
        11.3.11 编号定义部件

        该部件类型的一个实例包含该文档中每个唯一编号定义的结构定义。
        """


        part: Optional[NumberingDefinitionsPart] = PartFinder._part_by_rt(WRT.NumberingDefinitions, rels)

        return part

    @classmethod
    def style_definitions(cls, rels: RelationshipCollection):
        """
        11.3.12 样式定义部件

        该部件类型的一个实例包含该文档中每个唯一编号定义的结构定义。
        """


        part: StyleDefinitionsPart = PartFinder._part_require_by_rt(WRT.StyleDefinitions, rels)

        return part

    @classmethod
    def web_settings(cls, rels: RelationshipCollection):
        """
        11.3.13 web设置部件

        该部件类型的一个实例包含了文档中使用的特定于网络的设置的定义。

        一个包最多应包含两个网页设置部件。其中一个部件的一个实例应该是从主文档（[§11.3.10]）部件的隐式关系的目标，另一个应该是从词汇表文档（[§11.3.8]）部件的隐式关系的目标。
        """


        part: Optional[WebSettingsPart] = PartFinder._part_by_rt(WRT.WebSettings, rels)

        return part

    @classmethod
    def document_template(cls, rels: RelationshipCollection):
        """
        11.4 文档模板

        文档模板可以通过WordprocessingML包的一个实例来表示，其中包含了样式、编号定义等元素，这些元素在基于该模板编辑文档时可供使用。WordprocessingML文档可以通过包含一个文档设置部件（[§11.3.3]）来引用另一个文档作为其文档模板，该部件使用附加模板元素的id属性显式指定了所需文档模板的文件位置。
        """


        part: Optional[DocumentTemplatePart] = PartFinder._part_by_rt(WRT.DocumentTemplate, rels)

        return part

    @classmethod
    def framesets(cls, rels: RelationshipCollection):
        """
        11.5 框架集

        框架集(frameset)是一个WordprocessingML文档，用于指定其他WordprocessingML文档（在该上下文中称为框架）的位置和布局。框架集应由一个WordprocessingML文档的实例表示，该文档包含一个网页设置(Web Settings)部件（[§11.3.13]），其关系项指向该框架集的每个框架。
        """


        part: Optional[DocumentTemplatePart] = PartFinder._part_by_rt(WRT.DocumentTemplate, rels)

        return part

    @classmethod
    def subdocuments(cls, rels: RelationshipCollection):
        """
        11.6 主文档和子文档

        主文档(master document)应由一个WordprocessingML文档的实例表示，其主文档（[§11.3.10]）部件指向该主文档的每个子文档。

        [理由：有时，将文档作为一系列片段来处理会比较方便，特别是当这些片段可能由协作组中的不同作者编辑时。也许将一本书视为章节的集合而不是一个大文档更有意义。通过拥有一个或多个子文档的主文档来将文档拆分成这样的片段是可以实现的。理由结束]
        """


        part: Optional[SubdocumentsPart] = PartFinder._part_by_rt(WRT.Subdocuments, rels)

        return part

    @classmethod
    def mail_merge_data_source(cls, rels: RelationshipCollection):
        """
        11.7 邮件合并数据源

        一个存储有关邮件合并操作信息的文档可以包含一个文档设置部件（[§11.3.3]），其关系项使用此关系目标指向所需数据源的文件位置。
        """


        part: Optional[MailMergeDataSourcePart] = PartFinder._part_by_rt(WRT.MailMergeDataSource, rels)

        return part

    @classmethod
    def mail_merge_header_data_source(cls, rels: RelationshipCollection):
        """
        11.8 邮件合并标头数据源

        一个存储有关邮件合并操作信息的文档可以包含一个文档设置部件（[§11.3.3]），其关系项通过此关系指向必要标题数据源的文件位置。
        """


        part: Optional[MailMergeHeaderDataSourcePart] = PartFinder._part_by_rt(WRT.MailMergeHeaderDataSource, rels)

        return part

    @classmethod
    def xsl_transformation(cls, rels: RelationshipCollection):
        """
        11.9 XSL 转换

        文档可以存储关于XSL转换的信息，该转换可能在文档以单个文件格式输出时（例如，作为XML或HTML）应用。这些信息存储在一个文档设置部件（[§11.3.3]）中，其部件关系项包含使用此关系到XSL转换文件位置的显式关系。[注意：关于此关系如何使用（结合saveThroughXslt元素）的完整描述，请参阅§17.15.1.76。]
        """


        part: Optional[XSLTransformationPart] = PartFinder._part_by_rt(WRT.XSLTransformation, rels)

        return part


class SMLPartFinder(PartFinder):
    """
    12. SpreadsheetML

    该Finder 查找与xlsx包相关的部件

    注意：暂未实现，无需求
    """



class PMLPartFinder(PartFinder):
    """
    13. PresentationML

    该Finder 查找与pptx包相关的部件

    本节包含特定于PresentationML 的关系项和部件的规范。

    [§15.2] 中指定了PresentationML 文档中可能出现但不是 PresentationML 特定的部件。

    除非明确说明，否则本条款中对关系项、内容类型项和部件的所有引用均指的是 PresentationML ZIP 项。
    """

    @classmethod
    def comment_authors(cls, rels: RelationshipCollection):
        """
        13.3.1 评论作者部件

        此部件类型的实例包含有关向文档添加评论的每位作者的信息。
        该信息包括作者姓名、姓名缩写、唯一作者 ID、最后评论索引使用计数以及显示颜色。 （显示评论时可以使用颜色来区分不同作者的评论。）

        一个包最多应包含一个评论作者部件。 如果存在，则该部件应成为表示（[§13.3.6]）部件中隐式关系的目标。
        """


        part: Optional[CommentAuthorsPart] = cls._part_by_rt(PRT.CommentAuthors, rels)

        return part

    @classmethod
    def comment(cls, rels: RelationshipCollection):
        """
        13.3.2 评论部件

        此部件类型的实例包含单个幻灯片的评论。 每条评论都通过作者 ID 与其作者相关联。 每个评论的索引号和作者 ID 组合都是唯一的。

        对于包含一个或多个评论的每张幻灯片，包应包含一个评论部件，并且每个部件应是与其相应幻灯片 ([§13.3.8]) 部件的隐式关系的目标。
        """


        part: Optional[CommentsPart] = cls._part_by_rt(PRT.Comments, rels)

        return part

    @classmethod
    def handout_master(cls, rels: RelationshipCollection):
        """
        13.3.3 讲义母板部件

        此部件类型的实例包含演示文稿讲义上幻灯片、注释、页眉和页脚文本、日期或页码的外观、位置和大小。

        一个包最多应包含一个讲义母板部件，并且它应是演示文稿（[§13.3.6]）部件的显式关系的目标。
        """


        part: Optional[HandoutMasterPart] = cls._part_require_by_rt(PRT.HandoutMaster, rels)

        return part

    @classmethod
    def notes_master(cls, rels: RelationshipCollection):
        """
        13.3.4 笔记母版部件

        此部件类型的实例包含有关所有注释页面(notes pages)的内容和格式的信息。

        一个包最多应包含一个 Notes Master 部件，并且该部件应是 Notes Slide ([§13.3.5]) 部件的隐式关系以及演示部件(Presentation Part) ([§13.3.5]) 的显式关系的目标。
        """


        part: Optional[NotesMasterPart] = cls._part_require_by_rt(PRT.NotesMaster, rels)

        return part

    @classmethod
    def notes_slide(cls, rels: RelationshipCollection):
        """
        13.3.5 笔记幻灯片部件

        此部件类型的实例包含单个幻灯片的注释。

        对于每张包含注释的幻灯片，包应包含一个注释幻灯片部件。 如果存在，则这些部件均应成为幻灯片 ([§13.3.8]) 部件隐式关系的目标。
        """


        part: Optional[NotesSlidePart] = cls._part_require_by_rt(PRT.NotesSlide, rels)

        return part

    @classmethod
    def presentation(cls, rels: RelationshipCollection):
        """
        13.3.6 演示部件

        此部件类型的实例包含幻灯片演示文稿的定义。

        一个包应恰好包含一个演示部件(Presentation part)，并且该部件应是包关系项中关系的目标。
        """


        part: PresentaionPart = cls._part_require_by_rt(PRT.Presentation, rels)

        return part

    @classmethod
    def presentation_pr(cls, rels: RelationshipCollection):
        """
        13.3.7 演示属性部件

        此部件类型的实例包含演示文稿(presentation)的所有属性。

        包应恰好包含一个演示文稿属性(Presentation Properties)部件，并且该部件应是来自幻灯片部件(Presentation Part)（[§13.3.6]）的隐式关系的目标。
        """


        part: PresentationPropertiesPart = cls._part_require_by_rt(PRT.PresentationProperties, rels)

        return part

    @classmethod
    def slide(cls, rels: RelationshipCollection, rid: str):
        """
        13.3.8 幻灯片部件

        幻灯片部件(Slide Part)包含单张幻灯片的内容。

        包中每张幻灯片应包含一个幻灯片部件(Slide Part)，并且每个部件均应是演示文稿 ([§13.3.6]) 部件中显式关系的目标。
        """


        part: SlidePart = cls._part_require_by_rt(PRT.Slide, rels, rid)

        return part

    @classmethod
    def slide_layout(cls, rels: RelationshipCollection, rid: Optional[str] = None):
        """
        13.3.9 幻灯片布局部件

        此部件类型的实例包含此演示文稿的幻灯片布局模板(slide layout template)的定义。 此模板定义创建此幻灯片类型时绘图对象的默认外观和位置。

        包应包含一个或多个幻灯片布局部件，并且每个部件应是幻灯片母版 ([§13.3.10]) 部件中显式关系的目标，以及来自每个幻灯片 ( [§13.3.8]) 与此幻灯片布局相关的部件。
        """


        part: SlideLayoutPart = cls._part_require_by_rt(PRT.SlideLayout, rels, rid)

        return part

    @classmethod
    def slide_master(cls, rels: RelationshipCollection, rid: Optional[str] = None):
        """
        13.3.10 幻灯片母版部件

        此部件类型的实例包含格式、文本和对象的主定义，这些定义出现在从该幻灯片母版派生的演示文稿中的每张幻灯片上。

        包应包含一个或多个幻灯片母版部件([§13.3.9])，每个部件都应是演示部件([§13.3.6])的显式关系的目标，以及任何幻灯片布局部件([§13.3.9])的隐式关系（其中幻灯片布局是基于此幻灯片母版定义的）。 每一个幻灯片母板部件([§13.3.9])也可以选择成为幻灯片布局部件([§13.3.9])中关系的目标。
        """


        part: SlideMasterPart

        if rid is None:
            part = cls._part_require_by_rt(PRT.SlideMaster, rels)
        else:
            part = cls._part_require_by_rt(PRT.SlideMaster, rels, rid)

        return part

    @classmethod
    def slide_master_relationship(cls, rels: RelationshipCollection):
        """
        13.3.10 幻灯片母版部件

        此部件类型的实例包含格式、文本和对象的主定义，这些定义出现在从该幻灯片母版派生的演示文稿中的每张幻灯片上。

        包应包含一个或多个幻灯片母版部件([§13.3.9])，每个部件都应是演示部件([§13.3.6])的显式关系的目标，以及任何幻灯片布局部件([§13.3.9])的隐式关系（其中幻灯片布局是基于此幻灯片母版定义的）。 每一个幻灯片母板部件([§13.3.9])也可以选择成为幻灯片布局部件([§13.3.9])中关系的目标。
        """

        return rels.get_rels_by_type(PRT.SlideMaster)


    @classmethod
    def slide_sync_data(cls, rels: RelationshipCollection):
        """
        13.3.11 幻灯片同步数据部件

        此部件类型的实例包含格式、文本和对象的主定义，这些定义出现在从该幻灯片母版派生的演示文稿中的每张幻灯片上。

        包应包含一个或多个幻灯片母版部件([§13.3.9])，每个部件都应是演示部件([§13.3.6])的显式关系的目标，以及任何幻灯片布局部件([§13.3.9])的隐式关系（其中幻灯片布局是基于此幻灯片母版定义的）。 每一个幻灯片母板部件([§13.3.9])也可以选择成为幻灯片布局部件([§13.3.9])中关系的目标。
        """


        part: Optional[SlideSynchronizationDataPart] = cls._part_by_rt(PRT.SlideSynchronizationData, rels)

        return part

    @classmethod
    def user_defined_tags(cls, rels: RelationshipCollection):
        """
        13.3.12 用户已定义标签部件

        此部件类型的实例包含演示文稿中对象的一组用户定义属性（每个属性由名称/值对组成）。

        包应包含零个或多个用户定义标签部件，每个部件作为相应演示文稿 ([§13.3.6]) 或幻灯片 ([§13.3.8]) 部件的显式关系的目标。
        """


        part: list[UserDefinedTagsPart] = cls._parts_by_rt(PRT.UserDefinedTags, rels)

        return part

    @classmethod
    def view_pr(cls, rels: RelationshipCollection):
        """
        13.3.13 视图属性部件

        此部件类型的实例包含此演示文稿的视图属性。

        包应包含零个或一个“视图属性”部件，如果存在，则该部件应是来自“演示”([§13.3.6]) 部件的隐式关系的目标。
        """


        part: Optional[ViewProperitesPart] = cls._part_by_rt(PRT.ViewProperties, rels)

        return part

    @classmethod
    def html_publish_location(cls, rels: RelationshipCollection):
        """
        13.4 HTML 发布位置

        当演示文稿指定可以将 HTML 格式的可选副本推送到的外部位置时，应使用此关系来确定演示文稿的 HTML 副本发布的目标位置。

        包应包含与 HTML 发布位置链接的每张幻灯片的一个 HTML 发布位置关系，并且该关系应是来自相应演示文稿属性（[§13.3.7]）部件的显式关系。
        """


        parts: list[HTMLPublishLocation] = cls._parts_by_rt(PRT.HTMLPublishLocation, rels)

        return parts

    @classmethod
    def slide_sync_server_location(cls, rels: RelationshipCollection):
        """
        13.5 幻灯片同步服务器位置

        当幻灯片与远程服务器上存储的副本同步时，应使用此关系来确定幻灯片的服务器副本的存储位置。

        包应包含与服务器数据链接的每张幻灯片的一个幻灯片同步服务器位置关系，并且该关系应是来自相应幻灯片同步数据（[§13.3.11]）部件的隐式关系。
        """


        parts: list[SlideSynchronizationServerLocation] = cls._parts_by_rt(PRT.SlideSynchronizationServerLocation, rels)

        return parts
