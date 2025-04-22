"""
各种各样 特性(属性/Properties) 封装模块
"""

from ecma376_office.dml.text import TextListStyle
from ecma376_office.oxml.dml.main import CT_DefaultShapeDefinition


class ObjDefaultShapeDefinition:
    """默认形状定义时的特性"""

    def __init__(self, oxml: CT_DefaultShapeDefinition) -> None:
        """默认形状定义时的特性

        20.1.4.1.27 spDef 形状默认样式

        此元素定义与默认形状关联的格式。 当形状最初插入到文档中时，可以将默认格式应用于形状。
        """

        self.oxml = oxml

    @property
    def text_body_properties(self):
        """形状正文的默认特性"""

        from ecma376_office.dml.text import TextBodyProperties

        return TextBodyProperties(self.oxml.body_properties)

    @property
    def text_list_style(self):
        """项目列表的默认特性"""

        return TextListStyle(self.oxml.text_list_style)

    @property
    def shape_properties(self):
        """形状默认特性

        未封装
        """

        return self.oxml.shape_properties

    def shape_style(self):
        """形状默认样式

        未封装
        """

        if self.oxml.shape_style is None:
            return None

        return self.oxml.shape_style


class ObjDefaultLineDefinition:
    """连接线默认样式"""

    def __init__(self, oxml: CT_DefaultShapeDefinition) -> None:
        """线条默认样式

        20.1.4.1.20 lnDef 线条默认样式

        该元素定义文档中使用的默认线条样式。
        """

        self.oxml = oxml

    @property
    def text_body_properties(self):
        """形状正文的默认特性"""

        from ecma376_office.dml.text import TextBodyProperties

        return TextBodyProperties(self.oxml.body_properties)

    def text_list_style(self):
        """项目列表的默认特性

        未封装
        """

        return self.oxml.text_list_style

    def shape_properties(self):
        """形状默认特性

        未封装
        """

        return self.oxml.shape_properties

    def shape_style(self):
        """形状默认样式

        未封装
        """

        if self.oxml.shape_style is None:
            return None

        return self.oxml.shape_style


class ObjDefaultTextDefinition:
    """20.1.4.1.28 txDef 文本默认样式

    此元素定义默认应用于文档中文本的默认格式。 当形状最初插入文档时，可以而且应该将默认格式应用于形状.
    """

    def __init__(self, oxml: CT_DefaultShapeDefinition) -> None:
        """文本默认样式

        20.1.4.1.28 txDef

        此元素定义默认应用于文档中文本的默认格式。 当形状最初插入文档时，可以而且应该将默认格式应用于形状.
        """

        self.oxml = oxml

    @property
    def text_body_properties(self):
        """形状正文的默认特性"""

        from ecma376_office.dml.text import TextBodyProperties

        return TextBodyProperties(self.oxml.body_properties)

    def text_list_style(self):
        """项目列表的默认特性

        未封装
        """

        return self.oxml.text_list_style

    def shape_properties(self):
        """形状默认特性

        未封装
        """

        return self.oxml.shape_properties

    def shape_style(self):
        """形状默认样式

        未封装
        """

        if self.oxml.shape_style is None:
            return None

        return self.oxml.shape_style
