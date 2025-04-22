"""
主题封装类
"""

from ecma376_office.dml.parts import TableStylesPart


class TableStyles:
    """表格样式封装类"""

    def __init__(self, default_name: str, part: TableStylesPart) -> None:
        """表格样式封装类"""

        self.default_style_name = default_name  # 默认表格样式名称
        self.part = part
        self.oxml = part.oxml
