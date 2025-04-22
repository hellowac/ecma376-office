"""
对应xsd: shared-commonSimpleTypes.xsd

<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"
  xmlns="http://schemas.openxmlformats.org/officeDocument/2006/sharedTypes"
  targetNamespace="http://schemas.openxmlformats.org/officeDocument/2006/sharedTypes"
  elementFormDefault="qualified">
  ...
</xsd:schema>
"""

import logging
from typing import AnyStr, NewType, Self

from ecma376_office.oxml import utils
from ecma376_office.oxml.base import OxmlBaseElement, ST_BaseEnumType, ST_BaseType, lookup
from ecma376_office.oxml.exceptions import OxmlAttributeValidateError

logger = logging.getLogger(__name__)

# 共21个简单类型


namespace_s = 'http://schemas.openxmlformats.org/officeDocument/2006/sharedTypes'

logger = logging.getLogger(__name__)

ns_map = {
    's': namespace_s,  # 当前命名空间
}


def qn(tag: str):
    """将 dc:creator 这种的标签,转换为 {http://purl.org/dc/elements/1.1/}creator 这样的形式"""

    global ns_map

    if ':' not in tag:
        return tag

    ns_prefix, ns = tag.split(':')

    return f'{{{ns_map[ns_prefix]}}}{ns}'


ST_Lang = NewType('ST_Lang', str)


ST_HexColorRGB = NewType('ST_HexColorRGB', str)
"""十六进制颜色值

22.9.2.5 ST_HexColorRGB (Hexadecimal Color Value)

eg: BCBCBC"""


def to_ST_HexColorRGB(val: str) -> ST_HexColorRGB:
    """转为16进制的颜色RGB值"""

    if len(val) != 6:
        msg = f"RGB 字符串必须是六个字符长，得到 '{val}'"
        raise OxmlAttributeValidateError(msg)

    return ST_HexColorRGB(val)


class ST_Panose(ST_BaseType[AnyStr, str]):
    def _validate(self: Self) -> None:
        val = utils.AnyStrToStr(self._val)

        if len(val) != 20:
            msg = f"Panose 字符串必须是20字符长，得到 '{val}'"
            raise OxmlAttributeValidateError(msg)

        # 必须解析为十六进制 int --------
        try:
            int(val, 16)
        except ValueError:
            msg = f"Panose 字符串必须是有效的十六进制字符串，得到 '{val}'"
            raise OxmlAttributeValidateError(msg)

        self._python_val = val


class ST_CalendarType(ST_BaseEnumType):
    """日历类型"""

    Gregorian = 'gregorian'
    GregorianUs = 'gregorianUs'
    GregorianMeFrench = 'gregorianMeFrench'
    GregorianArabic = 'gregorianArabic'
    Hijri = 'hijri'
    Hebrew = 'hebrew'
    Taiwan = 'taiwan'
    Japan = 'japan'
    Thai = 'thai'
    Korea = 'korea'
    Saka = 'saka'
    GregorianXlitEnglish = 'gregorianXlitEnglish'
    GregorianXlitFrench = 'gregorianXlitFrench'
    NONE = 'none'


class ST_AlgClass(ST_BaseEnumType):
    Hash = 'hash'
    Custom = 'custom'


class ST_CryptProv(ST_BaseEnumType):
    RsaAES = 'rsaAES'
    RsaFull = 'rsaFull'
    Custom = 'custom'


class ST_AlgType(ST_BaseEnumType):
    TypeAny = 'typeAny'
    Custom = 'custom'


# <xsd:restriction base="xsd:string"/>
ST_ColorType = NewType('ST_ColorType', str)

# <xsd:pattern value="\{[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}\}"/>
ST_Guid = NewType('ST_Guid', str)


class ST_OnOff1(ST_BaseEnumType):
    On = 'on'
    Off = 'off'


