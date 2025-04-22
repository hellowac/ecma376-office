from __future__ import annotations

import colorsys
import logging
import math
from enum import Enum
from typing import NamedTuple, Optional, Union

import numpy as np

from ecma376_office.dml.style.color import (
    ColorMapping,
    ColorScheme,
    ColorTransformBase,
    ColorTypes,
    ColorTypesRequire,
    HslColor,
    PresetColor,
    SchemeColor,
    ScrgbColor,
    SrgbColor,
    SystemColor,
)
from ecma376_office.dml.tool.common import ThemeTool
from ecma376_office.oxml.dml.main import (
    ST_ColorSchemeIndex,
    ST_SchemeColorVal,
    to_ST_PositiveFixedPercentage,
)
from ecma376_office.pml.slide import Slide
from ecma376_office.pml.slide_layout import SlideLayout
from ecma376_office.pml.slide_master import SlideMaster

logger = logging.getLogger(__name__)


SlideTypes = Union[Slide, SlideLayout, SlideMaster]


class BaseEnumType(Enum):
    """参考:

    合法的枚举成员和属性

    https://docs.python.org/zh-cn/3.10/library/enum.html#allowed-members-and-attributes-of-enumerations
    """

    @classmethod
    def has_value(cls, value: str):
        """判断是否拥有某个值"""

        return value in [e.value for e in cls]


class RGBAColor(NamedTuple):
    """RGB 颜色

    所有浏览器都支持 RGB 颜色值。

    RGB 颜色值通过以下方式指定:

    rgb(red, green, blue)

    每个参数（红色、绿色和蓝色）定义颜色的强度，其值介于 0 到 255 之间。

    例如，rgb(255, 0, 0) 显示为红色，因为红色设置为其最高值 (255)，而其他两个（绿色和蓝色）设置为 0。

    另一个例子，rgb(0, 255, 0) 显示为绿色，因为绿色设置为其最高值 (255)，而其他两个（红色和蓝色）设置为 0。

    要显示黑色，请将所有颜色参数设置为 0，如下所示: rgb(0, 0, 0)。

    要显示白色，请将所有颜色参数设置为 255，如下所示: rgb(255, 255, 255)。
    """

    r: np.uint8  # 0-255
    g: np.uint8  # 0-255
    b: np.uint8  # 0-255
    a: np.float_ = np.float_(1.0)  # 0-1

    def __str__(self):
        """返回十六进制字符串 rgb 值，例如 '3C2F80'"""

        if self.a == 1:
            return f'{self.r:02X}{self.g:02X}{self.b:02X}'

        alpha = int(255 * self.a)
        return f'{self.r:02X}{self.g:02X}{self.b:02X}{alpha:02X}'

    @classmethod
    def from_string(cls, rgb_hex_str):
        """从 RGB 颜色十六进制字符串(如“3C2F80”)返回一个新实例。"""
        r = np.uint8(int(rgb_hex_str[:2], 16))
        g = np.uint8(int(rgb_hex_str[2:4], 16))
        b = np.uint8(int(rgb_hex_str[4:], 16))
        return cls(r, g, b)

    @property
    def rgb_html(self):
        return f'#{self.r:02X}{self.g:02X}{self.b:02X}'


class HSLAColor(NamedTuple):
    """HSL 颜色

    - Hue

        色调是色轮上从 0 到 360 的度数。0（或 360）是红色，120 是绿色，240 是蓝色。

    - Saturation:

        饱和度可以描述为颜色的强度。 它是从 0% 到 100% 的百分比值。

        100% 是全彩，没有灰色阴影。

        50%是50%灰色，但你仍然可以看到颜色。

        0%是完全灰色的； 你再也看不到颜色了。

    - Lightness:

        颜色的明度可以描述为您想要赋予该颜色多少光，其中0%表示没有光（暗），50%表示50%光（既不暗也不亮），100%表示全亮。
    """

    h: np.uint16  # 0-360
    s: np.float_  # 0-1 百分比
    l: np.float_  # 0-1 百分比
    a: np.float_ = np.float_(1.0)  # 0-1

    def __str__(self):
        """返回十六进制字符串 hsl 值，例如 '3C2F80'"""

        if self.a == 1:
            return f'hsl({self.h} {self.s * 100}% {self.l * 100}%)'

        alpha = self.a * 255
        return f'hsla({self.h} {self.s * 100}% {self.l * 100}% {alpha:X})'


