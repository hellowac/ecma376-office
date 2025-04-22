"""颜色相关类的封装"""

from typing import Generic, NamedTuple, Optional, TypeVar, Union

from ecma376_office.oxml.base import OxmlBaseElement
from ecma376_office.oxml.dml.main import (
    CT_ColorScheme,
    CT_HslColor,
    CT_PresetColor,
    CT_SchemeColor,
    CT_ScRgbColor,
    CT_SRgbColor,
    CT_SystemColor,
    EG_ColorTransform,
    ST_ColorSchemeIndex,
)

CT_ColorTypesRequire = CT_ScRgbColor | CT_SRgbColor | CT_HslColor | CT_SystemColor | CT_SchemeColor | CT_PresetColor


CT_ColorTypes = Optional[CT_ColorTypesRequire]


T = TypeVar('T', bound=EG_ColorTransform)
# SubBaseElement = TypeVar("SubBaseElement", bound=OxmlBaseElement)


class ColorTransformBase(Generic[T]):
    """颜色变换基类"""

    def __init__(self, oxml: T) -> None:
        self.oxml = oxml

    @property
    def tint(self):
        return self.oxml.tint

    @property
    def shade(self):
        return self.oxml.shade

    @property
    def comp(self):
        return self.oxml.comp

    @property
    def inv(self):
        return self.oxml.inv

    @property
    def gray(self):
        return self.oxml.gray

    @property
    def alpha(self):
        return self.oxml.alpha

    @property
    def alpha_off(self):
        return self.oxml.alpha_off

    @property
    def alpha_mod(self):
        return self.oxml.alpha_mod

    @property
    def hue(self):
        return self.oxml.hue

    @property
    def hue_off(self):
        return self.oxml.hue_off

    @property
    def hue_mod(self):
        return self.oxml.hue_mod

    @property
    def sat(self):
        return self.oxml.sat

    @property
    def sat_off(self):
        return self.oxml.sat_off

    @property
    def sat_mod(self):
        return self.oxml.sat_mod

    @property
    def lum(self):
        return self.oxml.lum

    @property
    def lum_off(self):
        return self.oxml.lum_off

    @property
    def lum_mod(self):
        return self.oxml.lum_mod

    @property
    def red(self):
        return self.oxml.red

    @property
    def red_off(self):
        return self.oxml.red_off

    @property
    def red_mod(self):
        return self.oxml.red_mod

    @property
    def green(self):
        return self.oxml.green

    @property
    def green_off(self):
        return self.oxml.green_off

    @property
    def green_mod(self):
        return self.oxml.green_mod

    @property
    def blue(self):
        return self.oxml.blue

    @property
    def blue_off(self):
        return self.oxml.blue_off

    @property
    def blue_mod(self):
        return self.oxml.blue_mod

    @property
    def gamma(self):
        """伽玛变换

        20.1.2.3.8 gamma (Gamma)

        该元素指定生成应用程序渲染的输出颜色应该是输入颜色的 sRGB gamma 偏移。
        """
        return self.oxml.gamma

    @property
    def inv_gamma(self):
        """逆伽玛变换

        20.1.2.3.18 invGamma (Inverse Gamma)

        该元素指定生成应用程序渲染的输出颜色应该是输入颜色的逆 sRGB gamma 偏移
        """
        return self.oxml.inv_gamma


class ScrgbColor(ColorTransformBase[CT_ScRgbColor]):
    """Scrgb类型的颜色"""

    @property
    def r(self):
        """红色的值"""

        return self.oxml.r

    @property
    def g(self):
        """绿色的值"""

        return self.oxml.g

    @property
    def b(self):
        """蓝色的值"""

        return self.oxml.b


class SrgbColor(ColorTransformBase[CT_SRgbColor]):
    """Srgb类型的颜色"""

    @property
    def value(self):
        """蓝色的值"""

        return self.oxml.value


class HslColor(ColorTransformBase[CT_HslColor]):
    """Hsl类型的颜色"""

    @property
    def attr_hue(self):
        """色调"""

        return self.oxml.attr_hue

    @property
    def attr_sat(self):
        """饱和度"""

        return self.oxml.attr_sat

    @property
    def attr_lum(self):
        """亮度"""

        return self.oxml.attr_lum


class SystemColor(ColorTransformBase[CT_SystemColor]):
    """System类型的颜色"""

    @property
    def value(self):
        """指定系统颜色值。"""

        return self.oxml.value

    @property
    def last_color(self):
        """指定生成应用程序最后计算的颜色值。"""

        return self.oxml.last_color


