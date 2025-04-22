"""
封装基于OXML的Presentaion数据模型, 提供更方便，快捷的访问方式
"""

import functools
import logging
import sys
from typing import TYPE_CHECKING, Any, NewType

from ecma376_office.descriptor import lazyproperty
from ecma376_office.dml.chart import DiagrameChart
from ecma376_office.dml.theme import Theme
from ecma376_office.oxml.vml.const import NS_MAP as namespaces
from ecma376_office.shared.image import Image

# from .slide import Slide
# from .slide_master import SlideMaster
# from .view_properties import ViewProperties
# from .presentaion_pr import PresentationProperties
from ecma376_office.utils import DMLPartFinder, SharedPartFinder, WMLPartFinder
from ecma376_office.wml.font_table import FontTable
from ecma376_office.wml.number import Numbering
from ecma376_office.wml.parts import MainDocumentPart
from ecma376_office.wml.styles import Styles

if TYPE_CHECKING:
    from ecma376_office.opc.package import WordPackage

logger = logging.getLogger(__name__)

__all__ = [
    "WordProcessing",
]

ThemeName = NewType("ThemeName", str)


class WordProcessing:
    """word文档的文稿对象

    17.2 Main Document Story

    该元素在其中指定了基本的表示范围属性
    """

    def __init__(self, package: Any, part: MainDocumentPart) -> None:
        """
        封装word主文档部件

        17.2.3 document (Document) - 根节点

        此元素指定 WordprocessingML 文档中主文档部分的内容。

        提供必要数据的直接访问方式，避免纷繁的数据解析逻辑。

        其中一些属性是选择性的提供接口，未提供快捷访问的属性属于忽略的属性
        """


        self.package: WordPackage = package
        self.part = part
        self.oxml = part.oxml

    @property
    def is_review(self):
        """文本是否是审阅状态"""

        # 查找批注部件
        if self.comments is not None:
            return True

        # 查找批注范围
        comment_starts = self.oxml.findall(".//w:commentRangeStart", namespaces)
        if len(comment_starts) > 0:
            # logger.info(f"发现批注范围: {len(comment_starts)}")
            return True

        # 查找插入和删除（修订）
        ins = self.oxml.findall(".//w:ins", namespaces)
        dels = self.oxml.findall(".//w:del", namespaces)
        if len(ins) > 0 or len(dels) > 0:
            # logger.info(f"插入和删除修订数量: {len(ins) = } {len(dels) = }")
            return True

        return False

    def close(self):
        """删除本次的解析包"""

        logger.info("清除docx的缓存")
        self.get_chart_data.cache_clear()
        self.get_image.cache_clear()
        self.get_hayperlink_target.cache_clear()

        logger.info(f"本次包引用次数: {sys.getrefcount(self.package) = }")

        del self.package

    @property
    def background(self):
        """背景"""

        return self.oxml.background

    @property
    def body(self):
        """正文"""

        return self.oxml.body

    @property
    def conformance(self):
        """文档符合类别"""

        return self.oxml.conformance

    @lazyproperty
    def styles(self):
        """文档样式表"""
        style_part = WMLPartFinder.style_definitions(self.part.rels)

        return Styles(self, style_part)

    @lazyproperty
    def number(self):
        number_part = WMLPartFinder.numbering_definition_one(self.part.rels)

        if number_part is not None:
            return Numbering(self, number_part)
        return None

    @lazyproperty
    def theme(self):
        """主题

        通过隐式关系包含零个或一个主题部件

        参考: https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-14/#1427-主题部件
        """

        part = DMLPartFinder.theme_one(self.part.rels)

        if part is None:
            return None

        # logger.debug(f"母板: {self.id} 采用主题: {part.theme_name}({part.part_name})")
        return Theme(part.theme_name, part)

    @lazyproperty
    def fonts(self):
        """文档字体表"""

        font_part = WMLPartFinder.font_table(self.part.rels)

        if font_part is not None:
            return FontTable(self, font_part)
        return None

    @lazyproperty
    def comments(self):
        """文档的批注"""

        comments_part = WMLPartFinder.comments(self.part.rels)

        if comments_part is not None:
            return comments_part

        return None

    @lazyproperty
    def settings(self):
        """文档的设置"""

        docx_settings = WMLPartFinder.document_settings(self.part.rels)

        if docx_settings is not None:
            return docx_settings

        return None

    @functools.lru_cache
    def get_image(self, r_id: str):
        """获取图片"""

        image_part = SharedPartFinder.image_one(self.part.rels, r_id)

        if image_part is None or isinstance(image_part, str):
            return None

        return Image(image_part)

    @functools.lru_cache
    def get_chart_data(self, rid: str):
        """获取跟当前docx关联的chart图形数据文件"""

        part = DMLPartFinder.chart_one(self.part.rels, rid)

        return DiagrameChart(part)

    @functools.lru_cache
    def get_hayperlink_target(self, rid: str):
        """获取跟当前docx关联的超链接目标"""

        hyperlink = SharedPartFinder.hyperlink_one(self.part.rels, rid)

        if hyperlink is not None:
            return hyperlink
        return None
