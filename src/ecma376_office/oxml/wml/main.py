"""
pptx 文档xsd转换成python类对象的模块

对应xsd: wml-main.xsd

前缀: 'w'

命名空间: http://schemas.openxmlformats.org/wordprocessingml/2006/main

        # http://purl.oclc.org/ooxml/presentationml/main

相关命名空间:

    m: http://schemas.openxmlformats.org/officeDocument/2006/math

    r: http://schemas.openxmlformats.org/officeDocument/2006/relationships

    sl: http://schemas.openxmlformats.org/schemaLibrary/2006/main

    wp: http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing

    s: http://schemas.openxmlformats.org/officeDocument/2006/sharedTypes

对应Reference: 21.1 DrawingML - Main
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import (
    TYPE_CHECKING,
    Any,
    AnyStr,
    Optional,
    Union,
)

from ecma376_office.oxml.base import OxmlBaseElement, ST_BaseEnumType, lookup
from ecma376_office.oxml.shared.common_simple_types import ST_AlgClass as s_ST_AlgClass
from ecma376_office.oxml.shared.common_simple_types import ST_AlgType as s_ST_AlgType
from ecma376_office.oxml.shared.common_simple_types import ST_CalendarType as s_ST_CalendarType
from ecma376_office.oxml.shared.common_simple_types import ST_ConformanceClass as s_ST_ConformanceClass
from ecma376_office.oxml.shared.common_simple_types import ST_CryptProv as s_ST_CryptProv
from ecma376_office.oxml.shared.common_simple_types import ST_Guid as s_ST_Guid
from ecma376_office.oxml.shared.common_simple_types import ST_HexColorRGB as s_ST_HexColorRGB
from ecma376_office.oxml.shared.common_simple_types import ST_Lang as s_ST_Lang
from ecma376_office.oxml.shared.common_simple_types import ST_OnOff as s_ST_OnOff
from ecma376_office.oxml.shared.common_simple_types import ST_TwipsMeasure as s_ST_TwipsMeasure
from ecma376_office.oxml.shared.common_simple_types import ST_UniversalMeasure as s_ST_UniversalMeasure
from ecma376_office.oxml.shared.common_simple_types import ST_UnsignedDecimalNumber as s_ST_UnsignedDecimalNumber
from ecma376_office.oxml.shared.common_simple_types import ST_VerticalAlignRun as s_ST_VerticalAlignRun
from ecma376_office.oxml.shared.common_simple_types import ST_XAlign as s_ST_XAlign
from ecma376_office.oxml.shared.common_simple_types import ST_YAlign as s_ST_YAlign
from ecma376_office.oxml.shared.common_simple_types import to_ST_HexColorRGB as s_to_ST_HexColorRGB
from ecma376_office.oxml.shared.common_simple_types import (
    to_ST_PositiveUniversalMeasure as s_to_ST_PositiveUniversalMeasure,
)
from ecma376_office.oxml.shared.common_simple_types import to_ST_TwipsMeasure as s_to_ST_TwipsMeasure
from ecma376_office.oxml.shared.common_simple_types import to_ST_UniversalMeasure as s_to_ST_UniversalMeasure
from ecma376_office.oxml.shared.relationship_reference import ST_RelationshipId as r_ST_RelationshipId
from ecma376_office.oxml.vml.const import NS_MAP as ns_map  # 当前命名空间
from ecma376_office.oxml.vml.const import NameSpace_w

if TYPE_CHECKING:
    from ecma376_office.oxml.dml.word_drawing import CT_Anchor as wp_CT_Anchor
    from ecma376_office.oxml.dml.word_drawing import CT_Inline as wp_CT_Inline
    from ecma376_office.oxml.shared.math import CT_OMath as m_CT_OMath
    from ecma376_office.oxml.shared.math import CT_OMathPara as m_CT_OMathPara
    from ecma376_office.oxml.vml.drawing import CT_OLEObject
    from ecma376_office.oxml.vml.main import CT_Shape

namespace_r = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

namespace_sl = 'http://schemas.openxmlformats.org/schemaLibrary/2006/main'

namespace_wp = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'

namespace_s = 'http://schemas.openxmlformats.org/officeDocument/2006/sharedTypes'

# 替代内容的命名空间,
# 参考标准的第三部分:
# https://hellowac.github.io/ecma-376-zh-cn/ecma-part3-refrence/
namespace_mc = 'http://schemas.openxmlformats.org/markup-compatibility/2006'

logger = logging.getLogger(__name__)


def qn(tag: str):
    """将 dc:creator 这种的标签,转换为 {http://purl.org/dc/elements/1.1/}creator 这样的形式"""

    global ns_map

    if ':' not in tag:
        return tag

    ns_prefix, ns = tag.split(':')

    return f'{{{ns_map[ns_prefix]}}}{ns}'


class CT_Empty(OxmlBaseElement):
    """17.17.4 布尔属性 (CT_OnOff)

    此通用复杂类型指定了在整个 WordprocessingML 中使用的布尔属性。
    """

    @property
    def is_empty(self):
        return True


class CT_OnOff(OxmlBaseElement):
    @property
    def val_on_off(self) -> Optional[s_ST_OnOff]:
        """val（开/关值）

        指定由父 XML 元素定义的属性的二进制值。

        值为 1 或 true 表示该属性应被明确应用。这是此属性的默认值，并在父元素存在但未指定此属性时被隐含应用。

        值为 0 或 false 表示该属性应被明确关闭。

        [示例：例如，考虑以下开/关属性：

        <… w:val="false"/>

        val 属性明确声明该属性为 false。end example]

        此属性的可能值由 ST_OnOff 简单类型定义（§22.9.2.7）。

        【有联合类型】
        """

        _val = self.attrib.get(qn('w:val'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def is_on(self):
        return self.val_on_off in {
            None,
            s_ST_OnOff.One,
            s_ST_OnOff.On,
            s_ST_OnOff.true,
        }

    @property
    def is_off(self):
        return self.val_on_off in {
            s_ST_OnOff.Zero,
            s_ST_OnOff.Off,
            s_ST_OnOff.false,
        }


class ST_LongHexNumber(str):
    """
    <xsd:simpleType name="ST_LongHexNumber">
        <xsd:restriction base="xsd:hexBinary">
            <xsd:length value="4"/>
        </xsd:restriction>
    </xsd:simpleType>
    """



class CT_LongHexNumber(OxmlBaseElement):
    @property
    def val(self) -> ST_LongHexNumber:
        """ "val（长十六进制数字值）

        指定一个数值（以四位十六进制数字表示），其内容根据父XML元素的上下文进行解释。

        【示例：考虑简单类型ST_LongHexNumber属性的以下值：00BE2C6C。

        这个值是允许的，因为它包含四个十六进制数字，每个数字都是实际十进制数字值的一个字节的编码。因此，它可以根据父XML元素的上下文进行解释。示例结束】

        此属性的可能值由ST_LongHexNumber简单类型定义（§17.18.50）。
        """
        return ST_LongHexNumber(self.attrib[qn('w:val')])


class ST_ShortHexNumber(str):
    """
    <xsd:simpleType name="ST_ShortHexNumber">
        <xsd:restriction base="xsd:hexBinary">
            <xsd:length value="2"/>
        </xsd:restriction>
    </xsd:simpleType>
    """



class ST_UcharHexNumber(str):
    """
    <xsd:simpleType name="ST_UcharHexNumber">
        <xsd:restriction base="xsd:hexBinary">
            <xsd:length value="1"/>
        </xsd:restriction>
    </xsd:simpleType>
    """



class CT_Charset(OxmlBaseElement):
    @property
    def val(self) -> Optional[ST_UcharHexNumber]:
        _val = self.attrib.get(qn('w:val'))

        if _val is None:
            return None

        return ST_UcharHexNumber(_val)

    @property
    def characterSet(self) -> str:
        _val = self.attrib.get(qn('w:characterSet'), 'ISO-8859-1')

        return str(_val)


ST_DecimalNumberOrPercent = Union[float, str]
"""
<xsd:simpleType name="ST_DecimalNumberOrPercent">
    <xsd:union memberTypes="ST_UnqualifiedPercentage s:ST_Percentage"/>
</xsd:simpleType>
"""


def to_ST_DecimalNumberOrPercent(_val: AnyStr):
    try:
        return float(_val)

    except Exception:
        return str(_val)


class ST_UnqualifiedPercentage(int):
    """
    <xsd:simpleType name="ST_UnqualifiedPercentage">
        <xsd:restriction base="xsd:integer"/>
    </xsd:simpleType>
    """



class ST_DecimalNumber(int):
    """
    <xsd:simpleType name="ST_DecimalNumber">
        <xsd:restriction base="xsd:integer"/>
    </xsd:simpleType>
    """



class CT_DecimalNumber(OxmlBaseElement):
    """
    17.9.3 ilvl

    17.9.12 multiLevelType (抽象编号定义类型)

    17.9.25 start (起始值)¶

    start (Starting Value)

    该元素指定父编号级别在给定编号级别定义中使用的编号的起始值。当此级别在文档中首次启动时，以及每当通过 lvlRestart 元素（§17.9.10）中设置的属性重新启动时，将使用此值。

    如果省略此元素，则起始值应为零（0）。

    【示例：考虑以下用于抽象编号定义的 WordprocessingML 片段：

    <w:abstractNum w:abstractNumId="1">
        …
        <w:lvl w:ilvl="0">
            <w:start w:val="2" />
            <w:numFmt w:val="upperLetter"/>
            …
        </w:lvl>
    </w:abstractNum>

    在此示例中，由于使用大写西方字母（upperLetter）作为此编号级别的编号符号，因此与此抽象编号定义和编号级别关联的编号段落的第一个实例将具有编号符号 B，即数字格式中的第二个字母。

    具有此抽象编号定义且在此级别的后续编号段落将从 B（此编号级别的起始值）开始递增其编号符号。示例结束】
    """

    @property
    def val_dec_num(self) -> ST_DecimalNumber:
        """val（十进制数值）

        指定此属性的内容包含十进制数。

        此十进制数的内容根据父 XML 元素的上下文进行解释。

        【示例：考虑以下简单类型 ST_DecimalNumber 的数值 WordprocessingML 属性：


        <… w:val="1512645511" />
        val 属性的值是一个十进制数，其值必须在父元素的上下文中进行解释。示例结束】



        【有联合类型】
        """
        _val = self.attrib[qn('w:val')]

        return ST_DecimalNumber(int(_val))


class CT_UnsignedDecimalNumber(OxmlBaseElement):
    @property
    def val(self) -> s_ST_UnsignedDecimalNumber:
        _val = self.attrib[qn('w:val')]

        return s_ST_UnsignedDecimalNumber(int(_val))


class CT_DecimalNumberOrPrecent(OxmlBaseElement):
    @property
    def val(self) -> ST_DecimalNumberOrPercent:
        _val = self.attrib[qn('w:val')]

        try:
            return float(_val)

        except Exception:
            return str(_val)


class CT_TwipsMeasure(OxmlBaseElement):
    @property
    def val_twips_measure(self) -> s_ST_TwipsMeasure:
        """
        [有联合类型]
        """
        _val = self.attrib[qn('w:val')]

        return s_to_ST_TwipsMeasure(_val)  # type: ignore


class ST_SignedTwipsMeasure(s_ST_UniversalMeasure):
    """
    17.18.81 ST_SignedTwipsMeasure (以二十分之一为单位的有符号测量)

    ST_SignedTwipsMeasure (Signed Measurement in Twentieths of a Point)

    这个简单类型规定其内容可以是以下之一：

    - 正数或负数的整数，其内容为二十分之一点（相当于1/1440英寸）的测量值，或
    - 紧随其后的正小数，后面紧跟着单位标识符。

    此测量的内容根据父级 XML 元素的上下文进行解释。

    【例如：考虑一个属性值为 720，其简单类型为 ST_SignedTwipsMeasure。此属性值指定一英寸的一半或者36点（720 二十分之一点 = 36 点 = 0.5英寸）。示例结束】

    【例如：考虑一个属性值为 -12.7mm，其类型为 ST_SignedTwipsMeasure。此属性值指定 -0.0127 米或者负一英寸或者 -36 点。示例结束】

    这个简单类型是以下类型的合并：

    - ST_UniversalMeasure 简单类型 (§22.9.2.15)。
    - W3C XML Schema 整数数据类型。

    <xsd:simpleType name="ST_SignedTwipsMeasure">
        <xsd:union memberTypes="xsd:integer s:ST_UniversalMeasure"/>
    </xsd:simpleType>
    """



def to_ST_SignedTwipsMeasure(val: AnyStr):
    try:
        # 17.18.81 ST_SignedTwipsMeasure (以二十分之一为单位的有符号测量)
        # 正数或负数的整数，其内容为二十分之一点（相当于1/1440英寸）的测量值
        return ST_SignedTwipsMeasure(float(val) / 20)  # 以point为单位
    except Exception:
        # 紧随其后的正小数，后面紧跟着单位标识符。
        return ST_SignedTwipsMeasure(s_to_ST_UniversalMeasure(str(val)))


class CT_SignedTwipsMeasure(OxmlBaseElement):
    """17.3.2.35 spacing (字符间距调整)"""

    @property
    def val(self) -> ST_SignedTwipsMeasure:
        """可能是数字，也可能是带单位的"""
        _val = self.attrib[qn('w:val')]

        return to_ST_SignedTwipsMeasure(str(_val))


class ST_PixelsMeasure(int):
    """
    <xsd:simpleType name="ST_PixelsMeasure">
        <xsd:restriction base="s:ST_UnsignedDecimalNumber"/>
    </xsd:simpleType>
    """



class CT_PixelsMeasure(OxmlBaseElement):
    """
    <xsd:complexType name="CT_PixelsMeasure">
        <xsd:attribute name="val" type="ST_PixelsMeasure" use="required"/>
    </xsd:complexType>
    """

    @property
    def val(self) -> ST_PixelsMeasure:
        _val = self.attrib[qn('w:val')]

        return ST_PixelsMeasure(int(_val))


class ST_HpsMeasure(int):
    """17.18.42 ST_HpsMeasure (以半点测量)

    这个简单类型指定其内容可以是以下之一：

    - 正整数，其内容是以半点为单位的测量值（相当于英寸的1/144），或者
    - 正十进制数，后面紧跟单位标识符。

    该测量的内容根据父 XML 元素的上下文进行解释。

    【示例：考虑一个简单类型为 ST_HpsMeasure 的属性值为 72。该属性值指定了半英寸或 36 点（72 半点 = 36 点 = 0.5 英寸）的大小。示例结束】

    【示例：考虑一个简单类型为 ST_HpsMeasure 的属性值为 12.7mm。该属性值指定了 0.0127 米或半英寸或 36 点的大小。示例结束】

    该简单类型是以下类型的并集：

    - ST_PositiveUniversalMeasure 简单类型（§22.9.2.12）。
    - ST_UnsignedDecimalNumber 简单类型（§22.9.2.16）。

    <xsd:simpleType name="ST_HpsMeasure">
        <xsd:union memberTypes="s:ST_UnsignedDecimalNumber s:ST_PositiveUniversalMeasure"/>
    </xsd:simpleType>
    """


def to_ST_HpsMeasure(_val: AnyStr) -> ST_HpsMeasure:
    try:
        return ST_HpsMeasure(int(float(_val)) / 2)

    except Exception:
        return ST_HpsMeasure(s_to_ST_PositiveUniversalMeasure(_val))  # type: ignore


class CT_HpsMeasure(OxmlBaseElement):
    """17.3.2.38 sz (非复杂脚本字体大小)

    17.3.2.39 szCs (复杂脚本字体大小)

    17.3.2.19 kern (字体字距调整)

    17.3.3.12 hpsRaise (拼音指南文本与拼音指南基础文本之间的距离)

    17.3.3.11 hpsBaseText (拼音指南基本文本字体大小)

    17.3.3.10 hps (拼音指南文字字体大小)

    """

    @property
    def val_hps_measure(self) -> ST_HpsMeasure:
        _val = self.attrib[qn('w:val')]

        return to_ST_HpsMeasure(str(_val))


class ST_SignedHpsMeasure(int):
    """
    <xsd:simpleType name="ST_SignedHpsMeasure">
        <xsd:union memberTypes="xsd:integer s:ST_UniversalMeasure"/>
    </xsd:simpleType>
    """



def to_ST_SignedHpsMeasure(_val: AnyStr) -> ST_SignedHpsMeasure:
    try:
        return ST_SignedHpsMeasure(int(_val))

    except Exception:
        return ST_SignedHpsMeasure(s_to_ST_UniversalMeasure(_val))  # type: ignore


class CT_SignedHpsMeasure(OxmlBaseElement):
    """17.3.2.24 position (垂直升高或降低的文本)

    position (Vertically Raised or Lowered Text)

    该元素指定相对于周围非定位文本的默认基线，文本应该被提升或降低的量。这允许重新定位文本，而不改变内容的字体大小。

    如果val属性为正数，则父运行将被提升到周围文本的基线上方指定数量的半点。如果val属性为负数，则父运行将被降低到周围文本的基线下方指定数量的半点。

    如果该元素不存在，则默认值是保留应用于样式层次结构中先前级别的格式。如果该元素在样式层次结构中从未被应用过，则相对于该运行内容的默认基线位置，文本不会被提升或降低。

    【示例：考虑一个运行，其内容在显示时必须相对于默认基线位置提升12点。此需求将使用以下 WordprocessingML 指定：

    <w:rPr>
        <w:position w:val="24" />
    </w:rPr>

    由于val属性的内容为正数，因此结果运行将位于默认基线位置上方24个半点。示例结束】
    """

    @property
    def val(self) -> ST_SignedHpsMeasure:
        """val（有符号半点度量）

        指定半点（1/144英寸）中的正数或负数度量。

        该属性值的内容根据父 XML 元素的上下文进行解释。

        [示例：考虑以下 WordprocessingML 片段：

        <w:rPr>
            <w:position w:val="-12" />
        </w:rPr>

        在这种情况下，val 属性中的值表示指定运行相对于周围文本基线提升或下降的量。

        在所有情况下，该值都是在父元素的上下文中进行解释的。示例结束]

        The possible values for this attribute are defined by the ST_SignedHpsMeasure simple type (§17.18.80).
        """
        _val = self.attrib[qn('w:val')]

        return to_ST_SignedHpsMeasure(str(_val))


class ST_DateTime(datetime):
    """
    <xsd:simpleType name="ST_DateTime">
        <xsd:restriction base="xsd:dateTime"/>
    </xsd:simpleType>
    """



def to_ST_DateTime(val: AnyStr) -> ST_DateTime:
    dt = datetime.strptime(str(val), '%Y-%m-%d %H:%M:%S')

    return ST_DateTime(dt.year, dt.month, dt.day)


class ST_MacroName(str):
    """
    <xsd:simpleType name="ST_MacroName">
        <xsd:restriction base="xsd:string">
            <xsd:maxLength value="33"/>
        </xsd:restriction>
    </xsd:simpleType>
    """


class CT_MacroName(OxmlBaseElement):
    @property
    def val(self) -> ST_MacroName:
        _val = self.attrib[qn('w:val')]

        return ST_MacroName(str(_val))


class ST_EighthPointMeasure(int):
    """
    <xsd:simpleType name="ST_EighthPointMeasure">
        <xsd:restriction base="s:ST_UnsignedDecimalNumber"/>
    </xsd:simpleType>
    """


class ST_PointMeasure(int):
    """
    <xsd:simpleType name="ST_EighthPointMeasure">
        <xsd:restriction base="s:ST_UnsignedDecimalNumber"/>
    </xsd:simpleType>
    """


class CT_String(OxmlBaseElement):
    @property
    def val_str(self) -> str:
        """
        【有联合类型】
        """
        _val = self.attrib[qn('w:val')]

        return str(_val)


ST_TextScale = Union[str, float]
"""
<xsd:simpleType name="ST_TextScale">
    <xsd:union memberTypes="ST_TextScalePercent ST_TextScaleDecimal"/>
</xsd:simpleType>
"""


def to_ST_TextScale(_val: AnyStr):
    if _val.endswith('%'):  # type: ignore
        return _val

    return float(_val)


class ST_TextScalePercent(str):
    """
    <xsd:simpleType name="ST_TextScalePercent">
        <xsd:restriction base="xsd:string">
            <xsd:pattern value="0*(600|([0-5]?[0-9]?[0-9]))%"/>
        </xsd:restriction>
    </xsd:simpleType>
    """


class ST_TextScaleDecimal(int):
    """
    <xsd:simpleType name="ST_TextScaleDecimal">
        <xsd:restriction base="xsd:integer">
            <xsd:minInclusive value="0"/>
            <xsd:maxInclusive value="600"/>
        </xsd:restriction>
    </xsd:simpleType>
    """



class CT_TextScale(OxmlBaseElement):
    """
    <xsd:complexType name="CT_TextScale">
        <xsd:attribute name="val" type="ST_TextScale"/>
    </xsd:complexType>
    """

    @property
    def val_text_scale(self) -> ST_TextScale:
        """

        [有联合类型]
        """
        _val = self.attrib[qn('w:val')]

        return to_ST_TextScale(_val)  # type: ignore


class ST_HighlightColor(ST_BaseEnumType):
    """17.18.40 ST_HighlightColor (文本突出显示颜色)

    这个简单类型指定了可以作为文本运行内容背后的背景应用的高亮颜色的可能值。

    【示例】考虑一个段落中的文本运行，使用高亮元素具有黄色文本高亮。 这种格式设置使用以下 WordprocessingML 指定：

    <w:rPr>
        <w:highlight w:val="yellow" />
    </w:rPr>

    结果运行的内容将有黄色的高亮显示。示例结束
    """

    Black = 'black'
    Blue = 'blue'
    Cyan = 'cyan'
    Green = 'green'
    Magenta = 'magenta'
    Red = 'red'
    Yellow = 'yellow'
    White = 'white'
    DarkBlue = 'darkBlue'
    DarkCyan = 'darkCyan'
    DarkGreen = 'darkGreen'
    DarkMagenta = 'darkMagenta'
    DarkRed = 'darkRed'
    DarkYellow = 'darkYellow'
    DarkGray = 'darkGray'
    LightGray = 'lightGray'
    none = 'none'


class CT_Highlight(OxmlBaseElement):
    """17.3.2.15 highlight (文本突出显示)¶

    highlight (Text Highlighting)

    该元素指定一个高亮颜色，作为此运行内容背后的背景应用。

    如果此运行具有使用 shd 元素（§17.3.2.32）指定的任何背景阴影，则当显示此运行的内容时，背景阴影将被高亮颜色取代。

    如果该元素不存在，则默认值是保留样式层次结构中先前级别应用的格式。如果该元素在样式层次结构中从未应用过，则不会对该运行的内容应用文本高亮。

    [示例：考虑一个段落中的运行，其中除了应用了运行阴影外，还使用 highlight 元素应用了黄色文本高亮。可以使用以下 WordprocessingML 指定此格式：

    <w:rPr>
        <w:highlight w:val="yellow" />
        <w:shd w:themeFill="accent2" w:themeFillTint="66" />
    </w:rPr>

    结果运行的内容将显示黄色高亮，因为高亮颜色会替代运行内容的阴影。示例结束]
    """

    @property
    def val(self) -> ST_HighlightColor:
        """17.18.40 ST_HighlightColor (文本突出显示颜色)

        这个简单类型指定了可以作为文本运行内容背后的背景应用的高亮颜色的可能值。

        【示例】考虑一个段落中的文本运行，使用高亮元素具有黄色文本高亮。 这种格式设置使用以下 WordprocessingML 指定：

        <w:rPr>
            <w:highlight w:val="yellow" />
        </w:rPr>

        结果运行的内容将有黄色的高亮显示。示例结束
        """

        _val = self.attrib[qn('w:val')]

        return ST_HighlightColor(_val)


class ST_HexColorAuto(ST_BaseEnumType):
    Auto = 'auto'


ST_HexColor = Union[ST_HexColorAuto, s_ST_HexColorRGB]


def to_ST_HexColor(_val: AnyStr) -> ST_HexColor:
    if ST_HexColorAuto.have_value(_val):
        return ST_HexColorAuto.Auto

    return s_to_ST_HexColorRGB(_val)  # type: ignore


class CT_Color(OxmlBaseElement):
    """17.3.2.6 color (运行内容颜色)

    该元素指定在文档中显示此运行内容时所使用的颜色。

    此颜色可以明确指定，也可以设置为允许消费者根据运行内容后面的背景颜色自动选择合适的颜色。

    如果此元素不存在，则默认值是保留样式层次结构中先前级别应用的格式。如果在样式层次结构中从未应用此元素，则字符被设置为允许消费者根据运行内容后面的背景颜色自动选择合适的颜色。

    [示例：考虑一个文本运行，其内容应该使用文档的主题部分中的accent3主题颜色显示。在生成的WordprocessingML中，该要求将指定如下：


    <w:rPr>
        <w:color w:themeColor="accent3" />
    </w:rPr>
    color属性指定该运行应使用accent3主题颜色。示例结束]
    """

    @property
    def val(self) -> ST_HexColor:
        """val（运行内容颜色）

        指定此运行的颜色。

        此颜色可以表示为十六进制值（以RRGGBB格式），也可以为auto，以允许消费者根据需要自动确定运行颜色。

        如果运行通过themeColor属性指定了使用主题颜色，则此值将被主题颜色值所取代。

        [示例：考虑一个值为auto的运行颜色，如下所示：

        ```xml

        因此，此颜色可以根据需要由消费者自动修改，例如，以确保运行内容与页面背景颜色区分开。示例结束]

        The possible values for this attribute are defined by the ST_HexColor simple type (§17.18.38).
        """
        _val = self.attrib[qn('w:val')]

        return to_ST_HexColor(_val)  # type: ignore

    @property
    def themeColor(self) -> ST_ThemeColor:
        """themeColor（运行内容主题颜色）

        指定应应用于当前运行的主题颜色。

        指定的主题颜色是对文档的主题部分中预定义主题颜色之一的引用，该部分允许在文档中集中设置颜色信息。

        如果指定了themeColor属性，则对于此运行，val属性将被忽略。

        [示例：考虑一个文本运行，其内容应该使用文档的主题部分中的accent3主题颜色显示。在生成的WordprocessingML中，该要求将指定如下：

        <w:rPr>
            <w:color w:themeColor="accent3" />
        </w:rPr>

        color属性指定该运行必须使用accent3主题颜色。示例结束]

        The possible values for this attribute are defined by the ST_ThemeColor simple type (§17.18.97).
        """
        _val = self.attrib[qn('w:themeColor')]

        return ST_ThemeColor(_val)

    @property
    def themeTint(self) -> ST_UcharHexNumber:
        """themeTint（运行内容主题颜色色调）

        指定应用于此运行内容所提供的主题颜色（如果有）的色调值。

        如果提供了themeTint，则它将应用于主题颜色的RGB值，以确定应用于此运行的最终颜色。

        themeTint值以十六进制编码的形式存储，表示应用于当前边框的色调值（从0到255）。

        [示例：考虑在文档中应用了60%的色调到一个运行。此色调的计算如下所示：

        𝑆𝑥𝑚𝑙 = 0.6 ∗ 255
            = 153
            = 99(十六进制)

        文件格式中的结果主题色调值将为99。示例结束]
        """
        _val = self.attrib[qn('w:themeTint')]

        return ST_UcharHexNumber(_val)  # type: ignore

    @property
    def themeShade(self) -> ST_UcharHexNumber:
        """themeShade（运行内容主题颜色阴影）

        指定应用于此运行内容所提供的主题颜色（如果有）的阴影值。

        如果提供了themeTint，则将忽略此属性的值。

        如果提供了themeShade，则它将应用于主题颜色的RGB值，以确定应用于此运行的最终颜色。

        themeShade值以十六进制编码的形式存储，表示应用于当前边框的阴影值（从0到255）。

        [示例：考虑在文档中应用了40%的阴影到一个运行。此阴影的计算如下所示：

        𝑆𝑥𝑚𝑙 = 0.4 ∗ 255
            = 102
            = 66(十六进制)

        文件格式中的结果主题阴影值将为66。示例结束]
        """
        _val = self.attrib[qn('w:themeShade')]

        return ST_UcharHexNumber(_val)  # type: ignore


class CT_Lang(OxmlBaseElement):
    @property
    def val(self) -> s_ST_Lang:
        _val = self.attrib[qn('w:val')]

        return s_ST_Lang(_val)  # type: ignore


class CT_Guid(OxmlBaseElement):
    @property
    def val(self) -> s_ST_Guid:
        _val = self.attrib[qn('w:val')]

        return s_ST_Guid(_val)  # type: ignore


class ST_Underline(ST_BaseEnumType):
    Single = 'single'
    Words = 'words'
    Double = 'double'
    Thick = 'thick'
    Dotted = 'dotted'
    DottedHeavy = 'dottedHeavy'
    Dash = 'dash'
    DashedHeavy = 'dashedHeavy'
    DashLong = 'dashLong'
    DashLongHeavy = 'dashLongHeavy'
    DotDash = 'dotDash'
    DashDotHeavy = 'dashDotHeavy'
    DotDotDash = 'dotDotDash'
    DashDotDotHeavy = 'dashDotDotHeavy'
    Wave = 'wave'
    WavyHeavy = 'wavyHeavy'
    WavyDouble = 'wavyDouble'
    none = 'none'


class CT_Underline(OxmlBaseElement):
    @property
    def val(self) -> Optional[ST_Underline]:
        _val = self.attrib.get(qn('w:val'))

        if _val is None:
            return None

        return ST_Underline(_val)

    @property
    def color(self) -> ST_HexColor:
        _val = self.attrib.get(qn('w:color'))

        if _val is None:
            return ST_HexColorAuto.Auto

        return to_ST_HexColor(_val)  # type: ignore

    @property
    def themeColor(self) -> ST_ThemeColor:
        _val = self.attrib[qn('w:themeColor')]

        return ST_ThemeColor(_val)

    @property
    def themeTint(self) -> ST_UcharHexNumber:
        _val = self.attrib[qn('w:themeTint')]

        return ST_UcharHexNumber(_val)  # type: ignore

    @property
    def themeShade(self) -> ST_UcharHexNumber:
        _val = self.attrib[qn('w:themeShade')]

        return ST_UcharHexNumber(_val)  # type: ignore


class ST_TextEffect(ST_BaseEnumType):
    BlinkBackground = 'blinkBackground'
    Lights = 'lights'
    AntsBlack = 'antsBlack'
    AntsRed = 'antsRed'
    Shimmer = 'shimmer'
    Sparkle = 'sparkle'
    none = 'none'


class CT_TextEffect(OxmlBaseElement):
    @property
    def val(self) -> ST_TextEffect:
        _val = self.attrib[qn('w:val')]

        return ST_TextEffect(_val)


class ST_Border(ST_BaseEnumType):
    """17.18.2 ST_Border (边框样式)

    这个简单类型指定了可以为具有边框的WordprocessingML对象设置的边框类型。

    边框可以分为两种类型：

    - 线条边框，用于指定在绘制指定对象的边框时使用的图案。
    - 艺术边框，用于指定在绘制指定对象的边框时使用的重复图像。

    线条边框可以在任何允许设置边框的对象上指定，但艺术边框只能在页面级别使用，即在pgBorders元素（[§17.6.10]）下的边框。

    [示例：考虑一个结果如下的左边框WordprocessingML：

    <w:left w:val="single" …/>

    这个边框的val属性是single，表示边框样式为单线边框。示例结束]
    """

    Nil = 'nil'
    none = 'none'
    Single = 'single'
    Thick = 'thick'
    Double = 'double'
    Dotted = 'dotted'
    Dashed = 'dashed'
    DotDash = 'dotDash'
    DotDotDash = 'dotDotDash'
    Triple = 'triple'
    ThinThickSmallGap = 'thinThickSmallGap'
    ThickThinSmallGap = 'thickThinSmallGap'
    ThinThickThinSmallGap = 'thinThickThinSmallGap'
    ThinThickMediumGap = 'thinThickMediumGap'
    ThickThinMediumGap = 'thickThinMediumGap'
    ThinThickThinMediumGap = 'thinThickThinMediumGap'
    ThinThickLargeGap = 'thinThickLargeGap'
    ThickThinLargeGap = 'thickThinLargeGap'
    ThinThickThinLargeGap = 'thinThickThinLargeGap'
    Wave = 'wave'
    DoubleWave = 'doubleWave'
    DashSmallGap = 'dashSmallGap'
    DashDotStroked = 'dashDotStroked'
    ThreeDEmboss = 'threeDEmboss'
    ThreeDEngrave = 'threeDEngrave'
    Outset = 'outset'
    Inset = 'inset'
    Apples = 'apples'
    ArchedScallops = 'archedScallops'
    BabyPacifier = 'babyPacifier'
    BabyRattle = 'babyRattle'
    Balloons3Colors = 'balloons3Colors'
    BalloonsHotAir = 'balloonsHotAir'
    BasicBlackDashes = 'basicBlackDashes'
    BasicBlackDots = 'basicBlackDots'
    BasicBlackSquares = 'basicBlackSquares'
    BasicThinLines = 'basicThinLines'
    BasicWhiteDashes = 'basicWhiteDashes'
    BasicWhiteDots = 'basicWhiteDots'
    BasicWhiteSquares = 'basicWhiteSquares'
    BasicWideInline = 'basicWideInline'
    BasicWideMidline = 'basicWideMidline'
    BasicWideOutline = 'basicWideOutline'
    Bats = 'bats'
    Birds = 'birds'
    BirdsFlight = 'birdsFlight'
    Cabins = 'cabins'
    CakeSlice = 'cakeSlice'
    CandyCorn = 'candyCorn'
    CelticKnotwork = 'celticKnotwork'
    CertificateBanner = 'certificateBanner'
    ChainLink = 'chainLink'
    ChampagneBottle = 'champagneBottle'
    CheckedBarBlack = 'checkedBarBlack'
    CheckedBarColor = 'checkedBarColor'
    Checkered = 'checkered'
    ChristmasTree = 'christmasTree'
    CirclesLines = 'circlesLines'
    CirclesRectangles = 'circlesRectangles'
    ClassicalWave = 'classicalWave'
    Clocks = 'clocks'
    Compass = 'compass'
    Confetti = 'confetti'
    ConfettiGrays = 'confettiGrays'
    ConfettiOutline = 'confettiOutline'
    ConfettiStreamers = 'confettiStreamers'
    ConfettiWhite = 'confettiWhite'
    CornerTriangles = 'cornerTriangles'
    CouponCutoutDashes = 'couponCutoutDashes'
    CouponCutoutDots = 'couponCutoutDots'
    CrazyMaze = 'crazyMaze'
    CreaturesButterfly = 'creaturesButterfly'
    CreaturesFish = 'creaturesFish'
    CreaturesInsects = 'creaturesInsects'
    CreaturesLadyBug = 'creaturesLadyBug'
    CrossStitch = 'crossStitch'
    Cup = 'cup'
    DecoArch = 'decoArch'
    DecoArchColor = 'decoArchColor'
    DecoBlocks = 'decoBlocks'
    DiamondsGray = 'diamondsGray'
    DoubleD = 'doubleD'
    DoubleDiamonds = 'doubleDiamonds'
    Earth1 = 'earth1'
    Earth2 = 'earth2'
    Earth3 = 'earth3'
    EclipsingSquares1 = 'eclipsingSquares1'
    EclipsingSquares2 = 'eclipsingSquares2'
    EggsBlack = 'eggsBlack'
    Fans = 'fans'
    Film = 'film'
    Firecrackers = 'firecrackers'
    FlowersBlockPrint = 'flowersBlockPrint'
    FlowersDaisies = 'flowersDaisies'
    FlowersModern1 = 'flowersModern1'
    FlowersModern2 = 'flowersModern2'
    FlowersPansy = 'flowersPansy'
    FlowersRedRose = 'flowersRedRose'
    FlowersRoses = 'flowersRoses'
    FlowersTeacup = 'flowersTeacup'
    FlowersTiny = 'flowersTiny'
    Gems = 'gems'
    GingerbreadMan = 'gingerbreadMan'
    Gradient = 'gradient'
    Handmade1 = 'handmade1'
    Handmade2 = 'handmade2'
    HeartBalloon = 'heartBalloon'
    HeartGray = 'heartGray'
    Hearts = 'hearts'
    HeebieJeebies = 'heebieJeebies'
    Holly = 'holly'
    HouseFunky = 'houseFunky'
    Hypnotic = 'hypnotic'
    IceCreamCones = 'iceCreamCones'
    LightBulb = 'lightBulb'
    Lightning1 = 'lightning1'
    Lightning2 = 'lightning2'
    MapPins = 'mapPins'
    MapleLeaf = 'mapleLeaf'
    MapleMuffins = 'mapleMuffins'
    Marquee = 'marquee'
    MarqueeToothed = 'marqueeToothed'
    Moons = 'moons'
    Mosaic = 'mosaic'
    MusicNotes = 'musicNotes'
    Northwest = 'northwest'
    Ovals = 'ovals'
    Packages = 'packages'
    PalmsBlack = 'palmsBlack'
    PalmsColor = 'palmsColor'
    PaperClips = 'paperClips'
    Papyrus = 'papyrus'
    PartyFavor = 'partyFavor'
    PartyGlass = 'partyGlass'
    Pencils = 'pencils'
    People = 'people'
    PeopleWaving = 'peopleWaving'
    PeopleHats = 'peopleHats'
    Poinsettias = 'poinsettias'
    PostageStamp = 'postageStamp'
    Pumpkin1 = 'pumpkin1'
    PushPinNote2 = 'pushPinNote2'
    PushPinNote1 = 'pushPinNote1'
    Pyramids = 'pyramids'
    PyramidsAbove = 'pyramidsAbove'
    Quadrants = 'quadrants'
    Rings = 'rings'
    Safari = 'safari'
    Sawtooth = 'sawtooth'
    SawtoothGray = 'sawtoothGray'
    ScaredCat = 'scaredCat'
    Seattle = 'seattle'
    ShadowedSquares = 'shadowedSquares'
    SharksTeeth = 'sharksTeeth'
    ShorebirdTracks = 'shorebirdTracks'
    Skyrocket = 'skyrocket'
    SnowflakeFancy = 'snowflakeFancy'
    Snowflakes = 'snowflakes'
    Sombrero = 'sombrero'
    Southwest = 'southwest'
    Stars = 'stars'
    StarsTop = 'starsTop'
    Stars3d = 'stars3d'
    StarsBlack = 'starsBlack'
    StarsShadowed = 'starsShadowed'
    Sun = 'sun'
    swirligig = 'swirligig'
    TornPaper = 'tornPaper'
    TornPaperBlack = 'tornPaperBlack'
    Trees = 'trees'
    TriangleParty = 'triangleParty'
    Triangles = 'triangles'
    Triangle1 = 'triangle1'
    Triangle2 = 'triangle2'
    TriangleCircle1 = 'triangleCircle1'
    TriangleCircle2 = 'triangleCircle2'
    Shapes1 = 'shapes1'
    Shapes2 = 'shapes2'
    TwistedLines1 = 'twistedLines1'
    TwistedLines2 = 'twistedLines2'
    Vine = 'vine'
    Waveline = 'waveline'
    WeavingAngles = 'weavingAngles'
    WeavingBraid = 'weavingBraid'
    WeavingRibbon = 'weavingRibbon'
    WeavingStrips = 'weavingStrips'
    WhiteFlowers = 'whiteFlowers'
    Woodwork = 'woodwork'
    XIllusions = 'xIllusions'
    ZanyTriangles = 'zanyTriangles'
    ZigZag = 'zigZag'
    ZigZagStitch = 'zigZagStitch'
    Custom = 'custom'


class CT_Border(OxmlBaseElement):
    """17.3.4 边框属性 (CT_Border)

    这个常见的复合类型指定了用于定义对象边框的一组属性。

    【示例：考虑以下运行边框：


    <w:r>
        <w:rPr>
            <w:bdr w:val="single" w:sz="36" w:space="0" w:themeColor="accent1"
                w:themeTint="66" />
        </w:rPr>
        <w:t xml:space="preserve">run one</w:t>
    </w:r>
    bdr 元素指定了一个带有3.5点宽度的单线边框，使用文档的 accent1 主题颜色。结束示例】
    """

    @property
    def val_border(self):
        """val（边框样式）指定此对象使用的边框样式。

        此边框可以是艺术边框（沿边框重复的图像 - 仅用于页面边框）或线条边框（沿边框重复的线条格式） - 有关每种边框样式的描述，请参阅简单类型定义。

        【示例：考虑一个左边框，导致以下WordprocessingML：

        <w:left w:val="single" …/>

        此边框的val为single，表示边框样式为单线。示例结束】
        """

        _val = self.attrib.get(qn('w:val'))

        if _val is not None:
            return ST_Border(_val)

        return None

    @property
    def color(self) -> ST_HexColor:
        """指定此边框的颜色。

        此值可以定义为以下之一：

        - 使用RGB颜色模型的颜色值，其红色、绿色和蓝色值被写为0到255范围内的数字，以十六进制编码，并连接在一起。

            【示例：完全强度的红色将是255红色，0绿色，0蓝色，编码为FF、00、00，并连接为FF0000。示例结束】。RGB颜色在sRGB色彩空间中指定。

        - auto，以允许消费者自动确定边框颜色，以使文档的文本可读性。

            【示例：具有白色文本和自动背景颜色的文档可能会导致使用黑色背景，以确保内容的可读性。示例结束】

        【示例：考虑以下值为auto的边框颜色：


        <w:bottom … w:color="auto"/ >
        因此，此颜色可以由消费者自动修改，以便确保边框可以与页面的背景颜色区分开。示例结束】

        如果边框样式（val属性）指定使用艺术边框，则将忽略此属性。此外，如果边框通过themeColor属性指定使用主题颜色，则此值将被主题颜色值所取代。
        """
        _val = self.attrib.get(qn('w:color'))

        if _val is None:
            return ST_HexColorAuto.Auto

        return to_ST_HexColor(_val)  # type: ignore

    @property
    def themeColor(self) -> Optional[ST_ThemeColor]:
        """themeColor（边框主题颜色）

        指定用于生成边框颜色的基本主题颜色。边框颜色是与themeColor相关联的RGB值，进一步通过themeTint或themeShade（如果存在）进行变换，否则背景颜色是与themeColor相关联的RGB值。

        指定的主题颜色是对预定义主题颜色之一的引用，位于文档的主题部分（§14.2.7和§20.1.6.9），这允许在文档中集中设置颜色信息。

        要确定要显示的颜色，执行以下操作：

        - 使用ST_ThemeColor简单类型中指定的映射，读取clrSchemeMapping元素（§17.15.1.20）上的适当属性。
        - 使用该值和ST_ColorSchemeIndex简单类型中指定的映射，读取文档主题部分中的适当元素，以获取基本主题颜色。
        - 根据themeTint或themeShade属性的存在修改指定的颜色。

        【示例：考虑一组配置为使用accent2主题颜色的边框，导致以下的WordprocessingML标记：


        <w:top … w:themeColor="accent2" w:themeTint="99" />
        <w:bottom … w:themeColor="accent2" w:themeTint="99" />
        <w:left … w:themeColor="accent2" w:themeTint="99" />
        <w:right … w:themeColor="accent2" w:themeTint="99" />
        如果Settings部分包含以下标记：


        <w:clrSchemeMapping … w:accent2="accent 2"/>
        和Theme部分包含以下XML标记：


        <a:accent 2>
            <a:srgbClr val=" 4F81BD"/>
        </a:accent 2>

        则结果边框颜色将为95B3D7（应用到原始主题颜色的60%着色结果；有关详细信息，请参见下面的themeTint中的计算）。示例结束】
        """
        _val = self.attrib.get(qn('w:themeColor'))

        if _val is None:
            return

        return ST_ThemeColor(_val)

    @property
    def themeTint(self) -> Optional[ST_UcharHexNumber]:
        """themeTint（边框主题颜色色调）

        指定应用于此边框实例的提供的主题颜色（如果有）的色调值。如果themeColor属性不存在，则不使用此属性。

        如果提供了themeTint，则将其应用于主题颜色（来自主题部分）的RGB值，以确定应用于此边框的最终颜色。

        themeTint值以色调值（从0到255）的十六进制编码存储，应用于当前边框。

        【示例：考虑文档中应用了60％的色调值到边框。此色调值计算如下：


        𝑇𝑥𝑚𝑙 =0.6∗255
            =153
            =99（十六进制）

        文件格式中的结果themeTint值为99。示例结束】

        给定以RRGGBB格式定义的RGB颜色为三个十六进制值，色调应用如下：

        - 将颜色转换为HSL颜色格式（值从0到1）
        - 修改亮度因子如下：

            [应有公式]

        - 将得到的HSL颜色转换为RGB

        【示例：考虑一个使用accent2主题颜色的背景的文档，其RGB值（以RRGGBB十六进制格式）为4F81BD。

        等效的HSL颜色值为（213/360，0.45，0.53）。

        应用60％色调到亮度的色调公式，我们得到：


        𝐿′=0.53∗0.6+(1−.6)
        =0.71

        取得到的HSL颜色值（213/360，0.45，0.71）并转换回RGB，我们得到95B3D7。

        此转换值可以在结果背景的颜色属性中看到：

        <w:top w:val="single" w:sz="4" w :space="24"
            w:color=" 95B3D7" w:themeColor="accent2"
            w:themeTint="99"/>

        示例结束】
        """
        _val = self.attrib.get(qn('w:themeTint'))

        if _val is None:
            return

        return ST_UcharHexNumber(_val)  # type: ignore

    @property
    def themeShade(self) -> Optional[ST_UcharHexNumber]:
        """themeShade（边框主题颜色阴影）

        指定应用于此边框实例的提供的主题颜色（如果有）的阴影值。如果themeColor属性不存在，则不使用此属性。

        如果提供了themeTint，则将忽略此属性。

        如果提供了themeShade，则将其应用于主题颜色（来自主题部分）的RGB值，以确定应用于此边框的最终颜色。

        themeShade值以阴影值（从0到255）的十六进制编码存储，应用于当前边框。

        【示例：考虑文档中应用了40％的阴影值到边框。此阴影值计算如下：


        𝑆ℎ𝑎𝑑𝑒=0.4∗255
            =102
            =66（十六进制）
        文件格式中的结果themeShade值为66。示例结束】

        给定以RRGGBB格式定义的RGB颜色为三个十六进制值，阴影应用如下：

        - 将颜色转换为HSL颜色格式（值从0到1）
        - 修改亮度因子如下：

            [应有公式]

        - 将得到的HSL颜色转换为RGB

        【示例：考虑一个使用accent2主题颜色的背景的文档，其RGB值（以RRGGBB十六进制格式）为C0504D。

        等效的HSL颜色值为（1/360，0.48，0.53）。

        应用75％阴影到亮度的阴影公式，我们得到：

        𝐿′ = 0.53∗0.75
            = 0.39698

        取得到的HSL颜色值（1/360，0.48，0.39698）并转换回RGB，我们得到943634。

        此转换值可以在结果背景的颜色属性中看到：


        <w:top w:val="single" w:sz="4" w:space="24"
            w:color=" 943634" w:themeColor="accent2"
            w:themeShade="BF"/>
        示例结束】
        """
        _val = self.attrib.get(qn('w:themeShade'))

        if _val is None:
            return

        return ST_UcharHexNumber(_val)  # type: ignore

    @property
    def size(self) -> Optional[ST_EighthPointMeasure]:
        """sz（边框宽度）

        指定当前边框的宽度。

        如果边框样式（val属性）指定为线条边框，则此边框的宽度以点的八分之一为单位进行测量，最小值为2（四分之一点）最大值为96（十二点）。超出此范围的任何值都可以重新分配为更合适的值。

        如果边框样式（val属性）指定为艺术边框，则此边框的宽度以点为单位进行测量，最小值为1，最大值为31。超出此范围的任何值都可以重新分配为更合适的值。

        【示例：考虑一个所有边都为三点宽的虚线边框的文档，导致以下的WordprocessingML标记：


        <w:top w:val="dashed" w:sz="24" …/>
        <w:left w:val="dashed" w:sz="24" …/>
        <w:bottom w:val="dashed" w:sz="24" …/>
        <w:right w:val="dashed" w:sz="24" …/>

        使用val属性指定边框样式，并且由于该边框样式为线条边框（虚线），sz属性指定了大小为八分之一点（24八分之一点=3点）。示例结束】
        """
        _val = self.attrib.get(qn('w:sz'))

        if _val is None:
            return

        return ST_EighthPointMeasure(_val)  # type: ignore

    @property
    def space(self) -> Optional[ST_PointMeasure]:
        """space（边框间距测量）

        指定应用于将此边框放置在父对象上的间距偏移量。

        当文档具有相对于页面边缘的页面边框（在pgBorders的offsetFrom属性中使用page值（§17.6.10））时，它应指定页面边缘与此边框开始之间的距离，以点为单位。

        当文档具有相对于文本范围的页面边框（在pgBorders的offsetFrom属性中使用text值（§17.6.10））或任何其他边框类型时，它应指定对象边缘与此边框开始之间的距离，以点为单位。

        【示例：考虑一个文档，其中一组页面边框都被指定为距页面边缘24点。生成的WordprocessingML如下：

        <w:pgBorders w:offsetFrom="page">
            <w:bottom … w:space="24" />
        </w:pgBorders>

        offsetFrom属性指定space值提供了页面边框与页面边缘之间的偏移量，space属性的值指定页面偏移必须为24点。示例结束】
        """
        _val = self.attrib.get(qn('w:space'))

        if _val is None:
            return ST_PointMeasure(0)

        return ST_PointMeasure(_val)  # type: ignore

    @property
    def shadow(self) -> Optional[s_ST_OnOff]:
        """shadow（边框阴影）

        指定是否应修改此边框以创建阴影效果。

        对于右边和底部边框，这通过在正常边框位置的下方和右侧复制边框来实现。对于右边和顶部边框，这通过将边框移动到其原始位置的下方和右侧来实现。

        如果省略此属性，则不给边框添加阴影效果。

        【示例：考虑一个必须显示阴影效果的顶部边框，导致以下的WordprocessingML：

        <w:bottom w:shadow="true" … />

        此处frame的val为true，表示必须应用阴影效果到边框。示例结束】
        """
        _val = self.attrib.get(qn('w:shadow'))

        if _val is None:
            return

        return s_ST_OnOff(_val)

    @property
    def frame(self) -> Optional[s_ST_OnOff]:
        """frame（创建框架效果）

        指定是否应修改指定的边框以创建框架效果，即将边框的外观从最靠近文本的边缘反转到最远离文本的边缘。

        如果省略此属性，则不给边框添加任何框架效果。

        【示例：考虑一个必须显示框架效果的底部边框，在以下的WordprocessingML中指定如下：

        <w:bottom w:frame="true" … />

        此处frame的val为true，表示必须应用边框框架效果。示例结束】
        """
        _val = self.attrib.get(qn('w:frame'))

        if _val is None:
            return

        return s_ST_OnOff(_val)  # type: ignore


class ST_Shd(ST_BaseEnumType):
    Nil = 'nil'
    Clear = 'clear'
    Solid = 'solid'
    HorzStripe = 'horzStripe'
    VertStripe = 'vertStripe'
    ReverseDiagStripe = 'reverseDiagStripe'
    DiagStripe = 'diagStripe'
    HorzCross = 'horzCross'
    DiagCross = 'diagCross'
    ThinHorzStripe = 'thinHorzStripe'
    ThinVertStripe = 'thinVertStripe'
    ThinReverseDiagStripe = 'thinReverseDiagStripe'
    ThinDiagStripe = 'thinDiagStripe'
    ThinHorzCross = 'thinHorzCross'
    ThinDiagCross = 'thinDiagCross'
    Pct5 = 'pct5'
    Pct10 = 'pct10'
    Pct12 = 'pct12'
    Pct15 = 'pct15'
    Pct20 = 'pct20'
    Pct25 = 'pct25'
    Pct30 = 'pct30'
    Pct35 = 'pct35'
    Pct37 = 'pct37'
    Pct40 = 'pct40'
    Pct45 = 'pct45'
    Pct50 = 'pct50'
    Pct55 = 'pct55'
    Pct60 = 'pct60'
    Pct62 = 'pct62'
    Pct65 = 'pct65'
    Pct70 = 'pct70'
    Pct75 = 'pct75'
    Pct80 = 'pct80'
    Pct85 = 'pct85'
    Pct87 = 'pct87'
    Pct90 = 'pct90'
    Pct95 = 'pct95'


class CT_Shd(OxmlBaseElement):
    """17.3.5 着色属性 (CT_Shd)

    这个常见的复合类型指定了用于定义对象阴影的一组属性。

    【示例：考虑以下段落的阴影：

    <w:pPr>
        <w:shd w:val="pct20" w:themeColor="accent6" w:themeFill="accent3" />
    </w:pPr>

    生成的段落使用了 accent3 的背景色，在前景图案色 accent6 中使用了 pct20 的模式掩码。结束示例】
    """

    @property
    def val(self) -> ST_Shd:
        """val（底纹图案）

        指定用于在段落底纹的背景颜色上铺设图案颜色的图案。

        这个图案由一个掩码组成，应用于背景底纹颜色，以确定图案颜色应该显示的位置。下面引用的简单类型值显示了每个可能的掩码。

        【示例：考虑一个使用 10% 前景填充的阴影段落，生成的 WordprocessingML 如下所示：


        <w:shd w:val="pct10" … />

        这个底纹的 val 是 pct10，表示边框样式是 10% 的前景填充掩码。结束示例】

        The possible values for this attribute are defined by the ST_Shd simple type (§17.18.78).
        """
        _val = self.attrib[qn('w:val')]

        return ST_Shd(_val)

    @property
    def color(self) -> Optional[ST_HexColor]:
        """color（阴影图案颜色）

        指定用于此阴影的任何前景图案的颜色，使用 val 属性指定。

        这种颜色可以以十六进制值（RRGGBB 格式）表示，或者以 auto 表示，以便消费者可以根据需要自动确定前景阴影颜色。

        如果阴影样式（val 属性）指定不使用阴影格式或者省略，则此属性无效。另外，如果阴影通过 themeColor 属性指定使用主题颜色，则该值将被主题颜色值所取代。

        如果省略了此属性，则其值将被视为 auto。

        【示例：考虑具有前景颜色值为 auto 的样式为 pct20 的阴影，如下所示：

        <w:shd w:val="pct20"… w:color="auto"/>

        因此，此阴影图案的前景颜色可以根据需要自动调整，例如，以确保阴影颜色与页面的背景颜色相区分。结束示例】
        """
        _val = self.attrib.get(qn('w:color'))

        if _val is None:
            return

        return to_ST_HexColor(_val)  # type: ignore

    @property
    def themeColor(self) -> Optional[ST_ThemeColor]:
        """themeColor（阴影图案主题颜色）

        指定一个主题颜色，应用于使用 val 属性指定的任何前景图案的阴影。

        指定的主题颜色是对文档主题部分中预定义的主题颜色之一的引用，这允许在文档中集中设置颜色信息。

        如果省略了此属性，则不应用任何主题颜色，而应使用 color 属性来确定阴影图案颜色。

        【示例：考虑一个段落，其背景必须由一个主题颜色 accent3 和一个主题颜色 accent6 叠加，使用 20% 的填充图案。这个要求使用以下 WordprocessingML 来指定：


        <w:pPr>
            <w:shd w:val="pct20" w:themeColor="accent6"
                w:themeFill="accent3" />
        </w:pPr>

        生成的段落在由 pct20 模式掩码指定的区域中使用了前景图案颜色 accent6。结束示例】
        """
        _val = self.attrib.get(qn('w:themeColor'))

        if _val is None:
            return

        return ST_ThemeColor(_val)

    @property
    def themeTint(self) -> Optional[ST_UcharHexNumber]:
        """themeTint（底纹图案主题颜色色调）

        指定应用于所提供的主题颜色（如果有）的色调值，用于此底纹颜色实例。

        如果提供了 themeTint，则将应用于来自主题部分的 themeFill 颜色的 RGB 值，以确定应用于此边框的最终颜色。

        themeTint 值以十六进制编码的色调值（从 0 到 255）存储，应用于当前边框。

        【示例：考虑在文档中应用了 60% 的边框色调。这个色调的计算如下：

        𝑆𝑥𝑚𝑙 = 0.6 ∗ 255
            = 153
            = 99(ℎ𝑒𝑥)

        文件格式中得到的 themeTint 值将是 99。结束示例】

        """
        _val = self.attrib.get(qn('w:themeTint'))

        if _val is None:
            return

        return ST_UcharHexNumber(_val)  # type: ignore

    @property
    def themeShade(self) -> Optional[ST_UcharHexNumber]:
        """themeShade（底纹图案主题颜色阴影）

        指定应用于所提供的主题颜色（如果有）的阴影值，用于此底纹颜色。

        如果提供了 themeTint，则将忽略此属性的值。

        如果提供了 themeShade，则将应用于来自主题部分的 themeColor 颜色的 RGB 值，以确定应用于此边框的最终颜色。

        themeShade 值以十六进制编码的应用于当前边框的阴影值（从 0 到 255）存储。

        【示例：考虑在文档中应用了 40% 的底纹阴影颜色。这个阴影的计算如下：

        𝑆𝑥𝑚𝑙 = 0.4 ∗ 255
            = 102
            = 66(ℎ𝑒𝑥)

        文件格式中得到的 themeFillShade 值将是 66。结束示例】
        """
        _val = self.attrib.get(qn('w:themeShade'))

        if _val is None:
            return

        return ST_UcharHexNumber(_val)  # type: ignore

    @property
    def fill(self) -> Optional[ST_HexColor]:
        """fill（阴影背景颜色）

        指定用于此阴影背景的颜色。

        这种颜色可以以十六进制值（RRGGBB 格式）表示，或者以 auto 表示，以便消费者可以根据需要自动确定背景阴影颜色。

        如果省略了此属性，则其值将被视为 auto。

        【示例：考虑使用十六进制值 C3D69B 作为背景颜色的阴影，使用以下 WordprocessingML：


        <w:shd w:val="pct15" w:fill="C3D69B" />
        因此，此阴影的背景颜色是十六进制值为 C3D69B 的颜色。结束示例】

        如果阴影通过 themeFill 属性指定使用主题颜色，则该值将被主题颜色值所取代。
        """
        _val = self.attrib.get(qn('w:fill'))

        if _val is None:
            return

        return to_ST_HexColor(_val)  # type: ignore

    @property
    def themeFill(self) -> Optional[ST_ThemeColor]:
        """themeFill（阴影背景主题颜色）

        指定应用于此阴影背景的主题颜色。

        指定的主题颜色是对文档主题部分中预定义的主题颜色之一的引用，这允许在文档中集中设置颜色信息。

        如果省略了此属性，则不应用任何主题颜色，而应使用 fill 属性来确定阴影背景颜色。

        【示例：考虑一个段落，其背景必须由一个主题颜色 accent3 和一个主题颜色 accent6 叠加，使用 20% 的填充图案。这个要求使用以下 WordprocessingML 来指定：


        <w:shd w:val="pct20" w:themeColor="accent6"
        w:themeFill="accent3" />

        生成的阴影使用了由 accent3 主题颜色指定的背景颜色。结束示例】
        """
        _val = self.attrib.get(qn('w:themeFill'))

        if _val is None:
            return

        return ST_ThemeColor(_val)  # type: ignore

    @property
    def themeFillTint(self) -> Optional[ST_UcharHexNumber]:
        """themeFillTint（底纹背景主题颜色色调）

        指定应用于所提供的主题颜色（如果有）的色调值，用于此底纹实例。

        如果提供了 themeFillTint，则它将应用于来自主题部分的 themeFill 颜色的 RGB 值，以确定应用于此边框的最终颜色。

        themeFillTint 值以十六进制编码的色调值（从 0 到 255）存储，应用于当前边框。

        【示例：考虑在文档中应用了 60% 的边框色调。这个色调的计算如下：

        𝑆𝑥𝑚𝑙 = 0.6 ∗ 255
            = 153
            = 99(ℎ𝑒𝑥)

        文件格式中得到的 themeFillTint 值将是 99。结束示例】
        """
        _val = self.attrib.get(qn('w:themeFillTint'))

        if _val is None:
            return

        return ST_UcharHexNumber(_val)  # type: ignore

    @property
    def themeFillShade(self) -> Optional[ST_UcharHexNumber]:
        """themeFillShade（底纹背景主题颜色阴影）

        指定应用于所提供的主题颜色（如果有）的阴影值，用于此底纹颜色。

        如果提供了 themeFillShade，则它将应用于来自主题部分的 themeFill 颜色的 RGB 值，以确定应用于此边框的最终颜色。

        themeFillShade 值以十六进制编码的阴影值（从 0 到 255）存储，应用于当前边框。

        【示例：考虑在文档中应用了 40% 的背景底纹颜色的阴影。这个阴影的计算如下：

        𝑆𝑥𝑚𝑙 = 0.4 ∗ 255
            = 102
            = 66(ℎ𝑒𝑥)

        文件格式中得到的 themeFillShade 值将是 66。结束示例】
        """
        _val = self.attrib.get(qn('w:themeFillShade'))

        if _val is None:
            return

        return ST_UcharHexNumber(_val)  # type: ignore


class CT_VerticalAlignRun(OxmlBaseElement):
    """17.3.2.42 vertAlign (下标/上标文本)

    该元素指定对当前运行内容相对于运行文本的默认外观应用的对齐方式。这允许文本被重新定位为下标或上标，而不改变运行属性的字体大小。

    如果此元素不存在，则默认值是保留应用于样式层次结构中先前级别的格式。如果此元素在样式层次结构中从未应用，则文本相对于运行内容的默认基线位置不应为下标或上标。

    【示例：考虑一个运行，其内容在显示时必须定位为上标。此要求可以使用以下 WordprocessingML 指定：

    <w:rPr>
        <w:vertAlign w:val="superscript" />
    </w:rPr>

    结果运行被定位为上标，因此它以较小的尺寸呈现在运行内容的默认基线位置之上。示例结束】
    """

    @property
    def val(self) -> s_ST_VerticalAlignRun:
        """val（下标/上标值）

        指定应用于当前运行内容的垂直对齐类型。

        【示例：考虑一个运行，其内容在显示时必须定位为上标。此要求可以使用以下 WordprocessingML 指定：

        <w:rPr>
            <w:vertAlign w:val="superscript" />
        </w:rPr>

        val 属性的值为 superscript，因此运行的内容以较小的尺寸呈现在运行内容的默认基线位置之上。示例结束】
        """
        _val = self.attrib[qn('w:val')]

        return s_ST_VerticalAlignRun(_val)


class CT_FitText(OxmlBaseElement):
    """17.3.2.14 fitText (手动运行宽度)¶

    fitText (Manual Run Width)

    该元素指定此运行的内容不应基于其内容的宽度自动显示，而是其内容应调整大小以适应 val 属性指定的宽度。当显示时，应通过等比例增加/减少此运行内容中每个字符的大小来执行此扩展/收缩。

    如果省略了该元素，则此运行的内容将根据其内容的大小进行显示。

    [示例：考虑一个文档，其中有一个运行，必须在正好半英寸的空间中显示，而不考虑其内容。可以使用以下 WordprocessingML 指定此约束：

    <w:r>
        <w:rPr>
            <w:fitText w:id="50" w:val="720" />
        </w:rPr>
        <w:t>This text must be displayed in one-half of an inch.</w:t>
    </w:r>

    当在文档中显示时，结果运行内容必须正好显示为 720 个二十分之一点（半英寸）。示例结束]
    """

    @property
    def val(self) -> s_ST_TwipsMeasure:
        """val（数值）

        此属性指定文档中显示时此运行应适应的确切宽度空间。

        [示例：考虑一个文档，其中有一个运行，必须在正好半英寸的空间中显示，而不考虑其内容。可以使用以下 WordprocessingML 指定此约束：

        <w:r>
            <w:rPr>
                <w:fitText w:id="50" w:val="720" />
            </w:rPr>
            <w:t>This text must be displayed in one-half of an inch.</w:t>
        </w:r>

        当在文档中显示时，结果运行内容必须正好显示为 720 个二十分之一点（半英寸）。示例结束]
        """
        _val = self.attrib[qn('w:val')]

        return s_to_ST_TwipsMeasure(_val)  # type: ignore

    @property
    def id(self) -> Optional[ST_DecimalNumber]:
        """id（适应文本运行标识符）

        指定一个唯一的标识符，用于将包含 fitText 元素的多个连续运行相互链接，以确保它们的内容在文档中正确合并到指定的宽度中。

        这意味着，由于格式上的差异而被分隔成多个运行的多个运行可以被识别为属于同一组适应文本属性，尽管它们在 WordprocessingML 中是多个文本运行。

        如果运行不是连续的，则将忽略 id 属性，并且运行不会被链接。

        如果省略了此属性，则此运行没有 id，并且不会与父段落中的任何其他运行链接。

        [示例：考虑文档中的以下三个运行，这些运行在显示时应该适应到正好一英寸：

        <w:r>
            <w:rPr>
                <w:fitText w:id="99" w:val="1440" />
            </w:rPr>
            <w:t>fit this into</w:t>
        </w:r>
        <w:r>
            <w:rPr>
                <w:b/>
                <w:fitText w:id="99" w:val="1440" />
            </w:rPr>
            <w:t>one</w:t>
        </w:r>
        <w:r>
            <w:rPr>
                <w:fitText w:id="99" w:val="1440" />
            </w:rPr>
            <w:t>inch</w:t>
        </w:r>

        尽管有三个内容运行，但根据所有三个运行中使用的相同 id 属性值，所有三个区域必须合并为单个适应文本区域（例如，它们全部适应到一英寸，而不是每个都适应到一英寸）。示例结束]
        """
        _val = self.attrib.get(qn('w:id'))

        if _val is None:
            return

        return ST_DecimalNumber(_val)  # type: ignore


class ST_Em(ST_BaseEnumType):
    """17.18.24 ST_Em (强调标记类型)

    该简单类型指定一个强调标记的枚举列表，可以选择其中任何一个应用于运行中的每个非空字符。当显示时，强调标记相对于其所应用字符的位置取决于语言和书写方向。当显示时，强调标记所用的字形是由实现决定的。

    【示例】考虑一个需要应用点强调标记的文本运行。这可以使用以下WordprocessingML指定：

    <w:rPr>
        <w:em w:val="dot"/>
    </w:rPr>

    结束示例

    该简单类型的内容是对W3C XML Schema字符串数据类型的限制。

    该简单类型限制为以下表中的值：

    - circle（圆形强调标记）

        指定强调标记是一个圆形。[注意：意图是使用类似于以下的强调标记：

    - dot（点强调标记）

        指定强调标记是一个点。[注意：意图是使用类似于以下的强调标记：

    - comma（逗号强调标记）

        指定强调标记是一个逗号。[注意：意图是使用类似于以下的强调标记：

    - underDot（字符下方的点强调标记）

        指定强调标记是一个点，应该在水平书写时呈现在每个字符的下方，垂直书写时在左边。[注意：意图是使用类似于以下的强调标记：

    - none（无强调标记）

        指定在运行中的任何字符上不应用任何强调标记。

    [注意：通常情况下，强调标记相对于其应用字符的位置由语言和书写方向自动决定。因此，不需要明确指定位置，并且不建议使用此值。结束注意]
    """

    none = 'none'
    """指定在运行中的任何字符上不应用任何强调标记。"""

    Dot = 'dot'
    """指定强调标记是一个点。"""

    Comma = 'comma'
    """指定强调标记是一个逗号。"""

    Circle = 'circle'
    """指定强调标记是一个圆形。"""

    UnderDot = 'underDot'
    """指定强调标记是一个点，应该在水平书写时呈现在每个字符的下方，垂直书写时在左边。"""


class CT_Em(OxmlBaseElement):
    """17.3.2.12 em (强调标记)

    该元素指定应该应用于该运行中的每个非空格字符的强调标记。强调标记是一个附加字符，其显示位置相对于应用的字符是依赖于语言和书写方向的。强调标记由 val 属性的内容指定。如果该元素不存在，则默认值是保留样式层次结构中先前级别应用的格式。如果该元素在样式层次结构中从未应用过，则不会对该运行中的任何字符应用任何强调标记。

    [示例：考虑一个文本运行，其应该具有点形式的强调标记。可以使用以下 WordprocessingML 指定此约束：

    <w:rPr>
        <w:em w:val="dot"/>
    </w:rPr>

    示例结束]
    """

    @property
    def val(self) -> ST_Em:
        """val (强调标记类型)

        指定应用于该运行中每个非空格字符的强调标记。
        """

        _val = self.attrib[qn('w:val')]

        return ST_Em(_val)  # type: ignore


class CT_Language(OxmlBaseElement):
    """17.3.2.20 lang (运行内容的语言)

    该元素指定在处理此运行的内容时，应使用哪些语言来检查拼写和语法（如果请求）。

    如果该元素不存在，则默认值是保留样式层次结构中先前级别应用的格式。如果该元素在样式层次结构中从未应用过，则将自动根据其内容使用任何所需的方法来确定此运行内容的语言。

    [示例：考虑一个包含拉丁字符和复杂脚本字符的运行。如果这些内容应分别被解释为法语（加拿大）和希伯来语，那么在生成的 WordprocessingML 中，该要求将被指定如下：

    <w:r>
        <w:rPr>
            <w:lang w:val="fr-CA" w:bidi="he-IL" />
        </w:rPr>
    </w:r>

    生成的运行指定了任何复杂脚本内容必须被视为希伯来语进行拼写和语法检查，而任何拉丁字符内容必须被视为法语（加拿大）进行拼写和语法检查。示例结束]
    """

    @property
    def val(self) -> Optional[s_ST_Lang]:
        """val（拉丁语言）

        指定处理此运行的内容时应使用的语言，这些内容使用了拉丁字符，由运行内容的 Unicode 字符值确定。

        如果省略了此属性，则将根据内容自动确定使用拉丁字符的此运行的语言，使用任何适当的方法。

        [示例：考虑一个包含拉丁字符的运行。如果这些内容应被解释为英语（加拿大），那么在生成的 WordprocessingML 中，该要求将被指定如下：

        <w:r>
            <w:rPr>
                <w:lang w:val="en-CA" />
            </w:rPr>
        </w:r>

        生成的运行指定了任何拉丁字符内容必须使用英语（加拿大）词典和语法引擎进行拼写和语法检查（如果可用）。示例结束]
        """
        _val = self.attrib.get(qn('w:val'))

        if _val is None:
            return

        return s_ST_Lang(_val)  # type: ignore

    @property
    def eastAsia(self) -> Optional[s_ST_Lang]:
        """eastAsia（东亚语言）

        指定处理此运行的内容时应使用的语言，这些内容使用了东亚字符，由运行内容的 Unicode 字符值确定。

        如果省略了此属性，则将根据内容自动确定使用东亚字符的此运行的语言，使用任何适当的方法。

        [示例：考虑一个包含东亚字符的运行。如果这些内容应被解释为韩语，那么在生成的 WordprocessingML 中，该要求将被指定如下：

        <w:r>
            <w:rPr>
                <w:lang w:eastAsia="ko-KR" />
            </w:rPr>
        </w:r>

        生成的运行指定了任何东亚字符内容必须使用韩语词典和语法引擎进行拼写和语法检查（如果可用）。示例结束]
        """
        _val = self.attrib.get(qn('w:eastAsia'))

        if _val is None:
            return

        return s_ST_Lang(_val)  # type: ignore

    @property
    def bidi(self) -> Optional[s_ST_Lang]:
        """bidi（复杂脚本语言）

        指定处理此运行的内容时应使用的语言，这些内容使用了复杂脚本字符，由运行内容的 Unicode 字符值确定。

        如果省略了此属性，则将根据内容自动确定使用复杂脚本字符的此运行的语言，使用任何适当的方法。

        [示例：考虑一个包含复杂脚本字符的运行。如果这些内容应被解释为希伯来语，那么在生成的 WordprocessingML 中，该要求将被指定如下：

        <w:r>
            <w:rPr>
                <w:lang w:bidi="he-IL" />
            </w:rPr>
        </w:r>

        生成的运行指定了任何复杂脚本内容必须使用希伯来语词典和语法引擎进行拼写和语法检查（如果可用）。示例结束]
        """
        _val = self.attrib.get(qn('w:bidi'))

        if _val is None:
            return

        return s_ST_Lang(_val)  # type: ignore


class ST_CombineBrackets(ST_BaseEnumType):
    """17.18.8 ST_CombineBrackets (两行合一封闭字符类型)

    ST_CombineBrackets (Two Lines in One Enclosing Character Type)

    这个简单类型指定了在显示当前运行中的文本时，用于括住“两行合一”文本的括号字符类型。

    [示例：考虑一个段落，其中包含文本“two lines in one”，该文本必须在文档中显示为一个逻辑行并用花括号括起来。这一约束可以在WordprocessingML中如下指定：

    <w:r>
        <w:rPr>
            <w:eastAsianLayout w:id="1" w:combine="on" w:combineBrackets="curly"/>
        </w:rPr>
        <w:t>two lines in one</w:t>
    </w:r>
    结果文本将在一行中的其他文本内显示为两行并用花括号括起来。示例结束]

    这个简单类型的内容是W3C XML Schema字符串数据类型的一个限制。

    这个简单类型仅限于下表中列出的值：

    angle（尖括号）

        指定使用尖括号字符括住当前运行的“两行合一”文本内容。

        [示例：<…> 示例结束]

    curly（花括号）

        指定使用花括号字符括住当前运行的“两行合一”文本内容。

        [示例：{…} 示例结束]

    none（无括号）

        指定不使用任何字符括住当前运行的“两行合一”文本内容。

    round（圆括号）

        指定使用圆括号字符括住当前运行的“两行合一”文本内容。

        [示例：(…) 示例结束]

    square（方括号）

        指定使用方括号字符括住当前运行的“两行合一”文本内容。

        [示例：[…] 示例结束]
    """

    none = 'none'
    """（无括号）

        指定不使用任何字符括住当前运行的“两行合一”文本内容。
    """

    Round = 'round'
    """（圆括号）

        指定使用圆括号字符括住当前运行的“两行合一”文本内容。
    """

    Square = 'square'
    """（方括号）

        指定使用方括号字符括住当前运行的“两行合一”文本内容。

        [示例：[…] 示例结束]
    """

    Angle = 'angle'
    """（尖括号）

        指定使用尖括号字符括住当前运行的“两行合一”文本内容。

        [示例：<…> 示例结束]
    """

    Curly = 'curly'
    """（花括号）

        指定使用花括号字符括住当前运行的“两行合一”文本内容。

        [示例：{…} 示例结束]
    """


class CT_EastAsianLayout(OxmlBaseElement):
    """17.3.2.10 eastAsianLayout (东亚版式设置)

    该元素指定应用于运行内容的任何东亚排版设置。此元素表示的具体排版设置包括“两行合一”和“横排竖排”选项。

    “两行合一”设置指定该运行中的字符应在文档中的单行上写出，通过在常规行内创建两个子行，并在这些子行之间均匀布局文本来实现。

    [示例：考虑一个段落，其中包含文本“两行合一”，必须在文档中的单个逻辑行内显示。在 WordprocessingML 中，可以将此约束指定为：

    <w:r>
        <w:rPr>
            <w:eastAsianLayout w:id="1" w:combine="on" />
        </w:rPr>
        <w:t>两行合一</w:t>
    </w:r>

    结果文本将显示在其他文本的两个子行内，如下所示：

    示例结束]

    “横排竖排”设置指定该运行中的字符应在文档中显示时向左旋转 90 度，而在段落中保持与所有其他文本在同一行。

    [示例：考虑一个段落，其中包含文本“this word is vertical”，其中单词“vertical”必须在文档中垂直显示。在 WordprocessingML 中，可以将此约束指定为：

    <w:r>
        <w:rPr>
            <w:eastAsianLayout w:id="2" w:vert="on" />
        </w:rPr>
        <w:t>vertical</w:t>
    </w:r>

    结果文本将与其他文本内容呈 90 度旋转。示例结束]
    """

    @property
    def id(self) -> Optional[ST_DecimalNumber]:
        """id（东亚排版运行标识符）

        指定一个唯一的标识符，用于将包含 eastAsianLayout 元素的多个运行相互链接，以确保它们的内容在文档中正确显示。

        这意味着，由于格式上的差异而被分隔成多个运行文本的多个运行可以被识别为属于同一组东亚排版属性，尽管它们被分成多个运行。

        [示例：考虑文档中的以下三个运行：

        <w:r>
            <w:rPr>
                <w:eastAsianLayout w:id="-1552701694" w:combine="lines" w:combineBrackets="curly" />
            </w:rPr>
            <w:t>two</w:t>
        </w:r>
        <w:r>
            <w:rPr>
                <w:u w:val="single" w:color="4F81BD" w:themeColor="accent1" />
                <w:eastAsianLayout w:id="-1552701694" w:combine="lines" w:combineBrackets="curly" />
            </w:rPr>
            <w:t>lines in</w:t>
        </w:r>
        <w:r>
            <w:rPr>
                <w:eastAsianLayout w:id="-1552701694" w:combine="lines" w:combineBrackets="curly" />
            </w:rPr>
            <w:t>one</w:t>
        </w:r>

        尽管有三个内容运行，但基于 id 属性中的相同值，所有三个区域必须组合成一个“两行合一”的区域。示例结束]
        """
        _val = self.attrib.get(qn('w:id'))

        if _val is None:
            return

        return ST_DecimalNumber(_val)  # type: ignore

    @property
    def combine(self) -> Optional[s_ST_OnOff]:
        """combine（两行合一）

        指定当前运行的内容是否应使用上面在父元素中描述的“两行合一”逻辑组合成一行。

        如果省略了此属性，则此运行将不会显示在两个子行上。

        [示例：考虑一个段落，其中包含文本“两行合一”，必须在文档中的单个逻辑行内显示。在 WordprocessingML 中，可以将此约束指定为：

        <w:r>
            <w:rPr>
                <w:eastAsianLayout w:id="1" w:combine="on" />
            </w:rPr>
            <w:t>两行合一</w:t>
        </w:r>

        结果文本将显示在此行上的其他文本的两个子行内。示例结束]
        """
        _val = self.attrib.get(qn('w:combine'))

        if _val is None:
            return

        return s_ST_OnOff(_val)  # type: ignore

    @property
    def combineBrackets(self) -> Optional[ST_CombineBrackets]:
        """combineBrackets（显示两行合一的括号）

        指定在显示时两行合一文本应该被括号括起来。此属性的值确定括号样式，用于放置在组合文本周围。

        如果未指定此属性，则在文档中显示时不会在此内容周围放置括号。如果未指定 combine 属性，则将忽略此属性。

        [示例：考虑一个段落，其中包含文本“两行合一”，必须在文档中的单个逻辑行内显示，并在花括号内显示。在 WordprocessingML 中，可以将此约束指定为：

        <w:r>
            <w:rPr>
                <w:eastAsianLayout w:id="1" w:combine="on"
                    w:combineBrackets="curly"/>
            </w:rPr>
            <w:t>两行合一</w:t>
        </w:r>

        结果文本将在此行上的其他文本内显示两个子行，并在显示时用花括号括起来。示例结束]
        """
        _val = self.attrib.get(qn('w:combineBrackets'))

        if _val is None:
            return

        return ST_CombineBrackets(_val)  # type: ignore

    @property
    def vert(self) -> Optional[s_ST_OnOff]:
        """vert（横排竖排（旋转文本））

        指定在文档中显示时，此运行中的字符应与其他内容相比，向左旋转 270 度。

        如果省略了此属性，则此运行的内容不会相对于正常文本流进行旋转。

        [示例：考虑一个段落，其中包含文本“this word is vertical”，其中单词“vertical”必须在文档中垂直显示。在 WordprocessingML 中，可以将此约束指定为：

        <w:r>
            <w:rPr>
                <w:eastAsianLayout w:id="2" w:vert="on" />
            </w:rPr>
            <w:t>vertical</w:t>
        </w:r>

        结果文本将与其他文本内容呈 270 度旋转。示例结束]
        """
        _val = self.attrib.get(qn('w:vert'))

        if _val is None:
            return

        return s_ST_OnOff(_val)  # type: ignore

    @property
    def vertCompress(self) -> Optional[s_ST_OnOff]:
        """vertCompress（压缩旋转文本至行高）

        指定在显示时，旋转的文本是否应压缩，以确保它适合现有行高，而不会增加行的整体高度。

        如果未指定 vert 属性，则将忽略此属性。如果省略了此属性，则当文本被旋转时不会压缩以适应行的现有高度。

        [示例：考虑一个段落，其中包含文本“this word is vertical”，其中单词“vertical”必须在文档中垂直显示，但不能改变行的高度。在 WordprocessingML 中，可以将此约束指定为：

        <w:r>
            <w:rPr>
                <w:eastAsianLayout w:id="2" w:vert="true"
                    w:vertCompress="true" />
            </w:rPr>
            <w:t>vertical</w:t>
        </w:r>

        结果文本将被压缩以适应所有非压缩字符定义的行高。示例结束]
        """
        _val = self.attrib.get(qn('w:vertCompress'))

        if _val is None:
            return

        return s_ST_OnOff(_val)  # type: ignore


class ST_HeightRule(ST_BaseEnumType):
    """17.18.37 ST_HeightRule (高度规则)

    该简单类型指定了在文档中显示时，父对象高度计算所采用的逻辑。

    【示例】考虑以下表格行：

    <w:trPr>
        <w:trHeight w:hRule="atLeast" w:val="2189" />
    </w:trPr>

    val属性指定了2189个点的二十分之一，因此，无论其内容如何，此表格行的高度至少为2189个点的二十分之一，因为其hRule值设置为atLeast。示例结束

    该简单类型的内容是对W3C XML Schema字符串数据类型的限制。

    该简单类型受限于以下表中列出的值：

    atLeast（最小高度）

        指定父对象的高度至少应为指定值，但可以根据需要扩展以适应其内容。

    auto（根据内容确定高度）

        指定父对象的高度应自动根据其内容的大小确定，没有预先确定的最小或最大大小。

    exact（确切高度）

        指定父对象的高度应完全按照指定值确定，而不考虑对象内容的大小。

        如果内容太大而超出指定的高度，则会被裁剪。
    """

    Auto = 'auto'
    """（根据内容确定高度）

        指定父对象的高度应自动根据其内容的大小确定，没有预先确定的最小或最大大小。
    """

    Exact = 'exact'
    """（确切高度）

        指定父对象的高度应完全按照指定值确定，而不考虑对象内容的大小。

        如果内容太大而超出指定的高度，则会被裁剪。
    """

    AtLeast = 'atLeast'
    """（最小高度）

        指定父对象的高度至少应为指定值，但可以根据需要扩展以适应其内容。
    """


class ST_Wrap(ST_BaseEnumType):
    """17.18.104 ST_Wrap (文本环绕文本框架类型)

    ST_Wrap (Text Wrapping around Text Frame Type)

    这个简单类型指定文本框在文档中允许的文本环绕类型。

    【示例：考虑以下指定文本框的WordprocessingML片段：

    <w:p>
        <w:pPr>
            <w:framePr w:w="2419" w:h="2189" w:hRule="atLeast" w:hSpace="187"
                w:wrap="around" w:vAnchor="text" w:hAnchor="page" w:x="1643" w:y="73" />
        </w:pPr>
        <w:r>
            <w:t>Text Frame Content.</w:t>
        </w:r>
    </w:p>

    这个文本框上的wrap属性指定了渲染框架在页面上时，任何本应该流经相同行的非文本框段落都必须允许环绕。]

    这个简单类型的内容是对W3C XML Schema字符串数据类型的限制。

    这个简单类型限制了以下表中列出的值：

    around（允许文本环绕框）

        指定文本可以环绕文档中此文本框周围每行上的剩余空间。

    auto（默认文本环绕框）

        指定文本将具有显示WordprocessingML文档的应用程序在文本框周围显示文本环绕方面的默认应用定义行为。

    none（禁止文本环绕框）

        指定文本不得以每行上的剩余空间围绕文本框。

        因此，任何文本内容都必须放置在不与框架范围相交的下一行上。

    notBeside（旁边禁止文本环绕框）

        指定文本不得以每行上的剩余空间围绕文本框。

        因此，任何文本内容都必须放置在不与框架范围相交的下一行上。

    through（穿越文本环绕框）

        指定文本可以环绕文档中此文本框周围每行上的剩余空间。

    tight（紧密文本环绕框）

        指定文本可以紧密环绕文档中此文本框周围每行上的剩余空间。
    """

    Auto = 'auto'
    """（默认文本环绕框）

        指定文本将具有显示WordprocessingML文档的应用程序在文本框周围显示文本环绕方面的默认应用定义行为。
    """

    NotBeside = 'notBeside'
    """（旁边禁止文本环绕框）

        指定文本不得以每行上的剩余空间围绕文本框。

        因此，任何文本内容都必须放置在不与框架范围相交的下一行上。
    """

    Around = 'around'
    """（允许文本环绕框）

        指定文本可以环绕文档中此文本框周围每行上的剩余空间。
    """

    Tight = 'tight'
    """（紧密文本环绕框）

        指定文本可以紧密环绕文档中此文本框周围每行上的剩余空间。
    """

    Through = 'through'
    """（穿越文本环绕框）

        指定文本可以环绕文档中此文本框周围每行上的剩余空间。
    """

    none = 'none'
    """（禁止文本环绕框）

        指定文本不得以每行上的剩余空间围绕文本框。

        因此，任何文本内容都必须放置在不与框架范围相交的下一行上。
    """


class ST_VAnchor(ST_BaseEnumType):
    """17.18.100 ST_VAnchor (垂直锚点位置)¶

    ST_VAnchor (Vertical Anchor Location)

    这种简单类型指定了父对象在文档中被锚定的垂直位置。此锚定位置将被用作确定文档中对象最终垂直位置的基准位置。

    [示例：考虑一个文本框，应该在从左到右的文档中位于其列的右侧一英寸处。此文本框将使用以下WordprocessingML进行指定：

    <w:pPr>
        <w:framePr … w:y="1440" w:vAnchor="page" />
    </w:pPr>

    这些框架垂直锚定属性指定它们相对于锚定段落的页面。示例结束]

    这种简单类型的内容是对W3C XML Schema字符串数据类型的限制。

    这种简单类型被限制为以下表中列出的值：

    margin（相对于页边距）

        指定父对象应垂直锚定到文本边距。

        这将用于指定任何垂直定位值应根据文本边距的位置计算。

    page（相对于页面）

        指定父对象应垂直锚定到页面边缘。

        这将用于指定任何垂直定位值应根据页面边缘的位置计算。

    text（相对于垂直文本范围）

        指定父对象应垂直锚定到文本范围。

        这将用于指定任何垂直定位值应根据锚定段落中文本顶部边缘的位置计算。
    """

    Text = 'text'
    """（相对于垂直文本范围）

        指定父对象应垂直锚定到文本范围。

        这将用于指定任何垂直定位值应根据锚定段落中文本顶部边缘的位置计算。
    """

    Margin = 'margin'
    """（相对于页边距）

        指定父对象应垂直锚定到文本边距。

        这将用于指定任何垂直定位值应根据文本边距的位置计算。
    """

    Page = 'page'
    """（相对于页面）

        指定父对象应垂直锚定到页面边缘。

        这将用于指定任何垂直定位值应根据页面边缘的位置计算。
    """


class ST_HAnchor(ST_BaseEnumType):
    """17.18.35 ST_HAnchor (水平锚点位置)¶

    ST_HAnchor (Horizontal Anchor Location)

    该简单类型指定了父对象在文档中锚定的水平位置。此锚定位置将被用作确定文档中对象最终水平位置的基准位置。

    【示例】考虑一个文本框，应该位于从左到右的文档中其列的右侧一英寸处。可以使用以下WordprocessingML指定此文本框：

    <w:pPr>
        <w:framePr … w:x="1440" w:hAnchor="margin" />
    </w:pPr>

    这些框架水平锚定属性指定它们相对于锚定段落的页边距（不包括任何缩进）。示例结束

    该简单类型的内容是对W3C XML Schema字符串数据类型的限制。

    该简单类型受限于以下表中列出的值：

    margin（相对于页边距）

        指定父对象应水平锚定到文本页边距。

        这将用于指定任何水平定位值应相对于文本页边距的位置进行计算。

    page（相对于页面）

        指定父对象应水平锚定到页面边缘。

        这将用于指定任何水平定位值应相对于页面边缘的位置进行计算。

    text（相对于文本范围）

        指定父对象应水平锚定到文本范围。

        这将用于指定任何水平定位值应相对于锚定段落中文本的边缘（包括文本页边距内的段落上的文本缩进）进行计算。
    """

    Text = 'text'
    """（相对于文本范围）

        指定父对象应水平锚定到文本范围。

        这将用于指定任何水平定位值应相对于锚定段落中文本的边缘（包括文本页边距内的段落上的文本缩进）进行计算。
    """

    Margin = 'margin'
    """（相对于页边距）

        指定父对象应水平锚定到文本页边距。

        这将用于指定任何水平定位值应相对于文本页边距的位置进行计算。
    """

    Page = 'page'
    """（相对于页面）

        指定父对象应水平锚定到页面边缘。

        这将用于指定任何水平定位值应相对于页面边缘的位置进行计算。
    """


class ST_DropCap(ST_BaseEnumType):
    """17.18.20 ST_DropCap (文本框架首字下沉位置)¶

    ST_DropCap (Text Frame Drop Cap Location)

    该简单类型指定了在显示时用于定位首字下沉文本框的位置，即当文本框的内容在锚定段落中显示时的位置。

    【注】虽然首字下沉只是一个文本框，但该简单类型的值用于确定首字应相对于后续的非框段落如何定位（见枚举值），而不是依赖绝对尺寸。结束注】

    【示例】考虑以下包含应定位为首字下沉的文本框的段落：

    <w:p>
        <w:pPr>
            <w:framePr w:dropCap="margin" w:lines="3" w:hSpace="432" w:wrap="around"
                w:vAnchor="text" w:hAnchor="page" />
        </w:pPr>
        <w:r>
            <w:t>A</w:t>
        </w:r>
    </w:p>

    dropCap属性指定为margin，因此该首字下沉被放置在当前文本开始之前的文本边距之外。结束示例】

    该简单类型的内容是对W3C XML Schema字符串数据类型的限制。

    该简单类型限制为下表中列出的值：

    drop（边距内首字下沉）

        指定当在文档中显示该文本框时，首字下沉文本框应定位在锚定段落的文本边距内。

    margin（边距外首字下沉）

        指定当在文档中显示该文本框时，首字下沉文本框应定位在锚定段落的文本边距外。

    none（非首字下沉）

        指定该文本框不是首字下沉文本框。
    """

    none = 'none'
    """（非首字下沉）

        指定该文本框不是首字下沉文本框。
    """

    Drop = 'drop'
    """（边距内首字下沉）

        指定当在文档中显示该文本框时，首字下沉文本框应定位在锚定段落的文本边距内。
    """

    Margin = 'margin'
    """（边距外首字下沉）

        指定当在文档中显示该文本框时，首字下沉文本框应定位在锚定段落的文本边距外。
    """


class CT_FramePr(OxmlBaseElement):
    """17.3.1.11 framePr (文本框属性)

    该元素指定关于当前段落与文本框架相关的信息。文本框架是文档中定位在文档的独立区域或框架中的文字段落，并且可以相对于文档中非框架段落的特定大小和位置进行定位。

    framePr元素指定的第一条信息是当前段落实际上是文框架中的一部分。这一信息仅通过段落属性中的framePr元素的存在来指定。如果省略了framePr元素，则该段落将不会成为文框架中的任何一部分。

    第二条信息涉及文档中当前文本框架的段落集合。这是根据framePr元素上的属性确定的。如果在两个相邻段落上指定的属性值集合相同，则这两个段落将被视为是同一文本框架的一部分，并在文档中的同一框架内呈现。

    [示例：考虑一个文档，其中以下两个段落相邻地位于一起：

    <w:p>
        <w:pPr>
            <w:framePr w:w="2191" w:h="811" w:hRule="exact" w:hSpace="180" w:wrap="around" w:vAnchor="text" w:hAnchor="page" w:x="1921"/>
        </w:pPr>
        <w:r>
            <w:t>第一段</w:t>
        </w:r>
    </w:p>
    <w:p>
        <w:pPr>
            <w:framePr w:w="2191" w:h="810" w:hRule="exact" w:hSpace="180" w:wrap="around" w:vAnchor="text" w:hAnchor="page" w:x="1921"/>
        </w:pPr>
        <w:r>
            <w:t>第二段。</w:t>
        </w:r>
    </w:p>

    这两个段落，尽管每个都是由于framePr元素的存在而成为文本框架的一部分，但由于不同的h值（810与811），它们是不同的文本框架。结束示例]

    框架相对于其属性值存储的定位应根据文档中的下一个段落计算，该段落本身不是文本框的一部分。
    """

    @property
    def dropCap(self) -> Optional[ST_DropCap]:
        """dropCap（首字下沉帧）

        指定当前帧包含一个首字下沉，该首字下沉将位于文档中下一个非帧段落的开头。其内容将用于指定该首字下沉相对于该段落应如何定位。

        如果省略了此属性，则此帧将不被视为首字下沉帧。

        [注：尽管首字下沉只是一个文本帧，但此元素用于确定首字下沉应如何相对于后续非帧段落定位（请参阅可能的值），而不是依赖于绝对大小。结束注释]

        [示例：考虑以下包含应定位为首字下沉的文本帧的段落：

        <w:p>
            <w:pPr>
                <w:framePr w:dropCap="margin" w:lines="3" w:hSpace="432" w:wrap="around" w:vAnchor="text" w:hAnchor="page" />
            </w:pPr>
            <w:r>
                <w:t>A</w:t>
            </w:r>
        </w:p>

        dropCap属性指定了一个margin值，因此此首字下沉位于当前文本开始之前的文本边距之外。结束示例]
        """
        _val = self.attrib.get(qn('w:dropCap'))

        if _val is not None:
            return ST_DropCap(_val)
        return None

    @property
    def lines(self) -> Optional[ST_DecimalNumber]:
        """lines（行中的首字下沉高度）

        指定非框架段落中的行数，用于计算首字下沉的高度，该文本框架与之锚定。

        如果当前框架不是首字下沉（父framePr元素没有dropCap属性），则忽略此值。如果当前文本框架是首字下沉并且存在此属性，则将忽略任何其他垂直定位信息。如果省略此属性，则其值应被视为1。

        【示例：考虑以下包含应定位为首字下沉的文本框架的段落：

        <w:p>
            <w:pPr>
                <w:framePr w:dropCap="margin" w:lines="3" w:hSpace="432" w:wrap="around" w:vAnchor="text" w:hAnchor="page" w:y="400" w:yAlign="text" />
            </w:pPr>
            <w:r>
                <w:t>O</w:t>
            </w:r>
        </w:p>

        由于此框架被用作首字下沉，将忽略y和yAlign属性，首字下沉的高度为锚定段落的前三行。结束示例】
        """
        _val = self.attrib.get(qn('w:lines'))

        if _val is not None:
            return ST_DecimalNumber(_val)
        return None

    @property
    def w(self) -> Optional[s_ST_TwipsMeasure]:
        """w（框架宽度）

        指定此文本框宽度的确切值。

        此值以点的二十分之一指定。

        当存在此属性时，文本框将呈现为指定的确切宽度。如果省略此属性，则文本框宽度将由文本框内内容的最大行宽自动确定。

        [示例：考虑以下指定文本框的WordprocessingML片段：

        <w:p>
            <w:pPr>
                <w:framePr w:w="2419" w:h="2189" w:hRule="atLeast" w:hSpace="187" w:wrap="around" w:vAnchor="text" w:hAnchor="page" w:x="1643" w:y="73" />
            </w:pPr>
            <w:r>
                <w:t>文本框内容。</w:t>
            </w:r>
        </w:p>

        此文本框指定其宽度必须为2419点。如果删除此属性，则文本框将以内容“文本框内容。”的宽度呈现。示例结束]
        """
        _val = self.attrib.get(qn('w:w'))

        if _val is not None:
            return s_to_ST_TwipsMeasure(_val)  # type: ignore
        return None

    @property
    def h(self) -> Optional[s_ST_TwipsMeasure]:
        """h（框架高度）

        指定框架的高度。

        此高度以点的二十分之一表示。

        如果省略此属性，则其值应假定为0。

        根据此文本框的hRule属性的值，定义h属性的值的含义如下：

        如果hRule的值为auto，则框架的高度应根据其内容的高度自动确定。此值将被忽略。
        如果hRule的值为atLeast，则框架的高度应至少为此属性的值。
        如果hRule的值为exact，则框架的高度应正好为此属性的值。
        [示例：考虑以下包含文本框的段落：

        <w:p>
            <w:pPr>
                <w:framePr w:w="2419" w:h="2189" w:hRule="atLeast" w:hSpace="187" w:wrap="around" w:vAnchor="text" w:hAnchor="page" w:x="1643" w:y="73" />
            </w:pPr>
            <w:r>
                <w:t>文本框内容。</w:t>
            </w:r>
        </w:p>

        h属性指定了2189点的二十分之一的值，因此此文本框的高度至少为2189点的二十分之一，不考虑其内容，因为其hRule值设置为atLeast。结束示例]
        """

        _val = self.attrib.get(qn('w:h'))

        if _val is not None:
            return s_to_ST_TwipsMeasure(_val)  # type: ignore
        return None

    @property
    def vSpace(self) -> Optional[s_ST_TwipsMeasure]:
        """vSpace（垂直框架填充）

        指定当前文本框与位于其上方或下方的任何非框架文本之间必须保持的最小距离。

        此距离以点的二十分之一表示。

        如果省略此属性，则假定其值为0。

        [示例：考虑一个文本框，其顶部和底部应至少与任何非框架文本保持半英寸间距。可以使用以下WordprocessingML指定此约束：

        <w:pPr>
            <w:framePr … w:vSpace="720" />
        </w:pPr>

        vspace属性指定文本与此框架之间的间距必须至少为720点的二十分之一。示例结束]
        """
        _val = self.attrib.get(qn('w:vSpace'))

        if _val is not None:
            return s_to_ST_TwipsMeasure(_val)  # type: ignore
        return None

    @property
    def hSpace(self) -> Optional[s_ST_TwipsMeasure]:
        """hSpace（水平框架填充）

        指定当前文本框与任何非框架文本之间应保持的最小距离，当此文本框上的环绕属性设置为around时，允许文本绕过此对象流动。

        此距离以点的二十分之一表示。

        如果环绕值未设置为around，则将忽略此值。如果省略此属性，则假定其值为0。

        [示例：考虑一个文本框，其左右两侧应与任何非框架文本保持至少半英寸的间距。可以使用以下WordprocessingML指定此约束：


        <w:pPr>
            <w:framePr … w:hSpace="720" w:wrap="around" />
        </w:pPr>
        around的环绕值允许文本绕过此文本框，hSpace属性指定文本与此框架之间的间距必须至少为720点的二十分之一。示例结束]
        """

        _val = self.attrib.get(qn('w:hSpace'))

        if _val is not None:
            return s_to_ST_TwipsMeasure(_val)  # type: ignore
        return None

    @property
    def wrap(self) -> Optional[ST_Wrap]:
        """wrap（围绕框架的文本环绕）

        指定应允许围绕此文本框内容的文本环绕样式。此属性确定非框架文本是否允许围绕此框架内容流动。

        如果省略此属性，则假定其值为around。

        [示例：考虑以下指定文本框的WordprocessingML片段：

        <w:p>
            <w:pPr>
                <w:framePr w:w="2419" w:h="2189" w:hRule="atLeast" w:hSpace="187" w:wrap="around" w:vAnchor="text" w:hAnchor="page" w:x="1643" w:y="73" />
            </w:pPr>
            <w:r>
                <w:t>文本框内容。</w:t>
            </w:r>
        </w:p>

        此文本框指定，当在页面上呈现框架时，通常会流向同一行的任何非文本框段落必须被允许这样做。结束示例]
        """
        _val = self.attrib.get(qn('w:wrap'))

        if _val is not None:
            return ST_Wrap(_val)  # type: ignore
        return None

    @property
    def hAnchor(self) -> Optional[ST_HAnchor]:
        """hAnchor（框架水平定位基准）

        指定应计算 x 属性中的水平定位的基本对象。

        文本框架可以相对于水平定位：

        在任何文本运行之前的页面垂直边缘（从左到右段落的左边缘，从右到左段落的右边缘）
        在任何文本运行之前的文本边距垂直边缘（从左到右段落的左边缘，从右到左段落的右边缘）
        锚定段落所在的列的文本边距的垂直边缘
        如果省略此属性，则假定其值为页面。

        [示例：考虑一个文本框架，应在从左到右的文档中的列的右侧一英寸处定位。可以使用以下 WordprocessingML 指定此文本框架：

        <w:pPr>
            <w:framePr … w:x="1440" w:hAnchor="column" />
        </w:pPr>

        这些框架属性指定它们相对于锚定段落的列，并相对于该列，框架应在文本流的方向（在本例中为右侧）上为 1440 个点的二十分之一。结束示例]
        """
        _val = self.attrib.get(qn('w:hAnchor'))

        if _val is not None:
            return ST_HAnchor(_val)  # type: ignore
        return None

    @property
    def vAnchor(self) -> Optional[ST_HAnchor]:
        """vAnchor（框架垂直定位基础）

        指定应从中计算y属性中的水平定位的基本对象。

        文本框架可以相对于水平页面边缘（在任何文本运行之前）水平定位：

        文本边距的水平边缘（在任何文本运行之前）水平定位
        页面的水平边缘（在任何文本运行之前）水平定位
        如果省略此属性，则假定其值为页面。

        [示例：考虑一个文本框架，应在从上到下的文档中页面顶部以下两英寸处定位。可以使用以下WordprocessingML指定此文本框架：

        <w:pPr>
            <w:framePr … w:y="2880" w:vAnchor="page" />
        </w:pPr>

        这些框架属性指定它们相对于锚定页面，并且相对于该列，框架应该在文本流的方向（在本例中向下）中为2880个点的二十分之一。结束示例]
        """
        _val = self.attrib.get(qn('w:vAnchor'))

        if _val is not None:
            return ST_HAnchor(_val)  # type: ignore
        return None

    @property
    def x(self) -> Optional[ST_SignedTwipsMeasure]:
        """x（绝对水平位置）

        指定文本框的绝对水平位置。此绝对位置相对于此文本框的hAnchor属性指定的水平锚点而言。

        此值以点的二十分之一表示。如果为正，则文本框在文档中水平文本流的方向上位于锚定对象之后。如果为负，则文本框在文档中水平文本流的方向上位于锚定对象之前。

        如果还指定了xAlign属性，则将忽略此值。如果省略此属性，则假定其值为0。

        [示例：考虑以下指定文本框的WordprocessingML片段：


        <w:p>
            <w:pPr>
                <w:framePr w:w="2419" w:h="2189" w:hRule="atLeast"
                    w:hSpace="187" w:wrap="around" w:vAnchor="text"
                    w:hAnchor="page" w:x="1643" w:y="73" />
            </w:pPr>
            <w:r>
                <w:t>文本框内容。</w:t>
            </w:r>
        </w:p>

        此文本框指定，它应该位于页面的垂直边缘（从hAnchor属性）之后的1643点的二十分之一处。结束示例]
        """
        _val = self.attrib.get(qn('w:x'))

        if _val is not None:
            return to_ST_SignedTwipsMeasure(int(_val))  # type: ignore
        return None

    @property
    def xAlign(self) -> Optional[s_ST_XAlign]:
        """xAlign（相对水平位置）

        指定文本框的相对水平位置。此相对位置是相对于此文本框的hAnchor属性指定的水平锚点而言。

        如果省略此属性，则未指定此属性，x属性的值将确定文本框的绝对水平位置。如果指定了此属性，则此属性的位置将取代x属性中指定的任何值，并且该值将被忽略。

        【示例：考虑以下指定文本框的WordprocessingML片段：

        <w:p>
            <w:pPr>
                <w:framePr w:w="2419" w:h="2189" w:hRule="atLeast"
                    w:hSpace="187" w:wrap="around" w:vAnchor="text"
                    w:hAnchor="page" w:x="1643" w:xAlign="left" w:y="73" />
            </w:pPr>
            <w:r>
                <w:t>文本框内容。</w:t>
            </w:r>
        </w:p>

        此文本框指定其水平放置位置相对于页面正好为1643个点的二十分之一，但通过xAlign属性的存在，该确切位置被覆盖，使框架放置在页面的左侧。结束示例】
        """
        _val = self.attrib.get(qn('w:xAlign'))

        if _val is not None:
            return s_ST_XAlign(_val)  # type: ignore
        return None

    @property
    def y(self) -> Optional[ST_SignedTwipsMeasure]:
        """y（绝对垂直位置）

        指定文本框的绝对垂直位置。此绝对位置是相对于此文本框的vAnchor属性指定的垂直锚点而言的。

        此数值以点的二十分之一为单位表示。如果为正值，则文本框在文档中垂直文本流的方向上位于锚定对象之后。如果为负值，则文本框在文档中垂直文本流的方向上位于锚定对象之前。

        如果还指定了yAlign属性，则将忽略此数值。如果省略此属性，则其值应被视为0。

        【示例：考虑以下指定文本框的WordprocessingML片段：


        <w:p>
            <w:pPr>
                <w:framePr w:w="2419" w:h="2189" w:hRule="atLeast"
                    w:hSpace="187" w:wrap="around" w:vAnchor="text"
                    w:hAnchor="page" w:x="1643" w:y="73" />
            </w:pPr>
            <w:r>
                <w:t>文本框内容。</w:t>
            </w:r>
        </w:p>

        此文本框指定应位于锚定段落文本的顶部垂直边缘以下79点的二十分之一处（根据vAnchor属性），假设垂直文本方向为自上而下。结束示例】
        """
        _val = self.attrib.get(qn('w:y'))

        if _val is not None:
            return to_ST_SignedTwipsMeasure(int(_val))  # type: ignore
        return None

    @property
    def yAlign(self) -> Optional[s_ST_YAlign]:
        """yAlign（相对垂直位置）

        指定文本框的相对垂直位置。此相对位置是相对于为此文本框指定的垂直锚点（vAnchor属性）而言的。

        如果省略此属性，则未指定此属性，y属性的值将确定文本框的绝对水平位置。如果指定了此属性，则此属性的位置将取代y属性中指定的任何值，并且该值将被忽略，除非vAnchor设置为文本，此时不允许任何相对定位，并且将被忽略。

        【示例：考虑以下指定文本框的WordprocessingML片段：

        <w:p>
            <w:pPr>
                <w:framePr w:w="2419" w:h="2189" w:hRule="atLeast"
                    w:hSpace="187" w:wrap="around" w:vAnchor="margin"
                    w:hAnchor="page" w:x="1643" w:y="73" w:yAlign="center" />
            </w:pPr>
            <w:r>
                <w:t>文本框内容。</w:t>
            </w:r>
        </w:p>

        此文本框指定其垂直放置位置相对于顶部边距为73个点的二十分之一，但由于yAlign属性的存在，确切位置被覆盖，以使框架位于边距的中心。结束示例】
        """
        _val = self.attrib.get(qn('w:yAlign'))

        if _val is not None:
            return s_ST_YAlign(_val)  # type: ignore
        return None

    @property
    def hRule(self) -> Optional[ST_HeightRule]:
        """hRule（框架高度类型）

        指定为此框架指定的高度的含义。

        根据此文本框架的hRule属性的值，定义h属性值的含义如下：

        如果hRule的值为auto，则框架的高度应根据其内容的高度自动确定。忽略h值。
        如果hRule的值为atLeast，则框架的高度应至少为h属性的值。
        如果hRule的值为exact，则框架的高度应正好为h属性的值。
        如果省略此属性，则假定其值为auto。

        [示例：考虑包含文本框架的以下段落：

        <?xml version="1.0"?>
        <w:p>
            <w:pPr>
                <w:framePr w:w="2419" w:h="2189" w:hRule="atLeast" w:hSpace="187" w:wrap="around"           w:vAnchor="text" w:hAnchor="page" w:x="1643" w:y="73" />
            </w:pPr>
            <w:r>
                <w:t>文本框架内容。</w:t>
            </w:r>
        </w:p>

        h属性指定为2189个点的二十分之一，因此此文本框架的高度至少为2189个点的二十分之一，无论其内容如何，因为其hRule值设置为atLeast。结束示例] 此属性的可能值由ST_HeightRule简单类型（§17.18.37）定义。
        """
        _val = self.attrib.get(qn('w:hRule'))

        if _val is not None:
            return ST_HeightRule(_val)  # type: ignore
        return None

    @property
    def anchorLock(self) -> Optional[s_ST_OnOff]:
        """anchorLock（将框锚定到段落）

        指定框始终保持相对于本文档中其前后的非框段落的相同逻辑位置。

        这意味着修改此文档的使用者应确保此文本框始终直接位于其当前所在的非框段落正上方，通过根据需要调整框的定位属性，随着段落在文档中移动而不是移动框在文档中的逻辑位置，如果这样更合适的话。

        如果省略此属性，则此框将不具有锁定的锚定位置。

        [示例：考虑包含在文本框中的以下WordprocessingML段落：


        <w:p>
            <w:pPr>
                <w:framePr w:w="2419" w:h="2189" w:hRule="exact" w:hSpace="187" w:wrap="around" w:vAnchor="text" w:hAnchor="page" w:x="1643" w:y="73" w:anchorLock="1" />
            </w:pPr>
            <w:r>
                <w:t>文本框内容。</w:t>
            </w:r>
        </w:p>
        此文本框使用anchorLock属性具有锁定的锚定。如果将文本框向下移动，必须调整文本框属性以相对于父段落的相同逻辑位置 - 段落不能在文档中重新定位，这导致框的属性发生变化，如下所示：

        <w:p>
            <w:pPr>
                <w:framePr w:w="2419" w:h="2189" w:hRule="exact" w:hSpace="187" w:wrap="around" w:vAnchor="text" w:hAnchor="page" w:x="1643" w:y="-5247" w:anchorLock="1" />
            </w:pPr>
            <w:r>
                <w:t>文本框内容。</w:t>
            </w:r>
        </w:p>

        非框段落在文档中下移了5320个点的二十分之一，框的垂直定位属性被调整以确保其在段落排序中的逻辑位置保持恒定，而其视觉位置发生了变化。结束示例]
        """
        _val = self.attrib.get(qn('w:anchorLock'))

        if _val is not None:
            return s_ST_OnOff(_val)  # type: ignore
        return None


class ST_TabJc(ST_BaseEnumType):
    """17.18.84 ST_TabJc (自定义制表位类型)

    ST_TabJc (Custom Tab Stop Type)

    这个简单类型指定了自定义制表位的可用类型，它确定了制表位的行为以及应用于当前自定义制表位输入文本的对齐方式。

    [例子：考虑在WordprocessingML文档中以1.5英寸的自定义制表位。该制表位将包含在定义制表位的制表元素内，如下所示：

    <w:tab w:val="start" w:pos="2160" />

    val属性指定了此自定义制表位必须将其位置输入的所有文本向左对齐。结束例子]

    这个简单类型的内容是对W3C XML Schema字符串数据类型的限制。

    这个简单类型被限制为以下表中列出的值：

    bar (Bar Tab)

        指定当前制表位是一个垂直线标签。垂直线标签是一个不会在父段落中生成自定义制表位的标签（在定位自定义制表字符时，将跳过此制表位的位置），而是将在父段落中的此位置画一条垂直线（或垂线）。

    center (Centered Tab)

        指定当前制表位将在文档中产生一个位置，其后的所有文本都居中（即在此制表位之后和下一个制表位之前的所有文本都将围绕制表位位置居中）。

    clear (No Tab Stop)

        指定当前制表位被清除，并且在处理此文档内容时将被移除和忽略。

    decimal (Decimal Tab)

        指定当前制表位将在文档中产生一个位置，其后的所有文本都围绕着以下文本运行的第一个小数字符对齐。

        第一个小数字符之前的所有文本运行都在制表位之前，之后的所有文本运行都在制表位位置之后。

    end (Trailing Tab)

        指定当前制表位将在文档中产生一个位置，其后的所有文本都对齐到其尾部（即在此制表位之后和下一个制表位之前的所有文本都相对于制表位位置的尾部对齐）。

        [例子：在RTL段落中，尾部对齐是左侧对齐，所以文本将对齐到该边缘，向右延伸。结束例子]

    num (List Tab)

        指定当前制表位是一个列表制表位，即编号段落中编号和段落内容之间的制表位。

        [注：此对齐样式用于向后兼容早期的文字处理器，应避免使用，而应采用悬挂段落缩进。结束注]

    start (Leading Tab)

        指定当前制表位将在文档中产生一个位置，其后的所有文本都对齐到其前缘（即在此制表位之后和下一个制表位之前的所有文本都相对于制表位位置的前缘对齐）。
    """

    Clear = 'clear'
    """(No Tab Stop)

        指定当前制表位被清除，并且在处理此文档内容时将被移除和忽略。
    """

    Start = 'start'
    """ (Leading Tab)

        指定当前制表位将在文档中产生一个位置，其后的所有文本都对齐到其前缘（即在此制表位之后和下一个制表位之前的所有文本都相对于制表位位置的前缘对齐）。
    """

    Center = 'center'
    """ (Centered Tab)

        指定当前制表位将在文档中产生一个位置，其后的所有文本都居中（即在此制表位之后和下一个制表位之前的所有文本都将围绕制表位位置居中）。
    """

    End = 'end'
    """(Trailing Tab)

        指定当前制表位将在文档中产生一个位置，其后的所有文本都对齐到其尾部（即在此制表位之后和下一个制表位之前的所有文本都相对于制表位位置的尾部对齐）。

        [例子：在RTL段落中，尾部对齐是左侧对齐，所以文本将对齐到该边缘，向右延伸。结束例子]
    """

    Decimal = 'decimal'
    """ (Decimal Tab)

        指定当前制表位将在文档中产生一个位置，其后的所有文本都围绕着以下文本运行的第一个小数字符对齐。

        第一个小数字符之前的所有文本运行都在制表位之前，之后的所有文本运行都在制表位位置之后。
    """

    Bar = 'bar'
    """ (Bar Tab)

        指定当前制表位是一个垂直线标签。垂直线标签是一个不会在父段落中生成自定义制表位的标签（在定位自定义制表字符时，将跳过此制表位的位置），而是将在父段落中的此位置画一条垂直线（或垂线）。
    """

    Num = 'num'
    """ (List Tab)

        指定当前制表位是一个列表制表位，即编号段落中编号和段落内容之间的制表位。

        [注：此对齐样式用于向后兼容早期的文字处理器，应避免使用，而应采用悬挂段落缩进。结束注]
    """

    Left = 'left'
    """[文档中没有资料]
    """

    Right = 'right'
    """[文档中没有资料]
    """


class ST_TabTlc(ST_BaseEnumType):
    """17.18.85 ST_TabTlc (自定义制表位前导符)

    ST_TabTlc (Custom Tab Stop Leader Character)

    这种简单类型指定了可以用来填充由制表符创建的空格的字符。所选字符将根据需要重复，以完全填充制表符字符生成的制表符间距。

    【示例：考虑一个应该由一系列下划线字符前置的制表位，如下所示：

        ______________制表位处的文本

    此制表位将具有下划线的前导属性值，表示制表位必须由下划线字符前置，以填充制表符间距。示例结束】

    这种简单类型的内容是对W3C XML Schema字符串数据类型的限制。

    这种简单类型被限制为以下表中列出的值：

    dot（点状前导线）

        指定此自定义制表位的前导字符将是一个点。

        【示例：

        ...................制表位处的文本。
        示例结束】

    heavy（粗实线前导线）

        指定此自定义制表位的前导字符将是一条粗实线，或一个下划线。

        【注意：此设置用于向后兼容较早的文字处理器，应避免使用，而应选择其他前导字符。如果需要，可以使用下划线显示。注意结束】

        【示例：

        _________制表位处的文本。

        示例结束】

    hyphen（虚线制表位前导线）

        指定此自定义制表位的前导字符将是一个连字符。

        【示例：

        --------------- 制表位处的文本。

        示例结束】

    middleDot（中点前导线）

        指定此自定义制表位的前导字符将是一个居中点。

        【示例：

        ···················制表位处的文本。

        示例结束】

    none（无制表位前导）

        指定此自定义制表位不应有前导字符。

        【示例：

                制表位处的文本。

        示例结束】

    underscore（实线前导线）

        指定此自定义制表位的前导字符将是一个下划线。

        【示例：

        _________制表位处的文本。

        示例结束】
    """

    none = 'none'
    """（无制表位前导）

        指定此自定义制表位不应有前导字符。

        【示例：

                制表位处的文本。

        示例结束】
    """

    dot = 'dot'
    """（点状前导线）

        指定此自定义制表位的前导字符将是一个点。

        【示例：

        ...................制表位处的文本。
        示例结束】
    """

    hyphen = 'hyphen'
    """（虚线制表位前导线）

        指定此自定义制表位的前导字符将是一个连字符。

        【示例：

        --------------- 制表位处的文本。

        示例结束】
    """

    underscore = 'underscore'
    """（实线前导线）

        指定此自定义制表位的前导字符将是一个下划线。

        【示例：

        _________制表位处的文本。

        示例结束】
    """

    heavy = 'heavy'
    """（粗实线前导线）

        指定此自定义制表位的前导字符将是一条粗实线，或一个下划线。

        【注意：此设置用于向后兼容较早的文字处理器，应避免使用，而应选择其他前导字符。如果需要，可以使用下划线显示。注意结束】

        【示例：

        _________制表位处的文本。

        示例结束】
    """

    middleDot = 'middleDot'
    """（中点前导线）

        指定此自定义制表位的前导字符将是一个居中点。

        【示例：

        ···················制表位处的文本。

        示例结束】
    """


class CT_TabStop(OxmlBaseElement):
    """17.3.1.37 tab (自定义制表位)

    该元素指定在文档中一组段落属性中定义的单个自定义制表位。制表位位置始终相对于其所在段落的前导边缘进行测量（即，从左到右段落的左边缘，从右到左段落的右边缘）。

    【示例：考虑一个位于WordprocessingML文档中1.5英寸处的自定义制表位。该制表位将包含在定义制表位的tab元素中，如下所示：

    <w:tab w:val="start" w:pos="2160" />

    tab元素为当前段落属性集指定了自定义制表位的所有属性。结束示例】


    """

    @property
    def val(self) -> ST_TabJc:
        """val（制表位类型）

        指定自定义制表位的样式，确定制表位的行为以及应用于在当前自定义制表位输入的文本的对齐方式。

        clear的值是独特的，它指定当文档下次被支持渲染文档内容的消费者编辑时，此制表位将被移除。

        [示例：考虑一个在WordprocessingML文档中位于1.5英寸处的自定义制表位。该制表位将包含在一个指定制表位的tab元素中，如下所示：

        <w:tab w:val="start" w:pos="2160" />

        val属性指定此自定义制表位必须将其位置处输入的所有文本向左对齐。结束示例]
        """
        _val = self.attrib[qn('w:val')]

        return ST_TabJc(_val)  # type: ignore

    @property
    def leader(self) -> Optional[ST_TabTlc]:
        """leader（制表符前导字符）

        指定用于填充以此自定义制表位结束的制表符所创建的空间的字符。此字符将根据需要重复，直到完全填满制表符字符生成的制表位间距。

        如果省略了此属性，则不会使用任何制表符前导字符。

        [示例：考虑一个应该由一系列下划线字符前置的制表位，如下所示：

        ______________制表位处的文本

        这个制表位将具有下划线作为leader属性的值，表示制表位必须在需要时由下划线字符前置以填充制表符间距。结束示例]
        """
        _val = self.attrib.get(qn('w:leader'))

        if _val is not None:
            return ST_TabTlc(_val)  # type: ignore
        return None

    @property
    def pos(self) -> ST_SignedTwipsMeasure:
        """pos（制表位位置）

        指定当前自定义制表位相对于当前页面边距的位置。

        允许负值，并将制表位移动到当前页面边距内指定的量。

        [示例：考虑一个在WordprocessingML文档中位于1.5英寸处的自定义制表位。该制表位将包含在一个指定制表位的tab元素中，如下所示：

        <w:tab w:val="start" w:pos="2160" />

        pos属性指定了这个自定义制表位必须位于起始文本边距内2160个点（1.5英寸）。结束示例]
        """
        _val = self.attrib[qn('w:pos')]

        return to_ST_SignedTwipsMeasure(str(_val))


class ST_LineSpacingRule(ST_BaseEnumType):
    """17.18.48 ST_LineSpacingRule (行距规则)

    ST_LineSpacingRule (Line Spacing Rule)

    这个简单类型指定了在文档中显示时，父对象的行间距计算逻辑。

    【示例：考虑以下 WordprocessingML 段落：

    <w:pPr>
        <w:spacing w:line="276" w:lineRule="auto" />
    </w:pPr>

    这个段落指定每行的间距应该使用正常单倍行距计算的1.15倍（276除以240）。示例结束】

    这个简单类型的内容是对 W3C XML Schema 字符串数据类型的限制。

    这个简单类型被限制为以下表格中列出的值：

    atLeast（最小行高）

        指定行的高度至少为指定的值，但可能根据需要扩展以适应其内容。

    auto（自动确定行高）

        指定父对象的行间距将根据其内容的大小自动确定，没有预先确定的最小或最大大小。

    exact（精确行高）

        指定行的高度应该完全符合指定的值，而不考虑内容的大小。

        如果内容过大以至于超出指定的高度，那么它们将被截断。
    """

    auto = 'auto'
    """（自动确定行高）

        指定父对象的行间距将根据其内容的大小自动确定，没有预先确定的最小或最大大小。
    """

    exact = 'exact'
    """（精确行高）

        指定行的高度应该完全符合指定的值，而不考虑内容的大小。

        如果内容过大以至于超出指定的高度，那么它们将被截断。
    """

    atLeast = 'atLeast'
    """（最小行高）

        指定行的高度至少为指定的值，但可能根据需要扩展以适应其内容。
    """


class CT_Spacing(OxmlBaseElement):
    """17.3.1.33 spacing (行与段落上方/下方的间距)

    该元素指定在消费者显示段落内容时应用于该段落内容的行间距和段间距。

    如果对于给定段落省略了此元素，则其属性表示的每个设置的值由在样式层次结构中先前设置的设置确定（即，该先前设置保持不变）。如果样式层次结构中以前未指定设置，则其值如下面对应属性所描述。

    【示例：考虑以下 WordprocessingML 段落：

    <w:pPr>
        <w:spacing w:after="200" w:line="276" w:lineRule="auto" />
    </w:pPr>
    此段落指定每段后面至少有 200 个二十分之一点，每行间距根据正常单倍行距计算的 1.15 倍（276 除以 240）自动计算。结束示例】

    在确定任意两个段落之间的间距时，消费者应使用每个段落的行间距的最大值、第一个段落后面的间距以及第二个段落前面的间距来确定段落之间的净间距。

    【示例：考虑文档中连续的两个单倍行距段落，第一个指定间距为 12 点，第二个指定间距为 4 点。这些约束使用以下 WordprocessingML 表示：

    <w:p>
        <w:pPr>
            <w:spacing w:after="240" />
        </w:pPr>
        …
        </w:p>
    <w:p>
        <w:pPr>
            <w:spacing w:before="80" />
        </w:pPr>
        …
    </w:p>

    第一个段落和第二个段落之间的间距为 12 点，因为这是两个段落之间请求的最大间距。结束示例】

    <xsd:complexType name="CT_Spacing">
        <xsd:attribute name="before" type="s:ST_TwipsMeasure" use="optional" default="0"/>
        <xsd:attribute name="beforeLines" type="ST_DecimalNumber" use="optional" default="0"/>
        <xsd:attribute name="beforeAutospacing" type="s:ST_OnOff" use="optional" default="off"/>
        <xsd:attribute name="after" type="s:ST_TwipsMeasure" use="optional" default="0"/>
        <xsd:attribute name="afterLines" type="ST_DecimalNumber" use="optional" default="0"/>
        <xsd:attribute name="afterAutospacing" type="s:ST_OnOff" use="optional" default="off"/>
        <xsd:attribute name="line" type="ST_SignedTwipsMeasure" use="optional" default="0"/>
        <xsd:attribute name="lineRule" type="ST_LineSpacingRule" use="optional" default="auto"/>
    </xsd:complexType>
    """

    @property
    def before(self):
        """before (段前间距)

        指定应在文档中此段落的第一行之前添加的间距，以绝对单位指定此属性的值。

        如果在给定段落中省略了此属性，则表示的设置的值为样式层次结构中先前设置的值。如果在样式层次结构中从未指定此设置，则段落的内容上方不应用任何间距。

        如果还指定了beforeLines属性或beforeAutoSpacing属性，则将忽略此属性值。

        【示例：考虑以下 WordprocessingML 段落：

        <w:p>
            <w:pPr>
                <w:spacing w:before="80" />
            </w:pPr>
            …
        </w:p>

        该段落的第一行上方必须至少有 80 个点的间距，尽管实际间距可以由行间距或前一个段落的最后一行下方的间距中的较大者确定。结束示例】

        此属性的可能值由ST_TwipsMeasure简单类型定义(§22.9.2.14)。
        """
        _val = self.attrib.get(qn('w:before'))

        if _val is not None:
            return s_to_ST_TwipsMeasure(str(_val))
        return None

    @property
    def beforeLines(self) -> ST_DecimalNumber:
        """beforeLines（段前间距，以行单位）

        指定应在文档中此段落的第一行之前添加的间距，以行单位指定此属性的值。

        此属性的值以百分之一行为单位指定。

        如果还指定了beforeAutoSpacing属性，则将忽略此属性值。如果在样式层次结构中从未指定此设置，则其值应为零。

        【示例：考虑以下 WordprocessingML 段落：

        <w:p>
            <w:pPr>
                <w:spacing w:beforeLines="100" />
            </w:pPr>
            …
        </w:p>

        该段落的第一行上方必须至少有 1 行的间距，尽管实际间距可以由行间距或前一个段落的最后一行下方的间距中的较大者确定。结束示例】

        此属性的可能值由ST_DecimalNumber简单类型定义(§17.18.10).
        """
        _val = self.attrib.get(qn('w:beforeLines'))

        if _val is not None:
            return ST_DecimalNumber(int(_val))  # type: ignore

        return ST_DecimalNumber(0)

    @property
    def beforeAutospacing(self) -> s_ST_OnOff:
        """beforeAutospacing (自动确定段前间距)

        指定消费者是否应根据段落内容自动确定此段落之前的间距。

        此自动间距应与在 HTML 文档中应用未指定明确前后间距时应用于段落的间距相匹配。

        如果指定了此属性，则忽略before或beforeLines中的任何值，并且间距由消费者自动确定。

        如果在给定段落中省略了此属性，则表示的设置的值为样式层次结构中先前设置的值。如果在样式层次结构中从未指定此设置，则自动间距被关闭。

        【示例：考虑文档中必须根据段落内容自动确定其上方的间距的段落。此约束由以下 WordprocessingML 指定：

        <w:p>
            <w:pPr>
                <w:spacing … w:beforeAutospacing="1" />
            </w:pPr>
            …
        </w:p>

        结果段落的第一行上方的间距必须由消费者自动确定，以匹配指定的 HTML 文档。结束示例】

        此属性的可能值由ST_OnOff简单类型定义(§22.9.2.7)。
        """
        _val = self.attrib.get(qn('w:beforeAutospacing'))

        if _val is not None:
            return s_ST_OnOff(_val)  # type: ignore

        return s_ST_OnOff.Off

    @property
    def after(self):
        """after（段后间距）

        指定在文档中此段落最后一行之后应添加的间距，单位为绝对单位。

        如果在给定段落中省略了此属性，则表示的设置的值为样式层次结构中先前设置的值。如果在样式层次结构中从未指定此设置，则该段落的内容下方不应用任何间距。

        如果还指定了afterLines属性或afterAutoSpacing属性，则将忽略此属性值。

        【示例：考虑以下 WordprocessingML 段落：


        <w:p>
            <w:pPr>
                <w:spacing w:after="240" />
            </w:pPr>
            …
        </w:p>

        该段落必须在其最后几行下方至少有 240 个二十分之一点的间距，尽管实际间距可以由行间距或下一个段落的上方间距中的较大者确定。结束示例】

        此属性的可能值由ST_TwipsMeasure简单类型定义。
        """

        _val = self.attrib.get(qn('w:after'))

        if _val is not None:
            return s_to_ST_TwipsMeasure(_val)  # type: ignore
        return None

    @property
    def afterLines(self) -> ST_DecimalNumber:
        """afterLines（段后间距的行单位）

        指定应在文档中此段落的最后一行之后添加的间距，以行单位指定此属性的值。

        此属性的值以每行百分之一为单位指定。

        如果还指定了afterAutoSpacing属性，则将忽略此属性值。如果在样式层次结构中从未指定此设置，则其值应为零。

        【示例：考虑以下 WordprocessingML 段落：

        <w:p>
            <w:pPr>
                <w:spacing w:afterLines="300" />
            </w:pPr>
            …
        </w:p>

        该段落必须在其最后几行下方至少有 3 行的间距，尽管实际间距可以由行间距或下一个段落的上方间距中的较大者确定。结束示例】

        此属性的可能值由ST_DecimalNumber简单类型定义。
        """
        _val = self.attrib.get(qn('w:afterLines'))

        if _val is not None:
            return ST_DecimalNumber(int(_val))  # type: ignore

        return ST_DecimalNumber(0)

    @property
    def afterAutospacing(self) -> s_ST_OnOff:
        """afterAutospacing（自动确定段后间距）

        指定消费者是否应根据段落内容自动确定此段落之后的间距。

        此自动间距应与在 HTML 文档中应用未指定明确前后间距时应用于段落的间距相匹配。

        如果指定了此属性，则忽略after或afterLines中的任何值，并且间距由消费者自动确定。

        如果在给定段落中省略了此属性，则表示的设置的值为样式层次结构中先前设置的值。如果在样式层次结构中从未指定此设置，则自动间距被关闭。

        【示例：考虑文档中必须根据段落内容自动确定其后的间距的段落。此约束由以下 WordprocessingML 指定：


        <w:pPr>
            <w:spacing … w:afterAutospacing="1" />
        </w:pPr>

        结果段落的间距下方的最后一行必须由消费者自动确定，以匹配指定的 HTML 文档。结束示例】

        此属性的可能值由ST_OnOff简单类型定义
        """
        _val = self.attrib.get(qn('w:afterAutospacing'))

        if _val is not None:
            return s_ST_OnOff(_val)  # type: ignore

        return s_ST_OnOff.Off

    @property
    def line(self) -> Optional[ST_SignedTwipsMeasure]:
        """line（段内行间距）

        此属性指定段落内文本行之间的垂直间距。

        如果在给定段落中省略了此属性，则表示的设置的值为样式层次结构中先前设置的值。如果在样式层次结构中从未指定此设置，则该段落内的行应用单行（无额外）行间距。

        如果lineRule属性的值为atLeast或exact，则此属性的值应解释为点的二十分之一。当lineRule属性的值为atLeast或exact时，文本应按照以下方式定位于该行高度内：

        - 当行高度太小时，文本应位于行底部（即从上到下剪切）
        - 当行高度太大时，文本应居中于可用空间中。

        如果lineRule属性的值为auto，则line属性的值应解释为行的240分之一，以简单类型的值描述的方式。

        【示例：考虑应具有行高的1.15倍的段落的以下 WordprocessingML。此约束应使用以下 WordprocessingML 指定：

        <w:p>
            <w:pPr>
                <w:spacing w:line="276" w:lineRule="auto" />
            </w:pPr>
            …
        </w:p>

        auto值的lineRule属性指定line属性的值应按照单行高的240分之一解释，这意味着净间距是276/240分之一行，或者高出1.15行。结束示例】

        此属性的可能值由ST_SignedTwipsMeasure简单类型定义(§17.18.81).
        """
        _val = self.attrib.get(qn('w:line'))

        if _val is not None:
            return to_ST_SignedTwipsMeasure(str(_val))
        return None

    @property
    def lineRule(self) -> ST_LineSpacingRule:
        """lineRule（行间距规则）

        指定如何计算存储在line属性中的行间距。

        如果省略此属性，则假定它的值是auto，如果存在line属性值。

        如果此属性的值为atLeast或exactly，则line属性的值应按照简单类型的值描述的方式解释为点的二十分之一。

        如果此属性的值为auto，则line属性的值应按照简单类型的值描述的方式解释为行的240分之一。

        【示例：考虑以下应具有行高的1.15倍的段落的 WordprocessingML。此约束应使用以下 WordprocessingML 指定：

        <w:pPr>
            <w:spacing w:line="276" w:lineRule="auto" />
        </w:pPr>

        auto值的lineRule属性指定line属性的值应按照单行高的240分之一解释。结束示例】

        此属性的可能值由ST_LineSpacingRule简单类型定义(§17.18.48).
        """
        _val = self.attrib.get(qn('w:lineRule'))

        if _val is not None:
            return ST_LineSpacingRule(_val)  # type: ignore

        return ST_LineSpacingRule.auto


class CT_Ind(OxmlBaseElement):
    """17.3.1.12 ind (段落缩进)

    该元素指定应用于当前段落的缩进属性集。

    缩进设置可以根据个别情况进行覆盖 - 如果在给定段落中省略了该元素的任何单个属性，则其值由在样式层次结构的任何级别上先前设置的设置确定（即该先前设置保持不变）。如果在样式层次结构中从未指定该元素的任何单个属性，则不会对段落应用该缩进类型的缩进。

    [示例：考虑一个段落，该段落应该从文本边距的左右两侧各缩进一英寸，除了每个段落的第一行，该行应该只从文本边距（开始该段落的一侧）缩进四分之一英寸。使用以下WordprocessingML指定这组缩进：

    <w:pPr>
        <w:ind w:start="1440" w:end="1440" w:hanging="1080" />
    </w:pPr>

    这组缩进属性指定应在该段落的文本边距的左右两侧提供1440个点的缩进，并且应在第一个段落的文本中应用1080个点的悬挂缩进（朝向文本边距），从而使其从文本边距缩进四分之一英寸。结束示例]
    """

    @property
    def start(self) -> Optional[ST_SignedTwipsMeasure]:
        """start（开始缩进）

        指定应放置在本段落开头的缩进量 - 在从左到右的段落中，该段落的左文本边距和该段落内容的左边缘之间，以及在从右到左的段落中，右文本边距和该段落文本的右边缘之间。如果为此段落指定了mirrorIndents属性（§17.3.1.18），则此缩进用于内部页面边缘 - 奇数页的右页面边缘和偶数页的左页面边缘。

        如果省略了此属性，则假定其值为零。

        此元素的所有其他值均相对于前导文本边距，负值定义为使文本移动超出文本边距，正值将文本移动到文本边距内部。此值仅可通过使用firstLine或hanging属性仅对第一行进行覆盖。此外，如果指定了startChars属性，则将忽略此值。

        [示例：考虑以下WordprocessingML片段：


        <w:pPr>
            <w:ind w:start="720" w:end="2880" />
        </w:pPr>

        此段落缩进设置指定此段落的文本应在此文档中距左文本边距720个点（半英寸）缩进，假设这是一个从左到右的段落。结束示例]
        """
        _val = self.attrib.get(qn('w:start'))

        if _val is not None:
            return to_ST_SignedTwipsMeasure(str(_val))
        return None

    @property
    def startChars(self) -> Optional[ST_DecimalNumber]:
        """startChars（以字符单位指定的开始缩进）

        指定应放置在本段落开头的缩进量 - 在从左到右的段落中，该段落的左文本边距和该段落内容的左边缘之间，以及在从右到左的段落中，右文本边距和该段落文本的右边缘之间。如果为此段落指定了mirrorIndents属性（§17.3.1.18），则此缩进用于内部页面边缘 - 奇数页的右页面边缘和偶数页的左页面边缘。

        此值以百分之一字符单位指定。

        如果省略了此属性，则假定其值为零。

        此元素的所有其他值均相对于前导文本边距，负值定义为使文本移动超出文本边距，正值将文本移动到文本边距内部。此值仅可通过使用firstLine或hanging属性仅对第一行进行覆盖。此外，如果指定了start属性，则其值将被忽略，并由此值取代。

        [示例：考虑以下WordprocessingML片段：


        <w:pPr>
            <w:ind w:startChars="250" />
        </w:pPr>

        此段落缩进设置指定此段落的文本应在此文档中距左文本边距两个半字符单位缩进，假设这是一个从左到右的段落。结束示例]
        """
        _val = self.attrib.get(qn('w:startChars'))

        if _val is not None:
            return ST_DecimalNumber(int(_val))
        return None

    @property
    def end(self) -> Optional[ST_SignedTwipsMeasure]:
        """end（结束缩进）

        指定应放置在本段落末尾的缩进量 - 在从左到右的段落中，该缩进位于本段落的右文本边距和该段落内容的右边缘之间，在从右到左的段落中，该缩进位于左文本边距和该段落文本的左边缘之间。如果为本段落指定了mirrorIndents属性（§17.3.1.18），则此缩进用于外部页面边缘 - 奇数页的左页面边缘和偶数页的右页面边缘。

        如果省略了此属性，则假定其值为零。

        此元素的所有其他值均相对于尾部文本边距，负值定义为将文本移动到文本边距之外，正值将文本移动到文本边距内。此外，如果指定了endChars属性，则将忽略此值。

        [示例：考虑以下WordprocessingML片段：

        <w:pPr>
            <w:ind w:start="720" w:end="-1440" />
        </w:pPr>

        此一组段落缩进指定了本段落的文本应在本文档中向右文本边距缩进1440个二十分之一点（一英寸），假设这是一个从左到右的段落。结束示例]
        """
        _val = self.attrib.get(qn('w:end'))

        if _val is not None:
            return to_ST_SignedTwipsMeasure(str(_val))
        return None

    @property
    def endChars(self) -> Optional[ST_DecimalNumber]:
        """endChars（字符单位中的结束缩进）

        指定应放置在本段落末尾的缩进量 - 在从左到右的段落中，位于本段落的右文本边距和该段落内容的右边缘之间，在从右到左的段落中，位于左文本边距和该段落文本的左边缘之间。如果为此段落指定了mirrorIndents属性（§17.3.1.18），则此缩进用于外部页面边缘 - 奇数页的左页面边缘和偶数页的右页面边缘。

        此值以字符单位的百分之一指定。

        如果省略此属性，则假定其值为零。

        此元素的所有其他值均相对于尾部文本边距，负值定义为使文本移动超出文本边距，正值使文本移动到文本边距内。此外，如果指定了end属性，则其值将被忽略，并被此值取代。

        [示例：考虑以下WordprocessingML片段：

        <w:pPr>
            <w:ind w:endChars="250" />
        </w:pPr>

        此段落缩进设置指定此段落的文本应从文档中的右文本边距向右缩进两个半字符单位，假设这是一个从左到右的段落。示例结束]
        """
        _val = self.attrib.get(qn('w:endChars'))

        if _val is not None:
            return ST_DecimalNumber(int(_val))
        return None

    @property
    def left(self) -> Optional[ST_SignedTwipsMeasure]:
        """没有文档资料

        根据ai回答，表示段落左缩进
        """
        _val = self.attrib.get(qn('w:left'))

        if _val is not None:
            return to_ST_SignedTwipsMeasure(str(_val))
        return None

    @property
    def leftChars(self) -> Optional[ST_DecimalNumber]:
        """没有文档资料

        根据ai回答，表示段落左缩进，以字符为单位

        例如，如果你想要设置一个段落的左缩进为4个字符宽度，你可以在样式定义中这样设置：

        <w:pPr>
            <w:pStyle w:val="YourStyleName" />
            <w:ind w:leftChars="40"/>
        </w:pPr>
        """
        _val = self.attrib.get(qn('w:leftChars'))

        if _val is not None:
            return ST_DecimalNumber(int(_val))
        return None

    @property
    def right(self) -> Optional[ST_SignedTwipsMeasure]:
        """没有文档资料"""
        _val = self.attrib.get(qn('w:right'))

        if _val is not None:
            return to_ST_SignedTwipsMeasure(str(_val))
        return None

    @property
    def rightChars(self) -> Optional[ST_DecimalNumber]:
        """没有文档资料"""
        _val = self.attrib.get(qn('w:rightChars'))

        if _val is not None:
            return ST_DecimalNumber(int(_val))
        return None

    @property
    def hanging(self) -> Optional[ST_SignedTwipsMeasure]:
        """hanging（从第一行移除的缩进）

        指定应从父段落的第一行移除的缩进，通过将第一行的缩进向文本流方向的开始移动。

        此缩进是相对于为父段落中的所有其他行指定的段落缩进而言的。 firstLine 和 hanging 属性是互斥的，如果两者都被指定，则忽略 firstLine 的值。如果还指定了 hangingChars 属性，则忽略此值。如果省略此属性，则其值将被假定为零（如果需要）。

        [示例：考虑以下 WordprocessingML 片段：

        <w:pPr>
            <w:ind w:start="1440" w:end="720" w:hanging="720" />
        </w:pPr>

        这组缩进指定第一行应该从为所有其余段落指定的缩进中向文本边距方向缩进 720 点的二十分之一（一英寸），而该缩进是由 start 属性指定的 1440 点的二十分之一。这使第一行从文本边距处缩进半英寸。结束示例]
        """
        _val = self.attrib.get(qn('w:hanging'))

        if _val is not None:
            return to_ST_SignedTwipsMeasure(str(_val))
        return None

    @property
    def hangingChars(self) -> Optional[ST_DecimalNumber]:
        """hangingChars（以字符单位为单位移除首行缩进）

        指定应从父段落的第一行移除的缩进量，通过将第一行的缩进向文本流方向的开头移动。

        此缩进相对于为父段落中的所有其他行指定的段落缩进而指定。

        它以字符单位的百分之一指定。

        firstLineChars和hangingChars属性是互斥的，如果两者都指定，则将忽略firstLine值。如果还指定了hanging属性，则其值将被此值取代。如果省略此属性，则假定其值为零（如果需要）。

        [示例：考虑以下WordprocessingML片段：


        <w:pPr>
            <w:ind w:start="1440" w:end="720" w:hangingChars="100" />
        </w:pPr>

        这组缩进指定第一行应该从所有剩余段落指定的缩进处向文本边距缩进一个字符单位，即由start属性指定的1440点的二十分之一。结束示例]
        """
        _val = self.attrib.get(qn('w:hangingChars'))

        if _val is not None:
            return ST_DecimalNumber(int(_val))
        return None

    @property
    def firstLine(self) -> Optional[ST_SignedTwipsMeasure]:
        """firstLine（额外的首行缩进）

        指定应应用于父段落第一行的额外缩进。此额外缩进相对于为父段落中所有其他行指定的段落缩进而言。

        firstLine和hanging属性是互斥的，如果两者都指定，则将忽略firstLine值。如果还指定了firstLineChars属性，则将忽略此值。如果省略此属性，则假定其值为零（如果需要）。

        [示例：考虑以下WordprocessingML片段：


        <w:pPr>
            <w:ind w:start="1440" w:end="720" w:firstLine="1440" />
        </w:pPr>

        此缩进设置指定第一行应从所有剩余段落指定的缩进处向右缩进1440个点的二十分之一（一英寸），如由start属性指定的1440个点的二十分之一。这使得第一行从文本边距向右缩进两英寸。示例结束]
        """
        _val = self.attrib.get(qn('w:firstLine'))

        if _val is not None:
            return to_ST_SignedTwipsMeasure(str(_val))
        return None

    @property
    def firstLineChars(self) -> Optional[ST_DecimalNumber]:
        """firstLineChars（字符单位中的额外首行缩进）

        指定应用于父段落第一行的额外缩进。此额外缩进是相对于为父段落中的所有其他行指定的段落缩进而言的。

        它以字符单位的百分之一来指定。

        firstLineChars 和 hangingChars 属性是互斥的，如果两者都被指定，则忽略 firstLineChars 的值。如果还指定了 firstLine 属性，则此值将取代其它值。如果省略此属性，则其值将被假定为零（如果需要）。

        [示例：考虑以下 WordprocessingML 片段：

        <w:pPr>
            <w:ind w:start="1440" w:end="720" w:firstLineChars="140" />
        </w:pPr>

        这组缩进指定第一行应该从为所有其余段落指定的缩进中缩进 140 个字符单位，而该缩进是由 start 属性指定的 1440 点的二十分之一。结束示例]
        """
        _val = self.attrib.get(qn('w:firstLineChars'))

        if _val is not None:
            return ST_DecimalNumber(int(_val))
        return None


class ST_Jc(ST_BaseEnumType):
    """17.18.44 ST_Jc (水平对齐类型)¶

    ST_Jc (Horizontal Alignment Type)

    这个简单类型指定了可以应用于 WordprocessingML 文档中对象的所有对齐方式。

    【示例：考虑一个段落，它被对齐到文本流的尾部。这个要求可以在 WordprocessingML 标记中指定如下：

    <w:pPr>
        <w:jc w:val="end" />
    </w:pPr>

    val 属性的值为 end，指定内容必须在页面上右对齐，对于从右向左的段落则左对齐。示例结束】

    这个简单类型的内容是对 W3C XML Schema 字符串数据类型的限制。

    这个简单类型受限于以下表中列出的值：

    both（两端对齐）

        指定文本应该在文档中的两个文本边界之间两端对齐。

        当应用此设置时，对阿拉伯文本也会应用低拉丝达设置。

        这种类型的两端对齐只会影响每行的单词之间的间距，而不会影响在两端对齐其内容时每个单词内的字符间距。

    center（居中对齐）

        指定文本应该在文档中的两个文本边界之间居中对齐。

    distribute（均匀分布）

        指定文本应该在文档中的两个文本边界之间两端对齐。

        这种类型的两端对齐会均匀地影响每行的单词之间的间距以及在两端对齐其内容时每个单词之间的字符间距——即，每行上所有字符都将增加相等数量的字符间距。

    end（对齐到尾部）

        指定文本应该对齐到文档中的尾部文本边界（对于从左到右的段落为右边，对于从右到左的段落为左边）。

    highKashida（最宽的 Kashida 长度）

        指定当前段落中文本的 Kashida 长度应该扩展到其可能的最宽长度。

        此设置仅影响 Kashidas，它们是用于扩展两个阿拉伯字符之间的连接符的特殊字符。【注：它们通常用于通过视觉延长单词而不是增加单词之间的间距来改善两端对齐文本的外观。结束注】

        【示例：以下示例说明了每种 Kashida 的类型：

        123

        示例结束】

    lowKashida（较低的 Kashida 长度）

        指定当前段落中文本的 Kashida 长度应该扩展到略长一点的长度。当应用 both 设置时，此设置也将应用于阿拉伯文本。

        此设置仅影响 Kashidas，它们是用于扩展两个阿拉伯字符之间的连接符的特殊字符。【注：它们通常用于通过视觉延长单词而不是增加单词之间的间距来改善两端对齐文本的外观。结束注】

        【示例：以下示例说明了每种 Kashida 的类型：

        123

        示例结束】

    mediumKashida（中等 Kashida 长度）

        指定当前段落中文本的 Kashida 长度应该扩展到由使用者确定的中等长度。

        此设置仅影响 Kashidas，它们是用于扩展两个阿拉伯字符之间的连接符的特殊字符。【注：它们通常用于通过视觉延长单词而不是增加单词之间的间距来改善两端对齐文本的外观。结束注】

        【示例：以下示例说明了每种 Kashida 的类型：

        123

        示例结束】

    numTab（对齐到列表制表位）

        指定文本应该对齐到列表制表位，即当前段落编号后的制表位。

        如果当前段落没有编号，此设置将不起作用。

        【注：此两端对齐样式用于向后兼容早期的文字处理器，应避免使用，应优先使用悬挂段落缩进。结束注】

    start（对齐到前导边缘）

        指定文本应该对齐到文档中的前导文本边缘（从左到右的段落为左边，从右到左的段落为右边）。

    thaiDistribute（泰语对齐）

        指定文本应该以针对泰语的优化方式进行两端对齐。

        这种类型的两端对齐会影响每行的单词之间的间距以及在两端对齐其内容时每个单词之间的字符间距，不同于 both 对齐。这种差异是通过略微增加字符间距来创建的，以确保对齐所创建的额外空间被减小。

        【注：此设置与对齐不同，因为在西方语言中，减少字符间距是不合适的。结束注】
    """

    start = 'start'
    """（对齐到前导边缘）

        指定文本应该对齐到文档中的前导文本边缘（从左到右的段落为左边，从右到左的段落为右边）。
    """

    center = 'center'
    """（居中对齐）

        指定文本应该在文档中的两个文本边界之间居中对齐。
    """

    end = 'end'
    """（对齐到尾部）

        指定文本应该对齐到文档中的尾部文本边界（对于从左到右的段落为右边，对于从右到左的段落为左边）。
    """

    both = 'both'
    """（两端对齐）

        指定文本应该在文档中的两个文本边界之间两端对齐。

        当应用此设置时，对阿拉伯文本也会应用低拉丝达设置。

        这种类型的两端对齐只会影响每行的单词之间的间距，而不会影响在两端对齐其内容时每个单词内的字符间距。
    """

    mediumKashida = 'mediumKashida'
    """（中等 Kashida 长度）

        指定当前段落中文本的 Kashida 长度应该扩展到由使用者确定的中等长度。

        此设置仅影响 Kashidas，它们是用于扩展两个阿拉伯字符之间的连接符的特殊字符。【注：它们通常用于通过视觉延长单词而不是增加单词之间的间距来改善两端对齐文本的外观。结束注】
    """

    distribute = 'distribute'
    """（均匀分布）

        指定文本应该在文档中的两个文本边界之间两端对齐。

        这种类型的两端对齐会均匀地影响每行的单词之间的间距以及在两端对齐其内容时每个单词之间的字符间距——即，每行上所有字符都将增加相等数量的字符间距。
    """

    numTab = 'numTab'
    """（对齐到列表制表位）

        指定文本应该对齐到列表制表位，即当前段落编号后的制表位。

        如果当前段落没有编号，此设置将不起作用。

        【注：此两端对齐样式用于向后兼容早期的文字处理器，应避免使用，应优先使用悬挂段落缩进。结束注】
    """

    highKashida = 'highKashida'
    """（最宽的 Kashida 长度）

        指定当前段落中文本的 Kashida 长度应该扩展到其可能的最宽长度。

        此设置仅影响 Kashidas，它们是用于扩展两个阿拉伯字符之间的连接符的特殊字符。【注：它们通常用于通过视觉延长单词而不是增加单词之间的间距来改善两端对齐文本的外观。结束注】
    """

    lowKashida = 'lowKashida'
    """（较低的 Kashida 长度）

        指定当前段落中文本的 Kashida 长度应该扩展到略长一点的长度。当应用 both 设置时，此设置也将应用于阿拉伯文本。

        此设置仅影响 Kashidas，它们是用于扩展两个阿拉伯字符之间的连接符的特殊字符。【注：它们通常用于通过视觉延长单词而不是增加单词之间的间距来改善两端对齐文本的外观。结束注】
    """

    thaiDistribute = 'thaiDistribute'
    """（泰语对齐）

        指定文本应该以针对泰语的优化方式进行两端对齐。

        这种类型的两端对齐会影响每行的单词之间的间距以及在两端对齐其内容时每个单词之间的字符间距，不同于 both 对齐。这种差异是通过略微增加字符间距来创建的，以确保对齐所创建的额外空间被减小。

        【注：此设置与对齐不同，因为在西方语言中，减少字符间距是不合适的。结束注】
    """

    left = 'left'
    """【无文档资料】
    """

    right = 'right'
    """【无文档资料】
    """


class ST_JcTable(ST_BaseEnumType):
    """17.18.45 ST_JcTable (表格对齐类型)

    ST_JcTable (Table Alignment Type)

    这个简单类型指定了在 WordprocessingML 文档中可应用于表格的所有对齐类型。

    【示例：考虑一个右对齐的表格行。这个需求可以在 WordprocessingML 标记中指定如下：

    <w:trPr>
        <w:jc w:val="end" />
    </w:trPr>

    val 属性的值 end 指定了表格在页面上右对齐（假设表格是从左到右对齐的）。示例结束】

    这个简单类型的内容是对 W3C XML Schema 字符串数据类型的限制。

    这个简单类型被限制为以下表格中列出的值：

    center（居中对齐）

        指定表格应该在文档中的两个文本边缘之间居中对齐。

    end（对齐到尾部边缘）

        指定表格应该对齐到文本流的尾部边缘 - 页面的右文本边缘（对于从左到右的表格）；或文档中的左文本边缘（对于从右到左的表格）。（见 §17.4.1）

    start（对齐到起始边缘）

        指定表格应该对齐到文本流的起始边缘 - 页面的左文本边缘（对于从左到右的表格）；或文档中的右文本边缘（对于从右到左的表格）。（见 §17.4.1）
    """

    center = 'center'
    """（居中对齐）

        指定表格应该在文档中的两个文本边缘之间居中对齐。
    """

    end = 'end'
    """（对齐到尾部边缘）

        指定表格应该对齐到文本流的尾部边缘 - 页面的右文本边缘（对于从左到右的表格）；或文档中的左文本边缘（对于从右到左的表格）。（见 §17.4.1）
    """

    start = 'start'
    """（对齐到起始边缘）

        指定表格应该对齐到文本流的起始边缘 - 页面的左文本边缘（对于从左到右的表格）；或文档中的右文本边缘（对于从右到左的表格）。（见 §17.4.1）
    """

    left = 'left'
    """[无文档资料]
    """

    right = 'right'
    """[无文档资料]
    """


class CT_Jc(OxmlBaseElement):
    """17.3.1.13 jc (段落对齐)

    该元素指定了应用于本段落文本的段落对齐方式。

    如果在给定段落中省略了该元素，则其值由样式层次结构的任何级别先前设置的设置确定（即该先前设置保持不变）。如果在样式层次结构中从未指定此设置，则不会应用段落对齐。

    [示例：考虑一个段落，应右对齐到文档中的右页边段落范围。此约束在以下WordprocessingML内容中指定：

    <w:pPr>
        <w:jc w:val="end" />
    </w:pPr>

    现在该段落在页面上右对齐。end 示例]
    """

    @property
    def val_jc(self) -> ST_Jc:
        """val（对齐类型）

        指定应用于文档中父对象的对齐方式。

        此属性的可能值（见下文）始终指定为左对齐相对于段落的前沿，因此在从右到左和从左到右的文档之间会改变语义。

        [示例：考虑以下WordprocessingML片段，用于文档中的段落：

        <w:pPr>
            <w:jc w:val="end" />
        </w:pPr>

        对于从左到右的段落，此段落现在右对齐在页面上，对于从右到左的段落，左对齐。结束示例]
        """
        _val = self.attrib[qn('w:val')]

        return ST_Jc(_val)


class CT_JcTable(OxmlBaseElement):
    @property
    def val_jc_table(self) -> ST_JcTable:
        _val = self.attrib[qn('w:val')]

        return ST_JcTable(_val)


class ST_View(ST_BaseEnumType):
    none = 'none'
    print = 'print'
    outline = 'outline'
    masterPages = 'masterPages'
    normal = 'normal'
    web = 'web'


class CT_View(OxmlBaseElement):
    @property
    def val(self) -> ST_View:
        _val = self.attrib[qn('w:val')]

        return ST_View(_val)


class ST_Zoom(ST_BaseEnumType):
    none = 'none'
    fullPage = 'fullPage'
    bestFit = 'bestFit'
    textFit = 'textFit'


class CT_Zoom(OxmlBaseElement):
    @property
    def val(self) -> Optional[ST_Zoom]:
        _val = self.attrib.get(qn('w:val'))

        if _val is not None:
            return ST_Zoom(_val)
        return None

    @property
    def percent(self) -> ST_DecimalNumberOrPercent:
        _val = self.attrib[qn('w:percent')]

        return to_ST_DecimalNumberOrPercent(_val)  # type: ignore


class CT_WritingStyle(OxmlBaseElement):
    @property
    def lang(self) -> s_ST_Lang:
        _val = self.attrib[qn('w:lang')]

        return s_ST_Lang(str(_val))

    @property
    def vendorID(self) -> str:
        _val = self.attrib[qn('w:vendorID')]

        return str(_val)

    @property
    def dllVersion(self) -> str:
        _val = self.attrib[qn('w:dllVersion')]

        return str(_val)

    @property
    def nlCheck(self) -> s_ST_OnOff:
        _val = self.attrib.get(qn('w:nlCheck'))

        if _val is not None:
            return s_ST_OnOff(_val)

        return s_ST_OnOff.Off

    @property
    def checkStyle(self) -> s_ST_OnOff:
        _val = self.attrib[qn('w:checkStyle')]

        return s_ST_OnOff(_val)

    @property
    def appName(self) -> str:
        _val = self.attrib[qn('w:appName')]

        return str(_val)


class ST_Proof(ST_BaseEnumType):
    clean = 'clean'
    dirty = 'dirty'


class CT_Proof(OxmlBaseElement):
    @property
    def spelling(self) -> Optional[ST_Proof]:
        _val = self.attrib.get(qn('w:spelling'))

        if _val is not None:
            return ST_Proof(_val)
        return None

    @property
    def grammar(self) -> Optional[ST_Proof]:
        _val = self.attrib.get(qn('w:grammar'))

        if _val is not None:
            return ST_Proof(_val)
        return None


class ST_DocType(str):
    """
    <xsd:simpleType name="ST_DocType">
        <xsd:restriction base="xsd:string"/>
    </xsd:simpleType>
    """


class CT_DocType(OxmlBaseElement):
    def grammar(self) -> ST_DocType:
        _val = self.attrib[qn('w:val')]

        return ST_DocType(str(_val))


class ST_DocProtect(ST_BaseEnumType):
    none = 'none'
    readOnly = 'readOnly'
    comments = 'comments'
    trackedChanges = 'trackedChanges'
    forms = 'forms'


class AG_Password(OxmlBaseElement):
    @property
    def algorithmName(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:algorithmName'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def hashValue(self) -> Optional[str]:
        """<xsd:attribute name="hashValue" type="xsd:base64Binary" use="optional"/>"""

        _val = self.attrib.get(qn('w:hashValue'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def saltValue(self) -> Optional[str]:
        """<xsd:attribute name="saltValue" type="xsd:base64Binary" use="optional"/>"""

        _val = self.attrib.get(qn('w:saltValue'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def spinCount(self) -> Optional[str]:
        """<xsd:attribute name="spinCount" type="xsd:base64Binary" use="optional"/>"""

        _val = self.attrib.get(qn('w:spinCount'))

        if _val is not None:
            return str(_val)
        return None


class AG_TransitionalPassword(OxmlBaseElement):
    @property
    def algorithmName(self) -> Optional[s_ST_CryptProv]:
        _val = self.attrib.get(qn('w:algorithmName'))

        if _val is not None:
            return s_ST_CryptProv(_val)
        return None

    @property
    def cryptAlgorithmClass(self) -> Optional[s_ST_AlgClass]:
        _val = self.attrib.get(qn('w:cryptAlgorithmClass'))

        if _val is not None:
            return s_ST_AlgClass(_val)
        return None

    @property
    def cryptAlgorithmType(self) -> Optional[s_ST_AlgType]:
        _val = self.attrib.get(qn('w:cryptAlgorithmType'))

        if _val is not None:
            return s_ST_AlgType(_val)
        return None

    @property
    def cryptAlgorithmSid(self) -> Optional[ST_DecimalNumber]:
        _val = self.attrib.get(qn('w:cryptAlgorithmSid'))

        if _val is not None:
            return ST_DecimalNumber(int(_val))
        return None

    @property
    def cryptSpinCount(self) -> Optional[ST_DecimalNumber]:
        _val = self.attrib.get(qn('w:cryptSpinCount'))

        if _val is not None:
            return ST_DecimalNumber(int(_val))
        return None

    @property
    def cryptProvider(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:cryptProvider'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def algIdExt(self) -> Optional[ST_LongHexNumber]:
        _val = self.attrib.get(qn('w:algIdExt'))

        if _val is not None:
            return ST_LongHexNumber(_val)  # type: ignore
        return None

    @property
    def algIdExtSource(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:algIdExtSource'))

        if _val is not None:
            return str(_val)  # type: ignore
        return None

    @property
    def cryptProviderTypeExt(self) -> Optional[ST_LongHexNumber]:
        _val = self.attrib.get(qn('w:cryptProviderTypeExt'))

        if _val is not None:
            return ST_LongHexNumber(_val)  # type: ignore
        return None

    @property
    def cryptProviderTypeExtSource(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:cryptProviderTypeExtSource'))

        if _val is not None:
            return str(_val)  # type: ignore
        return None

    @property
    def hash(self) -> Optional[str]:
        """<xsd:attribute name="hash" type="xsd:base64Binary"/>"""

        _val = self.attrib.get(qn('w:hash'))

        if _val is not None:
            return str(_val)  # type: ignore
        return None

    @property
    def salt(self) -> Optional[str]:
        """<xsd:attribute name="salt" type="xsd:base64Binary"/>"""

        _val = self.attrib.get(qn('w:salt'))

        if _val is not None:
            return str(_val)  # type: ignore
        return None


class CT_DocProtect(AG_Password, AG_TransitionalPassword):
    @property
    def edit(self) -> Optional[ST_DocProtect]:
        _val = self.attrib.get(qn('w:edit'))

        if _val is not None:
            return ST_DocProtect(_val)
        return None

    @property
    def formatting(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:formatting'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def enforcement(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:enforcement'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None


class ST_MailMergeDocType(ST_BaseEnumType):
    catalog = 'catalog'
    envelopes = 'envelopes'
    mailingLabels = 'mailingLabels'
    formLetters = 'formLetters'
    email = 'email'
    fax = 'fax'


class CT_MailMergeDocType(OxmlBaseElement):
    @property
    def val(self) -> ST_MailMergeDocType:
        _val = self.attrib[qn('w:val')]

        return ST_MailMergeDocType(_val)


class ST_MailMergeDataType(str):
    """
    <xsd:simpleType name="ST_MailMergeDataType">
        <xsd:restriction base="xsd:string"/>
    </xsd:simpleType>
    """



class CT_MailMergeDataType(OxmlBaseElement):
    @property
    def val(self) -> ST_MailMergeDataType:
        _val = self.attrib[qn('w:val')]

        return ST_MailMergeDataType(_val)


class ST_MailMergeDest(ST_BaseEnumType):
    newDocument = 'newDocument'
    printer = 'printer'
    email = 'email'
    fax = 'fax'


class CT_MailMergeDest(OxmlBaseElement):
    @property
    def val(self) -> ST_MailMergeDest:
        _val = self.attrib[qn('w:val')]

        return ST_MailMergeDest(_val)


class ST_MailMergeOdsoFMDFieldType(ST_BaseEnumType):
    null = 'null'
    dbColumn = 'dbColumn'


class CT_MailMergeOdsoFMDFieldType(OxmlBaseElement):
    @property
    def val_field_type(self) -> ST_MailMergeOdsoFMDFieldType:
        """[有联合类型]"""
        _val = self.attrib[qn('w:val')]

        return ST_MailMergeOdsoFMDFieldType(_val)


class CT_TrackChangesView(OxmlBaseElement):
    """ """

    @property
    def markup(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:markup'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def comments(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:comments'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def insDel(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:insDel'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def formatting(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:formatting'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def inkAnnotations(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:inkAnnotations'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None


class CT_Kinsoku(OxmlBaseElement):
    @property
    def lang(self) -> s_ST_Lang:
        _val = self.attrib[qn('w:lang')]

        return s_ST_Lang(str(_val))

    @property
    def val(self) -> str:
        _val = self.attrib[qn('w:val')]

        return str(_val)


class ST_TextDirection(ST_BaseEnumType):
    """17.18.93 ST_TextDirection (文本流方向)

    ST_TextDirection (Text Flow Direction)

    这种简单类型指定了父对象文本流的方向。

    [示例：考虑一个对象，其中文本必须垂直定向，水平从左到右在页面上流动。通过在类型为ST_TextDirection的元素中使用lr值来实现这一点。示例结束]

    这种简单类型的内容是对W3C XML Schema字符串数据类型的限制。
    """

    tb = 'tb'
    """指定父对象中的文本应水平定向，垂直从上到下在页面上流动。

    可以使用各个段落内的bidi元素（§17.3.1.6）将文本方向设置为从右到左。

    这意味着在文本垂直扩展之前，水平线被填充。
    """

    rl = 'rl'
    """指定父对象中的文本应垂直定向，水平从右到左在页面上流动，就好像文本被旋转了90度一样。

    这意味着在文本水平扩展之前，垂直线被填充。
    """

    lr = 'lr'
    """指定父对象中的文本应垂直定向，水平从左到右在页面上流动。

    这意味着在文本水平扩展之前，垂直线被填充。
    """

    tbV = 'tbV'
    """指定父对象中的文本应水平定向，垂直从上到下在页面上流动。

    这意味着在文本垂直扩展之前，水平线被填充。

    这种流动也被旋转，因此在页面上显示时，任何来自东亚文字的字符会顺时针旋转270度。
    """

    rlV = 'rlV'
    """指定父对象中的文本应垂直定向，水平从右到左在页面上流动。

    这意味着在文本水平扩展之前，垂直线被填充。

    这种流动也被旋转，因此在页面上显示时，不是东亚文字的文本会顺时针旋转90度。
    """

    lrV = 'lrV'
    """指定父对象中的文本应垂直定向，水平从左到右在页面上流动。

    这意味着在文本水平扩展之前，垂直线被填充。

    这种流动也顺时针旋转，因此在页面上显示时，不是东亚文字的文本会顺时针旋转90度。
    """

    btLr = 'btLr'
    """未知
    """

    lrTb = 'lrTb'
    """未知
    """

    lrTbV = 'lrTbV'
    """未知
    """

    tbLrV = 'tbLrV'
    """未知
    """

    tbRl = 'tbRl'
    """未知
    """

    tbRlV = 'tbRlV'
    """未知
    """


class CT_TextDirection(OxmlBaseElement):
    """17.3.1.41 textDirection (段落文本流方向)

    该元素指定了该段落的文本流方向。

    如果在给定段落中省略了此元素，则其值由先前在样式层次结构的任何级别上设置的设置确定（即，先前的设置保持不变）。如果样式层次结构中从未指定此设置，则段落将继承父节的文本流设置。

    [示例：考虑一个文档，其中有一个段落，文本必须是垂直定向的，从页面上的左到右水平流动。可以通过以下WordprocessingML指定此设置：

    <w:pPr>
        <w:textDirection w:val="lr" />
    </w:pPr>

    textDirection元素通过val属性中的lr值指定了文本流必须是垂直定向的，后续行从左到右堆叠。 示例结束]
    """

    @property
    def val(self) -> ST_TextDirection:
        """val（文本流的方向）

        指定此对象的文本流方向。

        [示例：考虑一个文档，其中一个部分的文本应该垂直定向，在页面上水平从左到右流动。需要以下WordprocessingML设置：

        <w:sectPr>
            …
            <w:textDirection w:val="lr" />
        </w:sectPr>

        textDirection元素通过val属性中的lr值指定了文本流必须是垂直定向的，后续行从左到右堆叠。示例结束]
        """
        _val = self.attrib[qn('w:val')]

        return ST_TextDirection(_val)


class ST_TextAlignment(ST_BaseEnumType):
    top = 'top'
    center = 'center'
    baseline = 'baseline'
    bottom = 'bottom'
    auto = 'auto'


class CT_TextAlignment(OxmlBaseElement):
    @property
    def val(self) -> ST_TextAlignment:
        _val = self.attrib[qn('w:val')]

        return ST_TextAlignment(_val)


class ST_DisplacedByCustomXml(ST_BaseEnumType):
    next = 'next'
    prev = 'prev'


class ST_AnnotationVMerge(ST_BaseEnumType):
    cont = 'cont'
    rest = 'rest'


class CT_Markup(OxmlBaseElement):
    @property
    def id(self) -> ST_DecimalNumber:
        _val = self.attrib[qn('w:id')]

        return ST_DecimalNumber(_val)


class CT_TrackChange(CT_Markup):
    @property
    def author(self) -> str:
        _val = self.attrib[qn('w:author')]

        return str(_val)

    @property
    def date(self) -> Optional[ST_DateTime]:
        _val = self.attrib.get(qn('w:date'))

        if _val is not None:
            _val = datetime.strptime(str(_val), '%Y-%m-%d %H:%M:%S')
            return ST_DateTime(_val.year, _val.month, _val.day, _val.hour, _val.minute, _val.second)
        return None


class CT_CellMergeTrackChange(CT_TrackChange):
    @property
    def vMerge(self) -> Optional[ST_AnnotationVMerge]:
        _val = self.attrib.get(qn('w:vMerge'))

        if _val is not None:
            return ST_AnnotationVMerge(_val)
        return None

    @property
    def vMergeOrig(self) -> Optional[ST_AnnotationVMerge]:
        _val = self.attrib.get(qn('w:vMergeOrig'))

        if _val is not None:
            return ST_AnnotationVMerge(_val)
        return None


class CT_TrackChangeRange(CT_TrackChange):
    @property
    def displacedByCustomXml(self) -> Optional[ST_DisplacedByCustomXml]:
        _val = self.attrib.get(qn('w:displacedByCustomXml'))

        if _val is not None:
            return ST_DisplacedByCustomXml(_val)
        return None


class CT_MarkupRange(CT_Markup):
    @property
    def displacedByCustomXml(self) -> Optional[ST_DisplacedByCustomXml]:
        _val = self.attrib.get(qn('w:displacedByCustomXml'))

        if _val is not None:
            return ST_DisplacedByCustomXml(_val)
        return None


class CT_BookmarkRange(CT_MarkupRange):
    @property
    def colFirst(self) -> Optional[ST_DecimalNumber]:
        _val = self.attrib.get(qn('w:colFirst'))

        if _val is not None:
            return ST_DecimalNumber(int(_val))
        return None

    @property
    def colLast(self) -> Optional[ST_DecimalNumber]:
        _val = self.attrib.get(qn('w:colLast'))

        if _val is not None:
            return ST_DecimalNumber(int(_val))
        return None


class CT_Bookmark(CT_BookmarkRange):
    @property
    def name(self) -> str:
        _val = self.attrib[qn('w:name')]

        return str(_val)


class CT_MoveBookmark(CT_Bookmark):
    @property
    def author(self) -> str:
        _val = self.attrib[qn('w:author')]

        return str(_val)

    @property
    def date(self) -> ST_DateTime:
        _val = self.attrib[qn('w:date')]

        _val = datetime.strptime(str(_val), '%Y-%m-%d %H:%M:%S')
        return ST_DateTime(_val.year, _val.month, _val.day, _val.hour, _val.minute, _val.second)


class EG_RangeMarkupElements(OxmlBaseElement):
    """
    <xsd:group name="EG_RangeMarkupElements">
        <xsd:choice>
            <xsd:element name="bookmarkStart" type="CT_Bookmark"/>
            <xsd:element name="bookmarkEnd" type="CT_MarkupRange"/>
            <xsd:element name="moveFromRangeStart" type="CT_MoveBookmark"/>
            <xsd:element name="moveFromRangeEnd" type="CT_MarkupRange"/>
            <xsd:element name="moveToRangeStart" type="CT_MoveBookmark"/>
            <xsd:element name="moveToRangeEnd" type="CT_MarkupRange"/>
            <xsd:element name="commentRangeStart" type="CT_MarkupRange"/>
            <xsd:element name="commentRangeEnd" type="CT_MarkupRange"/>
            <xsd:element name="customXmlInsRangeStart" type="CT_TrackChange"/>
            <xsd:element name="customXmlInsRangeEnd" type="CT_Markup"/>
            <xsd:element name="customXmlDelRangeStart" type="CT_TrackChange"/>
            <xsd:element name="customXmlDelRangeEnd" type="CT_Markup"/>
            <xsd:element name="customXmlMoveFromRangeStart" type="CT_TrackChange"/>
            <xsd:element name="customXmlMoveFromRangeEnd" type="CT_Markup"/>
            <xsd:element name="customXmlMoveToRangeStart" type="CT_TrackChange"/>
            <xsd:element name="customXmlMoveToRangeEnd" type="CT_Markup"/>
        </xsd:choice>
    </xsd:group>
    """

    # Union[CT_Bookmark, CT_MarkupRange, CT_MoveBookmark,CT_TrackChange, CT_Markup]
    range_markup_tags = (
        qn('w:bookmarkStart'),  # CT_Bookmark
        qn('w:bookmarkEnd'),  # CT_MarkupRange
        qn('w:moveFromRangeStart'),  # CT_MoveBookmark
        qn('w:moveFromRangeEnd'),  # CT_MarkupRange
        qn('w:moveToRangeStart'),  # CT_MoveBookmark
        qn('w:moveToRangeEnd'),  # CT_MarkupRange
        qn('w:commentRangeStart'),  # CT_MarkupRange
        qn('w:commentRangeEnd'),  # CT_MarkupRange
        qn('w:customXmlInsRangeStart'),  # CT_TrackChange
        qn('w:customXmlInsRangeEnd'),  # CT_Markup
        qn('w:customXmlDelRangeStart'),  # CT_TrackChange
        qn('w:customXmlDelRangeEnd'),  # CT_Markup
        qn('w:customXmlMoveFromRangeStart'),  # CT_TrackChange
        qn('w:customXmlMoveFromRangeEnd'),  # CT_Markup
        qn('w:customXmlMoveToRangeStart'),  # CT_TrackChange
        qn('w:customXmlMoveToRangeEnd'),  # CT_Markup
    )

    @property
    def bookmarkStart(self) -> Optional[CT_Bookmark]:
        return getattr(self, qn('w:bookmarkStart'), None)

    @property
    def bookmarkEnd(self) -> Optional[CT_MarkupRange]:
        return getattr(self, qn('w:bookmarkEnd'), None)

    @property
    def moveFromRangeStart(self) -> Optional[CT_MoveBookmark]:
        return getattr(self, qn('w:moveFromRangeStart'), None)

    @property
    def moveFromRangeEnd(self) -> Optional[CT_MarkupRange]:
        return getattr(self, qn('w:moveFromRangeEnd'), None)

    @property
    def moveToRangeStart(self) -> Optional[CT_MoveBookmark]:
        return getattr(self, qn('w:moveToRangeStart'), None)

    @property
    def moveToRangeEnd(self) -> Optional[CT_MarkupRange]:
        return getattr(self, qn('w:moveToRangeEnd'), None)

    @property
    def commentRangeStart(self) -> Optional[CT_MarkupRange]:
        return getattr(self, qn('w:commentRangeStart'), None)

    @property
    def commentRangeEnd(self) -> Optional[CT_MarkupRange]:
        return getattr(self, qn('w:commentRangeEnd'), None)

    @property
    def customXmlInsRangeStart(self) -> Optional[CT_TrackChange]:
        return getattr(self, qn('w:customXmlInsRangeStart'), None)

    @property
    def customXmlInsRangeEnd(self) -> Optional[CT_Markup]:
        return getattr(self, qn('w:customXmlInsRangeEnd'), None)

    @property
    def customXmlDelRangeStart(self) -> Optional[CT_TrackChange]:
        return getattr(self, qn('w:customXmlDelRangeStart'), None)

    @property
    def customXmlDelRangeEnd(self) -> Optional[CT_Markup]:
        return getattr(self, qn('w:customXmlDelRangeEnd'), None)

    @property
    def customXmlMoveFromRangeStart(self) -> Optional[CT_TrackChange]:
        return getattr(self, qn('w:customXmlMoveFromRangeStart'), None)

    @property
    def customXmlMoveFromRangeEnd(self) -> Optional[CT_Markup]:
        return getattr(self, qn('w:customXmlMoveFromRangeEnd'), None)

    @property
    def customXmlMoveToRangeStart(self) -> Optional[CT_TrackChange]:
        return getattr(self, qn('w:customXmlMoveToRangeStart'), None)

    @property
    def customXmlMoveToRangeEnd(self) -> Optional[CT_Markup]:
        return getattr(self, qn('w:customXmlMoveToRangeEnd'), None)


class EG_MathContent(OxmlBaseElement):
    """

    <xsd:group name="EG_MathContent">
        <xsd:choice>
            <xsd:element ref="m:oMathPara"/>
            <xsd:element ref="m:oMath"/>
        </xsd:choice>
    </xsd:group>
    """

    math_content_choice_tags = (
        qn('m:oMathPara'),  # Any
        qn('m:oMath'),  # Any
    )

    @property
    def oMathPara(self) -> Optional[m_CT_OMathPara]:
        return getattr(self, qn('m:oMathPara'), None)

    @property
    def oMath(self) -> Optional[m_CT_OMath]:
        return getattr(self, qn('m:oMath'), None)


class EG_RunLevelElts(EG_RangeMarkupElements, EG_MathContent):
    """

    <xsd:group name="EG_RunLevelElts">
        <xsd:choice>
            <xsd:element name="proofErr" minOccurs="0" type="CT_ProofErr"/>
            <xsd:element name="permStart" minOccurs="0" type="CT_PermStart"/>
            <xsd:element name="permEnd" minOccurs="0" type="CT_Perm"/>
            <xsd:group ref="EG_RangeMarkupElements" minOccurs="0" maxOccurs="unbounded"/>
            <xsd:element name="ins" type="CT_RunTrackChange" minOccurs="0"/>
            <xsd:element name="del" type="CT_RunTrackChange" minOccurs="0"/>
            <xsd:element name="moveFrom" type="CT_RunTrackChange"/>
            <xsd:element name="moveTo" type="CT_RunTrackChange"/>
            <xsd:group ref="EG_MathContent" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:choice>
    </xsd:group>
    """

    # Union[CT_ProofErr, CT_PermStart, CT_Perm,
    # CT_Bookmark, CT_MarkupRange, CT_MoveBookmark,CT_TrackChange, CT_Markup
    # CT_RunTrackChange, ]
    run_level_elts_choice_tags = (
        (
            qn('w:proofErr'),  # CT_ProofErr
            qn('w:permStart'),  # CT_PermStart
            qn('w:permEnd'),  # CT_Perm
        )
        + EG_RangeMarkupElements.range_markup_tags
        + (
            qn('w:ins'),  # CT_RunTrackChange
            qn('w:del'),  # CT_RunTrackChange
            qn('w:moveFrom'),  # CT_RunTrackChange
            qn('w:moveTo'),  # CT_RunTrackChange
        )
        + EG_MathContent.math_content_choice_tags
    )

    @property
    def proofErr(self) -> Optional[CT_ProofErr]:
        return getattr(self, qn('w:proofErr'), None)

    @property
    def permStart(self) -> Optional[CT_PermStart]:
        return getattr(self, qn('w:permStart'), None)

    @property
    def permEnd(self) -> Optional[CT_Perm]:
        return getattr(self, qn('w:permEnd'), None)

    @property
    def ins(self) -> Optional[CT_RunTrackChange]:
        return getattr(self, qn('w:ins'), None)

    @property
    def delete(self) -> Optional[CT_RunTrackChange]:
        return getattr(self, qn('w:del'), None)

    @property
    def moveFrom(self) -> Optional[CT_RunTrackChange]:
        return getattr(self, qn('w:moveFrom'), None)

    @property
    def moveTo(self) -> Optional[CT_RunTrackChange]:
        return getattr(self, qn('w:moveTo'), None)


class EG_ContentBlockContent(EG_RunLevelElts):
    """
    <xsd:group name="EG_ContentBlockContent">
        <xsd:choice>
            <xsd:element name="customXml" type="CT_CustomXmlBlock"/>
            <xsd:element name="sdt" type="CT_SdtBlock"/>
            <xsd:element name="p" type="CT_P" minOccurs="0" maxOccurs="unbounded"/>
            <xsd:element name="tbl" type="CT_Tbl" minOccurs="0" maxOccurs="unbounded"/>
            <xsd:group ref="EG_RunLevelElts" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:choice>
    </xsd:group>
    """

    # Union[CT_CustomXmlBlock, CT_SdtBlock, CT_P, CT_Tbl, CT_ProofErr, CT_PermStart, CT_Perm, CT_RunTrackChange]
    content_block_tags = (
        qn('w:customXml'),  # CT_CustomXmlBlock
        qn('w:sdt'),  # CT_SdtBlock
        qn('w:p'),  # CT_P
        qn('w:tbl'),  # CT_Tbl
    ) + EG_RunLevelElts.run_level_elts_choice_tags

    @property
    def customXml(self) -> Optional[CT_CustomXmlBlock]:
        return getattr(self, qn('w:customXml'), None)

    @property
    def sdt(self) -> Optional[CT_SdtBlock]:
        return getattr(self, qn('w:sdt'), None)

    @property
    def p_lst(self) -> list[CT_P]:
        return self.findall(qn('w:p'))  # type: ignore

    @property
    def tbl_lst(self) -> list[CT_P]:
        return self.findall(qn('w:tbl'))  # type: ignore


class CT_Comment(CT_TrackChange):
    @property
    def levels(
        self,
    ) -> list[
        CT_CustomXmlBlock | CT_SdtBlock | CT_P | CT_Tbl | CT_ProofErr | CT_PermStart | CT_Perm | CT_RunTrackChange | CT_AltChunk
    ]:
        return self.choice_and_more(*EG_BlockLevelElts.block_level_tags)  # type: ignore

    @property
    def initials(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:initials'))

        if _val is not None:
            return str(_val)
        return None


class CT_TrackChangeNumbering(CT_TrackChange):
    @property
    def original(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:original'))

        if _val is not None:
            return str(_val)
        return None


class CT_TblPrExChange(CT_TrackChange):
    @property
    def tblPrEx(self) -> CT_TblPrExBase:
        return getattr(self, qn('w:tblPrEx'))


class CT_TcPrChange(CT_TrackChange):
    @property
    def tcPr(self) -> CT_TcPrInner:
        return getattr(self, qn('w:tcPr'))


class CT_TrPrChange(CT_TrackChange):
    @property
    def trPr(self) -> CT_TrPrBase:
        return getattr(self, qn('w:trPr'))


class CT_TblGridChange(CT_Markup):
    @property
    def tblGrid(self) -> Optional[CT_TblGridBase]:
        return getattr(self, qn('w:tblGrid'), None)


class CT_TblPrChange(CT_TrackChange):
    """表格样式改变类"""

    @property
    def tblPr(self) -> Optional[CT_TblPrBase]:
        """17.4.58 tblPr (上一个表属性)¶

        tblPr (Previous Table Properties)

        此元素指定了一组先前的表格属性，其修改应归因于特定作者在特定时间进行的修订。该元素包含了在一个特定作者的一组修订之前曾经存在的表格属性设置。这些属性影响父表中所有行和单元格的外观，但可以被各个表级别、行和单元格级别的属性覆盖，每个属性都有自己的定义。

        【示例】考虑以下简单的WordprocessingML表格：

        alt text

        如果将表格对齐设置为居中，并将表格底纹设置为红色，并启用修订标记，如下所示：

        在WordprocessingML中，跟踪此表格上的修订将如下指定：

        <w:tblPr>
            <w:tblStyle w:val="TableGrid"/>
            <w:tblW w:w="0" w:type="auto"/>
            <w:jc w:val="center"/>
            <w:shd w:val="clear" w:color="auto" w:fill="FF0000"/>
            <w:tblLook w:firstRow="true" w:firstColumn="true"
                w:noVBand="true" />
            <w:tblPrChange w:id="0" … >
                <w:tblPr>
                    <w:tblStyle w:val="TableGrid"/>
                    <w:tblW w:w="0" w:type="auto"/>
                    <w:tblLook w:firstRow="true" w:firstColumn="true"
                        w:noVBand="true" />
                </w:tblPr>
            </w:tblPrChange>
        </w:tblPr>

        作为tblPrChange的子元素的tblPr包含了表格属性的先前定义，包括当前跟踪修订之前设置的属性。【示例结束】
        """

        return getattr(self, qn('w:tblPr'), None)


class CT_SectPrChange(CT_TrackChange):
    @property
    def sectPr(self) -> Optional[CT_SectPrBase]:
        return getattr(self, qn('w:sectPr'), None)


class CT_PPrChange(CT_TrackChange):
    @property
    def pPr(self) -> CT_PPrBase:
        """17.3.1.25 pPr (上一段落属性)

        该元素指定了一组段落属性，这些属性应该被归因于特定作者在特定时间的修订。该元素包含了由一个作者跟踪的一组特定修订的属性集。

        【示例：考虑一个应该具有一组段落格式化属性的段落，这些属性是在启用修订跟踪时添加的。此修订后的属性集在段落属性中如下指定：

        <w:p>
            <w:pPr>
                <w:pBdr>
                    <w:bottom w:val="single" w:sz="8" w:space="4" w:color="4F81BD" />
                </w:pBdr>
                <w:pPrChange w:author="user1">
                    <w:pPr>
                        <w:spacing w:after="300" />
                        <w:contextualSpacing />
                    </w:pPr>
                </w:pPrChange>
            </w:pPr>
        </w:p>

        在pPrChange下的pPr元素指定了应用于当前段落的属性，其中启用了修订跟踪 - 在本例中，使用spacing元素（§17.3.1.33）指定段落后的间距，并且应该使用contextualSpacing元素（§17.3.1.9）忽略相同样式的上/下段落的间距。结束示例】
        """
        return getattr(self, qn('w:pPr'))


class CT_RPrChange(CT_TrackChange):
    @property
    def rPr_origin(self) -> CT_RPrOriginal:
        """
        【有联合类型】
        """
        return getattr(self, qn('w:rPr'))


class CT_ParaRPrChange(CT_TrackChange):
    @property
    def rPr_para(self) -> CT_ParaRPrOriginal:
        """【有联合类型】"""
        return getattr(self, qn('w:rPr'))


class CT_RunTrackChange(CT_TrackChange):
    """

    <xsd:complexType name="CT_RunTrackChange">
        <xsd:complexContent>
            <xsd:extension base="CT_TrackChange">
                <xsd:choice minOccurs="0" maxOccurs="unbounded">
                    <xsd:group ref="EG_ContentRunContent"/>
                    <xsd:group ref="m:EG_OMathMathElements"/>
                </xsd:choice>
            </xsd:extension>
        </xsd:complexContent>
    </xsd:complexType>
    """

    def track_change(self):
        from ecma376_office.oxml.shared.math import CT_D as m_CT_D
        from ecma376_office.oxml.shared.math import CT_F as m_CT_F
        from ecma376_office.oxml.shared.math import CT_M as m_CT_M
        from ecma376_office.oxml.shared.math import CT_R as m_CT_R
        from ecma376_office.oxml.shared.math import CT_Acc as m_CT_Acc
        from ecma376_office.oxml.shared.math import CT_Bar as m_CT_Bar
        from ecma376_office.oxml.shared.math import CT_BorderBox as m_CT_BorderBox
        from ecma376_office.oxml.shared.math import CT_Box as m_CT_Box
        from ecma376_office.oxml.shared.math import CT_EqArr as m_CT_EqArr
        from ecma376_office.oxml.shared.math import CT_Func as m_CT_Func
        from ecma376_office.oxml.shared.math import CT_GroupChr as m_CT_GroupChr
        from ecma376_office.oxml.shared.math import CT_LimLow as m_CT_LimLow
        from ecma376_office.oxml.shared.math import CT_LimUpp as m_CT_LimUpp
        from ecma376_office.oxml.shared.math import CT_Nary as m_CT_Nary
        from ecma376_office.oxml.shared.math import CT_Phant as m_CT_Phant
        from ecma376_office.oxml.shared.math import CT_Rad as m_CT_Rad
        from ecma376_office.oxml.shared.math import CT_SPre as m_CT_SPre
        from ecma376_office.oxml.shared.math import CT_SSub as m_CT_SSub
        from ecma376_office.oxml.shared.math import CT_SSubSup as m_CT_SSubSup
        from ecma376_office.oxml.shared.math import CT_SSup as m_CT_SSup
        from ecma376_office.oxml.shared.math import EG_OMathMathElements as m_EG_OMathMathElements

        tags = EG_ContentRunContent.content_run_content_tags + m_EG_OMathMathElements.omath_elements_choice_tags

        elts: CT_CustomXmlRun | CT_SmartTagRun | CT_SdtRun | CT_DirContentRun | CT_BdoContentRun | CT_R | CT_ProofErr | CT_PermStart | CT_Perm | CT_RunTrackChange | CT_Bookmark | CT_MarkupRange | CT_MoveBookmark | CT_TrackChange | CT_Markup | m_CT_LimLow | m_CT_R | m_CT_Bar | m_CT_Nary | m_CT_EqArr | m_CT_Phant | m_CT_D | m_CT_SSup | m_CT_SSubSup | m_CT_Acc | m_CT_LimUpp | m_CT_Rad | m_CT_BorderBox | m_CT_GroupChr | m_CT_Box | m_CT_SSub | m_CT_M | m_CT_SPre | m_CT_Func | m_CT_F = self.choice_and_more(*tags)  # type: ignore

        return elts


class EG_PContentBase(OxmlBaseElement):
    p_content_base_tags = (
        qn('w:customXml'),  # CT_CustomXmlRun
        qn('w:fldSimple'),  # CT_SimpleField
        qn('w:hyperlink'),  # CT_Hyperlink
    )


class EG_ContentRunContentBase(OxmlBaseElement):
    content_run_content_base_tags = (
        qn('w:smartTag'),  # CT_SmartTagRun
        qn('w:sdt'),  # CT_SdtRun
        *EG_RunLevelElts.run_level_elts_choice_tags,
    )


class EG_PContentMath(OxmlBaseElement):
    p_content_math_choice_tags = (
        EG_PContentBase.p_content_base_tags + EG_ContentRunContentBase.content_run_content_base_tags
    )

    @property
    def p_content_base(self):
        return self.choice_and_more(*EG_PContentBase.p_content_base_tags)

    @property
    def content_run_content_base(self):
        return self.choice_and_more(*EG_ContentRunContentBase.content_run_content_base_tags)


class EG_CellMarkupElements(OxmlBaseElement):
    # Union[CT_TrackChange, CT_CellMergeTrackChange]
    cell_markup_tags = (
        qn('w:cellIns'),  # CT_TrackChange
        qn('w:cellDel'),  # CT_TrackChange
        qn('w:cellMerge'),  # CT_CellMergeTrackChange
    )


class CT_NumPr(OxmlBaseElement):
    """17.3.1.19 numPr (编号定义实例参考)

    Numbering Definition Instance Reference

    该元素指定当前段落使用由特定编号定义实例定义的编号信息。

    该元素的存在指定了该段落继承了在num元素（§17.9.15）中指定的编号定义所指定的属性，该编号定义在lvl元素（§17.9.6）中指定的级别处，并且该段落在文本流开始之前应该有一个相关的编号。当此元素出现作为段落样式的段落格式的一部分时，那么使用ilvl元素定义的任何编号级别都将被忽略，而将使用关联抽象编号定义的pStyle元素（§17.9.23）。

    【示例：考虑文档中的一个段落，应该与编号定义ID为0的编号定义的级别4关联。将段落与此编号定义相关联可以使用以下WordprocessingML来指定：

    <w:pPr>
        <w:numPr>
            <w:ilvl w:val="4" />
            <w:numId w:val="0" />
        </w:numPr>
    </w:pPr>

    numPr元素指定该段落必须包含编号信息，其子元素指定该编号信息的编号定义必须在该编号定义中具有编号ID为0和级别为4。结束示例】
    """

    @property
    def ilvl(self) -> Optional[CT_DecimalNumber]:
        """17.9.3 ilvl (编号级别参考)¶

        ilvl (Numbering Level Reference)

        此元素指定将应用于父段落的编号定义实例的编号级别。

        这个编号级别在抽象编号定义的 lvl 元素（§17.9.6）上指定，可以被编号定义实例级别覆盖的 lvl 元素（§17.9.5）重写。
        """

        return getattr(self, qn('w:ilvl'), None)

    @property
    def numId(self) -> Optional[CT_DecimalNumber]:
        """17.9.18 numId (编号定义实例参考)¶

        numId (Numbering Definition Instance Reference)

        该元素指定在 WordprocessingML 文档中给定的父编号段所使用的编号定义实例。

        val 属性的值为 0 时，绝不应用于指向编号定义实例，并且只能用于指示样式层次结构中特定级别的编号属性的移除（通常通过直接格式化）。

        【示例：考虑下面的 WordprocessingML，其中包含一个示例编号段：

            <w:p>
                <w:pPr>
                    <w:numPr>
                        <w:ilvl w:val="0" />
                        <w:numId w:val="5" />
                    </w:numPr>
                </w:pPr>
                …
            </w:p>

        该段落引用了一个 numId 属性值为 5 的编号定义实例，如下所示：


        <w:num w:numId="5">
            <w:abstractNumId w:val="4" />
        </w:num>

        编号定义实例引用指定了应用于给定段落的给定编号定义实例，该段落本身从 abstractNumId 为 4 的抽象编号定义中继承其属性。示例结束】
        """
        return getattr(self, qn('w:numId'), None)

    @property
    def numberingChange(self) -> Optional[CT_TrackChangeNumbering]:
        return getattr(self, qn('w:numberingChange'), None)

    @property
    def ins(self) -> Optional[CT_TrackChange]:
        return getattr(self, qn('w:ins'), None)


class CT_PBdr(OxmlBaseElement):
    @property
    def top(self) -> Optional[CT_Border]:
        return getattr(self, qn('w:top'), None)

    @property
    def left(self) -> Optional[CT_Border]:
        return getattr(self, qn('w:left'), None)

    @property
    def bottom(self) -> Optional[CT_Border]:
        return getattr(self, qn('w:bottom'), None)

    @property
    def right(self) -> Optional[CT_Border]:
        return getattr(self, qn('w:right'), None)

    @property
    def between(self) -> Optional[CT_Border]:
        return getattr(self, qn('w:between'), None)

    @property
    def bar(self) -> Optional[CT_Border]:
        return getattr(self, qn('w:bar'), None)


class CT_Tabs(OxmlBaseElement):
    @property
    def tab(self) -> list[CT_TabStop]:
        return self.findall(qn('w:tab'))  # type: ignore


class ST_TextboxTightWrap(ST_BaseEnumType):
    none = 'none'
    allLines = 'allLines'
    firstAndLastLine = 'firstAndLastLine'
    firstLineOnly = 'firstLineOnly'
    lastLineOnly = 'lastLineOnly'


class CT_TextboxTightWrap(OxmlBaseElement):
    @property
    def val(self) -> ST_TextboxTightWrap:
        return ST_TextboxTightWrap(self.attrib[qn('w:w:val')])


class CT_PPrBase(OxmlBaseElement):
    """17.3.1.25 pPr (上一段落属性)

    该元素指定了一组段落属性，这些属性应该被归因于特定作者在特定时间的修订。该元素包含了由一个作者跟踪的一组特定修订的属性集。

    【示例：考虑一个应该具有一组段落格式化属性的段落，这些属性是在启用修订跟踪时添加的。此修订后的属性集在段落属性中如下指定：

    <w:p>
        <w:pPr>
            <w:pBdr>
                <w:bottom w:val="single" w:sz="8" w:space="4" w:color="4F81BD" />
            </w:pBdr>
            <w:pPrChange w:author="user1">
                <w:pPr>
                    <w:spacing w:after="300" />
                    <w:contextualSpacing />
                </w:pPr>
            </w:pPrChange>
        </w:pPr>
    </w:p>

    在pPrChange下的pPr元素指定了应用于当前段落的属性，其中启用了修订跟踪 - 在本例中，使用spacing元素（§17.3.1.33）指定段落后的间距，并且应该使用contextualSpacing元素（§17.3.1.9）忽略相同样式的上/下段落的间距。结束示例】
    """

    @property
    def pStyle(self) -> Optional[CT_String]:
        """17.9.23 pStyle (段落样式关联的编号级别)

        这个元素指定了一个段落样式的名称，当应用到文档内容时，该样式将自动应用该编号级别。当定义一个段落样式以包含一个编号定义时，任何由 numPr 元素（§17.3.1.19）定义的编号级别都将被忽略，而代之以此元素指定的与该段落样式相关联的编号级别。

        如果这个元素引用了一个不存在或不是段落样式的样式，则可以忽略它。

        【示例：考虑以下 WordprocessingML，指定了当应用到文档中的段落时，样式为 example 的段落样式也必须应用抽象编号定义的第一个编号级别，该编号定义的 abstractNumId 等于 1，如下所示：

        <w:abstractNum w:abstractNumId="1">
            …
            <w:lvl w:ilvl="0">
                …
                <w:pStyle w:val="example" />
                <w:pPr>
                    <w:tabs>
                        <w:tab w:val="num" w:pos="720" />
                    </w:tabs>
                    <w:ind w:start="720" w:hanging="360" />
                </w:pPr>
                …
            </w:lvl>
        </w:abstractNum>

        段落样式的样式定义只包括编号定义实例的 numId，而不包括它的级别：

        <w:style w:styleId="example" w:type="paragraph">
            …
            <w:pPr>
                <w:numPr>
                <w:numId w:val="0" />
                </w:numPr>
            </w:pPr>
        </w:style>

        属性:

        val（字符串值）

        指定其内容包含一个字符串。

        该字符串的内容根据父 XML 元素的上下文进行解释。

        【示例：考虑以下 WordprocessingML 片段：

        <w:pPr>
            <w:pStyle w:val="Heading1" />
        </w:pPr>

        val 属性的值是关联段落样式的 styleId。

        但是，请考虑以下片段：

        <w:sdtPr>
            <w:alias w:val="SDT Title Example" />
            …
        </w:sdtPr>

        在这种情况下，val 属性中的十进制数是最近的祖先结构化文档标记的标题。在每种情况下，该值是根据父元素的上下文进行解释的。示例结束】
        """
        return getattr(self, qn('w:pStyle'), None)

    @property
    def keepNext(self) -> Optional[CT_OnOff]:
        """17.3.1.15 keepNext (使段落与下一段保持一致)

        这个元素指定，当前段落的内容在尽可能的情况下，与后续段落的内容至少部分地在同一页上渲染。

        这意味着如果当前段落的内容通常完全渲染在与后续段落不同的页面上（因为两个段落中只有一个能够适应在第一页上剩余的空间），那么这两个段落将会在同一页上渲染。该属性可以在多个段落之间链接，以确保所有段落都在同一页上渲染，而不会有任何干扰的页面边界。如果在任何情况下，这些使用此属性分组的整个段落集合都会超过一页，则这组“keep with next”段落将从新的一页开始，随后需要分页。

        如果在给定段落中省略了此元素，则其值由样式层次结构的任何级别之前设置的设置确定（即，先前的设置保持不变）。如果在样式层次结构中从未指定此设置，则不应用此属性。
        """
        return getattr(self, qn('w:keepNext'), None)

    @property
    def keepLines(self) -> Optional[CT_OnOff]:
        """17.3.1.14 keepLines (将所有行保留在一页上)

        这个元素指定了这个段落的所有行在可能的情况下应该保持在同一页。

        【注：这意味着如果当前段落的内容由于段落文本的放置而通常会跨越两页，那么这个段落中的所有行应该移动到下一页，以确保它们一起显示。如果这不可能，因为段落中的所有行无论如何都会超过一页，那么这个段落中的行应该从新的一页开始，之后需要分页符。

        如果在给定段落中省略了这个元素，则其值由在样式层次结构的任何级别之前设置的设置确定（即，之前的设置保持不变）。如果在样式层次结构中从未指定此设置，则不应用此属性。结束注】

        【示例：考虑一个 WordprocessingML 文档，其中定义了一个代码片段（例如本文档中的模式片段），这些代码片段应该永远不会跨越页面边界以提高可读性。可以使用以下 WordprocessingML 段落属性来指定这个约束：

        <w:pPr>
            <w:keepLines />
            …
        </w:pPr>

        这个设置确保了模式片段在可能的情况下显示在一页上。结束示例】
        """
        return getattr(self, qn('w:keepLines'), None)

    @property
    def pageBreakBefore(self) -> Optional[CT_OnOff]:
        """17.3.1.23 pageBreakBefore (从下一页开始段落)

        该元素指定当前段落的内容呈现在新页面的开头。

        这意味着，如果当前段落的内容通常应该呈现在主文档的页面中间，那么该段落将被呈现在一个新页面上，就好像在文档的WordprocessingML内容中该段落之前有一个分页符。此属性覆盖了任何使用keepNext属性的情况，因此如果任何段落希望与此段落在同一页上，它们仍然会被分隔开。

        如果在给定段落上省略了此元素，则其值由在样式层次结构中先前设置的设置确定（即该先前设置保持不变）。如果在样式层次结构中从未指定此设置，则不应用此属性。
        """
        return getattr(self, qn('w:pageBreakBefore'), None)

    @property
    def framePr(self) -> Optional[CT_FramePr]:
        """17.3.1.11 framePr (文本框属性)

        该元素指定关于当前段落与文本框架相关的信息。文本框架是文档中定位在文档的独立区域或框架中的文字段落，并且可以相对于文档中非框架段落的特定大小和位置进行定位。

        framePr元素指定的第一条信息是当前段落实际上是文框架中的一部分。这一信息仅通过段落属性中的framePr元素的存在来指定。如果省略了framePr元素，则该段落将不会成为文框架中的任何一部分。

        第二条信息涉及文档中当前文本框架的段落集合。这是根据framePr元素上的属性确定的。如果在两个相邻段落上指定的属性值集合相同，则这两个段落将被视为是同一文本框架的一部分，并在文档中的同一框架内呈现。

        [示例：考虑一个文档，其中以下两个段落相邻地位于一起：

        <w:p>
            <w:pPr>
                <w:framePr w:w="2191" w:h="811" w:hRule="exact" w:hSpace="180" w:wrap="around" w:vAnchor="text" w:hAnchor="page" w:x="1921"/>
            </w:pPr>
            <w:r>
                <w:t>第一段</w:t>
            </w:r>
        </w:p>
        <w:p>
            <w:pPr>
                <w:framePr w:w="2191" w:h="810" w:hRule="exact" w:hSpace="180" w:wrap="around" w:vAnchor="text" w:hAnchor="page" w:x="1921"/>
            </w:pPr>
            <w:r>
                <w:t>第二段。</w:t>
            </w:r>
        </w:p>

        这两个段落，尽管每个都是由于framePr元素的存在而成为文本框架的一部分，但由于不同的h值（810与811），它们是不同的文本框架。结束示例]

        框架相对于其属性值存储的定位应根据文档中的下一个段落计算，该段落本身不是文本框的一部分。
        """
        return getattr(self, qn('w:framePr'), None)

    @property
    def widowControl(self) -> Optional[CT_OnOff]:
        """17.3.1.44 widowControl (允许第一行/最后一行显示在单独的页面上)

        这个元素指定了消费者是否应该防止此段落的单行在显示时出现在独立页面上，并将该行移动到下一页。

        在页面上显示段落时，有时段落的第一行会显示为前一页的最后一行，而所有后续行会显示在下一页上。此属性确保消费者应该将单行也移动到下一页，以防止单独一页上仅有一行。此外，如果单行出现在页面顶部，消费者还应该将前一行移动到下一页，以防止单行显示在单独的页面上。

        如果在给定的段落中省略了此元素，则其值由样式层次结构的任何级别先前设置的设置确定（即，该先前设置保持不变）。如果在样式层次结构中从未指定此设置，则该段落应该在通常发生时防止单行显示在单独的页面上。
        """
        return getattr(self, qn('w:widowControl'), None)

    @property
    def numPr(self) -> Optional[CT_NumPr]:
        """17.3.1.19 numPr (编号定义实例参考)

        Numbering Definition Instance Reference

        该元素指定当前段落使用由特定编号定义实例定义的编号信息。

        该元素的存在指定了该段落继承了在num元素（§17.9.15）中指定的编号定义所指定的属性，该编号定义在lvl元素（§17.9.6）中指定的级别处，并且该段落在文本流开始之前应该有一个相关的编号。当此元素出现作为段落样式的段落格式的一部分时，那么使用ilvl元素定义的任何编号级别都将被忽略，而将使用关联抽象编号定义的pStyle元素（§17.9.23）。

        【示例：考虑文档中的一个段落，应该与编号定义ID为0的编号定义的级别4关联。将段落与此编号定义相关联可以使用以下WordprocessingML来指定：

        <w:pPr>
            <w:numPr>
                <w:ilvl w:val="4" />
                <w:numId w:val="0" />
            </w:numPr>
        </w:pPr>

        numPr元素指定该段落必须包含编号信息，其子元素指定该编号信息的编号定义必须在该编号定义中具有编号ID为0和级别为4。结束示例】
        """
        return getattr(self, qn('w:numPr'), None)

    @property
    def suppressLineNumbers(self) -> Optional[CT_OnOff]:
        """17.3.1.35 suppressLineNumbers (抑制段落的行号)

        这个元素指定了当段落的父节设置中使用lnNumType元素（§17.6.8）请求行编号时，消费者是否应计算该段落中的行编号。该元素指定了当前段落的行是否应免于由文档消费者应用于该文档的行编号，不仅抑制了编号的显示，而且从行编号计算中删除了这些行。

        如果在给定的段落中省略了此元素，则其值由之前在样式层次结构的任何级别上设置的设置确定（即，该先前设置保持不变）。如果样式层次结构中从未指定此设置，则节的默认行编号设置，如lnNumType元素中所指定的那样，将应用于该段落的每一行。

        【示例：考虑一个包含三个段落的文档，每个段落都显示在五行中，所有段落都包含在一个指定了lnNumType元素的节中。如果要求第二段落免于行编号，可以使用以下WordprocessingML指定此要求：

        <w:pPr>
            <w:suppressLineNumbers />
        </w:pPr>

        然后，在显示时，该段落将免于行编号，这将导致第一个段落使用第1至第5行的行号，第二个段落没有行号，第三个段落使用第6至第10行的行号。结束示例】
        """
        return getattr(self, qn('w:suppressLineNumbers'), None)

    @property
    def pBdr(self) -> Optional[CT_PBdr]:
        """17.3.1.24 pBdr (段落边框合集)

        该元素指定父段落的边框。每个子元素应指定一种特定类型的边框（左、右、底部、顶部和之间）。

        如果在给定段落上省略了此元素，则其值由在样式层次结构中先前设置的设置确定（即该先前设置保持不变）。如果在样式层次结构中从未指定此设置，则不应用任何段落边框。

        【示例：考虑一对具有三点红色边框和它们之间有六点边框的段落。这些段落各自具有以下段落边框集：

        <w:pBdr>
            <w:top w:val="single" w:sz="24" w:space="1" w:color="FF0000" />
            <w:left w:val="single" w:sz="24" w:space="4" w:color="FF0000" />
            <w:bottom w:val="single" w:sz="24" w:space="1" w:color="FF0000" />
            <w:right w:val="single" w:sz="24" w:space="4" w:color="FF0000" />
            <w:between w:val="single" w:sz="48" w:space="1" w:color="4D5D2C" />
        </w:pBdr>

        结果段落具有相同的 pBdr 值，因此它们将作为单元使用其周围的顶部、左侧、底部和右侧边框，并且它们之间有一个边框。此匹配启发式方法在 pBdr 元素的子元素中进一步讨论。结束示例】
        """
        return getattr(self, qn('w:pBdr'), None)

    @property
    def shd(self) -> Optional[CT_Shd]:
        """17.3.1.31 shd (段落底纹)

        该元素指定应用于段落内容的底纹。

        该底纹由三个组件组成：

        - 背景颜色（Background Color）
        - （可选）图案（ (optional) Pattern）
        - （可选）图案颜色（ (optional) Pattern Color）

        通过在段落后面设置背景颜色，然后使用图案提供的掩码在该背景上应用图案颜色来应用结果底纹。

        如果在给定段落中省略了此元素，则其值由在样式层次结构中先前设置的设置确定（即，该先前设置保持不变）。如果在样式层次结构中从未指定此设置，则不应用任何段落底纹。

        【示例：考虑一个必须具有由主题颜色 accent3 和主题填充 accent6 重叠使用 20% 填充图案的背景的段落。此要求使用以下 WordprocessingML 指定：

        <w:pPr>
            <w:shd w:val="pct20" w:themeColor="accent6" w:themeFill="accent3" />
        </w:pPr>

        根据 pct20图案掩码，生成的段落在前景图案颜色 accent6 下使用背景颜色 accent3。结束示例】

        此元素的内容模型由§17.3.5中的常见底纹属性定义。
        """
        return getattr(self, qn('w:shd'), None)

    @property
    def tabs(self) -> Optional[CT_Tabs]:
        """17.3.1.38 tabs (自定义制表位合集)

        这个元素指定了当前段落中所有制表符要使用的一系列自定义制表位。

        如果在给定段落中省略了此元素，则其值由先前在样式层次结构的任何级别上设置的设置确定（即，该先前设置保持不变）。如果在样式层次结构中从未指定此设置，则此段落将不使用自定义制表位。

        此外，此属性是可添加的 - 样式层次结构中的每个级别的制表位都会相互添加，以确定段落的全部制表位。通过在ind元素（§17.3.1.12）上的hanging属性指定的悬挂缩进也将隐式创建一个自定义制表位在其位置。

        [示例：考虑一个段落，其中包含两个分别位于1.5英寸和3.5英寸处的自定义制表位。这两个制表位将包含在一个tabs元素中，该元素定义了段落的制表位集，如下所示：

        <w:pPr>
            <w:tabs>
                <w:tab w:val="start" w:pos="2160" />
                <w:tab w:val="start" w:pos="5040" />
            </w:tabs>
        </w:pPr>

        tabs元素指定了当前段落的所有自定义制表位。结束示例]
        """
        return getattr(self, qn('w:tabs'), None)

    @property
    def suppressAutoHyphens(self) -> Optional[CT_OnOff]:
        """17.3.1.34 suppressAutoHyphens (禁止段落连字符)

        这个元素指定了当使用文档设置中的autoHyphenation元素（§17.15.1.10）请求时，消费者是否应对该段落执行任何连字处理。该元素指定了当前段落是否应免于由文档消费者应用于该文档的任何连字处理。

        如果在给定的段落中省略了此元素，则其值由之前在样式层次结构的任何级别上设置的设置确定（即，该先前设置保持不变）。如果样式层次结构中从未指定此设置，则文档的默认连字处理设置，如autoHyphenation元素中所指定的那样，将应用于该段落的内容。

        【示例：考虑一个文档，必须由消费者自动连字处理，因为它在其文档设置中将autoHyphenation元素设置为true。如果此段落应免于该连字处理过程，则可以使用以下 WordprocessingML 指定该要求：

        <w:pPr>
            <w:suppressAutoHyphens />
        </w:pPr>

        然后，该段落将在显示时免于消费者的连字处理，而不管文档的连字处理设置如何。结束示例】
        """
        return getattr(self, qn('w:suppressAutoHyphens'), None)

    @property
    def kinsoku(self) -> Optional[CT_OnOff]:
        """17.3.1.16 kinsoku (对每行的第一个和最后一个字符使用东亚版式规则)

        该元素指定了是否应用东亚排版和断行规则来确定每行的起始和结束字符。此属性仅适用于本段落中的简体中文、繁体中文和日文文本。

        如果在给定段落中省略了此元素，则其值由样式层次结构的任何级别之前设置的设置确定（即，先前的设置保持不变）。如果在样式层次结构中从未指定此设置，则该属性应用于本段落中的简体中文、繁体中文和日文文本。

        如果在当前段落上设置了这些规则，则将以下规则应用于段落中除第一个和最后一个字符之外的所有第一个和最后一个字符。默认情况下，kinsoku段落使用以下设置：

        ....
        """
        return getattr(self, qn('w:kinsoku'), None)

    @property
    def wordWrap(self) -> Optional[CT_OnOff]:
        """17.3.1.45 wordWrap (允许在字符级别换行)¶

        该元素指定了消费者是否应该在文本超出行的文本范围时通过在字符级别上分割单词（在字符级别上分割）或将单词移至下一行（在单词级别上分割）来分割文本。【注意：应用程序应该避免在会改变内容语义或外观的情况下分割文本。结束注意】

        如果在给定的段落中省略了此元素，则其值由样式层次结构的任何级别先前设置的设置确定（即，该先前设置保持不变）。如果在样式层次结构中从未指定此设置，则该段落应该在显示时按单词级别而不是字符级别分割空格分隔的语言中的单词。

        [示例：考虑一个段落，其第一行以单词world结束，该行的文本范围通常会落在字母o和字母r之间。如果省略了此元素，生产者通常会将整个单词world移至下一行，因为该单词不适合第一行的文本范围内。然而，如果此文档允许单词在字符级别被分割，该约束将如下所示指定：

        <w:pPr>
            <w:wordWrap w:val="off" />
        </w:pPr>

        结果段落指定了wordWrap被关闭，因此单词“world”将在确切的两个字符（o和r）之间被分割成两行以匹配文本范围。示例结束]


        """
        return getattr(self, qn('w:wordWrap'), None)

    @property
    def overflowPunct(self) -> Optional[CT_OnOff]:
        """17.3.1.21 overflowPunct (允许标点符号超出文本范围)

        该元素指定，当超出缩进/边距应用的范围时，如果超出范围的字符是标点符号，则允许该段落中的文本延伸一个字符。

        省略此元素会将其值设置为 true。

        【示例：考虑一个包含以下字符串的WordprocessingML文档，该字符串位于行尾：

            "This is some text in quotation marks"

        通常，如果文本范围通常会落在字母 s 和闭合引号之间，即使标点符号不是 marks 这个单词的一部分（因为省略 overflowPunct 等同于将其 val 属性设置为 true），引号也将允许延伸一个字符超出行的末尾。

        然而，如果不希望将此行为应用于此段落，生产者可以通过在WordprocessingML中设置属性来指定：

        <w:pPr>
            <w:overflowPunct w:val="0" />
        </w:pPr>

        现在，该行将在字母 s 之后换行，而不考虑下一个字符是否是引号。结束示例】
        """
        return getattr(self, qn('w:overflowPunct'), None)

    @property
    def topLinePunct(self) -> Optional[CT_OnOff]:
        """17.3.1.43 topLinePunct (压缩行首标点符号)

        这个元素指定了当标点符号出现在行首时，是否应该压缩它，以便后续字符可以相应地移动。

        如果在给定的段落中省略了此元素，则其值由样式层次结构的任何级别先前设置的设置确定（即，该先前设置保持不变）。如果在样式层次结构中从未指定此设置，则即使在行首出现时，该段落中的标点符号也不会被压缩。

        [示例：考虑一个段落，应允许行首的标点符号被压缩，以防止它占用不必要的空间。可以使用以下WordprocessingML来指定此约束：

        <w:pPr>
            <w:topLinePunct w:val="on" />
        </w:pPr>

        topLinePunct元素指定在显示此段落时必须允许此压缩。示例结束]
        """
        return getattr(self, qn('w:topLinePunct'), None)

    @property
    def autoSpaceDE(self) -> Optional[CT_OnOff]:
        """17.3.1.2 autoSpaceDE (自动调整拉丁文和东亚文本的间距)

        该元素指定当前段落中的拉丁文本区域和东亚文本区域之间的字符间距是否应自动调整。这些区域应由段落中文本内容的Unicode字符值确定。

        【注：此属性用于确保拉丁文本区域与相邻的东亚文本之间的间距足够，以便拉丁文本可以在东亚文本中轻松阅读。结束注释】

        如果在给定段落中省略了此元素，则其值由先前在样式层次结构的任何级别上设置的设置确定（即该先前设置保持不变）。如果在样式层次结构中从未指定此设置，则假定其值为true。

        【示例：考虑一个段落，其中间距不应根据拉丁文本和东亚文本的存在自动调整。可以使用以下WordprocessingML指定此设置：

        <w:p>
            <w:pPr>
                …
                <w:autoSpaceDE w:val="false" />
            </w:pPr>
            …
        </w:p>

        通过将val明确设置为false，此段落不得自动调整相邻的拉丁文本和东亚文本的间距。结束示例】
        """
        return getattr(self, qn('w:autoSpaceDE'), None)

    @property
    def autoSpaceDN(self) -> Optional[CT_OnOff]:
        """17.3.1.3 autoSpaceDN (自动调整东亚文本和数字的间距)¶

        该元素指定了当前段落中数字区域和东亚文本区域之间的字符间距是否应自动调整。这些区域将由段落内文本内容的Unicode字符值确定。

        【注：此属性用于确保数字区域和相邻的东亚文本之间的间距足够，以便数字可以在东亚文本中轻松阅读。结束注释】

        如果在给定段落中省略了该元素，则其值将由样式层次结构的任何级别先前设置的设置确定（即该先前设置保持不变）。如果在样式层次结构中从未指定此设置，则其值被假定为true。

        【示例：考虑一个段落，其中间距不应根据数字和东亚文本的存在自动调整。可以使用以下WordprocessingML指定此设置：

        <w:p>
            <w:pPr>
                …
                <w:autoSpaceDN w:val="false" />
            </w:pPr>
            …
        </w:p>

        通过将val明确设置为false，该段落会自动调整相邻数字和东亚文本的间距。结束示例】
        """
        return getattr(self, qn('w:autoSpaceDN'), None)

    @property
    def bidi(self) -> Optional[CT_OnOff]:
        """17.3.1.6 bidi (从右到左的段落布局)

        这个元素指定了这个段落应该从右到左显示。这个属性只影响以下一组段落级属性：

        - ind（§17.3.1.12）
        - jc（§17.3.1.13）
        - tab（§17.3.1.37）
        - textDirection（§17.3.1.41）

        这个设置本身不影响段落内文本的顺序 - 详细描述请参见rtl元素（§17.3.2.30）。

        这个元素指定了段落内文本的基本方向是从右到左（参见Unicode标准附录＃9中的HL1）。另请参见第1部分，[§I.2]。

        [示例：考虑一个具有以下bidi属性设置的段落：

        <w:p>
            <w:pPr>
                <w:bidi/>
            </w:pPr>
            …
        </w:p>

        现在这个段落的方向是从右到左，这意味着所有段落属性都是从右到左显示（例如，段落标记符号（如果有）显示在右侧，并且段落第一行的缩进出现在页面的右侧）。示例结束]
        """
        return getattr(self, qn('w:bidi'), None)

    @property
    def adjustRightInd(self) -> Optional[CT_OnOff]:
        """17.3.1.1 adjustRightInd (使用文档网格时自动调整右缩进)

        该元素指定当为当前节使用docGrid元素（§17.6.5）定义了文档网格时，对给定段落是否应自动调整右缩进，从而修改此段落上使用的当前右缩进。

        [注意：此设置用于确保该段落的断行不是由行末字符的宽度决定的。结束注意]

        如果在给定段落上省略了此元素，则其值由先前在样式层次结构的任何级别上设置的设置确定（即，先前的设置保持不变）。如果在样式层次结构中从未指定此设置，则其值假定为true。

        [示例：考虑一个段落，其中当前段落的右缩进不应根据文档网格中设置的字符间距自动确定。可以使用以下WordprocessingML指定此设置：

        <w:p>
            <w:pPr>
                …
                <w:adjustRightInd w:val="false" />
            </w:pPr>
            …
        </w:p>

        通过将val明确设置为false，该段落使用其指定的右缩进设置，而不考虑父节的文档网格的存在。结束示例]
        """
        return getattr(self, qn('w:adjustRightInd'), None)

    @property
    def snapToGrid(self) -> Optional[CT_OnOff]:
        """17.3.1.32 snapToGrid (使用文档网格设置设置行间段落间距)

        该元素指定当前段落在布局段落内容时是否应使用在docGrid元素（§17.6.5）中定义的每页文档网格线设置。此设置确定是否应根据文档网格指定的方式向本段落中的每行添加额外的行间距。

        如果在给定段落中省略了此元素，则其值由在样式层次结构中先前设置的设置确定（即，该先前设置保持不变）。如果在样式层次结构中从未指定此设置，则当为该文档定义文档网格时，段落将使用文档网格来排列文本。

        【示例：考虑一个具有允许每页 15 行的文档网格的部分中的两个单倍行距段落。此文档网格有效地指定必须向每行添加额外的 45.6 点的行间距，以确保生成的页面仅包含 15 行文本。

        如果在第一个段落上设置了此属性，但在第二个段落上关闭了此属性，如下所示：

        <w:p>
            <w:pPr>
                <w:snapToGrid w:val="off" />
            </w:pPr>
            …
        </w:p>
        <w:p>
            …
        </w:p>

        则生成的文档必须在第二个段落的每行中添加 45.6 点的额外行间距，但在第一个段落的每行中不添加额外的行间距，因为关闭了snapToGrid属性。结束示例】
        """
        return getattr(self, qn('w:snapToGrid'), None)

    @property
    def spacing(self) -> Optional[CT_Spacing]:
        """17.3.1.33 spacing (行与段落上方/下方的间距)

        该元素指定在消费者显示段落内容时应用于该段落内容的行间距和段间距。

        如果对于给定段落省略了此元素，则其属性表示的每个设置的值由在样式层次结构中先前设置的设置确定（即，该先前设置保持不变）。如果样式层次结构中以前未指定设置，则其值如下面对应属性所描述。

        【示例：考虑以下 WordprocessingML 段落：

        <w:pPr>
            <w:spacing w:after="200" w:line="276" w:lineRule="auto" />
        </w:pPr>

        此段落指定每段后面至少有 200 个二十分之一点，每行间距根据正常单倍行距计算的 1.15 倍（276 除以 240）自动计算。结束示例】

        在确定任意两个段落之间的间距时，消费者应使用每个段落的行间距的最大值、第一个段落后面的间距以及第二个段落前面的间距来确定段落之间的净间距。

        【示例：考虑文档中连续的两个单倍行距段落，第一个指定间距为 12 点，第二个指定间距为 4 点。这些约束使用以下 WordprocessingML 表示：

        <w:p>
            <w:pPr>
                <w:spacing w:after="240" />
            </w:pPr>
            …
            </w:p>
        <w:p>
            <w:pPr>
                <w:spacing w:before="80" />
            </w:pPr>
            …
        </w:p>

        第一个段落和第二个段落之间的间距为 12 点，因为这是两个段落之间请求的最大间距。结束示例】
        """
        return getattr(self, qn('w:spacing'), None)

    @property
    def ind(self) -> Optional[CT_Ind]:
        """17.3.1.12 ind (段落缩进)

        该元素指定应用于当前段落的缩进属性集。

        缩进设置可以根据个别情况进行覆盖 - 如果在给定段落中省略了该元素的任何单个属性，则其值由在样式层次结构的任何级别上先前设置的设置确定（即该先前设置保持不变）。如果在样式层次结构中从未指定该元素的任何单个属性，则不会对段落应用该缩进类型的缩进。

        [示例：考虑一个段落，该段落应该从文本边距的左右两侧各缩进一英寸，除了每个段落的第一行，该行应该只从文本边距（开始该段落的一侧）缩进四分之一英寸。使用以下WordprocessingML指定这组缩进：

        <w:pPr>
            <w:ind w:start="1440" w:end="1440" w:hanging="1080" />
        </w:pPr>

        这组缩进属性指定应在该段落的文本边距的左右两侧提供1440个点的缩进，并且应在第一个段落的文本中应用1080个点的悬挂缩进（朝向文本边距），从而使其从文本边距缩进四分之一英寸。结束示例]
        """
        return getattr(self, qn('w:ind'), None)

    @property
    def contextualSpacing(self) -> Optional[CT_OnOff]:
        """17.3.1.9 contextualSpacing (使用相同样式时忽略上方和下方的间距)

        该元素指定在此段落之前或之后指定的任何空间（使用间距(spacing)元素（§17.3.1.33）指定）不应在前后段落为相同段落样式时应用，分别影响顶部和底部间距。【示例：此值通常用于列表中的段落，其中不希望存在连续列表项之间的任何空间，即使是从另一个样式继承而来的。示例结束】

        如果在给定段落上省略了此元素，则其值由在样式层次结构的任何级别上先前设置的设置确定（即先前的设置保持不变）。如果在样式层次结构中从未指定此设置，则不会忽略间距。如果存在，则从此段落上方或下方的间距中减去此设置，如果上下文间距关闭，则不会低于零。

        【示例：考虑以下定义的两个段落：

        <w:p>
            <w:pPr>
                <w:pStyle w:val="TestParagraphStyle" />
                <w:spacing w:after="200"/>
                <w:contextualSpacing/>
            </w:pPr>
            …
        </w:p>
        <w:p>
            <w:pPr>
                <w:pStyle w:val="TestParagraphStyle" />
                <w:spacing w:before="240"/>
            </w:pPr>
            …
        </w:p>

        第一个段落指定后间距为10点，第二个段落指定前间距为12点，因此根据间距元素的规则，净段落间距应为12点。然而，由于第一个段落指定其间距在相同样式的段落之间应省略，并且两个段落使用相同的TestParagraphStyle，该值从总值中减去，因此段落间距为2点。示例结束】
        """
        return getattr(self, qn('w:contextualSpacing'), None)

    @property
    def mirrorIndents(self) -> Optional[CT_OnOff]:
        """17.3.1.18 mirrorIndents (使用左/右缩进作为内部/外部缩进)

        该元素指定段落缩进是否应被解释为镜像缩进。当存在该元素时，起始缩进将变为内部缩进（最靠近装订线的一侧），结束缩进将变为外部缩进（最远离装订线的一侧）。【注：此镜像通常用于当文档的内容用于生成签名时——生成的页面组合然后放置在装订线上。当签名在从左到右的文档中打印时，第一页、第三页等被打印在组合纸张的左侧，而第二页、第四页等被打印在右侧，然后装订和折叠。对于从右到左的文档，第一页、第三页等被打印在组合纸张的右侧，而第二页、第四页等被打印在左侧。结束注释】。

        如果为该段落指定了 mirrorIndents 属性，则奇数页的内侧页边缘是结束页边缘，偶数页的内侧页边缘是起始页边缘。相反，奇数页的外侧页边缘是起始页边缘，偶数页的外侧页边缘是结束页边缘。上文中的奇数和偶数编号指的是分页文档中页面的序数位置，而不是每页上可能出现的页码。

        如果在给定段落中省略了此元素，则其值由样式层次结构的任何级别之前设置的设置确定（即，先前的设置保持不变）。如果在样式层次结构中从未指定此设置，则不应用此属性。

        【示例：考虑文档的第一页上的一个段落，当打印和装订生成的文档时，应该从文本边界向内缩进一英寸。这意味着如果该段落在奇数页上，则有一英寸的右缩进，如果在偶数页上，则有一英寸的左缩进。可以使用以下WordprocessingML来指定这组缩进属性：

        <w:pPr>
            <w:ind w:start="1440" />
            <w:mirrorIndents />
        </w:pPr>

        该缩进属性集指定了一个1440 twip的缩进应提供在文本边界的前端。然而，由于设置了mirrorIndents属性，起始缩进实际上是内部缩进，如果此段落在第一页，则必须从文本边界产生一英寸的右缩进。结束示例】
        """
        return getattr(self, qn('w:mirrorIndents'), None)

    @property
    def suppressOverlap(self) -> Optional[CT_OnOff]:
        """17.3.1.36 suppressOverlap (防止文本框重叠)¶

        该元素指定了当一个文本框与另一个文本框在显示时相交时，是否允许其内容重叠。如果一个文本框不能重叠其他文本框，那么在显示时将重新定位以防止这种重叠。

        如果在给定段落中省略了该元素，则其值由之前在样式层次结构的任何级别上设置的设置确定（即，该先前设置保持不变）。如果样式层次结构中从未指定此设置，则允许在相同位置显示的另一个文本框之间允许重叠。

        【示例：考虑一个包含两个允许相互重叠的文本框的文档。如果第二个文本框应该重叠另一个文本框的内容，则可以通过以下WordprocessingML指定该约束：

        <w:p>
            …
        </w:p>
        <w:p>
            <w:pPr>
                <w:framePr … />
                <w:suppressOverlap />
            </w:pPr>
            …
        </w:p>

        指定了 suppressOverlap 属性的结果文本框永远不会与任何相交的文本框重叠。结束示例】
        """
        return getattr(self, qn('w:suppressOverlap'), None)

    @property
    def jc(self) -> Optional[CT_Jc]:
        """17.3.1.13 jc (段落对齐)

        该元素指定了应用于本段落文本的段落对齐方式。

        如果在给定段落中省略了该元素，则其值由样式层次结构的任何级别先前设置的设置确定（即该先前设置保持不变）。如果在样式层次结构中从未指定此设置，则不会应用段落对齐。

        [示例：考虑一个段落，应右对齐到文档中的右页边段落范围。此约束在以下WordprocessingML内容中指定：

        <w:pPr>
            <w:jc w:val="end" />
        </w:pPr>

        现在该段落在页面上右对齐。end 示例]
        """
        return getattr(self, qn('w:jc'), None)

    @property
    def textDirection(self) -> Optional[CT_TextDirection]:
        """17.3.1.41 textDirection (段落文本流方向)

        该元素指定了该段落的文本流方向。

        如果在给定段落中省略了此元素，则其值由先前在样式层次结构的任何级别上设置的设置确定（即，先前的设置保持不变）。如果样式层次结构中从未指定此设置，则段落将继承父节的文本流设置。

        [示例：考虑一个文档，其中有一个段落，文本必须是垂直定向的，从页面上的左到右水平流动。可以通过以下WordprocessingML指定此设置：

        <w:pPr>
            <w:textDirection w:val="lr" />
        </w:pPr>

        textDirection元素通过val属性中的lr值指定了文本流必须是垂直定向的，后续行从左到右堆叠。 示例结束]
        """
        return getattr(self, qn('w:textDirection'), None)

    @property
    def textAlignment(self) -> Optional[CT_TextAlignment]:
        """17.3.1.39 textAlignment (线上的垂直字符对齐方式)

        该元素指定了段落中每行显示的所有文本的垂直对齐方式。如果行高（在添加任何额外间距之前）大于一行或多行字符的高度，所有字符将按照该元素指定的方式相互对齐。

        如果在给定段落中省略了此元素，则其值由先前在样式层次结构的任何级别上设置的设置确定（即，该先前设置保持不变）。如果在样式层次结构中从未指定此设置，则所有字符在行上的垂直对齐方式将由使用者自动确定。
        """
        return getattr(self, qn('w:textAlignment'), None)

    @property
    def textboxTightWrap(self) -> Optional[CT_TextboxTightWrap]:
        """17.3.1.40 textboxTightWrap (允许周围的段落紧密包裹到文本框内容)

        这个元素指定了是否允许文本框中的段落，周围的文本可以与空文本框边界重叠，并且紧密地围绕文本框内的文本边界。

        该元素仅适用于包含在文本框内（具有 txbxContent 祖先）的段落，否则将被忽略。

        如果父文本框不符合以下三个条件，则此属性无效：

        - 文本框环绕应设置为紧密
        - 文本框边框不应设置
        - 文本框阴影不应设置

        如果在给定段落中省略了此元素，则其值由之前在样式层次结构的任何级别上设置的设置确定（即，该先前设置保持不变）。如果在样式层次结构中从未指定此设置，则文本框中的段落没有紧密包裹的覆盖，文本将紧密围绕文本框边界。
        """
        return getattr(self, qn('w:textboxTightWrap'), None)

    @property
    def outlineLvl(self) -> Optional[CT_DecimalNumber]:
        """17.3.1.20 outlineLvl (相关大纲级别)¶

        该元素指定文档中当前段落关联的大纲级别。大纲级别指定一个整数，定义了相关文本的级别。此级别不会影响文档中文本的外观，但将用于计算TOC字段（§17.16.5.68），如果已设置适当的字段开关，并且可以由使用者提供额外的应用行为。

        文档中文本的大纲级别（使用val属性指定）可以从0到9，其中9特别指示此段落未应用任何大纲级别。如果省略了此元素，则假定内容的大纲级别为9（无级别）。

        【示例：考虑文档中应用了大纲级别1的一个段落。此段落将指定以下WordprocessingML：

        <w:pPr>
            <w:outlineLvl w:val="0" />
        </w:pPr>

        此段落现在是大纲级别1，如果插入了利用大纲级别的目录字段，此段落中的文本将在目录中处于一级。结束示例】
        """
        return getattr(self, qn('w:outlineLvl'), None)

    @property
    def divId(self) -> Optional[CT_DecimalNumber]:
        """17.3.1.10 divId (关联的 HTML div ID)

        这个元素指定了当文档以HTML格式保存时，该段落应位于指定的HTML div标签内。然后使用此ID来查找存储在divs（§17.15.2.8）元素中的相关div。【注：当以WordprocessingML格式保存时，此元素用于保留现有HTML文档的保真度。结束注】。

        如果段落未指定此元素，则将关闭前一个段落引用的任何div，并且当保存为HTML时，此段落不属于任何div。如果在当前文档的divs集合中不存在指定的id，则将关闭前一个段落引用的任何div，并且当保存为HTML时，此段落不属于任何div。

        【示例：考虑以下WordprocessingML段落片段：

        <w:p>
            <w:pPr>
                <w:divId w:val="1512645511" />
            </w:pPr>
        </w:p>

        此段落指定其属于存储在divs元素中的id为1512645511的HTML div。结束示例】
        """
        return getattr(self, qn('w:divId'), None)

    @property
    def cnfStyle(self) -> Optional[CT_Cnf]:
        """7.3.1.8 cnfStyle (段落条件格式)

        这个元素指定了一组条件表格样式格式属性，这些属性已应用于此段落，如果此段落包含在表格单元格中。[注：此属性是一种优化，消费者可以使用它来确定段落上的给定属性是表格样式属性的结果还是段落本身的直接格式化。结束注释]

        如果此属性在不包含在表格单元格中的段落上指定，则在阅读文档内容时应忽略其内容。

        [示例：考虑一个位于表格右上角的段落，应用了表格样式，并且表格格式为从左到右。此段落需要指定以下WordprocessingML：

        <w:p>
            <w:pPr>
                <w:cnfStyle w:firstRow="true" w:lastColumn="true" w:firstRowLastColumn="true" />
                …
            </w:pPr>
            …
        </w:p>

        此段落通过设置适当的属性指定了它具有来自表格样式的条件属性，用于父表的第一列、第一行和右上角。结束示例]
        """
        return getattr(self, qn('w:cnfStyle'), None)


class CT_PPr(CT_PPrBase):
    """17.3.1.26 pPr (段落属性)

    该元素指定了一组段落属性，这些属性应用于父段落的内容，在所有样式/编号/表格属性都已应用到文本后。这些属性被定义为直接格式化，因为它们直接应用于段落，并覆盖了样式的任何格式化。

    示例：考虑一个应该具有一组段落格式化属性的段落。这组属性在段落属性中如下指定：

    ```xml
    <w:p>
        <w:pPr>
            <w:pBdr>
                <w:bottom w:val="single" w:sz="8" w:space="4" w:color="4F81BD" />
            </w:pBdr>
            <w:spacing w:after="300" />
            <w:contextualSpacing />
        </w:pPr>
    </w:p>

    pPr元素指定应用于当前段落的属性 - 在本例中，使用bottom元素（§17.3.1.7）指定段落底部的边框，使用spacing元素（§17.3.1.33）指定段落后的间距，并且应该使用contextualSpacing元素（§17.3.1.9）忽略相同样式的上/下段落的间距。
    """

    @property
    def rPr(self) -> Optional[CT_ParaRPr]:
        """17.3.1.29 rPr (段落标记的运行属性)

        这个元素指定应用于表示该段落标记的字符的字形的一组运行属性。作为文档中的一个实际字符，段落标记可以被格式化，因此应能够像文档中的任何其他字符一样表示这种格式化。

        如果此元素不存在，则段落标记未经格式化，就像文本中的任何其他运行一样。

        【示例：考虑以下显示为以下内容的文本运行，包括使用¶作为段落标记字形的显示格式：

        This is some text and the paragraph mark.¶

        如果我们将段落标记的显示格式化为红色，并给它一个 72 点的字体大小，那么 WordprocessingML 必须在段落中反映这种格式化，如下所示：

        <w:pPr>
            <w:rPr>
                <w:color w:val="FF0000" />
                <w:sz w:val="144" />
            </w:rPr>
        </w:pPr>

        段落标记的格式化存储在段落属性下的 rPr 元素中，因为没有为段落标记本身保存运行。结束示例】

        此元素内容模型（CT_ParaRPr）的 W3C XML Schema 定义位于§A.1。上表中的每个子元素不得超过一次。【注意：由于 W3C XML Schema 语言的限制，此限制未反映在元素的内容模型中。】
        """
        return getattr(self, qn('w:rPr'), None)

    @property
    def sectPr(self) -> Optional[CT_SectPr]:
        """17.6.18 sectPr (节属性)

        该元素定义了文档中某一节的节属性。[注意：对于文档中的最后一节，节属性被存储为body元素的子元素。结束注意]

        [示例：考虑一个具有多个节的文档。对于除最后一节之外的所有节，sectPr元素都存储为该节中最后一个段落的子元素，如下所示：

        <w:body>
            <w:p>
                <w:pPr>
                    <w:sectPr>
                        (最后一节的属性)
                    </w:sectPr>
                </w:pPr>
                …
            </w:p>
            …
            <w:sectPr>
                (最后一节的属性)
            </w:sectPr>
        </w:body>

        结束示例]
        """
        return getattr(self, qn('w:sectPr'), None)

    @property
    def pPrChange(self) -> Optional[CT_PPrChange]:
        """17.13.5.29 pPrChange (段落属性的修订信息)

        该元素指定了 WordprocessingML 文档中对一组段落属性的单个修订的详细信息。

        该元素将此修订存储如下：

        - 该元素的子元素包含在此修订之前应用于该段落的完整段落属性集。
        - 该元素的属性包含有关此修订何时发生的信息（即这些属性何时成为“前”一组段落属性）。

        [示例：考虑一个 WordprocessingML 文档中的段落，它被居中，并且此段落属性的更改被跟踪为修订。此修订将使用以下 WordprocessingML 标记指定：

        <w:pPr>
            <w:jc w:val="center"/>
            <w:pPrChange w:id="0" w:date="01-01-2006T12:00:00" w:author="John Doe">
                <w:pPr/>
            </w:pPrChange>
        </w:pPr>

        pPrChange 元素指定了在 2006 年 1 月 1 日由 John Doe 对段落属性进行了修订，且该段落上的前一组段落属性为空集（即在 pPr 元素下没有显式存在的段落属性）。示例结束]
        """
        return getattr(self, qn('w:pPrChange'), None)


class CT_PPrGeneral(CT_PPrBase):
    """17.7.5.2 pPr (段落属性)

    该元素指定了一组段落属性，这些属性包括当前WordprocessingML文档的默认段落属性。[理由：pPr元素存在于pPrDefault元素中的原因是为了方便在WordprocessingML文档中重新使用任何一组段落属性 - 因为段落属性始终是单个pPr元素的子元素，所以该元素可以完整地移动到所需的新位置，而无需进行其他修改。结束理由]

    如果省略此元素，则当前文档的默认段落属性不存在（即没有默认段落属性，因此默认值是应用程序定义的）。

    [示例：考虑以下WordprocessingML文档的文档默认值定义：


    <w:docDefaults>
        <w:pPrDefault>
            <w:pPr>
                <w:jc w:val="center"/>
            </w:pPr>
        </w:pPrDefault>
        …
    </w:docDefaults>

    作为pPrDefault元素的子元素的pPr元素包含此文档的默认段落属性集 - 在此示例中，是居中对齐的值。结束示例]
    """

    @property
    def pPrChange(self) -> Optional[CT_PPrChange]:
        """17.13.5.29 pPrChange (段落属性的修订信息)

        该元素指定了 WordprocessingML 文档中对一组段落属性的单个修订的详细信息。

        该元素将此修订存储如下：

        - 该元素的子元素包含在此修订之前应用于该段落的完整段落属性集。
        - 该元素的属性包含有关此修订何时发生的信息（即这些属性何时成为“前”一组段落属性）。

        [示例：考虑一个 WordprocessingML 文档中的段落，它被居中，并且此段落属性的更改被跟踪为修订。此修订将使用以下 WordprocessingML 标记指定：

        <w:pPr>
            <w:jc w:val="center"/>
            <w:pPrChange w:id="0" w:date="01-01-2006T12:00:00" w:author="John Doe">
                <w:pPr/>
            </w:pPrChange>
        </w:pPr>

        pPrChange 元素指定了在 2006 年 1 月 1 日由 John Doe 对段落属性进行了修订，且该段落上的前一组段落属性为空集（即在 pPr 元素下没有显式存在的段落属性）。示例结束]
        """
        return getattr(self, qn('w:pPrChange'), None)


class CT_Control(OxmlBaseElement):
    """17.3.3.3 control (嵌入式控制)¶

    control (Embedded Control)

    该元素指定父嵌入对象是嵌入式控件的表示。在文档显示时，应使用此元素来关联适当的嵌入式控件设置和属性。

    如果嵌入式控件不存在、由于应用程序设置无法加载，或者不受支持，则应使用适当的占位图像，以提供在文档中适当位置上存在嵌入式控件的表示。

    【示例：考虑一个包含嵌入式控件的运行。可以使用以下 WordprocessingML 指定该运行：

    <w:r>
        <w:object>
            …
            <w:control r:id="rId99" w:shapeid="10" … />
        </w:object>
    </w:r>

    control 元素指示父嵌入对象是嵌入式控件，其设置和属性存储在此元素上，并且使用 id 属性指定的关系的（可选）目标。结束示例】
    """

    @property
    def name(self) -> Optional[str]:
        """name（嵌入式控件的唯一名称）

        指定此嵌入式控件的唯一名称。此名称必须在此文档中的所有控件中唯一。

        【示例：考虑文档中嵌入式控件的以下 WordprocessingML 标记：


        <w:control r:id="rId5" w:name="CheckBox1"
            w:shapeid="_x0000_s1027" />
        name 属性指定此控件的唯一名称必须为 CheckBox1。结束示例】

        此属性的可能值由 ST_String 简单类型定义（§22.9.2.13）。
        """
        _val = self.attrib.get(qn('w:name'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def shapeid(self) -> Optional[str]:
        """shapeid（形状引用）

        指定形状 ID，用于定义此嵌入式控件在文档中的呈现和位置，如果使用 DrawingML 语法浮动控件。

        【注：此定位数据足以在以下任何情况下显示控件：

        - 嵌入式控件不在当前机器上
        - 禁用了嵌入式控件
        - 不支持此控件类型的嵌入式控件

        结束注】

        通过查找 id 属性与此属性中指定的值相匹配的 DrawingML 对象来解析此形状 ID 引用。如果没有这样的形状存在，则控件将以内联方式呈现在文档内容中的当前运行位置。

        如果省略此属性，则此嵌入式控件将在父运行的当前位置内联显示。

        【示例：考虑文档中嵌入式控件的以下 WordprocessingML 标记：

        <w:control r:id="rId5" w:name="CheckBox1" w:shapeid="10" />
        shapeid 属性指定具有 id 属性值为 10 的 DrawingML 对象必须包含此嵌入式控件的定位数据。结束示例】

        此属性的可能值由 ST_String 简单类型定义（§22.9.2.13）。
        """
        _val = self.attrib.get(qn('w:shapeid'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def r_id(self) -> Optional[str]:
        """id（嵌入式控件属性关系引用）

        命名空间：http://purl.oclc.org/ooxml/officeDocument/relationships

        指定包含此嵌入式控件属性的关系的关系 ID。此属性包袋包含在 Office Open XML 包中的一个单独的部分中。

        此属性明确指定的关系必须是类型为 http://purl.oclc.org/ooxml/officeDocument/relationships/control，否则文档将被视为不符合规范。

        如果省略此属性，则在实例化时，嵌入式控件将不会获得属性包袋。

        【示例：考虑文档中嵌入式控件的以下 WordprocessingML 标记：


        <w:control r:id="rId5" w:name="CheckBox1"
            w:shapeid="_x0000_s1027" />

            关系引用命名空间中的 id 属性指定关系 ID 为 rId5 的关系必须包含此嵌入式控件的属性数据。结束示例】

        此属性的可能值由 ST_RelationshipId 简单类型定义（[§22.8.2.1]）。
        """
        _val = self.attrib.get(qn('r:id'))

        if _val is not None:
            return str(_val)
        return None


class CT_Background(OxmlBaseElement):
    """17.2.1 background (文档背景)

    此元素指定包含背景元素的文档的每个页面的背景。文档的背景是整个页面表面的图像或填充，位于所有其他文档内容之后。

    背景元素的绘图 §17.3.3.9 子元素允许将任何DrawingML效果应用于文档的背景。

    然而，对于纯色填充背景，此元素上的属性允许使用任何RGB或主题颜色值（后者是对文档主题部分的引用）。

    <xsd:complexType name="CT_Background">
        <xsd:sequence>
            <xsd:sequence maxOccurs="unbounded">
                <xsd:any processContents="lax" namespace="urn:schemas-microsoft-com:vml" minOccurs="0" maxOccurs="unbounded"/>
                <xsd:any processContents="lax" namespace="urn:schemas-microsoft-com:office:office" minOccurs="0" maxOccurs="unbounded"/>
            </xsd:sequence>
            <xsd:element name="drawing" type="CT_Drawing" minOccurs="0"/>
        </xsd:sequence>
        <xsd:attribute name="color" type="ST_HexColor" use="optional" default="auto"/>
        <xsd:attribute name="themeColor" type="ST_ThemeColor" use="optional"/>
        <xsd:attribute name="themeTint" type="ST_UcharHexNumber" use="optional"/>
        <xsd:attribute name="themeShade" type="ST_UcharHexNumber" use="optional"/>
    </xsd:complexType>
    """

    @property
    def lax(self):
        """<xsd:any processContents="lax" namespace="urn:schemas-microsoft-com:vml" minOccurs="0"
        maxOccurs="unbounded"/>

        """
        return self.lax

    @property
    def drawing(self) -> Optional[CT_Drawing]:
        """17.3.3.9 drawing (DrawingML对象)

        该元素指定在运行内容中的此位置有一个DrawingML对象。该DrawingML对象的布局属性使用WordprocessingML Drawing语法（[§20.4]）来指定。

        示例：考虑一个运行内容为图片，该图片与段落中的文本在同一行（即，位于行中并影响行高）。该运行将使用以下WordprocessingML指定：

        ```xml
        <w:r>
            <w:drawing>
                <wp:inline>
                    …
                </wp:inline>
            </w:drawing>
        </w:r>
        ```

        drawing元素指示当前位置的运行中有一个DrawingML对象及其WordprocessingML Drawing定位数据（例如图片或图表）。
        """
        return getattr(self, qn('w:drawing'), None)

    @property
    def color(self) -> ST_HexColor:
        """背景颜色

        指定文档背景的颜色。

        该值可以定义为以下两种形式之一：

        - 使用RGB颜色模型的颜色值，其红、绿和蓝值以0到255的数字编写，以十六进制编码并连接在一起。【示例：全强度红色将是255红、0绿、0蓝，编码为FF、00、00，并连接为FF0000。示例结束】。RGB颜色在sRGB颜色空间中指定。
        - auto，以便允许使用者自动确定背景颜色，以使文档的文本可读。【示例：具有白色文本和自动背景颜色的文档可能会使用黑色背景，以确保内容的可读性。示例结束】
        如果背景通过themeColor属性指定使用主题颜色，则忽略此值。【注意：应用程序不建议在同一父元素上同时指定color和themeColor属性。注释结束】

        如果既没有color属性也没有themeColor属性，则将处理父页面，就好像没有定义背景一样。
        """
        _val = self.attrib.get(qn('w:color'))

        if _val is not None:
            return s_to_ST_HexColorRGB(_val)  # type: ignore

        return ST_HexColorAuto.Auto

    @property
    def themeColor(self) -> Optional[ST_ThemeColor]:
        """背景主题颜色

        指定用于生成背景颜色的基本主题颜色。背景颜色是与themeColor关联的RGB值，进一步通过themeTint或themeShade（如果存在）进行转换，否则背景颜色就是与themeColor关联的RGB值。

        指定的主题颜色是对文档主题部分（§14.2.7和§20.1.6.9）中预定义的主题颜色之一的引用，这允许在文档中集中设置颜色信息。

        如果指定了颜色属性，则将忽略其值，而使用该属性与任何适当的themeTint和themeShade属性值计算所产生的颜色。

        为了确定要显示的颜色，执行以下操作：

        - 使用ST_ThemeColor简单类型（§17.18.97）中指定的映射，读取clrSchemeMapping元素（§17.15.1.20）上的适当属性。
        - 使用该值和ST_ColorSchemeIndex简单类型（§17.18.103）中指定的映射，读取文档主题部分中的适当元素，以获取基本主题颜色。
        - 根据themeTint或themeShade属性的存在修改指定的颜色。
        """
        _val = self.attrib.get(qn('w:themeColor'))

        if _val is not None:
            return ST_ThemeColor(_val)
        return None

    @property
    def themeTint(self) -> Optional[ST_UcharHexNumber]:
        """背景主题颜色色调

        指定应用于此背景的提供的主题颜色（如果有）的色调值。如果未指定themeColor属性，则不应指定此属性。

        如果提供了themeTint，则将其应用于主题颜色（来自主题部分）的RGB值，以确定应用于文档背景的最终颜色。

        themeTint值存储为应用于当前背景的色调值的十六进制编码（从0到255）。
        """
        _val = self.attrib.get(qn('w:themeTint'))

        if _val is not None:
            return ST_UcharHexNumber(_val)  # type: ignore
        return None

    @property
    def themeShade(self) -> Optional[ST_UcharHexNumber]:
        """背景主题颜色阴影

        指定应用于此背景的提供的主题颜色（如果有）的阴影值。如果未指定themeColor属性，则不应指定此属性。

        如果提供了themeShade，则将其应用于主题颜色（来自主题部分）的RGB值，以确定应用于此背景的最终颜色。

        如果提供了themeTint，则应忽略此属性的值。

        themeShade值存储为应用于当前背景的阴影值的十六进制编码（从0到255）。
        """
        _val = self.attrib.get(qn('w:themeShade'))

        if _val is not None:
            return ST_UcharHexNumber(_val)  # type: ignore
        return None


class CT_Rel(OxmlBaseElement):
    """17.3.3.17 movie (嵌入式视频)¶

    movie (Embedded Video)

    该元素指定了文档中的一个位置，指定的父图像应被视为嵌入式电影的静态占位符。【注意：在§15.2.17中提供了建议的视频类型列表。】当在文档中的此位置请求时，应显示指定电影文件的内容。当支持时，应指定要显示的嵌入式电影的位置，该位置由其 Id 属性与此元素上的 id 属性匹配的关系指定。

    如果此元素指定的关系的关系类型不是 http://purl.oclc.org/ooxml/officeDocument/relationships/movie，或者不存在，则文档将被视为不符合规范。如果应用程序无法处理由目标部分指定的内容类型的外部内容，则可以忽略它。
    """

    @property
    def r_id(self) -> str:
        """id（与部件的关系）

        命名空间：http://purl.oclc.org/ooxml/officeDocument/relationships

        指定与指定部分的关系 ID。

        指定的关系应与父元素所需的关系类型匹配：

        - 对于 contentPart 元素，关系类型应为 http://purl.oclc.org/ooxml/officeDocument/relationships/customXml
        - 对于 footerReference 元素，关系类型应为 http://purl.oclc.org/ooxml/officeDocument/relationships/footer
        - 对于 headerReference 元素，关系类型应为 http://purl.oclc.org/ooxml/officeDocument/relationships/header
        - 对于 embedBold、embedBoldItalic、embedItalic 或 embedRegular 元素，关系类型应为 http://purl.oclc.org/ooxml/officeDocument/relationships/font
        - 对于 printerSettings 元素，关系类型应为 http://purl.oclc.org/ooxml/officeDocument/relationships/printerSettings
        - 对于 longDesc 或 hyperlink 元素，关系类型应为 http://purl.oclc.org/ooxml/officeDocument/relationships/hyperlink

        [示例：考虑一个具有以下 id 属性的 XML 元素：

        <… r:id="rId10" />

        该标记指定了关系 ID 为 rId1 的关联部分包含了父 XML 元素的相应关系信息。示例结束]
        """
        return self.attrib[qn('r:id')]



class CT_Object(OxmlBaseElement):
    """17.3.3.19 object (嵌入对象)

    object (Embedded Object)

    这个元素指定了一个嵌入对象位于运行内容中的当前位置。该嵌入对象的布局属性以及可选的静态表示是使用 drawing 元素（§17.3.3.9）指定的。

    [示例：考虑一个运行，其中包含一个嵌入对象，该对象与段落中的文本同行（即位于同一行，并影响行高）。该运行可以使用以下 WordprocessingML 进行指定：

    <w:r>
        <w:object>
            <w:drawing>
                …
            </w:drawing>
        </w:object>
    </w:r>
    object 元素指示一个嵌入对象及其定位数据位于运行的当前位置（例如，一个嵌入对象）。示例结束]

    <xsd:complexType name="CT_Object">
        <xsd:sequence>
            <xsd:sequence maxOccurs="unbounded">
                <xsd:any processContents="lax" namespace="urn:schemas-microsoft-com:vml" minOccurs="0"
                maxOccurs="unbounded"/>
                <xsd:any processContents="lax" namespace="urn:schemas-microsoft-com:office:office"
                minOccurs="0" maxOccurs="unbounded"/>
            </xsd:sequence>
            <xsd:element name="drawing" type="CT_Drawing" minOccurs="0"/>
            <xsd:choice minOccurs="0">
                <xsd:element name="control" type="CT_Control"/>
                <xsd:element name="objectLink" type="CT_ObjectLink"/>
                <xsd:element name="objectEmbed" type="CT_ObjectEmbed"/>
                <xsd:element name="movie" type="CT_Rel"/>
            </xsd:choice>
        </xsd:sequence>
        <xsd:attribute name="dxaOrig" type="s:ST_TwipsMeasure" use="optional"/>
        <xsd:attribute name="dyaOrig" type="s:ST_TwipsMeasure" use="optional"/>
    </xsd:complexType>

    <w:object>
        <v:shape id="_x0000_i1067" o:spt="75" type="#_x0000_t75" style="height:12pt;width:24.4pt;" o:ole="t" filled="f" o:preferrelative="t" stroked="f" coordsize="21600,21600">
            <v:path/>
            <v:fill on="f" focussize="0,0"/>
            <v:stroke on="f" color="#000000"/>
            <v:imagedata r:id="rId101" o:title="image49"/>
            <o:lock v:ext="edit" aspectratio="t"/>
            <w10:wrap type="none"/>
            <w10:anchorlock/>
        </v:shape>
        <o:OLEObject Type="Embed" ProgID="Package" ShapeID="_x0000_i1067" DrawAspect="Content" ObjectID="_1468075767" r:id="rId100">
            <o:LockedField>false</o:LockedField>
        </o:OLEObject>
    </w:object>
    """

    @property
    def shape(self):

        ele: Optional[CT_Shape] = getattr(self, qn('v:shape'), None)

        return ele

    @property
    def ole_object(self):

        ele: Optional[CT_OLEObject] = getattr(self, qn('o:OLEObject'), None)

        return ele

    @property
    def drawing(self) -> Optional[CT_Drawing]:
        """17.3.3.9 drawing (DrawingML对象)

        drawing (DrawingML Object)

        该元素指定在运行内容中的此位置有一个DrawingML对象。该DrawingML对象的布局属性使用WordprocessingML Drawing语法（§20.4）来指定。

        [示例：考虑一个运行内容为图片，该图片与段落中的文本在同一行（即，位于行中并影响行高）。该运行将使用以下WordprocessingML指定：

        <w:r>
            <w:drawing>
                <wp:inline>
                    …
                </wp:inline>
            </w:drawing>
        </w:r>

        drawing元素指示当前位置的运行中有一个DrawingML对象及其WordprocessingML Drawing定位数据（例如图片或图表）。示例结束]
        """
        return getattr(self, qn('w:drawing'), None)

    @property
    def obj(self) -> Optional[CT_Control | CT_ObjectLink | CT_ObjectEmbed | CT_Rel]:
        tags = (
            qn('w:control'),  # CT_Control
            qn('w:objectLink'),  # CT_ObjectLink
            qn('w:objectEmbed'),  # CT_ObjectEmbed
            qn('w:movie'),  # CT_Rel
        )

        return self.choice_one_child(*tags)  # type: ignore

    @property
    def control(self) -> Optional[CT_Control]:
        """17.3.3.3 control (嵌入式控制)¶

        control (Embedded Control)

        该元素指定父嵌入对象是嵌入式控件的表示。在文档显示时，应使用此元素来关联适当的嵌入式控件设置和属性。

        如果嵌入式控件不存在、由于应用程序设置无法加载，或者不受支持，则应使用适当的占位图像，以提供在文档中适当位置上存在嵌入式控件的表示。

        【示例：考虑一个包含嵌入式控件的运行。可以使用以下 WordprocessingML 指定该运行：

        <w:r>
            <w:object>
                …
                <w:control r:id="rId99" w:shapeid="10" … />
            </w:object>
        </w:r>

        control 元素指示父嵌入对象是嵌入式控件，其设置和属性存储在此元素上，并且使用 id 属性指定的关系的（可选）目标。结束示例】
        """
        return getattr(self, qn('w:control'), None)

    @property
    def objectLink(self) -> Optional[CT_ObjectLink]:
        """17.3.3.21 objectLink (链接对象属性)¶

        objectLink (Linked Object Properties)

        这个元素指定了嵌入链接对象的可视属性、相关服务器应用程序和刷新模式。

        [示例：以下演示了一个嵌入在 WordprocessingML 文档中的视频文件：

        <w:object … >
        <w:drawing> … </w:drawing>
        <w:objectLink drawAspect="icon" r:id="rId3" progId="AVIFile" shapeId="10"
            updateMode="user"/>
        </w:object>

        示例结束]
        """
        return getattr(self, qn('w:objectLink'), None)

    @property
    def objectEmbed(self) -> Optional[CT_ObjectEmbed]:
        """17.3.3.20 objectEmbed (嵌入对象属性)¶

        objectEmbed (Embedded Object Properties)

        这个元素指定了嵌入对象的视觉属性和关联的服务器应用程序。

        [示例：以下演示了一个视频文件嵌入到 WordprocessingML 文档中：

        <w:object … >
            <w:drawing> … </w:drawing>
            <w:objectEmbed drawAspect="content" r:id="rId3" progId="AVIFile"
                shapeId="10"/>
        </w:object>

        示例结束]
        """
        return getattr(self, qn('w:objectEmbed'), None)

    @property
    def movie(self) -> Optional[CT_Rel]:
        """17.3.3.17 movie (嵌入式视频)¶

        movie (Embedded Video)

        该元素指定了文档中的一个位置，指定的父图像应被视为嵌入式电影的静态占位符。【注意：在§15.2.17中提供了建议的视频类型列表。】当在文档中的此位置请求时，应显示指定电影文件的内容。当支持时，应指定要显示的嵌入式电影的位置，该位置由其 Id 属性与此元素上的 id 属性匹配的关系指定。

        如果此元素指定的关系的关系类型不是 http://purl.oclc.org/ooxml/officeDocument/relationships/movie，或者不存在，则文档将被视为不符合规范。如果应用程序无法处理由目标部分指定的内容类型的外部内容，则可以忽略它。
        """
        return getattr(self, qn('w:movie'), None)

    @property
    def dxaOrig(self) -> Optional[s_ST_TwipsMeasure]:
        """dxaOrig（原始图像宽度）

        指定文档中当前控件的图像表示的原始（自然）宽度。一些矢量图像格式不在其格式中存储原生大小，因此只有在这些情况下才应使用此属性来存储此信息，以便根据需要适当地恢复图像。

        如果省略此属性，则应使用存储在其格式中的图像的自然宽度。

        [示例：考虑以下用于嵌入对象的 WordprocessingML：

        <w:object w:dxaOrig="3360" w:dyaOrig="2520">
        …
        </w:object>

        dxaOrig 属性的值为 3360，指定用于嵌入对象的图像不存储其原生宽度，但该宽度应为 3360 个点的二十分之一。示例结束]

        此属性的可能值由 ST_TwipsMeasure 简单类型定义（§22.9.2.14）。
        """
        _val = self.attrib.get(qn('w:dxaOrig'))

        if _val is not None:
            return s_to_ST_TwipsMeasure(_val)  # type: ignore
        return None

    @property
    def dyaOrig(self) -> Optional[s_ST_TwipsMeasure]:
        """dyaOrig（原始图像高度）

        指定文档中当前控件的图像表示的原始（自然）高度。一些矢量图像格式不在其格式中存储原生大小，因此只有在这些情况下才应使用此属性来存储此信息，以便根据需要适当地恢复图像。

        如果省略此属性，则应使用存储在其格式中的图像的自然高度。

        [示例：考虑以下用于嵌入对象的 WordprocessingML：

        <w:object w:dxaOrig="3360" w:dyaOrig="2520">
        …
        </w:object>

        dyaOrig 属性的值为 2520，指定用于嵌入对象的图像不存储其原生高度，但该高度应为 2520 个点的二十分之一。示例结束]
        """
        _val = self.attrib.get(qn('w:dyaOrig'))

        if _val is not None:
            return s_to_ST_TwipsMeasure(_val)  # type: ignore
        return None


class CT_Picture(OxmlBaseElement):
    """17.5.2.24 picture (图片结构化文档标签)¶

    picture (Picture Structured Document Tag)

    该元素指定了在文档中显示时，最近祖先结构化文档标记应为图片。

    此设置指定了此结构化文档标记的行为应如下：

        - 内容应始终限制为单个图片，使用 DrawingML（§20.1）语法。

    此外，结构化文档标记应满足以下限制，否则文档将被视为不符合规范：


    - 内容应仅为单个图片，使用 DrawingML（§20.1）语法。
    - 内容不得包含多个段落或表格单元，也不得包含表格行或表格。

    <xsd:complexType name="CT_Picture">
        <xsd:sequence>
            <xsd:sequence maxOccurs="unbounded">
                <xsd:any processContents="lax" namespace="urn:schemas-microsoft-com:vml" minOccurs="0"
                maxOccurs="unbounded"/>
                <xsd:any processContents="lax" namespace="urn:schemas-microsoft-com:office:office"
                minOccurs="0" maxOccurs="unbounded"/>
            </xsd:sequence>
            <xsd:element name="movie" type="CT_Rel" minOccurs="0"/>
            <xsd:element name="control" type="CT_Control" minOccurs="0"/>
        </xsd:sequence>
    </xsd:complexType>
    """

    @property
    def v_shap(self):
        """vml中的shape"""

        v_s: Optional[CT_Shape] = getattr(self, qn('v:shape'), None)

        return v_s

    @property
    def lax(self):
        return self.lax

    @property
    def movie(self) -> Optional[CT_Rel]:
        return getattr(self, qn('w:movie'), None)

    @property
    def control(self) -> Optional[CT_Control]:
        """17.3.3.3 control (嵌入式控制)¶

        control (Embedded Control)

        该元素指定父嵌入对象是嵌入式控件的表示。在文档显示时，应使用此元素来关联适当的嵌入式控件设置和属性。

        如果嵌入式控件不存在、由于应用程序设置无法加载，或者不受支持，则应使用适当的占位图像，以提供在文档中适当位置上存在嵌入式控件的表示。

        【示例：考虑一个包含嵌入式控件的运行。可以使用以下 WordprocessingML 指定该运行：

        <w:r>
            <w:object>
                …
                <w:control r:id="rId99" w:shapeid="10" … />
            </w:object>
        </w:r>

        control 元素指示父嵌入对象是嵌入式控件，其设置和属性存储在此元素上，并且使用 id 属性指定的关系的（可选）目标。结束示例】
        """
        return getattr(self, qn('w:control'), None)


class CT_ObjectEmbed(OxmlBaseElement):
    @property
    def drawAspect(self) -> Optional[ST_ObjectDrawAspect]:
        _val = self.attrib.get(qn('w:drawAspect'))

        if _val is not None:
            return ST_ObjectDrawAspect(_val)
        return None

    @property
    def r_id(self) -> str:
        return self.attrib[qn('r:id')]


    @property
    def progId(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:progId'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def shapeId(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:shapeId'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def fieldCodes(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:fieldCodes'))

        if _val is not None:
            return str(_val)
        return None


class ST_ObjectDrawAspect(ST_BaseEnumType):
    content = 'content'
    icon = 'icon'


class CT_ObjectLink(CT_ObjectEmbed):
    @property
    def updateMode(self) -> ST_ObjectUpdateMode:
        _val = self.attrib[qn('w:updateMode')]

        return ST_ObjectUpdateMode(_val)

    @property
    def lockedField(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:lockedField'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None


class ST_ObjectUpdateMode(ST_BaseEnumType):
    always = 'always'
    onCall = 'onCall'


class CT_Drawing(OxmlBaseElement):
    """17.3.3.9 drawing (DrawingML对象)

    drawing (DrawingML Object)

    该元素指定在运行内容中的此位置有一个DrawingML对象。该DrawingML对象的布局属性使用WordprocessingML Drawing语法（§20.4）来指定。

    [示例：考虑一个运行内容为图片，该图片与段落中的文本在同一行（即，位于行中并影响行高）。该运行将使用以下WordprocessingML指定：

    <w:r>
        <w:drawing>
            <wp:inline>
                …
            </wp:inline>
        </w:drawing>
    </w:r>

    drawing元素指示当前位置的运行中有一个DrawingML对象及其WordprocessingML Drawing定位数据（例如图片或图表）。示例结束]

    <xsd:complexType name="CT_Drawing">
        <xsd:choice minOccurs="1" maxOccurs="unbounded">
            <xsd:element ref="wp:anchor" minOccurs="0"/>
            <xsd:element ref="wp:inline" minOccurs="0"/>
        </xsd:choice>
    </xsd:complexType>
    """

    @property
    def drawing(self):
        """内联或浮动的drawing对象

        - inline: 20.4.2.8 inline (内联DrawingML对象)

            绘图对象与文本一起排列，并影响其所在行的行高和布局（类似于相同大小的字符字形）。

        - anchor: 20.4.2.3 anchor (浮动 DrawingML 对象的锚点)

            浮动 - 绘图对象在文本中锚定，但可以相对于页面进行绝对定位。

        """

        tags = (qn('wp:anchor'), qn('wp:inline'))  # wp_CT_Anchor  # wp_CT_Inline

        ele: wp_CT_Anchor | wp_CT_Inline = self.choice_require_one_child(*tags)  # type: ignore

        return ele


class CT_SimpleField(OxmlBaseElement):
    @property
    def fldData(self) -> Optional[CT_Text]:
        return getattr(self, qn('w:fldData'), None)

    @property
    def p_content(
        self,
    ) -> CT_CustomXmlRun | CT_SmartTagRun | CT_SdtRun | CT_DirContentRun | CT_BdoContentRun | CT_R | CT_ProofErr | CT_PermStart | CT_Perm | CT_RunTrackChange | CT_Bookmark | CT_MarkupRange | CT_MoveBookmark | CT_TrackChange | CT_Markup | CT_SimpleField | CT_Hyperlink | CT_Rel:
        """<xsd:group ref="EG_PContent" minOccurs="0" maxOccurs="unbounded"/>"""

        return self.choice_and_more(*EG_PContent.p_content_choice_tags)  # type: ignore

    @property
    def instr(self) -> str:
        _val = self.attrib[qn('w:instr')]

        return str(_val)

    @property
    def fldLock(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:fldLock'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def dirty(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:dirty'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None


class ST_FldCharType(ST_BaseEnumType):
    begin = 'begin'
    separate = 'separate'
    end = 'end'


class ST_InfoTextType(ST_BaseEnumType):
    text = 'text'
    autoText = 'autoText'


class ST_FFHelpTextVal(str):
    """

    <xsd:simpleType name="ST_FFHelpTextVal">
        <xsd:restriction base="xsd:string">
            <xsd:maxLength value="256"/>
        </xsd:restriction>
    </xsd:simpleType>
    """



class ST_FFStatusTextVal(str):
    """

    <xsd:simpleType name="ST_FFStatusTextVal">
        <xsd:restriction base="xsd:string">
            <xsd:maxLength value="140"/>
        </xsd:restriction>
    </xsd:simpleType>
    """



class ST_FFName(str):
    """

    <xsd:simpleType name="ST_FFName">
        <xsd:restriction base="xsd:string">
            <xsd:maxLength value="65"/>
        </xsd:restriction>
    </xsd:simpleType>
    """



class ST_FFTextType(ST_BaseEnumType):
    regular = 'regular'
    number = 'number'
    date = 'date'
    currentTime = 'currentTime'
    currentDate = 'currentDate'
    calculated = 'calculated'


class CT_FFTextType(OxmlBaseElement):
    @property
    def val_text_type(self) -> ST_FFTextType:
        """
        [有联合类型]
        """
        return ST_FFTextType(str(self.attrib[qn('w:val')]))


class CT_FFName(OxmlBaseElement):
    @property
    def val_ffname(self) -> ST_FFName:
        """[有联合]"""

        return ST_FFName(str(self.attrib[qn('w:val')]))


class CT_FldChar(OxmlBaseElement):
    @property
    def char(self) -> Optional[CT_Text | CT_FFData | CT_TrackChangeNumbering]:
        tags = (
            qn('w:fldData'),  # CT_Text
            qn('w:ffData'),  # CT_FFData
            qn('w:numberingChange'),  # CT_TrackChangeNumbering
        )

        return self.choice_one_child(*tags)  # type: ignore

    @property
    def fldCharType(self) -> ST_FldCharType:
        _val = self.attrib[qn('w:fldCharType')]

        return ST_FldCharType(_val)

    @property
    def fldLock(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:fldLock'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def dirty(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:dirty'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None


class CT_FFData(OxmlBaseElement):
    """

    <xsd:complexType name="CT_FFData">
        <xsd:choice maxOccurs="unbounded">
            <xsd:element name="name" type="CT_FFName"/>
            <xsd:element name="label" type="CT_DecimalNumber" minOccurs="0"/>
            <xsd:element name="tabIndex" type="CT_UnsignedDecimalNumber" minOccurs="0"/>
            <xsd:element name="enabled" type="CT_OnOff"/>
            <xsd:element name="calcOnExit" type="CT_OnOff"/>
            <xsd:element name="entryMacro" type="CT_MacroName" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="exitMacro" type="CT_MacroName" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="helpText" type="CT_FFHelpText" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="statusText" type="CT_FFStatusText" minOccurs="0" maxOccurs="1"/>
            <xsd:choice>
                <xsd:element name="checkBox" type="CT_FFCheckBox"/>
                <xsd:element name="ddList" type="CT_FFDDList"/>
                <xsd:element name="textInput" type="CT_FFTextInput"/>
            </xsd:choice>
        </xsd:choice>
    </xsd:complexType>
    """

    @property
    def data(
        self,
    ) -> list[
        CT_FFName | CT_DecimalNumber | CT_UnsignedDecimalNumber | CT_OnOff | CT_MacroName | CT_FFHelpText | CT_FFStatusText | CT_FFCheckBox | CT_FFDDList | CT_FFTextInput
    ]:
        tags = (
            qn('w:name'),  # CT_FFName
            qn('w:label'),  # CT_DecimalNumber
            qn('w:tabIndex'),  # CT_UnsignedDecimalNumber
            qn('w:enabled'),  # CT_OnOff
            qn('w:calcOnExit'),  # CT_OnOff
            qn('w:entryMacro'),  # CT_MacroName
            qn('w:exitMacro'),  # CT_MacroName
            qn('w:helpText'),  # CT_FFHelpText
            qn('w:statusText'),  # CT_FFStatusText
            qn('w:checkBox'),  # CT_FFCheckBox
            qn('w:ddList'),  # CT_FFDDList
            qn('w:textInput'),  # CT_FFTextInput
        )

        return self.choice_and_more(*tags)  # type: ignore


class CT_FFHelpText(OxmlBaseElement):
    @property
    def type(self) -> Optional[ST_InfoTextType]:
        _val = self.attrib.get(qn('w:type'))

        if _val is not None:
            return ST_InfoTextType(_val)
        return None

    @property
    def val(self) -> Optional[ST_FFHelpTextVal]:
        _val = self.attrib.get(qn('w:val'))

        if _val is not None:
            return ST_FFHelpTextVal(_val)
        return None


class CT_FFStatusText(OxmlBaseElement):
    @property
    def type(self) -> Optional[ST_InfoTextType]:
        _val = self.attrib.get(qn('w:type'))

        if _val is not None:
            return ST_InfoTextType(_val)
        return None

    @property
    def val(self) -> Optional[ST_FFHelpTextVal]:
        _val = self.attrib.get(qn('w:val'))

        if _val is not None:
            return ST_FFHelpTextVal(_val)
        return None


class CT_FFCheckBox(OxmlBaseElement):
    @property
    def size(self) -> list[CT_HpsMeasure | CT_OnOff]:
        tags = (
            qn('w:size'),  # CT_HpsMeasure
            qn('w:sizeAuto'),  # CT_OnOff
        )

        return self.choice_and_more(*tags)  # type: ignore

    @property
    def default(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:default'), None)

    @property
    def checked(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:checked'), None)


class CT_FFDDList(OxmlBaseElement):
    @property
    def result(self) -> Optional[CT_DecimalNumber]:
        return getattr(self, qn('w:result'), None)

    @property
    def default(self) -> Optional[CT_DecimalNumber]:
        return getattr(self, qn('w:default'), None)

    @property
    def listEntry(self) -> list[CT_String]:
        return self.findall(qn('w:listEntry'))  # type: ignore


class CT_FFTextInput(OxmlBaseElement):
    @property
    def type(self) -> Optional[ST_InfoTextType]:
        _val = self.attrib.get(qn('w:type'))

        if _val is not None:
            return ST_InfoTextType(_val)
        return None

    @property
    def default(self) -> Optional[CT_String]:
        return getattr(self, qn('w:default'), None)

    @property
    def maxLength(self) -> Optional[CT_DecimalNumber]:
        return getattr(self, qn('w:maxLength'), None)

    @property
    def format(self) -> Optional[CT_String]:
        return getattr(self, qn('w:format'), None)


class ST_SectionMark(ST_BaseEnumType):
    nextPage = 'nextPage'
    nextColumn = 'nextColumn'
    continuous = 'continuous'
    evenPage = 'evenPage'
    oddPage = 'oddPage'


class CT_SectType(OxmlBaseElement):
    @property
    def val_sect_type(self) -> Optional[ST_SectionMark]:
        """
        [有联合类型]
        """
        _val = self.attrib.get(qn('w:val'))

        if _val is not None:
            return ST_SectionMark(_val)
        return None


class CT_PaperSource(OxmlBaseElement):
    @property
    def first(self) -> Optional[ST_DecimalNumber]:
        _val = self.attrib.get(qn('w:first'))

        if _val is not None:
            return ST_DecimalNumber(_val)
        return None

    @property
    def other(self) -> Optional[ST_DecimalNumber]:
        _val = self.attrib.get(qn('w:other'))

        if _val is not None:
            return ST_DecimalNumber(_val)
        return None


class ST_NumberFormat(ST_BaseEnumType):
    """17.18.59 ST_NumberFormat (编号格式)¶

    ST_NumberFormat (Numbering Format)

    这个简单类型指定了一组自动编号对象所使用的编号格式。

    [示例：页码编号为 lowerLetter 表示消费者必须在此节的每一页使用小写字母：a，b，c… 示例结束]

    这个简单类型的内容是对 W3C XML Schema 字符串数据类型的限制。
    """

    decimal = 'decimal'
    """十进制数

    指定序列将由十进制编号组成。

    要确定任何值的显示文本，此序列指定一组字符，表示位置 1–9，然后这些相同的字符与彼此和 0（表示数字零）组合以构建剩余的值。

    此编号格式用于值 0–9 的字符集为 U+0030–U+0039。通过以下步骤继续序列：

    - 增加最右边的位置。
    - 每当达到集合的末尾时，对于给定位置，递增到左边的位置（如果没有左边的位置，则创建一个新位置，并从 1 开始新位置的序列），并将当前位置重置为 0。

    [示例：项目的编号应由以下模式表示：1, 2, 3, …, 8, 9, 10, 11, 12, …, 18, 19, 20, 21, … 示例结束]
    """

    upperRoman = 'upperRoman'
    """大写罗马数字

    指定序列应由大写罗马数字组成。

    该系统使用一组字符来表示数字1, 5, 10, 50, 100, 500 和 1000，然后这些字符与彼此结合以构建剩余的值。

    此编号格式使用的字符集为 U+0049, U+0056, U+0058, U+004C, U+0043, U+0044, U+004D。

    要构建超出集合范围的数字，您从最大的组开始，按照以下步骤操作：

    - 创建尽可能多的包含一千的组。

        表示一千的符号（该位置所代表的十的幂）：M重复相应组的次数。

        如果没有形成组，请不写任何符号。

    - 对九百（CM）、五百（D）、四百（CD）、一百（C）、九十（XC）、五十（L）、四十（XL）、十（X）、九（IX）、五（V）、四（IV）和最后一（I）的组重复此操作，使用相应的符号表示组（例如，四百五十将是CDL，四十五将是XLV）。

    [示例：项目的编号应按照以下模式表示：I, II, III, IV, …, XVIII, XIX, XX, XXI, … 结束示例]
    """

    lowerRoman = 'lowerRoman'
    """小写罗马数字

    指定序列应由小写罗马数字组成。

    此系统使用一组字符来表示数字 1、5、10、50、100、500 和 1000，然后这些字符彼此组合以构建其余的值。

    此编号格式使用的字符集为 U+0069, U+0076, U+0078, U+006C, U+0063, U+0064, U+006D。

    要构建超出集合范围的数字，您需要从最大的组开始，依次进行以下步骤：

    - 创建尽可能多的包含每个组中的一千的组。

        表示一千的符号（该位置表示的十的幂）：m 被重复为形成的组数。

        如果未形成任何组，则不写入任何符号。

    - 重复此过程，使用相应的符号表示九百（cm）、五百（d）、四百（cd）、一百（c）、九十（xc）、五十（l）、四十（xl）、十（x）、九（ix）、五（v）、四（iv）和最后一个（i）来指示组（因此，四百五十将是 cdl，四十五将是 xlv）。

    [示例：项目的编号应按照以下模式表示：i, ii, iii, iv, …, xviii, xix, xx, xxi, … 结束示例]
    """

    upperLetter = 'upperLetter'
    """大写拉丁字母

    指定序列应由大写拉丁字母集合中的一个或多个字符组成。

    该系统使用一组字符来表示拉丁字母表语言长度范围内的数字1到最大值，然后将这些相同字符结合在一起以构建剩余值。

    此编号格式由 lang 元素（§17.3.2.20）的语言确定。具体如下：

    - 当使用的脚本源自拉丁字母表（A–Z）时，使用该字母表。

        [示例：对于挪威语（新挪威语），此编号格式使用以下Unicode字符：U+0041–U+005A, U+00C6, U+00D8, U+00C5。结束示例]

    - 当使用的语言基于其他系统时，使用字符 U+0041–U+005A。

    对于超出集合范围的值，数字的构建遵循以下步骤：

    - 重复从值中减去集合大小的步骤，直到结果等于或小于集合的大小。
    - 结果值确定要使用的字符，并且相同的字符写入一次，然后为从原始值中减去集合大小的每次重复。

    [示例：对于英语，项目的编号应按照以下模式表示：A, B, C, …, Y, Z, AA, BB, CC, …, YY, ZZ, AAA, BBB, CCC, … 结束示例]
    """

    lowerLetter = 'lowerLetter'
    """小写拉丁字母

    指定序列应由小写拉丁字母集合中的一个或多个字母的单个出现组成。

    此系统使用一组字符来表示数字 1 到字母表语言的长度，然后这些相同的字符被组合以构建其余的值。

    此编号格式使用的字符通过使用 lang 元素 (§17.3.2.20) 的语言确定。具体来说：

    - 当使用的脚本源自拉丁字母表（a-z）时，将使用该字母表。

        [示例：对于挪威语（尼诺斯克），此编号格式使用以下 Unicode 字符：U+0061–U+007A, U+00E6, U+00F8, U+00E5。 结束示例]

    - 当使用的语言基于任何其他系统时，将使用字符 U+0061–U+007A。

    对于大于字符集大小的值，通过执行以下步骤构建数字：

    - 反复从值中减去字符集的大小，直到结果等于或小于字符集的大小。
    - 结果值确定要使用的字符，然后相同的字符被写入一次，然后为从原始值中减去字符集大小的次数重复。

    [示例：对于英语，项目的编号应按照以下模式表示：a, b, c, …, y, z, aa, bb, cc, …, yy, zz, aaa, bbb, ccc, … 结束示例]
    """

    ordinal = 'ordinal'
    """序数

    指定序列应由运行语言的序数组成。

    此序列是一组字符串，其中每个字符串都是 lang 元素（§17.3.2.20）中的语言的文本表示中的不同唯一位置的序数。

    [示例：法语中项目的编号应按照以下模式表示：1er, 2e, 3e, …, 9e, 10e, 11e, … 19e, 20e, 21e, … 结束示例]
    """

    cardinalText = 'cardinalText'
    """基数文本

    指定序列将由运行语言的基数文本组成。

    此序列是一组字符串，其中每个字符串都是 lang 元素（§17.3.2.20）中语言的文本表示形式中的不同唯一位置的文本表示。

    [示例：西班牙语中项目的编号应由以下模式表示：Uno、Dos、Tres、…、Nueve、Diez、Once、…、Diecinueve、Veinte、Veintiuno、… 示例结束]
    """

    ordinalText = 'ordinalText'
    """序数文本

    指定序列应由运行语言的序数文本组成。

    此序列是一组字符串，其中每个字符串都是 lang 元素（§17.3.2.20）中的语言的文本表示中的不同唯一位置的序数。

    [示例：德语中项目的编号应按照以下模式表示：Erste, Zweite, Dritte, …, Neunte, Zehnte, Elfte, …, Neunzehnte, Zwanzigste, Einundzwanzigste, … 结束示例]
    """

    hex = 'hex'
    """十六进制编号

    指定序列应由十六进制编号组成。

    为确定任何值所显示的文本，此序列指定一组字符，表示位置 1 到 15，然后这些相同字符与 0（表示数字零）结合以构建其余值。

    此编号格式用于值 0 到 15 的字符集为 U+0030 到 U+0039，以及 U+0041 到 U+0046。

    对于大于字符集大小的值，按照以下步骤构建数字：

    - 将值除以 16，并写入表示余数的符号。
    - 将前一次除法的商除以 16，并将表示余数的符号写入现有位置的左侧。
    - 重复步骤 2，直到剩余值等于零。

    [示例：项目的编号应按照以下模式表示：1, 2, 3, …, E, F, 10,11, 12, …, 1E, 1F, 20, 21, … 结束示例]
    """

    chicago = 'chicago'
    """芝加哥风格手册

    指定序列将由下面列出的字符集中的一个或多个字符组成。

    要确定任何值的显示文本，此序列指定一组表示位置 1–4 的字符，然后使用下面定义的逻辑重复这些相同的字符以构造所有其他值。

    该编号格式在值 1–4 的字符集是分别为 U+002A、U+2020、U+2021 和 U+00A7。

    对于大于 4 的值，显示的文本将按以下方式构造：

    - 反复从值中减去集合的大小（4），直到结果等于或小于集合的大小。
    - 余数确定要从上面集合中使用的字符，该字符写一次，然后写一次，然后写一次，并且重复集合大小从原始值中减去的次数。

    [示例：此格式中的前九个项目为：、†、‡、§、、††、‡‡、§§、** 示例结束]
    """

    ideographDigital = 'ideographDigital'
    """象形数字

    指定序列应由连续的数字象形组成，使用适当的字符，如下所述。

    为确定任何值所显示的文本，此序列指定一组字符，表示位置 1 到 9，然后使用这些相同字符与彼此结合以及 〇（表示数字零）来构建其余值。

    此编号格式用于值 0 到 9 的字符集为 U+3007, U+4E00, U+4E8C, U+4E09, U+56DB, U+4E94, U+516D, U+4E03, U+516B, 和 U+4E5D。

    对于大于字符集大小的值，按照以下步骤构建数字：

    - 将值除以 10，并写入表示余数的符号。
    - 将前一次除法的商除以 10，并将表示余数的符号写入现有位置的左侧。
    - 重复步骤 2，直到剩余值等于零。

    [示例：项目的编号应按照以下模式表示：一, 二, 三, …, 八 , 九, 一〇, 一一, 一二, …, 一八, 一九, 二〇, 二一, … 结束示例]
    """

    japaneseCounting = 'japaneseCounting'
    """日语计数系统

    指定序列应包含日语计数系统的顺序数字。

    此系统使用一组字符来表示数字 1–9，然后将它们与其他字符组合以表示相应的十的幂。

    此编号格式用于的字符集为 U+3007, U+4E00, U+4E8C, U+4E09, U+56DB, U+4E94, U+516D, U+4E03, U+516B 和 U+4E5D。

    要构建小于一万的数字，您按照从最大到最小的顺序进行操作，执行以下步骤：

    ...
    """

    aiueo = 'aiueo'
    """AIUEO 顺序半角片假名

    指定序列将由单个半角片假名字符的一个或多个重复出现组成，按传统的 a-i-u-e-o 顺序列出。

    要确定任何值的显示文本，此序列指定一组表示位置 1–46 的字符，然后使用下面定义的逻辑重复这些相同的字符以构造所有其他值。

    该编号格式在值 1–46 的字符集是分别为 U+FF71–U+FF9C、U+FF66 和 U+FF9D。

    对于大于 46 的值，序列重新开始，通过相同的 46 个值进行迭代，根据需要重复此模式。

    [示例：这些项目的编号应由以下模式表示：ｱ，ｲ，ｳ，…，ｦ，ﾝ，ｱ ｱ，ｲｲ，ｳｳ，… 示例结束]
    """

    iroha = 'iroha'
    """いろは順カタカナ

    指定序列应包含いろは。

    要确定任何值显示的文本，此序列指定一组字符，表示位置 1–48，然后使用以下逻辑重复这些相同的字符以构建所有其他值。

    此编号格式用于值 1–48 的字符集为 U+FF72, U+FF9B, U+FF8A, U+FF86, U+FF8E, U+FF8D, U+FF84, U+FF81, U+FF98, U+FF87, U+FF99, U+FF66, U+FF9C, U+FF76, U+FF96, U+FF80, U+FF9A, U+FF7F, U+FF82, U+FF88, U+FF85, U+FF97, U+FF91, U+FF73, U+30F0, U+FF89, U+FF75, U+FF78, U+FF94, U+FF8F, U+FF79, U+FF8C, U+FF7A, U+FF74, U+FF83, U+FF71, U+FF7B, U+FF77, U+FF95, U+FF92, U+FF90, U+FF7C, U+30F1, U+FF8B, U+FF93, U+FF7E, U+FF7D 和 U+FF9D。

    对于大于字符集大小的值，按照以下步骤构建数字：

    - 重复地从值中减去字符集大小（48），直到结果等于或小于字符集大小。
    - 结果值确定要使用的字符。

    [示例：项目的编号应按照以下模式表示：ｲ, ﾛ, ﾊ, …, ｽ, ﾝ, ｲ, ﾛ, ﾊ, … 结束示例]
    """

    decimalFullWidth = 'decimalFullWidth'
    """全角阿拉伯数字

    指定序列将由全角阿拉伯数字组成。

    为了确定任何值的显示文本，该序列指定了一组字符，表示位置 1–9，然后这些相同的字符与彼此以及０（表示数字零）结合，以构建其余的值。

    此编号格式用于值 0–9 的字符集分别为 U+FF10–U+FF19。

    对于大于集合大小的值，数字将按照以下步骤构建：

    - 将值除以 10，并写下代表余数的符号。
    - 将上一次除法的商除以 10，并将代表余数的符号写在现有位置的左侧。
    - 重复步骤 2，直到剩余值等于零。

    [示例：项目的编号应由以下模式表示：１, ２, ３, …, ８, ９, １０, １１, １２, …, １８, １９, ２０, ２１, … 示例结束]
    """

    decimalHalfWidth = 'decimalHalfWidth'
    """半角阿拉伯数字

    指定序列将由半角阿拉伯数字组成。

    为了确定任何值的显示文本，该序列指定了一组字符，表示位置 1–9，然后这些相同的字符与彼此以及 0（表示数字零）结合，以构建其余的值。

    此编号格式用于值 0–9 的字符集分别为 U+0030–U+0039。

    对于大于集合大小的值，数字将按照以下步骤构建：

    - 将值除以 10，并写下代表余数的符号。
    - 将上一次除法的商除以 10，并将代表余数的符号写在现有位置的左侧。
    - 重复步骤 2，直到剩余值等于零。

    [示例：项目的编号应由以下模式表示：1, 2, 3, …, 8, 9, 10, 11, 12, …, 18, 19, 20, 21, … 示例结束]
    """

    japaneseLegal = 'japaneseLegal'
    """日本法定编号

    指定序列应包含日本法定计数系统的顺序数字。

    此系统使用一组字符来表示数字 1–9，然后将它们与其他字符组合以表示相应的十的幂。

    此编号格式用于值的字符集为 U+58F1, U+5F10, U+53C2, U+56DB, U+4F0D, U+516D, U+4E03, U+516B, U+4E5D, U+62FE, U+767E, U+842C 和 U+9621。

    要构建小于十万的数字，您按照从最大到最小的顺序进行操作，执行以下步骤：

    ...
    """

    japaneseDigitalTenThousand = 'japaneseDigitalTenThousand'
    """日语数字万计数系统

    指定序列应包含日语数字万计数系统的顺序数字。

    要确定任何值显示的文本，此序列指定一组字符，表示位置 1–9，然后这些相同的字符与彼此组合，并与 〇（表示零）一起构建其余值。

    此编号格式用于值 0–9 的字符集为 U+3007, U+4E00, U+4E8C, U+4E09, U+56DB, U+4E94, U+516D, U+4E03, U+516B 和 U+4E5D。

    对于大于字符集大小的值，按照以下步骤构建数字：

    - 将值除以 10 并写下表示余数的符号。
    - 将上一次除法的商除以 10，并将表示余数的符号写在现有位置的左侧。
    - 重复步骤 2，直到剩余值等于零。

    [示例：项目的编号应按照以下模式表示：一, 二, 三, …, 八 , 九, 一〇, 一一, 一二, …, 一八, 一九, 二〇, 二一, … 结束示例]
    """

    decimalEnclosedCircle = 'decimalEnclosedCircle'
    """带圆圈的十进制数

    定序列将由带圆圈的十进制编号组成，使用封闭字符。

    该系统使用一组字符表示数字 1–20。

    此编号格式用于值 1–20 的字符集分别为 U+2460–U+2473。

    对于大于集合大小的值，项目将回退到十进制格式。

    [示例：项目的编号应由以下模式表示：①, ②, ③, …, ⑲, ⑳, 21, … 示例结束]
    """

    decimalFullWidth2 = 'decimalFullWidth2'
    """aaaa
    """

    aiueoFullWidth = 'aiueoFullWidth'
    """AIUEO 顺序全角片假名

    指定序列将由单个全角片假名字符的一个或多个重复出现组成，按传统的 a-i-u-e-o 顺序列出。

    要确定任何值的显示文本，此序列指定一组表示位置 1–46 的字符，然后使用下面定义的逻辑重复这些相同的字符以构造所有其他值。

    ...
    """

    irohaFullWidth = 'irohaFullWidth'
    """全角いろは顺カタカナ

    指定序列应包含全角形式的いろは。

    要确定任何值显示的文本，此序列指定一组字符，表示位置 1–48，然后使用以下逻辑重复这些相同的字符以构建所有其他值。

    此编号格式用于值 1–48 的字符集为 U+30A4, U+30ED, U+30CF, U+30CB, U+30DB, U+30D8, U+30C8, U+30C1, U+30EA, U+30CC, U+30EB, U+30F2, U+30EF, U+30AB, U+30E8, U+30BF, U+30EC, U+30BD, U+30C4, U+30CD, U+30CA, U+30E9, U+30E0, U+30A6, U+30F0, U+30CE, U+30AA, U+30AF, U+30E4, U+30DE, U+30B1, U+30D5, U+30B3, U+30A8, U+30C6, U+30A2, U+30B5, U+30AD, U+30E6, U+30E1, U+30DF, U+30B7, U+30F1, U+30D2, U+30E2, U+30BB, U+30B9 和 U+30F3。

    对于大于字符集大小的值，按照以下步骤构建数字：

    - 重复地从值中减去字符集大小（48），直到结果等于或小于字符集大小。
    - 结果值确定要使用的字符。

    [示例：项目的编号应按照以下模式表示：イ, ロ, ハ, …, ス, ン, イ, ロ, ハ, … 结束示例]
    """

    decimalZero = 'decimalZero'
    """带零的阿拉伯数字

    指定序列将由阿拉伯数字加零构成，数字为 1 到 9。

    为了确定任何值的显示文本，该序列指定了一组配对字符（零后跟额外的符号），表示位置 1–9，然后这些相同的字符与彼此结合，以构建其余的值。

    此编号格式用于值 0–9 的字符集分别为 U+0030–U+0039。

    对于大于集合大小的值，数字将按照以下步骤构建：

    - 将值除以 10，并写下代表余数的符号。
    - 将上一次除法的商除以 10，并将代表余数的符号写在现有位置的左侧。
    - 重复步骤 2，直到剩余值等于零。

    [示例：项目的编号应由以下模式表示：01, 02, 03, …, 08, 09, 10, 11, 12, …, 18, 19, 20, 21, 22, …, 98, 99, 100, 101, … 示例结束]
    """

    bullet = 'bullet'
    """项目符号

    指定序列将由级别文本元素（§17.9.11）定义的项目符号字符组成。

    [示例：● 示例结束]
    """

    ganada = 'ganada'
    """韩文甲骨文编号

    指定序列将由韩文甲骨文格式中的单个顺序数字的一个或多个出现组成，从下面列出的集合中选择。

    为了确定任何值的显示文本，该序列指定了一组字符，表示位置 1–14，然后使用下面定义的逻辑重复这些相同的字符，以构建所有其他值。

    此编号格式用于值 1–14 的字符集分别为 U+AC00, U+B098, U+B2E4, U+B77C, U+B9C8, U+BC14, U+C0AC, U+C544, U+C790, U+CC28, U+CE74, U+D0C0, U+D30C, 和 U+D558。

    对于大于 14 的值，显示的文本将按照以下方式构建：

    - 反复从值中减去集合的大小（14），直到结果等于或小于集合的大小。
    - 余数确定要使用上述集合中的哪个字符，并将该字符序列重复多次，等于将集合的大小从原始值中减去的次数。

    [示例：项目的编号应由以下模式表示：가, 나, 다, …, 파, 하, 가가, 나나, 다다, … 示例结束]
    """

    chosung = 'chosung'
    """韩文拼音编号

    ...
    """

    decimalEnclosedFullstop = 'decimalEnclosedFullstop'
    """带句点的十进制数

    指定序列将由十进制编号后跟句点组成，使用适当的字符，如下所述。

    该系统使用一组字符表示数字 1–20。

    此编号格式用于值 1–20 的字符集分别为 U+2488–U+249B。

    对于大于集合大小的值，项目将回退到十进制格式。

    [示例：项目的编号应由以下模式表示：⒈, ⒉, ⒊, …, ⒚, ⒛, 21, … 示例结束]
    """

    decimalEnclosedParen = 'decimalEnclosedParen'
    """带括号的十进制数

    指定序列将由带括号的十进制编号组成，使用适当的字符，如下所述。

    该系统使用一组字符表示数字 1–20。

    此编号格式用于值 1–20 的字符集分别为 U+2474–U+2487。

    对于大于集合大小的值，项目将回退到十进制格式。

    [示例：项目的编号应由以下模式表示：⑴, ⑵, ⑶, …, ⒆, ⒇, 21, 22, … 示例结束]
    """

    decimalEnclosedCircleChinese = 'decimalEnclosedCircleChinese'
    """带圆圈的十进制数

    与 decimalEnclosedCircle 相同。
    """

    ideographEnclosedCircle = 'ideographEnclosedCircle'
    """圆圈内的象形数字

    指定序列应由连续的数字象形组成，使用适当的字符，如下所述。

    为确定任何值所显示的文本，此序列指定一组字符，表示位置 1 到 10。

    此编号格式用于值 1 到 10 的字符集为 U+3220 到 U+3229。

    对于大于字符集大小的值，项目将退回到十进制格式。

    [示例：项目的编号应按照以下模式表示：㈠, ㈡, ㈢, …, ㈨, ㈩, 11,12, … 结束示例]
    """

    ideographTraditional = 'ideographTraditional'
    """传统象形数字格式

    指定序列应由连续的传统象形数字组成。

    此系统使用一组字符（中国干支纪年中的元素）来表示 1–10。对于大于字符集大小的值，项目将退回到十进制格式。

    此编号格式用于值 1–10 的字符集为 U+7532, U+4E59, U+4E19, U+4E01, U+620A, U+5DF1, U+5E9A, U+8F9B, U+58EC 和 U+7678。

    [示例：项目的编号应按照以下模式表示：甲, 乙, 丙, 丁, …, 壬, 癸, 11, 12, … 结束示例]


    """

    ideographZodiac = 'ideographZodiac'
    """生肖象形数字格式

    指定序列应由连续的生肖象形数字组成。

    此系统使用一组字符（中国干支纪年中的动物）来表示 1–12。对于大于字符集大小的值，项目将退回到十进制格式。

    此编号格式用于值 1–12 的字符集为 U+5B50, U+4E11, U+5BC5, U+536F, U+8FB0, U+5DF3, U+5348, U+672A, U+7533, U+9149, U+620C 和 U+4EA5。

    [示例：项目的编号应按照以下模式表示：子, 丑, 寅, …, 戌 , 亥, 13, 14, … 结束示例]
    """

    ideographZodiacTraditional = 'ideographZodiacTraditional'
    """传统生肖象形数字格式

    指定序列应由连续的传统生肖象形数字组成。

    此系统使用一组字符对（中国干支纪年的所有元素-动物组合）来表示 1–60，然后重复这些相同的字符对以构建其余值。

    此编号格式用于值 1–60 的字符对集为 U+7532, U+5B50; U+4E59, U+4E11; U+4E19, U+5BC5; U+4E01, U+536F; U+620A, U+8FB0; U+5DF1, U+5DF3; U+5E9A, U+5348; U+8F9B, U+672A; U+58EC, U+7533; U+7678, U+9149; U+7532, U+620D; U+4E59, U+4EA5; U+4E19, U+5B50; U+4E01, U+4E11; U+620A, U+5BC5; U+5DF1, U+536F; U+5E9A, U+8FB0; U+8F9B, U+5DF3; U+58EC, U+5348; U+7678, U+672A; U+7532, U+7533; U+4E59, U+9149; U+4E19, U+620D; U+4E01, U+4EA5; U+620A, U+5B50; U+5DF1, U+4E11; U+5E9A, U+5BC5; U+8F9B, U+536F; U+58EC, U+8FB0; U+7678, U+5DF3; U+7532, U+5348; U+4E59, U+672A; U+4E19, U+7533; U+4E01, U+9149; U+620A, U+620D; U+5DF1, U+4EA5; U+5E9A, U+5B50; U+8F9B, U+4E11; U+58EC, U+5BC5; U+7678, U+536F; U+7532, U+8FB0; U+4E59, U+5DF3; U+4E19, U+5348; U+4E01, U+672A; U+620A, U+7533; U+5DF1, U+9149; U+5E9A, U+620D; U+8F9B, U+4EA5; U+58EC, U+5B50; U+7678, U+4E11; U+7532, U+5BC5; U+4E59, U+536F; U+4E19, U+8FB0; U+4E01, U+5DF3; U+620A, U+5348; U+5DF1, U+672A; U+5E9A, U+7533; U+8F9B, U+9149; U+58EC, U+620D; U+7678, U+4EA5。

    对于大于字符集大小的值，按照以下步骤构建数字：

    - 重复地从值中减去字符集大小（60），直到结果等于或小于字符集大小。
    - 结果值确定要使用的字符对。

    [示例：项目的编号应按照以下模式表示：甲子, 乙丑, 丙寅, …, 壬戌, 癸亥, 甲子, 乙丑, 丙寅, … 结束示例]
    """

    taiwaneseCounting = 'taiwaneseCounting'
    """台湾计数系统

    指定序列应由台湾计数系统的连续数字组成。

    为了确定任何值所显示的文本，此序列指定了一组字符，表示位置1–9，然后这些相同的字符彼此组合，并与○（U+25CB，表示数字零）一起构建其余的值。

    此编号格式用于值1–10的字符集是 U+4E00, U+4E8C, U+4E09, U+56DB, U+4E94, U+516D, U+4E03, U+516B, U+4E5D 和 U+5341。

    对于大于集合大小的值，通过执行以下步骤构建数字：

    - 将值除以10，并写下表示余数的符号。

        如果商小于10，则将 十 写在表示余数的符号的左侧。

    - 将前一次除法的商除以10，并将表示余数的符号写在现有位置的左侧。
    - 重复步骤2，直到剩余值等于零。

    [示例：项目的编号应按照以下模式表示：一, 二, 三, …, 九 , 十, 十一, 十二, …, 十九, 二十, 二十一, …, 九十九, 一 ○○, 一○一, … 结束示例]
    """

    ideographLegalTraditional = 'ideographLegalTraditional'
    """传统法律象形数字格式

    指定序列应由连续的传统法律象形数字组成。

    此系统使用一组字符来表示 1–9，并将其与其他字符组合以表示相应的十的幂。

    此编号格式用于值 1–9 的字符集为 U+58F9, U+8CB3, U+53C3, U+8086, U+4F0D, U+9678, U+67D2, U+634C, U+7396, U+62FE, U+4F70, U+4EDF 和 U+842C。

    要构建小于十万的数字，您按照从大到小的顺序从最大的组到最小的组进行以下步骤：

    ...
    """

    taiwaneseCountingThousand = 'taiwaneseCountingThousand'
    """台湾计数千位系统

    指定序列应由台湾计数千位系统的连续数字组成。

    此系统使用一组字符表示数字1–10，然后将其与附加字符组合以构建其余的字符。

    此编号格式用于值1–10的字符集是 U+4E00, U+4E8C, U+4E09, U+56DB, U+4E94, U+516D, U+4E03, U+516B, U+4E5D, U+842C, U+5343, U+5341, U+767E 和 U+96F6。

    对于超出集合范围但小于十万的数字，您从最大的组到最小的组依次进行以下步骤：

    ...
    """

    taiwaneseDigital = 'taiwaneseDigital'
    """台湾数字计数系统

    指定序列应由台湾数字计数系统的连续数字组成。

    为确定任何值所显示的文本，此序列指定一组字符，表示位置1–9，然后将这些相同字符结合在一起，并使用 ○（表示数字零）构建剩余值。

    此编号格式用于值0–9的字符集是 U+25CB, U+4E00, U+4E8C, U+4E09, U+56DB, U+4E94, U+516D, U+4E03, U+516B 和 U+4E5D。

    对于超出集合范围的值，数字的构建遵循以下步骤：

    - 将值除以10，并写下表示余数的符号。
    - 将上一次除法的商除以10，并将表示余数的符号写在现有位置的左侧。
    - 重复步骤2，直到剩余值等于零。

    [示例：项目的编号应按照以下模式表示：一, 二, …, 八, 九 , 一○,一一, 一二, …, 一八, 一九, 二○, 二一, … 结束示例]


    """

    chineseCounting = 'chineseCounting'
    """中文计数系统

    指定序列将由中文计数系统中的一个或多个递增数字组成，从下面列出的集合中选择。

    要确定任何值的显示文本，此序列指定一组表示位置 1–10 的字符，然后使用下面定义的逻辑重复这些相同的字符以构造所有其他值。〇代表数字零。

    该编号格式在值 0–10 的字符集是分别为 U+25CB、U+4E00、U+4E8C、U+4E09、U+56DB、U+4E94、U+516D、U+4E03、U+516B、U+4E5D 和 U+5341。

    对于大于 10 的值，显示的文本将按以下方式构造：

    - 将值除以 10，并写下表示余数的符号。如果商小于 10，则在符号的左侧写上代表余数的符号十。
    - 将上一次除法的商除以 10，并将表示余数的符号写在现有字符的左侧。
    - 重复步骤 2，直到剩余值等于零。

    [示例：项目的编号应由以下模式表示：一、二、三、…、九、十、十一、十二、…、十九、二十、二十一、…、九十九、一〇〇、一〇一、… 示例结束]
    """

    chineseLegalSimplified = 'chineseLegalSimplified'
    """简化版中文法律格式

    指定序列将由简化版中文法律格式中的一个或多个递增数字组成，从下面列出的集合中选择。

    要确定任何值的显示文本，此序列指定一组字符，表示位置 1–9，然后将其与额外的字符组合，以表示相应的十的幂次。

    该编号格式使用的字符集是 U+96F6、U+58F9、U+8D30、U+53C1、U+8086、U+4F0D、U+9646、U+67D2、U+634C 和 U+7396。

    要构建一个小于十万的数字，请按照从最大组到最小组的顺序执行以下步骤：

    ...
    """

    chineseCountingThousand = 'chineseCountingThousand'
    """中文计数千进制

    指定序列将由中文计数千进制系统中的一个或多个递增数字组成，从下面列出的集合中选择。

    要确定任何值的显示文本，此序列指定一组表示位置 1–10、100、1,000 和 10,000 的字符，然后使用下面定义的逻辑重复这些相同的字符以构造所有其他值。

    该编号格式使用的字符集是 U+96F6、U+4E00、U+4E8C、U+4E09、U+56DB、U+4E94、U+516D、U+4E03、U+516B、U+4E5D、U+5341、U+767E、U+5343 和 U+4E07。

    要构建一个超出集合但小于十万的值，请按照以下步骤从最大的组开始依次减少：

    ...
    """

    koreanDigital = 'koreanDigital'
    """韩国数字计数系统

    ...
    """

    koreanCounting = 'koreanCounting'
    """韩国计数系统

    ...
    """

    koreanLegal = 'koreanLegal'
    """韩国法定编号

    ...
    """

    koreanDigital2 = 'koreanDigital2'
    """韩国数字计数系统替代

    ...
    """

    vietnameseCounting = 'vietnameseCounting'
    """越南数字

    指定序列应由越南数字组成。

    此序列是一组字符串，其中每个字符串都是该序列中下一个值的全名，用越南语表示。

    [示例：một, hai, ba, bốn, năm, sáu, bảy, tám, chín, mười。结束示例]
    """

    russianLower = 'russianLower'
    """小写俄文字母

    ...
    """

    russianUpper = 'russianUpper'
    """大写俄文字母

    ...
    """

    none = 'none'
    """无编号

    指定序列不显示任何编号。
    """

    numberInDash = 'numberInDash'
    """带破折号的数字

    指定序列应由用连字符（U+002D）包围的阿拉伯数字组成。

    为了确定任何值所显示的文本，此序列指定了一组字符，表示位置1–9，然后这些相同的字符彼此组合，并与0（U+0030，表示数字零）一起构建其余的值。

    此编号格式使用的字符集是 U+002D (-) 和，对于值1–9，分别是 U+0031–U+0039。

    对于大于集合大小的值，通过执行以下步骤构建数字：

    - 将值除以10，并写下表示余数的符号。
    - 将前一次除法的商除以10，并将表示余数的符号写在现有位置的左侧。
    - 重复步骤2，直到剩余值等于零。
    - 将最终数字放置在两个破折号之间。

    [示例：项目的编号应按照以下模式表示：- 1 -,- 2 -, - 3 -, …, - 8 -,- 9 -,- 10 -, - 11 -, - 12 -, …, - 18 -, - 19 -, - 20 -, - 21 -, … 结束示例]
    """

    hebrew1 = 'hebrew1'
    """希伯来字母

    指定序列将由下面列出的希伯来字母组成。

    为了确定任何值的显示文本，该序列指定了一组字符，表示位置 1–9，以及每个十的倍数（小于 100），每个百的倍数（小于 1000），等等。然后将这些字符组合在一起以构建其余值。

    此编号格式使用的字符集是 U+05D0–U+05D9, U+05DB, U+05DC, U+05DE, U+05E0–U+05E2, U+05E4, U+05E6–U+05EA, U+05E7– U+05E9, U+05EA, U+05DA, U+05DD, U+05DF, U+05E3 和 U+05E5。

    要构建任何值的文本，将其从十进制等效值转换，按照以下步骤进行（从右到左写）：

    ...
    """

    hebrew2 = 'hebrew2'
    """希伯来字母

    指定序列应由希伯来字母组成。

    为确定任何值所显示的文本，此序列指定一组字符，表示位置 1 到 22，然后使用下面定义的逻辑重复这些相同字符以构建所有其他值。

    此编号格式用于值 1 到 22 的字符集为 U+05D0 到 U+05D9，U+05DB，U+05DC，U+05DE，U+05E0 到 U+05E2，U+05E4，以及 U+05E6 到 U+05EA。

    对于大于字符集大小的值，按照以下步骤构建数字：

    - 重复从值中减去字符集的大小（22），直到结果等于或小于字符集的大小。
    - 写入由结果值表示的符号。
    - 然后，‫ת‬ 符号重复（在第一个符号的右侧），每次从原始值中减去字符集大小时都要重复。
    - 重新排序数字组不会改变其值。如果一个数字拼写出带有负面或正面含义的希伯来字，那么数字组可以重新排列。

    [示例：项目的编号应按照以下模式表示： ‫א‬, ‫ב‬, ‫ג‬, …, ‫את‬, ‫בת‬, … 结束示例]
    """

    arabicAlpha = 'arabicAlpha'
    """阿拉伯字母表

    指定序列将由阿拉伯字母表中的一个或多个字符组成，从下面列出的集合中选择。

    要确定任何值的显示文本，此序列指定一组表示位置 1–28 的字符，然后使用下面定义的逻辑重复这些相同的字符以构造所有其他值。

    该编号格式在值 1–28 的字符集是分别为 U+0623、U+0628、U+062A、U+062B、U+062C、U+062D、U+062E、U+062F、U+0630、U+0631、U+0632、U+0633、U+0634、U+0635、U+0636、U+0637、U+0638、U+0639、U+063A、U+0641、U+0642、U+0643、U+0644、U+0645、U+0646、U+0647 和 U+0648。

    对于大于 28 的值，显示的文本将按以下方式构造：

    - 反复从值中减去集合的大小（28），直到结果等于或小于集合的大小。
    - 余数确定要从上面集合中使用的字符，该字符写一次，然后写一次，然后写一次，并且重复集合大小从原始值中减去的次数。

    [示例：项目的编号应由以下模式表示：‫أ‬、‫ب‬、‫ت‬、…、‫و‬、‫ي‬、‫أ‬ ‫أ‬、‫ب ب‬、‫ت ت‬、…、‫و و‬、‫ي ي‬、‫أ أ أ‬、‫ب ب ب‬、‫ت ت ت‬、… 示例结束]
    """

    arabicAbjad = 'arabicAbjad'
    """阿拉伯字母数字

    指定序列将由阿拉伯字母表中的一个或多个递增的 Abjad 数字组成，从下面列出的集合中选择。

    要确定任何值的显示文本，此序列指定一组表示位置 1–28 的字符，然后使用下面定义的逻辑重复这些相同的字符以构造所有其他值。

    该编号格式在值 1–28 的字符集是分别为 U+0623、U+0628、U+062C、U+062F、U+0647、U+0648、U+0632、U+062D、U+0637、U+064A、U+0643、U+0644、U+0645、U+0646、U+0633、U+0639、U+0641、U+0635、U+0642、U+0631、U+0634、U+062A、U+062B、U+062E、U+0630、U+0636、U+063A 和 U+0638。

    对于大于 28 的值，显示的文本将按以下方式构造：

    - 反复从值中减去集合的大小（28），直到结果等于或小于集合的大小。
    - 余数确定要从上面集合中使用的字符，该字符写一次，然后写一次，然后写一次，并且重复集合大小从原始值中减去的次数。

    [示例：项目的编号应由以下模式表示：‫أ‬、‫ب‬、‫ج‬、…、‫ظ‬、‫غ‬、‫أأ‬、‫ب ب‬、‫ج ج‬、…、‫ظ ظ‬、‫غ غ‬、‫أ أ أ‬、‫ب ب ب‬、‫ج ج ج‬、… 示例结束]
    """

    hindiVowels = 'hindiVowels'
    """印地语元音

    指定序列应由下面列出的单个印地语元音中的一个或多个出现。

    为确定任何值所显示的文本，此序列指定一组字符，表示位置 1 到 37，然后使用下面定义的逻辑重复这些相同字符以构建所有其他值。

    此编号格式用于值 1 到 37 的字符集为 U+0915 到 U+0939。

    对于大于字符集大小的值，按照以下步骤构建数字：

    - 重复从值中减去字符集的大小（37），直到结果等于或小于字符集的大小。
    - 结果值确定要使用的字符，然后同一个字符写入一次，然后针对从原始值中减去字符集大小的次数重复。

    [示例：项目的编号应按照以下模式表示：क, ख, ग, …, स, ह, कक, खख, गग, …, सस, हह, ककक, खखख, गगग, … 结束示例]
    """

    hindiConsonants = 'hindiConsonants'
    """印地语辅音

    指定序列应由下面列出的单个印地语辅音中的一个或多个出现。

    为确定任何值所显示的文本，此序列指定一组字符，表示位置 1 到 18，然后使用下面定义的逻辑重复这些相同字符以构建所有其他值。

    此编号格式用于值 1 到 18 的字符集为 U+0905 到 U+0914，U+0905 与 U+0902 结合，以及 U+0905 与 U+0903，分别。

    对于大于字符集大小的值，按照以下步骤构建数字：

    - 重复从值中减去字符集的大小（18），直到结果等于或小于字符集的大小。
    - 结果值确定要使用的字符，然后同一个字符写入一次，然后针对从原始值中减去字符集大小的次数重复。

    [示例：项目的编号应按照以下模式表示： अ, आ, इ, …, अं,अः, अअ, आआ, इइ, …, अंअ,ं अःअः, अअअ, आआआ, इइइ, … 结束示例]
    """

    hindiNumbers = 'hindiNumbers'
    """印地语数字

    指定序列应由下面列出的单个印地语数字中的一个或多个出现。

    为确定任何值所显示的文本，此序列指定一组字符，表示位置 1 到 9，然后使用这些相同字符与彼此结合以及 ०（U+0966，表示数字零）来构建其余值。

    此编号格式用于值 1 到 9 的字符集为 U+0967, U+0968, U+0969, U+096A, U+096B, U+096C, U+096D, U+096E, 和 U+096F。

    对于大于字符集大小的值，按照以下步骤构建数字：

    - 将值除以 10，并写入表示余数的符号。
    - 将前一次除法的商除以 10，并将表示余数的符号写入现有位置的左侧。
    - 重复步骤 2，直到剩余值等于零。

    [示例：项目的编号应按照以下模式表示：१, २, ३, …, ८, ९, १०, ११, १२, …, १८, १९, २०, २१, … 结束示例]
    """

    hindiCounting = 'hindiCounting'
    """印地语计数系统

    指定序列应由印地语计数系统中的连续数字组成。

    此序列是一组字符串，每个字符串都是该序列中下一个值的完整名称，用印地语表示。

    [示例：项目的编号应按照以下模式表示： एक, दो, तीन, चार, पााँच, छः, सात, आठ, नौ, दस, … 结束示例]
    """

    thaiLetters = 'thaiLetters'
    """泰国字母

    指定序列应由泰国字母集合中的一个或多个字符组成。

    为确定任何值所显示的文本，此序列指定一组字符，表示位置1–41，然后重复使用相同的字符，使用以下逻辑构建所有其他值。

    用于值1–41的字符集是 U+0E01, U+0E02, U+0E04, U+0E07– U+0E23, U+0E25 和 U+0E27–U+0E2E。

    对于超出集合范围的值，数字的构建遵循以下步骤：

    - 重复从值中减去集合大小（41）的步骤，直到结果等于或小于集合的大小。
    - 结果值确定要使用的字符，并且相同的字符写入一次，然后为从原始值中减去集合大小的每次重复。

    [示例：项目的编号应按照以下模式表示：ก, ข, ค, …, อ, ฮ, กก, ขข, คค, …, ออ, ฮฮ, กกก, ขขข, คคค, … 结束示例]
    """

    thaiNumbers = 'thaiNumbers'
    """泰国数字

    指定序列应由泰国数字组成。

    为确定任何值所显示的文本，此序列指定一组字符，表示位置1–9，然后将这些相同字符结合在一起，并使用 ๐（表示数字零）构建剩余值。

    此编号格式用于值0–9的字符集是 U+0E50, U+0E51, U+0E52, U+0E53, U+0E54, U+0E55, U+0E56, U+0E57, U+0E58 和 U+0E59。

    对于超出集合范围的值，数字的构建遵循以下步骤：

    - 将值除以10，并写下表示余数的符号。
    - 将上一次除法的商除以10，并将表示余数的符号写在现有位置的左侧。
    - 重复步骤2，直到剩余值等于零。

    [示例：项目的编号应按照以下模式表示：๑, ๒, ๓, …, ๘, ๙, ๑๐, ๑๑, ๑๒, …, ๑๘, ๑๙, ๒๐, ๒๑, ๒๒, …, ๒๘, ๒๙, … 结束示例]
    """

    thaiCounting = 'thaiCounting'
    """泰国计数系统

    指定序列应由泰国计数系统的连续数字组成。

    此序列是一组字符串，其中每个字符串都是该序列中下一个值的泰文全名。

    [示例：项目的编号应按照以下模式表示：หนึ่ง, สอง, สาม, สี่, ห้า, หก, เจ็ด, แปด, เก้า, สิบ, … 结束示例]
    """

    bahtText = 'bahtText'
    """泰国铢文本

    指定序列将由泰国计数系统中的数字值组成，并附加บาทถ้วน到结果。

    准备加入静态文本的序列部分将是泰国计数格式中的等值部分，定义如下。

    [示例：项目的值应该由以下模式表示：หนึ่งบาทถ้วน、สองบาทถ้วน、สามบาทถ้วน 示例结束]
    """

    dollarText = 'dollarText'
    """美元文本

    指定序列将由运行语言的基数文本值组成，并在结果后附加“and 00/100”（也是在运行语言中）。【注意：后面的文本是固定的，因为编号序列中的值是基于整数的。结束注意】

    前置于静态文本之前的基数文本值应为下文中定义的基数文本格式中的等效值。

    [示例：one and 00/100, two and 00/100, three and 00/100. 示例结束]
    """

    custom = 'custom'
    """自定义定义的编号格式

    指定使用父元素的属性来指定使用 XSLT 格式属性定义的机制的编号格式。
    """


class ST_PageOrientation(ST_BaseEnumType):
    portrait = 'portrait'
    landscape = 'landscape'


class CT_PageSz(OxmlBaseElement):
    @property
    def w(self) -> Optional[s_ST_TwipsMeasure]:
        _val = self.attrib.get(qn('w:w'))

        if _val is not None:
            return s_to_ST_TwipsMeasure(_val)  # type: ignore
        return None

    @property
    def h(self) -> Optional[s_ST_TwipsMeasure]:
        _val = self.attrib.get(qn('w:h'))

        if _val is not None:
            return s_to_ST_TwipsMeasure(_val)  # type: ignore
        return None

    @property
    def orient(self) -> Optional[ST_PageOrientation]:
        _val = self.attrib.get(qn('w:orient'))

        if _val is not None:
            return ST_PageOrientation(_val)
        return None

    @property
    def code(self) -> Optional[ST_DecimalNumber]:
        _val = self.attrib.get(qn('w:code'))

        if _val is not None:
            return ST_DecimalNumber(_val)
        return None


class CT_PageMar(OxmlBaseElement):
    @property
    def top(self) -> ST_SignedTwipsMeasure:
        _val = self.attrib[qn('w:top')]

        return to_ST_SignedTwipsMeasure(str(_val))

    @property
    def right(self) -> Optional[s_ST_TwipsMeasure]:
        _val = self.attrib[qn('w:right')]

        return s_to_ST_TwipsMeasure(str(_val))

    @property
    def bottom(self) -> ST_SignedTwipsMeasure:
        _val = self.attrib[qn('w:bottom')]

        return to_ST_SignedTwipsMeasure(str(_val))

    @property
    def left(self) -> Optional[s_ST_TwipsMeasure]:
        _val = self.attrib[qn('w:left')]

        return s_to_ST_TwipsMeasure(str(_val))

    @property
    def header(self) -> Optional[s_ST_TwipsMeasure]:
        _val = self.attrib[qn('w:header')]

        return s_to_ST_TwipsMeasure(str(_val))

    @property
    def footer(self) -> Optional[s_ST_TwipsMeasure]:
        _val = self.attrib[qn('w:footer')]

        return s_to_ST_TwipsMeasure(str(_val))

    @property
    def gutter(self) -> Optional[s_ST_TwipsMeasure]:
        _val = self.attrib[qn('w:gutter')]

        return s_to_ST_TwipsMeasure(str(_val))


class ST_PageBorderZOrder(ST_BaseEnumType):
    front = 'front'
    back = 'back'


class ST_PageBorderDisplay(ST_BaseEnumType):
    allPages = 'allPages'
    firstPage = 'firstPage'
    notFirstPage = 'notFirstPage'


class ST_PageBorderOffset(ST_BaseEnumType):
    page = 'page'
    text = 'text'


class CT_PageBorders(OxmlBaseElement):
    @property
    def top(self) -> Optional[CT_TopPageBorder]:
        return getattr(self, qn('w:top'), None)

    @property
    def left(self) -> Optional[CT_PageBorder]:
        return getattr(self, qn('w:left'), None)

    @property
    def bottom(self) -> Optional[CT_BottomPageBorder]:
        return getattr(self, qn('w:bottom'), None)

    @property
    def right(self) -> Optional[CT_PageBorder]:
        return getattr(self, qn('w:right'), None)

    @property
    def zOrder(self) -> ST_PageBorderZOrder:
        _val = self.attrib.get(qn('w:zOrder'))

        if _val is not None:
            return ST_PageBorderZOrder(str(_val))

        return ST_PageBorderZOrder.front

    @property
    def display(self) -> Optional[ST_PageBorderDisplay]:
        _val = self.attrib.get(qn('w:display'))

        if _val is not None:
            return ST_PageBorderDisplay(str(_val))
        return None

    @property
    def offsetFrom(self) -> ST_PageBorderOffset:
        _val = self.attrib.get(qn('w:offsetFrom'))

        if _val is not None:
            return ST_PageBorderOffset(str(_val))

        return ST_PageBorderOffset.text


class CT_PageBorder(CT_Border):
    @property
    def r_id(self) -> Optional[str]:
        """id（自定义定义的边框关系引用）

        指定了包含父元素的自定义边框图像的关系ID。此自定义边框图像包含在WordprocessingML包中的单独部分中。

        此属性显式指定的关系应为类型http://purl.oclc.org/ooxml/officeDocument/relationships/image，否则文档将被视为不符合规范。

        如果省略此属性，则不使用自定义边框。

        【示例：考虑以下WordprocessingML标记，用于文档中的自定义底部边框：

        <w:bottom w:val="custom" r:id="rIdCustomBottomBorder" …/>

        关系引用命名空间中的id属性指定了关系ID为rIdCustomBottomBorder的关系必须包含文档的自定义底部边框图像。示例结束】
        """
        _val = self.attrib.get(qn('r:id'))

        if _val is not None:
            return str(_val)
        return None


class CT_BottomPageBorder(CT_PageBorder):
    """17.6.2 bottom (下边框)

    该元素指定了在本节中每个页面底部显示的页面边框的呈现和显示方式。

    【示例：考虑一个要求每个页面底部都有由一个苹果的重复图像组成的边框的部分，如下所示：


    这个边框将导致以下的WordprocessingML：

    【此处应有图片】

    <w:sectPr>
        …
        <w:pgBorders>
            <w:bottom w:val="apples" …/>
        </w:pgBorders>
        …
    </w:sectPr>
    因为页面只有一个底部边框，所以在页面边框集合中只指定了底部元素。示例结束】

    当文档具有相对于页面边缘的底部边框（使用pgBorders上的offsetFrom属性）时，它应跨越页面底部边缘，在其属性定义的位置停止，直到：

    与相应的左侧或右侧页面边框相交（如果指定了一个）。
    达到页面的边缘。
    【示例：在上面的示例中，WordprocessingML中没有指定左侧或右侧边框，因此消费者必须将边框从页面的一侧绘制到另一侧。示例结束】

    当文档具有相对于文本的底部边框（使用pgBorders上的offsetFrom属性）时，它应仅跨越必要的宽度以满足跨越文本宽度的要求。当文档指定了由bottomLeft、bottomRight和/或id属性指定的自定义边框艺术时，它应使用相应的关系部件项作为底部左下角、底部右下角和/或底部边框的图像。如果找不到相应的关系部件项，则消费者应使用val属性的值指定的边框。如果无法解析val属性的相应值，则在显示页面时不存在底部左下角、底部右下角或底部边框。

    当文档通过id属性指定了自定义边框艺术，而没有指定bottomRight和/或bottomLeft属性时，由id属性的相应关系部件项解析的底部边框应跨越到由bottomRight和/或bottomLeft属性未指定的角落。


    """

    @property
    def bottomLeft(self) -> Optional[r_ST_RelationshipId]:
        """bottomLeft（自定义定义的底部左边框关系引用）

        指定了包含父元素的自定义底部左边框图像的关系ID。此自定义边框图像包含在WordprocessingML包中的单独部分中。

        此属性显式指定的关系应为类型http://purl.oclc.org/ooxml/officeDocument/relationships/image，否则文档将被视为不符合规范。

        如果省略此属性，则不使用自定义底部左边框。

        【示例：考虑以下WordprocessingML标记，用于文档中的自定义底部左边框：

        <w:bottom w:val="custom"
            r:bottomLeft="rIdCustomBottomLeftBorder" …/>

        关系引用命名空间中的id属性指定了关系ID为rIdCustomBottomLeftBorder的关系必须包含文档的自定义底部左边框图像。示例结束】
        """
        _val = self.attrib.get(qn('r:bottomLeft'))

        if _val is not None:
            return r_ST_RelationshipId(str(_val))
        return None

    @property
    def bottomRight(self) -> Optional[r_ST_RelationshipId]:
        """bottomRight（自定义定义的底部右边框关系引用）

        指定了包含父元素的自定义底部右边框图像的关系ID。此自定义边框图像包含在WordprocessingML包中的单独部分中。

        此属性显式指定的关系应为类型http://purl.oclc.org/ooxml/officeDocument/relationships/image，否则文档将被视为不符合规范。

        如果省略此属性，则不使用自定义底部右边框。

        【示例：考虑以下WordprocessingML标记，用于文档中的自定义底部右边框：

        <w:bottom w:val="custom"
            r:bottomRight="rIdCustomBottomRightBorder" …/>

        关系引用命名空间中的id属性指定了关系ID为rIdCustomBottomRightBorder的关系必须包含文档的自定义底部右边框图像。示例结束】
        """
        _val = self.attrib.get(qn('r:bottomRight'))

        if _val is not None:
            return r_ST_RelationshipId(str(_val))
        return None


class CT_TopPageBorder(CT_PageBorder):
    @property
    def topLeft(self) -> Optional[r_ST_RelationshipId]:
        _val = self.attrib.get(qn('r:topLeft'))

        if _val is not None:
            return r_ST_RelationshipId(str(_val))
        return None

    @property
    def topRight(self) -> Optional[r_ST_RelationshipId]:
        _val = self.attrib.get(qn('r:topRight'))

        if _val is not None:
            return r_ST_RelationshipId(str(_val))
        return None


class ST_ChapterSep(ST_BaseEnumType):
    hyphen = 'hyphen'
    period = 'period'
    colon = 'colon'
    emDash = 'emDash'
    enDash = 'enDash'


class ST_LineNumberRestart(ST_BaseEnumType):
    newPage = 'newPage'
    newSection = 'newSection'
    continuous = 'continuous'


class CT_LineNumber(OxmlBaseElement):
    @property
    def countBy(self) -> Optional[ST_DecimalNumber]:
        _val = self.attrib.get(qn('countBy'))

        if _val is not None:
            return ST_DecimalNumber(int(_val))
        return None

    @property
    def start(self) -> ST_DecimalNumber:
        _val = self.attrib.get(qn('start'))

        if _val is not None:
            return ST_DecimalNumber(int(_val))

        return ST_DecimalNumber(1)

    @property
    def distance(self) -> Optional[s_ST_TwipsMeasure]:
        _val = self.attrib.get(qn('distance'))

        if _val is not None:
            return s_to_ST_TwipsMeasure(str(_val))
        return None

    @property
    def restart(self) -> ST_LineNumberRestart:
        _val = self.attrib.get(qn('restart'))

        if _val is not None:
            return ST_LineNumberRestart(str(_val))

        return ST_LineNumberRestart.newPage


class CT_PageNumber(OxmlBaseElement):
    @property
    def fmt(self) -> ST_NumberFormat:
        _val = self.attrib.get(qn('w:fmt'))

        if _val is not None:
            return ST_NumberFormat(str(_val))

        return ST_NumberFormat.decimal

    @property
    def start(self) -> Optional[ST_DecimalNumber]:
        _val = self.attrib.get(qn('start'))

        if _val is not None:
            return ST_DecimalNumber(int(_val))
        return None

    @property
    def chapStyle(self) -> Optional[ST_DecimalNumber]:
        _val = self.attrib.get(qn('chapStyle'))

        if _val is not None:
            return ST_DecimalNumber(int(_val))
        return None

    @property
    def chapSep(self) -> ST_ChapterSep:
        _val = self.attrib.get(qn('chapSep'))

        if _val is not None:
            return ST_ChapterSep(int(_val))

        return ST_ChapterSep.hyphen


class CT_Column(OxmlBaseElement):
    @property
    def w(self) -> Optional[s_ST_TwipsMeasure]:
        _val = self.attrib.get(qn('w'))

        if _val is not None:
            return s_to_ST_TwipsMeasure(str(_val))
        return None

    @property
    def space(self) -> s_ST_TwipsMeasure:
        _val = self.attrib.get(qn('space'))

        if _val is not None:
            return s_to_ST_TwipsMeasure(str(_val))

        return s_ST_TwipsMeasure(0)


class CT_Columns(OxmlBaseElement):
    @property
    def col(self) -> list[CT_Column]:
        """

        <xsd:sequence minOccurs="0">
            <xsd:element name="col" type="CT_Column" maxOccurs="45"/>
        </xsd:sequence>
        """

        return self.findall(qn('w:col'))  # type: ignore

    @property
    def equalWidth(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('equalWidth'))

        if _val is not None:
            return s_ST_OnOff(str(_val))
        return None

    @property
    def space(self) -> s_ST_TwipsMeasure:
        _val = self.attrib.get(qn('space'))

        if _val is not None:
            return s_to_ST_TwipsMeasure(str(_val))

        return s_ST_TwipsMeasure(720)

    @property
    def num(self) -> ST_DecimalNumber:
        _val = self.attrib.get(qn('num'))

        if _val is not None:
            return ST_DecimalNumber(str(_val))

        return ST_DecimalNumber(1)

    @property
    def sep(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('sep'))

        if _val is not None:
            return s_ST_OnOff(str(_val))
        return None


class ST_VerticalJc(ST_BaseEnumType):
    """17.18.101 ST_VerticalJc (垂直排列型)¶

    ST_VerticalJc (Vertical Alignment Type)

    这种简单类型指定了文本在父容器（页面或表格单元格）的上边缘和下边缘之间的垂直对齐方式。

    【示例：考虑一个区域，其中文本必须在父元素中垂直居中。这将需要一个值为center的val值，以指定所有垂直对齐都必须相对于父元素进行居中。对于一个部分，该设置将如下所示：

    <w:vAlign w:val="center" />

    center的val属性指定内容相对于其容器居中。结束示例】

    这种简单类型的内容是对W3C XML Schema字符串数据类型的限制。
    """

    top = 'top'
    """top（顶部对齐）

    指定文本应垂直对齐到父对象的顶边缘，根据需要将所有文本移动到父对象内的顶部文本范围。
    """

    center = 'center'
    """center（居中对齐）

    指定文本应垂直对齐到父对象的中心。
    """

    both = 'both'
    """both（垂直对齐）

    指定文本应在父对象的上边缘和下边缘之间垂直对齐，在需要时通过为每个段落添加额外的行间距来实现。

    该设置仅适用于在完整页面上显示的节的内容。如果内容未使用整个页面（例如另一个部分在同一页开始，或者文档在页面中间结束），则在呈现该页面时忽略该值（返回默认值为top）。

    该值仅允许用于页面对齐设置，并且当在表格单元格上指定时将被忽略（返回默认值top）。
    """

    bottom = 'bottom'
    """bottom（底部对齐）

    指定文本应垂直对齐到父对象的底边缘，根据需要将所有文本移动到父对象内的底部文本范围。
    """


class CT_VerticalJc(OxmlBaseElement):
    @property
    def val(self) -> ST_VerticalJc:
        return ST_VerticalJc(self.attrib[qn('w:val')])


class ST_DocGrid(ST_BaseEnumType):
    default = 'default'
    lines = 'lines'
    linesAndChars = 'linesAndChars'
    snapToChars = 'snapToChars'


class CT_DocGrid(OxmlBaseElement):
    @property
    def type(self) -> Optional[ST_DocGrid]:
        _val = self.attrib.get(qn('w:type'))

        if _val is not None:
            return ST_DocGrid(str(_val))
        return None

    @property
    def linePitch(self) -> Optional[ST_DecimalNumber]:
        _val = self.attrib.get(qn('w:linePitch'))

        if _val is not None:
            return ST_DecimalNumber(int(_val))
        return None

    @property
    def charSpace(self) -> Optional[ST_DecimalNumber]:
        _val = self.attrib.get(qn('w:charSpace'))

        if _val is not None:
            return ST_DecimalNumber(int(_val))
        return None


class ST_HdrFtr(ST_BaseEnumType):
    even = 'even'
    default = 'default'
    first = 'first'


class ST_FtnEdn(ST_BaseEnumType):
    normal = 'normal'
    separator = 'separator'
    continuationSeparator = 'continuationSeparator'
    continuationNotice = 'continuationNotice'


class CT_HdrFtrRef(CT_Rel):
    @property
    def type(self) -> Optional[ST_HdrFtr]:
        _val = self.attrib[qn('w:type')]

        return ST_HdrFtr(str(_val))


class EG_HdrFtrReferences(OxmlBaseElement):
    """

    <xsd:choice>
      <xsd:element name="headerReference" type="CT_HdrFtrRef" minOccurs="0"/>
      <xsd:element name="footerReference" type="CT_HdrFtrRef" minOccurs="0"/>
    </xsd:choice>
    """

    hdr_ftr_references_tags = (
        qn('w:headerReference'),  # CT_HdrFtrRef
        qn('w:footerReference'),  # CT_HdrFtrRef
    )


class CT_HdrFtr(OxmlBaseElement):
    @property
    def references(self) -> list[CT_HdrFtrRef]:
        return self.findall(*EG_HdrFtrReferences.hdr_ftr_references_tags)  # type: ignore


class EG_SectPrContents(OxmlBaseElement):
    @property
    def footnotePr(self) -> Optional[CT_FtnProps]:
        return getattr(self, qn('w:footnotePr'), None)

    @property
    def endnotePr(self) -> Optional[CT_EdnProps]:
        return getattr(self, qn('w:endnotePr'), None)

    @property
    def type(self) -> Optional[CT_SectType]:
        return getattr(self, qn('w:type'), None)

    @property
    def pgSz(self) -> Optional[CT_PageSz]:
        return getattr(self, qn('w:pgSz'), None)

    @property
    def pgMar(self) -> Optional[CT_PageMar]:
        return getattr(self, qn('w:pgMar'), None)

    @property
    def paperSrc(self) -> Optional[CT_PaperSource]:
        return getattr(self, qn('w:paperSrc'), None)

    @property
    def pgBorders(self) -> Optional[CT_PageBorders]:
        return getattr(self, qn('w:pgBorders'), None)

    @property
    def lnNumType(self) -> Optional[CT_LineNumber]:
        return getattr(self, qn('w:lnNumType'), None)

    @property
    def pgNumType(self) -> Optional[CT_PageNumber]:
        return getattr(self, qn('w:pgNumType'), None)

    @property
    def cols(self) -> Optional[CT_Columns]:
        return getattr(self, qn('w:cols'), None)

    @property
    def formProt(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:formProt'), None)

    @property
    def vAlign(self) -> Optional[CT_VerticalJc]:
        return getattr(self, qn('w:vAlign'), None)

    @property
    def noEndnote(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:noEndnote'), None)

    @property
    def titlePg(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:titlePg'), None)

    @property
    def textDirection(self) -> Optional[CT_TextDirection]:
        return getattr(self, qn('w:textDirection'), None)

    @property
    def bidi(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:bidi'), None)

    @property
    def rtlGutter(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:rtlGutter'), None)

    @property
    def docGrid(self) -> Optional[CT_DocGrid]:
        return getattr(self, qn('w:docGrid'), None)

    @property
    def printerSettings(self) -> Optional[CT_Rel]:
        return getattr(self, qn('w:printerSettings'), None)


class AG_SectPrAttributes(OxmlBaseElement):
    """17.6.17 sectPr (文档最终节属性)"""

    @property
    def rsidRPr(self) -> Optional[ST_LongHexNumber]:
        """物理节标记字符修订标识

        指定用于跟踪编辑会话的唯一标识符，当表示此节标记的物理字符最后一次被格式化时使用。

        如果存在，本文档中所有等值的rsid*属性将指示这些区域在同一编辑会话期间被修改。

        制作人可以选择递增修订保存 ID 值，以指示后续的编辑会话（在保存操作之间的编辑），以指示执行的保存的顺序。

        此属性的可能值由ST_LongHexNumber简单类型定义（[§17.18.50]）。
        """
        _val = self.attrib.get(qn('w:rsidRPr'))

        if _val is not None:
            return ST_LongHexNumber(str(_val))
        return None

    @property
    def rsidDel(self) -> Optional[ST_LongHexNumber]:
        """节删除修订标识

        指定用于跟踪编辑会话的唯一标识符，当此节的节标记从文档中删除时使用。

        如果存在，本文档中所有等值的rsid*属性将指示这些区域在同一编辑会话期间被修改。

        制作人可以选择递增修订保存 ID 值，以指示后续的编辑会话（在保存操作之间的编辑），以指示执行的保存的顺序。

        此属性的可能值由ST_LongHexNumber简单类型定义（[§17.18.50]）。
        """
        _val = self.attrib.get(qn('w:rsidDel'))

        if _val is not None:
            return ST_LongHexNumber(str(_val))
        return None

    @property
    def rsidR(self) -> Optional[ST_LongHexNumber]:
        """节添加修订标识

        指定用于跟踪编辑会话的唯一标识符，当此节的节标记添加到文档中时使用。

        如果存在，本文档中所有等值的rsid*属性将指示这些区域在同一编辑会话期间被修改。

        制作人可以选择递增修订保存 ID 值，以指示后续的编辑会话（在保存操作之间的编辑），以指示执行的保存的顺序。

        此属性的可能值由ST_LongHexNumber简单类型定义（[§17.18.50]）。
        """
        _val = self.attrib.get(qn('w:rsidR'))

        if _val is not None:
            return ST_LongHexNumber(str(_val))
        return None

    @property
    def rsidSect(self) -> Optional[ST_LongHexNumber]:
        """节属性修订标识

        指定用于跟踪编辑会话的唯一标识符，当表示此节标记的物理字符最后一次被格式化时使用。

        如果存在，本文档中所有等值的rsid*属性将指示这些区域在同一编辑会话期间被修改。

        制作人可以选择递增修订保存 ID 值，以指示后续的编辑会话（在保存操作之间的编辑），以指示执行的保存的顺序。

        此属性的可能值由ST_LongHexNumber简单类型定义（[§17.18.50]）。
        """
        _val = self.attrib.get(qn('w:rsidSect'))

        if _val is not None:
            return ST_LongHexNumber(str(_val))
        return None


class CT_SectPrBase(EG_SectPrContents, AG_SectPrAttributes): ...


class CT_SectPr(EG_HdrFtrReferences, EG_SectPrContents, AG_SectPrAttributes):
    """17.6.17 sectPr (文档最终节属性)
    17.6.18 sectPr (节属性)
    17.6.19 sectPr (上一节属性)

    17.6.18 sectPr (节属性)

    该元素定义了文档中某一节的节属性。[注意：对于文档中的最后一节，节属性被存储为body元素的子元素。结束注意]

    [示例：考虑一个具有多个节的文档。对于除最后一节之外的所有节，sectPr元素都存储为该节中最后一个段落的子元素，如下所示：

    <w:body>
        <w:p>
            <w:pPr>
                <w:sectPr>
                    (最后一节的属性)
                </w:sectPr>
            </w:pPr>
            …
        </w:p>
        …
        <w:sectPr>
            (最后一节的属性)
        </w:sectPr>
    </w:body>

    结束示例]
    """

    @property
    def hdr_ftr(self) -> Optional[CT_HdrFtrRef]:
        """ """
        return self.choice_one_child(*EG_HdrFtrReferences.hdr_ftr_references_tags)  # type: ignore

    @property
    def sectPrChange(self) -> Optional[CT_SectPrChange]:
        """17.13.5.32 sectPrChange (节属性的修订信息)"""
        return getattr(self, qn('w:sectPrChange'), None)


class ST_BrType(ST_BaseEnumType):
    """17.18.4 ST_BrType (Break 类型)¶

    ST_BrType (Break Types)

    这个简单类型指定了WordprocessingML文档中可能的换行字符类型。换行类型决定了在应用此手动换行后文本将被放置的下一个位置（详见枚举值）。

    [示例：考虑一个必须将文本前进到文档中下一个文本列的手动换行符，而不仅仅是下一可用行。这个换行符应如下指定：

    <w:br w:type="column"/>

    type属性指定值为column，这意味着该换行必须将文档中的下一个字符强制重新开始于新文本列中的下一行。示例结束]

    这个简单类型的内容是W3C XML Schema字符串数据类型的一个限制。
    """

    page = 'page'
    """page（分页符）

    指定当前换行应重新开始于文档的下一页。

    分页符在框架中存在时应被忽略。
    """

    column = 'column'
    """column（列换行）

    指定当前换行应重新开始于当前页面上可用的下一列。

    如果当前节没有分成列，或者列换行出现在显示时的当前页面最后一列，则文本的重新开始位置应为文档中的下一页。
    """

    textWrapping = 'textWrapping'
    """textWrapping（换行符）

    指定当前换行应重新开始于文档中的下一行。

    下一行的确定应根据指定换行字符的clear属性值进行。
    """


class ST_BrClear(ST_BaseEnumType):
    """17.18.3 ST_BrClear (换行文本换行重新开始位置)¶

    ST_BrClear (Line Break Text Wrapping Restart Location)

    这个简单类型指定了一组可能的重启位置，用于在换行符的type属性值为textWrapping时确定下一个可用的行。当当前运行的文本由于浮动对象的存在而显示在未跨越全文本范围的行上时，此属性仅影响重启位置（详见枚举值）。

    [示例：考虑一个文本环绕换行符，该字符应将重启位置强制到跨越页面全文本范围的下一行（没有浮动对象中断该行）。

    该换行符的样式为textWrapping，因为它只需前进到下一行，但clear值必须指定此重启位置必须忽略所有不跨越全文本宽度的行，通过指定值all，如下所示：

    <w:br w:type="textWrapping" w:clear="all" />

    因此，该换行符不能使用下一个可用的行，而是应忽略所有不跨越全文本宽度的行并使用下一个可用的行。示例结束]

    这个简单类型的内容是W3C XML Schema字符串数据类型的一个限制。
    """

    none = 'none'
    """none（在下一行重新开始）

    指定文本环绕换行符应将文本前进到WordprocessingML文档中的下一行，而不管其位置是从左到右还是任何与该行相交的浮动对象的存在。

    这是文档中常规换行符的设置。
    """

    left = 'left'
    """left（在左侧未被阻挡的下一个文本区域重新开始）

    指定当该行与浮动对象相交时，文本环绕换行符应如下所示：

    如果父段落是从左到右：

        - 如果这是当前行中最左侧的文本流区域，
            -如果浮动对象出现在换行符左侧，将文本前进到下一行，该行左侧没有浮动对象。
            - 否则，将文本前进到当前行上可以显示文本的下一个位置。
        - 否则，将此视为类型为none的文本环绕换行符。

    如果父段落是从右到左：

        - 如果浮动对象出现在换行符左侧，将文本前进到下一行，该行左侧没有浮动对象。
        - 否则，将此视为类型为none的文本环绕换行符。

    在任何情况下，如果此行未与浮动对象相交，则将此换行符视为类型为none的文本环绕换行符。
    """

    right = 'right'
    """right（在右侧未被阻挡的下一个文本区域重新开始）

    指定当该行与浮动对象相交时，文本环绕换行符应如下所示：

    如果父段落是从左到右：

    - 如果浮动对象出现在换行符右侧，将文本前进到下一行，该行右侧没有浮动对象。
    - 否则，将此视为类型为none的文本环绕换行符。

    如果父段落是从右到左：

        - 如果浮动对象出现在换行符右侧，将文本前进到下一行，该行右侧没有浮动对象。
            - 如果这是当前行中最右侧的文本流区域，
            - 否则，将文本前进到当前行上可以显示文本的下一个位置。
        - 否则，将此视为类型为none的文本环绕换行符。

    在任何情况下，如果此行未与浮动对象相交，则将此换行符视为类型为none的文本环绕换行符。
    """

    all = 'all'
    """all（在下一个完整行重新开始）

    指定文本环绕换行符应将文本前进到WordprocessingML文档中跨越整行宽度的下一行（即在显示时不被任何浮动对象中断的下一行）。

    [注意：此设置通常用于将单行文本放置在浮动对象旁边作为标题。注意结束]
    """


class CT_Br(OxmlBaseElement):
    """17.3.3.1 br (折断/换行)

    br (Break)

    该元素指定在运行内容的当前位置放置一个换行符。换行符是一种特殊字符，用于覆盖基于文档内容的正常布局执行的正常换行。【示例：对于英语，正常换行仅在断字空格或可选连字符之后发生。示例结束】

    此换行符的行为（在此换行后文本应该重新开始的位置）将由其类型和清除属性值决定，如下所述。

    【示例：考虑一个WordprocessingML文档中的以下句子：

    This is a simple sentence.

    通常情况下，就像上面显示的那样，此句子将显示在单行中，因为它的长度不足以需要换行（给定当前页面的宽度）。然而，如果在单词 is 之后插入一个文本换行符（典型的换行符），如下所示：


    <w:r>
    <w:t>This is</w:t>
    <w:br/>
    <w:t xml:space="preserve"> a simple sentence.</w:t>
    </w:r>

    这意味着这个换行符必须被视为一个简单的换行符，并在该单词之后换行：

    This is
    a simple sentence.

    换行符强制使以下文本在文档中的下一行重新开始。示例结束】
    """

    @property
    def type(self) -> Optional[ST_BrType]:
        """type（换行符类型）

        指定当前换行符的换行类型。换行类型确定应用此手动换行符后文本内容中文本应放置的下一个位置（有关详细信息，请参见可能的值）。

        如果省略此属性，则假定它是样式 textWrapping。

        【示例：考虑一个手动换行符，它必须将文本移动到文档中的下一个文本列，而不仅仅是下一个可用行。因此，此换行将被指定如下：

        <w:br w:type="column"/>

        type 属性指定一个列值，这意味着换行符必须强制文档中的下一个字符在新的文本列中的下一行重新开始。示例结束】

        此属性的可能值由 ST_BrType 简单类型定义(§17.18.4)。
        """
        _val = self.attrib.get(qn('w:type'))

        if _val is not None:
            return ST_BrType(str(_val))
        return None

    @property
    def clear(self) -> Optional[ST_BrClear]:
        """clear（文本换行符的重启位置）

        指定当换行的类型属性具有 textWrapping 值时将用作下一个可用行的位置。此属性仅在当前运行显示在未跨越全文范围的行上时影响重启位置，这是由于存在浮动对象（有关详细信息，请参见可能的值）。

        如果此换行符不是样式 textWrapping，则应忽略此属性。如果省略此属性，则在需要时假定其值为 none。

        【示例：考虑一个文本换行符，它应该将重启位置强制到跨越页面文本范围的下一行（没有中断行的浮动对象）。

        这个换行是 textWrapping 样式的，因为它必须只前进到下一行，但 clear 值必须指定，这个重启位置必须忽略不跨越全文宽度的所有行，因此指定值为 all，如下所示：

        <w:br w:type="textWrapping" w:clear="all" />

        因此，此换行符不得使用下一个可用行，而是必须使用忽略不跨越全文宽度的所有行的下一个可用行。示例结束】

        此属性的可能值由 ST_BrClear 简单类型定义(§17.18.3)。
        """
        _val = self.attrib.get(qn('w:clear'))

        if _val is not None:
            return ST_BrClear(str(_val))
        return None


class ST_PTabAlignment(ST_BaseEnumType):
    left = 'left'
    center = 'center'
    right = 'right'


class ST_PTabRelativeTo(ST_BaseEnumType):
    margin = 'margin'
    indent = 'indent'


class ST_PTabLeader(ST_BaseEnumType):
    none = 'none'
    dot = 'dot'
    hyphen = 'hyphen'
    underscore = 'underscore'
    middleDot = 'middleDot'


class CT_PTab(OxmlBaseElement):
    @property
    def alignment(self) -> ST_PTabAlignment:
        _val = self.attrib[qn('w:alignment')]

        return ST_PTabAlignment(str(_val))

    @property
    def relativeTo(self) -> ST_PTabRelativeTo:
        _val = self.attrib[qn('w:relativeTo')]

        return ST_PTabRelativeTo(str(_val))

    @property
    def leader(self) -> ST_PTabLeader:
        _val = self.attrib[qn('w:leader')]

        return ST_PTabLeader(str(_val))


class CT_Sym(OxmlBaseElement):
    @property
    def font(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:font'))
        if _val is not None:
            return str(_val)
        return None

    @property
    def char(self) -> Optional[ST_ShortHexNumber]:
        _val = self.attrib.get(qn('w:char'))

        if _val is not None:
            return ST_ShortHexNumber(str(_val))
        return None


class ST_ProofErr(ST_BaseEnumType):
    spellStart = 'spellStart'
    spellEnd = 'spellEnd'
    gramStart = 'gramStart'
    gramEnd = 'gramEnd'


class CT_ProofErr(OxmlBaseElement):
    @property
    def type(self) -> ST_ProofErr:
        _val = self.attrib[qn('w:type')]

        return ST_ProofErr(str(_val))


class ST_EdGrp(ST_BaseEnumType):
    none = 'none'
    everyone = 'everyone'
    administrators = 'administrators'
    contributors = 'contributors'
    editors = 'editors'
    owners = 'owners'
    current = 'current'


class CT_Perm(OxmlBaseElement):
    @property
    def id(self) -> str:
        _val = self.attrib[qn('w:id')]

        return str(_val)

    @property
    def displacedByCustomXml(self) -> Optional[ST_DisplacedByCustomXml]:
        _val = self.attrib.get(qn('w:displacedByCustomXml'))

        if _val is not None:
            return ST_DisplacedByCustomXml(str(_val).encode())
        return None


class CT_PermStart(CT_Perm):
    @property
    def edGrp(self) -> Optional[ST_EdGrp]:
        _val = self.attrib.get(qn('w:edGrp'))

        if _val is not None:
            return ST_EdGrp(str(_val))
        return None

    @property
    def ed(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:ed'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def colFirst(self) -> Optional[ST_DecimalNumber]:
        _val = self.attrib.get(qn('w:colFirst'))

        if _val is not None:
            return ST_DecimalNumber(int(_val))
        return None

    @property
    def colLast(self) -> Optional[ST_DecimalNumber]:
        _val = self.attrib.get(qn('w:colLast'))

        if _val is not None:
            return ST_DecimalNumber(int(_val))
        return None


class CT_Text(OxmlBaseElement):
    @property
    def space(self) -> Optional[str]:
        _val = self.attrib.get(qn('xml:space'))

        if _val is not None:
            return str(_val)
        return None


class EG_RunInnerContent(OxmlBaseElement):
    """
    <xsd:group name="EG_RunInnerContent">
        <xsd:choice>
            <xsd:element name="br" type="CT_Br"/>
            <xsd:element name="t" type="CT_Text"/>
            <xsd:element name="contentPart" type="CT_Rel"/>
            <xsd:element name="delText" type="CT_Text"/>
            <xsd:element name="instrText" type="CT_Text"/>
            <xsd:element name="delInstrText" type="CT_Text"/>
            <xsd:element name="noBreakHyphen" type="CT_Empty"/>
            <xsd:element name="softHyphen" type="CT_Empty" minOccurs="0"/>
            <xsd:element name="dayShort" type="CT_Empty" minOccurs="0"/>
            <xsd:element name="monthShort" type="CT_Empty" minOccurs="0"/>
            <xsd:element name="yearShort" type="CT_Empty" minOccurs="0"/>
            <xsd:element name="dayLong" type="CT_Empty" minOccurs="0"/>
            <xsd:element name="monthLong" type="CT_Empty" minOccurs="0"/>
            <xsd:element name="yearLong" type="CT_Empty" minOccurs="0"/>
            <xsd:element name="annotationRef" type="CT_Empty" minOccurs="0"/>
            <xsd:element name="footnoteRef" type="CT_Empty" minOccurs="0"/>
            <xsd:element name="endnoteRef" type="CT_Empty" minOccurs="0"/>
            <xsd:element name="separator" type="CT_Empty" minOccurs="0"/>
            <xsd:element name="continuationSeparator" type="CT_Empty" minOccurs="0"/>
            <xsd:element name="sym" type="CT_Sym" minOccurs="0"/>
            <xsd:element name="pgNum" type="CT_Empty" minOccurs="0"/>
            <xsd:element name="cr" type="CT_Empty" minOccurs="0"/>
            <xsd:element name="tab" type="CT_Empty" minOccurs="0"/>
            <xsd:element name="object" type="CT_Object"/>
            <xsd:element name="pict" type="CT_Picture"/>
            <xsd:element name="fldChar" type="CT_FldChar"/>
            <xsd:element name="ruby" type="CT_Ruby"/>
            <xsd:element name="footnoteReference" type="CT_FtnEdnRef"/>
            <xsd:element name="endnoteReference" type="CT_FtnEdnRef"/>
            <xsd:element name="commentReference" type="CT_Markup"/>
            <xsd:element name="drawing" type="CT_Drawing"/>
            <xsd:element name="ptab" type="CT_PTab" minOccurs="0"/>
            <xsd:element name="lastRenderedPageBreak" type="CT_Empty" minOccurs="0" maxOccurs="1"/>
        </xsd:choice>
    </xsd:group>
    """

    run_inner_content_tags = (
        qn('w:br'),  # CT_Br
        qn('w:t'),  # CT_Text
        qn('w:contentPart'),  # CT_Rel
        qn('w:delText'),  # CT_Text
        qn('w:instrText'),  # CT_Text
        qn('w:delInstrText'),  # CT_Text
        qn('w:noBreakHyphen'),  # CT_Empty
        qn('w:softHyphen'),  # CT_Empty
        qn('w:dayShort'),  # CT_Empty
        qn('w:monthShort'),  # CT_Empty
        qn('w:yearShort'),  # CT_Empty
        qn('w:dayLong'),  # CT_Empty
        qn('w:monthLong'),  # CT_Empty
        qn('w:yearLong'),  # CT_Empty
        qn('w:annotationRef'),  # CT_Empty
        qn('w:footnoteRef'),  # CT_Empty
        qn('w:endnoteRef'),  # CT_Empty
        qn('w:separator'),  # CT_Empty
        qn('w:continuationSeparator'),  # CT_Empty
        qn('w:sym'),  # CT_Sym
        qn('w:pgNum'),  # CT_Empty
        qn('w:cr'),  # CT_Empty
        qn('w:tab'),  # CT_Empty
        qn('w:object'),  # CT_Object
        qn('w:pict'),  # CT_Picture
        qn('w:fldChar'),  # CT_FldChar
        qn('w:ruby'),  # CT_Ruby
        qn('w:footnoteReference'),  # CT_FtnEdnRef
        qn('w:endnoteReference'),  # CT_FtnEdnRef
        qn('w:commentReference'),  # CT_Markup
        qn('w:drawing'),  # CT_Drawing
        qn('w:ptab'),  # CT_PTab
        qn('w:lastRenderedPageBreak'),  # CT_Empty
        # 实际有mc:AlternateContent
        # from ..pml.core import CT_MC_AlternateContent
        qn('mc:AlternateContent'),  # CT_MC_AlternateContent
    )

    @property
    def br(self) -> Optional[CT_Br]:
        return getattr(self, qn('w:br'), None)  # CT_Br

    @property
    def t(self) -> Optional[CT_Text]:
        return getattr(self, qn('w:t'), None)  # CT_Text

    @property
    def contentPart(self) -> Optional[CT_Rel]:
        return getattr(self, qn('w:contentPart'), None)  # CT_Rel

    @property
    def delText(self) -> Optional[CT_Text]:
        return getattr(self, qn('w:delText'), None)  # CT_Text

    @property
    def instrText(self) -> Optional[CT_Text]:
        return getattr(self, qn('w:instrText'), None)  # CT_Text

    @property
    def delInstrText(self) -> Optional[CT_Text]:
        return getattr(self, qn('w:delInstrText'), None)  # CT_Text

    @property
    def noBreakHyphen(self) -> Optional[CT_Empty]:
        return getattr(self, qn('w:noBreakHyphen'), None)  # CT_Empty

    @property
    def softHyphen(self) -> Optional[CT_Empty]:
        return getattr(self, qn('w:softHyphen'), None)  # CT_Empty

    @property
    def dayShort(self) -> Optional[CT_Empty]:
        return getattr(self, qn('w:dayShort'), None)  # CT_Empty

    @property
    def monthShort(self) -> Optional[CT_Empty]:
        return getattr(self, qn('w:monthShort'), None)  # CT_Empty

    @property
    def yearShort(self) -> Optional[CT_Empty]:
        return getattr(self, qn('w:yearShort'), None)  # CT_Empty

    @property
    def dayLong(self) -> Optional[CT_Empty]:
        return getattr(self, qn('w:dayLong'), None)  # CT_Empty

    @property
    def monthLong(self) -> Optional[CT_Empty]:
        return getattr(self, qn('w:monthLong'), None)  # CT_Empty

    @property
    def yearLong(self) -> Optional[CT_Empty]:
        return getattr(self, qn('w:yearLong'), None)  # CT_Empty

    @property
    def annotationRef(self) -> Optional[CT_Empty]:
        return getattr(self, qn('w:annotationRef'), None)  # CT_Empty

    @property
    def footnoteRef(self) -> Optional[CT_Empty]:
        return getattr(self, qn('w:footnoteRef'), None)  # CT_Empty

    @property
    def endnoteRef(self) -> Optional[CT_Empty]:
        return getattr(self, qn('w:endnoteRef'), None)  # CT_Empty

    @property
    def separator(self) -> Optional[CT_Empty]:
        return getattr(self, qn('w:separator'), None)  # CT_Empty

    @property
    def continuationSeparator(self) -> Optional[CT_Empty]:
        return getattr(self, qn('w:continuationSeparator'), None)  # CT_Empty

    @property
    def sym(self) -> Optional[CT_Sym]:
        return getattr(self, qn('w:sym'), None)  # CT_Sym

    @property
    def pgNum(self) -> Optional[CT_Empty]:
        return getattr(self, qn('w:pgNum'), None)  # CT_Empty

    @property
    def cr(self) -> Optional[CT_Empty]:
        return getattr(self, qn('w:cr'), None)  # CT_Empty

    @property
    def tab(self) -> Optional[CT_Empty]:
        return getattr(self, qn('w:tab'), None)  # CT_Empty, Union_CT_TabStop

    @property
    def object(self) -> Optional[CT_Object]:
        return getattr(self, qn('w:object'), None)  # CT_Object

    @property
    def pict(self) -> Optional[CT_Picture]:
        return getattr(self, qn('w:pict'), None)  # CT_Picture

    @property
    def fldChar(self) -> Optional[CT_FldChar]:
        return getattr(self, qn('w:fldChar'), None)  # CT_FldChar

    @property
    def ruby(self) -> Optional[CT_Ruby]:
        return getattr(self, qn('w:ruby'), None)  # CT_Ruby

    @property
    def footnoteReference(self) -> Optional[CT_FtnEdnRef]:
        return getattr(self, qn('w:footnoteReference'), None)  # CT_FtnEdnRef

    @property
    def endnoteReference(self) -> Optional[CT_FtnEdnRef]:
        return getattr(self, qn('w:endnoteReference'), None)  # CT_FtnEdnRef

    @property
    def commentReference(self) -> Optional[CT_Markup]:
        return getattr(self, qn('w:commentReference'), None)  # CT_Markup

    @property
    def drawing(self) -> Optional[CT_Drawing]:
        return getattr(self, qn('w:drawing'), None)  # CT_Drawing

    @property
    def ptab(self) -> Optional[CT_PTab]:
        return getattr(self, qn('w:ptab'), None)  # CT_PTab

    @property
    def lastRenderedPageBreak(self) -> Optional[CT_Empty]:
        return getattr(self, qn('w:lastRenderedPageBreak'), None)  # CT_Empty


class EG_RPr(OxmlBaseElement):
    @property
    def rPr(self) -> Optional[CT_RPr]:
        return getattr(self, qn('w:rPr'), None)


class CT_R(EG_RPr, EG_RunInnerContent):
    """17.3.2.25 r (文本运行)

    该元素指定了父字段、超链接、自定义 XML 元素、结构化文档标记、智能标记或段落中的一段内容。

    WordprocessingML 文档中的一段内容可以由任意组合的内容组成。

    示例：考虑一个包含一对运行的基本 WordprocessingML 段落。该运行将表示如下：

    ```xml
    <w:document>
        <w:body>
            <w:p>
                <w:r>
                    <w:t>文本</w:t>
                </w:r>
                <w:fldSimple w:instr="作者">
                    <w:r>
                        <w:t>作者姓名</w:t>
                    </w:r>
                </w:fldSimple>
            </w:p>
        </w:body>
    </w:document>
    ```

    在此示例中，r 元素是运行中所有内容的容器，其中包括段落中的运行和简单字段内的运行。

    <xsd:complexType name="CT_R">
        <xsd:sequence>
            <xsd:group ref="EG_RPr" minOccurs="0"/>
            <xsd:group ref="EG_RunInnerContent" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
        <xsd:attribute name="rsidRPr" type="ST_LongHexNumber"/>
        <xsd:attribute name="rsidDel" type="ST_LongHexNumber"/>
        <xsd:attribute name="rsidR" type="ST_LongHexNumber"/>
    </xsd:complexType>
    """

    @property
    def run_inner_content(
        self,
    ) -> list[
        CT_Br | CT_Text | CT_Rel | CT_Empty | CT_Sym | CT_Object | CT_Picture | CT_FldChar | CT_FtnEdnRef | CT_Markup | CT_Drawing | CT_PTab
    ]:
        """运行内容标签合集"""
        return self.choice_and_more(*EG_RunInnerContent.run_inner_content_tags)  # type: ignore

    @property
    def rsidRPr(self) -> Optional[ST_LongHexNumber]:
        """运行属性修订标识符

        指定一个唯一标识符，用于跟踪编辑会话，在此会话中，上次修改了主文档中的运行属性。

        如果存在，此文档中所有具有相同值的 rsid* 属性应指示这些区域在同一编辑会话期间（连续保存操作之间的时间）被修改。

        生产者可以选择增加修订保存 ID 值，以指示后续编辑会话，以表明相对于此文档中其他修改的顺序。

        此属性的可能值由 ST_LongHexNumber 简单类型定义（[§17.18.50]）。
        """
        _val = self.attrib.get(qn('w:rsidRPr'))

        if _val is not None:
            return ST_LongHexNumber(str(_val))
        return None

    @property
    def rsidDel(self) -> Optional[ST_LongHexNumber]:
        """删除的运行修订标识符

        指定一个唯一标识符，用于跟踪编辑会话，在此会话中，从主文档中删除了该运行。

        如果存在，此文档中所有具有相同值的 rsid* 属性应指示这些区域在同一编辑会话期间（连续保存操作之间的时间）被修改。

        生产者可以选择增加修订保存 ID 值，以指示后续编辑会话，以表明相对于此文档中其他修改的顺序。

        此属性的可能值由 ST_LongHexNumber 简单类型定义（[§17.18.50]）。
        """
        _val = self.attrib.get(qn('w:rsidDel'))

        if _val is not None:
            return ST_LongHexNumber(str(_val))
        return None

    @property
    def rsidR(self) -> Optional[ST_LongHexNumber]:
        """运行修订标识符

        指定一个唯一标识符，用于跟踪编辑会话，在此会话中，将运行添加到主文档中。

        如果存在，此文档中所有具有相同值的 rsid* 属性应指示这些区域在同一编辑会话期间（连续保存操作之间的时间）被修改。

        生产者可以选择增加修订保存 ID 值，以指示后续编辑会话，以表明相对于此文档中其他修改的顺序。

        此属性的可能值由 ST_LongHexNumber 简单类型定义（[§17.18.50]）。
        """
        _val = self.attrib.get(qn('w:rsidR'))

        if _val is not None:
            return ST_LongHexNumber(str(_val))
        return None


class ST_Hint(ST_BaseEnumType):
    default = 'default'
    eastAsia = 'eastAsia'


class ST_Theme(ST_BaseEnumType):
    majorEastAsia = 'majorEastAsia'
    majorBidi = 'majorBidi'
    majorAscii = 'majorAscii'
    majorHAnsi = 'majorHAnsi'
    minorEastAsia = 'minorEastAsia'
    minorBidi = 'minorBidi'
    minorAscii = 'minorAscii'
    minorHAnsi = 'minorHAnsi'


class CT_Fonts(OxmlBaseElement):
    """17.3.2.26 rFonts (运行字体)

    此元素指定应用于显示此运行的文本内容的字体。在单个运行内，最多可以有四种类型的字体槽，每种类型允许使用唯一的字体：

    - ASCII（即，前 128 个 Unicode 代码点）
    - 高 ANSI
    - 复杂文本
    - 东亚

    如果此元素不存在，则默认值是保留在样式层次结构中前一级别应用的格式。如果此元素在样式层次结构中从未应用过，则文本将显示在支持该字符集的任何默认字体中。

    [示例：考虑一个包含阿拉伯文和英文文本的单个文本运行，可以表示如下：

    <w:r>
        <w:rPr>
            <w:rFonts w:ascii="Courier New" w:cs="Times New Roman" />
        </w:rPr>
        <w:t>English ‫العربية‬</w:t>
    </w:r>

    在此运行中，“English” 和 “‫”العربية‬ 应根据以下两步算法处于 ASCII 字体槽中。因此，它们都应该使用 Courier New 字体。

    相同的内容也可以表示如下：

    <w:r>
        <w:rPr>
            <w:rFonts w:ascii="Courier New" w:cs="Times New Roman" />
        <w:rtl/>
        </w:rPr>
        <w:t>English ‫العربية‬</w:t>
    </w:r>

    在此运行中，“English” 和 “‫”العربية‬ 应根据两步算法处于复杂文本字体槽中。因此，它们都应该使用 Times New Roman 字体。结束示例]

    对于运行中的每个 Unicode 字符，可以使用以下两步方法确定字体槽：

    ....
    """

    @property
    def hint(self) -> Optional[ST_Hint]:
        """hint（字体内容类型）

        指定应用于当前运行中任何模糊字符的字体类型。

        存在某些字符不是显式存储在文档中的，可以映射到上述四种类别中的多个类别。此属性应用于调停冲突，并确定如何处理此运行中的歧义。[注：这主要用于处理段落标记符号和其他未存储为文本的字符在 WordprocessingML 文档中的格式。结束注释]如果省略了此属性，则可以通过任何可用的方法解决这种模糊性。

        [示例：考虑两个运行，其中都包含文本中的省略号，但提示不同。第一个运行在 WordprocessingML 中指定如下：


        <w:r>
            <w:rPr>
                <w:rFonts/>
            </w:rPr>
            <w:t>省略号…</w:t>
        </w:r>
        此文本片段在文档中显示如下：

        123

        第二个运行在 WordprocessingML 中指定如下：


        <w:r>
            <w:rPr>
                <w:rFonts w:hint="eastAsia" />
            </w:rPr>
            <w:t>省略号…</w:t>
        </w:r>
        此文本片段在文档中显示如下：

        123

        尽管两个运行中的“…”具有相同的 Unicode 代码点，但第一个运行使用 ASCII 字体槽，而第二个运行使用 East Asian 字体槽，由提示属性确定。因此，这两个省略号在文档中看起来不同。结束示例]

        [示例：考虑表示段落标记符号的运行，它不作为物理字符存储。因此，可以使用运行指定的任何字体格式化此字符，可以使用以下 WordprocessingML 解决此歧义：


        <w:pPr>
            <w:rPr>
                <w:rFonts w:hint="eastAsia" />
            </w:rPr>
        </w:pPr>

        提示属性指定该运行必须使用针对此范围定义的 eastAsia 字体（主题或非主题，取决于东亚文本的使用情况）。结束示例]

        此属性的可能值由 ST_Hint 简单类型（§17.18.41）定义。
        """
        _val = self.attrib.get(qn('w:hint'))

        if _val is not None:
            return ST_Hint(str(_val))
        return None

    @property
    def ascii(self) -> Optional[str]:
        """ascii（ASCII 字体）

        指定一个字体，用于格式化父运行中 Unicode 代码点范围（U+0000–U+007F）内的所有字符。

        如果还指定了 asciiTheme 属性，则应忽略此属性，并改用该值。

        如果此属性不存在，则默认值是保留在样式层次结构中前一级别应用的格式。如果此属性在样式层次结构中从未应用过，则文本将显示在支持这些字符的任何默认字体中。

        [示例：考虑一个包含此范围内字符的文本运行，必须使用 Courier New 字体显示。在生成的 WordprocessingML 中，应按如下方式指定此要求：


        <w:rPr>
            <w:rFonts w:ascii="Courier New" />
        </w:rPr>
        ascii 属性指定该运行必须使用 Courier New 字体来表示此范围内的所有文本。示例结束]

        此属性的可能值由 ST_String 简单类型（§22.9.2.13）定义。
        """
        _val = self.attrib.get(qn('w:ascii'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def hAnsi(self) -> Optional[str]:
        """hAnsi（高 ANSI 字体）

        指定一个字体，用于格式化父运行中的 Unicode 代码点范围内的所有字符，这些字符不属于上述定义的三个类别之一，在 WordprocessingML 中称为高 ANSI 范围。

        如果还指定了 hAnsiTheme 属性，则应忽略此属性，并改用该值。

        如果此属性不存在，则默认值是保留在样式层次结构中前一级别应用的格式。如果此属性在样式层次结构中从未应用过，则文本将显示在支持高 ANSI 内容的任何默认字体中。

        [示例：考虑一个包含在高 ANSI 范围内的文本运行，必须使用 Bauhaus 93 字体显示。在生成的 WordprocessingML 中，应按如下方式指定此要求：

        <w:rPr>
            <w:rFonts w:hAnsi="Bauhaus 93" />
        </w:rPr>

        hAnsi 属性指定该运行必须使用 Bauhaus 93 字体来表示高 ANSI 范围内的所有文本。示例结束]

        此属性的可能值由 ST_String 简单类型（§22.9.2.13）定义。
        """
        _val = self.attrib.get(qn('w:hAnsi'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def eastAsia(self) -> Optional[str]:
        """eastAsia（东亚字体）

        指定一个字体，用于格式化父运行中东亚 Unicode 代码点范围内的所有字符。

        如果还指定了 eastAsiaTheme 属性，则应忽略此属性，并改用该值。

        如果此属性不存在，则默认值是保留在样式层次结构中前一级别应用的格式。如果此属性在样式层次结构中从未应用过，则文本将显示在支持东亚内容的任何默认字体中。

        [示例：考虑一个包含日文文本的运行，必须使用 MS Mincho 字体显示。在生成的 WordprocessingML 中，应按如下方式指定此要求：


        <w:rPr>
            <w:rFonts w:eastAsia="MS Mincho" />
        </w:rPr>

        eastAsia 属性指定该运行必须使用 MS Mincho 字体来表示东亚范围内的所有文本。示例结束]

        此属性的可能值由 ST_String 简单类型（§22.9.2.13）定义。
        """
        _val = self.attrib.get(qn('w:eastAsia'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def cs(self) -> Optional[str]:
        """cs（复杂文本字体）

        指定一个字体，用于格式化父运行中确定为复杂文本字体槽的所有字符。

        如果还指定了 cstheme 属性，则应忽略此属性，并改用该值。

        如果此属性不存在，则默认值是保留在样式层次结构中前一级别应用的格式。如果此属性在样式层次结构中从未应用过，则文本将显示在支持复杂文本内容的任何默认字体中。

        [示例：考虑一个阿拉伯文本运行，必须使用 Arial Unicode MS 字体显示。在生成的 WordprocessingML 中，应按如下方式指定此要求：


        <w:rPr>
            <w:rFonts w:cs="Arial Unicode MS" />
            <w:cs />
        </w:rPr>

        cs 属性指定该运行必须使用 Arial Unicode MS 字体来表示复杂文本范围内的所有文本。示例结束]

        此属性的可能值由 ST_String 简单类型（§22.9.2.13）定义。
        """
        _val = self.attrib.get(qn('w:cs'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def asciiTheme(self) -> Optional[ST_Theme]:
        """asciiTheme（ASCII 主题字体）

        指定一个主题字体，用于格式化父运行中 Unicode 代码点范围（U+0000–U+007F）内的所有字符。此主题字体是对文档的主题部分中预定义的主题字体之一的引用，允许在文档中集中设置字体信息。

        如果还指定了 ascii 属性，则应忽略该属性，并改用此值。

        如果此属性不存在，则默认值是保留在样式层次结构中前一级别应用的格式。如果此属性在样式层次结构中从未应用过，则文本将显示在由 ascii 属性指定的字体中。

        [示例：考虑一个 ASCII 文本运行，必须使用 majorAscii 主题字体显示。在生成的 WordprocessingML 中，应按如下方式指定此要求：


        <w:rPr>
            <w:rFonts w:asciiTheme="majorAscii" />
        </w:rPr>

        ascii 属性指定该运行必须使用文档主题部分中定义的 majorAscii 主题字体来表示此范围内的所有文本。示例结束]

        此属性的可能值由 ST_Theme 简单类型（§17.18.96）定义。
        """
        _val = self.attrib.get(qn('w:asciiTheme'))

        if _val is not None:
            return ST_Theme(str(_val))
        return None

    @property
    def hAnsiTheme(self) -> Optional[ST_Theme]:
        """hAnsiTheme（高 ANSI 主题字体）

        指定一个主题字体，用于格式化父运行中的 Unicode 代码点范围内的所有字符，这些字符不属于上述定义的三个类别之一，在 WordprocessingML 中称为高 ANSI 范围。此主题字体是对文档的主题部分中预定义的主题字体之一的引用，允许在文档中集中设置字体信息。

        如果还指定了 hAnsi 属性，则应忽略该属性，并改用此值。

        如果此属性不存在，则默认值是保留在样式层次结构中前一级别应用的格式。如果此属性在样式层次结构中从未应用过，则文本将显示在由 hAnsi 属性指定的字体中。

        [示例：考虑一个包含在高 ANSI 范围内的文本运行，必须使用 minorHAnsi 主题字体显示。在生成的 WordprocessingML 中，应按如下方式指定此要求：


        <w:rPr>
            <w:rFonts w:hAnsiTheme="minorHAnsi" />
        </w:rPr>

        hAnsiTheme 属性指定该运行必须使用文档主题部分中定义的 minorHAnsi 主题字体来表示高 ANSI 范围内的所有文本。示例结束]

        此属性的可能值由 ST_Theme 简单类型（§17.18.96）定义。
        """
        _val = self.attrib.get(qn('w:hAnsiTheme'))

        if _val is not None:
            return ST_Theme(str(_val))
        return None

    @property
    def eastAsiaTheme(self) -> Optional[ST_Theme]:
        """eastAsiaTheme（东亚主题字体）

        指定一个主题字体，用于格式化父运行中东亚 Unicode 代码点范围内的所有字符。此主题字体是对文档的主题部分中预定义的主题字体之一的引用，允许在文档中集中设置字体信息。

        如果还指定了 eastAsia 属性，则应忽略该属性，并改用此值。

        如果此属性不存在，则默认值是保留在样式层次结构中前一级别应用的格式。如果此属性在样式层次结构中从未应用过，则文本将显示在由 eastAsia 属性指定的字体中。

        [示例：考虑一个包含日文文本的运行，必须使用 minorEastAsia 主题字体显示。在生成的 WordprocessingML 中，应按如下方式指定此要求：

        <w:rPr>
            <w:rFonts w:eastAsiaTheme="minorEastAsia" />
        </w:rPr>

        eastAsiaTheme 属性指定该运行必须使用文档主题部分中定义的 minorEastAsia 主题字体来表示东亚范围内的所有文本。示例结束]

        此属性的可能值由 ST_Theme 简单类型（§17.18.96）定义。
        """

        _val = self.attrib.get(qn('w:eastAsiaTheme'))

        if _val is not None:
            return ST_Theme(str(_val))
        return None

    @property
    def cstheme(self) -> Optional[ST_Theme]:
        """cstheme（复杂文本主题字体）

        指定一个主题字体，用于格式化父运行中确定为复杂文本字体槽的所有字符。此主题字体是对文档的主题部分中预定义的主题字体之一的引用，允许在文档中集中设置字体信息。

        如果还指定了 cs 属性，则应忽略该属性，并改用此值。

        如果此属性不存在，则默认值是保留在样式层次结构中前一级别应用的格式。如果此属性在样式层次结构中从未应用过，则文本将显示在由 cs 属性指定的字体中。

        [示例：考虑一个阿拉伯文本运行，必须使用 majorBidi 主题字体显示。在生成的 WordprocessingML 中，应按如下方式指定此要求：


        <w:rPr>
            <w:rFonts w:cstheme="majorBidi" />
            <w:cs />
        </w:rPr>

        cstheme 属性指定该运行必须使用文档主题部分中定义的 majorBidi 主题字体来表示复杂文本范围内的所有文本。示例结束]

        此属性的可能值由 ST_Theme 简单类型（§17.18.96）定义。
        """
        _val = self.attrib.get(qn('w:cstheme'))

        if _val is not None:
            return ST_Theme(str(_val))
        return None


class EG_RPrBase(OxmlBaseElement):
    # Union[ CT_Highlight, CT_Em, CT_HpsMeasure, CT_String, CT_SignedHpsMeasure, CT_Underline, CT_Color, CT_OnOff, CT_Language, CT_Fonts, CT_TextEffect, CT_FitText, CT_EastAsianLayout, CT_VerticalAlignRun, CT_Border, CT_SignedTwipsMeasure, CT_TextScale, CT_Shd]
    rpr_base_tags = (
        qn('w:rStyle'),  # CT_String
        qn('w:rFonts'),  # CT_Fonts
        qn('w:b'),  # CT_OnOff
        qn('w:bCs'),  # CT_OnOff
        qn('w:i'),  # CT_OnOff
        qn('w:iCs'),  # CT_OnOff
        qn('w:caps'),  # CT_OnOff
        qn('w:smallCaps'),  # CT_OnOff
        qn('w:strike'),  # CT_OnOff
        qn('w:dstrike'),  # CT_OnOff
        qn('w:outline'),  # CT_OnOff
        qn('w:shadow'),  # CT_OnOff
        qn('w:emboss'),  # CT_OnOff
        qn('w:imprint'),  # CT_OnOff
        qn('w:noProof'),  # CT_OnOff
        qn('w:snapToGrid'),  # CT_OnOff
        qn('w:vanish'),  # CT_OnOff
        qn('w:webHidden'),  # CT_OnOff
        qn('w:color'),  # CT_Color
        qn('w:spacing'),  # CT_SignedTwipsMeasure
        qn('w:w'),  # CT_TextScale
        qn('w:kern'),  # CT_HpsMeasure
        qn('w:position'),  # CT_SignedHpsMeasure
        qn('w:sz'),  # CT_HpsMeasure
        qn('w:szCs'),  # CT_HpsMeasure
        qn('w:highlight'),  # CT_Highlight
        qn('w:u'),  # CT_Underline
        qn('w:effect'),  # CT_TextEffect
        qn('w:bdr'),  # CT_Border
        qn('w:shd'),  # CT_Shd
        qn('w:fitText'),  # CT_FitText
        qn('w:vertAlign'),  # CT_VerticalAlignRun
        qn('w:rtl'),  # CT_OnOff
        qn('w:cs'),  # CT_OnOff
        qn('w:em'),  # CT_Em
        qn('w:lang'),  # CT_Language
        qn('w:eastAsianLayout'),  # CT_EastAsianLayout
        qn('w:specVanish'),  # CT_OnOff
        qn('w:oMath'),  # CT_OnOff
    )

    @property
    def rStyle(self) -> Optional[CT_String]:
        """17.3.2.29 rStyle (引用的字符样式)

        该元素指定了应用于格式化本段落内容的字符样式的样式 ID。

        该格式应用于样式层次结构中的以下位置：

        - 文档默认值
        - 表格样式
        - 编号样式
        - 段落样式
        - 字符样式（该元素）
        - 直接格式化

        这意味着所有在样式元素（§17.7.4.17）中指定的属性，其 styleId 与此元素的 val 属性值相对应的属性，将被应用于层次结构中适当级别的运行。

        如果省略此元素，或者它引用一个不存在的样式，则不会应用任何字符样式于当前段落。此外，如果运行属性是字符样式的一部分，则忽略此属性。

        [示例：考虑以下 WordprocessingML 片段：

        <w:rPr>
            <w:pStyle w:val="TestCharacterStyle" />
            <w:b />
            <w:i />
        </w:rPr>

        该运行指定它继承了具有样式 ID 为 TestCharacterStyle 的段落样式指定的所有运行属性，然后将任何粗体或斜体设置覆盖并应用于该运行。示例结束]
        """

        return getattr(self, qn('w:rStyle'), None)

    @property
    def rFonts(self) -> Optional[CT_Fonts]:
        """17.3.2.26 rFonts (运行字体)

        此元素指定应用于显示此运行的文本内容的字体。在单个运行内，最多可以有四种类型的字体槽，每种类型允许使用唯一的字体：

        - ASCII（即，前 128 个 Unicode 代码点）
        - 高 ANSI
        - 复杂文本
        - 东亚

        如果此元素不存在，则默认值是保留在样式层次结构中前一级别应用的格式。如果此元素在样式层次结构中从未应用过，则文本将显示在支持该字符集的任何默认字体中。

        [示例：考虑一个包含阿拉伯文和英文文本的单个文本运行，可以表示如下：

        <w:r>
            <w:rPr>
                <w:rFonts w:ascii="Courier New" w:cs="Times New Roman" />
            </w:rPr>
            <w:t>English ‫العربية‬</w:t>
        </w:r>

        在此运行中，“English” 和 “‫”العربية‬ 应根据以下两步算法处于 ASCII 字体槽中。因此，它们都应该使用 Courier New 字体。

        相同的内容也可以表示如下：

        <w:r>
            <w:rPr>
                <w:rFonts w:ascii="Courier New" w:cs="Times New Roman" />
            <w:rtl/>
            </w:rPr>
            <w:t>English ‫العربية‬</w:t>
        </w:r>

        在此运行中，“English” 和 “‫”العربية‬ 应根据两步算法处于复杂文本字体槽中。因此，它们都应该使用 Times New Roman 字体。结束示例]

        对于运行中的每个 Unicode 字符，可以使用以下两步方法确定字体槽：

        ....
        """

        return getattr(self, qn('w:rFonts'), None)

    @property
    def bold(self) -> Optional[CT_OnOff]:
        """17.3.2.1 b (粗体)

        该元素指定了在文档中显示时，加粗属性是否应该应用于该运行内容中所有非复杂脚本字符。

        这个格式属性是一个开关属性（§17.7.3）。

        如果此元素不存在，则默认值是保留样式层次结构中先前级别应用的格式。如果在样式层次结构中从未应用此元素，则不应将加粗应用于非复杂脚本字符。

        [示例：考虑一个文本运行，必须为该运行的非复杂脚本内容显式关闭加粗属性。可以使用以下WordprocessingML指定此约束：

        <w:rPr>
            <w:b w:val="false"/>
        </w:rPr>

        该运行明确声明了该运行的非复杂脚本内容的加粗属性为false。示例结束]

        This element’s content model is defined by the common boolean property definition in §17.17.4.
        """
        return getattr(self, qn('w:b'), None)

    @property
    def bCs(self) -> Optional[CT_OnOff]:
        """17.3.2.2 bCs (复杂字体粗体)

        该元素指定了在文档中显示时，加粗属性是否应该应用于该运行内容中所有复杂脚本字符。

        这个格式属性是一个开关属性（§17.7.3）。

        如果此元素不存在，则默认值是保留样式层次结构中先前级别应用的格式。如果在样式层次结构中从未应用此元素，则不应将加粗应用于复杂脚本字符。

        [示例：考虑一个文本运行，必须为该运行的复杂脚本内容显式打开bCs属性（加粗）。可以使用以下WordprocessingML指定此约束：

        <w:rPr>
            <w:bCs w:val="true"/>
        </w:rPr>

        该运行明确声明了bCs属性为true，因此加粗被打开，应用于该运行的复杂脚本内容。示例结束]

        This element’s content model is defined by the common boolean property definition in §17.17.4.
        """
        return getattr(self, qn('w:bCs'), None)

    @property
    def italic(self) -> Optional[CT_OnOff]:
        """17.3.2.16 i (斜体)

        该元素指定在文档中显示时，是否应将斜体属性应用于此运行内容中的所有非复杂脚本字符。

        该格式属性是一个切换属性 (§17.7.3)。

        如果该元素不存在，则默认值是保留样式层次结构中先前级别应用的格式。如果该元素在样式层次结构中从未应用过，则不会将斜体应用于非复杂脚本字符。

        [示例：考虑一个文本运行，其必须明确打开斜体属性以应用于运行的非复杂脚本内容。可以使用以下 WordprocessingML 指定此约束：

        <w:rPr>
            <w:i />
        </w:rPr>

        此运行明确声明了斜体属性对于此运行的非复杂脚本内容为 true。示例结束]

        This element’s content model is defined by the common boolean property definition in §17.17.4.
        """
        return getattr(self, qn('w:i'), None)

    @property
    def iCs(self) -> Optional[CT_OnOff]:
        """17.3.2.17 iCs (复杂字体斜体)

        该元素指定在文档中显示时，是否应将斜体属性应用于此运行内容中的所有复杂脚本字符。

        该格式属性是一个切换属性（§17.7.3）。

        如果该元素不存在，则默认值是保留样式层次结构中先前级别应用的格式。如果该元素在样式层次结构中从未应用过，则不会将斜体应用于复杂脚本字符。

        [示例：考虑一个文本运行，其必须明确打开斜体属性以应用于运行的复杂脚本内容。可以使用以下 WordprocessingML 指定此约束：

        <w:rPr>
            <w:iCs w:val="true"/>
        </w:rPr>

        此运行明确声明了 iCs 属性为 true，因此斜体已应用于此运行的复杂脚本内容。示例结束]

        This element’s content model is defined by the common boolean property definition in §17.17.4.
        """
        return getattr(self, qn('w:iCs'), None)

    @property
    def caps(self) -> Optional[CT_OnOff]:
        """7.3.2.5 caps (将所有字符显示为大写字母)

        caps (Display All Characters As Capital Letters)

        该元素指定了该文本运行中的任何小写字符都应仅格式化为它们的大写字符等效项以供显示。此属性不影响该运行中的任何非字母字符，并且不会更改小写文本的Unicode字符，只会更改其显示方式。

        这个格式属性是一个开关属性（§17.7.3）。

        如果此元素不存在，则默认值是保留样式层次结构中先前级别应用的格式。如果在样式层次结构中从未应用此元素，则字符不会被格式化为大写字母。

        该元素不应与同一运行中的smallCaps（§17.3.2.33）属性一起出现，因为它们在外观上是互斥的。

        [示例：考虑单词Hello, world，它们必须在文档中以全大写形式显示。在WordprocessingML中，可以如下指定此约束：

        <w:r>
            <w:rPr>
                <w:caps w:val="true" />
            </w:rPr>
            <w:t>Hello, world</w:t>
        </w:r>

        即使由于使用了caps元素而在运行内容中使用了小写字符，但此运行显示为HELLO, WORLD。如果删除此属性，则显示原始字符形式（它们不会丢失）。示例结束]

        This element’s content model is defined by the common boolean property definition in §17.17.4.
        """
        return getattr(self, qn('w:caps'), None)

    @property
    def smallCaps(self) -> Optional[CT_OnOff]:
        """17.3.2.33 smallCaps (小号大写字母)¶

        smallCaps (Small Caps)

        这个元素指定了在此文本运行中的所有小写字符都应该被格式化为它们的大写字母等价字符，并且以比实际指定给这段文本的字体大小小两点的字体大小进行显示。该属性不影响此运行中的任何非字母字符，并且不改变小写文本的 Unicode 字符，只是改变了它们的显示方式。如果该字体不能比当前大小小两个点，则将以最小可能的大写字母字体大小显示。

        此格式化属性是一个切换属性(toggle property)(§17.7.3)。

        如果此元素不存在，则默认值是保留在样式层次结构(style hierarchy)中的上一级应用的格式。如果此元素从未在样式层次结构中应用过，则字符不会被格式化为大写字母。

        此元素不应与相同运行中的大写属性(caps (§17.3.2.5) property)同时出现，因为它们在外观上是互斥的。

        [示例：考虑需要在文档中以小型大写字母显示单词“Hello, world”。这个约束在 WordprocessingML 中指定如下：

        <w:r>
            <w:rPr>
                <w:smallCaps w:val="true" />
                <w:sz w:val="24" />
            </w:rPr>
            <w:t>Hello, world</w:t>
        </w:r>

        该运行使用 12 点的大写字母显示首字母 H 和 W，以及 10 点的大写字母显示运行中的小写字母，即使实际运行内容中使用的是小写字符。如果删除此属性，则显示原始字符形式（它们不会丢失）。结束示例]

        该元素的内容模型由 §17.17.4 中的常用布尔属性定义。
        """
        return getattr(self, qn('w:smallCaps'), None)

    @property
    def strike(self) -> Optional[CT_OnOff]:
        """17.3.2.37 strike (单删除线)

        strike (Single Strikethrough)

        该元素指定此运行的内容应该显示为一条横贯线穿过文本中心。

        这种格式化属性是一个切换属性（§17.7.3）。

        如果此元素不存在，则默认值是保留应用于样式层次结构中先前级别的格式。如果此元素在样式层次结构中从未应用过，则删除线将不会应用于此运行的内容。

        此元素不应出现在同一运行中的dstrike（§17.3.2.9）属性中，因为在外观上它们是互斥的。

        [示例：考虑一个文本运行，其内容必须明确地打开删除线属性。可以使用以下 WordprocessingML 指定此约束：

        <w:rPr>
            <w:strike w:val="true"/>
        </w:rPr>

        此运行明确声明删除线属性为 true，因此此运行的内容具有单个水平删除线。示例结束]

        This element’s content model is defined by the common boolean property definition in §17.17.4.
        """
        return getattr(self, qn('w:strike'), None)

    @property
    def dstrike(self) -> Optional[CT_OnOff]:
        """17.3.2.9 dstrike (双删除线)

        dstrike (Double Strikethrough)

        该元素指定此运行的内容应该以每个字符显示两条水平线的形式显示。

        如果该元素不存在，则默认值是保留样式层次结构中先前级别应用的格式。如果该元素在样式层次结构中从未应用过，则不会对该运行的内容应用双删除线。

        此元素不应与同一运行中的删除线属性（§17.3.2.37）一起出现，因为它们在外观上是互斥的。

        [示例：考虑一个文本运行，其内容必须明确打开 dstrike 属性以显示运行的内容。可以使用以下 WordprocessingML 指定此约束：


        此运行明确声明 dstrike 属性为 true，因此该运行的内容具有两条水平删除线。示例结束]

        This element’s content model is defined by the common boolean property definition in §17.17.4.
        """

        return getattr(self, qn('w:dstrike'), None)

    @property
    def outline(self) -> Optional[CT_OnOff]:
        """17.3.2.23 outline (显示字符轮廓)¶

        outline (Display Character Outline)

        该元素指定该运行的内容应该显示为具有轮廓，通过在运行中每个字符字形的内部和外部边框周围绘制一像素宽的边框。该格式化属性是一个切换属性（§17.7.3）。

        如果该元素不存在，则默认值是保留应用于样式层次结构中先前级别的格式。如果该元素在样式层次结构中从未被应用过，则不应将轮廓应用于该运行的内容。

        该元素不应与相同运行中的浮雕（§17.3.2.13）或压痕（§17.3.2.18）属性同时出现，因为它们在外观上是互斥的。

        【示例：考虑一个文本运行，其轮廓属性必须明确关闭。该约束可以使用以下 WordprocessingML 指定：

        <w:rPr>
            <w:outline w:val="false"/>
        </w:rPr>

        该运行明确声明轮廓属性为false，因此该运行的内容不会显示为具有外部轮廓。示例结束】

        This element’s content model is defined by the common boolean property definition in §17.17.4.
        """
        return getattr(self, qn('w:outline'), None)

    @property
    def shadow(self) -> Optional[CT_OnOff]:
        """17.3.2.31 shadow (阴影)

        shadow (Shadow)

        该元素指定此运行的内容应该显示为每个字符都有阴影。对于从左到右的文本，阴影位于文本下方且在其右侧；对于从右到左的文本，阴影位于文本下方且在其左侧。

        这个格式化属性是一个切换属性（§17.7.3）。

        如果此元素不存在，则默认值是保留应用于样式层次结构中先前级别的格式。如果此元素在样式层次结构中从未应用过，则不应将阴影应用于此运行的内容。

        该元素不应与相同运行中的凸出（§17.3.2.13）或浮雕（§17.3.2.18）属性同时出现，因为它们在外观上是互斥的。

        [示例：考虑一个文本运行，其内容必须显式地打开阴影属性。可以使用以下 WordprocessingML 来指定此约束：

        <w:rPr>
            <w:shadow w:val="true"/>
        </w:rPr>

        此运行明确声明了阴影属性为 true，因此此运行的内容将显示为有阴影。示例结束]

        This element’s content model is defined by the common boolean property definition in §17.17.4.
        """
        return getattr(self, qn('w:shadow'), None)

    @property
    def emboss(self) -> Optional[CT_OnOff]:
        """17.3.2.13 emboss (压花)¶

        emboss (Embossing)

        该元素指定此运行的内容应该显示为凸起效果，使文本看起来像是从页面上凸出来的浮雕效果。

        此格式属性是一个开关属性(§17.7.3)。

        如果该元素不存在，则默认值是保留样式层次结构中先前级别应用的格式。如果该元素在样式层次结构中从未应用过，则不会对该运行的内容应用浮雕效果。

        此元素不应与同一运行中的压印或轮廓属性一起出现，因为它们在外观上是互斥的。

        [示例：考虑一个文本运行，其内容必须显式地打开凸起属性。可以使用以下 WordprocessingML 指定此约束：

        <w:rPr>
            <w:emboss w:val="true"/>
        </w:rPr>

        此运行明确声明了凸起属性为 true，因此该运行的内容呈现浮雕效果。示例结束]

        This element’s content model is defined by the common boolean property definition in §17.17.4.
        """
        return getattr(self, qn('w:emboss'), None)

    @property
    def imprint(self) -> Optional[CT_OnOff]:
        """17.3.2.18 imprint (印记)

        该元素指定此运行的内容应该显示为压印效果，使文本看起来像是被印制或压入页面中（也称为“凹版”）。

        该格式属性是一个切换属性(§17.7.3)。

        如果该元素不存在，则默认值是保留样式层次结构中先前级别应用的格式。如果该元素在样式层次结构中从未应用过，则不会将凹印应用于此运行的内容。

        此元素不应与同一运行中的浮雕或轮廓属性一起出现，因为它们在外观上是互斥的。

        [示例：考虑一个文本运行，其必须明确打开压印属性以应用于运行的内容。可以使用以下 WordprocessingML 指定此约束：

        <w:rPr>
            <w:imprint w:val="true"/>
        </w:rPr>

        此运行明确声明了压印属性为 true，因此此运行的内容显示为压印效果。示例结束]

        This element’s content model is defined by the common boolean property definition in §17.17.4.
        """
        return getattr(self, qn('w:imprint'), None)

    @property
    def noProof(self) -> Optional[CT_OnOff]:
        """17.3.2.21 noProof (不检查拼写或语法)

        这个元素指定了当文档被扫描查找拼写和语法错误时，该运行的内容不会报告任何错误。【注：是否通过不检查区域的拼写和语法来实现，或者仅仅是抑制结果，完全取决于使用者/生产者的决定。注释结束】

        如果此元素不存在，则默认值是保留应用于样式层次结构中先前级别的格式。如果在样式层次结构中从未应用过此元素，则该运行的内容中不会抑制拼写和语法错误。

        【示例：考虑一个文本运行，其内容永远不应该报告拼写或语法错误，例如，在 ECMA-376 中包含的 XML 片段。这个约束可以使用以下 WordprocessingML 来指定：

        <w:rPr>
        <w:noProof w:val="true"/>
        </w:rPr>

        该运行明确声明 noProof 属性为 true，因此该运行的内容永远不会报告拼写或语法错误。示例结束】

        This element’s content model is defined by the common boolean property definition in §17.17.4.
        """
        return getattr(self, qn('w:noProof'), None)

    @property
    def snapToGrid(self) -> Optional[CT_OnOff]:
        """17.3.2.34 snapToGrid (使用文档网格设置来设置字符间距)¶

        snapToGrid (Use Document Grid Settings For Inter-Character Spacing)

        该元素指定当前运行是否应使用 docGrid 元素（§17.6.5）中定义的文档网格每行字符设置来布局此运行中的内容。此设置确定是否应根据文档网格中指定的额外字符间距来添加每个字符。

        如果此元素不存在，则默认值是保留应用于样式层次结构中先前级别的格式。如果此元素在样式层次结构中从未应用过，则当父节定义了文档网格时，该运行将使用文档网格设置来布局文本。

        [示例：考虑一个部分中的两个运行，其中文档网格设置为每行允许 20 个字符。该文档网格实际上指定每行必须添加额外的字符间距，以确保结果行仅包含 20 个东亚字符。

        如果在第一个运行上设置了此属性，但在第二个运行上关闭了此属性，如下所示：


        <w:r>
            <w:t>Run One</w:t>
        </w:r>
        <w:r>
            <w:rPr>
                <w:snapToGrid w:val="off" />
            </w:rPr>
            <w:t>Run Two</w:t>
        </w:r>
        则结果文档必须在第一个运行中的每个字符中添加所需的额外字符间距，但在第二个运行中的每个字符中添加零额外字符间距，因为关闭了 snapToGrid 属性。示例结束]

        This element’s content model is defined by the common boolean property definition in §17.17.4.
        """
        return getattr(self, qn('w:snapToGrid'), None)

    @property
    def vanish(self) -> Optional[CT_OnOff]:
        """17.3.2.41 vanish (隐藏文本)

        该元素指定是否在文档显示时将此运行内容隐藏。【注：该设置应影响文本的正常显示，但应用程序可能有设置以强制显示隐藏文本。】

        此格式化属性是一个切换属性（§17.7.3）。

        如果此元素不存在，则默认值是保留应用于样式层次结构中先前级别的格式。如果此元素在样式层次结构中从未应用，则在文档中显示时此文本不应被隐藏。

        【示例：考虑一个文本运行，其内容必须为隐藏文本属性打开。此约束使用以下 WordprocessingML 指定：

        <w:rPr>
            <w:vanish />
        </w:rPr>

        此运行声明 vanish 属性已设置为此运行的内容，因此在显示文档内容时此运行的内容被隐藏。示例结束】

        This element’s content model is defined by the common boolean property definition in §17.17.4.
        """
        return getattr(self, qn('w:vanish'), None)

    @property
    def webHidden(self) -> Optional[CT_OnOff]:
        """17.3.2.44 webHidden (网页隐藏文本)

        这个元素指定了在文档以网页视图（§17.18.102）显示时，此运行的内容是否应在显示时隐藏。【注意：该设置应该影响网页视图中文本的正常显示，但是应用程序可以具有强制显示隐藏文本的设置。结束注意】

        如果此元素不存在，则默认值是保留在样式层次结构中前一个级别应用的格式。如果此元素从未应用于样式层次结构中，则在网页视图中显示文档时，此文本不应被隐藏。

        【示例：考虑一个文本运行，其中运行的内容必须具有隐藏文本属性。可以使用以下 WordprocessingML 指定此约束：

        <w:rPr>
            <w:webHidden />
        </w:rPr>

        结束示例】

        This element’s content model is defined by the common boolean property definition in §17.17.4.
        """
        return getattr(self, qn('w:webHidden'), None)

    @property
    def color(self) -> Optional[CT_Color]:
        """17.3.2.6 color (运行内容颜色)

        该元素指定在文档中显示此运行内容时所使用的颜色。

        此颜色可以明确指定，也可以设置为允许消费者根据运行内容后面的背景颜色自动选择合适的颜色。

        如果此元素不存在，则默认值是保留样式层次结构中先前级别应用的格式。如果在样式层次结构中从未应用此元素，则字符被设置为允许消费者根据运行内容后面的背景颜色自动选择合适的颜色。

        [示例：考虑一个文本运行，其内容应该使用文档的主题部分中的accent3主题颜色显示。在生成的WordprocessingML中，该要求将指定如下：


        <w:rPr>
            <w:color w:themeColor="accent3" />
        </w:rPr>
        color属性指定该运行应使用accent3主题颜色。示例结束]
        """
        return getattr(self, qn('w:color'), None)

    @property
    def spacing(self) -> Optional[CT_SignedTwipsMeasure]:
        """17.3.2.35 spacing (字符间距调整)¶

        spacing (Character Spacing Adjustment)

        该元素指定在文档中呈现本运行的每个字符之前，应添加或移除的字符间距量。此属性产生的效果相当于应用于运行内容的文档网格添加的额外字符间距。

        如果此元素不存在，则默认值是保留应用于样式层次结构中先前级别的格式。如果此元素从未应用于样式层次结构中，则运行的内容不应对任何字符应用额外的字符间距。

        [示例：考虑一个文本运行，其中必须明确地在运行内容中的每个字符之间添加十个点的额外字符间距。可以使用以下 WordprocessingML 指定此约束：

        <w:rPr>
            <w:spacing w:val="200"/>
        </w:rPr>

        此运行明确声明间距值为 200，因此此运行的内容显示为它们之间添加了 10 个额外点的间距。示例结束]
        """
        return getattr(self, qn('w:spacing'), None)

    @property
    def w(self) -> Optional[CT_TextScale]:
        """17.3.2.43 w (展开/收缩文本)¶

        w (Expanded/Compressed Text)

        这个元素指定了在文档中呈现每个字符时应该扩展的量。此属性具有拉伸或压缩运行中每个字符的宽度的功能，而不是通过添加额外字符间距而不改变在行上显示的实际字符宽度的间距(spacing)元素（§17.3.2.35）。

        如果此元素不存在，则默认值是保留在样式层次结构中前一个级别应用的格式。如果此元素从未应用于样式层次结构中，则运行将以其正常宽度的100％显示。

        【示例：考虑一个文本运行，在其中每个字符在显示时必须扩展到其正常宽度的200％。可以使用以下 WordprocessingML 指定此约束：

        <w:rPr>
            <w:w w:val="200%"/>
        </w:rPr>

        这个运行显式声明了 w 值为200％，因此此运行的内容通过拉伸每个字符的宽度以显示为其正常字符宽度的200％。结束示例】
        """
        return getattr(self, qn('w:w'), None)

    @property
    def kern(self) -> Optional[CT_HpsMeasure]:
        """17.3.2.19 kern (字体字距调整)

        该元素指定是否应用字体紧排到此运行的内容。如果指定了它，那么在显示此运行的字符时，紧排将根据需要自动调整。

        val 属性指定了如果指定了此设置，则应自动调整紧排的最小字体大小。如果 sz 元素（§17.3.2.38）中的字体大小小于此值，则不会执行任何字体紧排。

        如果该元素不存在，则默认值是保留样式层次结构中先前级别应用的格式。如果该元素在样式层次结构中从未应用过，则不会将字体紧排应用于此运行的内容。

        [示例：考虑以下具有指定字体紧排属性的 WordprocessingML 运行：


        <w:r>
            <w:rPr>
                <w:kern w:val="28" />
                <w:sz w:val="22" />
            </w:rPr>
        </w:r>

        即使通过 kern 元素打开了字体紧排，但是此运行的内容不应进行紧排，因为该设置仅适用于字体大小为 14 点（28 半点）或更大的字体。如果 kern 元素的 val 属性小于或等于 sz 元素的 val 属性，则将应用紧排：

        <w:r>
            <w:rPr>
                <w:kern w:val="22" />
                <w:sz w:val="22" />
            </w:rPr>
        </w:r>

        示例结束]
        """
        return getattr(self, qn('w:kern'), None)

    @property
    def position(self) -> Optional[CT_SignedHpsMeasure]:
        """17.3.2.24 position (垂直升高或降低的文本)

        position (Vertically Raised or Lowered Text)

        该元素指定相对于周围非定位文本的默认基线，文本应该被提升或降低的量。这允许重新定位文本，而不改变内容的字体大小。

        如果val属性为正数，则父运行将被提升到周围文本的基线上方指定数量的半点。如果val属性为负数，则父运行将被降低到周围文本的基线下方指定数量的半点。

        如果该元素不存在，则默认值是保留应用于样式层次结构中先前级别的格式。如果该元素在样式层次结构中从未被应用过，则相对于该运行内容的默认基线位置，文本不会被提升或降低。

        【示例：考虑一个运行，其内容在显示时必须相对于默认基线位置提升12点。此需求将使用以下 WordprocessingML 指定：

        <w:rPr>
            <w:position w:val="24" />
        </w:rPr>

        由于val属性的内容为正数，因此结果运行将位于默认基线位置上方24个半点。示例结束】
        """
        return getattr(self, qn('w:position'), None)

    @property
    def size(self) -> Optional[CT_HpsMeasure]:
        """17.3.2.38 sz (非复杂脚本字体大小)

        sz (Non-Complex Script Font Size)

        该元素指定在显示时应用于此运行内容中所有非复杂脚本字符的字体大小。此元素的val属性指定的字体大小以半点值表示。

        如果此元素不存在，则默认值是保留在样式层次结构中前一级别应用的字体大小。如果此元素在样式层次结构中从未应用过，则可以为非复杂脚本字符使用任何适当的字体大小。

        [示例：考虑一个文本运行，其非复杂脚本内容必须具有明确的字体大小为13.5点。可以使用以下 WordprocessingML 指定此约束：

        <w:rPr>
            <w:sz w:val="27"/>
        </w:rPr>

        此运行明确声明了sz属性为27半点，用于此运行的非复杂脚本内容，因此文本显示为13.5点字体大小。示例结束]
        """
        return getattr(self, qn('w:sz'), None)

    @property
    def szCs(self) -> Optional[CT_HpsMeasure]:
        """17.3.2.39 szCs (复杂脚本字体大小)

        szCs (Complex Script Font Size)

        该元素指定在显示时应用于此运行内容中所有复杂脚本字符的字体大小。此元素的val属性指定的字体大小以半点值表示。

        如果此元素不存在，则默认值是保留在样式层次结构中前一级别应用的字体大小。如果此元素在样式层次结构中从未应用过，则可以为复杂脚本字符使用任何适当的字体大小。

        [示例：考虑一个文本运行，其复杂脚本内容必须具有明确的字体大小为10点。可以使用以下 WordprocessingML 指定此约束：

        <w:rPr>
        <w:szCs w:val="20"/>
        </w:rPr>

        此运行明确声明了 sz 属性为20半点，用于此运行的复杂脚本内容，因此文本显示为10点字体大小。示例结束]
        """
        return getattr(self, qn('w:szCs'), None)

    @property
    def highlight(self) -> Optional[CT_Highlight]:
        """17.3.2.15 highlight (文本突出显示)¶

        highlight (Text Highlighting)

        该元素指定一个高亮颜色，作为此运行内容背后的背景应用。

        如果此运行具有使用 shd 元素（§17.3.2.32）指定的任何背景阴影，则当显示此运行的内容时，背景阴影将被高亮颜色取代。

        如果该元素不存在，则默认值是保留样式层次结构中先前级别应用的格式。如果该元素在样式层次结构中从未应用过，则不会对该运行的内容应用文本高亮。

        [示例：考虑一个段落中的运行，其中除了应用了运行阴影外，还使用 highlight 元素应用了黄色文本高亮。可以使用以下 WordprocessingML 指定此格式：

        <w:rPr>
            <w:highlight w:val="yellow" />
            <w:shd w:themeFill="accent2" w:themeFillTint="66" />
        </w:rPr>

        结果运行的内容将显示黄色高亮，因为高亮颜色会替代运行内容的阴影。示例结束]
        """
        return getattr(self, qn('w:highlight'), None)

    @property
    def underline(self) -> Optional[CT_Underline]:
        """17.3.2.40 u (下划线)

        该元素指定此运行内容应与下划线一起显示，下划线直接出现在字符高度下方（减去字符所在行上下间距）。

        如果此元素不存在，则默认值是保留在样式层次结构中前一级别应用的格式。如果在样式层次结构中从未应用此元素，则不应将下划线应用于此运行的内容。

        [示例：考虑一个文本运行，其内容必须明确打开双下划线。可以使用以下 WordprocessingML 指定此约束：

        <w:rPr>
            <w:u w:val="double"/>
        </w:rPr>

        此运行明确使用 u 属性声明下划线。下划线的 val 值为 double，因此此运行上的下划线样式必须为双线。示例结束]
        """
        return getattr(self, qn('w:u'), None)

    @property
    def effect(self) -> Optional[CT_TextEffect]:
        """17.3.2.11 effect (动画文字效果)¶

        effect (Animated Text Effect)

        该元素指定在呈现此运行的内容时应该显示的动画文本效果。该效果在运行文本的范围周围呈现，与运行边框在相同位置呈现（如果存在零像素的填充）。

        如果该元素不存在，则默认值是保留样式层次结构中先前级别应用的格式。如果该元素在样式层次结构中从未应用过，则不会对该运行的内容应用任何文本效果。

        [示例：考虑一个文本运行，其必须具有由多个彩色闪烁灯组成的动画文本效果（有关每个效果的描述，请参见可能的属性值）。可以使用以下 WordprocessingML 指定此约束：

        <w:rPr>
            <w:effect w:val="lights"/>
        </w:rPr>

        此运行明确声明效果属性为 lights，因此该运行的内容具有动画闪烁灯文本效果。示例结束]
        """
        return getattr(self, qn('w:effect'), None)

    @property
    def border(self) -> Optional[CT_Border]:
        """17.3.4 边框属性 (CT_Border)

        这个常见的复合类型指定了用于定义对象边框的一组属性。

        【示例：考虑以下运行边框：

        <w:r>
            <w:rPr>
                <w:bdr w:val="single" w:sz="36" w:space="0" w:themeColor="accent1"
                    w:themeTint="66" />
            </w:rPr>
            <w:t xml:space="preserve">run one</w:t>
        </w:r>

        bdr 元素指定了一个带有3.5点宽度的单线边框，使用文档的 accent1 主题颜色。结束示例】
        """
        return getattr(self, qn('w:bdr'), None)

    @property
    def shd(self) -> Optional[CT_Shd]:
        """17.3.5 着色属性 (CT_Shd)¶

        Shading Properties (CT_Shd)

        这个常见的复合类型指定了用于定义对象阴影的一组属性。

        【示例：考虑以下段落的阴影：

        <w:pPr>
            <w:shd w:val="pct20" w:themeColor="accent6" w:themeFill="accent3" />
        </w:pPr>

        生成的段落使用了 accent3 的背景色，在前景图案色 accent6 中使用了 pct20 的模式掩码。结束示例】
        """
        return getattr(self, qn('w:shd'), None)

    @property
    def fitText(self) -> Optional[CT_FitText]:
        """17.3.2.14 fitText (手动运行宽度)¶

        fitText (Manual Run Width)

        该元素指定此运行的内容不应基于其内容的宽度自动显示，而是其内容应调整大小以适应 val 属性指定的宽度。当显示时，应通过等比例增加/减少此运行内容中每个字符的大小来执行此扩展/收缩。

        如果省略了该元素，则此运行的内容将根据其内容的大小进行显示。

        [示例：考虑一个文档，其中有一个运行，必须在正好半英寸的空间中显示，而不考虑其内容。可以使用以下 WordprocessingML 指定此约束：

        <w:r>
            <w:rPr>
                <w:fitText w:id="50" w:val="720" />
            </w:rPr>
            <w:t>This text must be displayed in one-half of an inch.</w:t>
        </w:r>

        当在文档中显示时，结果运行内容必须正好显示为 720 个二十分之一点（半英寸）。示例结束]
        """
        return getattr(self, qn('w:fitText'), None)

    @property
    def vertAlign(self) -> Optional[CT_VerticalAlignRun]:
        """17.3.2.42 vertAlign (下标/上标文本)¶

        vertAlign (Subscript/Superscript Text)

        该元素指定对当前运行内容相对于运行文本的默认外观应用的对齐方式。这允许文本被重新定位为下标或上标，而不改变运行属性的字体大小。

        如果此元素不存在，则默认值是保留应用于样式层次结构中先前级别的格式。如果此元素在样式层次结构中从未应用，则文本相对于运行内容的默认基线位置不应为下标或上标。

        【示例：考虑一个运行，其内容在显示时必须定位为上标。此要求可以使用以下 WordprocessingML 指定：

        <w:rPr>
            <w:vertAlign w:val="superscript" />
        </w:rPr>

        结果运行被定位为上标，因此它以较小的尺寸呈现在运行内容的默认基线位置之上。示例结束】
        """
        return getattr(self, qn('w:vertAlign'), None)

    @property
    def rtl(self) -> Optional[CT_OnOff]:
        """17.3.2.30 rtl (从右到左文本)

        该元素指定此运行的内容是否具有从右到左的特性。具体地，当此元素的 val 属性为 true（或等效值）时，将应用以下行为：

        - 格式化 – 当显示此运行的内容时，所有字符都将视为复杂脚本字符。这意味着将使用 bCs 元素（§17.3.2.2）和 iCs 元素（§17.3.2.17）的值来确定粗体和斜体格式，将使用 rFonts 元素（§17.3.2.26）上的 cs/cstheme 属性来确定字体，以及将使用 szCs 元素（§17.3.2.39）来确定字体大小。

        - 字符方向覆盖 – 当显示此运行的内容时，此属性充当了以下分类的字符的从右到左覆盖（使用 Unicode 字符数据库）：

            - 除了欧洲数字、欧洲数字终止符、常见数字分隔符、阿拉伯数字以及（对于希伯来文本）组成数字的欧洲数字分隔符之外的弱类型。
            - 中性类型

        - [理由：此覆盖允许应用程序存储和利用高级信息，超出了从 Unicode 双向算法隐式推导的信息。例如，如果字符串“first second”出现在文档中的右到左段落中，则 Unicode 算法在显示时始终会导致 “first second”（因为中性字符被强分类字符包围）。然而，如果空白是使用右到左的输入法输入的（例如希伯来键盘），那么可以使用此属性将该字符分类为 RTL，从而允许在右到左段落中显示“second first”，因为用户明确要求在右到左上下文中输入空格。结束理由]

            此元素提供了用于解析单个字符的（Unicode）分类为 L、R、AN 或 EN 的信息。一旦确定了这一点，应该根据 Unicode BiDi 算法的建议对行进行重新排序以保证显示。

        此属性不得与强左到右文本一起使用。在该条件下的任何行为都是未指定的。

        当此属性关闭时，不得与强右到左文本一起使用。在该条件下的任何行为都是未指定的。

        如果此元素不存在，则默认值是保留应用于样式层次结构中先前级别的格式。如果此元素在样式层次结构中从未应用过，则不应将从右到左的特性应用于此运行的内容。

        [示例：考虑以下 WordprocessingML 视觉内容：“first second, ‫ثاني‬ ‫أول‬”。此内容可能如下出现在其父段落中：

        <w:p>
            <w:r>
                <w:t xml:space="preserve">first second, </w:t>
            </w:r>
            <w:r>
                <w:rPr>
                    <w:rtl/>
                </w:rPr>
                <w:t>‫ثاني‬ ‫أول‬</w:t>
            </w:r>
        </w:p>

        第二个运行中的 rtl 元素的存在指定了：

        - 该运行的格式化是使用复杂脚本属性变体指定的。
        - 空白字符被视为从右到左。

        示例结束]

        This element’s content model is defined by the common boolean property definition in §17.17.4.
        """
        return getattr(self, qn('w:rtl'), None)

    @property
    def cs(self) -> Optional[CT_OnOff]:
        """17.3.2.7 cs (在运行时使用复杂的脚本格式)¶

        cs (Use Complex Script Formatting on Run)

        该元素指定了无论其Unicode字符值如何，此运行的内容是否应被视为复杂脚本文本，以确定此运行的格式。

        这意味着在确定结果格式属性时，消费者应使用应用于该运行的复杂脚本格式化（示例：bCs值（§17.3.2.2）而不是b值（§17.3.2.1））。）

        如果此元素不存在，则默认值是保留样式层次结构中先前级别应用的格式。如果在样式层次结构中从未应用此元素，则根据内容的Unicode字符位置设置运行内容为复杂脚本。

        [示例：考虑WordprocessingML文档中的以下英文文本运行：

        <w:r>
            <w:rPr>
                <w:bCs/>
                <w:i/>
                <w:cs/>
            </w:rPr>
            <w:t>some English text</w:t>
        </w:r>

        此运行对复杂脚本字符应用了加粗，对非复杂脚本字符应用了斜体。然而，由于设置了cs属性，因此在确定结果格式时，此运行中的文本必须被视为复杂脚本文本。因此，该运行在显示时具有加粗格式，但没有斜体格式。示例结束]

        This element’s content model is defined by the common boolean property definition in §17.17.4.
        """
        return getattr(self, qn('w:cs'), None)

    @property
    def em(self) -> Optional[CT_Em]:
        """17.3.2.12 em (强调标记)

        em (Emphasis Mark)

        该元素指定应该应用于该运行中的每个非空格字符的强调标记。强调标记是一个附加字符，其显示位置相对于应用的字符是依赖于语言和书写方向的。强调标记由 val 属性的内容指定。如果该元素不存在，则默认值是保留样式层次结构中先前级别应用的格式。如果该元素在样式层次结构中从未应用过，则不会对该运行中的任何字符应用任何强调标记。

        [示例：考虑一个文本运行，其应该具有点形式的强调标记。可以使用以下 WordprocessingML 指定此约束：

        <w:rPr>
            <w:em w:val="dot"/>
        </w:rPr>

        示例结束]
        """
        return getattr(self, qn('w:em'), None)

    @property
    def lang(self) -> Optional[CT_Language]:
        """17.3.2.20 lang (运行内容的语言)

        lang (Languages for Run Content)

        该元素指定在处理此运行的内容时，应使用哪些语言来检查拼写和语法（如果请求）。

        如果该元素不存在，则默认值是保留样式层次结构中先前级别应用的格式。如果该元素在样式层次结构中从未应用过，则将自动根据其内容使用任何所需的方法来确定此运行内容的语言。

        [示例：考虑一个包含拉丁字符和复杂脚本字符的运行。如果这些内容应分别被解释为法语（加拿大）和希伯来语，那么在生成的 WordprocessingML 中，该要求将被指定如下：

        <w:r>
            <w:rPr>
                <w:lang w:val="fr-CA" w:bidi="he-IL" />
            </w:rPr>
        </w:r>

        生成的运行指定了任何复杂脚本内容必须被视为希伯来语进行拼写和语法检查，而任何拉丁字符内容必须被视为法语（加拿大）进行拼写和语法检查。示例结束]
        """
        return getattr(self, qn('w:lang'), None)

    @property
    def eastAsianLayout(self) -> Optional[CT_EastAsianLayout]:
        """17.3.2.10 eastAsianLayout (东亚版式设置)¶

        eastAsianLayout (East Asian Typography Settings)

        该元素指定应用于运行内容的任何东亚排版设置。此元素表示的具体排版设置包括“两行合一”和“横排竖排”选项。

        “两行合一”设置指定该运行中的字符应在文档中的单行上写出，通过在常规行内创建两个子行，并在这些子行之间均匀布局文本来实现。

        [示例：考虑一个段落，其中包含文本“两行合一”，必须在文档中的单个逻辑行内显示。在 WordprocessingML 中，可以将此约束指定为：


        <w:r>
            <w:rPr>
                <w:eastAsianLayout w:id="1" w:combine="on" />
            </w:rPr>
            <w:t>两行合一</w:t>
        </w:r>

        结果文本将显示在其他文本的两个子行内，如下所示：

        [...image...]

        示例结束]

        “横排竖排”设置指定该运行中的字符应在文档中显示时向左旋转 90 度，而在段落中保持与所有其他文本在同一行。

        [示例：考虑一个段落，其中包含文本“this word is vertical”，其中单词“vertical”必须在文档中垂直显示。在 WordprocessingML 中，可以将此约束指定为：

        <w:r>
            <w:rPr>
                <w:eastAsianLayout w:id="2" w:vert="on" />
            </w:rPr>
            <w:t>vertical</w:t>
        </w:r>

        结果文本将与其他文本内容呈 90 度旋转。示例结束]
        """
        return getattr(self, qn('w:eastAsianLayout'), None)

    @property
    def specVanish(self) -> Optional[CT_OnOff]:
        """17.3.2.36 specVanish (段落标记始终隐藏)

        specVanish (Paragraph Mark Is Always Hidden)

        该元素指定给定的运行应始终表现为隐藏，即使当前文档中显示隐藏文本时也是如此。

        此属性仅用于指定段落标记永远不应用于断开段落的末尾以进行显示，即使它在文档中显示，就像通常隐藏的段落未在文档中显示一样。[注意：此属性通常用于确保可以将段落样式应用于段落的一部分，并且仍然显示为目录（在以前的文字处理器中，如果将样式用作字符样式，则会忽略其使用。结束注意] 如果此元素应用于任何其他运行，则可以忽略它。

        如果此元素不存在，则默认值是保留应用于样式层次结构中先前级别的格式。如果此元素从未应用于样式层次结构中，则段落标记的运行属性将不始终被视为隐藏。

        [示例：考虑永远不应用于断开段落的段落标记在文档中。可以使用以下 WordprocessingML 指定此约束：

        <w:pPr>
            <w:rPr>
                <w:specVanish />
            </w:rPr>
        </w:pPr>

        specVanish 元素的存在意味着该段落标记必须始终被视为隐藏（永远不应用于断开段落以进行显示），但可以用于标记段落样式的使用结束。示例结束]

        This element’s content model is defined by the common boolean property definition in §17.17.4.
        """
        return getattr(self, qn('w:specVanish'), None)

    @property
    def oMath(self) -> Optional[CT_OnOff]:
        """17.3.2.22 oMath (Office Open XML 数学)¶

        oMath (Office Open XML Math)

        这个元素指定，这个运行包含的 WordprocessingML 应当被处理，就好像它是 Office Open XML Math 一样。

        【理由：就像其他运行属性可以应用于表示段落标记的字形一样，也可以在空段落上创建一个 Office Open XML Math 方程。由于该段落标记必须由 WordprocessingML 定义，因此无法使用 Office Open XML Math 标记存储该段落。相反，此运行属性存储在段落标记的运行属性上，以指示段落标记是 Office Open XML Math 方程的一部分。例如，下面的第一个段落以 Office Open XML Math 格式存储：

        [123]

        段落必须是一个 p（§17.3.1.22）元素，但这意味着将 Math 标记保存为 WordprocessingML 包时会丢失数据。为了防止数据丢失，此属性将 Math 属性存储为运行属性。理由结束】

        如果此元素不存在，则默认值是保留应用于样式层次结构中先前级别的格式。如果在样式层次结构中从未应用过此元素，则此运行不应被视为 Office Open XML Math。

        此属性可以应用于任何运行，但这只应该在用户界面中引入运行是数学的语义，不应改变文本的外观。

        【示例：考虑一个 WordprocessingML 段落，在该段落中，段落标记字形（段落标记 - ¶）已被格式化为 Math。由于这个标记不是实际的运行，因此无法将其写成 Office Open XML Math 语法，并且必须将其写成实际运行的属性，如下所示：

        <w:pPr>
        <w:rPr>
        <w:oMath />
        </w:rPr>
        </w:pPr>

        因此，此属性用于往返传输此段落标记字符上的数学设置。示例结束】

        This element’s content model is defined by the common boolean property definition in §17.17.4.
        """
        return getattr(self, qn('w:oMath'), None)


class EG_RPrContent(EG_RPrBase):
    """

    <xsd:group name="EG_RPrContent">
        <xsd:sequence>
            <xsd:group ref="EG_RPrBase" minOccurs="0" maxOccurs="unbounded"/>
            <xsd:element name="rPrChange" type="CT_RPrChange" minOccurs="0"/>
        </xsd:sequence>
    </xsd:group>
    """

    @property
    def rpr_content(
        self,
    ) -> list[
        CT_Highlight | CT_Em | CT_HpsMeasure | CT_String | CT_SignedHpsMeasure | CT_Underline | CT_Color | CT_OnOff | CT_Language | CT_Fonts | CT_TextEffect | CT_FitText | CT_EastAsianLayout | CT_VerticalAlignRun | CT_Border | CT_SignedTwipsMeasure | CT_TextScale | CT_Shd
    ]:
        return self.choice_and_more(*EG_RPrBase.rpr_base_tags)  # type: ignore

    @property
    def rPrChange(self) -> Optional[CT_RPrChange]:
        return getattr(self, qn('w:rPrChange'), None)


class CT_RPr(EG_RPrContent): ...


class EG_RPrMath(OxmlBaseElement):
    # Union[CT_RPr, CT_MathCtrlIns, CT_MathCtrlDel]
    rpr_math_tags = (
        qn('w:rPr'),  # CT_RPr
        qn('w:ins'),  # CT_MathCtrlIns
        qn('w:del'),  # CT_MathCtrlDel
    )


class CT_MathCtrlIns(CT_TrackChange):
    @property
    def ctrl_ins(self) -> Optional[CT_RPrChange | CT_RPr]:
        tags = (
            qn('w:del'),  # CT_RPrChange
            qn('w:rPr'),  # CT_RPr
        )

        return self.choice_one_child(*tags)  # type: ignore


class CT_MathCtrlDel(CT_TrackChange):
    @property
    def rPr_run(self) -> Optional[CT_RPr]:
        return getattr(self, qn('w:rPr'), None)


class CT_RPrOriginal(EG_RPrBase):
    """

    <xsd:complexType name="CT_RPrOriginal">
        <xsd:sequence>
            <xsd:group ref="EG_RPrBase" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
    </xsd:complexType>
    """

    @property
    def base(
        self,
    ) -> list[
        CT_Highlight | CT_Em | CT_HpsMeasure | CT_String | CT_SignedHpsMeasure | CT_Underline | CT_Color | CT_OnOff | CT_Language | CT_Fonts | CT_TextEffect | CT_FitText | CT_EastAsianLayout | CT_VerticalAlignRun | CT_Border | CT_SignedTwipsMeasure | CT_TextScale | CT_Shd
    ]:
        return self.choice_and_more(*EG_RPrBase.rpr_base_tags)  # type: ignore


class EG_ParaRPrTrackChanges(OxmlBaseElement):
    @property
    def ins(self) -> Optional[CT_TrackChange]:
        return getattr(self, qn('w:ins'), None)

    @property
    def delete(self) -> Optional[CT_TrackChange]:
        return getattr(self, qn('w:del'), None)

    @property
    def moveFrom(self) -> Optional[CT_TrackChange]:
        return getattr(self, qn('w:moveFrom'), None)

    @property
    def moveTo(self) -> Optional[CT_TrackChange]:
        return getattr(self, qn('w:moveTo'), None)


class CT_ParaRPrOriginal(EG_RPrBase, EG_ParaRPrTrackChanges):
    """

    <xsd:complexType name="CT_ParaRPrOriginal">
        <xsd:sequence>
            <xsd:group ref="EG_ParaRPrTrackChanges" minOccurs="0"/>
            <xsd:group ref="EG_RPrBase" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
    </xsd:complexType>
    """

    @property
    def base(
        self,
    ) -> list[
        CT_Highlight | CT_Em | CT_HpsMeasure | CT_String | CT_SignedHpsMeasure | CT_Underline | CT_Color | CT_OnOff | CT_Language | CT_Fonts | CT_TextEffect | CT_FitText | CT_EastAsianLayout | CT_VerticalAlignRun | CT_Border | CT_SignedTwipsMeasure | CT_TextScale | CT_Shd
    ]:
        return self.choice_and_more(*EG_RPrBase.rpr_base_tags)  # type: ignore


class CT_ParaRPr(EG_RPrContent, EG_ParaRPrTrackChanges):
    """17.3.1.29 rPr (段落标记的运行属性)

    这个元素指定应用于表示该段落标记的字符的字形的一组运行属性。作为文档中的一个实际字符，段落标记可以被格式化，因此应能够像文档中的任何其他字符一样表示这种格式化。

    如果此元素不存在，则段落标记未经格式化，就像文本中的任何其他运行一样。

    【示例：考虑以下显示为以下内容的文本运行，包括使用¶作为段落标记字形的显示格式：

    This is some text and the paragraph mark.¶

    如果我们将段落标记的显示格式化为红色，并给它一个 72 点的字体大小，那么 WordprocessingML 必须在段落中反映这种格式化，如下所示：

    <w:pPr>
        <w:rPr>
            <w:color w:val="FF0000" />
            <w:sz w:val="144" />
        </w:rPr>
    </w:pPr>

    段落标记的格式化存储在段落属性下的 rPr 元素中，因为没有为段落标记本身保存运行。结束示例】

    此元素内容模型（CT_ParaRPr）的 W3C XML Schema 定义位于§A.1。上表中的每个子元素不得超过一次。【注意：由于 W3C XML Schema 语言的限制，此限制未反映在元素的内容模型中。】

    <xsd:complexType name="CT_ParaRPr">
        <xsd:sequence>
            <xsd:group ref="EG_ParaRPrTrackChanges" minOccurs="0"/>
            <xsd:group ref="EG_RPrBase" minOccurs="0" maxOccurs="unbounded"/>
            <xsd:element name="rPrChange" type="CT_ParaRPrChange" minOccurs="0"/>
        </xsd:sequence>
    </xsd:complexType>
    """

    @property
    def rPrChange(self) -> Optional[CT_ParaRPrChange]:
        return getattr(self, qn('w:rPrChange'), None)


class CT_AltChunk(OxmlBaseElement):
    """17.17.2.1 altChunk (导入外部内容的锚点)

    此元素指定文档中的一个位置，用于插入包含外部内容的指定文件的内容，这些内容将被导入到主WordprocessingML文档中。指定文件的内容应出现在文档中的指定位置，从此之后可以作为常规WordprocessingML内容进行处理，而无需区分其来源。要导入的外部内容的位置应由其关系的Id属性与此元素的id属性匹配的关系来指定。

    如果此元素指定的关系的关系类型不是 http://purl.oclc.org/ooxml/officeDocument/relationships/aFChunk，或者不存在，或者没有TargetMode属性值为Internal，那么该文档应被视为不符合规范。如果应用程序无法处理由目标部分指定的内容类型的外部内容，则它应忽略指定的备用内容，但继续处理文件。如果可能，还应提供某种指示，说明未导入未知内容。
    """

    @property
    def altChunkPr(self) -> Optional[CT_AltChunkPr]:
        """17.17.2.2 altChunkPr (外部内容导入属性)

        此元素指定要应用于父altChunk元素指定的外部内容导入的一组属性。在ECMA-376标准中，仅指定了一项属性。

        [示例：考虑一个包含在适当位置具有外部内容导入锚点的WordprocessingML文档：

        ```xml
        <w:body>
            <w:altChunk r:id="altChunk1">
                <w:altChunkPr>
                    <w:matchSrc w:val="false" />
                </w:altChunkPr>
            </w:altChunk>
            <w:p/>
            <w:sectPr>
                …
            </w:sectPr>
        </w:body>
        ```

        altChunkPr 元素指定在导入指定内容时应用于外部内容导入的一组属性。结束示例]
        """

        return getattr(self, qn('w:altChunkPr'), None)

    @property
    def r_id(self) -> Optional[str]:
        """关系ID"""

        _val = self.attrib.get(qn('r:id'))

        if _val is not None:
            return str(_val)
        return None


class CT_AltChunkPr(OxmlBaseElement):
    @property
    def matchSrc(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:matchSrc'), None)


class ST_RubyAlign(ST_BaseEnumType):
    center = 'center'
    distributeLetter = 'distributeLetter'
    distributeSpace = 'distributeSpace'
    left = 'left'
    right = 'right'
    rightVertical = 'rightVertical'


class CT_RubyAlign(OxmlBaseElement):
    @property
    def val(self) -> ST_RubyAlign:
        _val = self.attrib[qn('w:val')]

        return ST_RubyAlign(_val)


class CT_RubyPr(OxmlBaseElement):
    @property
    def rubyAlign(self) -> Optional[CT_RubyAlign]:
        return getattr(self, qn('w:rubyAlign'), None)

    @property
    def hps(self) -> Optional[CT_HpsMeasure]:
        return getattr(self, qn('w:hps'), None)

    @property
    def hpsRaise(self) -> Optional[CT_HpsMeasure]:
        return getattr(self, qn('w:hpsRaise'), None)

    @property
    def hpsBaseText(self) -> Optional[CT_HpsMeasure]:
        return getattr(self, qn('w:rubyAlign'), None)

    @property
    def lid(self) -> Optional[CT_Lang]:
        return getattr(self, qn('w:lid'), None)

    @property
    def dirty(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:dirty'), None)


class EG_RubyContent(OxmlBaseElement):
    """

    <xsd:group name="EG_RubyContent">
        <xsd:choice>
            <xsd:element name="r" type="CT_R"/>
            <xsd:group ref="EG_RunLevelElts" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:choice>
    </xsd:group>
    """

    ruby_content_tags = (qn('w:r'), *EG_RunLevelElts.run_level_elts_choice_tags)  # CT_R

    @property
    def ruby_content(
        self,
    ) -> Optional[CT_R | CT_ProofErr | CT_PermStart | CT_Perm | CT_RunTrackChange]:
        run: Optional[CT_R] = getattr(self, qn('w:r'), None)

        if run is not None:
            return run

        elts: Optional[CT_ProofErr | CT_PermStart | CT_Perm | CT_RunTrackChange] = self.choice_one_child(
            *EG_RunLevelElts.run_level_elts_choice_tags
        )  # type: ignore

        if elts is not None:
            return elts
        return None


class CT_RubyContent(OxmlBaseElement):
    """

    <xsd:complexType name="CT_RubyContent">
        <xsd:group ref="EG_RubyContent" minOccurs="0" maxOccurs="unbounded"/>
    </xsd:complexType>
    """

    @property
    def ruby_content(
        self,
    ) -> list[CT_R | CT_ProofErr | CT_PermStart | CT_Perm | CT_RunTrackChange]:
        return self.choice_and_more(*EG_RubyContent.ruby_content_tags)  # type: ignore


class CT_Ruby(OxmlBaseElement):
    @property
    def rubyPr(self) -> Optional[CT_RubyPr]:
        return getattr(self, qn('w:rubyPr'), None)

    @property
    def rt(self) -> Optional[CT_RubyContent]:
        return getattr(self, qn('w:rt'), None)

    @property
    def rubyBase(self) -> Optional[CT_RubyContent]:
        return getattr(self, qn('w:rubyBase'), None)


class ST_Lock(ST_BaseEnumType):
    sdtLocked = 'sdtLocked'
    contentLocked = 'contentLocked'
    unlocked = 'unlocked'
    sdtContentLocked = 'sdtContentLocked'


class CT_Lock(OxmlBaseElement):
    @property
    def val(self) -> Optional[ST_Lock]:
        _val = self.attrib.get(qn('w:val'))

        if _val is not None:
            return ST_Lock(_val)
        return None


class CT_SdtListItem(OxmlBaseElement):
    @property
    def displayText(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:displayText'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def value(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:value'))

        if _val is not None:
            return str(_val)
        return None


class ST_SdtDateMappingType(ST_BaseEnumType):
    text = 'text'
    date = 'date'
    dateTime = 'dateTime'


class CT_SdtDateMappingType(OxmlBaseElement):
    @property
    def val(self) -> Optional[ST_SdtDateMappingType]:
        _val = self.attrib.get(qn('w:val'))

        if _val is not None:
            return ST_SdtDateMappingType(_val)
        return None


class CT_CalendarType(OxmlBaseElement):
    @property
    def val(self) -> Optional[s_ST_CalendarType]:
        _val = self.attrib.get(qn('w:val'))

        if _val is not None:
            return s_ST_CalendarType(_val)
        return None


class CT_SdtDate(OxmlBaseElement):
    @property
    def dateFormat(self) -> Optional[CT_String]:
        return getattr(self, qn('w:dateFormat'), None)

    @property
    def lid(self) -> Optional[CT_Lang]:
        return getattr(self, qn('w:lid'), None)

    @property
    def storeMappedDataAs(self) -> Optional[CT_SdtDateMappingType]:
        return getattr(self, qn('w:storeMappedDataAs'), None)

    @property
    def calendar(self) -> Optional[CT_CalendarType]:
        return getattr(self, qn('w:calendar'), None)

    @property
    def fullDate(self) -> Optional[ST_DateTime]:
        _val = self.attrib.get(qn('w:fullDate'))

        if _val is not None:
            return to_ST_DateTime(str(_val))
        return None


class CT_SdtComboBox(OxmlBaseElement):
    @property
    def listItem(self) -> list[CT_SdtListItem]:
        return self.findall(qn('w:listItem'))  # type: ignore

    @property
    def lastValue(self) -> str:
        _val = self.attrib.get(qn('w:lastValue'))

        if _val is not None:
            return str(_val)

        return ''


class CT_SdtDocPart(OxmlBaseElement):
    """
    17.5.2.12 docPartList (文档部件图库结构化文档标签)

        该元素指定最近祖先结构化文档标记应为文档部件库类型。

        此设置不要求或暗示结构化文档标记的内容必须仅包含当前计算机上存在的指定库和类别的文档部件的确切内容，它仅用于指定结构化文档标记是此类的，应用程序将使用它来呈现插入到最近祖先结构化文档标记中的可能选择列表。

        【示例：考虑以下结构化文档标记：

        <w:sdt>
            <w:sdtPr>
                …
                <w:docPartList>
                    …
                </w:docPartList>
            </w:sdtPr>
            …
        </w:sdt>

        此结构化文档标记的属性中的docPartList元素指定了结构化文档标记的类型为文档部件库。如果有的话，子元素必须为此列表指定库和类别过滤器。结束示例】

    17.5.2.13 docPartObj (内置文档部件结构化文档标签)

        该元素指定最近祖先结构化文档标记应为文档部件类型。

        此设置不要求或暗示结构化文档标记的内容必须仅包含当前计算机上存在的指定库和类别的文档部件的确切内容，它仅用于指定结构化文档标记是此类的，应用程序将使用它来呈现插入到最近祖先结构化文档标记中的可能选择列表。

        该元素与docPartList元素（§17.5.2.12）不同之处在于，它可用于在WordprocessingML文档中语义标记一组块级对象，而无需通过用户界面指定可与之交换的对象的类别和库。

        【示例：考虑以下结构化文档标记：

        <w:sdt>
            <w:sdtPr>
                …
                <w:docPartObj>
                    …
                </w:docPartObj>
            </w:sdtPr>
            …
        </w:sdt>

        此结构化文档标记的属性中的docPartObj元素指定了结构化文档标记的类型为文档部件。如果有的话，子元素必须为此部分指定库和类别语义。结束示例】
    """

    @property
    def docPartGallery(self) -> Optional[CT_String]:
        """17.5.2.11 docPartGallery (文档部件图库过滤器)

        该元素指定了在确定显示哪些文档部件以供插入到最近祖先结构化文档标记中时，应使用的文档部件库作为过滤器。文档部件库是文档部件的分类，可能会进一步细分为类别。【示例：一个名称为custom1的库可能具有法律条款、一致性条款等类别。结束示例】。将要使用的库存储在此元素的val属性中。

        如果省略了此元素，则最近祖先结构化文档标记将显示其默认库中的所有文档部件。如果存在此元素，但应用程序未找到指定库中的文档部件，则将显示默认库中的文档部件（即，应用程序将表现得好像省略了值）。

        【示例：考虑以下结构化文档标记的属性：

        <w:sdtPr>
            <w:docPartList>
                <w:docPartGallery w:val="custom1"/>
            </w:docPartList>
        </w:sdtPr>

        此结构化文档标记指定它必须通过docPartList元素（§17.5.2.12）提供要插入的文档部件的选择，并且这些文档部件必须仅通过此元素位于custom1库中。结束示例】

        val（字符串值）

            指定其内容包含一个字符串。

            此字符串的内容根据父XML元素的上下文进行解释。

            [示例：考虑以下WordprocessingML片段：

                <w:pPr>
                    <w:pStyle w:val="Heading1" />
                </w:pPr>

            val属性的值是关联段落样式的styleId。

            但是，考虑以下片段：

                <w:sdtPr>
                    <w:alias w:val="SDT Title Example" />
                    …
                </w:sdtPr>

            在这种情况下，val属性中的十进制数是最近祖先结构化文档标记的标题。在每种情况下，该值都是根据父元素的上下文进行解释的。结束示例]

        """

        return getattr(self, qn('w:docPartGallery'), None)

    @property
    def docPartCategory(self) -> Optional[CT_String]:
        """17.5.2.10 docPartCategory (文档部件类别过滤器)

        该元素指定了在确定显示哪些文档部件以供插入到最近祖先结构化文档标记中时，应使用的文档部件类别过滤器。文档部件类别是给定文档部件库中的一个子分类，可用于进一步对给定库中的部件进行分类。【示例：库custom1可能具有法律条款、一致性条款等类别。结束示例】。应用程序存储在此元素的val属性中的类别作为过滤器。

        如果省略了此元素，则最近祖先结构化文档标记将显示指定库中的所有文档部件，而不考虑其指定的类别。如果存在此元素，但应用程序未找到指定库和类别组合的文档部件，则不会显示任何文档部件（即，应用程序不会回退到显示指定库中所有类别的文档部件）。

        【示例：考虑以下结构化文档标记的属性：

            <w:sdtPr>
                <w:docPartList>
                    <w:docPartGallery w:val="custom1"/>
                    <w:docPartCategory w:val="Legal Clauses"/>
                </w:docPartList>
            </w:sdtPr>

        此结构化文档标记指定它必须通过docPartList元素（§17.5.2.12）提供要插入的文档部件的选择，而这些文档部件必须仅通过docPartType元素（§17.5.2.11）位于custom1库中，并且在该库中，仅通过此元素位于名为Legal Clauses的类别中的文档部件。结束示例】
        """
        return getattr(self, qn('w:docPartCategory'), None)

    @property
    def docPartUnique(self) -> Optional[CT_OnOff]:
        """17.5.2.14 docPartUnique (内置文档部件)

        该元素指定此结构化文档标记用于封装内置文档部件（即，此元素出现为docPartObj元素的子元素）。

        【示例：考虑以下结构化文档标记：

        <w:sdt>
            <w:sdtPr>
                …
                <w:docPartObj>
                    …
                    <w:docPartUnique/>
                </w:docPartObj>
            </w:sdtPr>
            …
        </w:sdt>

        此结构化文档标记的属性中的docPartUnique元素指定了结构化文档标记的类型为文档部件的容器。结束示例】
        """
        return getattr(self, qn('w:docPartUnique'), None)


class CT_SdtDropDownList(OxmlBaseElement):
    @property
    def listItem(self) -> list[CT_SdtListItem]:
        return self.findall(qn('w:listItem'))  # type: ignore

    @property
    def lastValue(self) -> str:
        _val = self.attrib.get(qn('w:lastValue'))

        if _val is not None:
            return str(_val)

        return ''


class CT_Placeholder(OxmlBaseElement):
    @property
    def docPart(self) -> Optional[CT_String]:
        return getattr(self, qn('w:docPart'), None)


class CT_SdtText(OxmlBaseElement):
    @property
    def multiLine(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:multiLine'))

        if _val is not None:
            return s_ST_OnOff(str(_val))
        return None


class CT_DataBinding(OxmlBaseElement):
    @property
    def prefixMappings(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:prefixMappings'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def xpath(self) -> str:
        _val = self.attrib[qn('w:xpath')]

        return str(_val)

    @property
    def storeItemID(self) -> str:
        _val = self.attrib[qn('w:storeItemID')]

        return str(_val)


class CT_SdtPr(OxmlBaseElement):
    """17.5.2.38 sdtPr (结构化文档标签属性)

    此元素指定应用于最近的祖先结构化文档标记的属性集。

    【示例：考虑具有以下属性的结构化文档标记：

    <w:sdtPr>
        <w:alias w:val="Birthday"/>
        <w:id w:val="8775518"/>
        <w:date>
            <w:dateFormat w:val="M/d/yyyy"/>
            <w:lid w:val="EN-US"/>
        </w:date>
    </w:sdtPr>

    此结构化文档标记指定了三个属性：通过别名(alias)元素（§17.5.2.1）指定了友好名称为Birthday，通过ID(id)元素（§17.5.2.18）指定了唯一ID为8775518，通过日期(date)元素（§17.5.2.7）指定了日期选择器类型的结构化文档标记，日期元素本身具有一组日期特定的属性。结束示例】
    """

    @property
    def rPr(self) -> Optional[CT_RPr]:
        """17.5.2.28 rPr (结构化文档标记结束字符运行(run)属性)

        该元素指定应用于用于标识结构化文档标记内容结束的字符的一组运行属性。当应用这些属性时，它们将额外应用于通过标记的主属性容器中存储的 rPr 元素（§17.5.2.27）指定的整个结构化文档标记的运行属性。

        如果不存在此元素，则插入的闭合标记将与起始标记具有相同的格式。

        【示例：考虑以下结构化文档标记：

        <w:sdt>
            <w:sdtPr>
                <w:placeholder>
                    <w:docPart w:val="TestPlaceholderDocPart"/>
                </w:placeholder>
                <w:showingPlcHdr/>
                <w:rPr>
                    <w:rStyle w:val="UserName"/>
                </w:rPr>
                …
            </w:sdtPr>
            <w:sdtEndPr>
                <w:rPr>
                    <w:b/>
                    <w:i/>
                </w:rPr>
            </w:sdtEndPr>
            <w:sdtContent>
                …
            </w:sdtContent>
        </w:sdt>

        标记属性下的 rPr 元素指定了该结构化文档标记的起始字符必须具有字符样式 UserName 的格式，并且结束字符必须具有字符样式 UserName 以及粗体和斜体的直接格式化。结束示例】
        """
        return getattr(self, qn('w:rPr'), None)

    @property
    def alias(self) -> Optional[CT_String]:
        return getattr(self, qn('w:alias'), None)

    @property
    def tag(self) -> Optional[CT_String]:
        return getattr(self, qn('w:tag'), None)

    @property
    def id(self) -> Optional[CT_DecimalNumber]:
        return getattr(self, qn('w:id'), None)

    @property
    def lock(self) -> Optional[CT_Lock]:
        return getattr(self, qn('w:lock'), None)

    @property
    def placeholder(self) -> Optional[CT_Placeholder]:
        return getattr(self, qn('w:placeholder'), None)

    @property
    def temporary(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:temporary'), None)

    @property
    def showingPlcHdr(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:showingPlcHdr'), None)

    @property
    def dataBinding(self) -> Optional[CT_DataBinding]:
        return getattr(self, qn('w:dataBinding'), None)

    @property
    def label(self) -> Optional[CT_DecimalNumber]:
        return getattr(self, qn('w:label'), None)

    @property
    def tabIndex(self) -> Optional[CT_UnsignedDecimalNumber]:
        return getattr(self, qn('w:tabIndex'), None)

    @property
    def choice_one(
        self,
    ) -> Optional[
        CT_Empty | CT_SdtComboBox | CT_SdtDate | CT_SdtDocPart | CT_SdtDropDownList | CT_SdtText
    ]:
        tags = (
            qn('w:equation'),  # CT_Empty
            qn('w:comboBox'),  # CT_SdtComboBox
            qn('w:date'),  # CT_SdtDate
            qn('w:docPartObj'),  # CT_SdtDocPart
            qn('w:docPartList'),  # CT_SdtDocPart
            qn('w:dropDownList'),  # CT_SdtDropDownList
            qn('w:picture'),  # CT_Empty
            qn('w:richText'),  # CT_Empty
            qn('w:text'),  # CT_SdtText
            qn('w:citation'),  # CT_Empty
            qn('w:group'),  # CT_Empty
            qn('w:bibliography'),  # CT_Empty
        )

        return self.choice_one_child(*tags)  # type: ignore


class CT_SdtEndPr(OxmlBaseElement):
    @property
    def rPr(self) -> list[CT_RPr]:
        return self.findall(qn('w:rPr'))  # type: ignore


class EG_ContentRunContent(EG_RunLevelElts):
    """

    <xsd:group name="EG_ContentRunContent">
        <xsd:choice>
            <xsd:element name="customXml" type="CT_CustomXmlRun"/>
            <xsd:element name="smartTag" type="CT_SmartTagRun"/>
            <xsd:element name="sdt" type="CT_SdtRun"/>
            <xsd:element name="dir" type="CT_DirContentRun"/>
            <xsd:element name="bdo" type="CT_BdoContentRun"/>
            <xsd:element name="r" type="CT_R"/>
            <xsd:group ref="EG_RunLevelElts" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:choice>
    </xsd:group>
    """

    # Union[CT_CustomXmlRun, CT_SmartTagRun, CT_SdtRun, CT_DirContentRun, CT_BdoContentRun, CT_R, CT_ProofErr, CT_PermStart, CT_Perm, CT_RunTrackChange, CT_Bookmark, CT_MarkupRange, CT_MoveBookmark,CT_TrackChange, CT_Markup]
    content_run_content_tags = (
        qn('w:customXml'),  # CT_CustomXmlRun
        qn('w:smartTag'),  # CT_SmartTagRun
        qn('w:sdt'),  # CT_SdtRun
        qn('w:dir'),  # CT_DirContentRun
        qn('w:bdo'),  # CT_BdoContentRun
        qn('w:r'),  # CT_R
        *EG_RunLevelElts.run_level_elts_choice_tags,
    )

    @property
    def customXml(self) -> Optional[CT_CustomXmlRun]:
        return getattr(self, qn('w:customXml'), None)

    @property
    def smartTag(self) -> Optional[CT_SmartTagRun]:
        return getattr(self, qn('w:smartTag'), None)

    @property
    def sdt(self) -> Optional[CT_SdtRun]:
        return getattr(self, qn('w:sdt'), None)

    @property
    def dir(self) -> Optional[CT_DirContentRun]:
        return getattr(self, qn('w:dir'), None)

    @property
    def bdo(self) -> Optional[CT_BdoContentRun]:
        return getattr(self, qn('w:bdo'), None)

    @property
    def r(self) -> list[CT_R]:
        return self.findall(qn('w:r'))  # type: ignore


class CT_DirContentRun(OxmlBaseElement):
    @property
    def p_content(
        self,
    ) -> CT_CustomXmlRun | CT_SmartTagRun | CT_SdtRun | CT_DirContentRun | CT_BdoContentRun | CT_R | CT_ProofErr | CT_PermStart | CT_Perm | CT_RunTrackChange | CT_Bookmark | CT_MarkupRange | CT_MoveBookmark | CT_TrackChange | CT_Markup | CT_SimpleField | CT_Hyperlink | CT_Rel:
        return self.choice_and_more(*EG_PContent.p_content_choice_tags)  # type: ignore

    @property
    def val(self) -> Optional[ST_Direction]:
        _val = self.attrib.get(qn('w:val'))

        if _val is not None:
            return ST_Direction(str(_val))
        return None


class CT_BdoContentRun(OxmlBaseElement):
    @property
    def p_content(
        self,
    ) -> CT_CustomXmlRun | CT_SmartTagRun | CT_SdtRun | CT_DirContentRun | CT_BdoContentRun | CT_R | CT_ProofErr | CT_PermStart | CT_Perm | CT_RunTrackChange | CT_Bookmark | CT_MarkupRange | CT_MoveBookmark | CT_TrackChange | CT_Markup | CT_SimpleField | CT_Hyperlink | CT_Rel:
        return self.choice_and_more(*EG_PContent.p_content_choice_tags)  # type: ignore

    @property
    def val(self) -> Optional[ST_Direction]:
        _val = self.attrib.get(qn('w:val'))

        if _val is not None:
            return ST_Direction(str(_val))
        return None


class ST_Direction(ST_BaseEnumType):
    ltr = 'ltf'
    rtl = 'rtl'


class CT_SdtContentRun(OxmlBaseElement):
    """17.5.2.36 sdtContent (内联级结构化文档标签内容)

    该元素指定了围绕一个或多个内联级别结构（例如运行、DrawingML 对象、字段等）的结构化文档标记的最后已知内容。该元素的内容应被视为结构化文档标记中要显示的内容的缓存，原因如下：

    - 如果结构化文档标记通过 dataBinding 元素（§17.5.2.6）指定了 XML 映射，则自定义 XML 数据部分的更改应根据需要反映在结构化文档标记中。
    - 如果结构化文档标记的内容是通过 showingPlcHdr 元素（§17.5.2.39）作为占位符文本，则此内容可以使用存储在词汇表文档部分中的占位符文本进行更新。

    【示例：考虑一个在 WordprocessingML 文档中围绕两个运行的友好名称为 "firstName" 的结构化文档标记。该需求可以在 WordprocessingML 中如下指定：

    <w:p>
        <w:sdt>
            <w:sdtPr>
                <w:alias w:val="firstName"/>
            </w:sdtPr>
            <w:sdtContent>
                <w:r>
                    …
                </w:r>
                <w:r>
                    …
                </w:r>
            </w:sdtContent>
        </w:sdt>
        …
    </w:p>

    sdtContent 元素包含了两个相邻的运行（即一个内联级别的结构化文档标记内容容器）。】
    """

    @property
    def p_content(
        self,
    ) -> list[
        CT_CustomXmlRun | CT_SmartTagRun | CT_SdtRun | CT_DirContentRun | CT_BdoContentRun | CT_R | CT_ProofErr | CT_PermStart | CT_Perm | CT_RunTrackChange | CT_Bookmark | CT_MarkupRange | CT_MoveBookmark | CT_TrackChange | CT_Markup | CT_SimpleField | CT_Hyperlink | CT_Rel
    ]:
        return self.choice_and_more(*EG_PContent.p_content_choice_tags)  # type: ignore


class CT_SdtContentBlock(EG_ContentBlockContent):
    """17.5.2.34 sdtContent (块级结构化文档标签内容)

    该元素指定了围绕一个或多个块级结构（段落、表格等）的结构化文档标记的最后已知内容。该元素的内容应被视为结构化文档标记中要显示的内容的缓存，原因如下：

    - 如果结构化文档标记通过 dataBinding 元素（§17.5.2.6）指定了 XML 映射，则应根据需要反映在结构化文档标记中的自定义 XML 数据部分的更改
    - 如果结构化文档标记的内容是通过 showingPlcHdr 元素（§17.5.2.39）设置的占位符文本，则此内容可以使用存储在术语表文档部分中的占位符文本进行更新

    【示例：考虑一个在 WordprocessingML 文档中围绕单个段落的友好名称为 "address" 的结构化文档标记。该需求可以在 WordprocessingML 中如下指定：

    <w:body>
        <w:sdt>
            <w:sdtPr>
                <w:alias w:val="address"/>
            </w:sdtPr>
            <w:sdtContent>
                <w:p>
                    …
                </w:p>
            </w:sdtContent>
        </w:sdt>
        …
    </w:body>

    sdtContent 元素包含了一个单个段落（即一个块级结构化文档标记内容容器）。】
    """

    @property
    def content_block(
        self,
    ) -> list[
        CT_CustomXmlBlock | CT_SdtBlock | CT_P | CT_Tbl | CT_ProofErr | CT_PermStart | CT_Perm | CT_RunTrackChange
    ]:
        """块级结构化标签内容"""

        return self.choice_and_more(*EG_ContentBlockContent.content_block_tags)  # type: ignore


class EG_ContentRowContent(EG_RunLevelElts):
    """

    <xsd:group name="EG_ContentRowContent">
        <xsd:choice>
            <xsd:element name="tr" type="CT_Row" minOccurs="0" maxOccurs="unbounded"/>
            <xsd:element name="customXml" type="CT_CustomXmlRow"/>
            <xsd:element name="sdt" type="CT_SdtRow"/>
            <xsd:group ref="EG_RunLevelElts" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:choice>
    </xsd:group>
    """

    # Union[CT_Row, CT_CustomXmlRow, CT_SdtRow, CT_ProofErr, CT_PermStart, CT_Perm, CT_RunTrackChange, CT_Bookmark, CT_MarkupRange, CT_MoveBookmark,CT_TrackChange, CT_Markup]
    content_row_content_choice_tags = (
        qn('w:tr'),  # CT_Row
        qn('w:customXml'),  # CT_CustomXmlRow
        qn('w:sdt'),  # CT_SdtRow
        *EG_RunLevelElts.run_level_elts_choice_tags,
    )

    @property
    def tr_lst(self) -> list[CT_Row]:
        return self.findall(qn('w:tr'))  # type: ignore

    @property
    def customXml(self) -> Optional[CT_CustomXmlRow]:
        return getattr(self, qn('w:customXml'), None)

    @property
    def sdt(self) -> Optional[CT_SdtRow]:
        return getattr(self, qn('w:sdt'), None)


class CT_SdtContentRow(OxmlBaseElement):
    """17.5.2.35 sdtContent (行级结构化文档标签内容)

    该元素指定了围绕单个表格行的结构化文档标记的最后已知内容。

    【注意：与其他类型的结构化文档标记不同，这种类型的结构化文档标记不能显示占位符文本或具有映射的 XML 数据，因此它永远不是一个缓存。】

    【示例：考虑一个在 WordprocessingML 文档中围绕单个表格行的友好名称为 "invoiceItem" 的结构化文档标记。该需求可以在 WordprocessingML 中如下指定：

    <w:tbl>
        <w:sdt>
            <w:sdtPr>
                <w:alias w:val="invoiceItem"/>
            </w:sdtPr>
            <w:sdtContent>
                <w:tr>
                    …
                </w:tr>
            </w:sdtContent>
        </w:sdt>
        …
    </w:tbl>

    sdtContent 元素包含了一个单个表格行（即一个行级别结构化文档标记内容容器）。】


    <xsd:complexType name="CT_SdtContentRow">
        <xsd:group ref="EG_ContentRowContent" minOccurs="0" maxOccurs="unbounded"/>
    </xsd:complexType>
    """

    @property
    def content_row(
        self,
    ) -> Optional[
        CT_Row | CT_CustomXmlRow | CT_SdtRow | CT_ProofErr | CT_PermStart | CT_Perm | CT_RunTrackChange
    ]:
        return self.choice_and_more(*EG_ContentRowContent.content_row_content_choice_tags)  # type: ignore


class EG_ContentCellContent(EG_RunLevelElts):
    """

    <xsd:group name="EG_ContentCellContent">
        <xsd:choice>
            <xsd:element name="tc" type="CT_Tc" minOccurs="0" maxOccurs="unbounded"/>
            <xsd:element name="customXml" type="CT_CustomXmlCell"/>
            <xsd:element name="sdt" type="CT_SdtCell"/>
            <xsd:group ref="EG_RunLevelElts" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:choice>
    </xsd:group>
    """

    # Union[CT_Tc, CT_CustomXmlCell, CT_SdtCell, CT_ProofErr, CT_PermStart, CT_Perm, CT_RunTrackChange, CT_Bookmark, CT_MarkupRange, CT_MoveBookmark,CT_TrackChange, CT_Markup]
    content_cell_content_choice_tags = (
        qn('w:tc'),  # CT_Tc
        qn('w:customXml'),  # CT_CustomXmlCell
        qn('w:sdt'),  # CT_SdtCell
        *EG_RunLevelElts.run_level_elts_choice_tags,
    )

    @property
    def tc_lst(self) -> list[CT_Tc]:
        return self.findall(qn('w:tc'))  # type: ignore

    @property
    def customXml(self) -> Optional[CT_CustomXmlCell]:
        return getattr(self, qn('w:customXml'), None)

    @property
    def sdt(self) -> Optional[CT_SdtCell]:
        return getattr(self, qn('w:sdt'), None)


class CT_SdtContentCell(EG_ContentCellContent):
    """该元素指定了围绕单个表格单元格的结构化文档标记的最后已知内容。该元素的内容应被视为结构化文档标记中要显示的内容的缓存，原因如下：

    - 如果结构化文档标记通过 dataBinding 元素（§17.5.2.6）指定了 XML 映射，则应根据需要反映在结构化文档标记中的自定义 XML 数据部分的更改
    - 如果结构化文档标记的内容是通过 showingPlcHdr 元素（§17.5.2.39）设置的占位符文本，则此内容可以使用存储在术语表文档部分中的占位符文本进行更新

    【示例：考虑一个在 WordprocessingML 文档中围绕单个表格单元格的友好名称为 "company" 的结构化文档标记。该需求可以在 WordprocessingML 中如下指定：

        <w:tr>
            <w:sdt>
                <w:sdtPr>
                    <w:alias w:val="company"/>
                </w:sdtPr>
                <w:sdtContent>
                    <w:tc>
                        …
                    </w:tc>
                </w:sdtContent>
            </w:sdt>
            …
        </w:tr>

    sdtContent 元素包含了一个单个表格单元格（即一个单元格级结构化文档标记内容容器）。】
    """

    @property
    def content_cell(
        self,
    ) -> Optional[
        CT_Tc | CT_CustomXmlCell | CT_SdtCell | CT_ProofErr | CT_PermStart | CT_Perm | CT_RunTrackChange
    ]:
        return self.choice_and_more(*EG_ContentCellContent.content_cell_content_choice_tags)  # type: ignore


class CT_SdtBlock(OxmlBaseElement):
    """17.5.2.29 sdt (块级结构化文档标签)

    该元素指定一个结构化文档标记，围绕一个或多个块级结构（段落、表格等）。

    该元素的两个子元素应通过 sdtPr 和 sdtContent 元素分别用于指定当前结构化文档标记的属性和内容。

    【示例：考虑一个友好名称为 "address" 的结构化文档标记，必须位于 WordprocessingML 文档中的单个段落周围。在 WordprocessingML 中，可以如下指定该要求：

    <w:body>
        <w:sdt>
            <w:sdtPr>
                <w:alias w:val="address"/>
            </w:sdtPr>
            <w:sdtContent>
            <w:p>
                …
            </w:p>
            </w:sdtContent>
        </w:sdt>
        …
    </w:body>

    sdt 元素指定了结构化文档标记，子 sdtPr 元素包含了 friendly name 属性，其值为 address，而 sdtContent 元素包含了一个段落（这是一个块级结构化文档标记）。结束示例】
    """

    @property
    def sdtPr(self) -> Optional[CT_SdtPr]:
        """17.5.2.38 sdtPr (结构化文档标签属性)

        此元素指定应用于最近的祖先结构化文档标记的属性集。

        【示例：考虑具有以下属性的结构化文档标记：

        <w:sdtPr>
            <w:alias w:val="Birthday"/>
            <w:id w:val="8775518"/>
            <w:date>
                <w:dateFormat w:val="M/d/yyyy"/>
                <w:lid w:val="EN-US"/>
            </w:date>
        </w:sdtPr>

        此结构化文档标记指定了三个属性：通过别名(alias)元素（§17.5.2.1）指定了友好名称为Birthday，通过ID(id)元素（§17.5.2.18）指定了唯一ID为8775518，通过日期(date)元素（§17.5.2.7）指定了日期选择器类型的结构化文档标记，日期元素本身具有一组日期特定的属性。结束示例】
        """

        return getattr(self, qn('w:sdtPr'), None)

    @property
    def sdtEndPr(self) -> Optional[CT_SdtEndPr]:
        """17.5.2.37 sdtEndPr (结构化文档标签结束字符属性)

        该元素指定应用于结构化文档标记结束符的物理字符的属性。

        【示例：考虑一个具有以下属性的结构化文档标记的结束标记：

        <w:sdtEndPr>
            <w:rPr>
                …
            </w:rPr>
        </w:sdtEndPr>

        此结构化文档标记在 sdtEndPr 元素中指定了其结束字符的属性。】
        """

        return getattr(self, qn('w:sdtEndPr'))

    @property
    def sdtContent_block(self) -> Optional[CT_SdtContentBlock]:
        """17.5.2.34 sdtContent (块级结构化文档标签内容)

        该元素指定了围绕一个或多个块级结构（段落、表格等）的结构化文档标记的最后已知内容。该元素的内容应被视为结构化文档标记中要显示的内容的缓存，原因如下：

        - 如果结构化文档标记通过 dataBinding 元素（§17.5.2.6）指定了 XML 映射，则应根据需要反映在结构化文档标记中的自定义 XML 数据部分的更改
        - 如果结构化文档标记的内容是通过 showingPlcHdr 元素（§17.5.2.39）设置的占位符文本，则此内容可以使用存储在术语表文档部分中的占位符文本进行更新

        【示例：考虑一个在 WordprocessingML 文档中围绕单个段落的友好名称为 "address" 的结构化文档标记。该需求可以在 WordprocessingML 中如下指定：

        <w:body>
            <w:sdt>
                <w:sdtPr>
                    <w:alias w:val="address"/>
                </w:sdtPr>
                <w:sdtContent>
                    <w:p>
                        …
                    </w:p>
                </w:sdtContent>
            </w:sdt>
            …
        </w:body>

        sdtContent 元素包含了一个单个段落（即一个块级结构化文档标记内容容器）。】
        """

        return getattr(self, qn('w:sdtContent'), None)


class CT_SdtRun(OxmlBaseElement):
    """17.5.2.31 sdt (内联级结构化文档标签)

    该元素指定了围绕当前段落中一个或多个内联级结构（例如运行、DrawingML 对象、字段等）的结构化文档标记的存在。该元素的两个子元素将用于通过 sdtPr 和 sdtContent 元素指定当前结构化文档标记的属性和内容。

    【示例：考虑一个在 WordprocessingML 文档中围绕两个运行的友好名称为 "firstName" 的结构化文档标记。该需求可以在 WordprocessingML 中如下指定：

    <w:p>
        <w:sdt>
            <w:sdtPr>
                <w:alias w:val="firstName"/>
            </w:sdtPr>
            <w:sdtContent>
                <w:r>
                    …
                </w:r>
                <w:r>
                    …
                </w:r>
            </w:sdtContent>
        </w:sdt>
        …
    </w:p>

    在这个示例中，sdt 元素指定了结构化文档标记，子元素 sdtPr 包含了 friendly name 属性设置为 firstName，而 sdtContent 元素包含了两个运行（即一个内联级结构化文档标记）。】
    """

    @property
    def sdtPr(self) -> Optional[CT_SdtPr]:
        """17.5.2.38 sdtPr (结构化文档标签属性)

        此元素指定应用于最近的祖先结构化文档标记的属性集。

        【示例：考虑具有以下属性的结构化文档标记：

        <w:sdtPr>
            <w:alias w:val="Birthday"/>
            <w:id w:val="8775518"/>
            <w:date>
                <w:dateFormat w:val="M/d/yyyy"/>
                <w:lid w:val="EN-US"/>
            </w:date>
        </w:sdtPr>

        此结构化文档标记指定了三个属性：通过别名(alias)元素（§17.5.2.1）指定了友好名称为Birthday，通过ID(id)元素（§17.5.2.18）指定了唯一ID为8775518，通过日期(date)元素（§17.5.2.7）指定了日期选择器类型的结构化文档标记，日期元素本身具有一组日期特定的属性。结束示例】
        """

        return getattr(self, qn('w:sdtPr'), None)

    @property
    def sdtEndPr(self) -> Optional[CT_SdtEndPr]:
        """17.5.2.37 sdtEndPr (结构化文档标签结束字符属性)

        该元素指定应用于结构化文档标记结束符的物理字符的属性。

        【示例：考虑一个具有以下属性的结构化文档标记的结束标记：

        <w:sdtEndPr>
            <w:rPr>
                …
            </w:rPr>
        </w:sdtEndPr>

        此结构化文档标记在 sdtEndPr 元素中指定了其结束字符的属性。】
        """

        return getattr(self, qn('w:sdtEndPr'), None)

    @property
    def sdtContent_run(self) -> Optional[CT_SdtContentRun]:
        """17.5.2.36 sdtContent (内联级结构化文档标签内容)

        该元素指定了围绕一个或多个内联级别结构（例如运行、DrawingML 对象、字段等）的结构化文档标记的最后已知内容。该元素的内容应被视为结构化文档标记中要显示的内容的缓存，原因如下：

        - 如果结构化文档标记通过 dataBinding 元素（§17.5.2.6）指定了 XML 映射，则自定义 XML 数据部分的更改应根据需要反映在结构化文档标记中。
        - 如果结构化文档标记的内容是通过 showingPlcHdr 元素（§17.5.2.39）作为占位符文本，则此内容可以使用存储在词汇表文档部分中的占位符文本进行更新。

        【示例：考虑一个在 WordprocessingML 文档中围绕两个运行的友好名称为 "firstName" 的结构化文档标记。该需求可以在 WordprocessingML 中如下指定：

        <w:p>
            <w:sdt>
                <w:sdtPr>
                    <w:alias w:val="firstName"/>
                </w:sdtPr>
                <w:sdtContent>
                    <w:r>
                        …
                    </w:r>
                    <w:r>
                        …
                    </w:r>
                </w:sdtContent>
            </w:sdt>
            …
        </w:p>

        sdtContent 元素包含了两个相邻的运行（即一个内联级别的结构化文档标记内容容器）。】
        """

        return getattr(self, qn('w:sdtContent'), None)


class CT_SdtCell(OxmlBaseElement):
    """17.5.2.32 sdt (单元格级结构化文档标签)

    该元素指定了围绕单个表格单元格的结构化文档标记的存在。该元素的两个子元素将用于通过 sdtPr 和 sdtContent 元素指定当前结构化文档标记的属性和内容。

    【示例：考虑一个在 WordprocessingML 文档中围绕单个表格单元格的友好名称为 "company" 的结构化文档标记。该需求可以在 WordprocessingML 中如下指定：

    <w:tr>
        <w:sdt>
            <w:sdtPr>
                <w:alias w:val="company"/>
            </w:sdtPr>
            <w:sdtContent>
                <w:tc>
                    …
                </w:tc>
            </w:sdtContent>
        </w:sdt>
        …
    </w:tr>

    在这个示例中，sdt 元素指定了结构化文档标记，子元素 sdtPr 包含了 friendly name 属性设置为 company，而 sdtContent 元素包含了一个单个表格单元格（即一个单元格级结构化文档标记）。】
    """

    @property
    def sdtPr(self) -> Optional[CT_SdtPr]:
        """17.5.2.38 sdtPr (结构化文档标签属性)

        此元素指定应用于最近的祖先结构化文档标记的属性集。

        【示例：考虑具有以下属性的结构化文档标记：

        <w:sdtPr>
            <w:alias w:val="Birthday"/>
            <w:id w:val="8775518"/>
            <w:date>
                <w:dateFormat w:val="M/d/yyyy"/>
                <w:lid w:val="EN-US"/>
            </w:date>
        </w:sdtPr>

        此结构化文档标记指定了三个属性：通过别名(alias)元素（§17.5.2.1）指定了友好名称为Birthday，通过ID(id)元素（§17.5.2.18）指定了唯一ID为8775518，通过日期(date)元素（§17.5.2.7）指定了日期选择器类型的结构化文档标记，日期元素本身具有一组日期特定的属性。结束示例】
        """

        return getattr(self, qn('w:sdtPr'), None)

    @property
    def sdtEndPr(self) -> Optional[CT_SdtEndPr]:
        """17.5.2.37 sdtEndPr (结构化文档标签结束字符属性)

        该元素指定应用于结构化文档标记结束符的物理字符的属性。

        【示例：考虑一个具有以下属性的结构化文档标记的结束标记：

        <w:sdtEndPr>
            <w:rPr>
                …
            </w:rPr>
        </w:sdtEndPr>

        此结构化文档标记在 sdtEndPr 元素中指定了其结束字符的属性。】
        """

        return getattr(self, qn('w:sdtEndPr'), None)

    @property
    def sdtContent_cell(self) -> Optional[CT_SdtContentCell]:
        """该元素指定了围绕单个表格单元格的结构化文档标记的最后已知内容。该元素的内容应被视为结构化文档标记中要显示的内容的缓存，原因如下：

        - 如果结构化文档标记通过 dataBinding 元素（§17.5.2.6）指定了 XML 映射，则应根据需要反映在结构化文档标记中的自定义 XML 数据部分的更改
        - 如果结构化文档标记的内容是通过 showingPlcHdr 元素（§17.5.2.39）设置的占位符文本，则此内容可以使用存储在术语表文档部分中的占位符文本进行更新

        【示例：考虑一个在 WordprocessingML 文档中围绕单个表格单元格的友好名称为 "company" 的结构化文档标记。该需求可以在 WordprocessingML 中如下指定：

            <w:tr>
                <w:sdt>
                    <w:sdtPr>
                        <w:alias w:val="company"/>
                    </w:sdtPr>
                    <w:sdtContent>
                        <w:tc>
                            …
                        </w:tc>
                    </w:sdtContent>
                </w:sdt>
                …
            </w:tr>

        sdtContent 元素包含了一个单个表格单元格（即一个单元格级结构化文档标记内容容器）。】
        """

        return getattr(self, qn('w:sdtContent'), None)


class CT_SdtRow(OxmlBaseElement):
    @property
    def sdtPr(self) -> Optional[CT_SdtPr]:
        """17.5.2.38 sdtPr (结构化文档标签属性)

        此元素指定应用于最近的祖先结构化文档标记的属性集。

        【示例：考虑具有以下属性的结构化文档标记：

        <w:sdtPr>
            <w:alias w:val="Birthday"/>
            <w:id w:val="8775518"/>
            <w:date>
                <w:dateFormat w:val="M/d/yyyy"/>
                <w:lid w:val="EN-US"/>
            </w:date>
        </w:sdtPr>

        此结构化文档标记指定了三个属性：通过别名(alias)元素（§17.5.2.1）指定了友好名称为Birthday，通过ID(id)元素（§17.5.2.18）指定了唯一ID为8775518，通过日期(date)元素（§17.5.2.7）指定了日期选择器类型的结构化文档标记，日期元素本身具有一组日期特定的属性。结束示例】
        """

        return getattr(self, qn('w:sdtPr'), None)

    @property
    def sdtEndPr(self) -> Optional[CT_SdtEndPr]:
        """17.5.2.37 sdtEndPr (结构化文档标签结束字符属性)

        该元素指定应用于结构化文档标记结束符的物理字符的属性。

        【示例：考虑一个具有以下属性的结构化文档标记的结束标记：

        <w:sdtEndPr>
            <w:rPr>
                …
            </w:rPr>
        </w:sdtEndPr>

        此结构化文档标记在 sdtEndPr 元素中指定了其结束字符的属性。】
        """

        return getattr(self, qn('w:sdtEndPr'), None)

    @property
    def sdtContent_row(self) -> Optional[CT_SdtContentRow]:
        """17.5.2.35 sdtContent (行级结构化文档标签内容)

        该元素指定了围绕单个表格行的结构化文档标记的最后已知内容。

        【注意：与其他类型的结构化文档标记不同，这种类型的结构化文档标记不能显示占位符文本或具有映射的 XML 数据，因此它永远不是一个缓存。】

        【示例：考虑一个在 WordprocessingML 文档中围绕单个表格行的友好名称为 "invoiceItem" 的结构化文档标记。该需求可以在 WordprocessingML 中如下指定：

        <w:tbl>
            <w:sdt>
                <w:sdtPr>
                    <w:alias w:val="invoiceItem"/>
                </w:sdtPr>
                <w:sdtContent>
                    <w:tr>
                        …
                    </w:tr>
                </w:sdtContent>
            </w:sdt>
            …
        </w:tbl>

        sdtContent 元素包含了一个单个表格行（即一个行级别结构化文档标记内容容器）。】
        """

        return getattr(self, qn('w:sdtContent'), None)


class CT_Attr(OxmlBaseElement):
    @property
    def uri(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:uri'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def name(self) -> str:
        _val = self.attrib[qn('w:name')]

        return str(_val)

    @property
    def val(self) -> str:
        _val = self.attrib[qn('w:val')]

        return str(_val)


class CT_CustomXmlRun(OxmlBaseElement):
    @property
    def customXmlPr(self) -> Optional[CT_CustomXmlPr]:
        return getattr(self, qn('w:customXmlPr'), None)

    @property
    def p_content(
        self,
    ) -> list[
        CT_CustomXmlRun | CT_SmartTagRun | CT_SdtRun | CT_DirContentRun | CT_BdoContentRun | CT_R | CT_ProofErr | CT_PermStart | CT_Perm | CT_RunTrackChange | CT_Bookmark | CT_MarkupRange | CT_MoveBookmark | CT_TrackChange | CT_Markup | CT_SimpleField | CT_Hyperlink | CT_Rel
    ]:
        return self.choice_and_more(*EG_PContent.p_content_choice_tags)  # type: ignore

    @property
    def uri(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:uri'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def element(self) -> str:
        _val = self.attrib[qn('w:element')]

        return str(_val)


class CT_SmartTagRun(OxmlBaseElement):
    @property
    def smartTagPr(self) -> Optional[CT_SmartTagPr]:
        return getattr(self, qn('w:smartTagPr'), None)

    @property
    def p_content(
        self,
    ) -> list[
        CT_CustomXmlRun | CT_SmartTagRun | CT_SdtRun | CT_DirContentRun | CT_BdoContentRun | CT_R | CT_ProofErr | CT_PermStart | CT_Perm | CT_RunTrackChange | CT_Bookmark | CT_MarkupRange | CT_MoveBookmark | CT_TrackChange | CT_Markup | CT_SimpleField | CT_Hyperlink | CT_Rel
    ]:
        return self.choice_and_more(*EG_PContent.p_content_choice_tags)  # type: ignore

    @property
    def uri(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:uri'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def element(self) -> str:
        _val = self.attrib[qn('w:element')]

        return str(_val)


class CT_CustomXmlBlock(OxmlBaseElement):
    @property
    def customXmlPr(self) -> Optional[CT_CustomXmlPr]:
        return getattr(self, qn('w:customXmlPr'), None)

    @property
    def content_block(
        self,
    ) -> Optional[
        CT_CustomXmlBlock | CT_SdtBlock | CT_P | CT_Tbl | CT_ProofErr | CT_PermStart | CT_Perm | CT_RunTrackChange
    ]:
        return self.choice_and_more(*EG_ContentBlockContent.content_block_tags)  # type: ignore

    @property
    def uri(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:uri'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def element(self) -> str:
        _val = self.attrib[qn('w:element')]

        return str(_val)


class CT_CustomXmlPr(OxmlBaseElement):
    @property
    def placeholder(self) -> Optional[CT_String]:
        return getattr(self, qn('w:placeholder'), None)

    @property
    def attr(self) -> list[CT_Attr]:
        return self.findall(qn('w:attr'))  # type: ignore


class CT_CustomXmlRow(OxmlBaseElement):
    @property
    def customXmlPr(self) -> Optional[CT_CustomXmlPr]:
        return getattr(self, qn('w:customXmlPr'), None)

    @property
    def row_content(
        self,
    ) -> Optional[
        CT_Row | CT_CustomXmlRow | CT_SdtRow | CT_ProofErr | CT_PermStart | CT_Perm | CT_RunTrackChange
    ]:
        return self.choice_and_more(*EG_ContentRowContent.content_row_content_choice_tags)  # type: ignore

    @property
    def uri(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:uri'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def element(self) -> str:
        _val = self.attrib[qn('w:element')]

        return str(_val)


class CT_CustomXmlCell(OxmlBaseElement):
    @property
    def customXmlPr(self) -> Optional[CT_CustomXmlPr]:
        return getattr(self, qn('w:customXmlPr'), None)

    @property
    def cell_content(
        self,
    ) -> Optional[
        CT_Tc | CT_CustomXmlCell | CT_SdtCell | CT_ProofErr | CT_PermStart | CT_Perm | CT_RunTrackChange | CT_Bookmark | CT_MarkupRange | CT_MoveBookmark | CT_TrackChange | CT_Markup
    ]:
        return self.choice_and_more(*EG_ContentCellContent.content_cell_content_choice_tags)  # type: ignore

    @property
    def uri(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:uri'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def element(self) -> str:
        _val = self.attrib[qn('w:element')]

        return str(_val)


class CT_SmartTagPr(OxmlBaseElement):
    @property
    def attr(self) -> list[CT_Attr]:
        return self.findall(qn('w:attr'))  # type: ignore


class EG_PContent(EG_ContentRunContent):
    """
    <xsd:group name="EG_PContent">
        <xsd:choice>
            <xsd:group ref="EG_ContentRunContent" minOccurs="0" maxOccurs="unbounded"/>
            <xsd:element name="fldSimple" type="CT_SimpleField" minOccurs="0" maxOccurs="unbounded"/>
            <xsd:element name="hyperlink" type="CT_Hyperlink"/>
            <xsd:element name="subDoc" type="CT_Rel"/>
        </xsd:choice>
    </xsd:group>
    """

    # Union[CT_CustomXmlRun, CT_SmartTagRun, CT_SdtRun, CT_DirContentRun, CT_BdoContentRun, CT_R, CT_ProofErr, CT_PermStart, CT_Perm, CT_RunTrackChange, CT_Bookmark, CT_MarkupRange, CT_MoveBookmark,CT_TrackChange, CT_Markup, CT_SimpleField, CT_Hyperlink, CT_Rel]
    p_content_choice_tags = EG_ContentRunContent.content_run_content_tags + (
        qn('w:fldSimple'),  # CT_SimpleField
        qn('w:hyperlink'),  # CT_Hyperlink
        qn('w:subDoc'),  # CT_Rel
    )

    @property
    def fldSimple(self) -> Optional[CT_SimpleField]:
        return getattr(self, qn('w:fldSimple'), None)

    @property
    def hyperlink(self) -> Optional[CT_Hyperlink]:
        return getattr(self, qn('w:hyperlink'), None)

    @property
    def subDoc(self) -> Optional[CT_Rel]:
        return getattr(self, qn('w:subDoc'), None)


class CT_Hyperlink(EG_PContent):
    """17.16.22 hyperlink (超链接)

    hyperlink (Hyperlink)

    这个元素指定了文档中当前位置的超链接存在。

    [示例：考虑以下用于超链接的WordprocessingML片段：

    <w:hyperlink r:id="rId10">
        <w:r>
            <w:t>点击这里</w:t>
        </w:r>
    </w:hyperlink>

    hyperlink 元素定义了一个超链接，其显示文本为“点击这里”，目标由与 Id 属性值为 rId10 的关系指定。结束示例]
    """

    @property
    def p_content(
        self,
    ) -> list[
        CT_CustomXmlRun | CT_SmartTagRun | CT_SdtRun | CT_DirContentRun | CT_BdoContentRun | CT_R | CT_ProofErr | CT_PermStart | CT_Perm | CT_RunTrackChange | CT_Bookmark | CT_MarkupRange | CT_MoveBookmark | CT_TrackChange | CT_Markup | CT_SimpleField | CT_Hyperlink | CT_Rel
    ]:
        return self.choice_and_more(*EG_PContent.p_content_choice_tags)  # type: ignore

    @property
    def tgtFrame(self) -> Optional[str]:
        """tgtFrame（超链接目标框架）

        指定父 HTML 框架集中父超链接的目标框架（如果存在）。此元素指定的所有值应处理如下：

        值	描述
        _topOpen	将超链接目标显示在当前窗口的完整区域中。
        _selfOpen	将超链接目标显示在超链接出现的同一框架中。
        _parentOpen	将超链接目标显示在当前框架的父级中，或者如果此框架没有父级，则显示在当前框架中。
        _blankOpen	将超链接目标显示在新的 Web 浏览器窗口中。
        其他所有值	将超链接目标显示在具有指定名称的框架中。如果不存在具有此名称的框架，则在当前框架中打开。 如果此字符串不以字母字符开头，则将其忽略。

        如果省略此属性，则不会与父超链接关联任何目标框架信息。如果当前文档不是框架集的一部分，则可以忽略此信息。

        [示例：考虑以下用于超链接的 WordprocessingML 片段：

        <w:hyperlink r:id="rId9" w:tgtFrame="_top">
            <w:r>
                <w:t>http://example.com</w:t>
            </w:r>
        </w:hyperlink>

        tgtFrame 属性值 _top 指定此超链接的目标必须在当前窗口的完整区域中显示。结束示例]

        The possible values for this attribute are defined by the ST_String simple type (§22.9.2.13).
        """
        _val = self.attrib.get(qn('w:tgtFrame'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def tooltip(self) -> Optional[str]:
        """tooltip（关联字符串）

        指定一个字符串，可以在用户界面中显示为与父超链接相关联。此字符串由应用程序显示的方法不在 ECMA-376 的范围内。

        如果省略此属性，则在文档中不会将任何关联字符串链接到父超链接。

        [示例：考虑以下用于超链接的 WordprocessingML 片段：

        <w:hyperlink r:id="rId9" w:tooltip="点击这里！">
            <w:r>
                <w:t>http://example.com</w:t>
            </w:r>
        </w:hyperlink>

        tooltip 属性值指定父超链接具有关联字符串“点击这里！”，可以根据需要使用。结束示例]

        The possible values for this attribute are defined by the ST_String simple type (§22.9.2.13).
        """
        _val = self.attrib.get(qn('w:tooltip'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def docLocation(self) -> Optional[str]:
        """docLocation（目标文档中的位置）

        指定目标文档中没有书签的位置。如何将此属性的内容链接到文档文本的方法不在 ECMA-376 的范围之内。

        如果省略此属性，则不会将任何位置与父超链接关联起来。

        如果还指定了 anchor 属性，则在调用超链接时可以忽略此属性。

        [示例：考虑以下用于超链接的WordprocessingML片段：

        <w:hyperlink r:id="rId9" w:docLocation="table">
            <w:r>
                <w:t>点击此处</w:t>
            </w:r>
        </w:hyperlink>

        docLocation 属性指定当前超链接的目标必须是目标文档中由字符串 table 定位的区域。结束示例]

        此属性的可能值由 ST_String 简单类型（§22.9.2.13）定义。
        """
        _val = self.attrib.get(qn('w:docLocation'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def history(self) -> Optional[s_ST_OnOff]:
        """history（添加到已查看超链接）

        指定当调用超链接时，父超链接的目标（通过 r:id 属性指定）是否应添加到已查看超链接列表中。

        如果省略此属性，则其值应假定为 false。

        [示例：考虑以下用于超链接的WordprocessingML片段：

        <w:hyperlink r:id="rId9" w:history="true">
            <w:r>
                <w:t>http://www.example.com</w:t>
            </w:r>
        </w:hyperlink>

        history 属性值为 true 指定调用文档内的当前超链接时，其目标必须添加到已访问超链接列表中。结束示例]

        The possible values for this attribute are defined by the ST_OnOff simple type (§22.9.2.7).
        """
        _val = self.attrib.get(qn('w:history'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def anchor(self) -> Optional[str]:
        """anchor（超链接锚点）

        指定当前文档中一个书签的名称，该书签将成为此超链接的目标。

        如果省略此属性，则默认行为是导航到文档的开头。如果还使用 r:id 属性指定了超链接目标，则将忽略此属性。如果当前文档中不存在具有给定书签名称的书签，则默认行为是导航到文档的开头。

        [示例：考虑以下用于超链接的WordprocessingML片段：

        <w:hyperlink w:anchor="chapter3">
            <w:r>
                <w:t>转到第三章</w:t>
            </w:r>
        </w:hyperlink>

        anchor 属性指定当前超链接的目标必须是文档中的书签 chapter3 中包含的文本。结束示例]

        此属性的可能值由 ST_String 简单类型（§22.9.2.13）定义。
        """
        _val = self.attrib.get(qn('w:anchor'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def r_id(self) -> Optional[str]:
        """id（超链接目标）

        命名空间：http://purl.oclc.org/ooxml/officeDocument/relationships

        指定关系的ID，其目标将用作此超链接的目标。

        如果省略此属性，则当前超链接没有外部超链接目标 - 仍然可以通过 anchor 属性在当前文档中定位。

        如果存在此属性，则应该优先于 anchor 属性中的值。

        [示例：考虑以下用于超链接的 WordprocessingML 片段：

        <w:hyperlink r:id="rId9">
            <w:r>
                <w:t>http://www.example.com</w:t>
            </w:r>
        </w:hyperlink>

        id 属性值 rId9 指定与相应 ID 属性值的关系部分项中的关系，在调用此超链接时应导航到该部分项。例如，如果关系部分项中存在以下 XML：

        <Relationships xmlns="…">
            <Relationship Id="rId9" Mode="External" Target=http://www.example.com />
        </Relationships>

        则此超链接的目标将是关系 rId9 的目标 - 在此示例中为 http://www.example.com。结束示例]

        此属性的可能值由 ST_RelationshipId 简单类型（§22.8.2.1）定义。
        """
        _val = self.attrib.get(qn('r:id'))

        if _val is not None:
            return str(_val)
        return None


class CT_P(OxmlBaseElement):
    """17.3.1.22 p (段落)

    该元素指定文档中的一个段落内容。

    WordprocessingML文档中段落的内容应包括以下四种类型的内容的任意组合：

    - 段落属性（Paragraph properties）
    - 注解（书签、批注、修订）（Annotations (bookmarks, comments, revisions)）
    - 自定义标记（Custom markup）
    - 运行级别内容（字段、超链接、运行）（ Run level content (fields, hyperlinks, runs)）

    示例：考虑一个包含单个段落的基本WordprocessingML文档。此段落将表示如下：

    ```xml
    <w:document>
        <w:body>
            <w:p>
                <w:r>
                    <w:t>Text</w:t>
                </w:r>
                <w:fldSimple w:instr="AUTHOR">
                    <w:r>
                        <w:t>Author Name</w:t>
                    </w:r>
                </w:fldSimple>
            </w:p>
        </w:body>
    </w:document>
    ```

    p 元素是段落中所有内容的容器，在此示例中包括文本运行和简单字段。


    """

    @property
    def pPr(self) -> Optional[CT_PPr]:
        """17.3.1.26 pPr (段落属性)

        该元素指定了一组段落属性，这些属性应用于父段落的内容，在所有样式/编号/表格属性都已应用到文本后。这些属性被定义为直接格式化，因为它们直接应用于段落，并覆盖了样式的任何格式化。

        示例：考虑一个应该具有一组段落格式化属性的段落。这组属性在段落属性中如下指定：

        ```xml
        <w:p>
            <w:pPr>
                <w:pBdr>
                    <w:bottom w:val="single" w:sz="8" w:space="4" w:color="4F81BD" />
                </w:pBdr>
                <w:spacing w:after="300" />
                <w:contextualSpacing />
            </w:pPr>
        </w:p>

        pPr元素指定应用于当前段落的属性 - 在本例中，使用bottom元素（§17.3.1.7）指定段落底部的边框，使用spacing元素（§17.3.1.33）指定段落后的间距，并且应该使用contextualSpacing元素（§17.3.1.9）忽略相同样式的上/下段落的间距。
        """
        return getattr(self, qn('w:pPr'), None)

    @property
    def p_content(
        self,
    ) -> list[
        CT_CustomXmlRun | CT_SmartTagRun | CT_SdtRun | CT_DirContentRun | CT_BdoContentRun | CT_R | CT_ProofErr | CT_PermStart | CT_Perm | CT_RunTrackChange | CT_Bookmark | CT_MarkupRange | CT_MoveBookmark | CT_TrackChange | CT_Markup | CT_SimpleField | CT_Hyperlink | CT_Rel
    ]:
        """段落内容元素"""
        return self.choice_and_more(*EG_PContent.p_content_choice_tags)  # type: ignore

    @property
    def bookmarkStart(self) -> list[CT_Bookmark]:
        """17.13.6.2 bookmarkStart (书签开始)

        <xsd:group name="EG_RangeMarkupElements">
            <xsd:choice>
                <xsd:element name="bookmarkStart" type="CT_Bookmark"/>
                <xsd:element name="bookmarkEnd" type="CT_MarkupRange"/>
                ...
            </xsd:choice>
        </xsd:group>
        """

        return self.findall(qn('w:bookmarkStart'))  # type: ignore

    @property
    def bookmarkEnd(self) -> Optional[CT_MarkupRange]:
        """17.13.6.1 bookmarkEnd (书签结束)

        <xsd:group name="EG_RangeMarkupElements">
            <xsd:choice>
                <xsd:element name="bookmarkStart" type="CT_Bookmark"/>
                <xsd:element name="bookmarkEnd" type="CT_MarkupRange"/>
                ...
            </xsd:choice>
        </xsd:group>
        """

        return getattr(self, qn('w:bookmarkEnd'), None)

    @property
    def rsidRPr(self) -> Optional[ST_LongHexNumber]:
        """段落标志格式的修订标识符

        此属性指定用于跟踪最后修改主文档中段落标志表示的字形字符时的编辑会话的标识符。

        如果存在相同值的所有 rsid* 属性，则表示这些区域在同一编辑会话期间（在连续的保存操作之间的时间）内被修改。

        生产者可以选择增加修订保存 ID 的值，以指示后续的编辑会话，以表明修改的顺序相对于文档中其他修改的顺序。

        此属性的可能值由 ST_LongHexNumber 简单类型（[§17.18.50]）定义。
        """
        _val = self.attrib.get(qn('w:rsidRPr'))

        if _val is not None:
            return ST_LongHexNumber(str(_val))
        return None

    @property
    def rsidR(self) -> Optional[ST_LongHexNumber]:
        """段落的修订标识符

        此属性指定用于跟踪将段落添加到主文档时的编辑会话的标识符。

        如果存在相同值的所有 rsid* 属性，则表示这些区域在同一编辑会话期间（在连续的保存操作之间的时间）内被修改。

        生产者可以选择增加修订保存 ID 的值，以指示后续的编辑会话，以表明修改的顺序相对于文档中其他修改的顺序。

        此属性的可能值由 ST_LongHexNumber 简单类型（[§17.18.50]）定义。
        """
        _val = self.attrib.get(qn('w:rsidR'))

        if _val is not None:
            return ST_LongHexNumber(str(_val))
        return None

    @property
    def rsidDel(self) -> Optional[ST_LongHexNumber]:
        """段落删除的修订标识符

        指定用于跟踪段落从主文档中删除时的编辑会话的标识符。

        如果存在相同值的所有 rsid* 属性，则表示这些区域在同一编辑会话期间（在连续的保存操作之间的时间）内被修改。

        生产者可以选择增加修订保存 ID 的值，以指示后续的编辑会话，以表明修改的顺序相对于文档中其他修改的顺序。

        此属性的可能值由 ST_LongHexNumber 简单类型（[§17.18.50]）定义。
        """
        _val = self.attrib.get(qn('w:rsidDel'))

        if _val is not None:
            return ST_LongHexNumber(str(_val))
        return None

    @property
    def rsidP(self) -> Optional[ST_LongHexNumber]:
        """段落属性的修订标识符

        此属性指定用于跟踪在此文档中最后修改段落属性时的编辑会话的标识符。

        如果存在相同值的所有 rsid* 属性，则表示这些区域在同一编辑会话期间（在连续的保存操作之间的时间）内被修改。

        生产者可以选择增加修订保存 ID 的值，以指示后续的编辑会话，以表明修改的顺序相对于文档中其他修改的顺序。

        此属性的可能值由 ST_LongHexNumber 简单类型（[§17.18.50]）定义。
        """
        _val = self.attrib.get(qn('w:rsidP'))

        if _val is not None:
            return ST_LongHexNumber(str(_val))
        return None

    @property
    def rsidRDefault(self) -> Optional[ST_LongHexNumber]:
        """运行的默认修订标识符

        此属性指定用于此段落中所有未明确声明 rsidR 属性的运行的标识符。该属性允许使用者优化在文档中编写 rsid* 值的位置。

        如果存在相同值的所有 rsid* 属性，则表示这些区域在同一编辑会话期间（在连续的保存操作之间的时间）内被修改。

        生产者可以选择增加修订保存 ID 的值，以指示后续的编辑会话，以表明修改的顺序相对于文档中其他修改的顺序。

        此属性的可能值由 ST_LongHexNumber 简单类型（[§17.18.50]）定义。
        """
        _val = self.attrib.get(qn('w:rsidRDefault'))

        if _val is not None:
            return ST_LongHexNumber(str(_val))
        return None


class ST_TblWidth(ST_BaseEnumType):
    """17.18.90 ST_TblWidth (表格宽度单位)

    这个简单类型指定了由特定的表宽属性定义的宽度属性的可能值。这些属性用于定义表格的各种属性，包括：单元格间距、首选宽度和表格边距。

    【示例：考虑一个具有表格单元格底部间距类型为dxa的表格，如下所示：

    <w:bottom … w:type="dxa" />

    因此，必须使用此类型将w属性中指定的宽度解释为点的二十分之一的值。示例结束】

    这个简单类型的内容是对W3C XML Schema字符串数据类型的限制。

    这个简单类型被限制为以下表格中列出的值：

    - auto（自动确定宽度）

        指定当前表格宽度属性的测量值在父表格中将在表格显示时由表格布局算法自动确定（此宽度可以根据需要进行调整）。

        如果这个值对于当前的测量是不合适的（即该测量不受该算法的影响），那么这种宽度类型和相关的值可以被忽略。

    - dxa（点的二十分之一的宽度）

        指定当前表格宽度属性的测量值在父表格中应被解释为点的二十分之一的值（1/1440英寸）。

    - nil（无宽度）

        指定当前宽度为零，而不管父元素上指定的任何宽度值。

    - pct（表宽度的百分比宽度）

        指定当前表格宽度属性的测量值在父表格中应被解释为整个百分比点，当存在百分号（U+0025）时。

        这些百分比应相对于父XML元素指定的范围进行计算。

        如果这个值对于当前的测量是不合适的（即该测量不是表格的宽度的一部分），那么这种宽度类型和相关的值可以被忽略。
    """

    nil = 'nil'
    """指定当前宽度为零，而不管父元素上指定的任何宽度值。"""

    pct = 'pct'
    """指定当前表格宽度属性的测量值在父表格中应被解释为整个百分比点，当存在百分号（U+0025）时。

    这些百分比应相对于父XML元素指定的范围进行计算。

    如果这个值对于当前的测量是不合适的（即该测量不是表格的宽度的一部分），那么这种宽度类型和相关的值可以被忽略。
    """

    dxa = 'dxa'
    """指定当前表格宽度属性的测量值在父表格中应被解释为点的二十分之一的值（1/1440英寸）。
    """

    auto = 'auto'
    """指定当前表格宽度属性的测量值在父表格中将在表格显示时由表格布局算法自动确定（此宽度可以根据需要进行调整）。

    如果这个值对于当前的测量是不合适的（即该测量不受该算法的影响），那么这种宽度类型和相关的值可以被忽略。
    """


class CT_Height(OxmlBaseElement):
    """17.4.80 trHeight (表格行高)

    trHeight (Table Row Height)

    该元素指定当前表格中当前表格行的高度。该高度将用于确定表格行的最终高度，可以是绝对值或相对值（取决于其属性值）。

    如果省略，则表格行将自动调整其高度以适应其内容所需的高度（相当于hRule值为auto）。

    【示例：考虑以下WordprocessingML表格：

    123

    检查此表格的WordprocessingML，未指定trHeight元素，因此行高度由其内容自动确定（在第一行中，文本为Some text in R1C1.）。如果要将第一行的高度限制为0.1英寸高（144个点的二十分之一），则可以使用trHeight元素指定如下：

    <w:trPr>
        <w:trHeight w:val="144" w:hRule="exact"/>
    </w:trPr>

    结果的表格行将正好高144个点的二十分之一：
    """

    @property
    def val(self) -> Optional[s_ST_TwipsMeasure]:
        """val（表格行高度）

        指定表格行的高度。

        该高度以点的二十分之一表示。

        如果省略了此属性，则其值应被视为0。

        根据此表格行的hRule属性的值，val属性的含义如下所示：

        - 如果hRule的值为auto，则表格行的高度应根据其内容的高度自动确定。忽略此值。
        - 如果hRule的值为atLeast，则表格行的高度应至少为此属性的值。
        - 如果hRule的值为exact，则表格行的高度应完全等于此属性的值。

        【示例：考虑以下表格行：

        <w:tr>
            <w:trPr>
                <w:trHeight w:val="2189" w:hRule="atLeast"/>
            </w:trPr>
            …
        </w:tr>

        val属性指定了2189个点的二十分之一的值，因此无论其内容如何，该表格行的高度至少为2189个点的二十分之一（如果需要则增加），因为其hRule值设置为atLeast。示例结束】

        此属性的可能值由ST_TwipsMeasure简单类型（§22.9.2.14）定义。
        """

        _val = self.attrib.get(qn('w:val'))

        if _val is not None:
            return s_to_ST_TwipsMeasure(str(_val))
        return None

    @property
    def hRule(self) -> ST_HeightRule:
        """hRule（表格行高度类型）

        指定为该表格行指定的高度的含义。

        根据此表格行的hRule属性的值，val属性的值的含义如下所示：

        - 如果hRule的值为auto，则表格行的高度应根据其内容的高度自动确定。忽略h值。
        - 如果hRule的值为atLeast，则表格行的高度应至少为h属性的值。
        - 如果hRule的值为exact，则表格行的高度应完全等于h属性的值。

        如果省略了此属性，则其值应被视为auto。

        【示例：考虑以下包含表格行的段落：

        <w:tr>
            <w:trPr>
                <w:trHeight w:val="2189" w:hRule="atLeast"/>
            </w:trPr>
            …
        </w:tr>

        hRule属性指定了atLeast的值，因此表格行的高度至少为2189个点的二十分之一，无论其内容如何，因为其val值为2189个点的二十分之一。示例结束】

        此属性的可能值由ST_HeightRule简单类型（§17.18.37）定义。
        """
        _val = self.attrib.get(qn('w:hRule'))

        if _val is not None:
            return ST_HeightRule(str(_val))

        return ST_HeightRule.Auto


ST_MeasurementOrPercent = Union[ST_DecimalNumberOrPercent, s_ST_UniversalMeasure]


def to_ST_MeasurementOrPercent(val: str):
    try:
        return int(val)
    except Exception:
        try:
            return float(val)
        except Exception:
            return s_to_ST_UniversalMeasure(val)


class CT_TblWidth(OxmlBaseElement):
    """17.4.87 表格测量 (CT_TblWidth)¶

    Table Measurement (CT_TblWidth)

    这个常见的复杂类型指定在表格中使用的度量。这些属性包含两个信息：

    - 度量的类型（基于百分比、绝对值或自动）
    - 度量的值

    【示例：考虑以下表格度量：

    <… w:type="pct" w:w="100%"/>

    type属性指定度量是基于百分比的，而w属性指定度量为100%。示例结束】
    """

    @property
    def w(self) -> Optional[ST_MeasurementOrPercent]:
        """w（表格宽度值）

        指定由父元素定义的宽度属性的值。此属性用于定义表格的各种属性，包括：单元格间距、首选宽度和表格边距。

        如果省略了此属性，则其值应被视为0。

        【示例：考虑一个具有302的底部边距的表格，如下所示：

        <w:bottom w:w="302" w:type="dxa" />

        因此，必须使用w属性中的值来确定相对于type属性指定的单位的宽度。在这种情况下，类型是点的二十分之一（dxa），所以宽度为302个点的二十分之一（0.2097英寸）。示例结束】

        此属性的可能值由ST_MeasurementOrPercen简单类型（§17.18.107）定义。
        """
        _val = self.attrib.get(qn('w:w'))

        if _val is not None:
            return to_ST_MeasurementOrPercent(str(_val))
        return None

    @property
    def type(self) -> ST_TblWidth:
        """type（表格宽度类型）

        指定由父元素的w属性定义的宽度属性的单位。此属性用于定义表格的各种属性，包括：单元格间距、首选宽度和表格边距。

        如果省略了此属性，则其值应被视为dxa（点的二十分之一）。

        【示例：考虑一个具有类型为dxa的表格单元格底部单元格间距的表格，如下所示：

        <w:bottom … w:type="dxa" />

        因此，必须使用此类型来解释w属性中指定的宽度，作为点的二十分之一的值。示例结束】

        如果type属性的值和w属性指定的实际度量矛盾，则将忽略type属性指定的类型。

        此属性的可能值由ST_TblWidth简单类型（§17.18.90）定义。
        """
        _val = self.attrib.get(qn('w:type'))

        if _val is not None:
            return ST_TblWidth(str(_val))

        return ST_TblWidth.dxa


class CT_TblGridCol(OxmlBaseElement):
    """17.4.16 gridCol (网格列定义)¶

    gridCol (Grid Column Definition)

    该元素指定表格网格中的单个网格列的存在和详细信息。网格列是表格中的逻辑列，用于指定表格中共享垂直边缘的存在。然后，当将表格单元格添加到此表格时，这些共享边缘（或者查看介于这些共享边缘之间的网格列）决定了如何将表格单元格放置到表格网格中。

    【示例：如果表格行指定其前面有两个网格列，则它将从表格中的第三个垂直边缘开始，包括未被所有列共享的边缘。示例结束】

    如果表格网格不符合表格中一个或多个行的要求（即，它未定义足够的网格列），则在处理表格时可以根据需要重新定义网格。

    【示例：考虑以下更复杂的表格，它有两行和两列；如下所示，列没有对齐：

    123

    该表格通过将单元格布局在由三个表格网格列组成的表格网格上来表示，每个网格列代表表格中的一个逻辑垂直列：

    123

    虚线表示每个表格网格列的虚拟垂直延续，因此得到的表格网格表示为以下 WordprocessingML：


    <w:tblGrid>
        <w:gridCol w:w="5051" />
        <w:gridCol w:w="3008" />
        <w:gridCol w:w="1531" />
    </w:tblGrid>

    示例结束】
    """

    @property
    def w(self) -> Optional[s_ST_TwipsMeasure]:
        """w（网格列宽度）

        指定此网格列的宽度。

        【注意：此值并不单独确定文档中生成的网格列的实际宽度。当表格在文档中显示时，这些宽度确定每个网格列的初始宽度，然后可以被以下内容覆盖：

        应用于当前表格行的表格布局算法（§17.4.52;§17.4.53）
        显示的表格中的特定单元格的首选宽度（这是上述算法的输入）
        注意结束】

        此值以点的二十分之一为单位指定。

        如果省略了此属性，则假定网格列的最后保存宽度为零。

        【示例：考虑以下表格网格定义：

        <w:tblGrid>
            <w:gridCol w:w="6888"/>
            <w:gridCol w:w="248"/>
            <w:gridCol w:w="886"/>
            <w:gridCol w:w="1554"/>
        </w:tblGrid>

        此表格网格指定四个网格列，每个初始大小分别为 6888 点的二十分之一，248 点的二十分之一，886 点的二十分之一和 1554 点的二十分之一。示例结束】

        此属性的可能取值由 ST_TwipsMeasure 简单类型定义（§22.9.2.14）。
        """
        _val = self.attrib.get(qn('w:w'))

        if _val is not None:
            return s_to_ST_TwipsMeasure(str(_val))
        return None


class CT_TblGridBase(OxmlBaseElement):
    """17.4.47 tblGrid (上一个表格网格)¶

    tblGrid (Previous Table Grid)

    该元素指定了先前的表格网格状态，其修改应归因于特定作者在特定时间的修订。该元素包含在某位作者进行特定修订前的表格网格设置。表格网格定义了一组网格列，这些网格列定义了表格所有共享的垂直边缘，以及每个网格列的默认宽度。这些网格列宽度然后根据使用的表格布局算法来确定表格的大小 (§17.4.52;§17.4.53)。

    [示例：考虑以下具有四个垂直边缘（网格列）的表格：

    123

    如果我们现在通过减少最后一列的大小来修改此表格，而不改变整个表格的宽度，如下所示：

    12323

    此表格将具有由以下四个网格列组成的表格网格：


    <w:tblGrid>
        <w:gridCol w:w="2088"/>
        <w:gridCol w:w="1104"/>
        <w:gridCol w:w="3583"/>
        <w:gridCol w:w="2801"/>
        <w:tblGridChange w:id="1">
            <w:tblGrid>
                <w:gridCol w:w="2088"/>
                <w:gridCol w:w="1104"/>
                <w:gridCol w:w="3192"/>
                <w:gridCol w:w="3192"/>
            </w:tblGrid>
        </w:tblGridChange>
    </w:tblGrid>

    作为 tblGridChange 子元素的 tblGrid 包含表格网格的先前定义，包括所有的网格列以及这些列的原始宽度。示例结束]
    """

    @property
    def gridCol(self) -> list[CT_TblGridCol]:
        """17.4.16 gridCol (网格列定义)¶

        gridCol (Grid Column Definition)

        该元素指定表格网格中的单个网格列的存在和详细信息。网格列是表格中的逻辑列，用于指定表格中共享垂直边缘的存在。然后，当将表格单元格添加到此表格时，这些共享边缘（或者查看介于这些共享边缘之间的网格列）决定了如何将表格单元格放置到表格网格中。

        【示例：如果表格行指定其前面有两个网格列，则它将从表格中的第三个垂直边缘开始，包括未被所有列共享的边缘。示例结束】

        如果表格网格不符合表格中一个或多个行的要求（即，它未定义足够的网格列），则在处理表格时可以根据需要重新定义网格。

        【示例：考虑以下更复杂的表格，它有两行和两列；如下所示，列没有对齐：

        123

        该表格通过将单元格布局在由三个表格网格列组成的表格网格上来表示，每个网格列代表表格中的一个逻辑垂直列：

        123

        虚线表示每个表格网格列的虚拟垂直延续，因此得到的表格网格表示为以下 WordprocessingML：


        <w:tblGrid>
            <w:gridCol w:w="5051" />
            <w:gridCol w:w="3008" />
            <w:gridCol w:w="1531" />
        </w:tblGrid>

        示例结束】
        """
        return self.findall(qn('w:gridCol'))  # type: ignore


class CT_TblGrid(CT_TblGridBase):
    """17.4.48 tblGrid (表格网格)

    该元素指定了当前表格的表格网格。表格网格定义了一组网格列，这些网格列定义了表格所有共享的垂直边缘，以及每个网格列的默认宽度。这些网格列宽度随后根据使用的表格布局算法来确定表格的大小 (§17.4.52;§17.4.53)。

    如果省略了表格网格，则将从表格的实际内容中构建一个新网格，假设所有网格列的宽度为0。

    [示例：考虑以下具有四个垂直边缘（网格列）的表格：

    123

    此表格将具有由以下四个网格列组成的表格网格：

    <w:tblGrid>
        <w:gridCol w:w="2088"/>
        <w:gridCol w:w="1104"/>
        <w:gridCol w:w="3192"/>
        <w:gridCol w:w="3192"/>
    </w:tblGrid>

    tblGrid 元素包含表格网格的当前定义，包括所有网格列以及这些列的默认宽度。示例结束]
    """

    @property
    def tblGridChange(self) -> Optional[CT_TblGridChange]:
        return getattr(self, qn('w:tblGridChange'), None)


class CT_TcBorders(OxmlBaseElement):
    """17.4.66 tcBorders (表格单元格边框合集)

    tcBorders (Table Cell Borders)

    该元素指定了当前表单元格边缘的边框集合，使用其子元素定义的八种边框类型。

    如果任何行的单元格间距非零，如使用tblCellSpacing元素（§17.4.44；§17.4.43；§17.4.45）指定，则永远不会存在边框冲突（因为非零的单元格间距应用于每个单独单元格边框的宽度之上），并且将显示所有表、表级异常和表单元格边框。

    如果单元格间距为零，则两个相邻单元格边框之间可能存在冲突【示例：在表的第二列中所有单元格的左边框和表的第一列中所有单元格的右边框之间。结束示例】，应解决如下：

    1. 如果任一冲突的表单元格边框为nil或none（无边框），则对立边框将被显示。
    2. 如果单元格边框与表边框冲突，则始终显示单元格边框。
    3. 然后，使用以下公式为每个边框分配权重，并使用此计算的边框值显示在替代边框上：

    ...
    """

    @property
    def top(self) -> Optional[CT_Border]:
        """17.4.74 top (表格单元格顶部边框)

        top (Table Cell Top Border)

        该元素指定应在当前表单元格的顶部显示的边框。此表单元格边框在文档中的外观应由以下设置确定：

        - 如果应用于单元格的净tblCellSpacing元素值（§17.4.44；§17.4.43；§17.4.45）为非零，则始终应显示单元格边框
        - 否则，边框的显示取决于由tcBorders元素（§17.4.66）和tblBorders元素（§17.4.39；§17.4.38）定义的冲突解决算法

        如果省略了此元素，则此表单元格的顶部不应有单元格边框，并且其边框可以根据需要使用表格的边框设置。
        """
        return getattr(self, qn('w:top'), None)

    @property
    def start(self) -> Optional[CT_Border]:
        """17.4.33 start (表格单元前缘边框)

        start (Table Cell Leading Edge Border)

        该元素指定了应显示在当前表格单元格前沿（LTR表格为左侧，RTL表格为右侧）的边框。文档中该表格单元格边框的外观应由以下设置确定：

        - 如果应用于单元格的净tblCellSpacing元素值（§17.4.44;§17.4.43;§17.4.45）为非零，则始终显示单元格边框
        - 否则，边框的显示取决于由tcBorders元素（§17.4.66）和tblBorders元素（§17.4.39;§17.4.38）定义的冲突解决算法

        如果省略了此元素，则此表格单元格的前沿将不具有单元格边框，并且其边框可以根据需要使用表格的边框设置。
        """
        return getattr(self, qn('w:start'), None)

    @property
    def left(self) -> Optional[CT_Border]:
        """左边框

        文档中没有
        """
        return getattr(self, qn('w:left'), None)

    @property
    def bottom(self) -> Optional[CT_Border]:
        """17.4.3 bottom (表格单元格底部边框)

        该元素指定了当前表格单元格底部显示的边框。此单元格边框在文档中的显示方式应由以下设置决定：

        - 如果应用于单元格的 net tblCellSpacing 元素值（§17.4.44;§17.4.43;§17.4.45）为非零值，则单元格边框始终显示。
        - 否则，边框的显示受 tcBorders 元素（§17.4.66）和 tblBorders 元素（§17.4.39;§17.4.38）定义的冲突解决算法的影响。

        如果省略此元素，则该表格单元格的底部没有单元格边框，并且其边框可以根据需要使用表格的边框设置。
        """
        return getattr(self, qn('w:bottom'), None)

    @property
    def end(self) -> Optional[CT_Border]:
        """17.4.12 end (表格单元格后缘边框)

        end (Table Cell Trailing Edge Border)

        该元素指定当前表格单元格的尾部边界（LTR 表格的右侧，RTL 表格的左侧）应显示的边框。文档中此表格单元格边框的外观将由以下设置确定：

        - 如果应用于单元格的净 tblCellSpacing 元素值（§17.4.44; §17.4.43; §17.4.45）为非零，则始终显示单元格边框。
        - 否则，边框的显示将受到由 tcBorders 元素（§17.4.66）和 tblBorders 元素（§17.4.39; §17.4.38）定义的冲突解决算法的影响。

        如果省略此元素，则此表格单元格的尾部边缘将不显示单元格边框，并且其边框可以根据需要使用表格的边框设置。
        """
        return getattr(self, qn('w:end'), None)

    @property
    def right(self) -> Optional[CT_Border]:
        """右边框

        文档中没有
        """
        return getattr(self, qn('w:right'), None)

    @property
    def insideH(self) -> Optional[CT_Border]:
        """17.4.23 insideH (表格单元格内部水平边缘边框)

        该元素指定应显示在当前表格单元格组的所有内部水平边缘上的边框。【注：尽管单个表格单元格没有内部边缘的概念，在大多数情况下这个属性将变得无用，但它被用于确定应用于表格样式中的特定单元格组的单元格边框，例如，在第一列中的单元格集合上的内部水平边缘。结束注】

        该表格单元格边框在文档中的显示方式应由以下设置确定：

        - 如果应用于单元格的净tblCellSpacing元素值（§17.4.44；§17.4.43；§17.4.45）是非零的，则始终显示单元格边框。
        - 否则，边框的显示取决于由tcBorders元素（§17.4.66）和tblBorders元素（§17.4.39；§17.4.38）定义的冲突解析算法。

        如果省略此元素，则表格上指定的条件格式不会更改其表格单元格集合上的当前一组内部边缘边框（即，它们的当前设置将保持不变）。
        """
        return getattr(self, qn('w:insideH'), None)

    @property
    def insideV(self) -> Optional[CT_Border]:
        """17.4.25 insideV (表格单元格内部垂直边缘边框)

        insideV (Table Cell Inside Vertical Edges Border)

        该元素指定应显示在当前表格单元格组的所有内部垂直边缘上的边框。【注：尽管单个表格单元格没有内部边缘的概念，在大多数情况下这个属性将变得无用，但它被用于确定应用于表格样式中的特定单元格组的单元格边框，例如，在标题行中的单元格集合上的内部垂直边缘。结束注】

        该表格单元格边框在文档中的显示方式应由以下设置确定：

        - 如果应用于单元格的净tblCellSpacing元素值（§17.4.44;§17.4.43;§17.4.45）是非零的，则始终显示单元格边框。
        - 否则，边框的显示取决于由tcBorders元素（§17.4.66）和tblBorders元素（§17.4.39;§17.4.38）定义的冲突解析算法。

        如果省略此元素，则表格上指定的条件格式不会更改其表格单元格集合上的当前一组内部边缘边框（即，它们的当前设置将保持不变）。
        """
        return getattr(self, qn('w:insideV'), None)

    @property
    def tl2br(self) -> Optional[CT_Border]:
        """17.4.73 tl2br (表格单元格左上到右下对角边框)¶

        tl2br (Table Cell Top Left to Bottom Right Diagonal Border)

        该元素指定应在当前表单元格内的从左上到右下对角线上显示的边框。

        如果省略了此元素，则此表单元格的左上到右下对角线上不应有单元格边框，并且其边框可以根据需要使用表格的边框设置。
        """
        return getattr(self, qn('w:tl2br'), None)

    @property
    def tr2bl(self) -> Optional[CT_Border]:
        """17.4.79 tr2bl (表格单元格右上到左下对角边框)¶

        tr2bl (Table Cell Top Right to Bottom Left Diagonal Border)

        该元素指定当前表格单元格内从右上到左下的对角线上应显示的边框。

        如果省略了此元素，则该表格单元格的右上到左下对角线将不会有单元格边框，并且其边框可以根据需要使用表格的边框设置。
        """
        return getattr(self, qn('w:tr2bl'), None)


class CT_TcMar(OxmlBaseElement):
    """17.4.68 tcMar (单个表格单元格边距)

    该元素指定父表中单个表单元格的一组单元格边距。

    如果存在此设置，则应覆盖来自表级单元格边距（§17.4.42）的表单元格边距。

    【示例：考虑一个表格，其第一个单元格被定义为具有0.5英寸的默认单元格边距，而不是表格默认值，如下所示：

    123

    使用以下WordprocessingML指定了此表单元格边距集合：

    <w:tcPr>
        <w:tcMar>
            <w:top w:w="720" w:type="dxa"/>
            <w:start w:w="720" w:type="dxa"/>
            <w:bottom w:w="720" w:type="dxa"/>
            <w:end w:w="720" w:type="dxa"/>
        </w:tcMar>
        …
    </w:tcPr>

    作为tcPr的子元素的tcMar元素指定了用于第一个表单元格的一组表单元格边距，在本例中，每个边缘均为720个点的二十分之一。结束示例】
    """

    @property
    def top(self) -> Optional[CT_TblWidth]:
        return getattr(self, qn('w:top'), None)

    @property
    def start(self) -> Optional[CT_TblWidth]:
        return getattr(self, qn('w:start'), None)

    @property
    def left(self) -> Optional[CT_TblWidth]:
        return getattr(self, qn('w:left'), None)

    @property
    def bottom(self) -> Optional[CT_TblWidth]:
        return getattr(self, qn('w:bottom'), None)

    @property
    def end(self) -> Optional[CT_TblWidth]:
        return getattr(self, qn('w:end'), None)

    @property
    def right(self) -> Optional[CT_TblWidth]:
        return getattr(self, qn('w:right'), None)


class ST_Merge(ST_BaseEnumType):
    """17.18.57 ST_Merge (合并单元格类型)¶

    ST_Merge (Merged Cell Type)

    这个元素指定了在父表格中将单元格包含在合并的单元格组中的方式（水平或垂直）。
    """

    Continue = 'continue'
    """continue（继续合并区域）

    指定当前单元格继续父表格中先前存在的合并单元格组。

    如果文档中的前一个单元格（水平或垂直）不是开始或继续一组合并单元格，则此值将被忽略（即，合并单元格组将以 ST_Merge 值为 restart 的合并开始）。
    """

    restart = 'restart'
    """restart（开始/重新开始合并区域）

    指定当前单元格在父表格中开始（或重新开始）一组合并的单元格。

    在此值之后，所有后续具有 continue 值的单元格都将合并到此合并单元格组中。
    """


class CT_VMerge(OxmlBaseElement):
    """17.4.84 vMerge (垂直合并单元格)

    vMerge (Vertically Merged Cell)

    该元素指定此单元格是表格中一组垂直合并单元格的一部分。该元素上的val属性确定了此单元格相对于表格中前一个单元格的定义方式（即，此单元格是继续垂直合并还是开始一组新的合并单元格）。

    如果省略了此元素，则此单元格不应是任何垂直合并单元格组的一部分，并且任何前面单元格的垂直合并组将被关闭。如果一组垂直合并的单元格没有跨越相同的网格列，则文档不符合规范。
    """

    @property
    def val(self) -> ST_Merge:
        """val（垂直合并类型）

        指定表格单元格如何成为垂直合并区域的一部分。这确定了单元格是否应连接到现有的任何合并单元格组，或者开始一个新的合并单元格组。有关每种类型的完整描述，请参考简单类型定义。

        如果省略了此属性，则其值应被视为continue。

        【示例：考虑一个表格单元格，其中垂直合并开始。这个设置表示为以下WordprocessingML：

        <w:tcPr>
            <w:vMerge w:val="restart"/>
        </w:tcPr>

        restart的属性值指定此元素必须在此表格中开始一个新的垂直合并区域。示例结束】

        此属性的可能值由ST_Merge简单类型（§17.18.57）定义。
        """
        _val = self.attrib.get(qn('w:val'))

        if _val is not None:
            return ST_Merge(_val)

        return ST_Merge.Continue


class CT_HMerge(OxmlBaseElement):
    @property
    def val(self) -> Optional[ST_Merge]:
        _val = self.attrib.get(qn('w:val'))

        if _val is not None:
            return ST_Merge(_val)
        return None


class CT_TcPrBase(OxmlBaseElement):
    @property
    def cnfStyle(self) -> Optional[CT_Cnf]:
        """17.4.8 cnfStyle (表格单元格条件格式)

        该元素指定应用于此表格单元格的一组条件表格样式格式化属性。【注：此属性是一种优化，用于由使用者确定表格单元格上的给定属性是否是表格样式条件格式化属性与表格单元格本身的直接格式化的结果。它指定了应用于此单元格的表格样式中的条件格式化的组件，以便在文档显示后应用表格的条件格式化，而不会使表格样式属性覆盖样式层次结构。结束注解】

        如果省略此元素，则其值应假定为位掩码中所有条目的零。

        【示例：考虑一个应用了表格样式的表格中右上角的表格单元格，并且表格按从左到右的格式进行了格式化。此表格单元格需要指定以下 WordprocessingML 来表示这一事实：

        <w:tc>
            <w:tcPr>
                <w:cnfStyle w:firstRow="true" w:lastColumn="true"
                    w:firstRowLastColumn="true" />
                …
            </w:tcPr>
            …
        </w:tc>
        此表格单元格指定其具有来自表格样式的条件属性，即父表格的第一列、第一行和右上角，通过设置适当的属性。结束示例】
        """
        return getattr(self, qn('w:cnfStyle'), None)

    @property
    def tcW(self) -> Optional[CT_TblWidth]:
        """17.4.71 tcW (首选的表格单元格宽度)

        该元素指定了此表单元格的首选宽度。此首选宽度作为由tblLayout元素（§17.4.52；§17.4.53）指定的表格布局算法的一部分使用 - 有关算法的完整描述，请参阅ST_TblLayout简单类型（§17.18.87）。

        表中的所有宽度都被视为首选宽度，因为：

        表格应满足由tblGrid元素指定的共享列（§17.4.48）
        两个或更多个宽度可以对同一网格列的宽度具有冲突的值
        表格布局算法（§17.18.87）可能需要覆盖首选项
        此值由其type属性应用的单位指定。对于此元素的类型pct的任何宽度值应相对于表格的总宽度计算。

        如果省略了此元素，则单元格宽度应为自动类型。

        【示例：考虑一个定义如下的WordprocessingML表格：

        <w:tbl>
            <w:tr>
                <w:tc>
                    <w:tcPr>
                        <w:tcW w:type="pct" w:w="33.3%"/>
                    </w:tcPr>
                    …
                </w:tc>
                <w:tc>
                    <w:tcPr>
                        <w:tcW w:type="pct" w:w="33.3%"/>
                    </w:tcPr>
                    …
                </w:tc>
                <w:tc>
                    <w:tcPr>
                        <w:tcW w:type="pct" w:w="33.3%"/>
                    </w:tcPr>
                    …
                </w:tc>
            </w:tr>
        </w:tbl>

        此表格指定它没有首选表格宽度，但每个单元格必须正好为表格总宽度的33.3％。因此，结果表格将调整大小，以使所有列的宽度等于最大列的宽度，如下所示：

        123

        文本Hello world使得中间单元格变大，其他两个单元格增加大小以保持表格总宽度的三分之一的首选宽度。然而，当中间表格单元格需要更大的尺寸来容纳非断行文本时，可以根据需要覆盖该首选项：

        123

        在这种情况下，中间单元格的长非断行字符串导致表格达到页面的文本边距，因此覆盖了空单元格上的首选宽度。结束示例】
        """
        return getattr(self, qn('w:tcW'), None)

    @property
    def gridSpan(self) -> Optional[CT_DecimalNumber]:
        """17.4.17 gridSpan (当前表格单元格跨越的网格列)

        gridSpan (Grid Columns Spanned by Current Table Cell)

        该元素指定了父表格的表格网格中当前单元格应跨越的网格列数。该属性允许单元格具有合并的外观，因为它们跨越表格中其他单元格的垂直边界。

        如果省略了此元素，则假定该单元格跨越的网格单位数为一。如果 val 属性指定的网格单位数超过表格网格的大小，则表格网格将根据需要进行扩充，以创建所需数量的网格列。
        """
        return getattr(self, qn('w:gridSpan'), None)

    @property
    def hMerge(self) -> Optional[CT_HMerge]:
        """水平合并单元格..

        文档无资料...
        """
        return getattr(self, qn('w:hMerge'), None)

    @property
    def vMerge(self) -> Optional[CT_VMerge]:
        """17.4.84 vMerge (垂直合并单元格)

        vMerge (Vertically Merged Cell)

        该元素指定此单元格是表格中一组垂直合并单元格的一部分。该元素上的val属性确定了此单元格相对于表格中前一个单元格的定义方式（即，此单元格是继续垂直合并还是开始一组新的合并单元格）。

        如果省略了此元素，则此单元格不应是任何垂直合并单元格组的一部分，并且任何前面单元格的垂直合并组将被关闭。如果一组垂直合并的单元格没有跨越相同的网格列，则文档不符合规范。
        """
        return getattr(self, qn('w:vMerge'), None)

    @property
    def tcBorders(self) -> Optional[CT_TcBorders]:
        """17.4.66 tcBorders (表格单元格边框合集)

        tcBorders (Table Cell Borders)

        该元素指定了当前表单元格边缘的边框集合，使用其子元素定义的八种边框类型。

        如果任何行的单元格间距非零，如使用tblCellSpacing元素（§17.4.44；§17.4.43；§17.4.45）指定，则永远不会存在边框冲突（因为非零的单元格间距应用于每个单独单元格边框的宽度之上），并且将显示所有表、表级异常和表单元格边框。

        如果单元格间距为零，则两个相邻单元格边框之间可能存在冲突【示例：在表的第二列中所有单元格的左边框和表的第一列中所有单元格的右边框之间。结束示例】，应解决如下：

        ...
        """
        return getattr(self, qn('w:tcBorders'), None)

    @property
    def shd(self) -> Optional[CT_Shd]:
        """17.4.32 shd (表格单元格底纹)

        该元素指定了应用于当前表格单元格范围的底纹。类似于段落底纹，此底纹应用于单元格内容直至单元格边界，无论文本是否存在。

        该底纹由三个组成部分组成：

        - 背景颜色
        - （可选）图案
        - （可选）图案颜色

        通过在段落后设置背景颜色，然后使用图案提供的蒙版在该背景上应用图案颜色来应用生成的底纹。

        如果省略了此元素，则当前表格中的单元格底纹将由表级别或表级别异常的单元格底纹设置确定（§17.4.30;§17.4.31）。
        """
        return getattr(self, qn('w:shd'), None)

    @property
    def noWrap(self) -> Optional[CT_OnOff]:
        """17.4.29 noWrap (不要包裹单元格内容)¶

        noWrap (Don't Wrap Cell Content)

        该元素指定了当父表格在文档中显示时，该表格单元格应该如何布局。此设置仅影响当为该行设置了tblLayout为使用自动算法时 (§17.4.52; §17.4.53)，该单元格的行为。

        该设置应该在tcW元素 (§17.4.71) 的上下文中解释如下：

        - 如果表格单元格宽度具有固定的 type 属性值，则该元素指定了当行上的其他单元格没有达到绝对最小宽度时，该表格单元格绝不应该小于该固定值。
        - 如果表格单元格宽度具有百分比或自动 type 属性值，则该元素指定了在运行自动适应算法时，该表格单元格的内容应被视为没有断字符（内容应被视为单一连续的不可断字符串）。

        如果省略此元素，则单元格内容应允许换行（如果是固定的首选宽度值，则可以根据需要缩小单元格，并且如果是百分比或自动宽度值，则应将内容视为具有断字符）。
        """
        return getattr(self, qn('w:noWrap'), None)

    @property
    def tcMar(self) -> Optional[CT_TcMar]:
        """17.4.68 tcMar (单个表格单元格边距)¶

        tcMar (Single Table Cell Margins)

        该元素指定父表中单个表单元格的一组单元格边距。

        如果存在此设置，则应覆盖来自表级单元格边距（§17.4.42）的表单元格边距。
        """

        return getattr(self, qn('w:tcMar'), None)

    @property
    def textDirection(self) -> Optional[CT_TextDirection]:
        """17.4.72 textDirection (表格单元格文本流方向)

        textDirection (Table Cell Text Flow Direction)

        该元素指定此表单元格的文本流方向。

        如果在给定的表单元格上省略了此元素，则其值由先前设置的任何样式层次结构的水平方向上的设置确定（即，先前的设置保持不变）。如果在样式层次结构中从未指定此设置，则表单元格应继承父节的文本流设置。

        【示例：考虑一个具有一个单元格的表格，在该单元格中，所有表单元格的文本流都是垂直定向的，从右向左水平流动：

        123

        该表单元格将使用以下WordprocessingML指定此文本流：

        <w:tc>
            <w:tcPr>
                …
                <w:textDirection w:val="rl" />
            </w:tcPr>
            …
        </w:tc>

        textDirection元素通过val属性中的rl值指定，文本流应垂直定向，并且随后的行从右向左堆叠。结束示例】
        """
        return getattr(self, qn('w:textDirection'), None)

    @property
    def tcFitText(self) -> Optional[CT_OnOff]:
        """17.4.67 tcFitText (适合单元格内的文本)¶

        tcFitText (Fit Text Within Cell)

        该元素指定，当前单元格的内容应根据需要增加或减少字符间距，以适应当前单元格文本范围的宽度。如果该元素上提供的宽度与当前单元格的宽度匹配，则此设置应与将本段落的内容放置在一个运行中并使用fitText元素（§17.3.2.14）的行为完全相同。

        如果省略了此元素，则此单元格中的文本不应适合当前单元格范围。

        【示例：考虑一个2行2列的表格，在其中第一行的两个单元格的内容都设置了fit text属性，如下所示：


        <w:tcPr>
            <w:tcFitText w:val="true"/>
        </w:tcPr>
        生成的表格单元格的内容必须适合父表单元格的范围，如下所示：

        123

        结束示例】
        """
        return getattr(self, qn('w:tcFitText'), None)

    @property
    def vAlign(self) -> Optional[CT_VerticalJc]:
        """17.4.83 vAlign (表格单元格垂直对齐方式)¶

        vAlign (Table Cell Vertical Alignment)

        该元素指定当前表格单元格内文本的垂直对齐方式。该文本的垂直对齐方式由val属性的值确定。

        【示例：考虑一个只有一个单元格的表格，其中文本垂直对齐到单元格底部：

        123

        可以使用以下WordprocessingML指定这个要求：


        <w:tc>
            <w:tcPr>
                <w:vAlign w:val="bottom" />
            </w:tcPr>
            <w:p>
                <w:r>
                    <w:t>R1C1</w:t>
                </w:r>
            </w:p>
        </w:tc>
        vAlign元素指定了单元格内容的垂直对齐方式，这里是单元格底部。

        示例结束】
        """
        return getattr(self, qn('w:vAlign'), None)

    @property
    def hideMark(self) -> Optional[CT_OnOff]:
        """17.4.21 hideMark (在行高计算中忽略单元格末尾标记)¶

        hideMark (Ignore End Of Cell Marker In Row Height Calculation)

        该元素指定结束单元格符号是否会影响表格中给定表格行的高度。如果指定了该元素，则只有该单元格中的打印字符将用于确定行高度。

        【理由：通常，表格行的高度由该行中所有单元格中的所有字形的高度决定，包括非打印的单元格结束符号字符。然而，如果这些字符没有格式化，它们总是使用文档默认的样式属性创建。这意味着表格行的高度永远不能减小到低于单元格结束标记符号的大小，而不手动格式化该运行中的每个段落。

        在典型文档中，这种行为是可取的，因为它防止了没有内容的表格行“消失”。但是，如果表格行被用作边框（例如，通过对其单元格进行着色或放置图像），那么这种行为将使得无法拥有一个合理小的虚拟边框，而不必直接格式化每个单元格的内容。该设置指定该单元格的结束单元格符号应该被忽略，允许其折叠到其内容的高度，而不必格式化每个单元格的结束单元格标记，这将导致格式化输入到该单元格中的任何文本。结束理由】

        如果省略此元素，则将包括单元格标记符号在内，以确定该行的高度。
        """
        return getattr(self, qn('w:hideMark'), None)

    @property
    def headers(self) -> Optional[CT_Headers]:
        """17.4.19 headers (与表格单元关联的标题单元)¶

        headers (Header Cells Associated With Table Cell)

        此元素指定标题单元格列表，如子标题元素所指定，提供与当前表格单元格相关联的标题信息。每个标题单元格应指定一个唯一标识符，由标题单元格tc元素上的id属性指定。此元素通常用于收集关于数据和子标题单元格的标题信息。

        如果省略此元素或不存在子标题元素，则不应将任何标题单元格与给定表格单元格关联。
        """
        return getattr(self, qn('w:headers'), None)


class CT_TcPrInner(CT_TcPrBase):
    """17.4.70 tcPr (上一表格单元格属性)¶

    tcPr (Previous Table Cell Properties)

    该元素指定先前的一组表单元格属性，其修改应归因于特定作者和特定时间的修订。该元素包含了在某一作者的一组特定修订之前先前存在的表单元格属性设置。每个唯一属性由此元素的子元素指定。在任何表级、表级异常或行级属性与相应表单元格属性存在冲突的情况下，这些属性将覆盖表格或行范围的属性。

    【示例：考虑一个基本的2行2列表格，如下所示：

    ...

    如果在启用修订跟踪的情况下，将第一个单元格中的单元格底纹设置为红色，如下所示：

    ...

    这个修订在相关的WordprocessingML中指定如下：

    <w:tc>
        <w:tcPr>
            <w:tcW w:w="4788" w:type="dxa"/>
            <w:shd w:val="clear" w:color="auto" w:fill="FF0000"/>
            <w:tcPrChange w:id="2" …>
                <w:tcPr>
                    <w:tcW w:w="4788" w:type="dxa"/>
                </w:tcPr>
            </w:tcPrChange>
        </w:tcPr>
        <w:p/>
    </w:tc>

    tcPrChange元素下面的tcPr元素指定了在当前文档修订之前先前存在的表单元格属性集。结束示例】
    """

    @property
    def cell_marker_elements(
        self,
    ) -> Optional[CT_TrackChange | CT_CellMergeTrackChange]:
        return self.choice_one_child(*EG_CellMarkupElements.cell_markup_tags)  # type: ignore


class CT_TcPr(CT_TcPrInner):
    """17.4.69 tcPr (表格单元格属性)¶

    tcPr (Table Cell Properties)

    该元素指定应用于特定表单元格的一组属性。每个唯一属性由此元素的子元素指定。在任何表级、表级异常或行级属性与相应表单元格属性存在冲突的情况下，这些属性将覆盖表格或行范围的属性。

    【示例：考虑一个表格，其中单元格宽度覆盖了以下WordprocessingML中表示的表格宽度：

    <w:tbl>
        <w:tblPr>
            <w:tblCellMar>
                <w:start w:w="0" w:type="dxa"/>
            </w:tblCellMar>
            </w:tblPr>
            …
        <w:tr>
        <w:tc>
            <w:tcPr>
                <w:tcMar>
                    <w:start w:w="720" w:type="dxa"/>
                </w:tcMar>
            </w:tcPr>
            …
            </w:tc>
        </w:tr>
    </w:tbl>

    此表单元格具有左边距为720个点的二十分之一（即半英寸），如tcMar元素中所指定的，它覆盖了表级设置的0个左表单元格边距。结束示例】
    """

    @property
    def tcPrChange(self) -> Optional[CT_TcPrChange]:
        return getattr(self, qn('w:tcPrChange'), None)


class EG_BlockLevelElts(EG_ContentBlockContent):
    """

    <xsd:group name="EG_BlockLevelElts">
        <xsd:choice>
            <xsd:group ref="EG_BlockLevelChunkElts" minOccurs="0" maxOccurs="unbounded"/>
            <xsd:element name="altChunk" type="CT_AltChunk" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:choice>
    </xsd:group>
    """

    # Union[CT_CustomXmlBlock, CT_SdtBlock, CT_P, CT_Tbl, CT_ProofErr, CT_PermStart, CT_Perm, CT_RunTrackChange, CT_AltChunk]
    block_level_elts_choice_tags = (*EG_ContentBlockContent.content_block_tags, qn('w:altChunk'))

    @property
    def altChunk(self) -> list[CT_AltChunk]:
        return self.findall(qn('w:altChunk'))  # type: ignore


class CT_Tc(EG_BlockLevelElts):
    """17.4.65 tc (表格单元格)

    tc (Table Cell)

    该元素指定表行中的单个单元格，其中包含表的内容。WordprocessingML中的表单元格类似于HTML中的td元素。

    tc元素具有一个格式化子元素tcPr（§17.4.69），它定义了单元格的属性。表单元格上的每个唯一属性由此元素的子元素指定。此外，表单元格可以包含任何块级内容，这允许在表单元格中嵌套段落和表格。

    如果表单元格不包含至少一个块级元素，则应将此文档视为损坏。

    【示例：考虑由包含文本“Hello, world”的单个表单元格组成的表格：

    ....

    此表单元格的内容由以下WordprocessingML表示：

    <w:tc>
        <w:tcPr>
            <w:tcW w:w="0" w:type="auto"/>
        </w:tcPr>
        <w:p>
            <w:r>
                <w:t>Hello, world</w:t>
            </w:r>
        </w:p>
    </w:tc>

    tc元素包含使用tcPr元素定义的一组单元格级属性，以及一个块级元素 - 在本例中为段落。结束示例】

    <xsd:complexType name="CT_Tc">
        <xsd:sequence>
            <xsd:element name="tcPr" type="CT_TcPr" minOccurs="0" maxOccurs="1"/>
            <xsd:group ref="EG_BlockLevelElts" minOccurs="1" maxOccurs="unbounded"/>
        </xsd:sequence>
        <xsd:attribute name="id" type="s:ST_String" use="optional"/>
    </xsd:complexType>
    """

    @property
    def tcPr(self) -> Optional[CT_TcPr]:
        """17.4.69 tcPr (表格单元格属性)¶

        tcPr (Table Cell Properties)

        该元素指定应用于特定表单元格的一组属性。每个唯一属性由此元素的子元素指定。在任何表级、表级异常或行级属性与相应表单元格属性存在冲突的情况下，这些属性将覆盖表格或行范围的属性。

        【示例：考虑一个表格，其中单元格宽度覆盖了以下WordprocessingML中表示的表格宽度：

        <w:tbl>
            <w:tblPr>
                <w:tblCellMar>
                    <w:start w:w="0" w:type="dxa"/>
                </w:tblCellMar>
                </w:tblPr>
                …
            <w:tr>
            <w:tc>
                <w:tcPr>
                    <w:tcMar>
                        <w:start w:w="720" w:type="dxa"/>
                    </w:tcMar>
                </w:tcPr>
                …
                </w:tc>
            </w:tr>
        </w:tbl>

        此表单元格具有左边距为720个点的二十分之一（即半英寸），如tcMar元素中所指定的，它覆盖了表级设置的0个左表单元格边距。结束示例】
        """
        return getattr(self, qn('w:tcPr'), None)

    @property
    def levels(
        self,
    ) -> list[
        CT_CustomXmlBlock | CT_SdtBlock | CT_P | CT_Tbl | CT_ProofErr | CT_PermStart | CT_Perm | CT_RunTrackChange | CT_AltChunk
    ]:
        return self.choice_and_more(*EG_BlockLevelElts.block_level_elts_choice_tags)  # type: ignore

    @property
    def id(self) -> Optional[str]:
        """id（表单元格标识符）

        指定当前表单元格的唯一标识符。此标识符在表中必须是唯一的，并用于使用headers子元素将此表单元格标识为表中其他单元格的标题单元格。

        如果省略此属性，则此表单元格没有唯一标识符。

        【示例：考虑定义如下的表单元格：

        <w:tc w:id="januaryeight">
            …
        </w:tc>

        id中的值指定了januaryeight的唯一标识符。然后，表中的其他单元格可以通过引用此ID将其引用为行或列标题。结束示例】

        此属性的可能值由ST_String简单类型（§22.9.2.13）定义。
        """
        _val = self.attrib.get(qn('w:id'))

        if _val is not None:
            return str(_val)
        return None


class ST_Cnf(str):
    """
    <xsd:simpleType name="ST_Cnf">
        <xsd:restriction base="xsd:string">
            <xsd:length value="12"/>
            <xsd:pattern value="[01]*"/>
        </xsd:restriction>
    </xsd:simpleType>
    """



class CT_Cnf(OxmlBaseElement):
    """7.3.1.8 cnfStyle (段落条件格式)

    这个元素指定了一组条件表格样式格式属性，这些属性已应用于此段落，如果此段落包含在表格单元格中。[注：此属性是一种优化，消费者可以使用它来确定段落上的给定属性是表格样式属性的结果还是段落本身的直接格式化。结束注释]

    如果此属性在不包含在表格单元格中的段落上指定，则在阅读文档内容时应忽略其内容。

    [示例：考虑一个位于表格右上角的段落，应用了表格样式，并且表格格式为从左到右。此段落需要指定以下WordprocessingML：

    <w:p>
        <w:pPr>
            <w:cnfStyle w:firstRow="true" w:lastColumn="true" w:firstRowLastColumn="true" />
            …
        </w:pPr>
        …
    </w:p>

    此段落通过设置适当的属性指定了它具有来自表格样式的条件属性，用于父表的第一列、第一行和右上角。结束示例]
    """

    @property
    def val(self) -> Optional[ST_Cnf]:
        """无资料？ 开启或关闭当前配置?"""
        _val = self.attrib.get(qn('w:val'))

        if _val is not None:
            return ST_Cnf(_val)
        return None

    @property
    def firstRow(self) -> Optional[s_ST_OnOff]:
        """firstRow（第一行）

        指定对象已继承应用于父对象的第一行的条件属性。

        [示例：考虑一个表格顶部行中的段落，应用了表格样式。此段落需要指定以下WordprocessingML：

        <w:p>
            <w:pPr>
                <w:cnfStyle w:firstRow="true" />
                …
            </w:pPr>
            …
        </w:p>

        此段落指定它具有父表格的第一行的表格样式的条件属性。示例结束]
        """
        _val = self.attrib.get(qn('w:firstRow'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def lastRow(self) -> Optional[s_ST_OnOff]:
        """lastRow（最后一行）

        指定对象已继承应用于父对象最后一行的条件属性。

        [示例：考虑一个表格中底部行的段落，应用了表格样式。此段落需要指定以下WordprocessingML：

        <w:p>
            <w:pPr>
                <w:cnfStyle w:lastRow="true" />
                …
            </w:pPr>
            …
        </w:p>

        此段落指定它具有父表格最后一行的表格样式的条件属性。示例结束]
        """
        _val = self.attrib.get(qn('w:lastRow'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def firstColumn(self) -> Optional[s_ST_OnOff]:
        """firstColumn（第一列）

        指定对象已继承应用于父对象的第一列的条件属性。

        [示例：考虑一个表格中第一列中的段落，应用了表格样式。此段落需要指定以下WordprocessingML：

        <w:p>
            <w:pPr>
                <w:cnfStyle w:firstColumn="true" />
                …
            </w:pPr>
            …
        </w:p>

        此段落指定它具有父表格的第一列的表格样式的条件属性。示例结束]
        """
        _val = self.attrib.get(qn('w:firstColumn'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def lastColumn(self) -> Optional[s_ST_OnOff]:
        """lastColumn（最后一列）

        指定对象已继承应用于父对象最后一列的条件属性。

        [示例：考虑一个表格中最后一列的段落，应用了表格样式。此段落需要指定以下WordprocessingML：

        <w:p>
            <w:pPr>
                <w:cnfStyle w:lastColumn="true" />
                …
            </w:pPr>
            …
        </w:p>

        此段落指定它具有父表格最后一列的表格样式的条件属性。示例结束]
        """
        _val = self.attrib.get(qn('w:lastColumn'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def oddVBand(self) -> Optional[s_ST_OnOff]:
        """oddVBand（奇数垂直带）

        指定对象已继承应用于父对象的奇数垂直带的条件属性。

        [示例：考虑一个应用了表格样式的表格中第三列的段落，其中带宽为一列。此段落需要指定以下WordprocessingML：


        <w:p>
            <w:pPr>
                <w:cnfStyle w:oddVBand="true" />
                …
            </w:pPr>
            …
        </w:p>
        此段落指定它具有父表格的奇数垂直带的表格样式的条件属性。示例结束]

        此属性的可能值由ST_OnOff简单类型（§22.9.2.7）定义。
        """
        _val = self.attrib.get(qn('w:oddVBand'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def evenVBand(self) -> Optional[s_ST_OnOff]:
        """evenVBand（偶数垂直带）

        指定对象已继承应用于父对象的偶数垂直带的条件属性。

        [示例：考虑一个应用了表格样式的表格中第二列的段落，并且带宽为一列。此段落需要指定以下WordprocessingML：

        <w:p>
            <w:pPr>
                <w:cnfStyle w:evenVBand="true" />
                …
            </w:pPr>
            …
        </w:p>

        此段落指定它具有父表格的偶数垂直带的表格样式的条件属性。示例结束]
        """
        _val = self.attrib.get(qn('w:evenVBand'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def oddHBand(self) -> Optional[s_ST_OnOff]:
        """oddHBand（奇数水平带）

        指定对象已继承应用于父对象的奇数水平带的条件属性。

        [示例：考虑一个应用了表格样式的表格中第三行的段落，其中带宽为一列。此段落需要指定以下WordprocessingML：

        <w:p>
            <w:pPr>
                <w:cnfStyle w:oddHBand="true" />
                …
            </w:pPr>
            …
        </w:p>

        此段落指定它具有父表格的奇数水平带的表格样式的条件属性。示例结束]
        """
        _val = self.attrib.get(qn('w:oddHBand'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def evenHBand(self) -> Optional[s_ST_OnOff]:
        """evenHBand（偶数水平带）

        指定对象已继承应用于父对象的偶数水平带的条件属性。

        [示例：考虑一个应用了表格样式的表格中第二行的段落，并且带宽为一行。此段落需要指定以下WordprocessingML：

        <w:p>
            <w:pPr>
                <w:cnfStyle w:evenHBand="true" />
                …
            </w:pPr>
            …
        </w:p>

        此段落指定它具有父表格的偶数水平带的表格样式的条件属性。示例结束]
        """
        _val = self.attrib.get(qn('w:evenHBand'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def firstRowFirstColumn(self) -> Optional[s_ST_OnOff]:
        """firstRowFirstColumn（第一行和第一列）

        指定对象已继承应用于父对象的第一行和第一列中的单元格的条件属性。

        [示例：考虑表格中第一行和第一列中的段落。此段落需要指定以下WordprocessingML：

        <w:p>
            <w:pPr>
                <w:cnfStyle w:firstRow="true" w:firstColumn="true" w:firstRowFirstColumn="true" />
                …
            </w:pPr>
            …
        </w:p>

        此段落指定它具有父表格中第一行和第一列中的单元格的表格样式的条件属性。示例结束]
        """
        _val = self.attrib.get(qn('w:firstRowFirstColumn'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def firstRowLastColumn(self) -> Optional[s_ST_OnOff]:
        """firstRowLastColumn（第一行和最后一列）

        指定对象已继承应用于父对象的第一行和最后一列中的单元格的条件属性。

        [示例：考虑表格中第一行和最后一列中的段落。此段落需要指定以下WordprocessingML：

        <w:p>
            <w:pPr>
                <w:cnfStyle w:firstRow="true" w:lastColumn="true" w:firstRowLastColumn="true" />
                …
            </w:pPr>
            …
        </w:p>

        此段落指定它具有父表格中第一行和最后一列中的单元格的表格样式的条件属性。示例结束]
        """
        _val = self.attrib.get(qn('w:firstRowLastColumn'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def lastRowFirstColumn(self) -> Optional[s_ST_OnOff]:
        """lastRowFirstColumn（最后一行和第一列）

        指定对象已继承应用于父对象中最后一行和第一列的单元格的条件属性。

        [示例：考虑表格中最后一行和第一列的段落。此段落需要指定以下WordprocessingML：

        <w:p>
            <w:pPr>
                <w:cnfStyle w:lastRow="true" w:firstColumn="true" w:lastRowFirstColumn="true" />
                …
            </w:pPr>
            …
        </w:p>

        此段落指定它具有父表中最后一行和第一列单元格的表样式的条件属性。示例结束]
        """
        _val = self.attrib.get(qn('w:lastRowFirstColumn'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def lastRowLastColumn(self) -> Optional[s_ST_OnOff]:
        """lastRowLastColumn（最后一行和最后一列）

        指定对象已继承应用于父对象中最后一行和最后一列的单元格的条件属性。

        [示例：考虑表格中最后一行和最后一列的段落。此段落需要指定以下WordprocessingML：

        <w:p>
            <w:pPr>
                <w:cnfStyle w:lastRow="true" w:firstColumn="true" w:lastRowLastColumn="true" />
                …
            </w:pPr>
            …
        </w:p>

        此段落指定它具有父表中最后一行和最后一列单元格的表样式的条件属性。示例结束]

        此属性的可能值由ST_OnOff简单类型（§22.9.2.7）定义。
        """
        _val = self.attrib.get(qn('w:lastRowLastColumn'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None


class CT_Headers(OxmlBaseElement):
    @property
    def header(self) -> list[CT_String]:
        return self.findall(qn('w:header'))  # type: ignore


class CT_TrPrBase(OxmlBaseElement):
    @property
    def cnfStyle(self) -> Optional[CT_Cnf]:
        """17.4.7 cnfStyle (表行条件格式)

        该元素指定了应用于此表格行的条件表格样式格式属性集。【注意：此属性是一种优化，用于消费者确定表格行上的给定属性是表格样式条件格式属性的结果，还是直接在表格单元格上进行的格式设置。它指定了应用于此单元格的表格样式中的条件格式的组件，以便在文档显示后可以应用表格的条件格式，而不会让表格样式属性覆盖样式层次结构。结束注意】

        如果省略此元素，则其值应假定为位掩码中的所有条目均为零。

        【示例：考虑一个位于表格顶部的表格行，应用了一个表格样式。此表格单元格需要指定以下 WordprocessingML 以表达该事实：

        <w:tr>
            <w:trPr>
                <w:cnfStyle w:firstRow="true" />
                …
            </w:trPr>
            …
        </w:tr>

        此表格行通过设置适当的属性值，指定它具有来自父表格的第一行的表格样式的条件属性。结束示例】
        """
        return getattr(self, qn('w:cnfStyle'), None)

    @property
    def divId(self) -> Optional[CT_DecimalNumber]:
        """17.4.9 divId (关联的 HTML div ID)¶

        divId (Associated HTML div ID)

        该元素指定与当前表格行关联的 HTML div 信息。此信息存储在 Web 设置部分中，用于将一个或多个表格行与特定的 HTML div 元素关联起来。【注：此属性用于在将 HTML 文档保存为 WordprocessingML 格式时，防止丢失所有 HTML div 信息，以便稍后将文档保存回 HTML 格式并替换存储的信息，因为 HTML div 可以在任意区域存储格式化属性。结束注解】

        为了确定关联的 HTML div 属性，将使用此元素上的 val 属性的值查找一个与此值匹配的关联 div 元素（§17.15.2.8）的 id 属性。

        如果此表格行没有 divId 元素，那么此表格行将不具有任何关联的 HTML div 信息。如果此元素存在，但 val 属性指定了一个没有关联 div 元素的 id 值，则将忽略此元素。
        """
        return getattr(self, qn('w:divId'), None)

    @property
    def gridBefore(self) -> Optional[CT_DecimalNumber]:
        """17.4.15 gridBefore (第一个单元格之前的网格列)¶

        gridBefore (Grid Columns Before First Cell)

        该元素指定父表格的表格网格（§17.4.48; §17.4.47）中，在将该表格行的内容（其表格单元格）添加到父表格之前必须跳过的网格列数。【注：此属性用于指定其前导边缘（对于从左到右的表格为左边，对于从右到左的表格为右边）不从第一个网格列（相同的共享边缘）开始的表格。】如果省略此元素，则其值应被假定为零个网格单元。如果此元素的值大于表格网格的大小，则应忽略该值，并且行中的第一个单元格可以跨越整个表格网格（即，如果存在第二个单元格，则应从表格中的最后一个共享边缘开始）。
        """
        return getattr(self, qn('w:gridBefore'), None)

    @property
    def gridAfter(self) -> Optional[CT_DecimalNumber]:
        """17.4.14 gridAfter (最后一个单元格之后的网格列)¶

        gridAfter (Grid Columns After Last Cell)

        该元素指定了父表格的表格网格（§17.4.48; §17.4.47）中，表格行中最后一个单元格之后应保留的网格列数。

        如果此元素与将所有此行中的表格单元格添加到网格后文档网格的剩余大小存在冲突，则将忽略它。如果未指定此元素，则其值将被假定为零个网格单位。
        """
        return getattr(self, qn('w:gridAfter'), None)

    @property
    def wBefore(self) -> Optional[CT_TblWidth]:
        """17.4.86 wBefore (表行之前的首选宽度)

        wBefore (Preferred Width Before Table Row)

        该元素指定了在该表格行之前的网格列的总数的首选宽度，如gridAfter元素（§17.4.14）所指定。此首选宽度是由tblLayout元素（§17.4.52; §17.4.53）指定的表格布局算法的一部分 - 该算法的完整描述在ST_TblLayout简单类型中（§17.18.87）。

        在表格中，所有宽度都被视为首选，因为：

        - 表格应满足由tblGrid元素（§17.4.48）指定的共享列
        - 两个或更多的宽度可能对同一网格列的宽度有冲突的值
        - 表格布局算法（§17.18.87）可能需要覆盖首选项

        此值是通过其type属性应用的单位中指定的。对于此元素，类型为pct的任何宽度值都应相对于页面的文本范围（不包括页边距）进行计算。

        如果省略了此元素，则单元格宽度将为auto类型。
        """
        return getattr(self, qn('w:wBefore'), None)

    @property
    def wAfter(self) -> Optional[CT_TblWidth]:
        """17.4.85 wAfter (表行后的首选宽度)¶

        wAfter (Preferred Width After Table Row)

        该元素指定了在表格行后面的网格列的总数的首选宽度，如gridAfter元素（§17.4.14）所指定。此首选宽度是由tblLayout元素（§17.4.52; §17.4.53）指定的表格布局算法的一部分 - 该算法的完整描述在ST_TblLayout简单类型中（§17.18.87）。

        在表格中，所有宽度都被视为首选，因为：

        - 表格应满足由tblGrid元素（§17.4.48）指定的共享列
        - 两个或更多的宽度可能对同一网格列的宽度有冲突的值
        - 表格布局算法（§17.18.87）可能需要覆盖首选项

        此值是通过其type属性应用的单位中指定的。对于此元素，类型为pct的任何宽度值都应相对于页面的文本范围（不包括页边距）进行计算。

        如果省略了此元素，则单元格宽度将为auto类型。
        """
        return getattr(self, qn('w:wAfter'), None)

    @property
    def cantSplit(self) -> Optional[CT_OnOff]:
        """17.4.6 cantSplit (表格行不能跨页中断)¶

        cantSplit (Table Row Cannot Break Across Pages)

        该元素指定了当前单元格内的内容是否应在单个页面上呈现。当显示表格单元格的内容时（如 ECMA-376 标准中的表格单元格），可能会出现页面断裂落在单元格内容中的情况，导致该单元格的内容分布在两个不同的页面上。如果设置了此属性，则所有表格行的内容应在同一页面上呈现，如果有必要，将当前行的起始位置移动到新页面的开始处。如果该表格行的内容无法在单个页面上容纳，则该行应在新页面上开始，并根据需要流动到多个页面。

        如果未出现此元素，则默认行为由关联的表格样式中的设置决定。如果样式层次结构中未指定此属性，则该表格行允许跨多个页面拆分。
        """
        return getattr(self, qn('w:cantSplit'), None)

    @property
    def trHeight(self) -> Optional[CT_Height]:
        """17.4.80 trHeight (表格行高)¶

        trHeight (Table Row Height)

        该元素指定当前表格中当前表格行的高度。该高度将用于确定表格行的最终高度，可以是绝对值或相对值（取决于其属性值）。

        如果省略，则表格行将自动调整其高度以适应其内容所需的高度（相当于hRule值为auto）。
        """
        return getattr(self, qn('w:trHeight'), None)

    @property
    def tblHeader(self) -> Optional[CT_OnOff]:
        """17.4.49 tblHeader (在每个新页面上重复表行)¶

        tblHeader (Repeat Table Row on Every New Page)

        该元素指定当前表格行应在显示表格的每个新页面顶部重复。这使得该表格行在每个页面上表现得像一个“标题”行。此元素可以应用于表格结构顶部的任意数量的行，以生成多行表格标题。

        如果省略此元素，则该表格行不会在显示表格的每个新页面上重复。此外，如果该行与表格的第一行不连续连接（即，如果该表格行不是第一行，或在此行与第一行之间的所有行都未标记为标题行），则此属性将被忽略。

        [示例：考虑一个表格，其第一行必须在每个新页面上重复，例如 ECMA-376 中的属性列表：

        注意表格中的第一行在第二页顶部重复。此需求将在该行的 WordprocessingML 中指定如下：

        <w:trPr>
            <w:tblHeader />
        </w:trPr>

        tblHeader 元素指定该表格行在每个页面的顶部作为标题行重复。示例结束]
        """
        return getattr(self, qn('w:tblHeader'), None)

    @property
    def tblCellSpacing(self) -> Optional[CT_TblWidth]:
        """17.4.43 tblCellSpacing (表格行单元格间距)¶

        tblCellSpacing (Table Row Cell Spacing)

        该元素指定了父行中所有单元格的默认表格单元格间距（相邻单元格与表格边缘之间的间距）。如果指定了此元素，则它表示表格中所有单元格之间应保留的最小空间，包括表格边框的宽度。需要注意的是，行级单元格间距应添加在文本边距内，并与没有行级缩进或单元格间距的单元格中文本范围的最内侧起始边对齐。行级单元格间距不应增加整体表格的宽度。

        此值以其类型属性应用的单位指定。任何类型为pct或auto的宽度值将被忽略。
        """
        return getattr(self, qn('w:tblCellSpacing'), None)

    @property
    def jc(self) -> Optional[CT_JcTable]:
        """17.4.27 jc (表格行对齐)¶

        jc (Table Row Alignment)

        此元素指定了父表格中单个行相对于当前部分的文本边距的对齐方式。当将表格放置在宽度与边距不同的WordprocessingML文档中时，此属性用于确定表格中特定行相对于这些边距的位置。如果父表格使用bidiVisual元素（§17.4.1）从右到左排列，则属性的解释将被反转。

        如果在表格上省略此属性，则对齐方式将由父表格上的默认表格属性集确定。

        [示例：考虑以下居中于文本边距的WordprocessingML表格，其中第二行通过表格行级别对齐被左对齐到左边距：

        123

        可以使用以下WordprocessingML来指定该行级别设置：

        <w:trPr>
            <w:jc w:val="start"/>
        </w:trPr>

        jc元素指定了作为表格属性异常的行集合必须相对于文本边距左对齐。结束示例]
        """
        return getattr(self, qn('w:jc'), None)

    @property
    def hidden(self) -> Optional[CT_OnOff]:
        """17.4.20 hidden (隐藏表行标记)¶

        hidden (Hidden Table Row Marker)

        该元素指定当前表格行的结束字符所代表的字形不会显示在当前文档中。

        【注：此设置用于隐藏行尾符号，以确保整个表格行被隐藏并不在文档中显示，因为如果行的任何部分可见，则该行会被显示。结束注】

        【注：应用程序可以具有允许显示隐藏内容的设置，在这种情况下，此内容可以可见 - 此属性并不意味着取代该设置。结束注】

        如果省略此元素，则此表格行将不会在文档中隐藏。

        【示例：考虑一个具有指定隐藏行的表格，该要求使用以下WordprocessingML来指定：

        <w:tbl>
            …
            <w:tr>
                <w:trPr>
                    <w:hidden />
                    …
                </w:trPr>
                …
            </w:tr>
        </w:tbl>

        在此示例中，该行将不会显示也不会打印，因为隐藏元素在表格行的属性中被指定。示例结束】

        该元素的内容模型由§17.17.4中的通用布尔属性定义确定。
        """
        return getattr(self, qn('w:hidden'), None)


class CT_TrPr(CT_TrPrBase):
    """17.4.81 trPr (表格行属性)

    trPr (Table Row Properties)

    该元素指定应用于当前表格行的行级属性集合。每个唯一属性由此元素的子元素指定。这些属性影响父表格中当前行中所有单元格的外观，但可以被各个单元格级别的属性覆盖，如每个属性所定义的那样。

    【示例：考虑以下WordprocessingML表格：

    ...

    第一行必须具有一个表格行级别的属性，该属性指定无论其内容如何，该行的高度都应限制为0.1英寸（144个点的二十分之一），可使用trHeight元素指定如下：

    <w:trPr>
        <w:trHeight w:val="144" w:hRule="exact"/>
        …
    </w:trPr>

    trPr元素指定应用于文档中当前表格行的表格行属性集合，本例中使用了trHeight元素指定了行高要求（§17.4.80）。示例结束】
    """

    @property
    def ins(self) -> Optional[CT_TrackChange]:
        return getattr(self, qn('w:ins'), None)

    @property
    def delete(self) -> Optional[CT_TrackChange]:
        return getattr(self, qn('w:del'), None)

    @property
    def trPrChange(self) -> Optional[CT_TrPrChange]:
        return getattr(self, qn('w:trPrChange'), None)


class CT_Row(EG_ContentCellContent):
    """17.4.78 tr (表格行)

    tr (Table Row)

    该元素指定一个单独的表格行，其中包含表格的单元格。WordprocessingML中的表格行类似于HTML的tr元素。

    一个tr元素具有一个格式化的子元素trPr（§17.4.81），它定义了该行的属性。表格行上的每个唯一属性都由该元素的子元素指定。此外，表格行可以包含任何行级内容，这允许使用表格单元格。

    如果表格单元格不包含除行属性之外的至少一个子元素，则此文档应被视为损坏。

    【示例：考虑由一个单元格组成的单个表格，其中包含文本Hello, world：

    ...

    这个表格行的内容由以下WordprocessingML表示：

    <w:tr>
        <w:tc>
            <w:tcPr>
                <w:tcW w:w="0" w:type="auto"/>
            </w:tcPr>
            <w:p>
                <w:r>
                    <w:t>Hello, world</w:t>
                </w:r>
            </w:p>
        </w:tc>
    </w:tr>

    tr元素包含一个行级元素 - 在这种情况下是一个表格单元格。示例结束】
    """

    @property
    def tblPrEx(self) -> Optional[CT_TblPrEx]:
        """17.4.60 tblPrEx (表级属性异常)¶

        tblPrEx (Table-Level Property Exceptions)

        此元素指定一组表格属性，应用于此行的内容，而不是在tblPr元素中指定的表格属性。

        【注意：这些属性通常用于旧文档的情况，以及两个现有独立表格合并的情况（为了防止第二个表格的外观被第一个表格的外观覆盖）。结束注意】
        """
        return getattr(self, qn('w:tblPrEx'), None)

    @property
    def trPr(self) -> Optional[CT_TrPr]:
        """17.4.81 trPr (表格行属性)¶

        trPr (Table Row Properties)

        该元素指定应用于当前表格行的行级属性集合。每个唯一属性由此元素的子元素指定。这些属性影响父表格中当前行中所有单元格的外观，但可以被各个单元格级别的属性覆盖，如每个属性所定义的那样。

        【示例：考虑以下WordprocessingML表格：

        ...

        第一行必须具有一个表格行级别的属性，该属性指定无论其内容如何，该行的高度都应限制为0.1英寸（144个点的二十分之一），可使用trHeight元素指定如下：

        <w:trPr>
            <w:trHeight w:val="144" w:hRule="exact"/>
            …
        </w:trPr>

        trPr元素指定应用于文档中当前表格行的表格行属性集合，本例中使用了trHeight元素指定了行高要求（§17.4.80）。示例结束】
        """

        return getattr(self, qn('w:trPr'), None)

    @property
    def content_cell(
        self,
    ) -> Optional[
        CT_Tc | CT_CustomXmlCell | CT_SdtCell | CT_ProofErr | CT_PermStart | CT_Perm | CT_RunTrackChange
    ]:
        return self.choice_and_more(*EG_ContentCellContent.content_cell_content_choice_tags)  # type: ignore

    @property
    def rsidRPr(self) -> Optional[ST_LongHexNumber]:
        """rsidRPr（表格行字符格式的修订标识符）

        指定一个用于跟踪最后修改主文档中表示表格行标记的字形字符时的编辑会话的唯一标识符。

        如果文档中存在具有相同值的所有rsid*属性，则应表明这些区域在同一个编辑会话中被修改（在连续保存操作之间的时间）。

        生产者可以选择增加修订保存ID值，以指示后续的编辑会话，从而表明修改相对于该文档中其他修改的顺序。

        此属性的可能值由ST_LongHexNumber简单类型（§17.18.50）定义。
        """
        _val = self.attrib.get(qn('w:rsidRPr'))

        if _val is not None:
            return ST_LongHexNumber(str(_val))
        return None

    @property
    def rsidR(self) -> Optional[ST_LongHexNumber]:
        """rsidR（表格行的修订标识符）

        指定一个用于跟踪将表格行添加到主文档时的编辑会话的唯一标识符。

        如果文档中存在具有相同值的所有rsid*属性，则应表明这些区域在同一个编辑会话中被修改（在连续保存操作之间的时间）。

        生产者可以选择增加修订保存ID值，以指示后续的编辑会话，从而表明修改相对于该文档中其他修改的顺序。

        此属性的可能值由ST_LongHexNumber简单类型（§17.18.50）定义。
        """
        _val = self.attrib.get(qn('w:rsidR'))

        if _val is not None:
            return ST_LongHexNumber(str(_val))
        return None

    @property
    def rsidDel(self) -> Optional[ST_LongHexNumber]:
        """rsidDel（删除表格行的修订标识符）

        指定一个用于跟踪从主文档中删除该行时的编辑会话的唯一标识符。

        如果文档中存在具有相同值的所有rsid*属性，则应表明这些区域在同一个编辑会话中被修改（在连续保存操作之间的时间）。

        生产者可以选择增加修订保存ID值，以指示后续的编辑会话，从而表明修改相对于该文档中其他修改的顺序。

        此属性的可能值由ST_LongHexNumber简单类型（§17.18.50）定义。
        """
        _val = self.attrib.get(qn('w:rsidDel'))

        if _val is not None:
            return ST_LongHexNumber(str(_val))
        return None

    @property
    def rsidTr(self) -> Optional[ST_LongHexNumber]:
        """rsidTr（表格行属性的修订标识符）

        指定一个用于跟踪在此文档中最后修改表格行属性时的编辑会话的唯一标识符。

        如果文档中存在具有相同值的所有rsid*属性，则应表明这些区域在同一个编辑会话中被修改（在连续保存操作之间的时间）。

        生产者可以选择增加修订保存ID值，以指示后续的编辑会话，从而表明修改相对于该文档中其他修改的顺序。

        此属性的可能值由ST_LongHexNumber简单类型（§17.18.50）定义。
        """
        _val = self.attrib.get(qn('w:rsidTr'))

        if _val is not None:
            return ST_LongHexNumber(str(_val))
        return None


class ST_TblLayoutType(ST_BaseEnumType):
    fixed = 'fixed'
    autofit = 'autofit'


class CT_TblLayoutType(OxmlBaseElement):
    @property
    def type(self) -> Optional[ST_TblLayoutType]:
        _val = self.attrib.get(qn('w:type'))

        if _val is not None:
            return ST_TblLayoutType(str(_val))
        return None


class ST_TblOverlap(ST_BaseEnumType):
    never = 'never'
    overlap = 'overlap'


class CT_TblOverlap(OxmlBaseElement):
    @property
    def val(self) -> ST_TblOverlap:
        _val = self.attrib[qn('w:val')]

        return ST_TblOverlap(str(_val))


class CT_TblPPr(OxmlBaseElement):
    @property
    def leftFromText(self) -> Optional[s_ST_TwipsMeasure]:
        _val = self.attrib.get(qn('w:leftFromText'))

        if _val is not None:
            return s_to_ST_TwipsMeasure(str(_val))
        return None

    @property
    def rightFromText(self) -> Optional[s_ST_TwipsMeasure]:
        _val = self.attrib.get(qn('w:rightFromText'))

        if _val is not None:
            return s_to_ST_TwipsMeasure(str(_val))
        return None

    @property
    def topFromText(self) -> Optional[s_ST_TwipsMeasure]:
        _val = self.attrib.get(qn('w:topFromText'))

        if _val is not None:
            return s_to_ST_TwipsMeasure(str(_val))
        return None

    @property
    def bottomFromText(self) -> Optional[s_ST_TwipsMeasure]:
        _val = self.attrib.get(qn('w:bottomFromText'))

        if _val is not None:
            return s_to_ST_TwipsMeasure(str(_val))
        return None

    @property
    def vertAnchor(self) -> Optional[ST_VAnchor]:
        _val = self.attrib.get(qn('w:vertAnchor'))

        if _val is not None:
            return ST_VAnchor(str(_val))
        return None

    @property
    def horzAnchor(self) -> Optional[ST_HAnchor]:
        _val = self.attrib.get(qn('w:horzAnchor'))

        if _val is not None:
            return ST_HAnchor(str(_val))
        return None

    @property
    def tblpXSpec(self) -> Optional[s_ST_XAlign]:
        _val = self.attrib.get(qn('w:tblpXSpec'))

        if _val is not None:
            return s_ST_XAlign(str(_val))
        return None

    @property
    def tblpX(self) -> Optional[ST_SignedTwipsMeasure]:
        _val = self.attrib.get(qn('w:tblpX'))

        if _val is not None:
            return to_ST_SignedTwipsMeasure(str(_val))
        return None

    @property
    def tblpYSpec(self) -> Optional[s_ST_YAlign]:
        _val = self.attrib.get(qn('w:tblpYSpec'))

        if _val is not None:
            return s_ST_YAlign(str(_val))
        return None

    @property
    def tblpY(self) -> Optional[ST_SignedTwipsMeasure]:
        _val = self.attrib.get(qn('w:tblpY'))

        if _val is not None:
            return to_ST_SignedTwipsMeasure(str(_val))
        return None


class CT_TblCellMar(OxmlBaseElement):
    """17.4.42 tblCellMar (表格单元格边距默认值)¶

        tblCellMar (Table Cell Margin Defaults)

        该元素指定了当前表中所有单元格的默认单元格边距设置。这些设置可以被包含在表格单元格属性内的tcMar元素指定的表格单元格边距定义 (§17.4.68) 或一组表级属性异常 (§17.4.41) 所覆盖。

        如果省略了此元素，则它应从相关表样式中继承表格单元格边距。如果在样式层次结构中从未指定表格边距，则每个边距应使用其默认边距大小（参见子元素定义）。

        [示例：考虑一个表，其默认单元格边距为所有边的0.1英寸，如下所示：

        123

        通过以下 WordprocessingML 指定了此默认表格单元格边距集合：

        <w:tblPr>
            <w:tblCellMar>
                <w:top w:w="144" w:type="dxa"/>
                <w:start w:w="144" w:type="dxa"/>
                <w:bottom w:w="144" w:type="dxa"/>
                <w:end w:w="144" w:type="dxa"/>
            </w:tblCellMar>
            …
        </w:tblPr>

        作为 tblPr 的子元素的 tblCellMar 指定了当前表中所有单元格的默认单元格边距集合，在此示例中为所有边 144 点的二十分之一。示例结束]

    17.4.41 tblCellMar (表格单元格边距异常)

        tblCellMar (Table Cell Margin Exceptions)

        该元素通过一组表级属性异常指定了父表行中所有单元格的单元格边距。这些设置可以被包含在表格单元格属性内的tcMar元素指定的表格单元格边距定义所覆盖 (§17.4.41)。

        如果省略了此元素，则它应从表级单元格边距 (§17.4.42) 继承表格单元格边距。

        [示例：考虑一个表，其最后两行通过表级属性异常被定义为所有边的默认单元格边距为0.1英寸，如下所示：

        123

        通过以下 WordprocessingML 指定了此表格单元格边距异常集合：

        <w:tblPrEx>
            <w:tblCellMar>
                <w:top w:w="144" w:type="dxa"/>
                <w:start w:w="144" w:type="dxa"/>
                <w:bottom w:w="144" w:type="dxa"/>
                <w:end w:w="144" w:type="dxa"/>
            </w:tblCellMar>
            …
        </w:tblPrEx>

        作为 tblPrEx 的子元素的 tblCellMar 指定了当前表中最后两行中所有单元格的默认单元格边距，此示例中为所有边 144 点的二十分之一。示例结束]
    """

    @property
    def top(self) -> Optional[CT_TblWidth]:
        """17.4.75 top (表格单元格上边距默认值)¶

        top (Table Cell Top Margin Default)

        该元素指定应在单元格内容的顶部范围和父表中所有表单元格的顶部边框之间留下的空间量。此设置可以被包含在表单元格属性（§17.4.77）中的top元素指定的表单元格顶部边距定义所覆盖。

        该值由其type属性应用的单位指定。对于此元素的类型pct或auto的任何宽度值都将被忽略。

        如果省略了此元素，则它应继承与关联表样式的表单元格边距。如果在样式层次结构中从未指定顶部边距，则此表格默认情况下不应具有顶部单元格填充（除了单个单元格覆盖）。

        【示例：考虑一个二乘二表格，在其中默认表单元格顶部边距被指定为正好0.25英寸，如下所示（在下面的第一个表单元格中用箭头标记）：

        123

        此表格属性使用以下WordprocessingML标记指定：

        <w:tbl>
            <w:tblPr>
                <w:tblCellMar>
                    <w:top w:w="360" w:type="dxa"/>
                </w:tblCellMar>
            </w:tblPr>
            …
        </w:tbl>

        表中的每个单元格都具有将其设置为360个二十分之一点的默认单元格边距。结束示例】

        17.4.77 top (表格单元格上边距异常)

        top (Table Cell Top Margin Exception)

        该元素指定了在表格中的特定单元格内容的顶部边界和表格中特定单元格顶部边框之间应留出的空间量。此设置应覆盖表格属性中包含的顶部元素指定的表格单元格顶部边距定义（§17.4.75）。

        此值以其type属性应用的单位指定。对于此元素，任何类型为pct或auto的宽度值都将被忽略。

        如果省略，则此表格单元格将使用在表格属性中包含的顶部元素中定义的底部单元格边距（§17.4.75）。

        【示例：考虑一个带有两个单元格的表格，其中通过例外指定第一个表格单元格的顶部边距要比其他表格单元格的边距大十倍（0.2英寸对比0.02英寸）：

        123

        表格中的第一个单元格将使用以下WordprocessingML进行指定：

        <w:tc>
            <w:tcPr>
                <w:tcMar>
                    <w:top w:w="288" w:type="dxa" />
                </w:tcMar>
            </w:tcPr>
        </w:tc>

        这个表格中的第一个单元格应用了一个例外，将表格单元格的顶部边距设置为288个点的二十分之一（0.2英寸）。示例结束】
        """
        return getattr(self, qn('w:top'), None)

    @property
    def start(self) -> Optional[CT_TblWidth]:
        """17.4.34 start (表格单元前导边距默认值)¶

            start (Table Cell Leading Margin Default)

            该元素指定了应在单元格内容的前沿与父表格（或表格行）中所有表格单元格的前沿之间留下的空间量。此设置可以通过单元格的属性中包含的start元素指定的表格单元格前导边距定义进行覆盖（§17.4.35）。

            此值以其type属性应用的单位指定。对于此元素，类型为pct或auto的任何宽度值都将被忽略。

            如果省略了此元素，则应从关联表样式继承表格单元格边距。如果在样式层次结构中从未指定前导边距，则此表将默认具有115个点的左单元格填充（除非有单独的单元格覆盖）。

            [示例：考虑一个2x2的LTR表格，其中默认的表格单元格前导边距被指定为确切的0.25英寸，如下所示（在下面的第一个表格单元格中用箭头标记）：

            123 123

            此表属性使用以下WordprocessingML标记指定：

            <w:tbl>
                <w:tblPr>
                    <w:tblCellMar>
                        <w:start w:w="360" w:type="dxa"/>
                    </w:tblCellMar>
                </w:tblPr>
                …
            </w:tbl>

            表中的每个单元格都具有将其默认前导单元格边距设置为360个点的设置。示例结束]

        17.4.35 start (表格单元前导边距异常)

            start (Table Cell Leading Margin Exception)

            该元素指定了应在当前单元格内容的前沿与表格中特定单个单元格的前沿边框之间留下的空间量。此设置应覆盖表格属性中包含的start元素指定的表格单元格前导边距定义（§17.4.34）。

            此值以其type属性应用的单位指定。对于此元素，类型为pct或auto的任何宽度值都将被忽略。

            如果省略了此元素，则此表格单元格将使用表格属性中包含的start元素定义的前导单元格边距。

            [示例：考虑一个两行两列的LTR表格，其中第二行的第一个表格单元格通过异常指定的前导边距为0.5英寸，导致文本位于单元格内部0.5英寸处，如下所示：

            123

            可以使用以下WordprocessingML为此单元格指定异常：

            <w:tc>
                <w:tcPr>
                    <w:tcMar>
                        <w:start w:w="720" w:type="dxa" />
                    </w:tcMar>
                </w:tcPr>
            </w:tc>

            此表中的R2C1单元格具有应用于表格单元格前导边距设置的异常，使其为720个点（0.5英寸）。示例结束]
        """
        return getattr(self, qn('w:start'), None)

    @property
    def left(self) -> Optional[CT_TblWidth]:
        """无资料 左边距离 ?"""
        return getattr(self, qn('w:left'), None)

    @property
    def bottom(self) -> Optional[CT_TblWidth]:
        """17.4.5 bottom (表格单元格底部边距默认值)¶

            bottom (Table Cell Bottom Margin Default)

            该元素指定了在父表格（或表格行）内所有表格单元格的内容底部范围与边框之间应留出的空间量。此设置可以被表格单元格属性中 bottom 元素指定的单元格底部边距定义覆盖（§17.4.2）。

            该值以其类型属性所应用的单位指定。对于该元素，任何类型为 pct 或 auto 的宽度值应被忽略。

            如果省略此元素，则应继承关联表格样式的表格单元格边距。如果在样式层次结构中从未指定底部边距，则默认情况下此表格将没有底部单元格填充（除非有单独的单元格覆盖）。

            【示例：考虑一个 2x2 的表格，其中默认表格单元格底部边距被指定为 0.25 英寸，如下所示（以下图第一个单元格中的箭头所示）：

            此表格属性使用以下 WordprocessingML 标记指定：

            <w:tbl>
                <w:tblPr>
                    <w:tblCellMar>
                        <w:bottom w:w="360" w:type="dxa"/>
                    </w:tblCellMar>
                </w:tblPr>
                …
            </w:tbl>

            表格中的每个单元格都有一个默认的单元格边距，设置为 360 个二十分之一点。结束示例】

        17.4.2 bottom (表格单元格底部边距异常)

            bottom (Table Cell Bottom Margin Exception)

            该元素指定了在表格中某个特定单元格的内容底部范围与单元格边框之间应留出的空间量。此设置应覆盖表格属性中 bottom 元素指定的单元格底部边距定义（§17.4.5）。

            该值以其类型属性所应用的单位指定。对于该元素，任何类型为 pct 或 auto 的宽度值应被忽略。

            如果省略此元素，则该单元格应使用表格属性中 bottom 元素中定义的底部单元格边距（§17.4.5）。

            【示例：考虑一个包含两个单元格的表格，其中第一个单元格的底部边距通过例外情况指定为比其他单元格边距大十倍（0.2 英寸对比 0.02 英寸）：

            表格中第一个单元格的 WordprocessingML 指定如下：

            <w:tc>
                <w:tcPr>
                    <w:tcMar>
                        <w:bottom w:w="288" w:type="dxa" />
                    </w:tcMar>
                </w:tcPr>
            </w:tc>

            此表格中的第一个单元格应用了一个例外情况，将单元格底部边距设置为 288 个二十分之一点（0.2 英寸）。结束示例】
        """
        return getattr(self, qn('w:bottom'), None)

    @property
    def end(self) -> Optional[CT_TblWidth]:
        """17.4.11 end (表格单元格尾随边距默认值)¶

        end (Table Cell Trailing Margin Default)

        该元素指定了在父表格（或表格行）中所有表格单元格的尾部内容和尾部边框之间应存在的空间量。此设置可以被表格单元格属性中包含的 end 元素指定的单元格尾部边距覆盖（§17.4.10）。

        此值以其 type 属性应用的单位指定。对于此元素的类型为百分比或自动的任何宽度值都将被忽略。

        如果省略，则它将继承与关联表格样式相关联的表格单元格边距。如果从未在样式层次结构中指定尾部边距，则此表将具有默认的 115 个点（0.08 英寸）左单元格填充（除非单个单元格被覆盖）。

        【示例：考虑一个两行两列的从左到右的表格，其中默认表格单元格尾部边距被指定为确切的 0.25 英寸，如下图所示（在下面的第一个表格单元格中用箭头标记）：

        此表格属性使用以下 WordprocessingML 标记指定：

        <w:tbl>
            <w:tblPr>
                <w:tblCellMar>
                    <w:end w:w="360" w:type="dxa"/>
                </w:tblCellMar>
            </w:tblPr>
            …
        </w:tbl>

        表格中的每个单元格都具有将其默认尾部单元格边距设置为 360 个点的设置。结束示例】

        17.4.10 end (表格单元格尾随边距异常)¶

        end (Table Cell Trailing Margin Exception)

        该元素指定了当前单元格文本内容的尾部范围与表格中特定单个表格单元格的尾部边框之间应存在的空间量。此设置将覆盖表格属性中包含的 end 元素指定的单元格尾部边距定义（§17.4.11）。

        此值以其 type 属性应用的单位指定。对于此元素的类型为百分比或自动的任何宽度值都将被忽略。

        如果省略，则此表格单元格将使用表格属性中包含的 end 元素指定的尾部单元格边距。

        【示例：考虑一个两行两列的从左到右的表格，其中第二行的第一个表格单元格的尾部边距通过异常指定为0.5英寸，如下图所示的区域：

        123

        此单元格的异常将使用以下 WordprocessingML 指定：

        <w:tc>
            <w:tcPr>
                <w:tcMar>
                    <w:end w:w="720" w:type="dxa" />
                </w:tcMar>
            </w:tcPr>
            …
        </w:tc>

        此表格中的 R2C1 单元格具有应用于表格单元格尾部单元格边距的异常，将其设置为720个点（0.5英寸）。结束示例】
        """
        return getattr(self, qn('w:end'), None)

    @property
    def right(self) -> Optional[CT_TblWidth]:
        """无资料 右边距离 ?"""
        return getattr(self, qn('w:right'), None)


class CT_TblBorders(OxmlBaseElement):
    """17.4.38 tblBorders (表格边框合集)

        tblBorders (Table Borders)

        该元素使用其子元素定义的六种边框类型，指定了当前表格边缘的边框集合。

        如果任何行的单元格间距非零，如使用tblCellSpacing元素（§17.4.44; §17.4.43; §17.4.45）指定的，那么没有边框冲突，表格边框（或如果指定了表级别异常边框，则显示表级别异常边框）将显示出来。

        如果单元格间距为零，则存在冲突 [示例：在第一列的所有单元格的左边框和表格的左边框之间的冲突。示例结束]，应按以下方式解决：

        - 如果存在单元格边框，则显示单元格边框
        - 如果没有单元格边框，但在此表格行上存在表级别异常边框，则显示表级别异常边框
        - 如果没有单元格或表级别异常边框，则显示表格边框

        如果省略了此元素，则此表格将具有由关联表样式指定的边框。如果在样式层次结构中未指定边框，则此表格将不具有任何表格边框。

    17.4.39 tblBorders (表格边框异常合集)

        tblBorders (Table Borders Exceptions)

        该元素通过一组表级别属性异常，使用其子元素定义的六种边框类型，指定了父表格行边缘的边框集合。

        如果任何行的单元格间距非零，如使用tblCellSpacing元素（§17.4.44; §17.4.43; §17.4.45）指定的，那么没有边框冲突，并且将显示表级别异常边框。

        如果单元格间距为零，则存在冲突 [示例：在第一列的所有单元格的左边框和表级别异常的左边框之间的冲突。示例结束]，应按以下方式解决：

        - 如果存在单元格边框，则显示单元格边框
        - 如果不存在单元格边框，则显示表级别异常边框

        如果省略了此元素，则此表格将具有由关联表级别边框（§17.4.38）指定的边框。
    """

    @property
    def top(self) -> Optional[CT_Border]:
        """17.4.76 top (表格上边框)¶

        top (Table Top Border)

        该元素指定应在当前表格的顶部显示的边框。此表格边框在文档中的外观应由以下设置确定：

        - 边框的显示取决于由tcBorders元素（§17.4.66）和tblBorders元素（§17.4.39；§17.4.38）定义的冲突解决算法。

        如果省略了此元素，则此表格的顶部应具有由关联表样式指定的边框。

        如果在样式层次结构中未指定顶部边框，则此表格不应具有顶部边框。

        【示例：考虑一个表格，在其中表格属性指定了顶部表格边框，如下所示：

        此顶部表格边框使用以下WordprocessingML指定：

        <w:tbl>
            <w:tblPr>
                <w:tblBorders>
                    <w:top w:val="thinThickThinMediumGap" w:sz="24" w:space="0"
                        w:color="D0D0D0" w:themeColor="accent3" w:themeTint="99"/>
                </w:tblBorders>
            </w:tblPr>
            …
        </w:tbl>

        top元素指定了一个类型为thinThinThickMediumGap的三点顶部表格边框。结束示例】
        """
        return getattr(self, qn('w:top'), None)

    @property
    def start(self) -> Optional[CT_Border]:
        """17.4.36 start (表格前缘边框)¶

        start (Table Leading Edge Border)

        该元素指定了应在当前表格的前沿（LTR表格为左侧，RTL表格为右侧）显示的边框。文档中该表格边框的外观应由以下设置确定：

        边框的显示取决于由tcBorders元素（§17.4.66）和tblBorders元素（§17.4.39;§17.4.38）定义的冲突解决算法
        如果省略了此元素，则此表格的前沿将具有由相关表样式指定的边框。如果在样式层次结构中未指定前沿边框，则此表将不具有左边框。

        [示例：考虑一个LTR表格，其中表格属性指定了前沿表格边框，如下所示：

        123

        此前沿表格边框将使用以下WordprocessingML指定：

        <w:tbl>
            <w:tblPr>
                <w:tblBorders>
                    <w:start w:val="thinThickThinMediumGap" w:sz="24" w:space="0"
                        w:color="D0D0D0" w:themeColor="accent3" w:themeTint="99"/>
                </w:tblBorders>
            </w:tblPr>
            …
        </w:tbl>

        start元素指定了类型为thinThinThickMediumGap的三点前沿表格边框。示例结束]
        """
        return getattr(self, qn('w:start'), None)

    @property
    def left(self) -> Optional[CT_Border]:
        """无资料 左边框 ?"""
        return getattr(self, qn('w:left'), None)

    @property
    def bottom(self) -> Optional[CT_Border]:
        """17.4.4 bottom (表格底部边框)

        bottom (Table Bottom Border)

        该元素指定了当前表格底部显示的边框。此表格边框在文档中的显示方式应由以下设置决定：

        - 边框的显示受 tcBorders 元素（§17.4.66）和 tblBorders 元素（§17.4.39;§17.4.38）定义的冲突解决算法的影响。

        如果省略此元素，则该表格底部将使用关联表格样式指定的边框。如果样式层次结构中未指定底部边框，则该表格将没有底部边框。

        【示例：考虑一个表格，其中表格属性指定了底部表格边框，如下所示：

        123

        此底部表格边框使用以下 WordprocessingML 指定：

        <w:tbl>
            <w:tblPr>
                <w:tblBorders>
                    <w:bottom w:val="thinThickThinMediumGap" w:sz="24" w:space="0" w:color="D0D0D0" w:themeColor="accent3" w:themeTint="99"/>
                </w:tblBorders>
            </w:tblPr>
            …
        </w:tbl>

        bottom 元素指定了一种类型为 thinThinThickMediumGap 的三点底部表格边框。结束示例】
        """
        return getattr(self, qn('w:bottom'), None)

    @property
    def end(self) -> Optional[CT_Border]:
        """17.4.13 end (表格后缘边框)¶

        end (Table Trailing Edge Border)

        该元素指定当前表格的尾部边界（LTR 表格的右侧，RTL 表格的左侧）应显示的边框。文档中此表格边框的外观将由以下设置确定：

        - 边框的显示受到由 tcBorders 元素（§17.4.66）和 tblBorders 元素（§17.4.39; §17.4.38）定义的冲突解决算法的影响。

        如果省略此元素，则此表格的尾部边缘将具有由关联表格样式指定的边框。如果样式层次结构中未指定尾部边界，则此表格将不具有尾部边界。

        【示例：考虑一个 LTR 表格，在其中表格属性指定了尾部边界表格边框，如下所示：

        123

        此尾部边界表格边框使用以下 WordprocessingML 指定：

        <w:tbl>
            <w:tblPr>
                <w:tblBorders>
                    <w:end w:val="thinThickThinMediumGap" w:sz="24" w:space="0"
                        w:color="D0D0D0" w:themeColor="accent3" w:themeTint="99"/>
                </w:tblBorders>
            </w:tblPr>
            …
        </w:tbl>

        end 元素指定了一个类型为 thinThinThickMediumGap 的三点尾部边界表格边框。结束示例】
        """
        return getattr(self, qn('w:end'), None)

    @property
    def right(self) -> Optional[CT_Border]:
        """无资料 右边框 ?"""
        return getattr(self, qn('w:right'), None)

    @property
    def insideH(self) -> Optional[CT_Border]:
        """17.4.22 insideH (表格内水平边缘边框)¶

        insideH (Table Inside Horizontal Edges Border)

        该元素指定在父表格的最外边缘之外的所有水平表格单元格边框上应显示的边框（所有不是顶部或底部边框的水平边框）。

        该表格单元格边框在文档中的显示方式应由以下设置确定：

        - 边框在内部边缘上的显示取决于由tcBorders元素（§17.4.66）和tblBorders元素（§17.4.39;§17.4.38）定义的冲突解析算法。

        如果省略此元素，则该表格的内部水平边框将具有与关联表格样式中指定的边框相同的边框。如果在样式层次结构中未指定内部水平边框，则该表格将不具有内部水平边框。

        【示例：考虑一个表格，在该表格中，表格指定在所有内部水平和垂直边缘上都有边框，如下所示：

        123

        这个内部水平单元格边框使用以下WordprocessingML指定：

        <w:tblPr>
            <w:tblBorders>
                <w:insideH w:val="thickThinSmallGap" w:sz="24" w:space="0" w:color="auto"/>
                <w:insideV w:val="thickThinSmallGap" w:sz="24" w:space="0" w:color="auto"/>
            </w:tblBorders>
            …
        </w:tblPr>

        insideH元素指定了一个3点的thickThinSmallGap类型的边框。结束示例】
        """
        return getattr(self, qn('w:insideH'), None)

    @property
    def insideV(self) -> Optional[CT_Border]:
        """17.4.24 insideV (表格内部垂直边缘边框)¶

        insideV (Table Inside Vertical Edges Border)

        该元素指定应显示在父表格的最外边缘之外的所有垂直表格单元格边框上的边框（所有垂直边框，不是最左边或最右边的边框）。该表格单元格边框在文档中的显示方式应由以下设置确定：

        - 边框在内部边缘上的显示取决于由tcBorders元素（§17.4.66）和tblBorders元素（§17.4.39;§17.4.38）定义的冲突解析算法。

        如果省略此元素，则此表格的内部垂直边框将具有与关联表格样式中指定的边框相同的边框。如果在样式层次结构中未指定内部垂直边框，则该表格中的这些单元格将不具有内部垂直边框。

        【示例：考虑一个表格，在该表格中，表格指定了所有内部水平和垂直边缘上的边框，如下所示：

        123

        这个内部水平单元格边框使用以下WordprocessingML指定：

        <w:tblPr>
            <w:tblBorders>
                <w:insideH w:val="thickThinSmallGap" w:sz="24" w:space="0"
                    w:color="auto"/>
                <w:insideV w:val="thickThinSmallGap" w:sz="24" w:space="0"
                    w:color="auto"/>
            </w:tblBorders>
            …
        </w:tblPr>

        insideV元素指定了一个3点的thickThinSmallGap类型的边框。结束示例】
        """
        return getattr(self, qn('w:insideV'), None)


class CT_TblPrBase(OxmlBaseElement):
    """17.4.58 tblPr (上一个表属性)¶

    tblPr (Previous Table Properties)

    此元素指定了一组先前的表格属性，其修改应归因于特定作者在特定时间进行的修订。该元素包含了在一个特定作者的一组修订之前曾经存在的表格属性设置。这些属性影响父表中所有行和单元格的外观，但可以被各个表级别、行和单元格级别的属性覆盖，每个属性都有自己的定义。

    【示例】考虑以下简单的WordprocessingML表格：

    alt text

    如果将表格对齐设置为居中，并将表格底纹设置为红色，并启用修订标记，如下所示：

    在WordprocessingML中，跟踪此表格上的修订将如下指定：

    <w:tblPr>
        <w:tblStyle w:val="TableGrid"/>
        <w:tblW w:w="0" w:type="auto"/>
        <w:jc w:val="center"/>
        <w:shd w:val="clear" w:color="auto" w:fill="FF0000"/>
        <w:tblLook w:firstRow="true" w:firstColumn="true"
            w:noVBand="true" />
        <w:tblPrChange w:id="0" … >
            <w:tblPr>
                <w:tblStyle w:val="TableGrid"/>
                <w:tblW w:w="0" w:type="auto"/>
                <w:tblLook w:firstRow="true" w:firstColumn="true"
                    w:noVBand="true" />
            </w:tblPr>
        </w:tblPrChange>
    </w:tblPr>

    作为tblPrChange的子元素的tblPr包含了表格属性的先前定义，包括当前跟踪修订之前设置的属性。【示例结束】
    """

    @property
    def tblStyle(self) -> Optional[CT_String]:
        """17.4.62 tblStyle (参考表格样式)¶

        tblStyle (Referenced Table Style)

        这个元素指定了表格样式的样式ID，该样式将用于格式化该表格的内容。

        此格式应用于样式层次结构中的以下位置：

        - 文档默认值
        - 表格样式（此元素）
        - 编号样式
        - 段落样式
        - 字符样式
        - 直接格式设置

        这意味着样式元素（§17.7.4.17）中指定的所有属性，其styleId对应于此元素val属性中的值，在层次结构中的适当级别上应用于表格。

        如果省略了此元素，或者引用了不存在的样式，则不会将任何表格样式应用于当前表格。此外，如果表格属性本身是表格样式的一部分，则此属性将被忽略。

        【示例：考虑以下WordprocessingML片段：

        <w:tblPr>
            <w:tblStyle w:val="TestTableStyle" />
        </w:tblPr>

        该表格指定它将继承styleId为TestTableStyle的表格样式指定的所有表格属性。结束示例】
        """
        return getattr(self, qn('w:tblStyle'), None)

    @property
    def tblpPr(self) -> Optional[CT_TblPPr]:
        """17.4.57 tblpPr (浮动表定位)¶

        tblpPr (Floating Table Positioning)

        该元素指定了关于当前表格的浮动表格的信息。浮动表格是文档中不属于文本主体流的表格，而是绝对定位于当前文档中的非框架内容的特定大小和位置。

        tblpPr元素指定的第一个信息是当前表格实际上是一个浮动表格。这个信息仅通过表格属性中存在tblpPr元素来指定。如果省略了tblpPr元素，则表格在文档中不浮动。

        第二个信息是表格的定位，由存储在tblpPr元素上的属性值指定。在所有绝对定位情况下，表格的定位是相对于其左上角位置的。对于相对定位（例如，居中），表格的定位是相对于其整个框架的。

        请注意，表格仍然在文件中具有逻辑位置（即其在文档中块级元素内的位置）。这个逻辑位置将用于计算表格相对于段落的位置，使用文档中下一个常规（非表格、非框架）段落。

        [示例：考虑一个浮动表格，其在页面范围上的顶部和左侧边缘距离页面范围边缘各三英寸（即左上角位于3英寸 x 3英寸）。可以使用以下WordprocessingML指定这个浮动表格：

        <w:tbl>
            <w:tblPr>
                <w:tblpPr w:leftFromText="144" w:rightFromText="144" w:topFromText="144"
                    w:bottomFromText="144" w:vertAnchor="page" w:horzAnchor="page" w:tblpX="4320"
                    w:tblpY="4320"/>
                …
            </w:tblPr>
            …
        </w:tbl>

        tblpPr元素的存在指示这个表格是一个浮动表格，其属性指定浮动表格应该从当前页面的顶部和左侧边缘各移动4320个twentieths of a point（即3英寸）。结束示例]
        """
        return getattr(self, qn('w:tblpPr'), None)

    @property
    def tblOverlap(self) -> Optional[CT_TblOverlap]:
        """17.4.56 tblOverlap (浮动表允许其他表重叠)¶

        tblOverlap (Floating Table Allows Other Tables to Overlap)

        该元素指定了当前表格在文档中显示时是否允许其他浮动表格与其重叠。如果指定了，则不会进行任何调整以防止具有属性的表格在显示时重叠。如果关闭，则将根据需要调整表格以防止在显示时重叠，并根据需要调整浮动表格的属性。

        如果在给定表格上省略了此元素，则该表格在显示时将允许其他表格重叠。如果父表格不是通过tblpPr元素（§17.4.57）进行浮动，则将忽略此元素。
        """
        return getattr(self, qn('w:tblOverlap'), None)

    @property
    def bidiVisual(self) -> Optional[CT_OnOff]:
        """17.4.1 bidiVisual (视觉上从右到左的表格)

        bidiVisual (Visually Right to Left Table)

        这个元素指定了该表格中的单元格应以从右到左的方向显示。这个元素还影响所有表格级属性的应用。

        当指定此属性时，表格中所有单元格（及表格级属性）的顺序应假设表格为正常的从左到右表格，但单元格应以从右到左的方向显示。【例如：在一个视觉上从右到左的表格中，第一个单元格的左边框必须显示在该单元格的右侧（也就是最右边的单元格）。结束示例】

        如果省略此元素，则表格不应以从右到左的方式显示。
        """
        return getattr(self, qn('w:bidiVisual'), None)

    @property
    def tblStyleRowBandSize(self) -> Optional[CT_DecimalNumber]:
        """17.7.6.7 tblStyleRowBandSize (行带中的行数)

        tblStyleRowBandSize (Number of Rows in Row Band)

        该元素指定了每个表格样式的行带应包含的行数。该元素确定了当前表格中每个行带包含多少行，允许在格式化表格时将行带格式应用于一组行（而不仅仅是单个交替行）。

        如果省略了该元素，则将假定单个行带中的默认行数为1。

        [示例：考虑以下定义的表格样式：


        <w:style w:type="table" w:styleId="exampleTableStyle">
            <w:tblPr>
                <w:tblStyleRowBandSize w:val="3" />
                <w:tblStyleColBandSize w:val="2" />
            </w:tblPr>
            …
        </w:style>

        tblStyleRowBandSize元素指定每个行带的宽度必须为3列 - 因此，必须将band1Horiz行带条件格式应用于表格中的第1至3行，第7至9行等。结束示例]
        """
        return getattr(self, qn('w:tblStyleRowBandSize'), None)

    @property
    def tblStyleColBandSize(self) -> Optional[CT_DecimalNumber]:
        """17.7.6.5 tblStyleColBandSize (列带中的列数)

        该元素指定了每个表格样式列带所包含的列数。该元素确定目前表格的每个列带包含多少列，使得在表格格式化时，可以将列带格式应用于一组列（而不仅仅是单个交替列）。

        如果省略该元素，则默认认为每个单个列带中的列数为1。例如，考虑以下定义的表格样式：

        <w:style w:type="table" w:styleId="exampleTableStyle">
            <w:tblPr>
                <w:tblStyleRowBandSize w:val="3" />
                <w:tblStyleColBandSize w:val="2" />
            </w:tblPr>
            …
        </w:style>

        tblStyleColBandSize元素指定每个列带的宽度必须是2列 - 因此，在表格中，必须对列1和2、5和6等应用band1Vert列带条件格式。示例结束。
        """
        return getattr(self, qn('w:tblStyleColBandSize'), None)

    @property
    def tblW(self) -> Optional[CT_TblWidth]:
        """17.4.63 tblW (首选表格宽度)¶

        tblW (Preferred Table Width)

        这个元素指定了该表格的首选宽度。这个首选宽度是表格布局算法的一部分，由tblLayout元素（§17.4.52; §17.4.53）指定 - 算法的完整描述在ST_TblLayout简单类型中（§17.18.87）。

        表格中的所有宽度都被视为首选，因为：

        - 表格应满足由tblGrid元素（§17.4.48）指定的共享列
        - 两个或更多宽度可能对同一网格列的宽度具有冲突的值
        - 表格布局算法（§17.18.87）可能需要覆盖首选项

        此值是通过其type属性应用的单位中指定的。对于此元素，任何类型为pct的宽度值应相对于页面的文本范围（不包括边距）进行计算。

        如果省略了此元素，则单元格宽度应为auto类型。
        """
        return getattr(self, qn('w:tblW'), None)

    @property
    def jc(self) -> Optional[CT_JcTable]:
        """17.4.28 jc (表格对齐)

        jc (Table Alignment)

        该元素指定了当前表格相对于当前部分的文本边距的对齐方式。当将表格放置在宽度与边距不同的WordprocessingML文档中时，此属性用于确定表格相对于这些边距的位置。如果父表格使用bidiVisual元素（§17.4.1）从右到左排列，则属性的解释将被反转。

        如果在表格上省略此属性，则对齐方式将由相关表格样式确定。如果在样式层次结构中未指定此属性，则表格将从主要边距（在从左到右的表格中为左边距，而在从右到左的表格中为右边距）左对齐，并且缩进为零。

        [示例：考虑以下默认左对齐的WordprocessingML表格：

        ...
        """
        return getattr(self, qn('w:jc'), None)

    @property
    def tblCellSpacing(self) -> Optional[CT_TblWidth]:
        """17.4.43 tblCellSpacing (表格行单元格间距)

        tblCellSpacing (Table Row Cell Spacing)

        该元素指定了父行中所有单元格的默认表格单元格间距（相邻单元格与表格边缘之间的间距）。如果指定了此元素，则它表示表格中所有单元格之间应保留的最小空间，包括表格边框的宽度。需要注意的是，行级单元格间距应添加在文本边距内，并与没有行级缩进或单元格间距的单元格中文本范围的最内侧起始边对齐。行级单元格间距不应增加整体表格的宽度。

        此值以其类型属性应用的单位指定。任何类型为pct或auto的宽度值将被忽略。

        [示例：考虑一个表，其第二行通过表格行属性指定了所有边为0.1英寸的单元格间距，如下所示：

        ...

        此表格行的单元格间距使用以下 WordprocessingML 指定：

        <w:trPr>
            <w:tblCellSpacing w:w="144" w:type="dxa"/>
            …
        </w:trPr>

        作为 trPr 的子元素的 tblCellSpacing 指定了当前行中所有单元格之间的默认单元格间距，在此示例中为144点的二十分之一。示例结束]
        """
        return getattr(self, qn('w:tblCellSpacing'), None)

    @property
    def tblInd(self) -> Optional[CT_TblWidth]:
        """17.4.50 tblInd (表格从前导边距缩进)

        tblInd (Table Indent from Leading Margin)

        该元素指定在文档中当前表格的前导边缘之前添加的缩进（在从左到右的表格中为左边缘，在从右到左的表格中为右边缘）。此缩进应将表格按指定量移入文本边距内。

        该值按照其 type 属性指定的单位来表示。对于此元素，任何类型为 pct 或 auto 的宽度值都将被忽略。

        如果省略此元素，则表格将从关联的表格样式中继承表格缩进。如果在样式层次结构中从未指定表格缩进，则不会向父表格添加缩进。如果在应用 jc 元素的值后，任何表格行的最终对齐方式不是左对齐（§17.4.26;§17.4.27;§17.4.28），则此属性将被忽略。
        """
        return getattr(self, qn('w:tblInd'), None)

    @property
    def tblBorders(self) -> Optional[CT_TblBorders]:
        """17.4.38 tblBorders (表格边框合集)

        tblBorders (Table Borders)

        该元素使用其子元素定义的六种边框类型，指定了当前表格边缘的边框集合。

        如果任何行的单元格间距非零，如使用tblCellSpacing元素（§17.4.44; §17.4.43; §17.4.45）指定的，那么没有边框冲突，表格边框（或如果指定了表级别异常边框，则显示表级别异常边框）将显示出来。

        如果单元格间距为零，则存在冲突 [示例：在第一列的所有单元格的左边框和表格的左边框之间的冲突。示例结束]，应按以下方式解决：

        - 如果存在单元格边框，则显示单元格边框
        - 如果没有单元格边框，但在此表格行上存在表级别异常边框，则显示表级别异常边框
        - 如果没有单元格或表级别异常边框，则显示表格边框

        如果省略了此元素，则此表格将具有由关联表样式指定的边框。如果在样式层次结构中未指定边框，则此表格将不具有任何表格边框。


        """
        return getattr(self, qn('w:tblBorders'), None)

    @property
    def shd(self) -> Optional[CT_Shd]:
        """17.4.31 shd (表格底纹)

        该元素指定了应用于当前表的底纹。与段落底纹类似，此底纹应用于标签内容直至表边界，无论文本是否存在 - 与单元格底纹不同，表底纹应包括任何单元格填充。此属性应被通过任何表级属性异常（§17.4.30）；或此行中任何单元格上的任何单元格级底纹所取代（§17.4.32）。

        该底纹由三个组成部分组成：

        - 背景颜色
        - （可选）图案
        - （可选）图案颜色

        通过在段落后设置背景颜色，然后使用图案提供的蒙版在该背景上应用图案颜色来应用生成的底纹。

        如果省略了此元素，则此表格中的单元格将具有由相关表样式指定的底纹。如果在样式层次结构中未指定单元格底纹，则此表中的单元格将不具有任何单元格底纹（即它们将是透明的）。

        [示例：考虑一个表格，其中第一行的第一个单元格具有单元格级别的红色底纹，如下所示：

        ...

        此表级单元格底纹将使用以下WordprocessingML指定：

        <w:tbl>
            <w:tblPr>
                <w:shd w:val="clear" w:color="auto" w:fill="FF0000"/>
                …
            </w:tblPr>
            …
        </w:tbl>

        shd元素指定使用红色（FF0000）的背景颜色，使用清晰图案的单元格底纹。示例结束]
        """
        return getattr(self, qn('w:shd'), None)

    @property
    def tblLayout(self) -> Optional[CT_TblLayoutType]:
        """17.4.52 tblLayout (表格布局)

        tblLayout (Table Layout)

        这个元素指定了用于在文档中布置该表格内容的算法。当表格在文档中显示时，可以使用固定宽度或自动调整布局算法（每种算法详见val属性引用的简单类型）。

        如果省略了这个元素，则该元素的值应被假定为auto。

        [示例：考虑一个必须使用固定宽度表格布局算法的表格。这一要求使用以下WordprocessingML指定：

        <w:tblPr>
            <w:tblLayout w:type="fixed"/>
        </w:tblPr>

        tblLayout元素指定了表格必须使用固定布局算法。 结束示例]
        """
        return getattr(self, qn('w:tblLayout'), None)

    @property
    def tblCellMar(self) -> Optional[CT_TblCellMar]:
        """17.4.42 tblCellMar (表格单元格边距默认值)¶

        tblCellMar (Table Cell Margin Defaults)

        该元素指定了当前表中所有单元格的默认单元格边距设置。这些设置可以被包含在表格单元格属性内的tcMar元素指定的表格单元格边距定义 (§17.4.68) 或一组表级属性异常 (§17.4.41) 所覆盖。

        如果省略了此元素，则它应从相关表样式中继承表格单元格边距。如果在样式层次结构中从未指定表格边距，则每个边距应使用其默认边距大小（参见子元素定义）。

        [示例：考虑一个表，其默认单元格边距为所有边的0.1英寸，如下所示：

        123

        通过以下 WordprocessingML 指定了此默认表格单元格边距集合：

        <w:tblPr>
            <w:tblCellMar>
                <w:top w:w="144" w:type="dxa"/>
                <w:start w:w="144" w:type="dxa"/>
                <w:bottom w:w="144" w:type="dxa"/>
                <w:end w:w="144" w:type="dxa"/>
            </w:tblCellMar>
            …
        </w:tblPr>

        作为 tblPr 的子元素的 tblCellMar 指定了当前表中所有单元格的默认单元格边距集合，在此示例中为所有边 144 点的二十分之一。示例结束]
        """
        return getattr(self, qn('w:tblCellMar'), None)

    @property
    def tblLook(self) -> Optional[CT_TblLook]:
        """17.4.55 tblLook (表格样式条件格式设置)

        tblLook (Table Style Conditional Formatting Settings)

        该元素指定了所引用的表格样式（如果存在）的条件格式的组件，应用于当前表格。表格样式可以指定多达六种不同的可选条件格式[示例：对第一列进行不同的格式设置。结束示例]，然后可以应用或省略文档中各个表格中的这些格式。

        默认设置是应用行和列条带格式，但不应用第一行、最后一行、第一列或最后一列的格式。

        [示例：考虑一个必须使用所引用的表格样式中以下条件格式属性的表格：

        - 第一行条件格式
        - 最后一行条件格式
        - 无行条带格式
        - 无列条带格式

        生成的WordprocessingML将被指定如下：

        <w:tblPr>
            <w:tblLook w:firstRow="true" w:lastRow="true" w:noHBand="true" w:noVBand="true" />
        </w:tblPr>

        tblLook元素指定了应用于当前表格的表格样式的哪些组件。结束示例]
        """
        return getattr(self, qn('w:tblLook'), None)

    @property
    def tblCaption(self) -> Optional[CT_String]:
        """17.4.40 tblCaption (表格标题)¶

        tblCaption (Table Caption)

        该元素指定了表的标题。

        [示例：考虑一个指定了标题的表。此对象可能包含以下 XML 标记：

        <w:tbl>
            <w:tblPr>
                <w:tblCaption w:val="这是表的标题" />
                …
            </w:tblPr>
        </w:tbl>

        示例结束]
        """
        return getattr(self, qn('w:tblCaption'), None)

    @property
    def tblDescription(self) -> Optional[CT_String]:
        """17.4.46 tblDescription (表格描述)

        该元素指定表格的描述。

        [示例：考虑一个指定了描述的表格。此对象可能包含以下 XML 标记：

        <w:tbl>
            <w:tblPr>
                <w:tblDescription w:val="这里是表格的描述" />
                …
            </w:tblPr>
        </w:tbl>

        示例结束]
        """
        return getattr(self, qn('w:tblDescription'), None)


class CT_TblPr(CT_TblPrBase):
    """17.4.59 tblPr (表属性)

    tblPr (Table Properties)

    此元素指定应用于当前表格的一组表格级别属性。这些属性影响父表中所有行和单元格的外观，但可以被各个表级别、行和单元格级别的属性覆盖，每个属性都有自己的定义。

    【示例】考虑以下简单的WordprocessingML表格：

    ....

    此表格定义了所有边框类型的一点单边框，并设置为页面宽度的100% - 这两个是表格级别的属性。结果表格由以下WordprocessingML表示：

    <w:tbl>
        <w:tblPr>
            <w:tblW w:w="0" w:type="auto"/>
            <w:tblBorders>
                <w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                <w:start w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                <w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                <w:end w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                <w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                <w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>
            </w:tblBorders>
        </w:tblPr>
        …
    </w:tbl>

    在此示例中，tblW元素（§17.4.63）定义了表格的总宽度，这里设置为auto类型，指定表格应自动调整大小以适应其内容。tblBorders元素（§17.4.38）指定了表格的每条边框，并指定了上、左、下、右、内部水平和垂直边框的一点边框。【示例结束】
    """

    @property
    def tblPrChange(self) -> Optional[CT_TblPrChange]:
        return getattr(self, qn('w:tblPrChange'), None)


class CT_TblPrExBase(OxmlBaseElement):
    @property
    def tblW(self) -> Optional[CT_TblWidth]:
        return getattr(self, qn('w:tblW'), None)

    @property
    def jc(self) -> Optional[CT_JcTable]:
        return getattr(self, qn('w:jc'), None)

    @property
    def tblCellSpacing(self) -> Optional[CT_TblWidth]:
        return getattr(self, qn('w:tblCellSpacing'), None)

    @property
    def tblInd(self) -> Optional[CT_TblWidth]:
        return getattr(self, qn('w:tblInd'), None)

    @property
    def tblBorders(self) -> Optional[CT_TblBorders]:
        """17.4.39 tblBorders (表格边框异常合集)

        tblBorders (Table Borders Exceptions)

        该元素通过一组表级别属性异常，使用其子元素定义的六种边框类型，指定了父表格行边缘的边框集合。

        如果任何行的单元格间距非零，如使用tblCellSpacing元素（§17.4.44; §17.4.43; §17.4.45）指定的，那么没有边框冲突，并且将显示表级别异常边框。

        如果单元格间距为零，则存在冲突 [示例：在第一列的所有单元格的左边框和表级别异常的左边框之间的冲突。示例结束]，应按以下方式解决：

        - 如果存在单元格边框，则显示单元格边框
        - 如果不存在单元格边框，则显示表级别异常边框

        如果省略了此元素，则此表格将具有由关联表级别边框（§17.4.38）指定的边框。
        """
        return getattr(self, qn('w:tblBorders'), None)

    @property
    def shd(self) -> Optional[CT_Shd]:
        return getattr(self, qn('w:shd'), None)

    @property
    def tblLayout(self) -> Optional[CT_TblLayoutType]:
        return getattr(self, qn('w:tblLayout'), None)

    @property
    def tblCellMar(self) -> Optional[CT_TblCellMar]:
        """
        17.4.41 tblCellMar (表格单元格边距异常)

        tblCellMar (Table Cell Margin Exceptions)

        该元素通过一组表级属性异常指定了父表行中所有单元格的单元格边距。这些设置可以被包含在表格单元格属性内的tcMar元素指定的表格单元格边距定义所覆盖 (§17.4.41)。

        如果省略了此元素，则它应从表级单元格边距 (§17.4.42) 继承表格单元格边距。

        [示例：考虑一个表，其最后两行通过表级属性异常被定义为所有边的默认单元格边距为0.1英寸，如下所示：

        123

        通过以下 WordprocessingML 指定了此表格单元格边距异常集合：

        <w:tblPrEx>
            <w:tblCellMar>
                <w:top w:w="144" w:type="dxa"/>
                <w:start w:w="144" w:type="dxa"/>
                <w:bottom w:w="144" w:type="dxa"/>
                <w:end w:w="144" w:type="dxa"/>
            </w:tblCellMar>
            …
        </w:tblPrEx>

        作为 tblPrEx 的子元素的 tblCellMar 指定了当前表中最后两行中所有单元格的默认单元格边距，此示例中为所有边 144 点的二十分之一。示例结束]
        """
        return getattr(self, qn('w:tblCellMar'), None)

    @property
    def tblLook(self) -> Optional[CT_TblLook]:
        return getattr(self, qn('w:tblLook'), None)


class CT_TblPrEx(CT_TblPrExBase):
    """17.4.60 tblPrEx (表级属性异常)¶

    tblPrEx (Table-Level Property Exceptions)

    此元素指定一组表格属性，应用于此行的内容，而不是在tblPr元素中指定的表格属性。

    【注意：这些属性通常用于旧文档的情况，以及两个现有独立表格合并的情况（为了防止第二个表格的外观被第一个表格的外观覆盖）。结束注意】
    """

    @property
    def tblPrChange(self) -> Optional[CT_TblPrChange]:
        return getattr(self, qn('w:tblPrChange'), None)


class CT_Tbl(EG_ContentRowContent, EG_RangeMarkupElements):
    """17.4.37 tbl (表格)

    该元素指定了文档中存在的表格的内容。表格是一组段落（和其他块级内容），按行和列排列。WordprocessingML中的表格通过tbl元素定义，类似于HTML中的table标签。

    当文档内容中存在两个具有相同样式（§17.4.62）的tbl元素，并且没有任何插入的p元素时，相应的表格将被视为单个表格。

    [示例：考虑一个空的单元格表格（即一个行、一个列的表格）和四周都有1点边框：

    ...

    该表格由以下WordprocessingML表示：

    <w:tbl>
        <w:tblPr>
            <w:tblW w:w="5000" w:type="pct"/>
            <w:tblBorders>
                <w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                <w:start w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                <w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                <w:end w:val="single" w:sz="4" w:space="0" w:color="auto"/>
            </w:tblBorders>
        </w:tblPr>
        <w:tblGrid>
            <w:gridCol w:w="10296"/>
        </w:tblGrid>
        <w:tr>
            <w:tc>
                <w:tcPr>
                    <w:tcW w:w="0" w:type="auto"/>
                </w:tcPr>
                <w:p/>
            </w:tc>
        </w:tr>
    </w:tbl>

    此表格使用tblW元素（§17.4.63）指定了100%页面宽度的表格宽度；使用tblBorders元素（§17.4.38）指定了一组表格边框；使用tblGrid元素（§17.4.48）定义了表格内共享的一组垂直边缘；并使用tr元素（§17.4.78）定义了单个表格行。示例结束]
    """

    @property
    def range_markup_elements(
        self,
    ) -> list[CT_Bookmark | CT_MarkupRange | CT_MoveBookmark | CT_TrackChange | CT_Markup]:
        return self.choice_and_more(*EG_RangeMarkupElements.range_markup_tags)  # type: ignore

    @property
    def tblPr(self) -> Optional[CT_TblPr]:
        """17.4.59 tblPr (表属性)

        tblPr (Table Properties)

        此元素指定应用于当前表格的一组表格级别属性。这些属性影响父表中所有行和单元格的外观，但可以被各个表级别、行和单元格级别的属性覆盖，每个属性都有自己的定义。

        【示例】考虑以下简单的WordprocessingML表格：

        ....

        此表格定义了所有边框类型的一点单边框，并设置为页面宽度的100% - 这两个是表格级别的属性。结果表格由以下WordprocessingML表示：

        <w:tbl>
            <w:tblPr>
                <w:tblW w:w="0" w:type="auto"/>
                <w:tblBorders>
                    <w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                    <w:start w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                    <w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                    <w:end w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                    <w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                    <w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>
                </w:tblBorders>
            </w:tblPr>
            …
        </w:tbl>

        在此示例中，tblW元素（§17.4.63）定义了表格的总宽度，这里设置为auto类型，指定表格应自动调整大小以适应其内容。tblBorders元素（§17.4.38）指定了表格的每条边框，并指定了上、左、下、右、内部水平和垂直边框的一点边框。【示例结束】
        """
        return getattr(self, qn('w:tblPr'), None)

    @property
    def tblGrid(self) -> Optional[CT_TblGrid]:
        """17.4.48 tblGrid (表格网格)

        tblGrid (Table Grid)

        该元素指定了当前表格的表格网格。表格网格定义了一组网格列，这些网格列定义了表格所有共享的垂直边缘，以及每个网格列的默认宽度。这些网格列宽度随后根据使用的表格布局算法来确定表格的大小 (§17.4.52;§17.4.53)。

        如果省略了表格网格，则将从表格的实际内容中构建一个新网格，假设所有网格列的宽度为0。

        [示例：考虑以下具有四个垂直边缘（网格列）的表格：

        ...

        此表格将具有由以下四个网格列组成的表格网格：

        <w:tblGrid>
            <w:gridCol w:w="2088"/>
            <w:gridCol w:w="1104"/>
            <w:gridCol w:w="3192"/>
            <w:gridCol w:w="3192"/>
        </w:tblGrid>

        tblGrid 元素包含表格网格的当前定义，包括所有网格列以及这些列的默认宽度。示例结束]
        """
        return getattr(self, qn('w:tblGrid'), None)

    @property
    def row_content(
        self,
    ) -> list[
        CT_Row | CT_CustomXmlRow | CT_SdtRow | CT_ProofErr | CT_PermStart | CT_Perm | CT_RunTrackChange | CT_Bookmark | CT_MarkupRange | CT_MoveBookmark | CT_TrackChange | CT_Markup
    ]:
        return self.choice_and_more(*EG_ContentRowContent.content_row_content_choice_tags)  # type: ignore


class CT_TblLook(OxmlBaseElement):
    @property
    def firstRow(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:firstRow'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def lastRow(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:lastRow'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def firstColumn(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:firstColumn'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def lastColumn(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:lastColumn'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def noHBand(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:noHBand'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def noVBand(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:noVBand'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def val(self) -> Optional[ST_ShortHexNumber]:
        _val = self.attrib.get(qn('w:val'))

        if _val is not None:
            return ST_ShortHexNumber(str(_val))
        return None


class ST_FtnPos(ST_BaseEnumType):
    pageBottom = 'pageBottom'
    beneathText = 'beneathText'
    sectEnd = 'sectEnd'
    docEnd = 'docEnd'


class CT_FtnPos(OxmlBaseElement):
    @property
    def val(self) -> ST_FtnPos:
        _val = self.attrib[qn('w:val')]

        return ST_FtnPos(str(_val))


class ST_EdnPos(ST_BaseEnumType):
    sectEnd = 'sectEnd'
    docEnd = 'docEnd'


class CT_EdnPos(OxmlBaseElement):
    @property
    def val(self) -> ST_EdnPos:
        _val = self.attrib[qn('w:val')]

        return ST_EdnPos(_val)


class CT_NumFmt(OxmlBaseElement):
    """17.9.17 numFmt (编号格式)¶

    numFmt (Numbering Format)

    该元素指定了编号定义中此级别的所有编号应使用的编号格式。此信息用于替换级别文本字符串中的 %x，其中 x 是特定的基于一的级别索引，使用适当的值，除非 numFmt 值为 bullet，在这种情况下使用级别文本字符串的字面文本。此值应通过计算自上次使用 val 属性中定义的编号系统以来此级别的段落数来计算。

    当文档具有由 format 属性指定的自定义编号格式时，应使用引用的编号格式。如果无法将引用的编号格式解析为编号格式，则使用 val 属性值指定的编号格式。如果 val 属性的相应值为 custom，则结果由实现定义。

    如果省略此元素，则假定该级别为十进制级别。

    【示例：考虑编号定义中编号级别的以下 WordprocessingML 片段：

    <w:lvl w:ilvl="2">
        <w:start w:val="1" />
        <w:numFmt w:val="lowerRoman" />
        <w:lvlRestart w:val="0" />
        <w:lvlText w:val="%3)" />
        <w:lvlJc w:val="start" />
        <w:pPr>
            <w:ind w:start="1080" w:hanging="360" />
        </w:pPr>
        <w:rPr>
            <w:rFonts w:hint="default" />
        </w:rPr>
    </w:lvl>

    numFmt 值为 lowerLetter 表示消费者必须使用小写字母对此级别的所有编号进行编号：a、b、c…… 示例结束】
    """

    @property
    def val(self) -> ST_NumberFormat:
        """val（编号格式类型）

        指定应用于父对象中所有编号的编号格式。

        【示例：值 lowerLetter 表示消费者必须对此分组中的每个编号使用小写字母：a、b、c…… 示例结束】

        此属性的可能值由 ST_NumberFormat 简单类型（§17.18.59）定义。
        """
        _val = self.attrib[qn('w:val')]

        return ST_NumberFormat(_val)

    @property
    def format(self) -> Optional[str]:
        """format（自定义定义的编号格式）

        使用 XSLT 格式属性定义的语法指定自定义编号格式。

        此格式应用于父对象中的所有编号。

        【示例：值 ア 表示消费者必须使用片假名编号。示例结束】

        此属性的可能值由 ST_String 简单类型（§22.9.2.13）定义。
        """
        _val = self.attrib.get(qn('w:format'))

        if _val is not None:
            return str(str(_val))
        return None


class ST_RestartNumber(ST_BaseEnumType):
    continuous = 'continuous'
    eachSect = 'eachSect'
    eachPage = 'eachPage'


class CT_NumRestart(OxmlBaseElement):
    @property
    def val(self) -> ST_RestartNumber:
        _val = self.attrib[qn('w:val')]

        return ST_RestartNumber(_val)


class CT_FtnEdnRef(OxmlBaseElement):
    @property
    def customMarkFollows(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:customMarkFollows'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def id(self) -> ST_DecimalNumber:
        _val = self.attrib[qn('w:id')]

        return ST_DecimalNumber(_val)


class CT_FtnEdnSepRef(OxmlBaseElement):
    @property
    def id(self) -> ST_DecimalNumber:
        _val = self.attrib[qn('w:id')]

        return ST_DecimalNumber(_val)


class CT_FtnEdn(OxmlBaseElement):
    @property
    def levels(
        self,
    ) -> list[
        CT_CustomXmlBlock | CT_SdtBlock | CT_P | CT_Tbl | CT_ProofErr | CT_PermStart | CT_Perm | CT_RunTrackChange | CT_AltChunk
    ]:
        return self.choice_and_more(*EG_BlockLevelElts.block_level_tags)  # type: ignore

    @property
    def type(self) -> Optional[ST_FtnEdn]:
        _val = self.attrib.get(qn('w:type'))

        if _val is not None:
            return ST_FtnEdn(_val)
        return None

    @property
    def id(self) -> ST_DecimalNumber:
        _val = self.attrib[qn('w:id')]

        return ST_DecimalNumber(_val)


class EG_FtnEdnNumProps(OxmlBaseElement):
    @property
    def numStart(self) -> Optional[CT_DecimalNumber]:
        return getattr(self, qn('w:numStart'), None)

    @property
    def numRestart(self) -> Optional[CT_NumRestart]:
        return getattr(self, qn('w:numRestart'), None)


class CT_FtnProps(EG_FtnEdnNumProps):
    @property
    def pos(self) -> Optional[CT_FtnPos]:
        return getattr(self, qn('w:pos'), None)

    @property
    def numFmt(self) -> Optional[CT_NumFmt]:
        return getattr(self, qn('w:numFmt'), None)


class CT_EdnProps(EG_FtnEdnNumProps):
    @property
    def pos(self) -> Optional[CT_FtnPos]:
        return getattr(self, qn('w:pos'), None)

    @property
    def numFmt(self) -> Optional[CT_NumFmt]:
        return getattr(self, qn('w:numFmt'), None)


class CT_FtnDocProps(CT_FtnProps):
    """

    <xsd:complexType name="CT_FtnDocProps">
        <xsd:complexContent>
            <xsd:extension base="CT_FtnProps">
                <xsd:sequence>
                <xsd:element name="footnote" type="CT_FtnEdnSepRef" minOccurs="0" maxOccurs="3"/>
                </xsd:sequence>
            </xsd:extension>
        </xsd:complexContent>
    </xsd:complexType>
    """

    @property
    def footnote(self) -> list[CT_FtnEdnSepRef]:
        """
        <xsd:element name="footnote" type="CT_FtnEdnSepRef" minOccurs="0" maxOccurs="3"/>
        """

        return self.findall(qn('w:footnote'))  # type: ignore


class CT_EdnDocProps(CT_EdnProps):
    @property
    def endnote(self) -> list[CT_FtnEdnSepRef]:
        return self.findall(qn('w:endnote'))  # type: ignore


class CT_RecipientData(OxmlBaseElement):
    @property
    def active(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:active'), None)

    @property
    def column(self) -> CT_DecimalNumber:
        return getattr(self, qn('w:column'))

    @property
    def uniqueTag(self) -> CT_Base64Binary:
        return getattr(self, qn('w:uniqueTag'))


class CT_Base64Binary(OxmlBaseElement):
    """
    <xsd:complexType name="CT_Base64Binary">
        <xsd:attribute name="val" type="xsd:base64Binary" use="required"/>
    </xsd:complexType>
    """

    @property
    def val(self) -> str:
        return str(self.attrib[qn('w:val')])


class CT_Recipients(OxmlBaseElement):
    @property
    def recipientData(self) -> list[CT_RecipientData]:
        return self.findall(qn('w:recipientData'))  # type: ignore


class CT_OdsoFieldMapData(OxmlBaseElement):
    @property
    def type(self) -> Optional[CT_MailMergeOdsoFMDFieldType]:
        return getattr(self, qn('w:type'), None)

    @property
    def name(self) -> Optional[CT_String]:
        return getattr(self, qn('w:name'), None)

    @property
    def mappedName(self) -> Optional[CT_String]:
        return getattr(self, qn('w:mappedName'), None)

    @property
    def column(self) -> Optional[CT_DecimalNumber]:
        return getattr(self, qn('w:column'), None)

    @property
    def lid(self) -> Optional[CT_Lang]:
        return getattr(self, qn('w:lid'), None)

    @property
    def dynamicAddress(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:dynamicAddress'), None)


class ST_MailMergeSourceType(ST_BaseEnumType):
    database = 'database'
    addressBook = 'addressBook'
    document1 = 'document1'
    document2 = 'document2'
    text = 'text'
    email = 'email'
    native = 'native'
    legacy = 'legacy'
    master = 'master'


class CT_MailMergeSourceType(OxmlBaseElement):
    @property
    def val_source_type(self) -> ST_MailMergeSourceType:
        """

        [有联合类型]
        """
        return ST_MailMergeSourceType(self.attrib[qn('w:val')])


class CT_Odso(OxmlBaseElement):
    @property
    def udl(self) -> Optional[CT_String]:
        return getattr(self, qn('w:udl'), None)

    @property
    def table(self) -> Optional[CT_String]:
        return getattr(self, qn('w:table'), None)

    @property
    def src(self) -> Optional[CT_Rel]:
        return getattr(self, qn('w:src'), None)

    @property
    def colDelim(self) -> Optional[CT_DecimalNumber]:
        return getattr(self, qn('w:colDelim'), None)

    @property
    def type(self) -> Optional[CT_MailMergeSourceType]:
        return getattr(self, qn('w:type'), None)

    @property
    def fHdr(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:fHdr'), None)

    @property
    def fieldMapData(self) -> list[CT_OdsoFieldMapData]:
        return self.findall(qn('w:fieldMapData'))  # type: ignore

    @property
    def recipientData(self) -> list[CT_Rel]:
        return self.findall(qn('w:recipientData'))  # type: ignore


class CT_MailMerge(OxmlBaseElement):
    @property
    def mainDocumentType(self) -> CT_MailMergeDocType:
        return getattr(self, qn('w:mainDocumentType'))

    @property
    def linkToQuery(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:linkToQuery'), None)

    @property
    def dataType(self) -> CT_MailMergeDataType:
        return getattr(self, qn('w:dataType'))

    @property
    def connectString(self) -> Optional[CT_String]:
        return getattr(self, qn('w:connectString'), None)

    @property
    def query(self) -> Optional[CT_String]:
        return getattr(self, qn('w:query'), None)

    @property
    def dataSource(self) -> Optional[CT_Rel]:
        return getattr(self, qn('w:dataSource'), None)

    @property
    def headerSource(self) -> Optional[CT_Rel]:
        return getattr(self, qn('w:headerSource'), None)

    @property
    def doNotSuppressBlankLines(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotSuppressBlankLines'), None)

    @property
    def destination(self) -> Optional[CT_MailMergeDest]:
        return getattr(self, qn('w:destination'), None)

    @property
    def addressFieldName(self) -> Optional[CT_String]:
        return getattr(self, qn('w:addressFieldName'), None)

    @property
    def mailSubject(self) -> Optional[CT_String]:
        return getattr(self, qn('w:mailSubject'), None)

    @property
    def mailAsAttachment(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:mailAsAttachment'), None)

    @property
    def viewMergedData(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:viewMergedData'), None)

    @property
    def activeRecord(self) -> Optional[CT_DecimalNumber]:
        return getattr(self, qn('w:activeRecord'), None)

    @property
    def checkErrors(self) -> Optional[CT_DecimalNumber]:
        return getattr(self, qn('w:checkErrors'), None)

    @property
    def odso(self) -> Optional[CT_Odso]:
        return getattr(self, qn('w:odso'), None)


class ST_TargetScreenSz(ST_BaseEnumType):
    screen_sz_544 = '544x376'
    screen_sz_640 = '640x480'
    screen_sz_720 = '720x512'
    screen_sz_800 = '800x600'
    screen_sz_1024 = '1024x768'
    screen_sz_1152 = '1152x882'
    screen_sz_1152900 = '1152x900'
    screen_sz_1280 = '1280x1024'
    screen_sz_1600 = '1600x1200'
    screen_sz_1800 = '1800x1440'
    screen_sz_1920 = '1920x1200'


class CT_TargetScreenSz(OxmlBaseElement):
    @property
    def val(self) -> ST_TargetScreenSz:
        return ST_TargetScreenSz(self.attrib[qn('w:val')])


class CT_Compat(OxmlBaseElement):
    @property
    def useSingleBorderforContiguousCells(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:useSingleBorderforContiguousCells'), None)

    @property
    def wpJustification(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:wpJustification'), None)

    @property
    def noTabHangInd(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:noTabHangInd'), None)

    @property
    def noLeading(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:noLeading'), None)

    @property
    def spaceForUL(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:spaceForUL'), None)

    @property
    def noColumnBalance(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:noColumnBalance'), None)

    @property
    def balanceSingleByteDoubleByteWidth(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:balanceSingleByteDoubleByteWidth'), None)

    @property
    def noExtraLineSpacing(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:noExtraLineSpacing'), None)

    @property
    def doNotLeaveBackslashAlone(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotLeaveBackslashAlone'), None)

    @property
    def ulTrailSpace(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:ulTrailSpace'), None)

    @property
    def doNotExpandShiftReturn(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotExpandShiftReturn'), None)

    @property
    def spacingInWholePoints(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:spacingInWholePoints'), None)

    @property
    def lineWrapLikeWord6(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:lineWrapLikeWord6'), None)

    @property
    def printBodyTextBeforeHeader(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:printBodyTextBeforeHeader'), None)

    @property
    def printColBlack(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:printColBlack'), None)

    @property
    def wpSpaceWidth(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:wpSpaceWidth'), None)

    @property
    def showBreaksInFrames(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:showBreaksInFrames'), None)

    @property
    def subFontBySize(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:subFontBySize'), None)

    @property
    def suppressBottomSpacing(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:suppressBottomSpacing'), None)

    @property
    def suppressTopSpacing(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:suppressTopSpacing'), None)

    @property
    def suppressSpacingAtTopOfPage(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:suppressSpacingAtTopOfPage'), None)

    @property
    def suppressTopSpacingWP(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:suppressTopSpacingWP'), None)

    @property
    def suppressSpBfAfterPgBrk(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:suppressSpBfAfterPgBrk'), None)

    @property
    def swapBordersFacingPages(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:swapBordersFacingPages'), None)

    @property
    def convMailMergeEsc(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:convMailMergeEsc'), None)

    @property
    def truncateFontHeightsLikeWP6(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:truncateFontHeightsLikeWP6'), None)

    @property
    def mwSmallCaps(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:mwSmallCaps'), None)

    @property
    def usePrinterMetrics(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:usePrinterMetrics'), None)

    @property
    def doNotSuppressParagraphBorders(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotSuppressParagraphBorders'), None)

    @property
    def wrapTrailSpaces(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:wrapTrailSpaces'), None)

    @property
    def footnoteLayoutLikeWW8(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:footnoteLayoutLikeWW8'), None)

    @property
    def shapeLayoutLikeWW8(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:shapeLayoutLikeWW8'), None)

    @property
    def alignTablesRowByRow(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:alignTablesRowByRow'), None)

    @property
    def forgetLastTabAlignment(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:forgetLastTabAlignment'), None)

    @property
    def adjustLineHeightInTable(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:adjustLineHeightInTable'), None)

    @property
    def autoSpaceLikeWord95(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:autoSpaceLikeWord95'), None)

    @property
    def noSpaceRaiseLower(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:noSpaceRaiseLower'), None)

    @property
    def doNotUseHTMLParagraphAutoSpacing(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotUseHTMLParagraphAutoSpacing'), None)

    @property
    def layoutRawTableWidth(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:layoutRawTableWidth'), None)

    @property
    def layoutTableRowsApart(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:layoutTableRowsApart'), None)

    @property
    def useWord97LineBreakRules(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:useWord97LineBreakRules'), None)

    @property
    def doNotBreakWrappedTables(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotBreakWrappedTables'), None)

    @property
    def doNotSnapToGridInCell(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotSnapToGridInCell'), None)

    @property
    def selectFldWithFirstOrLastChar(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:selectFldWithFirstOrLastChar'), None)

    @property
    def applyBreakingRules(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:applyBreakingRules'), None)

    @property
    def doNotWrapTextWithPunct(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotWrapTextWithPunct'), None)

    @property
    def doNotUseEastAsianBreakRules(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotUseEastAsianBreakRules'), None)

    @property
    def useWord2002TableStyleRules(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:useWord2002TableStyleRules'), None)

    @property
    def growAutofit(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:growAutofit'), None)

    @property
    def useFELayout(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:useFELayout'), None)

    @property
    def useNormalStyleForList(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:useNormalStyleForList'), None)

    @property
    def doNotUseIndentAsNumberingTabStop(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotUseIndentAsNumberingTabStop'), None)

    @property
    def useAltKinsokuLineBreakRules(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:useAltKinsokuLineBreakRules'), None)

    @property
    def allowSpaceOfSameStyleInTable(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:allowSpaceOfSameStyleInTable'), None)

    @property
    def doNotSuppressIndentation(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotSuppressIndentation'), None)

    @property
    def doNotAutofitConstrainedTables(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotAutofitConstrainedTables'), None)

    @property
    def autofitToFirstFixedWidthCell(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:autofitToFirstFixedWidthCell'), None)

    @property
    def underlineTabInNumList(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:underlineTabInNumList'), None)

    @property
    def displayHangulFixedWidth(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:displayHangulFixedWidth'), None)

    @property
    def splitPgBreakAndParaMark(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:splitPgBreakAndParaMark'), None)

    @property
    def doNotVertAlignCellWithSp(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotVertAlignCellWithSp'), None)

    @property
    def doNotBreakConstrainedForcedTable(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotBreakConstrainedForcedTable'), None)

    @property
    def doNotVertAlignInTxbx(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotVertAlignInTxbx'), None)

    @property
    def useAnsiKerningPairs(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:useAnsiKerningPairs'), None)

    @property
    def cachedColBalance(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:cachedColBalance'), None)

    @property
    def compatSetting(self) -> list[CT_CompatSetting]:
        return self.findall(qn('w:compatSetting'))  # type: ignore


class CT_CompatSetting(OxmlBaseElement):
    @property
    def name(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:name'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def uri(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:uri'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def val(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:val'))

        if _val is not None:
            return str(_val)
        return None


class CT_DocVar(OxmlBaseElement):
    @property
    def name(self) -> Optional[str]:
        return str(self.attrib[qn('w:name')])

    @property
    def val(self) -> Optional[str]:
        return str(self.attrib[qn('w:val')])


class CT_DocVars(OxmlBaseElement):
    @property
    def docVar(self) -> list[CT_DocVar]:
        return self.findall(qn('w:docVar'))  # type: ignore


class CT_DocRsids(OxmlBaseElement):
    @property
    def rsidRoot(self) -> Optional[CT_LongHexNumber]:
        return getattr(self, qn('w:rsidRoot'), None)

    @property
    def rsid(self) -> list[CT_LongHexNumber]:
        return self.findall(qn('w:rsid'))  # type: ignore


class ST_CharacterSpacing(ST_BaseEnumType):
    doNotCompress = 'doNotCompress'
    compressPunctuation = 'compressPunctuation'
    compressPunctuationAndJapaneseKana = 'compressPunctuationAndJapaneseKana'


class CT_CharacterSpacing(OxmlBaseElement):
    @property
    def val(self) -> Optional[ST_CharacterSpacing]:
        return ST_CharacterSpacing(self.attrib[qn('w:val')])


class CT_SaveThroughXslt(OxmlBaseElement):
    @property
    def r_id(self) -> Optional[str]:
        _val = self.attrib.get(qn('r:id'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def solutionID(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:solutionID'))

        if _val is not None:
            return str(_val)
        return None


class CT_RPrDefault(OxmlBaseElement):
    @property
    def rPr(self) -> Optional[CT_RPr]:
        return getattr(self, qn('w:rPr'), None)


class CT_PPrDefault(OxmlBaseElement):
    """17.7.5.3 pPrDefault (默认段落属性)

    该元素指定了当前文档的一组默认段落属性的存在。实际的段落属性存储在当前元素的pPr子元素中。

    如果省略了该元素，则当前文档的默认段落属性不存在（即文档中没有默认段落属性，因此默认值是应用程序定义的）。

    [示例：考虑以下 WordprocessingML 文档的文档默认值定义：

    <w:docDefaults>
        <w:pPrDefault>
            <w:pPr>
                <w:jc w:val="center"/>
            </w:pPr>
        </w:pPrDefault>
        …
    </w:docDefaults>

    pPrDefault 元素是该文档的默认段落属性集合的容器。示例结束]
    """

    @property
    def pPr(self) -> Optional[CT_PPrGeneral]:
        """17.7.5.2 pPr (段落属性)

        该元素指定了一组段落属性，这些属性包括当前WordprocessingML文档的默认段落属性。[理由：pPr元素存在于pPrDefault元素中的原因是为了方便在WordprocessingML文档中重新使用任何一组段落属性 - 因为段落属性始终是单个pPr元素的子元素，所以该元素可以完整地移动到所需的新位置，而无需进行其他修改。结束理由]

        如果省略此元素，则当前文档的默认段落属性不存在（即没有默认段落属性，因此默认值是应用程序定义的）。

        [示例：考虑以下WordprocessingML文档的文档默认值定义：


        <w:docDefaults>
            <w:pPrDefault>
                <w:pPr>
                    <w:jc w:val="center"/>
                </w:pPr>
            </w:pPrDefault>
            …
        </w:docDefaults>

        作为pPrDefault元素的子元素的pPr元素包含此文档的默认段落属性集 - 在此示例中，是居中对齐的值。结束示例]
        """
        return getattr(self, qn('w:pPr'), None)


class CT_DocDefaults(OxmlBaseElement):
    """17.7.5.1 docDefaults (文档默认的段落和运行属性)

    该元素指定了应用于当前WordprocessingML文档中每个段落和文本运行的默认段落和运行属性集。这些属性首先应用于样式层次结构中；因此，它们会被任何进一步冲突的格式覆盖，但如果没有进一步的格式存在，则会应用。

    如果省略了此元素，则文档默认值将由托管应用程序定义。

    [示例：考虑以下WordprocessingML文档的文档默认值定义：

    <w:docDefaults>
        <w:rPrDefault>
            <w:rPr>
                <w:b/>
            </w:rPr>
        </w:rPrDefault>
        <w:pPrDefault>
            <w:pPr>
                <w:jc w:val="center"/>
            </w:pPr>
        </w:pPrDefault>
    </w:docDefaults>

    docDefaults的子元素指定了居中文本的默认段落属性和粗体文本的默认运行属性。将此格式应用于同一文档的主文档部分中的以下片段：

    <w:body>
        <w:p>
            <w:r>
                <w:t>Hello, world</w:t>
            </w:r>
        </w:p>
    </w:body>

    此段落不包含任何格式属性，因此，使用样式层次结构，文档默认段落和运行属性将按照docDefaults元素中指定的方式应用，生成的段落将按照jc元素（§17.3.1.13）指定的方式居中，以及按照b元素（§17.3.2.1）指定的方式加粗。示例结束]
    """

    @property
    def rPrDefault(self) -> Optional[CT_RPrDefault]:
        return getattr(self, qn('w:rPrDefault'), None)

    @property
    def pPrDefault(self) -> Optional[CT_PPrDefault]:
        return getattr(self, qn('w:pPrDefault'), None)


class ST_WmlColorSchemeIndex(ST_BaseEnumType):
    dark1 = 'dark1'
    light1 = 'light1'
    dark2 = 'dark2'
    light2 = 'light2'
    accent1 = 'accent1'
    accent2 = 'accent2'
    accent3 = 'accent3'
    accent4 = 'accent4'
    accent5 = 'accent5'
    accent6 = 'accent6'
    hyperlink = 'hyperlink'
    followedHyperlink = 'followedHyperlink'


class CT_ColorSchemeMapping(OxmlBaseElement):
    @property
    def bg1(self) -> Optional[ST_WmlColorSchemeIndex]:
        _val = self.attrib.get(qn('w:bg1'))

        if _val is not None:
            return ST_WmlColorSchemeIndex(_val)
        return None

    @property
    def t1(self) -> Optional[ST_WmlColorSchemeIndex]:
        _val = self.attrib.get(qn('w:t1'))

        if _val is not None:
            return ST_WmlColorSchemeIndex(_val)
        return None

    @property
    def bg2(self) -> Optional[ST_WmlColorSchemeIndex]:
        _val = self.attrib.get(qn('w:bg2'))

        if _val is not None:
            return ST_WmlColorSchemeIndex(_val)
        return None

    @property
    def t2(self) -> Optional[ST_WmlColorSchemeIndex]:
        _val = self.attrib.get(qn('w:t2'))

        if _val is not None:
            return ST_WmlColorSchemeIndex(_val)
        return None

    @property
    def accent1(self) -> Optional[ST_WmlColorSchemeIndex]:
        _val = self.attrib.get(qn('w:accent1'))

        if _val is not None:
            return ST_WmlColorSchemeIndex(_val)
        return None

    @property
    def accent2(self) -> Optional[ST_WmlColorSchemeIndex]:
        _val = self.attrib.get(qn('w:accent2'))

        if _val is not None:
            return ST_WmlColorSchemeIndex(_val)
        return None

    @property
    def accent3(self) -> Optional[ST_WmlColorSchemeIndex]:
        _val = self.attrib.get(qn('w:accent3'))

        if _val is not None:
            return ST_WmlColorSchemeIndex(_val)
        return None

    @property
    def accent4(self) -> Optional[ST_WmlColorSchemeIndex]:
        _val = self.attrib.get(qn('w:accent4'))

        if _val is not None:
            return ST_WmlColorSchemeIndex(_val)
        return None

    @property
    def accent5(self) -> Optional[ST_WmlColorSchemeIndex]:
        _val = self.attrib.get(qn('w:accent5'))

        if _val is not None:
            return ST_WmlColorSchemeIndex(_val)
        return None

    @property
    def accent6(self) -> Optional[ST_WmlColorSchemeIndex]:
        _val = self.attrib.get(qn('w:accent6'))

        if _val is not None:
            return ST_WmlColorSchemeIndex(_val)
        return None

    @property
    def hyperlink(self) -> Optional[ST_WmlColorSchemeIndex]:
        _val = self.attrib.get(qn('w:hyperlink'))

        if _val is not None:
            return ST_WmlColorSchemeIndex(_val)
        return None

    @property
    def followedHyperlink(self) -> Optional[ST_WmlColorSchemeIndex]:
        _val = self.attrib.get(qn('w:followedHyperlink'))

        if _val is not None:
            return ST_WmlColorSchemeIndex(_val)
        return None


class CT_ReadingModeInkLockDown(OxmlBaseElement):
    @property
    def actualPg(self) -> s_ST_OnOff:
        return s_ST_OnOff(self.attrib[qn('w:actualPg')])

    @property
    def w(self) -> ST_PixelsMeasure:
        return ST_PixelsMeasure(self.attrib[qn('w:w')])

    @property
    def h(self) -> ST_PixelsMeasure:
        return ST_PixelsMeasure(self.attrib[qn('w:h')])

    @property
    def fontSz(self) -> ST_DecimalNumberOrPercent:
        return to_ST_DecimalNumberOrPercent(str(self.attrib[qn('w:fontSz')]))


class CT_WriteProtection(AG_Password, AG_TransitionalPassword):
    @property
    def recommended(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:recommended'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None


class CT_Settings(OxmlBaseElement):
    @property
    def writeProtection(self) -> Optional[CT_WriteProtection]:
        return getattr(self, qn('w:writeProtection'), None)

    @property
    def view(self) -> Optional[CT_View]:
        return getattr(self, qn('w:view'), None)

    @property
    def zoom(self) -> Optional[CT_Zoom]:
        return getattr(self, qn('w:zoom'), None)

    @property
    def removePersonalInformation(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:removePersonalInformation'), None)

    @property
    def removeDateAndTime(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:removeDateAndTime'), None)

    @property
    def doNotDisplayPageBoundaries(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotDisplayPageBoundaries'), None)

    @property
    def displayBackgroundShape(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:displayBackgroundShape'), None)

    @property
    def printPostScriptOverText(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:printPostScriptOverText'), None)

    @property
    def printFractionalCharacterWidth(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:printFractionalCharacterWidth'), None)

    @property
    def printFormsData(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:printFormsData'), None)

    @property
    def embedTrueTypeFonts(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:embedTrueTypeFonts'), None)

    @property
    def embedSystemFonts(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:embedSystemFonts'), None)

    @property
    def saveSubsetFonts(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:saveSubsetFonts'), None)

    @property
    def saveFormsData(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:saveFormsData'), None)

    @property
    def mirrorMargins(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:mirrorMargins'), None)

    @property
    def alignBordersAndEdges(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:alignBordersAndEdges'), None)

    @property
    def bordersDoNotSurroundHeader(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:bordersDoNotSurroundHeader'), None)

    @property
    def bordersDoNotSurroundFooter(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:bordersDoNotSurroundFooter'), None)

    @property
    def gutterAtTop(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:gutterAtTop'), None)

    @property
    def hideSpellingErrors(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:hideSpellingErrors'), None)

    @property
    def hideGrammaticalErrors(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:hideGrammaticalErrors'), None)

    @property
    def activeWritingStyle(self) -> list[CT_WritingStyle]:
        return self.findall(qn('w:activeWritingStyle'))  # type: ignore

    @property
    def proofState(self) -> Optional[CT_Proof]:
        return getattr(self, qn('w:proofState'), None)

    @property
    def formsDesign(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:formsDesign'), None)

    @property
    def attachedTemplate(self) -> Optional[CT_Rel]:
        return getattr(self, qn('w:attachedTemplate'), None)

    @property
    def linkStyles(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:linkStyles'), None)

    @property
    def stylePaneFormatFilter(self) -> Optional[CT_StylePaneFilter]:
        return getattr(self, qn('w:stylePaneFormatFilter'), None)

    @property
    def stylePaneSortMethod(self) -> Optional[CT_StyleSort]:
        return getattr(self, qn('w:stylePaneSortMethod'), None)

    @property
    def documentType(self) -> Optional[CT_DocType]:
        return getattr(self, qn('w:documentType'), None)

    @property
    def mailMerge(self) -> Optional[CT_MailMerge]:
        return getattr(self, qn('w:mailMerge'), None)

    @property
    def revisionView(self) -> Optional[CT_TrackChangesView]:
        return getattr(self, qn('w:revisionView'), None)

    @property
    def trackRevisions(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:trackRevisions'), None)

    @property
    def doNotTrackMoves(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotTrackMoves'), None)

    @property
    def doNotTrackFormatting(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotTrackFormatting'), None)

    @property
    def documentProtection(self) -> Optional[CT_DocProtect]:
        return getattr(self, qn('w:documentProtection'), None)

    @property
    def autoFormatOverride(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:autoFormatOverride'), None)

    @property
    def styleLockTheme(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:styleLockTheme'), None)

    @property
    def styleLockQFSet(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:styleLockQFSet'), None)

    @property
    def defaultTabStop(self) -> Optional[CT_TwipsMeasure]:
        return getattr(self, qn('w:defaultTabStop'), None)

    @property
    def autoHyphenation(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:autoHyphenation'), None)

    @property
    def consecutiveHyphenLimit(self) -> Optional[CT_DecimalNumber]:
        return getattr(self, qn('w:consecutiveHyphenLimit'), None)

    @property
    def hyphenationZone(self) -> Optional[CT_TwipsMeasure]:
        return getattr(self, qn('w:hyphenationZone'), None)

    @property
    def doNotHyphenateCaps(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotHyphenateCaps'), None)

    @property
    def showEnvelope(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:showEnvelope'), None)

    @property
    def summaryLength(self) -> Optional[CT_DecimalNumberOrPrecent]:
        return getattr(self, qn('w:summaryLength'), None)

    @property
    def clickAndTypeStyle(self) -> Optional[CT_String]:
        return getattr(self, qn('w:clickAndTypeStyle'), None)

    @property
    def defaultTableStyle(self) -> Optional[CT_String]:
        return getattr(self, qn('w:defaultTableStyle'), None)

    @property
    def evenAndOddHeaders(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:evenAndOddHeaders'), None)

    @property
    def bookFoldRevPrinting(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:bookFoldRevPrinting'), None)

    @property
    def bookFoldPrinting(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:bookFoldPrinting'), None)

    @property
    def bookFoldPrintingSheets(self) -> Optional[CT_DecimalNumber]:
        return getattr(self, qn('w:bookFoldPrintingSheets'), None)

    @property
    def drawingGridHorizontalSpacing(self) -> Optional[CT_TwipsMeasure]:
        return getattr(self, qn('w:drawingGridHorizontalSpacing'), None)

    @property
    def drawingGridVerticalSpacing(self) -> Optional[CT_TwipsMeasure]:
        return getattr(self, qn('w:drawingGridVerticalSpacing'), None)

    @property
    def displayHorizontalDrawingGridEvery(self) -> Optional[CT_DecimalNumber]:
        return getattr(self, qn('w:displayHorizontalDrawingGridEvery'), None)

    @property
    def displayVerticalDrawingGridEvery(self) -> Optional[CT_DecimalNumber]:
        return getattr(self, qn('w:displayVerticalDrawingGridEvery'), None)

    @property
    def doNotUseMarginsForDrawingGridOrigin(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotUseMarginsForDrawingGridOrigin'), None)

    @property
    def drawingGridHorizontalOrigin(self) -> Optional[CT_TwipsMeasure]:
        return getattr(self, qn('w:drawingGridHorizontalOrigin'), None)

    @property
    def drawingGridVerticalOrigin(self) -> Optional[CT_TwipsMeasure]:
        return getattr(self, qn('w:drawingGridVerticalOrigin'), None)

    @property
    def doNotShadeFormData(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotShadeFormData'), None)

    @property
    def noPunctuationKerning(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:noPunctuationKerning'), None)

    @property
    def characterSpacingControl(self) -> Optional[CT_CharacterSpacing]:
        return getattr(self, qn('w:characterSpacingControl'), None)

    @property
    def printTwoOnOne(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:printTwoOnOne'), None)

    @property
    def strictFirstAndLastChars(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:strictFirstAndLastChars'), None)

    @property
    def noLineBreaksAfter(self) -> Optional[CT_Kinsoku]:
        return getattr(self, qn('w:noLineBreaksAfter'), None)

    @property
    def noLineBreaksBefore(self) -> Optional[CT_Kinsoku]:
        return getattr(self, qn('w:noLineBreaksBefore'), None)

    @property
    def savePreviewPicture(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:savePreviewPicture'), None)

    @property
    def doNotValidateAgainstSchema(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotValidateAgainstSchema'), None)

    @property
    def saveInvalidXml(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:saveInvalidXml'), None)

    @property
    def ignoreMixedContent(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:ignoreMixedContent'), None)

    @property
    def alwaysShowPlaceholderText(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:alwaysShowPlaceholderText'), None)

    @property
    def doNotDemarcateInvalidXml(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotDemarcateInvalidXml'), None)

    @property
    def saveXmlDataOnly(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:saveXmlDataOnly'), None)

    @property
    def useXSLTWhenSaving(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:useXSLTWhenSaving'), None)

    @property
    def saveThroughXslt(self) -> Optional[CT_SaveThroughXslt]:
        return getattr(self, qn('w:saveThroughXslt'), None)

    @property
    def showXMLTags(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:showXMLTags'), None)

    @property
    def alwaysMergeEmptyNamespace(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:alwaysMergeEmptyNamespace'), None)

    @property
    def updateFields(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:updateFields'), None)

    @property
    def hdrShapeDefaults(self) -> Optional[CT_ShapeDefaults]:
        return getattr(self, qn('w:hdrShapeDefaults'), None)

    @property
    def footnotePr(self) -> Optional[CT_FtnDocProps]:
        return getattr(self, qn('w:footnotePr'), None)

    @property
    def endnotePr(self) -> Optional[CT_EdnDocProps]:
        return getattr(self, qn('w:endnotePr'), None)

    @property
    def compat(self) -> Optional[CT_Compat]:
        return getattr(self, qn('w:compat'), None)

    @property
    def docVars(self) -> Optional[CT_DocVars]:
        return getattr(self, qn('w:docVars'), None)

    @property
    def rsids(self) -> Optional[CT_DocRsids]:
        return getattr(self, qn('w:rsids'), None)

    @property
    def m(self) -> Optional[Any]:
        return getattr(self, qn('m:mathPr'), None)

    @property
    def attachedSchema(self) -> list[CT_String]:
        return self.findall(qn('w:attachedSchema'))  # type: ignore

    @property
    def themeFontLang(self) -> Optional[CT_Language]:
        return getattr(self, qn('w:themeFontLang'), None)

    @property
    def clrSchemeMapping(self) -> Optional[CT_ColorSchemeMapping]:
        return getattr(self, qn('w:clrSchemeMapping'), None)

    @property
    def doNotIncludeSubdocsInStats(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotIncludeSubdocsInStats'), None)

    @property
    def doNotAutoCompressPictures(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotAutoCompressPictures'), None)

    @property
    def forceUpgrade(self) -> Optional[CT_Empty]:
        return getattr(self, qn('w:forceUpgrade'), None)

    @property
    def captions(self) -> Optional[CT_Captions]:
        return getattr(self, qn('w:captions'), None)

    @property
    def readModeInkLockDown(self) -> Optional[CT_ReadingModeInkLockDown]:
        return getattr(self, qn('w:readModeInkLockDown'), None)

    @property
    def smartTagType(self) -> list[CT_SmartTagType]:
        return self.findall(qn('w:smartTagType'))  # type: ignore

    @property
    def sl(self) -> Optional[Any]:
        return getattr(self, qn('sl:schemaLibrary'), None)

    @property
    def shapeDefaults(self) -> Optional[CT_ShapeDefaults]:
        return getattr(self, qn('w:shapeDefaults'), None)

    @property
    def doNotEmbedSmartTags(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotEmbedSmartTags'), None)

    @property
    def decimalSymbol(self) -> Optional[CT_String]:
        return getattr(self, qn('w:decimalSymbol'), None)

    @property
    def listSeparator(self) -> Optional[CT_String]:
        return getattr(self, qn('w:listSeparator'), None)


class CT_StyleSort(OxmlBaseElement):
    @property
    def val(self) -> Optional[ST_StyleSort]:
        _val = self.attrib[qn('w:val')]

        return ST_StyleSort(_val)


class CT_StylePaneFilter(OxmlBaseElement):
    @property
    def allStyles(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:allStyles'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def customStyles(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:customStyles'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def latentStyles(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:latentStyles'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def stylesInUse(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:stylesInUse'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def headingStyles(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:headingStyles'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def numberingStyles(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:numberingStyles'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def tableStyles(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:tableStyles'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def directFormattingOnRuns(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:directFormattingOnRuns'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def directFormattingOnParagraphs(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:directFormattingOnParagraphs'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def directFormattingOnNumbering(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:directFormattingOnNumbering'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def directFormattingOnTables(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:directFormattingOnTables'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def clearFormatting(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:clearFormatting'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def top3HeadingStyles(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:top3HeadingStyles'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def visibleStyles(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:visibleStyles'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def alternateStyleNames(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:alternateStyleNames'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def val(self) -> Optional[ST_ShortHexNumber]:
        _val = self.attrib.get(qn('w:val'))

        if _val is not None:
            return ST_ShortHexNumber(_val)
        return None


class ST_StyleSort(ST_BaseEnumType):
    Name = 'name'
    priority = 'priority'
    default = 'default'
    font = 'font'
    basedOn = 'basedOn'
    type = 'type'
    zero = '0000'
    one = '0001'
    two = '0002'
    three = '0003'
    four = '0004'
    five = '0005'


class CT_WebSettings(OxmlBaseElement):
    @property
    def frameset(self) -> Optional[CT_Frameset]:
        return getattr(self, qn('w:frameset'), None)

    @property
    def divs(self) -> Optional[CT_Divs]:
        return getattr(self, qn('w:divs'), None)

    @property
    def encoding(self) -> Optional[CT_String]:
        return getattr(self, qn('w:encoding'), None)

    @property
    def optimizeForBrowser(self) -> Optional[CT_OptimizeForBrowser]:
        return getattr(self, qn('w:optimizeForBrowser'), None)

    @property
    def relyOnVML(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:relyOnVML'), None)

    @property
    def allowPNG(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:allowPNG'), None)

    @property
    def doNotRelyOnCSS(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotRelyOnCSS'), None)

    @property
    def doNotSaveAsSingleFile(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotSaveAsSingleFile'), None)

    @property
    def doNotOrganizeInFolder(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotOrganizeInFolder'), None)

    @property
    def doNotUseLongFileNames(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:doNotUseLongFileNames'), None)

    @property
    def pixelsPerInch(self) -> Optional[CT_DecimalNumber]:
        return getattr(self, qn('w:pixelsPerInch'), None)

    @property
    def targetScreenSz(self) -> Optional[CT_TargetScreenSz]:
        return getattr(self, qn('w:targetScreenSz'), None)

    @property
    def saveSmartTagsAsXml(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:saveSmartTagsAsXml'), None)


class ST_FrameScrollbar(ST_BaseEnumType):
    on = 'on'
    off = 'off'
    auto = 'auto'


class CT_FrameScrollbar(OxmlBaseElement):
    @property
    def val(self) -> ST_FrameScrollbar:
        _val = self.attrib[qn('w:val')]

        return ST_FrameScrollbar(_val)


class CT_OptimizeForBrowser(CT_OnOff):
    @property
    def target(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:target'))

        if _val is not None:
            return str(_val)
        return None


class CT_Frame(OxmlBaseElement):
    @property
    def sz(self) -> Optional[CT_String]:
        return getattr(self, qn('w:sz'), None)

    @property
    def name(self) -> Optional[CT_String]:
        return getattr(self, qn('w:name'), None)

    @property
    def title(self) -> Optional[CT_String]:
        return getattr(self, qn('w:title'), None)

    @property
    def longDesc(self) -> Optional[CT_Rel]:
        return getattr(self, qn('w:longDesc'), None)

    @property
    def sourceFileName(self) -> Optional[CT_Rel]:
        return getattr(self, qn('w:sourceFileName'), None)

    @property
    def marW(self) -> Optional[CT_PixelsMeasure]:
        return getattr(self, qn('w:marW'), None)

    @property
    def marH(self) -> Optional[CT_PixelsMeasure]:
        return getattr(self, qn('w:marH'), None)

    @property
    def scrollbar(self) -> Optional[CT_FrameScrollbar]:
        return getattr(self, qn('w:scrollbar'), None)

    @property
    def noResizeAllowed(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:noResizeAllowed'), None)

    @property
    def linkedToFile(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:linkedToFile'), None)


class ST_FrameLayout(ST_BaseEnumType):
    rows = 'rows'
    cols = 'cols'
    none = 'none'


class CT_FrameLayout(OxmlBaseElement):
    @property
    def val(self) -> ST_FrameLayout:
        _val = self.attrib[qn('w:val')]

        return ST_FrameLayout(_val)


class CT_FramesetSplitbar(OxmlBaseElement):
    @property
    def w(self) -> Optional[CT_TwipsMeasure]:
        return getattr(self, qn('w:w'), None)

    @property
    def color(self) -> Optional[CT_Color]:
        return getattr(self, qn('w:color'), None)

    @property
    def noBorder(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:noBorder'), None)

    @property
    def flatBorders(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:flatBorders'), None)


class CT_Frameset(OxmlBaseElement):
    @property
    def sz(self) -> Optional[CT_String]:
        return getattr(self, qn('w:sz'), None)

    @property
    def framesetSplitbar(self) -> Optional[CT_FramesetSplitbar]:
        return getattr(self, qn('w:framesetSplitbar'), None)

    @property
    def frameLayout(self) -> Optional[CT_FrameLayout]:
        return getattr(self, qn('w:frameLayout'), None)

    @property
    def title(self) -> Optional[CT_String]:
        return getattr(self, qn('w:title'), None)

    @property
    def frame(self) -> list[CT_Frame | CT_Frameset]:
        """

        <xsd:choice minOccurs="0" maxOccurs="unbounded">
            <xsd:element name="frameset" type="CT_Frameset" minOccurs="0" maxOccurs="unbounded"/>
            <xsd:element name="frame" type="CT_Frame" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:choice>
        """

        tags = (
            qn('w:frame'),  # CT_Frame
            qn('w:frameset'),  # CT_Frameset
        )
        return self.choice_one_list_child(*tags)  # type: ignore


class CT_NumPicBullet(OxmlBaseElement):
    """17.9.20 numPicBullet (图片编号符号定义)

    numPicBullet (Picture Numbering Symbol Definition)

    这个元素指定了文档中编号级别定义中要使用的特定图片的外观和行为，并且是 WordprocessingML 文档中所有图片编号符号信息的基础。

    这个元素不直接在抽象编号定义中使用，而是通过其 numPicBulletId 属性被编号级别定义中使用的 lvlPicBulletId 元素（§17.9.9）引用。
    """

    @property
    def pict(self) -> Optional[CT_Picture]:
        """项目列表图片"""

        return getattr(self, qn('w:pict'), None)

    @property
    def drawing(self) -> Optional[CT_Drawing]:
        """17.3.3.9 drawing (DrawingML对象)¶

        drawing (DrawingML Object)

        该元素指定在运行内容中的此位置有一个DrawingML对象。该DrawingML对象的布局属性使用WordprocessingML Drawing语法（§20.4）来指定。

        [示例：考虑一个运行内容为图片，该图片与段落中的文本在同一行（即，位于行中并影响行高）。该运行将使用以下WordprocessingML指定：

        <w:r>
            <w:drawing>
                <wp:inline>
                    …
                </wp:inline>
            </w:drawing>
        </w:r>

        drawing元素指示当前位置的运行中有一个DrawingML对象及其WordprocessingML Drawing定位数据（例如图片或图表）。示例结束]
        """
        return getattr(self, qn('w:drawing'), None)

    @property
    def numPicBulletId(self) -> ST_DecimalNumber:
        """numPicBulletId（图片编号符号 ID）

        指定此图片符号定义的唯一 ID，用于从编号级别定义中引用此图片符号。

        【示例：考虑下面的 WordprocessingML 片段，说明了如何通过 numPicBulletId 属性引用 numPicBullet 定义的图片编号符号定义：

            <w:numPicBullet w:numPicBulletId="1">
                …
            </w:numPicBullet>
            …
            <w:abstractNum w:abstractNumId="7">
                <w:lvl w:ilvl="0" w:tplc="B7663E56">
                    …
                    <w:lvlPicBulletId w:val="1" />
                </w:lvl>
            </w:abstractNum>

        lvlPicBulletId 元素直接引用了 numPicBulletId 属性中的 ID。示例结束】
        """
        _val = self.attrib[qn('w:numPicBulletId')]

        return ST_DecimalNumber(_val)


class ST_LevelSuffix(ST_BaseEnumType):
    """17.18.46 ST_LevelSuffix (编号符号和段落文本之间的内容)¶

    ST_LevelSuffix (Content Between Numbering Symbol and Paragraph Text)

    这个简单类型指定了在给定编号级别的文本和引用该编号级别的每个编号段落的文本之间可能存在的内容类型。
    """

    tab = 'tab'
    """tab（编号和文本之间有制表符）

    指定在显示编号段落时，在编号级别文本和段落内容之间显示一个制表符字符。

    这个制表符将遵循普通的制表位规则来确定其长度。
    """
    space = 'space'
    """space（编号和文本之间有空格）

    指定在显示编号段落时，在编号级别文本和段落内容之间显示一个空格字符。
    """

    nothing = 'nothing'
    """nothing（编号和文本之间无内容）

    指定在显示编号段落时，在编号级别文本和段落内容之间不显示任何字符。
    """


class CT_LevelSuffix(OxmlBaseElement):
    """17.9.28 suff (编号符号和段落文本之间的内容)¶

    suff (Content Between Numbering Symbol and Paragraph Text)

    这个元素指定了在给定编号级别的文本和引用该编号级别的每个编号段落的文本之间应添加的内容。

    如果省略此元素，则其值将被假定为制表符。
    """

    @property
    def val(self) -> ST_LevelSuffix:
        """val（编号和文本之间的字符类型）

        指定应跟在列表编号后面的字符。

        【示例：考虑一个编号段落，编号符号和编号段落的文本之间存在一个制表符。该制表符将在WordprocessingML中指定如下：

        <w:lvl w:ilvl="0">
            …
            <w:suff w:val="tab" />
            …
        </w:lvl>

        值为tab的val属性指定编号级别文本和段落文本之间的字符必须是一个制表符。此制表符遵循正常的制表位规则。示例结束】
        """
        _val = self.attrib[qn('w:val')]

        return ST_LevelSuffix(_val)


class CT_LevelText(OxmlBaseElement):
    """17.9.11 lvlText (编号级别文本)¶

    lvlText (Numbering Level Text)

    该元素指定了在显示具有给定编号级别的段落时应显示的文本内容。

    此元素的 val 属性中的所有文本都将被视为要在每个此编号级别的实例中重复的文字文本，除了任何使用百分号（%）后跟数字的情况，该百分号后的数字用于指示在此级别使用的基于一的编号的索引。任何比此级别高的级别的数字都将被忽略。

    当使用 % 语法时，数字将针对该级别的每个后续段落（无论是否连续）递增，直到在两个后续段落之间看到重新开始级别为止。
    """

    @property
    def val(self) -> Optional[str]:
        """val（级别文本）

        指定在文档内容中引用编号级别时要使用的实际文本。

        如果未指定此属性，则应将空字符串用作级别的文本。

        [示例：考虑以下 WordprocessingML：

        <w:lvl w:ilvl="1">
            …
            <w:lvlText w:val="test" />
            …
        </w:lvl>

        这里 val 属性指定了文字字符串 test 作为给定编号级别的文本，无论其位置如何。示例结束】

        此属性的可能值由 ST_String 简单类型定义（§22.9.2.13）。
        """
        _val = self.attrib.get(qn('w:val'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def null(self) -> Optional[s_ST_OnOff]:
        """null（级别文本为空字符）

        指定空字符应作为给定编号级别的编号符号。

        如果 val 属性包含任何内容，则应忽略此属性。

        如果省略此属性，则不应使用空字符串替代空字符串。【注意：空字符与空字符串不同。结束注意】

        [示例：考虑以下 WordprocessingML：

        <w:lvl w:ilvl="1">
            …
            <w:lvlText w:null="on" />
            …
        </w:lvl>

        此级别文本由单个空字符组成，而不是空字符串，因为设置了 null 属性。示例结束】
        """
        _val = self.attrib.get(qn('w:null'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None


class CT_LvlLegacy(OxmlBaseElement):
    @property
    def legacy(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:legacy'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def legacySpace(self) -> Optional[s_ST_TwipsMeasure]:
        _val = self.attrib.get(qn('w:legacySpace'))

        if _val is not None:
            return s_to_ST_TwipsMeasure(str(_val))
        return None

    @property
    def legacyIndent(self) -> Optional[ST_SignedTwipsMeasure]:
        _val = self.attrib.get(qn('w:legacyIndent'))

        if _val is not None:
            return to_ST_SignedTwipsMeasure(str(_val))
        return None


class CT_Lvl(OxmlBaseElement):
    """17.9.5 lvl (编号级别覆盖定义)¶

    lvl (Numbering Level Override Definition)

    此元素指定使用 lvlOverride 元素（§17.9.8）定义的特定编号级别在给定编号级别定义覆盖中的外观和行为。

    编号级别覆盖定义与编号级别定义相同，不同之处在于它是使用 num 元素（§17.9.15）作为编号定义实例的一部分定义的，而不是使用 abstractNum 元素（§17.9.1）作为抽象编号定义的一部分。

    <xsd:element name="lvl" type="CT_Lvl" minOccurs="0" maxOccurs="9"/>

    【示例：请考虑一个编号定义实例，它从 abstractNumId 为 4 的抽象编号定义继承信息，但应为编号定义的级别 0 使用一组不同的属性。生成的 WordprocessingML 如下所示：

        <w:num w:numId="6">
            <w:abstractNumId w:val="4" />
            <w:lvlOverride w:ilvl="0">
                <w:lvl w:ilvl="0">
                    <w:start w:val="4" />
                    <w:lvlText w:val="%1)" />
                    <w:lvlJc w:val="start" />
                    <w:pPr>
                        <w:ind w:start="360" w:hanging="360" />
                    </w:pPr>
                </w:lvl>
            </w:lvlOverride>
        </w:num>

    此编号定义实例用指定的编号级别覆盖定义覆盖了列表的级别 0，替换了抽象编号级别定义中的那些属性。示例结束】

    【注意：设置级别覆盖的能力优化了 WordprocessingML 中编号的使用，因为它避免了在编号集稍有不同的情况下写出冗余的抽象编号定义。

    请考虑使用 WordprocessingML 创建两个编号集，它们仅在第一级编号级别的外观和样式上有所不同。只要每个编号集引用不同的编号定义实例，其中一个编号定义实例利用第一级编号级别的级别覆盖，这两个编号集都可以使用相同的抽象编号定义。下面是展示这一点的 WordprocessingML：

        <w:num w:numId="5">
            <w:abstractNumId w:val="4" />
        </w:num>
        <w:num w:numId="6">
            <w:abstractNumId w:val="4" />
            <w:lvlOverride w:ilvl="0">
            <w:lvl w:ilvl="0">
                <w:start w:val="4" />
                <w:lvlText w:val="%1)" />
                <w:lvlJc w:val="start" />
                <w:pPr>
                    <w:ind w:start="360" w:hanging="360" />
                </w:pPr>
            </w:lvl>
            </w:lvlOverride>
        </w:num>

    注意结束】
    """

    @property
    def start(self) -> Optional[CT_DecimalNumber]:
        """17.9.25 start (起始值)¶

        start (Starting Value)

        该元素指定父编号级别在给定编号级别定义中使用的编号的起始值。当此级别在文档中首次启动时，以及每当通过 lvlRestart 元素（§17.9.10）中设置的属性重新启动时，将使用此值。

        如果省略此元素，则起始值应为零（0）。

        【示例：考虑以下用于抽象编号定义的 WordprocessingML 片段：

        <w:abstractNum w:abstractNumId="1">
            …
            <w:lvl w:ilvl="0">
                <w:start w:val="2" />
                <w:numFmt w:val="upperLetter"/>
                …
            </w:lvl>
        </w:abstractNum>

        在此示例中，由于使用大写西方字母（upperLetter）作为此编号级别的编号符号，因此与此抽象编号定义和编号级别关联的编号段落的第一个实例将具有编号符号 B，即数字格式中的第二个字母。

        具有此抽象编号定义且在此级别的后续编号段落将从 B（此编号级别的起始值）开始递增其编号符号。示例结束】
        """
        return getattr(self, qn('w:start'), None)

    @property
    def numFmt(self) -> Optional[CT_NumFmt]:
        """17.9.17 numFmt (编号格式)¶

        numFmt (Numbering Format)

        该元素指定了编号定义中此级别的所有编号应使用的编号格式。此信息用于替换级别文本字符串中的 %x，其中 x 是特定的基于一的级别索引，使用适当的值，除非 numFmt 值为 bullet，在这种情况下使用级别文本字符串的字面文本。此值应通过计算自上次使用 val 属性中定义的编号系统以来此级别的段落数来计算。

        当文档具有由 format 属性指定的自定义编号格式时，应使用引用的编号格式。如果无法将引用的编号格式解析为编号格式，则使用 val 属性值指定的编号格式。如果 val 属性的相应值为 custom，则结果由实现定义。

        如果省略此元素，则假定该级别为十进制级别。

        【示例：考虑编号定义中编号级别的以下 WordprocessingML 片段：

        <w:lvl w:ilvl="2">
            <w:start w:val="1" />
            <w:numFmt w:val="lowerRoman" />
            <w:lvlRestart w:val="0" />
            <w:lvlText w:val="%3)" />
            <w:lvlJc w:val="start" />
            <w:pPr>
                <w:ind w:start="1080" w:hanging="360" />
            </w:pPr>
            <w:rPr>
                <w:rFonts w:hint="default" />
            </w:rPr>
        </w:lvl>

        numFmt 值为 lowerLetter 表示消费者必须使用小写字母对此级别的所有编号进行编号：a、b、c…… 示例结束】
        """
        return getattr(self, qn('w:numFmt'), None)

    @property
    def lvlRestart(self) -> Optional[CT_DecimalNumber]:
        """17.9.10 lvlRestart (重新启动编号级别符号)¶

        lvlRestart (Restart Numbering Level Symbol)

        该元素指定了一个基于一的索引，用于确定何时重新开始编号级别到其起始值（§17.9.25）。当指定的编号级别的一个实例（它应该是高级别（比此级别早）或任何更早级别）在给定文档的内容中使用时，编号级别将重新开始。[示例：如果此值为2，则级别二和级别一都会重置此值。示例结束]

        如果省略了此元素，则编号级别将在每次使用前一个编号级别或任何更早级别时重新开始。如果指定的级别高于当前级别，则将忽略此元素。同样，值为0将指定此级别永远不会重新开始。
        """
        return getattr(self, qn('w:lvlRestart'), None)

    @property
    def pStyle(self) -> Optional[CT_String]:
        """17.9.23 pStyle (段落样式关联的编号级别)¶

        pStyle (Paragraph Style's Associated Numbering Level)

        这个元素指定了一个段落样式的名称，当应用到文档内容时，该样式将自动应用该编号级别。当定义一个段落样式以包含一个编号定义时，任何由 numPr 元素（§17.3.1.19）定义的编号级别都将被忽略，而代之以此元素指定的与该段落样式相关联的编号级别。

        如果这个元素引用了一个不存在或不是段落样式的样式，则可以忽略它。
        """
        return getattr(self, qn('w:pStyle'), None)

    @property
    def isLgl(self) -> Optional[CT_OnOff]:
        """17.9.4 isLgl (使用阿拉伯数字显示所有级别)¶

        isLgl (Display All Levels Using Arabic Numerals)

        此元素指定是否应将给定编号级别的所有显示级别的文本使用十进制数格式显示，而不论该级别在列表中的实际编号格式如何。【注意：这种编号样式通常称为法律编号样式。注意结束】

        如果存在此元素，那么在显示此级别的编号格式时，lvlTxt 元素（§17.9.11）中的所有编号级别都将转换为其十进制等价物。如果省略此元素，那么每个级别将使用该级别的 numFmt（§17.9.17）显示。
        """
        return getattr(self, qn('w:isLgl'), None)

    @property
    def suff(self) -> Optional[CT_LevelSuffix]:
        """17.9.28 suff (编号符号和段落文本之间的内容)¶

        suff (Content Between Numbering Symbol and Paragraph Text)

        这个元素指定了在给定编号级别的文本和引用该编号级别的每个编号段落的文本之间应添加的内容。

        如果省略此元素，则其值将被假定为制表符。
        """
        return getattr(self, qn('w:suff'), None)

    @property
    def lvlText(self) -> Optional[CT_LevelText]:
        """17.9.11 lvlText (编号级别文本)¶

        lvlText (Numbering Level Text)

        该元素指定了在显示具有给定编号级别的段落时应显示的文本内容。

        此元素的 val 属性中的所有文本都将被视为要在每个此编号级别的实例中重复的文字文本，除了任何使用百分号（%）后跟数字的情况，该百分号后的数字用于指示在此级别使用的基于一的编号的索引。任何比此级别高的级别的数字都将被忽略。

        当使用 % 语法时，数字将针对该级别的每个后续段落（无论是否连续）递增，直到在两个后续段落之间看到重新开始级别为止。

        [示例：考虑以下用于编号级别的 WordprocessingML：


        <w:lvl w:ilvl="1">
            …
            <w:lvlText w:val="字符串A %2 字符串B %1 字符串C %3"/>
            …
        </w:lvl>

        这指定了三个字符串（字符串A、字符串B、字符串C）必须与级别二（ilvl 为 1）的编号一起作为字符串文字使用，同时还要使用级别一和级别零的编号符号。尽管此处还引用了级别二，但由于它是高于当前编号级别的级别，因此将其忽略。
        """
        return getattr(self, qn('w:lvlText'), None)

    @property
    def lvlPicBulletId(self) -> Optional[CT_DecimalNumber]:
        """17.9.9 lvlPicBulletId (图片编号符号定义参考)¶

        lvlPicBulletId (Picture Numbering Symbol Definition Reference)

        这个元素指定了一个图片，该图片将被用作给定编号级别的编号符号，通过引用图片编号符号定义的 numPictBullet 元素（§17.9.20）来实现。通过此元素的 val 属性进行此引用。

        图片将被添加到编号级别中，通过用此图片的一个实例替换 lvlText 中的每个字符。

        [示例：考虑以下 WordprocessingML，说明了 lvlPicBulletId 通过其 val 属性引用图片编号符号定义的方式：

        <w:numPicBullet w:numPicBulletId="1">
            <w:drawing>
            …
            </w:drawing>
        </w:numPicBullet>
        …
        <w:abstractNum w:abstractNumId="7">
            <w:nsid w:val="71A06359" />
            <w:multiLevelType w:val="hybridMultilevel" />
            <w:tmpl w:val="10643FE6" />
            <w:lvl w:ilvl="0" w:tplc="B7663E56">
                <w:start w:val="1" />
                <w:numFmt w:val="bullet" />
                <w:lvlText w:val="AA" />
                <w:lvlPicBulletId w:val="1" />
            </w:lvl>
        </w:abstractNum>

        生成的编号必须由两个使用 numPicBullet 元素指定的图片实例组成。示例结束]
        """
        return getattr(self, qn('w:lvlPicBulletId'), None)

    @property
    def legacy(self) -> Optional[CT_LvlLegacy]:
        return getattr(self, qn('w:legacy'), None)

    @property
    def lvlJc(self) -> Optional[CT_Jc]:
        """17.9.7 lvlJc (文本对齐方式)¶

        lvlJc (Justification)

        该元素指定在给定编号级别中使用的文本的对齐方式。

        此对齐是相对于文档中父编号段落的文本边距应用的。

        如果省略，则段落将相对于文本边距左对齐（对于从左到右的段落），并相对于文本边距右对齐（对于从右到左的段落）。
        """
        return getattr(self, qn('w:lvlJc'), None)

    @property
    def pPr(self) -> Optional[CT_PPrGeneral]:
        """17.9.22 pPr (编号级别关联段落的属性)¶

        pPr (Numbering Level Associated Paragraph Properties)

        这个元素指定了在父编号定义中的特定编号级别中应用的段落属性。这些段落属性应用于引用给定编号定义和编号级别的任何带编号的段落。

        在带编号的段落本身上指定的段落属性会覆盖编号级别元素内的 pPr 元素指定的段落属性（§17.9.5，§17.9.6）。

        【示例：考虑以下 WordprocessingML，指定了编号级别段落属性：


        <w:abstractNum w:abstractNumId="1">
            …
            <w:lvl w:ilvl="0">
                …
                <w:pPr>
                    <w:tabs>
                        <w:tab w:val="num" w:pos="720" />
                    </w:tabs>
                    <w:ind w:start="720" w:hanging="360" />
                </w:pPr>
            </w:lvl>
        </w:abstractNum>

        pPr 元素内指定的每个段落属性都应用于继承此编号级别定义作为编号属性的任何带编号的段落，按照样式层次结构中定义的顺序应用。示例结束】
        """
        return getattr(self, qn('w:pPr'), None)

    @property
    def rPr(self) -> Optional[CT_RPr]:
        """17.9.24 rPr (编号符号的运行(Run)属性)¶

        rPr (Numbering Symbol Run Properties)

        该元素指定应用于文档中的段落的编号级别文本（由 lvlText 元素指定）的运行属性。

        这些运行属性应用于给定抽象编号定义和编号级别使用的所有编号级别文本。应该注意，指定在编号段落本身或编号段落中的文本运行上的运行属性与编号级别中的 rPr 元素指定的运行属性是分开的，因为后者仅影响编号文本本身，而不影响编号段落中的其他运行。

        【示例：考虑以下 WordprocessingML，其中使用 rPr 元素指定给定编号级别内使用的编号符号应为粗体，并且字号为 16：

        <w:lvl w:ilvl="1">
            …
            <w:rPr>
                <w:b />
                <w:sz w:val="32" />
            </w:rPr>
        </w:lvl>

        生成的段落使用其常规段落格式，但编号级别文本本身必须特别以粗体格式和 16 号字体显示。示例结束】

        该元素的内容模型（CT_RPr）的 W3C XML Schema 定义位于 §A.1。以上表中的每个子元素不得出现超过一次。【注：由于 W3C XML Schema 语言的限制，该限制未反映在元素的内容模型中。】
        """
        return getattr(self, qn('w:rPr'), None)

    @property
    def ilvl(self) -> ST_DecimalNumber:
        """ilvl（编号级别）

        指定由这组编号属性定义的编号级别定义。

        此覆盖是文档中列表级别数量的零起始索引。【示例：值为 2 表示文档中的第三个列表级别。示例结束】

        【示例：请考虑以下编号定义实例的 WordprocessingML：

        <w:num w:numId="6">
            <w:abstractNumId w:val="4" />
            <w:lvlOverride w:ilvl="0">
            …
            </w:lvlOverride>
        </w:num>

        在此示例中，被引用的抽象编号定义中的第一个编号级别定义（具有 ilvl 为 0）被覆盖。示例结束】

        此属性的可能值由 ST_DecimalNumber 简单类型定义（§17.18.10）。
        """
        _val = self.attrib[qn('w:ilvl')]

        return ST_DecimalNumber(_val)

    @property
    def tplc(self) -> Optional[ST_LongHexNumber]:
        """tplc（模板代码）

        指定一个唯一的十六进制值，可用于指定应在应用程序用户界面中显示此编号级别的位置。该值的解释方法由应用程序定义。

        如果省略了此属性，则此编号可以显示在消费者选择的任何位置。

        【示例：考虑以下抽象编号定义：

        <w:abstractNum w:abstractNumId="1" >
        …
        </w:abstractNum>

        在此示例中，具有 abstractNumId 属性值为 1 的 abstractNum 元素将显示在由模板代码 04090019 指定的消费者应用程序用户界面内的区域中。示例结束】

        此属性的可能值由 ST_LongHexNumber 简单类型定义（§17.18.50）。
        """
        _val = self.attrib.get(qn('w:tplc'))

        if _val is not None:
            return ST_LongHexNumber(str(_val))
        return None

    @property
    def tentative(self) -> Optional[s_ST_OnOff]:
        """tentative（临时编号）

        指定给定编号级别已由生产者保存，但未在父文档中使用。这意味着该编号级别可以由未来的消费者重新定义，而不会更改文档的实际内容。

        对于此属性值，值为 1 或 true 表示该编号级别未在当前文档内容中使用。

        对于此属性值，值为 0 或 false 表示该编号级别已在父文档中使用，且不能重新定义而不更改其内容。这是此属性的默认值，在省略此属性时隐含。

        【示例：考虑以下 WordprocessingML 编号级别：


        <w:lvl w:ilvl="0" w:tentative="true" >
        …
        </w:lvl>

        此级别的 tentative 属性设置为 true，因此此编号级别的内容尚未在文档中使用，可以由消费者根据需要重新定义。示例结束】

        如果此属性等于 1 或 true，则给定文档的 WordprocessingML 包含与此编号级别相关联的编号级别信息，但“tentative”编号级别将不会在任何与编号级别相关的宿主应用程序用户界面中表示。

        此属性的可能值由 ST_OnOff 简单类型定义（§22.9.2.7）。
        """
        _val = self.attrib.get(qn('w:tentative'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None


class ST_MultiLevelType(ST_BaseEnumType):
    """17.18.58 ST_MultiLevelType (编号定义类型)¶

    ST_MultiLevelType (Numbering Definition Type)

    这个简单类型指定了由给定抽象编号类型定义的可能编号的类型。此信息仅用于消费者确定此编号定义的用户界面行为，并且不应用于限制列表的行为（即，将多个级别标记为 singleLevel 的列表不应阻止使用第 2 至第 9 级）。
    """

    singleLevel = 'singleLevel'
    """（单级别编号定义）

    指定此编号定义定义了仅包含单个级别的编号格式。
    """

    multilevel = 'multilevel'
    """（多级编号定义）

    指定此编号定义定义了由多个级别组成的编号格式，每个级别都是相同类型的（项目符号 vs. 级别文本）。
    """

    hybridMultilevel = 'hybridMultilevel'
    """（混合多级编号定义）

    指定此编号定义定义了由多个级别组成的编号格式，每个级别可能是不同类型的（项目符号 vs. 级别文本）。
    """


class CT_MultiLevelType(OxmlBaseElement):
    """17.9.12 multiLevelType (抽象编号定义类型)¶

    multiLevelType (Abstract Numbering Definition Type)

    这个元素指定了由给定抽象编号类型定义的编号类型。此信息仅用于由消费者确定此编号定义的用户界面行为，并不用于限制列表的行为（即，将多个级别标记为单级别的列表不会阻止使用第2至第9级别）。

    如果省略此元素，则假定列表为消费者所需的任何编号类型。
    """

    @property
    def val(self) -> ST_MultiLevelType:
        """val（抽象编号定义类型）

        指定由给定抽象编号定义启用的特定编号类型。

        [示例：考虑以下 WordprocessingML：

        <w:abstractNum w:abstractNumId="8">
            …
            <w:multiLevelType w:val="multilevel" />
            …
        </w:abstractNum>

        此抽象编号定义被指定为多级编号类型，消费者可以使用该类型将此编号正确放置在用户界面中。示例结束]

        此属性的可能值由 ST_MultiLevelType 简单类型定义（[§17.18.58]）。
        """
        _val = self.attrib[qn('w:val')]

        return ST_MultiLevelType(_val)


class CT_AbstractNum(OxmlBaseElement):
    """17.9.1 abstractNum (摘要编号定义)¶

    abstractNum (Abstract Numbering Definition)

    此元素指定了一组属性，这些属性将决定 WordprocessingML 文档中一组编号段落的外观和行为。这些属性统称为抽象编号定义，是所有编号信息在 WordprocessingML 文档中的基础。

    虽然抽象编号定义包含了一整套编号信息，但它不会被内容直接引用（因此称为抽象）。相反，这些属性将通过编号定义实例使用 num 元素 (§17.9.15) 继承，然后该实例本身可以被内容引用。
    """

    @property
    def nsid(self) -> Optional[CT_LongHexNumber]:
        """17.9.14 nsid (抽象编号定义标识符)¶

        nsid (Abstract Numbering Definition Identifier)

        这个元素将一个唯一的十六进制 ID 关联到父抽象编号定义。对于两个基于相同初始编号定义的抽象编号定义，这个编号应该是相同的 - 如果一个文档被重新制作并且底层编号定义被更改，它应该保持其原始的 nsid。

        如果省略此元素，则列表将没有 nsid，生产者可以任意添加一个。

        【注：此元素可用于确定要应用于从一个文档复制并粘贴到另一个文档的带编号段落的抽象编号定义。考虑一个这样的情况：一个与 nsid 为 FFFFFF23 的抽象编号定义相关联的给定带编号段落，被粘贴到了与完全不同外观和 nsid 为 FFFFFF23 的抽象编号定义相关联的带编号段落之间。在这种情况下，由于相同的 nsid 值所启用的区别，主机应用程序不必随意保留被粘贴的带编号段落与其原始抽象编号定义相关联，因为它可以使用抽象编号定义的相同 nsid 值提供的信息来知道这两个编号集是相同的，并将段落合并到目标编号格式中。结束注】

        【示例：考虑以下抽象编号定义的 WordprocessingML：

        <w:abstractNum w:abstractNumId="3">
            <w:nsid w:val="FFFFFF89" />
            <w:multiLevelType w:val="singleLevel" />
            <w:tmpl w:val="D9842532" />
            …
        </w:abstractNum>

        在这个例子中，给定的抽象编号定义与唯一的十六进制 ID FFFFFF89 相关联。示例结束】
        """
        return getattr(self, qn('w:nsid'), None)

    @property
    def multiLevelType(self) -> Optional[CT_MultiLevelType]:
        """17.9.12 multiLevelType (抽象编号定义类型)¶

        multiLevelType (Abstract Numbering Definition Type)

        这个元素指定了由给定抽象编号类型定义的编号类型。此信息仅用于由消费者确定此编号定义的用户界面行为，并不用于限制列表的行为（即，将多个级别标记为单级别的列表不会阻止使用第2至第9级别）。

        如果省略此元素，则假定列表为消费者所需的任何编号类型。

        [示例：考虑以下 WordprocessingML：

        <w:abstractNum w:abstractNumId="8">
            …
            <w:multiLevelType w:val="singleLevel" />
            …
        </w:abstractNum>

        通过 multiLevelType 元素，此抽象编号定义被指定为 singleLevel 编号类型。示例结束]
        """
        return getattr(self, qn('w:multiLevelType'), None)

    @property
    def tmpl(self) -> Optional[CT_LongHexNumber]:
        """17.9.29 tmpl (编号模板代码)¶

        tmpl (Numbering Template Code)

        这个元素指定了一个唯一的十六进制代码，用于确定此抽象编号定义应该显示在应用程序用户界面中的位置。

        如果省略此元素，则此抽象编号定义可以显示在消费者选择的任何位置。

        【示例：考虑以下抽象编号定义：

        <w:abstractNum w:abstractNumId="1">
            …
            <w:tmpl w:val="CA48B6BA" />
            …
        </w:abstractNum>

        在这个示例中，具有属性abstractNumId等于1的abstractNum元素将显示在消费者应用程序用户界面中的模板代码CA48B6BA指定的区域内。示例结束】
        """
        return getattr(self, qn('w:tmpl'), None)

    @property
    def name(self) -> Optional[CT_String]:
        """17.9.13 name (摘要编号定义名称)¶

        name (Abstract Numbering Definition Name)

        这个元素指定了给定抽象编号定义的名称。该名称可用于提供给定编号定义的用户友好别名，但不应影响列表的行为 - 具有不同 name 元素的两个相同定义应该表现相同。

        如果省略此元素，则此抽象编号定义将没有名称。

        [示例：考虑以下 WordprocessingML：

        <w:abstractNum w:abstractNumId="4">
            <w:nsid w:val="5C294B5B" />
            <w:multiLevelType w:val="multilevel" />
            <w:tmpl w:val="6F8A81B0" />
            <w:name w:val="Example Name" />
            …
        </w:abstractNum>

        在此示例中，通过 name 元素，给定的抽象编号定义被命名为 Example Name。示例结束]
        """
        return getattr(self, qn('w:name'), None)

    @property
    def styleLink(self) -> Optional[CT_String]:
        """17.9.27 styleLink (编号样式定义)¶

        styleLink (Numbering Style Definition)

        这个元素指定了父抽象编号定义是指定编号样式的基本编号定义，其在其 val 属性中引用。

        如果省略此元素，或者它引用不存在的样式，则此编号定义将不是编号样式的基本属性。

        【注：编号样式从不直接由文档中的段落或文本运行引用 - 相反，抽象编号定义指定它包含编号样式的基本编号信息，并且一个或多个编号定义实例引用从中继承的编号定义。编号样式本身只是抽象编号定义上的友好名称。 结束注释】

        【示例：考虑下面的 WordprocessingML 片段，表示一个抽象编号定义，它定义了编号样式的属性：

        <w:numbering>
            …
            <w:abstractNum w:abstractNumId="5">
                …
                <w:styleLink w:val="ExampleNumberingStyle" />
                …
            </w:abstractNum>
        </w:numbering>
        …
        <w:styles>
            …
            <w:style w:type="numbering" w:styleId="ExampleNumberingStyle">
                <w:name w:val="ExampleNumberingStyle" />
                …
                <w:pPr>
                    <w:numPr>
                        <w:numId w:val="6" />
                    </w:numPr>
                </w:pPr>
            </w:style>
            …
        </w:styles>

        styleLink 元素指定抽象编号定义定义了样式 ID 与其 val 属性匹配的编号样式的属性，并在 WordprocessingML 的 styles 元素中定义。】

        end example]
        """
        return getattr(self, qn('w:styleLink'), None)

    @property
    def numStyleLink(self) -> Optional[CT_String]:
        """17.9.21 numStyleLink (编号样式参考)¶

        numStyleLink (Numbering Style Reference)

        这个元素指定一个抽象编号，不包含其编号类型的实际编号属性，而是作为对存储在文档中的编号样式的引用，当引用此抽象编号定义时应用该编号样式，并且它本身指向要使用的实际底层抽象编号定义。

        当引用此抽象编号定义时要应用的编号样式由 numStyleLink 的 val 属性中包含的字符串标识。

        【示例：考虑以下抽象编号定义：

        <w:abstractNum w:abstractNumId="0">
            <w:nsid w:val="38901FA4" />
            <w:multiLevelType w:val="multilevel" />
            <w:numStyleLink w:val="TestNumberingStyle" />
        </w:abstractNum>

        这个抽象编号定义引用了具有 styleId 属性等于 TestNumberingStyle 的编号样式，如下所示：

        <w:style w:type="numbering" w:styleId="TestNumberingStyle">
            …
        </w:style>

        因此，每当基本抽象编号定义被编号段继承时，必须应用此编号样式。示例结束】
        """
        return getattr(self, qn('w:numStyleLink'), None)

    @property
    def lvl(self) -> list[CT_Lvl]:
        """17.9.5 lvl (编号级别覆盖定义)¶

        lvl (Numbering Level Override Definition)

        此元素指定使用 lvlOverride 元素（§17.9.8）定义的特定编号级别在给定编号级别定义覆盖中的外观和行为。

        编号级别覆盖定义与编号级别定义相同，不同之处在于它是使用 num 元素（§17.9.15）作为编号定义实例的一部分定义的，而不是使用 abstractNum 元素（§17.9.1）作为抽象编号定义的一部分。

        <xsd:element name="lvl" type="CT_Lvl" minOccurs="0" maxOccurs="9"/>

        【示例：请考虑一个编号定义实例，它从 abstractNumId 为 4 的抽象编号定义继承信息，但应为编号定义的级别 0 使用一组不同的属性。生成的 WordprocessingML 如下所示：

            <w:num w:numId="6">
                <w:abstractNumId w:val="4" />
                <w:lvlOverride w:ilvl="0">
                    <w:lvl w:ilvl="0">
                        <w:start w:val="4" />
                        <w:lvlText w:val="%1)" />
                        <w:lvlJc w:val="start" />
                        <w:pPr>
                            <w:ind w:start="360" w:hanging="360" />
                        </w:pPr>
                    </w:lvl>
                </w:lvlOverride>
            </w:num>

        此编号定义实例用指定的编号级别覆盖定义覆盖了列表的级别 0，替换了抽象编号级别定义中的那些属性。示例结束】

        【注意：设置级别覆盖的能力优化了 WordprocessingML 中编号的使用，因为它避免了在编号集稍有不同的情况下写出冗余的抽象编号定义。

        请考虑使用 WordprocessingML 创建两个编号集，它们仅在第一级编号级别的外观和样式上有所不同。只要每个编号集引用不同的编号定义实例，其中一个编号定义实例利用第一级编号级别的级别覆盖，这两个编号集都可以使用相同的抽象编号定义。下面是展示这一点的 WordprocessingML：

            <w:num w:numId="5">
                <w:abstractNumId w:val="4" />
            </w:num>
            <w:num w:numId="6">
                <w:abstractNumId w:val="4" />
                <w:lvlOverride w:ilvl="0">
                <w:lvl w:ilvl="0">
                    <w:start w:val="4" />
                    <w:lvlText w:val="%1)" />
                    <w:lvlJc w:val="start" />
                    <w:pPr>
                        <w:ind w:start="360" w:hanging="360" />
                    </w:pPr>
                </w:lvl>
                </w:lvlOverride>
            </w:num>

        注意结束】
        """
        return self.findall(qn('w:lvl'))  # type: ignore

    @property
    def abstractNumId(self) -> ST_DecimalNumber:
        """abstractNumId（抽象编号定义ID）

        指定一个唯一的编号，作为此抽象编号定义的标识符。任何编号定义实例要继承此抽象编号定义指定的属性，必须引用此唯一编号。

        【示例：请考虑一个 abstractNumId 属性为 4 的抽象编号定义的 WordprocessingML 代码：

            <w:abstractNum w:abstractNumId="4">
                <w:nsid w:val="FFFFFF7F" />
                <w:multiLevelType w:val="singleLevel" />
                <w:lvl w:ilvl="0">
                    <w:start w:val="1" />
                    <w:lvlText w:val="%1." />
                    <w:lvlJc w:val="start" />
                    <w:pPr>
                        <w:tabs>
                            <w:tab w:val="num" w:pos="720" />
                        </w:tabs>
                        <w:ind w:left="720"/>
                    </w:pPr>
                </w:lvl>
            </w:abstractNum>

        abstractNumId 属性作为抽象编号定义的唯一标识符，使具有匹配属性值的 abstractNumId 元素的编号定义实例 (§17.9.15) 能够继承抽象编号定义的属性，例如：

            <w:numbering>
                …
                <w:num w:numId="2">
                    <w:abstractNumId w:val="0" />
                </w:num>
                <w:num w:numId="3">
                    <w:abstractNumId w:val="1" />
                </w:num>
                <w:num w:numId="4">
                    <w:abstractNumId w:val="4" />
                </w:num>
                <w:num w:numId="5">
                    <w:abstractNumId w:val="4" />
                </w:num>
            </w:numbering>

        在这种情况下，最后两个编号定义实例都继承自 abstractNumId 为 4 的抽象编号定义。示例结束】

        此属性的可能值由 ST_DecimalNumber 简单类型定义（§17.18.10）。
        """
        _val = self.attrib[qn('w:abstractNumId')]

        return ST_DecimalNumber(_val)


class CT_NumLvl(OxmlBaseElement):
    """17.9.8 lvlOverride (编号级别定义覆盖)¶

    lvlOverride (Numbering Level Definition Override)

    该元素指定一个可选的覆盖，应用于给定编号定义实例的抽象编号定义中的零个或多个级别。每个此元素的实例用于覆盖给定抽象编号定义中的特定编号级别定义的外观和行为。

    【注意：设置级别覆盖的能力可优化 WordprocessingML 中编号的使用，因为它可以防止在编号集仅略有不同的情况下写出冗余的抽象编号定义。

    考虑使用 WordprocessingML 创建两个编号集，它们在第一个编号级别的外观和样式上略有不同。只要每个引用不同的编号定义实例，并且其中一个编号定义实例利用级别覆盖来设置第一个编号级别，两者可以使用相同的抽象编号定义。以下是说明此示例的 WordprocessingML：

    <w:num w:numId="5">
        <w:abstractNumId w:val="4" />
    </w:num>
    <w:num w:numId="6">
        <w:abstractNumId w:val="4" />
        <w:lvlOverride w:ilvl="0">
        <w:lvl w:ilvl="0">
            <w:start w:val="4" />
            <w:lvlText w:val="%1)" />
            <w:lvlJc w:val="start" />
            <w:pPr>
                <w:ind w:start="360" w:hanging="360" />
            </w:pPr>
        </w:lvl>
        </w:lvlOverride>
    </w:num>

    注意结束】
    """

    @property
    def startOverride(self) -> Optional[CT_DecimalNumber]:
        """17.9.26 startOverride (编号级别起始值覆盖)¶

        startOverride (Numbering Level Starting Value Override)

        这个元素指定了指定级别覆盖的编号从哪里开始。这个值用于在给定级别重置编号。
        """
        return getattr(self, qn('w:startOverride'), None)

    @property
    def lvl(self) -> Optional[CT_Lvl]:
        """17.9.6 lvl (编号级别定义)¶

        lvl (Numbering Level Definition)

        该元素指定了在给定抽象编号定义中编号级别的外观和行为。编号级别包含一组属性，用于在抽象编号定义中为给定的编号级别显示编号。

        编号级别定义与编号级别覆盖定义相同，不同之处在于它是作为编号定义实例的一部分使用 abstractNum 元素（§17.9.1）而不是作为抽象编号定义的一部分使用 num 元素（§17.9.15）来定义的。

        【示例：考虑以下 WordprocessingML 示例：

        <w:abstractNum w:abstractNumId="4">
            <w:nsid w:val="1DE04504" />
            <w:multiLevelType w:val="hybridMultilevel" />
            <w:lvl w:ilvl="0" w:tplc="0409000F">
                …
            </w:lvl>
            <w:lvl w:ilvl="1" w:tplc="04090019">
                …
            </w:lvl>
            <w:lvl w:ilvl="2" w:tplc="04090019">
                …
            </w:lvl>
            <w:lvl w:ilvl="3" w:tplc="0409000F">
                …
            </w:lvl>
            …
        </w:abstractNum>

        该示例表明，任何使用具有属性 val 设置为 0、1、2 或 3 的 ilvl 元素的编号属性的段落，其外观和行为与上述给定的 lvl 元素指定的其前四个编号级别相对应（假设未指定级别覆盖）。示例结束】
        """
        return getattr(self, qn('w:lvl'), None)

    @property
    def ilvl(self) -> ST_DecimalNumber:
        """ilvl（编号级别 ID）

        指定要覆盖的给定抽象编号定义的编号级别。

        如果此数字与子级别（lvl 元素）的 ilvl 冲突，则后者将被忽略。

        [示例：考虑一个编号定义实例，该实例从抽象编号定义（abstractNumId 为 4）继承其信息，但希望对编号定义的级别 0 使用不同的属性。生成的 WordprocessingML 如下所示：

        <w:num w:numId="6">
            <w:abstractNumId w:val="4" />
            <w:lvlOverride w:ilvl="0">
                <w:lvl w:ilvl="0">
                    <w:start w:val="4" />
                    <w:lvlText w:val="%1)" />
                    <w:lvlJc w:val="start" />
                    <w:pPr>
                        <w:ind w:left="360" />
                    </w:pPr>
                </w:lvl>
            </w:lvlOverride>
        </w:num>

        此级别使用指定的编号属性覆盖了抽象编号定义的级别 0 属性，替换了抽象编号定义中的属性。示例结束]
        """
        _val = self.attrib[qn('w:ilvl')]

        return ST_DecimalNumber(_val)


class CT_Num(OxmlBaseElement):
    """17.9.15 num (编号定义实例)¶

    num (Numbering Definition Instance)

    这个元素指定了一个唯一的编号信息实例，可以被父 WordprocessingML 文档中的零个或多个段落引用。

    此实例需要通过 abstractNumId 子元素（§17.9.2）引用基本抽象编号定义。此元素还可以用于指定应用于从此实例继承的抽象编号定义中的零个或多个级别的一组可选覆盖，通过可选的 lvlOverride 子元素（§17.9.8）。

    【示例：考虑一个包含四个编号定义实例的文档的 WordprocessingML，其中有两个引用相同的底层抽象编号定义：

    <w:numbering>
        …
        <w:num w:numId="2">
            <w:abstractNumId w:val="0" />
        </w:num>
        <w:num w:numId="3">
            <w:abstractNumId w:val="1" />
        </w:num>
        <w:num w:numId="4">
            <w:abstractNumId w:val="4" />
        </w:num>
        <w:num w:numId="5">
            <w:abstractNumId w:val="4" />
        </w:num>
    </w:numbering>

    如上所示，前两个编号定义实例分别引用了 abstractNumId 值为 0 和 1 的抽象编号定义，而最后两个都引用了抽象编号定义的 abstractNumId 为 4。示例结束】

    【示例：考虑一个编号定义实例，它从抽象编号定义的 abstractNumId 为 4 的编号信息中继承了其信息，但希望对编号定义的级别 0 使用不同的属性集。生成的 WordprocessingML 如下所示：

    <w:num w:numId="6">
        <w:abstractNumId w:val="4" />
        <w:lvlOverride w:ilvl="0">
            <w:lvl w:ilvl="0">
                <w:start w:val="4" />
                <w:lvlText w:val="%1)" />
                <w:lvlJc w:val="start" />
                <w:pPr>
                    <w:ind w:start="360" w:hanging="360" />
                </w:pPr>
            </w:lvl>
        </w:lvlOverride>
    </w:num>

    lvlOverride 元素指定了抽象编号定义级别 0 的覆盖。示例结束】
    """

    @property
    def abstractNumId(self) -> CT_DecimalNumber:
        """17.9.2 abstractNumId (摘要编号定义参考)

        abstractNumId (Abstract Numbering Definition Reference)

        此元素指定抽象编号定义信息，其属性将由父编号定义实例继承。

        【示例：请考虑一个包含两个编号定义实例的文档的 WordprocessingML，其中每个实例引用不同的抽象编号定义：

        <w:numbering>
            <w:abstractNum w:abstractNumId="0">
                …
            </w:abstractNum>
            <w:abstractNum w:abstractNumId="1">
                …
            </w:abstractNum>
            …
            <w:num w:numId="1">
                <w:abstractNumId w:val="0" />
            </w:num>
            <w:num w:numId="2">
                <w:abstractNumId w:val="1" />
            </w:num>
            …
        </w:numbering>

        这两个编号定义实例通过其 abstractNumId 元素分别引用 abstractNumId 属性值为 0 和 1 的抽象编号定义。示例结束】
        """
        return getattr(self, qn('w:abstractNumId'))

    @property
    def lvlOverride(self) -> list[CT_NumLvl]:
        """17.9.8 lvlOverride (编号级别定义覆盖)¶

        lvlOverride (Numbering Level Definition Override)

        该元素指定一个可选的覆盖，应用于给定编号定义实例的抽象编号定义中的零个或多个级别。每个此元素的实例用于覆盖给定抽象编号定义中的特定编号级别定义的外观和行为。

        【注意：设置级别覆盖的能力可优化 WordprocessingML 中编号的使用，因为它可以防止在编号集仅略有不同的情况下写出冗余的抽象编号定义。

        考虑使用 WordprocessingML 创建两个编号集，它们在第一个编号级别的外观和样式上略有不同。只要每个引用不同的编号定义实例，并且其中一个编号定义实例利用级别覆盖来设置第一个编号级别，两者可以使用相同的抽象编号定义。以下是说明此示例的 WordprocessingML：

        <w:num w:numId="5">
            <w:abstractNumId w:val="4" />
        </w:num>
        <w:num w:numId="6">
            <w:abstractNumId w:val="4" />
            <w:lvlOverride w:ilvl="0">
            <w:lvl w:ilvl="0">
                <w:start w:val="4" />
                <w:lvlText w:val="%1)" />
                <w:lvlJc w:val="start" />
                <w:pPr>
                    <w:ind w:start="360" w:hanging="360" />
                </w:pPr>
            </w:lvl>
            </w:lvlOverride>
        </w:num>

        注意结束】

        <xsd:element name="lvlOverride" type="CT_NumLvl" minOccurs="0" maxOccurs="9"/>
        """
        return self.findall(qn('w:lvlOverride'))  # type: ignore

    @property
    def numId(self) -> ST_DecimalNumber:
        """numId（编号定义实例 ID）

        指定一个唯一的ID，任何希望继承这些编号属性的编号段落都应使用 numPr 元素（§17.3.1.19）进行引用。

        【示例：考虑以下用于示例编号段落的 WordprocessingML：

        <w:p>
            <w:pPr>
                <w:numPr>
                <w:ilvl w:val="0" />
                <w:numId w:val="5" />
                </w:numPr>
            </w:pPr>
            …
        </w:p>

        此段落引用了一个 numId 属性为 5 的编号定义实例：

        <w:num w:numId="5">
            <w:abstractNumId w:val="4" />
        </w:num>

        numId 属性为 5 的编号定义实例与具有 val 为 5 的编号段落相关联，因此编号段落继承其属性。示例结束】
        """
        _val = self.attrib[qn('w:numId')]

        return ST_DecimalNumber(_val)


class CT_Numbering(OxmlBaseElement):
    """17.9.16 numbering (编号定义)

    numbering (Numbering Definitions)

    此元素指定了在 WordprocessingML 文档中用于标记单独文本段落的编号格式、显示和功能，包括阿拉伯数字、罗马数字、符号字符（"项目符号"）和文本字符串等。

    【示例：以下两个段落都包含由 WordprocessingML 定义的编号：第一个使用阿拉伯数字，第二个使用符号字符：

    这是一个具有编号信息的段落。

        这也是一个具有编号信息的段落。

    示例结束】

    [Note: The W3C XML Schema definition of this element’s content model (CT_Numbering) is located in §A.1. end note]
    """

    @property
    def numPicBullet(self) -> list[CT_NumPicBullet]:
        """17.9.20 numPicBullet (图片编号符号定义)

        numPicBullet (Picture Numbering Symbol Definition)

        这个元素指定了文档中编号级别定义中要使用的特定图片的外观和行为，并且是 WordprocessingML 文档中所有图片编号符号信息的基础。

        这个元素不直接在抽象编号定义中使用，而是通过其 numPicBulletId 属性被编号级别定义中使用的 lvlPicBulletId 元素（§17.9.9）引用。
        """
        return self.findall(qn('w:numPicBullet'))  # type: ignore

    @property
    def abstractNum(self) -> list[CT_AbstractNum]:
        """17.9.1 abstractNum (摘要编号定义)¶

        abstractNum (Abstract Numbering Definition)

        此元素指定了一组属性，这些属性将决定 WordprocessingML 文档中一组编号段落的外观和行为。这些属性统称为抽象编号定义，是所有编号信息在 WordprocessingML 文档中的基础。

        虽然抽象编号定义包含了一整套编号信息，但它不会被内容直接引用（因此称为抽象）。相反，这些属性将通过编号定义实例使用 num 元素 (§17.9.15) 继承，然后该实例本身可以被内容引用。
        """
        return self.findall(qn('w:abstractNum'))  # type: ignore

    @property
    def num(self) -> list[CT_Num]:
        """17.9.15 num (编号定义实例)¶

        num (Numbering Definition Instance)

        这个元素指定了一个唯一的编号信息实例，可以被父 WordprocessingML 文档中的零个或多个段落引用。

        此实例需要通过 abstractNumId 子元素（§17.9.2）引用基本抽象编号定义。此元素还可以用于指定应用于从此实例继承的抽象编号定义中的零个或多个级别的一组可选覆盖，通过可选的 lvlOverride 子元素（§17.9.8）。
        """
        return self.findall(qn('w:num'))  # type: ignore

    @property
    def numIdMacAtCleanup(self) -> Optional[CT_DecimalNumber]:
        """17.9.19 numIdMacAtCleanup (最后审查的摘要编号定义)¶

        numIdMacAtCleanup (Last Reviewed Abstract Numbering Definition)

        这个元素向消费者指示应用程序在尝试从给定文档中删除未使用的抽象编号定义时的进度。如果消费者打开了一个旧版本的文档，它可以选择删除那些“孤立”的抽象编号定义（没有关联的编号定义实例）。这个元素被那些消费者用来指示他们在审查现有的抽象编号定义时的进度（如果尚未完成的话）。【注意：从文档中删除未使用的抽象编号定义可以减小文件大小，但不是必需的。】

        如果省略，则所有抽象编号定义都应被视为已审阅。

        【示例：考虑一个包含 32 个抽象编号定义的文档，其中 abstractNumId 的值范围从 0 到 85。如果应用程序只在保存时审阅了 abstractNumId 值低于 25 的那些抽象编号定义，它将指示为如下状态：

            <w:numIdMacAtCleanup w:val="25"/>

        此值指定所有 abstractNumId 值大于 25 的抽象编号定义尚未被审阅。示例结束】
        """
        return getattr(self, qn('w:numIdMacAtCleanup'), None)


class ST_TblStyleOverrideType(ST_BaseEnumType):
    """17.18.89 ST_TblStyleOverrideType (条件表样式格式设置类型)

    ST_TblStyleOverrideType (Conditional Table Style Formatting Types)
    这种简单类型指定了在使用此表样式时，当前条件格式属性应用于表各部分的可能取值。

    [示例：考虑一个包含条件格式的表样式，定义如下：

    <w:style w:type="table" …>
        …
        <w:tblStylePr w:type="lastRow">
            …
        </w:tblStylePr>
    </w:style>

    lastRow的type属性值指定此组条件格式属性仅应用于表的最后一行。示例结束]

    这种简单类型的内容是对W3C XML Schema字符串数据类型的限制。
    """

    wholeTable = 'wholeTable'
    """wholeTable (整个表格式)

    指定条件格式适用于整个表。
    """

    firstRow = 'firstRow'
    """firstRow (第一行条件格式)

    指定表格式适用于第一行。

    有tblHeader元素存在（§17.4.49），任何后续行也应使用该条件格式。
    """

    lastRow = 'lastRow'
    """lastRow (最后一行表格式)

    指定表格式适用于最后一行。
    """

    firstCol = 'firstCol'
    """firstCol (第一列条件格式)

    指定表格式适用于第一列。
    """

    lastCol = 'lastCol'
    """lastCol (最后一列表格式)

    指定表格式适用于最后一列。
    """

    band1Vert = 'band1Vert'
    """band1Vert (交错列条件格式)

    指定表格式适用于列的奇数编号分组。
    """

    band2Vert = 'band2Vert'
    """band2Vert (偶数列条纹条件格式)

    指定表格式适用于列的偶数编号分组。
    """

    band1Horz = 'band1Horz'
    """band1Horz (交错行条件格式)

    指定表格式适用于行的奇数编号分组。
    """

    band2Horz = 'band2Horz'
    """band2Horz (偶数行条纹条件格式)

    指定表格式适用于行的偶数编号分组。
    """

    neCell = 'neCell'
    """neCell (右上角表格单元格格式)

    指定表格式适用于右上角单元格。
    """

    nwCell = 'nwCell'
    """nwCell (左上角表格单元格格式)

    指定表格式适用于左上角单元格。
    """

    seCell = 'seCell'
    """seCell (右下角表格单元格格式)

    指定表格式适用于右下角单元格。
    """

    swCell = 'swCell'
    """swCell (左下角表格单元格格式)

    指定表格式适用于左下角单元格。
    """


class CT_TblStylePr(OxmlBaseElement):
    """17.7.6.6 tblStylePr (样式条件表格式化属性)

    该元素指定了一组格式属性，这些属性应根据在type属性上指定的要求匹配的表部分进行有条件地应用。这些表条件格式应用于表的不同区域，如下所示：

    表中的所有行也可以根据交替行/列的基础进行条件格式设置，如下所示：

    当指定时，这些条件格式应按以下顺序应用（因此后续格式将覆盖先前格式的属性）：

    - 整个表
    - 带状列，偶数列带状
    - 带状行，偶数行带状
    - 第一行，最后一行
    - 第一列，最后一列
    - 左上，右上，左下，右下

    [示例：考虑一个包含条件格式设置的表样式，定义如下：


    <w:style w:type="table" w:styleId="exampleTableStyle">
        …
        <w:tblStylePr w:type="firstRow">
            <w:tblPr>
                <w:tblCellSpacing w:w="29" w:type="dxa"/>
            </w:tblPr>
            …
        </w:tblStylePr>
    </w:style>

    tblStylePr元素指定了一组表属性，这些属性必须有条件地应用于符合type属性指定的标准的表的所有部分（在本例中，当前表的所有标题行）。
    """

    @property
    def pPr(self) -> Optional[CT_PPrGeneral]:
        """17.7.8.2 pPr (样式段落属性)

        该元素指定应用于段落的段落属性集。

        【示例：考虑一个定义如下的段落样式：

        <w:style w:type="paragraph" w:styleId="TestParaStyle">
            <w:pPr>
                <w:keepLines/>
            </w:pPr>
        </w:style>

        在样式元素内指定的pPr元素指定了必须应用于引用段落的段落属性集。在此示例中，应用的单个段落属性是段落必须通过keepLines元素（§17.3.1.14）显示为单页。结束示例】
        """
        return getattr(self, qn('w:pPr'), None)

    @property
    def rPr(self) -> Optional[CT_RPr]:
        """17.7.9.1 rPr (Run 属性)

        该元素指定应用于文本运行的运行属性集。

        【示例：考虑一个定义如下的字符样式：

        <w:style w:type="character" w:styleId="TestCharStyle">
            <w:rPr>
                <w:dstrike/>
            </w:rPr>
        </w:style>

        在样式元素内指定的rPr元素指定了必须应用于引用运行的运行属性集。在此示例中，应用的单个运行属性是段落必须通过dstrike元素（§17.3.2.9）显示为双删除线。结束示例】

        该元素的内容模型（CT_RPr）的W3C XML Schema定义位于§A.1中。上表中的每个子元素不得出现多次。【注意：由于W3C XML Schema语言的限制，该限制未反映在元素的内容模型中。】
        """
        return getattr(self, qn('w:rPr'), None)

    @property
    def tblPr(self) -> Optional[CT_TblPrBase]:
        """17.7.6.3 tblPr (表格样式条件格式表格属性)

        该元素指定了应用于表格中所有符合父tblStylePr元素上指定的条件格式类型的区域的表格属性集。这些属性按照样式层次结构中指定的顺序应用。

        如果当前的条件格式类型不包含一个或多个完整的表格行，则无法应用于单个单元格或列的表格属性[示例：表格对齐。结束示例]可以被忽略。

        例如：考虑一个包含其firstRow条件格式的表格样式，定义如下：

        <w:style w:type="table" w:styleId="exampleTableStyle">
            …
            <w:tblStylePr w:type="firstRow">
                <w:tblPr>
                    <w:tblCellSpacing w:w="29" w:type="dxa"/>
                </w:tblPr>
                …
            </w:tblStylePr>
        </w:style>

        在tblStylePr元素中指定的tblPr元素指定了必须应用于符合firstRow类型值指定的标准的表格的所有部分的表格属性 - 表格的所有标题行。在这个示例中，应用的单个表格属性是通过tblCellSpacing元素（§17.4.45）设置的默认表格单元间距值为0.02英寸。结束示例。
        """

        return getattr(self, qn('w:tblPr'), None)

    @property
    def trPr(self) -> Optional[CT_TrPr]:
        """17.7.6.10 trPr (表格样式条件格式表格行属性)

        该元素指定了应用于表格中所有符合父tblStylePr元素上指定的条件格式类型的所有行的表格行属性集。这些属性按照样式层次结构中指定的顺序应用。

        [示例：考虑一个包含其firstRow条件格式的表格样式，定义如下：

        <w:style w:type="table" w:styleId="exampleTableStyle">
            …
            <w:tblStylePr w:type="firstRow">
                <w:trPr>
                    <w:tblHeader/>
                    <w:cantSplit/>
                </w:trPr>
                …
            </w:tblStylePr>
        </w:style>

        在tblStylePr元素中指定的trPr元素指定了必须应用于表格的所有行的表格行属性集，这些行符合firstRow的type值指定的条件 - 表格的所有标题行。在此示例中，应用的表格行属性是这些行必须通过tblHeader元素（§17.4.49）在每个页面上重复显示，以及这些行不能使用cantSplit元素（§17.4.6）跨页面分割。示例结束]
        """
        return getattr(self, qn('w:trPr'), None)

    @property
    def tcPr(self) -> Optional[CT_TcPr]:
        """17.7.6.8 tcPr (表格样式条件格式表格单元格属性)

        该元素指定了应用于表格中所有与父tblStylePr元素上指定的条件格式类型匹配的区域的表格单元属性集。这些属性按照样式层次结构中指定的顺序应用。

        [示例：考虑一个包含其firstRow条件格式的表格样式，定义如下：

        <w:style w:type="table" w:styleId="exampleTableStyle">
            …
            <w:tblStylePr w:type="firstRow">
                <w:tcPr>
                    <w:tcBorders>
                    <w:top w:val="nil" />
                    <w:start w:val="nil" />
                    <w:bottom w:val="nil" />
                    <w:end w:val="nil" />
                    <w:insideH w:val="nil" />
                    <w:insideV w:val="nil" />
                    </w:tcBorders>
                </w:tcPr>
                …
            </w:tblStylePr>
        </w:style>

        在tblStylePr元素中指定的tcPr元素指定了必须应用于表格的所有部分的表格单元属性集，这些部分符合firstRow的type值指定的条件 - 表格的所有标题行。在此示例中，应用的单个表格单元属性是通过tcBorders元素（§17.4.66）应用的一组表格单元边框。在这种情况下，这些单元边框仅将任何先前的单元边框重置为nil。

        示例结束]
        """
        return getattr(self, qn('w:tcPr'), None)

    @property
    def type(self) -> ST_TblStyleOverrideType:
        """ "type（表格样式条件格式类型）

        指定应用当前条件格式属性的表格部分。

        [示例：考虑一个包含条件格式的表格样式，定义如下：

        <w:style w:type="table" …>
            …
            <w:tblStylePr w:type="lastRow">
                …
            </w:tbl StylePr>
        </w:style>

        lastRow 的 type 属性值指定这组条件格式属性仅应用于表格的最后一行。结束示例]
        """
        _val = self.attrib[qn('w:type')]

        return ST_TblStyleOverrideType(_val)


class ST_StyleType(ST_BaseEnumType):
    """17.18.83 ST_StyleType (样式类型)

    这种简单类型指定了在ordprocessingML文档中定义的样式定义类型的可能值。WordprocessingML支持六种样式定义类型：

    - 段落样式
    - 字符样式
    - 表格样式
    - 编号样式
    - 关联样式（段落+字符）
    - 默认段落+字符属性

    前四种样式类型中的每一种对应于下面的不同值，因此定义了当前样式的样式类型。[注意：最后两种样式类型是独特的，因为它们不仅仅是样式类型：关联样式是通过链接元素（[§17.7.4.6]）将字符和段落样式配对而成的；文档默认属性是通过docDefaults元素（[§17.7.5.1]）定义的。结束注释]

    [示例：考虑以下样式定义：

    <w:style w:type="paragraph" … >
        <w:name w:val="My Paragraph Style"/>
        <w:rPr>
            <w:b/>
        </w:rPr>
    </w:style>

        类型属性是简单类型ST_StyleType，其值为paragraph指定了这个样式定义创建了一个段落样式。结束示例]

    这种简单类型的内容是对W3C XML Schema字符串数据类型的限制。

    这种简单类型限制为以下表格中列出的值：

    - character（字符样式）

        指定父样式定义为字符样式。

    - numbering（编号样式）

        指定父样式定义为编号样式。

    - paragraph（段落样式）

        指定父样式定义为段落样式。

    - table（表格样式）

        指定父样式定义为表格样式。
    """

    paragraph = 'paragraph'
    """指定父样式定义为段落样式。"""

    character = 'character'
    """指定父样式定义为字符样式。"""

    table = 'table'
    """指定父样式定义为表格样式。"""

    numbering = 'numbering'
    """指定父样式定义为编号样式。"""


class CT_Style(OxmlBaseElement):
    """17.7.4.17 style (样式定义)

    这个元素指定了WordprocessingML文档中单个样式的定义。样式是一组预定义的表格、编号、段落和/或字符属性，可以应用于文档中的区域。

    任何样式定义的样式定义可以分为三个部分：

    - 通用样式属性(General style properties)
    - 样式类型(Style type)
    - 样式类型特定属性(Style type-specific properties)

    通用样式属性是指可以在不考虑样式类型的情况下使用的属性集；例如，样式名称，样式的其他别名，样式ID（文档内容用来引用样式的），样式是否隐藏，样式是否锁定等。

    [示例：考虑文档中名为“标题1”的样式如下所示：

    <w:style w:type="paragraph" w:styleId="Heading1">
        <w:name w:val="Heading 1"/>
        <w:basedOn w:val="Normal"/>
        <w:next w:val="Normal"/>
        <w:link w:val="Heading1Char"/>
        <w:uiPriority w:val="1"/>
        <w:qFormat/>
        <w:rsid w:val="00F303CE"/>
        …
    </w:style>

    上面针对此样式类型的格式信息之上是一组通用样式属性，定义了所有样式类型共享的信息。结束示例]

    样式类型是指样式上的属性，用于定义使用此样式定义创建的样式的类型。WordprocessingML通过样式定义的类型属性的值支持六种样式定义类型：

    - 段落样式(Paragraph styles)
    - 字符样式(Character styles)
    - 链接样式（段落+字符）(Linked styles (paragraph + character))【注：通过 link 元素（§17.7.4.6）实现。结束注释】
    - 表格样式(Table styles)
    - 编号样式(Numbering styles)
    - 默认段落+字符属性(Default paragraph + character properties)

    [示例：考虑文档中名为 Heading 1 的样式如下所示：

    <w:style w:type="paragraph" w:styleId="Heading1">
        <w:name w:val="Heading 1"/>
        <w:basedOn w:val="Normal"/>
        <w:next w:val="Normal"/>
        <w:link w:val="Heading1Char"/>
        <w:uiPriority w:val="1"/>
        <w:qFormat/>
        <w:rsid w:val="00F303CE"/>
        …
    </w:style>

    type 属性的值为 paragraph，表示以下样式定义是一个段落样式。示例结束]

    样式类型特定属性指的是样式的有效载荷：其格式信息以及仅适用于该样式类型的任何属性。

    [示例：考虑一个名为普通表的主要名称为 Normal Table 的表样式定义如下：

    <w:style w:type="table" w:default="1" w:styleId="TableNormal">
        <w:name w:val="Normal Table"/>
        …
        <w:tblPr>
            <w:tblInd w:w="0" w:type="dxa"/>
            <w:tblCellMar>
                <w:top w:w="0" w:type="dxa"/>
                <w:start w:w="108" w:type="dxa"/>
                <w:bottom w:w="0" w:type="dxa"/>
                <w:end w:w="108" w:type="dxa"/>
            </w:tblCellMar>
        </w:tblPr>
    </w:style>

    tblPr 元素包含此表样式的格式有效载荷，仅适用于表样式。示例结束]

    xsd定义:

    <xsd:complexType name="CT_Style">
        <xsd:sequence>
            <xsd:element name="name" type="CT_String" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="aliases" type="CT_String" minOccurs="0"/>
            <xsd:element name="basedOn" type="CT_String" minOccurs="0"/>
            <xsd:element name="next" type="CT_String" minOccurs="0"/>
            <xsd:element name="link" type="CT_String" minOccurs="0"/>
            <xsd:element name="autoRedefine" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="hidden" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="uiPriority" type="CT_DecimalNumber" minOccurs="0"/>
            <xsd:element name="semiHidden" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="unhideWhenUsed" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="qFormat" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="locked" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="personal" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="personalCompose" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="personalReply" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="rsid" type="CT_LongHexNumber" minOccurs="0"/>
            <xsd:element name="pPr" type="CT_PPrGeneral" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="rPr" type="CT_RPr" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="tblPr" type="CT_TblPrBase" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="trPr" type="CT_TrPr" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="tcPr" type="CT_TcPr" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="tblStylePr" type="CT_TblStylePr" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
        <xsd:attribute name="type" type="ST_StyleType" use="optional"/>
        <xsd:attribute name="styleId" type="s:ST_String" use="optional"/>
        <xsd:attribute name="default" type="s:ST_OnOff" use="optional"/>
        <xsd:attribute name="customStyle" type="s:ST_OnOff" use="optional"/>
    </xsd:complexType>
    """

    @property
    def name(self) -> Optional[CT_String]:
        """17.7.4.9 name (主要样式名称)

        该元素指定了文档中当前样式的主要名称。此名称可根据需要在应用程序的用户界面中使用。该样式的实际主要名称存储在其val属性中。

        如果存在，备用样式名称（§17.7.4.1）应在用户界面中替代内置名称，当在stylePaneFormatFilter元素（§17.15.1.85）中设置适当值时。

        如果省略此元素，则该样式将没有主要样式名称。

        [示例：考虑一个具有主要名称和两个备用名称的样式，使用name和aliases元素定义如下：

        <w:style w:styleId="TestStyle" … >
            <w:name w:val="GD20Complex"/>
            <w:aliases w:val="Regional Growth,Complex Growth"/>
            …
        </w:style>

        此样式使用name元素指定其具有主要名称GD20Complex。示例结束]
        """
        return getattr(self, qn('w:name'), None)

    @property
    def aliases(self) -> Optional[CT_String]:
        """17.7.4.1 aliases (替代样式名称)

        这个元素指定了父样式定义的一组备用名称。这些名称可以根据需要在应用程序的用户界面中使用。备用名称应存储在该元素的val属性中，每个名称之间应以一个或多个连续逗号字符（Unicode字符值002C）分隔。所有存在的逗号都应解释为分隔符字符，绝不作为备用样式名称的一部分。

        如果存在备用样式名称，则当在stylePaneFormatFilter元素中设置了适当的值时，将在用户界面中使用这些备用样式名称替代name元素（§17.7.4.9）中指定的内置名称。

        如果省略了该元素，则该样式将不具有任何备用样式名称。

        【示例：考虑具有主要名称和两个备用名称的样式，使用name和aliases元素定义如下：

        <w:style w:styleId="TestStyle" … >
            <w:name w:val="GD20Complex"/>
            <w:aliases w:val="Regional Growth,Complex Growth"/>
            …
        </w:style>

        该样式使用name元素（§17.7.4.9）指定了主要名称GD20Complex，以及使用aliases元素指定了两个备用名称Regional Growth和Complex Growth。结束示例】
        """
        return getattr(self, qn('w:aliases'), None)

    @property
    def basedOn(self) -> Optional[CT_String]:
        """17.7.4.3 basedOn (父样式 ID)

        该元素指定了父样式的样式ID，该样式从中继承样式继承。样式继承是指一组样式相互继承，以生成单个样式的属性集。该元素的val属性指定了样式继承中父样式的styleId属性。

        如果省略了该元素，则该样式不应基于当前文档中的任何其他样式（即，该元素是样式的样式继承的根）。如果当前文档中没有任何样式指定val属性中存在的styleId，则应忽略该元素（即，该元素是样式的样式继承的根）。

        如果存在具有此styleId的样式，则应遵循以下限制：

        - 如果当前样式是表样式，则父样式也必须是表样式，否则应忽略该元素。
        - 如果当前样式是段落样式，则父样式也必须是段落样式，否则应忽略该元素。
        - 如果当前样式是字符样式，则父样式也必须是字符样式，否则应忽略该元素。
        - 如果当前样式是编号样式，则应忽略该元素。

        [示例：考虑以下定义的三个WordprocessingML字符样式：

        - 具有styleId值为Strong的字符样式，其属性包括粗体属性
        - 具有styleId值为Underline的字符样式，其属性包括下划线属性
        - 具有styleId值为Emphasis的字符样式，其属性包括斜体属性

        每个字符样式定义了单个字符格式属性。如果每个元素的basedOn值定义如下：

        <w:style w:styleId="Strong">
            <w:basedOn w:val="Underline"/>
            …
            <w:rPr>
                <w:b/>
            </w:rPr>
        </w:style>
        <w:style w:styleId="Underline">
            <w:basedOn w:val="Emphasis"/>
            …
            <w:rPr>
                <w:u/>
            </w:rPr>
        </w:style>
        <w:style w:styleId="Emphasis">
            …
            <w:rPr>
                <w:i/>
            </w:rPr>
        </w:style>

        强调样式基于下划线样式，而下划线样式则基于强调样式。这意味着强调样式的实际定义如下：

        - 粗体(Bold)
        - 下划线(Underline)（继承自下划线）
        - 斜体(Italics)（继承自强调）

        强调样式的样式链定义如下：

        - 强调(Emphasis)
        - 下划线(Underline)
        - 强调(Strong)

        类似地，下划线样式的样式链定义如下：

        - 强调(Emphasis)
        - 下划线(Underline)

        在每种情况下，样式链是所有样式的列表，这些样式按顺序组合以生成任何给定样式的全部属性集。示例结束】

        """
        return getattr(self, qn('w:basedOn'), None)

    @property
    def next(self) -> Optional[CT_String]:
        """17.7.4.10 next (下一段落的样式)

        该元素指定了在应用了父段落样式的段落后创建的新段落上自动应用的样式。[注：当当前样式的使用仅限于一个段落时，通常不希望将此样式应用于后续段落 - 例如，标题样式可能会指定其后续段落必须返回到常规文本格式。结束注释]

        如果在除段落样式之外的任何样式类型的样式上指定了该元素，则将忽略此元素。如果不存在样式的styleId与此元素的val属性匹配，或该样式不是段落样式，则将忽略此元素。

        如果省略了该元素，则下一个段落将使用与当前段落相同的段落样式。

        [示例：考虑在WordprocessingML文档中定义如下样式：

        <w:style w:styleId="TestParagraphStyle" … >
            <w:name w:val="测试段落样式"/>
            <w:next w:val="AnotherParagraphStyle"/>
            <w:rPr>
                <w:b/>
            </w:rPr>
            …
        </w:style>

        该样式通过使用next元素指定，文档中下一个段落的样式必须是其styleId属性值为AnotherParagraphStyle的段落样式（如果存在这样的段落样式）。结束示例]
        """
        return getattr(self, qn('w:next'), None)

    @property
    def link(self) -> Optional[CT_String]:
        """17.7.4.6 link (链接的样式引用)

        该元素指定了构成链接样式的样式配对。链接样式是段落样式和字符样式的分组，在用户界面中用于允许应用相同的格式属性集：

        - 到一个或多个整个段落的内容（即作为段落样式）
        - 到一个或多个段落内的运行内容（即作为字符样式）

        每种样式在文件格式中仍然独立存在，因为在样式元素（§17.7.4.18）中同时存在段落样式和字符样式，但这两种样式将合并为一种，并根据它们是否应用于运行或段落来适当应用，通过引用通过该元素的val属性引用的配对链接样式的styleId属性。

        没有子链接元素的样式元素不是链接样式配对的一部分。如果当前文档中没有样式指定val属性中存在的styleId，则将忽略该元素。

        如果存在具有此styleId的样式，则应符合以下限制：

        - 如果父样式是表格样式，则将忽略该元素。
        - 如果父样式是段落样式，则该元素的val属性必须引用字符样式，否则将忽略该元素。
        - 如果父样式是字符样式，则该元素的val属性必须引用段落样式，否则将忽略该元素。
        - 如果父样式是编号样式，则将忽略该元素。

        [示例：考虑在WordprocessingML文档中定义如下的链接样式：

        <w:style w:type="paragraph" w:styleId="TestParagraphStyle">
            <w:link w:val="TestCharacterStyle"/>
            …
            </w:style>
        <w:style w:type="character" w:styleId="TestCharacterStyle">
            <w:link w:val="TestParagraphStyle"/>
            …
        </w:style>

        通过链接元素将段落样式和字符样式配对，用于从字符样式定义中引用段落样式的styleId，反之亦然。由于根据上述规则允许此配对，因此必须将结果组合用作链接样式，该样式在应用程序中显示为一个样式，但根据需要使用字符和/或段落样式。示例结束]
        """
        return getattr(self, qn('w:link'), None)

    @property
    def autoRedefine(self) -> Optional[CT_OnOff]:
        """17.7.4.2 autoRedefine (自动将用户格式合并到样式定义中)

        这个元素指定了应用程序是否在修改应用了此样式的整个段落内容时自动修改此样式，确保虽然只有一个文本实例应用了此样式被修改，但该更改被存储在样式上，因此传播到使用该样式的所有位置。

        如果省略了此元素，则格式化将不会自动合并回样式定义中。

        【示例：考虑在 WordprocessingML 文档中定义的如下样式：

        <w:style w:styleId="Normal" … >
            <w:name w:val="Normal"/>
            <w:autoRedefine/>
            <w:rPr>
                <w:b/>
            </w:rPr>
            …
        </w:style>

        通过使用autoRedefine元素，此样式指定任何应用了此样式的文本所应用的任何格式化都必须合并回样式定义中（当然，前提是这是一个段落样式）。
        """
        return getattr(self, qn('w:autoRedefine'), None)

    @property
    def hidden(self) -> Optional[CT_OnOff]:
        """17.7.4.4 hidden (从用户界面隐藏样式)

        该元素指定了当应用程序加载此文档时，此样式是否应该从任何用户界面中隐藏。如果设置了该元素，则此样式可用于格式化内容（即引用此样式的任何内容应具有其属性正常），但该样式将从与该应用程序关联的所有用户界面中隐藏。[注：此设置通常用于隐藏应用程序内部正在使用但不应在典型情况下用作格式化的样式。结束注释]

        如果省略了该元素，则样式不需要从用户界面中隐藏。

        [示例：考虑一个主名称为InternalStyle的样式，不应在任何用户界面中显示。可以使用以下WordprocessingML来指定此要求：

        <w:style … w:styleId="Style2">
            <w:name w:val="InternalStyle"/>
            <w:hidden/>
            …
        </w:style>

        hidden元素指定此样式定义应与文件往返传输（因为它是文档的一部分），但不应在处理此文档的应用程序的任何用户界面中显示。结束示例]
        """
        return getattr(self, qn('w:hidden'), None)

    @property
    def uiPriority(self) -> Optional[CT_DecimalNumber]:
        """17.7.4.19 uiPriority (可选的用户界面排序顺序)

        该元素指定一个数字，可用于在应用程序加载此文档时对用户界面中的样式定义集进行排序，建议的设置在stylePaneSortMethod元素中指定（§17.15.1.86）。如果设置了该元素，则应使用此优先级按升序值对所有可用样式进行排序。

        如果省略了该元素，则该样式将不具有关联的优先级值，并且在指定了建议的排序顺序设置时，将被排序到样式定义列表的末尾（与无穷大优先级值几乎等效）。

        [示例：考虑一个具有主要名称为“评论样式”的样式，应具有关联的优先级值为十。可以使用以下WordprocessingML来指定此要求：

        <w:style … w:styleId="CStyle">
            <w:name w:val="Comment Style"/>
            <w:uiPriority w:val="10"/>
            …
        </w:style>

        uiPriority元素指定，当使用stylePaneSortMethod元素（§17.15.1.86）按建议顺序列出样式时，此样式定义应按值为10进行排序。

        end example]
        """
        return getattr(self, qn('w:uiPriority'), None)

    @property
    def semiHidden(self) -> Optional[CT_OnOff]:
        """17.7.4.16 semiHidden (从主用户界面隐藏样式)

        这个元素指定了当应用程序加载此文档时，是否应该将此样式从主用户界面中隐藏。如果设置了此元素，则可以使用此样式来格式化内容（即引用此样式的任何内容都应该具有其正常属性），但是该样式应该在与该应用程序关联的主用户界面中隐藏。

        【注：不应由ECMA-376来规定“主”用户界面的解释，可以由应用程序根据需要定义。

        此设置旨在定义一种样式属性，允许在高级用户界面中查看和修改样式，而不会在较低级别的设置中暴露样式，例如，用于格式化评论内容的样式通常不应该显示在简单用户界面中（因为通常不需要修改它），但是完全使用隐藏元素（§17.7.4.4）隐藏它将是不合适的，因为非常高级的用户可能想要更改其外观。结束注】

        如果省略了此元素，则不需要将该样式从主用户界面中隐藏。

        【示例：考虑一个名为“评论样式”的样式，不应该在主用户界面中显示。可以使用以下WordprocessingML来指定此要求：


        <w:style … w:styleId="CStyle">
            <w:name w:val="Comment Style"/>
            <w:semiHidden/>
            …
        </w:style>
        semiHidden元素指定此样式定义不应在处理此文档的应用程序中的任何主用户界面中显示。结束示例】
        """
        return getattr(self, qn('w:semiHidden'), None)

    @property
    def unhideWhenUsed(self) -> Optional[CT_OnOff]:
        """17.7.4.20 unhideWhenUsed (使用样式时删除半隐藏属性)

        Remove Semi-Hidden Property When Style Is Used

        该元素指定了当文档内容使用此样式时，是否应删除 semiHidden 属性（§17.7.4.16）。如果设置了该元素，则应用程序应确保，即使在样式上指定了 semiHidden 元素，当文档被重新保存时，如果样式被文档中的任何内容引用，该属性也会被删除。

        如果省略了该元素，则样式在文档内容中使用时不会自动丢失 semi-hidden 属性。

        [示例：考虑一个主要名称为“测试段落样式”的样式，在使用之前不应在主用户界面中显示。可以使用以下 WordprocessingML 来指定此要求：


        <w:style … w:styleId="TestStyle">
            <w:name w:val="Test Paragraph Style"/>
            <w:semiHidden/>
            <w:unhideWhenUsed/>
            …
        </w:style>

        unhideWhenUsed 元素指定此样式定义在处理此文档的应用程序关联的任何主用户界面中，直到被文档内容引用之前不应显示。如果向文档添加了引用此样式的段落：


        <w:p>
            <w:pPr>
                <w:pStyle w:val="TestStyle"/>
            </w:pPr>
            …
        </w:p>

        此样式现在被文档内容引用，并且在保存时将删除 semiHidden 元素。示例结束]
        """
        return getattr(self, qn('w:unhideWhenUsed'), None)

    @property
    def qFormat(self) -> Optional[CT_OnOff]:
        """17.7.4.14 qFormat (主要样式)

        这个元素指定了当应用程序加载此文档时，是否应将此样式视为主样式。如果设置了此元素，则表示当前文档中已将此样式指定为特别重要，并且应用程序可以以任何所需方式使用此信息。【注：此设置不意味着样式的任何行为，只表示该样式对于此文档非常重要。结束注】

        如果省略了此元素，则该样式不会被视为此文档的主样式。

        【示例：考虑一个名为PrimaryStyleExample的主样式，应被视为文档的主样式。可以使用以下WordprocessingML来指定此要求：


        <w:style … w:styleId="PStyle">
            <w:name w:val="PrimaryStyleExample"/>
            <w:qFormat/>
            …
        </w:style>

        qFormat元素指定此样式定义必须被视为此文档的主样式。

        结束示例】
        """

        return getattr(self, qn('w:qFormat'), None)

    @property
    def locked(self) -> Optional[CT_OnOff]:
        """17.7.4.7 locked (样式无法应用)

        该元素指定应用程序在加载和/或修改文档时是否应阻止使用此样式。如果设置了该元素，则可以使用此样式来格式化现有内容（即引用此样式的任何内容都应具有其属性），但应阻止通过与该应用程序相关的所有机制应用样式的新实例。

        如果省略了该元素，则应用程序处理此文档时不应阻止使用样式。

        [示例：考虑一个具有主名称为“测试样式”的样式，应锁定并阻止将其添加到给定文档中的任何内容。可以使用以下WordprocessingML来指定此要求：


        <w:style … w:styleId="TestStyle">
            <w:name w:val="Test Style"/>
            <w:locked/>
            …
        </w:style>

        锁定元素的存在指定必须通过与该应用程序相关的所有机制阻止应用样式的新实例。示例结束]
        """
        return getattr(self, qn('w:locked'), None)

    @property
    def personal(self) -> Optional[CT_OnOff]:
        """17.7.4.11 personal (电子邮件消息文本样式)

        该元素指定了父样式，在电子邮件消息的上下文中使用时，默认用于格式化一个或多个用户的所有消息文本。【注：此设置不提供关于样式的任何额外语义，但可在电子邮件的上下文中使用，自动重新格式化电子邮件消息的内容，同时忽略任何故意应用样式的内容（因为此样式隐式应用于消息文本，无需用户交互）。结束注】

        如果此元素在非字符样式的任何样式类型上指定，则应忽略此元素。如果不存在与此元素的val属性匹配的styleId的样式，或该样式不是字符样式，则应忽略此元素。

        如果省略此元素，则当前样式在电子邮件消息的上下文中不应被视为消息文本样式。

        【示例：考虑在WordprocessingML文档中定义如下样式：

        <w:style w:styleId="EmailText" w:type="character" >
            <w:name w:val="EmailText"/>
            <w:personal w:val="true" />
            <w:rPr>
                …
            </w:rPr>
        </w:style>

        通过使用personal元素，此样式指定了该样式是用于在电子邮件上下文中格式化消息文本的样式。结束示例】
        """
        return getattr(self, qn('w:personal'), None)

    @property
    def personalCompose(self) -> Optional[CT_OnOff]:
        """17.7.4.12 personalCompose (电子邮件信息撰写样式)

        该元素指定了父样式，在电子邮件消息的上下文中使用时，默认用于格式化电子邮件消息中的新消息文本。【注：此设置不提供关于样式的任何额外语义，但可在电子邮件的上下文中用于自动格式化电子邮件消息中新消息的内容。结束注】

        如果此元素在非字符样式的任何样式类型上指定，则应将此元素忽略。如果不存在样式的styleId与此元素的val属性匹配，或该样式不是字符样式，则应将此元素忽略。

        如果省略此元素，则当前样式在电子邮件消息的上下文中不应被视为消息组成文本样式。

        【示例：考虑在WordprocessingML文档中定义如下样式：


        <w:style w:styleId="EmailText" w:type="character" >
            <w:name w:val="EmailText"/>
            <w:personalCompose w:val="true" />
            <w:rPr>
                …
            </w:rPr>
        </w:style>

        通过personalCompose元素的使用，此样式指定为用于在电子邮件上下文中格式化新消息文本的样式。结束示例】
        """
        return getattr(self, qn('w:personalCompose'), None)

    @property
    def personalReply(self) -> Optional[CT_OnOff]:
        """17.7.4.13 personalReply (电子邮件回复样式)

        该元素指定，当在电子邮件消息的上下文中使用时，父样式可以默认用于格式化电子邮件消息中现有消息文本的新回复生成时。【注：此设置不提供关于样式的任何额外语义，但可用于在电子邮件上下文中自动格式化电子邮件消息中现有测试内容。结束注】

        如果此元素在非字符样式的任何样式类型上指定，则应将此元素忽略。如果不存在样式的styleId与此元素的val属性匹配，或该样式不是字符样式，则应将此元素忽略。

        如果省略此元素，则当前样式在电子邮件消息的上下文中不应被视为消息回复文本样式。

        【示例：考虑在WordprocessingML文档中定义如下样式：


        <w:style w:styleId="EmailText" w:type="character" >
            <w:name w:val="EmailText"/>
            <w:personalReply w:val="true" />
            <w:rPr>
                …
            </w:rPr>
        </w:style>

        通过使用personalReply元素，此样式指定该样式用于格式化电子邮件上下文中现有消息文本。结束示例】
        """
        return getattr(self, qn('w:personalReply'), None)

    @property
    def rsid(self) -> Optional[CT_LongHexNumber]:
        """17.7.4.15 rsid (样式定义的修订标识符)

        该元素指定一个唯一的四位数字，用于确定最后修改此样式定义的编辑会话。该值应符合以下约束：所有指定相同rsid*值的文档元素应对应于在同一编辑会话中进行的更改。编辑会话被定义为发生在任意两个连续保存操作之间的编辑期间。[注：此设置不暗示样式的任何行为，只是该样式在一个特定编辑会话中最后被修改。此信息可以由应用程序以任何所需方式进行解释。结束注]

        如果省略此元素，则不应将修订标识符与父样式定义关联。

        [示例：考虑一个名为PrimaryStyleExample的主样式的样式，定义如下：

        <w:style … w:styleId="PStyle">
            <w:name w:val="PrimaryStyleExample"/>
            <w:rsid w:val="3E412D01"/>
            …
        </w:style>

        rsid元素指定此样式定义最后在与值3E412D01对应的编辑会话中进行了编辑。结束示例]
        """
        return getattr(self, qn('w:rsid'), None)

    @property
    def pPr(self) -> Optional[CT_PPrGeneral]:
        """17.7.5.2 pPr (段落属性)

        该元素指定了一组段落属性，这些属性包括当前WordprocessingML文档的默认段落属性。[理由：pPr元素存在于pPrDefault元素中的原因是为了方便在WordprocessingML文档中重新使用任何一组段落属性 - 因为段落属性始终是单个pPr元素的子元素，所以该元素可以完整地移动到所需的新位置，而无需进行其他修改。结束理由]

        如果省略此元素，则当前文档的默认段落属性不存在（即没有默认段落属性，因此默认值是应用程序定义的）。

        [示例：考虑以下WordprocessingML文档的文档默认值定义：


        <w:docDefaults>
            <w:pPrDefault>
                <w:pPr>
                    <w:jc w:val="center"/>
                </w:pPr>
            </w:pPrDefault>
            …
        </w:docDefaults>

        作为pPrDefault元素的子元素的pPr元素包含此文档的默认段落属性集 - 在此示例中，是居中对齐的值。结束示例]
        """
        return getattr(self, qn('w:pPr'), None)

    @property
    def rPr(self) -> Optional[CT_RPr]:
        """17.7.5.4 rPr (Run属性)

        该元素指定了组成当前WordprocessingML文档默认运行属性集的运行属性。[理由：rPrDefault元素中存在rPr元素的原因是为了允许在WordprocessingML文档中轻松重新利用任何运行属性集 - 因为运行属性始终是单个rPr元素的子元素，所以该元素可以完整地移动到所需的新位置而无需额外修改。结束理由]

        如果省略此元素，则当前文档的默认运行属性不存在（即没有默认运行属性，因此默认值由应用程序定义）。

        [示例：考虑以下WordprocessingML文档的文档默认值定义：


        <w:docDefaults>
            …
            <w:rPrDefault>
                <w:rPr>
                    <w:b/>
                </w:rPr>
            </w:rPrDefault>
        </w:docDefaults>

        作为rPrDefault元素的子元素的rPr元素包含了此文档的默认运行属性集 - 在本例中为粗体文本。结束示例]

        该元素内容模型（CT_RPr）的W3C XML模式定义位于§A.1。上表中的每个子元素不得出现超过一次。

        [注：由于W3C XML模式语言的限制，此限制未反映在元素的内容模型中。结束注]
        """
        return getattr(self, qn('w:rPr'), None)

    @property
    def tblPr(self) -> Optional[CT_TblPrBase]:
        """17.7.6.4 tblPr (样式表属性)

        这个元素指定了应用于表格的一组表格属性。这些属性不是有条件的，应始终应用（尽管它们是在所有有条件格式属性之前应用）。

        [示例：考虑以下定义的表格样式：


        <w:style w:type="table" w:styleId="exampleTableStyle">
            <w:tblPr>
                <w:tblCellSpacing w:w="15" w:type="dxa"/>
            </w:tblPr>
            …
            <w:tblStylePr w:type="firstRow">-
                <w:tblPr>
                    <w:tblCellSpacing w:w="29" w:type="dxa"/>
                </w:tblPr>
                …
            </w:tblStylePr>
        </w:style>
        在样式元素内指定的tblPr元素指定了必须应用于表格所有部分的一组表格属性。在这个示例中，应用的单个表格属性是通过tblCellSpacing元素（§17.4.45）设置的默认表格单元间距值为0.01英寸。结束示例]
        """
        return getattr(self, qn('w:tblPr'), None)

    @property
    def trPr(self) -> Optional[CT_TrPr]:
        """17.7.6.11 trPr (样式表行属性)

        该元素指定应用于表格的一组表行属性。这些属性不是有条件的，应始终应用（尽管它们是在所有有条件格式属性之前应用）。

        [示例：考虑以下定义的表格样式：

        <w:style w:type="table" w:styleId="exampleTableStyle">
            <w:trPr>
                <w:jc w:val="center"/>
            </w:trPr>
        </w:style>

        在样式元素中指定的trPr元素指定了必须应用于表格所有部分的一组表行属性。在此示例中，应用的单个表行属性是通过jc元素设置为居中的对齐设置（§17.4.27）。示例结束]
        """
        return getattr(self, qn('w:trPr'), None)

    @property
    def tcPr(self) -> Optional[CT_TcPr]:
        """17.7.6.9 tcPr (样式表单元格属性)

        该元素指定应用于表格的一组表格单元格属性。这些属性不是有条件的，应始终应用（尽管它们是在所有有条件格式设置之前应用）。

        [示例：考虑以下定义的表格样式：

        <w:style w:type="table" w:styleId="exampleTableStyle">
            <w:tcPr>
                <w:tcFitText/>
            </w:tcPr>
        </w:style>

        在样式元素中指定的tcPr元素指定了必须应用于表格所有部分的表格单元格属性集。在此示例中，应用的单个表格单元格属性是通过tcFitText元素设置的适合文本设置（§17.4.67）。示例结束]
        """
        return getattr(self, qn('w:tcPr'), None)

    @property
    def tblStylePr(self) -> list[CT_TblStylePr]:
        """17.7.6.6 tblStylePr (样式条件表格式化属性)

        该元素指定了一组格式属性，这些属性应根据在type属性上指定的要求匹配的表部分进行有条件地应用。这些表条件格式应用于表的不同区域，如下所示：

        表中的所有行也可以根据交替行/列的基础进行条件格式设置，如下所示：

        当指定时，这些条件格式应按以下顺序应用（因此后续格式将覆盖先前格式的属性）：

        - 整个表
        - 带状列，偶数列带状
        - 带状行，偶数行带状
        - 第一行，最后一行
        - 第一列，最后一列
        - 左上，右上，左下，右下

        [示例：考虑一个包含条件格式设置的表样式，定义如下：


        <w:style w:type="table" w:styleId="exampleTableStyle">
            …
            <w:tblStylePr w:type="firstRow">
                <w:tblPr>
                    <w:tblCellSpacing w:w="29" w:type="dxa"/>
                </w:tblPr>
                …
            </w:tblStylePr>
        </w:style>

        tblStylePr元素指定了一组表属性，这些属性必须有条件地应用于符合type属性指定的标准的表的所有部分（在本例中，当前表的所有标题行）。
        """

        return self.findall(qn('w:tblStylePr'))  # type: ignore

    @property
    def type(self) -> ST_StyleType:
        """type（样式类型）

        指定由此元素定义的样式定义的类型。WordprocessingML支持六种样式定义类型：

        - 段落样式(Paragraph styles)
        - 字符样式(Character styles)
        - 表格样式(Table styles)
        - 编号样式(Numbering styles)
        - 链接样式（段落 + 字符）(Linked styles (paragraph + character))
        - 默认段落 + 字符属性 (Default paragraph + character properties)

        前四种样式类型中的每一种对应于此属性中的不同值，因此定义了当前样式的样式类型。[注：最后两种样式类型是独特的，它们不仅仅是一种样式类型：链接样式是通过链接元素（[§17.7.4.6]）将字符和段落样式配对；文档默认属性是通过docDefaults元素（[§17.7.5.1]）定义的。结束注]

        如果未指定此属性，则应假定默认值为段落。

        [示例：考虑以下定义的样式：

        <w:style w:type="paragraph" … >
            <w:name w:val="My Paragraph Style"/>
            <w:rPr>
                <w:b/>
            </w:rPr>
        </w:style>

        段落的type属性值指定此样式定义创建了一个段落样式。结束示例]
        """
        _val = self.attrib.get(qn('w:type'))

        if _val is not None:
            return ST_StyleType(_val)

        return ST_StyleType.paragraph

    @property
    def styleId(self) -> Optional[str]:
        """styleId（样式ID）

        指定父样式定义的唯一标识符。此标识符应在多个上下文中使用，以在文档中唯一引用此样式定义。

        [示例：以下是通过其styleId属性值引用样式的元素示例：

        - 通过元素如 pStyle 元素（§17.3.1.27）、rStyle元素（§17.3.2.29）和tblStyle元素（§17.4.62）分别用于段落、运行和表格的内容引用样式。
        - 通过 link 元素（§17.7.4.6）链接样式的段落和字符版本。
        - 通过basedOn元素（§17.7.4.3）引用样式继承的父样式。 结束示例]

        如果多个样式定义各自声明其styleId的相同值，则第一个这样的实例应保留其当前标识符，所有其他实例可以以任何所需方式重新分配。此重新分配不需要修复内容中对这些样式定义的引用（即，由于文档格式不正确，某些内容可能会丢失其样式定义信息）。

        如果未指定此属性，则可以以任何所需方式分配样式ID。

        [示例：考虑以下定义的段落样式：

        <w:style w:type="paragraph" w:styleId="MyStyle" >
            <w:name w:val="My Paragraph Style"/>
            <w:rPr>
                <w:b/>
            </w:rPr>
        </w:style>

        此段落样式指定其样式标识符必须为MyStyle，使用styleId属性。

        现在考虑同一WordprocessingML文档中的以下段落：

        <w:p>
            <w:pPr>
                <w:pStyle w:val="MyStyle"/>
            </w:pPr>
            …
        </w:p>
        <w:p>
            …
        </w:p>

        第一个段落的内容必须应用加粗段落属性，因为其段落属性指定它们必须继承其styleId为MyStyle的段落样式，因此使用样式层次结构的规则继承其属性。结束示例]
        """
        _val = self.attrib.get(qn('w:styleId'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def default(self) -> Optional[s_ST_OnOff]:
        """default（默认样式）

        指定此样式为此样式类型的默认样式。

        此属性与type属性一起使用，用于确定应用于未明确声明样式的对象的样式。【示例：设置了默认属性的段落样式是应用于所有未明确使用pStyle元素（§17.3.1.27）引用段落样式的段落的段落样式。示例结束】

        如果未为任何样式指定此属性，则不应用任何属性于指定样式类型的对象。如果多个样式指定了此属性，则将使用具有此属性的样式的最后一个实例。

        【示例：考虑以下定义的段落样式：

        <w:style w:type="paragraph" w:default="1" w:styleId="MyStyle" >
            <w:name w:val="My Paragraph Style"/>
            <w:rPr>
            <w:b/>
            </w:rPr>
        </w:style>

        此段落样式指定为默认段落样式，因此所有未明确引用段落样式的段落必须应用此样式。

        例如，考虑同一WordprocessingML文档中的以下段落：

        <w:p>
            <w:pPr>
                <w:pStyle w:val="Normal"/>
            </w:pPr>
            …
        </w:p>
        <w:p>
            …
        </w:p>

        第一个段落的内容必须应用Normal段落样式，而第二个段落的内容必须应用MyStyle段落样式，因为它未明确引用段落样式，因此继承默认样式。示例结束】
        """
        _val = self.attrib.get(qn('w:default'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def customStyle(self) -> Optional[s_ST_OnOff]:
        """customStyle（用户定义样式）

        指定此样式为用户定义样式（即非应用程序自动生成的样式）。此设置（具体为true或其等效值）不应允许应用程序自动更改与样式相关联的格式，但可用于指定，如果已知相关样式ID，则可以将某些用户界面行为应用于其定义。【示例：样式的主要名称可以本地化以匹配当前用户界面语言。示例结束】

        如果省略此属性，则应假定该样式为内置样式。

        【示例：考虑以下定义的段落样式：

            <w:style w:type="paragraph" w:styleId="MyStyle"
                w:customStyle="true">
                <w:name w:val="My Paragraph Style"/>
                <w:rPr>
                    <w:b/>
                </w:rPr>
            </w:style>

        此段落样式指定其为用户定义样式，使用customStyle属性的值为true。因此，如果应用程序与样式ID MyStyle 关联了行为，则可以对该样式采取行动。示例结束】
        """
        _val = self.attrib.get(qn('w:customStyle'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None


class CT_LsdException(OxmlBaseElement):
    """17.7.4.8 lsdException (潜在样式异常)

    该元素指定了应用于此文档的单个潜在样式的属性。潜在样式是指任何已知样式定义集，这些定义未包含在当前文档中。

    [示例：考虑一个包含在两种样式之一（Heading1或Normal）中指定文本的WordprocessingML文档。基于此，文档只需要存储这两种样式的格式属性，从而节省了保存托管应用程序支持的所有样式所需的额外开销。

    然而，如果documentProtection元素（§17.15.1.29）指定托管应用程序必须阻止使用任何其locked元素（§17.7.4.7）设置为false的样式，则该应用程序已知的所有样式的锁定状态变得有用且必要以维持文档的当前状态。使用潜在样式，可以存储此信息，而无需存储这些样式的任何格式属性。

    例如，如果所有未存储在文档中的样式必须被锁定，除了具有主名称（§17.7.4.9）为Heading 2的样式。可以使用潜在样式来指定此要求，如下所示：


    <w:latentStyles … w:defLockedState="true">
        <w:lsdException w:name="Heading 2" w:locked="false"/>
    </w:latentStyles>
    lsdException元素指定具有主名称Heading 2的潜在样式必须具有false的锁定状态设置。示例结束]

    如果省略此元素，则latentStyles元素上指定的默认值没有潜在样式异常。
    """

    @property
    def name(self) -> str:
        """name（主样式名称）

        指定应继承此一组潜在样式属性异常的样式的主名称。

        如果当前应用程序不知道具有当前名称的内部主样式，则可以忽略此一组潜在样式异常。

        [示例：考虑一个WordprocessingML文档，其中所有未存储在文档中的样式必须被锁定，除了TestStyle样式。可以使用潜在样式来指定此要求，如下所示：

        <w:latentStyles … w:defLockedState="true">
            <w:lsdException w:name="TestStyle" w:locked="false"/>
        </w:latentStyles>

        潜在样式异常上的name属性指定TestStyle样式必须具有此一组潜在样式属性（如果应用程序知道具有此名称的样式）。示例结束]
        """
        _val = self.attrib[qn('w:name')]

        return str(_val)

    @property
    def locked(self) -> Optional[s_ST_OnOff]:
        """locked（潜在样式锁定设置）

        指定将应用于具有匹配样式名称值的潜在样式的锁定元素（§17.7.4.7）的默认设置。

        如果省略此属性，则此潜在样式的默认锁定状态将由父潜在样式元素上的defLockedState属性确定。

        [示例：考虑一个WordprocessingML文档，其中所有未存储在文档中的样式必须被锁定，除了TestStyle样式。可以使用潜在样式来指定此要求，如下所示：

        <w:latentStyles … w:defLockedState="true">
            <w:lsdException w:name="TestStyle" w:locked="false"/>
        </w:latentStyles>

        潜在样式异常上的locked属性指定TestStyle样式必须默认具有false的锁定元素设置。示例结束]
        """
        _val = self.attrib.get(qn('w:locked'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def uiPriority(self) -> Optional[ST_DecimalNumber]:
        """uiPriority（覆盖默认排序顺序）

        指定应用于具有匹配样式名称值的潜在样式的uiPriority元素（§17.7.4.19）的默认设置。

        如果省略此属性，则此潜在样式的默认uiPriority状态将由父latentStyles元素上的defUIPriority属性确定。

        [示例：考虑一个WordprocessingML文档，其中所有未存储在文档中的样式必须具有优先级值为10，除了TestStyle样式。

        可以使用潜在样式来指定此要求，如下所示：


        <w:latentStyles … w:defUIPriority="10">
            <w:lsdException w:name="TestStyle" w:uiPriority="25"/>
        </w:latentStyles>

        潜在样式异常上的uiPriority属性指定TestStyle样式必须具有默认的uiPriority元素设置为25。结束示例]
        """

        _val = self.attrib.get(qn('w:uiPriority'))

        if _val is not None:
            return ST_DecimalNumber(_val)
        return None

    @property
    def semiHidden(self) -> Optional[s_ST_OnOff]:
        """semiHidden（半隐藏文本覆盖）

        指定应用于具有匹配样式名称值的潜在样式的semiHidden元素（§17.7.4.16）的默认设置。

        如果省略此属性，则将通过父潜在样式元素上的defSemiHidden属性确定此潜在样式的默认semiHidden状态。

        [示例：考虑一个WordprocessingML文档，其中所有未存储在文档中的样式必须不是半隐藏的，除了TestStyle样式。可以使用潜在样式来指定此要求，如下所示：

        <w:latentStyles … w:defSemiHidden="false">
            <w:lsdException w:name="TestStyle" w:semiHidden="true"/>
        </w:latentStyles>

        潜在样式异常上的semiHidden属性指定TestStyle样式必须默认具有semiHidden元素设置为true。结束示例]
        """
        _val = self.attrib.get(qn('w:semiHidden'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def unhideWhenUsed(self) -> Optional[s_ST_OnOff]:
        """unhideWhenUsed（在使用时取消隐藏）

        指定应用于具有匹配样式名称值的潜在样式的unhideWhenUsed元素（§17.7.4.20）的默认设置。

        如果省略此属性，则此潜在样式的默认unhideWhenUsed状态将由父latentStyles元素上的defUnhideWhenUsed属性确定。

        [示例：考虑一个WordprocessingML文档，其中所有样式在使用前都应该被隐藏，除了TestStyle样式。可以使用潜在样式来指定此要求，如下所示：

        <w:latentStyles … w:defUnhideWhenUsed="true">
            <w:lsdException w:name="TestStyle" w:unhideWhenUsed="false"/>
        </w:latentStyles>

        潜在样式异常上的unhideWhenUsed属性指定TestStyle样式必须具有默认的unhideWhenUsed元素设置为false。结束示例]
        """
        _val = self.attrib.get(qn('w:unhideWhenUsed'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def qFormat(self) -> Optional[s_ST_OnOff]:
        """qFormat（潜在样式主样式设置）

        指定应用于具有匹配样式名称值的潜在样式的qFormat元素（§17.7.4.14）的默认设置。

        如果省略此属性，则将通过父潜在样式元素上的defQFormat属性确定此潜在样式的默认qFormat状态。

        [示例：考虑一个WordprocessingML文档，其中所有未存储在文档中的样式必须不是主样式，除了TestStyle样式。可以使用潜在样式来指定此要求，如下所示：


        <w:latentStyles … w:defQFormat="false">
            <w:lsdException w:name="TestStyle" w:qFormat="true"/>
        </w:latentStyles>
        潜在样式异常上的qFormat属性指定TestStyle样式必须默认具有qFormat元素设置为true。结束示例]
        """
        _val = self.attrib.get(qn('w:qFormat'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None


class CT_LatentStyles(OxmlBaseElement):
    """17.7.4.5 latentStyles (潜在样式信息)

    该元素指定应用于此文档的一组潜在样式的属性。潜在样式是指应用程序已知但未包含在当前文档中的任何样式定义集。【示例：潜在样式可以包括特定托管应用程序已知的附加样式。示例结束】

    当样式定义嵌入文档时，它指定了两个不同的属性组：

    - 行为属性(Behavior properties)
    - 格式属性(Formatting properties)

    显然，在每个文档中嵌入特定应用程序已知的所有样式将极大地增加文件大小。潜在样式提供了一种存储信息片段的方式，用于第一组（行为属性）应用于所有应用程序已知的样式，而无需存储第二组（格式属性）。

    如果省略此元素，则其各个属性所代表的设置值由下面属性描述中的默认值给出。

    【示例：考虑一个包含在两种样式中指定文本的WordprocessingML文档：Heading1或Normal。基于此，文档只需要存储这两种样式的格式属性，从而节省了保存托管应用程序支持的所有样式所需的额外开销。

    但是，如果documentProtection元素（§17.15.1.29）指定托管应用程序应阻止任何已锁定元素（§17.7.4.7）设置为false的样式的使用，则该应用程序已知的所有样式的锁定状态变得有用且必要以维护文档的当前状态。使用潜在样式，可以存储此信息，而无需存储这些样式的任何格式属性。

    例如，如果文档中未存储的所有样式必须被锁定，除了具有主名称（§17.7.4.9）为Heading 2的样式。可以使用潜在样式来指定此要求如下：

    <w:latentStyles … w:defLockedState="true">
        <w:lsdException w:name="Heading 2" w:locked="false"/>
    </w:latentStyles>

    latentStyles元素指定任何托管应用程序已知的所有潜在样式必须具有默认锁定状态为true，除了任何已知托管应用程序的主名称为Heading 2的样式，其潜在样式定义指定其锁定状态必须为false。示例结束】
    """

    @property
    def lsdException(self) -> list[CT_LsdException]:
        """17.7.4.8 lsdException (潜在样式异常)

        该元素指定了应用于此文档的单个潜在样式的属性。潜在样式是指任何已知样式定义集，这些定义未包含在当前文档中。

        [示例：考虑一个包含在两种样式之一（Heading1或Normal）中指定文本的WordprocessingML文档。基于此，文档只需要存储这两种样式的格式属性，从而节省了保存托管应用程序支持的所有样式所需的额外开销。

        然而，如果documentProtection元素（§17.15.1.29）指定托管应用程序必须阻止使用任何其locked元素（§17.7.4.7）设置为false的样式，则该应用程序已知的所有样式的锁定状态变得有用且必要以维持文档的当前状态。使用潜在样式，可以存储此信息，而无需存储这些样式的任何格式属性。

        例如，如果所有未存储在文档中的样式必须被锁定，除了具有主名称（§17.7.4.9）为Heading 2的样式。可以使用潜在样式来指定此要求，如下所示：


        <w:latentStyles … w:defLockedState="true">
            <w:lsdException w:name="Heading 2" w:locked="false"/>
        </w:latentStyles>
        lsdException元素指定具有主名称Heading 2的潜在样式必须具有false的锁定状态设置。示例结束]

        如果省略此元素，则latentStyles元素上指定的默认值没有潜在样式异常。
        """
        return self.findall(qn('w:lsdException'))  # type: ignore

    @property
    def defLockedState(self) -> Optional[s_ST_OnOff]:
        """defLockedState（默认样式锁定设置）

        指定应用于当前文档中未明确定义的由托管应用程序提供的任何样式的锁定元素（§17.7.4.7）的默认设置。对于存在潜在样式异常（§17.7.4.8）的每个样式，此设置将被覆盖。

        如果省略此属性，则当前文档中所有潜在样式的默认锁定状态应为 false。

        【示例：考虑一个 WordprocessingML 文档，其中所有未存储在文档中的样式必须被锁定。此要求将使用潜在样式指定如下：

        <w:latentStyles … w:defLockedState="true">
            …
        </w:latentStyles>

        defLockedState 属性指定了当前文档中所有潜在样式的默认锁定元素设置为 true。结束示例】
        """
        _val = self.attrib.get(qn('w:defLockedState'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def defUIPriority(self) -> Optional[ST_DecimalNumber]:
        """指定uiPriority元素（§17.7.4.19）的默认设置，该设置应用于主机应用程序提供的任何未在当前文档中明确定义的样式。对于存在潜在样式异常（§17.7.4.8）的每个样式，此设置将被覆盖。

        如果省略此属性，则当前文档中所有潜在样式的默认uiPriority状态为99。

        [示例：考虑一个WordprocessingML文档，其中所有未存储在文档中的样式不能标记为半隐藏。可以使用潜在样式来指定此要求，如下所示：

        <w:latentStyles … w:defUIPriority="10">
        …
        </w:latentStyles>

        defUIPriority属性指定当前文档中所有潜在样式必须默认具有uiPriority元素设置为10。示例结束]
        """
        _val = self.attrib.get(qn('w:defUIPriority'))

        if _val is not None:
            return ST_DecimalNumber(_val)
        return None

    @property
    def defSemiHidden(self) -> Optional[s_ST_OnOff]:
        """defSemiHidden（默认半隐藏设置）

        指定semiHidden元素（§17.7.4.16）的默认设置，应用于主机应用程序提供的任何未在当前文档中明确定义的样式。对于存在潜在样式异常（§17.7.4.8）的每个样式，将覆盖此设置。

        如果省略此属性，则当前文档中所有潜在样式的默认semiHidden状态应为false。

        [示例：考虑一个WordprocessingML文档，其中所有未存储在文档中的样式都不得标记为半隐藏。可以使用潜在样式来指定此要求，如下所示：

        <w:latentStyles … w:defSemiHidden="false">
            …
        </w:latentStyles>

        defSemiHidden属性指定当前  文档中所有潜在样式的默认semiHidden元素设置为false。示例结束]
        """
        _val = self.attrib.get(qn('w:defSemiHidden'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def defUnhideWhenUsed(self) -> Optional[s_ST_OnOff]:
        """defUnhideWhenUsed（默认隐藏直到使用设置）

        指定unhideWhenUsed元素（§17.7.4.20）的默认设置，该设置应用于主机应用程序提供的任何未在当前文档中明确定义的样式。对于存在潜在样式异常（§17.7.4.8）的每个样式，此设置将被覆盖。

        如果省略此属性，则当前文档中所有潜在样式的默认unhideWhenUsed状态为false。

        [示例：考虑一个WordprocessingML文档，其中所有未存储在文档中的样式必须在文档内容中使用时才显示。

        可以使用潜在样式来指定此要求，如下所示：

        <w:latentStyles … w:defUnhideWhenUsed="true">
        …
        </w:latentStyles>

        defUnhideWhenUsed属性指定当前文档中所有潜在样式必须默认具有unhideWhenUsed元素设置为true。示例结束]
        """
        _val = self.attrib.get(qn('w:defUnhideWhenUsed'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def defQFormat(self) -> Optional[s_ST_OnOff]:
        """defQFormat（默认主样式设置）

        指定qFormat元素（§17.7.4.14）的默认设置，应用于主机应用程序提供的任何未在当前文档中明确定义的样式。对于存在潜在样式异常（§17.7.4.8）的每个样式，将覆盖此设置。

        如果省略此属性，则当前文档中所有潜在样式的默认qFormat状态应为false。

        [示例：考虑一个WordprocessingML文档，其中所有未存储在文档中的样式都不得标记为主样式。可以使用潜在样式来指定此要求，如下所示：

        <w:latentStyles … w:defQFormat="false">
            …
        </w:latentStyles>

        defQFormat属性指定当前文档中所有潜在样式的默认qFormat元素设置为false。示例结束]
        """
        _val = self.attrib.get(qn('w:defQFormat'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None

    @property
    def count(self) -> Optional[ST_DecimalNumber]:
        """count（潜在样式计数）

        指定在首次处理此文档时应将已知样式的数量初始化为当前潜在样式默认值。【注：应用程序可根据需要使用此属性，以确保仅有在创建此文档时已知的样式数量会使用父元素上的默认值进行初始化，并且所有新的已知样式将使用它们的默认值。结束注】

        【示例：考虑一个 WordprocessingML 文档，其中只有前 20 个潜在样式必须被初始化。此要求将被指定如下：

        <w:latentStyles w:count="20" … >
            …
        </w:latentStyles>

        count 属性指定了在文档首次打开时必须将 20 个已知样式初始化为默认设置，并且任何额外的样式应使用应用程序定义的默认值。结束示例】
        """
        _val = self.attrib.get(qn('w:count'))

        if _val is not None:
            return ST_DecimalNumber(_val)
        return None


class CT_Styles(OxmlBaseElement):
    """17.7.4.18 styles (样式定义合集)

    该元素指定了存储在WordprocessingML文档中的所有样式信息：样式定义以及潜在样式信息。

    【示例：文字处理文档中的普通段落样式可以具有任意数量的格式属性，例如字体 = Times New Roman；字号 = 12pt；段落对齐 = 左对齐。引用此段落样式的所有段落将自动继承这些属性。示例结束】
    """

    @property
    def docDefaults(self) -> Optional[CT_DocDefaults]:
        """17.7.5.1 docDefaults (文档默认的段落和运行属性)

        该元素指定了应用于当前WordprocessingML文档中每个段落和文本运行的默认段落和运行属性集。这些属性首先应用于样式层次结构中；因此，它们会被任何进一步冲突的格式覆盖，但如果没有进一步的格式存在，则会应用。

        如果省略了此元素，则文档默认值将由托管应用程序定义。

        [示例：考虑以下WordprocessingML文档的文档默认值定义：

        <w:docDefaults>
            <w:rPrDefault>
                <w:rPr>
                    <w:b/>
                </w:rPr>
            </w:rPrDefault>
            <w:pPrDefault>
                <w:pPr>
                    <w:jc w:val="center"/>
                </w:pPr>
            </w:pPrDefault>
        </w:docDefaults>

        docDefaults的子元素指定了居中文本的默认段落属性和粗体文本的默认运行属性。将此格式应用于同一文档的主文档部分中的以下片段：

        <w:body>
            <w:p>
                <w:r>
                    <w:t>Hello, world</w:t>
                </w:r>
            </w:p>
        </w:body>

        此段落不包含任何格式属性，因此，使用样式层次结构，文档默认段落和运行属性将按照docDefaults元素中指定的方式应用，生成的段落将按照jc元素（§17.3.1.13）指定的方式居中，以及按照b元素（§17.3.2.1）指定的方式加粗。示例结束]
        """
        return getattr(self, qn('w:docDefaults'), None)

    @property
    def latentStyles(self) -> Optional[CT_LatentStyles]:
        """17.7.4.5 latentStyles (潜在样式信息)

        该元素指定应用于此文档的一组潜在样式的属性。潜在样式是指应用程序已知但未包含在当前文档中的任何样式定义集。【示例：潜在样式可以包括特定托管应用程序已知的附加样式。示例结束】

        当样式定义嵌入文档时，它指定了两个不同的属性组：

        - 行为属性(Behavior properties)
        - 格式属性(Formatting properties)

        显然，在每个文档中嵌入特定应用程序已知的所有样式将极大地增加文件大小。潜在样式提供了一种存储信息片段的方式，用于第一组（行为属性）应用于所有应用程序已知的样式，而无需存储第二组（格式属性）。

        如果省略此元素，则其各个属性所代表的设置值由下面属性描述中的默认值给出。

        【示例：考虑一个包含在两种样式中指定文本的WordprocessingML文档：Heading1或Normal。基于此，文档只需要存储这两种样式的格式属性，从而节省了保存托管应用程序支持的所有样式所需的额外开销。

        但是，如果documentProtection元素（§17.15.1.29）指定托管应用程序应阻止任何已锁定元素（§17.7.4.7）设置为false的样式的使用，则该应用程序已知的所有样式的锁定状态变得有用且必要以维护文档的当前状态。使用潜在样式，可以存储此信息，而无需存储这些样式的任何格式属性。

        例如，如果文档中未存储的所有样式必须被锁定，除了具有主名称（§17.7.4.9）为Heading 2的样式。可以使用潜在样式来指定此要求如下：

        <w:latentStyles … w:defLockedState="true">
            <w:lsdException w:name="Heading 2" w:locked="false"/>
        </w:latentStyles>

        latentStyles元素指定任何托管应用程序已知的所有潜在样式必须具有默认锁定状态为true，除了任何已知托管应用程序的主名称为Heading 2的样式，其潜在样式定义指定其锁定状态必须为false。示例结束】
        """
        return getattr(self, qn('w:latentStyles'), None)

    @property
    def style(self) -> list[CT_Style]:
        """样式合集"""

        return self.findall(qn('w:style'))  # type: ignore


class CT_Panose(OxmlBaseElement):
    @property
    def val(self) -> str:
        _val = self.attrib[qn('w:val')]

        return str(_val)


class ST_FontFamily(ST_BaseEnumType):
    decorative = 'decorative'
    modern = 'modern'
    roman = 'roman'
    script = 'script'
    swiss = 'swiss'
    auto = 'auto'


class CT_FontFamily(OxmlBaseElement):
    @property
    def val(self) -> ST_FontFamily:
        _val = self.attrib[qn('w:val')]

        return ST_FontFamily(_val)


class ST_Pitch(ST_BaseEnumType):
    fixed = 'fixed'
    variable = 'variable'
    default = 'default'


class CT_Pitch(OxmlBaseElement):
    @property
    def val(self) -> ST_Pitch:
        _val = self.attrib[qn('w:val')]

        return ST_Pitch(_val)


class CT_FontSig(OxmlBaseElement):
    @property
    def usb0(self) -> ST_LongHexNumber:
        _val = self.attrib[qn('w:usb0')]

        return ST_LongHexNumber(_val)

    @property
    def usb1(self) -> ST_LongHexNumber:
        _val = self.attrib[qn('w:usb1')]

        return ST_LongHexNumber(_val)

    @property
    def usb2(self) -> ST_LongHexNumber:
        _val = self.attrib[qn('w:usb2')]

        return ST_LongHexNumber(_val)

    @property
    def usb3(self) -> ST_LongHexNumber:
        _val = self.attrib[qn('w:usb3')]

        return ST_LongHexNumber(_val)

    @property
    def csb0(self) -> ST_LongHexNumber:
        _val = self.attrib[qn('w:csb0')]

        return ST_LongHexNumber(_val)

    @property
    def csb1(self) -> ST_LongHexNumber:
        _val = self.attrib[qn('w:csb1')]

        return ST_LongHexNumber(_val)


class CT_FontRel(CT_Rel):
    @property
    def fontKey(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:fontKey'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def subsetted(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:subsetted'))

        if _val is not None:
            return s_ST_OnOff(_val)
        return None


class CT_Font(OxmlBaseElement):
    @property
    def altName(self) -> Optional[CT_String]:
        return getattr(self, qn('w:altName'), None)

    @property
    def panose1(self) -> Optional[CT_Panose]:
        return getattr(self, qn('w:panose1'), None)

    @property
    def charset(self) -> Optional[CT_Charset]:
        return getattr(self, qn('w:charset'), None)

    @property
    def family(self) -> Optional[CT_FontFamily]:
        return getattr(self, qn('w:family'), None)

    @property
    def notTrueType(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:notTrueType'), None)

    @property
    def pitch(self) -> Optional[CT_Pitch]:
        return getattr(self, qn('w:pitch'), None)

    @property
    def sig(self) -> Optional[CT_FontSig]:
        return getattr(self, qn('w:sig'), None)

    @property
    def embedRegular(self) -> Optional[CT_FontRel]:
        return getattr(self, qn('w:embedRegular'), None)

    @property
    def embedBold(self) -> Optional[CT_FontRel]:
        return getattr(self, qn('w:embedBold'), None)

    @property
    def embedItalic(self) -> Optional[CT_FontRel]:
        return getattr(self, qn('w:embedItalic'), None)

    @property
    def embedBoldItalic(self) -> Optional[CT_FontRel]:
        return getattr(self, qn('w:embedBoldItalic'), None)

    @property
    def name(self) -> str:
        _val = self.attrib[qn('w:name')]

        return str(_val)


class CT_FontsList(OxmlBaseElement):
    @property
    def font(self) -> list[CT_Font]:
        return self.findall(qn('w:font'))  # type: ignore


class CT_DivBdr(OxmlBaseElement):
    @property
    def top(self) -> Optional[CT_Border]:
        return getattr(self, qn('w:top'), None)

    @property
    def left(self) -> Optional[CT_Border]:
        return getattr(self, qn('w:left'), None)

    @property
    def bottom(self) -> Optional[CT_Border]:
        return getattr(self, qn('w:bottom'), None)

    @property
    def right(self) -> Optional[CT_Border]:
        return getattr(self, qn('w:right'), None)


class CT_Div(OxmlBaseElement):
    @property
    def blockQuote(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:blockQuote'), None)

    @property
    def bodyDiv(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('w:bodyDiv'), None)

    @property
    def marLeft(self) -> Optional[CT_SignedTwipsMeasure]:
        return getattr(self, qn('w:marLeft'), None)

    @property
    def marRight(self) -> Optional[CT_SignedTwipsMeasure]:
        return getattr(self, qn('w:marRight'), None)

    @property
    def marTop(self) -> Optional[CT_SignedTwipsMeasure]:
        return getattr(self, qn('w:marTop'), None)

    @property
    def marBottom(self) -> Optional[CT_SignedTwipsMeasure]:
        return getattr(self, qn('w:marBottom'), None)

    @property
    def divBdr(self) -> Optional[CT_DivBdr]:
        return getattr(self, qn('w:divBdr'), None)

    @property
    def divsChild(self) -> list[CT_Divs]:
        return self.findall(qn('w:divsChild'))  # type: ignore

    @property
    def id(self) -> str:
        _val = self.attrib[qn('w:id')]

        return str(_val)


class CT_Divs(OxmlBaseElement):
    @property
    def div(self) -> list[CT_Div]:
        return self.findall(qn('w:div'))  # type: ignore


class CT_TxbxContent(OxmlBaseElement):
    """
    <xsd:complexType name="CT_TxbxContent">
        <xsd:group ref="EG_BlockLevelElts" minOccurs="1" maxOccurs="unbounded"/>
    </xsd:complexType>
    """

    @property
    def block_level_eles(
        self,
    ) -> list[
        CT_CustomXmlBlock | CT_SdtBlock | CT_P | CT_Tbl | CT_ProofErr | CT_PermStart | CT_Perm | CT_RunTrackChange | CT_AltChunk
    ]:
        return self.choice_and_more(*EG_BlockLevelElts.block_level_elts_choice_tags)  # type: ignore


class EG_BlockLevelChunkElts(OxmlBaseElement):
    """

    <xsd:group name="EG_BlockLevelChunkElts">
        <xsd:choice>
            <xsd:group ref="EG_ContentBlockContent" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:choice>
    </xsd:group>
    """

    # Union[CT_CustomXmlBlock, CT_SdtBlock, CT_P, CT_Tbl, CT_ProofErr, CT_PermStart, CT_Perm, CT_RunTrackChange]
    block_level_chunk_elts_choice_tags = EG_ContentBlockContent.content_block_tags


class CT_Body(OxmlBaseElement):
    """17.2.2 body (文档正文)

    该元素指定文档主体的内容 - 即主文档编辑级别。

    文档主体包含所谓的块级标记 - 可以作为WordprocessingML文档中段落的同级元素存在的标记。

    [示例：考虑一个主文档故事中只有一个段落的文档。该文档在其主文档部件中需要以下WordprocessingML：

    ```xml
    <w:document>
        <w:body>
            <w:p/>
        </w:body>
    </w:document>
    ```

    段落在body元素内部使其成为主文档故事的一部分。]
    """

    @property
    def block_level_elts(
        self,
    ) -> list[
        CT_CustomXmlBlock | CT_SdtBlock | CT_P | CT_Tbl | CT_ProofErr | CT_PermStart | CT_Perm | CT_RunTrackChange | CT_AltChunk
    ]:
        """块级别元素合集

        <xsd:group ref="EG_BlockLevelElts" minOccurs="0" maxOccurs="unbounded"/>
        """

        return self.choice_and_more(EG_BlockLevelElts.block_level_elts_choice_tags)  # type: ignore

    @property
    def sectPr(self) -> Optional[CT_SectPr]:
        """17.6.17 sectPr (文档最终节属性)

        该元素定义了文档的最后一节的节属性。[注意：对于任何其他节，属性都存储为与给定节的最后一段相对应的段落元素的子元素。结束注意]

        示例：考虑一个具有多个节的文档。对于除最后一节之外的所有节，sectPr元素都存储为该节中最后一个段落的子元素。对于最后一节，此信息存储为body元素的最后一个子元素，如下所示：

            ```xml
            <w:body>
                <w:p>
                    …
                </w:p>
                …
                <w:sectPr>
                    (最后一节的属性)
                </w:sectPr>
            </w:body>
            ```
        """
        return getattr(self, qn('w:sectPr'), None)


class CT_ShapeDefaults(OxmlBaseElement):
    """

    <xsd:complexType name="CT_ShapeDefaults">
        <xsd:choice maxOccurs="unbounded">
            <xsd:any processContents="lax" namespace="urn:schemas-microsoft-com:office:office"
                minOccurs="0" maxOccurs="unbounded"/>
        </xsd:choice>
    </xsd:complexType>
    """



class CT_Comments(OxmlBaseElement):
    @property
    def comment(self) -> list[CT_Comment]:
        return self.findall(qn('w:comment'))  # type: ignore


class CT_Footnotes(OxmlBaseElement):
    """

    <xsd:complexType name="CT_Footnotes">
        <xsd:sequence maxOccurs="unbounded">
            <xsd:element name="footnote" type="CT_FtnEdn" minOccurs="0"/>
        </xsd:sequence>
    </xsd:complexType>
    """

    @property
    def footnote(self) -> list[CT_FtnEdn]:
        return self.findall(qn('w:footnote'))  # type: ignore


class CT_Endnotes(OxmlBaseElement):
    """

    <xsd:complexType name="CT_Endnotes">
        <xsd:sequence maxOccurs="unbounded">
            <xsd:element name="endnote" type="CT_FtnEdn" minOccurs="0"/>
        </xsd:sequence>
    </xsd:complexType>
    """

    @property
    def endnote(self) -> list[CT_FtnEdn]:
        return self.findall(qn('w:endnote'))  # type: ignore


class CT_SmartTagType(OxmlBaseElement):
    @property
    def namespaceuri(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:namesapceuri'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def name(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:name'))

        if _val is not None:
            return str(_val)
        return None

    @property
    def url(self) -> Optional[str]:
        _val = self.attrib.get(qn('w:url'))

        if _val is not None:
            return str(_val)
        return None


class ST_ThemeColor(ST_BaseEnumType):
    dark1 = 'dark1'
    light1 = 'light1'
    dark2 = 'dark2'
    light2 = 'light2'
    accent1 = 'accent1'
    accent2 = 'accent2'
    accent3 = 'accent3'
    accent4 = 'accent4'
    accent5 = 'accent5'
    accent6 = 'accent6'
    hyperlink = 'hyperlink'
    followedHyperlink = 'followedHyperlink'
    none = 'none'
    background1 = 'background1'
    text1 = 'text1'
    background2 = 'background2'
    text2 = 'text2'


class ST_DocPartBehavior(ST_BaseEnumType):
    content = 'content'
    p = 'p'
    pg = 'pg'


class CT_DocPartBehavior(OxmlBaseElement):
    @property
    def val(self) -> ST_DocPartBehavior:
        return ST_DocPartBehavior(self.attrib[qn('w:val')])


class CT_DocPartBehaviors(OxmlBaseElement):
    @property
    def behavior(self) -> list[CT_DocPartBehavior]:
        return self.findall(qn('w:behavior'))  # type: ignore


class ST_DocPartType(ST_BaseEnumType):
    none = 'none'
    normal = 'normal'
    autoExp = 'autoExp'
    toolbar = 'toolbar'
    speller = 'speller'
    formFld = 'formFld'
    bbPlcHdr = 'bbPlcHdr'


class CT_DocPartType(OxmlBaseElement):
    @property
    def val_part_type(self) -> ST_DocPartType:
        """

        [有联合类型]
        """
        return ST_DocPartType(self.attrib[qn('w:val')])


class CT_DocPartTypes(OxmlBaseElement):
    @property
    def type(self) -> list[CT_DocPartType]:
        return self.findall(qn('w:type'))  # type: ignore

    @property
    def all(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:all'))

        if _val is not None:
            return s_ST_OnOff(str(_val))
        return None


class ST_DocPartGallery(ST_BaseEnumType):
    placeholder = 'placeholder'
    any = 'any'
    default = 'default'
    docParts = 'docParts'
    coverPg = 'coverPg'
    eq = 'eq'
    ftrs = 'ftrs'
    hdrs = 'hdrs'
    pgNum = 'pgNum'
    tbls = 'tbls'
    watermarks = 'watermarks'
    autoTxt = 'autoTxt'
    txtBox = 'txtBox'
    pgNumT = 'pgNumT'
    pgNumB = 'pgNumB'
    pgNumMargins = 'pgNumMargins'
    tblOfContents = 'tblOfContents'
    bib = 'bib'
    custQuickParts = 'custQuickParts'
    custCoverPg = 'custCoverPg'
    custEq = 'custEq'
    custFtrs = 'custFtrs'
    custHdrs = 'custHdrs'
    custPgNum = 'custPgNum'
    custTbls = 'custTbls'
    custWatermarks = 'custWatermarks'
    custAutoTxt = 'custAutoTxt'
    custTxtBox = 'custTxtBox'
    custPgNumT = 'custPgNumT'
    custPgNumB = 'custPgNumB'
    custPgNumMargins = 'custPgNumMargins'
    custTblOfContents = 'custTblOfContents'
    custBib = 'custBib'
    custom1 = 'custom1'
    custom2 = 'custom2'
    custom3 = 'custom3'
    custom4 = 'custom4'
    custom5 = 'custom5'


class CT_DocPartGallery(OxmlBaseElement):
    @property
    def val(self) -> ST_DocPartGallery:
        return ST_DocPartGallery(self.attrib[qn('w:val')])


class CT_DocPartCategory(OxmlBaseElement):
    @property
    def name(self) -> CT_String:
        return getattr(self, qn('w:name'))

    @property
    def gallery(self) -> CT_DocPartGallery:
        return getattr(self, qn('w:gallery'))


class CT_DocPartName(OxmlBaseElement):
    @property
    def val(self) -> str:
        return str(self.attrib[qn('w:val')])

    @property
    def decorated(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:decorated'))

        if _val is not None:
            return s_ST_OnOff(str(_val))
        return None


class CT_DocPartPr(OxmlBaseElement):
    @property
    def name(self) -> CT_DocPartName:
        return getattr(self, qn('w:name'))

    @property
    def style(self) -> Optional[CT_String]:
        return getattr(self, qn('w:style'), None)

    @property
    def category(self) -> Optional[CT_DocPartCategory]:
        return getattr(self, qn('w:category'), None)

    @property
    def types(self) -> Optional[CT_DocPartTypes]:
        return getattr(self, qn('w:types'), None)

    @property
    def behaviors(self) -> Optional[CT_DocPartBehaviors]:
        return getattr(self, qn('w:behaviors'), None)

    @property
    def description(self) -> Optional[CT_String]:
        return getattr(self, qn('w:description'), None)

    @property
    def guid(self) -> Optional[CT_Guid]:
        return getattr(self, qn('w:guid'), None)


class CT_DocPart(OxmlBaseElement):
    @property
    def docPartPr(self) -> Optional[CT_DocPartPr]:
        return getattr(self, qn('w:docPartPr'), None)

    @property
    def docPartBody(self) -> Optional[CT_Body]:
        return getattr(self, qn('w:docPartBody'), None)


class CT_DocParts(OxmlBaseElement):
    @property
    def docPart(self) -> list[CT_DocPart]:
        return self.findall(qn('w:docPart'))  # type: ignore


class ST_CaptionPos(ST_BaseEnumType):
    above = 'above'
    below = 'below'
    left = 'left'
    right = 'right'


class CT_Caption(OxmlBaseElement):
    @property
    def name(self) -> str:
        return str(self.attrib[qn('w:name')])

    @property
    def pos(self) -> Optional[ST_CaptionPos]:
        _val = self.attrib.get(qn('w:pos'))

        if _val is not None:
            return ST_CaptionPos(str(_val))
        return None

    @property
    def chapNum(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:chapNum'))

        if _val is not None:
            return s_ST_OnOff(str(_val))
        return None

    @property
    def heading(self) -> Optional[ST_DecimalNumber]:
        _val = self.attrib.get(qn('w:heading'))

        if _val is not None:
            return ST_DecimalNumber(str(_val))
        return None

    @property
    def noLabel(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get(qn('w:noLabel'))

        if _val is not None:
            return s_ST_OnOff(str(_val))
        return None

    @property
    def numFmt(self) -> Optional[ST_DecimalNumber]:
        _val = self.attrib.get(qn('w:numFmt'))

        if _val is not None:
            return ST_DecimalNumber(str(_val))
        return None

    @property
    def sep(self) -> Optional[ST_ChapterSep]:
        _val = self.attrib.get(qn('w:sep'))

        if _val is not None:
            return ST_ChapterSep(str(_val))
        return None


class CT_AutoCaption(OxmlBaseElement):
    @property
    def name(self) -> str:
        return str(self.attrib[qn('w:name')])

    @property
    def caption(self) -> str:
        return str(self.attrib[qn('w:caption')])


class CT_AutoCaptions(OxmlBaseElement):
    @property
    def autoCaption(self) -> list[CT_AutoCaption]:
        return self.findall(qn('w:autoCaption'))  # type: ignore


class CT_Captions(OxmlBaseElement):
    @property
    def caption(self) -> list[CT_Caption]:
        return self.findall(qn('w:caption'))  # type: ignore

    @property
    def autoCaptions(self) -> Optional[CT_AutoCaptions]:
        return getattr(self, qn('w:autoCaptions'), None)


class CT_DocumentBase(OxmlBaseElement):
    @property
    def background(self) -> Optional[CT_Background]:
        """17.2.1 background (文档背景)

        此元素指定包含背景元素的文档的每个页面的背景。文档的背景是整个页面表面的图像或填充，位于所有其他文档内容之后。

        背景元素的绘图 §17.3.3.9 子元素允许将任何DrawingML效果应用于文档的背景。

        然而，对于纯色填充背景，此元素上的属性允许使用任何RGB或主题颜色值（后者是对文档主题部分的引用）。
        """

        return getattr(self, qn('w:background'), None)


class CT_Document(CT_DocumentBase):
    """17.2.3 document (文档)

    该元素指定WordprocessingML文档中主文档部分的内容。
    """

    @property
    def body(self) -> Optional[CT_Body]:
        """17.2.2 body (文档正文)

        该元素指定文档主体的内容 - 即主文档编辑级别。

        文档主体包含所谓的块级标记 - 可以作为WordprocessingML文档中段落的同级元素存在的标记。

        [示例：考虑一个主文档故事中只有一个段落的文档。该文档在其主文档部件中需要以下WordprocessingML：

        ```xml
        <w:document>
            <w:body>
                <w:p/>
            </w:body>
        </w:document>
        ```

        段落在body元素内部使其成为主文档故事的一部分。]

        """
        return getattr(self, qn('w:body'), None)

    @property
    def conformance(self) -> s_ST_ConformanceClass:
        """conformance（文档符合类别）

        指定WordprocessingML文档符合的符合类别（§2.1）。

        如果省略此属性，则其默认值为transitional。
        """
        _val = self.attrib.get(qn('w:conformance'))

        if _val is not None:
            return s_ST_ConformanceClass(_val)

        return s_ST_ConformanceClass.Transitional


class CT_GlossaryDocument(CT_DocumentBase):
    @property
    def docParts(self) -> Optional[CT_DocParts]:
        return getattr(self, qn('w:docParts'), None)


wml_main_namespace = lookup.get_namespace(NameSpace_w)
wml_main_namespace[None] = OxmlBaseElement

wml_main_namespace['glossaryDocument'] = CT_GlossaryDocument
wml_main_namespace['document'] = CT_Document
wml_main_namespace['docParts'] = CT_DocParts
wml_main_namespace['body'] = CT_Body
wml_main_namespace['background'] = CT_Background
wml_main_namespace['caption'] = CT_Caption
wml_main_namespace['autoCaptions'] = CT_AutoCaptions
wml_main_namespace['autoCaption'] = CT_AutoCaption
wml_main_namespace['docPartPr'] = CT_DocPartPr
wml_main_namespace['docPartBody'] = CT_Body
wml_main_namespace['category'] = CT_DocPartCategory
wml_main_namespace['types'] = CT_DocPartTypes
wml_main_namespace['behaviors'] = CT_DocPartBehaviors
wml_main_namespace['description'] = CT_String
wml_main_namespace['guid'] = CT_Guid
wml_main_namespace['gallery'] = CT_DocPartGallery
wml_main_namespace['behavior'] = CT_DocPartBehavior
wml_main_namespace['webSettings'] = CT_WebSettings
wml_main_namespace['numbering'] = CT_Numbering
wml_main_namespace['footnotes'] = CT_Footnotes
wml_main_namespace['settings'] = CT_Settings
wml_main_namespace['comments'] = CT_Comments
wml_main_namespace['endnotes'] = CT_Endnotes
wml_main_namespace['fonts'] = CT_FontsList
wml_main_namespace['styles'] = CT_Styles
wml_main_namespace['hdr'] = CT_HdrFtr
wml_main_namespace['ftr'] = CT_HdrFtr
wml_main_namespace['div'] = CT_Div
wml_main_namespace['comment'] = CT_Comment
wml_main_namespace['altChunk'] = CT_AltChunk
wml_main_namespace['proofErr'] = CT_ProofErr
wml_main_namespace['permStart'] = CT_PermStart
wml_main_namespace['permEnd'] = CT_Perm
wml_main_namespace['blockQuote'] = CT_OnOff
wml_main_namespace['marBottom'] = CT_SignedTwipsMeasure
wml_main_namespace['divBdr'] = CT_DivBdr
wml_main_namespace['bodyDiv'] = CT_OnOff
wml_main_namespace['marRight'] = CT_SignedTwipsMeasure
wml_main_namespace['marLeft'] = CT_SignedTwipsMeasure
wml_main_namespace['marTop'] = CT_SignedTwipsMeasure
wml_main_namespace['txbxContent'] = CT_TxbxContent
wml_main_namespace['divsChild'] = CT_Divs
wml_main_namespace['font'] = CT_Font
wml_main_namespace['altName'] = CT_String
wml_main_namespace['panose1'] = CT_Panose
wml_main_namespace['charset'] = CT_Charset
wml_main_namespace['family'] = CT_FontFamily
wml_main_namespace['notTrueType'] = CT_OnOff
wml_main_namespace['docDefaults'] = CT_DocDefaults
wml_main_namespace['pitch'] = CT_Pitch
wml_main_namespace['sig'] = CT_FontSig
wml_main_namespace['embedRegular'] = CT_FontRel
wml_main_namespace['embedBold'] = CT_FontRel
wml_main_namespace['embedItalic'] = CT_FontRel
wml_main_namespace['embedBoldItalic'] = CT_FontRel
wml_main_namespace['latentStyles'] = CT_LatentStyles
wml_main_namespace['lsdException'] = CT_LsdException
wml_main_namespace['uiPriority'] = CT_DecimalNumber
wml_main_namespace['unhideWhenUsed'] = CT_OnOff
wml_main_namespace['autoRedefine'] = CT_OnOff
wml_main_namespace['semiHidden'] = CT_OnOff
wml_main_namespace['aliases'] = CT_String
wml_main_namespace['basedOn'] = CT_String
wml_main_namespace['next'] = CT_String
wml_main_namespace['link'] = CT_String
wml_main_namespace['hidden'] = CT_OnOff
wml_main_namespace['qFormat'] = CT_OnOff
wml_main_namespace['locked'] = CT_OnOff
wml_main_namespace['personal'] = CT_OnOff
wml_main_namespace['personalCompose'] = CT_OnOff
wml_main_namespace['personalReply'] = CT_OnOff
wml_main_namespace['rsid'] = CT_LongHexNumber
wml_main_namespace['tblStylePr'] = CT_TblStylePr
wml_main_namespace['numPicBullet'] = CT_NumPicBullet
wml_main_namespace['abstractNum'] = CT_AbstractNum
wml_main_namespace['num'] = CT_Num
wml_main_namespace['numIdMacAtCleanup'] = CT_DecimalNumber
wml_main_namespace['abstractNumId'] = CT_DecimalNumber
wml_main_namespace['lvlOverride'] = CT_NumLvl
wml_main_namespace['startOverride'] = CT_DecimalNumber
wml_main_namespace['lvl'] = CT_Lvl
wml_main_namespace['nsid'] = CT_LongHexNumber
wml_main_namespace['multiLevelType'] = CT_MultiLevelType
wml_main_namespace['tmpl'] = CT_LongHexNumber
wml_main_namespace['styleLink'] = CT_String
wml_main_namespace['numStyleLink'] = CT_String
wml_main_namespace['numFmt'] = CT_NumFmt
wml_main_namespace['lvlRestart'] = CT_DecimalNumber
wml_main_namespace['isLgl'] = CT_OnOff
wml_main_namespace['suff'] = CT_LevelSuffix
wml_main_namespace['lvlText'] = CT_LevelText
wml_main_namespace['lvlPicBulletId'] = CT_DecimalNumber
wml_main_namespace['legacy'] = CT_LvlLegacy
wml_main_namespace['lvlJc'] = CT_Jc
wml_main_namespace['pict'] = CT_Picture
wml_main_namespace['drawing'] = CT_Drawing
wml_main_namespace['framesetSplitbar'] = CT_FramesetSplitbar
wml_main_namespace['frameLayout'] = CT_FrameLayout
wml_main_namespace['title'] = CT_String
wml_main_namespace['frameset'] = CT_Frameset
wml_main_namespace['frame'] = CT_Frame
wml_main_namespace['color'] = CT_Color
wml_main_namespace['noBorder'] = CT_OnOff
wml_main_namespace['flatBorders'] = CT_OnOff
wml_main_namespace['longDesc'] = CT_Rel
wml_main_namespace['sourceFileName'] = CT_Rel
wml_main_namespace['marW'] = CT_PixelsMeasure
wml_main_namespace['marH'] = CT_PixelsMeasure
wml_main_namespace['scrollbar'] = CT_FrameScrollbar
wml_main_namespace['noResizeAllowed'] = CT_OnOff
wml_main_namespace['linkedToFile'] = CT_OnOff
wml_main_namespace['divs'] = CT_Divs
wml_main_namespace['encoding'] = CT_String
wml_main_namespace['optimizeForBrowser'] = CT_OptimizeForBrowser
wml_main_namespace['relyOnVML'] = CT_OnOff
wml_main_namespace['allowPNG'] = CT_OnOff
wml_main_namespace['doNotRelyOnCSS'] = CT_OnOff
wml_main_namespace['doNotSaveAsSingleFile'] = CT_OnOff
wml_main_namespace['doNotOrganizeInFolder'] = CT_OnOff
wml_main_namespace['doNotUseLongFileNames'] = CT_OnOff
wml_main_namespace['pixelsPerInch'] = CT_DecimalNumber
wml_main_namespace['targetScreenSz'] = CT_TargetScreenSz
wml_main_namespace['saveSmartTagsAsXml'] = CT_OnOff
wml_main_namespace['writeProtection'] = CT_WriteProtection
wml_main_namespace['view'] = CT_View
wml_main_namespace['zoom'] = CT_Zoom
wml_main_namespace['removePersonalInformation'] = CT_OnOff
wml_main_namespace['removeDateAndTime'] = CT_OnOff
wml_main_namespace['doNotDisplayPageBoundaries'] = CT_OnOff
wml_main_namespace['displayBackgroundShape'] = CT_OnOff
wml_main_namespace['printPostScriptOverText'] = CT_OnOff
wml_main_namespace['printFractionalCharacterWidth'] = CT_OnOff
wml_main_namespace['printFormsData'] = CT_OnOff
wml_main_namespace['embedTrueTypeFonts'] = CT_OnOff
wml_main_namespace['embedSystemFonts'] = CT_OnOff
wml_main_namespace['saveSubsetFonts'] = CT_OnOff
wml_main_namespace['saveFormsData'] = CT_OnOff
wml_main_namespace['mirrorMargins'] = CT_OnOff
wml_main_namespace['alignBordersAndEdges'] = CT_OnOff
wml_main_namespace['bordersDoNotSurroundHeader'] = CT_OnOff
wml_main_namespace['bordersDoNotSurroundFooter'] = CT_OnOff
wml_main_namespace['gutterAtTop'] = CT_OnOff
wml_main_namespace['hideSpellingErrors'] = CT_OnOff
wml_main_namespace['hideGrammaticalErrors'] = CT_OnOff
wml_main_namespace['activeWritingStyle'] = CT_WritingStyle
wml_main_namespace['proofState'] = CT_Proof
wml_main_namespace['formsDesign'] = CT_OnOff
wml_main_namespace['attachedTemplate'] = CT_Rel
wml_main_namespace['linkStyles'] = CT_OnOff
wml_main_namespace['stylePaneFormatFilter'] = CT_StylePaneFilter
wml_main_namespace['stylePaneSortMethod'] = CT_StyleSort
wml_main_namespace['documentType'] = CT_DocType
wml_main_namespace['mailMerge'] = CT_MailMerge
wml_main_namespace['revisionView'] = CT_TrackChangesView
wml_main_namespace['trackRevisions'] = CT_OnOff
wml_main_namespace['doNotTrackMoves'] = CT_OnOff
wml_main_namespace['doNotTrackFormatting'] = CT_OnOff
wml_main_namespace['documentProtection'] = CT_DocProtect
wml_main_namespace['autoFormatOverride'] = CT_OnOff
wml_main_namespace['styleLockTheme'] = CT_OnOff
wml_main_namespace['styleLockQFSet'] = CT_OnOff
wml_main_namespace['defaultTabStop'] = CT_TwipsMeasure
wml_main_namespace['autoHyphenation'] = CT_OnOff
wml_main_namespace['consecutiveHyphenLimit'] = CT_DecimalNumber
wml_main_namespace['hyphenationZone'] = CT_TwipsMeasure
wml_main_namespace['doNotHyphenateCaps'] = CT_OnOff
wml_main_namespace['showEnvelope'] = CT_OnOff
wml_main_namespace['summaryLength'] = CT_DecimalNumberOrPrecent
wml_main_namespace['clickAndTypeStyle'] = CT_String
wml_main_namespace['defaultTableStyle'] = CT_String
wml_main_namespace['evenAndOddHeaders'] = CT_OnOff
wml_main_namespace['bookFoldRevPrinting'] = CT_OnOff
wml_main_namespace['bookFoldPrinting'] = CT_OnOff
wml_main_namespace['bookFoldPrintingSheets'] = CT_DecimalNumber
wml_main_namespace['drawingGridHorizontalSpacing'] = CT_TwipsMeasure
wml_main_namespace['drawingGridVerticalSpacing'] = CT_TwipsMeasure
wml_main_namespace['displayHorizontalDrawingGridEvery'] = CT_DecimalNumber
wml_main_namespace['displayVerticalDrawingGridEvery'] = CT_DecimalNumber
wml_main_namespace['doNotUseMarginsForDrawingGridOrigin'] = CT_OnOff
wml_main_namespace['drawingGridHorizontalOrigin'] = CT_TwipsMeasure
wml_main_namespace['drawingGridVerticalOrigin'] = CT_TwipsMeasure
wml_main_namespace['doNotShadeFormData'] = CT_OnOff
wml_main_namespace['noPunctuationKerning'] = CT_OnOff
wml_main_namespace['characterSpacingControl'] = CT_CharacterSpacing
wml_main_namespace['printTwoOnOne'] = CT_OnOff
wml_main_namespace['strictFirstAndLastChars'] = CT_OnOff
wml_main_namespace['noLineBreaksAfter'] = CT_Kinsoku
wml_main_namespace['noLineBreaksBefore'] = CT_Kinsoku
wml_main_namespace['savePreviewPicture'] = CT_OnOff
wml_main_namespace['doNotValidateAgainstSchema'] = CT_OnOff
wml_main_namespace['saveInvalidXml'] = CT_OnOff
wml_main_namespace['ignoreMixedContent'] = CT_OnOff
wml_main_namespace['alwaysShowPlaceholderText'] = CT_OnOff
wml_main_namespace['doNotDemarcateInvalidXml'] = CT_OnOff
wml_main_namespace['saveXmlDataOnly'] = CT_OnOff
wml_main_namespace['useXSLTWhenSaving'] = CT_OnOff
wml_main_namespace['saveThroughXslt'] = CT_SaveThroughXslt
wml_main_namespace['showXMLTags'] = CT_OnOff
wml_main_namespace['alwaysMergeEmptyNamespace'] = CT_OnOff
wml_main_namespace['updateFields'] = CT_OnOff
wml_main_namespace['hdrShapeDefaults'] = CT_ShapeDefaults
wml_main_namespace['compat'] = CT_Compat
wml_main_namespace['docVars'] = CT_DocVars
wml_main_namespace['rsids'] = CT_DocRsids
wml_main_namespace['attachedSchema'] = CT_String
wml_main_namespace['themeFontLang'] = CT_Language
wml_main_namespace['clrSchemeMapping'] = CT_ColorSchemeMapping
wml_main_namespace['doNotIncludeSubdocsInStats'] = CT_OnOff
wml_main_namespace['doNotAutoCompressPictures'] = CT_OnOff
wml_main_namespace['forceUpgrade'] = CT_Empty
wml_main_namespace['captions'] = CT_Captions
wml_main_namespace['readModeInkLockDown'] = CT_ReadingModeInkLockDown
wml_main_namespace['smartTagType'] = CT_SmartTagType
wml_main_namespace['shapeDefaults'] = CT_ShapeDefaults
wml_main_namespace['doNotEmbedSmartTags'] = CT_OnOff
wml_main_namespace['decimalSymbol'] = CT_String
wml_main_namespace['listSeparator'] = CT_String
wml_main_namespace['rPrDefault'] = CT_RPrDefault
wml_main_namespace['pPrDefault'] = CT_PPrDefault
wml_main_namespace['rsidRoot'] = CT_LongHexNumber
wml_main_namespace['docVar'] = CT_DocVar
wml_main_namespace['useSingleBorderforContiguousCells'] = CT_OnOff
wml_main_namespace['wpJustification'] = CT_OnOff
wml_main_namespace['noTabHangInd'] = CT_OnOff
wml_main_namespace['noLeading'] = CT_OnOff
wml_main_namespace['spaceForUL'] = CT_OnOff
wml_main_namespace['noColumnBalance'] = CT_OnOff
wml_main_namespace['balanceSingleByteDoubleByteWidth'] = CT_OnOff
wml_main_namespace['noExtraLineSpacing'] = CT_OnOff
wml_main_namespace['doNotLeaveBackslashAlone'] = CT_OnOff
wml_main_namespace['ulTrailSpace'] = CT_OnOff
wml_main_namespace['doNotExpandShiftReturn'] = CT_OnOff
wml_main_namespace['spacingInWholePoints'] = CT_OnOff
wml_main_namespace['lineWrapLikeWord6'] = CT_OnOff
wml_main_namespace['printBodyTextBeforeHeader'] = CT_OnOff
wml_main_namespace['printColBlack'] = CT_OnOff
wml_main_namespace['wpSpaceWidth'] = CT_OnOff
wml_main_namespace['showBreaksInFrames'] = CT_OnOff
wml_main_namespace['subFontBySize'] = CT_OnOff
wml_main_namespace['suppressBottomSpacing'] = CT_OnOff
wml_main_namespace['suppressTopSpacing'] = CT_OnOff
wml_main_namespace['suppressSpacingAtTopOfPage'] = CT_OnOff
wml_main_namespace['suppressTopSpacingWP'] = CT_OnOff
wml_main_namespace['suppressSpBfAfterPgBrk'] = CT_OnOff
wml_main_namespace['swapBordersFacingPages'] = CT_OnOff
wml_main_namespace['convMailMergeEsc'] = CT_OnOff
wml_main_namespace['truncateFontHeightsLikeWP6'] = CT_OnOff
wml_main_namespace['mwSmallCaps'] = CT_OnOff
wml_main_namespace['usePrinterMetrics'] = CT_OnOff
wml_main_namespace['doNotSuppressParagraphBorders'] = CT_OnOff
wml_main_namespace['wrapTrailSpaces'] = CT_OnOff
wml_main_namespace['footnoteLayoutLikeWW8'] = CT_OnOff
wml_main_namespace['shapeLayoutLikeWW8'] = CT_OnOff
wml_main_namespace['alignTablesRowByRow'] = CT_OnOff
wml_main_namespace['forgetLastTabAlignment'] = CT_OnOff
wml_main_namespace['adjustLineHeightInTable'] = CT_OnOff
wml_main_namespace['autoSpaceLikeWord95'] = CT_OnOff
wml_main_namespace['noSpaceRaiseLower'] = CT_OnOff
wml_main_namespace['doNotUseHTMLParagraphAutoSpacing'] = CT_OnOff
wml_main_namespace['layoutRawTableWidth'] = CT_OnOff
wml_main_namespace['layoutTableRowsApart'] = CT_OnOff
wml_main_namespace['useWord97LineBreakRules'] = CT_OnOff
wml_main_namespace['doNotBreakWrappedTables'] = CT_OnOff
wml_main_namespace['doNotSnapToGridInCell'] = CT_OnOff
wml_main_namespace['selectFldWithFirstOrLastChar'] = CT_OnOff
wml_main_namespace['applyBreakingRules'] = CT_OnOff
wml_main_namespace['doNotWrapTextWithPunct'] = CT_OnOff
wml_main_namespace['doNotUseEastAsianBreakRules'] = CT_OnOff
wml_main_namespace['useWord2002TableStyleRules'] = CT_OnOff
wml_main_namespace['growAutofit'] = CT_OnOff
wml_main_namespace['useFELayout'] = CT_OnOff
wml_main_namespace['useNormalStyleForList'] = CT_OnOff
wml_main_namespace['doNotUseIndentAsNumberingTabStop'] = CT_OnOff
wml_main_namespace['useAltKinsokuLineBreakRules'] = CT_OnOff
wml_main_namespace['allowSpaceOfSameStyleInTable'] = CT_OnOff
wml_main_namespace['doNotSuppressIndentation'] = CT_OnOff
wml_main_namespace['doNotAutofitConstrainedTables'] = CT_OnOff
wml_main_namespace['autofitToFirstFixedWidthCell'] = CT_OnOff
wml_main_namespace['underlineTabInNumList'] = CT_OnOff
wml_main_namespace['displayHangulFixedWidth'] = CT_OnOff
wml_main_namespace['splitPgBreakAndParaMark'] = CT_OnOff
wml_main_namespace['doNotVertAlignCellWithSp'] = CT_OnOff
wml_main_namespace['doNotBreakConstrainedForcedTable'] = CT_OnOff
wml_main_namespace['doNotVertAlignInTxbx'] = CT_OnOff
wml_main_namespace['useAnsiKerningPairs'] = CT_OnOff
wml_main_namespace['cachedColBalance'] = CT_OnOff
wml_main_namespace['compatSetting'] = CT_CompatSetting
wml_main_namespace['mainDocumentType'] = CT_MailMergeDocType
wml_main_namespace['linkToQuery'] = CT_OnOff
wml_main_namespace['dataType'] = CT_MailMergeDataType
wml_main_namespace['connectString'] = CT_String
wml_main_namespace['query'] = CT_String
wml_main_namespace['dataSource'] = CT_Rel
wml_main_namespace['headerSource'] = CT_Rel
wml_main_namespace['doNotSuppressBlankLines'] = CT_OnOff
wml_main_namespace['destination'] = CT_MailMergeDest
wml_main_namespace['addressFieldName'] = CT_String
wml_main_namespace['mailSubject'] = CT_String
wml_main_namespace['mailAsAttachment'] = CT_OnOff
wml_main_namespace['viewMergedData'] = CT_OnOff
wml_main_namespace['activeRecord'] = CT_DecimalNumber
wml_main_namespace['checkErrors'] = CT_DecimalNumber
wml_main_namespace['odso'] = CT_Odso
wml_main_namespace['udl'] = CT_String
wml_main_namespace['table'] = CT_String
wml_main_namespace['src'] = CT_Rel
wml_main_namespace['colDelim'] = CT_DecimalNumber
wml_main_namespace['fHdr'] = CT_OnOff
wml_main_namespace['fieldMapData'] = CT_OdsoFieldMapData
wml_main_namespace['mappedName'] = CT_String
wml_main_namespace['column'] = CT_DecimalNumber
wml_main_namespace['lid'] = CT_Lang
wml_main_namespace['dynamicAddress'] = CT_OnOff
wml_main_namespace['recipients'] = CT_Recipients
wml_main_namespace['active'] = CT_OnOff
wml_main_namespace['uniqueTag'] = CT_Base64Binary
wml_main_namespace['numStart'] = CT_DecimalNumber
wml_main_namespace['numRestart'] = CT_NumRestart
wml_main_namespace['tblPrExChange'] = CT_TblPrExChange
wml_main_namespace['tblW'] = CT_TblWidth
wml_main_namespace['tblCellSpacing'] = CT_TblWidth
wml_main_namespace['tblInd'] = CT_TblWidth
wml_main_namespace['tblBorders'] = CT_TblBorders
wml_main_namespace['tblLayout'] = CT_TblLayoutType
wml_main_namespace['tblCellMar'] = CT_TblCellMar
wml_main_namespace['tblLook'] = CT_TblLook
wml_main_namespace['tblPrChange'] = CT_TblPrChange
wml_main_namespace['tblStyle'] = CT_String
wml_main_namespace['tblpPr'] = CT_TblPPr
wml_main_namespace['tblOverlap'] = CT_TblOverlap
wml_main_namespace['bidiVisual'] = CT_OnOff
wml_main_namespace['tblStyleRowBandSize'] = CT_DecimalNumber
wml_main_namespace['tblStyleColBandSize'] = CT_DecimalNumber
wml_main_namespace['tblCaption'] = CT_String
wml_main_namespace['tblDescription'] = CT_String
wml_main_namespace['insideH'] = CT_Border
wml_main_namespace['insideV'] = CT_Border
wml_main_namespace['trPrChange'] = CT_TrPrChange
wml_main_namespace['cnfStyle'] = CT_Cnf
wml_main_namespace['divId'] = CT_DecimalNumber
wml_main_namespace['gridBefore'] = CT_DecimalNumber
wml_main_namespace['gridAfter'] = CT_DecimalNumber
wml_main_namespace['wBefore'] = CT_TblWidth
wml_main_namespace['wAfter'] = CT_TblWidth
wml_main_namespace['cantSplit'] = CT_OnOff
wml_main_namespace['trHeight'] = CT_Height
wml_main_namespace['tblHeader'] = CT_OnOff
wml_main_namespace['header'] = CT_String
wml_main_namespace['tcPrChange'] = CT_TcPrChange
wml_main_namespace['tcW'] = CT_TblWidth
wml_main_namespace['gridSpan'] = CT_DecimalNumber
wml_main_namespace['hMerge'] = CT_HMerge
wml_main_namespace['vMerge'] = CT_VMerge
wml_main_namespace['tcBorders'] = CT_TcBorders
wml_main_namespace['shd'] = CT_Shd
wml_main_namespace['noWrap'] = CT_OnOff
wml_main_namespace['tcMar'] = CT_TcMar
wml_main_namespace['textDirection'] = CT_TextDirection
wml_main_namespace['tcFitText'] = CT_OnOff
wml_main_namespace['vAlign'] = CT_VerticalJc
wml_main_namespace['hideMark'] = CT_OnOff
wml_main_namespace['headers'] = CT_Headers
wml_main_namespace['tl2br'] = CT_Border
wml_main_namespace['tr2bl'] = CT_Border
wml_main_namespace['tblGridChange'] = CT_TblGridChange
wml_main_namespace['gridCol'] = CT_TblGridCol
wml_main_namespace['fldSimple'] = CT_SimpleField
wml_main_namespace['hyperlink'] = CT_Hyperlink
wml_main_namespace['subDoc'] = CT_Rel
wml_main_namespace['attr'] = CT_Attr
wml_main_namespace['customXmlPr'] = CT_CustomXmlPr
wml_main_namespace['smartTagPr'] = CT_SmartTagPr
wml_main_namespace['sdtPr'] = CT_SdtPr
wml_main_namespace['sdtEndPr'] = CT_SdtEndPr
wml_main_namespace['tc'] = CT_Tc
wml_main_namespace['tr'] = CT_Row
wml_main_namespace['p'] = CT_P
wml_main_namespace['tbl'] = CT_Tbl
wml_main_namespace['smartTag'] = CT_SmartTagRun
wml_main_namespace['dir'] = CT_DirContentRun
wml_main_namespace['bdo'] = CT_BdoContentRun
wml_main_namespace['r'] = CT_R
wml_main_namespace['equation'] = CT_Empty
wml_main_namespace['comboBox'] = CT_SdtComboBox
wml_main_namespace['date'] = CT_SdtDate
wml_main_namespace['docPartObj'] = CT_SdtDocPart
wml_main_namespace['docPartList'] = CT_SdtDocPart
wml_main_namespace['dropDownList'] = CT_SdtDropDownList
wml_main_namespace['picture'] = CT_Empty
wml_main_namespace['richText'] = CT_Empty
wml_main_namespace['text'] = CT_SdtText
wml_main_namespace['citation'] = CT_Empty
wml_main_namespace['group'] = CT_Empty
wml_main_namespace['bibliography'] = CT_Empty
wml_main_namespace['alias'] = CT_String
wml_main_namespace['tag'] = CT_String
wml_main_namespace['id'] = CT_DecimalNumber
wml_main_namespace['lock'] = CT_Lock
wml_main_namespace['temporary'] = CT_OnOff
wml_main_namespace['showingPlcHdr'] = CT_OnOff
wml_main_namespace['dataBinding'] = CT_DataBinding
wml_main_namespace['label'] = CT_DecimalNumber
wml_main_namespace['tabIndex'] = CT_UnsignedDecimalNumber
wml_main_namespace['listItem'] = CT_SdtListItem
wml_main_namespace['docPartGallery'] = CT_String
wml_main_namespace['docPartCategory'] = CT_String
wml_main_namespace['docPartUnique'] = CT_OnOff
wml_main_namespace['dateFormat'] = CT_String
wml_main_namespace['storeMappedDataAs'] = CT_SdtDateMappingType
wml_main_namespace['calendar'] = CT_CalendarType
wml_main_namespace['rubyPr'] = CT_RubyPr
wml_main_namespace['rt'] = CT_RubyContent
wml_main_namespace['rubyBase'] = CT_RubyContent
wml_main_namespace['rubyAlign'] = CT_RubyAlign
wml_main_namespace['hps'] = CT_HpsMeasure
wml_main_namespace['hpsRaise'] = CT_HpsMeasure
wml_main_namespace['hpsBaseText'] = CT_HpsMeasure
wml_main_namespace['dirty'] = CT_OnOff
wml_main_namespace['matchSrc'] = CT_OnOff
wml_main_namespace['altChunkPr'] = CT_AltChunkPr
wml_main_namespace['rStyle'] = CT_String
wml_main_namespace['rFonts'] = CT_Fonts
wml_main_namespace['b'] = CT_OnOff
wml_main_namespace['bCs'] = CT_OnOff
wml_main_namespace['i'] = CT_OnOff
wml_main_namespace['iCs'] = CT_OnOff
wml_main_namespace['caps'] = CT_OnOff
wml_main_namespace['smallCaps'] = CT_OnOff
wml_main_namespace['strike'] = CT_OnOff
wml_main_namespace['dstrike'] = CT_OnOff
wml_main_namespace['outline'] = CT_OnOff
wml_main_namespace['shadow'] = CT_OnOff
wml_main_namespace['emboss'] = CT_OnOff
wml_main_namespace['imprint'] = CT_OnOff
wml_main_namespace['noProof'] = CT_OnOff
wml_main_namespace['snapToGrid'] = CT_OnOff
wml_main_namespace['vanish'] = CT_OnOff
wml_main_namespace['webHidden'] = CT_OnOff
wml_main_namespace['color'] = CT_Color
wml_main_namespace['kern'] = CT_HpsMeasure
wml_main_namespace['position'] = CT_SignedHpsMeasure
wml_main_namespace['szCs'] = CT_HpsMeasure
wml_main_namespace['highlight'] = CT_Highlight
wml_main_namespace['u'] = CT_Underline
wml_main_namespace['effect'] = CT_TextEffect
wml_main_namespace['bdr'] = CT_Border
wml_main_namespace['fitText'] = CT_FitText
wml_main_namespace['vertAlign'] = CT_VerticalAlignRun
wml_main_namespace['rtl'] = CT_OnOff
wml_main_namespace['cs'] = CT_OnOff
wml_main_namespace['em'] = CT_Em
wml_main_namespace['lang'] = CT_Language
wml_main_namespace['eastAsianLayout'] = CT_EastAsianLayout
wml_main_namespace['specVanish'] = CT_OnOff
wml_main_namespace['oMath'] = CT_OnOff
wml_main_namespace['br'] = CT_Br
wml_main_namespace['t'] = CT_Text
wml_main_namespace['contentPart'] = CT_Rel
wml_main_namespace['delText'] = CT_Text
wml_main_namespace['instrText'] = CT_Text
wml_main_namespace['delInstrText'] = CT_Text
wml_main_namespace['noBreakHyphen'] = CT_Empty
wml_main_namespace['softHyphen'] = CT_Empty
wml_main_namespace['dayShort'] = CT_Empty
wml_main_namespace['monthShort'] = CT_Empty
wml_main_namespace['yearShort'] = CT_Empty
wml_main_namespace['dayLong'] = CT_Empty
wml_main_namespace['monthLong'] = CT_Empty
wml_main_namespace['yearLong'] = CT_Empty
wml_main_namespace['annotationRef'] = CT_Empty
wml_main_namespace['footnoteRef'] = CT_Empty
wml_main_namespace['endnoteRef'] = CT_Empty
wml_main_namespace['separator'] = CT_Empty
wml_main_namespace['continuationSeparator'] = CT_Empty
wml_main_namespace['sym'] = CT_Sym
wml_main_namespace['pgNum'] = CT_Empty
wml_main_namespace['cr'] = CT_Empty
wml_main_namespace['object'] = CT_Object
wml_main_namespace['fldChar'] = CT_FldChar
wml_main_namespace['ruby'] = CT_Ruby
wml_main_namespace['footnoteReference'] = CT_FtnEdnRef
wml_main_namespace['endnoteReference'] = CT_FtnEdnRef
wml_main_namespace['commentReference'] = CT_Markup
wml_main_namespace['ptab'] = CT_PTab
wml_main_namespace['lastRenderedPageBreak'] = CT_Empty
wml_main_namespace['sectPrChange'] = CT_SectPrChange
wml_main_namespace['pgSz'] = CT_PageSz
wml_main_namespace['pgMar'] = CT_PageMar
wml_main_namespace['paperSrc'] = CT_PaperSource
wml_main_namespace['pgBorders'] = CT_PageBorders
wml_main_namespace['lnNumType'] = CT_LineNumber
wml_main_namespace['pgNumType'] = CT_PageNumber
wml_main_namespace['cols'] = CT_Columns
wml_main_namespace['formProt'] = CT_OnOff
wml_main_namespace['noEndnote'] = CT_OnOff
wml_main_namespace['titlePg'] = CT_OnOff
wml_main_namespace['bidi'] = CT_OnOff
wml_main_namespace['rtlGutter'] = CT_OnOff
wml_main_namespace['docGrid'] = CT_DocGrid
wml_main_namespace['printerSettings'] = CT_Rel
wml_main_namespace['headerReference'] = CT_HdrFtrRef
wml_main_namespace['footerReference'] = CT_HdrFtrRef
wml_main_namespace['col'] = CT_Column
wml_main_namespace['maxLength'] = CT_DecimalNumber
wml_main_namespace['format'] = CT_String
wml_main_namespace['result'] = CT_DecimalNumber
wml_main_namespace['listEntry'] = CT_String
wml_main_namespace['checked'] = CT_OnOff
wml_main_namespace['size'] = CT_HpsMeasure
wml_main_namespace['sizeAuto'] = CT_OnOff
wml_main_namespace['checkBox'] = CT_FFCheckBox
wml_main_namespace['ddList'] = CT_FFDDList
wml_main_namespace['textInput'] = CT_FFTextInput
wml_main_namespace['enabled'] = CT_OnOff
wml_main_namespace['calcOnExit'] = CT_OnOff
wml_main_namespace['entryMacro'] = CT_MacroName
wml_main_namespace['exitMacro'] = CT_MacroName
wml_main_namespace['helpText'] = CT_FFHelpText
wml_main_namespace['statusText'] = CT_FFStatusText
wml_main_namespace['fldData'] = CT_Text
wml_main_namespace['ffData'] = CT_FFData
wml_main_namespace['numberingChange'] = CT_TrackChangeNumbering
wml_main_namespace['movie'] = CT_Rel
wml_main_namespace['control'] = CT_Control
wml_main_namespace['objectLink'] = CT_ObjectLink
wml_main_namespace['objectEmbed'] = CT_ObjectEmbed
wml_main_namespace['pPrChange'] = CT_PPrChange
wml_main_namespace['keepNext'] = CT_OnOff
wml_main_namespace['keepLines'] = CT_OnOff
wml_main_namespace['pageBreakBefore'] = CT_OnOff
wml_main_namespace['framePr'] = CT_FramePr
wml_main_namespace['widowControl'] = CT_OnOff
wml_main_namespace['numPr'] = CT_NumPr
wml_main_namespace['suppressLineNumbers'] = CT_OnOff
wml_main_namespace['pBdr'] = CT_PBdr
wml_main_namespace['tabs'] = CT_Tabs
wml_main_namespace['suppressAutoHyphens'] = CT_OnOff
wml_main_namespace['kinsoku'] = CT_OnOff
wml_main_namespace['wordWrap'] = CT_OnOff
wml_main_namespace['overflowPunct'] = CT_OnOff
wml_main_namespace['topLinePunct'] = CT_OnOff
wml_main_namespace['autoSpaceDE'] = CT_OnOff
wml_main_namespace['autoSpaceDN'] = CT_OnOff
wml_main_namespace['adjustRightInd'] = CT_OnOff
wml_main_namespace['snapToGrid'] = CT_OnOff
wml_main_namespace['ind'] = CT_Ind
wml_main_namespace['contextualSpacing'] = CT_OnOff
wml_main_namespace['mirrorIndents'] = CT_OnOff
wml_main_namespace['suppressOverlap'] = CT_OnOff
wml_main_namespace['textAlignment'] = CT_TextAlignment
wml_main_namespace['textboxTightWrap'] = CT_TextboxTightWrap
wml_main_namespace['outlineLvl'] = CT_DecimalNumber
wml_main_namespace['between'] = CT_Border
wml_main_namespace['bar'] = CT_Border
wml_main_namespace['ilvl'] = CT_DecimalNumber
wml_main_namespace['numId'] = CT_DecimalNumber
wml_main_namespace['bookmarkStart'] = CT_Bookmark
wml_main_namespace['bookmarkEnd'] = CT_MarkupRange
wml_main_namespace['moveFromRangeStart'] = CT_MoveBookmark
wml_main_namespace['moveFromRangeEnd'] = CT_MarkupRange
wml_main_namespace['moveToRangeStart'] = CT_MoveBookmark
wml_main_namespace['moveToRangeEnd'] = CT_MarkupRange
wml_main_namespace['commentRangeStart'] = CT_MarkupRange
wml_main_namespace['commentRangeEnd'] = CT_MarkupRange
wml_main_namespace['customXmlInsRangeStart'] = CT_TrackChange
wml_main_namespace['customXmlInsRangeEnd'] = CT_Markup
wml_main_namespace['customXmlDelRangeStart'] = CT_TrackChange
wml_main_namespace['customXmlDelRangeEnd'] = CT_Markup
wml_main_namespace['customXmlMoveFromRangeStart'] = CT_TrackChange
wml_main_namespace['customXmlMoveFromRangeEnd'] = CT_Markup
wml_main_namespace['customXmlMoveToRangeStart'] = CT_TrackChange
wml_main_namespace['customXmlMoveToRangeEnd'] = CT_Markup
wml_main_namespace['cellIns'] = CT_TrackChange
wml_main_namespace['cellDel'] = CT_TrackChange
wml_main_namespace['cellMerge'] = CT_CellMergeTrackChange
wml_main_namespace['pStyle'] = CT_String


# wml_main_namespace["name"] = CT_DocPartName
# wml_main_namespace["name"] = CT_String
# wml_main_namespace["name"] = CT_FFName


class Union_CT_FFNameString(CT_DocPartName, CT_String, CT_FFName):
    """
    <xsd:complexType name="CT_DocPartName">
        <xsd:attribute name="val" type="s:ST_String" use="required"/>
        <xsd:attribute name="decorated" type="s:ST_OnOff" use="optional"/>
    </xsd:complexType>

    <xsd:complexType name="CT_String">
        <xsd:attribute name="val" type="s:ST_String" use="required"/>
    </xsd:complexType>

    <xsd:complexType name="CT_FFName">
        <xsd:attribute name="val" type="ST_FFName"/>
    </xsd:complexType>
    """



wml_main_namespace['name'] = Union_CT_FFNameString

# wml_namespace["docPart"] = CT_DocPart
# wml_namespace["docPart"] = CT_String


class Union_CT_DocPartString(CT_DocPart, CT_String):
    """
    <xsd:complexType name="CT_DocPart">
        <xsd:sequence>
            <xsd:element name="docPartPr" type="CT_DocPartPr" minOccurs="0"/>
            <xsd:element name="docPartBody" type="CT_Body" minOccurs="0"/>
        </xsd:sequence>
    </xsd:complexType>

    <xsd:complexType name="CT_String">
        <xsd:attribute name="val" type="s:ST_String" use="required"/>
    </xsd:complexType>
    """



wml_main_namespace['docPart'] = Union_CT_DocPartString

# wml_namespace["type"] = CT_DocPartType
# wml_namespace["type"] = CT_SectType
# wml_namespace["type"] = CT_MailMergeSourceType
# wml_namespace["type"] = CT_MailMergeOdsoFMDFieldType
# wml_namespace["type"] = CT_FFTextType


class Union_CT_DocPartType(
    CT_DocPartType,
    CT_SectType,
    CT_MailMergeSourceType,
    CT_MailMergeOdsoFMDFieldType,
    CT_FFTextType,
):
    """
    <xsd:complexType name="CT_DocPartType">
        <xsd:attribute name="val" use="required" type="ST_DocPartType"/>
    </xsd:complexType>

    <xsd:complexType name="CT_SectType">
        <xsd:attribute name="val" type="ST_SectionMark"/>
    </xsd:complexType>

    <xsd:complexType name="CT_MailMergeSourceType">
        <xsd:attribute name="val" use="required" type="ST_MailMergeSourceType"/>
    </xsd:complexType>

    <xsd:complexType name="CT_MailMergeOdsoFMDFieldType">
        <xsd:attribute name="val" type="ST_MailMergeOdsoFMDFieldType" use="required"/>
    </xsd:complexType>

    <xsd:complexType name="CT_FFTextType">
        <xsd:attribute name="val" type="ST_FFTextType" use="required"/>
    </xsd:complexType>
    """



wml_main_namespace['type'] = Union_CT_DocPartType

# wml_namespace["moveFrom"] = CT_RunTrackChange
# wml_namespace["moveFrom"] = CT_TrackChange


class Union_CT_TrackChange(CT_RunTrackChange, CT_TrackChange):
    """
    <xsd:complexType name="CT_RunTrackChange">
        <xsd:complexContent>
            <xsd:extension base="CT_TrackChange">
                <xsd:choice minOccurs="0" maxOccurs="unbounded">
                    <xsd:group ref="EG_ContentRunContent"/>
                    <xsd:group ref="m:EG_OMathMathElements"/>
                </xsd:choice>
            </xsd:extension>
        </xsd:complexContent>
    </xsd:complexType>

    <xsd:complexType name="CT_TrackChange">
        <xsd:complexContent>
            <xsd:extension base="CT_Markup">
                <xsd:attribute name="author" type="s:ST_String" use="required"/>
                <xsd:attribute name="date" type="ST_DateTime" use="optional"/>
            </xsd:extension>
        </xsd:complexContent>
    </xsd:complexType>
    """



wml_main_namespace['moveFrom'] = Union_CT_TrackChange

# wml_namespace["moveTo"] = CT_RunTrackChange
# wml_namespace["moveTo"] = CT_TrackChange

wml_main_namespace['moveTo'] = Union_CT_TrackChange

# wml_namespace["endnote"] = CT_FtnEdn
# wml_namespace["endnote"] = CT_FtnEdnSepRef


class Union_CT_FtnEdn(CT_FtnEdn, CT_FtnEdnSepRef):
    """
    <xsd:complexType name="CT_FtnEdn">
        <xsd:sequence>
            <xsd:group ref="EG_BlockLevelElts" minOccurs="1" maxOccurs="unbounded"/>
        </xsd:sequence>
        <xsd:attribute name="type" type="ST_FtnEdn" use="optional"/>
        <xsd:attribute name="id" type="ST_DecimalNumber" use="required"/>
    </xsd:complexType>

    <xsd:complexType name="CT_FtnEdnSepRef">
        <xsd:attribute name="id" type="ST_DecimalNumber" use="required"/>
    </xsd:complexType>
    """



wml_main_namespace['endnote'] = Union_CT_FtnEdn

# wml_namespace["footnote"] = CT_FtnEdn
# wml_namespace["footnote"] = CT_FtnEdnSepRef

wml_main_namespace['footnote'] = Union_CT_FtnEdn

# wml_namespace["sectPr"] = CT_SectPr
# wml_namespace["sectPr"] = CT_SectPrBase


class Union_CT_SectPr(CT_SectPr, CT_SectPrBase):
    """
    <xsd:complexType name="CT_SectPr">
        <xsd:sequence>
            <xsd:group ref="EG_HdrFtrReferences" minOccurs="0" maxOccurs="6"/>
            <xsd:group ref="EG_SectPrContents" minOccurs="0"/>
            <xsd:element name="sectPrChange" type="CT_SectPrChange" minOccurs="0"/>
        </xsd:sequence>
        <xsd:attributeGroup ref="AG_SectPrAttributes"/>
    </xsd:complexType>

    <xsd:complexType name="CT_FtnEdnSepRef">
        <xsd:attribute name="id" type="ST_DecimalNumber" use="required"/>
    </xsd:complexType>
    """



wml_main_namespace['sectPr'] = Union_CT_SectPr

# wml_namespace["ins"] = CT_RunTrackChange
# wml_namespace["ins"] = CT_TrackChange
# wml_namespace["ins"] = CT_MathCtrlIns


class Union_CT_TrackChangeMath(Union_CT_TrackChange, CT_MathCtrlIns):
    """
    <xsd:complexType name="CT_RunTrackChange">
        <xsd:complexContent>
            <xsd:extension base="CT_TrackChange">
                <xsd:choice minOccurs="0" maxOccurs="unbounded">
                    <xsd:group ref="EG_ContentRunContent"/>
                    <xsd:group ref="m:EG_OMathMathElements"/>
                </xsd:choice>
            </xsd:extension>
        </xsd:complexContent>
    </xsd:complexType>

    <xsd:complexType name="CT_TrackChange">
        <xsd:complexContent>
            <xsd:extension base="CT_Markup">
                <xsd:attribute name="author" type="s:ST_String" use="required"/>
                <xsd:attribute name="date" type="ST_DateTime" use="optional"/>
            </xsd:extension>
        </xsd:complexContent>
    </xsd:complexType>

    <xsd:complexType name="CT_MathCtrlIns">
        <xsd:complexContent>
            <xsd:extension base="CT_TrackChange">
                <xsd:choice minOccurs="0">
                    <xsd:element name="del" type="CT_RPrChange" minOccurs="1"/>
                    <xsd:element name="rPr" type="CT_RPr" minOccurs="1"/>
                </xsd:choice>
            </xsd:extension>
        </xsd:complexContent>
    </xsd:complexType>
    """



wml_main_namespace['ins'] = Union_CT_TrackChangeMath

# wml_namespace["del"] = CT_RunTrackChange
# wml_namespace["del"] = CT_TrackChange
# wml_namespace["del"] = CT_RPrChange
# wml_namespace["del"] = CT_MathCtrlDel


class Union_CT_TrackChangeMathDel(Union_CT_TrackChange, CT_RPrChange, CT_MathCtrlDel):
    """
    <xsd:complexType name="CT_RunTrackChange">
        <xsd:complexContent>
            <xsd:extension base="CT_TrackChange">
                <xsd:choice minOccurs="0" maxOccurs="unbounded">
                    <xsd:group ref="EG_ContentRunContent"/>
                    <xsd:group ref="m:EG_OMathMathElements"/>
                </xsd:choice>
            </xsd:extension>
        </xsd:complexContent>
    </xsd:complexType>

    <xsd:complexType name="CT_TrackChange">
        <xsd:complexContent>
            <xsd:extension base="CT_Markup">
                <xsd:attribute name="author" type="s:ST_String" use="required"/>
                <xsd:attribute name="date" type="ST_DateTime" use="optional"/>
            </xsd:extension>
        </xsd:complexContent>
    </xsd:complexType>

    <xsd:complexType name="CT_RPrChange">
        <xsd:complexContent>
            <xsd:extension base="CT_TrackChange">
                <xsd:sequence>
                    <xsd:element name="rPr" type="CT_RPrOriginal" minOccurs="1"/>
                </xsd:sequence>
            </xsd:extension>
        </xsd:complexContent>
    </xsd:complexType>

    <xsd:complexType name="CT_MathCtrlDel">
        <xsd:complexContent>
            <xsd:extension base="CT_TrackChange">
                <xsd:choice minOccurs="0">
                    <xsd:element name="rPr" type="CT_RPr" minOccurs="1"/>
                </xsd:choice>
            </xsd:extension>
        </xsd:complexContent>
    </xsd:complexType>
    """



wml_main_namespace['del'] = Union_CT_TrackChangeMathDel

# wml_namespace["bottom"] = CT_Border
# wml_namespace["bottom"] = CT_BottomPageBorder
# wml_namespace["bottom"] = CT_TblWidth


class Union_CT_BottomPageBorderTblWidth(CT_BottomPageBorder, CT_Border, CT_TblWidth):
    """
    <xsd:complexType name="CT_Border">
        <xsd:attribute name="val" type="ST_Border" use="required"/>
        <xsd:attribute name="color" type="ST_HexColor" use="optional" default="auto"/>
        <xsd:attribute name="themeColor" type="ST_ThemeColor" use="optional"/>
        <xsd:attribute name="themeTint" type="ST_UcharHexNumber" use="optional"/>
        <xsd:attribute name="themeShade" type="ST_UcharHexNumber" use="optional"/>
        <xsd:attribute name="sz" type="ST_EighthPointMeasure" use="optional"/>
        <xsd:attribute name="space" type="ST_PointMeasure" use="optional" default="0"/>
        <xsd:attribute name="shadow" type="s:ST_OnOff" use="optional"/>
        <xsd:attribute name="frame" type="s:ST_OnOff" use="optional"/>
    </xsd:complexType>

    <xsd:complexType name="CT_BottomPageBorder">
        <xsd:complexContent>
            <xsd:extension base="CT_PageBorder">
                <xsd:attribute ref="r:bottomLeft" use="optional"/>
                <xsd:attribute ref="r:bottomRight" use="optional"/>
            </xsd:extension>
        </xsd:complexContent>
    </xsd:complexType>

    <xsd:complexType name="CT_TblWidth">
        <xsd:attribute name="w" type="ST_MeasurementOrPercent"/>
        <xsd:attribute name="type" type="ST_TblWidth"/>
    </xsd:complexType>
    """



wml_main_namespace['bottom'] = Union_CT_BottomPageBorderTblWidth

# wml_namespace["end"] = CT_Border
# wml_namespace["end"] = CT_TblWidth


class Union_CT_BorderTblWidth(CT_Border, CT_TblWidth):
    """
    <xsd:complexType name="CT_Border">
        <xsd:attribute name="val" type="ST_Border" use="required"/>
        <xsd:attribute name="color" type="ST_HexColor" use="optional" default="auto"/>
        <xsd:attribute name="themeColor" type="ST_ThemeColor" use="optional"/>
        <xsd:attribute name="themeTint" type="ST_UcharHexNumber" use="optional"/>
        <xsd:attribute name="themeShade" type="ST_UcharHexNumber" use="optional"/>
        <xsd:attribute name="sz" type="ST_EighthPointMeasure" use="optional"/>
        <xsd:attribute name="space" type="ST_PointMeasure" use="optional" default="0"/>
        <xsd:attribute name="shadow" type="s:ST_OnOff" use="optional"/>
        <xsd:attribute name="frame" type="s:ST_OnOff" use="optional"/>
    </xsd:complexType>

    <xsd:complexType name="CT_TblWidth">
        <xsd:attribute name="w" type="ST_MeasurementOrPercent"/>
        <xsd:attribute name="type" type="ST_TblWidth"/>
    </xsd:complexType>
    """



wml_main_namespace['end'] = Union_CT_BorderTblWidth

# wml_namespace["right"] = CT_Border
# wml_namespace["right"] = CT_PageBorder
# wml_namespace["right"] = CT_TblWidth


class Union_CT_PageBorderTblWidth(CT_PageBorder, CT_Border, CT_TblWidth):
    """
    <xsd:complexType name="CT_Border">
        <xsd:attribute name="val" type="ST_Border" use="required"/>
        <xsd:attribute name="color" type="ST_HexColor" use="optional" default="auto"/>
        <xsd:attribute name="themeColor" type="ST_ThemeColor" use="optional"/>
        <xsd:attribute name="themeTint" type="ST_UcharHexNumber" use="optional"/>
        <xsd:attribute name="themeShade" type="ST_UcharHexNumber" use="optional"/>
        <xsd:attribute name="sz" type="ST_EighthPointMeasure" use="optional"/>
        <xsd:attribute name="space" type="ST_PointMeasure" use="optional" default="0"/>
        <xsd:attribute name="shadow" type="s:ST_OnOff" use="optional"/>
        <xsd:attribute name="frame" type="s:ST_OnOff" use="optional"/>
    </xsd:complexType>

    <xsd:complexType name="CT_PageBorder">
        <xsd:complexContent>
            <xsd:extension base="CT_Border">
                <xsd:attribute ref="r:id" use="optional"/>
            </xsd:extension>
        </xsd:complexContent>
    </xsd:complexType>

    <xsd:complexType name="CT_TblWidth">
        <xsd:attribute name="w" type="ST_MeasurementOrPercent"/>
        <xsd:attribute name="type" type="ST_TblWidth"/>
    </xsd:complexType>
    """



wml_main_namespace['right'] = Union_CT_PageBorderTblWidth

# wml_namespace["left"] = CT_Border
# wml_namespace["left"] = CT_PageBorder
# wml_namespace["left"] = CT_TblWidth

wml_main_namespace['left'] = Union_CT_PageBorderTblWidth

# wml_namespace["top"] = CT_Border
# wml_namespace["top"] = CT_TopPageBorder
# wml_namespace["top"] = CT_TblWidth

wml_main_namespace['top'] = Union_CT_PageBorderTblWidth

# wml_namespace["style"] = CT_Style
# wml_namespace["style"] = CT_String


class Union_CT_StyleString(CT_Style, CT_String):
    """
    <xsd:complexType name="CT_Style">
        <xsd:sequence>
            <xsd:element name="name" type="CT_String" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="aliases" type="CT_String" minOccurs="0"/>
            <xsd:element name="basedOn" type="CT_String" minOccurs="0"/>
            <xsd:element name="next" type="CT_String" minOccurs="0"/>
            <xsd:element name="link" type="CT_String" minOccurs="0"/>
            <xsd:element name="autoRedefine" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="hidden" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="uiPriority" type="CT_DecimalNumber" minOccurs="0"/>
            <xsd:element name="semiHidden" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="unhideWhenUsed" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="qFormat" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="locked" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="personal" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="personalCompose" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="personalReply" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="rsid" type="CT_LongHexNumber" minOccurs="0"/>
            <xsd:element name="pPr" type="CT_PPrGeneral" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="rPr" type="CT_RPr" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="tblPr" type="CT_TblPrBase" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="trPr" type="CT_TrPr" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="tcPr" type="CT_TcPr" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="tblStylePr" type="CT_TblStylePr" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
        <xsd:attribute name="type" type="ST_StyleType" use="optional"/>
        <xsd:attribute name="styleId" type="s:ST_String" use="optional"/>
        <xsd:attribute name="default" type="s:ST_OnOff" use="optional"/>
        <xsd:attribute name="customStyle" type="s:ST_OnOff" use="optional"/>
    </xsd:complexType>

    <xsd:complexType name="CT_String">
        <xsd:attribute name="val" type="s:ST_String" use="required"/>
    </xsd:complexType>
    """



wml_main_namespace['style'] = Union_CT_StyleString

# wml_namespace["pPr"] = CT_PPrBase
# wml_namespace["pPr"] = CT_PPr
# wml_namespace["pPr"] = CT_PPrGeneral


# class Union_CT_PPr(CT_PPrBase, CT_PPrGeneral,  CT_PPr):
# CT_PPrGeneral 和 CT_PPr 均继承自 CT_PPrBase
class Union_CT_PPr(CT_PPrGeneral, CT_PPr):
    """
    <xsd:complexType name="CT_PPrBase">
        <xsd:sequence>
            <xsd:element name="pStyle" type="CT_String" minOccurs="0"/>
            <xsd:element name="keepNext" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="keepLines" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="pageBreakBefore" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="framePr" type="CT_FramePr" minOccurs="0"/>
            <xsd:element name="widowControl" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="numPr" type="CT_NumPr" minOccurs="0"/>
            <xsd:element name="suppressLineNumbers" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="pBdr" type="CT_PBdr" minOccurs="0"/>
            <xsd:element name="shd" type="CT_Shd" minOccurs="0"/>
            <xsd:element name="tabs" type="CT_Tabs" minOccurs="0"/>
            <xsd:element name="suppressAutoHyphens" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="kinsoku" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="wordWrap" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="overflowPunct" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="topLinePunct" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="autoSpaceDE" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="autoSpaceDN" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="bidi" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="adjustRightInd" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="snapToGrid" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="spacing" type="CT_Spacing" minOccurs="0"/>
            <xsd:element name="ind" type="CT_Ind" minOccurs="0"/>
            <xsd:element name="contextualSpacing" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="mirrorIndents" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="suppressOverlap" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="jc" type="CT_Jc" minOccurs="0"/>
            <xsd:element name="textDirection" type="CT_TextDirection" minOccurs="0"/>
            <xsd:element name="textAlignment" type="CT_TextAlignment" minOccurs="0"/>
            <xsd:element name="textboxTightWrap" type="CT_TextboxTightWrap" minOccurs="0"/>
            <xsd:element name="outlineLvl" type="CT_DecimalNumber" minOccurs="0"/>
            <xsd:element name="divId" type="CT_DecimalNumber" minOccurs="0"/>
            <xsd:element name="cnfStyle" type="CT_Cnf" minOccurs="0" maxOccurs="1"/>
        </xsd:sequence>
    </xsd:complexType>

    <xsd:complexType name="CT_PPrGeneral">
        <xsd:complexContent>
            <xsd:extension base="CT_PPrBase">
                <xsd:sequence>
                    <xsd:element name="pPrChange" type="CT_PPrChange" minOccurs="0"/>
                </xsd:sequence>
            </xsd:extension>
        </xsd:complexContent>
    </xsd:complexType>

    <xsd:complexType name="CT_PPr">
        <xsd:complexContent>
            <xsd:extension base="CT_PPrBase">
                <xsd:sequence>
                    <xsd:element name="rPr" type="CT_ParaRPr" minOccurs="0"/>
                    <xsd:element name="sectPr" type="CT_SectPr" minOccurs="0"/>
                    <xsd:element name="pPrChange" type="CT_PPrChange" minOccurs="0"/>
                </xsd:sequence>
            </xsd:extension>
        </xsd:complexContent>
    </xsd:complexType>
    """



wml_main_namespace['pPr'] = Union_CT_PPr

# wml_namespace["rPr"] = CT_RPr
# wml_namespace["rPr"] = CT_ParaRPrOriginal
# wml_namespace["rPr"] = CT_RPrOriginal
# wml_namespace["rPr"] = CT_ParaRPr


class Union_CT_RPr(CT_RPr, CT_ParaRPrOriginal, CT_RPrOriginal, CT_ParaRPr):
    """
    <xsd:complexType name="CT_RPr">
        <xsd:sequence>
            <xsd:group ref="EG_RPrContent" minOccurs="0"/>
        </xsd:sequence>
    </xsd:complexType>

    <xsd:complexType name="CT_ParaRPrOriginal">
        <xsd:sequence>
            <xsd:group ref="EG_ParaRPrTrackChanges" minOccurs="0"/>
            <xsd:group ref="EG_RPrBase" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
    </xsd:complexType>

    <xsd:complexType name="CT_RPrOriginal">
        <xsd:sequence>
            <xsd:group ref="EG_RPrBase" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
    </xsd:complexType>

    <xsd:complexType name="CT_ParaRPr">
        <xsd:sequence>
            <xsd:group ref="EG_ParaRPrTrackChanges" minOccurs="0"/>
            <xsd:group ref="EG_RPrBase" minOccurs="0" maxOccurs="unbounded"/>
            <xsd:element name="rPrChange" type="CT_ParaRPrChange" minOccurs="0"/>
        </xsd:sequence>
    </xsd:complexType>
    """



wml_main_namespace['rPr'] = Union_CT_RPr

# wml_namespace["tblPr"] = CT_TblPrBase
# wml_namespace["tblPr"] = CT_TblPr

# class Union_CT_RPr(CT_TblPrBase, CT_TblPr):


# CT_TblPr 继承自 CT_TblPrBase
class Union_CT_TblPr(CT_TblPr):
    """
    <xsd:complexType name="CT_TblPrBase">
        <xsd:sequence>
            <xsd:element name="tblStyle" type="CT_String" minOccurs="0"/>
            <xsd:element name="tblpPr" type="CT_TblPPr" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="tblOverlap" type="CT_TblOverlap" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="bidiVisual" type="CT_OnOff" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="tblStyleRowBandSize" type="CT_DecimalNumber" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="tblStyleColBandSize" type="CT_DecimalNumber" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="tblW" type="CT_TblWidth" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="jc" type="CT_JcTable" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="tblCellSpacing" type="CT_TblWidth" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="tblInd" type="CT_TblWidth" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="tblBorders" type="CT_TblBorders" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="shd" type="CT_Shd" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="tblLayout" type="CT_TblLayoutType" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="tblCellMar" type="CT_TblCellMar" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="tblLook" type="CT_TblLook" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="tblCaption" type="CT_String" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="tblDescription" type="CT_String" minOccurs="0" maxOccurs="1"/>
        </xsd:sequence>
    </xsd:complexType>

    <xsd:complexType name="CT_TblPr">
        <xsd:complexContent>
            <xsd:extension base="CT_TblPrBase">
                <xsd:sequence>
                    <xsd:element name="tblPrChange" type="CT_TblPrChange" minOccurs="0"/>
                </xsd:sequence>
            </xsd:extension>
        </xsd:complexContent>
    </xsd:complexType>
    """



wml_main_namespace['tblPr'] = Union_CT_TblPr

wml_main_namespace['trPr'] = CT_TrPrBase
wml_main_namespace['trPr'] = CT_TrPr


# CT_TrPr 继承自 CT_TrPrBase
class Union_CT_TrPr(CT_TrPr):
    """
    <xsd:complexType name="CT_TrPrBase">
        <xsd:choice maxOccurs="unbounded">
            <xsd:element name="cnfStyle" type="CT_Cnf" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="divId" type="CT_DecimalNumber" minOccurs="0"/>
            <xsd:element name="gridBefore" type="CT_DecimalNumber" minOccurs="0"/>
            <xsd:element name="gridAfter" type="CT_DecimalNumber" minOccurs="0"/>
            <xsd:element name="wBefore" type="CT_TblWidth" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="wAfter" type="CT_TblWidth" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="cantSplit" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="trHeight" type="CT_Height" minOccurs="0"/>
            <xsd:element name="tblHeader" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="tblCellSpacing" type="CT_TblWidth" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="jc" type="CT_JcTable" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="hidden" type="CT_OnOff" minOccurs="0"/>
        </xsd:choice>
    </xsd:complexType>

    <xsd:complexType name="CT_TrPr">
        <xsd:complexContent>
            <xsd:extension base="CT_TrPrBase">
                <xsd:sequence>
                    <xsd:element name="ins" type="CT_TrackChange" minOccurs="0"/>
                    <xsd:element name="del" type="CT_TrackChange" minOccurs="0"/>
                    <xsd:element name="trPrChange" type="CT_TrPrChange" minOccurs="0"/>
                </xsd:sequence>
            </xsd:extension>
        </xsd:complexContent>
    </xsd:complexType>
    """



wml_main_namespace['trPr'] = Union_CT_TrPr

# wml_namespace["tcPr"] = CT_TcPrInner
# wml_namespace["tcPr"] = CT_TcPr


# CT_TcPr 继承自 CT_TcPrInner
class Union_CT_TcPr(CT_TcPr):
    """
    <xsd:complexType name="CT_TcPrInner">
        <xsd:complexContent>
            <xsd:extension base="CT_TcPrBase">
                <xsd:sequence>
                    <xsd:group ref="EG_CellMarkupElements" minOccurs="0" maxOccurs="1"/>
                </xsd:sequence>
            </xsd:extension>
        </xsd:complexContent>
    </xsd:complexType>

    <xsd:complexType name="CT_TcPr">
        <xsd:complexContent>
            <xsd:extension base="CT_TcPrInner">
                <xsd:sequence>
                    <xsd:element name="tcPrChange" type="CT_TcPrChange" minOccurs="0"/>
                </xsd:sequence>
            </xsd:extension>
        </xsd:complexContent>
    </xsd:complexType>
    """



wml_main_namespace['tcPr'] = Union_CT_TcPr

# wml_namespace["start"] = CT_DecimalNumber
# wml_namespace["start"] = CT_TblWidth
# wml_namespace["start"] = CT_Border


class Union_CT_DecimalNumberTblWidthBorder(CT_DecimalNumber, CT_TblWidth, CT_Border):
    """
    <xsd:complexType name="CT_DecimalNumber">
        <xsd:attribute name="val" type="ST_DecimalNumber" use="required"/>
    </xsd:complexType>

    <xsd:complexType name="CT_TblWidth">
        <xsd:attribute name="w" type="ST_MeasurementOrPercent"/>
        <xsd:attribute name="type" type="ST_TblWidth"/>
    </xsd:complexType>

    <xsd:complexType name="CT_Border">
        <xsd:attribute name="val" type="ST_Border" use="required"/>
        <xsd:attribute name="color" type="ST_HexColor" use="optional" default="auto"/>
        <xsd:attribute name="themeColor" type="ST_ThemeColor" use="optional"/>
        <xsd:attribute name="themeTint" type="ST_UcharHexNumber" use="optional"/>
        <xsd:attribute name="themeShade" type="ST_UcharHexNumber" use="optional"/>
        <xsd:attribute name="sz" type="ST_EighthPointMeasure" use="optional"/>
        <xsd:attribute name="space" type="ST_PointMeasure" use="optional" default="0"/>
        <xsd:attribute name="shadow" type="s:ST_OnOff" use="optional"/>
        <xsd:attribute name="frame" type="s:ST_OnOff" use="optional"/>
    </xsd:complexType>
    """



wml_main_namespace['start'] = Union_CT_DecimalNumberTblWidthBorder

# wml_namespace["sz"] = CT_String
# wml_namespace["sz"] = CT_HpsMeasure


class Union_CT_StringHpsMeasure(CT_String, CT_HpsMeasure):
    """
    <xsd:complexType name="CT_String">
        <xsd:attribute name="val" type="s:ST_String" use="required"/>
    </xsd:complexType>

    <xsd:complexType name="CT_HpsMeasure">
        <xsd:attribute name="val" type="ST_HpsMeasure" use="required"/>
    </xsd:complexType>
    """



wml_main_namespace['sz'] = Union_CT_StringHpsMeasure

# wml_namespace["footnotePr"] = CT_FtnDocProps
# wml_namespace["footnotePr"] = CT_FtnProps


class Union_CT_FtnDocProps(CT_FtnDocProps, CT_FtnProps):
    """
    <xsd:complexType name="CT_FtnDocProps">
        <xsd:complexContent>
            <xsd:extension base="CT_FtnProps">
                <xsd:sequence>
                    <xsd:element name="footnote" type="CT_FtnEdnSepRef" minOccurs="0" maxOccurs="3"/>
                </xsd:sequence>
            </xsd:extension>
        </xsd:complexContent>
    </xsd:complexType>

    <xsd:complexType name="CT_FtnProps">
        <xsd:sequence>
            <xsd:element name="pos" type="CT_FtnPos" minOccurs="0"/>
            <xsd:element name="numFmt" type="CT_NumFmt" minOccurs="0"/>
            <xsd:group ref="EG_FtnEdnNumProps" minOccurs="0"/>
        </xsd:sequence>
    </xsd:complexType>
    """



wml_main_namespace['footnotePr'] = Union_CT_FtnDocProps

# wml_namespace["endnotePr"] = CT_EdnDocProps
# wml_namespace["endnotePr"] = CT_EdnProps


# CT_EdnDocProps 继承自 CT_EdnProps
class Union_CT_EdnDocProps(CT_EdnDocProps):
    """
    <xsd:complexType name="CT_EdnDocProps">
        <xsd:complexContent>
            <xsd:extension base="CT_EdnProps">
                <xsd:sequence>
                    <xsd:element name="endnote" type="CT_FtnEdnSepRef" minOccurs="0" maxOccurs="3"/>
                </xsd:sequence>
            </xsd:extension>
        </xsd:complexContent>
    </xsd:complexType>

    <xsd:complexType name="CT_EdnProps">
        <xsd:sequence>
            <xsd:element name="pos" type="CT_EdnPos" minOccurs="0"/>
            <xsd:element name="numFmt" type="CT_NumFmt" minOccurs="0"/>
            <xsd:group ref="EG_FtnEdnNumProps" minOccurs="0"/>
        </xsd:sequence>
    </xsd:complexType>
    """



wml_main_namespace['endnotePr'] = Union_CT_EdnDocProps

# wml_namespace["recipientData"] = CT_Rel
# wml_namespace["recipientData"] = CT_RecipientData


class Union_CT_Rel(CT_Rel, CT_RecipientData):
    """
    <xsd:complexType name="CT_Rel">
        <xsd:attribute ref="r:id" use="required"/>
    </xsd:complexType>

    <xsd:complexType name="CT_RecipientData">
        <xsd:sequence>
            <xsd:element name="active" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="column" type="CT_DecimalNumber" minOccurs="1"/>
            <xsd:element name="uniqueTag" type="CT_Base64Binary" minOccurs="1"/>
        </xsd:sequence>
    </xsd:complexType>
    """



wml_main_namespace['recipientData'] = Union_CT_Rel

# wml_namespace["pos"] = CT_EdnPos
# wml_namespace["pos"] = CT_FtnPos


class Union_CT_EdnPos(CT_EdnPos, CT_FtnPos):
    """
    <xsd:complexType name="CT_EdnPos">
        <xsd:attribute name="val" type="ST_EdnPos" use="required"/>
    </xsd:complexType>

    <xsd:complexType name="CT_RecipientData">
        <xsd:sequence>
            <xsd:element name="active" type="CT_OnOff" minOccurs="0"/>
            <xsd:element name="column" type="CT_DecimalNumber" minOccurs="1"/>
            <xsd:element name="uniqueTag" type="CT_Base64Binary" minOccurs="1"/>
        </xsd:sequence>
    </xsd:complexType>
    """



wml_main_namespace['pos'] = Union_CT_EdnPos

# wml_namespace["tblGrid"] = CT_TblGridBase
# wml_namespace["tblGrid"] = CT_TblGrid


# CT_TblGrid 继承自 CT_TblGridBase
class Union_CT_TblGrid(CT_TblGrid):
    """
    <xsd:complexType name="CT_TblGridBase">
        <xsd:sequence>
            <xsd:element name="gridCol" type="CT_TblGridCol" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
    </xsd:complexType>

    <xsd:complexType name="CT_TblGrid">
        <xsd:complexContent>
            <xsd:extension base="CT_TblGridBase">
                <xsd:sequence>
                    <xsd:element name="tblGridChange" type="CT_TblGridChange" minOccurs="0"/>
                </xsd:sequence>
            </xsd:extension>
        </xsd:complexContent>
    </xsd:complexType>
    """



wml_main_namespace['tblGrid'] = Union_CT_TblGrid

# wml_namespace["tblPrEx"] = CT_TblPrExBase
# wml_namespace["tblPrEx"] = CT_TblPrEx


# CT_TblPrEx 继承自 CT_TblPrExBase
class Union_CT_TblPrEx(CT_TblPrEx):
    """
    <xsd:complexType name="CT_TblPrExBase">
        <xsd:sequence>
            <xsd:element name="tblW" type="CT_TblWidth" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="jc" type="CT_JcTable" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="tblCellSpacing" type="CT_TblWidth" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="tblInd" type="CT_TblWidth" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="tblBorders" type="CT_TblBorders" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="shd" type="CT_Shd" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="tblLayout" type="CT_TblLayoutType" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="tblCellMar" type="CT_TblCellMar" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="tblLook" type="CT_TblLook" minOccurs="0" maxOccurs="1"/>
        </xsd:sequence>
    </xsd:complexType>

    <xsd:complexType name="CT_TblPrEx">
        <xsd:complexContent>
            <xsd:extension base="CT_TblPrExBase">
                <xsd:sequence>
                    <xsd:element name="tblPrExChange" type="CT_TblPrExChange" minOccurs="0"/>
                </xsd:sequence>
            </xsd:extension>
        </xsd:complexContent>
    </xsd:complexType>
    """



wml_main_namespace['tblPrEx'] = Union_CT_TblPrEx

# wml_namespace["jc"] = CT_Jc
# wml_namespace["jc"] = CT_JcTable


class Union_CT_JcTable(CT_Jc, CT_JcTable):
    """
    <xsd:complexType name="CT_Jc">
        <xsd:attribute name="val" type="ST_Jc" use="required"/>
    </xsd:complexType>

    <xsd:complexType name="CT_JcTable">
        <xsd:attribute name="val" type="ST_JcTable" use="required"/>
    </xsd:complexType>
    """



wml_main_namespace['jc'] = Union_CT_JcTable

# wml_namespace["placeholder"] = CT_String
# wml_namespace["placeholder"] = CT_Placeholder


class Union_CT_StringPlaceholder(CT_String, CT_Placeholder):
    """
    <xsd:complexType name="CT_String">
        <xsd:attribute name="val" type="s:ST_String" use="required"/>
    </xsd:complexType>

    <xsd:complexType name="CT_Placeholder">
        <xsd:sequence>
            <xsd:element name="docPart" type="CT_String"/>
        </xsd:sequence>
    </xsd:complexType>
    """



wml_main_namespace['placeholder'] = Union_CT_StringPlaceholder

# wml_namespace["sdtContent"] = CT_SdtContentRow
# wml_namespace["sdtContent"] = CT_SdtContentCell
# wml_namespace["sdtContent"] = CT_SdtContentRun
# wml_namespace["sdtContent"] = CT_SdtContentBlock


class Union_CT_SdtContentRowCellRunBlock(CT_SdtContentRow, CT_SdtContentCell, CT_SdtContentRun, CT_SdtContentBlock):
    """
    <xsd:complexType name="CT_SdtContentRow">
        <xsd:group ref="EG_ContentRowContent" minOccurs="0" maxOccurs="unbounded"/>
    </xsd:complexType>

    <xsd:complexType name="CT_SdtContentCell">
        <xsd:group ref="EG_ContentCellContent" minOccurs="0" maxOccurs="unbounded"/>
    </xsd:complexType>

    <xsd:complexType name="CT_SdtContentRun">
        <xsd:group ref="EG_PContent" minOccurs="0" maxOccurs="unbounded"/>
    </xsd:complexType>

    <xsd:complexType name="CT_SdtContentBlock">
        <xsd:group ref="EG_ContentBlockContent" minOccurs="0" maxOccurs="unbounded"/>
    </xsd:complexType>
    """



wml_main_namespace['sdtContent'] = Union_CT_SdtContentRowCellRunBlock

# wml_namespace["customXml"] = CT_CustomXmlCell
# wml_namespace["customXml"] = CT_CustomXmlRow
# wml_namespace["customXml"] = CT_CustomXmlRun
# wml_namespace["customXml"] = CT_CustomXmlBlock


class Union_CT_CustomXmlCellRowRunBlock(CT_CustomXmlCell, CT_CustomXmlRow, CT_CustomXmlRun, CT_CustomXmlBlock):
    """
    <xsd:complexType name="CT_CustomXmlCell">
        <xsd:sequence>
            <xsd:element name="customXmlPr" type="CT_CustomXmlPr" minOccurs="0" maxOccurs="1"/>
            <xsd:group ref="EG_ContentCellContent" minOccurs="0" maxOccurs="unbounded"/>

            <xsd:group name="EG_ContentCellContent">
                <xsd:choice>
                    <xsd:element name="tc" type="CT_Tc" minOccurs="0" maxOccurs="unbounded"/>
                    <xsd:element name="customXml" type="CT_CustomXmlCell"/>
                    <xsd:element name="sdt" type="CT_SdtCell"/>
                    <xsd:group ref="EG_RunLevelElts" minOccurs="0" maxOccurs="unbounded"/>
                </xsd:choice>
            </xsd:group>

        </xsd:sequence>
        <xsd:attribute name="uri" type="s:ST_String"/>
        <xsd:attribute name="element" type="s:ST_XmlName" use="required"/>
    </xsd:complexType>

    <xsd:complexType name="CT_CustomXmlRow">
        <xsd:sequence>
            <xsd:element name="customXmlPr" type="CT_CustomXmlPr" minOccurs="0" maxOccurs="1"/>
            <xsd:group ref="EG_ContentRowContent" minOccurs="0" maxOccurs="unbounded"/>

            <xsd:group name="EG_ContentRowContent">
                <xsd:choice>
                    <xsd:element name="tr" type="CT_Row" minOccurs="0" maxOccurs="unbounded"/>
                    <xsd:element name="customXml" type="CT_CustomXmlRow"/>
                    <xsd:element name="sdt" type="CT_SdtRow"/>
                    <xsd:group ref="EG_RunLevelElts" minOccurs="0" maxOccurs="unbounded"/>
                </xsd:choice>
            </xsd:group>

        </xsd:sequence>
        <xsd:attribute name="uri" type="s:ST_String"/>
        <xsd:attribute name="element" type="s:ST_XmlName" use="required"/>
    </xsd:complexType>

    <xsd:complexType name="CT_CustomXmlRun">
        <xsd:sequence>
            <xsd:element name="customXmlPr" type="CT_CustomXmlPr" minOccurs="0" maxOccurs="1"/>
            <xsd:group ref="EG_PContent" minOccurs="0" maxOccurs="unbounded"/>

                <xsd:group name="EG_PContent">
                    <xsd:choice>
                        <xsd:group ref="EG_ContentRunContent" minOccurs="0" maxOccurs="unbounded"/>
                        <xsd:element name="fldSimple" type="CT_SimpleField" minOccurs="0" maxOccurs="unbounded"/>
                        <xsd:element name="hyperlink" type="CT_Hyperlink"/>
                        <xsd:element name="subDoc" type="CT_Rel"/>
                    </xsd:choice>
                </xsd:group>

        </xsd:sequence>
        <xsd:attribute name="uri" type="s:ST_String"/>
        <xsd:attribute name="element" type="s:ST_XmlName" use="required"/>
    </xsd:complexType>

    <xsd:complexType name="CT_CustomXmlBlock">
        <xsd:sequence>
            <xsd:element name="customXmlPr" type="CT_CustomXmlPr" minOccurs="0" maxOccurs="1"/>
            <xsd:group ref="EG_ContentBlockContent" minOccurs="0" maxOccurs="unbounded"/>

            <xsd:group name="EG_ContentBlockContent">
                <xsd:choice>
                    <xsd:element name="customXml" type="CT_CustomXmlBlock"/>
                    <xsd:element name="sdt" type="CT_SdtBlock"/>
                    <xsd:element name="p" type="CT_P" minOccurs="0" maxOccurs="unbounded"/>
                    <xsd:element name="tbl" type="CT_Tbl" minOccurs="0" maxOccurs="unbounded"/>
                    <xsd:group ref="EG_RunLevelElts" minOccurs="0" maxOccurs="unbounded"/>
                </xsd:choice>
            </xsd:group>
        </xsd:sequence>
        <xsd:attribute name="uri" type="s:ST_String"/>
        <xsd:attribute name="element" type="s:ST_XmlName" use="required"/>
    </xsd:complexType>
    """



wml_main_namespace['customXml'] = Union_CT_CustomXmlCellRowRunBlock

# wml_main_namespace["sdt"] = CT_SdtCell
# wml_main_namespace["sdt"] = CT_SdtRow
# wml_main_namespace["sdt"] = CT_SdtBlock
# wml_main_namespace["sdt"] = CT_SdtRun


class Union_CT_SdtCellRowRunBlock(CT_SdtCell, CT_SdtRow, CT_SdtBlock, CT_SdtRun):
    """
    <xsd:complexType name="CT_SdtCell">
        <xsd:sequence>
            <xsd:element name="sdtPr" type="CT_SdtPr" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="sdtEndPr" type="CT_SdtEndPr" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="sdtContent" type="CT_SdtContentCell" minOccurs="0" maxOccurs="1"/>
        </xsd:sequence>
    </xsd:complexType>

    <xsd:complexType name="CT_SdtRow">
        <xsd:sequence>
            <xsd:element name="sdtPr" type="CT_SdtPr" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="sdtEndPr" type="CT_SdtEndPr" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="sdtContent" type="CT_SdtContentRow" minOccurs="0" maxOccurs="1"/>
        </xsd:sequence>
    </xsd:complexType>

    <xsd:complexType name="CT_SdtBlock">
        <xsd:sequence>
            <xsd:element name="sdtPr" type="CT_SdtPr" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="sdtEndPr" type="CT_SdtEndPr" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="sdtContent" type="CT_SdtContentBlock" minOccurs="0" maxOccurs="1"/>
        </xsd:sequence>
    </xsd:complexType>

    <xsd:complexType name="CT_SdtRun">
        <xsd:sequence>
            <xsd:element name="sdtPr" type="CT_SdtPr" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="sdtEndPr" type="CT_SdtEndPr" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="sdtContent" type="CT_SdtContentRun" minOccurs="0" maxOccurs="1"/>
        </xsd:sequence>
    </xsd:complexType>
    """



wml_main_namespace['sdt'] = Union_CT_SdtCellRowRunBlock

# wml_namespace["rPrChange"] = CT_ParaRPrChange
# wml_namespace["rPrChange"] = CT_RPrChange


class Union_CT_RPrChange(CT_ParaRPrChange, CT_RPrChange):
    """
    <xsd:complexType name="CT_ParaRPrChange">
        <xsd:complexContent>
            <xsd:extension base="CT_TrackChange">
                <xsd:sequence>
                    <xsd:element name="rPr" type="CT_ParaRPrOriginal" minOccurs="1"/>
                </xsd:sequence>
            </xsd:extension>
        </xsd:complexContent>
    </xsd:complexType>

    <xsd:complexType name="CT_RPrChange">
        <xsd:complexContent>
            <xsd:extension base="CT_TrackChange">
                <xsd:sequence>
                    <xsd:element name="rPr" type="CT_RPrOriginal" minOccurs="1"/>
                </xsd:sequence>
            </xsd:extension>
        </xsd:complexContent>
    </xsd:complexType>
    """



wml_main_namespace['rPrChange'] = Union_CT_RPrChange

# wml_namespace["spacing"] = CT_SignedTwipsMeasure
# wml_namespace["spacing"] = CT_Spacing


class Union_CT_Spacing(CT_SignedTwipsMeasure, CT_Spacing):
    """
    <xsd:complexType name="CT_Spacing">
        <xsd:attribute name="before" type="s:ST_TwipsMeasure" use="optional" default="0"/>
        <xsd:attribute name="beforeLines" type="ST_DecimalNumber" use="optional" default="0"/>
        <xsd:attribute name="beforeAutospacing" type="s:ST_OnOff" use="optional" default="off"/>
        <xsd:attribute name="after" type="s:ST_TwipsMeasure" use="optional" default="0"/>
        <xsd:attribute name="afterLines" type="ST_DecimalNumber" use="optional" default="0"/>
        <xsd:attribute name="afterAutospacing" type="s:ST_OnOff" use="optional" default="off"/>
        <xsd:attribute name="line" type="ST_SignedTwipsMeasure" use="optional" default="0"/>
        <xsd:attribute name="lineRule" type="ST_LineSpacingRule" use="optional" default="auto"/>
    </xsd:complexType>

    <xsd:complexType name="CT_SignedTwipsMeasure">
        <xsd:attribute name="val" type="ST_SignedTwipsMeasure" use="required"/>
    </xsd:complexType>
    """



wml_main_namespace['spacing'] = Union_CT_Spacing

# wml_namespace["w"] = CT_TextScale
# wml_namespace["w"] = CT_TwipsMeasure


class Union_CT_TextScale(CT_TextScale, CT_TwipsMeasure):
    """
    <xsd:complexType name="CT_TextScale">
        <xsd:attribute name="val" type="ST_TextScale"/>
    </xsd:complexType>

    <xsd:complexType name="CT_TwipsMeasure">
        <xsd:attribute name="val" type="s:ST_TwipsMeasure" use="required"/>
    </xsd:complexType>
    """



wml_main_namespace['w'] = Union_CT_TextScale

# wml_namespace["tab"] = CT_Empty
# wml_namespace["tab"] = CT_TabStop


class Union_CT_TabStop(CT_Empty, CT_TabStop):
    """
    <xsd:complexType name="CT_Empty"/>

    <xsd:complexType name="CT_TabStop">
        <xsd:attribute name="val" type="ST_TabJc" use="required"/>
        <xsd:attribute name="leader" type="ST_TabTlc" use="optional"/>
        <xsd:attribute name="pos" type="ST_SignedTwipsMeasure" use="required"/>
    </xsd:complexType>
    """



wml_main_namespace['tab'] = Union_CT_TabStop

# wml_namespace["default"] = CT_String
# wml_namespace["default"] = CT_DecimalNumber
# wml_namespace["default"] = CT_OnOff


class Union_CT_OnOffStringDecimalNumber(CT_String, CT_DecimalNumber, CT_OnOff):
    """
    <xsd:complexType name="CT_String">
        <xsd:attribute name="val" type="s:ST_String" use="required"/>
    </xsd:complexType>

    <xsd:complexType name="CT_DecimalNumber">
        <xsd:attribute name="val" type="ST_DecimalNumber" use="required"/>
    </xsd:complexType>

    <xsd:complexType name="CT_OnOff">
        <xsd:attribute name="val" type="s:ST_OnOff"/>
    </xsd:complexType>
    """



wml_main_namespace['default'] = Union_CT_OnOffStringDecimalNumber
