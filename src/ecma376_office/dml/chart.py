"""Diagrame 绘制对象的 部件封装类"""

from ecma376_office.dml.parts import ChartPart


class DiagrameChart:
    """绘制数据"""

    def __init__(self, part: ChartPart) -> None:
        self.part = part

    @property
    def oxml(self):
        return self.part.oxml
