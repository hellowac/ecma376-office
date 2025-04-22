"""
DrawingML 部件概览

参考: https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-14/#142-概览
"""

from typing import TYPE_CHECKING

from ecma376_office.part import Part

if TYPE_CHECKING:
    from ecma376_office.oxml.dml.chart import CT_ChartSpace
    from ecma376_office.oxml.dml.diagram import (
        CT_ColorTransform,
        CT_DataModel,
        CT_DiagramDefinition,
        CT_StyleDefinition,
    )
    from ecma376_office.oxml.dml.main import CT_BaseStylesOverride, CT_OfficeStyleSheet, CT_TableStyleList


class ChartPart(Part):
    """14.2.1 图表部件

    根节点: chartSpace

    可能是以下部件的 关系目标部件

    - WordprocessingML: Main Document
    - SpreadsheetML: Drawings
    - PresentationML: Handout Master, Notes Master, Notes Slide, Slide Layout, Slide Master, Slide
    - All: Chart Drawing
    """

    @property
    def oxml(self):
        """
        经过lxml解析过后的对象化的xml文档
        """

        oxml: CT_ChartSpace = super().oxml

        return oxml


class ChartDrawingPart(Part):
    """14.2.2 图表绘制部件

    根节点: userShapes

    可能是以下部件的 关系目标部件

    - All: Chart Drawing
    """

    # @property
    # def oxml(self):
    #     """
    #     经过lxml解析过后的对象化的xml文档
    #     """
    #     from ..oxml.pml.core import CT_CommentAuthorList

    #     oxml: CT_CommentAuthorList = super().oxml

    #     return oxml



class DiagramColorsPart(Part):
    """14.2.3 绘制颜色部件

    根节点: colorsDef

    可能是以下部件的 关系目标部件

    - WordprocessingML: Main Document
    - SpreadsheetML: Drawings
    - PresentationML: Handout Master, Notes Master, Notes Slide, Slide Layout, Slide Master, Slide
    """

    @property
    def oxml(self):
        """
        经过lxml解析过后的对象化的xml文档
        """

        oxml: CT_ColorTransform = super().oxml

        return oxml


class DiagramDataPart(Part):
    """14.2.4 绘制数据部件

    根节点: dataModel

    可能是以下部件的 关系目标部件

    - WordprocessingML: Main Document
    - SpreadsheetML: Drawings
    - PresentationML: Handout Master, Notes Master, Notes Slide, Slide Layout, Slide Master, Slide
    """

    @property
    def oxml(self):
        """
        经过lxml解析过后的对象化的xml文档
        """

        oxml: CT_DataModel = super().oxml

        return oxml


class DiagramLayoutDefinitionPart(Part):
    """14.2.5 绘制布局定义部件

    根节点: layoutDef

    可能是以下部件的 关系目标部件

    - WordprocessingML: Main Document
    - SpreadsheetML: Drawings
    - PresentationML: Handout Master, Notes Master, Notes Slide, Slide Layout, Slide Master, Slide
    """

    @property
    def oxml(self):
        """
        经过lxml解析过后的对象化的xml文档
        """

        oxml: CT_DiagramDefinition = super().oxml

        return oxml


class DiagrameStylePart(Part):
    """14.2.6 绘制样式部件

    根节点: styleDef

    可能是以下部件的 关系目标部件

    - WordprocessingML: Main Document
    - SpreadsheetML: Drawings
    - PresentationML: Handout Master, Notes Master, Notes Slide, Slide Layout, Slide Master, Slide
    """

    @property
    def oxml(self):
        """
        经过lxml解析过后的对象化的xml文档
        """

        oxml: CT_StyleDefinition = super().oxml

        return oxml


class ThemePart(Part):
    """14.2.7 主题部件

    根节点: theme

    可能是以下部件的 关系目标部件

    - WordprocessingML: Main Document
    - SpreadsheetML: Drawings
    - PresentationML: Handout Master, Notes Master, Notes Slide, Slide Layout, Slide Master
    """

    @property
    def oxml(self):
        """
        经过lxml解析过后的对象化的xml文档
        """

        oxml: CT_OfficeStyleSheet = super().oxml

        return oxml

    @property
    def theme_name(self):
        """主题部件的主题名称， 隐式关系需要"""

        return self.oxml.name


class ThemeOverridePart(Part):
    """14.2.8 主题覆盖部件

    根节点: themeOverride

    可能是以下部件的 关系目标部件

    - PresentationML: Notes Slide, Slide, Slide Layout
    """

    @property
    def oxml(self):
        """
        经过lxml解析过后的对象化的xml文档
        """

        oxml: CT_BaseStylesOverride = super().oxml

        return oxml


class TableStylesPart(Part):
    """14.2.8 主题覆盖部件

    根节点: tblStyleLst

    可能是以下部件的 关系目标部件

    - PresentationML: Presentation
    """

    @property
    def oxml(self):
        """
        经过lxml解析过后的对象化的xml文档
        """

        oxml: CT_TableStyleList = super().oxml

        return oxml

    @property
    def default_style_name(self):
        """默认表格样式名称"""

        return self.oxml.default
