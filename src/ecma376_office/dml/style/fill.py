from typing import TYPE_CHECKING, Any, Optional

from ecma376_office.dml.style.color import color_factory
from ecma376_office.oxml.dml.main import (
    CT_BlipFillProperties,
    CT_GradientFillProperties,
    CT_GradientStop,
    CT_GroupFillProperties,
    CT_LinearShadeProperties,
    CT_NoFillProperties,
    CT_PathShadeProperties,
    CT_PatternFillProperties,
    CT_SolidColorFillProperties,
    CT_StretchInfoProperties,
    CT_TileInfoProperties,
)

if TYPE_CHECKING:
    from ecma376_office.pml.slide import Slide
    from ecma376_office.pml.slide_layout import SlideLayout
    from ecma376_office.pml.slide_master import SlideMaster

FillProperties = Optional[
    CT_NoFillProperties | CT_SolidColorFillProperties | CT_GradientFillProperties | CT_BlipFillProperties | CT_PatternFillProperties | CT_GroupFillProperties
]


# ------------------ 无填充相关类型 ------------------


class NoFill:
    """没有任何填充"""

    def __init__(self, oxml: Optional[CT_NoFillProperties]) -> None:
        """没有任何填充"""

        self.oxml = oxml


# ------------------ 纯颜色相关类型 ------------------


class SolidColorFill:
    """纯色填充"""

    def __init__(self, oxml: CT_SolidColorFillProperties) -> None:
        """纯色填充"""

        self.oxml = oxml

    @property
    def color(self):
        """颜色"""

        return color_factory(self.oxml.color)


# ------------------ 渐变填充相关类型 ------------------


class GradientStop:
    def __init__(self, oxml: CT_GradientStop) -> None:
        self.oxml = oxml

    @property
    def pos(self):
        """渐变停止点位置"""

        return self.oxml.position

    @property
    def color(self):
        """渐变颜色"""

        return color_factory(self.oxml.color)


class GradientLinearShade:
    """线性渐变"""

    def __init__(self, oxml: CT_LinearShadeProperties) -> None:
        """线性渐变"""
        self.oxml = oxml

    @property
    def angle(self):
        """渐变角度

        指定渐变颜色变化的方向。 要定义该角度，请将其值设为 x 顺时针测量。
        那么 ( -sin x, cos x ) 是与渐变填充中恒定颜色线平行的向量。
        """

        return self.oxml.angle

    @property
    def is_scaled(self) -> bool:
        """缩放

        渐变角度是否随填充区域缩放。

        从数学上讲，如果此标志为 true，则梯度向量 ( cos x , sin x ) 将按填充区域的宽度 (w) 和高度 (h) 缩放，
        从而向量变为 ( w cos x, h sin x ）（标准化之前）。
        现在观察一下，如果渐变角度为 45 度，则渐变向量为 ( w, h )，它从填充区域的左上角到右下角。

        如果此标志为 false，则渐变角度与填充区域无关，并且不会使用上述操作进行缩放。
        因此，45 度的渐变角总是给出一个渐变带，其恒定颜色线平行于向量 (1, -1)。
        """

        return self.oxml.scaled


class GradientPathShade:
    """路径渐变"""

    def __init__(self, oxml: CT_PathShadeProperties) -> None:
        """路径渐变"""
        self.oxml = oxml

    @property
    def path(self):
        return self.oxml.path

    @property
    def fill_to_rect(self):
        return self.oxml.fill_to_rect


class GradientFill:
    """渐变颜色填充"""

    def __init__(self, oxml: CT_GradientFillProperties) -> None:
        """渐变颜色填充"""

        self.oxml = oxml

    @property
    def flip(self):
        """平铺时翻转渐变的方向。

        通常，渐变填充包含包含填充的形状的整个边界框。
        然而，使用tileRect元素，可以定义一个小于边界框的“平铺”矩形。
        在这种情况下，渐变填充包含在平铺矩形内，并且平铺矩形跨边界框平铺以填充整个区域。

        """

        return self.oxml.tile_flip

    @property
    def rotate_with_shape(self):
        """背景随着图形旋转"""

        return self.oxml.rotate_with_shape

    @property
    def stops(self):
        """渐变停止点列表"""

        lst = self.oxml.gradit_stop_lst

        if lst is None:
            return None

        return [GradientStop(stop) for stop in lst.gradient_stops]

    @property
    def tile_rect(self):
        """平铺图形"""

        return self.oxml.tile_rect

    @property
    def shade(self) -> Optional[GradientLinearShade | GradientPathShade]:
        """渐变方式"""

        shade = self.oxml.shade

        if shade is None:
            return None

        if isinstance(shade, CT_LinearShadeProperties):
            return GradientLinearShade(shade)

        return GradientPathShade(shade)


# ------------------ 图片填充相关类型 ------------------


