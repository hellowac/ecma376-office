from ecma376_office.pml.parts import ViewProperitesPart


class ViewProperties:
    """视窗属性封装类"""

    def __init__(self, part: ViewProperitesPart) -> None:
        """
        视窗属性封装类

        参考: https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-13/#13313-视图属性部件
        """

        self.part = part
        self.oxml = part.oxml
