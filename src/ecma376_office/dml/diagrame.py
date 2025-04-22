"""Diagrame 绘制对象的 部件封装类"""

from ecma376_office.dml.parts import DiagramColorsPart, DiagramDataPart, DiagrameStylePart, DiagramLayoutDefinitionPart


class DiagrameData:
    """绘制数据"""

    def __init__(self, part: DiagramDataPart) -> None:
        self.part = part

    @property
    def oxml(self):
        return self.part.oxml


class DiagrameColors:
    """绘制颜色定义"""

    def __init__(self, part: DiagramColorsPart) -> None:
        self.part = part

    @property
    def oxml(self):
        return self.part.oxml


class DiagrameStyle:
    """绘制样式定义"""

    def __init__(self, part: DiagrameStylePart) -> None:
        self.part = part

    @property
    def oxml(self):
        return self.part.oxml


class DiagramLayout:
    """绘制布局定义"""

    def __init__(self, part: DiagramLayoutDefinitionPart) -> None:
        self.part = part

    @property
    def oxml(self):
        return self.part.oxml
