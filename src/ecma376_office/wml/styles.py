"""
封装基于OXML的Presentaion数据模型, 提供更方便，快捷的访问方式
"""

import functools
import logging
from typing import TYPE_CHECKING, Any, Optional

from ecma376_office.descriptor import lazyproperty
from ecma376_office.oxml.wml.main import CT_Style, CT_Styles, ST_StyleType
from ecma376_office.wml.parts import StyleDefinitionsPart

if TYPE_CHECKING:
    from ecma376_office.opc.package import WordPackage

logger = logging.getLogger(__name__)

__all__ = [
    'Styles',
]


class Styles:
    """word文档的样式表对象

    11.3.12 样式定义部件

    该部件类型的一个实例包含了该文档中使用的一组样式的定义。

    一个包最多应包含两个样式定义部件。其中一个部件的一个实例应该是从主文档（§11.3.10）部件的隐式关系的目标，另一个应该是从词汇表文档（§11.3.8）部件的隐式关系的目标。

    <Relationships xmlns="…">
        <Relationship Id="rId3"
            Type="http://…/styles" Target="styles.xml"/>
    </Relationships>

    样式定义部件的根元素应该是 styles，它是一个包含一个或多个样式元素的容器。

    [示例：这是 ListBullet 样式（在§11.3.10中的主文档部件中使用）：

    <w:styles xmlns:w="…" … xml:space="preserve">
        <w:style w:type="paragraph" w:styleId="ListBullet">
            <w:name w:val="List Bullet"/>
            <w:basedOn w:val="Text"/>
            <w:autoRedefine/>
            <w:rsid w:val="00081289"/>
            <w:pPr>
                <w:pStyle w:val="ListBullet"/>
                <w:numPr>
                    <w:numId w:val="1"/>
                </w:numPr>
                <w:tabs>
                    <w:tab w:val="clear" w:pos="360"/>
                </w:tabs>
                <w:ind w:start="648"/>
            </w:pPr>
        </w:style>
    </w:styles>

    结束示例]

    样式定义部件应位于包含关系部件的包内（在语法上表达，关系元素的 TargetMode 属性应该是 Internal）。
    """

    def __init__(self, main_doc: Any, part: StyleDefinitionsPart) -> None:
        """
        封装word主文档样式表部件操作类
        """


        self.main_doc: WordPackage = main_doc
        self.part = part
        self.oxml = part.oxml
        self.style_map = self.build_style_map(part.oxml)

    def __del__(self):
        """清除缓存"""
        logger.info('清除docx样式的缓存')
        self.get_styles.cache_clear()

    @property
    def count(self):
        """样式数量"""

        return len(self.oxml.style)

    @lazyproperty
    def doc_defaults(self):
        """文档默认样式"""

        return self.oxml.docDefaults

    @lazyproperty
    def laten_styles(self):
        """潜在样式信息"""

        return self.oxml.latentStyles

    @lazyproperty
    def raw_collect(self):
        """xoml格式的样式合集"""

        return self.oxml.style

    @lazyproperty
    def paragrah_style_default(self):
        """<style>标签的默认段落样式"""

        for sid, sty in self.style_map.items():
            if sty.type == ST_StyleType.paragraph and sty.default:
                logger.info(f'段落默认style样式ID: {sid}')
                return sty
        return None

    @lazyproperty
    def character_style_default(self):
        """<style>标签的默认字符(run)样式"""

        for sid, sty in self.style_map.items():
            if sty.type == ST_StyleType.character and sty.default:
                logger.info(f'字符默认style样式ID: {sid}')
                return sty
        return None

    @lazyproperty
    def table_style_default(self):
        """<style>标签的默认表格样式"""

        for sid, sty in self.style_map.items():
            if sty.type == ST_StyleType.table and sty.default:
                logger.info(f'表格默认style样式ID: {sid}')
                return sty
        return None

    @lazyproperty
    def numbering_style_default(self):
        """<style>标签的默认编号样式"""

        for sid, sty in self.style_map.items():
            if sty.type == ST_StyleType.numbering and sty.default:
                logger.info(f'编号默认style样式ID: {sid}')
                return sty
        return None

    @classmethod
    def build_style_map(cls, oxml: CT_Styles):
        """构建样式的字典"""

        style_map: dict[Optional[str], CT_Style] = {style.styleId: style for style in oxml.style}

        return style_map

    @functools.lru_cache
    def get_styles(self, style_id: str):
        """根据样式ID获取指定样式, 包括继承的父级样式链条

        styles = [current_style, parent_style, grand_style, ...]
        """

        if style_id not in self.style_map:
            return []

        final_style = self.style_map[style_id]

        styles: list[CT_Style] = [final_style]

        parent_style = final_style

        # 遍历父级样式
        while True:
            # 默认样式了，不找了
            if parent_style.basedOn is None:
                break

            parent_style_id = parent_style.basedOn.val_str

            # parent_style_id 可能不在样式表中存在
            current_style = self.style_map.get(parent_style_id)

            # 父级对象找不到了，退出 child -> parent -> parent -> None
            if current_style is None:
                break

            styles.append(parent_style)
            parent_style = current_style

        # 倒序排列
        styles.reverse()

        return styles