class PresetColorValues(BaseEnumType):
    """预置颜色的rgb值

    参考:

    https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter20/main/simple_types/#2011048-st_presetcolorval-预设颜色值
    """

    aliceBlue = RGBAColor(np.uint8(240), np.uint8(248), np.uint8(255))  # 爱丽丝蓝
    antiqueWhite = RGBAColor(np.uint8(250), np.uint8(235), np.uint8(215))  # 古董白
    aqua = RGBAColor(np.uint8(0), np.uint8(255), np.uint8(255))  # 水绿
    aquamarine = RGBAColor(np.uint8(127), np.uint8(255), np.uint8(212))  # 碧绿
    azure = RGBAColor(np.uint8(240), np.uint8(255), np.uint8(255))  # 天蓝
    beige = RGBAColor(np.uint8(245), np.uint8(245), np.uint8(220))  # 米色
    bisque = RGBAColor(np.uint8(255), np.uint8(228), np.uint8(196))  # 橙黄
    black = RGBAColor(np.uint8(0), np.uint8(0), np.uint8(0))  # 黑色
    blanchedAlmond = RGBAColor(np.uint8(255), np.uint8(235), np.uint8(205))  # 杏仁白
    blue = RGBAColor(np.uint8(0), np.uint8(0), np.uint8(255))  # 蓝色
    blueViolet = RGBAColor(np.uint8(138), np.uint8(43), np.uint8(226))
    brown = RGBAColor(np.uint8(165), np.uint8(42), np.uint8(42))
    burlyWood = RGBAColor(np.uint8(222), np.uint8(184), np.uint8(135))
    cadetBlue = RGBAColor(np.uint8(95), np.uint8(158), np.uint8(160))
    chartreuse = RGBAColor(np.uint8(127), np.uint8(255), np.uint8(0))
    chocolate = RGBAColor(np.uint8(210), np.uint8(105), np.uint8(30))
    coral = RGBAColor(np.uint8(255), np.uint8(127), np.uint8(80))
    cornflowerBlue = RGBAColor(np.uint8(100), np.uint8(149), np.uint8(237))
    cornsilk = RGBAColor(np.uint8(255), np.uint8(248), np.uint8(220))
    crimson = RGBAColor(np.uint8(220), np.uint8(20), np.uint8(60))
    cyan = RGBAColor(np.uint8(0), np.uint8(255), np.uint8(255))
    darkBlue = RGBAColor(np.uint8(0), np.uint8(0), np.uint8(139))
    darkCyan = RGBAColor(np.uint8(0), np.uint8(139), np.uint8(139))
    darkGoldenrod = RGBAColor(np.uint8(184), np.uint8(134), np.uint8(11))
    darkGray = RGBAColor(np.uint8(169), np.uint8(169), np.uint8(169))
    darkGreen = RGBAColor(np.uint8(0), np.uint8(100), np.uint8(0))
    darkGrey = RGBAColor(np.uint8(169), np.uint8(169), np.uint8(169))
    darkKhaki = RGBAColor(np.uint8(189), np.uint8(183), np.uint8(107))
    darkMagenta = RGBAColor(np.uint8(139), np.uint8(0), np.uint8(139))
    darkOliveGreen = RGBAColor(np.uint8(85), np.uint8(107), np.uint8(47))
    darkOrange = RGBAColor(np.uint8(255), np.uint8(140), np.uint8(0))
    darkOrchid = RGBAColor(np.uint8(153), np.uint8(50), np.uint8(204))
    darkRed = RGBAColor(np.uint8(139), np.uint8(0), np.uint8(0))
    darkSalmon = RGBAColor(np.uint8(233), np.uint8(150), np.uint8(122))
    darkSeaGreen = RGBAColor(np.uint8(143), np.uint8(188), np.uint8(143))
    darkSlateBlue = RGBAColor(np.uint8(72), np.uint8(61), np.uint8(139))
    darkSlateGray = RGBAColor(np.uint8(47), np.uint8(79), np.uint8(79))
    darkSlateGrey = RGBAColor(np.uint8(47), np.uint8(79), np.uint8(79))
    darkTurquoise = RGBAColor(np.uint8(0), np.uint8(206), np.uint8(209))
    darkViolet = RGBAColor(np.uint8(148), np.uint8(0), np.uint8(211))
    deepPink = RGBAColor(np.uint8(255), np.uint8(20), np.uint8(147))
    deepSkyBlue = RGBAColor(np.uint8(0), np.uint8(191), np.uint8(255))
    dimGray = RGBAColor(np.uint8(105), np.uint8(105), np.uint8(105))
    dimGrey = RGBAColor(np.uint8(105), np.uint8(105), np.uint8(105))
    dkBlue = RGBAColor(np.uint8(0), np.uint8(0), np.uint8(139))
    dkCyan = RGBAColor(np.uint8(0), np.uint8(139), np.uint8(139))
    dkGoldenrod = RGBAColor(np.uint8(184), np.uint8(134), np.uint8(11))
    dkGray = RGBAColor(np.uint8(169), np.uint8(169), np.uint8(169))
    dkGreen = RGBAColor(np.uint8(0), np.uint8(100), np.uint8(0))
    dkGrey = RGBAColor(np.uint8(169), np.uint8(169), np.uint8(169))
    dkKhaki = RGBAColor(np.uint8(189), np.uint8(183), np.uint8(107))
    dkMagenta = RGBAColor(np.uint8(139), np.uint8(0), np.uint8(139))
    dkOliveGreen = RGBAColor(np.uint8(85), np.uint8(107), np.uint8(47))
    dkOrange = RGBAColor(np.uint8(255), np.uint8(140), np.uint8(0))
    dkOrchid = RGBAColor(np.uint8(153), np.uint8(50), np.uint8(204))
    dkRed = RGBAColor(np.uint8(139), np.uint8(0), np.uint8(0))
    dkSalmon = RGBAColor(np.uint8(233), np.uint8(150), np.uint8(122))
    dkSeaGreen = RGBAColor(np.uint8(143), np.uint8(188), np.uint8(139))
    dkSlateBlue = RGBAColor(np.uint8(72), np.uint8(61), np.uint8(139))
    dkSlateGray = RGBAColor(np.uint8(47), np.uint8(79), np.uint8(79))
    dkSlateGrey = RGBAColor(np.uint8(47), np.uint8(79), np.uint8(79))
    dkTurquoise = RGBAColor(np.uint8(0), np.uint8(206), np.uint8(209))
    dkViolet = RGBAColor(np.uint8(148), np.uint8(0), np.uint8(211))
    dodgerBlue = RGBAColor(np.uint8(30), np.uint8(144), np.uint8(255))
    firebrick = RGBAColor(np.uint8(178), np.uint8(34), np.uint8(34))
    floralWhite = RGBAColor(np.uint8(255), np.uint8(250), np.uint8(240))
    forestGreen = RGBAColor(np.uint8(34), np.uint8(139), np.uint8(34))
    fuchsia = RGBAColor(np.uint8(255), np.uint8(0), np.uint8(255))
    gainsboro = RGBAColor(np.uint8(220), np.uint8(220), np.uint8(220))
    ghostWhite = RGBAColor(np.uint8(248), np.uint8(248), np.uint8(255))
    gold = RGBAColor(np.uint8(255), np.uint8(215), np.uint8(0))
    goldenrod = RGBAColor(np.uint8(218), np.uint8(165), np.uint8(32))
    gray = RGBAColor(np.uint8(128), np.uint8(128), np.uint8(128))
    green = RGBAColor(np.uint8(0), np.uint8(128), np.uint8(0))
    greenYellow = RGBAColor(np.uint8(173), np.uint8(255), np.uint8(47))
    grey = RGBAColor(np.uint8(128), np.uint8(128), np.uint8(128))
    honeydew = RGBAColor(np.uint8(240), np.uint8(255), np.uint8(240))
    hotPink = RGBAColor(np.uint8(255), np.uint8(105), np.uint8(180))
    indianRed = RGBAColor(np.uint8(205), np.uint8(92), np.uint8(92))
    indigo = RGBAColor(np.uint8(75), np.uint8(0), np.uint8(130))
    ivory = RGBAColor(np.uint8(255), np.uint8(255), np.uint8(240))
    khaki = RGBAColor(np.uint8(240), np.uint8(230), np.uint8(140))
    lavender = RGBAColor(np.uint8(230), np.uint8(230), np.uint8(250))
    lavenderBlush = RGBAColor(np.uint8(255), np.uint8(240), np.uint8(245))
    lawnGreen = RGBAColor(np.uint8(124), np.uint8(252), np.uint8(0))
    lemonChiffon = RGBAColor(np.uint8(255), np.uint8(250), np.uint8(205))
    lightBlue = RGBAColor(np.uint8(173), np.uint8(216), np.uint8(230))
    lightCoral = RGBAColor(np.uint8(240), np.uint8(128), np.uint8(128))
    lightCyan = RGBAColor(np.uint8(224), np.uint8(255), np.uint8(255))
    lightGoldenrodYellow = RGBAColor(np.uint8(250), np.uint8(250), np.uint8(210))
    lightGray = RGBAColor(np.uint8(211), np.uint8(211), np.uint8(211))
    lightGreen = RGBAColor(np.uint8(144), np.uint8(238), np.uint8(144))
    lightGrey = RGBAColor(np.uint8(211), np.uint8(211), np.uint8(211))
    lightPink = RGBAColor(np.uint8(255), np.uint8(182), np.uint8(193))
    lightSalmon = RGBAColor(np.uint8(255), np.uint8(160), np.uint8(122))
    lightSeaGreen = RGBAColor(np.uint8(32), np.uint8(178), np.uint8(170))
    lightSkyBlue = RGBAColor(np.uint8(135), np.uint8(206), np.uint8(250))
    lightSlateGray = RGBAColor(np.uint8(119), np.uint8(136), np.uint8(153))
    lightSlateGrey = RGBAColor(np.uint8(119), np.uint8(136), np.uint8(153))
    lightSteelBlue = RGBAColor(np.uint8(176), np.uint8(196), np.uint8(222))
    lightYellow = RGBAColor(np.uint8(255), np.uint8(255), np.uint8(224))
    lime = RGBAColor(np.uint8(0), np.uint8(255), np.uint8(0))
    limeGreen = RGBAColor(np.uint8(50), np.uint8(205), np.uint8(50))
    linen = RGBAColor(np.uint8(250), np.uint8(240), np.uint8(230))
    ltBlue = RGBAColor(np.uint8(173), np.uint8(216), np.uint8(230))
    ltCoral = RGBAColor(np.uint8(240), np.uint8(128), np.uint8(128))
    ltCyan = RGBAColor(np.uint8(224), np.uint8(255), np.uint8(255))
    ltGoldenrodYellow = RGBAColor(np.uint8(250), np.uint8(250), np.uint8(120))
    ltGray = RGBAColor(np.uint8(211), np.uint8(211), np.uint8(211))
    ltGreen = RGBAColor(np.uint8(144), np.uint8(238), np.uint8(144))
    ltGrey = RGBAColor(np.uint8(211), np.uint8(211), np.uint8(211))
    ltPink = RGBAColor(np.uint8(255), np.uint8(182), np.uint8(193))
    ltSalmon = RGBAColor(np.uint8(255), np.uint8(160), np.uint8(122))
    ltSeaGreen = RGBAColor(np.uint8(32), np.uint8(178), np.uint8(170))
    ltSkyBlue = RGBAColor(np.uint8(135), np.uint8(206), np.uint8(250))
    ltSlateGray = RGBAColor(np.uint8(119), np.uint8(136), np.uint8(153))
    ltSlateGrey = RGBAColor(np.uint8(119), np.uint8(136), np.uint8(153))
    ltSteelBlue = RGBAColor(np.uint8(176), np.uint8(196), np.uint8(222))
    ltYellow = RGBAColor(np.uint8(255), np.uint8(255), np.uint8(224))
    magenta = RGBAColor(np.uint8(255), np.uint8(0), np.uint8(255))
    maroon = RGBAColor(np.uint8(128), np.uint8(0), np.uint8(0))
    medAquamarine = RGBAColor(np.uint8(102), np.uint8(205), np.uint8(170))
    medBlue = RGBAColor(np.uint8(0), np.uint8(0), np.uint8(205))
    mediumAquamarine = RGBAColor(np.uint8(102), np.uint8(205), np.uint8(170))
    mediumBlue = RGBAColor(np.uint8(0), np.uint8(0), np.uint8(205))
    mediumOrchid = RGBAColor(np.uint8(186), np.uint8(85), np.uint8(211))
    mediumPurple = RGBAColor(np.uint8(147), np.uint8(112), np.uint8(219))
    mediumSeaGreen = RGBAColor(np.uint8(60), np.uint8(179), np.uint8(113))
    mediumSlateBlue = RGBAColor(np.uint8(123), np.uint8(104), np.uint8(238))
    mediumSpringGreen = RGBAColor(np.uint8(0), np.uint8(250), np.uint8(154))
    mediumTurquoise = RGBAColor(np.uint8(72), np.uint8(209), np.uint8(204))
    mediumVioletRed = RGBAColor(np.uint8(199), np.uint8(21), np.uint8(133))
    medOrchid = RGBAColor(np.uint8(186), np.uint8(85), np.uint8(211))
    medPurple = RGBAColor(np.uint8(147), np.uint8(112), np.uint8(219))
    medSeaGreen = RGBAColor(np.uint8(60), np.uint8(179), np.uint8(113))
    medSlateBlue = RGBAColor(np.uint8(123), np.uint8(104), np.uint8(238))
    medSpringGreen = RGBAColor(np.uint8(0), np.uint8(250), np.uint8(154))
    medTurquoise = RGBAColor(np.uint8(72), np.uint8(209), np.uint8(204))
    medVioletRed = RGBAColor(np.uint8(199), np.uint8(21), np.uint8(133))
    midnightBlue = RGBAColor(np.uint8(25), np.uint8(25), np.uint8(112))
    mintCream = RGBAColor(np.uint8(245), np.uint8(255), np.uint8(250))
    mistyRose = RGBAColor(np.uint8(255), np.uint8(228), np.uint8(225))
    moccasin = RGBAColor(np.uint8(255), np.uint8(228), np.uint8(181))
    navajoWhite = RGBAColor(np.uint8(255), np.uint8(222), np.uint8(173))
    navy = RGBAColor(np.uint8(0), np.uint8(0), np.uint8(128))
    oldLace = RGBAColor(np.uint8(253), np.uint8(245), np.uint8(230))
    olive = RGBAColor(np.uint8(128), np.uint8(128), np.uint8(0))
    oliveDrab = RGBAColor(np.uint8(107), np.uint8(142), np.uint8(35))
    orange = RGBAColor(np.uint8(255), np.uint8(165), np.uint8(0))
    orangeRed = RGBAColor(np.uint8(255), np.uint8(69), np.uint8(0))
    orchid = RGBAColor(np.uint8(218), np.uint8(112), np.uint8(214))
    paleGoldenrod = RGBAColor(np.uint8(238), np.uint8(232), np.uint8(170))
    paleGreen = RGBAColor(np.uint8(152), np.uint8(251), np.uint8(152))
    paleTurquoise = RGBAColor(np.uint8(175), np.uint8(238), np.uint8(238))
    paleVioletRed = RGBAColor(np.uint8(219), np.uint8(112), np.uint8(147))
    papayaWhip = RGBAColor(np.uint8(255), np.uint8(239), np.uint8(213))
    peachPuff = RGBAColor(np.uint8(255), np.uint8(218), np.uint8(185))
    peru = RGBAColor(np.uint8(205), np.uint8(133), np.uint8(63))
    pink = RGBAColor(np.uint8(255), np.uint8(192), np.uint8(203))
    plum = RGBAColor(np.uint8(221), np.uint8(160), np.uint8(221))
    powderBlue = RGBAColor(np.uint8(176), np.uint8(224), np.uint8(230))
    purple = RGBAColor(np.uint8(128), np.uint8(0), np.uint8(128))
    red = RGBAColor(np.uint8(255), np.uint8(0), np.uint8(0))
    rosyBrown = RGBAColor(np.uint8(188), np.uint8(143), np.uint8(143))
    royalBlue = RGBAColor(np.uint8(65), np.uint8(105), np.uint8(225))
    saddleBrown = RGBAColor(np.uint8(139), np.uint8(69), np.uint8(19))
    salmon = RGBAColor(np.uint8(250), np.uint8(128), np.uint8(114))
    sandyBrown = RGBAColor(np.uint8(244), np.uint8(164), np.uint8(96))
    seaGreen = RGBAColor(np.uint8(46), np.uint8(139), np.uint8(87))
    seaShell = RGBAColor(np.uint8(255), np.uint8(245), np.uint8(238))
    sienna = RGBAColor(np.uint8(160), np.uint8(82), np.uint8(45))
    silver = RGBAColor(np.uint8(192), np.uint8(192), np.uint8(192))
    skyBlue = RGBAColor(np.uint8(135), np.uint8(206), np.uint8(235))
    slateBlue = RGBAColor(np.uint8(106), np.uint8(90), np.uint8(205))
    slateGray = RGBAColor(np.uint8(112), np.uint8(128), np.uint8(144))
    slateGrey = RGBAColor(np.uint8(112), np.uint8(128), np.uint8(144))
    snow = RGBAColor(np.uint8(255), np.uint8(250), np.uint8(250))
    springGreen = RGBAColor(np.uint8(0), np.uint8(255), np.uint8(127))
    steelBlue = RGBAColor(np.uint8(70), np.uint8(130), np.uint8(180))
    tan = RGBAColor(np.uint8(210), np.uint8(180), np.uint8(140))
    teal = RGBAColor(np.uint8(0), np.uint8(128), np.uint8(128))
    thistle = RGBAColor(np.uint8(216), np.uint8(191), np.uint8(216))
    tomato = RGBAColor(np.uint8(255), np.uint8(99), np.uint8(71))
    turquoise = RGBAColor(np.uint8(64), np.uint8(224), np.uint8(208))
    violet = RGBAColor(np.uint8(238), np.uint8(130), np.uint8(238))
    wheat = RGBAColor(np.uint8(245), np.uint8(222), np.uint8(179))
    white = RGBAColor(np.uint8(255), np.uint8(255), np.uint8(255))
    whiteSmoke = RGBAColor(np.uint8(245), np.uint8(245), np.uint8(245))
    yellow = RGBAColor(np.uint8(255), np.uint8(255), np.uint8(0))
    yellowGreen = RGBAColor(np.uint8(154), np.uint8(205), np.uint8(50))


