from typing import NamedTuple, Optional

from ecma376_office.dml.style.color import ColorTypesRequire, color_factory_require
from ecma376_office.oxml.dml.main import (
    CT_EffectContainer,
    CT_EffectList,
    CT_EffectStyleItem,
    CT_SoftEdgesEffect,
    ST_BlendMode,
    ST_EffectContainerType,
    ST_FixedAngle,
    ST_PositiveFixedAngle,
    ST_PresetShadowVal,
    ST_RectAlignment,
)
from ecma376_office.units import Emu, Percent

# -------------- 具体各个效果类------------------------------


class BlurEffect(NamedTuple):
    """模糊效果

    CT_BlurEffect

    20.1.8.15 blur (Blur Effect)

    该元素指定应用于整个形状（包括其填充）的模糊效果。 所有颜色通道（包括 Alpha）都会受到影响。
    """

    grow: bool
    """模糊界限是否成长

    对象的边界是否应因模糊而增大。 True 表示边界已增长，而 false 表示边界未增长.

    grow_bounds
    """

    radius: Emu
    """模糊半径."""


class FillOverlayEffect(NamedTuple):
    """填充叠加效果

    20.1.8.29 fillOverlay

    该元素指定填充叠加效果。 填充叠加可用于为对象指定附加填充并将两个填充混合在一起。
    """

    blend: ST_BlendMode
    """指定如何将填充与基本效果混合."""


class GlowEffect(NamedTuple):
    """发光效果

    20.1.8.32 glow

    其中在对象边缘外部添加颜色模糊轮廓.
    """

    color: ColorTypesRequire
    """ 发光颜色 """

    radius: Emu
    """发光的半径."""


class InnerShadowEffect(NamedTuple):
    """内阴影效果

    20.1.8.40 innerShdw

    根据属性给定的参数，在对象的边缘内应用阴影。
    """

    color: ColorTypesRequire
    """ 阴影颜色 """

    blur_radius: Emu
    """指定模糊半径."""

    direction: ST_PositiveFixedAngle
    """偏移阴影的方向.

    表示 60000 度的正角。 范围从 [0, 360 度)
    """

    distance: Emu
    """阴影偏移的距离.."""


class OuterShadowEffect(NamedTuple):
    """外阴影效果

    20.1.8.45 outerShdw

    根据属性给定的参数，在对象的边缘外应用阴影。
    """

    color: ColorTypesRequire
    """ 阴影颜色 """

    blur_radius: Emu
    """指定模糊半径."""

    direction: ST_PositiveFixedAngle
    """偏移阴影的方向.

    表示 60000 度的正角。 范围从 [0, 360 度)
    """

    distance: Emu
    """阴影偏移距离"""

    sx: Percent
    """水平缩放因子

     负缩放会导致翻转.
    """

    sy: Percent
    """垂直比例因子

    负缩放会导致翻转.
    """

    kx: ST_FixedAngle
    """水平倾斜角度"""

    ky: ST_FixedAngle
    """垂直倾斜角度"""

    alignment: ST_RectAlignment
    """ 阴影对齐方式；

    首先进行对齐，有效地设置缩放、倾斜和偏移的原点.
    """

    rotate_with_shape: bool
    """ 随形状旋转 """


class PresetShadowEffect(NamedTuple):
    """预置阴影效果

    20.1.8.40 innerShdw

    根据属性给定的参数，在对象的边缘内应用阴影。
    """

    color: ColorTypesRequire
    """ 阴影颜色 """

    preset: ST_PresetShadowVal
    """指定要使用的预设阴影."""

    direction: ST_PositiveFixedAngle
    """偏移阴影的方向.

    表示 60000 度的正角。 范围从 [0, 360 度)
    """

    distance: Emu
    """阴影偏移的距离.."""


class ReflectionEffect(NamedTuple):
    """反射效果

    20.1.8.50 reflection
    """

    alignment: ST_RectAlignment
    """ 阴影对齐方式；

    首先进行对齐，有效地设置缩放、倾斜和偏移的原点.
    """

    blur_radius: Emu
    """指定模糊半径."""

    direction: ST_PositiveFixedAngle
    """偏移阴影的方向.

    表示 60000 度的正角。 范围从 [0, 360 度)
    """

    distance: Emu
    """阴影偏移距离"""

    end_alpha: Percent
    """ 指定结束反射不透明度. """

    end_position: Percent
    """ 指定结束 alpha 值的结束位置（沿着 alpha 渐变斜坡）. """

    fade_direction: ST_PositiveFixedAngle
    """ 指定偏移反射的方向. """

    kx: ST_FixedAngle
    """水平倾斜角度"""

    ky: ST_FixedAngle
    """垂直倾斜角度"""

    rotate_with_shape: bool
    """ 随形状旋转 """

    start_alpha: Percent
    """ 反射开始不透明度 """

    start_position: Percent
    """ 指定起始 alpha 值的起始位置（沿着 alpha 渐变斜坡）. """

    sx: Percent
    """水平缩放因子

     负缩放会导致翻转.
    """

    sy: Percent
    """垂直比例因子

    负缩放会导致翻转.
    """


