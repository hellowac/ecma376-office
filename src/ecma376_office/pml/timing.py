"""
幻灯片动画信息封装类
"""

from ecma376_office.oxml.pml.core import CT_SlideTiming


class Animation:
    """幻灯片动画数据封装类"""

    def __init__(self, oxml: CT_SlideTiming) -> None:
        """幻灯片动画数据封装类

        19.3.1.48 timing

        更多详细信息参考: https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter19/animation/
        """

        self.oxml = oxml