class ColorTool:
    """颜色工具类"""

    @classmethod
    def extract_schema_color(cls, color: SchemeColor, slide: SlideTypes):
        """提取schema color 的值

        1. 从 slide > layout > master 中依次获取颜色映射: color_map
        2. 然后根据 schema_color 的值，找到schem_color 在 颜色方案(color_schema) 中的索引
        3. 根据 索引，获取 主题覆盖(theme_override) 或 主题(theme) 中的具体的颜色。
        """

        # logger.debug(f"主题(schema)颜色key为 {color.value.value =}")

        color_map = ThemeTool.choice_color_map(slide)
        color_schema = ThemeTool.choice_color_schema(slide)

        # logger.debug(f"颜色方案(color Schema)名称为: {color_schema.name = }")

        return cls.extract_schema_index(color_map, color_schema, color.value)

        # logger.debug(f"主题(schema)颜色: {schema_color = }")


    @classmethod
    def extract_schema_index(
        cls,
        color_map: ColorMapping,
        color_schema: ColorScheme,
        schema_color_value: ST_SchemeColorVal,
    ):
        # logger.info(f"{color_map = }")
        # logger.info(f"{schema_color_value = }")
        # logger.info(color_map.oxml.xml)

        scheme_idx: Optional[ST_ColorSchemeIndex] = None

        index_map: dict[ST_SchemeColorVal, Optional[ST_ColorSchemeIndex]] = {
            ST_SchemeColorVal.Background1: color_map.bg1,
            ST_SchemeColorVal.Background2: color_map.bg2,
            ST_SchemeColorVal.Text1: color_map.tx1,
            ST_SchemeColorVal.Text2: color_map.tx2,
            ST_SchemeColorVal.Accent1: color_map.accent1,
            ST_SchemeColorVal.Accent2: color_map.accent2,
            ST_SchemeColorVal.Accent3: color_map.accent3,
            ST_SchemeColorVal.Accent4: color_map.accent4,
            ST_SchemeColorVal.Accent5: color_map.accent5,
            ST_SchemeColorVal.Accent6: color_map.accent6,
            ST_SchemeColorVal.Hyperlink: color_map.hlink,
            ST_SchemeColorVal.FollowedHyperlink: color_map.folHlink,
            ST_SchemeColorVal.Dark1: ST_ColorSchemeIndex.Dark1,
            ST_SchemeColorVal.Dark2: ST_ColorSchemeIndex.Dark2,
            ST_SchemeColorVal.Light1: ST_ColorSchemeIndex.Light1,
            ST_SchemeColorVal.Light2: ST_ColorSchemeIndex.Light2,
            # 占位符颜色特殊处理, 会报错
            ST_SchemeColorVal.Placeholder: None,
        }

        scheme_idx = index_map.get(schema_color_value)

        # logger.debug(f"颜色: {scheme_idx = }")

        if scheme_idx is None:
            msg = f'获取方案颜色索引(schema color index) 失败: {schema_color_value = }'
            raise ValueError(msg)

        if scheme_idx == ST_ColorSchemeIndex.Dark1:
            return color_schema.dk1

        if scheme_idx == ST_ColorSchemeIndex.Dark2:
            return color_schema.dk2

        if scheme_idx == ST_ColorSchemeIndex.Light1:
            return color_schema.lt1

        if scheme_idx == ST_ColorSchemeIndex.Light2:
            return color_schema.lt2

        if scheme_idx == ST_ColorSchemeIndex.Accent1:
            return color_schema.accent1

        if scheme_idx == ST_ColorSchemeIndex.Accent2:
            return color_schema.accent2

        if scheme_idx == ST_ColorSchemeIndex.Accent3:
            return color_schema.accent3

        if scheme_idx == ST_ColorSchemeIndex.Accent4:
            return color_schema.accent4

        if scheme_idx == ST_ColorSchemeIndex.Accent5:
            return color_schema.accent5

        if scheme_idx == ST_ColorSchemeIndex.Accent6:
            return color_schema.accent6

        if scheme_idx == ST_ColorSchemeIndex.Hyperlink:
            return color_schema.hlink

        if scheme_idx == ST_ColorSchemeIndex.Followed_hyperlink:
            return color_schema.folHlink

        msg = f'获取方案颜色(schema color) 失败: {scheme_idx = }'
        raise ValueError(msg)

    @classmethod
    def ph_color_value(cls, raw_color: ColorTypes, ph_color: SchemeColor, slide: SlideTypes):
        """处理占位符颜色以及相关的变换

        - raw_color: 要使用的颜色，定义的原始颜色值
        - ph_color: 占位符颜色, 为主题颜色(SchemaColor)，并且 color.value 为 phClr, 这里传进来，主要是要应用该颜色下面的其他属性, 比如: tint, mod, off, 等等属性

        """

        ph_color_mode = cls.color_mode(raw_color, slide)

        # 对颜色有更改/变换，比如色调，亮度，对比度等等
        has_color_transform = bool(raw_color.oxml.countchildren())  # type: ignore

        if has_color_transform and isinstance(ph_color_mode, (RGBAColor, HSLAColor)):
            logger.info(f'#{ph_color_mode = } 需要变换...')
            ph_color_mode = cls.transform_color(ph_color_mode, ph_color)

        if isinstance(ph_color_mode, RGBAColor):
            return f'#{ph_color_mode}'
        if isinstance(ph_color_mode, HSLAColor):
            return str(ph_color_mode)
        return ph_color_mode

    @classmethod
    def color_mode(cls, color: ColorTypes, slide: SlideTypes, default: str = 'transparent'):
        """将颜色转换为str类型"""

        color_val: RGBAColor | HSLAColor | str = default

        if isinstance(color, ScrgbColor):
            color_val = RGBAColor(
                np.uint8(color.r * 100),
                np.uint8(color.g * 100),
                np.uint8(color.b * 100),
            )

        elif isinstance(color, HslColor):
            """html的hsl颜色值"""
            color_val = HSLAColor(
                np.uint16(color.attr_hue),
                np.float_(color.attr_sat),
                np.float_(color.attr_lum),
            )

        elif isinstance(color, SrgbColor):
            color_val = RGBAColor.from_string(color.value)

        elif isinstance(color, PresetColor):
            color_val = PresetColorValues[color.value.value].value

        elif isinstance(color, SystemColor):
            if color.last_color is not None:
                color_val = RGBAColor.from_string(color.last_color)

        elif isinstance(color, SchemeColor):
            # logger.debug(f"color为Schema(主题颜色): {color = }")

            if color.value == ST_SchemeColorVal.Placeholder:
                # 不处理占位符的颜色
                msg = f'占位符颜色: {color}， 请使用ColorTool.ph_color_vale方法'
                raise ValueError(msg)

            # 预期这里返回的color实例不是SchemeColor,
            # 也就是主题当中定义非 SchemeColor 的 其他类型Color
            color = cls.extract_schema_color(color, slide)
            color_val = cls.color_mode(color, slide)  # 回调，

        else:
            logger.warning(f'获取颜色值失败: {type(color) = } {color = }')
            color_val = default

        return color_val

    @classmethod
    def color_val(cls, color: ColorTypesRequire, slide: SlideTypes, default: str = 'transparent'):
        color_val = cls.color_mode(color, slide, default)

        # 对颜色有更改/变换，比如色调，亮度，对比度等等
        has_color_transform = bool(color.oxml.countchildren())  # type: ignore

        # 颜色要进行变换，
        if has_color_transform and isinstance(color_val, (RGBAColor, HSLAColor)):
            color_val = cls.transform_color(color_val, color)

        return color_val

    @classmethod
    def color_html(cls, color: ColorTypes, slide: SlideTypes, default: str = 'transparent') -> str:
        """将 color 转化为 html 中 可用的值"""

        if color is None:
            return default

        color_val = cls.color_val(color, slide, default)

        if isinstance(color_val, RGBAColor):
            return f'#{color_val}'
        if isinstance(color_val, HSLAColor):
            return str(color_val)
        return color_val

    @classmethod
    def color_svg(cls, color: ColorTypes, slide: SlideTypes, default: str = 'transparent'):
        """将 color 转化为 html 中 可用的值"""

        if color is None:
            return default

        color_val = cls.color_val(color, slide, default)

        if isinstance(color_val, RGBAColor):
            return color_val
        if isinstance(color_val, HSLAColor):
            return TransformTool.hsl_to_rgb(color_val)
        return color_val

    @classmethod
    def transform_color(cls, color: RGBAColor | HSLAColor, raw_color: ColorTransformBase):
        """变换颜色"""

        # logger.info(f"变换颜色: 【{color = }】 => {color}")
        # logger.info(raw_color.oxml.xml)

        result_color = color

        if raw_color.tint is not None:
            # 与 CT_PositiveFixedPercentage 类 表示的 tint 节点有冲突
            # 所以这里的值，通过 attrib["val"] 获取
            tint_raw_val = raw_color.tint.attrib['val']
            tint_val = to_ST_PositiveFixedPercentage(str(tint_raw_val))
            result_color = TransformTool.tint(result_color, tint_val)

        if raw_color.shade is not None:
            result_color = TransformTool.shade(result_color, raw_color.shade.value)

        if raw_color.comp is not None:
            result_color = TransformTool.comp(result_color)

        if raw_color.inv is not None:
            result_color = TransformTool.inv(result_color)

        if raw_color.gray is not None:
            result_color = TransformTool.gray(result_color)

        if raw_color.alpha is not None:
            result_color = TransformTool.alpha(result_color, raw_color.alpha.value)

        if raw_color.alpha_mod is not None:
            result_color = TransformTool.alphaMod(result_color, raw_color.alpha_mod.value)

        if raw_color.alpha_off is not None:
            result_color = TransformTool.alphaOff(result_color, raw_color.alpha_off.value)

        if raw_color.red is not None:
            result_color = TransformTool.red(result_color, raw_color.red.value)

        if raw_color.red_mod is not None:
            result_color = TransformTool.redMod(result_color, raw_color.red_mod.value)

        if raw_color.red_off is not None:
            result_color = TransformTool.redOff(result_color, raw_color.red_off.value)

        if raw_color.green is not None:
            result_color = TransformTool.green(result_color, raw_color.green.value)

        if raw_color.green_mod is not None:
            result_color = TransformTool.greenMod(result_color, raw_color.green_mod.value)

        if raw_color.green_off is not None:
            result_color = TransformTool.greenOff(result_color, raw_color.green_off.value)

        if raw_color.blue is not None:
            result_color = TransformTool.blue(result_color, raw_color.blue.value)

        if raw_color.blue_mod is not None:
            result_color = TransformTool.blueMod(result_color, raw_color.blue_mod.value)

        if raw_color.blue_off is not None:
            result_color = TransformTool.blueOff(result_color, raw_color.blue_off.value)

        if raw_color.hue is not None:
            result_color = TransformTool.hue(result_color, np.uint16(raw_color.hue.value))

        if raw_color.hue_mod is not None:
            result_color = TransformTool.hueMod(result_color, raw_color.hue_mod.value)

        if raw_color.hue_off is not None:
            result_color = TransformTool.hueOff(result_color, int(raw_color.hue_off.value))

        if raw_color.sat is not None:
            result_color = TransformTool.sat(result_color, raw_color.sat.value)

        if raw_color.sat_mod is not None:
            result_color = TransformTool.satMod(result_color, raw_color.sat_mod.value)

        if raw_color.sat_off is not None:
            result_color = TransformTool.satOff(result_color, int(raw_color.sat_off.value))

        if raw_color.lum is not None:
            result_color = TransformTool.lum(result_color, raw_color.lum.value)

        if raw_color.lum_mod is not None:
            result_color = TransformTool.lumMod(result_color, raw_color.lum_mod.value)

        if raw_color.lum_off is not None:
            result_color = TransformTool.lumOff(result_color, raw_color.lum_off.value)

        if raw_color.gamma is not None:
            result_color = TransformTool.gamma(result_color)

        if raw_color.inv_gamma is not None:
            result_color = TransformTool.invGamma(result_color)

        # logger.info(f"变换结果: 【{result_color = }】 => {result_color}")

        return result_color