class ST_OnOff(ST_BaseEnumType):
    """开关 17.17.4 22.9.2.7 ST_OnOff (开/关值)

    此简单类型为 WordprocessingML 文档中定义的任何二进制（true 或 false）属性指定一组值。

    值 1 或 true 指定应打开该属性。 这是该属性的默认值，当父元素存在时隐含该值，但该属性被省略。

    值 0 或 false 指定应显式关闭该属性。

    此简单类型的内容是 W3C XML Schema 布尔数据类型的限制

    <xsd:union memberTypes="xsd:boolean ST_OnOff1"/>
    """

    One = '1'
    Zero = '0'
    On = 'on'
    Off = 'off'
    false = 'false'
    true = 'true'

    def __bool__(self) -> bool:
        return self.value in {'on', '1'}


# <xsd:restriction base="xsd:string"/>
ST_String = NewType('ST_String', str)

CT_String = OxmlBaseElement


class ST_XmlName(ST_BaseType[str, str]):
    """xml名称"""

    def _validate(self: Self) -> None:
        """xml名称"""

        if not (1 <= len(self._val) <= 255):
            msg = f'长度最大值应为255,最小值为1: {self._val}'
            raise OxmlAttributeValidateError(msg)

        self._python_val = self._val


class ST_TrueFalse(ST_BaseEnumType):
    true = 'true'
    false = 'false'
    true1 = 't'
    false1 = 'f'


class ST_TrueFalseBlank(ST_BaseEnumType):
    true = 'true'
    false = 'false'
    true1 = 't'
    false1 = 'f'
    Blank = ''
    true2 = 'True'
    false2 = 'False'


class ST_UnsignedDecimalNumber(int):
    """无符号十进制数值

    Unsigned Decimal Number Value
    """



class ST_UniversalMeasure(int):
    """通用测量
    22.9.2.15

    Universal Measurement

    eg:

        123456mm

        123456cm

        ...
    """


def to_ST_UniversalMeasure(val: str) -> ST_UniversalMeasure:
    """无符号大浮点数"""

    float_part, units_part = val[:-2], val[-2:]
    quantity = float(float_part)
    multiplier = {
        'mm': 36000,
        'cm': 360000,
        'in': 914400,
        'pt': 12700,
        'pc': 152400,
        'pi': 152400,
    }[units_part]

    emu_value = int(round(quantity * multiplier))

    return ST_UniversalMeasure(emu_value)


class ST_PositiveUniversalMeasure(int):
    r"""正向通用测量
    22.9.2.12

    Positive Universal Measurement

    <xsd:pattern value="[0-9]+(\.[0-9]+)?(mm|cm|in|pt|pc|pi)"/>
    """


def to_ST_PositiveUniversalMeasure(val: str) -> ST_PositiveUniversalMeasure:
    """正向通用测量"""

    pyval = to_ST_UniversalMeasure(val)

    if pyval < 0:
        msg = f'测量数应为大于0的正数: {pyval}'
        raise OxmlAttributeValidateError(msg)

    return ST_PositiveUniversalMeasure(pyval)


# 22.9.2.14
# 积极的普遍测量
# Measurement in Twentieths of a Point
# <xsd:simpleType name="ST_TwipsMeasure">
#     <xsd:union memberTypes="ST_UnsignedDecimalNumber ST_PositiveUniversalMeasure"/>
# </xsd:simpleType>
# ST_TwipsMeasure = Union[ST_UnsignedDecimalNumber, ST_PositiveUniversalMeasure]


class ST_TwipsMeasure(int): ...


def to_ST_TwipsMeasure(_val: AnyStr) -> ST_TwipsMeasure:
    val = utils.AnyStrToStr(_val)

    if not val[-2:].isdigit():
        return ST_TwipsMeasure(to_ST_PositiveUniversalMeasure(val))

    return ST_TwipsMeasure(int(val) / 20)


