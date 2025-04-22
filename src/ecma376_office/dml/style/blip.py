"""图片填充/光点 效果"""

from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

from ecma376_office.dml.style.color import ColorTypes, ColorTypesRequire, color_factory, color_factory_require
from ecma376_office.dml.style.effect import EffectContainer
from ecma376_office.dml.style.fill import FillTypes, fill_factory
from ecma376_office.units import Emu, Percent

if TYPE_CHECKING:
    from ecma376_office.oxml.dml.main import CT_Blip, ST_BlendMode, ST_PositiveFixedAngle

# ---------- 各个图片/光点填充效果的封装 -------------------------


class AlphaBiLevelEffect(NamedTuple):
    """阿尔法双水平效果

    20.1.8.1 alphaBiLevel

    小于阈值的 Alpha（不透明度）值将更改为 0（完全透明），大于或等于阈值的 Alpha 值将更改为 100%（完全不透明）。
    """

    thresh: Percent
    """ 指定 alpha 双水平效应的阈值. """


class AlphaCeilingEffect(NamedTuple):
    """阿尔法天花板效果

    20.1.8.2 alphaCeiling

    大于零的 Alpha（不透明度）值将更改为 100%。 换句话说，任何部分不透明的东西都会变得完全不透明。
    """



class AlphaFloorEffect(NamedTuple):
    """阿尔法地板效果

    20.1.8.3 alphaFloor

    小于 100% 的 Alpha（不透明度）值将更改为零。 换句话说，任何部分透明的东西都会变得完全透明。
    """



class AlphaInverseEffect(NamedTuple):
    """阿尔法逆效果

    20.1.8.4 alphaInv

    Alpha（不透明度）值通过从 100% 中减去来反转
    """

    color: ColorTypes


class AlphaModulateEffect(NamedTuple):
    """阿尔法调制效果

    20.1.8.5 alphaMod

    效果 alpha（不透明度）值乘以固定百分比。 效果容器指定包含要调制的 alpha 值的效果。
    """

    container: EffectContainer


class AlphaModulateFixedEffect(NamedTuple):
    """Alpha 调制固定效果

    20.1.8.6 alphaModFix

    该元素代表阿尔法调制固定效应。
    """

    amount: Percent
    """ 指定缩放 Alpha 的百分比量。 默认 100% """


class AlphaReplaceEffect(NamedTuple):
    """Alpha 替换效果

    20.1.8.8 alphaRepl

    效果 alpha（不透明度）值被固定 alpha 替换。
    """

    alpha: Percent
    """ 新的不透明度值. (alpha val)"""


class BiLevelEffect(NamedTuple):
    """双级（黑/白）效果

    此元素指定了双级（黑/白）效果。其阈值以下的输入颜色亮度被改为黑色。亮度大于或等于指定值的输入颜色被设置为白色。该效果不影响 alpha 效果值。
    """

    thresh: Percent
    """ 阈值

    指定 Bi-Level 效果的亮度阈值。 大于或等于阈值的值设置为白色。 小于阈值的值设置为黑色.
    """


class BlurEffect(NamedTuple):
    """模糊效果

    20.1.8.15 blur

    该元素指定应用于整个形状（包括其填充）的模糊效果。 所有颜色通道（包括 Alpha）都会受到影响。
    """

    grow: bool
    """指定对象的边界是否应因模糊而增大

    True 表示边界已增长，而 false 表示边界未增长.
    """

    radius: Emu
    """ 模糊半径 """


class ColorChangeEffect(NamedTuple):
    """变色效果

    20.1.8.16 clrChange

    该元素指定颜色变化效果。 clrFrom 的实例替换为 clrTo 的实例。
    """

    color_from: ColorTypesRequire
    """改变的源颜色
    """

    color_to: ColorTypesRequire
    """ 改变的目标颜色 """

    use_alpha: bool
    """
    指定效果是否考虑 alpha 值。 如果 useA 为 true，则考虑效果 alpha 值，否则将忽略它们.
    """


class ColorReplaceEffect(NamedTuple):
    """颜色替换效果

    该元素指定纯色替换值。 所有效果颜色都更改为固定颜色。 Alpha 值不受影响。
    """

    color: ColorTypesRequire
    """ 要替换为的颜色 """


class DuotoneEffect(NamedTuple):
    """双色调效果

    20.1.8.23 duotone

    该元素指定双色调效果.

    对于每个像素，通过线性插值组合 clr1 和 clr2 以确定该像素的新颜色.
    """

    color1: ColorTypesRequire
    """ 颜色1 """

    color2: ColorTypesRequire
    """ 颜色2 """


class FillOverlayEffect(NamedTuple):
    """填充叠加效果

    该元素指定填充叠加效果。 填充叠加可用于为对象指定附加填充并将两个填充混合在一起。
    """

    fill: FillTypes
    """ 填充样式 """

    blend: ST_BlendMode
    """ 混合

    指定如何将填充与基本效果混合.
    """


class GrayscaleEffect(NamedTuple):
    """灰度效果

    20.1.8.34 grayscl

    该元素指定灰度效果。 将所有效果颜色值转换为与其亮度相对应的灰色阴影。 效果 alpha（不透明度）值不受影响。
    """



class HSLEffect(NamedTuple):
    """色相饱和度亮度效果

    20.1.8.39 hsl

    该元素指定色调/饱和度/亮度效果。 色调、饱和度和亮度均可以相对于其当前值进行调整。
    """

    hue: ST_PositiveFixedAngle
    """ 色调度数 """

    lum: Percent
    """ 亮度百分比 """

    sat: Percent
    """ 饱和度百分比 """


