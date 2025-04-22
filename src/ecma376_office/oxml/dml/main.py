"""
对应xsd: dml-main.xsd

<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    xmlns:s="http://schemas.openxmlformats.org/officeDocument/2006/sharedTypes"
    xmlns="http://schemas.openxmlformats.org/drawingml/2006/main"
    targetNamespace="http://schemas.openxmlformats.org/drawingml/2006/main"
    elementFormDefault="qualified">
    <xsd:import namespace="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
        schemaLocation="shared-relationshipReference.xsd"/>
    <xsd:import namespace="http://schemas.openxmlformats.org/officeDocument/2006/sharedTypes"
        schemaLocation="shared-commonSimpleTypes.xsd"/>
    <xsd:import namespace="http://schemas.openxmlformats.org/drawingml/2006/diagram"
        schemaLocation="dml-diagram.xsd"/>
    <xsd:import namespace="http://schemas.openxmlformats.org/drawingml/2006/chart"
        schemaLocation="dml-chart.xsd"/>
    <xsd:import namespace="http://schemas.openxmlformats.org/drawingml/2006/picture"
        schemaLocation="dml-picture.xsd"/>
    <xsd:import namespace="http://schemas.openxmlformats.org/drawingml/2006/lockedCanvas"
        schemaLocation="dml-lockedCanvas.xsd"/>
        ...
</xsd:schema>

对应Reference: 21.1 DrawingML - Main
"""

from __future__ import annotations

import logging
import math
from typing import TYPE_CHECKING, AnyStr, NewType, Optional, Self, TypeVar, Union

from ecma376_office.oxml import utils
from ecma376_office.oxml.base import OxmlBaseElement, ST_BaseEnumType, ST_BaseType, lookup
from ecma376_office.oxml.exceptions import OxmlAttributeValidateError, OxmlElementValidateError
from ecma376_office.oxml.shared.common_simple_types import ST_FixedPercentage as s_ST_FixedPercentage
from ecma376_office.oxml.shared.common_simple_types import ST_Guid as s_ST_Guid
from ecma376_office.oxml.shared.common_simple_types import ST_HexColorRGB, to_ST_UniversalMeasure
from ecma376_office.oxml.shared.common_simple_types import ST_Lang as s_ST_Lang
from ecma376_office.oxml.shared.common_simple_types import ST_OnOff as s_ST_OnOff
from ecma376_office.oxml.shared.common_simple_types import ST_Panose as s_ST_Panose
from ecma376_office.oxml.shared.common_simple_types import ST_Percentage as s_ST_Percentage
from ecma376_office.oxml.shared.common_simple_types import ST_PositiveFixedPercentage as s_ST_PositiveFixedPercentage
from ecma376_office.oxml.shared.common_simple_types import ST_PositivePercentage as s_ST_PositivePercentage
from ecma376_office.oxml.shared.common_simple_types import to_FixedPercentage as s_to_ST_FixedPercentage
from ecma376_office.oxml.shared.common_simple_types import to_ST_HexColorRGB as s_to_ST_HexColorRGB
from ecma376_office.oxml.shared.common_simple_types import to_ST_Percentage as s_to_ST_Percentage
from ecma376_office.oxml.shared.common_simple_types import (
    to_ST_PositiveFixedPercentage as s_to_ST_PositiveFixedPercentage,
)
from ecma376_office.oxml.shared.common_simple_types import to_ST_PositivePercentage as s_to_ST_PositivePercentage
from ecma376_office.oxml.shared.relationship_reference import ST_RelationshipId as r_ST_RelationshipId
from ecma376_office.oxml.xsd_types import (
    XSD_Boolean,
    XSD_Byte,
    XSD_Long,
    XSD_Token,
    XSD_UnsignedByte,
    XSD_UnsignedInt,
    to_xsd_bool,
    to_xsd_byte,
    to_xsd_unsigned_byte,
    to_xsd_unsigned_int,
)
from ecma376_office.units import Pt

if TYPE_CHECKING:
    from ecma376_office.oxml.dml.picture import CT_Picture as pic_CT_Picture
    from ecma376_office.oxml.pml.core import CT_MC_AlternateContent

namespace_a = 'http://schemas.openxmlformats.org/drawingml/2006/main'

namespace_r = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

namespace_s = 'http://schemas.openxmlformats.org/officeDocument/2006/sharedTypes'

namespace_dgm = 'http://schemas.openxmlformats.org/drawingml/2006/diagram'

namespace_tb = 'http://schemas.openxmlformats.org/drawingml/2006/table'

namespace_c = 'http://schemas.openxmlformats.org/drawingml/2006/chart'

namespace_pic = 'http://schemas.openxmlformats.org/drawingml/2006/picture'

# https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/annexL/topics/#l725-presentationml文档中的嵌入
namespace_ole = 'http://schemas.openxmlformats.org/presentationml/2006/ole'

# https://hellowac.github.io/ecma-376-zh-cn/ecma-part3-refrence/#7-mce-元素和属性
# Open XML 文件格式中用于描述兼容性设置的命名空间 URI。
# 它被用于处理在不同版本的应用程序之间文档兼容性的问题。
# 该命名空间定义了如何在文档中包含兼容性设置，这些设置允许旧版本的应用程序忽略不支持的新功能，同时仍能正确处理支持的内容。
namespace_mce = 'http://schemas.openxmlformats.org/markup-compatibility/2006'
namespace_mc = 'http://schemas.openxmlformats.org/markup-compatibility/2006'

logger = logging.getLogger(__name__)

ns_map = {
    'a': namespace_a,  # 当前命名空间
    'r': namespace_r,
    's': namespace_s,
    'pic': namespace_pic,  # docx 中嵌入的图片
    'mce': namespace_mce,  # 兼容性命名空间
    'mc': namespace_mce,  # 兼容性命名空间
    'ole': namespace_ole,  # ppt嵌入式对象
}


def qn(tag: str):
    """将 dc:creator 这种的标签,转换为 {http://purl.org/dc/elements/1.1/}creator 这样的形式"""

    global ns_map

    if ':' not in tag:
        return tag

    ns_prefix, ns = tag.split(':')

    return f'{{{ns_map[ns_prefix]}}}{ns}'


SubBaseElement = TypeVar('SubBaseElement', bound=OxmlBaseElement)


class CT_AudioFile(OxmlBaseElement):
    """文件中的音频

    20.1.3.2

    Audio from File

    该元素指定音频文件的存在。 该元素在对象的非视觉属性中指定。 音频应附加到对象，因为这是它在文档中的表示方式。 然而，音频的实际播放是在计时元素下指定的计时节点列表内完成的。
    """

    @property
    def ext_lst(self) -> list[CT_OfficeArtExtensionList]:
        """文件中的音频"""

        return self.findall(qn('a:extLst'))  # type: ignore

    @property
    def r_link(self) -> r_ST_RelationshipId:
        """关联关系 ID

        20.1.3.2 Linked Relationship ID"""

        return r_ST_RelationshipId(str(self.attrib[qn('r:link')]))

    @property
    def content_type(self) -> Optional[str]:
        """Content Type of Linked Audio File

        音频文件的内容类型

        eg: audio/mpeg ISO/IEC 11172-3

        内容类型定义媒体类型、子类型和可选参数集，如第 2 部分中所定义。如果呈现应用程序无法处理指定内容类型的外部内容，则可以忽略指定内容. [Note: [§15.2.2] 中提供了建议的音频类型列表。 end note]

        如果省略此属性，应用程序应尝试通过读取关系目标的内容来确定内容类型.

        想要互操作性的生产者应该使用以下标准格式:

        - audio/mpeg ISO/IEC 11172-3
        """

        ct = self.attrib.get('contentType')

        return str(ct) if ct else None


class CT_VideoFile(OxmlBaseElement):
    """文件中的视频

    20.1.3.6

    Video from File

    该元素指定视频文件的存在。 该元素在对象的非视觉属性中指定。 视频应附加到对象上，因为这是它在文档中的表示方式。 然而，视频的实际播放是在定时元素下指定的定时节点列表内完成的。


    """

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """文件中的音频"""
        return getattr(self, qn('a:extLst'), None)

    @property
    def r_link(self) -> r_ST_RelationshipId:
        """关联关系 ID

        20.1.3.6 Linked Relationship ID"""

        return r_ST_RelationshipId(str(self.attrib[qn('r:link')]))

    @property
    def content_type(self) -> Optional[str]:
        """媒体类型

        Content Type of Linked Audio File

        链接视频文件的内容类型

        内容类型定义媒体类型、子类型和可选参数集，如第 2 部分中所定义。如果呈现应用程序无法处理指定内容类型的外部内容，则可以忽略指定内容. [Note: 第 15.2.17 节中提供了建议的视频类型列表。 end note]

        如果省略此属性，应用程序应尝试通过读取关系目标的内容来确定内容类型.

        """

        ct = self.attrib.get('contentType')

        return str(ct) if ct else None


class CT_QuickTimeFile(OxmlBaseElement):
    """来自文件的 QuickTime

    20.1.3.4

    QuickTime from File
    """

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """文件中的音频"""

        return getattr(self, qn('a:extLst'), None)

    @property
    def r_link(self) -> r_ST_RelationshipId:
        """20.1.3.6 Linked Relationship ID"""

        return r_ST_RelationshipId(str(self.attrib[qn('r:link')]))


class CT_AudioCDTime(OxmlBaseElement):
    """CD 中的音频
    20.1.3.3

    CD Time
    """

    @property
    def track(self) -> XSD_UnsignedByte:
        """0到255之间的整数

        指定此音频在 CD 的哪个轨道上停止播放。 该属性是必需的，不能省略。

        type: xsd:unsignedByte

        <xsd:attribute name="track" type="xsd:unsignedByte" use="required"/>
        """

        value = self.attrib['track']

        return to_xsd_unsigned_byte(value)  # type: ignore

    @property
    def time(self) -> XSD_UnsignedInt:
        """大于0的整数

        指定 CD 音频应停止的时间（以秒为单位）。 如果省略该属性，则假定值为 0。

        type: xsd:unsignedInt

        <xsd:attribute name="time" type="xsd:unsignedInt" use="optional" default="0"/>
        """

        value = self.attrib.get('time', '0')

        return to_xsd_unsigned_int(value)  # type: ignore


class CT_AudioCD(OxmlBaseElement):
    """CD 中的音频

    20.1.3.1

    Audio from CD

    该元素指定 CD 中是否存在音频。 该元素在对象的非视觉属性中指定。
    音频应附加到对象，因为这是它在文档中的表示方式。
    然而，声音的实际播放是在计时元素下指定的计时节点列表内完成的。
    """

    @property
    def start(self) -> CT_AudioCDTime:
        """开始时间"""

        return getattr(self, qn('a:st'))

    @property
    def end(self) -> CT_AudioCDTime:
        """结束时间"""

        return getattr(self, qn('a:st'))

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """文件中的音频"""
        return getattr(self, qn('a:extLst'), None)


class EG_Media(OxmlBaseElement):
    """媒体节点

    <xsd:group name="EG_Media">
        <xsd:choice>
            <xsd:element name="audioCd" type="CT_AudioCD"/>
            <xsd:element name="wavAudioFile" type="CT_EmbeddedWAVAudioFile"/>
            <xsd:element name="audioFile" type="CT_AudioFile"/>
            <xsd:element name="videoFile" type="CT_VideoFile"/>
            <xsd:element name="quickTimeFile" type="CT_QuickTimeFile"/>
        </xsd:choice>
    </xsd:group>
    """

    media_tags = (
        qn('a:audioCd'),  # CT_AudioCD
        qn('a:wavAudioFile'),  # CT_EmbeddedWAVAudioFile
        qn('a:audioFile'),  # CT_AudioFile
        qn('a:videoFile'),  # CT_VideoFile
        qn('a:quickTimeFile'),  # CT_QuickTimeFile
    )


# <xsd:restriction base="xsd:unsignedInt"/>
ST_StyleMatrixColumnIndex = NewType('ST_StyleMatrixColumnIndex', int)
"""样式矩阵列索引

20.1.10.57

这个简单类型指定了一个索引，该索引指向由fmtScheme元素（bgFillStyleLst、effectStyleLst、fillStyleLst或lnStyleLst）指定的样式矩阵中的一个列表。

这个简单类型的内容是对W3C XML Schema中unsignedInt数据类型的限制。
"""


class ST_FontCollectionIndex(ST_BaseEnumType):
    """字体集合索引
    20.1.10.25

    Font Collection Index

    这种简单的类型代表与该样式相关的字体之一。

    样式相关的字体之一
    """

    Major = 'major'
    """样式字体方案的主要字体。"""

    Minor = 'minor'
    """样式字体方案的次要字体。"""

    none = 'none'
    """没有字体引用"""


class ST_ColorSchemeIndex(ST_BaseEnumType):
    """主题颜色参考
    20.1.10.14

    Theme Color Reference

    对配色方案中颜色的引用。
    """

    Dark1 = 'dk1'
    """代表第一个深色。"""

    Light1 = 'lt1'
    """代表第一个浅色。"""

    Dark2 = 'dk2'
    """代表第二个深色。"""

    Light2 = 'lt2'
    """代表第二个浅色。"""

    Accent1 = 'accent1'
    """代表强调 1 的颜色。"""

    Accent2 = 'accent2'
    """代表强调 2 的颜色。"""

    Accent3 = 'accent3'
    """代表强调 3 的颜色。"""

    Accent4 = 'accent4'
    """代表强调 4 的颜色。"""

    Accent5 = 'accent5'
    """代表强调 5 的颜色。"""

    Accent6 = 'accent6'
    """代表强调 6 的颜色。"""

    Hyperlink = 'hlink'
    """代表超链接颜色"""

    #   Represents the followed hyperlink color.
    Followed_hyperlink = 'folHlink'
    """代表点击过的超链接颜色。"""


class CT_ColorScheme(OxmlBaseElement):
    """颜色方案

    20.1.6.2 clrScheme

    该元素定义了一组颜色，称为配色方案。 配色方案负责定义十二种颜色的列表。 这十二种颜色包括六种强调色、两种深色、两种浅色以及每个超链接和已关注超链接的颜色。

    配色方案颜色元素按顺序出现。 以下列表显示了索引值和相应的颜色名称。

    - 0:    dk1 (暗色 1)
    - 1:    lt1 (亮色 1)
    - 2:    dk2 (暗色 2)
    - 3:    lt2 (亮色 2)
    - 4:    accent1 (强调色 1)
    - 5:    accent2 (强调色 2)
    - 6:    accent3 (强调色 3)
    - 7:    accent4 (强调色 4)
    - 8:    accent5 (强调色 5)
    - 9:    accent6 (强调色 6)
    - 10:    hlink (超链接)
    - 11:    folHlink (已关注超链接)
    """

    @property
    def name(self) -> str:
        """方案名称

        此配色方案的通用名称。 该名称可以显示在用户界面的配色方案列表中.
        """

        return str(self.attrib['name'])

    @property
    def dark1(self) -> CT_Color:
        """深色1

        20.1.4.1.9 dk1

        该元素定义了一种恰好是深色 1 的颜色。 十二种颜色组合在一起形成主题的配色方案。
        """

        clr: CT_Color = getattr(self, qn('a:dk1'))

        return clr

    @property
    def light1(self) -> CT_Color:
        """浅色1

        20.1.4.1.22 lt1

        该元素定义的颜色恰好是 浅色 1 颜色。 十二种颜色组合在一起形成主题的配色方案。
        """

        clr: CT_Color = getattr(self, qn('a:lt1'))

        return clr

    @property
    def dark2(self) -> CT_Color:
        """深色2

        20.1.4.1.10 dk2

        该元素定义了一种恰好是深色 2 的颜色。 十二种颜色组合在一起形成主题的配色方案。
        """

        clr: CT_Color = getattr(self, qn('a:dk2'))

        return clr

    @property
    def light2(self) -> CT_Color:
        """浅色2

        20.1.4.1.23 lt2

        该元素定义的颜色恰好是 浅色 2 颜色。 十二种颜色组合在一起形成主题的配色方案。
        """

        clr: CT_Color = getattr(self, qn('a:lt2'))

        return clr

    @property
    def accent1(self) -> CT_Color:
        """强调色 1

        20.1.4.1.1 accent1 (强调色 1)

        该元素定义了一种恰好是强调色 1 的颜色。 十二种颜色组合在一起形成主题的配色方案。
        """

        clr: CT_Color = getattr(self, qn('a:accent1'))

        return clr

    @property
    def accent2(self) -> CT_Color:
        """强调色 2

        20.1.4.1.2 accent2 (强调色 2)

        该元素定义了一种恰好是强调色 2 的颜色。 十二种颜色组合在一起形成主题的配色方案。
        """

        clr: CT_Color = getattr(self, qn('a:accent2'))

        return clr

    @property
    def accent3(self) -> CT_Color:
        """强调色 3

        20.1.4.1.3 accent3 (强调色 3)

        该元素定义了一种恰好是强调 3 颜色的颜色。 十二种颜色组合在一起形成主题的配色方案。
        """

        clr: CT_Color = getattr(self, qn('a:accent3'))

        return clr

    @property
    def accent4(self) -> CT_Color:
        """强调色 4

        20.1.4.1.4 accent4

        该元素定义了一种恰好是强调 4 颜色的颜色。 十二种颜色组合在一起形成主题的配色方案。
        """

        clr: CT_Color = getattr(self, qn('a:accent4'))

        return clr

    @property
    def accent5(self) -> CT_Color:
        """强调色 5

        20.1.4.1.5 accent5

        该元素定义了一种恰好是强调 5 颜色的颜色。 十二种颜色组合在一起形成主题的配色方案。
        """

        clr: CT_Color = getattr(self, qn('a:accent5'))

        return clr

    @property
    def accent6(self) -> CT_Color:
        """强调色 6

        20.1.4.1.6 accent6

        该元素定义了一种恰好是强调 6 颜色的颜色。 十二种颜色组合在一起形成主题的配色方案。
        """

        clr: CT_Color = getattr(self, qn('a:accent6'))

        return clr

    @property
    def hyperlink(self) -> CT_Color:
        """超链接颜色

        20.1.4.1.19 hlink

        该元素定义了一种恰好是超链接颜色的颜色。 十二种颜色组合在一起形成主题的配色方案。
        """

        clr: CT_Color = getattr(self, qn('a:hlink'))

        return clr

    @property
    def followed_hyperlink(self) -> CT_Color:
        """已点击超链接颜色

        20.1.4.1.15 folHlink

        该元素定义了一种颜色，该颜色恰好是已关注的超链接颜色。 十二种颜色组合在一起形成主题的配色方案。
        """

        clr: CT_Color = getattr(self, qn('a:folHlink'))

        return clr

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)


class EG_ColorChoice(OxmlBaseElement):
    """颜色选择

    <xsd:group name="EG_ColorChoice">
        <xsd:choice>
            <xsd:element name="scrgbClr" type="CT_ScRgbColor" minOccurs="1" maxOccurs="1"/>
            <xsd:element name="srgbClr" type="CT_SRgbColor" minOccurs="1" maxOccurs="1"/>
            <xsd:element name="hslClr" type="CT_HslColor" minOccurs="1" maxOccurs="1"/>
            <xsd:element name="sysClr" type="CT_SystemColor" minOccurs="1" maxOccurs="1"/>
            <xsd:element name="schemeClr" type="CT_SchemeColor" minOccurs="1" maxOccurs="1"/>
            <xsd:element name="prstClr" type="CT_PresetColor" minOccurs="1" maxOccurs="1"/>
        </xsd:choice>
    </xsd:group>
    """

    color_tags = (
        qn('a:scrgbClr'),  # CT_ScRgbColor
        qn('a:srgbClr'),  # CT_SRgbColor
        qn('a:hslClr'),  # CT_HslColor
        qn('a:sysClr'),  # CT_SystemColor
        qn('a:schemeClr'),  # CT_SchemeColor
        qn('a:prstClr'),  # CT_PresetColor
    )

    # Union[
    #     CT_ScRgbColor,
    #     CT_SRgbColor,
    #     CT_HslColor,
    #     CT_SystemColor,
    #     CT_SchemeColor,
    #     CT_PresetColor,
    # ]


class CT_CustomColor(EG_ColorChoice):
    """自定义颜色
    20.1.4.1.8

    Custom color

    该元素定义自定义颜色。
    自定义颜色在自定义颜色列表中使用来定义自定义颜色，这些自定义颜色是可以附加到主题的额外颜色。
    这在有一组可供使用的企业调色板的企业场景中非常有用。
    """

    @property
    def color(
        self,
    ) -> CT_ScRgbColor | CT_SRgbColor | CT_HslColor | CT_SystemColor | CT_SchemeColor | CT_PresetColor:
        """颜色

        <xsd:group ref="EG_ColorChoice" minOccurs="1" maxOccurs="1"/>
        """
        """参考:


        20.1.2.3 Colors

        17.3.2.6 color (Run Content Color)

        """

        return self.choice_require_one_child(*self.color_tags)  # type: ignore

    @property
    def name(self) -> Optional[str]:
        """名称

        颜色选择器中显示的颜色名称.
        """
        n = self.attrib.get('name')

        return str(n) if n is not None else None


class CT_SupplementalFont(OxmlBaseElement):
    """补充字体
    20.1.4.1.16

    Font

    此元素定义 DrawingML 样式区域内的字体。 字体由脚本和字体一起定义。

    eg: <font script="Thai" typeface="Cordia New"/>
    """

    @property
    def script(self) -> str:
        """<xsd:attribute name="script" type="xsd:string" use="required"/>"""

        return str(self.attrib['script'])

    @property
    def typeface(self) -> ST_TextTypeface:
        """<xsd:attribute name="typeface" type="ST_TextTypeface" use="required"/>"""

        val = self.attrib['typeface']

        return ST_TextTypeface(utils.AnyStrToStr(val))  # type: ignore


class CT_CustomColorList(OxmlBaseElement):
    """自定义颜色列表

    20.1.6.3

    Custom Color List

    该元素允许创建自定义调色板，并与其他配色方案一起显示。 例如，当有人想要维护公司调色板时，这可能非常有用。
    """

    @property
    def custom_colors_lst(self) -> list[CT_CustomColor]:
        """自定义颜色列表

        <xsd:element name="custClr" type="CT_CustomColor" minOccurs="0" maxOccurs="unbounded"/>
        """

        return self.findall(self, qn('a:custClr'))  # type: ignore


class CT_FontCollection(OxmlBaseElement):
    """字体合集
    L.4.3.2.5

    Font Collection

    复杂类型 CT_FontCollection 定义了字体方案中使用的主要字体和次要字体。
    字体集合包含拉丁文、东亚文和复杂脚本的字体定义。
    除了这三个定义之外，还可以定义一种用于特定语言的字体。
    """

    @property
    def latin(self) -> CT_TextFont:
        return getattr(self, qn('a:latin'))

    @property
    def east_asia(self) -> CT_TextFont:
        return getattr(self, qn('a:ea'))

    @property
    def complex_script(self) -> CT_TextFont:
        return getattr(self, qn('a:cs'))

    @property
    def font(self) -> list[CT_SupplementalFont]:
        return self.findall(qn('a:latin'))  # type: ignore

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """文件中的音频"""

        return getattr(self, qn('a:extLst'), None)


class EG_EffectProperties(OxmlBaseElement):
    """效果属性"""

    effect_pr_tags = (
        qn('a:effectLst'),  # CT_EffectList
        qn('a:effectDag'),  # CT_EffectContainer
    )


class CT_EffectStyleItem(EG_EffectProperties):
    """效果样式项
    L.4.3.2.11

    Effect Style Item

    复杂类型 CT_EffectStyleItem 保存给定效果样式的属性。
    在这种复杂的类型中，我们可以定义一系列效果（模糊、阴影、反射等）以及要应用于对象的任何 3-D 属性。

    20.1.4.1.11 effectStyle

    该元素定义了一组可应用于对象的效果和 3D 属性。
    """

    @property
    def effect(self) -> Optional[CT_EffectList | CT_EffectContainer]:
        """效果样式

        20.1.4.1.12 effectStyleLst

        此元素定义一组三种效果样式，用于为主题创建效果样式列表。 效果风格按照从微妙到中度到强烈的顺序排列。

        <xsd:group ref="EG_EffectProperties" minOccurs="1" maxOccurs="1"/>
        """

        return self.choice_require_one_child(*self.effect_pr_tags)  # type: ignore

    @property
    def scene_3d(self) -> Optional[CT_Scene3D]:
        """3d效果样式"""

        return getattr(self, qn('a:scene3d'), None)

    @property
    def shape_3d(self) -> Optional[CT_Shape3D]:
        """形状3D"""

        return getattr(self, qn('a:sp3d'), None)


class CT_FontScheme(OxmlBaseElement):
    """字体方案

    L.4.3.2.4

    Font Scheme

    复杂类型 CT_FontScheme 定义字体对。 该对由主要字体和次要字体组成。
    使用的示例是文档标题中使用的主要字体和文档段落部分中使用的次要字体。
    主要字体和次要字体是通过基于每种语言定义的字体集合来定义的。
    例如，可以仅定义一种基于拉丁语的字体，或者可以为主要或次要字体的不同局部定义许多不同的字体。
    文档中使用的字体取决于用户的语言。

    20.1.4.1.18 fontScheme该元素定义主题内的字体方案。 字体方案由一对在文档中使用的主要字体和次要字体组成。 主要字体与文档的标题区域很好地对应，次要字体与普通文本或段落区域很好地对应。
    该元素定义主题内的字体方案。 字体方案由一对在文档中使用的主要字体和次要字体组成。 主要字体与文档的标题区域很好地对应，次要字体与普通文本或段落区域很好地对应。
    """

    @property
    def name(self) -> str:
        """名称

        用户界面中显示的字体方案的名称.
        """

        return str(self.attrib['name'])

    @property
    def major_font(self) -> CT_FontCollection:
        """主要字体

        20.1.4.1.24 majorFont

        该元素定义了在不同语言或本地语言下使用的主要字体集.
        """

        return getattr(self, qn('a:majorFont'))

    @property
    def minor_font(self) -> CT_FontCollection:
        """次要字体

        20.1.4.1.25 minorFont

        该元素定义了在不同语言或本地语言下使用的小字体集.
        """

        return getattr(self, qn('a:minorFont'))

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)


class EG_FillProperties(OxmlBaseElement):
    """
    填充属性
    """

    fill_pr_tags = (
        qn('a:noFill'),  # CT_NoFillProperties
        qn('a:solidFill'),  # CT_SolidColorFillProperties
        qn('a:gradFill'),  # CT_GradientFillProperties
        qn('a:blipFill'),  # CT_BlipFillProperties
        qn('a:pattFill'),  # CT_PatternFillProperties
        qn('a:grpFill'),  # CT_GroupFillProperties
    )


class CT_FillStyleList(EG_FillProperties):
    """填充样式列表

    20.1.4.1.13 fillStyleLst

    该元素定义了主题中使用的一组三种填充样式。 三种填充风格按从微妙到中等到强烈的顺序排列。

    L.4.3.2.8 填充样式列表

    Fill Style List

    复杂类型 CT_FillStyleList 定义了一组三种填充类型。
    目前仅使用三种填充类型，分别对应于微妙、中等和强烈填充，但可以定义的填充数量是无限的。
    图 3 中可以看到可能存在的三种填充的示例。
    在该图中，我们在细微槽中使用纯蓝色填充，在中等槽中使用渐变填充，在强烈槽中使用图像填充。
    """

    @property
    def fill_style_lst(
        self,
    ) -> list[
        CT_NoFillProperties | CT_SolidColorFillProperties | CT_GradientFillProperties | CT_BlipFillProperties | CT_PatternFillProperties | CT_GroupFillProperties
    ]:
        """填充属性

        <xsd:group ref="EG_FillProperties" minOccurs="3" maxOccurs="unbounded"/>
        """

        elements = self.choice_and_more(*self.fill_pr_tags)

        if len(elements) < 3:
            msg = '应至少有3个元素'
            raise OxmlElementValidateError(msg)

        return elements  # type: ignore


class CT_LineStyleList(OxmlBaseElement):
    """线条样式列表

    20.1.4.1.21 lnStyleLst

    该元素定义了主题中使用的三种线条样式的列表。 三种线条风格按照线条从微妙到温和到强烈的顺序排列。 该列表构成了风格矩阵的一部分。

    填充样式列表

    L.4.3.2.9

    Line Style List

    复杂类型 CT_LineStyleList 定义一组三种线型。
    与填充样式列表一样，当前仅使用三种样式，即对应于细线、中等线和浓线。(subtle line, moderate line, and intense line.)
    """

    @property
    def line_lst(self) -> list[CT_LineProperties]:
        """线条的样式(属性)

        20.1.2.2.24 ln

        此元素指定可应用于许多不同对象（例如形状和文本）的轮廓样式。 该线允许指定许多不同类型的轮廓，包括甚至线虚线和斜角。

        <xsd:element name="ln" type="CT_LineProperties" minOccurs="3" maxOccurs="unbounded"/>
        """

        elements = self.findall(qn('a:ln'))

        if len(elements) < 3:
            msg = '应至少有3个元素'
            raise OxmlElementValidateError(msg)

        return elements  # type: ignore


class CT_EffectStyleList(OxmlBaseElement):
    """效果样式列表

    20.1.4.1.12 effectStyleLst

    此元素定义一组三种效果样式，用于为主题创建效果样式列表。 效果风格按照从微妙到中度到强烈的顺序排列。

    L.4.3.2.10 效果样式列表

    Effect Style List

    复杂类型 CT_EffectStyleList 定义一组三种效果样式。
    与前面提到的样式列表一样，当前使用三种样式，对应于微妙、中等和强烈的效果样式，但该列表仍然不受限制。
    在图 4 中，我们看到用蓝色填充对给定形状应用了微妙、中等和强烈的效果。
    微妙的效果基本上是没有效果，而中等的效果是围绕形状的发光，而强烈的效果是 3-D 斜角以及应用于形状的阴影。
    """

    @property
    def effect_styles(self) -> list[CT_EffectStyleItem]:
        """效果样式列表

        20.1.4.1.11 effectStyle

        该元素定义了一组可应用于对象的效果和 3D 属性。

        <xsd:element name="effectStyle" type="CT_EffectStyleItem" minOccurs="3" maxOccurs="unbounded" />
        """

        elements = self.findall(qn('a:effectStyle'))

        if len(elements) < 3:
            msg = '应至少有3个元素'
            raise OxmlElementValidateError(msg)

        return elements  # type: ignore


class CT_BackgroundFillStyleList(EG_FillProperties):
    """背景填充样式列表

    20.1.4.1.7 bgFillStyleLst

        此元素定义主题中使用的背景填充列表。 背景填充由三种填充组成，按从微妙到中等到强烈的顺序排列。

    L.4.3.2.12

    Background Fill Style List

    复杂类型 CT_BackgroundFillStyleList 定义了一组类似于填充样式列表的三种填充类型。
    同样，他们定义了三种填充类型，分别对应于微妙、中等和强烈的背景填充，但列表本身是无限的。
    例如，背景填充意味着应用于幻灯片背景，或者作为形状或表格中的背景填充。
    """

    @property
    def fill_style_lst(
        self,
    ) -> list[
        CT_NoFillProperties | CT_SolidColorFillProperties | CT_GradientFillProperties | CT_BlipFillProperties | CT_PatternFillProperties | CT_GroupFillProperties
    ]:
        """填充样式列表

        <xsd:group ref="EG_FillProperties" minOccurs="3" maxOccurs="unbounded"/>
        """

        elements = self.choice_and_more(*self.fill_pr_tags)

        if len(elements) < 3:
            msg = '应至少有3个元素'
            raise OxmlElementValidateError(msg)

        return elements  # type: ignore


class CT_StyleMatrix(OxmlBaseElement):
    """格式方案（样式矩阵）
    L.4.3.2.7

    Format Scheme (Style Matrix)

    复杂类型 CT_StyleMatrix 定义了一组格式化选项，这些选项可由将某种样式应用于对象的给定部分的文档引用。
    例如，在给定形状（例如矩形）中，可以引用主题线条样式、主题效果和主题填充，这些主题特定于主题并在主题更改时更改。
    所有这些格式选项都在此样式矩阵中定义。 背景填充也可以包含在样式矩阵中。
    这对于引用不同背景填充作为幻灯片背景的演示文稿最有用（但并非演示文稿所独有）。
    每种类型的格式定义了三组，对应于每种风格的微妙、中等和强烈版本。
    样式的组合用于创建，例如形状样式。 例如，形状样式利用微妙的填充、适度的线条和强烈的效果来定义形状的整体外观。

    20.1.4.1.14 fmtScheme

    此元素包含背景填充样式、效果样式、填充样式和线条样式，它们定义主题的样式矩阵。 风格矩阵由微妙、适度和强烈的填充、线条和效果组成。 背景填充通常不被认为与矩阵直接相关，但确实在整个文档的风格中发挥着作用。 通常，给定对象选择单一线条样式、单一填充样式和单一效果样式，以便定义对象的整体最终外观。
    """

    @property
    def name(self) -> str:
        """名称

        定义格式方案的名称。 该名称只是一个人类可读的字符串，用于标识用户界面中的格式方案.
        """
        return str(self.attrib.get('name', ''))

    @property
    def fill_style(self) -> CT_FillStyleList:
        """填充样式列表

        20.1.4.1.13 fillStyleLst

        该元素定义了主题中使用的一组三种填充样式。 三种填充风格按从微妙到中等到强烈的顺序排列。

        <xsd:element name="fillStyleLst" type="CT_FillStyleList" minOccurs="1" maxOccurs="1"/>
        """
        return getattr(self, qn('a:fillStyleLst'))

    @property
    def line_style(self) -> CT_LineStyleList:
        """线条样式列表

        20.1.4.1.21 lnStyleLst

        该元素定义了主题中使用的三种线条样式的列表。 三种线条风格按照线条从微妙到温和到强烈的顺序排列。 该列表构成了风格矩阵的一部分。

        <xsd:element name="lnStyleLst" type="CT_LineStyleList" minOccurs="1" maxOccurs="1"/>
        """
        return getattr(self, qn('a:lnStyleLst'))

    @property
    def effect_style(self) -> CT_EffectStyleList:
        """效果样式列表

        20.1.4.1.12 effectStyleLst

        此元素定义一组三种效果样式，用于为主题创建效果样式列表。 效果风格按照从微妙到中度到强烈的顺序排列。

        <xsd:element name="effectStyleLst" type="CT_EffectStyleList" minOccurs="1" maxOccurs="1"/>
        """
        return getattr(self, qn('a:effectStyleLst'))

    @property
    def background_style(self) -> CT_BackgroundFillStyleList:
        """背景填充样式列表

        20.1.4.1.7 bgFillStyleLst

        此元素定义主题中使用的背景填充列表。 背景填充由三种填充组成，按从微妙到中等到强烈的顺序排列。

        <xsd:element name="bgFillStyleLst" type="CT_BackgroundFillStyleList" minOccurs="1" maxOccurs="1"/>
        """
        return getattr(self, qn('a:bgFillStyleLst'))


class CT_BaseStyles(OxmlBaseElement):
    """主题元素, 基本样式

    L.4.3.2.2

    Theme Elements

    复杂类型 CT_BaseStyles 定义主题的主题元素，并且是主题的主力。
    给定文档使用的大部分共享主题信息均在此处定义。
    在这个复杂的类型中定义了颜色方案、字体方案和样式矩阵（格式方案），该样式矩阵为文档的不同部分定义了不同的格式选项。
    复杂类型 CT_BaseStyles 按以下方式定义:
    """

    @property
    def color_scheme(self) -> CT_ColorScheme:
        """颜色方案

        20.1.6.2 clrScheme

        该元素定义了一组颜色，称为配色方案。 配色方案负责定义十二种颜色的列表。 这十二种颜色包括六种强调色、两种深色、两种浅色以及每个超链接和已关注超链接的颜色。

        配色方案颜色元素按顺序出现。 以下列表显示了索引值和相应的颜色名称。

        - 0:    dk1 (暗色 1)
        - 1:    lt1 (亮色 1)
        - 2:    dk2 (暗色 2)
        - 3:    lt2 (亮色 2)
        - 4:    accent1 (强调色 1)
        - 5:    accent2 (强调色 2)
        - 6:    accent3 (强调色 3)
        - 7:    accent4 (强调色 4)
        - 8:    accent5 (强调色 5)
        - 9:    accent6 (强调色 6)
        - 10:    hlink (超链接)
        - 11:    folHlink (已关注超链接)

        <xsd:element name="clrScheme" type="CT_ColorScheme" minOccurs="1" maxOccurs="1"/>
        """

        return getattr(self, qn('a:clrScheme'))

    @property
    def font_scheme(self) -> CT_FontScheme:
        """字体方案

        20.1.4.1.18 fontScheme

        该元素定义主题内的字体方案。 字体方案由一对在文档中使用的主要字体和次要字体组成。 主要字体与文档的标题区域很好地对应，次要字体与普通文本或段落区域很好地对应。

        <xsd:element name="fontScheme" type="CT_FontScheme" minOccurs="1" maxOccurs="1"/>
        """

        return getattr(self, qn('a:fontScheme'))

    @property
    def format_scheme(self) -> CT_StyleMatrix:
        """格式方案

        20.1.4.1.14 fmtScheme

        此元素包含背景填充样式、效果样式、填充样式和线条样式，它们定义主题的样式矩阵。 风格矩阵由微妙、适度和强烈的填充、线条和效果组成。 背景填充通常不被认为与矩阵直接相关，但确实在整个文档的风格中发挥着作用。 通常，给定对象选择单一线条样式、单一填充样式和单一效果样式，以便定义对象的整体最终外观。

        <xsd:element name="fmtScheme" type="CT_StyleMatrix" minOccurs="1" maxOccurs="1"/>
        """

        return getattr(self, qn('a:fmtScheme'))

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)


class CT_OfficeArtExtension(OxmlBaseElement):
    """扩展元素，任何元素都可以
    20.1.2.2.14

    ext (Extension)

    此元素指定用于将来对 DrawingML 当前版本进行扩展的扩展。
    这允许将来指定当前未知的元素，用于生成应用程序的更高版本。

    注意: 该元素无意将过渡模式重新引入严格一致性类。

    <xsd:sequence>
      <xsd:any processContents="lax" minOccurs="0" maxOccurs="unbounded"/>
    </xsd:sequence>
    <xsd:attribute name="uri" type="xsd:token" use="required"/>
    """

    def extensions(self):
        """
        <xsd:any processContents="lax" minOccurs="0" maxOccurs="unbounded"/>
        """

        return list(self.iterchildren())

    def URI(self) -> XSD_Token:
        """uri"""

        return XSD_Token(str(self.attrib['uri']))


ST_CoordinateUnqualified = NewType('ST_CoordinateUnqualified', int)
"""坐标

20.1.10.19 ST_CoordinateUnqualified

Coordinate

这种简单类型表示一维中的位置或长度， 单位为 EMU

这个简单类型还指定了以下限制:

此简单类型的最小值大于或等于 -27273042329600。
此简单类型的最大值小于或等于 27273042316900。
"""


def to_ST_CoordinateUnqualified(val: str) -> ST_CoordinateUnqualified:
    pyval = int(val)

    if not (-27273042329600 <= pyval <= 27273042316900):
        msg = f'预期外的值: {val}'
        raise OxmlAttributeValidateError(msg)

    return ST_CoordinateUnqualified(pyval)


# <xsd:union memberTypes="ST_CoordinateUnqualified s:ST_UniversalMeasure"/>
# ST_Coordinate = Union[ST_CoordinateUnqualified, Shared_ST_UniversalMeasure]


ST_Coordinate = NewType('ST_Coordinate', float)
"""整合单位为 emu

20.1.10.16 ST_Coordinate (Coordinate)

这种简单类型将一维位置或长度表示为:

    EMU。

    数字后紧跟单位标识符， eg: xxxcm, xxxpt

这个简单类型是以下类型的联合:

    ST_CoordinateUnqualified 简单类型 (§20.1.10.19).
    ST_CoordinateUnqualified 简单类型 (§20.1.10.19).
"""


def to_ST_Coordinate(val: str) -> ST_Coordinate:
    # 针对 1234123
    if val.isdigit():
        return ST_Coordinate(to_ST_CoordinateUnqualified(val))

    # 针对 1234cm 等等带单位的
    if val[-2:] in {'mm', 'cm', 'in', 'pt', 'pc', 'pi'}:
        return ST_Coordinate(to_ST_UniversalMeasure(val))

    return ST_Coordinate(to_ST_CoordinateUnqualified(val))


ST_Coordinate32Unqualified = NewType('ST_Coordinate32Unqualified', int)
"""坐标点

20.1.10.18

Coordinate Point

这个简单的类型指定文档内的坐标。 这可用于测量或间距，最大尺寸要求为 32 位整数。

这里使用的测量单位是 EMU（英制公制单位）。
"""


# ST_Coordinate32 = Union[ST_Coordinate32Unqualified, Shared_ST_UniversalMeasure]
ST_Coordinate32 = NewType('ST_Coordinate32', int)
"""整合单位为 emu

20.1.10.16 ST_Coordinate (Coordinate)

这种简单类型将一维位置或长度表示为:

    EMU。

    数字后紧跟单位标识符， eg: xxxcm, xxxpt

这个简单类型是以下类型的联合:

    ST_CoordinateUnqualified 简单类型 (§20.1.10.19).
    ST_CoordinateUnqualified 简单类型 (§20.1.10.19).

20.1.10.17 ST_Coordinate32 坐标32位

这个简单类型指定文档中的坐标。这可以用于测量或间距；其最大大小为 2147483647 EMUs。

它的内容可以是:

- 一个整数，其内容是以 EMUs（英文单位）为单位的测量值
- 一个数字，紧跟着一个单位标识符

这个简单类型是以下类型的联合体:

- ST_Coordinate32Unqualified 简单类型（§20.1.10.18）。
- ST_UniversalMeasure 简单类型（§22.9.2.15）。
"""


def to_ST_Coordinate32(_val: AnyStr) -> ST_Coordinate32:
    val = utils.AnyStrToStr(_val)

    # 针对 1234123
    try:
        int(val)

        return ST_Coordinate32(to_ST_CoordinateUnqualified(val))

    # 针对 1234cm 等等带单位的
    except Exception:
        return ST_Coordinate32(to_ST_UniversalMeasure(val))


ST_PositiveCoordinate = NewType('ST_PositiveCoordinate', int)
"""正坐标

20.1.10.42 Positive Coordinate

这个简单类型表示在 EMU 中的正位置或长度。

这个简单类型的内容是对 W3C XML Schema 长整型数据类型的限制。

这个简单类型还指定了以下限制:

- 该简单类型的最小值大于或等于0。
- 该简单类型的最大值小于或等于27273042316900。
"""


def to_ST_PositiveCoordinate(val: AnyStr) -> ST_PositiveCoordinate:
    pyval = int(utils.AnyStrToStr(val))

    if not (0 <= pyval <= 27273042316900):
        msg = f'预期外的值: {pyval}'
        raise OxmlAttributeValidateError(msg)

    return ST_PositiveCoordinate(pyval)


ST_PositiveCoordinate32 = NewType('ST_PositiveCoordinate32', int)
"""正坐标点

20.1.10.43 Positive Coordinate Point

这个简单类型指定了一个最大为32位的正坐标点。

此处使用的测量单位是 EMU（英语度量单位）。

这个简单类型的内容是对 ST_Coordinate32Unqualified 数据类型的限制（§20.1.10.18）。

此外，这个简单类型还指定了以下限制:

- 该简单类型的最小值大于或等于0。
"""


def to_ST_PositiveCoordinate32(_val: AnyStr) -> ST_PositiveCoordinate32:
    pyval = int(utils.AnyStrToStr(_val))

    if pyval < 0:
        msg = f'预期外的值: {pyval}'
        raise OxmlAttributeValidateError(msg)

    return ST_PositiveCoordinate32(pyval)


ST_Angle = NewType('ST_Angle', float)
"""角度

20.1.10.3

Angle

这个简单的类型代表六万分之一度的角度。
正角度是顺时针方向（即，朝向正 y 轴）；
负角度是逆时针方向（即，朝向负 y 轴）。


DEGREE_INCREMENTS = 60000
THREE_SIXTY = 360 * DEGREE_INCREMENTS

rot = int(val) % THREE_SIXTY
angle = float(rot) / DEGREE_INCREMENTS  # 角度
"""


def to_ST_Angle(val: str) -> ST_Angle:
    """转换为角度

    参考: https://zhuanlan.zhihu.com/p/70819721
    """

    # rot = float(val) % (360 * 60000)  # 会丢失符号
    # "-5400000.0" 就会被计算为 16200000.0 # 导致 arcto 怎么绘制都不对。
    rot = math.fmod(float(val), 360 * 60000)
    angle = float(rot) / 60000  # 角度

    # logger.info(f"val: {val = } => {angle}")

    return ST_Angle(angle)


class CT_Angle(OxmlBaseElement):
    """色相偏移
    20.1.2.3.16

    Hue Offset

    该元素指定输入颜色，其色调发生变化，但饱和度和亮度不变
    """

    @property
    def value(self) -> ST_Angle:
        """偏移度

        <xsd:attribute name="val" type="ST_Angle" use="required"/>"""

        return to_ST_Angle(str(self.attrib['val']))


ST_FixedAngle = NewType('ST_FixedAngle', float)
"""固定范围角度

20.1.10.23 ST_FixedAngle

Fixed Angle

这个简单类型表示以 60000 分之一度为单位的固定范围角度。范围从（-90，90 度）。

这个简单类型的内容是对 ST_Angle 数据类型（§20.1.10.3）的限制。

这个简单类型还指定了以下限制:

- 该简单类型的最小值大于 -5400000。
- 该简单类型的最大值小于 5400000。
"""


def to_ST_FixedAngle(val: str) -> ST_FixedAngle:
    int_val = int(val)

    if not (-5400000 < int_val < 5400000):
        msg = f'预期外的值: {val}'
        raise OxmlAttributeValidateError(msg)

    return ST_FixedAngle(to_ST_Angle(val))


ST_PositiveFixedAngle = NewType('ST_PositiveFixedAngle', float)
"""正固定角度

20.1.10.44 Positive Fixed Angle

这个简单类型表示一个正角度，以60000分之一度为单位。范围从 [0, 360度)。

这个简单类型的内容是对 ST_Angle 数据类型（§20.1.10.3）的限制。

此外，这个简单类型还指定了以下限制:

- 该简单类型的最小值大于或等于0。
- 该简单类型的最大值小于21600000。
"""


def to_ST_PositiveFixedAngle(val: str) -> ST_PositiveFixedAngle:
    """正固定角度

    20.1.10.44

    Positive Fixed Angle

    这个简单的类型表示 60000 度的正角。 范围从 [0, 360 度)
    """

    int_val = int(val)

    if not (0 <= int_val < 21600000):
        msg = f'预期外的值: {val}'
        raise OxmlAttributeValidateError(msg)

    return ST_PositiveFixedAngle(to_ST_Angle(val))


class CT_PositiveFixedAngle(OxmlBaseElement):
    """正固定偏移
    20.1.2.3.14

    Hue

    该元素指定具有指定色调的输入颜色，但其饱和度和亮度不变。
    """

    @property
    def value(self) -> ST_PositiveFixedAngle:
        """指定要与输入颜色的色调分量一起使用的实际角度值。

        <xsd:attribute name="val" type="ST_PositiveFixedAngle" use="required"/>
        """

        return to_ST_PositiveFixedAngle(str(self.attrib['val']))


# <xsd:union memberTypes="s:ST_Percentage"/>
# 20.1.10.40 ST_Percentage (Percentage)
# 这个简单类型指定其内容将包含百分比值。 有关详细信息，请参阅联合的成员类型。
# ST_Percentage 简单类型 (§22.9.2.9).
ST_Percentage = s_ST_Percentage
"""百分比

20.1.10.40 ST_Percentage

这个简单类型指定其内容将包含一个百分比值。有关详细信息，请参阅联合成员类型。

这个简单类型是以下类型的联合体:

- ST_Percentage 简单类型（§22.9.2.9）。
"""

to_ST_Percentage = s_to_ST_Percentage

# <xsd:restriction base="xsd:int"/>
ST_PercentageDecimal = NewType('ST_PercentageDecimal', float)


class CT_Percentage(OxmlBaseElement):
    """百分比
    20.1.2.3.28

    20.1.2.3.4 blue (Blue)
    20.1.2.3.5 blueMod (Blue Modulation)
    20.1.2.3.6 blueOff (Blue Offset)
    20.1.2.3.10 green (Green)
    20.1.2.3.11 greenMod (Green Modulation)
    20.1.2.3.12 greenOff (Green Offset)
    20.1.2.3.19 lum (Luminance)
    20.1.2.3.20 lumMod (Luminance Modulation)
    20.1.2.3.21 lumOff (Luminance Offset)
    20.1.2.3.23 red (Red)
    20.1.2.3.24 redMod (Red Modulation)
    20.1.2.3.25 redOff (Red Offset)
    20.1.2.3.26 sat (Saturation)
    20.1.2.3.27 satMod (Saturation Modulation)
    20.1.2.3.28 satOff (Saturation Offset)

    很多元素都是该通用类型
    """

    @property
    def value(self) -> ST_Percentage:
        """

        <xsd:attribute name="val" type="ST_PositiveFixedAngle" use="required"/>
        """

        return to_ST_Percentage(str(self.attrib['val']))


ST_PositivePercentage = s_ST_PositivePercentage
"""带符号的正百分比

20.1.10.46 ST_PositivePercentage

这个简单类型指定其内容将包含一个正百分比值。有关详细信息，请参阅该联合的成员类型。

这个简单类型是以下类型的联合:

- ST_PositivePercentage 简单类型（§22.9.2.11）。
"""


def to_ST_PositivePercentage(val: str) -> ST_PositivePercentage:
    return s_to_ST_PositivePercentage(val)


class CT_PositivePercentage(OxmlBaseElement):
    """正百分比

    20.1.2.3.2 alphaMod (Alpha Modulation)
    20.1.2.3.15 hueMod (Hue Modulate)

    很多元素都是该通用类型
    """

    @property
    def value(self) -> ST_PositivePercentage:
        """

        <xsd:attribute name="val" type="ST_PositivePercentage" use="required"/>
        """

        return to_ST_PositivePercentage(str(self.attrib['val']))


class ST_PositivePercentageDecimal(ST_BaseType[AnyStr, int]):
    """ """

    def _validate(self: Self) -> None:
        val = int(utils.AnyStrToStr(self._val))

        if val < 0:
            msg = '值不应小于0'
            raise OxmlAttributeValidateError(msg)

        self._python_val = val


ST_FixedPercentage = s_ST_FixedPercentage
"""固定百分比

20.1.10.24 ST_FixedPercentage

这个简单类型表示从负一百到正一百百分比的固定百分比。有关详细信息，请参阅联合成员类型。这个简单类型是以下类型的联合体:

ST_FixedPercentage 简单类型（§22.9.2.3）。
"""

to_ST_FixedPercentage = s_to_ST_FixedPercentage


class CT_FixedPercentage(OxmlBaseElement):
    """固定百分比

    20.1.2.3.3 alphaOff (Alpha Offset)
    """

    @property
    def value(self) -> ST_FixedPercentage:
        """

        <xsd:attribute name="val" type="ST_FixedPercentage" use="required"/>
        """

        return to_ST_FixedPercentage(str(self.attrib['val']))


class ST_FixedPercentageDecimal(ST_BaseType[AnyStr, int]):
    """aaa"""

    def _validate(self: Self) -> None:
        val = int(utils.AnyStrToStr(self._val))

        if not (-100000 < val < 100000):
            msg = '值应在区间: -100000 至 100000 内'
            raise OxmlAttributeValidateError(msg)

        self._python_val = val


ST_PositiveFixedPercentage = s_ST_PositiveFixedPercentage
"""正百分比值

20.1.10.45 ST_PositiveFixedPercentage

这个简单类型指定其内容将包含一个从零到百分之百的正百分比值。有关详细信息，请参阅该联合的成员类型。

这个简单类型是以下类型的联合:

- ST_PositiveFixedPercentage 简单类型（§22.9.2.10）。
"""

to_ST_PositiveFixedPercentage = s_to_ST_PositiveFixedPercentage


class ST_PositiveFixedPercentageDecimal(ST_BaseType[AnyStr, int]):
    """aaa"""

    def _validate(self: Self) -> None:
        val = int(utils.AnyStrToStr(self._val))

        if not (0 < val < 100000):
            msg = '值应在区间: 0 至 100000 内'
            raise OxmlAttributeValidateError(msg)

        self._python_val = val


class CT_PositiveFixedPercentage(OxmlBaseElement):
    """正固定百分比

    20.1.2.3.1 alpha (Alpha)
    20.1.2.3.31 shade (Shade)
    20.1.2.3.34 tint (Tint)  # tint 有冲突 与 CT_TintEffect 类
    """

    @property
    def value(self) -> ST_PositiveFixedPercentage:
        """

        <xsd:attribute name="val" type="ST_PositiveFixedPercentage" use="required"/>
        """

        return to_ST_PositiveFixedPercentage(str(self.attrib['val']))


class CT_Ratio(OxmlBaseElement):
    """比率

    20.1.2.2.38 sx (Horizontal Ratio)
    20.1.2.2.39 sy (Vertical Ratio)
    """

    @property
    def numerator(self) -> XSD_Long:
        """指定方程中使用的分子。

        <xsd:attribute name="n" type="xsd:long" use="required"/>
        """

        return XSD_Long(int(self.attrib['n']))

    @property
    def denominator(self) -> int:
        """指定方程中使用的分母。

        <xsd:attribute name="n" type="xsd:long" use="required"/>
        """

        return XSD_Long(int(self.attrib['d']))


class CT_Point2D(OxmlBaseElement):
    """2D中点

    20.1.2.2.38 sx (Horizontal Ratio)
    20.1.2.2.39 sy (Vertical Ratio)
    20.4.2.13 simplePos (简单定位坐标)

    20.4.2.9 lineTo (包裹多边形线结束位置)
    """

    @property
    def x_val(self) -> ST_Coordinate:
        """x（X轴坐标）

        命名空间：http://purl.oclc.org/ooxml/drawingml/main

        指定x轴上的坐标。该坐标的原点由父XML元素指定。

        【示例：考虑绘图对象的基本包裹多边形上的以下点：

        <… x="0" y="100" />

        x属性定义了x坐标为0。示例结束】

        该属性的可能值由ST_Coordinate简单类型（[§20.1.10.16]）定义。

        <xsd:attribute name="n" type="xsd:long" use="required"/>
        """
        return to_ST_Coordinate(str(self.attrib['x']))

    @property
    def y_val(self) -> ST_Coordinate:
        """y（Y轴坐标）

        命名空间：http://purl.oclc.org/ooxml/drawingml/main

        指定y轴上的坐标。该坐标的原点由父XML元素指定。

        【示例：考虑绘图对象的基本包裹多边形上的以下点：

        <… x="0" y="100" />

        y属性定义了y坐标为100。示例结束】

        该属性的可能值由ST_Coordinate简单类型（[§20.1.10.16]）定义。

        <xsd:attribute name="n" type="xsd:long" use="required"/>
        """
        return to_ST_Coordinate(str(self.attrib['y']))


class CT_PositiveSize2D(OxmlBaseElement):
    """正的尺寸大小, 2D中

    19.2.1.22 notesSz (Notes Slide Size)
    19.2.2.3 gridSpacing (Grid Spacing)
    20.1.7.1 chExt (Child Extents)
    20.1.7.3 ext (Extents)
    20.4.2.7 extent (Drawing Object Size)
    20.5.2.14 ext (Shape Extent)
    21.3.2.10 ext (Shape Extent)
    """

    @property
    def cx_val(self) -> ST_PositiveCoordinate:
        """指定方程中使用的分子。

        <xsd:attribute name="cx" type="ST_PositiveCoordinate" use="required"/>
        """
        return to_ST_PositiveCoordinate(str(self.attrib['cx']))

    @property
    def cy_val(self) -> ST_PositiveCoordinate:
        """指定方程中使用的分子。

        <xsd:attribute name="cy" type="ST_PositiveCoordinate" use="required"/>
        """
        return to_ST_PositiveCoordinate(str(self.attrib['cy']))


class CT_ComplementTransform(OxmlBaseElement):
    """补码变换

    20.1.2.3.7 comp (Complement)

    该元素指定渲染的颜色应该是其输入颜色的补色，补色是这样定义的。
    如果两种颜色混合时产生灰色阴影，则称为互补色。
    例如，红色的补色是 RGB (255, 0, 0)，而青色是 RGB (0, 255, 255)。
    """



class CT_InverseTransform(OxmlBaseElement):
    """逆变换

    20.1.2.3.17 inv (Inverse)

    该元素指定其输入颜色的反色。
    """



class CT_GrayscaleTransform(OxmlBaseElement):
    """灰度变换

    20.1.2.3.9 gray (Gray)

    该元素指定其输入颜色的灰度，考虑红、绿、蓝原色的相对强度。
    """



class CT_GammaTransform(OxmlBaseElement):
    """伽玛变换

    20.1.2.3.8 gamma (Gamma)

    该元素指定生成应用程序渲染的输出颜色应该是输入颜色的 sRGB gamma 偏移。
    """



class CT_InverseGammaTransform(OxmlBaseElement):
    """逆伽玛变换

    20.1.2.3.18 invGamma (Inverse Gamma)

    该元素指定生成应用程序渲染的输出颜色应该是输入颜色的逆 sRGB gamma 偏移。
    """



class EG_ColorTransform(OxmlBaseElement):
    """颜色变换"""

    # color_trans_tags = (
    # qn("a:tint"),  # CT_PositiveFixedPercentage
    # qn("a:shade"),  # CT_PositiveFixedPercentage
    # qn("a:comp"),  # CT_ComplementTransform
    # qn("a:inv"),  # CT_InverseTransform
    # qn("a:gray"),  # CT_GrayscaleTransform
    # qn("a:alpha"),  # CT_PositiveFixedPercentage
    # qn("a:alphaOff"),  # CT_PositiveFixedPercentage
    # qn("a:alphaMod"),  # CT_PositivePercentage
    # qn("a:hue"),  # CT_PositiveFixedAngle
    # qn("a:hueOff"),  # CT_Angle
    # qn("a:hueMod"),  # CT_PositivePercentage
    # qn("a:sat"),  # CT_Percentage
    # qn("a:satOff"),  # CT_Percentage
    # qn("a:satMod"),  # CT_Percentage
    # qn("a:lum"),  # CT_Percentage
    # qn("a:lumOff"),  # CT_Percentage
    # qn("a:lumMod"),  # CT_Percentage
    # qn("a:red"),  # CT_Percentage
    # qn("a:redOff"),  # CT_Percentage
    # qn("a:redMod"),  # CT_Percentage
    # qn("a:green"),  # CT_Percentage
    # qn("a:greenOff"),  # CT_Percentage
    # qn("a:greenMod"),  # CT_Percentage
    # qn("a:blue"),  # CT_Percentage
    # qn("a:blueOff"),  # CT_Percentage
    # qn("a:blueMod"),  # CT_Percentage
    # qn("a:gamma"),  # CT_GammaTransform
    # qn("a:invGamma"),  # CT_InverseGammaTransform
    # )

    # List[
    #     Union[
    #         CT_PositiveFixedPercentage,
    #         CT_ComplementTransform,
    #         CT_InverseTransform,
    #         CT_GrayscaleTransform,
    #         CT_PositivePercentage,
    #         CT_PositiveFixedAngle,
    #         CT_Angle,
    #         CT_Percentage,
    #         CT_GammaTransform,
    #         CT_InverseGammaTransform,
    #     ]
    # ]

    @property
    def tint(self) -> Optional[CT_PositiveFixedPercentage]:
        return getattr(self, qn('a:tint'), None)

    @property
    def shade(self) -> Optional[CT_PositiveFixedPercentage]:
        return getattr(self, qn('a:shade'), None)

    @property
    def comp(self) -> Optional[CT_ComplementTransform]:
        return getattr(self, qn('a:comp'), None)

    @property
    def inv(self) -> Optional[CT_InverseTransform]:
        return getattr(self, qn('a:inv'), None)

    @property
    def gray(self) -> Optional[CT_GrayscaleTransform]:
        return getattr(self, qn('a:gray'), None)

    @property
    def alpha(self) -> Optional[CT_PositiveFixedPercentage]:
        return getattr(self, qn('a:alpha'), None)

    @property
    def alpha_off(self) -> Optional[CT_PositiveFixedPercentage]:
        return getattr(self, qn('a:alphaOff'), None)

    @property
    def alpha_mod(self) -> Optional[CT_PositivePercentage]:
        return getattr(self, qn('a:alphaMod'), None)

    @property
    def hue(self) -> Optional[CT_PositiveFixedAngle]:
        return getattr(self, qn('a:hue'), None)

    @property
    def hue_off(self) -> Optional[CT_Angle]:
        return getattr(self, qn('a:hueOff'), None)

    @property
    def hue_mod(self) -> Optional[CT_PositivePercentage]:
        return getattr(self, qn('a:hueMod'), None)

    @property
    def sat(self) -> Optional[CT_Percentage]:
        return getattr(self, qn('a:sat'), None)

    @property
    def sat_off(self) -> Optional[CT_Percentage]:
        return getattr(self, qn('a:satOff'), None)

    @property
    def sat_mod(self) -> Optional[CT_Percentage]:
        return getattr(self, qn('a:satMod'), None)

    @property
    def lum(self) -> Optional[CT_Percentage]:
        return getattr(self, qn('a:lum'), None)

    @property
    def lum_off(self) -> Optional[CT_Percentage]:
        return getattr(self, qn('a:lumOff'), None)

    @property
    def lum_mod(self) -> Optional[CT_Percentage]:
        return getattr(self, qn('a:lumMod'), None)

    @property
    def red(self) -> Optional[CT_Percentage]:
        return getattr(self, qn('a:red'), None)

    @property
    def red_off(self) -> Optional[CT_Percentage]:
        return getattr(self, qn('a:redOff'), None)

    @property
    def red_mod(self) -> Optional[CT_Percentage]:
        return getattr(self, qn('a:redMod'), None)

    @property
    def green(self) -> Optional[CT_Percentage]:
        return getattr(self, qn('a:green'), None)

    @property
    def green_off(self) -> Optional[CT_Percentage]:
        return getattr(self, qn('a:greenOff'), None)

    @property
    def green_mod(self) -> Optional[CT_Percentage]:
        return getattr(self, qn('a:greenMod'), None)

    @property
    def blue(self) -> Optional[CT_Percentage]:
        return getattr(self, qn('a:blue'), None)

    @property
    def blue_off(self) -> Optional[CT_Percentage]:
        return getattr(self, qn('a:blueOff'), None)

    @property
    def blue_mod(self) -> Optional[CT_Percentage]:
        """蓝色百分占比"""
        return getattr(self, qn('a:blueMod'), None)

    @property
    def gamma(self) -> Optional[CT_GammaTransform]:
        """伽玛变换

        20.1.2.3.8 gamma (Gamma)

        该元素指定生成应用程序渲染的输出颜色应该是输入颜色的 sRGB gamma 偏移。
        """
        return getattr(self, qn('a:gamma'), None)

    @property
    def inv_gamma(self) -> Optional[CT_InverseGammaTransform]:
        """逆伽玛变换

        20.1.2.3.18 invGamma (Inverse Gamma)

        该元素指定生成应用程序渲染的输出颜色应该是输入颜色的逆 sRGB gamma 偏移。
        """
        return getattr(self, qn('a:invGamma'), None)


class CT_ScRgbColor(EG_ColorTransform):
    """RGB 颜色模型 - 百分比变体

    20.1.2.3.30 scrgbClr (RGB Color Model - Percentage Variant)

    该元素使用红、绿、蓝 RGB 颜色模型指定颜色。 每个分量（红色、绿色和蓝色）均表示为 0% 到 100% 的百分比。 假设线性伽马为 1.0。

    指定红色级别，以相对于输入颜色的偏移增加或减少百分比表示。
    """

    # @property
    # def color_transform(self)-> List[
    #     Union[
    #         CT_PositiveFixedPercentage,
    #         CT_ComplementTransform,
    #         CT_InverseTransform,
    #         CT_GrayscaleTransform,
    #         CT_PositivePercentage,
    #         CT_PositiveFixedAngle,
    #         CT_Angle,
    #         CT_Percentage,
    #         CT_GammaTransform,
    #         CT_InverseGammaTransform,
    #     ]
    # ]:
    #     """颜色变换

    #     <xsd:sequence>
    #         <xsd:group ref="EG_ColorTransform" minOccurs="0" maxOccurs="unbounded"/>
    #     </xsd:sequence>
    #     """

    #     return self.choice_and_more(*self.color_trans_tags)

    @property
    def r(self) -> ST_Percentage:
        """红色占比"""

        return to_ST_Percentage(str(self.attrib['r']))

    @property
    def g(self) -> ST_Percentage:
        """绿色占比"""

        return to_ST_Percentage(str(self.attrib['g']))

    @property
    def b(self) -> ST_Percentage:
        """蓝色占比"""

        return to_ST_Percentage(str(self.attrib['b']))


class CT_SRgbColor(EG_ColorTransform):
    """RGB 颜色模型 - 十六进制变体

    20.1.2.3.32 srgbClr (RGB Color Model - Hex Variant)

    该元素使用红、绿、蓝 RGB 颜色模型指定颜色。 红色、绿色和蓝色表示为十六进制数字序列 RRGGBB。 使用 2.2 的感知伽玛。

    指定红色级别，以相对于输入颜色的偏移增加或减少百分比表示
    """

    # @property
    # def color_transform(self)-> List[
    #     Union[
    #         CT_PositiveFixedPercentage,
    #         CT_ComplementTransform,
    #         CT_InverseTransform,
    #         CT_GrayscaleTransform,
    #         CT_PositivePercentage,
    #         CT_PositiveFixedAngle,
    #         CT_Angle,
    #         CT_Percentage,
    #         CT_GammaTransform,
    #         CT_InverseGammaTransform,
    #     ]
    # ]:
    #     """颜色变换

    #     <xsd:sequence>
    #         <xsd:group ref="EG_ColorTransform" minOccurs="0" maxOccurs="unbounded"/>
    #     </xsd:sequence>
    #     """

    #     return self.choice_and_more(*self.color_trans_tags)

    @property
    def value(self) -> ST_HexColorRGB:
        """实际颜色值。 表示为十六进制数字 RRGGBB 序列。"""

        return s_to_ST_HexColorRGB(str(self.attrib['val']))


class CT_HslColor(EG_ColorTransform):
    """色相、饱和度、亮度颜色模型

    20.1.2.3.13 hslClr (Hue, Saturation, Luminance Color Model)

    该元素使用 HSL 颜色模型指定颜色。 假设感知伽玛值为 2.2。
    """

    # @property
    # def color_transform(self)-> List[
    #     Union[
    #         CT_PositiveFixedPercentage,
    #         CT_ComplementTransform,
    #         CT_InverseTransform,
    #         CT_GrayscaleTransform,
    #         CT_PositivePercentage,
    #         CT_PositiveFixedAngle,
    #         CT_Angle,
    #         CT_Percentage,
    #         CT_GammaTransform,
    #         CT_InverseGammaTransform,
    #     ]
    # ]:
    #     """颜色变换

    #     <xsd:sequence>
    #         <xsd:group ref="EG_ColorTransform" minOccurs="0" maxOccurs="unbounded"/>
    #     </xsd:sequence>
    #     """

    #     return self.choice_and_more(*self.color_trans_tags)

    @property
    def attr_hue(self) -> ST_PositiveFixedAngle:
        """色相

        <xsd:attribute name="hue" type="ST_PositiveFixedAngle" use="required"/>
        """

        return to_ST_PositiveFixedAngle(str(self.attrib['hue']))

    @property
    def attr_sat(self) -> ST_Percentage:
        """饱和度

        <xsd:attribute name="sat" type="ST_Percentage" use="required"/>
        """

        return to_ST_Percentage(str(self.attrib['sat']))

    @property
    def attr_lum(self) -> ST_Percentage:
        """亮度

        <xsd:attribute name="sat" type="ST_Percentage" use="required"/>
        """

        return to_ST_Percentage(str(self.attrib['lum']))


class ST_SystemColorVal(ST_BaseEnumType):
    """系统颜色值

    20.1.10.58 ST_SystemColorVal (System Color Value)

    这个简单类型指定系统颜色值。 该颜色基于该颜色当前在查看文档的系统中具有的值。
    """

    ScrollBar = 'scrollBar'
    """指定滚动条灰色区域的颜色。"""

    Background = 'background'
    """指定桌面背景颜色。"""

    ActiveCaption = 'activeCaption'
    """指定活动窗口标题栏颜色，特别是如果启用了渐变效果，则为渐变的标题栏的左侧颜色。"""

    InactiveCaption = 'inactiveCaption'
    """指定非活动窗口标题栏的颜色，特别是如果启用了渐变效果，则为渐变的标题栏的左侧颜色。"""

    Menu = 'menu'
    """指定菜单的背景颜色。"""

    Window = 'window'
    """指定窗口背景颜色。"""

    WindowFrame = 'windowFrame'
    """指定窗口框架的颜色。"""

    MenuText = 'menuText'
    """指定菜单中文本的颜色。"""

    WindowText = 'windowText'
    """指定窗口中文本的颜色。"""

    CaptionText = 'captionText'
    """指定标题、大小框和滚动条箭头框的文本颜色。"""

    ActiveBorder = 'activeBorder'
    """指定活动窗口边框颜色。"""

    InactiveBorder = 'inactiveBorder'
    """指定非活动窗口边框的颜色。"""

    AppWorkspace = 'appWorkspace'
    """指定多文档界面（MDI）应用程序的背景颜色。"""

    Highlight = 'highlight'
    """指定在控件中选择的项目的颜色。"""

    HighlightText = 'highlightText'
    """指定在控件中选择的项目的文本颜色。"""

    BtnFace = 'btnFace'
    """指定三维显示元素和对话框框背景的表面颜色。"""

    BtnShadow = 'btnShadow'
    """指定三维显示元素的阴影颜色（背离光源的边缘）。"""

    GrayText = 'grayText'
    """指定灰色（禁用）文本。如果当前显示驱动程序不支持纯灰色，则此颜色设置为0。"""

    BtnText = 'btnText'
    """指定按下按钮上的文本颜色。"""

    InactiveCaptionText = 'inactiveCaptionText'
    """指定非活动标题中的文本颜色。"""

    BtnHighlight = 'btnHighlight'
    """指定三维显示元素的高亮颜色（面向光源的边缘）。"""

    ThreedDkShadow = '3dDkShadow'
    """指定三维显示元素的深色阴影颜色。"""

    ThreedLight = '3dLight'
    """指定三维显示元素的亮色（面向光源的边缘）。"""

    InfoText = 'infoText'
    """指定工具提示控件的文本颜色。"""

    InfoBk = 'infoBk'
    """指定工具提示控件的背景颜色。"""

    HotLight = 'hotLight'
    """指定超链接或热跟踪项的颜色。"""

    GradientActiveCaption = 'gradientActiveCaption'
    """指定活动窗口标题栏渐变的右侧颜色。"""

    GradientInactiveCaption = 'gradientInactiveCaption'
    """指定非活动窗口标题栏渐变的右侧颜色。"""

    MenuHighlight = 'menuHighlight'
    """指定在菜单以平面样式显示时用于突出显示菜单项的颜色。"""

    MenuBar = 'menuBar'
    """指定菜单以平面样式显示时菜单栏的背景颜色。"""


class CT_SystemColor(EG_ColorTransform):
    """系统颜色

    20.1.2.3.33 sysClr (System Color)

    该元素指定绑定到预定义操作系统元素的颜色
    """

    # @property
    # def color_transform(self)-> List[
    #     Union[
    #         CT_PositiveFixedPercentage,
    #         CT_ComplementTransform,
    #         CT_InverseTransform,
    #         CT_GrayscaleTransform,
    #         CT_PositivePercentage,
    #         CT_PositiveFixedAngle,
    #         CT_Angle,
    #         CT_Percentage,
    #         CT_GammaTransform,
    #         CT_InverseGammaTransform,
    #     ]
    # ]:
    #     """颜色变换

    #     <xsd:sequence>
    #         <xsd:group ref="EG_ColorTransform" minOccurs="0" maxOccurs="unbounded"/>
    #     </xsd:sequence>
    #     """

    #     return self.choice_and_more(*self.color_trans_tags)

    @property
    def value(self) -> ST_SystemColorVal:
        """指定系统颜色值。"""

        return ST_SystemColorVal(str(self.attrib['val']))

    @property
    def last_color(self) -> Optional[ST_HexColorRGB]:
        """指定生成应用程序最后计算的颜色值。"""

        clr = self.attrib.get('lastClr')

        return s_to_ST_HexColorRGB(str(clr)) if clr is not None else None


class ST_SchemeColorVal(ST_BaseEnumType):
    """方案颜色值

    20.1.10.54 ST_SchemeColorVal (Scheme Color)

    这个简单类型表示方案颜色值。
    """

    Background1 = 'bg1'
    """语义背景颜色"""

    Text1 = 'tx1'
    """语义文本颜色"""

    Background2 = 'bg2'
    """语义附加背景颜色"""

    Text2 = 'tx2'
    """语义附加文本颜色"""

    Accent1 = 'accent1'
    """额外方案颜色1"""

    Accent2 = 'accent2'
    """额外方案颜色2"""

    Accent3 = 'accent3'
    """额外方案颜色3"""

    Accent4 = 'accent4'
    """额外方案颜色4"""

    Accent5 = 'accent5'
    """额外方案颜色5"""

    Accent6 = 'accent6'
    """额外方案颜色6"""

    Hyperlink = 'hlink'
    """常规超链接颜色"""

    FollowedHyperlink = 'folHlink'
    """跟随的超链接颜色"""

    Placeholder = 'phClr'
    """主题定义中使用的颜色，表示使用样式的颜色。"""

    Dark1 = 'dk1'
    """主深色1"""

    Light1 = 'lt1'
    """主浅色1"""

    Dark2 = 'dk2'
    """主深色2"""

    Light2 = 'lt2'
    """主浅色2"""


class CT_SchemeColor(EG_ColorTransform):
    """方案颜色

    20.1.2.3.29 schemeClr (Scheme Color)

    该元素指定与用户主题绑定的颜色。 与定义颜色的所有元素一样，可以将颜色变换列表应用于定义的基色。
    """

    # @property
    # def color_transform(self)-> List[
    #     Union[
    #         CT_PositiveFixedPercentage,
    #         CT_ComplementTransform,
    #         CT_InverseTransform,
    #         CT_GrayscaleTransform,
    #         CT_PositivePercentage,
    #         CT_PositiveFixedAngle,
    #         CT_Angle,
    #         CT_Percentage,
    #         CT_GammaTransform,
    #         CT_InverseGammaTransform,
    #     ]
    # ]:
    #     """颜色变换

    #     <xsd:sequence>
    #         <xsd:group ref="EG_ColorTransform" minOccurs="0" maxOccurs="unbounded"/>
    #     </xsd:sequence>
    #     """

    #     return self.choice_and_more(*self.color_trans_tags)

    @property
    def value(self) -> ST_SchemeColorVal:
        """指定所需的方案(schema)。"""

        return ST_SchemeColorVal(str(self.attrib['val']))


class ST_PresetColorVal(ST_BaseEnumType):
    """预设颜色值

    20.1.10.48 ST_PresetColorVal (Preset Color Value)

    这个简单的类型表示预设的颜色值。
    """

    AliceBlue = 'aliceBlue'
    """爱丽丝蓝(Alice Blue) """

    AntiqueWhite = 'antiqueWhite'
    """古董白(Antique White)"""

    Aqua = 'aqua'
    """水绿(Aqua) """

    Aquamarine = 'aquamarine'
    """碧绿(Aquamarine) """

    Azure = 'azure'
    """天蓝(Azure) """

    Beige = 'beige'
    """米色(Beige) """

    Bisque = 'bisque'
    """橙黄(Bisque) """

    Black = 'black'
    """黑色(Black) """

    BlanchedAlmond = 'blanchedAlmond'
    """杏仁白(Blanched Almond) """

    Blue = 'blue'
    """蓝色(Blue)"""

    BlueViolet = 'blueViolet'
    Brown = 'brown'
    BurlyWood = 'burlyWood'
    CadetBlue = 'cadetBlue'
    Chartreuse = 'chartreuse'
    Chocolate = 'chocolate'
    Coral = 'coral'
    CornflowerBlue = 'cornflowerBlue'
    Cornsilk = 'cornsilk'
    Crimson = 'crimson'
    Cyan = 'cyan'
    DarkBlue = 'darkBlue'
    DarkCyan = 'darkCyan'
    DarkGoldenrod = 'darkGoldenrod'
    DarkGray = 'darkGray'
    DarkGrey = 'darkGrey'
    DarkGreen = 'darkGreen'
    DarkKhaki = 'darkKhaki'
    DarkMagenta = 'darkMagenta'
    DarkOliveGreen = 'darkOliveGreen'
    DarkOrange = 'darkOrange'
    DarkOrchid = 'darkOrchid'
    DarkRed = 'darkRed'
    DarkSalmon = 'darkSalmon'
    DarkSeaGreen = 'darkSeaGreen'
    DarkSlateBlue = 'darkSlateBlue'
    DarkSlateGray = 'darkSlateGray'
    DarkSlateGrey = 'darkSlateGrey'
    DarkTurquoise = 'darkTurquoise'
    DarkViolet = 'darkViolet'
    DkBlue = 'dkBlue'
    DkCyan = 'dkCyan'
    DkGoldenrod = 'dkGoldenrod'
    DkGray = 'dkGray'
    DkGrey = 'dkGrey'
    DkGreen = 'dkGreen'
    DkKhaki = 'dkKhaki'
    DkMagenta = 'dkMagenta'
    DkOliveGreen = 'dkOliveGreen'
    DkOrange = 'dkOrange'
    DkOrchid = 'dkOrchid'
    DkRed = 'dkRed'
    DkSalmon = 'dkSalmon'
    DkSeaGreen = 'dkSeaGreen'
    DkSlateBlue = 'dkSlateBlue'
    DkSlateGray = 'dkSlateGray'
    DkSlateGrey = 'dkSlateGrey'
    DkTurquoise = 'dkTurquoise'
    DkViolet = 'dkViolet'
    DeepPink = 'deepPink'
    DeepSkyBlue = 'deepSkyBlue'
    DimGray = 'dimGray'
    DimGrey = 'dimGrey'
    DodgerBlue = 'dodgerBlue'
    Firebrick = 'firebrick'
    FloralWhite = 'floralWhite'
    ForestGreen = 'forestGreen'
    Fuchsia = 'fuchsia'
    Gainsboro = 'gainsboro'
    GhostWhite = 'ghostWhite'
    Gold = 'gold'
    Goldenrod = 'goldenrod'
    Gray = 'gray'
    Grey = 'grey'
    Green = 'green'
    GreenYellow = 'greenYellow'
    Honeydew = 'honeydew'
    HotPink = 'hotPink'
    HndianRed = 'indianRed'
    Indigo = 'indigo'
    Ivory = 'ivory'
    Khaki = 'khaki'
    Lavender = 'lavender'
    LavenderBlush = 'lavenderBlush'
    LawnGreen = 'lawnGreen'
    LemonChiffon = 'lemonChiffon'
    LightBlue = 'lightBlue'
    LightCoral = 'lightCoral'
    LightCyan = 'lightCyan'
    LightGoldenrodYellow = 'lightGoldenrodYellow'
    LightGray = 'lightGray'
    LightGrey = 'lightGrey'
    LightGreen = 'lightGreen'
    LightPink = 'lightPink'
    LightSalmon = 'lightSalmon'
    LightSeaGreen = 'lightSeaGreen'
    LightSkyBlue = 'lightSkyBlue'
    LightSlateGray = 'lightSlateGray'
    LightSlateGrey = 'lightSlateGrey'
    LightSteelBlue = 'lightSteelBlue'
    LightYellow = 'lightYellow'
    LtBlue = 'ltBlue'
    LtCoral = 'ltCoral'
    LtCyan = 'ltCyan'
    LtGoldenrodYellow = 'ltGoldenrodYellow'
    LtGray = 'ltGray'
    LtGrey = 'ltGrey'
    LtGreen = 'ltGreen'
    LtPink = 'ltPink'
    LtSalmon = 'ltSalmon'
    LtSeaGreen = 'ltSeaGreen'
    LtSkyBlue = 'ltSkyBlue'
    LtSlateGray = 'ltSlateGray'
    LtSlateGrey = 'ltSlateGrey'
    LtSteelBlue = 'ltSteelBlue'
    LtYellow = 'ltYellow'
    Lime = 'lime'
    LimeGreen = 'limeGreen'
    Linen = 'linen'
    Magenta = 'magenta'
    Maroon = 'maroon'
    MedAquamarine = 'medAquamarine'
    MedBlue = 'medBlue'
    MedOrchid = 'medOrchid'
    MedPurple = 'medPurple'
    MedSeaGreen = 'medSeaGreen'
    MedSlateBlue = 'medSlateBlue'
    MedSpringGreen = 'medSpringGreen'
    MedTurquoise = 'medTurquoise'
    MedVioletRed = 'medVioletRed'
    MediumAquamarine = 'mediumAquamarine'
    MediumBlue = 'mediumBlue'
    MediumOrchid = 'mediumOrchid'
    MediumPurple = 'mediumPurple'
    MediumSeaGreen = 'mediumSeaGreen'
    MediumSlateBlue = 'mediumSlateBlue'
    MediumSpringGreen = 'mediumSpringGreen'
    MediumTurquoise = 'mediumTurquoise'
    MediumVioletRed = 'mediumVioletRed'
    MidnightBlue = 'midnightBlue'
    MintCream = 'mintCream'
    MistyRose = 'mistyRose'
    Moccasin = 'moccasin'
    NavajoWhite = 'navajoWhite'
    Navy = 'navy'
    OldLace = 'oldLace'
    Olive = 'olive'
    OliveDrab = 'oliveDrab'
    Orange = 'orange'
    OrangeRed = 'orangeRed'
    Orchid = 'orchid'
    PaleGoldenrod = 'paleGoldenrod'
    PaleGreen = 'paleGreen'
    PaleTurquoise = 'paleTurquoise'
    PaleVioletRed = 'paleVioletRed'
    PapayaWhip = 'papayaWhip'
    PeachPuff = 'peachPuff'
    Peru = 'peru'
    Pink = 'pink'
    Plum = 'plum'
    PowderBlue = 'powderBlue'
    Purple = 'purple'
    Red = 'red'
    RosyBrown = 'rosyBrown'
    RoyalBlue = 'royalBlue'
    SaddleBrown = 'saddleBrown'
    Salmon = 'salmon'
    SandyBrown = 'sandyBrown'
    SeaGreen = 'seaGreen'
    SeaShell = 'seaShell'
    Sienna = 'sienna'
    Silver = 'silver'
    SkyBlue = 'skyBlue'
    SlateBlue = 'slateBlue'
    SlateGray = 'slateGray'
    SlateGrey = 'slateGrey'
    Snow = 'snow'
    SpringGreen = 'springGreen'
    SteelBlue = 'steelBlue'
    Tan = 'tan'
    Teal = 'teal'
    Thistle = 'thistle'
    Tomato = 'tomato'
    Turquoise = 'turquoise'
    Violet = 'violet'
    Wheat = 'wheat'
    White = 'white'
    WhiteSmoke = 'whiteSmoke'
    Yellow = 'yellow'
    YellowGreen = 'yellowGreen'


class CT_PresetColor(EG_ColorTransform):
    """预设颜色值

    20.1.2.3.22 prstClr (Preset Color)

    该元素指定绑定到预定义颜色集合之一的颜色。
    """

    # @property
    # def color_transform(
    #     self,
    # ) -> List[
    #     Union[
    #         CT_PositiveFixedPercentage,
    #         CT_ComplementTransform,
    #         CT_InverseTransform,
    #         CT_GrayscaleTransform,
    #         CT_PositivePercentage,
    #         CT_PositiveFixedAngle,
    #         CT_Angle,
    #         CT_Percentage,
    #         CT_GammaTransform,
    #         CT_InverseGammaTransform,
    #     ]
    # ]:
    #     """颜色变换

    #     <xsd:sequence>
    #         <xsd:group ref="EG_ColorTransform" minOccurs="0" maxOccurs="unbounded"/>
    #     </xsd:sequence>
    #     """

    #     return self.choice_and_more(*self.color_trans_tags)  # type: ignore

    @property
    def value(self) -> ST_PresetColorVal:
        """指定实际的预设颜色值。"""

        return ST_PresetColorVal(str(self.attrib['val']))


class EG_OfficeArtExtensionList(OxmlBaseElement):
    """
    <xsd:group name="EG_OfficeArtExtensionList">
        <xsd:sequence>
            <xsd:element name="ext" type="CT_OfficeArtExtension" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
    </xsd:group>
    """

    @property
    def office_art_extension_lst(self) -> list[CT_OfficeArtExtension]:
        """返回扩展列表"""

        return self.findall(qn('a:ext'))  # type: ignore


class CT_OfficeArtExtensionList(EG_OfficeArtExtensionList):
    """很多扩展集合

    21.4.2.13 extLst (Extension List)

    该元素指定一个扩展列表，其中所有未来的扩展都在 ext 元素中定义。

    扩展列表以及相应的未来扩展用于扩展 DrawingML 框架的存储功能。 这允许在现有图表语法中本地存储各种新类型的数据。
    """

    @property
    def extension_list(self):
        """扩展元素列表"""

        return super().office_art_extension_lst


class CT_Scale2D(OxmlBaseElement):
    """查看比例

    19.2.2.13 scale (View Scale)

    此元素指定上次查看演示文稿时使用的视图缩放系数。
    """

    def scale_x(self) -> CT_Ratio:
        """x轴缩放"""

        return getattr(self, qn('a:sx'))

    def scale_y(self) -> CT_Ratio:
        """Y轴缩放"""

        return getattr(self, qn('a:sx'))


class CT_Transform2D(OxmlBaseElement):
    """2D变换

    19.3.1.53 xfrm (2D Transform for Graphic Frame)

        该元素指定要应用于相应图形框架的变换。 此变换应用于图形框架，就像应用于形状或组形状一样。

    20.1.7.6 xfrm (2D Transform for Individual Objects)
    20.5.2.36 xfrm (2D Transform for Graphic Frames)
    21.3.2.28 xfrm (Graphic Frame Transform)
    """

    @property
    def offset(self) -> Optional[CT_Point2D]:
        """偏移量"""

        return getattr(self, qn('a:off'), None)

    @property
    def ext(self) -> Optional[CT_PositiveSize2D]:
        """延伸量 ext"""

        return getattr(self, qn('a:ext'), None)

    @property
    def rotate(self) -> ST_Angle:
        """旋转

        指定图形框架的旋转。 指定此属性的单位驻留在下面引用的简单类型定义中.
        """

        rot = self.attrib.get('rot')

        if rot is None:
            return ST_Angle(0)

        return to_ST_Angle(str(rot))

    @property
    def flip_H(self) -> XSD_Boolean:
        """水平翻转

        这指定水平翻转。 当为 true 时，此属性定义形状围绕其边界框的中心水平翻转.
        """

        val = self.attrib.get('flipH')

        if val is None:
            return XSD_Boolean(False)

        return XSD_Boolean(to_xsd_bool(val))

    @property
    def flip_V(self) -> XSD_Boolean:
        """垂直翻转

        指定垂直翻转。 当为 true 时，此属性定义组围绕其边界框的中心垂直翻转.
        """

        val = self.attrib.get('flipV')

        if val is None:
            return XSD_Boolean(False)

        return XSD_Boolean(to_xsd_bool(val))


class CT_GroupTransform2D(OxmlBaseElement):
    """组变换

    20.1.7.5 xfrm (2D Transform for Grouped Objects)
    """

    @property
    def offset(self) -> Optional[CT_Point2D]:
        """偏移量"""

        return getattr(self, qn('a:off'), None)

    @property
    def ext(self) -> Optional[CT_PositiveSize2D]:
        """延伸量

        Extend
        """

        return getattr(self, qn('a:ext'), None)

    @property
    def child_offset(self) -> Optional[CT_Point2D]:
        """偏移量"""

        return getattr(self, qn('a:chOff'), None)

    @property
    def child_extend(self) -> Optional[CT_PositiveSize2D]:
        """延伸量"""

        return getattr(self, qn('a:chExt'), None)

    @property
    def rotate(self) -> ST_Angle:
        """角度"""

        rot = self.attrib.get('rot')

        if rot is None:
            return ST_Angle(0)

        return to_ST_Angle(str(rot))

    @property
    def flip_H(self) -> XSD_Boolean:
        """水平反转"""

        val = self.attrib.get('flipH')

        if val is None:
            return XSD_Boolean(False)

        return XSD_Boolean(to_xsd_bool(val))

    @property
    def flip_V(self) -> XSD_Boolean:
        """垂直反转"""

        val = self.attrib.get('flipV')

        if val is None:
            return XSD_Boolean(False)

        return XSD_Boolean(to_xsd_bool(val))


class CT_Point3D(OxmlBaseElement):
    """3维点

    20.1.5.1 anchor (Anchor Point)

    该元素指定 3D 空间中的一个点。 该点是空间中锚定背景平面的点。
    请参阅背景 (§20.1.5.2) 定义中的示例以获取此元素的深入说明。
    """

    def x_val(self) -> ST_Coordinate:
        """x轴位置"""

        return to_ST_Coordinate(str(self.attrib['x']))

    def y_val(self) -> ST_Coordinate:
        """x轴位置"""

        return to_ST_Coordinate(str(self.attrib['y']))

    def z_val(self) -> ST_Coordinate:
        """x轴位置"""

        return to_ST_Coordinate(str(self.attrib['z']))


class CT_Vector3D(OxmlBaseElement):
    """3D向量

    20.1.5.10 norm (Normal)

        该元素定义法向量。 更准确地说，该属性定义了一个垂直于背景平面表面的向量

    20.1.5.13 up (Up Vector)

        该元素定义了一个表示向上的向量。 更准确地说，该属性定义了一个相对于背景平面的面向上表示的向量
    """

    def distance_x(self):
        """3D 中沿 X 轴的距离

        Distance along X-axis in 3D
        """

        return to_ST_Coordinate(str(self.attrib['dx']))

    def distance_y(self) -> ST_Coordinate:
        """3D 中沿 Y 轴的距离

        Distance along Y-axis in 3D
        """

        return to_ST_Coordinate(str(self.attrib['dy']))

    def distance_z(self) -> ST_Coordinate:
        """3D 中沿 Y 轴的距离

        Distance along Y-axis in 3D
        """

        return to_ST_Coordinate(str(self.attrib['dz']))


class CT_SphereCoords(OxmlBaseElement):
    """球体坐标

    20.1.5.11 rot (Rotation)

        该元素定义 3D 空间中的旋转。 DrawingML 中的旋转是通过使用纬度坐标、经度坐标以及绕轴（作为纬度和经度坐标）的旋转来定义的。
    """

    @property
    def latitude(self) -> ST_PositiveFixedAngle:
        """定义旋转的纬度值。

        <xsd:attribute name="lat" type="ST_PositiveFixedAngle" use="required"/>
        """

        return to_ST_PositiveFixedAngle(str(self.attrib['lat']))

    @property
    def longitude(self) -> ST_PositiveFixedAngle:
        """定义旋转的经度值。

        <xsd:attribute name="lat" type="ST_PositiveFixedAngle" use="required"/>
        """

        return to_ST_PositiveFixedAngle(str(self.attrib['lon']))

    @property
    def revolution(self) -> ST_PositiveFixedAngle:
        """该属性定义了旋转中绕中心轴的旋转。

        <xsd:attribute name="lat" type="ST_PositiveFixedAngle" use="required"/>
        """

        return to_ST_PositiveFixedAngle(str(self.attrib['rev']))


class CT_RelativeRect(OxmlBaseElement):
    """相对矩形

    20.1.8.30 fillRect (Fill Rectangle)(填充矩形)

        该元素指定一个填充矩形。 当指定图像拉伸时，源矩形 srcRect 将缩放以适合指定的填充矩形。

        填充矩形的每条边都由相对于形状边界框的相应边的偏移百分比来定义。 正百分比指定插入，负百分比指定开始. [Note: 例如，左偏移 25% 指定填充矩形的左边缘位于边界框左边缘的右侧，偏移量等于边界框宽度的 25%. end note]

    20.1.8.31 fillToRect (Fill To Rectangle)
    20.1.8.55 srcRect (Source Rectangle) (源矩形)

        该元素指定用于填充的 blip 部分。

        源矩形的每条边均由距边界框相应边的偏移百分比定义。 正百分比指定插入，负百分比指定开始. [Note: 例如，左偏移 25% 指定源矩形的左边缘位于边界框左边缘的右侧，偏移量等于边界框宽度的 25%. end note]

    20.1.8.59 tileRect (Tile Rectangle)
    """

    @property
    def left_offset(self) -> ST_Percentage:
        """左偏移量

        指定矩形的左边缘。

        <xsd:attribute name="l" type="ST_Percentage" use="optional" default="0%"/>
        """

        l = self.attrib.get('l')
        l = '0%' if l is None else str(l)

        return to_ST_Percentage(l)

    @property
    def top_offset(self) -> ST_Percentage:
        """顶部偏移量

        指定矩形的顶部边缘。

        <xsd:attribute name="t" type="ST_Percentage" use="optional" default="0%"/>
        """

        t = self.attrib.get('t')
        t = '0%' if t is None else str(t)

        return to_ST_Percentage(t)

    @property
    def right_offset(self) -> ST_Percentage:
        """右偏移量

        指定矩形的右边缘。

        <xsd:attribute name="r" type="ST_Percentage" use="optional" default="0%"/>
        """

        r = self.attrib.get('r')
        r = '0%' if r is None else str(r)

        return to_ST_Percentage(r)

    @property
    def bottom_offset(self) -> ST_Percentage:
        """底部偏移量

        指定矩形的底部边缘。

        <xsd:attribute name="b" type="ST_Percentage" use="optional" default="0%"/>
        """

        b = self.attrib.get('b')
        b = '0%' if b is None else str(b)

        return to_ST_Percentage(b)


class ST_RectAlignment(ST_BaseEnumType):
    """矩形对齐方式

    20.1.10.53 ST_RectAlignment (Rectangle Alignments)

        这个简单的类型描述了如何定位两个矩形的相对位置。
    """

    TopLeft = 'tl'
    Top = 't'
    TopRight = 'tr'
    Left = 'l'
    Center = 'ctr'
    Right = 'r'
    BottomLeft = 'bl'
    Bottom = 'b'
    BottomRight = 'br'


class CT_Color(EG_ColorChoice):
    """颜色

    参考: 20.1.2.3 Colors

    17.3.2.6 color (Run Content Color) §A.1

        该元素指定用于在文档中显示此 Run 的内容的颜色。

        该颜色可以明确指定，或设置为允许消费者根据运行内容背后的背景颜色自动选择适当的颜色。

        如果此元素不存在，则默认值是保留样式层次结构中上一级别所应用的格式。
        如果此元素从未在样式层次结构中应用，则字符将设置为允许消费者根据运行内容背后的背景颜色自动选择适当的颜色。

    17.15.2.5 color (Frameset Splitter Color)   §A.1

        此元素指定此 WordprocessingML 文档中框架集中分隔线的颜色。 该元素只能在本文档的根框架集上使用，并且对于本文档中的所有嵌套框架集可以忽略。

    - 18.3.1.15 color (Data Bar Color)  §A.2
    - 18.3.1.93 tabColor (Sheet Tab Color)  §A.2
    - 18.8.3 bgColor (Background Color) §A.2
    - 18.8.19 fgColor (Foreground Color) §A.2
    - 19.2.1.23 penClr (Pen Color for Slide Show)  §A.4.1.
    - 19.5.27 clrVal (Color Value) §A.4.1.
    - 19.5.43 from (From) §A.4.1.
    - 19.5.90 to (To) §A.4.1.
    - 20.1.4.1.1 accent1 (Accent 1) §A.4.1.

        ...

    - 20.1.4.1.6 accent6 (Accent 6) §A.4.1.
    """

    @property
    def color(
        self,
    ) -> CT_ScRgbColor | CT_SRgbColor | CT_HslColor | CT_SystemColor | CT_SchemeColor | CT_PresetColor:
        """颜色

        <xsd:group ref="EG_ColorChoice"/>

        maxOccurs 和 minOccurs 默认值为 1
        """

        return self.choice_require_one_child(*self.color_tags)  # type: ignore


class CT_ColorMRU(EG_ColorChoice):
    """彩色 MRU

    19.2.1.4 clrMru (Color MRU)

    这指定了演示文稿中最近使用的用户选择的颜色。 此列表包含演示文稿主题颜色之外的自定义用户选择颜色，使应用程序能够公开这些附加颜色选择以便于重用。 列表中的第一项是最近使用的颜色。
    """

    @property
    def colors(self):
        """颜色"""

        return self.choice_and_more(*self.color_tags)


class ST_BlackWhiteMode(ST_BaseEnumType):
    """黑白模式

    20.1.10.10 ST_BlackWhiteMode (Black and White Mode)

    这个简单类型指定当指定为黑白模式时应如何呈现对象。
    """

    Color = 'clr'
    """使用正常颜色渲染的对象"""

    Automatic = 'auto'
    """使用自动着色渲染的对象"""

    Gray = 'gray'
    """使用灰色渲染的对象"""
    LightGreay = 'ltGray'
    """使用浅灰色渲染的对象"""

    InverseGray = 'invGray'
    """使用反灰色着色渲染的对象"""

    GrayAndWhite = 'grayWhite'
    """以灰色和白色渲染的对象"""

    BlackAndGray = 'blackGray'
    """使用黑色和灰色渲染的对象"""

    BlackAndWhite = 'blackWhite'
    """以黑白着色呈现的对象"""

    Black = 'black'
    """使用纯黑色着色渲染的对象"""

    White = 'white'
    """用白色渲染的对象"""

    Hidden = 'hidden'
    """使用隐藏颜色渲染的对象"""


# attributeGroup
class AG_Blob(OxmlBaseElement):
    """嵌入的文件信息，

    参考:

        20.1.8.13 blip (Blip)

        该元素指定图像（二进制大图像或图片）的存在并包含对图像数据的引用。

    定义信息:

        <xsd:attributeGroup name="AG_Blob">
            <xsd:attribute ref="r:embed" use="optional" default=""/>
            <xsd:attribute ref="r:link" use="optional" default=""/>
        </xsd:attributeGroup>

    使用信息:

        <xsd:attributeGroup ref="AG_Blob"/>
    """

    @property
    def r_embed(self) -> r_ST_RelationshipId:
        """嵌入图片参考 r:embed

        Embedded Picture Reference

        指定嵌入图片的标识信息。 该属性用于指定驻留在文件本地的图像。

        来自: AG_Blob
        """

        r_embed = self.attrib.get(qn('r:embed'), '')

        return r_ST_RelationshipId(utils.AnyStrToStr(r_embed))  # type: ignore

    @property
    def r_link(self) -> r_ST_RelationshipId:
        """链接图片参考

        Linked Picture Reference

        指定链接图片的标识信息。 该属性用于指定不驻留在该文件中的图像。

        来自: AG_Blob
        """

        r_link = self.attrib.get(qn('r:link'), '')

        return r_ST_RelationshipId(utils.AnyStrToStr(r_link))  # type: ignore


class CT_EmbeddedWAVAudioFile(OxmlBaseElement):
    """嵌入的 WAV 音频文件

    19.5.68 snd (Sound)
    19.5.70 sndTgt (Sound Target)
    20.1.2.2.32 snd (Hyperlink Sound)
    20.1.3.7 wavAudioFile (Audio from WAV File)
    """

    @property
    def r_embed(self):
        """嵌入的关系id"""

        r_embed = self.attrib[qn('r:embed')]

        return r_ST_RelationshipId(str(r_embed))

    @property
    def name(self) -> str:
        """ """

        name = self.attrib.get('name')

        return '' if name is None else str(name)


class CT_Hyperlink(OxmlBaseElement):
    """超链接

    - 17.16.22 hyperlink (Hyperlink)
    - 18.3.1.47 hyperlink (Hyperlink)
    - 20.1.2.2.23 hlinkHover (Hyperlink for Hover)
    - 21.1.2.3.5 hlinkClick (Click Hyperlink)
    - 21.1.2.3.6 hlinkMouseOver (Mouse-Over Hyperlink)
    """

    @property
    def sound(self) -> Optional[CT_EmbeddedWAVAudioFile]:
        """声音文件连接"""

        return self.find(qn('a:snd'))  # type: ignore

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return self.find(qn('a:extLst'))  # type: ignore

    @property
    def r_id(self):
        """绘图对象超链接目标

        Drawing Object Hyperlink Target

        指定在此幻灯片关系文件中查找时包含此超链接目标的关系 ID。 该属性不能省略。
        """
        r_id = self.attrib.get(qn('r:id'))

        return r_ST_RelationshipId(str(r_id)) if r_id is not None else None

    @property
    def invalid_url(self) -> str:
        """无效的网址 / Invalid URL

        当生成应用程序确定 URL 无效时指定该 URL。 也就是说，生成应用程序仍然可以存储 URL，但已知该 URL 不正确。
        """
        url = self.attrib.get('invalidUrl')

        return str(url) if url is not None else ''

    @property
    def action(self) -> str:
        """动作设定

        Action Setting

        指定激活此超链接时要执行的操作。 这可用于指定要导航到的幻灯片或要运行的代码脚本。
        """
        val = self.attrib.get('action')

        return str(val) if val is not None else ''

    @property
    def target_frame(self) -> str:
        """目标框架 / Target Frame

        指定打开此超链接时要使用的目标框架。 当超链接被激活时，该属性用于确定是否启动新窗口以供查看或是否可以使用现有窗口。 如果省略此属性，则会打开一个新窗口。
        """
        val = self.attrib.get('tgtFrame')

        return str(val) if val is not None else ''

    @property
    def tooltip(self) -> str:
        """超链接工具提示 / Hyperlink Tooltip

        指定当鼠标悬停在超链接文本上时应显示的工具提示。 如果省略此属性，则可以显示超链接文本本身。
        """
        val = self.attrib.get('tooltip')

        return str(val) if val is not None else ''

    @property
    def history(self) -> XSD_Boolean:
        """添加超链接到页面历史记录

        Add Hyperlink to Page History

        指定导航到此 URI 时是否将此 URI 添加到历史记录中。 这允许观看该演示文稿而无需在观看机器上存储历史信息。 如果省略此属性，则假定值为 1 或 true。

        <xsd:attribute name="history" type="xsd:boolean" use="optional" default="true"/>
        """

        val = self.attrib.get('history')

        return XSD_Boolean(to_xsd_bool(val, none=True))

    @property
    def highlight_click(self) -> XSD_Boolean:
        """突出显示单击

        Highlight Click

        指定此属性是否已在本文档中使用。 也就是说，当超链接已被访问时，将利用该属性，以便生成应用程序可以确定该文本的颜色。 如果省略此属性，则隐含值 0 或 false。
        """
        val = self.attrib.get('highlightClick')

        return XSD_Boolean(to_xsd_bool(val, none=False))

    @property
    def end_sound(self) -> XSD_Boolean:
        """结束声音

        End Sounds

        指定相关 URL 是否应在单击该 URL 时停止正在播放的所有声音.
        """
        val = self.attrib.get('endSnd')

        return XSD_Boolean(to_xsd_bool(val, none=False))


ST_DrawingElementId = NewType('ST_DrawingElementId', int)
"""Drawing 元素ID标识符

20.1.10.21 ST_DrawingElementId

这个简单类型指定了每个绘图元素的唯一整数标识符。

这个简单类型的内容是对 W3C XML Schema unsignedInt 数据类型的限制。

<xsd:simpleType name="ST_DrawingElementId">
    <xsd:restriction base="xsd:unsignedInt"/>
</xsd:simpleType>
"""


# attributeGroup
class AG_Locking(OxmlBaseElement):
    """关于锁定的 属性组

    参考: 20.1.2.2.11 cxnSpLocks (Connection Shape Locks)

    <xsd:attributeGroup name="AG_Locking">
        <xsd:attribute name="noGrp" type="xsd:boolean" use="optional" default="false"/>
        <xsd:attribute name="noSelect" type="xsd:boolean" use="optional" default="false"/>
        <xsd:attribute name="noRot" type="xsd:boolean" use="optional" default="false"/>
        <xsd:attribute name="noChangeAspect" type="xsd:boolean" use="optional" default="false"/>
        <xsd:attribute name="noMove" type="xsd:boolean" use="optional" default="false"/>
        <xsd:attribute name="noResize" type="xsd:boolean" use="optional" default="false"/>
        <xsd:attribute name="noEditPoints" type="xsd:boolean" use="optional" default="false"/>
        <xsd:attribute name="noAdjustHandles" type="xsd:boolean" use="optional" default="false"/>
        <xsd:attribute name="noChangeArrowheads" type="xsd:boolean" use="optional" default="false"/>
        <xsd:attribute name="noChangeShapeType" type="xsd:boolean" use="optional" default="false"/>
    </xsd:attributeGroup>
    """

    @property
    def no_group(self) -> XSD_Boolean:
        """不允许组合"""

        val = self.attrib.get('noGrp')

        return to_xsd_bool(val, none=False)

    @property
    def no_select(self) -> XSD_Boolean:
        """不允许选择"""

        val = self.attrib.get('noSelect')

        return to_xsd_bool(val, none=False)

    @property
    def no_rotate(self) -> XSD_Boolean:
        """不允许旋转"""

        val = self.attrib.get('noRot')

        return to_xsd_bool(val, none=False)

    @property
    def no_change_aspect(self) -> XSD_Boolean:
        """禁止更改宽高比"""

        val = self.attrib.get('noChangeAspect')

        return to_xsd_bool(val, none=False)

    @property
    def no_move(self) -> XSD_Boolean:
        """不允许移动"""

        val = self.attrib.get('noMove')

        return to_xsd_bool(val, none=False)

    @property
    def no_resize(self) -> XSD_Boolean:
        """禁止调整形状大小"""

        val = self.attrib.get('noResize')

        return to_xsd_bool(val, none=False)

    @property
    def no_edit_points(self) -> XSD_Boolean:
        """禁止形状点编辑"""

        val = self.attrib.get('noEditPoints')

        return to_xsd_bool(val, none=False)

    @property
    def no_adjust_handles(self) -> XSD_Boolean:
        """禁止显示调整手柄"""

        val = self.attrib.get('noAdjustHandles')

        return to_xsd_bool(val, none=False)

    @property
    def no_change_arrowheads(self) -> XSD_Boolean:
        """禁止更改箭头"""

        val = self.attrib.get('noChangeArrowheads')

        return to_xsd_bool(val, none=False)

    @property
    def no_change_shape_type(self) -> XSD_Boolean:
        """禁止更改形状类型"""

        val = self.attrib.get('noChangeShapeType')

        return to_xsd_bool(val, none=False)


class CT_ConnectorLocking(AG_Locking):
    """连接器锁定

    20.1.2.2.11 cxnSpLocks (Connection Shape Locks)

    该元素指定连接形状的所有锁定属性。 这些属性向生成应用程序通知先前已锁定的特定属性，因此不应更改。
    """

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)


class CT_ShapeLocking(AG_Locking):
    """图形锁定

    20.1.2.2.34 spLocks (Shape Locks)

    该元素指定形状的所有锁定属性。 这些属性向生成应用程序通知先前已锁定的特定属性，因此不应更改。
    """

    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)

    @property
    def no_text_edit(self) -> bool:
        """不允许文本编辑"""

        val = self.attrib.get('noTextEdit')

        return utils.XsdBool(val)


class CT_PictureLocking(AG_Locking):
    """

    20.1.2.2.31 picLocks (Picture Locks)

    该元素指定图形框架的所有锁定属性。 这些属性向生成应用程序通知先前已锁定的特定属性，因此不应更改。
    """

    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)

    @property
    def no_crop(self) -> bool:
        """不允许裁减

        指定生成应用程序不应允许裁剪相应的图片。 如果未指定此属性，则假定值为 false。
        """

        val = self.attrib.get('noCrop')

        return utils.XsdBool(val)


class CT_GroupLocking(OxmlBaseElement):
    """组合锁定

    20.1.2.2.21 grpSpLocks (Group Shape Locks)

    该元素指定图形框架的所有锁定属性。 这些属性向生成应用程序通知先前已锁定的特定属性，因此不应更改。
    """

    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)

    @property
    def no_group(self) -> XSD_Boolean:
        """不允许组合

        Disallow Shape Grouping

        指定对应的组形状无法分组。 也就是说，它不能与其他形状组合以形成一组形状。 如果未指定此属性，则假定值为 false。
        """

        val = self.attrib.get('noGrp')

        return to_xsd_bool(val)

    @property
    def no_ungroup(self) -> XSD_Boolean:
        """不允许解组合

        Disallow Shape Ungrouping

        指定生成应用程序不应显示相应连接形状的调整手柄。 如果未指定此属性，则假定值为 false。
        """

        val = self.attrib.get('noUngrp')

        return to_xsd_bool(val)

    @property
    def no_select(self) -> XSD_Boolean:
        """不允许选择

        Disallow Shape Selection

        指定对应的组形状的任何部分都不能被选择。 这意味着如果指定了此属性，则无法选择图片、形状或附加文本。 如果未指定此属性，则假定值为 false。
        """

        val = self.attrib.get('noSelect')

        return to_xsd_bool(val)

    @property
    def no_rotate(self) -> XSD_Boolean:
        """不允许旋转

        Disallow Shape Rotation

        指定相应的组形状无法旋转，驻留在组内的对象仍然可以旋转，除非它们也已被锁定。 如果未指定此属性，则假定值为 false。
        """

        val = self.attrib.get('noRot')

        return to_xsd_bool(val)

    @property
    def no_change_aspect(self) -> XSD_Boolean:
        """不允许改变纵横比

        Disallow Aspect Ratio Change

        指定生成应用程序不应允许更改相应连接形状的纵横比。 如果未指定此属性，则假定值为 false。
        """

        val = self.attrib.get('noChangeAspect')

        return to_xsd_bool(val)

    @property
    def no_move(self) -> XSD_Boolean:
        """不允许移动

        Disallow Moving Shape

        指定对应的图形框不能移动。 驻留在图形框架内的对象仍然可以移动，除非它们也已被锁定。 如果未指定此属性，则假定值为 false。
        """

        val = self.attrib.get('noMove')

        return to_xsd_bool(val)

    @property
    def no_resize(self) -> XSD_Boolean:
        """不允许调整尺寸大小

        Disallow Shape Resizing

        指定对应的组形状不能调整大小。 如果未指定此属性，则假定值为 false。
        """

        val = self.attrib.get('noResize')

        return to_xsd_bool(val)


class CT_GraphicalObjectFrameLocking(OxmlBaseElement):
    """图形对象框架锁定

    20.1.2.2.19 graphicFrameLocks (Graphic Frame Locks)

    该元素指定图形框架的所有锁定属性。 这些属性向生成应用程序通知先前已锁定的特定属性，因此不应更改。
    """

    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'))

    @property
    def no_group(self) -> XSD_Boolean:
        """不允许组合

        Disallow Shape Grouping

        指定对应的组形状无法分组。 也就是说，它不能与其他形状组合以形成一组形状。 如果未指定此属性，则假定值为 false。
        """

        val = self.attrib.get('noGrp')

        return to_xsd_bool(val, none=False)

    @property
    def no_drilldown(self) -> XSD_Boolean:
        """禁止选择子形状

        Disallow Selection of Child Shapes

        指定生成应用程序不应允许选择相应图形框架内的对象，但允许选择图形框架本身。 如果未指定此属性，则假定值为 false。
        """

        val = self.attrib.get('noDrilldown')

        return to_xsd_bool(val, none=False)

    @property
    def no_select(self) -> XSD_Boolean:
        """不允许选择

        Disallow Shape Selection

        指定对应的组形状的任何部分都不能被选择。 这意味着如果指定了此属性，则无法选择图片、形状或附加文本。 如果未指定此属性，则假定值为 false。
        """

        val = self.attrib.get('noSelect')

        return to_xsd_bool(val, none=False)

    @property
    def no_change_aspect(self) -> XSD_Boolean:
        """不允许改变纵横比

        Disallow Aspect Ratio Change

        指定生成应用程序不应允许更改相应连接形状的纵横比。 如果未指定此属性，则假定值为 false。
        """

        val = self.attrib.get('noChangeAspect')

        return to_xsd_bool(val, none=False)

    @property
    def no_move(self) -> XSD_Boolean:
        """不允许移动

        Disallow Moving Shape

        指定对应的图形框不能移动。 驻留在图形框架内的对象仍然可以移动，除非它们也已被锁定。 如果未指定此属性，则假定值为 false。
        """

        val = self.attrib.get('noMove')

        return to_xsd_bool(val, none=False)

    @property
    def no_resize(self) -> XSD_Boolean:
        """不允许调整尺寸大小

        Disallow Shape Resizing

        指定对应的组形状不能调整大小。 如果未指定此属性，则假定值为 false。
        """

        val = self.attrib.get('noResize')

        return to_xsd_bool(val, none=False)


class CT_ContentPartLocking(AG_Locking):
    """内容部分锁定

    20.1.2.2.43 cpLocks (Content Part Locks)

    该元素指定内容部分的所有锁定属性。 这些属性向生成应用程序通知先前已锁定的特定属性，因此不应更改。
    """

    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)


class CT_NonVisualDrawingProps(OxmlBaseElement):
    """非可视绘图属性

    该元素指定非可视画布属性。 这允许存储不影响图片外观的附加信息。

    19.3.1.12 cNvPr (Non-Visual Drawing Properties)

        该元素指定非可视画布属性。 这允许存储不影响图片外观的附加信息。

    20.1.2.2.8 cNvPr (Non-Visual Drawing Properties)

        该元素指定非可视画布属性。 这允许存储不影响图片外观的附加信息。

    20.2.2.3 cNvPr (Non-Visual Drawing Properties)

    20.4.2.5 docPr (Drawing Object Non-Visual Properties)

    20.4.2.27 cNvPr (Non-Visual Drawing Properties)

    20.5.2.8 cNvPr (Non-Visual Drawing Properties)

    21.3.2.7 cNvPr (Non-Visual Drawing Properties)
    """

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)

    @property
    def hlink_Click(self) -> Optional[CT_Hyperlink]:
        return getattr(self, qn('a:hlinkClick'), None)

    @property
    def hlink_Hover(self) -> Optional[CT_Hyperlink]:
        return getattr(self, qn('a:hlinkHover'), None)

    @property
    def id(self) -> ST_DrawingElementId:
        """唯一标识符

        Unique Identifier

        指定当前文档中当前 DrawingML 对象的唯一标识符。 该 ID 可用于帮助唯一标识该对象，以便文档的其他部分可以引用它。

        如果同一文档中的多个对象共享相同的 id 属性值，则该文档应被视为不合格。
        """
        val = self.attrib['id']

        return ST_DrawingElementId(int(val))

    @property
    def name(self) -> str:
        """名称

        Name

        指定对象的名称。 [注意: 通常，这用于存储图片对象的原始文件名。]

        """
        val = self.attrib['name']

        return str(val)

    @property
    def desc(self) -> str:
        """对象的替代文本

        Alternative Text for Object

        指定当前 DrawingML 对象的替代文本，以供不显示当前对象的辅助技术或应用程序使用。
        """
        val = self.attrib['descr']

        return str(val) if val is not None else ''

    @property
    def hidden(self) -> bool:
        """是否隐藏， 默认 Flase

        Hidden

        指定是否显示此 DrawingML 对象。 当 DrawingML 对象在文档中显示时，该对象可以被隐藏（即存在，但不可见）。
        该属性决定对象是渲染还是隐藏。 [注意: 应用程序可以具有允许查看该对象的设置。]

        如果省略此属性，则应显示父 DrawingML 对象（即不隐藏）。
        """

        val = self.attrib.get('hidden')

        return to_xsd_bool(val, none=False)

    @property
    def title(self) -> str:
        """标题

        Title

        指定当前 DrawingML 对象的标题 (caption)。

        如果省略此属性，则父对象不存在标题文本。
        """
        val = self.attrib['title']

        return str(val) if val is not None else ''


class CT_NonVisualDrawingShapeProps(OxmlBaseElement):
    """形状的非可视绘图属性

    19.3.1.13 cNvSpPr (Non-Visual Drawing Properties for a Shape)

    该元素指定形状的非可视绘图属性。 生成应用程序将使用这些属性来确定如何处理这些形状

    20.1.2.2.9 cNvSpPr (Non-Visual Shape Drawing Properties)
    20.5.2.9 cNvSpPr (Connection Non-Visual Shape Properties)
    21.3.2.8 cNvSpPr (Non-Visual Shape Drawing Properties)
    """

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)

    @property
    def shape_locks(self) -> Optional[CT_ShapeLocking]:
        """图形锁定属性信息"""
        return getattr(self, qn('a:spLocks'), None)

    @property
    def text_box(self) -> XSD_Boolean:
        """是否为文本框

        Text Box

        指定相应的形状是文本框，因此生成应用程序应将其视为文本框。 如果省略此属性，则假定相应的形状不是特定的文本框。

        [注意: 因为形状未指定为文本框，但这并不意味着它不能附加文本。 文本框只是具有特定属性的特殊形状。]
        """
        val = self.attrib.get('txBox')

        return to_xsd_bool(val, none=False)


class CT_NonVisualConnectorProperties(OxmlBaseElement):
    """非可视连接器形状绘图属性

    此元素指定特定于连接器形状的非可视绘图属性。 这包括指定连接器形状所连接的形状的信息。

    19.3.1.8 cNvCxnSpPr (Non-Visual Connector Shape Drawing Properties)
    20.1.2.2.4 cNvCxnSpPr (Non-Visual Connector Shape Drawing Properties)
    20.4.2.23 cNvCnPr (Non-Visual Connector Shape Drawing Properties)
    20.5.2.4 cNvCxnSpPr (Non-Visual Connector Shape Drawing Properties)
    21.3.2.3 cNvCxnSpPr (Non-Visual Connection Shape Drawing Properties)
    """

    @property
    def connector_shape_locks(self) -> Optional[CT_ConnectorLocking]:
        """连接器锁定属性

        20.1.2.2.11 cxnSpLocks (Connection Shape Locks)

        该元素指定连接形状的所有锁定属性。 这些属性向生成应用程序通知先前已锁定的特定属性，因此不应更改。

        """
        return getattr(self, qn('a:cxnSpLocks'), None)

    @property
    def start_connector(self) -> Optional[CT_Connection]:
        """连接开始

        20.1.2.2.36 stCxn

        该元素指定应由相应连接器形状建立的起始连接。 这将连接器的头部连接到第一个形状。
        """
        return getattr(self, qn('a:stCxn'), None)

    @property
    def end_connector(self) -> Optional[CT_Connection]:
        """连接结束

        20.1.2.2.13 endCxn

        该元素指定应由相应连接器形状形成的结束连接。 这会将连接器的尾部连接到最终目标形状。
        """
        return getattr(self, qn('a:endCxn'), None)

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)


class CT_NonVisualPictureProperties(OxmlBaseElement):
    """非视觉图片属性

    该元素指定图片画布(picture canvas)的非视觉属性。 生成应用程序将使用这些属性来确定如何更改所讨论的图片对象的某些属性。

    19.3.1.11 cNvPicPr (Non-Visual Picture Drawing Properties)非视觉绘图属性

        该元素指定图片画布的非视觉属性。 生成应用程序将使用这些属性来确定如何更改所讨论的图片对象的某些属性。

    20.1.2.2.7 cNvPicPr (Non-Visual Picture Drawing Properties)
    20.2.2.2 cNvPicPr (Non-Visual Picture Drawing Properties)
    20.5.2.7 cNvPicPr (Non-Visual Picture Drawing Properties)
    21.3.2.6 cNvPicPr (Non-Visual Picture Drawing Properties)
    """

    @property
    def picture_locks(self) -> Optional[CT_PictureLocking]:
        """图片锁定属性

        20.1.2.2.31 picLocks

        该元素指定图形框架的所有锁定属性。 这些属性向生成应用程序通知先前已锁定的特定属性，因此不应更改。
        """

        return getattr(self, qn('a:picLocks'), None)

    @property
    def prefer_relative_resize(self) -> XSD_Boolean:
        """首选相对调整大小

        Relative Resize Preferred

        指定用户界面是否应根据图片的当前大小或其原始大小显示图片的大小调整。
        如果此属性设置为 true，则缩放是相对于原始图片大小而不是当前图片大小。

        [示例: 考虑这样的情况: 文档中的图片大小已调整，现在是原始插入图片大小的 50%。 现在，如果用户选择稍后在生成应用程序中调整该图片的大小，则应检查该属性的值。

        如果此属性设置为 true，则显示值 50%。 同样，如果此属性设置为 false，则应显示 100% 的值，因为图片尚未从其当前（较小）尺寸调整大小。]
        """

        val = self.attrib.get('preferRelativeResize')

        return to_xsd_bool(val, none=True)

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)


class CT_NonVisualGroupDrawingShapeProps(OxmlBaseElement):
    """非可视组形状绘图属性

    此元素指定组形状的非可视绘图属性。 这些非视觉属性是生成应用程序在渲染幻灯片表面时将使用的属性。

    19.3.1.10 cNvGrpSpPr (Non-Visual Group Shape Drawing Properties)
    20.1.2.2.6 cNvGrpSpPr (Non-Visual Group Shape Drawing Properties)

        此元素指定组形状的非可视绘图属性。 这些非视觉属性是生成应用程序在渲染幻灯片表面时将使用的属性。

    20.5.2.6 cNvGrpSpPr (Non-Visual Group Shape Drawing Properties)
    21.3.2.5 cNvGrpSpPr (Non-Visual Group Shape Drawing Properties)
    """

    @property
    def group_shape_locks(self) -> Optional[CT_GroupLocking]:
        """组合图形锁定信息

        20.1.2.2.21 grpSpLocks

        该元素指定连接形状的所有锁定属性。 这些属性向生成应用程序通知先前已锁定的特定属性，因此不应更改。
        """

        return getattr(self, qn('a:grpSpLocks'), None)

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)


class CT_NonVisualGraphicFrameProperties(OxmlBaseElement):
    """非可视图形框架绘图属性

    19.3.1.9 cNvGraphicFramePr

    该元素指定图形框架的非可视绘图属性。 这些非视觉属性是生成应用程序在渲染幻灯片表面时将使用的属性。
    """

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)

    @property
    def graphic_frame_locks(self) -> Optional[CT_GraphicalObjectFrameLocking]:
        """图形对象框架锁定

        20.1.2.2.19 graphicFrameLocks (Graphic Frame Locks)

        该元素指定图形框架的所有锁定属性。 这些属性向生成应用程序通知先前已锁定的特定属性，因此不应更改。
        """

        return getattr(self, qn('a:graphicFrameLocks'), None)


class CT_NonVisualContentPartProperties(OxmlBaseElement):
    """非视觉内容部分绘图属性

    20.4.2.24 cNvContentPartPr (Non-Visual Content Part Drawing Properties)

    """

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)

    @property
    def content_part_locks(self) -> Optional[CT_ContentPartLocking]:
        """内容部分锁定信息"""

        return getattr(self, qn('a:cpLocks'), None)

    @property
    def is_comment(self) -> XSD_Boolean:
        """是否为评论

        Is a Comment

        指定内容部分是评论(comment)还是注释(annotation)。 如果为真，则为评论； 否则为一般注释。
        """

        val = self.attrib.get('isComment')

        return to_xsd_bool(val, none=True)


class CT_GraphicalObjectData(OxmlBaseElement):
    """图形对象数据

    20.1.2.2.17 graphicData (Graphic Object Data)

    该元素指定对文档中图形对象的引用。 该图形对象完全由选择将此数据保留在文档中的文档作者提供。

    """

    @property
    def chart_data_rid(self):
        """获取图表数据
        <a:graphic>
            <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/chart">
                <c:chart xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:id="rId4"/>
            </a:graphicData>
        </a:graphic>
        """

        if self.uri != namespace_c:
            msg = '获取图表数据失败， URI不匹配'
            raise OxmlElementValidateError(msg)

        cchart: OxmlBaseElement = getattr(self, f'{{{namespace_c}}}chart')

        # <Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/chart" Target="../charts/chart1.xml"/>
        return r_ST_RelationshipId(str(cchart.attrib[f'{{{namespace_r}}}id']))


    @property
    def table_data(self):
        """获取表格数据

        <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/table">
            <a:tbl>
            ...
            </a:tbl>
        </a:graphicData>
        """

        if self.uri != namespace_tb:
            msg = '获取表格数据失败， URI不匹配'
            raise OxmlElementValidateError(msg)

        oxml_table: CT_Table = getattr(self, qn('a:tbl'))

        return oxml_table

    @property
    def smart_data(self):
        """获取smart图形的数据
        <a:graphic>
            <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/diagram">
                <dgm:relIds xmlns:dgm="http://schemas.openxmlformats.org/drawingml/2006/diagram" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:dm="rId4" r:lo="rId5" r:qs="rId6" r:cs="rId7"/>
            </a:graphicData>
        </a:graphic>
        """

        if self.uri != namespace_dgm:
            msg = '获取smart图形数据失败， URI不匹配'
            raise OxmlElementValidateError(msg)

        relIds: OxmlBaseElement = getattr(self, f'{{{namespace_dgm}}}relIds')

        # <Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/diagramData" Target="../diagrams/data1.xml"/>
        r_dm_id = r_ST_RelationshipId(str(relIds.attrib[f'{{{namespace_r}}}dm']))

        # <Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/diagramLayout" Target="../diagrams/layout1.xml"/>
        r_lo_id = r_ST_RelationshipId(str(relIds.attrib[f'{{{namespace_r}}}lo']))

        # <Relationship Id="rId6" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/diagramQuickStyle" Target="../diagrams/quickStyle1.xml"/>
        r_qs_id = r_ST_RelationshipId(str(relIds.attrib[f'{{{namespace_r}}}qs']))

        # <Relationship Id="rId7" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/diagramColors" Target="../diagrams/colors1.xml"/>
        r_cs_id = r_ST_RelationshipId(str(relIds.attrib[f'{{{namespace_r}}}cs']))

        return r_dm_id, r_lo_id, r_qs_id, r_cs_id

    @property
    def picuture_data(self):
        """获取图形数据

        <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
                <pic:nvPicPr>
                    <pic:cNvPr id="9" name="图片 9"/>
                    <pic:cNvPicPr>
                        <a:picLocks noChangeAspect="1"/>
                    </pic:cNvPicPr>
                </pic:nvPicPr>
                <pic:blipFill>
                    <a:blip r:embed="rId4"/>
                    <a:stretch>
                        <a:fillRect/>
                    </a:stretch>
                </pic:blipFill>
                <pic:spPr>
                    <a:xfrm>
                        <a:off x="0" y="0"/>
                        <a:ext cx="5274310" cy="3242945"/>
                    </a:xfrm>
                    <a:prstGeom prst="rect">
                        <a:avLst/>
                    </a:prstGeom>
                    <a:noFill/>
                    <a:ln>
                        <a:noFill/>
                    </a:ln>
                </pic:spPr>
            </pic:pic>
        </a:graphicData>
        """

        # 防止循环导入

        if self.uri != namespace_pic:
            msg = '获取图片数据失败， URI不匹配'
            raise OxmlElementValidateError(msg)

        oxml_pic: pic_CT_Picture = getattr(self, qn('pic:pic'))

        return oxml_pic

    @property
    def ole_fallback_pic(self):
        """获取嵌入对象数据

        <a:graphicData uri="http://schemas.openxmlformats.org/presentationml/2006/ole">
            <mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">
                <mc:Choice Requires="v">
                    <p:oleObj spid="_x0000_s17449" name="" r:id="rId1" imgW="1245235" imgH="213995" progId="Equation.3">
                        <p:embed/>
                    </p:oleObj>
                </mc:Choice>
                <mc:Fallback>
                    <p:oleObj name="" r:id="rId1" imgW="1245235" imgH="213995" progId="Equation.3">
                        <p:embed/>
                        <p:pic>
                            ...
                        </p:pic>
                    </p:oleObj>
                </mc:Fallback>
            </mc:AlternateContent>
        </a:graphicData>
        """

        if self.uri != namespace_ole:
            msg = '获取嵌入对象(oleObj)数据失败， URI不匹配'
            raise OxmlElementValidateError(msg)


        ole: CT_MC_AlternateContent = getattr(self, qn('mc:AlternateContent'))

        return ole.fallback.p_oleObj.picture

    @property
    def child_elements(self) -> list[OxmlBaseElement]:
        return list(self.iterchildren())  # type: ignore

    @property
    def uri(self) -> XSD_Token:
        """统一资源标识符

        Uniform Resource Identifier

        指定表示存储在该标签下的数据的 URI 或统一资源标识符。 URI 用于标识可以处理此标签内容的正确“服务器”(server)。

        可能是

        - 表格: http://schemas.openxmlformats.org/drawingml/2006/table
        - 图片: http://schemas.openxmlformats.org/drawingml/2006/picture
        - 智能图形: http://schemas.openxmlformats.org/drawingml/2006/diagram
        - 图表: http://schemas.openxmlformats.org/drawingml/2006/chart
        - ole对象: http://schemas.openxmlformats.org/presentationml/2006/ole
        """

        return XSD_Token(str(self.attrib['uri']))


class CT_GraphicalObject(OxmlBaseElement):
    """图形对象

    20.1.2.2.16 graphic (Graphic Object)

    该元素指定单个图形对象的存在。 当文档作者希望保留某种图形对象时，应该引用此元素。
    该图形对象的规范完全由文档作者提供并在 graphicData 子元素中引用。
    """

    @property
    def graphic_data(self) -> CT_GraphicalObjectData:
        """图形对象数据

        20.1.2.2.17 graphicData (Graphic Object Data)

        该元素指定对文档中图形对象的引用。 该图形对象完全由选择将此数据保留在文档中的文档作者提供。
        """

        return getattr(self, qn('a:graphicData'))

    @property
    def ole_graphic_data(self) -> CT_GraphicalObjectData:
        """图形对象数据

        20.1.2.2.17 graphicData (Graphic Object Data)

        该元素指定对文档中图形对象的引用。 该图形对象完全由选择将此数据保留在文档中的文档作者提供。
        """

        return getattr(self, qn('ole:graphicData'))


class ST_ChartBuildStep(ST_BaseEnumType):
    """Chart图表动画构建步骤

    这个简单的类型指定图表动画中的动画构建步骤。

    20.1.10.13 ST_ChartBuildStep (Chart Animation Build Step)
    """

    Category = 'category'
    """为此动画构建步骤制作图表类别动画"""

    CategoryPoints = 'ptInCategory'
    """为此动画构建步骤对图表类别中的点进行动画处理"""

    Series = 'series'
    """为此动画构建步骤制作图表系列动画"""

    SeriesPoints = 'ptInSeries'
    """为此动画构建步骤对图表系列中的一个点进行动画处理"""

    AllPoints = 'allPts'
    """为此动画构建步骤对图表内的所有点进行动画处理"""

    GridAndLegend = 'gridLegend'
    """为此动画构建步骤制作图表网格和图例的动画"""


class ST_DgmBuildStep(ST_BaseEnumType):
    """Diagram图表动画构建步骤

    这个简单的类型指定图表动画中的动画构建步骤。

    20.1.10.20 ST_DgmBuildStep (Diagram Animation Build Steps)
    """

    Background = 'bg'
    """为该动画构建步骤的图表背景设置动画"""

    Shape = 'sp'
    """为此动画构建步骤制作图表形状动画"""


class CT_AnimationDgmElement(OxmlBaseElement):
    """动画绘制(Diagram)元素

    20.1.2.2.12 dgm (Diagram to Animate)

    此元素指定对应在幻灯片动画序列中进行动画处理的图表的引用。 除了简单地充当图表的参考之外，还定义了动画构建步骤。
    """

    @property
    def id(self) -> s_ST_Guid:
        """标识符

        Identifier

        指定动画中此构建步骤的形状的 GUID。
        """

        val = self.attrib.get('id')

        if val is not None:
            val = utils.AnyStrToStr(val)  # type: ignore
        else:
            val = '{00000000-0000-0000-0000-000000000000}'

        return s_ST_Guid(val)

    @property
    def build_step(self) -> ST_DgmBuildStep:
        """动画构建步骤

        Animation Build Step

        指定应使用哪个步骤来构建图的这一部分。 例如，图表可以构建为一个对象，这意味着它可以作为单个图形进行动画处理。
        或者，图表可以是动画的，或者构建为单独的部分。

        <xsd:attribute name="bldStep" type="ST_DgmBuildStep" use="optional" default="sp"/>
        """

        val = self.attrib.get('bldStep')

        if val is not None:
            return ST_DgmBuildStep(utils.AnyStrToStr(val))  # type: ignore

        return ST_DgmBuildStep.Shape


class CT_AnimationChartElement(OxmlBaseElement):
    """图表动画

    20.1.2.2.3 chart (Chart to Animate)

    此元素指定对应在幻灯片动画序列中进行动画处理的图表的引用。 除了简单地充当图表的参考之外，还定义了动画构建步骤。
    """

    @property
    def series_idx(self) -> int:
        """系列索引

        Series Index

        指定应设置动画的相应图表中的系列索引。
        """

        val = self.attrib.get('seriesIdx')

        return int(val) if val is not None else -1

    @property
    def category_idx(self) -> int:
        """分类索引

        Category Index

        指定应设置动画的相应图表中的类别索引。
        """

        val = self.attrib.get('categoryIdx')

        return int(val) if val is not None else -1

    @property
    def build_step(self) -> ST_ChartBuildStep:
        """动画构建步骤

        Animation Build Step

        指定应使用哪个步骤来构建图表的这一部分。 例如，图表可以构建为一个对象，这意味着它可以作为单个图形进行动画处理。 或者，图表可以是动画的，或者构建为单独的部分。
        """

        val = self.attrib['bldStep']

        return ST_ChartBuildStep(str(val))


class CT_AnimationElementChoice(OxmlBaseElement):
    """动画元素

    该元素指定要设置动画的图形元素。

    19.5.45 graphicEl (Graphic Element)
    """

    @property
    def animation_element(
        self,
    ) -> CT_AnimationDgmElement | CT_AnimationChartElement:
        """动画元素

        至少应存在一个
        """

        tags = (
            qn('a:dgm'),  # CT_AnimationDgmElement
            qn('a:chart'),  # CT_AnimationChartElement
        )

        return self.choice_require_one_child(*tags)  # type: ignore


class ST_AnimationBuildType(ST_BaseEnumType):
    """动画构建类型

    20.1.10.4 ST_AnimationBuildType (Animation Build Type)

    这个简单的类型指定了构建动画或设置动画的方式。
    """

    AllAtOnce = 'allAtOnce'
    """将所有对象作为一个整体进行动画处理。"""


class ST_AnimationDgmOnlyBuildType(ST_BaseEnumType):
    """仅图表动画类型

    20.1.10.8 ST_AnimationDgmOnlyBuildType (Diagram only Animation Types)

    这种简单类型指定仅可用于对图表进行动画处理的构建选项。 这些选项指定图表中对象的分组和动画方式。
    """

    One = 'one'
    """按元素对图表进行动画处理。 对于树形图"""

    LevelOneByOne = 'lvlOne'
    """通过级别内的元素对图表进行动画处理，一次为一个级别元素添加动画效果。"""

    EachLevelAtOnce = 'lvlAtOnce'
    """一次为一个级别的图表设置动画，将整个级别作为一个对象进行动画处理"""


class ST_AnimationDgmBuildType(ST_BaseEnumType):
    """绘制(Diagram)动画构建类型

    20.1.10.7 ST_AnimationDgmBuildType (Diagram Animation Build Type)

    这个简单的类型指定了构建图表动画的方法。 也就是说，它指定了图表图形对象中的对象应该被动画化的方式。
    """

    AllAtOnce = 'allAtOnce'
    """将所有对象作为一个整体进行动画处理。"""

    One = 'one'
    """按元素对图表进行动画处理。 对于树形图"""

    LevelOneByOne = 'lvlOne'
    """通过级别内的元素对图表进行动画处理，一次为一个级别元素添加动画效果。"""

    EachLevelAtOnce = 'lvlAtOnce'
    """一次为一个级别的图表设置动画，将整个级别作为一个对象进行动画处理"""


class CT_AnimationDgmBuildProperties(OxmlBaseElement):
    """动画: 绘制(Diagram)的构建属性

    20.1.2.2.2 bldDgm (Build Diagram)

    该元素指定如何构建图表的动画。
    """

    @property
    def build_type(self) -> ST_AnimationDgmBuildType:
        """构建方式

        Build

        指定图表的构建方式。 动画按照该属性定义的特定顺序对容器中的子元素进行动画处理。
        """
        val = self.attrib.get('bld')

        if val is not None:
            return ST_AnimationDgmBuildType(utils.AnyStrToStr(val))  # type: ignore

        return ST_AnimationDgmBuildType.AllAtOnce

    def reverse_animation(self) -> bool:
        """反转动画

        Reverse Animation

        指定该图中对象的动画是否应该反转。 如果未指定此属性，则假定值为 false。
        """

        val = self.attrib.get('rev')

        return utils.XsdBool(val, none=False)


class ST_AnimationChartOnlyBuildType(ST_BaseEnumType):
    """仅图表动画类型

    20.1.10.6 ST_AnimationChartOnlyBuildType (Chart only Animation Types)

    此简单类型指定仅可用于对图表进行动画处理的构建选项。 这些选项指定图表中对象的分组和动画方式。
    """

    Category = 'gategory'
    """按类别制作动画"""

    CategoryElement = 'categoryEl'
    """按类别中的每个元素制作动画"""

    Series = 'series'
    """按每个系列制作动画。"""

    SeriesElement = 'seriesEl'
    """按系列中的每个元素制作动画"""


class ST_AnimationChartBuildType(ST_BaseEnumType):
    """图表动画构建类型

    20.1.10.5 ST_AnimationChartBuildType (Chart Animation Build Type)

    这个简单的类型指定了构建图表动画的方法。 也就是说，它指定图表中的对象应采用的动画方式。

    <xsd:union memberTypes="ST_AnimationBuildType ST_AnimationChartOnlyBuildType"/>
    """

    AllAtOnce = 'allAtOnce'
    """将所有对象作为一个整体进行动画处理。"""

    Category = 'gategory'
    """按类别制作动画"""

    CategoryElement = 'categoryEl'
    """按类别中的每个元素制作动画"""

    Series = 'series'
    """按每个系列制作动画。"""

    SeriesElement = 'seriesEl'
    """按系列中的每个元素制作动画"""


class CT_AnimationChartBuildProperties(OxmlBaseElement):
    """动画: 图表(chuart)构建属性

    20.1.2.2.1 bldChart (Build Chart)

    该元素指定如何构建图表的动画。
    """

    @property
    def build_type(self) -> ST_AnimationChartBuildType:
        """构建方式

        Build

        指定图表的构建方式。 动画按照该属性定义的特定顺序对容器中的子元素进行动画处理。
        """
        val = self.attrib.get('bld')

        if val is not None:
            return ST_AnimationChartBuildType(utils.AnyStrToStr(val))  # type: ignore

        return ST_AnimationChartBuildType.AllAtOnce

    def background_animation(self) -> XSD_Boolean:
        """背景设置也动画

        Animate Background

        指定图表背景元素是否也应设置动画。 [注意: 背景元素的示例是网格线和图表图例。 ]
        """

        val = self.attrib.get('animBg')

        return to_xsd_bool(val, none=True)


class CT_AnimationGraphicalObjectBuildProperties(OxmlBaseElement):
    """动画: 图形对象构建属性

    19.5.17 bldSub (Build Sub Elements)

    该元素指定图形对象子元素的动画属性。
    """

    @property
    def build_element(
        self,
    ) -> CT_AnimationDgmBuildProperties | CT_AnimationChartBuildProperties:
        """构建元素

        至少应存在一个
        """

        tags = (
            qn('a:bldDgm'),  # CT_AnimationDgmBuildProperties
            qn('a:bldChart'),  # CT_AnimationChartBuildProperties
        )

        return self.choice_require_one_child(*tags)  # type: ignore


class CT_BackgroundFormatting(EG_FillProperties, EG_EffectProperties):
    """背景格式

    21.4.3.1 bg (Background Formatting)

    此元素定义可应用于整个图表的背景形状的格式。 背景形状可以保存格式选项，就像普通形状可以在 DrawingML 中保存一样。
    """

    @property
    def fill(
        self,
    ) -> Optional[
        CT_NoFillProperties | CT_SolidColorFillProperties | CT_GradientFillProperties | CT_BlipFillProperties | CT_PatternFillProperties | CT_GroupFillProperties
    ]:
        """
        填充属性

        <xsd:group ref="EG_FillProperties" minOccurs="0" maxOccurs="1"/>
        """

        return self.choice_one_child(*self.fill_pr_tags)  # type: ignore

    @property
    def effect(self) -> Optional[CT_EffectList | CT_EffectContainer]:
        """效果属性

        <xsd:group ref="EG_EffectProperties" minOccurs="0" maxOccurs="1"/>
        """

        return self.choice_one_child(*self.effect_pr_tags)  # type: ignore


class CT_WholeE2oFormatting(EG_EffectProperties):
    """整个E2O格式属性

    21.4.3.9 whole (Whole E2O Formatting)

    适用于整个图表对象（而不仅仅是背景）的格式, 包括线条和效果属性。
    """

    @property
    def line(self) -> Optional[CT_LineProperties]:
        """线条"""

        return getattr(self, qn('a:ln'), None)

    @property
    def effect(self) -> Optional[CT_EffectList | CT_EffectContainer]:
        """效果属性

        <xsd:group ref="EG_EffectProperties" minOccurs="0" maxOccurs="1"/>
        """

        return self.choice_one_child(*self.effect_pr_tags)  # type: ignore


class CT_GvmlUseShapeRectangle(OxmlBaseElement):
    """gvml 使用形状文本矩形

    20.1.2.2.42 useSpRect (Use Shape Text Rectangle)

    此元素指定父形状中的文本矩形应用于此文本形状。 如果指定了此属性，则文本矩形或文本边界框（也称为文本边界框）应与此文本形状所在的父形状的文本边界框具有相同的尺寸。

    <xsd:complexType name="CT_GvmlUseShapeRectangle"/>
    """



class CT_GvmlTextShape(OxmlBaseElement):
    """Gvml文本图形

    20.1.2.2.41 txSp (Text Shape)

    该元素指定父形状中是否存在文本形状。 此文本形状专门用于显示文本，因为它仅具有与文本相关的子元素。
    """

    @property
    def text_body(self) -> CT_TextBody:
        """ """

        return getattr(self, qn('a:txBody'))

    @property
    def shape_choice(self) -> CT_GvmlUseShapeRectangle | CT_Transform2D:
        """图形选择"""

        tags = (
            qn('a:useSpRect'),  # CT_GvmlUseShapeRectangle
            qn('a:xfrm'),  # CT_GvmlUseShapeRectangle
        )

        return self.choice_require_one_child(tags)  # type: ignore

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)


class CT_GvmlShapeNonVisual(OxmlBaseElement):
    """gvml: 形状的非视觉属性

    20.1.2.2.29 nvSpPr (Non-Visual Properties for a Shape)

    该元素指定形状的所有非视觉属性。 该元素是与形状关联的非视觉识别属性、形状属性和应用程序属性的容器。
    这允许存储不影响形状外观的附加信息。
    """

    @property
    def cnv_properties(self) -> CT_NonVisualDrawingProps:
        """非可视绘图属性

        20.1.2.2.8 cNvPr

        该元素指定非可视画布属性。 这允许存储不影响图片外观的附加信息。
        """

        return getattr(self, qn('a:cNvPr'))

    @property
    def cnv_shape_properties(self) -> CT_NonVisualDrawingShapeProps:
        """形状的非可视绘图属性

        19.3.1.13 cNvSpPr

        该元素指定形状的非可视绘图属性。 生成应用程序将使用这些属性来确定如何处理形状
        """

        return getattr(self, qn('a:cNvSpPr'))


class CT_GvmlShape(OxmlBaseElement):
    """Gvml: 形状的非视觉属性

    20.1.2.2.33 sp (Shape)

    该元素指定单个形状的存在。 形状可以是使用 DrawingML 框架定义的预设几何图形或自定义几何图形。
    除了几何形状之外，每个形状还可以附加视觉和非视觉属性。 文本和相应的样式信息也可以附加到形状。
    该形状与形状树或组形状元素中的所有其他形状一起指定。

    """

    @property
    def nv_shape_properties(self) -> CT_GvmlShapeNonVisual:
        """形状的非可视属性"""

        return getattr(self, qn('a:nvSpPr'))

    @property
    def shape_properites(self) -> CT_ShapeProperties:
        """形状属性"""

        return getattr(self, qn('a:spPr'))

    @property
    def text_shape(self) -> Optional[CT_GvmlTextShape]:
        """文本形状"""

        return getattr(self, qn('a:txSp'), None)

    @property
    def style(self) -> Optional[CT_ShapeStyle]:
        """样式"""

        return getattr(self, qn('a:style'), None)

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)


class CT_GvmlConnectorNonVisual(OxmlBaseElement):
    """gvml: 连接形状的非视觉属性

    20.1.2.2.25 nvCxnSpPr (Non-Visual Properties for a Connection Shape)

    该元素指定连接形状的所有非视觉属性。 该元素是与连接形状关联的非视觉识别属性、形状属性和应用程序属性的容器。 这允许存储不影响连接形状外观的附加信息。
    """

    @property
    def cnv_properties(self) -> CT_NonVisualDrawingProps:
        """非可视绘图属性

        20.1.2.2.8 cNvPr

        该元素指定非可视画布属性。 这允许存储不影响图片外观的附加信息。
        """

        return getattr(self, qn('a:cNvPr'))

    @property
    def cnv_connector_shape_properties(self) -> CT_NonVisualConnectorProperties:
        """连接器图形的非可视属性"""

        return getattr(self, qn('a:cNvCxnSpPr'))


class CT_GvmlConnector(OxmlBaseElement):
    """gvml: 连接图形

    20.1.2.2.10 cxnSp (Connection Shape)

    该元素指定用于连接两个 sp 元素的连接形状。 使用 cxnSp 指定连接后，生成应用程序将确定连接器采用的确切路径。
    也就是说，连接器路由算法由生成的应用程序决定，因为所需的路径可能会根据应用程序的特定需求而有所不同。
    """

    @property
    def cn_connector_shape_properties(self) -> CT_GvmlConnectorNonVisual:
        """连接图形的非可视属性"""

        return getattr(self, qn('a:nvCxnSpPr'))

    @property
    def shape_properties(self) -> CT_ShapeProperties:
        """图形属性"""

        return getattr(self, qn('a:nvCxnSpPr'))

    @property
    def style(self) -> Optional[CT_ShapeStyle]:
        """样式"""

        return getattr(self, qn('a:style'), None)

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)


class CT_GvmlPictureNonVisual(OxmlBaseElement):
    """gvml: 图片的非视觉属性

    20.1.2.2.28 nvPicPr (Non-Visual Properties for a Picture)

    该元素指定图片的所有非视觉属性。 该元素是与图片关联的非视觉识别属性、形状属性和应用程序属性的容器。 这允许存储不影响图片外观的附加信息。
    """

    @property
    def cnv_properties(self) -> CT_NonVisualDrawingProps:
        """非可视绘图属性

        20.1.2.2.8 cNvPr

        该元素指定非可视画布属性。 这允许存储不影响图片外观的附加信息。
        """

        return getattr(self, qn('a:cNvPr'))

    @property
    def cnv_picture_properties(self) -> CT_NonVisualPictureProperties:
        """图片的非可视属性"""

        return getattr(self, qn('a:cNvPicPr'))


class CT_GvmlPicture(OxmlBaseElement):
    """gvml: 图片

    20.1.2.2.30 pic (Picture)

    该元素指定文档中是否存在图片对象。
    """

    @property
    def nv_picture_properties(self) -> CT_GvmlPictureNonVisual:
        """图片非可视属性"""

        return getattr(self, qn('a:nvPicPr'))

    @property
    def blip_fill(self) -> CT_BlipFillProperties:
        """点填充属性"""

        return getattr(self, qn('a:blipFill'))

    @property
    def shape_properties(self) -> CT_ShapeProperties:
        """点填充属性"""
        return getattr(self, qn('a:spPr'))

    @property
    def style(self) -> Optional[CT_ShapeStyle]:
        """样式"""

        return getattr(self, qn('a:style'), None)

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)


class CT_GvmlGraphicFrameNonVisual(OxmlBaseElement):
    """gvml: 图形框架的非视觉属性

    20.1.2.2.26 nvGraphicFramePr (Non-Visual Properties for a Graphic Frame)

    该元素指定图形框架的所有非视觉属性。 该元素是与图形框架关联的非视觉识别属性、形状属性和应用程序属性的容器。
    这允许存储不影响图形框架的外观的附加信息。
    """

    @property
    def cnv_properties(self) -> CT_NonVisualDrawingProps:
        """非可视绘图属性

        20.1.2.2.8 cNvPr

        该元素指定非可视画布属性。 这允许存储不影响图片外观的附加信息。
        """

        return getattr(self, qn('a:cNvPr'))

    @property
    def cnv_graphic_frame_properties(self) -> CT_NonVisualGraphicFrameProperties:
        """非可视图形框架绘图属性

        19.3.1.9 cNvGraphicFramePr

        该元素指定图形框架的非可视绘图属性。 这些非视觉属性是生成应用程序在渲染幻灯片表面时将使用的属性。
        """

        return getattr(self, qn('a:cNvGraphicFramePr'))


class CT_GvmlGraphicalObjectFrame(OxmlBaseElement):
    """gvml: 图形框架对象

    20.1.2.2.18 graphicFrame (Graphic Frame)

    该元素指定图形框架的存在。 该框架包含由外部源生成的图形，并且需要一个容器来在幻灯片表面上显示。
    """

    @property
    def nv_graphic_frame_properties(self) -> CT_GvmlGraphicFrameNonVisual:
        """非可视图形框架属性"""

        return getattr(self, qn('a:nvGraphicFramePr'))

    @property
    def graphic(self) -> CT_GraphicalObject:
        """非可视图形框架属性"""

        return getattr(self, qn('a:graphic'))

    @property
    def xfrm(self) -> CT_Transform2D:
        """图形框架的 2D 变换

        19.3.1.53 xfrm

        该元素指定要应用于相应图形框架的变换。 此变换应用于图形框架，就像应用于形状或组形状一样。
        """

        return getattr(self, qn('a:xfrm'))

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)


class CT_GvmlGroupShapeNonVisual(OxmlBaseElement):
    """gvml: 组形状的非视觉属性

    20.1.2.2.27 nvGrpSpPr (Non-Visual Properties for a Group Shape)

    该元素指定组形状的所有非视觉属性。 该元素是与组形状关联的非视觉识别属性、形状属性和应用程序属性的容器。 这允许存储不影响组形状外观的附加信息。
    """

    @property
    def cnv_properties(self) -> CT_NonVisualDrawingProps:
        """非可视绘图属性

        20.1.2.2.8 cNvPr

        该元素指定非可视画布属性。 这允许存储不影响图片外观的附加信息。
        """

        return getattr(self, qn('a:cNvPr'))

    @property
    def cnv_group_drawing_shape_properties(self) -> CT_NonVisualGroupDrawingShapeProps:
        """组形状的非视觉绘制属性"""

        return getattr(self, qn('a:cNvGrpSpPr'))


class CT_GvmlGroupShape(OxmlBaseElement):
    """gvml: 组合图形

    20.1.2.2.20 grpSp (Group shape)

    该元素指定一个组形状，表示组合在一起的许多形状。 该形状应被视为规则形状，但不是由单个几何形状来描述，而是由其中包含的所有形状几何形状组成。 在组形状中，组成该组的每个形状都按照通常的方式指定。 然而，对元素进行分组的想法是，单个变换可以同时应用于多个形状。
    """

    @property
    def nv_group_shape_properties(self) -> CT_GvmlGroupShapeNonVisual:
        """非视觉组合图形属性"""

        return getattr(self, qn('a:nvGrpSpPr'))

    @property
    def group_shape_properties(self) -> CT_GroupShapeProperties:
        """组合图形属性

        19.3.1.23 grpSpPr

        该元素指定相应组内所有形状所共有的属性。 如果组形状属性和单个形状属性之间存在任何冲突属性，则应优先考虑单个形状属性。
        """

        return getattr(self, qn('a:grpSpPr'))

    @property
    def shapes(
        self,
    ) -> list[
        CT_GvmlTextShape | CT_GvmlShape | CT_GvmlConnector | CT_GvmlPicture | CT_GvmlGraphicalObjectFrame | CT_GvmlGroupShape
    ]:
        """组合图形包含的形状"""

        tags = (
            qn('a:txSp'),  # CT_GvmlTextShape
            qn('a:sp'),  # CT_GvmlShape
            qn('a:cxnSp'),  # CT_GvmlConnector
            qn('a:pic'),  # CT_GvmlPicture
            qn('a:graphicFrame'),  # CT_GvmlGraphicalObjectFrame
            qn('a:grpSp'),  # CT_GvmlGroupShape
        )

        return self.choice_and_more(*tags)  # type: ignore

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        val = getattr(self, qn('a:extLst'), None)

        return val if val is not None else None


class ST_PresetCameraType(ST_BaseEnumType):
    """预设摄像机类型

    20.1.10.47 ST_PresetCameraType (Preset Camera Type)

    这些枚举值代表用于设置所有相机属性（包括位置）的不同算法方法。 下面的示例图像均基于以下形状:
    """

    LegacyObliqueTopLeft = 'legacyObliqueTopLeft'
    LegacyObliqueTop = 'legacyObliqueTop'
    LegacyObliqueTopRight = 'legacyObliqueTopRight'
    LegacyObliqueLeft = 'legacyObliqueLeft'
    LegacyObliqueFront = 'legacyObliqueFront'
    LegacyObliqueRight = 'legacyObliqueRight'
    LegacyObliqueBottomLeft = 'legacyObliqueBottomLeft'
    LegacyObliqueBottom = 'legacyObliqueBottom'
    LegacyObliqueBottomRight = 'legacyObliqueBottomRight'
    LegacyPerspectiveTopLeft = 'legacyPerspectiveTopLeft'
    LegacyPerspectiveTop = 'legacyPerspectiveTop'
    LegacyPerspectiveTopRight = 'legacyPerspectiveTopRight'
    LegacyPerspectiveLeft = 'legacyPerspectiveLeft'
    LegacyPerspectiveFront = 'legacyPerspectiveFront'
    LegacyPerspectiveRight = 'legacyPerspectiveRight'
    LegacyPerspectiveBottomLeft = 'legacyPerspectiveBottomLeft'
    LegacyPerspectiveBottom = 'legacyPerspectiveBottom'
    LegacyPerspectiveBottomRight = 'legacyPerspectiveBottomRight'
    OrthographicFront = 'orthographicFront'
    IsometricTopUp = 'isometricTopUp'
    IsometricTopDown = 'isometricTopDown'
    IsometricBottomUp = 'isometricBottomUp'
    IsometricBottomDown = 'isometricBottomDown'
    IsometricLeftUp = 'isometricLeftUp'
    IsometricLeftDown = 'isometricLeftDown'
    IsometricRightUp = 'isometricRightUp'
    IsometricRightDown = 'isometricRightDown'
    IsometricOffAxis1Left = 'isometricOffAxis1Left'
    IsometricOffAxis1Right = 'isometricOffAxis1Right'
    IsometricOffAxis1Top = 'isometricOffAxis1Top'
    IsometricOffAxis2Left = 'isometricOffAxis2Left'
    IsometricOffAxis2Right = 'isometricOffAxis2Right'
    IsometricOffAxis2Top = 'isometricOffAxis2Top'
    IsometricOffAxis3Left = 'isometricOffAxis3Left'
    IsometricOffAxis3Right = 'isometricOffAxis3Right'
    IsometricOffAxis3Bottom = 'isometricOffAxis3Bottom'
    IsometricOffAxis4Left = 'isometricOffAxis4Left'
    IsometricOffAxis4Right = 'isometricOffAxis4Right'
    IsometricOffAxis4Bottom = 'isometricOffAxis4Bottom'
    ObliqueTopLeft = 'obliqueTopLeft'
    ObliqueTop = 'obliqueTop'
    ObliqueTopRight = 'obliqueTopRight'
    ObliqueLeft = 'obliqueLeft'
    ObliqueRight = 'obliqueRight'
    ObliqueBottomLeft = 'obliqueBottomLeft'
    ObliqueBottom = 'obliqueBottom'
    ObliqueBottomRight = 'obliqueBottomRight'
    PerspectiveFront = 'perspectiveFront'
    PerspectiveLeft = 'perspectiveLeft'
    PerspectiveRight = 'perspectiveRight'
    PerspectiveAbove = 'perspectiveAbove'
    PerspectiveBelow = 'perspectiveBelow'
    PerspectiveAboveLeftFacing = 'perspectiveAboveLeftFacing'
    PerspectiveAboveRightFacing = 'perspectiveAboveRightFacing'
    PerspectiveContrastingLeftFacing = 'perspectiveContrastingLeftFacing'
    PerspectiveContrastingRightFacing = 'perspectiveContrastingRightFacing'
    PerspectiveHeroicLeftFacing = 'perspectiveHeroicLeftFacing'
    PerspectiveHeroicRightFacing = 'perspectiveHeroicRightFacing'
    PerspectiveHeroicExtremeLeftFacing = 'perspectiveHeroicExtremeLeftFacing'
    PerspectiveHeroicExtremeRightFacing = 'perspectiveHeroicExtremeRightFacing'
    PerspectiveRelaxed = 'perspectiveRelaxed'
    PerspectiveRelaxedModerately = 'perspectiveRelaxedModerately'


class ST_FOVAngle(ST_BaseType[AnyStr, int]):
    """视场角度

    20.1.10.26 ST_FOVAngle (Field of View Angle)

    表示 60000 度的正角。 范围为 [0, 180] 度。
    """

    def _validate(self: Self) -> None:
        int_val = int(self._val)

        if not (0 <= int_val <= 10800000):
            msg = f'预期外的值: {self._val!r}'
            raise OxmlAttributeValidateError(msg)

        self._python_val = int_val


class CT_Camera(OxmlBaseElement):
    """相机

    20.1.5.5 camera (Camera)

    该元素定义相机在 3D 场景中的位置和属性。 相机位置和属性会修改场景的视图。
    """

    @property
    def rotate(self) -> Optional[CT_SphereCoords]:
        """旋转角度（球体）"""

        return getattr(self, qn('a:rot'), None)


    @property
    def preset_type(self) -> ST_PresetCameraType:
        """预设摄像机类型

        Preset Camera Type

        定义相机元素正在使用的预设相机。 预设摄像机定义了空间中常见预设旋转的起点。
        """
        val = self.attrib['prst']

        return ST_PresetCameraType(str(val))

    @property
    def field_of_view(self) -> Optional[ST_FOVAngle]:
        """视野

        Field of View

        提供对相机默认视野的覆盖。 通过修改该属性可以获得不同的视角。
        """
        val = self.attrib.get('fov')

        return ST_FOVAngle(str(val)) if val is not None else None

    @property
    def zoom(self) -> ST_PositivePercentage:
        """缩放比例

        Zoom

        定义给定相机元素的缩放系数。 缩放会修改整个场景并相应地放大或缩小
        """
        val = self.attrib.get('zoom')

        return to_ST_PositivePercentage(str(val) if val is not None else '100%')


class ST_LightRigDirection(ST_BaseEnumType):
    """灯光装置方向

    20.1.10.29 ST_LightRigDirection (Light Rig Direction)

    表示灯光装置相对于场景的定位方向。 灯光装置本身可以由围绕给定形状的任何方向的多个灯光组成。
    这种简单的类型定义了整个灯光装置的方向，而不是装置内各个灯光的方向。
    这意味着，因为灯光装置的方向是向左的，所以不能保证光线来自形状的左侧，而是整个装置的方向向左旋转。
    """

    TopLeft = 'tl'
    """左上方的光照方向"""

    Top = 't'
    """顶部的光照方向"""

    TopRight = 'tr'
    """右上方的光照方向"""

    Left = 'l'
    """左侧的光照方向"""

    Right = 'r'
    """右侧的光照方向"""

    BottomLeft = 'bl'
    """左下方的光照方向"""

    Bottom = 'b'
    """底部的光照方向"""

    BottomRight = 'br'
    """右下方的光照方向"""


class ST_LightRigType(ST_BaseEnumType):
    """光照类型

    20.1.10.30 ST_LightRigType (Light Rig Type)

    光源组类型

    这个简单类型表示可以应用于形状的预设光源组。光源组表示一组相对于3D场景以特定方式定向的灯光。以下属性用于定义下面图像示例中使用的形状:

    - 圆角矩形形状
    - 圆形倒角类型
    - 暖色哑光材质类型
    - 由perspectiveContrastingRightFacing预设定义的相机类型
    - 倒角宽度和高度均为190500
    """

    LegacyFlat1 = 'legacyFlat1'
    LegacyFlat2 = 'legacyFlat2'
    LegacyFlat3 = 'legacyFlat3'
    LegacyFlat4 = 'legacyFlat4'
    LegacyNormal1 = 'legacyNormal1'
    LegacyNormal2 = 'legacyNormal2'
    LegacyNormal3 = 'legacyNormal3'
    LegacyNormal4 = 'legacyNormal4'
    LegacyHarsh1 = 'legacyHarsh1'
    LegacyHarsh2 = 'legacyHarsh2'
    LegacyHarsh3 = 'legacyHarsh3'
    LegacyHarsh4 = 'legacyHarsh4'
    ThreePt = 'threePt'
    Balanced = 'balanced'
    Soft = 'soft'
    Harsh = 'harsh'
    Flood = 'flood'
    Contrasting = 'contrasting'
    Morning = 'morning'
    Sunrise = 'sunrise'
    Sunset = 'sunset'
    Chilly = 'chilly'
    Freezing = 'freezing'
    Flat = 'flat'
    TwoPt = 'twoPt'
    Glow = 'glow'
    BrightRoom = 'brightRoom'


class CT_LightRig(OxmlBaseElement):
    """灯光装置

    20.1.5.9 lightRig (Light Rig)

    该元素定义与桌子(table)关联的灯光装置。 当对单元应用 3D 斜角时，灯光装置就会发挥作用。 使用 3D 时，灯光装备定义与场景关联的照明属性。
    """

    @property
    def rotate(self) -> Optional[CT_SphereCoords]:
        """旋转角度（球体）"""

        return getattr(self, qn('a:rot'), None)

    @property
    def rig_type(self) -> ST_LightRigType:
        """装置类型(预置)

        Rig Preset

        定义要应用于场景的灯光装备的预设类型。
        """

        val = self.attrib['rig']

        return ST_LightRigType(str(val))

    @property
    def direction(self) -> ST_LightRigDirection:
        """灯光方向

        Direction

        定义灯光装置相对于场景的方向。
        """

        val = self.attrib['dir']

        return ST_LightRigDirection(str(val))


class CT_Scene3D(OxmlBaseElement):
    """3D 场景属性

    20.1.4.1.26 scene3d (3D Scene Properties)

    该元素定义了应用于对象的可选场景级 3D 属性。
    """

    @property
    def camera(self) -> CT_Camera:
        """相机"""

        return getattr(self, qn('a:camera'))

    @property
    def light_rig(self) -> CT_LightRig:
        """灯光装置"""

        return getattr(self, qn('a:lightRig'))

    @property
    def backdrop(self) -> Optional[CT_Backdrop]:
        """背景平面"""

        return getattr(self, qn('a:backdrop'), None)

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展属性"""

        return getattr(self, qn('a:extLst'), None)


class CT_Backdrop(OxmlBaseElement):
    """背景平面

    Backdrop Plane

    该元素定义了一个平面，在该平面中应用发光和阴影等效果，并与它们所应用到的形状相关。
    背景中包含的点和向量定义了 3D 空间中的平面。

    20.1.5.2 backdrop (Backdrop Plane)

    L.4.6.2.4 Backdrop

        复杂类型 CT_Backdrop 定义了 3D 场景中的独特位置。
        背景是一个平坦的 2D 平面，可以容纳在 3D 空间中定向的效果，例如阴影。
        背景中包含的点和向量是相对于世界空间的。
    """

    @property
    def anchor(self) -> CT_Point3D:
        return getattr(self, qn('a:anchor'))

    @property
    def normal(self) -> CT_Vector3D:
        return getattr(self, qn('a:norm'))

    @property
    def up(self) -> CT_Vector3D:
        return getattr(self, qn('a:up'))

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展属性"""

        return getattr(self, qn('a:extLst'), None)


class ST_BevelPresetType(ST_BaseEnumType):
    """斜角预设类型

    20.1.10.9 ST_BevelPresetType (Bevel Presets)

    表示可应用于 3D 形状的斜角类型的预设。 根据为形状定义的斜角类型，斜角属性的应用方式有所不同。
    """

    RelaxedInset = 'relaxedInset'
    Circle = 'circle'
    Slope = 'slope'
    Cross = 'cross'
    Angle = 'angle'
    SoftRound = 'softRound'
    Convex = 'convex'
    CoolSlant = 'coolSlant'
    Divot = 'divot'
    Riblet = 'riblet'
    HardEdge = 'hardEdge'
    ArtDeco = 'artDeco'


class CT_Bevel(OxmlBaseElement):
    """斜角

    20.1.4.2.5 bevel (Bevel)

    此元素定义与应用于表格中单元格的 3D 效果关联的斜角属性。
    """

    def width(self) -> ST_PositiveCoordinate:
        """宽度

        Width

        指定斜角的宽度，或者斜角应用到形状中的深度。
        """

        val = self.attrib.get('w')

        return to_ST_PositiveCoordinate(str(val) if val is not None else '76200')

    def height(self) -> ST_PositiveCoordinate:
        """高度

        Height

        指定斜角的高度，或者斜角应用到的形状之上多远。
        """

        val = self.attrib.get('h')

        return to_ST_PositiveCoordinate(str(val) if val is not None else '76200')

    def preset(self) -> ST_BevelPresetType:
        """斜角类型

        Preset Bevel

        指定定义斜角外观的预设斜角类型。
        """

        val = self.attrib.get('prst')

        if val is None:
            return ST_BevelPresetType.Circle

        return ST_BevelPresetType(str(val))


class ST_PresetMaterialType(ST_BaseEnumType):
    """预设材质类型

    20.1.10.50 ST_PresetMaterialType (Preset Material Type)

    描述形状的表面外观。材质类型与光照特性结合，以创建形状的最终外观和感觉。可以组合在一起创建以下预设的一组材质属性包括:

    - 镜面颜色(Specular color) – 定义与材料关联的高光的颜色。
    - 镜面功率(Specular power) – 定义高光的大小和强度。较小的值提供较大但不太强烈的高光，而较大的值提供较小但更强烈的高光。
    - 漫反射颜色(Diffuse color) – 定义材料在直接受到光源照明的地方的感知颜色。一般来说，这里的默认颜色将基于形状的填充颜色。
    - 环境颜色(Ambient color) – 定义材料在没有直接受到光源照明的地方的感知颜色。一般来说，这里的默认颜色将基于形状的填充颜色。
    - 自发光颜色(Emissive color) – 定义由对象发出的光的颜色。
    - 漫反射菲涅耳效应(Diffuse Fresnel effect) – 这是一种在斜视角度上使材料类型的漫反射颜色变暗（趋向于黑色）或变亮（趋向于白色）的效果。正值使材料变得更亮，负值使材料变得更暗。
    - Alpha 菲涅耳效应(Alpha Fresnel effect) – 这是一种在斜视角度上使材料变得更不透明或更透明的效果。正值使材料变得更不透明，负值使材料变得更透明。

    在以下示例中，对于某些属性给出的确切值应被理解为相对值，以提供参考。这些值可能因用于渲染材料类型的技术而有所不同。以下属性用于定义下面示例图像中使用的形状:

    - 圆角矩形形状(Rounded rectangle shape)
    - 圆形斜角类型(Circle bevel type)
    - 三点光照系统类型(Three Point light rig type)
    - 由透视对比右侧预设定义的摄像机类型(Camera type defined by the perspectiveContrastingRightFacing preset)
    - 斜角宽度和高度均等于 190500(Bevel width and height each equal to 190500)
    """

    legacyMatte = 'legacyMatte'
    legacyPlastic = 'legacyPlastic'
    legacyMetal = 'legacyMetal'
    legacyWireframe = 'legacyWireframe'
    matte = 'matte'
    plastic = 'plastic'
    metal = 'metal'
    warmMatte = 'warmMatte'
    translucentPowder = 'translucentPowder'
    powder = 'powder'
    dkEdge = 'dkEdge'
    softEdge = 'softEdge'
    clear = 'clear'
    flat = 'flat'
    softmetal = 'softmetal'


class CT_Shape3D(OxmlBaseElement):
    """3D图形属性

    21.4.5.6 sp3d (3-D Shape Properties)

    形状可以包含的一组 3-D 属性。

    L.4.6.3.2.2 Shape 3-D

    复杂类型 CT_Shape3D 定义与单个形状关联的所有 3-D 属性。 形状可以有两个斜角，一个在顶部，一个在底部。 还定义了挤出颜色，应用该颜色时，会将颜色应用于挤出的表面。 还有一个挤出宽度，它定义了挤出的宽度。 可以为形状定义轮廓颜色和宽度。 Zaxi 锚点是在复杂类型中定义的，是相对于形状顶面的锚点。 形状 3-D 复合类型也包含当前材料。 最后，形状 3-D 包含另一个元素，就像之前的复杂类型一样，用于将来的可扩展性。 CT_Shape3D 复杂类型按以下方式定义:

    """

    @property
    def bevel_top(self) -> Optional[CT_Bevel]:
        """顶部斜角"""

        return getattr(self, qn('a:bevelT'), None)

    @property
    def bevel_bottom(self) -> Optional[CT_Bevel]:
        """底部斜角"""

        return getattr(self, qn('a:bevelB'), None)

    @property
    def extrusion_color(self) -> Optional[CT_Color]:
        """挤压色"""

        return getattr(self, qn('a:extrusionClr'), None)

    @property
    def contour_color(self) -> Optional[CT_Color]:
        """轮廓颜色"""

        return getattr(self, qn('a:contourClr'), None)

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展属性"""

        return getattr(self, qn('a:extLst'), None)

    @property
    def z_coordinate(self) -> ST_Coordinate:
        """z坐标

        Shape Depth

        定义 3D 形状的 z 坐标。
        """

        val = self.attrib.get('z')

        return to_ST_Coordinate(str(val) if val is not None else '0')

    @property
    def contour_width(self) -> ST_PositiveCoordinate:
        """轮廓宽度

        Contour Width

        定义形状上轮廓的宽度。
        """

        val = self.attrib.get('contourW')

        return to_ST_PositiveCoordinate(str(val) if val is not None else '0')

    @property
    def extrusion_height(self) -> ST_PositiveCoordinate:
        """拉伸高度

        Extrusion Height

        定义应用于形状的拉伸高度。
        """

        val = self.attrib.get('extrusionH')

        return to_ST_PositiveCoordinate(str(val) if val is not None else '0')

    @property
    def prst_material(self) -> ST_PresetMaterialType:
        """预设材质

        Preset Material Type

        定义与照明属性相结合的预设材质，以提供形状的最终外观和感觉。
        """

        val = self.attrib.get('prstMaterial')

        return ST_PresetMaterialType(str(val) if val is not None else ST_PresetMaterialType.warmMatte)


class CT_FlatText(OxmlBaseElement):
    """平面文本

    20.1.5.8 flatTx (No text in 3D scene)

    将文本完全排除在 3D 场景之外。

    L.4.6.3.2.3 Flat Text

    复杂类型 CT_FlatText 定义 3D 场景中的文本对象，该对象应在 3D 场景之外呈现为普通、平面文本覆盖。
    """

    @property
    def z_coordinate(self) -> ST_Coordinate:
        """z坐标

        (Z Coordinate)

        指定用于在 3D 场景中定位平面文本的 Z 坐标。
        """

        val = self.attrib.get('z')

        return to_ST_Coordinate(str(val) if val is not None else '0')


class EG_Text3D(OxmlBaseElement):
    """3D中的文本

    <xsd:group name="EG_Text3D">
        <xsd:choice>
            <xsd:element name="sp3d" type="CT_Shape3D" minOccurs="1" maxOccurs="1"/>
            <xsd:element name="flatTx" type="CT_FlatText" minOccurs="1" maxOccurs="1"/>
        </xsd:choice>
    </xsd:group>
    """

    text3d_tags = (
        qn('a:sp3d'),  # CT_Shape3D
        qn('a:flatTx'),  # CT_FlatText
    )

    # Optional[Union[CT_Shape3D, CT_FlatText]]


class CT_AlphaBiLevelEffect(OxmlBaseElement):
    """Alpha双水平效应

    20.1.8.1 alphaBiLevel (Alpha Bi-Level Effect)

    该元素代表 Alpha 双级效应。

    小于阈值的 Alpha（不透明度）值将更改为 0（完全透明），大于或等于阈值的 Alpha 值将更改为 100%（完全不透明）。
    """

    @property
    def threshold(self) -> ST_PositiveFixedPercentage:
        """阈值

        Threshold

        指定 alpha 双水平效应的阈值。
        """

        val = self.attrib['thresh']

        return to_ST_PositiveFixedPercentage(str(val))


class CT_AlphaCeilingEffect(OxmlBaseElement):
    """该元素代表阿尔法天花板效果

    20.1.8.2 alphaCeiling (Alpha Ceiling Effect)

    该元素代表阿尔法天花板效果

    大于零的 Alpha（不透明度）值将更改为 100%。 换句话说，任何部分不透明的东西都会变得完全不透明。
    """



class CT_AlphaFloorEffect(OxmlBaseElement):
    """阿尔法地板效果

    20.1.8.3 alphaFloor (Alpha Floor Effect)

    该元素代表阿尔法地板效果。

    小于 100% 的 Alpha（不透明度）值将更改为零。 换句话说，任何部分透明的东西都会变得完全透明。
    """



class CT_AlphaInverseEffect(EG_ColorChoice):
    """阿尔法逆效果

    20.1.8.4 alphaInv (Alpha Inverse Effect)

    该元素代表阿尔法逆效果。

    Alpha（不透明度）值通过从 100% 中减去来反转。
    """

    @property
    def color(
        self,
    ) -> Optional[
        CT_ScRgbColor | CT_SRgbColor | CT_HslColor | CT_SystemColor | CT_SchemeColor | CT_PresetColor
    ]:
        """颜色

        <xsd:group ref="EG_ColorChoice" minOccurs="0" maxOccurs="1"/>
        """

        return self.choice_one_child(*self.color_tags)  # type: ignore


class CT_AlphaModulateFixedEffect(OxmlBaseElement):
    """Alpha 调制固定效果

    20.1.8.6 alphaModFix (Alpha Modulate Fixed Effect)

    该元素代表阿尔法调制固定效应。

    效果 alpha（不透明度）值乘以固定百分比。
    """

    @property
    def amount(self) -> ST_PositivePercentage:
        """缩放量

        Amount

        指定缩放 Alpha 的百分比量。
        """
        val = self.attrib.get('amt')

        return to_ST_PositivePercentage(str(val) if val is not None else '100%')


class CT_AlphaOutsetEffect(OxmlBaseElement):
    """Alpha 插入/起始效果

    20.1.8.7 alphaOutset (Alpha Inset/Outset Effect)

    该元素指定 Alpha 开始/插入效果。

    这相当于 alpha 上限，然后是 alpha 模糊，然后是 alpha 上限（正半径）或 alpha 下限（负半径）。
    """

    @property
    def radius(self) -> ST_Coordinate:
        """半径

        Radius

        指定起始/插入的半径。
        """
        val = self.attrib.get('rad')

        return to_ST_Coordinate(str(val) if val is not None else '0')


class CT_AlphaReplaceEffect(OxmlBaseElement):
    """Alpha 插入/起始效果

    20.1.8.8 alphaRepl (Alpha Replace Effect)

    该元素指定 alpha 替换效果。

    效果 alpha（不透明度）值被替换为固定的 alpha 值 。
    """

    @property
    def alpha(self) -> ST_PositiveFixedPercentage:
        """阿尔法值

        Alpha

        指定新的不透明度值。
        """
        val = self.attrib['a']

        return to_ST_PositiveFixedPercentage(str(val) if val is not None else '0%')


class CT_BiLevelEffect(OxmlBaseElement):
    """双层（黑/白）效果

    20.1.8.11 biLevel (Bi-Level (Black/White) Effect)

    该元素指定双层（黑/白）效果。 亮度低于指定阈值的输入颜色将更改为黑色。 亮度大于或等于指定值的输入颜色设置为白色。 Alpha 效果值不受此效果的影响。
    """

    @property
    def threshold(self) -> ST_PositiveFixedPercentage:
        """阈值

        Threshold

        指定 Bi-Level 效果的亮度阈值。 大于或等于阈值的值设置为白色。 小于阈值的值设置为黑色。
        """

        val = self.attrib['thresh']

        return to_ST_PositiveFixedPercentage(str(val))


class CT_BlurEffect(OxmlBaseElement):
    """模糊效果

    20.1.8.15 blur (Blur Effect)

    该元素指定应用于整个形状（包括其填充）的模糊效果。 所有颜色通道（包括 Alpha）都会受到影响。
    """

    @property
    def radius(self) -> ST_PositiveCoordinate:
        """半径

        Radius

        指定模糊半径。
        """

        val = self.attrib.get('rad')

        return to_ST_PositiveCoordinate(str(val) if val is not None else '0')

    @property
    def grow_bounds(self) -> XSD_Boolean:
        """边界成长

        Grow Bounds

        指定对象的边界是否应因模糊而增大。 True 表示边界已增长，而 false 表示边界未增长。
        """

        val = self.attrib.get('grow')

        return to_xsd_bool(val, none=True)


class CT_ColorChangeEffect(OxmlBaseElement):
    """变色效果

    20.1.8.16 clrChange (Color Change Effect)

    该元素指定颜色变化效果。 clrFrom 的实例替换为 clrTo 的实例。
    """

    @property
    def color_from(self) -> CT_Color:
        """来源颜色"""

        return getattr(self, qn('a:clrFrom'))

    @property
    def color_to(self) -> CT_Color:
        """目标颜色"""

        return getattr(self, qn('a:clrTo'))

    @property
    def use_alpha(self) -> XSD_Boolean:
        """考虑阿尔法值

        Consider Alpha Values

        指定效果是否考虑 alpha 值。 如果 useA 为 true，则考虑效果 alpha 值，否则将忽略它们。
        """

        val = self.attrib.get('useA')

        return to_xsd_bool(val, none=True)


class CT_ColorReplaceEffect(EG_ColorChoice):
    """纯色更换

    20.1.8.18 clrRepl (Solid Color Replacement)

    该元素指定纯色替换值。 所有效果颜色都更改为固定颜色。 Alpha 值不受影响。
    """

    @property
    def color(
        self,
    ) -> CT_ScRgbColor | CT_SRgbColor | CT_HslColor | CT_SystemColor | CT_SchemeColor | CT_PresetColor:
        """颜色

        <xsd:group ref="EG_ColorChoice" minOccurs="1" maxOccurs="1"/>
        """

        return self.choice_require_one_child(*self.color_tags)  # type: ignore


class CT_DuotoneEffect(EG_ColorChoice):
    """双色调效果

    20.1.8.23 duotone (Duotone Effect)

    该元素指定双色调效果。

    对于每个像素，通过线性插值组合 clr1 和 clr2 以确定该像素的新颜色。
    """

    @property
    def colors(
        self,
    ) -> list[
        CT_ScRgbColor | CT_SRgbColor | CT_HslColor | CT_SystemColor | CT_SchemeColor | CT_PresetColor
    ]:
        """
         <xsd:complexType name="CT_DuotoneEffect">
            <xsd:sequence>
                <xsd:group ref="EG_ColorChoice" minOccurs="2" maxOccurs="2"/>
            </xsd:sequence>
        </xsd:complexType>
        """

        elements = self.choice_and_more(*self.color_tags)

        if len(elements) != 2:
            msg = '颜色元素个数应为2'
            raise OxmlElementValidateError(msg)

        return elements  # type: ignore


class CT_GlowEffect(EG_ColorChoice):
    """发光效果

    20.1.8.32 glow (Glow Effect)

    该元素指定发光效果，其中在对象边缘外部添加颜色模糊轮廓。
    """

    @property
    def color(
        self,
    ) -> CT_ScRgbColor | CT_SRgbColor | CT_HslColor | CT_SystemColor | CT_SchemeColor | CT_PresetColor:
        """颜色

        <xsd:group ref="EG_ColorChoice" minOccurs="1" maxOccurs="1"/>
        """

        return self.choice_require_one_child(*self.color_tags)  # type: ignore

    @property
    def radius(self) -> ST_PositiveCoordinate:
        """半径

        Radius

        指定发光的半径。

        <xsd:attribute name="rad" type="ST_PositiveCoordinate" use="optional" default="0"/>
        """

        val = self.attrib.get('rad')

        return to_ST_PositiveCoordinate(str(val) if val is not None else '0')


class CT_GrayscaleEffect(OxmlBaseElement):
    """灰度效果

    20.1.8.34 grayscl (Gray Scale Effect)

    该元素指定灰度效果。 将所有效果颜色值转换为与其亮度相对应的灰色阴影。 效果 alpha（不透明度）值不受影响。
    """



class CT_HSLEffect(OxmlBaseElement):
    """色相饱和度亮度效果

    20.1.8.39 hsl (Hue Saturation Luminance Effect)

    该元素指定色调/饱和度/亮度效果。 色调、饱和度和亮度均可以相对于其当前值进行调整。
    """

    @property
    def hue(self) -> ST_PositiveFixedAngle:
        """色调

        Hue

        指定色调调整的度数。
        """

        val = self.attrib.get('hue')

        return to_ST_PositiveFixedAngle(str(val) if val is not None else '0')

    @property
    def luminance(self) -> ST_PositiveFixedAngle:
        """亮度

        Luminance

        指定亮度调整的百分比。
        """

        val = self.attrib.get('sat')

        return to_ST_PositiveFixedAngle(str(val) if val is not None else '0%')

    @property
    def saturation(self) -> ST_FixedPercentage:
        """饱和度

        Saturation

        指定饱和度调整的百分比。
        """

        val = self.attrib.get('sat')

        return to_ST_FixedPercentage(str(val) if val is not None else '0%')


class CT_InnerShadowEffect(EG_ColorChoice):
    """内阴影效果

    20.1.8.40 innerShdw (Inner Shadow Effect)

    该元素指定内部阴影效果。 根据属性给定的参数，在对象的边缘内应用阴影。
    """

    @property
    def color(
        self,
    ) -> CT_ScRgbColor | CT_SRgbColor | CT_HslColor | CT_SystemColor | CT_SchemeColor | CT_PresetColor:
        """颜色

        <xsd:group ref="EG_ColorChoice" minOccurs="1" maxOccurs="1"/>
        """

        return self.choice_require_one_child(*self.color_tags)  # type: ignore

    @property
    def blur_radius(self) -> ST_PositiveCoordinate:
        """模糊半径

        Blur Radius

        指定模糊半径。
        """

        val = self.attrib.get('blurRad')

        return to_ST_PositiveCoordinate(str(val) if val is not None else '0')

    @property
    def direction(self) -> ST_PositiveFixedAngle:
        """方向

        Direction

        指定偏移阴影的方向。
        """

        val = self.attrib.get('dist')

        return to_ST_PositiveFixedAngle(str(val) if val is not None else '0')

    @property
    def distance(self) -> ST_PositiveCoordinate:
        """距离

        Distance

        指定阴影偏移的距离。
        """

        val = self.attrib.get('dir')

        return to_ST_PositiveCoordinate(str(val) if val is not None else '0')


class CT_LuminanceEffect(OxmlBaseElement):
    """亮度效果

    20.1.8.42 lum (Luminance Effect)

    该元素指定亮度效果。 亮度使所有颜色线性地接近白色或黑色。 对比度使所有颜色变得更近或更远。
    """

    @property
    def brightness(self) -> ST_FixedPercentage:
        """亮度百分比

        Brightness

        指定更改亮度的百分比。
        """

        val = self.attrib.get('bright')

        return to_ST_FixedPercentage(str(val) if val is not None else '0%')

    @property
    def contrast(self) -> ST_FixedPercentage:
        """对比度百分比

        Contrast

        指定更改对比度的百分比。
        """

        val = self.attrib.get('contrast')

        return to_ST_FixedPercentage(str(val) if val is not None else '0%')


class CT_OuterShadowEffect(EG_ColorChoice):
    """外阴影效果

    20.1.8.45 outerShdw (Outer Shadow Effect)

    该元素指定外部阴影效果。
    """

    @property
    def color(
        self,
    ) -> CT_ScRgbColor | CT_SRgbColor | CT_HslColor | CT_SystemColor | CT_SchemeColor | CT_PresetColor:
        """颜色

        <xsd:group ref="EG_ColorChoice" minOccurs="1" maxOccurs="1"/>
        """

        return self.choice_require_one_child(*self.color_tags)  # type: ignore

    @property
    def blur_radius(self) -> ST_PositiveCoordinate:
        """模糊半径

        Blur Radius

        指定模糊半径。
        """

        val = self.attrib.get('blurRad')

        return to_ST_PositiveCoordinate(str(val) if val is not None else '0')

    @property
    def distance(self) -> ST_PositiveCoordinate:
        """距离

        Shadow Offset Distance

        指定阴影偏移的距离。
        """

        val = self.attrib.get('dist')

        return to_ST_PositiveCoordinate(str(val) if val is not None else '0')

    @property
    def direction(self) -> ST_PositiveFixedAngle:
        """方向

        Direction

        指定偏移阴影的方向。
        """

        val = self.attrib.get('dir')

        return to_ST_PositiveFixedAngle(str(val) if val is not None else '0')

    @property
    def horizontal_scale(self) -> ST_Percentage:
        """水平缩放因子 sx

        Horizontal Scaling Factor

        指定水平缩放因子； 负缩放会导致翻转。
        """

        val = self.attrib.get('sx')

        return to_ST_Percentage(str(val) if val is not None else '100%')

    @property
    def vertical_scale(self) -> ST_Percentage:
        """垂直缩放因子 sy

        Vertical Scaling Factor

        指定垂直缩放因子； 负缩放会导致翻转。
        """

        val = self.attrib.get('sy')

        return to_ST_Percentage(str(val) if val is not None else '100%')

    @property
    def horizontal_skew(self) -> ST_FixedAngle:
        """水平倾斜角度 kx

        Horizontal Skew

        指定水平倾斜角度。
        """

        val = self.attrib.get('kx')

        return to_ST_FixedAngle(str(val) if val is not None else '0')

    @property
    def vertical_skew(self) -> ST_FixedAngle:
        """垂直倾斜角度 ky

        Vertical Skew

        指定垂直倾斜角度。
        """

        val = self.attrib.get('ky')

        return to_ST_FixedAngle(str(val) if val is not None else '0')

    @property
    def shadow_alignment(self) -> ST_RectAlignment:
        """方向 algn

        Shadow Alignment

        指定阴影对齐方式； 首先进行对齐，有效地设置缩放、倾斜和偏移的原点。
        """

        val = self.attrib.get('algn')

        if val is None:
            return ST_RectAlignment.Bottom

        return ST_RectAlignment(str(val))

    @property
    def rotate_with_shape(self) -> bool:
        """是否随形状旋转 rotWithShape

        Rotate With Shape

        指定如果形状旋转，阴影是否随形状旋转。
        """

        val = self.attrib.get('rotWithShape')

        return utils.XsdBool(val, none=True)


class ST_PresetShadowVal(ST_BaseEnumType):
    """预设阴影类型

    20.1.10.52 ST_PresetShadowVal (Preset Shadow Type)

    这个简单类型表示 20 种预设阴影类型之一。每个枚举值的描述都说明了该值表示的阴影类型。
    每个描述都包含预设的外部阴影效果的参数，以及所有 prstShdw 效果共有的属性。

    [备注: 效果参数参考文档列表]
    """

    Shadow1 = 'shdw1'  # Top Left Drop Shadow
    Shadow2 = 'shdw2'  # Top Right Drop Shadow
    Shadow3 = 'shdw3'  # Back Left Perspective Shadow
    Shadow4 = 'shdw4'  # Back Right Perspective Shadow
    Shadow5 = 'shdw5'  # Bottom Left Drop Shadow
    Shadow6 = 'shdw6'  # Bottom Right Drop Shadow
    Shadow7 = 'shdw7'  # Front Left Perspective Shadow
    Shadow8 = 'shdw8'  # Front Right Perspective Shadow
    Shadow9 = 'shdw9'  # Top Left Small Drop Shadow
    Shadow10 = 'shdw10'  # Top Left Large Drop Shadow
    Shadow11 = 'shdw11'  # Back Left Long Perspective Shadow
    Shadow12 = 'shdw12'  # Back Right Long Perspective Shadow
    Shadow13 = 'shdw13'  # Top Left Double Drop Shadow
    Shadow14 = 'shdw14'  # Bottom Right Small Drop Shadow
    Shadow15 = 'shdw15'  # Front Left Long Perspective Shadow
    Shadow16 = 'shdw16'  # Front Right LongPerspective Shadow
    Shadow17 = 'shdw17'  # 3D Outer Box Shadow
    Shadow18 = 'shdw18'  # 3D Inner Box Shadow
    Shadow19 = 'shdw19'  # Back Center Perspective Shadow
    Shadow20 = 'shdw20'  # Front Bottom Shadow


class CT_PresetShadowEffect(EG_ColorChoice):
    """预设阴影

    20.1.8.49 prstShdw (Preset Shadow)

    该元素指定要使用预设阴影。 每个预设阴影相当于一个特定的外阴影效果。
    对于每个预设阴影，颜色元素、方向属性和距离属性分别代表对应外阴影的颜色、方向和距离参数。
    另外，相应外阴影的rotateWithShape属性始终为false。 外部阴影的其他非默认参数取决于 pst 属性。
    """

    @property
    def color(
        self,
    ) -> CT_ScRgbColor | CT_SRgbColor | CT_HslColor | CT_SystemColor | CT_SchemeColor | CT_PresetColor:
        """颜色

        <xsd:group ref="EG_ColorChoice" minOccurs="1" maxOccurs="1"/>
        """

        return self.choice_require_one_child(*self.color_tags)  # type: ignore

    @property
    def preset(self) -> ST_PresetShadowVal:
        """预设阴影

        Preset Shadow

        指定要使用的预设阴影。
        """

        val = self.attrib['prst']

        return ST_PresetShadowVal(str(val))

    @property
    def distance(self) -> ST_PositiveCoordinate:
        """

        Distance

        指定阴影偏移的距离。
        """

        val = self.attrib.get('dist')

        return to_ST_PositiveCoordinate(str(val) if val is not None else '0')

    @property
    def direction(self) -> ST_PositiveFixedAngle:
        """方向

        Direction

        指定偏移阴影的方向。
        """

        val = self.attrib.get('dir')

        return to_ST_PositiveFixedAngle(str(val) if val is not None else '0')


class CT_ReflectionEffect(OxmlBaseElement):
    """反射效果

    20.1.8.50 reflection (Reflection Effect)

    该元素指定反射效果。
    """

    @property
    def blur_radius(self) -> ST_PositiveCoordinate:
        """模糊半径 blurRad

        Blur Radius

        指定模糊半径。
        """

        val = self.attrib.get('blurRad')

        return to_ST_PositiveCoordinate(str(val) if val is not None else '0')

    @property
    def start_opcacity(self) -> ST_PositiveFixedPercentage:
        """开始不透明度 stA

        Start Opacity

        开始反射不透明度。
        """

        return to_ST_PositiveFixedPercentage(str(self.attrib.get('stA', '100%')))

    @property
    def start_position(self) -> ST_PositiveFixedPercentage:
        """起始位置 stPos

        Start Position

        指定起始 Alpha 值的起始位置（沿着 Alpha 渐变斜坡）。
        """

        return to_ST_PositiveFixedPercentage(str(self.attrib.get('stPos', '0%')))

    @property
    def end_opcacity(self) -> ST_PositiveFixedPercentage:
        """结束不透明度 endA

        End Alpha

        指定结束反射不透明度
        """

        return to_ST_PositiveFixedPercentage(str(self.attrib.get('endA', '0%')))

    @property
    def end_position(self) -> ST_PositiveFixedPercentage:
        """结束位置 endPos

        End Position

        指定结束 alpha 值的结束位置（沿着 alpha 渐变斜坡）。
        """

        return to_ST_PositiveFixedPercentage(str(self.attrib.get('endPos', '100%')))

    @property
    def distance(self) -> ST_PositiveCoordinate:
        """距离 dist

        Distance

        指定阴影的距离。
        """

        return to_ST_PositiveCoordinate(str(self.attrib.get('dist', '0')))

    @property
    def direction(self) -> ST_PositiveFixedAngle:
        """方向

        Direction

        指定偏移阴影的方向。
        """

        return to_ST_PositiveFixedAngle(str(self.attrib.get('dir', '0')))

    @property
    def fade_direction(self) -> ST_PositiveFixedAngle:
        """淡入淡出方向 fadeDir

        Fade Direction

        指定偏移反射的方向。
        """

        return to_ST_PositiveFixedAngle(str(self.attrib.get('fadeDir', '5400000')))

    @property
    def horizontal_scale(self) -> ST_Percentage:
        """水平缩放因子 sx

        Horizontal Scaling Factor

        指定水平缩放因子； 负缩放会导致翻转。
        """

        return to_ST_Percentage(str(self.attrib.get('sx', '100%')))

    @property
    def vertical_scale(self) -> ST_Percentage:
        """垂直缩放因子 sy

        Vertical Scaling Factor

        指定垂直缩放因子； 负缩放会导致翻转。
        """

        return to_ST_Percentage(str(self.attrib.get('sy', '100%')))

    @property
    def horizontal_skew(self) -> ST_FixedAngle:
        """水平倾斜角度 kx

        Horizontal Skew

        指定水平倾斜角度。
        """

        return to_ST_FixedAngle(str(self.attrib.get('kx', '0')))

    @property
    def vertical_skew(self) -> ST_FixedAngle:
        """垂直倾斜角度 ky

        Vertical Skew

        指定垂直倾斜角度。
        """

        return to_ST_FixedAngle(str(self.attrib.get('ky', '0')))

    @property
    def shadow_alignment(self) -> ST_RectAlignment:
        """矩形对齐 方向 algn

        20.1.10.53 ST_RectAlignment Shadow Alignment

        指定阴影对齐方式； 首先进行对齐，有效地设置缩放、倾斜和偏移的原点。
        """

        val = self.attrib.get('algn')

        if val is None:
            return ST_RectAlignment.Bottom

        return ST_RectAlignment(utils.AnyStrToStr(val))  # type: ignore

    @property
    def rotate_with_shape(self) -> XSD_Boolean:
        """是否随形状旋转 rotWithShape

        Rotate With Shape

        指定如果形状旋转，阴影是否随形状旋转。
        """

        val = self.attrib.get('rotWithShape')

        return to_xsd_bool(val, none=True)


class CT_RelativeOffsetEffect(OxmlBaseElement):
    """相对偏移效果

    20.1.8.51 relOff (Relative Offset Effect)

    该元素指定相对偏移效果。 通过相对于前一个效果的大小进行偏移来设置新原点。
    """

    @property
    def offset_x(self) -> ST_Percentage:
        """X轴偏移 tx

        Offset X

        指定 X 偏移。
        """

        return to_ST_Percentage(str(self.attrib.get('tx', '0%')))

    @property
    def offset_y(self) -> ST_Percentage:
        """Y轴偏移 ty

        Offset Y

        指定垂直缩放因子； 负缩放会导致翻转。
        """

        return to_ST_Percentage(str(self.attrib.get('ty', '0%')))


class CT_SoftEdgesEffect(OxmlBaseElement):
    """软边缘效果

    20.1.8.53 softEdge (Soft Edge Effect)

    该元素指定软边缘效果。 形状的边缘变得模糊，而填充不受影响。
    """

    @property
    def radius(self) -> ST_PositiveCoordinate:
        """半径 rad

        Radius

        指定应用于边缘的模糊半径
        """

        val = self.attrib['rad']

        return to_ST_PositiveCoordinate(val)


class CT_TintEffect(OxmlBaseElement):
    """色调效果

    20.1.8.60 tint (Tint Effect)

    该元素指定色调效果。 将效果颜色值向/远离色调移动指定的量

    注意: 与 CT_PositiveFixedPercentage 类 表示的 tint 节点有冲突
    """

    @property
    def hue(self) -> ST_PositiveFixedAngle:
        """色调 hue

        Hue

        指定要着色的色调。

        """

        val = self.attrib.get('hue', '0')

        return to_ST_PositiveFixedAngle(str(val))

    @property
    def amount(self) -> ST_FixedPercentage:
        """量 amt

        Amount

        指定颜色值移动的量。
        """

        val = self.attrib.get('amt', '0%')

        return to_ST_FixedPercentage(str(val))


class CT_TransformEffect(OxmlBaseElement):
    """变换效果

    20.1.8.61 xfrm (Transform Effect)

    该元素指定变换效果。 使用以下矩阵将变换应用于形状几何中的每个点:

    | sx       tan(kx)  tx |     | x |

    | tan(ky)  sy       ty |  *  | y |

    | 0        0         1 |     | 1 |
    """

    @property
    def horizontal_scale(self) -> ST_Percentage:
        """水平缩放因子 sx

        Horizontal Scaling Factor

        指定水平缩放因子； 负缩放会导致翻转。
        """

        return to_ST_Percentage(str(self.attrib.get('sx', '100%')))

    @property
    def vertical_scale(self) -> ST_Percentage:
        """垂直缩放因子 sy

        Vertical Scaling Factor

        指定垂直缩放因子； 负缩放会导致翻转。
        """

        return to_ST_Percentage(str(self.attrib.get('sy', '100%')))

    @property
    def horizontal_skew(self) -> ST_FixedAngle:
        """水平倾斜角度 kx

        Horizontal Skew

        指定水平倾斜角度。
        """

        return to_ST_FixedAngle(str(self.attrib.get('kx', '0')))

    @property
    def vertical_skew(self) -> ST_FixedAngle:
        """垂直倾斜角度 ky

        Vertical Skew

        指定垂直倾斜角度。
        """

        return to_ST_FixedAngle(str(self.attrib.get('ky', '0')))

    @property
    def offset_x(self) -> ST_Percentage:
        """X轴偏移 tx

        Offset X

        指定 X 偏移。
        """

        return to_ST_Percentage(str(self.attrib.get('tx', '0%')))

    @property
    def offset_y(self) -> ST_Percentage:
        """Y轴偏移 ty

        Offset Y

        指定垂直缩放因子； 负缩放会导致翻转。
        """

        return to_ST_Percentage(str(self.attrib.get('ty', '0%')))


class CT_NoFillProperties(OxmlBaseElement):
    """无填充

    20.1.8.44 noFill (No Fill)

    该元素指定不向父元素应用填充。
    """



class CT_SolidColorFillProperties(EG_ColorChoice):
    """纯色填充

    20.1.8.54 solidFill (Solid Fill)

    该元素指定纯色填充。 该形状完全用指定的颜色填充。
    """

    @property
    def color(
        self,
    ) -> Optional[
        CT_ScRgbColor | CT_SRgbColor | CT_HslColor | CT_SystemColor | CT_SchemeColor | CT_PresetColor
    ]:
        """颜色

        <xsd:group ref="EG_ColorChoice" minOccurs="1" maxOccurs="1"/>
        """

        return self.choice_one_child(*self.color_tags)  # type: ignore


class CT_LinearShadeProperties(OxmlBaseElement):
    """线性渐变填充

    20.1.8.41 lin (Linear Gradient Fill)

    该元素指定线性渐变。
    """

    @property
    def angle(self) -> Optional[ST_PositiveFixedAngle]:
        """角度 ang

        Angle

        指定渐变颜色变化的方向。 要定义该角度，请将其值设为 x 顺时针测量。
        那么 ( -sin x, cos x ) 是与渐变填充中恒定颜色线平行的向量。
        """

        val = self.attrib.get('ang')

        if val is None:
            return None

        return to_ST_PositiveFixedAngle(str(val))

    @property
    def scaled(self) -> XSD_Boolean:
        """缩放的 scaled

        Scaled

        渐变角度是否随填充区域缩放。

        从数学上讲，如果此标志为 true，则梯度向量 ( cos x , sin x ) 将按填充区域的宽度 (w) 和高度 (h) 缩放，
        从而向量变为 ( w cos x, h sin x ）（标准化之前）。
        现在观察一下，如果渐变角度为 45 度，则渐变向量为 ( w, h )，它从填充区域的左上角到右下角。

        如果此标志为 false，则渐变角度与填充区域无关，并且不会使用上述操作进行缩放。
        因此，45 度的渐变角总是给出一个渐变带，其恒定颜色线平行于向量 (1, -1)。
        """

        val = self.attrib.get('scaled')

        return to_xsd_bool(val)


class ST_PathShadeType(ST_BaseEnumType):
    """路径阴影类型

    20.1.10.38 ST_PathShadeType (Path Shade Type)

    这个简单的类型描述了路径渐变阴影所遵循的路径形状。
    """

    Circle = 'circle'
    """渐变遵循圆形路径"""

    Rectange = 'rect'
    """渐变遵循矩形路径"""

    Shape = 'shape'
    """渐变跟随形状"""


class CT_PathShadeProperties(OxmlBaseElement):
    """路径阴影属性(路径渐变)

    20.1.8.46 path (Path Gradient)

    该元素定义渐变填充遵循路径与线性线。
    """

    @property
    def fill_to_rect(self) -> Optional[CT_RelativeRect]:
        """fillToRect"""

        return getattr(self, qn('a:fillToRect'), None)

    @property
    def path(self) -> Optional[ST_PathShadeType]:
        """渐变填充路径 path

        Gradient Fill Path

        指定要遵循的路径的形状。
        """

        val = self.attrib.get('path')

        if val is None:
            return None

        return ST_PathShadeType(val)


class EG_ShadeProperties(OxmlBaseElement):
    """
    阴影属性组合

    <xsd:group name="EG_ShadeProperties">
        <xsd:choice>
            <xsd:element name="lin" type="CT_LinearShadeProperties" minOccurs="1" maxOccurs="1"/>
            <xsd:element name="path" type="CT_PathShadeProperties" minOccurs="1" maxOccurs="1"/>
        </xsd:choice>
    </xsd:group>
    """

    shade_tags = (
        # 线性渐变
        qn('a:lin'),  # CT_LinearShadeProperties
        # 路径阴影属性(路径渐变)
        qn('a:path'),  # CT_PathShadeProperties
    )


class ST_TileFlipMode(ST_BaseEnumType):
    """平铺翻转模式

    20.1.10.86 ST_TileFlipMode (Tile Flip Mode)

    此简单类型指示在使用图块区域填充较大的填充区域时是否/如何翻转图块区域的内容。
    """

    none = 'none'  # None
    """平铺不翻转。"""

    x = 'x'  # Horizontal
    """平铺在水平方向翻转。"""

    y = 'y'  # Vertical
    """平铺在垂直方向翻转。"""

    xy = 'xy'  # Horizontal and Vertical
    """平铺在水平和垂直方向都翻转。"""


class CT_GradientStop(EG_ColorChoice):
    """渐变停止点

    18.8.38 stop (Gradient Stop)

    构成此渐变填充的两个或多个渐变停止点序列之一。
    """

    @property
    def color(
        self,
    ) -> CT_ScRgbColor | CT_SRgbColor | CT_HslColor | CT_SystemColor | CT_SchemeColor | CT_PresetColor:
        """颜色

        <xsd:group ref="EG_ColorChoice" minOccurs="1" maxOccurs="1"/>
        """

        return self.choice_require_one_child(*self.color_tags)  # type: ignore

    @property
    def position(self) -> ST_PositiveFixedPercentage:
        """
        Gradient Stop Position

        该梯度停止点的位置信息。 解释完全类似于渐变填充左、右、下、上。
        这里指示的位置表示颜色纯的点。 在此位置之前和之后，颜色可以过渡（或纯颜色，取决于这是否是最后一站）。
        """

        return to_ST_PositiveFixedPercentage(str(self.attrib['pos']))


class CT_GradientStopList(OxmlBaseElement):
    """渐变停止点列表

    20.1.8.37 gsLst (Gradient Stop List)

    渐变停止点列表，指定渐变颜色及其在色带中的相对位置。
    """

    @property
    def gradient_stops(self) -> list[CT_GradientStop]:
        """渐变停止点 <a:gs>

        Gradient Stop

        [注意, 该渐变停止点最少两个.]

        <xsd:element name="gs" type="CT_GradientStop" minOccurs="2" maxOccurs="unbounded"/>
        """

        return self.findall(qn('a:gs'))  # type: ignore


class CT_GradientFillProperties(EG_ShadeProperties):
    """渐变填充(属性)

    20.1.8.33 gradFill (Gradient Fill)

    该元素定义渐变填充。

    渐变填充是一种填充，其特征是从一种颜色平滑逐渐过渡到下一种颜色。
    最简单的是，它是在两种颜色之间过渡的填充； 或者更一般地说，它可以是任意数量的颜色的过渡。

    所需的过渡颜色和位置在渐变停止列表 (gsLst) 子元素中定义。

    另一个子元素定义渐变填充的属性（有两种样式 - 线性阴影样式以及路径阴影样式）
    """

    @property
    def gradit_stop_lst(self) -> Optional[CT_GradientStopList]:
        """渐变停止点列表 <a:gsLst>"""

        return getattr(self, qn('a:gsLst'), None)

    @property
    def shade(
        self,
    ) -> Optional[CT_LinearShadeProperties | CT_PathShadeProperties]:
        """图形属性"""

        return self.choice_one_child(*self.shade_tags)  # type: ignore

    @property
    def tile_rect(self) -> Optional[CT_RelativeRect]:
        """平铺图形"""

        return getattr(self, qn('a:tileRect'), None)

    @property
    def tile_flip(self) -> ST_TileFlipMode:
        """平铺翻转

        Tile Flip

        指定平铺时翻转渐变的方向。

        通常，渐变填充包含包含填充的形状的整个边界框。
        然而，使用tileRect元素，可以定义一个小于边界框的“平铺”矩形。
        在这种情况下，渐变填充包含在平铺矩形内，并且平铺矩形跨边界框平铺以填充整个区域。
        """

        val = self.attrib.get('flip', 'none')

        return ST_TileFlipMode(val)

    @property
    def rotate_with_shape(self) -> XSD_Boolean:
        """是否随形状旋转 rotWithShape

        Rotate With Shape

        指定如果形状旋转，阴影是否随形状旋转。
        """

        val = self.attrib.get('rotWithShape')

        return to_xsd_bool(val, none=True)


class CT_TileInfoProperties(OxmlBaseElement):
    """平铺信息属性

    20.1.8.58 tile (Tile)

    该元素指定 BLIP 应平铺以填充可用空间。
    该元素在边界框中定义了一个“平铺”矩形。
    图像包含在平铺矩形内，并且平铺矩形跨边界框平铺以填充整个区域。
    """

    @property
    def offset_x(self) -> Optional[ST_Percentage]:
        """X轴偏移 tx

        Offset X

        指定 X 偏移。
        """

        val = self.attrib.get('tx')

        if val is None:
            return None

        return to_ST_Percentage(str(val))

    @property
    def offset_y(self) -> Optional[ST_Percentage]:
        """Y轴偏移 ty

        Offset Y

        指定垂直缩放因子； 负缩放会导致翻转。
        """

        val = self.attrib.get('ty')

        if val is None:
            return None

        return to_ST_Percentage(str(val))

    @property
    def horizontal_scale(self) -> Optional[ST_Percentage]:
        """水平缩放因子 sx

        Horizontal Scaling Factor

        指定水平缩放因子； 负缩放会导致翻转。
        """

        val = self.attrib.get('sx')

        if val is None:
            return None

        return to_ST_Percentage(str(val))

    @property
    def vertical_scale(self) -> Optional[ST_Percentage]:
        """垂直缩放因子 sy

        Vertical Scaling Factor

        指定垂直缩放因子； 负缩放会导致翻转。
        """

        val = self.attrib.get('sy')

        if val is None:
            return None

        return to_ST_Percentage(str(val))

    @property
    def tile_flip(self) -> ST_TileFlipMode:
        """平铺翻转

        Tile Flip

        指定平铺时翻转渐变的方向。

        通常，渐变填充包含包含填充的形状的整个边界框。
        然而，使用tileRect元素，可以定义一个小于边界框的“平铺”矩形。
        在这种情况下，渐变填充包含在平铺矩形内，并且平铺矩形跨边界框平铺以填充整个区域。
        """

        val = self.attrib.get('flip', 'none')

        return ST_TileFlipMode(val)

    @property
    def alignment(self) -> Optional[ST_RectAlignment]:
        """对齐位置 algn

        Alignment

        指定第一个图块相对于形状的对齐位置。 对齐发生在缩放之后、附加偏移之前。
        """

        val = self.attrib.get('algn')

        if val is not None:
            return ST_RectAlignment(val)

        return None


class CT_StretchInfoProperties(OxmlBaseElement):
    """拉伸

    20.1.8.56 stretch (Stretch)

    此元素指定应拉伸 BLIP 以填充目标矩形。 另一个选项是平铺 BLIP，其中平铺 BLIP 来填充可用区域。
    """

    @property
    def fill_rect(self) -> Optional[CT_RelativeRect]:
        """填充矩形"""

        return getattr(self, qn('a:fillRect'), None)


class EG_FillModeProperties(OxmlBaseElement):
    """
    <xsd:group name="EG_FillModeProperties">
        <xsd:choice>
            <xsd:element name="tile" type="CT_TileInfoProperties" minOccurs="1" maxOccurs="1"/>
            <xsd:element name="stretch" type="CT_StretchInfoProperties" minOccurs="1" maxOccurs="1"/>
        </xsd:choice>
    </xsd:group>
    """

    fill_mode_tags = (
        # 平铺信息属性
        qn('a:tile'),  # CT_TileInfoProperties
        # 拉伸信息
        qn('a:stretch'),  # CT_StretchInfoProperties
    )

    @property
    def fill_mode_properties(
        self,
    ) -> Optional[CT_TileInfoProperties | CT_StretchInfoProperties]:
        """
        填充模型属性
        """

        return self.choice_one_child(*self.fill_mode_tags)  # type: ignore


class ST_BlipCompression(ST_BaseEnumType):
    """Blip 压缩类型

    20.1.10.12 ST_BlipCompression (Blip Compression Type)

    此类型指定用于特定二进制大图像或图片 (blip) 的压缩量。
    """

    Email = 'email'
    """电子邮件压缩 适合包含在电子邮件中的压缩尺寸"""

    Screen = 'screen'
    """屏幕观看压缩 适合在屏幕上查看的压缩尺寸 """

    Print = 'print'
    """打印压缩 适合打印的压缩尺寸"""

    HqPrint = 'hqprint'
    """High Quality Printing Compression 高品质打印压缩 适合高质量打印的压缩尺寸"""

    Null = 'none'
    """无压缩 未使用任何压缩"""


class CT_Blip(AG_Blob):
    """光点 / 图片填充

    20.1.8.13 blip (Blip)

    该元素指定图像（二进制大图像或图片）的存在并包含对图像数据的引用。
    """

    @property
    def alphaBiLevel_effect(self) -> Optional[CT_AlphaBiLevelEffect]:
        """阿尔法双水平效果

        20.1.8.1 alphaBiLevel

        """

        return getattr(self, qn('a:alphaBiLevel'), None)

    @property
    def alphaCeiling_effect(self) -> Optional[CT_AlphaCeilingEffect]:
        """阿尔法双水平效果

        20.1.8.2 alphaCeiling

        """

        return getattr(self, qn('a:alphaCeiling'), None)

    @property
    def alphaFloor_effect(self) -> Optional[CT_AlphaFloorEffect]:
        """阿尔法双水平效果

        20.1.8.3 alphaFloor

        """

        return getattr(self, qn('a:alphaFloor'), None)

    @property
    def alphaInv_effect(self) -> Optional[CT_AlphaInverseEffect]:
        """阿尔法双水平效果

        20.1.8.4 alphaInv

        """

        return getattr(self, qn('a:alphaInv'), None)

    @property
    def alphaMod_effect(self) -> Optional[CT_AlphaModulateEffect]:
        """阿尔法双水平效果

        20.1.8.5 alphaMod

        """

        return getattr(self, qn('a:alphaMod'), None)

    @property
    def alphaModFix_effect(self) -> Optional[CT_AlphaModulateFixedEffect]:
        """Alpha 调制固定效果

        - 20.1.8.6 alphaModFix
        """

        return getattr(self, qn('a:alphaModFix'), None)

    @property
    def alphaRepl_effect(self) -> Optional[CT_AlphaReplaceEffect]:
        """Alpha 替换效果

        - 20.1.8.8 alphaRepl

        """

        return getattr(self, qn('a:alphaRepl'), None)

    @property
    def biLevel_effect(self) -> Optional[CT_BiLevelEffect]:
        """双层（黑/白）效果

        - 20.1.8.11 biLevel

        """

        return getattr(self, qn('a:biLevel'), None)

    @property
    def blur_effect(self) -> Optional[CT_BlurEffect]:
        """模糊效果

        - 20.1.8.15 blur

        """

        return getattr(self, qn('a:blur'), None)

    @property
    def clrChange_effect(self) -> Optional[CT_ColorChangeEffect]:
        """变色效果

        - 20.1.8.16 clrChange

        """

        return getattr(self, qn('a:clrChange'), None)

    @property
    def clrRepl_effect(self) -> Optional[CT_ColorReplaceEffect]:
        """纯色更换

        - 20.1.8.18 clrRepl

        """

        return getattr(self, qn('a:clrRepl'), None)

    @property
    def duotone_effect(self) -> Optional[CT_DuotoneEffect]:
        """双色调效果

        - 20.1.8.23 duotone

        """

        return getattr(self, qn('a:duotone'), None)

    @property
    def fillOverlay_effect(self) -> Optional[CT_FillOverlayEffect]:
        """填充叠加效果

        - 20.1.8.29 fillOverlay

        """

        return getattr(self, qn('a:fillOverlay'), None)

    @property
    def grayscl_effect(self) -> Optional[CT_GrayscaleEffect]:
        """灰度效果

        - 20.1.8.34 grayscl

        """

        return getattr(self, qn('a:grayscl'), None)

    @property
    def hsl_effect(self) -> Optional[CT_HSLEffect]:
        """色相饱和度亮度效果

        - 20.1.8.39 hsl

        """

        return getattr(self, qn('a:hsl'), None)

    @property
    def lum_effect(self) -> Optional[CT_LuminanceEffect]:
        """亮度效果

        - 20.1.8.42 lum

        """

        return getattr(self, qn('a:lum'), None)

    @property
    def tint_effect(self) -> Optional[CT_TintEffect]:
        """色调效果

        - 20.1.8.60 tint (色调效果)

        """

        return getattr(self, qn('a:tint'), None)

    @property
    def effects(
        self,
    ) -> list[
        CT_AlphaBiLevelEffect | CT_AlphaCeilingEffect | CT_AlphaFloorEffect | CT_AlphaInverseEffect | CT_AlphaModulateEffect | CT_AlphaModulateFixedEffect | CT_AlphaReplaceEffect | CT_BiLevelEffect | CT_BlurEffect | CT_ColorChangeEffect | CT_ColorReplaceEffect | CT_DuotoneEffect | CT_FillOverlayEffect | CT_GrayscaleEffect | CT_HSLEffect | CT_LuminanceEffect | CT_TintEffect
    ]:
        """嵌入文件展示的效果

        主要有:

        - 20.1.8.1 alphaBiLevel (阿尔法双水平效应) -> CT_AlphaBiLevelEffect
        - 20.1.8.2 alphaCeiling (阿尔法天花板效应) -> CT_AlphaCeilingEffect
        - 20.1.8.3 alphaFloor (阿尔法地板效应) -> CT_AlphaFloorEffect
        - 20.1.8.4 alphaInv (阿尔法逆效应) -> CT_AlphaInverseEffect
        - 20.1.8.5 alphaMod (阿尔法调制效果) -> CT_AlphaModulateEffect
        - 20.1.8.6 alphaModFix (Alpha 调制固定效果) -> CT_AlphaModulateFixedEffect
        - 20.1.8.8 alphaRepl (Alpha 替换效果) -> CT_AlphaReplaceEffect
        - 20.1.8.11 biLevel (双层（黑/白）效果) -> CT_BiLevelEffect
        - 20.1.8.15 blur (模糊效果) -> CT_BlurEffect
        - 20.1.8.16 clrChange (变色效果) -> CT_ColorChangeEffect
        - 20.1.8.18 clrRepl (纯色更换) -> CT_ColorReplaceEffect
        - 20.1.8.23 duotone (双色调效果) -> CT_DuotoneEffect
        - 20.1.8.29 fillOverlay (填充叠加效果) -> CT_FillOverlayEffect
        - 20.1.8.34 grayscl (灰度效果) -> CT_GrayscaleEffect
        - 20.1.8.39 hsl (色相饱和度亮度效果) -> CT_HSLEffect
        - 20.1.8.42 lum (亮度效果) -> CT_LuminanceEffect
        - 20.1.8.60 tint (色调效果) -> CT_TintEffect
        """

        tags = (
            qn('a:alphaBiLevel'),  # CT_AlphaBiLevelEffect
            qn('a:alphaCeiling'),  # CT_AlphaCeilingEffect
            qn('a:alphaFloor'),  # CT_AlphaFloorEffect
            qn('a:alphaInv'),  # CT_AlphaInverseEffect
            qn('a:alphaMod'),  # CT_AlphaModulateEffect
            qn('a:alphaModFix'),  # CT_AlphaModulateFixedEffect
            qn('a:alphaRepl'),  # CT_AlphaReplaceEffect
            qn('a:biLevel'),  # CT_BiLevelEffect
            qn('a:blur'),  # CT_BlurEffect
            qn('a:clrChange'),  # CT_ColorChangeEffect
            qn('a:clrRepl'),  # CT_ColorReplaceEffect
            qn('a:duotone'),  # CT_DuotoneEffect
            qn('a:fillOverlay'),  # CT_FillOverlayEffect
            qn('a:grayscl'),  # CT_GrayscaleEffect
            qn('a:hsl'),  # CT_HSLEffect
            qn('a:lum'),  # CT_LuminanceEffect
            qn('a:tint'),  # CT_TintEffect
        )

        return list(self.iterchildren(*tags, reversed=False))  # type: ignore

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展元素合集"""

        return getattr(self, qn('a:extLst'), None)

    @property
    def compression_state(self) -> ST_BlipCompression:
        """压缩状态 cstate

        Compression State

        指定存储图片的压缩状态。 这允许应用程序指定已应用于图片的压缩量。
        """

        val = self.attrib.get('cstate')

        if val is None:
            return ST_BlipCompression.Null

        return ST_BlipCompression(val)


class CT_BlipFillProperties(EG_FillModeProperties):
    """图片填充属性

    19.3.1.4 blipFill (Picture Fill)

    20.1.8.14 blipFill (Picture Fill)

    该元素指定图片对象具有的图片填充类型。 由于默认情况下图片已具有图片填充，因此可以为图片对象指定两种填充。
    """

    @property
    def blip(self) -> Optional[CT_Blip]:
        """填充的图片"""

        return getattr(self, qn('a:blip'), None)

    @property
    def src_rect(self) -> Optional[CT_RelativeRect]:
        """源矩形

        20.1.8.55 srcRect (Source Rectangle)

        该元素指定用于填充的 blip 部分。

        源矩形的每条边均由距边界框相应边的偏移百分比定义。 正百分比指定插入，负百分比指定开始. [Note: 例如，左偏移 25% 指定源矩形的左边缘位于边界框左边缘的右侧，偏移量等于边界框宽度的 25%. end note]
        """

        return getattr(self, qn('a:srcRect'), None)

    @property
    def fill_mode(
        self,
    ) -> Optional[CT_TileInfoProperties | CT_StretchInfoProperties]:
        """
        填充模型属性
        """

        return self.choice_one_child(*self.fill_mode_tags)  # type: ignore

    @property
    def dpi(self) -> Optional[XSD_UnsignedInt]:
        """每英寸点数设置 dpi

        DPI Setting

        指定用于计算光点大小的 DPI（每英寸点数）。 如果不存在或为零，则使用 blip 中的 DPI。
        """

        val = self.attrib.get('dpi')

        if val is not None:
            to_xsd_unsigned_int(val)  # type: ignore

        return None

    @property
    def ratate_with_shape(self) -> Optional[XSD_Boolean]:
        """随形状旋转 rotWithShape

        Rotate With Shape

        指定填充应随形状旋转。 也就是说，当用图片填充的形状和包含的形状（例如矩形）通过旋转进行变换时，
        填充也会通过相同的旋转进行变换。
        """

        val = self.attrib.get('rotWithShape')

        if val is None:
            return None

        return to_xsd_bool(val)


class ST_PresetPatternVal(ST_BaseEnumType):
    """预设图案值 Preset Pattern Value

    20.1.10.51 ST_PresetPatternVal (Preset Pattern Value)

    该简单类型表示图案填充的预设类型。 每个值的描述包含填充类型的说明。

    [注意: 这些预设对应于 Microsoft .NET Framework 中 HatchStyle 枚举的成员。
    此类型的参考可以在 http://msdn2.microsoft.com/enus/library/system.drawing.drawing2d.hatchstyle.aspx 中找到。 ]

    """

    Pct5 = 'pct5'
    Pct10 = 'pct10'
    Pct20 = 'pct20'
    Pct25 = 'pct25'
    Pct30 = 'pct30'
    Pct40 = 'pct40'
    Pct50 = 'pct50'
    Pct60 = 'pct60'
    Pct70 = 'pct70'
    Pct75 = 'pct75'
    Pct80 = 'pct80'
    Pct90 = 'pct90'
    Horz = 'horz'
    Vert = 'vert'
    LtHorz = 'ltHorz'
    LtVert = 'ltVert'
    DkHorz = 'dkHorz'
    DkVert = 'dkVert'
    NarHorz = 'narHorz'
    NarVert = 'narVert'
    DashHorz = 'dashHorz'
    DashVert = 'dashVert'
    Cross = 'cross'
    DnDiag = 'dnDiag'
    UpDiag = 'upDiag'
    LtDnDiag = 'ltDnDiag'
    LtUpDiag = 'ltUpDiag'
    DkDnDiag = 'dkDnDiag'
    DkUpDiag = 'dkUpDiag'
    WdDnDiag = 'wdDnDiag'
    WdUpDiag = 'wdUpDiag'
    DashDnDiag = 'dashDnDiag'
    DashUpDiag = 'dashUpDiag'
    DiagCross = 'diagCross'
    SmCheck = 'smCheck'
    LgCheck = 'lgCheck'
    SmGrid = 'smGrid'
    LgGrid = 'lgGrid'
    DotGrid = 'dotGrid'
    SmConfetti = 'smConfetti'
    LgConfetti = 'lgConfetti'
    HorzBrick = 'horzBrick'
    DiagBrick = 'diagBrick'
    SolidDmnd = 'solidDmnd'
    OpenDmnd = 'openDmnd'
    DotDmnd = 'dotDmnd'
    Plaid = 'plaid'
    Sphere = 'sphere'
    Weave = 'weave'
    Divot = 'divot'
    Shingle = 'shingle'
    Wave = 'wave'
    Trellis = 'trellis'
    ZigZag = 'zigZag'


class CT_PatternFillProperties(OxmlBaseElement):
    """图案填充 属性

    20.1.8.47 pattFill (Pattern Fill)

    该元素指定图案填充。 使用重复图案来填充对象。
    """

    @property
    def forege_color(self) -> Optional[CT_Color]:
        """前置颜色

        aaa
        """

        return getattr(self, qn('a:fgClr'), None)

    @property
    def background_color(self) -> Optional[CT_Color]:
        """后置颜色

        aaa
        """

        return getattr(self, qn('a:bgClr'), None)

    @property
    def preset(self) -> Optional[ST_PresetPatternVal]:
        """预设模式

        Preset Pattern

        指定一组预设图案中的一个来填充对象。
        """

        val = self.attrib.get('prst')

        if val is None:
            return None

        return ST_PresetPatternVal(val)


class CT_GroupFillProperties(OxmlBaseElement):
    """组合填充属性

    20.1.8.35 grpFill (Group Fill)

    该元素指定组填充。 指定后，此设置指示父元素是组的一部分，并且应继承该组的填充属性。
    """



class CT_FillProperties(EG_FillProperties):
    """填充属性 Fill Properties

    20.1.4.2.9 fill (Fill)

    该元素定义应用于整个表格的填充。 表格的背景可以包含整个表格大小的单个填充。 这可以允许跨越整个表格大小的渐变填充或图像填充。
    """

    @property
    def fill(
        self,
    ) -> Optional[
        CT_NoFillProperties | CT_SolidColorFillProperties | CT_GradientFillProperties | CT_BlipFillProperties | CT_PatternFillProperties | CT_GroupFillProperties
    ]:
        """填充属性

        <xsd:complexType name="CT_FillProperties">
            <xsd:sequence>
                <xsd:group ref="EG_FillProperties" minOccurs="1" maxOccurs="1"/>
            </xsd:sequence>
        </xsd:complexType>

        """

        return self.choice_require_one_child(*self.fill_pr_tags)  # type: ignore


class CT_FillEffect(EG_FillProperties):
    """填充效果 Fill Effect

    该元素指定填充效果，该填充是 blipFill、gradFill、grpFill、noFill、pattFill 或 solidFill 之一。
    """

    @property
    def fill(
        self,
    ) -> Optional[
        CT_NoFillProperties | CT_SolidColorFillProperties | CT_GradientFillProperties | CT_BlipFillProperties | CT_PatternFillProperties | CT_GroupFillProperties
    ]:
        """填充属性

        <xsd:complexType name="CT_FillProperties">
            <xsd:sequence>
                <xsd:group ref="EG_FillProperties" minOccurs="1" maxOccurs="1"/>
            </xsd:sequence>
        </xsd:complexType>

        """

        return self.choice_require_one_child(*self.fill_pr_tags)  # type: ignore


class ST_BlendMode(ST_BaseEnumType):
    """混合模式

    20.1.10.11 ST_BlendMode (Blend Mode)

    这种简单的类型描述了如何在另一个之上渲染效果。
    """

    Over = 'over'
    Mult = 'mult'
    Screen = 'screen'
    Darken = 'darken'
    Lighten = 'lighten'


class CT_FillOverlayEffect(EG_FillProperties):
    """填充叠加效果 Fill Overlay Effect

    20.1.8.29 fillOverlay (Fill Overlay Effect)

    该元素指定填充叠加效果。 填充叠加可用于为对象指定附加填充并将两个填充混合在一起。
    """

    @property
    def fill(
        self,
    ) -> Optional[
        CT_NoFillProperties | CT_SolidColorFillProperties | CT_GradientFillProperties | CT_BlipFillProperties | CT_PatternFillProperties | CT_GroupFillProperties
    ]:
        """填充属性

        <xsd:complexType name="CT_FillProperties">
            <xsd:sequence>
                <xsd:group ref="EG_FillProperties" minOccurs="1" maxOccurs="1"/>
            </xsd:sequence>
        </xsd:complexType>

        """

        return self.choice_require_one_child(*self.fill_pr_tags)  # type: ignore

    @property
    def blend_mode(self) -> ST_BlendMode:
        """
        混合模式
        """

        _val = self.attrib['blend']

        return ST_BlendMode(_val)


class CT_EffectReference(OxmlBaseElement):
    """效果 引用

    20.1.8.24 effect (Effect)

    该元素指定对现有效果容器的引用。
    """

    @property
    def ref(self) -> XSD_Token:
        """引用

        Reference

        指定引用。 它的值可以是效果容器的名称，或者四个之一

        特别参考:

        fill - 指填充效果

        line - 指线条效果

        fillLine - 指组合的填充和线条效果

        children - 指逻辑子形状或文本的综合效果
        """
        val = self.attrib['ref']

        return XSD_Token(utils.AnyStrToStr(val))  # type: ignore


class EG_Effect(OxmlBaseElement):
    """
    <xsd:group name="EG_Effect">
        <xsd:choice>
            <xsd:element name="cont" type="CT_EffectContainer" minOccurs="1" maxOccurs="1"/>
            ....
        </xsd:choice>
    </xsd:group>
    """

    effect_tags = (
        qn('a:cont'),  # CT_EffectContainer"
        qn('a:effect'),  # CT_EffectReference"
        qn('a:alphaBiLevel'),  # CT_AlphaBiLevelEffect"
        qn('a:alphaCeiling'),  # CT_AlphaCeilingEffect"
        qn('a:alphaFloor'),  # CT_AlphaFloorEffect"
        qn('a:alphaInv'),  # CT_AlphaInverseEffect"
        qn('a:alphaMod'),  # CT_AlphaModulateEffect"
        qn('a:alphaModFix'),  # CT_AlphaModulateFixedEffect"
        qn('a:alphaOutset'),  # CT_AlphaOutsetEffect"
        qn('a:alphaRepl'),  # CT_AlphaReplaceEffect"
        qn('a:biLevel'),  # CT_BiLevelEffect"
        qn('a:blend'),  # CT_BlendEffect"
        qn('a:blur'),  # CT_BlurEffect"
        qn('a:clrChange'),  # CT_ColorChangeEffect"
        qn('a:clrRepl'),  # CT_ColorReplaceEffect"
        qn('a:duotone'),  # CT_DuotoneEffect"
        qn('a:fill'),  # CT_FillEffect"
        qn('a:fillOverlay'),  # CT_FillOverlayEffect"
        qn('a:glow'),  # CT_GlowEffect"
        qn('a:grayscl'),  # CT_GrayscaleEffect"
        qn('a:hsl'),  # CT_HSLEffect"
        qn('a:innerShdw'),  # CT_InnerShadowEffect"
        qn('a:lum'),  # CT_LuminanceEffect"
        qn('a:outerShdw'),  # CT_OuterShadowEffect"
        qn('a:prstShdw'),  # CT_PresetShadowEffect"
        qn('a:reflection'),  # CT_ReflectionEffect"
        qn('a:relOff'),  # CT_RelativeOffsetEffect"
        qn('a:softEdge'),  # CT_SoftEdgesEffect"
        qn('a:tint'),  # CT_TintEffect"
        qn('a:xfrm'),  # CT_TransformEffect"
    )


class ST_EffectContainerType(ST_BaseEnumType):
    """效果容器类型

    20.1.10.22 ST_EffectContainerType (Effect Container Type)

    这个简单的类型决定了容器（同级容器或树）中效果之间的关系。
    """

    Sibling = 'sib'
    """每个效果都单独应用于父对象。

    [示例: 如果父元素包含外部阴影和反射，则产生的效果是父对象周围的阴影和该对象的反射。 反射没有阴影。]
    """

    Tree = 'tree'
    """每个效果都会应用于前一个效果的结果。

    [示例: 如果父元素包含一个外部阴影，后跟一个辉光，则该阴影首先应用于父对象。 然后，将发光应用于阴影（而不是原始对象）。 由此产生的效果将是发光的阴影。 ]
    """


class CT_EffectContainer(EG_Effect):
    """效果容器 Effect Container

    该元素指定一个效果容器。 这是一个效果列表。

    20.1.8.20 cont (Effect Container)
    """

    @property
    def effect_list(
        self,
    ) -> list[
        CT_EffectContainer | CT_EffectReference | CT_AlphaBiLevelEffect | CT_AlphaCeilingEffect | CT_AlphaFloorEffect | CT_AlphaInverseEffect | CT_AlphaModulateEffect | CT_AlphaModulateFixedEffect | CT_AlphaOutsetEffect | CT_AlphaReplaceEffect | CT_BiLevelEffect | CT_BlendEffect | CT_BlurEffect | CT_ColorChangeEffect | CT_ColorReplaceEffect | CT_DuotoneEffect | CT_FillEffect | CT_FillOverlayEffect | CT_GlowEffect | CT_GrayscaleEffect | CT_HSLEffect | CT_InnerShadowEffect | CT_LuminanceEffect | CT_OuterShadowEffect | CT_PresetShadowEffect | CT_ReflectionEffect | CT_RelativeOffsetEffect | CT_SoftEdgesEffect | CT_TintEffect | CT_TransformEffect
    ]:
        """
        效果元素

        可能是列表

        <xsd:group ref="EG_Effect" minOccurs="0" maxOccurs="unbounded"/>
        """

        return self.choice_and_more(*self.effect_tags)  # type: ignore

    @property
    def type(self) -> ST_EffectContainerType:
        """效果容器类型

        Effect Container Type

        指定容器的类型，可以是兄弟容器，也可以是树容器。
        """

        val = self.attrib.get('type')

        if val is None:
            return ST_EffectContainerType.Sibling

        return ST_EffectContainerType(val)

    @property
    def name(self) -> Optional[str]:
        """名称

        Name

        为此效果列表指定一个可选名称，以便稍后引用。 在所有效果树和效果容器中应是唯一的。
        """

        val = self.attrib.get('name')

        if val is not None:
            return str(val)

        return None


class CT_AlphaModulateEffect(OxmlBaseElement):
    """Alpha 调制效果

    20.1.8.5 alphaMod (Alpha Modulate Effect)

    该元素代表阿尔法调制效果。

    效果 alpha（不透明度）值乘以固定百分比。 效果容器指定包含要调制的 alpha 值的效果。
    """

    @property
    def container(self) -> CT_EffectContainer:
        """容器

        <xsd:sequence>
            <xsd:element name="cont" type="CT_EffectContainer" minOccurs="1" maxOccurs="1"/>
        </xsd:sequence>
        """

        return getattr(self, qn('a:cont'))


class CT_BlendEffect(OxmlBaseElement):
    """混合效果

    20.1.8.12 blend (Blend Effect)

    该元素指定了多种效果的混合。 容器指定要混合的原始效果，而混合模式则指定如何混合效果。
    """

    @property
    def container(self) -> CT_EffectContainer:
        """容器

        <xsd:sequence>
            <xsd:element name="cont" type="CT_EffectContainer" minOccurs="1" maxOccurs="1"/>
        </xsd:sequence>
        """

        return getattr(self, qn('a:cont'))

    @property
    def blend_mode(self) -> ST_BlendMode:
        """混合模式

        Blend Mode

        指定如何混合两种效果。
        """

        val = self.attrib['blend']

        return ST_BlendMode(val)


class CT_EffectList(OxmlBaseElement):
    """效果列表(容器)

    20.1.8.26 effectLst (Effect Container)
    """

    @property
    def blur(self) -> Optional[CT_BlurEffect]:
        """
        模糊效果
        """

        return getattr(self, qn('a:blur'), None)

    @property
    def fill_overlay(self) -> Optional[CT_FillOverlayEffect]:
        """
        填充叠加效果
        """

        return getattr(self, qn('a:fillOverlay'), None)

    @property
    def glow(self) -> Optional[CT_GlowEffect]:
        """
        发光效果
        """

        return getattr(self, qn('a:glow'), None)

    @property
    def inner_shdw(self) -> Optional[CT_InnerShadowEffect]:
        """
        内阴影效果
        """

        return getattr(self, qn('a:innerShdw'), None)

    @property
    def outer_shdw(self) -> Optional[CT_OuterShadowEffect]:
        """
        外阴影效果
        """

        return getattr(self, qn('a:outerShdw'), None)

    @property
    def prst_shdw(self) -> Optional[CT_PresetShadowEffect]:
        """
        预置效果
        """

        return getattr(self, qn('a:prstShdw'), None)

    @property
    def reflection(self) -> Optional[CT_ReflectionEffect]:
        """
        反射效果
        """

        return getattr(self, qn('a:reflection'), None)

    @property
    def soft_edge(self) -> Optional[CT_SoftEdgesEffect]:
        """
        软边缘效果
        """

        return getattr(self, qn('a:softEdge'), None)


class CT_EffectProperties(EG_EffectProperties):
    """效果属性

    20.1.4.2.7 effect (Effect)

    该元素定义了可以通过表格样式应用于整个表格的效果
    """

    @property
    def effect(self) -> Optional[CT_EffectList | CT_EffectContainer]:
        """
        效果属性

        <xsd:sequence>
            <xsd:group ref="EG_EffectProperties" minOccurs="1" maxOccurs="1"/>
        </xsd:sequence>
        """

        return self.choice_require_one_child(*self.effect_pr_tags)  # type: ignore


class ST_ShapeType(ST_BaseEnumType):
    """预设形状类型

    20.1.10.56 ST_ShapeType (Preset Shape Types)

    此简单类型指定要用于形状的预设形状几何形状。
    使用这种简单类型的枚举，以便不必指定自定义几何图形，而是可以由生成应用程序自动构造。
    对于列出的每个枚举，还有相应的 DrawingML 代码，如果它是自定义几何图形，则将使用该代码来构造此形状。
    在每个预设形状的构造规范中，都有预定义的指南，生成应用程序应始终维护这些指南以用于计算目的。
    必要的指南应具有以下值。

    公式语法组件在 gd 元素的 fmla 属性中定义（第 20.1.9.11 节）。
    """

    Line = 'line'
    LineInv = 'lineInv'
    Triangle = 'triangle'
    RtTriangle = 'rtTriangle'
    Rect = 'rect'
    Diamond = 'diamond'
    Parallelogram = 'parallelogram'
    Trapezoid = 'trapezoid'
    NonIsoscelesTrapezoid = 'nonIsoscelesTrapezoid'
    Pentagon = 'pentagon'
    Hexagon = 'hexagon'
    Heptagon = 'heptagon'
    Octagon = 'octagon'
    Decagon = 'decagon'
    Dodecagon = 'dodecagon'
    Star4 = 'star4'
    Star5 = 'star5'
    Star6 = 'star6'
    Star7 = 'star7'
    Star8 = 'star8'
    Star10 = 'star10'
    Star12 = 'star12'
    Star16 = 'star16'
    Star24 = 'star24'
    Star32 = 'star32'
    RoundRect = 'roundRect'
    Round1Rect = 'round1Rect'
    Round2SameRect = 'round2SameRect'
    Round2DiagRect = 'round2DiagRect'
    SnipRoundRect = 'snipRoundRect'
    Snip1Rect = 'snip1Rect'
    Snip2SameRect = 'snip2SameRect'
    Snip2DiagRect = 'snip2DiagRect'
    Plaque = 'plaque'
    Ellipse = 'ellipse'
    Teardrop = 'teardrop'
    HomePlate = 'homePlate'
    Chevron = 'chevron'
    PieWedge = 'pieWedge'
    Pie = 'pie'
    BlockArc = 'blockArc'
    Donut = 'donut'
    NoSmoking = 'noSmoking'
    RightArrow = 'rightArrow'
    LeftArrow = 'leftArrow'
    UpArrow = 'upArrow'
    DownArrow = 'downArrow'
    StripedRightArrow = 'stripedRightArrow'
    NotchedRightArrow = 'notchedRightArrow'
    BentUpArrow = 'bentUpArrow'
    LeftRightArrow = 'leftRightArrow'
    UpDownArrow = 'upDownArrow'
    LeftUpArrow = 'leftUpArrow'
    LeftRightUpArrow = 'leftRightUpArrow'
    QuadArrow = 'quadArrow'
    LeftArrowCallout = 'leftArrowCallout'
    RightArrowCallout = 'rightArrowCallout'
    UpArrowCallout = 'upArrowCallout'
    DownArrowCallout = 'downArrowCallout'
    LeftRightArrowCallout = 'leftRightArrowCallout'
    UpDownArrowCallout = 'upDownArrowCallout'
    QuadArrowCallout = 'quadArrowCallout'
    BentArrow = 'bentArrow'
    UturnArrow = 'uturnArrow'
    CircularArrow = 'circularArrow'
    LeftCircularArrow = 'leftCircularArrow'
    LeftRightCircularArrow = 'leftRightCircularArrow'
    CurvedRightArrow = 'curvedRightArrow'
    CurvedLeftArrow = 'curvedLeftArrow'
    CurvedUpArrow = 'curvedUpArrow'
    CurvedDownArrow = 'curvedDownArrow'
    SwooshArrow = 'swooshArrow'
    Cube = 'cube'
    Can = 'can'
    LightningBolt = 'lightningBolt'
    Heart = 'heart'
    Sun = 'sun'
    Moon = 'moon'
    SmileyFace = 'smileyFace'
    IrregularSeal1 = 'irregularSeal1'
    IrregularSeal2 = 'irregularSeal2'
    FoldedCorner = 'foldedCorner'
    Bevel = 'bevel'
    Frame = 'frame'
    HalfFrame = 'halfFrame'
    Corner = 'corner'
    DiagStripe = 'diagStripe'
    Chord = 'chord'
    Arc = 'arc'
    LeftBracket = 'leftBracket'
    RightBracket = 'rightBracket'
    LeftBrace = 'leftBrace'
    RightBrace = 'rightBrace'
    BracketPair = 'bracketPair'
    BracePair = 'bracePair'
    StraightConnector1 = 'straightConnector1'
    BentConnector2 = 'bentConnector2'
    BentConnector3 = 'bentConnector3'
    BentConnector4 = 'bentConnector4'
    BentConnector5 = 'bentConnector5'
    CurvedConnector2 = 'curvedConnector2'
    CurvedConnector3 = 'curvedConnector3'
    CurvedConnector4 = 'curvedConnector4'
    CurvedConnector5 = 'curvedConnector5'
    Callout1 = 'callout1'
    Callout2 = 'callout2'
    Callout3 = 'callout3'
    AccentCallout1 = 'accentCallout1'
    AccentCallout2 = 'accentCallout2'
    AccentCallout3 = 'accentCallout3'
    BorderCallout1 = 'borderCallout1'
    BorderCallout2 = 'borderCallout2'
    BorderCallout3 = 'borderCallout3'
    AccentBorderCallout1 = 'accentBorderCallout1'
    AccentBorderCallout2 = 'accentBorderCallout2'
    AccentBorderCallout3 = 'accentBorderCallout3'
    WedgeRectCallout = 'wedgeRectCallout'
    WedgeRoundRectCallout = 'wedgeRoundRectCallout'
    WedgeEllipseCallout = 'wedgeEllipseCallout'
    CloudCallout = 'cloudCallout'
    Cloud = 'cloud'
    Ribbon = 'ribbon'
    Ribbon2 = 'ribbon2'
    EllipseRibbon = 'ellipseRibbon'
    EllipseRibbon2 = 'ellipseRibbon2'
    LeftRightRibbon = 'leftRightRibbon'
    VerticalScroll = 'verticalScroll'
    HorizontalScroll = 'horizontalScroll'
    Wave = 'wave'
    DoubleWave = 'doubleWave'
    Plus = 'plus'
    FlowChartProcess = 'flowChartProcess'
    FlowChartDecision = 'flowChartDecision'
    FlowChartInputOutput = 'flowChartInputOutput'
    FlowChartPredefinedProcess = 'flowChartPredefinedProcess'
    FlowChartInternalStorage = 'flowChartInternalStorage'
    FlowChartDocument = 'flowChartDocument'
    FlowChartMultidocument = 'flowChartMultidocument'
    FlowChartTerminator = 'flowChartTerminator'
    FlowChartPreparation = 'flowChartPreparation'
    FlowChartManualInput = 'flowChartManualInput'
    FlowChartManualOperation = 'flowChartManualOperation'
    FlowChartConnector = 'flowChartConnector'
    FlowChartPunchedCard = 'flowChartPunchedCard'
    FlowChartPunchedTape = 'flowChartPunchedTape'
    FlowChartSummingJunction = 'flowChartSummingJunction'
    FlowChartOr = 'flowChartOr'
    FlowChartCollate = 'flowChartCollate'
    FlowChartSort = 'flowChartSort'
    FlowChartExtract = 'flowChartExtract'
    FlowChartMerge = 'flowChartMerge'
    FlowChartOfflineStorage = 'flowChartOfflineStorage'
    FlowChartOnlineStorage = 'flowChartOnlineStorage'
    FlowChartMagneticTape = 'flowChartMagneticTape'
    FlowChartMagneticDisk = 'flowChartMagneticDisk'
    FlowChartMagneticDrum = 'flowChartMagneticDrum'
    FlowChartDisplay = 'flowChartDisplay'
    FlowChartDelay = 'flowChartDelay'
    FlowChartAlternateProcess = 'flowChartAlternateProcess'
    FlowChartOffpageConnector = 'flowChartOffpageConnector'
    ActionButtonBlank = 'actionButtonBlank'
    ActionButtonHome = 'actionButtonHome'
    ActionButtonHelp = 'actionButtonHelp'
    ActionButtonInformation = 'actionButtonInformation'
    ActionButtonForwardNext = 'actionButtonForwardNext'
    ActionButtonBackPrevious = 'actionButtonBackPrevious'
    ActionButtonEnd = 'actionButtonEnd'
    ActionButtonBeginning = 'actionButtonBeginning'
    ActionButtonReturn = 'actionButtonReturn'
    ActionButtonDocument = 'actionButtonDocument'
    ActionButtonSound = 'actionButtonSound'
    ActionButtonMovie = 'actionButtonMovie'
    Gear6 = 'gear6'
    Gear9 = 'gear9'
    Funnel = 'funnel'
    MathPlus = 'mathPlus'
    MathMinus = 'mathMinus'
    MathMultiply = 'mathMultiply'
    MathDivide = 'mathDivide'
    MathEqual = 'mathEqual'
    MathNotEqual = 'mathNotEqual'
    CornerTabs = 'cornerTabs'
    SquareTabs = 'squareTabs'
    PlaqueTabs = 'plaqueTabs'
    ChartX = 'chartX'
    ChartStar = 'chartStar'
    ChartPlus = 'chartPlus'


class ST_TextShapeType(ST_BaseEnumType):
    """预设文本形状类型

    20.1.10.76 ST_TextShapeType (Preset Text Shape Types)

    此简单类型指定要用于形状的预设文本形状几何形状。
    使用这种简单类型的枚举，以便不必指定自定义几何图形，而是可以由生成应用程序自动构造。
    对于列出的每个枚举，还有相应的 DrawingML 代码，如果它是自定义几何图形，则将使用该代码来构造此形状。
    在每个预设文本形状的构造代码中，都有预定义的指南，生成应用程序应始终维护这些指南以用于计算目的。
    必要的指南应具有以下值。 公式语法组件在 gd 元素的 fmla 属性中定义（第 20.1.9.11 节）。
    """

    TextNoShape = 'textNoShape'
    TextPlain = 'textPlain'
    TextStop = 'textStop'
    TextTriangle = 'textTriangle'
    TextTriangleInverted = 'textTriangleInverted'
    TextChevron = 'textChevron'
    TextChevronInverted = 'textChevronInverted'
    TextRingInside = 'textRingInside'
    TextRingOutside = 'textRingOutside'
    TextArchUp = 'textArchUp'
    TextArchDown = 'textArchDown'
    TextCircle = 'textCircle'
    TextButton = 'textButton'
    TextArchUpPour = 'textArchUpPour'
    TextArchDownPour = 'textArchDownPour'
    TextCirclePour = 'textCirclePour'
    TextButtonPour = 'textButtonPour'
    TextCurveUp = 'textCurveUp'
    TextCurveDown = 'textCurveDown'
    TextCanUp = 'textCanUp'
    TextCanDown = 'textCanDown'
    TextWave1 = 'textWave1'
    TextWave2 = 'textWave2'
    TextDoubleWave1 = 'textDoubleWave1'
    TextWave4 = 'textWave4'
    TextInflate = 'textInflate'
    TextDeflate = 'textDeflate'
    TextInflateBottom = 'textInflateBottom'
    TextDeflateBottom = 'textDeflateBottom'
    TextInflateTop = 'textInflateTop'
    TextDeflateTop = 'textDeflateTop'
    TextDeflateInflate = 'textDeflateInflate'
    TextDeflateInflateDeflate = 'textDeflateInflateDeflate'
    TextFadeRight = 'textFadeRight'
    TextFadeLeft = 'textFadeLeft'
    TextFadeUp = 'textFadeUp'
    TextFadeDown = 'textFadeDown'
    TextSlantUp = 'textSlantUp'
    TextSlantDown = 'textSlantDown'
    TextCascadeUp = 'textCascadeUp'
    TextCascadeDown = 'textCascadeDown'


# <xsd:restriction base="xsd:token"/>
ST_GeomGuideName = NewType('ST_GeomGuideName', str)
"""几何指南名称属性

20.1.10.28 ST_GeomGuideName (Geometry Guide Name Properties)

这个简单的类型指定了几何指南名称。
"""


ST_GeomGuideFormula = NewType('ST_GeomGuideFormula', str)
"""几何指南公式属性

20.1.10.27 ST_GeomGuideFormula (Geometry Guide Formula Properties)

这个简单的类型指定了几何指南公式。
"""


class CT_GeomGuide(OxmlBaseElement):
    """形状指南

    20.1.9.11 gd (Shape Guide)

    该元素指定用于控制指定形状的几何形状的形状引导的优先级。 形状指南由公式和公式结果所分配的名称组成。 已识别的公式与该元素的 fmla 属性文档一起列出。

    [注意: 指定参考线的顺序决定了计算其值的顺序。 例如，当尚未计算该指南时，不可能指定使用另一个指南结果的指南。]
    """

    @property
    def name(self) -> ST_GeomGuideName:
        """名称

        Shape Guide Name

        指定用于引用本指南的名称。 该名称可以像方程中的变量一样使用。
        也就是说，该名称可以替换其他指南或形状路径规范中的文字值。
        """

        val = self.attrib['name']

        return ST_GeomGuideName(utils.AnyStrToStr(val))  # type: ignore

    @property
    def formula(self) -> ST_GeomGuideFormula:
        """公式

        Shape Guide Formula

        指定用于计算指南值的公式。 每个公式都有一定数量的参数以及对这些参数执行的一组特定操作，以便生成指南的值。
        共有 17 种不同的公式可用。 下面显示了它们以及每个定义的用法。

        参考: 原文, 第2898页([2909])
        """

        val = self.attrib['fmla']

        return ST_GeomGuideFormula(utils.AnyStrToStr(val))  # type: ignore


class CT_GeomGuideList(OxmlBaseElement):
    """形状参考列表

    20.1.9.12 gdLst (List of Shape Guides)

    该元素指定用于该形状的所有参考线。 参考线由 gd 元素指定，并定义可用于构造相应形状的计算值。

    [注意: 具有通过上面的 fmla="val x" 指定的文字值公式的指南只能在 avLst 中用作形状的调整值。 然而，这并没有严格执行。]
    """

    @property
    def gd_lst(self) -> list[CT_GeomGuide]:
        """几何指南列表"""

        return self.findall(qn('a:gd'))  # type: ignore


# <xsd:simpleType name="ST_AdjCoordinate">
#     <xsd:union memberTypes="ST_Coordinate ST_GeomGuideName"/>
# </xsd:simpleType>
# ST_AdjCoordinate = Union[ST_Coordinate, ST_GeomGuideName]
ST_AdjCoordinate = Union[str, int]
"""可调整坐标

20.1.10.2 ST_AdjCoordinate (Adjustable Coordinate Methods)

这种简单类型是可调整的坐标，可以是绝对坐标位置，也可以是对几何参考线的引用。

这个简单类型是以下类型的联合:

ST_Coordinate 简单类型（§20.1.10.16）。

ST_GeomGuideName 简单类型 (§20.1.10.28)。
"""


def to_ST_AdjCoordinate(val: str) -> ST_AdjCoordinate:
    if not val:
        return 0

    val = utils.AnyStrToStr(val)
    suffix = val[-2:]

    # 针对 1234123
    if val.isdigit():
        pyval = int(val)

        if not (-27273042329600 <= pyval <= 27273042316900):
            msg = f'预期外的值: {pyval}'
            raise OxmlAttributeValidateError(msg)

        return pyval

    # 针对 1234cm 等等带单位的
    if suffix in {'mm', 'cm', 'in', 'pt', 'pc', 'pi'}:
        return to_ST_UniversalMeasure(val)

    return val


# <xsd:simpleType name="ST_AdjAngle">
#     <xsd:union memberTypes="ST_Angle ST_GeomGuideName"/>
# </xsd:simpleType>
# ST_AdjAngle = Union[ST_Angle, ST_GeomGuideName]
ST_AdjAngle = Union[str, float]
"""可调整角度

20.1.10.1 ST_AdjAngle (Adjustable Angle Methods)

这种简单的类型是可调节的角度，可以是绝对角度，也可以是几何参考线的参考。 可调节角度的单位是六万分之一度。

这个简单类型是以下类型的联合:

ST_Angle 简单类型（§20.1.10.3）

ST_GeomGuideName 简单类型 (§20.1.10.28)。
"""


def to_ST_AdjAngle(val: str) -> ST_AdjAngle:
    try:
        return float(val)
    except Exception:
        return val


class CT_AdjPoint2D(OxmlBaseElement):
    """2维点坐标

    20.1.9.17 pos (Shape Position Coordinate)  - 形状位置坐标

    指定形状边界框内的位置坐标。
    应该注意的是，该坐标使用变换坐标系放置在形状边界框内，变换坐标系也称为形状坐标系，因为它包含整个形状。
    该坐标系的宽度和高度在 ext 变换元素中指定。

    [注意: 在路径坐标空间中指定点坐标时，应注意坐标空间的左上角为x=0，y=0，x 的坐标点向右增长，y 的坐标点向下增长。]
    """

    @property
    def x(self) -> ST_AdjCoordinate:
        """x坐标

        X-Coordinate

        指定该位置坐标的 x 坐标。 该坐标空间的单位由路径坐标系的宽度定义。
        该坐标系覆盖在形状坐标系之上，从而占据整个形状边界框。
        由于此坐标空间内的单位由路径宽度和高度确定，因此无法在此处指定精确的测量单位。
        """

        return to_ST_AdjCoordinate(str(self.attrib['x']))

    @property
    def y(self) -> ST_AdjCoordinate:
        """y坐标

        Y-Coordinate

        指定该位置坐标的 y 坐标。 该坐标空间的单位由路径坐标系的高度定义。
        该坐标系覆盖在形状坐标系之上，从而占据整个形状边界框。
        由于此坐标空间内的单位由路径宽度和高度确定，因此无法在此处指定精确的测量单位。
        """

        return to_ST_AdjCoordinate(str(self.attrib['y']))


class CT_GeomRect(OxmlBaseElement):
    """形状文本矩形

    20.1.9.22 rect (Shape Text Rectangle)

    此元素指定 custGeom 形状内文本的矩形边界框。 该矩形的默认值是形状的边界框。
    可以使用此元素的四个属性来修改此属性以插入或扩展文本边界框

    [注意: 指定驻留在该形状文本矩形内的文本可以流到该边界框之外。 根据 txBody 元素中的自动调整选项，文本可能不会完全驻留在该形状文本矩形内。 ]
    """

    @property
    def left(self) -> ST_AdjCoordinate:
        """左边缘

        Left

        指定形状文本矩形左边缘的 x 坐标。 该边缘的单位在 EMU 中指定，因为此处的定位基于形状坐标系。 该坐标系的宽度和高度在 ext 变换元素中指定。
        """

        return to_ST_AdjCoordinate(str(self.attrib['l']))

    @property
    def top(self) -> ST_AdjCoordinate:
        """顶部边缘

        Top

        指定形状文本矩形顶部边缘的 y 坐标。 该边缘的单位在 EMU 中指定，因为此处的定位基于形状坐标系。 该坐标系的宽度和高度在 ext 变换元素中指定。
        """

        return to_ST_AdjCoordinate(str(self.attrib['t']))

    @property
    def right(self) -> ST_AdjCoordinate:
        """右边缘

        Right

        指定形状文本矩形右边缘的 x 坐标。 该边缘的单位在 EMU 中指定，因为此处的定位基于形状坐标系。 该坐标系的宽度和高度在 ext 变换元素中指定。
        """

        return to_ST_AdjCoordinate(str(self.attrib['r']))

    @property
    def bottom(self) -> ST_AdjCoordinate:
        """底部边缘

        Bottom Position

        指定形状文本矩形底部边缘的 y 坐标。 该边缘的单位在 EMU 中指定，因为此处的定位基于形状坐标系。 该坐标系的宽度和高度在 ext 变换元素中指定。
        """

        return to_ST_AdjCoordinate(str(self.attrib['b']))


class CT_XYAdjustHandle(OxmlBaseElement):
    """XY 调整手柄

    20.1.9.3 ahXY (XY Adjust Handle)

    此元素为自定义形状指定基于 XY 的调整手柄。 该调整手柄的位置由相应的 pos 子元素指定。
    该调整手柄允许的调整是通过其 min 和 max 类型属性指定的。
    基于此调整手柄的调整，更新某些相应的参考线以包含这些值。
    """

    @property
    def position(self) -> CT_AdjPoint2D:
        """
        位置
        """

        return getattr(self, qn('a:pos'))

    @property
    def gd_refx(self) -> Optional[ST_GeomGuideName]:
        """水平调整指南

        Horizontal Adjustment Guide

        指定使用此调整手柄的调整 x 位置更新的参考线的名称。
        """

        val = self.attrib['gdRefX']

        return ST_GeomGuideName(utils.AnyStrToStr(val))  # type: ignore

    @property
    def min_x(self) -> Optional[ST_AdjCoordinate]:
        """最小水平调整

        Minimum Horizontal Adjustment

        指定此调整手柄允许的最小水平位置。 如果省略该属性，则假定该调整手柄不能在 x 方向移动。 即 maxX 和 minX 相等。
        """

        return to_ST_AdjCoordinate(str(self.attrib['minX']))

    @property
    def max_x(self) -> Optional[ST_AdjCoordinate]:
        """最大水平调整

        Maximum Horizontal Adjustment

        指定此调整手柄允许的最大水平位置。 如果省略该属性，则假定该调整手柄不能在 x 方向移动。 即 maxX 和 minX 相等。
        """

        return to_ST_AdjCoordinate(str(self.attrib['maxX']))

    @property
    def gd_refy(self) -> Optional[ST_GeomGuideName]:
        """垂直调整指南

        Vertical Adjustment Guide

        指定使用此调整手柄的调整 y 位置更新的参考线的名称。
        """

        val = self.attrib['gdRefY']

        return ST_GeomGuideName(utils.AnyStrToStr(val))  # type: ignore

    @property
    def min_y(self) -> Optional[ST_AdjCoordinate]:
        """最小垂直调整

        Minimum Vertical Adjustment

        指定此调整手柄允许的最小垂直位置。 如果省略该属性，则假定该调整手柄无法沿 y 方向移动。 即 maxY 和 minY 相等。
        """

        return to_ST_AdjCoordinate(str(self.attrib['minY']))

    @property
    def max_y(self) -> Optional[ST_AdjCoordinate]:
        """最大垂直调整

        Maximum Vertical Adjustment

        指定此调整手柄允许的最大垂直位置。 如果省略该属性，则假定该调整手柄无法沿 y 方向移动。 即 maxY 和 minY 相等。
        """

        return to_ST_AdjCoordinate(str(self.attrib['maxY']))


class CT_PolarAdjustHandle(OxmlBaseElement):
    """极坐标调节手柄

    20.1.9.2 ahPolar (Polar Adjust Handle)

    此元素指定自定义形状的极坐标调整手柄。 该调整手柄的位置由相应的 pos 子元素指定。 该调整手柄允许的调整是通过其 min 和 max 属性指定的。 基于此调整手柄的调整，更新某些相应的参考线以包含这些值。

    This element specifies a polar adjust handle for a custom shape. The position of this adjust handle is specified by the corresponding pos child element. The allowed adjustment of this adjust handle are specified via it's min and max attributes. Based on the adjustment of this adjust handle certain corresponding guides are updated to contain these values.
    """

    @property
    def position(self) -> CT_AdjPoint2D:
        """
        位置
        """

        return getattr(self, qn('a:pos'))

    @property
    def gd_refr(self) -> Optional[ST_GeomGuideName]:
        """径向调整指南 gdRefR

        Radial Adjustment Guide

        指定使用此调整手柄的调整半径更新的参考线的名称。
        """

        val = self.attrib['gdRefR']

        return ST_GeomGuideName(utils.AnyStrToStr(val))  # type: ignore

    @property
    def min_r(self) -> Optional[ST_AdjCoordinate]:
        """最小径向调整 minR

        Minimum Radial Adjustment

        指定此调整手柄允许的最小径向位置。 如果省略该属性，则假定该调整手柄不能径向移动。 即 maxR 和 minR 相等。
        """

        return to_ST_AdjCoordinate(str(self.attrib['minR']))

    @property
    def max_r(self) -> Optional[ST_AdjCoordinate]:
        """最大径向调整 maxR

        Maximum Radial Adjustment

        指定此调整手柄允许的最大径向位置。 如果省略该属性，则假定该调整手柄不能径向移动。 即 maxR 和 minR 相等。
        """

        return to_ST_AdjCoordinate(str(self.attrib['maxR']))

    @property
    def gd_ref_ang(self) -> Optional[ST_GeomGuideName]:
        """角度调整指南 gdRefAng

        Angle Adjustment Guide

        指定使用此调整手柄的调整角度更新的参考线的名称。
        """

        val = self.attrib['gdRefAng']

        return ST_GeomGuideName(utils.AnyStrToStr(val))  # type: ignore

    @property
    def min_ang(self) -> Optional[ST_AdjAngle]:
        """最小角度调整

        Minimum Angle Adjustment

        指定此调整手柄允许的最小角度位置。 如果省略该属性，则假定该调整手柄不能进行角度移动。 即 maxAng 和 minAng 相等。
        """

        val = self.attrib['minAng']

        return to_ST_AdjAngle(str(val))

    @property
    def max_ang(self) -> Optional[ST_AdjAngle]:
        """最大角度调节

        Maximum Angle Adjustment

        指定此调整手柄允许的最大角度位置。 如果省略该属性，则假定该调整手柄不能进行角度移动。 即 maxAng 和 minAng 相等。
        """

        val = self.attrib['maxAng']

        return to_ST_AdjAngle(str(val))


class CT_ConnectionSite(OxmlBaseElement):
    """形状连接部位

    20.1.9.9 cxn (Shape Connection Site)

    此元素指定自定义形状上是否存在连接站点。 连接位点允许 cxnSp 连接到该形状。
    当形状在文档中重新定位时，这种连接会保持不变。
    应该注意的是，该连接是使用变换坐标系放置在形状边界框内的，变换坐标系也称为形状坐标系，因为它包含整个形状。
    该坐标系的宽度和高度在 ext 变换元素中指定。

    [注意: 变换坐标系与路径坐标系不同，因为它是针对每个形状而不是形状内的每个路径。]
    """

    @property
    def position(self) -> CT_AdjPoint2D:
        """
        位置
        """

        return getattr(self, qn('a:pos'))

    @property
    def angle(self) -> ST_AdjAngle:
        """连接部位角度

        Connection Site Angle

        指定传入连接器角度。 该角度是传入连接器尝试路由到的连接站点周围的角度。
        这使得连接器能够知道形状相对于连接位置和路由连接器的位置，以避免与形状重叠。
        """

        return to_ST_AdjAngle(str(self.attrib['ang']))


class CT_AdjustHandleList(OxmlBaseElement):
    """形状调整手柄列表

    20.1.9.1 ahLst (List of Shape Adjust Handles)

    该元素指定应用于自定义几何体的调整手柄。 这些调整手柄指定几何形状内的点，可用于对形状执行某些变换操作。
    """

    @property
    def adjust_handle(self) -> list[CT_XYAdjustHandle | CT_PolarAdjustHandle]:
        """
        调整列表
        """

        tags = (
            qn('a:ahXY'),  # CT_XYAdjustHandle
            qn('a:ahPolar'),  # CT_PolarAdjustHandle
        )

        return self.choice_and_more(*tags)  # type: ignore


class CT_ConnectionSiteList(OxmlBaseElement):
    """形状连接位点列表

    20.1.9.10 cxnLst (List of Shape Connection Sites)

    该元素指定用于该形状的所有连接点。 连接点是通过在形状边界框中定义一个点来指定的，该点可以附加一个 cxnSp 元素。
    这些连接点是使用 ext 变换元素中指定的形状坐标系来指定的。
    """

    def connectors(self) -> list[CT_ConnectionSite]:
        """
        连接点
        """

        return self.findall(qn('a:cxn'))  # type: ignore


class CT_Connection(OxmlBaseElement):
    """连接结束

    20.1.2.2.13 endCxn

    该元素指定应由相应连接器形状形成的结束连接。 这会将连接器的尾部连接到最终目标形状。
    """

    @property
    def id(self) -> ST_DrawingElementId:
        """标识符

        指定要进行最终连接的形状的 id.
        """

        val = self.attrib['id']

        return ST_DrawingElementId(utils.AnyStrToStr(val))  # type: ignore

    @property
    def idx(self) -> XSD_UnsignedInt:
        """索引

        指定最终连接形状的连接站点表的索引。 即一个形状上有很多连接点，需要指定对应的连接器形状应该连接到哪个连接点.
        """

        val = self.attrib['idx']

        return to_xsd_unsigned_int(val)  # type: ignore


class CT_Path2DMoveTo(OxmlBaseElement):
    """将路径移至

    20.1.9.14 moveTo

    此元素指定要将形状光标移动到的一组新坐标。 该元素仅用于绘制自定义几何图形。 当使用此元素时，pt 元素用于指定形状光标应移动到的一组新的形状坐标。 这不会从旧位置绘制直线或曲线到新位置，而只是将光标移动到新的起始位置。 只有当使用lnTo等路径绘制元素时，才会绘制路径的一部分.
    """

    @property
    def point(self) -> CT_AdjPoint2D:
        """目标点"""

        return getattr(self, qn('a:pt'))


class CT_Path2DLineTo(OxmlBaseElement):
    """画线至

    20.1.9.13 lnTo

    该元素指定从当前笔位置到指定的新点的直线绘制。 这条线成为形状几何的一部分，代表形状的一侧。 指定这条线时使用的坐标系是路径坐标系。
    """

    @property
    def point(self) -> CT_AdjPoint2D:
        """目标点"""

        return getattr(self, qn('a:pt'))


class CT_Path2DArcTo(OxmlBaseElement):
    """绘制圆弧至

    20.1.9.4 arcTo

    该元素指定形状路径中是否存在圆弧。 它使用指定的参数从当前笔位置到指定的新点绘制一条圆弧。 弧是根据假定的圆的形状弯曲的线。 该弧的长度是通过指定起始角度和结束角度来确定的，这两个角度共同作用以有效地指定弧的终点。
    """

    @property
    def w_r(self) -> ST_AdjCoordinate:
        """形状 弧宽 半径

        该属性指定用于绘制圆弧的假设圆的宽度半径。 这使得圆的总宽度为 (2 * wR)。 该总宽度也可以称为水平直径，因为它只是 x 轴的直径.
        """

        return to_ST_AdjCoordinate(str(self.attrib['wR']))

    @property
    def h_r(self) -> ST_AdjCoordinate:
        """形状 弧高 半径

        该属性指定用于绘制圆弧的假设圆的高度半径。 这使得圆的总高度为 (2 * hR)。 这个总高度也可以称为它的垂直直径，因为它只是 y 轴的直径.
        """

        return to_ST_AdjCoordinate(str(self.attrib['hR']))

    @property
    def st_ang(self) -> ST_AdjAngle:
        """形状圆弧起始角度

        start angle

        指定圆弧的起始角度。 该角度指定沿着假定的圆路径的哪个角度用作绘制圆弧的起始位置。 该起始角度被锁定到形状路径中最后已知的笔位置。 从而保证连续的形状路径.
        """

        return to_ST_AdjAngle(str(self.attrib['stAng']))

    @property
    def sw_ang(self) -> ST_AdjAngle:
        """形状圆弧摆动角度

        swing angle

        指定圆弧的摆动角度。 该角度指定圆弧沿假定的圆弧路径以角度方向延伸的距离。 从起始角开始的延伸始终围绕假定的圆沿顺时针方向延伸.
        """

        return to_ST_AdjAngle(str(self.attrib['swAng']))


class CT_Path2DQuadBezierTo(OxmlBaseElement):
    """绘制二次贝塞尔曲线

    20.1.9.21 quadBezTo

    该元素指定沿指定点绘制二次贝塞尔曲线。 要指定二次贝塞尔曲线，需要指定 2 个点。 第一个是二次贝塞尔曲线计算中使用的控制点，最后一个是曲线的终点。 用于此类曲线的坐标系是路径坐标系，因为该元素是特定于路径的.
    """

    @property
    def points(self) -> tuple[CT_AdjPoint2D, CT_AdjPoint2D]:
        """绘制的两个点"""

        tag = qn('a:pt')

        pts = self.findall(tag)

        if len(pts) != 2:
            msg = '元素节点数量应为2'
            raise OxmlElementValidateError(msg)

        return pts[0], pts[1]  # type: ignore


class CT_Path2DCubicBezierTo(OxmlBaseElement):
    """绘制三次贝塞尔曲线至

    20.1.9.7 cubicBezTo

    该元素指定沿指定点绘制三次贝塞尔曲线。 要指定三次贝塞尔曲线，需要指定 3 个点。 前两个是三次贝塞尔曲线计算中使用的控制点，最后一个是曲线的终点。 用于这种曲线的坐标系是路径坐标系，因为该元素是特定于路径的。
    """

    @property
    def points(self) -> tuple[CT_AdjPoint2D, CT_AdjPoint2D, CT_AdjPoint2D]:
        """3个点"""

        tag = qn('a:pt')

        pts = self.findall(tag)

        if len(pts) != 3:
            msg = '元素节点数量应为3'
            raise OxmlElementValidateError(msg)

        return pts[0], pts[1], pts[2]  # type: ignore


class CT_Path2DClose(OxmlBaseElement):
    """路径绘制结束"""



class ST_PathFillMode(ST_BaseEnumType):
    """路径填充模式

    20.1.10.37 ST_PathFillMode

    这个简单类型规定了路径填充的方式。路径的明暗变化允许根据用户的偏好对形状的特定部分进行轻或重的着色。

    这个简单类型的内容是对W3C XML Schema标记数据类型的限制。

    这个简单类型被限制为以下表格中列出的值:
    """

    none = 'none'
    """（无路径填充）: 指定相应的路径不应填充任何颜色。"""

    Norm = 'norm'
    """（正常路径填充）: 指定相应的路径应该用正常阴影颜色进行填充。"""

    Lighten = 'lighten'
    """加亮路径填充）: 指定相应的路径应该用较浅的阴影颜色进行填充。"""

    LightenLess = 'lightenLess'
    """（稍加亮路径填充）: 指定相应的路径应该用略微较浅的阴影颜色进行填充。"""

    Darken = 'darken'
    """（加深路径填充）: 指定相应的路径应该用较深的阴影颜色进行填充。"""

    DarkenLess = 'darkenLess'
    """（稍加深路径填充）: 指定相应的路径应该用略微较深的阴影颜色进行填充。"""


class CT_Path2D(OxmlBaseElement):
    """形状路径

    20.1.9.15 path

    该元素指定由一系列移动、直线和曲线组成的创建路径，这些移动、直线和曲线组合起来形成几何形状。 仅当指定了自定义几何图形时才使用此元素。

    [Note: 由于允许多个路径，因此绘制规则是在 pathLst 中稍后指定的路径绘制在所有先前路径的顶部. end note]
    """

    @property
    def paths(
        self,
    ) -> list[
        CT_Path2DClose | CT_Path2DMoveTo | CT_Path2DLineTo | CT_Path2DArcTo | CT_Path2DQuadBezierTo | CT_Path2DCubicBezierTo
    ]:
        """
        路径列表
        """

        tags = (
            qn('a:close'),
            qn('a:moveTo'),
            qn('a:lnTo'),
            qn('a:arcTo'),
            qn('a:quadBezTo'),
            qn('a:cubicBezTo'),
        )

        return self.choice_and_more(*tags)  # type: ignore

    @property
    def width(self) -> Optional[ST_PositiveCoordinate]:
        """路径宽度

        指定路径坐标系内应使用的宽度或最大 x 坐标。 该值确定相应路径内所有点的水平位置，因为它们都是使用该宽度属性作为最大 x 坐标来计算的.
        """

        w = self.attrib.get('w')

        if w is None:
            return None

        return to_ST_PositiveCoordinate(str(w))

    @property
    def height(self) -> Optional[ST_PositiveCoordinate]:
        """路径高度

        指定路径坐标系内应使用的高度或最大 y 坐标。 该值确定相应路径内所有点的垂直位置，因为它们都是使用该高度属性作为最大 y 坐标来计算的.
        """

        h = self.attrib.get('h')

        if h is None:
            return None

        return to_ST_PositiveCoordinate(str(h))

    @property
    def fill(self) -> ST_PathFillMode:
        """路径填充模式

        指定应如何填充相应的路径。 如果省略此属性，则假定值为“norm”.

        - darken（加深路径填充）: 指定相应的路径应该用较深的阴影颜色进行填充。
        - darkenLess（稍加深路径填充）: 指定相应的路径应该用略微较深的阴影颜色进行填充。
        - lighten（加亮路径填充）: 指定相应的路径应该用较浅的阴影颜色进行填充。
        - lightenLess（稍加亮路径填充）: 指定相应的路径应该用略微较浅的阴影颜色进行填充。
        - none（无路径填充）: 指定相应的路径不应填充任何颜色。
        - norm（正常路径填充）: 指定相应的路径应该用正常阴影颜色进行填充。
        """

        val = self.attrib.get('fill')

        if val is None:
            return ST_PathFillMode.Norm

        return ST_PathFillMode(val)

    @property
    def stroke(self) -> XSD_Boolean:
        """路径描边

        指定相应路径是否应显示路径描边。 这是一个影响路径轮廓的布尔值。 如果省略此属性，则假定值为 true.
        """

        val = self.attrib.get('stroke')

        return to_xsd_bool(val, none=True)

    @property
    def extrusion_ok(self) -> XSD_Boolean:
        """允许 3D 挤压

        指定在此路径上可以使用 3D 拉伸。 这使得生成应用程序能够知道 3D 挤压是否可以以任何形式应用。 如果省略此属性，则假定值为 0 或 false.
        """

        val = self.attrib.get('extrusionOk')

        return to_xsd_bool(val, none=True)


class CT_Path2DList(OxmlBaseElement):
    """形状路径列表

    20.1.9.16 pathLst

    该元素指定组成单个几何形状的整个路径。 pathLst 中可以包含许多单独的路径。

    [Note: 具有多个路径的几何体应该在视觉上被视为每个路径都是一个不同的形状。 也就是说，每个创建路径都有其第一个点和最后一个点连接起来形成一个封闭的形状。 但是，生成应用程序随后应将新形状的最后一个点连接到第一个点。 如果在先前创建路径的末尾遇到关闭元素，则生成应用程序不应呈现该连接线。 渲染应从新创建路径上的第一条直线或曲线开始。 end note]

    注意:

    一个包含多个路径的几何图形在视觉上应被视为每个路径都是一个独立的形状。也就是说，每个创建路径都有其第一个点和最后一个点连接形成一个闭合的形状。然而，生成应用程序应该将最后一个点连接到新形状的第一个点。如果在前一个创建路径的末尾遇到一个闭合元素，那么生成应用程序不应该渲染这个连接线。渲染应该从新创建路径的第一条线或曲线开始。
    """

    @property
    def path_lst(self) -> list[CT_Path2D]:
        """
        2D 路径集
        """

        return self.findall(qn('a:path'))  # type: ignore


class CT_PresetGeometry2D(OxmlBaseElement):
    """预置几何图形

    20.1.9.18 prstGeom

    此元素指定何时应使用预设几何形状而不是自定义几何形状。 生成应用程序应该能够渲染 ST_ShapeType 列表中枚举的所有预设几何图形。
    """

    @property
    def av_lst(self) -> Optional[CT_GeomGuideList]:
        """形状指南列表

        20.1.9.12 gdLst (List of Shape Guides)

        该元素指定用于该形状的所有参考线。 参考线由 gd 元素指定，并定义可用于构造相应形状的计算值。

        [注意: 具有通过上面的 fmla="val x" 指定的文字值公式的指南只能在 avLst 中用作形状的调整值。 然而，这并没有严格执行。]
        """

        return getattr(self, qn('a:avLst'), None)

    @property
    def preset(self) -> ST_ShapeType:
        """预设形状类型

        20.1.10.56 ST_ShapeType (Preset Shape Types)

        此简单类型指定要用于形状的预设形状几何形状。
        使用这种简单类型的枚举，以便不必指定自定义几何图形，而是可以由生成应用程序自动构造。
        对于列出的每个枚举，还有相应的 DrawingML 代码，如果它是自定义几何图形，则将使用该代码来构造此形状。
        在每个预设形状的构造规范中，都有预定义的指南，生成应用程序应始终维护这些指南以用于计算目的。

        必要的指南应具有以下值。

        公式语法组件在 gd 元素的 fmla 属性中定义（第 20.1.9.11 节）。
        """

        return ST_ShapeType(self.attrib['prst'])


class CT_PresetTextShape(OxmlBaseElement):
    """预设文本及格式

    20.1.9.19 prstTxWarp

    该元素指定何时应使用预设的几何形状来变换一段文本。 此操作的正式名称为文本扭曲。 生成应用程序应该能够渲染 ST_TextShapeType 列表中枚举的所有预设几何图形。
    """

    @property
    def av_lst(self) -> Optional[CT_GeomGuideList]:
        """形状参考列表

        20.1.9.12 gdLst (List of Shape Guides)

        该元素指定用于该形状的所有参考线。 参考线由 gd 元素指定，并定义可用于构造相应形状的计算值。

        [注意: 具有通过上面的 fmla="val x" 指定的文字值公式的指南只能在 avLst 中用作形状的调整值。 然而，这并没有严格执行。]
        """

        return getattr(self, qn('a:avLst'), None)

    @property
    def preset(self) -> ST_ShapeType:
        """预设变形形状

        指定用于文本片段形状扭曲的预设几何体。 此预设可以具有 ST_TextShapeType 枚举列表中的任何值。 为了渲染文本扭曲，需要此属性。
        """

        return ST_ShapeType(self.attrib['prst'])


class CT_CustomGeometry2D(OxmlBaseElement):
    """自定义几何图形

    20.1.9.8 custGeom

    该元素指定是否存在自定义几何形状。 该形状由创建路径中描述的一系列直线和曲线组成。 除此之外，还可以有调整值、参考线、调整手柄、连接点和为此自定义几何形状指定的内接矩形。
    """

    @property
    def av_lst(self) -> Optional[CT_GeomGuideList]:
        """形状参考列表

        20.1.9.12 gdLst (List of Shape Guides)

        该元素指定用于该形状的所有参考线。 参考线由 gd 元素指定，并定义可用于构造相应形状的计算值。

        [注意: 具有通过上面的 fmla="val x" 指定的文字值公式的指南只能在 avLst 中用作形状的调整值。 然而，这并没有严格执行。]
        """

        return getattr(self, qn('a:avLst'), None)

    @property
    def gd_lst(self) -> Optional[CT_GeomGuideList]:
        """形状参考列表

        20.1.9.12 gdLst (List of Shape Guides)

        该元素指定用于该形状的所有参考线。 参考线由 gd 元素指定，并定义可用于构造相应形状的计算值。

        [注意: 具有通过上面的 fmla="val x" 指定的文字值公式的指南只能在 avLst 中用作形状的调整值。 然而，这并没有严格执行。]
        """

        return getattr(self, qn('a:gdLst'), None)

    @property
    def ah_lst(self) -> Optional[CT_AdjustHandleList]:
        """形状调整手柄列表

        20.1.9.1 ahLst (List of Shape Adjust Handles)

        该元素指定应用于自定义几何体的调整手柄。 这些调整手柄指定几何形状内的点，可用于对形状执行某些变换操作。
        """

        return getattr(self, qn('a:ahLst'), None)

    @property
    def cxn_lst(self) -> Optional[CT_ConnectionSiteList]:
        """形状连接位点列表

        20.1.9.10 cxnLst (List of Shape Connection Sites)

        该元素指定用于该形状的所有连接点。 连接点是通过在形状边界框中定义一个点来指定的，该点可以附加一个 cxnSp 元素。
        这些连接点是使用 ext 变换元素中指定的形状坐标系来指定的。
        """

        return getattr(self, qn('a:cxnLst'), None)

    @property
    def rect(self) -> Optional[CT_GeomRect]:
        """形状文本矩形

        20.1.9.22 rect (Shape Text Rectangle)

        此元素指定 custGeom 形状内文本的矩形边界框。 该矩形的默认值是形状的边界框。
        可以使用此元素的四个属性来修改此属性以插入或扩展文本边界框

        [注意: 指定驻留在该形状文本矩形内的文本可以流到该边界框之外。 根据 txBody 元素中的自动调整选项，文本可能不会完全驻留在该形状文本矩形内。 ]
        """

        return getattr(self, qn('a:rect'), None)

    @property
    def path_lst(self) -> CT_Path2DList:
        """
        aaa
        """

        return getattr(self, qn('a:pathLst'))


class EG_Geometry(OxmlBaseElement):
    """几何图形

    <xsd:group name="EG_Geometry">
        <xsd:choice>
            <xsd:element name="custGeom" type="CT_CustomGeometry2D" minOccurs="1" maxOccurs="1"/>
            <xsd:element name="prstGeom" type="CT_PresetGeometry2D" minOccurs="1" maxOccurs="1"/>
        </xsd:choice>
    </xsd:group>
    """

    geometry_tags = (
        # 自定义几何
        qn('a:custGeom'),  # CT_CustomGeometry2D
        # 预置几何
        qn('a:prstGeom'),  # CT_PresetGeometry2D
    )


class EG_TextGeometry(OxmlBaseElement):
    """文本几何图形

    <xsd:group name="EG_TextGeometry">
        <xsd:choice>
            <xsd:element name="custGeom" type="CT_CustomGeometry2D" minOccurs="1" maxOccurs="1"/>
            <xsd:element name="prstTxWarp" type="CT_PresetTextShape" minOccurs="1" maxOccurs="1"/>
        </xsd:choice>
    </xsd:group>
    """

    text_geometry_tags = (
        # 自定义几何
        qn('a:custGeom'),  # CT_CustomGeometry2D
        # 预置文本几何
        qn('a:prstTxWarp'),  # CT_PresetTextShape
    )

    def text_geometry(
        self,
    ) -> Optional[CT_CustomGeometry2D | CT_PresetTextShape]:
        """几何图形"""

        return self.choice_one_child(*self.text_geometry_tags)  # type: ignore


class ST_LineEndType(ST_BaseEnumType):
    """线头/线尾 类型

    20.1.10.33 ST_LineEndType

    这个简单类型表示出现在线条末端的形状装饰，例如箭头头部。
    """

    none = 'none'
    Triangle = 'triangle'  # Triangle Arrow Head
    Stealth = 'stealth'  # Stealth Arrow
    Diamond = 'diamond'
    Oval = 'oval'
    Arrow = 'arrow'  # Line arrow head


class ST_LineEndWidth(ST_BaseEnumType):
    """线头/线尾 宽度

    20.1.10.34 ST_LineEndWidth

    这个简单类型表示线条末端装饰（例如箭头头部）相对于线条本身宽度的宽度。
    """

    Small = 'sm'
    Medium = 'med'
    Large = 'lg'


class ST_LineEndLength(ST_BaseEnumType):
    """线头/线尾 长度

    20.1.10.32 ST_LineEndLength

    这个简单类型表示线条结束装饰（例如箭头）相对于线条本身宽度的长度。
    """

    Small = 'sm'
    Medium = 'med'
    Large = 'lg'


class CT_LineEndProperties(OxmlBaseElement):
    """线头/线尾样式

    20.1.8.38 headEnd

    该元素指定可以添加到行首的装饰。
    """

    @property
    def type(self) -> ST_LineEndType:
        """线头/线尾类型

        指定线端装饰，例如三角形或箭头.

        该属性的可能值由 ST_LineEndType 简单类型定义 (§20.1.10.33).
        """

        val = self.attrib.get('type')

        if val is None:
            return ST_LineEndType.none

        return ST_LineEndType(val)

    @property
    def width(self) -> Optional[ST_LineEndWidth]:
        """头/尾宽度

        指定相对于线宽的线端宽度.

        该属性的可能值由 ST_LineEndWidth 简单类型定义 (§20.1.10.34).
        """

        val = self.attrib.get('w')

        if val is not None:
            return ST_LineEndWidth(val)

        return None

    @property
    def length(self) -> Optional[ST_LineEndLength]:
        """头/尾长度

        指定与线宽相关的线端长度.

        该属性的可能值由 ST_LineEndLength 简单类型定义 (§20.1.10.32).
        """

        val = self.attrib.get('len')

        if val is not None:
            return ST_LineEndLength(val)

        return None


class EG_LineFillProperties(OxmlBaseElement):
    """
    <xsd:group name="EG_LineFillProperties">
        <xsd:choice>
            <xsd:element name="noFill" type="CT_NoFillProperties" minOccurs="1" maxOccurs="1"/>
            <xsd:element name="solidFill" type="CT_SolidColorFillProperties" minOccurs="1" maxOccurs="1"/>
            <xsd:element name="gradFill" type="CT_GradientFillProperties" minOccurs="1" maxOccurs="1"/>
            <xsd:element name="pattFill" type="CT_PatternFillProperties" minOccurs="1" maxOccurs="1"/>
        </xsd:choice>
    </xsd:group>
    """

    line_fill_pr_tags = (
        qn('a:noFill'),  # CT_NoFillProperties
        qn('a:solidFill'),  # CT_SolidColorFillProperties
        qn('a:gradFill'),  # CT_GradientFillProperties
        qn('a:pattFill'),  # CT_PatternFillProperties
    )


class CT_LineJoinBevel(OxmlBaseElement):
    """斜角连接样式

    20.1.8.9 bevel

    该元素指定斜角线连接。

    斜角接头指定使用角度接头来连接线条。
    """



class CT_LineJoinRound(OxmlBaseElement):
    """圆形连接样式

    20.1.8.52 round

    该元素指定连接在一起的线具有圆形连接。
    """



class CT_LineJoinMiterProperties(OxmlBaseElement):
    """斜接连接样式

    20.1.8.43 miter

    该元素指定线连接应进行斜接。
    """

    @property
    def limit(self) -> Optional[ST_PositivePercentage]:
        """斜接连接限制

        指定线延伸形成斜接的量 - 否则斜接可以无限延伸（对于几乎平行的线）.
        """

        val = self.attrib.get('lim')

        if val is not None:
            return to_ST_PositivePercentage(str(val))

        return None


class EG_LineJoinProperties(OxmlBaseElement):
    """
    <xsd:group name="EG_LineJoinProperties">
        <xsd:choice>
            <xsd:element name="round" type="CT_LineJoinRound" minOccurs="1" maxOccurs="1"/>
            <xsd:element name="bevel" type="CT_LineJoinBevel" minOccurs="1" maxOccurs="1"/>
            <xsd:element name="miter" type="CT_LineJoinMiterProperties" minOccurs="1" maxOccurs="1"/>
        </xsd:choice>
    </xsd:group>
    """

    line_join_pr_tags = (
        qn('a:round'),  # CT_LineJoinRound
        qn('a:bevel'),  # CT_LineJoinBevel
        qn('a:miter'),  # CT_LineJoinMiterProperties
    )

    @property
    def line_join_properties(
        self,
    ) -> Optional[CT_LineJoinRound | CT_LineJoinBevel | CT_LineJoinMiterProperties]:
        """
        aaa
        """

        return self.choice_one_child(*self.line_join_pr_tags)  # type: ignore


class ST_PresetLineDashVal(ST_BaseEnumType):
    """预设线型/轮廓虚线

    20.1.10.49 ST_PresetLineDashVal

    这个简单类型表示预设线条虚线样式。每种样式的描述都显示了该线条样式的示意图。每种样式还包含了一个精确的二进制表示，表示重复的虚线样式。每个1对应于与线宽相同长度的线段，而每个0对应于与线宽相同长度的空白(space)。

    - dash（短划线）: 1111000
    - dashDot（短划点线）: 11110001000
    - dot（点线）: 1000
    - lgDash（长短划线）: 11111111000
    - lgDashDot（长短划点线）: 111111110001000
    - lgDashDotDot（长短划点点线）: 1111111100010001000
    - solid（实线）: 1
    - sysDash（系统短划线）: 1110
    - sysDashDot（系统短划点线）: 111010
    - sysDashDotDot（系统短划点点线）: 11101010
    - sysDot（系统点线）: 10
    """

    Solid = 'solid'
    """ （实线）:1 """

    Dot = 'dot'
    """ （点线）:1000 """

    Dash = 'dash'
    """ （短划线）: 1111000 """

    LgDash = 'lgDash'
    """ 长短划线）:11111111000 """

    DashDot = 'dashDot'
    """ （短划点线）:11110001000 """

    LgDashDot = 'lgDashDot'
    """ （长短划点线）:111111110001000 """

    LgDashDotDot = 'lgDashDotDot'
    """ （长短划点点线）:1111111100010001000 """

    SysDash = 'sysDash'
    """ （系统短划线）:1110 """

    SysDot = 'sysDot'
    """ （系统点线）:10 """

    SysDashDot = 'sysDashDot'
    """ （系统短划点线）:111010 """

    SysDashDotDot = 'sysDashDotDot'
    """ （系统短划点点线）:11101010 """


class CT_PresetLineDashProperties(OxmlBaseElement):
    """预设虚线样式

    20.1.8.48 prstDash

    该元素指定应使用预设的虚线方案。
    """

    @property
    def value(self) -> Optional[ST_PresetLineDashVal]:
        """预设线型/轮廓虚线

        20.1.10.49 ST_PresetLineDashVal

        这个简单类型表示预设线条虚线样式。每种样式的描述都显示了该线条样式的示意图。每种样式还包含了一个精确的二进制表示，表示重复的虚线样式。每个1对应于与线宽相同长度的线段，而每个0对应于与线宽相同长度的空白(space)。

        - dash（短划线）:1111000
        - dashDot（短划点线）:11110001000
        - dot（点线）:1000
        - lgDash（长短划线）:11111111000
        - lgDashDot（长短划点线）: 111111110001000
        - lgDashDotDot（长短划点点线）: 1111111100010001000
        - solid（实线）: 1
        - sysDash（系统短划线）: 1110
        - sysDashDot（系统短划点线）: 111010
        - sysDashDotDot（系统短划点点线）: 11101010
        - sysDot（系统点线）: 10
        """

        val = self.attrib.get('val')

        if val is not None:
            return ST_PresetLineDashVal(val)

        return None


class CT_DashStop(OxmlBaseElement):
    """虚线停止点

    20.1.8.22 ds (Dash Stop)

    该元素指定破折号停止原语。 冲线方案是通过指定冲线停止原语的有序列表来构建的。 破折号停止基元由破折号和空格组成。

    """

    @property
    def dash(self) -> ST_PositivePercentage:
        """虚线长度

        Dash Length

        指定虚线相对于线宽的长度。
        """

        return to_ST_PositivePercentage(str(self.attrib['d']))

    @property
    def stop(self) -> ST_PositivePercentage:
        """空格长度

        Space Length

        指定相对于线宽的空间长度。
        """

        return to_ST_PositivePercentage(str(self.attrib['sp']))


class CT_DashStopList(OxmlBaseElement):
    """虚线自定义停止 列表

    20.1.8.21 custDash (Custom Dash)

    该元素指定自定义虚线方案。 它是一个虚线停止元素列表，代表构建自定义虚线方案的构建块原子。
    """

    @property
    def dash_stops(self) -> list[CT_DashStop]:
        """虚线停止点"""

        return self.findall(qn('a:ds'))  # type: ignore


# element group
class EG_LineDashProperties(OxmlBaseElement):
    """
    <xsd:group name="EG_LineDashProperties">
        <xsd:choice>
            <xsd:element name="prstDash" type="CT_PresetLineDashProperties" minOccurs="1" maxOccurs="1"/>
            <xsd:element name="custDash" type="CT_DashStopList" minOccurs="1" maxOccurs="1"/>
        </xsd:choice>
    </xsd:group>
    """

    line_dash_pr_tags = (
        qn('a:prstDash'),  # CT_PresetLineDashProperties
        qn('a:custDash'),  # CT_DashStopList
    )

    @property
    def line_dash_properties(
        self,
    ) -> Optional[CT_PresetLineDashProperties | CT_DashStopList]:
        """
        aaa
        """

        return self.choice_one_child(*self.line_dash_pr_tags)  # type: ignore


class ST_LineCap(ST_BaseEnumType):
    """线端点类型

    20.1.10.31 ST_LineCap

    这个简单类型指定了如何对线的端点进行截断。这也会影响虚线的线段端点。

    - flat（平直线端点）: 线段在端点结束。
    - rnd（圆形线端点）: 圆形端点。半圆突出半条线宽。
    - sq（方形线端点）: 方形端点。方形突出半条线宽。
    """

    Round = 'rnd'
    """ （圆形线端点）: 圆形端点。半圆突出半条线宽。 """

    Square = 'sq'
    """ （方形线端点）: 方形端点。方形突出半条线宽。 """

    Flat = 'flat'
    """ （平直线端点）: 线段在端点结束。 """


class ST_LineWidth(ST_BaseType[AnyStr, int]):
    """线宽度

    20.1.10.35 ST_LineWidth

    这个简单类型指定了线条的宽度，以 EMUs（English Metric Units）为单位。1磅等于12700 EMUs。

    这个简单类型的内容是对 ST_Coordinate32Unqualified 数据类型（§20.1.10.18）的限制。

    这个简单类型还指定了以下限制:

    - 该简单类型的最小值大于或等于0。
    - 该简单类型的最大值小于或等于20116800。
    """

    def _validate(self: Self) -> None:
        val = int(utils.AnyStrToStr(self._val))

        if not (0 <= val <= 20116800):
            msg = f'预期外的值: {val}'
            raise OxmlAttributeValidateError(msg)

        self._python_val = val


class ST_PenAlignment(ST_BaseEnumType):
    """笔对齐类型

    20.1.10.39 ST_PenAlignment (Alignment Type)

    此简单类型指定在文本正文中使用的笔对齐类型。
    """

    Center = 'ctr'
    """Center Alignment  中心笔（在路径描边中心绘制的线）。"""

    Inset = 'in'
    """Inset Alignment  插入笔（笔在路径边缘的内侧对齐）。"""


class ST_CompoundLine(ST_BaseEnumType):
    """复合线型

    20.1.10.15 ST_CompoundLine (Compound Line Type)

    此简单类型指定用于带有文本（例如下划线）的线条的复合线条类型。
    """

    SingleLine = 'sng'
    """（单线）-- 单线，正常宽度"""

    DoubleLines = 'dbl'
    """（双线）-- 双线，宽度相等"""

    ThickThin = 'thickThin'
    """ （粗细双线）-- 双线，一粗一细 """

    ThinThick = 'thinThick'
    """ （细粗双线）-- 双线，一细一粗 """

    Tri = 'tri'
    """ （细粗细三重线）-- 三条线，细、粗、细 """


class CT_LineProperties(EG_LineDashProperties, EG_LineFillProperties, EG_LineJoinProperties):
    """线条特性(属性)

    20.1.2.2.24 ln

    此元素指定可应用于许多不同对象（例如形状和文本）的轮廓样式。 该线允许指定许多不同类型的轮廓，包括甚至线虚线和斜角。
    """

    @property
    def line_fill(
        self,
    ) -> Optional[
        CT_NoFillProperties | CT_SolidColorFillProperties | CT_GradientFillProperties | CT_PatternFillProperties
    ]:
        """填充样式"""

        return self.choice_one_child(*self.line_fill_pr_tags)  # type: ignore

    @property
    def line_dash(
        self,
    ) -> Optional[CT_PresetLineDashProperties | CT_DashStopList]:
        """虚线样式"""

        return self.choice_one_child(*self.line_dash_pr_tags)  # type: ignore

    @property
    def line_join(
        self,
    ) -> Optional[CT_LineJoinRound | CT_LineJoinBevel | CT_LineJoinMiterProperties]:
        """线条连接样式"""

        return self.choice_one_child(*self.line_join_pr_tags)  # type: ignore

    @property
    def head_end(self) -> Optional[CT_LineEndProperties]:
        """线头样式"""

        return getattr(self, qn('a:headEnd'), None)

    @property
    def tail_end(self) -> Optional[CT_LineEndProperties]:
        """线尾样式"""

        return getattr(self, qn('a:tailEnd'), None)

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)

    @property
    def width(self) -> ST_LineWidth:
        """线条的宽度 Line Width

        以 EMUs 为单位。1pt = 12700 EMUs。

        如果省略了该属性，则假定为0。
        """

        val = self.attrib.get('w')

        if val is not None:
            return ST_LineWidth(val)

        return ST_LineWidth('0')

    @property
    def cap(self) -> ST_LineCap:
        """线端盖类型 Line Ending Cap Type

        指定应用于该行的结束大写。 [注: 上限类型的示例有圆形、扁平等。尾注]

        如果省略此属性，则假定值为 square .

        线端点类型

        20.1.10.31 ST_LineCap

        这个简单类型指定了如何对线的端点进行截断。这也会影响虚线的线段端点。

        - flat（平直线端点）: 线段在端点结束。
        - rnd（圆形线端点）: 圆形端点。半圆突出半条线宽。
        - sq（方形线端点）: 方形端点。方形突出半条线宽。
        """

        val = self.attrib.get('cap')

        if val is not None:
            return ST_LineCap(val)

        return ST_LineCap.Square

    @property
    def cmpd(self) -> ST_CompoundLine:
        """复合线型 Compound Line Type

        指定用于下划线描边的复合线类型。 如果省略此属性，则假定值为 sng.

        - dbl（双线）-- 双线，宽度相等
        - sng（单线）-- 单线，正常宽度
        - thickThin（粗细双线）-- 双线，一粗一细
        - thinThick（细粗双线）-- 双线，一细一粗
        - tri（细粗细三重线）-- 三条线，细、粗、细
        """

        val = self.attrib.get('cmpd')

        if val is not None:
            return ST_CompoundLine(val)

        return ST_CompoundLine.SingleLine

    @property
    def algn(self) -> Optional[ST_PenAlignment]:
        """对齐方式 Stroke Alignment

        指定用于下划线描边的对齐方式.
        """

        val = self.attrib.get('algn')

        if val is not None:
            return ST_PenAlignment(val)

        return None


# <xsd:restriction base="xsd:token"/>
ST_ShapeID = NewType('ST_ShapeID', str)
"""形状ID

20.1.10.55 ST_ShapeID

指定用于传统形状标识目的的形状 ID。
"""


class CT_ShapeProperties(EG_FillProperties, EG_EffectProperties, EG_Geometry):
    """形状特性

    19.3.1.44 spPr

    此元素指定可应用于形状的视觉形状属性。 这些属性包括形状填充、轮廓、几何形状、效果和 3D 方向。
    """

    @property
    def xfrm(self) -> Optional[CT_Transform2D]:
        """位置"""

        return getattr(self, qn('a:xfrm'), None)

    @property
    def geometry(self) -> Optional[CT_CustomGeometry2D | CT_PresetGeometry2D]:
        """几何图形

        预置几何图形

        20.1.9.18 prstGeom

        此元素指定何时应使用预设几何形状而不是自定义几何形状。 生成应用程序应该能够渲染 ST_ShapeType 列表中枚举的所有预设几何图形。


        20.1.9.8 custGeom 自定义几何图形

        该元素指定是否存在自定义几何形状。 该形状由创建路径中描述的一系列直线和曲线组成。 除此之外，还可以有调整值、参考线、调整手柄、连接点和为此自定义几何形状指定的内接矩形。

        """

        return self.choice_one_child(*self.geometry_tags)  # type: ignore

    @property
    def fill(
        self,
    ) -> Optional[
        CT_NoFillProperties | CT_SolidColorFillProperties | CT_GradientFillProperties | CT_BlipFillProperties | CT_PatternFillProperties | CT_GroupFillProperties
    ]:
        """填充"""

        return self.choice_one_child(*self.fill_pr_tags)  # type: ignore

    @property
    def line(self) -> Optional[CT_LineProperties]:
        """线"""

        return getattr(self, qn('a:ln'), None)

    @property
    def effect(self) -> Optional[CT_EffectList | CT_EffectContainer]:
        """效果"""

        return self.choice_one_child(*self.effect_pr_tags)  # type: ignore

    @property
    def scene_3d(self) -> Optional[CT_Scene3D]:
        """
        aaa
        """

        return getattr(self, qn('a:scene3d'), None)

    @property
    def shape_3d(self) -> Optional[CT_Shape3D]:
        """
        aaa
        """

        return getattr(self, qn('a:sp3d'), None)

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展属性"""

        return getattr(self, qn('a:extLst'), None)

    @property
    def bw_mode(self) -> Optional[ST_BlackWhiteMode]:
        """黑白模式

        指定仅使用黑白颜色渲染图片。 即渲染图片时应将图片的颜色信息转换为黑色或白色.

        渲染该图像时不使用灰色，仅使用纯黑和纯白.

        [Note: 这并不意味着存储在文件中的图片本身一定是黑白图片。 该属性设置渲染时图片所应用的渲染模式. end note]
        """

        val = self.attrib.get('bwMode')

        if val is not None:
            return ST_BlackWhiteMode(val)

        return None


class CT_GroupShapeProperties(EG_FillProperties, EG_EffectProperties):
    """组合图形属性

    19.3.1.23 grpSpPr

    该元素指定相应组内所有形状所共有的属性。 如果组形状属性和单个形状属性之间存在任何冲突属性，则应优先考虑单个形状属性。
    """

    @property
    def xfrm(self) -> Optional[CT_GroupTransform2D]:
        """图形框架的 2D 变换

        19.3.1.53 xfrm

        该元素指定要应用于相应图形框架的变换。 此变换应用于图形框架，就像应用于形状或组形状一样。
        """

        return getattr(self, qn('a:xfrm'), None)

    @property
    def fill(
        self,
    ) -> Optional[
        CT_NoFillProperties | CT_SolidColorFillProperties | CT_GradientFillProperties | CT_BlipFillProperties | CT_PatternFillProperties | CT_GroupFillProperties
    ]:
        """填充"""

        return self.choice_one_child(*self.fill_pr_tags)  # type: ignore

    @property
    def effect(self) -> Optional[CT_EffectList | CT_EffectContainer]:
        """效果"""

        return self.choice_one_child(self.effect_pr_tags)  # type: ignore

    @property
    def scene_3d(self) -> Optional[CT_Scene3D]:
        """
        aaa
        """

        return getattr(self, qn('a:scene3d'), None)

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """
        aaa
        """

        return getattr(self, qn('a:extLst'), None)

    @property
    def bw_mode(self) -> Optional[ST_BlackWhiteMode]:
        """黑白模式

        指定应仅使用黑色和白色来渲染组形状。 也就是说，在渲染相应形状时，组形状的颜色信息应转换为黑色或白色.

        [Note: 这并不意味着组形状本身仅存储有黑白颜色信息。 该属性设置形状在渲染时使用的渲染模式。 end note]
        """

        val = self.attrib.get('bwMode')

        if val is not None:
            return ST_BlackWhiteMode(val)

        return None


class CT_StyleMatrixReference(EG_ColorChoice):
    """背景样式参考

    19.3.1.3 bgRef

    该元素指定幻灯片背景使用样式矩阵中定义的填充样式。

    idx 属性指的是背景填充样式或演示文稿样式矩阵中的填充样式的索引，由 fmtScheme 元素定义。

    值 0 或 1000 表示无背景，值 1-999 指 fillStyleLst 元素内的填充样式的索引，

    值 1001 及以上指 bgFillStyleLst 元素内的背景填充样式的索引。

    值 1001 对应于第一个背景填充样式，1002 对应于第二个背景填充样式，依此类推。
    """

    @property
    def color(
        self,
    ) -> Optional[
        CT_ScRgbColor | CT_SRgbColor | CT_HslColor | CT_SystemColor | CT_SchemeColor | CT_PresetColor
    ]:
        """颜色

        <xsd:group ref="EG_ColorChoice" minOccurs="0" maxOccurs="1"/>
        """

        return self.choice_one_child(*self.color_tags)  # type: ignore

    @property
    def idx(self) -> ST_StyleMatrixColumnIndex:
        """样式矩阵索引

        指定所引用样式的样式矩阵索引.

        idx 属性指的是背景填充样式或演示文稿样式矩阵中的填充样式的索引，由 fmtScheme 元素定义。

        值 0 或 1000 表示无背景，值 1-999 指 fillStyleLst 元素内的填充样式的索引，

        值 1001 及以上指 bgFillStyleLst 元素内的背景填充样式的索引。

        值 1001 对应于第一个背景填充样式，1002 对应于第二个背景填充样式，依此类推。
        """

        return ST_StyleMatrixColumnIndex(int(self.attrib['idx']))


class CT_FontReference(EG_ColorChoice):
    """字体引用

    20.1.4.1.17 fontRe

    该元素表示对主题字体的引用。 使用时，它指定要使用的主题字体以及颜色选择。
    """

    @property
    def color(
        self,
    ) -> Optional[
        CT_ScRgbColor | CT_SRgbColor | CT_HslColor | CT_SystemColor | CT_SchemeColor | CT_PresetColor
    ]:
        """颜色

        <xsd:group ref="EG_ColorChoice" minOccurs="0" maxOccurs="1"/>
        """

        return self.choice_one_child(*self.color_tags)  # type: ignore

    @property
    def idx(self) -> ST_FontCollectionIndex:
        """字体索引

        20.1.10.25 ST_FontCollectionIndex

        这个简单类型表示与样式相关联的字体之一。

        这个简单类型的内容是对 W3C XML Schema token 数据类型的限制。

        这个简单类型限制为以下表格中列出的值:

        - major（主要字体）: 样式字体方案的主要字体。
        - minor（次要字体）: 样式字体方案的次要字体。
        - none（无）: 没有字体引用。
        """

        return ST_FontCollectionIndex(self.attrib['idx'])


class CT_ShapeStyle(OxmlBaseElement):
    """形状样式

    19.3.1.46 style

    该元素指定形状的样式信息。 这用于根据主题的样式矩阵定义的预设样式来定义形状的外观。
    """

    @property
    def line_ref(self) -> CT_StyleMatrixReference:
        """轮廓样式引用

        20.1.4.2.19 lnRef

        此元素定义对样式矩阵内的线条样式的引用。 idx 属性引用 fillStyleLst 元素中线条(轮廓)样式的索引。
        """

        return getattr(self, qn('a:lnRef'))

    @property
    def fill_ref(self) -> CT_StyleMatrixReference:
        """填充样式引用

        20.1.4.2.10 fillRef

        该元素定义对样式矩阵内的填充样式的引用。 idx 属性指的是演示文稿样式矩阵中填充样式或背景填充样式的索引，由 fmtScheme 元素定义。

        值 0 或 1000 表示无背景，值 1-999 指 fillStyleLst 元素内的填充样式的索引，

        值 1001 及以上指 bgFillStyleLst 元素内的背景填充样式的索引。

        值 1001 对应于第一个背景填充样式，1002 对应于第二个背景填充样式，依此类推。
        """

        return getattr(self, qn('a:fillRef'))

    @property
    def effect_ref(self) -> CT_StyleMatrixReference:
        """效果样式引用

        20.1.4.2.8 effectRef

        该元素定义对样式矩阵中效果样式的引用。 idx 属性指的是effectStyleLst 元素中效果样式的索引。
        """

        return getattr(self, qn('a:effectRef'))

    @property
    def font_ref(self) -> CT_FontReference:
        """字体样式引用

        20.1.4.1.17 fontRef

        该元素表示对主题字体的引用。 使用时，它指定要使用的主题字体以及颜色选择。
        """

        return getattr(self, qn('a:fontRef'))


class CT_DefaultShapeDefinition(OxmlBaseElement):
    """默认样式定义

    20.1.4.1.27 spDef 形状默认样式

    此元素定义与默认形状关联的格式。 当形状最初插入到文档中时，可以将默认格式应用于形状。

    20.1.4.1.20 lnDef 线条默认样式

    该元素定义文档中使用的默认线条样式。

    20.1.4.1.28 txDef 文本默认样式

    此元素定义默认应用于文档中文本的默认格式。 当形状最初插入文档时，可以而且应该将默认格式应用于形状.
    """

    @property
    def shape_properties(self) -> CT_ShapeProperties:
        """形状特性(属性)

        20.1.2.2.35 spPr

        该元素指定可应用于形状的视觉形状特性.
        """

        return getattr(self, qn('a:spPr'))

    @property
    def body_properties(self) -> CT_TextBodyProperties:
        """此元素定义形状内文本正文的正文属性。

        21.1.2.1.1 bodyPr

        此元素定义形状内文本正文的正文属性。
        """

        return getattr(self, qn('a:bodyPr'))

    @property
    def text_list_style(self) -> CT_TextListStyle:
        """文本列表样式

        21.1.2.4.12 lstStyle

        此元素指定与此文本正文关联的样式列表。
        """

        return getattr(self, qn('a:lstStyle'))

    @property
    def shape_style(self) -> Optional[CT_ShapeStyle]:
        """形状样式

        20.1.2.2.37 style

        该元素指定形状的样式信息.
        """

        return getattr(self, qn('a:style'), None)

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)


class CT_ObjectStyleDefaults(OxmlBaseElement):
    """对象默认特性

    20.1.6.7 objectDefaults

    该元素允许定义默认形状、线条和文本框格式的特性。
    应用程序可以在插入文档时使用此信息来格式化形状（或文本）。
    """

    @property
    def shape_def(self) -> Optional[CT_DefaultShapeDefinition]:
        """形状默认样式

        20.1.4.1.27 spDef

        此元素定义与默认形状关联的格式。 当形状最初插入到文档中时，可以将默认格式应用于形状。
        """

        return getattr(self, qn('a:spDef'), None)

    @property
    def line_def(self) -> Optional[CT_DefaultShapeDefinition]:
        """线条默认样式

        20.1.4.1.20 lnDef

        该元素定义文档中使用的默认线条样式。
        """

        return getattr(self, qn('a:lnDef'), None)

    @property
    def text_def(self) -> Optional[CT_DefaultShapeDefinition]:
        """文本默认样式

        20.1.4.1.28 txDef

        此元素定义默认应用于文档中文本的默认格式。 当形状最初插入文档时，可以而且应该将默认格式应用于形状.
        """

        return getattr(self, qn('a:txDef'), None)

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'))


class CT_EmptyElement(OxmlBaseElement):
    """空元素

    20.1.6.6 masterClrMapping 母板颜色映射

        该元素是在文档中使用颜色映射的选择的一部分。
        还定义了 overrideClrMapping (§20.1.6.8) 元素，当指定该元素时，将使用覆盖而不是主文件中定义的颜色映射。
        如果指定了该元素，那么我们将专门使用 master.xml 中定义的颜色映射。

    """



class CT_ColorMapping(OxmlBaseElement):
    """颜色映射

    20.1.6.8 overrideClrMapping

        此元素提供文档中颜色映射的覆盖。 定义后，此颜色映射将用于代替已定义的颜色映射或主颜色映射。 此颜色映射的定义方式与本文档中的其他映射相同。

    19.3.1.6 clrMap

        此元素指定将一种颜色方案定义转换为另一种颜色方案定义的映射层。 每个属性代表一个在这个master中可以引用的颜色名称，其值为主题中对应的颜色。

    20.1.6.1 clrMap

        该元素指定颜色映射层，允许用户定义背景和文本的颜色。 这允许交换背景和背景顶部文本的浅色/深色，以保持文本的可读性。 在更深层次上，这准确指定了配色方案中前 12 个值引用的颜色。
    """

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展数据"""

        return getattr(self, qn('a:extLst'), None)

    @property
    def bg1(self) -> ST_ColorSchemeIndex:
        """背景色 1

        指定与背景色 1 关联的颜色定义.
        """

        return ST_ColorSchemeIndex(self.attrib['bg1'])

    @property
    def tx1(self) -> ST_ColorSchemeIndex:
        """文本 1

        指定与第一个文本颜色关联的颜色定义.
        """

        return ST_ColorSchemeIndex(self.attrib['tx1'])

    @property
    def bg2(self) -> ST_ColorSchemeIndex:
        """背景色 2

        指定与背景色 2 关联的颜色定义.
        """

        return ST_ColorSchemeIndex(self.attrib['bg2'])

    @property
    def tx2(self) -> ST_ColorSchemeIndex:
        """文本 2

        指定与第二个文本颜色关联的定义颜色.
        """

        return ST_ColorSchemeIndex(self.attrib['tx2'])

    @property
    def accent1(self) -> ST_ColorSchemeIndex:
        """强调色 1

        指定与强调色 1 关联的颜色定义.
        """

        return ST_ColorSchemeIndex(self.attrib['accent1'])

    @property
    def accent2(self) -> ST_ColorSchemeIndex:
        """强调色 2

        指定与强调色 2 关联的颜色定义.
        """

        return ST_ColorSchemeIndex(self.attrib['accent2'])

    @property
    def accent3(self) -> ST_ColorSchemeIndex:
        """强调色 3

        指定与强调色 3 关联的颜色定义.
        """

        return ST_ColorSchemeIndex(self.attrib['accent3'])

    @property
    def accent4(self) -> ST_ColorSchemeIndex:
        """强调色 4

        指定与强调色 4 关联的颜色定义.
        """

        return ST_ColorSchemeIndex(self.attrib['accent4'])

    @property
    def accent5(self) -> ST_ColorSchemeIndex:
        """强调色 5

        指定与强调色 5 关联的颜色定义.
        """

        return ST_ColorSchemeIndex(self.attrib['accent5'])

    @property
    def accent6(self) -> ST_ColorSchemeIndex:
        """强调色 6

        指定与强调色 1 关联的颜色定义.
        """

        return ST_ColorSchemeIndex(self.attrib['accent6'])

    @property
    def hlink(self) -> ST_ColorSchemeIndex:
        """超链接颜色

        指定与超链接颜色关联的颜色定义.
        """

        return ST_ColorSchemeIndex(self.attrib['hlink'])

    @property
    def folHlink(self) -> ST_ColorSchemeIndex:
        """已关注超链接颜色

        指定定义的颜色，该颜色与已关注超链接的颜色相关联.
        """

        return ST_ColorSchemeIndex(self.attrib['folHlink'])


class CT_ColorMappingOverride(OxmlBaseElement):
    """颜色映射覆盖值

    19.3.1.7 clrMapOvr

    该元素提供了一种机制，用于覆盖 ClrMap 元素中列出的颜色方案。

    如果 masterClrMapping 元素存在，则使用 master 定义的配色方案。

    如果 overrideClrMapping 元素存在，它将定义特定于父笔记幻灯片、演示文稿幻灯片或幻灯片布局的新配色方案。
    """

    @property
    def color_mapping(self) -> CT_EmptyElement | CT_ColorMapping:
        """颜色映射方案

        该元素提供了一种机制，用于覆盖 ClrMap 元素中列出的颜色方案。

        如果 masterClrMapping 元素存在，则使用 master 定义的配色方案。

        如果 overrideClrMapping 元素存在，它将定义特定于父笔记幻灯片、演示文稿幻灯片或幻灯片布局的新配色方案。
        """

        tags = (
            qn('a:masterClrMapping'),  # CT_EmptyElement
            qn('a:overrideClrMapping'),  # CT_ColorMapping
        )

        return self.choice_require_one_child(*tags)  # type: ignore


class CT_ColorSchemeAndMapping(OxmlBaseElement):
    """额外的配色方案

    20.1.6.4 extraClrScheme

    该元素定义了辅助配色方案，其中包括配色方案和颜色映射。 这主要用于向后兼容性问题和早期版本所需的往返信息。
    """

    @property
    def color_schema(self) -> CT_ColorScheme:
        """颜色方案

        20.1.6.2 clrScheme

        该元素定义了一组颜色，称为配色方案。 配色方案负责定义十二种颜色的列表。 这十二种颜色包括六种强调色、两种深色、两种浅色以及每个超链接和已关注超链接的颜色。

        配色方案颜色元素按顺序出现。 以下列表显示了索引值和相应的颜色名称。

        - 0: dk1 (暗色 1)
        - 1: lt1 (亮色 1)
        - 2: dk2 (暗色 2)
        - 3: lt2 (亮色 2)
        - 4: accent1 (强调色 1)
        - 5: accent2 (强调色 2)
        - 6: accent3 (强调色 3)
        - 7: accent4 (强调色 4)
        - 8: accent5 (强调色 5)
        - 9: accent6 (强调色 6)
        - 10: hlink (超链接)
        - 11: folHlink (已关注超链接)
        """

        return getattr(self, qn('a:clrScheme'))

    @property
    def color_map(self) -> Optional[CT_ColorMapping]:
        """颜色映射

        20.1.6.1 clrMap

        该元素指定颜色映射层，允许用户定义背景和文本的颜色。 这允许交换背景和背景顶部文本的浅色/深色，以保持文本的可读性。 在更深层次上，这准确指定了配色方案中前 12 个值引用的颜色。
        """

        return getattr(self, qn('a:clrMap'), None)


class CT_ColorSchemeList(OxmlBaseElement):
    """额外配色方案列表

    20.1.6.5 extraClrSchemeLst

    该元素是文档中存在的额外配色方案列表的容器.
    """

    @property
    def extra_color_scheme_lst(self) -> list[CT_ColorSchemeAndMapping]:
        """额外的配色方案

        20.1.6.4 extraClrScheme

        该元素定义了辅助配色方案，其中包括配色方案和颜色映射。 这主要用于向后兼容性问题和早期版本所需的往返信息。
        """

        return self.findall(qn('a:extraClrScheme'))  # type: ignore


class CT_OfficeStyleSheet(OxmlBaseElement):
    """基本样式(样式表)

    20.1.6.9 theme

    主题部件的根  theme 元素的类型

    该元素定义与共享样式表（或主题）关联的根级复杂类型。
    该元素通过主题保存文档可用的所有不同格式选项，并定义在文档中使用主题对象时文档的整体外观和感觉。
    """

    @property
    def theme_elements(self) -> CT_BaseStyles:
        """主题元素集

        20.1.6.10 themeElements

        元素定义主题的主题格式选项，并且是主题的主力。 这是文档包含和使用大部分共享主题信息的地方。

        此元素包含颜色方案、字体方案和格式方案元素，它们定义主题定义的不同格式方面。
        """

        return getattr(self, qn('a:themeElements'))

    @property
    def object_defaults(self) -> Optional[CT_ObjectStyleDefaults]:
        """对象默认样式

        20.1.6.7 objectDefaults

        该元素允许定义默认形状、线条和文本框格式属性。 应用程序可以在插入文档时使用此信息来格式化形状（或文本）。

        [Note: 该元素内容模型 (CT_ObjectStyleDefaults) 的 W3C XML 架构定义位于 §A.4.1 中。 end note]
        """

        return getattr(self, qn('a:objectDefaults'), None)

    @property
    def extra_color_scheme_lst(self) -> Optional[CT_ColorSchemeList]:
        """额外的颜色方案列表

        20.1.6.5 extraClrSchemeLst

        该元素是文档中存在的额外配色方案列表的容器.

        [Note: 该元素内容模型 (CT_ColorSchemeList) 的 W3C XML 架构定义位于 §A.4.1. end note]
        """

        return getattr(self, qn('a:extraClrSchemeLst'), None)

    @property
    def cust_color_lst(self) -> Optional[CT_CustomColorList]:
        """自定义颜色列表

        20.1.6.3 custClrLst

        该元素允许创建自定义调色板，并与其他配色方案一起显示。 例如，当有人想要维护公司调色板时，这可能非常有用。
        """

        return getattr(self, qn('a:custClrLst'), None)

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)

    @property
    def name(self) -> str:
        """名称

        默认值为: ''
        """

        val = self.attrib.get('name')

        if val is None:
            return ''

        return utils.AnyStrToStr(val)  # type: ignore


class CT_BaseStylesOverride(OxmlBaseElement):
    """基本样式覆盖

    主题覆盖部件的 themeOverride 根元素 的 类型
    主题覆盖部件的 themeOverride 根元素 的 类型
    """

    @property
    def color_schema(self) -> Optional[CT_ColorScheme]:
        """颜色方案"""

        return getattr(self, qn('a:clrScheme'), None)

    @property
    def font_scheme(self) -> Optional[CT_FontScheme]:
        """字体方案"""

        return getattr(self, qn('a:fontScheme'), None)

    @property
    def format_scheme(self) -> Optional[CT_StyleMatrix]:
        """格式方案(样式矩阵)"""

        return getattr(self, qn('a:fmtScheme'), None)


class CT_ClipboardStyleSheet(OxmlBaseElement):
    """剪贴板样式表"""

    @property
    def theme_elements(self) -> CT_BaseStyles:
        """主题元素"""

        return getattr(self, qn('a:themeElements'))

    @property
    def color_map(self) -> CT_ColorMapping:
        """颜色映射"""

        return getattr(self, qn('a:clrMap'))


class CT_TableCellProperties(EG_FillProperties):
    """单元格属性

    21.1.3.17 tcPr

    该元素定义与单元格关联的格式属性。 可调整的格式选项范围从用于边框的线型到单元格填充，再到与单元格中文本布局相关的边距。
    """

    @property
    def line_left(self) -> Optional[CT_LineProperties]:
        """左边框线属性

        21.1.3.7 lnL

        该元素定义与单元格左边框关联的线条属性
        """

        return getattr(self, qn('a:lnL'), None)

    @property
    def line_right(self) -> Optional[CT_LineProperties]:
        """右边框线属性

        21.1.3.8 lnR

        该元素定义与单元格右边框相关的线条属性。
        """

        return getattr(self, qn('a:lnR'), None)

    @property
    def line_top(self) -> Optional[CT_LineProperties]:
        """顶部边框线属性

        21.1.3.9 lnT

        该元素定义与单元格上边框关联的线条属性。
        """

        return getattr(self, qn('a:lnT'), None)

    @property
    def line_bottom(self) -> Optional[CT_LineProperties]:
        """底部边框线属性

        21.1.3.5 lnB

        该元素定义与给定单元格的下边框关联的线条属性。
        """

        return getattr(self, qn('a:lnB'), None)

    @property
    def line_tltobr(self) -> Optional[CT_LineProperties]:
        """左上角到右下角边框线属性

        21.1.3.10 lnTlToBr

        此元素定义与从单元格左上角到右下角的对角线关联的线条属性。
        """

        return getattr(self, qn('a:lnTlToBr'), None)

    @property
    def line_bltotr(self) -> Optional[CT_LineProperties]:
        """左下角到右上角的边框线属性

        21.1.3.6 lnBlToTr

        此元素定义与从单元格左下角到右上角的对角线关联的线条属性。
        """

        return getattr(self, qn('a:lnBlToTr'), None)

    @property
    def cell_3d(self) -> Optional[CT_Cell3D]:
        """单元格 3-D

        21.1.3.1 cell3D

        该元素指定一组属性，这些属性决定表中给定单元格的 3D 外观。 这些属性统称为单元 3-D。 这些属性的应用发生在表中的 percell 基础上。
        """

        return getattr(self, qn('a:cell3D'))

    @property
    def fill(
        self,
    ) -> Optional[
        CT_NoFillProperties | CT_SolidColorFillProperties | CT_GradientFillProperties | CT_BlipFillProperties | CT_PatternFillProperties | CT_GroupFillProperties
    ]:
        """
        填充样式
        """

        return self.choice_one_child(*self.fill_pr_tags)  # type: ignore

    @property
    def headers(self) -> Optional[CT_Headers]:
        """与表格单元关联的标题单元

        21.1.3.4 headers

        此元素指定标题单元格列表（由子标题元素指定），这些单元格提供与当前表格单元格关联的标题信息。 每个标题单元格应指定一个唯一标识符，如使用标题单元格 tc 元素上的属性 id 所指定的那样。 该元素通常用于收集有关数据和子标题单元格的标题信息。

        如果省略此元素或不存在子标题元素，则标题单元格不应与给定的表格单元格关联.
        """

        return getattr(self, qn('a:headers'), None)

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """
        aaa
        """

        return getattr(self, qn('a:extLst'), None)

    @property
    def margin_left(self) -> ST_Coordinate32:
        """左边距

        Left Margin

        该属性指定单元格的左边距。 此属性中指定的值是从 EMU 中单元格左侧偏移的距离。
        """

        val = self.attrib.get('marL')

        if val is None:
            val = '91440'

        return to_ST_Coordinate32(val)  # type: ignore

    @property
    def margin_right(self) -> ST_Coordinate32:
        """
        aaa
        """

        val = self.attrib.get('marR')

        if val is None:
            val = '91440'

        return to_ST_Coordinate32(val)  # type: ignore

    @property
    def margin_top(self) -> ST_Coordinate32:
        """上边距

        Top Margin

        该属性指定单元格的上边距。 此属性中指定的值是距 EMU 单元格顶部的偏移距离。
        """

        val = self.attrib.get('marT')

        if val is None:
            val = '45720'

        return to_ST_Coordinate32(val)  # type: ignore

    @property
    def margin_bottom(self) -> ST_Coordinate32:
        """下边距

        Bottom Margin

        指定单元格的下边距。 该属性中指定的值是距单元格底部的偏移距离。
        """

        val = self.attrib.get('marB')

        if val is None:
            val = '45720'

        return to_ST_Coordinate32(val)  # type: ignore

    @property
    def vert(self) -> ST_TextVerticalType:
        """文字方向

        Text Direction

        定义单元格内的文本方向。
        """

        val = self.attrib.get('vert')

        if val is None:
            return ST_TextVerticalType.Horz

        return ST_TextVerticalType(val)

    @property
    def anchor(self) -> ST_TextAnchoringType:
        """锚

        Anchor

        定义单元格内文本的垂直对齐方式。
        """

        val = self.attrib.get('anchor')

        if val is None:
            return ST_TextAnchoringType.Top

        return ST_TextAnchoringType(val)

    @property
    def anchor_ctr(self) -> bool:
        """锚定中心

        Anchor Center

        当此属性为 1 或 true 时，它会修改锚属性。 该属性使文本框本身居中对齐，例如允许文本沿单元格的中心左对齐。
        """

        val = self.attrib.get('anchor')

        return utils.XsdBool(val, none=False)

    @property
    def horz_overflow(self) -> ST_TextHorzOverflowType:
        """水平溢出

        Horizontal Overflow

        指定单元格的剪切行为。 这里的两个选项允许文本在单元格边界之外时被剪切并在视图之外，或者允许文本保持可见并溢出到单元格之外。

        如果省略该元素，则该表单元格没有唯一标识符。
        """
        val = self.attrib.get('horzOverflow')

        if val is None:
            return ST_TextHorzOverflowType.Clip

        return ST_TextHorzOverflowType(val)


class CT_Headers(OxmlBaseElement):
    """
    aaa

    <xsd:complexType name="CT_Headers">
        <xsd:sequence minOccurs="0" maxOccurs="unbounded">
            <xsd:element name="header" type="xsd:string"/>
        </xsd:sequence>
    </xsd:complexType>
    """

    @property
    def headers(self) -> list[CT_Header]:
        """
        aaa
        """

        return self.findall(qn('a:header'))  # type: ignore


# <xsd:element name="header" type="xsd:string"/>
CT_Header = OxmlBaseElement


class CT_TableCol(OxmlBaseElement):
    """表格网格列

    21.1.3.2 gridCol

    该元素指定表中给定列的宽度。 对于表中的每一列，都有一个关联的表网格列定义列的宽度。
    """

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)

    @property
    def width(self) -> ST_Coordinate:
        """宽度

        Width

        列的宽度(EMU单位).
        """

        val = self.attrib['w']

        return to_ST_Coordinate(str(val))


class CT_TableGrid(OxmlBaseElement):
    """表格网格

    21.1.3.14 tblGrid

    此元素定义表列 (§21.1.3.2) 元素的列表。 表中的每一列都应该有一个表列 (§21.1.3.2) 元素。
    """

    @property
    def grid_col(self) -> list[CT_TableCol]:
        """表格网格列

        21.1.3.2 gridCol

        该元素指定表中给定列的宽度。 对于表中的每一列，都有一个关联的表网格列定义列的宽度。
        """

        return self.findall(qn('a:gridCol'))  # type: ignore


class CT_TableCell(OxmlBaseElement):
    """表格单元格

    21.1.3.16 tc

    该元素定义表内的一个单元格。 表格单元格包含一个文本正文，该文本正文实际上包含单元格内保存的数据以及表格单元格的属性，这些属性包含与单元格关联的格式选项。
    """

    @property
    def text_body(self) -> Optional[CT_TextBody]:
        """文本主体

        20.1.2.2.40 txBody

        该元素指定相应形状中是否存在要包含的文本。 所有可见文本和可见文本相关属性都包含在此元素内。 可以有多个段落，段落内可以有多个文本段.
        """

        return getattr(self, qn('a:txBody'), None)

    @property
    def cell_properties(self) -> Optional[CT_TableCellProperties]:
        """单元格属性

        21.1.3.17 tcPr

        该元素定义与单元格关联的格式属性。 可调整的格式选项范围从用于边框的线型到单元格填充，再到与单元格中文本布局相关的边距。
        """

        return getattr(self, qn('a:tcPr'), None)

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展元素"""

        return getattr(self, qn('a:extLst'), None)

    @property
    def row_span(self) -> int:
        """行跨度

        定合并单元格跨越的行数。 它与其他单元格上的 vMerge 属性结合使用，以指定水平合并的起始单元格。
        """

        val = self.attrib.get('rowSpan')

        if val is None:
            return 1

        return int(utils.AnyStrToStr(val))  # type: ignore

    @property
    def grid_span(self) -> int:
        """网格跨度

        指定合并单元格跨越的列数。 它与其他单元格上的 hMerge 属性结合使用，以指定水平合并的起始单元格。
        """

        val = self.attrib.get('gridSpan')

        if val is None:
            return 1

        return int(utils.AnyStrToStr(val))  # type: ignore

    @property
    def h_merge(self) -> XSD_Boolean:
        """水平合并 Horizontal Merge

        当此属性设置为1或true时，表格在创建时将合并此单元格与前一个水平单元格。
        """

        val = self.attrib.get('hMerge')

        return to_xsd_bool(val, none=False)

    @property
    def v_merge(self) -> XSD_Boolean:
        """垂直合并

        当此属性设置为 1 或 true 时，创建表格时此表格单元格将与前一个垂直表格单元格合并。
        """

        val = self.attrib.get('vMerge')

        return to_xsd_bool(val, none=False)

    @property
    def id(self) -> Optional[str]:
        """单元格标识符

        Table Cell Identifier
        """

        val = self.attrib.get('vMerge')

        if val is not None:
            return utils.AnyStrToStr(val)  # type: ignore

        return val


class CT_TableRow(OxmlBaseElement):
    """21.1.3.18 tr

    表格行

    该元素定义表中的一行。 表中定义的行只是表单元格的列表（第 21.1.3.16 节）。 为表中的每一行定义了一个表行元素。
    """

    @property
    def table_cells(self) -> list[CT_TableCell]:
        """21.1.3.16 tc

        该元素定义表内的一个单元格。 表格单元格包含一个文本正文，该文本正文实际上包含单元格内保存的数据以及表格单元格的属性，这些属性包含与单元格关联的格式选项。
        """

        return self.findall(qn('a:tc'))  # type: ignore

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)

    @property
    def height(self) -> ST_Coordinate:
        """高度

        定义表中行的高度。
        """

        return to_ST_Coordinate(str(self.attrib['h']))


class CT_TableProperties(EG_FillProperties, EG_EffectProperties):
    """21.1.3.15 tblPr

    表格属性

    该元素定义了整个表的属性。 该元素内有许多可应用于表格的视觉修改。
    """

    @property
    def fill(
        self,
    ) -> Optional[
        CT_NoFillProperties | CT_SolidColorFillProperties | CT_GradientFillProperties | CT_BlipFillProperties | CT_PatternFillProperties | CT_GroupFillProperties
    ]:
        """
        填充样式
        """
        return self.choice_one_child(*self.fill_pr_tags)  # type: ignore

    @property
    def effect(self) -> Optional[CT_EffectList | CT_EffectContainer]:
        """
        效果样式
        """
        return self.choice_one_child(*self.effect_pr_tags)  # type: ignore

    @property
    def style(self) -> Optional[CT_TableStyle | OxmlBaseElement]:
        """表格样式

        自定义或引用
        """

        tags = (
            qn('a:tableStyle'),  # CT_TableStyle
            qn('a:tableStyleId'),  # s_ST_Guid -> str -> OxmlBaseElement
        )

        return self.choice_one_child(*tags)  # type: ignore

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)

    @property
    def rtl(self) -> XSD_Boolean:
        """右到左

        Right-to-Left

        定义启用表格的从右到左设置。 如果 rtl 的值为 1 或 true ，则表格从右到左排列，而不是默认的从左到右排列。
        """
        val = self.attrib.get('rtl')

        return to_xsd_bool(val, none=False)

    @property
    def first_row(self) -> XSD_Boolean:
        """第一行

        First Row

        启用或禁用表格样式的第一行格式。 值 1 或 true 启用表样式中定义的第一行格式。 如果未指定，该属性默认为 false。
        """
        val = self.attrib.get('firstRow')

        return to_xsd_bool(val, none=False)

    @property
    def first_col(self) -> XSD_Boolean:
        """第一列

        First Column

        启用或禁用表格样式的第一列格式。 值 1 或 true 启用表样式中定义的第一列格式。 如果未指定，该属性默认为 false。
        """
        val = self.attrib.get('firstCol')

        return to_xsd_bool(val, none=False)

    @property
    def last_row(self) -> XSD_Boolean:
        """最后一行

        Last Row

        启用或禁用表格样式的最后一行格式。 值 1 或 true 启用表样式中定义的最后一行格式。 如果未指定，该属性默认为 false。
        """
        val = self.attrib.get('lastRow')

        return to_xsd_bool(val, none=False)

    @property
    def last_col(self) -> XSD_Boolean:
        """最后一列

        Last Column

        启用或禁用表格样式的最后一列格式。 值 1 或 true 启用表样式中定义的最后一个列格式。 如果未指定，该属性默认为 false。
        """
        val = self.attrib.get('lastCol')

        return to_xsd_bool(val, none=False)

    @property
    def band_row(self) -> XSD_Boolean:
        """带状行

        Banded Rows

        启用或禁用表格样式的带状行格式。 值 1 或 true 启用表格样式中定义的带状行格式。 如果未指定，该属性默认为 false。
        """
        val = self.attrib.get('bandRow')

        return to_xsd_bool(val, none=False)

    @property
    def band_col(self) -> XSD_Boolean:
        """带状列

        Banded Columns

        启用或禁用表格样式的带状列格式。 值 1 或 true 启用表格样式中定义的带状列格式。 如果未指定，该属性默认为关闭。
        """
        val = self.attrib.get('bandCol')

        return to_xsd_bool(val, none=False)


class CT_Table(OxmlBaseElement):
    """21.1.3.13 tbl

    该元素是表的根元素。 该元素包含在 DrawingML 中定义表格所需的所有内容。
    """

    @property
    def table_properties(self) -> Optional[CT_TableProperties]:
        """21.1.3.15 tblPr

        表格属性

        该元素定义了整个表的属性。 该元素内有许多可应用于表格的视觉修改。
        """
        return getattr(self, qn('a:tblPr'), None)

    @property
    def table_grid(self) -> CT_TableGrid:
        """表格网格

        21.1.3.14 tblGrid

        此元素定义表列 (§21.1.3.2) 元素的列表。 表中的每一列都应该有一个表列 (§21.1.3.2) 元素。
        """
        return getattr(self, qn('a:tblGrid'))

    @property
    def table_row_lst(self) -> list[CT_TableRow]:
        """21.1.3.18 tr

        表格行

        该元素定义表中的一行。 表中定义的行只是表单元格的列表（第 21.1.3.16 节）。 为表中的每一行定义了一个表行元素。
        """
        return self.findall(qn('a:tr'))  # type: ignore


class CT_Cell3D(OxmlBaseElement):
    """单元格 3-D

    21.1.3.1 cell3D

    该元素指定一组属性，这些属性决定表中给定单元格的 3D 外观。 这些属性统称为单元 3-D。 这些属性的应用发生在表中的 percell 基础上。
    """

    @property
    def bevel(self) -> CT_Bevel:
        """
        aaa
        """

        return getattr(self, qn('a:bevel'))

    @property
    def light_rig(self) -> Optional[CT_LightRig]:
        """
        aaa
        """

        return getattr(self, qn('lightRig'), None)

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """
        aaa
        """

        return getattr(self, qn('a:extLst'), None)

    @property
    def preset_material(self) -> ST_PresetMaterialType:
        """预设材质

        Preset Material

        指定用于定义单元材料特性的材料类型。 材料属性与场景的照明特性相结合，定义了单元 3D 外观的最终外观和感觉。
        """
        val = self.attrib.get('prstMaterial')

        if val is None:
            return ST_PresetMaterialType.plastic

        return ST_PresetMaterialType(val)


class EG_ThemeableFillStyle(OxmlBaseElement):
    """主题填充样式"""

    themeable_fill_style_tags = (
        qn('a:fill'),  # CT_FillProperties
        qn('a:fillRef'),  # CT_StyleMatrixReference
    )

    @property
    def themeable_fill_style(
        self,
    ) -> Optional[CT_FillProperties | CT_StyleMatrixReference]:
        """主题填充样式"""

        return self.choice_one_child(*self.themeable_fill_style_tags)  # type: ignore


class CT_ThemeableLineStyle(OxmlBaseElement):
    """主题化的边框线条样式

    20.1.4.2.6 bottom (Bottom Border)

    此元素定义与表格单元格中的底部边框关联的线条属性。

    20.1.4.2.14 insideH (Inside Horizontal Border)

    此元素定义与表格中的内部水平边框关联的线条属性。

    20.1.4.2.15 insideV (Inside Vertical Border)

    此元素定义与表格中的内部垂直边框关联的线条属性。

    20.1.4.2.18 left (Left Border)

    此元素定义与表格单元格中的左边框关联的线条属性。

    20.1.4.2.22 right (Right Border)

    此元素定义与表格单元格中的右边框关联的线条属性。

    20.1.4.2.31 tl2br (Top Left to Bottom Right Border)

    此元素定义与表格单元格中从左上角到右下角的边框关联的线条属性。

    20.1.4.2.32 top (Top Border)

    此元素定义与表格单元格中的顶部边框关联的线条属性。

    20.1.4.2.33 tr2bl (Top Right to Bottom Left Border)

    此元素定义与表格单元格中从右上角到左下角的边框关联的线条属性。

    其他:

    <xsd:complexType name="CT_ThemeableLineStyle">
        <xsd:choice>
            <xsd:element name="ln" type="CT_LineProperties" minOccurs="1" maxOccurs="1" />
            <xsd:element name="lnRef" type="CT_StyleMatrixReference" minOccurs="1" maxOccurs="1" />
        </xsd:choice>
    </xsd:complexType>
    """

    def style(self) -> Optional[CT_LineProperties | CT_StyleMatrixReference]:
        """边框/线条样式"""

        tags = (
            qn('a:ln'),  # CT_LineProperties
            qn('a:lnRef'),  # CT_StyleMatrixReference
        )

        return self.choice_one_child(*tags)  # type: ignore


class EG_ThemeableEffectStyle(OxmlBaseElement):
    """
    <xsd:group name="EG_ThemeableEffectStyle">
        <xsd:choice>
            <xsd:element name="effect" type="CT_EffectProperties" minOccurs="1" maxOccurs="1"/>
            <xsd:element name="effectRef" type="CT_StyleMatrixReference" minOccurs="1" maxOccurs="1"/>
        </xsd:choice>
    </xsd:group>
    """

    themeable_effect_style_tags = (
        qn('a:effect'),  # CT_EffectProperties
        qn('a:effectRef'),  # CT_StyleMatrixReference
    )

    @property
    def themeable_effect_style(
        self,
    ) -> Optional[CT_EffectProperties | CT_StyleMatrixReference]:
        """主题i效果样式, 自定义或引用样式"""

        return self.choice_one_child(*self.themeable_effect_style_tags)  # type: ignore


class EG_ThemeableFontStyles(OxmlBaseElement):
    """
    <xsd:group name="EG_ThemeableFontStyles">
        <xsd:choice>
            <xsd:element name="font" type="CT_FontCollection" minOccurs="1" maxOccurs="1"/>
            <xsd:element name="fontRef" type="CT_FontReference" minOccurs="1" maxOccurs="1"/>
        </xsd:choice>
    </xsd:group>
    """

    themeable_font_style_tags = (
        qn('a:font'),  # CT_FontCollection
        qn('a:fontRef'),  # CT_FontReference
    )

    @property
    def themeable_font_style_element(
        self,
    ) -> Optional[CT_FontCollection | CT_FontReference]:
        """aaa"""

        return self.choice_one_child(*self.themeable_font_style_tags)  # type: ignore


class ST_OnOffStyleType(ST_BaseEnumType):
    """样式类型开关

    20.1.10.36 ST_OnOffStyleType

    这个简单类型表示是否应用样式属性。

    这个简单类型被限制为以下表格中列出的值:

    - def（默认）: 遵循父级设置。对于主题化属性，遵循主题设置。对于非主题化属性，遵循属性继承链中的父级设置。
    - off（关闭）: 属性被关闭。
    - on（打开）: 属性被打开。
    """

    On = 'on'
    """属性被打开。"""

    Off = 'off'
    """属性被关闭。"""

    Def = 'def'
    """遵循父级设置。对于主题化属性，遵循主题设置。对于非主题化属性，遵循属性继承链中的父级设置。"""


class CT_TableStyleTextStyle(EG_ThemeableFontStyles, EG_ColorChoice):
    """表格单元格文本样式

    20.1.4.2.30 tcTxStyle (Table Cell Text Style)

    该元素定义与表格单元格内包含的文本关联的文本属性。
    """

    @property
    def themeable_font_style(
        self,
    ) -> Optional[CT_FontCollection | CT_FontReference]:
        """主题化的字体样式, 自定义和字体合集/字体引用"""

        return self.choice_one_child(*self.themeable_font_style_tags)  # type: ignore

    @property
    def color(
        self,
    ) -> Optional[
        CT_ScRgbColor | CT_SRgbColor | CT_HslColor | CT_SystemColor | CT_SchemeColor | CT_PresetColor
    ]:
        """颜色

        <xsd:group ref="EG_ColorChoice" minOccurs="0" maxOccurs="1"/>
        """

        return self.choice_one_child(*self.color_tags)  # type: ignore

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        return getattr(self, qn('a:extLst'), None)

    @property
    def bold(self) -> ST_OnOffStyleType:
        """粗体

        Bold

        指定文本是否加粗。
        """

        val = self.attrib.get('b')

        if val is None:
            return ST_OnOffStyleType.Def

        return ST_OnOffStyleType(val)

    @property
    def italic(self) -> ST_OnOffStyleType:
        """斜体

        Italic

        指定文本是否为斜体。
        """

        val = self.attrib.get('i')

        if val is None:
            return ST_OnOffStyleType.Def

        return ST_OnOffStyleType(val)


class CT_TableCellBorderStyle(OxmlBaseElement):
    """单元格边框

    20.1.4.2.28 tcBdr

    该元素定义表格内单元格的边框。
    """

    @property
    def left(self) -> Optional[CT_ThemeableLineStyle]:
        """左边框

        20.1.4.2.18 left (Left Border)

        此元素定义与表格单元格中的左边框关联的线条属性。
        """
        return getattr(self, qn('a:left'), None)

    @property
    def right(self) -> Optional[CT_ThemeableLineStyle]:
        """右边框

        20.1.4.2.22 right (Right Border)

        此元素定义与表格单元格中的右边框关联的线条属性。
        """
        return getattr(self, qn('a:right'), None)

    @property
    def top(self) -> Optional[CT_ThemeableLineStyle]:
        """上边框

        20.1.4.2.32 top (Top Border)

        此元素定义与表格单元格中的顶部边框关联的线条属性。
        """
        return getattr(self, qn('a:top'), None)

    @property
    def bottom(self) -> Optional[CT_ThemeableLineStyle]:
        """下边框

        20.1.4.2.6 bottom (Bottom Border)

        此元素定义与表格单元格中的底部边框关联的线条属性。
        """
        return getattr(self, qn('a:bottom'), None)

    @property
    def insideH(self) -> Optional[CT_ThemeableLineStyle]:
        """内部水平边框

        20.1.4.2.14 insideH (Inside Horizontal Border)

        此元素定义与表格中的内部水平边框关联的线条属性。
        """
        return getattr(self, qn('a:insideH'), None)

    @property
    def insideV(self) -> Optional[CT_ThemeableLineStyle]:
        """内部垂直边框

        20.1.4.2.15 insideV (Inside Vertical Border)

        此元素定义与表格中的内部垂直边框关联的线条属性。
        """
        return getattr(self, qn('a:insideV'), None)

    @property
    def tl2br(self) -> Optional[CT_ThemeableLineStyle]:
        """从左上角到右下角的边框

        20.1.4.2.31 tl2br (Top Left to Bottom Right Border)

        此元素定义与表格单元格中从左上角到右下角的边框关联的线条属性。
        """
        return getattr(self, qn('a:tl2br'), None)

    @property
    def tr2bl(self) -> Optional[CT_ThemeableLineStyle]:
        """从右上角到左下角的边框

        20.1.4.2.33 tr2bl (Top Right to Bottom Left Border)

        此元素定义与表格单元格中从右上角到左下角的边框关联的线条属性。
        """
        return getattr(self, qn('a:tr2bl'), None)

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        return getattr(self, qn('a:extLst'), None)


class CT_TableBackgroundStyle(EG_ThemeableFillStyle, EG_ThemeableEffectStyle):
    """表格背景

    20.1.4.2.25 tblBg

    此元素定义可应用于表格背景形状的格式选项。 背景形状与整个表格的大小相同，并且可以容纳跨越整个表格的填充或效果。
    """

    @property
    def themeable_fill_style(
        self,
    ) -> Optional[CT_FillProperties | CT_StyleMatrixReference]:
        """主题填充样式属性/ 自定义填充样式"""
        return self.choice_one_child(*self.themeable_fill_style_tags)  # type: ignore

    @property
    def themeable_effect_style(
        self,
    ) -> Optional[CT_EffectProperties | CT_StyleMatrixReference]:
        """主题效果样式 / 自定义效果样式"""

        return self.choice_one_child(*self.themeable_effect_style_tags)  # type: ignore


class CT_TableStyleCellStyle(EG_ThemeableFillStyle):
    """单元格样式

    20.1.4.2.29 tcStyle

    该元素定义表格中给定单元格的样式。
    """

    @property
    def table_cell_border(self) -> Optional[CT_TableCellBorderStyle]:
        """单元格边框

        20.1.4.2.28 tcBdr

        该元素定义表格内单元格的边框。

        例如:

            <tcBdr>
                <left>
                    <lnRef idx="1">
                        <schemeClr val="accent1" />
                    </lnRef>
                </left>
                <right>
                    <lnRef idx="1">
                        <schemeClr val="accent1" />
                    </lnRef>
                </right>
                <top>
                    <lnRef idx="1">
                        <schemeClr val="accent1" />
                    </lnRef>
                </top>
                <bottom>
                    <lnRef idx="2">
                        <schemeClr val="lt1" />
                    </lnRef>
                </bottom>
                <insideH>
                    <ln>
                        <noFill />
                    </ln>
                </insideH>
                <insideV>
                    <ln>
                        <noFill />
                    </ln>
                </insideV>
            </tcBdr>

            定义了单元格的下、上、右、左边框.
        """
        return getattr(self, qn('a:tcBdr'), None)

    @property
    def themeable_fill_style(
        self,
    ) -> Optional[CT_FillProperties | CT_StyleMatrixReference]:
        """单元格填充样式, 自定义填充 / 样式引用"""

        return self.choice_one_child(*self.themeable_fill_style_tags)  # type: ignore

    @property
    def cell_3d(self) -> Optional[CT_Cell3D]:
        """单元格 3-D

        21.1.3.1 cell3D

        该元素指定一组属性，这些属性决定表中给定单元格的 3D 外观。 这些属性统称为单元 3-D。 这些属性的应用发生在表中的 percell 基础上。
        """
        return getattr(self, qn('a:cell3D'), None)


class CT_TablePartStyle(OxmlBaseElement):
    """整个表格样式

    20.1.4.2.34 wholeTbl

    此元素包含格式化选项，当表格处于默认状态且未启用格式化选项（第一行、最后一行等）时，这些选项将应用于整个表格。

    """

    @property
    def table_cell_text_style(self) -> Optional[CT_TableStyleTextStyle]:
        """单元格文本样式

        20.1.4.2.30 tcTxStyle

        该元素定义与表格单元格中包含的文本关联的文本属性.
        """
        return getattr(self, qn('a:tcTxStyle'), None)

    @property
    def table_cell_style(self) -> Optional[CT_TableStyleCellStyle]:
        """单元格样式

        20.1.4.2.29 tcStyle

        该元素定义表格中给定单元格的样式。
        """
        return getattr(self, qn('a:tcStyle'), None)


class CT_TableStyle(OxmlBaseElement):
    """表格样式

    21.1.3.11 tableStyle

    该元素指定特定的表格样式。 十四个元素组成了给定表格样式的样式信息。 这十四个元素协同工作，为以下切换的开/关状态提供可视化格式选项：

    - 第一行 on/off - 关联元素: firstRow
    - 最后一行 on/off - 关联元素: lastRow
    - 第一列 on/off - 关联元素: firstCol
    - 最后一列 on/off - 关联元素: lastCol
    - 行条带 on/off - 关联元素: band1H, band2H
    - 列条带 on/off - 关联元素: band1V, band2V

    与 WholeTbl 元素关联的格式定义了所有选项关闭时的表格式。 打开某个选项后，该特定选项的格式将应用于表格。 当打开重叠选项时，将启用四个单元格特定格式选项。 例如，当启用第一行和第一列格式设置选项时，也会应用西北单元格内的任何格式设置，因为当第一列和第一行格式设置选项都启用时，该单元格是重叠的表格单元格。

    """

    @property
    def table_background(self) -> Optional[CT_TableBackgroundStyle]:
        """表格背景

        20.1.4.2.25 tblBg

        此元素定义可应用于表格背景形状的格式选项。 背景形状与整个表格的大小相同，并且可以容纳跨越整个表格的填充或效果。
        """
        return getattr(self, qn('a:tblBg'), None)

    @property
    def whole_table(self) -> Optional[CT_TablePartStyle]:
        """整个表格样式

        20.1.4.2.34 wholeTbl

        此元素包含格式化选项，当表格处于默认状态且未启用格式化选项（第一行、最后一行等）时，这些选项将应用于整个表格。
        """
        return getattr(self, qn('a:wholeTbl'), None)

    @property
    def band_1h(self) -> Optional[CT_TablePartStyle]:
        """水平条带样式1

        20.1.4.2.1 band1H

        此元素描述水平条带中第一行的格式。 两种不同的行格式交替应用于表格，以便在表格上创建条带效果。
        """
        return getattr(self, qn('a:band1H'), None)

    @property
    def band_2h(self) -> Optional[CT_TablePartStyle]:
        """水平条带样式2

        20.1.4.2.3 band2H

        此元素描述水平条带中第二行的格式。 两种不同的行格式交替应用于表格，以便在表格上创建条带效果。
        """
        return getattr(self, qn('a:band2H'), None)

    @property
    def band_1v(self) -> Optional[CT_TablePartStyle]:
        """垂直条带样式1

        20.1.4.2.2 band1V

        此元素描述垂直条带中第一列的格式。 两种不同的列格式交替应用于表格，以便在表格上创建条带效果。
        """
        return getattr(self, qn('a:band1V'), None)

    @property
    def band_2v(self) -> Optional[CT_TablePartStyle]:
        """垂直条带样式2

        20.1.4.2.4 band2V

        此元素描述垂直条带中第二行的格式。 两种不同的行格式交替应用于表格，以便在表格上创建条带效果。
        """
        return getattr(self, qn('a:band2V'), None)

    @property
    def last_col(self) -> Optional[CT_TablePartStyle]:
        """最后一列

        20.1.4.2.16 lastCol

        此元素定义可应用于表格最后一列的单元格格式。
        """
        return getattr(self, qn('a:lastCol'), None)

    @property
    def first_col(self) -> Optional[CT_TablePartStyle]:
        """第一列

        20.1.4.2.11 firstCol

        此元素定义可应用于表格第一列的单元格格式。
        """
        return getattr(self, qn('a:firstCol'), None)

    @property
    def last_row(self) -> Optional[CT_TablePartStyle]:
        """最后一行

        20.1.4.2.17 lastRow

        此元素定义可应用于表格最后一行的单元格格式。
        """
        return getattr(self, qn('a:lastRow'), None)

    @property
    def se_cell(self) -> Optional[CT_TablePartStyle]:
        """东南角单元格

        20.1.4.2.23 seCell

        当最后一行格式设置和最后一列格式设置都启用时，此元素会违反表格东南角单元格的格式设置。 此格式仅应用于两个格式选项之间重叠的单个单元格。
        """
        return getattr(self, qn('a:seCell'), None)

    @property
    def sw_cell(self) -> Optional[CT_TablePartStyle]:
        """西南角单元格

        20.1.4.2.24 swCell

        当最后一行格式和第一列格式都启用时，此元素会违反表格西南角单元格的格式。 此格式仅应用于两个格式选项之间重叠的单个单元格。
        """
        return getattr(self, qn('a:swCell'), None)

    @property
    def first_row(self) -> Optional[CT_TablePartStyle]:
        """第一行

        20.1.4.2.12 firstRow

        此元素定义可应用于表格第一行的单元格格式。
        """
        return getattr(self, qn('a:firstRow'), None)

    @property
    def ne_cell(self) -> Optional[CT_TablePartStyle]:
        """东北角单元格

        20.1.4.2.20 neCell

        当启用第一行格式和最后一列格式时，此元素会违反表格东北角单元格的格式。 此格式仅应用于两个格式选项之间重叠的单个单元格。
        """
        return getattr(self, qn('a:neCell'), None)

    @property
    def nw_cell(self) -> Optional[CT_TablePartStyle]:
        """西北角单元格

        20.1.4.2.21 nwCell

        当启用第一行格式和第一列格式时，此元素会违反表格西北角单元格的格式。 此格式仅应用于两个格式选项之间重叠的单个单元格。
        """
        return getattr(self, qn('a:nwCell'), None)

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)

    @property
    def style_id(self) -> s_ST_Guid:
        """样式ID

        Style ID

        指定以唯一方式标识表格样式的 GUID。
        """

        val = self.attrib['styleId']

        return s_ST_Guid(utils.AnyStrToStr(val))  # type: ignore

    @property
    def style_name(self) -> str:
        """样式名称

        Name

        指定表格样式的名称，该名称可以显示在用户界面中，向用户标识该样式。
        """
        return utils.AnyStrToStr(self.attrib['styleName'])  # type: ignore


class CT_TableStyleList(OxmlBaseElement):
    """表格样式列表

    20.1.4.2.27 tblStyleLst (Table Style List)

    该元素只是文档中使用的表格样式的列表。
    """

    @property
    def table_style_lst(self) -> list[CT_TableStyle]:
        """
        表格样式
        """

        return self.findall(qn('a:tblStyle'))  # type: ignore

    @property
    def default(self) -> s_ST_Guid:
        """默认

        Default

        表格样式列表中默认表格样式对应的 GUID。 当表格最初插入到文档中时，可以使用此默认值。
        """

        val = self.attrib['def']

        return s_ST_Guid(utils.AnyStrToStr(val))  # type: ignore


class EG_TextRun(OxmlBaseElement):
    """

    <xsd:group name="EG_TextRun">
        <xsd:choice>
            <xsd:element name="r" type="CT_RegularTextRun"/>
            <xsd:element name="br" type="CT_TextLineBreak"/>
            <xsd:element name="fld" type="CT_TextField"/>
        </xsd:choice>
    </xsd:group>
    """

    text_run_tags = (
        qn('a:r'),  # CT_RegularTextRun
        qn('a:br'),  # CT_TextLineBreak
        qn('a:fld'),  # CT_TextField
    )

    # Optional[Union[CT_RegularTextRun, CT_TextLineBreak, CT_TextField]]


class CT_TextParagraph(EG_TextRun):
    """文本段落

    21.1.2.2.6 p

    此元素指定包含的文本正文中是否存在文本段落。 段落是文本正文中最高级别的文本分隔机制。 段落可以包含与该段落关联的文本段落属性。 如果未列出任何属性，则使用 defPPr 元素中指定的属性。
    """

    @property
    def paragraph_properites(self) -> Optional[CT_TextParagraphProperties]:
        """文本段落特性

        21.1.2.2.7 pPr

        此元素包含包含段落的所有段落级别文本属性。 这些段落属性应覆盖与相关段落关联的所有冲突属性。

        [Note: 要解决冲突的段落属性，应首先从 pPr 元素开始检查段落属性的线性层次结构。 这里的规则是在更接近实际文本的级别定义的属性应优先。 也就是说，如果 pPr 和 lvl1pPr 元素之间存在冲突属性，则 pPr 属性应优先，因为在属性层次结构中它更接近所表示的实际文本。 end note]
        """

        return getattr(self, qn('a:pPr'), None)

    @property
    def text_run_lst(
        self,
    ) -> list[CT_RegularTextRun | CT_TextLineBreak | CT_TextField]:
        """文本run列表

        21.1.2.3.8 r (文本运行)  - CT_RegularTextRun

            该元素指定包含文本正文中是否存在一系列文本。 run 元素是文本正文中最低级别的文本分隔机制。 文本运行可以包含与该运行关联的文本运行属性。 如果未列出任何属性，则使用 defRPr 元素中指定的属性。

        21.1.2.2.1 br (文本换行)  - CT_TextLineBreak

            此元素指定段落内两行文本之间是否存在垂直换行符。 除了指定两次文本之间的垂直间距之外，此元素还可以具有通过 rPr 子元素指定的运行(run)特性。 这设置了换行符的文本格式，以便以后在此处插入文本时可以使用正确的格式生成新的运行(run)。

        21.1.2.2.4 fld (文本域)  - CT_TextField

            该元素指定一个文本字段，其中包含应用程序应定期更新的生成文本。 每一段文本在生成时都会被赋予一个唯一的标识号，用于引用特定的字段。 创建时，文本字段指示应用于更新该字段的文本类型。 使用此更新类型是为了使所有未创建此文本字段的应用程序仍然可以知道应使用哪种类型的文本进行更新。 因此，新应用程序可以将更新类型附加到文本字段 id 以进行持续更新。
        """

        return self.choice_and_more(*self.text_run_tags)  # type: ignore

    @property
    def end_paraRPr(self) -> Optional[CT_TextCharacterProperties]:
        """段落结尾的运行特性

        21.1.2.2.3 endParaRPr

        此元素指定在指定的最后一个运行之后插入另一个运行时要使用的文本运行属性。 这有效地保存了运行属性状态，以便在用户输入其他文本时可以应用它。 如果省略此元素，则应用程序可以确定要应用哪些默认属性。 建议在段落内的文本列表末尾指定此元素，以便维护有序列表。
        """

        return getattr(self, qn('a:endParaRPr'), None)


class ST_TextAnchoringType(ST_BaseEnumType):
    """文本锚定类型

    20.1.10.60 ST_TextAnchoringType

    这个简单类型指定了文本可用的锚定类型列表。
    """

    Top = 't'
    """将文本锚定在边界矩形的顶部。"""

    Center = 'ctr'
    """将文本锚定在边界矩形的中间。"""

    Bottom = 'b'
    """将文本锚定在边界矩形的底部。"""

    Justify = 'just'
    """将文本锚定，使其在垂直方向上两端对齐。当文本是水平的时候，这会拉开实际的文本行，几乎总是与'distrib'相同（特殊情况: 如果只有1行，那么锚定在顶部）。当文本是垂直的时候，它会在垂直方向上两端对齐字母。这与anchorDistributed不同，因为在某些情况下，比如一行很少文本的情况下，它不会对齐。"""

    Distance = 'dist'
    """以垂直方向分布文本。当文本是水平的时候，这会拉开实际的文本行，几乎总是与anchorJustified相同（特殊情况: 如果只有1行，那么锚定在中间）。当文本是垂直的时候，它会在垂直方向分布字母。这与anchorJustified不同，因为它总是强制分布单词，即使一行只有一个或两个单词。"""


class ST_TextVertOverflowType(ST_BaseEnumType):
    """文本垂直溢出方式

    20.1.10.84 ST_TextVertOverflowType

    这个简单类型指定了文本的垂直溢出方式。
    """

    OverFlow = 'overflow'
    """文本溢出，不注意上下边界。"""

    Ellipsis = 'ellipsis'
    """注意上下边界。使用省略号表示存在不可见文本。"""

    Clip = 'clip'
    """注意上下边界。不提供任何指示存在不可见文本的迹象。"""


class ST_TextHorzOverflowType(ST_BaseEnumType):
    """文本水平溢出类型

    20.1.10.69 ST_TextHorzOverflowType
    """

    OverFlow = 'overflow'
    """当一个大字符无法放入一行时，允许水平溢出。"""

    Clip = 'clip'
    """当一个大字符无法放入一行时，在适当的水平溢出处裁剪它。"""


class ST_TextVerticalType(ST_BaseEnumType):
    """垂直文本类型

    20.1.10.83 ST_TextVerticalType

    如果存在垂直文本，确定将使用哪种类型的垂直文本。

    这个简单类型的内容是对W3C XML模式token数据类型的限制。
    """

    Horz = 'horz'
    """水平文本。这应该是默认值。"""

    Vert = 'vert'
    """确定是否所有文本都是垂直方向的（每行顺时针旋转90度，所以从上到下; 每一行都在前一行的左侧）。"""

    Vert270 = 'vert270'
    """确定是否所有文本都是垂直方向的（每行顺时针旋转270度，所以从下到上; 每一行都在前一行的右侧）。"""

    WordArtVert = 'wordArtVert'
    """确定是否所有文本都是垂直的（"一个字母在另一个字母的上面"）。"""

    EaVert = 'eaVert'
    """垂直文本的特殊版本，其中一些字体显示为沿90度旋转，而另一些字体（主要是东亚字体）显示为垂直。"""

    MongolianVert = 'mongolianVert'
    """垂直文本的特殊版本，其中一些字体显示为沿90度旋转，而另一些字体（主要是东亚字体）以垂直方式显示。与eastAsianVertical的区别在于文本从上到下然后从左到右流动，而不是从右到左。"""

    WordArtVertRtl = 'wordArtVertRtl'
    """指定应该从右到左而不是从左到右显示垂直WordArt。"""


class ST_TextWrappingType(ST_BaseEnumType):
    """文本包裹/换行类型

    20.1.10.85 ST_TextWrappingType

    文本换行类型
    """

    none = 'none'
    """文本换行类型枚举（无）"""

    Square = 'square'
    """文本换行类型枚举（方形）"""


ST_TextColumnCount = NewType('ST_TextColumnCount', int)
"""文本列数量

20.1.10.65 ST_TextColumnCount

这个简单类型指定了列的数量。

这个简单类型的内容是对W3C XML Schema int 数据类型的限制。

这个简单类型还指定了以下限制:

- 这个简单类型的最小值大于或等于1。
- 这个简单类型的最大值小于或等于16。
"""


def to_ST_TextColumnCount(_val: AnyStr) -> ST_TextColumnCount:
    value = int(utils.AnyStrToStr(_val))

    if not (1 <= value <= 16):
        msg = f'预期外的值: {value}'
        raise OxmlAttributeValidateError(msg)

    return ST_TextColumnCount(value)


class CT_TextListStyle(OxmlBaseElement):
    """文本列表样式

    19.3.1.49 titleStyle 幻灯片母版标题文本样式

        此元素指定母版幻灯片中标题文本的文本格式样式。 此格式适用于相关演示文稿幻灯片中的所有标题文本。 文本格式是通过利用 DrawingML 框架来指定的，就像在常规演示幻灯片中一样。 在标题样式中可以定义许多不同的样式类型，因为幻灯片标题中存储了不同类型的文本。

    19.3.1.5 bodyStyle 幻灯片母版正文文本样式

        此元素指定母版幻灯片中所有正文文本的文本格式样式。 此格式适用于与该母版相关的演示文稿幻灯片中的所有正文文本。 文本格式是通过利用 DrawingML 框架来指定的，就像在常规演示幻灯片中一样。 在 bodyStyle 元素中可以定义许多不同的样式类型，因为幻灯片正文中存储了不同类型的文本。

    19.3.1.35 otherStyle 幻灯片母版其他文本样式

        此元素指定母版幻灯片中所有其他文本的文本格式样式。 此格式适用于相关演示文稿幻灯片中 titleStyle 或 bodyStyle 元素未涵盖的所有文本。 文本格式是通过利用 DrawingML 框架来指定的，就像在常规演示幻灯片中一样。 在 otherStyle 元素中，可以定义许多不同的样式类型，因为幻灯片中存储了不同类型的文本。

        [Note: otherStyle 元素用于指定幻灯片形状内而非文本框中文本的文本格式。 文本框样式是在 bodyStyle 元素内处理的. end note]

    """

    @property
    def default_paragraph_properties(self) -> Optional[CT_TextParagraphProperties]:
        """默认段落属性

        21.1.2.2.2 defPPr (Default Paragraph Style)

        此元素指定在未指定其他段落属性时要应用的段落属性。 如果省略此属性，则由应用程序决定应应用的默认段落属性集。
        """
        return getattr(self, qn('a:defPPr'), None)

    @property
    def level_1_paragraph_properties(self) -> Optional[CT_TextParagraphProperties]:
        """
        21.1.2.4.13 lvl1pPr (List Level 1 Text Style)

        此元素指定具有属性 lvl="0" 的所有元素的所有段落级文本属性。 总共允许 9 级文本属性元素，级别 0-8。
        建议指定此级别属性元素和其他级别属性元素的顺序是级别递增的顺序。
        也就是说 lvl2pPr 应该出现在 lvl3pPr 之前。
        这允许较低级别的属性优先于较高级别的属性，因为它们首先被解析。
        """
        return getattr(self, qn('a:lvl1pPr'), None)

    @property
    def level_2_paragraph_properties(self) -> Optional[CT_TextParagraphProperties]:
        """
        21.1.2.4.14 lvl2pPr (List Level 2 Text Style)

        此元素指定具有属性 lvl="1" 的所有元素的所有段落级文本属性。 总共允许 9 级文本属性元素，级别 0-8。
        建议指定此级别属性元素和其他级别属性元素的顺序是级别递增的顺序。
        也就是说 lvl2pPr 应该出现在 lvl3pPr 之前。
        这允许较低级别的属性优先于较高级别的属性，因为它们首先被解析。
        """
        return getattr(self, qn('a:lvl2pPr'), None)

    @property
    def level_3_paragraph_properties(self) -> Optional[CT_TextParagraphProperties]:
        """
        21.1.2.4.15 lvl3pPr (List Level 3 Text Style)

        此元素指定具有属性 lvl="2" 的所有元素的所有段落级文本属性。 总共允许 9 级文本属性元素，级别 0-8。
        建议指定此级别属性元素和其他级别属性元素的顺序是级别递增的顺序。
        也就是说 lvl2pPr 应该出现在 lvl3pPr 之前。
        这允许较低级别的属性优先于较高级别的属性，因为它们首先被解析。
        """
        return getattr(self, qn('a:lvl3pPr'), None)

    @property
    def level_4_paragraph_properties(self) -> Optional[CT_TextParagraphProperties]:
        """
        21.1.2.4.16 lvl4pPr (List Level 4 Text Style)

        此元素指定具有属性 lvl="3" 的所有元素的所有段落级文本属性。 总共允许 9 级文本属性元素，级别 0-8。
        建议指定此级别属性元素和其他级别属性元素的顺序是级别递增的顺序。
        也就是说 lvl2pPr 应该出现在 lvl3pPr 之前。
        这允许较低级别的属性优先于较高级别的属性，因为它们首先被解析。
        """
        return getattr(self, qn('a:lvl4pPr'), None)

    @property
    def level_5_paragraph_properties(self) -> Optional[CT_TextParagraphProperties]:
        """
        21.1.2.4.17 lvl5pPr (List Level 5 Text Style)

        此元素指定具有属性 lvl="4" 的所有元素的所有段落级文本属性。 总共允许 9 级文本属性元素，级别 0-8。
        建议指定此级别属性元素和其他级别属性元素的顺序是级别递增的顺序。
        也就是说 lvl2pPr 应该出现在 lvl3pPr 之前。
        这允许较低级别的属性优先于较高级别的属性，因为它们首先被解析。
        """
        return getattr(self, qn('a:lvl5pPr'), None)

    @property
    def level_6_paragraph_properties(self) -> Optional[CT_TextParagraphProperties]:
        """
        21.1.2.4.18 lvl6pPr (List Level 6 Text Style)

        此元素指定具有属性 lvl="5" 的所有元素的所有段落级文本属性。 总共允许 9 级文本属性元素，级别 0-8。
        建议指定此级别属性元素和其他级别属性元素的顺序是级别递增的顺序。
        也就是说 lvl2pPr 应该出现在 lvl3pPr 之前。
        这允许较低级别的属性优先于较高级别的属性，因为它们首先被解析。
        """
        return getattr(self, qn('a:lvl6pPr'), None)

    @property
    def level_7_paragraph_properties(self) -> Optional[CT_TextParagraphProperties]:
        """
        21.1.2.4.19 lvl7pPr (List Level 7 Text Style)

        此元素指定具有属性 lvl="6" 的所有元素的所有段落级文本属性。 总共允许 9 级文本属性元素，级别 0-8。
        建议指定此级别属性元素和其他级别属性元素的顺序是级别递增的顺序。
        也就是说 lvl2pPr 应该出现在 lvl3pPr 之前。
        这允许较低级别的属性优先于较高级别的属性，因为它们首先被解析。
        """
        return getattr(self, qn('a:lvl7pPr'), None)

    @property
    def level_8_paragraph_properties(self) -> Optional[CT_TextParagraphProperties]:
        """
        21.1.2.4.20 lvl8pPr (List Level 8 Text Style)

        此元素指定具有属性 lvl="7" 的所有元素的所有段落级文本属性。 总共允许 9 级文本属性元素，级别 0-8。
        建议指定此级别属性元素和其他级别属性元素的顺序是级别递增的顺序。
        也就是说 lvl2pPr 应该出现在 lvl3pPr 之前。
        这允许较低级别的属性优先于较高级别的属性，因为它们首先被解析。
        """
        return getattr(self, qn('a:lvl8pPr'), None)

    @property
    def level_9_paragraph_properties(self) -> Optional[CT_TextParagraphProperties]:
        """
        21.1.2.4.21 lvl9pPr (List Level 9 Text Style)

        此元素指定具有属性 lvl="8" 的所有元素的所有段落级文本属性。 总共允许 9 级文本属性元素，级别 0-8。
        建议指定此级别属性元素和其他级别属性元素的顺序是级别递增的顺序。
        也就是说 lvl2pPr 应该出现在 lvl3pPr 之前。
        这允许较低级别的属性优先于较高级别的属性，因为它们首先被解析。
        """
        return getattr(self, qn('a:lvl9pPr'), None)

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""
        return getattr(self, qn('a:extLst'), None)


class ST_TextFontScalePercent(ST_BaseType[AnyStr, int]):
    def _validate(self: Self) -> None:
        val = int(utils.AnyStrToStr(self._val))

        if not (1000 <= val <= 100000):
            msg = f'预期外的值: {val}'
            raise OxmlAttributeValidateError(msg)

        self._python_val = val


class ST_TextFontScalePercentOrPercentString(ST_BaseType[AnyStr, Union[ST_TextFontScalePercent, s_ST_Percentage]]):
    """文本字体缩放百分比

    20.1.10.67 ST_TextFontScalePercentOrPercentString

    这个简单类型指定其内容将包含一个文本字体缩放百分比。有关详细信息，请参阅联合体的成员类型。

    这个简单类型是以下类型的联合体:

    - ST_Percentage 简单类型 (§22.9.2.9)。
    """

    def _validate(self: Self) -> None:
        val = utils.AnyStrToStr(self._val)

        if val.isdigit():
            self._python_val = ST_TextFontScalePercent(self._val)

        else:
            self._python_val = s_to_ST_Percentage(str(self._val))


class CT_TextNormalAutofit(OxmlBaseElement):
    """文本正常自动调整(适应)

    21.1.2.1.3 normAutofit

    此元素指定文本正文中的文本通常应自动适合边界框。 自动调整是指缩放文本框中的文本以使其保留在文本框中。 如果省略此元素，则暗示 noAutofit 或 auto-fit off。
    """

    @property
    def font_scale(self) -> ST_TextFontScalePercentOrPercentString:
        """字体比例

        指定文本正文中每次运行缩放到的原始字体大小的百分比。 为了在边界框中自动调整文本，有时需要将字体大小减小一定的百分比。 使用此属性，可以根据提供的值缩放文本框中的字体。 值为 100% 会将文本缩放到 100%，而值为 1% 会将文本缩放到 1%。 如果省略此属性，则暗示值为 100%。
        """
        val = self.attrib.get('fontScale')

        if val is None:
            val = '100%'

        return ST_TextFontScalePercentOrPercentString(val)

    @property
    def line_space_reduction(self) -> ST_TextSpacingPercentOrPercentString:
        """减少行距

        指定文本正文中每个段落的行间距减少的百分比量。 通过从原始行距值中减去它来应用减少。 使用此属性，文本行之间的垂直间距可以按百分比缩放。 值为 100% 时，行间距会减少 100%，而值为 1% 时，行间距会减少百分之一。 如果省略此属性，则暗示值为 0%。

        [Note: 该属性仅适用于具有百分比行间距的段落. end note]
        """
        val = self.attrib.get('lnSpcReduction')

        if val is None:
            val = '0%'

        return to_ST_TextSpacingPercentOrPercentString(str(val))


class CT_TextShapeAutofit(OxmlBaseElement):
    """文本随形状自动调整适应

    21.1.2.1.4 spAutoFit

    此元素指定形状应自动调整以完全包含其中描述的文本。 自动调整是指缩放形状内的文本以包含其中的所有文本。 如果省略此元素，则暗示 noAutofit 或 auto-fit off。
    """



class CT_TextNoAutofit(OxmlBaseElement):
    """不自动调整(适应)

    21.1.2.1.2 noAutofit

    此元素指定文本正文中的文本不应自动适合边界框。 自动调整是指缩放文本框中的文本以使其保留在文本框中。 如果省略此元素，则暗示 noAutofit 或 auto-fit off.
    """



class EG_TextAutofit(OxmlBaseElement):
    """
    <xsd:group name="EG_TextAutofit">
        <xsd:choice>
            <xsd:element name="noAutofit" type="CT_TextNoAutofit"/>
            <xsd:element name="normAutofit" type="CT_TextNormalAutofit"/>
            <xsd:element name="spAutoFit" type="CT_TextShapeAutofit"/>
        </xsd:choice>
    </xsd:group>
    """

    text_autofix_tags = (
        qn('a:noAutofit'),  # CT_TextNoAutofit
        qn('a:normAutofit'),  # CT_TextNormalAutofit
        qn('a:spAutoFit'),  # CT_TextShapeAutofit
    )

    # Optional[Union[CT_TextNoAutofit, CT_TextNormalAutofit, CT_TextShapeAutofit]]


class CT_TextBodyProperties(EG_TextAutofit, EG_Text3D):
    """正文特性

    21.1.2.1.1 bodyPr

    此元素定义形状内文本正文的正文特性(属性)

    样例: 考虑一个带有文本正文的形状，该文本正文具有一些与其关联的格式属性。 对于文本正文属性的格式设置，应按如下方式使用 bodyPr 元素:

    <p:sp>
        …
        <p:txBody>
            <a:bodyPr>
                (text body properties)
            </a:bodyPr>
            …
        </p:txBody>
    </p:sp>
    """

    @property
    def preset_text_warp(self) -> Optional[CT_PresetTextShape]:
        """预设文本及格式

        20.1.9.19 prstTxWarp

        该元素指定何时应使用预设的几何形状来变换一段文本。 此操作的正式名称为文本扭曲。 生成应用程序应该能够渲染 ST_TextShapeType 列表中枚举的所有预设几何图形。
        """
        return getattr(self, qn('a:prstTxWarp'), None)

    @property
    def text_autofit(
        self,
    ) -> Optional[CT_TextNoAutofit | CT_TextNormalAutofit | CT_TextShapeAutofit]:
        """文本自适应方式

        <xsd:group ref="EG_TextAutofit" minOccurs="0" maxOccurs="1"/>
        """

        return self.choice_one_child(*self.text_autofix_tags)  # type: ignore

    @property
    def scene_3d(self) -> Optional[CT_Scene3D]:
        """3D 场景特性(属性)

        20.1.4.1.26 scene3d (3D Scene Properties)

        该元素定义了应用于对象的可选场景级 3D 属性。
        """
        return getattr(self, qn('a:scene3d'), None)

    @property
    def text_3d(self) -> Optional[CT_Shape3D | CT_FlatText]:
        """
        aaa

        <xsd:group ref="EG_Text3D" minOccurs="0" maxOccurs="1"/>
        """

        return self.choice_one_child(*self.text3d_tags)  # type: ignore

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)

    @property
    def rotate(self) -> ST_Angle:
        """rot (旋转)

        指定应用于边界框内文本的旋转。 如果未指定，则使用伴随形状的旋转。 如果指定了，则其应用将独立于形状。 也就是说，除了文本本身应用旋转之外，形状还可以应用旋转。 如果省略该属性，则隐含值为 0。
        """
        val = self.attrib.get('rot')

        if val is not None:
            return to_ST_Angle(str(val))

        return ST_Angle(0)

    @property
    def spc_first_last_para(self) -> bool:
        """spcFirstLastPara (段落间距)

        指定是否遵守用户定义的前后段落间距。 虽然段落之间的间距很有帮助，但能够设置一个标志来确定是否在文本正文的边缘（即文本正文中的第一个和最后一个段落）遵循此间距也很有用。 更准确地说，由于这是文本主体级别的属性，因此它应该只影响给定文本主体的第一段之前的段落间距和最后一段的之后段落间距。 如果省略此属性，则隐含值为 0 或 false.
        """
        val = self.attrib.get('spcFirstLastPara')

        return utils.XsdBool(val, none=False)

    @property
    def vert_overflow(self) -> ST_TextVertOverflowType:
        """vertOverflow (文本垂直溢出)

        确定文本是否可以垂直流出边界框。 这用于确定如果形状内的文本对于其包含的边界框来说太大，会发生什么情况。 如果省略该属性，则隐含溢出值。
        """
        val = self.attrib.get('vertOverflow')

        if val is not None:
            return ST_TextVertOverflowType(val)

        return ST_TextVertOverflowType.OverFlow

    @property
    def horz_overflow(self) -> ST_TextHorzOverflowType:
        """horzOverflow (文本水平溢出)

        确定文本是否可以水平流出边界框。 这用于确定如果形状内的文本对于其包含的边界框来说太大，会发生什么情况。 如果省略该属性，则隐含溢出值。
        """
        val = self.attrib.get('horzOverflow')

        if val is not None:
            return ST_TextHorzOverflowType(val)

        return ST_TextHorzOverflowType.OverFlow

    @property
    def vert(self) -> ST_TextVerticalType:
        """vert (竖排文字)

        确定给定文本正文中的文本是否应垂直显示。 如果省略此属性，则隐含水平值，或不隐含垂直文本。
        """
        val = self.attrib.get('vert')

        if val is not None:
            return ST_TextVerticalType(val)

        return ST_TextVerticalType.Horz

    @property
    def wrap(self) -> ST_TextWrappingType:
        """wrap (文本包裹类型)

        指定用于此文本正文的换行选项。 如果省略此属性，则隐含 square 值，该值使用边界文本框包裹文本。
        """
        val = self.attrib.get('wrap')

        if val is not None:
            return ST_TextWrappingType(val)

        return ST_TextWrappingType.Square

    @property
    def left_ins(self) -> ST_Coordinate32:
        """lIns (左插图)

        指定边界矩形的左插图。 插图仅用作形状内文本框的内部边距。 如果省略此属性，则隐含值 91440 或 0.1 英寸。
        """
        val = self.attrib.get('lIns')

        if val is not None:
            return to_ST_Coordinate32(val)  # type: ignore

        return to_ST_Coordinate32('91440')

    @property
    def top_ins(self) -> ST_Coordinate32:
        """tIns (顶部插图)

        指定边界矩形的顶部插入。 插图仅用作形状内文本框的内部边距。 如果省略此属性，则隐含值 45720 或 0.05 英寸。
        """
        val = self.attrib.get('tIns')

        if val is not None:
            return to_ST_Coordinate32(val)  # type: ignore

        return to_ST_Coordinate32('45720')

    @property
    def right_ins(self) -> ST_Coordinate32:
        """rIns (右插图)

        指定边界矩形的右插图。 插图仅用作形状内文本框的内部边距。 如果省略此属性，则隐含值 91440 或 0.1 英寸。
        """
        val = self.attrib.get('rIns')

        if val is not None:
            return to_ST_Coordinate32(val)  # type: ignore

        return to_ST_Coordinate32('91440')

    @property
    def bottom_ins(self) -> ST_Coordinate32:
        """bIns (底部插图)

        指定边界矩形的底部插入。 插图仅用作形状内文本框的内部边距。

        如果省略此属性，则隐含值 45720 或 0.05 英寸。
        """
        val = self.attrib.get('bIns')

        if val is not None:
            return to_ST_Coordinate32(val)  # type: ignore

        return to_ST_Coordinate32('45720')

    @property
    def num_col(self) -> ST_TextColumnCount:
        """numCol (列数)

        指定边框中文本的列数。 当应用于文本串时，此属性采用文本边框的宽度并将其除以指定的列数。 然后，这些列被视为溢出容器，因为当前一列已填充文本时，下一列将充当附加文本的存储库。 当所有列都已填充且文本仍然保留时，将使用为此文本正文设置的溢出属性，并重新排列文本以为其他文本腾出空间。 如果省略该属性，则隐含值为 1。
        """
        val = self.attrib.get('numCol')

        if val is not None:
            return to_ST_TextColumnCount(val)  # type: ignore

        return to_ST_TextColumnCount('1')

    @property
    def spc_col(self) -> ST_PositiveCoordinate32:
        """spcCol (列之间的空间)

        指定文本区域中文本列之间的间距。 这仅适用于存在多于 1 列的情况。 如果省略该属性，则隐含值为 0。
        """
        val = self.attrib.get('spcCol')

        if val is not None:
            return to_ST_PositiveCoordinate32(val)  # type: ignore

        return to_ST_PositiveCoordinate32('0')

    @property
    def rtl_col(self) -> XSD_Boolean:
        """rtlCol (列从右到左)

        指定是按从右到左还是从左到右的顺序使用列。 此属性的用法仅设置列顺序，该顺序用于确定下一个溢出文本应转到哪一列。 如果省略此属性，则隐含值 0 或 false，在这种情况下，文本从最左边的列开始并向右流动。
        """
        val = self.attrib.get('rtlCol')

        return to_xsd_bool(val, none=False)

    @property
    def from_word_art(self) -> XSD_Boolean:
        """fromWordArt (来自艺术字)

        指定此文本框中的文本是从艺术字对象转换而来的文本。 这更多的是一个向后兼容性属性，从跟踪的角度来看，它对应用程序很有用。 艺术字是应用文本效果的前一种方式，因此该属性在文档转换场景中非常有用。 如果省略此属性，则隐含值 0 或 false。
        """
        val = self.attrib.get('fromWordArt')

        return to_xsd_bool(val, none=False)

    @property
    def anchor(self) -> ST_TextAnchoringType:
        """anchor (锚)

        指定 txBody 在形状内的锚定位置。 如果省略此属性，则隐含 t 或 top 值。
        """

        val = self.attrib.get('anchor')

        if val is not None:
            return ST_TextAnchoringType(val)

        return ST_TextAnchoringType.Top

    @property
    def anchor_center(self) -> XSD_Boolean:
        """anchorCtr (锚定中心)

        指定文本框的居中位置。 它的基本工作方式是确定文本的最小可能“边界框”，然后相应地将该“边界框”居中。 这与段落对齐不同，段落对齐在文本的“边界框”内对齐文本。 该标志与所有不同类型的锚定兼容。 如果省略此属性，则隐含值 0 或 false。
        """
        val = self.attrib.get('anchorCtr')

        return to_xsd_bool(val, none=False)

    @property
    def force_aa(self) -> XSD_Boolean:
        """forceAA (强制抗锯齿)

        无论字体大小如何，强制文本呈现抗锯齿效果。 某些字体的边缘可能会出现颗粒状，除非它们经过抗锯齿处理。 因此，此属性允许指定哪些文本正文应始终消除锯齿，哪些不应消除锯齿。 如果省略此属性，则隐含值 0 或 false。
        """
        val = self.attrib.get('forceAA')

        return to_xsd_bool(val, none=False)

    @property
    def up_right(self) -> XSD_Boolean:
        """upright (文字直立)

        指定文本是否应保持直立，无论对其应用的变换以及伴随的形状变换如何。 如果省略此属性，则隐含值为 0 或 false.
        """
        val = self.attrib.get('upright')

        return to_xsd_bool(val, none=False)

    @property
    def compat_line_space(self) -> XSD_Boolean:
        """compatLnSpc (兼容的行距)

        指定使用字体场景以简单的方式决定此文本正文的行距。 如果省略此属性，则隐含值 0 或 false。
        """
        val = self.attrib.get('compatLnSpc')

        return to_xsd_bool(val, none=False)


class CT_TextBody(OxmlBaseElement):
    """形状文本主体

    20.1.2.2.40 txBody

    该元素指定相应形状中是否存在要包含的文本。 所有可见文本和可见文本相关属性都包含在此元素内。 可以有多个段落，段落内可以有多个文本段.
    """

    @property
    def body_properties(self) -> CT_TextBodyProperties:
        """主体属性

        <xsd:element name="bodyPr" type="CT_TextBodyProperties" minOccurs="1" maxOccurs="1"/>
        """

        return getattr(self, qn('a:bodyPr'))

    @property
    def text_list_style(self) -> Optional[CT_TextListStyle]:
        """
        文本列表样式

        <xsd:element name="lstStyle" type="CT_TextListStyle" minOccurs="0" maxOccurs="1"/>
        """

        return getattr(self, qn('a:lstStyle'), None)

    @property
    def text_paragraphs(self) -> list[CT_TextParagraph]:
        """
        文本段落列表

        <xsd:element name="p" type="CT_TextParagraph" minOccurs="1" maxOccurs="unbounded"/>
        """

        return self.findall(qn('a:p'))  # type: ignore


class ST_TextBulletStartAtNum(ST_BaseType[AnyStr, int]):
    """项目符号起始编号范围

    20.1.10.63 ST_TextBulletStartAtNum

    这个简单类型指定了项目符号的自动编号序列的起始编号范围。当编号是按字母顺序时，数字映射到相应的字母。1->a，2->b等。如果数字超过26，那么数字开始重复。例如，27->aa，53->aaa。

    这个简单类型的内容是对W3C XML Schema int 数据类型的限制。

    这个简单类型还指定了以下限制:

    - 这个简单类型的最小值大于或等于1。
    - 这个简单类型的最大值小于或等于32767。
    """

    def _validate(self: Self) -> None:
        val = int(utils.AnyStrToStr(self._val))

        if not (1 <= val <= 32767):
            msg = f'预期外的值: {val}'
            raise OxmlAttributeValidateError(msg)

        self._python_val = val


class ST_TextAutonumberScheme(ST_BaseEnumType):
    """文本自动编号方案

    20.1.10.61 ST_TextAutonumberScheme

    这个简单类型指定了自动编号方案的列表。
    """

    AlphaLcParenBoth = 'alphaLcParenBoth'
    """自动编号枚举（小写字母括号两边）

    (a), (b), ©, …
    """

    AlphaUcParenBoth = 'alphaUcParenBoth'
    """自动编号枚举（大写字母括号两边）

    (A), (B), (C), …
    """

    AlphaLcParenR = 'alphaLcParenR'
    """自动编号枚举（小写字母右括号）

    a), b), c), …
    """

    AlphaUcParenR = 'alphaUcParenR'
    """自动编号枚举（大写字母右括号）

    A), B), C), …
    """

    AlphaLcPeriod = 'alphaLcPeriod'
    """自动编号枚举（小写字母句点）

    a., b., c., …
    """

    AlphaUcPeriod = 'alphaUcPeriod'
    """自动编号枚举（大写字母句点）

    A., B., C., …
    """

    ArabicParenBoth = 'arabicParenBoth'
    """自动编号枚举（阿拉伯数字括号两边）

    (1), (2), (3), …
    """

    ArabicParenR = 'arabicParenR'
    """自动编号枚举（阿拉伯数字右括号）

    1), 2), 3), …
    """

    ArabicPeriod = 'arabicPeriod'
    """自动编号枚举（阿拉伯数字句点）

    1., 2., 3., …
    """

    ArabicPlain = 'arabicPlain'
    """自动编号枚举（阿拉伯数字）

    1, 2, 3, …
    """

    RomanLcParenBoth = 'romanLcParenBoth'
    """自动编号枚举（罗马字母小写括号两边）

    (i), (ii), (iii), …
    """

    RomanUcParenBoth = 'romanUcParenBoth'
    """自动编号枚举（罗马字母大写括号两边）

    (I), (II), (III), …
    """

    RomanLcParenR = 'romanLcParenR'
    """自动编号枚举（罗马字母小写右括号）

    i), ii), iii), …
    """

    RomanUcParenR = 'romanUcParenR'
    """自动编号枚举（罗马字母大写右括号）

    I), II), III), …
    """

    RomanLcPeriod = 'romanLcPeriod'
    """自动编号枚举（罗马字母小写句点）

    i., ii., iii., …
    """

    RomanUcPeriod = 'romanUcPeriod'
    """自动编号枚举（罗马字母大写句点）

    I., II., III., …
    """

    CircleNumDbPlain = 'circleNumDbPlain'
    """自动编号枚举（双字节圆圈数字）

    双字节圆圈数字（1-10 圆圈[0x2460-]，11-阿拉伯数字）
    """

    CircleNumWdBlackPlain = 'circleNumWdBlackPlain'
    """自动编号枚举（Wingdings黑色圆圈数字）

    Wingdings黑色圆圈数字
    """
    CircleNumWdWhitePlain = 'circleNumWdWhitePlain'
    """自动编号枚举（Wingdings白色圆圈数字）

    Wingdings白色圆圈数字（0-10 圆圈[0x0080-]，11-阿拉伯数字）
    """

    ArabicDbPeriod = 'arabicDbPeriod'
    """自动编号枚举（双字节阿拉伯数字带双字节句点）

    双字节阿拉伯数字带有双字节句点
    """

    ArabicDbPlain = 'arabicDbPlain'
    """自动编号枚举（双字节阿拉伯数字）

    双字节阿拉伯数字
    """

    Ea1ChsPeriod = 'ea1ChsPeriod'
    """自动编号枚举（EA: 简体中文带单字节句点）

    EA: 简体中文带单字节句点
    """

    Ea1ChsPlain = 'ea1ChsPlain'
    """自动编号枚举（EA: 简体中文）

    EA: 简体中文（TypeA 1-99，TypeC 100-）
    """

    Ea1ChtPeriod = 'ea1ChtPeriod'
    """自动编号枚举（EA: 繁体中文带单字节句点）

    EA: 繁体中文带单字节句点
    """

    Ea1ChtPlain = 'ea1ChtPlain'
    """自动编号枚举（EA: 繁体中文）

    EA: 繁体中文（TypeA 1-19，TypeC 20-）
    """

    Ea1JpnChsDbPeriod = 'ea1JpnChsDbPeriod'
    """自动编号枚举（EA: 日语/简体中文带双字节句点）

    EA: 日语带双字节句点
    """
    Ea1JpnKorPlain = 'ea1JpnKorPlain'
    """自动编号枚举（EA: 日语/韩语带单字节句点）

    EA: 日语/韩语带单字节句点
    """

    Ea1JpnKorPeriod = 'ea1JpnKorPeriod'
    """自动编号枚举（EA: 日语/韩语）

    EA: 日语/韩语（TypeC 1-）
    """

    Arabic1Minus = 'arabic1Minus'
    """自动编号枚举（阿拉伯数字1带负号）

    双向阿拉伯数字1（AraAlpha），带有ANSI减号符号
    """

    Arabic2Minus = 'arabic2Minus'
    """自动编号枚举（阿拉伯数字2带负号）

    双向阿拉伯数字2（AraAbjad），带有ANSI减号符号
    """

    Hebrew2Minus = 'hebrew2Minus'
    """自动编号枚举（希伯来语2带负号）

    双向希伯来语2带ANSI减号
    """

    ThaiAlphaPeriod = 'thaiAlphaPeriod'
    """自动编号枚举（泰文数字句点）

    泰文数字句点
    """
    ThaiAlphaParenR = 'thaiAlphaParenR'
    """自动编号枚举（泰文数字右括号）

    泰文数字括号 - 右边
    """
    ThaiAlphaParenBoth = 'thaiAlphaParenBoth'
    """自动编号枚举（泰文字母括号两边）

    泰文字母括号 - 两边
    """
    ThaiNumPeriod = 'thaiNumPeriod'
    """自动编号枚举（印地语字母带句点）

    印地语字母句点 - 元音
    """
    ThaiNumParenR = 'thaiNumParenR'
    """自动编号枚举（泰文字母右括号）

    泰文字母括号 - 右边
    """
    ThaiNumParenBoth = 'thaiNumParenBoth'
    """自动编号枚举（泰文数字括号两边）

    泰文数字括号 - 两边
    """
    HindiAlphaPeriod = 'hindiAlphaPeriod'
    """自动编号枚举（泰文字母句点）

    泰文字母句点
    """

    HindiNumPeriod = 'hindiNumPeriod'
    """自动编号枚举（印地数字句点）

    印地数字句点
    """
    HindiNumParenR = 'hindiNumParenR'
    """自动编号枚举（印地数字右括号）

    印地数字右括号
    """
    HindiAlpha1Period = 'hindiAlpha1Period'
    """自动编号枚举（印地语字母1带句点）

    印地语字母句点 - 辅音
    """


class CT_TextBulletColorFollowText(OxmlBaseElement):
    """指定段落项目符号的颜色应与包含每个项目符号的文本颜色相同

    21.1.2.4.5 buClrTx

    此元素指定段落项目符号的颜色应与包含每个项目符号的文本颜色相同。
    """



class EG_TextBulletColor(OxmlBaseElement):
    """
    <xsd:group name="EG_TextBulletColor">
        <xsd:choice>
            <xsd:element name="buClrTx" type="CT_TextBulletColorFollowText" minOccurs="1" maxOccurs="1"/>
            <xsd:element name="buClr" type="CT_Color" minOccurs="1" maxOccurs="1"/>
        </xsd:choice>
    </xsd:group>
    """

    text_bullet_color_tags = (
        qn('a:buClrTx'),  # CT_TextBulletColorFollowText
        qn('a:buClr'),  # CT_Color
    )

    # Optional[Union[CT_TextBulletColorFollowText, CT_Color]]


class ST_TextBulletSizeDecimal(ST_BaseType[AnyStr, int]):
    def _validate(self: Self) -> None:
        val = int(utils.AnyStrToStr(self._val))

        if not (25000 <= val <= 400000):
            msg = '预期外的值'
            raise OxmlAttributeValidateError(msg)

        self._python_val = val


ST_TextBulletSizePercent = NewType('ST_TextBulletSizePercent', float)
"""项目符号百分比

20.1.10.62 ST_TextBulletSizePercent

这个简单类型指定了项目符号百分比的范围。项目符号百分比是指项目符号相对于应该跟随它的文本的大小。

这个简单类型还指定了以下限制:

- 这个简单类型的内容应该匹配以下正则表达式模式: 0*((2[5-9])|([3-9][0-9])|([1-3][0-9][0-9])|400)%。

<xsd:pattern value="0*((2[5-9])|([3-9][0-9])|([1-3][0-9][0-9])|400)%"/>
"""


def to_ST_TextBulletSizePercent(val: str) -> ST_TextBulletSizePercent:
    """文本项目符号大小/百分比为单位"""

    return ST_TextBulletSizePercent(to_ST_Percentage(val))


class ST_TextBulletSize(ST_BaseType[AnyStr, Union[int, str]]):
    """文本项目符号百分比

    20.1.10.87 ST_TextBulletSize

    这个简单类型指定了项目符号百分比的范围。项目符号百分比是项目符号相对于接下来的文本的大小，最小大小为25%，最大大小为400%。

    这个简单类型是以下类型的并集：

    - ST_TextBulletSizePercent 简单类型 (§20.1.10.62)
    """

    def _validate(self: Self) -> None:
        val = utils.AnyStrToStr(self._val)

        if val.isdigit():
            self._python_val = ST_TextBulletSizeDecimal(self._val).value

        else:
            self._python_val = to_ST_TextBulletSizePercent(val)


class CT_TextBulletSizeFollowText(OxmlBaseElement):
    """21.1.2.4.11 buSzTx (项目符号大小跟随文本)

    此元素指定段落项目符号的大小应与包含每个项目符号的文本运行的磅值相同。
    """



class CT_TextBulletSizePercent(OxmlBaseElement):
    """21.1.2.4.9 buSzPct (项目符号大小百分比)

    此元素指定给定段落内的项目符号字符所使用的周围文本的大小（以百分比表示）.
    """

    @property
    def value(self) -> ST_TextBulletSizePercent:
        """项目符号应占文本大小的百分比

        指定该项目符号应占文本大小的百分比。 该属性不应低于25%且不应高于400%。
        """
        val = str(self.attrib['val'])

        return to_ST_TextBulletSizePercent(val)


class CT_TextBulletSizePoint(OxmlBaseElement):
    """项目符号大小Points

    21.1.2.4.10 buSzPts

    此元素指定给定段落内项目符号字符使用的大小（以磅为单位）。

    使用点指定大小，其中 100 等于 1 点字体，1200 等于 12 点字体。
    """

    @property
    def value(self) -> ST_TextFontSize:
        """以点大小指定项目符号的大小

        以点大小指定项目符号的大小。 整点以 100 为增量指定，从 100 开始，点大小为 1。例如，字体点大小 12 将是 1200，字体点大小 12.5 将是 1250。
        """
        val = self.attrib['val']

        return to_ST_TextFontSize(str(val))


class EG_TextBulletSize(OxmlBaseElement):
    """
    <xsd:group name="EG_TextBulletSize">
        <xsd:choice>
            <xsd:element name="buSzTx" type="CT_TextBulletSizeFollowText"/>
            <xsd:element name="buSzPct" type="CT_TextBulletSizePercent"/>
            <xsd:element name="buSzPts" type="CT_TextBulletSizePoint"/>
        </xsd:choice>
    </xsd:group>
    """

    text_bullet_size_tags = (
        qn('a:buSzTx'),  # CT_TextBulletSizeFollowText
        qn('a:buSzPct'),  # CT_TextBulletSizePercent
        qn('a:buSzPts'),  # CT_TextBulletSizePoint
    )

    # Optional[
    #     Union[
    #         CT_TextBulletSizeFollowText,
    #         CT_TextBulletSizePercent,
    #         CT_TextBulletSizePoint,
    #     ]
    # ]


class CT_TextBulletTypefaceFollowText(OxmlBaseElement):
    """字体跟随文本

    21.1.2.4.7 buFontTx (跟随文字)

    此元素指定段落项目符号的字体应与包含每个项目符号的文本的字体相同。
    """



class EG_TextBulletTypeface(OxmlBaseElement):
    """
    <xsd:group name="EG_TextBulletTypeface">
        <xsd:choice>
            <xsd:element name="buFontTx" type="CT_TextBulletTypefaceFollowText"/>
            <xsd:element name="buFont" type="CT_TextFont"/>
        </xsd:choice>
    </xsd:group>
    """

    text_bullet_typeface_tags = (
        qn('a:buFontTx'),  # CT_TextBulletTypefaceFollowText
        qn('a:buFont'),  # CT_TextFont
    )

    # Optional[Union[CT_TextBulletTypefaceFollowText, CT_TextFont]]


class CT_TextAutonumberBullet(OxmlBaseElement):
    """自动编号项目符号

    21.1.2.4.1 buAutoNum

    此元素指定应将自动编号的项目符号点应用于段落。 这些不仅仅是用作要点的数字，而是基于 buAutoNum 属性和段落级别自动分配的数字。
    """

    @property
    def type(self) -> ST_TextAutonumberScheme:
        """项目符号自动编号类型

        Bullet Autonumbering Type

        指定要使用的编号方案。 这允许描述除严格数字之外的格式。 例如，一组项目符号可以用一系列罗马数字来表示，而不是标准的 1、2、3 等。 号码设定。
        """

        val = self.attrib['type']

        return ST_TextAutonumberScheme(val)

    @property
    def start_at(self) -> ST_TextBulletStartAtNum:
        """开始编号 Start Numbering At

        20.1.10.63 ST_TextBulletStartAtNum

        指定给定的自动编号项目符号序列的开始编号。 当编号按字母顺序排列时，数字应映射到适当的字母。 例如，1 映射到“a”，2 映射到“b”，依此类推。 如果数字大于 26，则应使用多个字母。 例如，27 应表示为“aa”，类似地，53 应表示为“aaa”。
        """

        val = self.attrib.get('startAt')

        if val is None:
            val = '1'

        return ST_TextBulletStartAtNum(val)


class CT_TextCharBullet(OxmlBaseElement):
    """字符项目符号

    21.1.2.4.3 buChar

    该元素指定将一个字符应用于一组项目符号。 这些项目符号可以是系统能够支持的任何字体的任何字符。 如果没有与此元素一起指定项目符号字体，则使用段落字体。
    """

    @property
    def char(self) -> str:
        """作为项目符号的字符

        Bullet Character

        指定用于代替标准项目符号点的字符。 该字符可以是查看本文档的系统支持的指定字体的任何字符。
        """

        return utils.AnyStrToStr(self.attrib['char'])  # type: ignore


class CT_TextBlipBullet(OxmlBaseElement):
    """图片项目符号

    21.1.2.4.2 buBlip

    此元素指定将图片应用于一组项目符号。 该元素允许使用任何标准图片格式图形来代替典型的项目符号字符。 这使得项目符号成为生成应用程序想要应用的任何东西的可能性。
    """

    @property
    def blip(self) -> CT_Blip:
        """图片"""

        return getattr(self, qn('a:blip'))


class CT_TextNoBullet(OxmlBaseElement):
    """无项目符号

    21.1.2.4.8 buNone

    此元素指定应用该元素的段落不应用项目符号格式。 也就是说，在指定此元素的段落中不应找到项目符号。
    """



class EG_TextBullet(OxmlBaseElement):
    """
    <xsd:group name="EG_TextBullet">
        <xsd:choice>
            <xsd:element name="buNone" type="CT_TextNoBullet"/>
            <xsd:element name="buAutoNum" type="CT_TextAutonumberBullet"/>
            <xsd:element name="buChar" type="CT_TextCharBullet"/>
            <xsd:element name="buBlip" type="CT_TextBlipBullet"/>
        </xsd:choice>
    </xsd:group>
    """

    text_bullet_tags = (
        qn('a:buNone'),  # CT_TextNoBullet
        qn('a:buAutoNum'),  # CT_TextAutonumberBullet
        qn('a:buChar'),  # CT_TextCharBullet
        qn('a:buBlip'),  # CT_TextBlipBullet
    )

    # Union[
    #         CT_TextNoBullet,
    #         CT_TextAutonumberBullet,
    #         CT_TextCharBullet,
    #         CT_TextBlipBullet,
    #     ]


class ST_TextPointUnqualified(ST_BaseType[AnyStr, int]):
    """文本字号点数

    20.1.10.75 ST_TextPointUnqualified

    这种简单类型指定了字号的点数的百分之一。取值范围限定在[-400000, 400000]之间，即从-4000磅到4000磅。

    这种简单类型的内容是对W3C XML Schema int数据类型的限制。

    这种简单类型还指定了以下限制:

    - 最小值大于或等于-400000。
    - 最大值小于或等于400000。
    """

    def _validate(self: Self) -> None:
        val = int(utils.AnyStrToStr(self._val))

        if not (-400000 <= val <= 400000):
            msg = f'预期外的值: {val}'
            raise OxmlAttributeValidateError(msg)

        self._python_val = val


ST_TextPoint = NewType('ST_TextPoint', int)
"""文本point大小

20.1.10.74 ST_TextPoint

这个简单类型指定了文档的点大小。它可以用于测量或间距；其最大尺寸为± 4000点。

它的内容可以包含以下内容之一:

- 整数，其内容包括以点的百分之一为单位的测量值
- 数字后面紧跟单位标识符

这个简单类型是以下类型的并集:

- ST_TextPointUnqualified 简单类型（§20.1.10.75）。
- ST_UniversalMeasure 简单类型（§22.9.2.15）。
"""
# ST_TextPoint = Union[ST_TextPointUnqualified, Shared_ST_UniversalMeasure]


def to_ST_TextPoint(val: str) -> ST_TextPoint:
    try:
        pyval = int(val)

        if not (-400000 <= pyval <= 400000):
            msg = f'预期外的值: {val}'
            raise OxmlAttributeValidateError(msg)

        return ST_TextPoint(Pt(pyval).emu)

    except Exception:
        return ST_TextPoint(to_ST_UniversalMeasure(val))


ST_TextNonNegativePoint = NewType('ST_TextNonNegativePoint', int)
""" 文本非负字体大小

20.1.10.73 ST_TextNonNegativePoint

这个简单类型指定了以点的百分之一为单位的非负字体大小。它的取值范围是[0, 400000]。这个简单类型的内容是对W3C XML Schema int数据类型的限制。此外，它还指定了以下限制:

- 最小值大于或等于0。
- 最大值小于或等于400000。
"""


def to_ST_TextNonNegativePoint(val: str) -> ST_TextNonNegativePoint:
    pyval = int(val)

    if not (0 <= pyval <= 400000):
        msg = f'预期外的值: {val}'
        raise OxmlAttributeValidateError(msg)

    return ST_TextNonNegativePoint(Pt(pyval).emu)


ST_TextFontSize = NewType('ST_TextFontSize', int)
"""文本字体尺寸

20.1.10.68 ST_TextFontSize

这个简单类型指定任何文本的大小，单位为百分之一磅。必须至少为1磅。

此简单类型还指定了以下限制:

- 此简单类型的最小值大于或等于100。
- 此简单类型的最大值小于或等于400000。

注意:

这里返回的是int 代表 EMU ， 是经过转换的。
"""


def to_ST_TextFontSize(val: str) -> ST_TextFontSize:
    pyval = int(val)

    if not (100 <= pyval <= 400000):
        msg = f'预期外的值: {val}'
        raise OxmlAttributeValidateError(msg)

    return ST_TextFontSize(int(pyval / 100))


ST_TextTypeface = NewType('ST_TextTypeface', str)
"""文本字体字形(typeface)

20.1.10.81 ST_TextTypeface

这个简单类型指定了我们表示字体字形的方式。
"""


class ST_PitchFamily(ST_BaseEnumType):
    """字体间距家族

    20.1.10.41 ST_PitchFamily (Pitch Family)

    这个简单的类型指定字体间距。

    [注: 虽然类型名称为 ST_PitchFamily，但该属性的整数值指定高 4 位的字体系列和低 4 位的字体间距。 ]
    """

    DefaultPitchAndUnFmly = 0x00  # 00 DEFAULT PITCH + UNKNOWN FONT FAMILY
    """默认字符间距 + 未知字体族"""

    FixedPitchAndUnFmly = 0x01  # 01 FIXED PITCH + UNKNOWN FONT FAMILY
    """固定字符间距 + 未知字体族"""

    VariablePitchAndUnFmly = 0x02  # 02 VARIABLE PITCH + UNKNOWN FONT FAMILY
    """可变字符间距 + 未知字体族"""

    DefaultPitchAndRFmly = 0x10  # 16 DEFAULT PITCH + ROMAN FONT FAMILY
    """默认字符间距 + 罗马字体族"""

    FixedPtichAndRFmly = 0x11  # 17 FIXED PITCH + ROMAN FONT FAMILY
    """固定字符间距 + 罗马字体族"""

    VariablePitchAndRFmly = 0x12  # 18 VARIABLE PITCH + ROMAN FONT FAMILY
    """可变字符间距 + 罗马字体族"""

    DefaultPitchAndSFmly = 0x20  # 32 DEFAULT PITCH + SWISS FONT FAMILY
    """默认字符间距 + 瑞士字体族"""

    FixedPtichAndSFmly = 0x21  # 33  FIXED PITCH + SWISS FONT FAMILY
    """固定字符间距 + 瑞士字体族"""

    VariablePitchAndSFmly = 0x22  # 34 VARIABLE PITCH + SWISS FONT FAMILY
    """可变字符间距 + 瑞士字体族"""

    DefaultPitchAndMFmly = 0x30  # 48 DEFAULT PITCH + MODERN FONT FAMILY
    """默认字符间距 + 现代字体族"""

    FixedPtichAndMFmly = 0x31  # 49 FIXED PITCH + MODERN FONT FAMILY
    """固定字符间距 + 现代字体族"""

    VariablePitchAndMFmly = 0x32  # 50 VARIABLE PITCH + MODERN FONT FAMILY
    """可变字符间距 + 现代字体族"""

    DefaultPitchAndSCFmly = 0x40  # 64 DEFAULT PITCH + SCRIPT FONT FAMILY
    """默认字符间距 + 草书字体族"""

    FixedPtichAndSCFmly = 0x41  # 65 FIXED PITCH + SCRIPT FONT FAMILY
    """固定字符间距 + 草书字体族"""

    VariablePitchAndSCFmly = 0x42  # 66 VARIABLE PITCH + SCRIPT FONT FAMILY
    """可变字符间距 + 草书字体族"""

    DefaultPitchAndDFmly = 0x50  # 80 DEFAULT PITCH + DECORATIVE FONT FAMILY
    """默认字符间距 + 装饰字体族"""

    FixedPtichAndDFmly = 0x51  # 81 FIXED PITCH + DECORATIVE FONT FAMILY
    """固定字符间距 + 装饰字体族"""

    VariablePitchAndDFmly = 0x52  # 82 VARIABLE PITCH + DECORATIVE FONT FAMILY
    """可变字符间距 + 装饰字体族"""


class CT_TextFont(OxmlBaseElement):
    """文本字体

    21.1.2.3.1 cs (复杂脚本字体)

        该元素指定将复杂的脚本字体用于特定的文本运行。 该字体由与其他字体非常相似的字体属性指定，但被明确分类为复杂脚本字体。

    21.1.2.3.3 ea (东亚字体)

        此元素指定将东亚字体用于特定的文本运行。 该字体指定的字体属性与其他字体非常相似，但被明确分类为东亚字体。

    21.1.2.3.7 latin (拉丁字体)

        此元素指定将拉丁字体用于特定的文本运行。 该字体由与其他字体非常相似的字体属性指定，但被明确分类为拉丁字体。

    21.1.2.3.10 sym (符号字体)

        此元素指定用于特定文本运行的符号字体。 该字体由与其他字体非常相似的字体属性指定，但被专门分类为符号字体。

    21.1.2.4.6 buFont (特定字体)

        此元素指定给定段落内项目符号字符使用的字体。 字体是使用在生成应用程序中注册的字体来指定的。
    """

    @property
    def typeface(self) -> ST_TextTypeface:
        """文本字体名称

        Text Typeface

        指定要使用的字体或字体名称。 字体是渲染演示文稿时应使用的特定字体的字符串名称。 如果该字体在生成应用程序的字体列表中不可用，则应利用字体替换逻辑来选择替代字体。
        """

        val = self.attrib['typeface']

        val = utils.AnyStrToStr(val)  # type: ignore

        return ST_TextTypeface(val)

    @property
    def panose(self) -> Optional[s_ST_Panose]:
        """帕诺塞设置

        Panose Setting

        使用 ISO/IEC 14496-22 §5.2.7.17 中定义的机制指定当前字体的 Panose-1 分类号。
        """

        val = self.attrib.get('panose')

        if val is not None:
            return s_ST_Panose(val)

        return None

    @property
    def pitch_family(self) -> ST_PitchFamily:
        """类似字体家族

        Similar Font Family

        指定字体间距以及相应字体的字体系列.

        该信息是通过查询存在的字体来确定的，并且在字体不可用时不得修改。 该信息可用于字体替换逻辑，以在该字体不可用时找到适当的替换字体。
        """

        val = self.attrib.get('pitchFamily')

        if val is None:
            return ST_PitchFamily.DefaultPitchAndUnFmly  # 0x00

        return ST_PitchFamily(val)

    @property
    def charset(self) -> XSD_Byte:
        """相似的字符集

        Similar Character Set

        指定父字体支持的字符集。 该信息可用于字体替换逻辑，以在该字体不可用时找到适当的替换字体。 该信息是通过查询存在的字体来确定的，并且在字体不可用时不得修改。

        该属性的值应解释如下:

        - 0x00: 指定 ANSI 字符集. (IANA 名称 iso-8859-1)
        - 0x01: 指定默认字符集.
        - 0x02: 指定符号字符集。 该值指定应该使用字体的 Unicode 专用区域（U+FF00 到 U+FFFF）中的字符来显示 U+0000 到 U+00FF 范围内的字符。
        - 0x4D: 指定 Macintosh（标准罗马）字符集. (IANA 名称 macintosh)
        - 0x80: 指定 JIS 字符集. (IANA 名称 shift_jis)
        - 0x81: 指定朝鲜文字(Hangul)符集. (IANA 名称 ks_c_5601-1987)
        - 0x82: 指定 Johab 字符集. (IANA 名称 KS C-5601-1992)
        - 0x86: 指定 GB-2312 字符集. (IANA 名称 GBK)
        - 0x88: 指定中文大五字符集. (IANA name Big5)
        - 0xA1: 指定希腊字符集. (IANA 名称 windows-1253)
        - 0xA2: 指定土耳其语字符集. (IANA 名称 iso-8859-9)
        - 0xA3: 指定越南语字符集. (IANA 名称 windows-1258)
        - 0xB1: 指定希伯来语字符集. (IANA 名称 windows-1255)
        - 0xB2: 指定阿拉伯字符集. (IANA 名称 windows-1256)
        - 0xBA: 指定波罗的海字符集. (IANA 名称 windows-1257)
        - 0xCC: 指定俄语字符集. (IANA 名称 windows-1251)
        - 0xDE: 指定泰语字符集. (IANA 名称 windows-874)
        - 0xEE: 指定东欧字符集. (IANA 名称 windows1250)
        - 0xFF: 指定 ECMA-376 未定义的 OEM 字符集。
        - Any other value: 应用程序定义的，可以忽略。
        """

        val = self.attrib.get('charset')

        if val is None:
            return XSD_Byte(b'1')

        return to_xsd_byte(val)  # type: ignore


class ST_TextUnderlineType(ST_BaseEnumType):
    """文本下划线类型

    20.1.10.82 ST_TextUnderlineType

    指定了所使用的文本下划线类型。
    """

    none = 'none'
    """" 无 下划线 （即也不派生） """

    Words = 'words'
    """" 单词 下划线 """

    Sng = 'sng'
    """" 单线 """

    Dbl = 'dbl'
    """" 双线 """

    Heavy = 'heavy'
    """" 粗线 """

    Dotted = 'dotted'
    """" 点线 用普通粗细的点线为文本加下划线。"""

    DottedHeavy = 'dottedHeavy'
    """" 粗点线 """

    Dash = 'dash'
    """" 用普通粗细的单虚线为文本加下划线。 """

    DashHeavy = 'dashHeavy'
    """" 用粗虚线为文本加下划线。 """

    DashLong = 'dashLong'
    """" 用普通粗细的长虚线为文本加下划线。 """

    DashLongHeavy = 'dashLongHeavy'
    """" 用粗长虚线为文本加下划线。  """

    DotDash = 'dotDash'
    """" 用由点和虚线重复组成的普通粗细线为文本加下划线。 """

    DotDashHeavy = 'dotDashHeavy'
    """" 用由点和虚线重复组成的粗线为文本加下划线。 """

    DotDotDash = 'dotDotDash'
    """" 用由两个点和虚线重复组成的普通粗细线为文本加下划线。 """

    DotDotDashHeavy = 'dotDotDashHeavy'
    """" 用由两个点和虚线重复组成的粗线为文本加下划线。 """

    Wavy = 'wavy'
    """" 用普通粗细的波浪线为文本加下划线。 """

    WavyHeavy = 'wavyHeavy'
    """" 用粗波浪线为文本加下划线。 """

    WavyDbl = 'wavyDbl'
    """" 用普通粗细的双波浪线为文本加下划线。 """


class CT_TextUnderlineLineFollowText(OxmlBaseElement):
    """下划线跟随文本

    21.1.2.3.15 uLnTx

    此元素指定文本串的下划线的笔划样式应与其包含的文本串相同。
    """



class CT_TextUnderlineFillFollowText(OxmlBaseElement):
    """下划线填充属性跟随文本

    21.1.2.3.13 uFillTx

    此元素指定一段文本下划线的填充颜色应与包含该文本段的文本颜色相同。
    """



class CT_TextUnderlineFillGroupWrapper(EG_FillProperties):
    """下划线填充

    21.1.2.3.12 uFill

    该元素指定一段文本下划线的填充颜色。
    """

    @property
    def fill(
        self,
    ) -> Optional[
        CT_NoFillProperties | CT_SolidColorFillProperties | CT_GradientFillProperties | CT_BlipFillProperties | CT_PatternFillProperties | CT_GroupFillProperties
    ]:
        """填充类型

        <xsd:group ref="EG_FillProperties" minOccurs="1" maxOccurs="1"/>
        """

        return self.choice_require_one_child(*self.fill_pr_tags)  # type: ignore


class EG_TextUnderlineLine(OxmlBaseElement):
    """
    <xsd:group name="EG_TextUnderlineLine">
        <xsd:choice>
            <xsd:element name="uLnTx" type="CT_TextUnderlineLineFollowText"/>
            <xsd:element name="uLn" type="CT_LineProperties" minOccurs="0" maxOccurs="1"/>
        </xsd:choice>
    </xsd:group>
    """

    text_underline_line_tags = (
        qn('a:uLnTx'),  # CT_TextUnderlineLineFollowText
        qn('a:uLn'),  # CT_LineProperties
    )

    # Optional[Union[CT_TextUnderlineLineFollowText, CT_LineProperties]]


class EG_TextUnderlineFill(OxmlBaseElement):
    """
    <xsd:group name="EG_TextUnderlineFill">
        <xsd:choice>
            <xsd:element name="uFillTx" type="CT_TextUnderlineFillFollowText"/>
            <xsd:element name="uFill" type="CT_TextUnderlineFillGroupWrapper"/>
        </xsd:choice>
    </xsd:group>
    """

    text_underline_fill_tags = (
        qn('a:uFillTx'),  # CT_TextUnderlineFillFollowText
        qn('a:uFill'),  # CT_TextUnderlineFillGroupWrapper
    )

    # Union[CT_TextUnderlineFillFollowText, CT_TextUnderlineFillGroupWrapper]


class ST_TextStrikeType(ST_BaseEnumType):
    """文本删除线类型

    20.1.10.79 ST_TextStrikeType

    这个简单类型指定了删除线类型。

    这个简单类型被限制为以下表中列出的值:

    - dblStrike（文本删除线枚举（双删除线））: 文本上应用了双删除线
    - noStrike（文本删除线枚举（无删除线））: 文本上没有应用删除线
    - sngStrike（文本删除线枚举（单删除线））: 文本上应用了单删除线
    """

    NoStrike = 'noStrike'
    """文本上没有应用删除线"""

    SngStrike = 'sngStrike'
    """文本上应用了单删除线"""

    DblStrike = 'dblStrike'
    """文本上应用了双删除线"""


class ST_TextCapsType(ST_BaseEnumType):
    """文本大写类型

    20.1.10.64 ST_TextCapsType

    这个简单类型指定了文本的大写类型。
    """

    Null = 'none'
    """我们不能隐式地将noCaps设为未指定大写的场景，因为不指定意味着从特定样式派生，用户可能想要覆盖并使一些文本不具有大写方案，即使样式要求不同。
    """

    Small = 'small'
    """对文本应用小写。所有字母都转换为小写。"""

    All = 'all'
    """Text Caps Enum（全部）

    将全部文字转换为大写。即使它们在后台存储中以不同的方式存储，所有小写字母也会转换为大写。
    """


class CT_TextCharacterProperties(EG_FillProperties, EG_EffectProperties, EG_TextUnderlineFill, EG_TextUnderlineLine):
    """结束段落运行属性

    21.1.2.2.3 endParaRPr (End Paragraph Run Properties)

    此元素指定在指定的最后一个运行之后插入另一个运行时要使用的文本运行属性。
    这有效地保存了运行属性状态，以便在用户输入其他文本时可以应用它。
    如果省略此元素，则应用程序可以确定要应用哪些默认属性。
    建议在段落内的文本列表末尾指定此元素，以便维护有序列表。

    21.1.2.3.9 rPr (Text Run Properties)

    此元素包含包含段落内的文本运行的所有运行级别文本属性。

    21.1.2.3.2 defRPr (默认文本运行特性)

    此元素包含包含段落内的文本运行的所有默认运行级别文本属性。 当 rPr 元素中尚未定义覆盖属性时，将使用这些属性。

    """

    @property
    def line_properties(self) -> Optional[CT_LineProperties]:
        """线条特性(属性)

        20.1.2.2.24 ln

        此元素指定可应用于许多不同对象（例如形状和文本）的轮廓样式。 该
        线允许指定许多不同类型的轮廓，包括甚至线虚线和斜角。
        """
        return getattr(self, qn('a:ln'), None)

    @property
    def fill(
        self,
    ) -> Optional[
        CT_NoFillProperties | CT_SolidColorFillProperties | CT_GradientFillProperties | CT_BlipFillProperties | CT_PatternFillProperties | CT_GroupFillProperties
    ]:
        """填充样式

        <xsd:group ref="EG_FillProperties" minOccurs="0" maxOccurs="1"/>
        """

        return self.choice_one_child(*self.fill_pr_tags)  # type: ignore

    @property
    def effect(self) -> Optional[CT_EffectList | CT_EffectContainer]:
        """效果样式

        <xsd:group ref="EG_EffectProperties" minOccurs="0" maxOccurs="1"/>
        """

        return self.choice_one_child(*self.effect_pr_tags)  # type: ignore

    @property
    def highlight(self) -> Optional[CT_Color]:
        """高亮颜色

        21.1.2.3.4 highlight

        该元素指定一系列文本的突出显示颜色。
        """

        return getattr(self, qn('a:highlight'), None)

    @property
    def text_underline_line(
        self,
    ) -> Optional[CT_TextUnderlineLineFollowText | CT_LineProperties]:
        """下划线的线样式

        <xsd:group ref="EG_TextUnderlineLine" minOccurs="0" maxOccurs="1"/>
        """

        return self.choice_one_child(*self.text_underline_line_tags)  # type: ignore

    @property
    def text_underline_fill(
        self,
    ) -> Optional[CT_TextUnderlineFillFollowText | CT_TextUnderlineFillGroupWrapper]:
        """下划线的填充样式

        <xsd:group ref="EG_TextUnderlineLine" minOccurs="0" maxOccurs="1"/>
        """

        return self.choice_one_child(*self.text_underline_fill_tags)  # type: ignore

    @property
    def latin_font(self) -> Optional[CT_TextFont]:
        """拉丁字体

        21.1.2.3.7 latin

        此元素指定将拉丁字体用于特定的文本运行。 该字体由与其他字体非常相似的字体属性指定，但被明确分类为拉丁字体。
        """

        return getattr(self, qn('a:latin'), None)

    @property
    def ea_font(self) -> Optional[CT_TextFont]:
        """东亚字体

        21.1.2.3.3 ea

        此元素指定将东亚字体用于特定的文本运行。 该字体指定的字体属性与其他字体非常相似，但被明确分类为东亚字体。
        """
        return getattr(self, qn('a:ea'), None)

    @property
    def cs_font(self) -> Optional[CT_TextFont]:
        """复杂脚本字体

        21.1.2.3.1 cs

        该元素指定将复杂的脚本字体用于特定的文本运行。 该字体由与其他字体非常相似的字体属性指定，但被明确分类为复杂脚本字体。

        如果指定的字体在用于渲染的系统上不可用，则可以利用该元素的属性来选择替代字体。
        """
        return getattr(self, qn('a:cs'), None)

    @property
    def sym_font(self) -> Optional[CT_TextFont]:
        """符号字体

        21.1.2.3.10 sym

        此元素指定用于特定文本运行的符号字体。 该字体由与其他字体非常相似的字体属性指定，但被专门分类为符号字体。
        """
        return getattr(self, qn('a:sym'), None)

    @property
    def hlink_click(self) -> Optional[CT_Hyperlink]:
        """单击超链接

        21.1.2.3.5 hlinkClick

        指定要应用于一系列文本的单击超链接信息。 单击超链接文本时，将获取链接。
        """

        return getattr(self, qn('a:hlinkClick'), None)

    @property
    def hlink_mouse_over(self) -> Optional[CT_Hyperlink]:
        """鼠标悬停超链接

        21.1.2.3.6 hlinkMouseOver

        指定要应用于文本串的鼠标悬停超链接信息。 当鼠标悬停在此超链接文本上时，将获取链接。
        """
        return getattr(self, qn('a:hlinkMouseOver'), None)

    @property
    def rtl(self) -> Optional[CT_Boolean]:
        """Run从右向左

        21.1.2.2.8 rtl

        该元素指定该运行(run)的内容是否应具有从右到左的特征。 具体来说，当该元素的 val 属性为 true（或等效属性）时，将应用以下行为:

        - Formatting – 当显示本次运行的内容时，所有字符都将被视为复杂的脚本字符。 这意味着 cs 元素 ([§21.1.2.3.1]) 的值应用于确定字体。
        - Character Directionality Override – 当显示此运行的内容时，此属性充当按如下方式分类的字符的从右到左覆盖（使用 Unicode 字符数据库）:
            - 构成数字一部分时，除欧洲数字、欧洲数字终止符、普通数字分隔符、阿拉伯数字和（对于希伯来语文本）欧洲数字分隔符之外的弱类型
            - 中性类型 / Neutral types
        - [Rationale: 此覆盖允许应用程序存储和利用超出从 Unicode 双向算法隐式导出的信息的更高级别信息。 例如，如果字符串“第一秒”出现在文档内从右到左的段落中，则 Unicode 算法在显示时将始终导致“第一秒”（因为中性字符被强分类字符包围）。 但是，如果使用从右到左的输入法（例如希伯来语键盘）输入空格，则可以使用此属性将该字符分类为 RTL，从而允许以从右到左的方式显示“第二个第一” 段落，因为用户明确要求在从右到左的上下文中提供空格。 end rationale]

        此元素提供用于将单个字符的 (Unicode) 分类解析为 L、R、AN 或 EN 的信息。 一旦确定，该行的显示应遵循 Unicode 双向算法在重新排序已解析级别时的建议。

        此属性不得与强从左到右的文本一起使用。 该条件下的任何行为均未指定。 关闭此属性后，不应将其与强从右到左的文本一起使用。 该条件下的任何行为均未指定。

        如果此元素不存在，则默认值是保留样式层次结构中上一级别所应用的格式。 如果此元素从未应用于样式层次结构，则从右到左的特征不应应用于此运行的内容。
        """
        return getattr(self, qn('a:rtl'), None)

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)

    @property
    def kumimoji(self) -> Optional[XSD_Boolean]:
        """继续垂直

        指定垂直文本中包含的数字是否与文本垂直连续，或者是否水平显示而周围的字符继续垂直。 如果省略此属性，则假定值为 0 或 false。
        """

        val = self.attrib.get('kumimoji')

        if val is None:
            return None

        return to_xsd_bool(val)

    @property
    def language(self) -> Optional[s_ST_Lang]:
        """语言ID / Language ID

        指定生成应用程序显示用户界面控件时要使用的语言。 如果省略此属性，则生成应用程序可以选择其选择的语言。
        """
        val = self.attrib.get('lang')

        if val is None:
            return None

        return s_ST_Lang(utils.AnyStrToStr(val))  # type: ignore

    @property
    def alt_language(self) -> Optional[s_ST_Lang]:
        """替代语言 / Alternative Language

        指定生成应用程序显示用户界面控件时要使用的备用语言。 如果省略此属性，则此处使用 lang 属性。
        """
        val = self.attrib.get('altLang')

        if val is None:
            return None

        return s_ST_Lang(utils.AnyStrToStr(val))  # type: ignore

    @property
    def font_size(self) -> Optional[ST_TextFontSize]:
        """字体大小 / Font Size

        sz

        指定文本串中文本的大小。 整点以 100 为增量指定，从 100 开始，点大小为 1。

        例如，

        - 字体点大小 12 将是 1200，
        - 字体点大小 12.5 将是 1250。

        如果省略此属性，则比中的值 应使用 defRPr 中的值。
        """
        val = self.attrib.get('sz')

        if val is None:
            return None

        return to_ST_TextFontSize(str(val))

    @property
    def blod(self) -> Optional[XSD_Boolean]:
        """粗体 / Bold

        指定文本串是否设置为粗体文本。 如果省略此属性，则假定值为 0 或 false。
        """

        val = self.attrib.get('b')

        if val is None:
            return None

        return to_xsd_bool(val)

    @property
    def italic(self) -> Optional[XSD_Boolean]:
        """斜体 / Italics

        指定文本串是否设置为斜体文本格式。 如果省略此属性，则假定值为 0 或 false。
        """

        val = self.attrib.get('i')

        if val is None:
            return None

        return to_xsd_bool(val)

    @property
    def underline_type(self) -> Optional[ST_TextUnderlineType]:
        """下划线类型

        下划线 / Underline

        指定文本串的格式是否为带下划线的文本。 如果省略此属性，则假定没有下划线。
        """

        val = self.attrib.get('u')

        if val is None:
            return None

        return ST_TextUnderlineType(val)

    @property
    def strike(self) -> Optional[ST_TextStrikeType]:
        """删除线 / Strikethrough

        指定一系列文本的格式是否为删除线文本。 如果省略此属性，则假定没有删除线。
        """

        val = self.attrib.get('strike')

        if val is None:
            return None

        return ST_TextStrikeType(val)

    @property
    def kerning(self) -> Optional[ST_TextNonNegativePoint]:
        """字距调整

        Kerning

        指定在此文本运行中进行字符字距调整的最小字体大小。
        整点以 100 为增量指定，从 100 开始，点大小为 1。
        例如，字体点大小 12 将是 1200，字体点大小 12.5 将是 1250。
        如果省略此属性，则会出现字距调整 所有字体大小均降至 0 磅字体。
        """
        val = self.attrib.get('kern')

        if val is None:
            return None

        return to_ST_TextNonNegativePoint(str(val))

    @property
    def capitalization(self) -> Optional[ST_TextCapsType]:
        """大写

        Capitalization

        指定要应用于文本串的大写。 这是仅渲染的修改，不会影响存储在文本运行中的实际字符。
        此属性也不同于切换功能，在切换功能中，存储在文本串中的实际字符会发生更改。
        """

        val = self.attrib.get('cap')

        if val is None:
            return None

        return ST_TextCapsType(val)

    @property
    def spacing(self) -> Optional[ST_TextPoint]:
        """间距 字符间距

        Spacing

        指定文本串中字符之间的间距。 此间距以数字形式指定，并且应由生成应用程序在整个文本运行中一致应用。
        整点以 100 为增量指定，从 100 开始，点大小为 1。例如，字体点大小 12 将是 1200，字体点大小 12.5 将是 1250。

        如果省略此属性，则值为 0 或者假设没有调整。
        """

        val = self.attrib.get('spc')

        if val is None:
            return None

        return to_ST_TextPoint(str(val))

    @property
    def normalize_heights(self) -> Optional[XSD_Boolean]:
        """标准化高度

        Normalize Heights

        指定是否已检查文本运行中的智能标记。 此属性的作用与用于检查拼写、语法等的 dirty 属性剂量非常相似。
        此处的 true 值指示生成应用程序应检查此文本运行是否有智能标记。 如果省略此属性，则假定值为 0 或 false。
        """

        val = self.attrib.get('normalizeH')

        if val is None:
            return None

        return to_xsd_bool(val)

    @property
    def baseline(self) -> Optional[ST_Percentage]:
        """基线

        Baseline

        指定上标和下标字体的基线。 使用百分比指定大小，其中 1% 等于字体大小的 1%，100% 等于字体大小的 100%。
        """

        val = self.attrib.get('baseline')

        if val is None:
            return None

        return to_ST_Percentage(str(val))

    @property
    def no_proof(self) -> Optional[XSD_Boolean]:
        """无需打样

        No Proofing

        指定用户已选择不检查错误的一系列文本。 因此，如果文本中存在拼写、语法等错误，生成应用程序应忽略它们。
        """

        val = self.attrib.get('noProof')

        if val is None:
            return None

        return to_xsd_bool(val)

    @property
    def dirty(self) -> XSD_Boolean:
        """标记为脏数据

        Dirty

        指定自上次运行校对工具以来文本运行的内容已更改。 实际上，这会标记要由生成应用程序再次检查拼写、语法等错误的文本。
        """

        val = self.attrib.get('dirty')

        return to_xsd_bool(val, none=True)

    @property
    def error(self) -> XSD_Boolean:
        """拼写错误

        Spelling Error

        指定当检查该文本运行的拼写、语法等时确实发现了错误。 这允许生成应用程序有效地保存文档内的错误状态，而不必在打开文档时执行全通过检查。
        """

        val = self.attrib.get('err')

        return to_xsd_bool(val, none=False)

    @property
    def smart_clean(self) -> XSD_Boolean:
        """智能标签清洁

        SmartTag Clean

        指定是否已检查文本运行中的智能标记。 此属性的作用与用于检查拼写、语法等的 dirty 属性剂量非常相似。
        此处的 true 值指示生成应用程序应检查此文本运行是否有智能标记。
        如果省略此属性，则假定值为 0 或 false。
        """

        val = self.attrib.get('smtClean')

        return to_xsd_bool(val, none=True)

    @property
    def smart_id(self) -> Optional[int]:
        """智能标签 ID

        SmartTag ID

        指定一系列文本的智能标记标识符。 该ID在整个演示过程中是唯一的，用于引用有关智能标签的相应辅助信息。
        [注意: 有关智能标记的完整定义（在整个 Office Open XML 中语义相同），请参阅§17.5.1。 ]
        """

        val = self.attrib.get('smtId')

        if val is None:
            return 0

        return utils.XsdUnsignedInt(val)

    @property
    def bookmark(self) -> Optional[str]:
        """书签链接目标

        Bookmark Link Target

        指定用于引用文档内自定义 XML 部件中正确链接属性的链接目标名称。
        """

        val = self.attrib.get('bmk')

        if val is None:
            return None

        return utils.AnyStrToStr(val)  # type: ignore


class CT_Boolean(OxmlBaseElement):
    """
    aaaa
    """

    @property
    def value(self) -> s_ST_OnOff:
        val = self.attrib.get('val')

        if val is None:
            return s_ST_OnOff.Zero

        return s_ST_OnOff(val)


ST_TextSpacingPoint = NewType('ST_TextSpacingPoint', int)
"""文本字体间距点

20.1.10.78 ST_TextSpacingPoint (Text Spacing Point)

此简单类型指定根据字体点大小使用的文本间距。

这个简单类型还指定了以下限制:

- 此简单类型的最小值大于或等于 0。
- 此简单类型的最大值小于或等于 158400。

"""


def to_ST_TextSpacingPoint(val: str):
    """转换为文本点大小的固定值"""

    pyval = int(val)

    if not (0 <= pyval <= 158400):
        msg = f'预期外的值: {val}'
        raise OxmlAttributeValidateError(msg)

    return ST_TextSpacingPoint(int(pyval))  # 以xx磅为单位


class ST_TextSpacingPercent(ST_BaseType[AnyStr, int]):
    """
    aaa
    """

    def _validate(self: Self) -> None:
        value = int(utils.AnyStrToStr(self._val))

        if not (0 <= value <= 13200000):
            msg = f'预期外的值: {value}'
            raise OxmlAttributeValidateError(msg)

        self._python_val = value


ST_TextSpacingPercentOrPercentString = NewType('ST_TextSpacingPercentOrPercentString', float)
"""文本字体间距百分比

20.1.10.77 ST_TextSpacingPercentOrPercentString (Text Spacing Percent)

此简单类型指定其内容将包含文本字体间距百分比。 有关详细信息，请参阅工会的成员类型。

这个简单类型是以下类型的联合:

- ST_Percentage 简单类型（第 22.9.2.9 节）。

<xsd:union memberTypes="ST_TextSpacingPercent s:ST_Percentage"/>
"""


def to_ST_TextSpacingPercentOrPercentString(
    val: str,
) -> ST_TextSpacingPercentOrPercentString:
    # 200%
    if val.endswith('%'):
        pyval = int(val[:-1]) / 100

    # <a:spcPct val="90000"/>
    else:
        pyval = to_ST_Percentage(val)

    return ST_TextSpacingPercentOrPercentString(pyval)


class CT_TextSpacingPercent(OxmlBaseElement):
    """百分比间距

    21.1.2.2.11 spcPct (Spacing Percent)

    此元素以文本大小的百分比形式指定行和段落之间要使用的空白量。
    此处用于计算间距的文本大小是每次运行的文本，最大的文本大小优先。
    也就是说，如果有一串 10 磅字体的文本，并且在同一行的同一段落内有一串 12 磅字体大小的文本，则应使用 12 磅来计算要使用的间距。
    """

    @property
    def value(self) -> ST_TextSpacingPercentOrPercentString:
        """值

        Value

        指定空白应占大小的百分比。
        """
        val = self.attrib['val']

        return to_ST_TextSpacingPercentOrPercentString(str(val))


class CT_TextSpacingPoint(OxmlBaseElement):
    """点间距

    21.1.2.2.12 spcPts (Spacing Points)

    此元素以文本点大小的形式指定行和段落之间要使用的空白量。
    大小使用点指定，其中 100 等于 1 点字体，1200 等于 12 点字体。

    This element specifies the amount of white space that is to be used between lines and paragraphs in the form of a text point size.
    The size is specified using points where 100 is equal to 1 point font and 1200 is equal to 12 point.
    """

    @property
    def value(self) -> ST_TextSpacingPoint:
        """值

        Value

        以磅值指定空白区域的大小。 整点以 100 为增量指定，从 100 开始，点大小为 1。
        例如，字体点大小 12 将是 1200，字体点大小 12.5 将是 1250。

        Specifies the size of the white space in point size. Whole points are specified in increments of 100 starting with 100 being a point size of 1. For instance a font point size of 12 would be 1200 and a font point size of 12.5 would be 1250.
        """
        val = self.attrib['val']

        return to_ST_TextSpacingPoint(str(val))


ST_TextMargin = NewType('ST_TextMargin', int)
"""文本边距

20.1.10.72 ST_TextMargin (Text Margin)

这个简单类型指定所使用的边距及其相应的大小。

这个简单类型还指定了以下限制:

- 此简单类型的最小值大于或等于 0。

- 此简单类型的最大值小于或等于 51206400。

"""


def to_ST_TextMargin(_val: AnyStr) -> ST_TextMargin:
    val = int(utils.AnyStrToStr(_val))

    if not (0 <= val <= 51206400):
        msg = f'预期外的值: {val}'
        raise OxmlAttributeValidateError(msg)

    return ST_TextMargin(val)


ST_TextIndent = NewType('ST_TextIndent', int)
"""文本缩进

20.1.10.70 ST_TextIndent (Text Indentation)

这个简单类型指定要使用的文本缩进量。

这里使用的测量单位是 EMU（英制公制单位）。

此简单类型的内容是 ST_Cooperative32Unqualified 数据类型 (§20.1.10.18) 的限制。

这个简单类型还指定了以下限制:

- 此简单类型的最小值大于或等于 -51206400。

- 此简单类型的最大值小于或等于 51206400。
"""


def to_ST_TextIndent(_val: AnyStr) -> ST_TextIndent:
    val = int(utils.AnyStrToStr(_val))

    if not (-51206400 <= val <= 51206400):
        msg = f'预期外的值: {val}'
        raise OxmlAttributeValidateError(msg)

    return ST_TextIndent(val)


class ST_TextTabAlignType(ST_BaseEnumType):
    """文本制表符对齐类型

    20.1.10.80 ST_TextTabAlignType (Text Tab Alignment Types)

    这个简单类型指定了文本制表符对齐类型。

    这个简单类型的内容是对W3C XML Schema令牌数据类型的限制。

    这个简单类型被限制为以下表中列出的值：

    ctr（文本制表符对齐枚举（居中））

        这个制表位上的文本是居中对齐的。

    dec（文本制表符对齐枚举（小数））

        在这个制表位上，小数点对齐。从用户的角度来看，这里的文本行为类似于右对齐，直到小数点，然后在小数点后就是左对齐。

    l（文本制表符对齐枚举（左））

        这个制表位上的文本是左对齐的。

    r（文本制表符对齐枚举（右））

        这个制表位上的文本是右对齐的。

    """

    Left = 'l'
    """这个制表位上的文本是左对齐的。"""

    Center = 'ctr'
    """这个制表位上的文本是居中对齐的。"""

    Right = 'r'
    """这个制表位上的文本是右对齐的。"""

    Decimal = 'dec'
    """在这个制表位上，小数点对齐。从用户的角度来看，这里的文本行为类似于右对齐，直到小数点，然后在小数点后就是左对齐。"""


class CT_TextTabStop(OxmlBaseElement):
    """制表位

    21.1.2.2.13 tab

    当文本中存在一个或多个制表符时，此元素指定在一行文本上使用的单个制表位。 当存在多个时，应按通过 pos 属性指定的递增位置顺序使用它们。
    """

    @property
    def position(self) -> Optional[ST_Coordinate32]:
        """tab位置

        Tab Position

        指定制表位相对于左边距的位置。 如果省略此属性，则使用应用程序默认的制表位。
        """
        val = self.attrib.get('pos')

        if val is None:
            return None

        return to_ST_Coordinate32(val)  # type: ignore

    @property
    def align(self) -> Optional[ST_TextTabAlignType]:
        """tab对齐方式

        Tab Alignment

        使用此制表位指定要应用于文本的对齐方式。 如果省略此属性，则应用程序默认为生成应用程序。
        """
        val = self.attrib.get('algn')

        if val is None:
            return None

        return ST_TextTabAlignType(val)


class CT_TextTabStopList(OxmlBaseElement):
    """制表位列表 tabLst

    21.1.2.2.14 tabLst

    此元素指定要在段落中使用的所有制表位的列表。 在描述文档中的任何自定义制表位时应使用这些制表符。 如果未指定这些，则应使用生成应用程序的默认制表位。
    """

    @property
    def tabs(self) -> list[CT_TextTabStop]:
        """制表位

        21.1.2.2.13 tab

        当文本中存在一个或多个制表符时，此元素指定在一行文本上使用的单个制表位。 当存在多个时，应按通过 pos 属性指定的递增位置顺序使用它们。
        """

        text_tabs = self.findall(qn('a:tab'))

        if len(text_tabs) > 32:
            msg = '元素数量超出逾期'
            raise OxmlElementValidateError(msg)

        return text_tabs  # type: ignore


class CT_TextLineBreak(OxmlBaseElement):
    """文本换行

    21.1.2.2.1 br

        此元素指定段落内两行文本之间是否存在垂直换行符。 除了指定两次文本之间的垂直间距之外，此元素还可以具有通过 rPr 子元素指定的运行(run)特性。 这设置了换行符的文本格式，以便以后在此处插入文本时可以使用正确的格式生成新的运行(run)。
    """

    @property
    def text_character_pr(self) -> Optional[CT_TextCharacterProperties]:
        return getattr(self, qn('a:rPr'), None)


class CT_TextSpacing(OxmlBaseElement):
    """文本间距

    21.1.2.2.5 lnSpc (Line Spacing)

    此元素指定段落内要使用的垂直行距。
    这可以通过两种不同的方式指定: 百分比间距和字体点间距。
    如果省略此元素，则两行文本之间的间距应由一行内最大文本片段的磅值确定。

    21.1.2.2.9 spcAft (Space After)

    该元素指定段落之后出现的垂直空白量。该间距通过子元素 spcPct 和 spcPts 以百分比或点数指定。

    21.1.2.2.10 spcBef (Space Before)

    此元素指定段落之前存在的垂直空白量。该间距通过子元素 spcPct 和 spcPts 以百分比或点数指定。
    """

    @property
    def spacing(self) -> CT_TextSpacingPercent | CT_TextSpacingPoint:
        """间距

        百分比间距 / 字体点间距
        """

        tags = (
            qn('a:spcPct'),  # CT_TextSpacingPercent
            qn('a:spcPts'),  # CT_TextSpacingPoint
        )

        return self.choice_require_one_child(*tags)  # type: ignore


class ST_TextAlignType(ST_BaseEnumType):
    """文本对齐类型

    - ctr（文本对齐枚举（居中））: 将文本居中对齐。
    - dist（文本对齐枚举（分布式））: 将文本单词分布在整个文本行上。
    - just（文本对齐枚举（两端对齐））: 使文本在整行上两端对齐。它是智能的，不会对短句进行两端对齐。
    - justLow（文本对齐枚举（调整低））: 使用调整后的Kashida长度对阿拉伯文本进行对齐。
    - l（文本对齐枚举（左对齐））: 将文本与左边距对齐。
    - r（文本对齐枚举（右对齐））: 将文本与右边距对齐。
    - thaiDist（文本对齐枚举（泰语分布式））: 特别分布泰文文本，因为每个字符都被视为一个单词。
    """

    Left = 'l'
    """ Left  将文本与左边距对齐。"""

    Center = 'ctr'
    """ Center  将文本居中对齐。"""

    Right = 'r'
    """ Right  将文本与右边距对齐。"""

    Justify = 'just'
    """ Justified  使文本在整行上两端对齐。它是智能的，不会对短句进行两端对齐。"""

    JustLow = 'justLow'
    """ Justified Low  使用调整后的Kashida长度对阿拉伯文本进行对齐。"""

    Dist = 'dist'
    """ Distributed  将文本单词分布在整个文本行上。"""

    ThaiDist = 'thaiDist'
    """ Thai Distributed  特别分布泰文文本，因为每个字符都被视为一个单词。"""


class ST_TextFontAlignType(ST_BaseEnumType):
    """文本字体对齐方式

    20.1.10.66 ST_TextFontAlignType

    这个简单类型指定了不同类型的字体对齐方式。
    """

    Auto = 'auto'
    """当文本流是水平或简单垂直时，与字体基线相同，但对于其他垂直模式，与字体中心相同。"""

    Top = 't'
    """字母锚定在单行的顶部基线上。"""

    Center = 'ctr'
    """字母锚定在单行的两个基线之间。"""

    Base = 'base'
    """字母锚定在单行的底部基线上。"""

    Bottom = 'b'
    """字母锚定在单行的底部。这与底部基线不同，因为包括字母 "g," "q," "y," 等。"""


class ST_TextIndentLevelType(int):
    """文本缩进级别类型

    20.1.10.71 ST_TextIndentLevelType

    这个简单类型指定缩进级别类型。我们支持列表级别从0到8，并使用-1和-2表示仅应存在于内存中的大纲模式级别。

    此简单类型还指定了以下限制:

        - 该简单类型的最小值大于或等于0。
        - 该简单类型的最大值小于或等于8。

    """



class CT_TextParagraphProperties(EG_TextBulletColor, EG_TextBulletSize, EG_TextBulletTypeface, EG_TextBullet):
    """文本段落属性

    21.1.2.2.7 pPr (Text Paragraph Properties)

    此元素包含包含段落的所有段落级别文本属性。 这些段落属性应覆盖与相关段落关联的所有冲突属性。

    [注意: 要解决冲突的段落属性，应首先从 pPr 元素开始检查段落属性的线性层次结构。
    这里的规则是在更接近实际文本的级别定义的属性应优先。
    也就是说，如果 pPr 和 lvl1pPr 元素之间存在冲突属性，则 pPr 属性应优先，
    因为在属性层次结构中它更接近所表示的实际文本。 ]
    """

    @property
    def line_spacing(self) -> Optional[CT_TextSpacing]:
        """行间距

        21.1.2.2.5 lnSpc (Line Spacing)

        此元素指定段落内要使用的垂直行距。
        这可以通过两种不同的方式指定: 百分比间距和字体点间距。
        如果省略此元素，则两行文本之间的间距应由一行内最大文本片段的磅值确定。
        """

        return getattr(self, qn('a:lnSpc'), None)

    @property
    def spacing_before(self) -> Optional[CT_TextSpacing]:
        """段前间距

        21.1.2.2.10 spcBef (Space Before)

        此元素指定段落之前存在的垂直空白量。该间距通过子元素 spcPct 和 spcPts 以百分比或点数指定。
        """

        return getattr(self, qn('a:spcBef'), None)

    @property
    def spacing_after(self) -> Optional[CT_TextSpacing]:
        """段后间距

        21.1.2.2.9 spcAft (Space After)

        该元素指定段落之后出现的垂直空白量。该间距通过子元素 spcPct 和 spcPts 以百分比或点数指定。
        """

        return getattr(self, qn('a:spcAft'), None)

    @property
    def text_bullet_color(
        self,
    ) -> Optional[CT_TextBulletColorFollowText | CT_Color]:
        """项目列表符号颜色类型

        21.1.2.4.4 buClr (指定颜色) -> CT_Color

            此元素指定给定段落中项目符号字符使用的颜色。 使用数字 RGB 颜色格式指定颜色。

        21.1.2.4.5 buClrTx (跟随文字)

            此元素指定段落项目符号的颜色应与包含每个项目符号的文本颜色相同。

        <xsd:group ref="EG_TextBulletColor" minOccurs="0" maxOccurs="1"/>
        """

        return self.choice_one_child(*self.text_bullet_color_tags)  # type: ignore

    @property
    def text_bullet_size(
        self,
    ) -> Optional[
        CT_TextBulletSizeFollowText | CT_TextBulletSizePercent | CT_TextBulletSizePoint
    ]:
        """项目列表符号大小

        <xsd:group ref="EG_TextBulletSize" minOccurs="0" maxOccurs="1"/>
        """

        return self.choice_one_child(*self.text_bullet_size_tags)  # type: ignore

    @property
    def text_bullet_typeface(
        self,
    ) -> Optional[CT_TextBulletTypefaceFollowText | CT_TextFont]:
        """项目列表符号字体

        <xsd:group ref="EG_TextBulletTypeface" minOccurs="0" maxOccurs="1"/>
        """

        return self.choice_one_child(*self.text_bullet_typeface_tags)  # type: ignore

    @property
    def text_bullet(
        self,
    ) -> Optional[
        CT_TextNoBullet | CT_TextAutonumberBullet | CT_TextCharBullet | CT_TextBlipBullet
    ]:
        """项目列表符号类型

        <xsd:group ref="EG_TextBullet" minOccurs="0" maxOccurs="1"/>
        """

        return self.choice_one_child(*self.text_bullet_tags)  # type: ignore

    @property
    def tab_lst(self) -> Optional[CT_TextTabStopList]:
        """制表位列表 tabLst

        21.1.2.2.14 tabLst

        此元素指定要在段落中使用的所有制表位的列表。 在描述文档中的任何自定义制表位时应使用这些制表符。 如果未指定这些，则应使用生成应用程序的默认制表位。
        """

        return getattr(self, qn('a:tabLst'), None)

    @property
    def default_RPr(self) -> Optional[CT_TextCharacterProperties]:
        """默认文本运行特性

        21.1.2.3.2 defRPr

        此元素包含包含段落内的文本运行的所有默认运行级别文本属性。 当 rPr 元素中尚未定义覆盖属性时，将使用这些属性。
        """

        return getattr(self, qn('a:defRPr'), None)

    @property
    def ext_lst(self) -> Optional[CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('a:extLst'), None)

    @property
    def margin_left(self) -> Optional[ST_TextMargin]:
        """左边距

        Left Margin

        指定段落的左边距。 这是除了文本正文插入之外指定的，并且仅适用于该文本段落。
        也就是说，文本正文插入和 marL 属性相对于文本位置是相加的。
        如果省略此属性，则隐含值 347663。
        """
        val = self.attrib.get('marL')

        if val is not None:
            return to_ST_TextMargin(val)  # type: ignore

        return None

    @property
    def margin_right(self) -> Optional[ST_TextMargin]:
        """右边距

        Right Margin

        指定段落的右边距。 这是除了文本正文插入之外指定的，并且仅适用于该文本段落。
        也就是说，文本正文插入和 marR 属性相对于文本位置是相加的。
        如果省略该属性，则隐含值为 0。
        """
        val = self.attrib.get('marR')

        if val is not None:
            return to_ST_TextMargin(val)  # type: ignore

        return None

    @property
    def level(self) -> Optional[ST_TextIndentLevelType]:
        """级别

        Level

        指定该段落所遵循的特定级别文本属性。
        此属性的值为数字，并根据 lstStyle 元素中列出的相应级别段落属性来设置文本格式。
        由于定义了九个单独的级别属性，因此该标记的有效范围为 0-8 = 9 个可用值。

        """

        val = self.attrib.get('lvl')

        if val is not None:
            return ST_TextIndentLevelType(val)

        return None

    @property
    def indent(self) -> Optional[ST_TextIndent]:
        """缩进

        Indent

        指定应用于段落中第一行文本的缩进大小。 缩进 0 被认为与 marL 属性位于同一位置。 如果省略此属性，则隐含值 -342900。
        """
        val = self.attrib.get('indent')

        if val is not None:
            return to_ST_TextIndent(val)  # type: ignore

        return None

    @property
    def alignment(self) -> Optional[ST_TextAlignType]:
        """对齐方式

        Alignment

        指定要应用于段落的对齐方式。 可能的值包括左、右、居中、对齐和分布。 如果省略此属性，则隐含 left 值。
        """
        val = self.attrib.get('algn')

        if val is not None:
            return ST_TextAlignType(val)

        return ST_TextAlignType.Left

    @property
    def default_tab_size(self) -> Optional[ST_Coordinate32]:
        """默认制表符大小

        Default Tab Size

        指定该段落中制表符的默认大小。 该属性应用于描述段落内制表符的间距，而不是前导缩进制表符。
        对于缩进选项卡，有 marL 和 indent 属性可以帮助实现这一点。
        """
        val = self.attrib.get('defTabSz')

        if val is not None:
            return to_ST_Coordinate32(val)  # type: ignore

        return None

    @property
    def right_to_left(self) -> Optional[XSD_Boolean]:
        """从右到左

        Right To Left

        指定文本的流动方向是从右到左还是从左到右。 如果省略此属性，则隐含值 0 或从左到右。
        """
        val = self.attrib.get('rtl')

        if val is not None:
            return to_xsd_bool(val)

        return None

    @property
    def ea_line_break(self) -> Optional[XSD_Boolean]:
        """东亚字体行折断

        East Asian Line Break

        指定是否可以将东亚单词分成两半并换行到下一行而不添加连字符。
        为了确定东亚单词是否可以被分解，演示应用程序将使用此处的避头尾设置。
        当某个单词不能在没有连字符的情况下分成多个部分时，专门使用此属性。
        也就是说，它不存在于正常的可分解东亚单词的存在中，但是当出现不应因换行而被分解的特殊情况单词时出现。
        如果省略此属性，则隐含值 1 或 true。
        """
        val = self.attrib.get('eaLnBrk')

        if val is not None:
            return to_xsd_bool(val)

        return None

    @property
    def font_align(self) -> Optional[ST_TextFontAlignType]:
        """字体对齐类型

        Font Alignment

        确定实际单词在文本行上的垂直位置。 这涉及字符相对于基线的垂直放置。
        例如，将文本锚定到顶部基线、锚定到底部基线、居中等。要了解此属性及其用途，了解什么是基线将很有帮助。
        描述这些不同情况的图表如下所示。 如果省略此属性，则隐含 base 值。
        """
        val = self.attrib.get('fontAlgn')

        if val is not None:
            return ST_TextFontAlignType(val)

        return None

    @property
    def latin_line_break(self) -> Optional[XSD_Boolean]:
        """拉丁字体行折断

        Latin Line Break

        指定是否可以将拉丁语单词分成两半并换行到下一行而不添加连字符。
        当某个单词不能在没有连字符的情况下分成多个部分时，专门使用此属性。
        它不存在于正常的可分解拉丁单词中，但当出现特殊情况单词时，不应因换行而被分解。
        如果省略此属性，则隐含值 1 或 true。
        """
        val = self.attrib.get('latinLnBrk')

        if val is not None:
            return to_xsd_bool(val)

        return None

    @property
    def hanging_punct(self) -> Optional[XSD_Boolean]:
        """悬挂标点符号

        Hanging Punctuation

        指定标点符号是强制放置在文本行上还是放置在不同的文本行上。
        也就是说，如果一串文本末尾有标点符号，应该将其转移到单独的行，那么它实际上会被转移。
        true 值允许悬挂标点符号，强制标点符号不被保留，而 false 值允许标点符号被保留到下一个文本行。
        如果省略此属性，则隐含值 0 或 false。
        """
        val = self.attrib.get('hangingPunct')

        if val is not None:
            return to_xsd_bool(val)

        return None


class CT_TextField(OxmlBaseElement):
    """文本字段(域)

    21.1.2.2.4 fld (Text Field)

    该元素指定一个文本字段，其中包含应用程序应定期更新的生成文本。
    每一段文本在生成时都会被赋予一个唯一的标识号，用于引用特定的字段。
    创建时，文本字段指示应用于更新该字段的文本类型。
    使用此更新类型是为了使所有未创建此文本字段的应用程序仍然可以知道应使用哪种类型的文本进行更新。
    因此，新应用程序可以将更新类型附加到文本字段 id 以进行持续更新。
    """

    @property
    def text_character_pr(self) -> Optional[CT_TextCharacterProperties]:
        """文本运行属性"""

        return getattr(self, qn('a:rPr'), None)

    @property
    def text_paragraph_pr(self) -> Optional[CT_TextParagraphProperties]:
        """文本段落属性"""

        return getattr(self, qn('a:pPr'), None)

    @property
    def t(self) -> str:
        """文本"""

        ele = self.find(qn('a:t'))

        if ele is not None:
            return ele.text or ''

        return ''

    @property
    def id(self) -> s_ST_Guid:
        """字段ID

        Field ID

        指定此文档唯一的、主机指定的用于标识字段的标记。
        该标记在创建文本字段时生成，并作为相同标记保留在文件中，直到删除文本字段。
        任何应用程序都应在将新标记分配给文本字段之前检查文档是否存在冲突标记。
        """
        val = self.attrib['id']

        return s_ST_Guid(utils.AnyStrToStr(val))  # type: ignore

    @property
    def type(self) -> Optional[str]:
        """文本类型

        Field Type

        指定应用于更新此文本字段的文本类型。
        这用于通知渲染应用程序应该使用什么文本来更新此文本字段。
        此属性没有特定的语法限制。 生成应用程序可以使用它来表示在渲染演示文稿之前应更新的任何文本。

        保留值:

        slidenum - 演示幻灯片编号(presentation slide number)

        datetime - 渲染应用程序的默认日期时间格式(default date time format for the rendering application)

        datetime1 - MM/DD/YYYY 日期时间格式 [示例: 10/12/2007 ] (MM/DD/YYYY date time format [Example: 10/12/2007 end example])

        datetime2 - Day, Month DD, YYYY 日期时间格式 [示例: Friday, October 12, 2007 ] (Day, Month DD, YYYY date time format [Example: Friday, October 12, 2007 end example])

        datetime3 - DD Month YYYY 日期时间格式 [示例: 12 October 2007 ]

        datetime4 - Month DD, YYYY 日期时间格式 [示例: October 12, 2007 ]

        datetime5 - DD-Mon-YY 日期时间格式 [示例: 12-Oct-07 ]

        datetime6 - Month YY 日期时间格式 [示例: October 07 ]

        datetime7 - Mon-YY 日期时间格式 [示例: Oct-07 ]

        datetime8 - MM/DD/YYYY hh:mm AM/PM 日期时间格式 [示例: 10/12/2007 4:28 PM ]

        datetime9 - MM/DD/YYYY hh:mm:ss AM/PM 日期时间格式 [示例: 10/12/2007 4:28:34 PM ]

        datetime10 - hh:mm 日期时间格式 [示例: 16:28 ]

        datetime11 - hh:mm:ss 日期时间格式 [示例: 16:28:34 ]

        datetime12 - hh:mm AM/PM 日期时间格式 [示例: 4:28 PM ]

        datetime13 - hh:mm:ss: AM/PM 日期时间格式 [示例: 4:28:34 PM ]
        """
        val = self.attrib['type']

        if val is None:
            return None

        return utils.AnyStrToStr(val)  # type: ignore


class CT_RegularTextRun(OxmlBaseElement):
    """系列文本

    21.1.2.3.8 r (Text Run)

    该元素指定包含文本正文中是否存在一系列文本。 run 元素是文本正文中最低级别的文本分隔机制。
    文本运行可以包含与该运行关联的文本运行属性。
    如果未列出任何属性，则使用 defRPr 元素中指定的属性。

    例如:

    <a:r>
        <a:rPr b="1"></a:rPr>
        <a:t>Some text</a:t>
    </a:r>
    """

    @property
    def text_character_pr(self) -> Optional[CT_TextCharacterProperties]:
        """文本属性

        21.1.2.3.9 rPr (Text Run Properties)

        此元素包含包含段落内的文本运行的所有运行级别文本属性。

        例如:

        <a:rPr u="sng"/>
        """
        return getattr(self, qn('a:rPr'), None)

    @property
    def t(self) -> str:
        """文本字符串

        21.1.2.3.11 t (Text String)

        此元素指定此文本运行的实际文本。 这是使用所有指定的正文、段落和运行属性格式化的文本。 该元素应出现在一系列文本中。
        """

        ele = self.find(qn('a:t'))

        if ele is not None:
            return ele.text or ''

        return ''


# ----------------------------------------------------------------------------

dml_main_namespace = lookup.get_namespace(namespace_a)
dml_main_namespace[None] = OxmlBaseElement

# <xsd:element name="t" type="xsd:string" minOccurs="0" maxOccurs="1"/>
# <a:t>Sample Text</a:t>
dml_main_namespace['t'] = OxmlBaseElement

# 公共元素:
dml_main_namespace['extLst'] = CT_OfficeArtExtensionList
dml_main_namespace['st'] = CT_AudioCDTime
dml_main_namespace['end'] = CT_AudioCDTime
dml_main_namespace['audioCd'] = CT_AudioCD
dml_main_namespace['wavAudioFile'] = CT_EmbeddedWAVAudioFile
dml_main_namespace['audioFile'] = CT_AudioFile
dml_main_namespace['videoFile'] = CT_VideoFile
dml_main_namespace['quickTimeFile'] = CT_QuickTimeFile

dml_main_namespace['dk1'] = CT_Color
dml_main_namespace['lt1'] = CT_Color
dml_main_namespace['dk2'] = CT_Color
dml_main_namespace['lt2'] = CT_Color
dml_main_namespace['accent1'] = CT_Color
dml_main_namespace['accent2'] = CT_Color
dml_main_namespace['accent3'] = CT_Color
dml_main_namespace['accent4'] = CT_Color
dml_main_namespace['accent5'] = CT_Color
dml_main_namespace['accent6'] = CT_Color
dml_main_namespace['hlink'] = CT_Color
dml_main_namespace['folHlink'] = CT_Color

dml_main_namespace['custClr'] = CT_CustomColor
dml_main_namespace['latin'] = CT_TextFont
dml_main_namespace['ea'] = CT_TextFont
dml_main_namespace['cs'] = CT_TextFont
dml_main_namespace['sym'] = CT_TextFont

# pml 冲突 父级类型: CT_EmbeddedFontListEntry
dml_main_namespace['font'] = CT_SupplementalFont
dml_main_namespace['rtl'] = CT_Boolean

dml_main_namespace['scene3d'] = CT_Scene3D
dml_main_namespace['sp3d'] = CT_Shape3D

dml_main_namespace['majorFont'] = CT_FontCollection
dml_main_namespace['minorFont'] = CT_FontCollection

dml_main_namespace['ln'] = CT_LineProperties
dml_main_namespace['effectStyle'] = CT_EffectStyleItem

dml_main_namespace['fillStyleLst'] = CT_FillStyleList
dml_main_namespace['lnStyleLst'] = CT_LineStyleList
dml_main_namespace['effectStyleLst'] = CT_EffectStyleList
dml_main_namespace['bgFillStyleLst'] = CT_BackgroundFillStyleList

dml_main_namespace['clrScheme'] = CT_ColorScheme
dml_main_namespace['fontScheme'] = CT_FontScheme
dml_main_namespace['fmtScheme'] = CT_StyleMatrix

dml_main_namespace['tint'] = CT_PositiveFixedPercentage
dml_main_namespace['shade'] = CT_PositiveFixedPercentage
dml_main_namespace['comp'] = CT_ComplementTransform
dml_main_namespace['inv'] = CT_InverseTransform
dml_main_namespace['gray'] = CT_GrayscaleTransform
dml_main_namespace['alpha'] = CT_PositiveFixedPercentage
dml_main_namespace['alphaOff'] = CT_PositiveFixedPercentage
dml_main_namespace['alphaMod'] = CT_PositivePercentage
dml_main_namespace['hue'] = CT_PositiveFixedAngle
dml_main_namespace['hueOff'] = CT_Angle
dml_main_namespace['hueMod'] = CT_PositivePercentage
dml_main_namespace['sat'] = CT_Percentage
dml_main_namespace['satOff'] = CT_Percentage
dml_main_namespace['satMod'] = CT_Percentage
dml_main_namespace['lum'] = CT_Percentage
dml_main_namespace['lumOff'] = CT_Percentage
dml_main_namespace['lumMod'] = CT_Percentage
dml_main_namespace['red'] = CT_Percentage
dml_main_namespace['redOff'] = CT_Percentage
dml_main_namespace['redMod'] = CT_Percentage
dml_main_namespace['green'] = CT_Percentage
dml_main_namespace['greenOff'] = CT_Percentage
dml_main_namespace['greenMod'] = CT_Percentage
dml_main_namespace['blue'] = CT_Percentage
dml_main_namespace['blueOff'] = CT_Percentage
dml_main_namespace['blueMod'] = CT_Percentage
dml_main_namespace['gamma'] = CT_GammaTransform
dml_main_namespace['invGamma'] = CT_InverseGammaTransform

dml_main_namespace['sx'] = CT_Ratio
dml_main_namespace['sy'] = CT_Ratio

dml_main_namespace['off'] = CT_Point2D
dml_main_namespace['ext'] = CT_PositiveSize2D
dml_main_namespace['chOff'] = CT_Point2D
dml_main_namespace['chExt'] = CT_PositiveSize2D

dml_main_namespace['scrgbClr'] = CT_ScRgbColor
dml_main_namespace['srgbClr'] = CT_SRgbColor
dml_main_namespace['hslClr'] = CT_HslColor
dml_main_namespace['sysClr'] = CT_SystemColor
dml_main_namespace['schemeClr'] = CT_SchemeColor
dml_main_namespace['prstClr'] = CT_PresetColor

dml_main_namespace['snd'] = CT_EmbeddedWAVAudioFile

dml_main_namespace['hlinkClick'] = CT_Hyperlink
dml_main_namespace['hlinkHover'] = CT_Hyperlink
dml_main_namespace['hlinkMouseOver'] = CT_Hyperlink
dml_main_namespace['spLocks'] = CT_ShapeLocking

dml_main_namespace['cxnSpLocks'] = CT_ConnectorLocking
dml_main_namespace['stCxn'] = CT_Connection
dml_main_namespace['endCxn'] = CT_Connection

dml_main_namespace['picLocks'] = CT_PictureLocking
dml_main_namespace['grpSpLocks'] = CT_GroupLocking
dml_main_namespace['graphicFrameLocks'] = CT_GraphicalObjectFrameLocking
dml_main_namespace['cpLocks'] = CT_ContentPartLocking
dml_main_namespace['graphicData'] = CT_GraphicalObjectData

dml_main_namespace['graphic'] = CT_GraphicalObject
dml_main_namespace['dgm'] = CT_AnimationDgmElement
dml_main_namespace['chart'] = CT_AnimationChartElement
dml_main_namespace['bldDgm'] = CT_AnimationDgmBuildProperties
dml_main_namespace['bldChart'] = CT_AnimationChartBuildProperties

dml_main_namespace['txBody'] = CT_TextBody
dml_main_namespace['useSpRect'] = CT_GvmlUseShapeRectangle
# dml_main_namespace["xfrm"] = CT_Transform2D
dml_main_namespace['xfrm'] = CT_GroupTransform2D

dml_main_namespace['cNvPr'] = CT_NonVisualDrawingProps
dml_main_namespace['cNvSpPr'] = CT_NonVisualDrawingShapeProps
dml_main_namespace['cNvGrpSpPr'] = CT_NonVisualGroupDrawingShapeProps
dml_main_namespace['nvCxnSpPr'] = CT_GvmlConnectorNonVisual
dml_main_namespace['cNvCxnSpPr'] = CT_NonVisualConnectorProperties
dml_main_namespace['cNvPicPr'] = CT_NonVisualPictureProperties
dml_main_namespace['nvPicPr'] = CT_GvmlPictureNonVisual

dml_main_namespace['nvSpPr'] = CT_GvmlShapeNonVisual
dml_main_namespace['spPr'] = CT_ShapeProperties
dml_main_namespace['style'] = CT_ShapeStyle

dml_main_namespace['blipFill'] = CT_BlipFillProperties
dml_main_namespace['cNvGraphicFramePr'] = CT_NonVisualGraphicFrameProperties
dml_main_namespace['nvGraphicFramePr'] = CT_GvmlGraphicFrameNonVisual

dml_main_namespace['nvGrpSpPr'] = CT_GvmlGroupShapeNonVisual
dml_main_namespace['grpSpPr'] = CT_GroupShapeProperties
dml_main_namespace['txSp'] = CT_GvmlTextShape
dml_main_namespace['sp'] = CT_GvmlShape
dml_main_namespace['cxnSp'] = CT_GvmlConnector
dml_main_namespace['pic'] = CT_GvmlPicture
dml_main_namespace['graphicFrame'] = CT_GvmlGraphicalObjectFrame
dml_main_namespace['grpSp'] = CT_GvmlGroupShape

dml_main_namespace['rot'] = CT_SphereCoords
dml_main_namespace['camera'] = CT_Camera
dml_main_namespace['lightRig'] = CT_LightRig
dml_main_namespace['backdrop'] = CT_Backdrop

dml_main_namespace['anchor'] = CT_Point3D
dml_main_namespace['norm'] = CT_Vector3D
dml_main_namespace['up'] = CT_Vector3D

dml_main_namespace['bevelT'] = CT_Bevel
dml_main_namespace['bevelB'] = CT_Bevel
dml_main_namespace['extrusionClr'] = CT_Color
dml_main_namespace['contourClr'] = CT_Color

dml_main_namespace['flatTx'] = CT_FlatText
dml_main_namespace['clrFrom'] = CT_Color
dml_main_namespace['clrTo'] = CT_Color

dml_main_namespace['fillToRect'] = CT_RelativeRect
dml_main_namespace['lin'] = CT_LinearShadeProperties
# dml_main_namespace["path"] = CT_PathShadeProperties  # 名称有冲突

dml_main_namespace['gs'] = CT_GradientStop
dml_main_namespace['gsLst'] = CT_GradientStopList
dml_main_namespace['tileRect'] = CT_RelativeRect

dml_main_namespace['fillRect'] = CT_RelativeRect
dml_main_namespace['tile'] = CT_TileInfoProperties
dml_main_namespace['stretch'] = CT_StretchInfoProperties

dml_main_namespace['alphaBiLevel'] = CT_AlphaBiLevelEffect
dml_main_namespace['alphaCeiling'] = CT_AlphaCeilingEffect
dml_main_namespace['alphaFloor'] = CT_AlphaFloorEffect
dml_main_namespace['alphaInv'] = CT_AlphaInverseEffect
dml_main_namespace['alphaMod'] = CT_AlphaModulateEffect
dml_main_namespace['alphaModFix'] = CT_AlphaModulateFixedEffect
dml_main_namespace['alphaRepl'] = CT_AlphaReplaceEffect
dml_main_namespace['biLevel'] = CT_BiLevelEffect
dml_main_namespace['blur'] = CT_BlurEffect
dml_main_namespace['clrChange'] = CT_ColorChangeEffect
dml_main_namespace['clrRepl'] = CT_ColorReplaceEffect
dml_main_namespace['duotone'] = CT_DuotoneEffect
dml_main_namespace['fill'] = CT_FillEffect
dml_main_namespace['fillOverlay'] = CT_FillOverlayEffect
dml_main_namespace['grayscl'] = CT_GrayscaleEffect
dml_main_namespace['hsl'] = CT_HSLEffect
dml_main_namespace['lum'] = CT_LuminanceEffect
# 与 CT_PositiveFixedPercentage 类 表示的 tint 节点有冲突
dml_main_namespace['tint'] = CT_TintEffect

dml_main_namespace['blip'] = CT_Blip
dml_main_namespace['srcRect'] = CT_RelativeRect

dml_main_namespace['fgClr'] = CT_Color
dml_main_namespace['bgClr'] = CT_Color

dml_main_namespace['noFill'] = CT_NoFillProperties
dml_main_namespace['solidFill'] = CT_SolidColorFillProperties
dml_main_namespace['gradFill'] = CT_GradientFillProperties
dml_main_namespace['blipFill'] = CT_BlipFillProperties
dml_main_namespace['pattFill'] = CT_PatternFillProperties
dml_main_namespace['grpFill'] = CT_GroupFillProperties

dml_main_namespace['cont'] = CT_EffectContainer
dml_main_namespace['effect'] = CT_EffectReference
dml_main_namespace['alphaOutset'] = CT_AlphaOutsetEffect
dml_main_namespace['blend'] = CT_BlendEffect

dml_main_namespace['glow'] = CT_GlowEffect
dml_main_namespace['innerShdw'] = CT_InnerShadowEffect
dml_main_namespace['outerShdw'] = CT_OuterShadowEffect
dml_main_namespace['prstShdw'] = CT_PresetShadowEffect
dml_main_namespace['reflection'] = CT_ReflectionEffect
dml_main_namespace['relOff'] = CT_RelativeOffsetEffect
dml_main_namespace['softEdge'] = CT_SoftEdgesEffect

dml_main_namespace['effectLst'] = CT_EffectList
dml_main_namespace['effectDag'] = CT_EffectContainer

dml_main_namespace['gd'] = CT_GeomGuide
dml_main_namespace['pos'] = CT_AdjPoint2D

dml_main_namespace['ahXY'] = CT_XYAdjustHandle
dml_main_namespace['ahPolar'] = CT_PolarAdjustHandle

dml_main_namespace['cxn'] = CT_ConnectionSite
dml_main_namespace['pt'] = CT_AdjPoint2D

dml_main_namespace['close'] = CT_Path2DClose
dml_main_namespace['moveTo'] = CT_Path2DMoveTo
dml_main_namespace['lnTo'] = CT_Path2DLineTo
dml_main_namespace['arcTo'] = CT_Path2DArcTo
dml_main_namespace['quadBezTo'] = CT_Path2DQuadBezierTo
dml_main_namespace['cubicBezTo'] = CT_Path2DCubicBezierTo

# dml_main_namespace["path"] = CT_Path2D  # 名称有冲突


class CT_CommanPath(CT_PathShadeProperties, CT_Path2D): ...


dml_main_namespace['path'] = CT_CommanPath

dml_main_namespace['avLst'] = CT_GeomGuideList
dml_main_namespace['gdLst'] = CT_GeomGuideList
dml_main_namespace['ahLst'] = CT_AdjustHandleList
dml_main_namespace['cxnLst'] = CT_ConnectionSiteList
dml_main_namespace['rect'] = CT_GeomRect
dml_main_namespace['pathLst'] = CT_Path2DList

dml_main_namespace['custGeom'] = CT_CustomGeometry2D
dml_main_namespace['prstGeom'] = CT_PresetGeometry2D

dml_main_namespace['prstTxWarp'] = CT_PresetTextShape
dml_main_namespace['round'] = CT_LineJoinRound
dml_main_namespace['bevel'] = CT_LineJoinBevel
dml_main_namespace['miter'] = CT_LineJoinMiterProperties

dml_main_namespace['ds'] = CT_DashStop
dml_main_namespace['prstDash'] = CT_PresetLineDashProperties
dml_main_namespace['custDash'] = CT_DashStopList

dml_main_namespace['headEnd'] = CT_LineEndProperties
dml_main_namespace['tailEnd'] = CT_LineEndProperties

dml_main_namespace['lnRef'] = CT_StyleMatrixReference
dml_main_namespace['fillRef'] = CT_StyleMatrixReference
dml_main_namespace['effectRef'] = CT_StyleMatrixReference
dml_main_namespace['fontRef'] = CT_FontReference


dml_main_namespace['bodyPr'] = CT_TextBodyProperties
dml_main_namespace['lstStyle'] = CT_TextListStyle
dml_main_namespace['p'] = CT_TextParagraph


dml_main_namespace['spDef'] = CT_DefaultShapeDefinition
dml_main_namespace['lnDef'] = CT_DefaultShapeDefinition
dml_main_namespace['txDef'] = CT_DefaultShapeDefinition

dml_main_namespace['masterClrMapping'] = CT_EmptyElement
dml_main_namespace['overrideClrMapping'] = CT_ColorMapping

dml_main_namespace['clrScheme'] = CT_ColorScheme
dml_main_namespace['clrMap'] = CT_ColorMapping

dml_main_namespace['extraClrScheme'] = CT_ColorSchemeAndMapping

dml_main_namespace['themeElements'] = CT_BaseStyles
dml_main_namespace['objectDefaults'] = CT_ObjectStyleDefaults
dml_main_namespace['extraClrSchemeLst'] = CT_ColorSchemeList
dml_main_namespace['custClrLst'] = CT_CustomColorList

dml_main_namespace['fontScheme'] = CT_FontScheme
dml_main_namespace['fmtScheme'] = CT_StyleMatrix

dml_main_namespace['theme'] = CT_OfficeStyleSheet
dml_main_namespace['themeOverride'] = CT_BaseStylesOverride
dml_main_namespace['themeManager'] = CT_EmptyElement

dml_main_namespace['lnL'] = CT_LineProperties
dml_main_namespace['lnR'] = CT_LineProperties
dml_main_namespace['lnT'] = CT_LineProperties
dml_main_namespace['lnB'] = CT_LineProperties
dml_main_namespace['lnTlToBr'] = CT_LineProperties
dml_main_namespace['lnBlToTr'] = CT_LineProperties
dml_main_namespace['cell3D'] = CT_Cell3D
dml_main_namespace['headers'] = CT_Headers
dml_main_namespace['header'] = CT_Header

dml_main_namespace['gridCol'] = CT_TableCol
dml_main_namespace['tcPr'] = CT_TableCellProperties
dml_main_namespace['tc'] = CT_TableCell
dml_main_namespace['tableStyle'] = CT_TableStyle

# <xsd:element name="tableStyleId" type="s:ST_Guid"/>
# dml_core_namespace["tableStyleId"] = s_ST_Guid
dml_main_namespace['tableStyleId'] = OxmlBaseElement

dml_main_namespace['tblPr'] = CT_TableProperties
dml_main_namespace['tblGrid'] = CT_TableGrid
dml_main_namespace['tr'] = CT_TableRow
dml_main_namespace['tbl'] = CT_Table

dml_main_namespace['left'] = CT_ThemeableLineStyle
dml_main_namespace['right'] = CT_ThemeableLineStyle

dml_main_namespace['top'] = CT_ThemeableLineStyle
dml_main_namespace['bottom'] = CT_ThemeableLineStyle
dml_main_namespace['insideH'] = CT_ThemeableLineStyle
dml_main_namespace['insideV'] = CT_ThemeableLineStyle
dml_main_namespace['tl2br'] = CT_ThemeableLineStyle
dml_main_namespace['tr2bl'] = CT_ThemeableLineStyle

dml_main_namespace['tcBdr'] = CT_TableCellBorderStyle

dml_main_namespace['tcTxStyle'] = CT_TableStyleTextStyle
dml_main_namespace['tcStyle'] = CT_TableStyleCellStyle

dml_main_namespace['tblBg'] = CT_TableBackgroundStyle
dml_main_namespace['wholeTbl'] = CT_TablePartStyle
dml_main_namespace['band1H'] = CT_TablePartStyle

dml_main_namespace['band2H'] = CT_TablePartStyle
dml_main_namespace['band1V'] = CT_TablePartStyle
dml_main_namespace['band2V'] = CT_TablePartStyle
dml_main_namespace['lastCol'] = CT_TablePartStyle
dml_main_namespace['firstCol'] = CT_TablePartStyle
dml_main_namespace['lastRow'] = CT_TablePartStyle
dml_main_namespace['seCell'] = CT_TablePartStyle
dml_main_namespace['swCell'] = CT_TablePartStyle
dml_main_namespace['firstRow'] = CT_TablePartStyle
dml_main_namespace['neCell'] = CT_TablePartStyle
dml_main_namespace['nwCell'] = CT_TablePartStyle

dml_main_namespace['tblStyle'] = CT_TableStyle
dml_main_namespace['tblStyleLst'] = CT_TableStyleList
dml_main_namespace['pPr'] = CT_TextParagraphProperties
dml_main_namespace['endParaRPr'] = CT_TextCharacterProperties
dml_main_namespace['defPPr'] = CT_TextParagraphProperties
dml_main_namespace['lvl1pPr'] = CT_TextParagraphProperties
dml_main_namespace['lvl2pPr'] = CT_TextParagraphProperties
dml_main_namespace['lvl3pPr'] = CT_TextParagraphProperties
dml_main_namespace['lvl4pPr'] = CT_TextParagraphProperties
dml_main_namespace['lvl5pPr'] = CT_TextParagraphProperties
dml_main_namespace['lvl6pPr'] = CT_TextParagraphProperties
dml_main_namespace['lvl7pPr'] = CT_TextParagraphProperties
dml_main_namespace['lvl8pPr'] = CT_TextParagraphProperties
dml_main_namespace['lvl9pPr'] = CT_TextParagraphProperties

dml_main_namespace['noAutofit'] = CT_TextNoAutofit
dml_main_namespace['normAutofit'] = CT_TextNormalAutofit
dml_main_namespace['spAutoFit'] = CT_TextShapeAutofit

dml_main_namespace['buClrTx'] = CT_TextBulletColorFollowText
dml_main_namespace['buClr'] = CT_Color

dml_main_namespace['buSzTx'] = CT_TextBulletSizeFollowText
dml_main_namespace['buSzPct'] = CT_TextBulletSizePercent
dml_main_namespace['buSzPts'] = CT_TextBulletSizePoint

dml_main_namespace['buFontTx'] = CT_TextBulletTypefaceFollowText
dml_main_namespace['buFont'] = CT_TextFont
dml_main_namespace['buNone'] = CT_TextNoBullet
dml_main_namespace['buAutoNum'] = CT_TextAutonumberBullet
dml_main_namespace['buChar'] = CT_TextCharBullet
dml_main_namespace['buBlip'] = CT_TextBlipBullet

dml_main_namespace['uLnTx'] = CT_TextUnderlineLineFollowText
dml_main_namespace['uLn'] = CT_LineProperties

dml_main_namespace['uFillTx'] = CT_TextUnderlineFillFollowText
dml_main_namespace['uFill'] = CT_TextUnderlineFillGroupWrapper

dml_main_namespace['highlight'] = CT_Color
dml_main_namespace['latin'] = CT_TextFont

dml_main_namespace['tab'] = CT_TextTabStop
dml_main_namespace['rPr'] = CT_TextCharacterProperties

dml_main_namespace['spcPct'] = CT_TextSpacingPercent
dml_main_namespace['spcPts'] = CT_TextSpacingPoint

dml_main_namespace['lnSpc'] = CT_TextSpacing
dml_main_namespace['spcBef'] = CT_TextSpacing
dml_main_namespace['spcAft'] = CT_TextSpacing

dml_main_namespace['tabLst'] = CT_TextTabStopList
dml_main_namespace['defRPr'] = CT_TextCharacterProperties

dml_main_namespace['r'] = CT_RegularTextRun
dml_main_namespace['br'] = CT_TextLineBreak
dml_main_namespace['fld'] = CT_TextField
dml_main_namespace['t'] = OxmlBaseElement

# 在pml中使用类型
dml_main_namespace['graphicEl'] = CT_AnimationElementChoice
dml_main_namespace['sndTgt'] = CT_EmbeddedWAVAudioFile
dml_main_namespace['clrVal'] = CT_Color
dml_main_namespace['from'] = CT_Color
dml_main_namespace['to'] = CT_Color
dml_main_namespace['penClr'] = CT_Color
dml_main_namespace['bldSub'] = CT_AnimationGraphicalObjectBuildProperties
dml_main_namespace['pos'] = CT_Point2D  # 有冲突 CT_Comment
dml_main_namespace['font'] = CT_TextFont  # pml 冲突 父级类型: CT_EmbeddedFontListEntry
dml_main_namespace['notesSz'] = CT_PositiveSize2D
dml_main_namespace['gridSpacing'] = CT_PositiveSize2D
dml_main_namespace['defaultTextStyle'] = CT_TextListStyle
dml_main_namespace['clrMru'] = CT_ColorMRU
dml_main_namespace['clrMapOvr'] = CT_ColorMappingOverride
dml_main_namespace['bgRef'] = CT_StyleMatrixReference
dml_main_namespace['titleStyle'] = CT_TextListStyle
dml_main_namespace['bodyStyle'] = CT_TextListStyle
dml_main_namespace['otherStyle'] = CT_TextListStyle
dml_main_namespace['notesStyle'] = CT_TextListStyle
dml_main_namespace['scale'] = CT_Scale2D
dml_main_namespace['origin'] = CT_Point2D