class ST_VerticalAlignRun(ST_BaseEnumType):
    """垂直定位位置
    22.9.2.17

    Vertical Positioning Location
    """

    Baseline = 'baseline'
    Superscript = 'superscript'
    Subscript = 'subscript'


ST_Xstring = NewType('ST_Xstring', str)


class ST_XAlign(ST_BaseEnumType):
    """水平对齐位置
    22.9.2.18

    Horizontal Alignment Location
    """

    Left = 'left'
    Center = 'center'
    Right = 'right'
    Inside = 'inside'
    Outside = 'outside'


class ST_YAlign(ST_BaseEnumType):
    """垂直对齐位置
    22.9.2.18

    Vertical Alignment Location
    """

    Inline = 'inline'
    Top = 'top'
    Center = 'center'
    Bottom = 'bottom'
    Inside = 'inside'
    Outside = 'outside'


class ST_ConformanceClass(ST_BaseEnumType):
    """文档一致性等级值
    22.9.2.2

    Document Conformance Class Value
    """

    Strict = 'strict'
    """指定文档符合 Office Open XML 严格(Strict) 模式。"""

    Transitional = 'transitional'
    """指定文档符合 Office Open XML 过渡(Transitional) 模式。"""


ST_Percentage = NewType('ST_Percentage', float)
r"""带符号的百分比值
22.9.2.9

Percentage Value with Sign

<xsd:pattern value="-?[0-9]+(\.[0-9]+)?%"/>
"""


def to_ST_Percentage(val: str) -> ST_Percentage:
    """转为百分比"""

    # if not val.endswith("%"):
    #     logger.warning(f"预期外的值: {val}")

    if val.isdigit():
        # 800000 -> 0.8 = 80%
        return ST_Percentage(int(val) / (1000 * 100))

    if val.endswith('%'):
        # -10% -> -0.1
        # 50%  ->  0.5

        return ST_Percentage(int(val[:-1]) / 100.0)

    # -30000 -> -0.3 = -30%
    return ST_Percentage(int(val) / (1000 * 100))


ST_FixedPercentage = NewType('ST_FixedPercentage', float)
r"""带符号的固定百分比值
22.9.2.3

Fixed Percentage Value with Sign

<xsd:pattern value="-?((100)|([0-9][0-9]?))(\.[0-9][0-9]?)?%"/>

例如:

<w:tcPr>
    <w:tcW w:type="pct" w:w="33.3%" />
</w:pPr>
"""


def to_FixedPercentage(val: str) -> ST_FixedPercentage:
    # -10% -> -0.1
    # 50%  ->  0.5

    return ST_FixedPercentage(to_ST_Percentage(val))


# 继承自 ST_Percentage
ST_PositivePercentage = NewType('ST_PositivePercentage', float)
r"""带符号的正百分比值

22.9.2.11

Positive Percentage Value with Sign

<xsd:pattern value="[0-9]+(\.[0-9]+)?%"/>
"""


def to_ST_PositivePercentage(val: str) -> ST_PositivePercentage:
    """返回百分比, 一个浮点数, 0-1 之间"""

    if val.startswith('-'):
        msg = f'预期外的值: {val}'
        raise OxmlAttributeValidateError(msg)

    return ST_PositivePercentage(to_ST_Percentage(val))


# 继承自 ST_Percentage
ST_PositiveFixedPercentage = NewType('ST_PositiveFixedPercentage', float)
r"""带符号的正固定百分比值

22.9.2.10

Positive Fixed Percentage Value with Sign

<xsd:pattern value="((100)|([0-9][0-9]?))(\.[0-9][0-9]?)?%"/>
"""


def to_ST_PositiveFixedPercentage(val: str) -> ST_PositiveFixedPercentage:
    r"""带符号的正固定百分比值
    22.9.2.10

    Positive Fixed Percentage Value with Sign

    <xsd:pattern value="((100)|([0-9][0-9]?))(\.[0-9][0-9]?)?%"/>
    """

    # -10% -> -0.1
    # 50%  ->  0.5

    return ST_PositiveFixedPercentage(to_ST_Percentage(val))


