from __future__ import annotations

from typing import NamedTuple, Optional, Union

from ecma376_office.dml.style.fill import fill_factory
from ecma376_office.oxml.dml.main import (
    CT_DashStopList,
    CT_LineJoinBevel,
    CT_LineJoinMiterProperties,
    CT_LineJoinRound,
    CT_LineProperties,
    CT_PresetLineDashProperties,
    ST_LineEndLength,
    ST_LineEndType,
    ST_LineEndWidth,
    ST_PositivePercentage,
    ST_PresetLineDashVal,
)
from ecma376_office.units import Emu


class LineEndStyle(NamedTuple):
    """线头/线尾样式

    参考:

    - https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter20/main/shape_fill/#201838-headend-线头线尾样式
    """

    length: Optional[ST_LineEndLength]
    """头/尾长度

    指定与线宽相关的线端长度.
    """

    type: ST_LineEndType
    """线头/线尾类型

        指定线端装饰，例如三角形或箭头.
    """

    width: Optional[ST_LineEndWidth]
    """头/尾宽度

        指定相对于线宽的线端宽度.
    """


class LineDashPresetStyle(NamedTuple):
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

    value: Optional[ST_PresetLineDashVal]
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


class LineDashCustomStyle(NamedTuple):
    """自定义虚线

    该元素指定应使用预设的虚线方案。
    """

    stops: list[LineDashStop]
    """虚线停止点"""


class LineDashStop(NamedTuple):
    """自定义虚线停止点"""

    dash_length: ST_PositivePercentage
    """ 虚线长度

    指定虚线相对于线宽的长度。 百分比为单位
    """

    stop: ST_PositivePercentage
    """空格长度

    指定相对于线宽的空间长度。 百分比为单位
    """


def line_dash_factory(oxml: CT_PresetLineDashProperties | CT_DashStopList):
    """线条虚线样式工厂函数"""

    if isinstance(oxml, CT_PresetLineDashProperties):
        return LineDashPresetStyle(oxml.value)

    stops = [LineDashStop(stop.dash, stop.stop) for stop in oxml.dash_stops if stop.dash and stop.stop]

    return LineDashCustomStyle(stops)


class LineJoinRoundStyle:
    """圆形连接样式

    20.1.8.52 round

    该元素指定连接在一起的线具有圆形连接。
    """



class LineJoinBevelStyle:
    """斜角连接样式

    20.1.8.9 bevel

    该元素指定斜角线连接。

    斜角接头指定使用角度接头来连接线条。
    """



class LineJoinMiterStyle(NamedTuple):
    """斜接连接样式

    20.1.8.43 miter

    该元素指定线连接应进行斜接。
    """

    miter_limit: Optional[ST_PositivePercentage]
    """斜接连接限制

    指定线延伸形成斜接的量 - 否则斜接可以无限延伸（对于几乎平行的线）.

    百分比为单位, 这里返回为 0 - 1 之间的浮点数
    """


LineJoinStyleTypes = Union[LineJoinRoundStyle, LineJoinBevelStyle, LineJoinMiterStyle]


def line_join_factory(
    oxml: CT_LineJoinRound | CT_LineJoinBevel | CT_LineJoinMiterProperties,
) -> LineJoinStyleTypes:
    """线连接样式工厂函数"""

    if isinstance(oxml, CT_LineJoinRound):
        return LineJoinRoundStyle()

    if isinstance(oxml, CT_LineJoinBevel):
        return LineJoinBevelStyle()

    return LineJoinMiterStyle(oxml.limit)


class LineStyle:
    """线的样式"""

    def __init__(self, oxml: CT_LineProperties) -> None:
        """线的样式

        参考: https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter21/main/#2112314-uln-下划线
        """
        self.oxml = oxml

    @property
    def width(self) -> Emu:
        """线条的宽度, 也就是轮廓的宽度

        以 EMUs 为单位, 默认为 0
        """

        w = self.oxml.width

        return Emu(w.value or 0)

    @property
    def end_cap(self):
        """线端盖类型 Line Ending Cap Type

        指定应用于该行的结束大写。 [注: 上限类型的示例有圆形、扁平等。尾注]

        默认值为 square .

        线端点类型

        20.1.10.31 ST_LineCap

        指定了如何对线的端点进行截断。这也会影响虚线的线段端点。

        - flat（平直线端点）：线段在端点结束。
        - rnd（圆形线端点）：圆形端点。半圆突出半条线宽。
        - sq（方形线端点）：方形端点。方形突出半条线宽。 -- 默认
        """

        return self.oxml.cap

    @property
    def compound_type(self):
        """复合线类型 Compound Line Type

        指定用于下划线描边的复合线类型。

        默认值为 sng(Single Line)

        - dbl（双线）-- 双线，宽度相等
        - sng（单线）-- 单线，正常宽度
        - thickThin（粗细双线）-- 双线，一粗一细
        - thinThick（细粗双线）-- 双线，一细一粗
        - tri（细粗细三重线）-- 三条线，细、粗、细
        """

        return self.oxml.cmpd

    @property
    def stroke_alignment(self):
        """笔画对齐方式 Stroke Alignment

        指定用于下划线描边的对齐方式.
        """

        return self.oxml.algn

    @property
    def head_end(self):
        """线头样式"""

        if self.oxml.head_end is None:
            return None

        end = self.oxml.head_end

        return LineEndStyle(end.length, end.type, end.width)

    @property
    def tail_end(self):
        """线尾样式"""

        if self.oxml.tail_end is None:
            return None

        end = self.oxml.tail_end

        return LineEndStyle(end.length, end.type, end.width)

    @property
    def fill_style(self):
        """线的填充样式"""

        fill = self.oxml.line_fill

        return fill_factory(fill)

    @property
    def dash_style(self):
        """线的虚线样式"""

        dash = self.oxml.line_dash

        if dash is None:
            return None

        return line_dash_factory(dash)

    @property
    def join_style(self):
        """线的连接(加入)样式"""

        join = self.oxml.line_join

        if join is None:
            return None

        return line_join_factory(join)