class LuminanceEffect(NamedTuple):
    """亮度效果

    20.1.8.42 lum

    该元素指定亮度效果。 亮度使所有颜色线性地接近白色或黑色。 对比度使所有颜色变得更近或更远.
    """

    bright: Percent
    """
    指定改变亮度的百分比.
    """

    contrast: Percent
    """
    指定更改对比度的百分比.
    """


class TintEffect(NamedTuple):
    """色调效果

    20.1.8.60 tint

    该元素指定色调效果。 将效果颜色值向/远离色调移动指定的量。
    """

    amount: Percent
    """
    指定颜色值偏移的量.
    """

    hue: ST_PositiveFixedAngle
    """ 色调度数 """


# ---------- 图片填充效果的封装 -------------------------


class BlipEffect:
    """图片填充/光点 效果封装类"""

    def __init__(self, oxml: CT_Blip) -> None:
        self.oxml = oxml

    @property
    def r_embed(self):
        """嵌入图片参考 r:embed

        Embedded Picture Reference

        指定嵌入图片的标识信息。 该属性用于指定驻留在文件本地的图像。

        来自: AG_Blob
        """

        return self.oxml.r_embed

    @property
    def r_link(self):
        """链接图片参考

        Linked Picture Reference

        指定链接图片的标识信息。 该属性用于指定不驻留在该文件中的图像。

        来自: AG_Blob
        """

        return self.oxml.r_link

    @property
    def alpha_bi_level(self):
        if self.oxml.alphaBiLevel_effect is not None:
            return AlphaBiLevelEffect(Percent(self.oxml.alphaBiLevel_effect.threshold))

        return None

    @property
    def alpha_ceiling(self):
        if self.alpha_ceiling is not None:
            return AlphaCeilingEffect()

        return None

    @property
    def alpha_floor(self):
        if self.alpha_floor is not None:
            return AlphaFloorEffect()

        return None

    @property
    def alpha_inverse(self):
        if self.oxml.alphaInv_effect is not None:
            return AlphaInverseEffect(color_factory(self.oxml.alphaInv_effect.color))

        return None

    @property
    def alpha_modulate(self):
        if self.oxml.alphaMod_effect is not None:
            return AlphaModulateEffect(EffectContainer(self.oxml.alphaMod_effect.container))

        return None

    @property
    def alpha_modulate_fixed(self):
        if self.oxml.alphaModFix_effect is not None:
            return AlphaModulateFixedEffect(Percent(self.oxml.alphaModFix_effect.amount))

        return None

    @property
    def alpha_replace(self):
        if self.oxml.alphaRepl_effect is not None:
            return AlphaReplaceEffect(Percent(self.oxml.alphaRepl_effect.alpha))

        return None

    @property
    def bi_level(self):
        if self.oxml.biLevel_effect is not None:
            return BiLevelEffect(Percent(self.oxml.biLevel_effect.threshold))

        return None

    @property
    def blur(self):
        """模糊效果"""

        if self.oxml.blur_effect is not None:
            return BlurEffect(self.oxml.blur_effect.grow_bounds, Emu(self.oxml.blur_effect.radius))

        return None

    @property
    def color_change(self):
        """颜色改变效果"""

        if self.oxml.clrChange_effect is not None:
            return ColorChangeEffect(
                color_factory_require(self.oxml.clrChange_effect.color_from.color),
                color_factory_require(self.oxml.clrChange_effect.color_to.color),
                self.oxml.clrChange_effect.use_alpha,
            )

        return None

    @property
    def color_replace(self):
        """颜色改变效果"""

        if self.oxml.clrRepl_effect is not None:
            return ColorReplaceEffect(color_factory_require(self.oxml.clrRepl_effect.color))

        return None

    @property
    def duotone(self):
        """双色调效果"""

        if self.oxml.duotone_effect is not None:
            return DuotoneEffect(
                color_factory_require(self.oxml.duotone_effect.colors[0]),
                color_factory_require(self.oxml.duotone_effect.colors[1]),
            )

        return None

    @property
    def fill_overlay(self):
        """填充叠加效果"""

        if self.oxml.fillOverlay_effect is not None:
            return FillOverlayEffect(
                fill_factory(self.oxml.fillOverlay_effect.fill),
                self.oxml.fillOverlay_effect.blend_mode,
            )

        return None

    @property
    def grayscale(self):
        """灰度效果"""

        if self.oxml.grayscl_effect is not None:
            return GrayscaleEffect()

        return None

    @property
    def hsl(self):
        """色相饱和度亮度效果"""

        if self.oxml.hsl_effect is not None:
            return HSLEffect(
                self.oxml.hsl_effect.hue,
                Percent(self.oxml.hsl_effect.luminance),
                Percent(self.oxml.hsl_effect.saturation),
            )

        return None

    @property
    def luminance(self):
        """亮度效果"""

        if self.oxml.lum_effect is not None:
            return LuminanceEffect(
                Percent(self.oxml.lum_effect.brightness),
                Percent(self.oxml.lum_effect.contrast),
            )

        return None

    @property
    def tint(self):
        """色调效果"""

        if self.oxml.tint_effect is not None:
            return TintEffect(
                Percent(self.oxml.tint_effect.amount),
                self.oxml.tint_effect.hue,
            )

        return None
