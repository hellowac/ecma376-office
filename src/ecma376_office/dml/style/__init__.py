from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, NamedTuple

from ecma376_office.dml.style.color import ColorTypes, color_factory
from ecma376_office.oxml.dml.main import CT_ShapeStyle, ST_FontCollectionIndex

if TYPE_CHECKING:
    from ecma376_office.pml.shapes import ConnectorShape, NormalShape, PictureShape

logger = logging.getLogger(__name__)


class LineReference(NamedTuple):
    """线条样式引用

    20.1.4.2.19 lnRef

    此元素定义对样式矩阵内的线条样式的引用。 idx 属性引用 fillStyleLst 元素中线条样式(line style)的索引。

    原型跟踪: CT_StyleMatrixReference
    """

    color: ColorTypes
    """线条覆盖主题中的颜色"""

    idx: int
    """引用 fillStyleLst 元素中线条样式的索引"""


class FillReference(NamedTuple):
    """填充样式引用

    20.1.4.2.10 fillRef

    该元素定义对样式矩阵内的填充样式的引用。 idx 属性引用 fillStyleLst 元素中填充样式或背景填充样式的索引。

    由 fmtScheme 元素定义。

    原型跟踪: CT_StyleMatrixReference
    """

    color: ColorTypes
    """线条覆盖主题中的填充颜色"""

    idx: int
    """指定所引用样式的样式矩阵索引."""


class EffectReference(NamedTuple):
    """效果样式引用

    20.1.4.2.8 effectRef

    该元素定义对样式矩阵中效果样式的引用。 idx 属性指的是effectStyleLst 元素中效果样式的索引。

    由 fmtScheme 元素定义。

    原型跟踪: CT_StyleMatrixReference
    """

    color: ColorTypes
    """线条覆盖主题中的填充颜色"""

    idx: int
    """指定所引用样式的样式矩阵索引."""


class FontReference(NamedTuple):
    """效果样式引用

    20.1.4.2.8 effectRef

    该元素定义对样式矩阵中效果样式的引用。 idx 属性指的是effectStyleLst 元素中效果样式的索引。

    由 fmtScheme 元素定义。

    原型跟踪: CT_StyleMatrixReference
    """

    color: ColorTypes
    """线条覆盖主题中的字体颜色"""

    idx: ST_FontCollectionIndex
    """指定所引用字体矩阵索引."""


class ShapeStyle:
    """形状级别(shape level)的样式

    19.3.1.46 style

    该元素指定形状的样式信息。 这用于根据主题的样式矩阵定义的预设样式来定义形状的外观。
    """

    def __init__(self, parent: Any, oxml: CT_ShapeStyle):
        """形状级别(shape level)的样式

        19.3.1.46 style

        该元素指定形状的样式信息。 这用于根据主题的样式矩阵定义的预设样式来定义形状的外观。
        """

        self.parent: NormalShape | PictureShape | ConnectorShape = parent
        self.oxml = oxml

    @property
    def line_reference(self):
        """线条样式引用

        20.1.4.2.19 lnRef

        此元素定义对样式矩阵内的线条样式的引用。 idx 属性引用 fillStyleLst 元素中线条(轮廓)样式的索引。
        """

        return LineReference(color_factory(self.oxml.line_ref.color), self.oxml.line_ref.idx)

    @property
    def fill_reference(self):
        """填充样式引用"""

        return FillReference(color_factory(self.oxml.fill_ref.color), self.oxml.fill_ref.idx)

    @property
    def effect_reference(self):
        """效果引用"""

        return EffectReference(color_factory(self.oxml.effect_ref.color), self.oxml.effect_ref.idx)

    @property
    def font_reference(self):
        """字体引用"""

        return FontReference(color_factory(self.oxml.font_ref.color), self.oxml.font_ref.idx)

    @property
    def slide(self):
        """当前图形样式所属的幻灯片"""

        return self.parent.slide

    @property
    def format_scheme(self):
        """当前图形样式所属的格式方案"""

        from ecma376_office.pml.common import ThemeTool

        return ThemeTool.choice_format_scheme(self.slide)

    @property
    def font_scheme(self):
        """当前图形样式所属的格式方案"""

        from ecma376_office.pml.common import ThemeTool

        return ThemeTool.choice_font_scheme(self.slide)

    @property
    def line(self):
        """填充样式"""

        logger.info(f'[{self.parent.name}]边框样式idx: {self.line_reference.idx}')  # noqa: G004

        ref_idx = self.line_reference.idx

        return self.format_scheme.line_styles[ref_idx - 1]  # 索引从1开始，所以在取的时候要减1

    @property
    def fill(self):
        """填充样式

        https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter20/main/styles/#2014210-fillref-填充引用

        值 0 或 1000 表示无背景，值 1-999 指 fillStyleLst 元素内的填充样式的索引，

        值 1001 及以上指 bgFillStyleLst 元素内的背景填充样式的索引。

        值 1001 对应于第一个背景填充样式，1002 对应于第二个背景填充样式，依此类推。
        """  # noqa: RUF002

        logger.info(f'[{self.parent.name}]填充样式idx: {self.fill_reference.idx}')  # noqa: G004

        ref_idx = self.fill_reference.idx

        # 无样式，无背景，无填充  # noqa: RUF003
        if ref_idx in {0, 1000}:
            return None

        if 0 < ref_idx < 1000:  # noqa: PLR2004
            return self.format_scheme.fill_styles[ref_idx - 1]  # 索引从1开始，所以在取的时候要减1  # noqa: RUF003

        if ref_idx > 1000:  # noqa: PLR2004
            return self.format_scheme.background_styles[(ref_idx % 1000) - 1]  # 索引从1开始，所以在取的时候要减1

        return None

    @property
    def effect(self):
        """效果样式"""

        return self.format_scheme.effect_styles[self.effect_reference.idx]

    @property
    def font(self):
        """字体"""

        if self.font_reference.idx == ST_FontCollectionIndex.Major:
            return self.font_scheme.major_font
        if self.font_reference.idx == ST_FontCollectionIndex.Minor:
            return self.font_scheme.minor_font
        return None
