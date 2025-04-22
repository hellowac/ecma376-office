from ecma376_office.dml.style.effect import EffectStyle
from ecma376_office.dml.style.fill import fill_factory
from ecma376_office.dml.style.line import LineStyle
from ecma376_office.oxml.dml.main import CT_StyleMatrix


class StyleMatrix:
    """样式矩阵"""

    def __init__(self, oxml: CT_StyleMatrix) -> None:
        self.oxml = oxml

    @property
    def name(self):
        """样式名称"""

        return self.oxml.name

    @property
    def fill_styles(self):
        """填充样式"""

        return [fill_factory(fill_style) for fill_style in self.oxml.fill_style.fill_style_lst]

    @property
    def line_styles(self):
        """线段的样式"""

        return [LineStyle(line_style) for line_style in self.oxml.line_style.line_lst]

    @property
    def effect_styles(self):
        """效果/阴影的样式"""

        return [EffectStyle(effect_style) for effect_style in self.oxml.effect_style.effect_styles]

    @property
    def background_styles(self):
        """背景的样式"""

        return [fill_factory(effect_style) for effect_style in self.oxml.background_style.fill_style_lst]