class TransformTool:
    @classmethod
    def rgb_to_hsl(cls, color: RGBAColor):
        r, g, b, a = color

        r /= 255.0
        g /= 255.0
        b /= 255.0
        h, l, s = colorsys.rgb_to_hls(r, g, b)  # type: ignore
        h = np.uint16(h * 360)  # 将色相值从小数转换为0到360之间的整数
        # s = numpy.float_(s * 100)  # 将饱和度值从小数转换为0到100之间的整数
        # l = numpy.float_(l * 100)  # 将亮度值从小数转换为0到100之间的整数
        s = np.float_(s)  # 将饱和度值从小数转换为0到100之间的整数
        l = np.float_(l)  # 将亮度值从小数转换为0到100之间的整数
        return HSLAColor(h, s, l, a)

    @classmethod
    def hsl_to_rgb(cls, color: HSLAColor):
        h, s, l, a = color
        h /= 360.0
        # s /= 100.0
        # l /= 100.0
        r, g, b = colorsys.hls_to_rgb(h, l, s)  # type: ignore
        r = np.uint8(r * 255)  # 将红色分量值从小数转换为0到255之间的整数
        g = np.uint8(g * 255)  # 将绿色分量值从小数转换为0到255之间的整数
        b = np.uint8(b * 255)  # 将蓝色分量值从小数转换为0到255之间的整数
        return RGBAColor(r, g, b, a)

    @classmethod
    def _rgb(cls, color: RGBAColor | HSLAColor):
        if isinstance(color, HSLAColor):
            return cls.hsl_to_rgb(color)

        return color

    @classmethod
    def _hsl(cls, color: RGBAColor | HSLAColor):
        if isinstance(color, RGBAColor):
            return cls.rgb_to_hsl(color)

        return color

    @classmethod
    def tint(cls, color: RGBAColor | HSLAColor, val: float):
        """颜色的浅色版本

        参考: https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter20/main/basics/#2012334-tint-色调
        """

        r, g, b, a = cls._rgb(color)

        r = np.uint8(r * val + (1 - val) * 255)  # ff 白色
        g = np.uint8(g * val + (1 - val) * 255)
        b = np.uint8(b * val + (1 - val) * 255)

        return RGBAColor(r, g, b, a)

    @classmethod
    def shade(cls, color: RGBAColor | HSLAColor, val: float):
        """颜色的深色版本

        参考: https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter20/main/basics/#2012334-tint-色调
        """

        r, g, b, a = cls._rgb(color)

        r = np.uint8(r * val + (1 - val) * 0)  # 00 黑色
        g = np.uint8(g * val + (1 - val) * 0)
        b = np.uint8(b * val + (1 - val) * 0)

        return RGBAColor(r, g, b, a)

    @classmethod
    def comp(cls, color: RGBAColor | HSLAColor):
        """颜色的补色"""

        rgb_color = cls._rgb(color)

        r = rgb_color.b
        g = rgb_color.r + rgb_color.b - rgb_color.g
        b = rgb_color.r

        return RGBAColor(r, g, b)

    @classmethod
    def inv(cls, color: RGBAColor | HSLAColor):
        """颜色的反色"""

        rgb_color = cls._rgb(color)

        percent_r = rgb_color.r / 255.0
        percent_g = rgb_color.g / 255.0
        percent_b = rgb_color.b / 255.0

        r = np.uint8(255 * abs(1.0 - percent_r))
        g = np.uint8(255 * abs(1.0 - percent_g))
        b = np.uint8(255 * abs(1.0 - percent_b))

        return RGBAColor(r, g, b)

    @classmethod
    def gray(cls, color: RGBAColor | HSLAColor):
        """颜色的灰度

        参考: https://www.cnblogs.com/ryzen/p/16370464.html#1680685485
        """

        rgb_color = cls._rgb(color)

        # 灰度系数
        gray = math.pow(
            math.pow(rgb_color.r, 2.2) * 0.2126
            + math.pow(rgb_color.g, 2.2) * 0.7152
            + math.pow(rgb_color.b, 2.2) * 0.0722,
            1 / 2.2,
        )

        gray_result = np.uint8(round(gray, 0))

        return RGBAColor(gray_result, gray_result, gray_result)

    @classmethod
    def alpha(cls, color: RGBAColor | HSLAColor, alpha: float):
        """颜色的透明度"""

        r, g, b, a = cls._rgb(color)

        return RGBAColor(r, g, b, np.float_(alpha))

    @classmethod
    def alphaMod(cls, color: RGBAColor | HSLAColor, percent: float):
        """蓝色调制"""

        r, g, b, a = cls._rgb(color)

        a *= percent

        if a > 1:  # 透明度 不会大于 1
            a = np.float_(1.0)

        if a < 0:  # 透明度 不会小于 0
            a = np.float_(0.0)

        return RGBAColor(r, g, b, a)

    @classmethod
    def alphaOff(cls, color: RGBAColor | HSLAColor, percent: float):
        """蓝色偏移"""

        r, g, b, a = cls._rgb(color)

        a += percent

        if a > 1:  # 透明度 不会大于 1
            a = np.float_(1.0)

        if a < 0:  # 透明度 不会小于 0
            a = np.float_(0.0)

        a = np.float_(a)

        return RGBAColor(r, g, b, a)

    @classmethod
    def red(cls, color: RGBAColor | HSLAColor, percent: float):
        """红色替换"""

        r, g, b, a = cls._rgb(color)

        return RGBAColor(np.uint8(255 * percent), g, b, a)

    @classmethod
    def redMod(cls, color: RGBAColor | HSLAColor, percent: float):
        """红色调制"""

        r, g, b, a = cls._rgb(color)

        r *= percent

        r = min(r, 255)

        r = max(r, 0)

        r = np.uint8(r)

        return RGBAColor(r, g, b, a)

    @classmethod
    def redOff(cls, color: RGBAColor | HSLAColor, percent: float):
        """红色偏移"""

        r, g, b, a = cls._rgb(color)

        r += r * percent

        r = min(r, 255)

        r = max(r, 0)

        r = np.uint8(r)

        return RGBAColor(r, g, b, a)

    @classmethod
    def green(cls, color: RGBAColor | HSLAColor, green: float):
        """蓝色替换"""

        r, g, b, a = cls._rgb(color)

        return RGBAColor(r, np.uint8(255 * green), b, a)

    @classmethod
    def greenMod(cls, color: RGBAColor | HSLAColor, percent: float):
        """绿色调制"""

        r, g, b, a = cls._rgb(color)

        g *= percent

        g = min(g, 255)

        g = max(g, 0)

        g = np.uint8(g)

        return RGBAColor(r, g, b, a)

    @classmethod
    def greenOff(cls, color: RGBAColor | HSLAColor, percent: float):
        """绿色偏移"""

        r, g, b, a = cls._rgb(color)

        g += g * percent

        g = min(g, 255)

        g = max(g, 0)

        g = np.uint8(g)

        return RGBAColor(r, g, b, a)

    @classmethod
    def blue(cls, color: RGBAColor | HSLAColor, percent: float):
        """蓝色替换"""

        r, g, b, a = cls._rgb(color)

        return RGBAColor(r, g, np.uint8(255 * percent), a)

    @classmethod
    def blueMod(cls, color: RGBAColor | HSLAColor, percent: float):
        """蓝色调制"""

        r, g, b, a = cls._rgb(color)

        b *= percent

        b = min(b, 255)

        b = max(b, 0)

        b = np.uint8(b)

        return RGBAColor(r, g, b, a)

    @classmethod
    def blueOff(cls, color: RGBAColor | HSLAColor, percent: float):
        """蓝色偏移"""

        r, g, b, a = cls._rgb(color)

        b += b * percent

        b = min(b, 255)

        b = max(b, 0)

        b = np.uint8(b)

        return RGBAColor(r, g, b, a)

    @classmethod
    def hue(cls, color: RGBAColor | HSLAColor, hue: np.uint16):
        """颜色的色调 mod"""

        h, s, l, a = cls._hsl(color)

        return cls._rgb(HSLAColor(hue, s, l, a))

    @classmethod
    def hueMod(cls, color: RGBAColor | HSLAColor, mod: float):
        """色调调试"""

        h, s, l, a = cls._hsl(color)

        h *= mod

        h = min(h, 360)

        h = max(h, 0)

        h = np.uint16(h)

        return cls._rgb(HSLAColor(h, s, l, a))

    @classmethod
    def hueOff(cls, color: RGBAColor | HSLAColor, off: int):
        """色调偏移"""

        h, s, l, a = cls._hsl(color)

        h += off

        h = min(h, 360)

        h = max(h, 0)

        h = np.uint16(h)

        return cls._rgb(HSLAColor(h, s, l, a))

    @classmethod
    def sat(cls, color: RGBAColor | HSLAColor, percent: float):
        """颜色的亮度 mod"""

        h, s, l, a = cls._hsl(color)

        return cls._rgb(HSLAColor(h, np.float_(percent), l, a))

    @classmethod
    def satMod(cls, color: RGBAColor | HSLAColor, percent: float):
        """颜色的亮度 mod"""

        h, s, l, a = cls._hsl(color)

        s *= percent

        s = min(s, 1)

        s = max(s, 0)

        return cls._rgb(HSLAColor(h, np.float_(s), l, a))

    @classmethod
    def satOff(cls, color: RGBAColor | HSLAColor, percent: float):
        """颜色的亮度 mod"""

        h, s, l, a = cls._hsl(color)

        s += percent

        s = min(s, 1)

        s = max(s, 0)

        return cls._rgb(HSLAColor(h, np.float_(s), l, a))

    @classmethod
    def lum(cls, color: RGBAColor | HSLAColor, percent: float):
        """颜色的亮度替换"""

        h, s, l, a = cls._hsl(color)

        return cls._rgb(HSLAColor(h, s, np.float_(percent), a))

    @classmethod
    def lumMod(cls, color: RGBAColor | HSLAColor, percent: float):
        """颜色的亮度 mod"""

        # logger.info(f"lumMod: {percent = }")

        h, s, l, a = cls._hsl(color)

        l *= percent

        l = min(l, 1)

        l = max(l, 0)

        return cls._rgb(HSLAColor(h, s, np.float_(l), a))

    @classmethod
    def lumOff(cls, color: RGBAColor | HSLAColor, percent: float):
        """颜色的亮度 mod"""

        # logger.info(f"lumOff: {percent = }")

        h, s, l, a = cls._hsl(color)

        l += percent

        l = min(l, 1)

        l = max(l, 0)

        return cls._rgb(HSLAColor(h, s, np.float_(l), a))

    @classmethod
    def gamma(cls, color: RGBAColor | HSLAColor):
        """伽马矫正"""

        rgb_color = cls._rgb(color)

        r = math.pow(rgb_color.r / 255.0, 1 / 2.2)
        g = math.pow(rgb_color.g / 255.0, 1 / 2.2)
        b = math.pow(rgb_color.b / 255.0, 1 / 2.2)

        return RGBAColor(np.uint8(r), np.uint8(g), np.uint8(b), rgb_color.a)

    @classmethod
    def invGamma(cls, color: RGBAColor | HSLAColor):
        rgb_color = cls._rgb(color)

        r = math.pow(rgb_color.r / 255.0, 2.2)
        g = math.pow(rgb_color.g / 255.0, 2.2)
        b = math.pow(rgb_color.b / 255.0, 2.2)

        return RGBAColor(np.uint8(r), np.uint8(g), np.uint8(b), rgb_color.a)
