"""
主题封装类
"""

from typing import NamedTuple, Optional

from ecma376_office.descriptor import lazyproperty
from ecma376_office.dml.parts import ThemeOverridePart, ThemePart
from ecma376_office.dml.style.color import ColorMapping, ColorScheme
from ecma376_office.dml.style.font import FontScheme
from ecma376_office.dml.style.format import StyleMatrix
from ecma376_office.dml.style.properties import (
    ObjDefaultLineDefinition,
    ObjDefaultShapeDefinition,
    ObjDefaultTextDefinition,
)
from ecma376_office.oxml.dml.main import CT_ObjectStyleDefaults


class ColorSchemaAndMapping(NamedTuple):
    name: str
    schema: ColorScheme
    mapping: Optional[ColorMapping]


class Theme:
    """主题封装类"""

    def __init__(self, them_name: str, part: ThemePart) -> None:
        """主题封装类"""

        self.name = them_name  # 主题名称
        self.part = part
        self.oxml = part.oxml

    @lazyproperty
    def color_scheme(self):
        """主题颜色方案"""

        schema = self.oxml.theme_elements.color_scheme

        if schema is not None:
            return ColorScheme(schema)

        return None

    @lazyproperty
    def font_scheme(self):
        """字体方案"""

        schema = self.oxml.theme_elements.font_scheme

        if schema is not None:
            return FontScheme(schema)

        return None

    @lazyproperty
    def format_scheme(self):
        """格式方案（样式矩阵）"""

        schema = self.oxml.theme_elements.format_scheme

        if schema is not None:
            return StyleMatrix(schema)

        return None

    @lazyproperty
    def extra_color_scheme(self):
        """额外颜色方案

        一般用不上，因为:

        辅助配色方案，其中包括配色方案和颜色映射。 这主要用于向后兼容性问题和早期版本所需的往返信息。
        """

        extra_scheme = self.oxml.extra_color_scheme_lst

        if extra_scheme is None:
            return None

        extra_color_schema_lst = extra_scheme.extra_color_scheme_lst

        extra_color_schemes: list[ColorSchemaAndMapping] = []

        for item in extra_color_schema_lst:
            name = item.color_schema.name
            scheme = ColorScheme(item.color_schema)
            mapping = None

            if item.color_map is not None:
                mapping = ColorMapping(
                    item.color_map,
                    item.color_map.bg1,
                    item.color_map.tx1,
                    item.color_map.bg2,
                    item.color_map.tx2,
                    item.color_map.accent1,
                    item.color_map.accent2,
                    item.color_map.accent3,
                    item.color_map.accent4,
                    item.color_map.accent5,
                    item.color_map.accent6,
                    item.color_map.hlink,
                    item.color_map.folHlink,
                )

            color_and_mapping = ColorSchemaAndMapping(name, scheme, mapping)
            extra_color_schemes.append(color_and_mapping)

        return extra_color_schemes

    @lazyproperty
    def cust_color(self):
        """自定义颜色

        一般用不上，因为没有：

        自定义颜色在自定义颜色列表中使用来定义自定义颜色，这些自定义颜色是可以附加到主题的额外颜色。
        """

        cust_color_lst = self.oxml.cust_color_lst

        if cust_color_lst is None:
            return None

        return [{item.name: item.color} for item in cust_color_lst.custom_colors_lst]

    @lazyproperty
    def object_defaults(self):
        """对象默认样式

        一般用不上，因为没有：

        """

        defaults = self.oxml.object_defaults

        if defaults is None:
            return None

        return ObjectDefaults(defaults)


class ThemeOverride:
    """主题覆盖封装类"""

    def __init__(self, part: ThemeOverridePart) -> None:
        """主题覆盖封装类"""

        self.part = part
        self.oxml = part.oxml

    @lazyproperty
    def color_scheme(self):
        """颜色方案"""

        schema = self.oxml.color_schema

        if schema is not None:
            return ColorScheme(schema)

        return None

    @lazyproperty
    def font_scheme(self):
        """字体方案"""

        schema = self.oxml.font_scheme

        if schema is not None:
            return FontScheme(schema)

        return None

    @lazyproperty
    def format_scheme(self):
        """格式方案（样式矩阵）"""

        schema = self.oxml.format_scheme

        if schema is not None:
            return StyleMatrix(schema)

        return None


class ObjectDefaults:
    """主题级别的默认对象样式封装

    对象默认特性

    20.1.6.7 objectDefaults

    该元素允许定义默认形状、线条和文本框格式的特性。 应用程序可以在插入文档时使用此信息来格式化形状（或文本）。
    """

    def __init__(self, oxml: CT_ObjectStyleDefaults) -> None:
        """主题级别的默认对象样式封装"""

        self.oxml = oxml

    @lazyproperty
    def shape_def(self):
        """形状默认样式"""

        defaults = self.oxml.shape_def

        if defaults is None:
            return None

        return ObjDefaultShapeDefinition(defaults)

    @lazyproperty
    def line_def(self):
        """默认连接线的默认样式"""

        defaults = self.oxml.line_def

        if defaults is None:
            return None

        return ObjDefaultLineDefinition(defaults)

    @lazyproperty
    def text_def(self):
        """文本默认样式

        未封装，后面有需求再封装
        """

        defaults = self.oxml.text_def

        if defaults is None:
            return None

        return ObjDefaultTextDefinition(defaults)