class SchemeColor(ColorTransformBase[CT_SchemeColor]):
    """主题方案类型的颜色"""

    @property
    def value(self):
        """主题方案的颜色值"""

        return self.oxml.value


class PresetColor(ColorTransformBase[CT_PresetColor]):
    """Scrg类型的颜色"""

    @property
    def value(self):
        """指定实际的预设颜色值。"""

        return self.oxml.value


# ------------- 颜色工厂函数 ----------------

ColorTypesRequire = Union[ScrgbColor, SrgbColor, HslColor, SystemColor, SchemeColor, PresetColor]

ColorTypes = Optional[ColorTypesRequire]


def color_factory(oxml: CT_ColorTypes) -> ColorTypes:
    """颜色构造工厂"""

    if isinstance(oxml, CT_ScRgbColor):
        return ScrgbColor(oxml)

    if isinstance(oxml, CT_SRgbColor):
        return SrgbColor(oxml)

    if isinstance(oxml, CT_HslColor):
        return HslColor(oxml)

    if isinstance(oxml, CT_SystemColor):
        return SystemColor(oxml)

    if isinstance(oxml, CT_SchemeColor):
        return SchemeColor(oxml)

    if isinstance(oxml, CT_PresetColor):
        return PresetColor(oxml)

    return None


def color_factory_require(oxml: CT_ColorTypesRequire) -> ColorTypesRequire:
    """颜色构造工厂"""

    if isinstance(oxml, CT_ScRgbColor):
        return ScrgbColor(oxml)

    if isinstance(oxml, CT_SRgbColor):
        return SrgbColor(oxml)

    if isinstance(oxml, CT_HslColor):
        return HslColor(oxml)

    if isinstance(oxml, CT_SystemColor):
        return SystemColor(oxml)

    if isinstance(oxml, CT_SchemeColor):
        return SchemeColor(oxml)

    if isinstance(oxml, CT_PresetColor):
        return PresetColor(oxml)
    return None


# 颜色映射类的封装 / CT_ColorMapping
# https://docs.python.org/zh-cn/3.10/library/typing.html#typing.NamedTuple


class ColorMapping(NamedTuple):
    oxml: OxmlBaseElement
    bg1: ST_ColorSchemeIndex
    tx1: ST_ColorSchemeIndex
    bg2: ST_ColorSchemeIndex
    tx2: ST_ColorSchemeIndex
    accent1: ST_ColorSchemeIndex
    accent2: ST_ColorSchemeIndex
    accent3: ST_ColorSchemeIndex
    accent4: ST_ColorSchemeIndex
    accent5: ST_ColorSchemeIndex
    accent6: ST_ColorSchemeIndex
    hlink: ST_ColorSchemeIndex
    folHlink: ST_ColorSchemeIndex


# ColorMapping = namedtuple(
#     "ColorMapping",
#     [
#         "bg1",
#         "tx1",
#         "bg2",
#         "tx2",
#         "accent1",
#         "accent2",
#         "accent3",
#         "accent4",
#         "accent5",
#         "accent6",
#         "hlink",
#         "folHlink",
#     ],
# )


class ColorScheme:
    """颜色方案封装"""

    def __init__(self, oxml: CT_ColorScheme) -> None:
        """颜色方案封装"""
        self.oxml = oxml

    @property
    def name(self):
        """方案名称"""

        return self.oxml.name

    @property
    def dk1(self):
        """深色1"""

        return color_factory(self.oxml.dark1.color)

    @property
    def dk2(self):
        """深色2"""

        return color_factory(self.oxml.dark2.color)

    @property
    def lt1(self):
        """浅色1"""

        return color_factory(self.oxml.light1.color)

    @property
    def lt2(self):
        """浅色2"""

        return color_factory(self.oxml.light2.color)

    @property
    def accent1(self):
        """强调色1"""

        return color_factory(self.oxml.accent1.color)

    @property
    def accent2(self):
        """强调色2"""

        return color_factory(self.oxml.accent2.color)

    @property
    def accent3(self):
        """强调色3"""

        return color_factory(self.oxml.accent3.color)

    @property
    def accent4(self):
        """强调色4"""

        return color_factory(self.oxml.accent4.color)

    @property
    def accent5(self):
        """强调色5"""

        return color_factory(self.oxml.accent5.color)

    @property
    def accent6(self):
        """强调色6"""

        return color_factory(self.oxml.accent6.color)

    @property
    def hlink(self):
        """超链接颜色"""

        return color_factory(self.oxml.hyperlink.color)

    @property
    def folHlink(self):
        """已关注超链接颜色"""

        return color_factory(self.oxml.followed_hyperlink.color)
