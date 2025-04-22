"""
封装基于OXML的Presentaion数据模型, 提供更方便，快捷的访问方式
"""

import logging
from typing import TYPE_CHECKING, Any

from ecma376_office.wml.parts import FontTablePart

if TYPE_CHECKING:
    from ecma376_office.opc.package import WordPackage

logger = logging.getLogger(__name__)

__all__ = [
    'FontTable',
]


class FontTable:
    """word文档的字体表对象

    11.3.5 字体表部件

    此部件类型的一个实例包含文档中每个使用的字体的信息。当使用者阅读一个 WordprocessingML 文档时，应该使用此信息来确定在消费者的系统上指定的字体不可用时，要使用哪些字体来显示文档。

    一个包不应包含多于两个 Font Table 部件。如果存在，该部件的一个实例应该成为 Main Document（§11.3.10）部件中隐式关系的目标，而另一个实例应该成为 Glossary Document（§11.3.8）部件的隐式关系的目标。

    以下是 Main Document 部件关系项，其中包含一个与 Font Table 部件的关系，该关系以 fontTable.xml 作为 ZIP 项存储：

    <Relationships xmlns="…">
        <Relationship Id="rId1"
            Type="http://…/fontTable" Target="fontTable.xml"/>
    </Relationships>

    此内容类型的部件的根元素应该是 fonts。

    <w:fonts … >
        <w:font w:name="Calibri">
            <w:panose1 w:val="020F0502020204030204"/>
            <w:charset w:val="00"/>
            <w:family w:val="swiss"/>
            <w:pitch w:val="variable"/>
            <w:sig w:usb0="A00002EF" w:usb1="4000207B" w:usb2="00000000"
                w:usb3="00000000" w:csb0="0000009F" w:csb1="00000000"/>
        </w:font>
    </w:fonts>

    Font Table 部件应该位于包含关系部件的包中（在语法上表达，Relationship 元素的 TargetMode 属性应为 Internal）。

    Font Table 部件可以包含到由 ECMA-376 定义的以下部件的显式关系：

    - 字体(Fonts)（§15.2.13）

    Font Table 部件不应该有任何与由 ECMA-376 定义的其他部件的隐式或显式关系。
    """

    def __init__(self, main_doc: Any, part: FontTablePart) -> None:
        """
        封装word主文档字体表部件操作类
        """


        self.main_doc: WordPackage = main_doc
        self.part = part
        self.oxml = part.oxml

    @property
    def count(self):
        """字体数量"""

        return len(self.oxml.font)

    @property
    def raw_collect(self):
        """xoml格式的字体合集"""

        return self.oxml.font