class BlipTileInfo:
    """矩形重复平铺"""

    def __init__(self, oxml: CT_TileInfoProperties) -> None:
        """指定 BLIP 应平铺以填充可用空间。 该元素在边界框中定义了一个“平铺”矩形。 图像包含在平铺矩形内，并且平铺矩形跨边界框平铺以填充整个区域。"""

        self.oxml = oxml

    @property
    def offset_x(self):
        """X轴偏移 tx

        Offset X

        指定 X 偏移。
        """

        return self.oxml.offset_x

    @property
    def offset_y(self):
        """Y轴偏移 ty

        Offset Y

        指定垂直缩放因子； 负缩放会导致翻转。
        """

        return self.oxml.offset_y

    @property
    def horizontal_scale(self):
        """水平缩放因子 sx

        Horizontal Scaling Factor

        指定水平缩放因子； 负缩放会导致翻转。
        """

        return self.oxml.horizontal_scale

    @property
    def vertical_scale(self):
        """垂直缩放因子 sy

        Vertical Scaling Factor

        指定垂直缩放因子； 负缩放会导致翻转。
        """

        self.oxml.vertical_scale

    @property
    def tile_flip(self):
        """平铺翻转

        Tile Flip

        指定平铺时翻转渐变的方向。

        通常，渐变填充包含包含填充的形状的整个边界框。
        然而，使用tileRect元素，可以定义一个小于边界框的“平铺”矩形。
        在这种情况下，渐变填充包含在平铺矩形内，并且平铺矩形跨边界框平铺以填充整个区域。
        """

        return self.oxml.tile_flip

    @property
    def alignment(self):
        """对齐位置 algn

        Alignment

        指定第一个图块相对于形状的对齐位置。 对齐发生在缩放之后、附加偏移之前。
        """

        return self.oxml.alignment


class BlipStretchInfo:
    """拉伸平铺"""

    def __init__(self, oxml: CT_StretchInfoProperties) -> None:
        """指定应拉伸 BLIP 以填充目标矩形。 另一个选项是平铺 BLIP，其中平铺 BLIP 来填充可用区域。"""

        self.oxml = oxml

    def rect(self):
        """拉伸的矩形"""

        return self.oxml.fill_rect


class BlipFill:
    """图片填充"""

    def __init__(self, oxml: CT_BlipFillProperties) -> None:
        """图片填充"""

        self.oxml = oxml

    @property
    def fill_mode(self):
        """
        填充的平铺类型及定义

        注意：【不知道前端不支持】
        """

        pr = self.oxml.fill_mode_properties

        if pr is None:
            return None

        if isinstance(pr, CT_TileInfoProperties):
            return BlipTileInfo(pr)

        if isinstance(pr, CT_StretchInfoProperties):
            return BlipStretchInfo(pr)

        return pr

    @property
    def blip(self):
        """填充的图片

        二进制对象引用
        """

        # 防止循环引用
        from ecma376_office.dml.style.blip import BlipEffect

        if self.oxml.blip is None:
            return None

        return BlipEffect(self.oxml.blip)

    @property
    def src_rect(self):
        """填充的矩形

        前段不支持
        """

        return self.oxml.src_rect

    @property
    def dpi(self):
        """每英寸点数设置 dpi

        DPI Setting

        指定用于计算光点大小的 DPI（每英寸点数）。 如果不存在或为零，则使用 blip 中的 DPI。
        """

        return self.oxml.dpi

    @property
    def ratate_with_shape(self):
        """随形状旋转 rotWithShape

        Rotate With Shape

        指定填充应随形状旋转。 也就是说，当用图片填充的形状和包含的形状（例如矩形）通过旋转进行变换时，
        填充也会通过相同的旋转进行变换。
        """

        return self.oxml.ratate_with_shape

    def get_image(self, slide: Any):
        """获取图片"""

        # 防止循环引用

        slide1: Slide | SlideLayout | SlideMaster = slide

        if self.blip is not None and self.blip.r_embed:
            return slide1.get_image(self.blip.r_embed)

        return None


# ------------------ 图案填充相关类型 ------------------


class PatternFill:
    """图案填充"""

    def __init__(self, oxml: CT_PatternFillProperties) -> None:
        """图案填充"""

        self.oxml = oxml


# ------------------ 组填充相关类型 ------------------


class GroupFill:
    """组填充"""

    def __init__(self, oxml: CT_GroupFillProperties) -> None:
        """图案填充"""

        self.oxml = oxml


# ------------------ 填充样式工厂函数 ------------------


FillTypes = Optional[NoFill | SolidColorFill | GradientFill | BlipFill | PatternFill | GroupFill]


def fill_factory(oxml: FillProperties) -> FillTypes:
    """填充实例"""

    if isinstance(oxml, CT_NoFillProperties):
        return NoFill(oxml)

    if isinstance(oxml, CT_SolidColorFillProperties):
        return SolidColorFill(oxml)

    if isinstance(oxml, CT_GradientFillProperties):
        return GradientFill(oxml)

    if isinstance(oxml, CT_BlipFillProperties):
        return BlipFill(oxml)

    if isinstance(oxml, CT_PatternFillProperties):
        return PatternFill(oxml)

    if isinstance(oxml, CT_GroupFillProperties):
        return GroupFill(oxml)

    if isinstance(oxml, CT_NoFillProperties):
        return NoFill(oxml)

    # 没有填充样式，不代表没有线条样式
    return None