class SoftEdgesEffect(NamedTuple):
    """软边缘效果

    20.1.8.53 softEdge

    该元素指定软边缘效果。 形状的边缘变得模糊，而填充不受影响。
    """

    oxml: CT_SoftEdgesEffect

    radius: Emu
    """ 指定应用于边缘的模糊半径. """


# ------------------- 效果容器封装类------------------------------------


class EffectList:
    """效果列表的封装类"""

    def __init__(self, oxml: CT_EffectList) -> None:
        """效果列表的封装类"""
        self.oxml = oxml

    @property
    def blue(self):
        """模糊效果"""

        oxml = self.oxml.blur

        if oxml is not None:
            return BlurEffect(oxml.grow_bounds, Emu(oxml.radius))

        return None

    @property
    def fill_overlay(self):
        """填充叠加效果"""

        oxml = self.oxml.fill_overlay

        if oxml is not None:
            return FillOverlayEffect(oxml.blend_mode)

        return None

    @property
    def glow(self):
        """发光效果"""

        oxml = self.oxml.glow

        if oxml is not None:
            color = color_factory_require(oxml.color)

            return GlowEffect(color, Emu(oxml.radius))

        return None

    @property
    def inner_shadow(self):
        """内部阴影"""

        oxml = self.oxml.inner_shdw

        if oxml is not None:
            color = color_factory_require(oxml.color)

            return InnerShadowEffect(color, Emu(oxml.blur_radius), oxml.direction, Emu(oxml.distance))

        return None

    @property
    def outer_shadow(self):
        """外部阴影"""

        oxml = self.oxml.outer_shdw

        if oxml is not None:
            color = color_factory_require(oxml.color)

            return OuterShadowEffect(
                color,
                Emu(oxml.blur_radius),
                oxml.direction,
                Emu(oxml.distance),
                Percent(oxml.horizontal_scale),
                Percent(oxml.vertical_scale),
                oxml.horizontal_skew,
                oxml.vertical_skew,
                oxml.shadow_alignment,
                oxml.rotate_with_shape,
            )

        return None

    @property
    def preset_shadow(self):
        """预置阴影"""

        oxml = self.oxml.prst_shdw

        if oxml is not None:
            color = color_factory_require(oxml.color)

            return PresetShadowEffect(color, oxml.preset, oxml.direction, Emu(oxml.distance))

        return None

    @property
    def reflection_shadow(self):
        """反射效果"""

        oxml = self.oxml.reflection

        if oxml is not None:
            return ReflectionEffect(
                oxml.shadow_alignment,
                Emu(oxml.blur_radius),
                oxml.direction,
                Emu(oxml.distance),
                Percent(oxml.end_opcacity),
                Percent(oxml.end_position),
                oxml.fade_direction,
                oxml.horizontal_skew,
                oxml.vertical_skew,
                oxml.rotate_with_shape,
                Percent(oxml.start_opcacity),
                Percent(oxml.start_position),
                Percent(oxml.horizontal_scale),
                Percent(oxml.vertical_scale),
            )

        return None

    @property
    def soft_edge(self):
        """边缘柔化(羽化)效果"""

        oxml = self.oxml.soft_edge

        if oxml is not None:
            return SoftEdgesEffect(oxml, Emu(oxml.radius))

        return None

    @property
    def duotone(self):
        """双色调效果"""

        oxml = self.oxml.soft_edge

        if oxml is not None:
            return SoftEdgesEffect(oxml, Emu(oxml.radius))

        return None


class EffectContainer:
    """效果列表容器的封装类

    20.1.8.25 effectDag

    该元素指定效果列表。 效果按照容器类型（同级或树）指定的顺序应用。

    [Note: EffectDag 元素可以包含多个效果容器作为子元素。 具有不同样式的效果容器可以组合在effectDag中，以定义有向无环图（DAG），该图指定所有效果的应用顺序. end note]

    """

    def __init__(self, oxml: CT_EffectContainer) -> None:
        """效果容器的封装类"""

        self.oxml = oxml

    @property
    def effects(self):
        """效果列表

        效果按照容器类型（同级或树）指定的顺序应用。

        注意:

            未封装详细的效果类型，太多了...
        """

        return self.oxml.effect_list

    @property
    def type(self) -> ST_EffectContainerType:
        """效果列表"""

        return self.oxml.type

    @property
    def name(self):
        """为此效果列表指定一个可选名称，以便稍后引用。 在所有效果树和效果容器中应是唯一的."""

        return self.oxml.name


# --------------------效果工厂函数 ------------------------------------


def effect_factory(oxml: Optional[CT_EffectList | CT_EffectContainer]):
    """效果工厂函数"""

    if oxml is None:
        return None

    if isinstance(oxml, CT_EffectList):
        return EffectList(oxml)

    return EffectContainer(oxml)


# --------------------主题/样式矩阵定义效果（顶级）----------------------


class EffectStyle:
    """效果样式封装类"""

    def __init__(self, oxml: CT_EffectStyleItem) -> None:
        self.oxml = oxml

    @property
    def effect(self):
        """效果"""
        return self.oxml.effect