# shared-bibliography.xsd 使用 ST_String, 这里用CT_String替换
shared_common_st_namespace = lookup.get_namespace(namespace_s)
shared_common_st_namespace[None] = OxmlBaseElement
shared_common_st_namespace['Last'] = CT_String
shared_common_st_namespace['First'] = CT_String
shared_common_st_namespace['Middle'] = CT_String
shared_common_st_namespace['Corporate'] = CT_String
shared_common_st_namespace['SelectedStyle'] = CT_String
shared_common_st_namespace['StyleName'] = CT_String
shared_common_st_namespace['URI'] = CT_String
shared_common_st_namespace['AbbreviatedCaseNumber'] = CT_String
shared_common_st_namespace['AlbumTitle'] = CT_String
shared_common_st_namespace['Author'] = CT_String
shared_common_st_namespace['BookTitle'] = CT_String
shared_common_st_namespace['Broadcaster'] = CT_String
shared_common_st_namespace['BroadcastTitle'] = CT_String
shared_common_st_namespace['CaseNumber'] = CT_String
shared_common_st_namespace['ChapterNumber'] = CT_String
shared_common_st_namespace['City'] = CT_String
shared_common_st_namespace['Comments'] = CT_String
shared_common_st_namespace['ConferenceName'] = CT_String
shared_common_st_namespace['CountryRegion'] = CT_String
shared_common_st_namespace['Court'] = CT_String
shared_common_st_namespace['Day'] = CT_String
shared_common_st_namespace['DayAccessed'] = CT_String
shared_common_st_namespace['Department'] = CT_String
shared_common_st_namespace['Distributor'] = CT_String
shared_common_st_namespace['Edition'] = CT_String
shared_common_st_namespace['Guid'] = CT_String
shared_common_st_namespace['Institution'] = CT_String
shared_common_st_namespace['InternetSiteTitle'] = CT_String
shared_common_st_namespace['Issue'] = CT_String
shared_common_st_namespace['JournalName'] = CT_String
shared_common_st_namespace['LCID'] = CT_String
shared_common_st_namespace['Medium'] = CT_String
shared_common_st_namespace['Month'] = CT_String
shared_common_st_namespace['MonthAccessed'] = CT_String
shared_common_st_namespace['NumberVolumes'] = CT_String
shared_common_st_namespace['Pages'] = CT_String
shared_common_st_namespace['PatentNumber'] = CT_String
shared_common_st_namespace['PeriodicalTitle'] = CT_String
shared_common_st_namespace['ProductionCompany'] = CT_String
shared_common_st_namespace['PublicationTitle'] = CT_String
shared_common_st_namespace['Publisher'] = CT_String
shared_common_st_namespace['RecordingNumber'] = CT_String
shared_common_st_namespace['RefOrder'] = CT_String
shared_common_st_namespace['Reporter'] = CT_String
shared_common_st_namespace['SourceType'] = CT_String
shared_common_st_namespace['ShortTitle'] = CT_String
shared_common_st_namespace['StandardNumber'] = CT_String
shared_common_st_namespace['StateProvince'] = CT_String
shared_common_st_namespace['Station'] = CT_String
shared_common_st_namespace['Tag'] = CT_String
shared_common_st_namespace['Theater'] = CT_String
shared_common_st_namespace['ThesisType'] = CT_String
shared_common_st_namespace['Title'] = CT_String
shared_common_st_namespace['Type'] = CT_String
shared_common_st_namespace['URL'] = CT_String
shared_common_st_namespace['Version'] = CT_String
shared_common_st_namespace['Volume'] = CT_String
shared_common_st_namespace['Year'] = CT_String
shared_common_st_namespace['YearAccessed'] = CT_String
