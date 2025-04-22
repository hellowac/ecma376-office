from ecma376_office.oxml.dml.main import CT_FontScheme


class FontScheme:
    """字体方案"""

    def __init__(self, oxml: CT_FontScheme) -> None:
        """字体方案"""
        self.oxml = oxml

    @property
    def name(self) -> str:
        """名称

        用户界面中显示的字体方案的名称.
        """

        return self.oxml.name

    @property
    def major_font(self):
        """主要字体"""

        return self.oxml.major_font

    @property
    def minor_font(self):
        """次要字体"""

        return self.oxml.minor_font
