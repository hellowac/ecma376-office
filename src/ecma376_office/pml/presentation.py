"""
封装基于OXML的Presentaion数据模型, 提供更方便，快捷的访问方式
"""

import logging
import sys
from typing import TYPE_CHECKING, Any, NewType, Optional

from ecma376_office.descriptor import lazyproperty
from ecma376_office.dml.text import TextListStyle
from ecma376_office.oxml.pml.core import ST_SlideSizeType
from ecma376_office.pml.parts import PresentaionPart
from ecma376_office.pml.presentaion_pr import PresentationProperties
from ecma376_office.pml.slide import Slide
from ecma376_office.pml.slide_master import SlideMaster
from ecma376_office.pml.view_properties import ViewProperties
from ecma376_office.preset.shapes import PresetShapes
from ecma376_office.units import Emu
from ecma376_office.utils import DMLPartFinder, PMLPartFinder

if TYPE_CHECKING:
    from ecma376_office.opc.package import PPTxPackage
    from ecma376_office.pml.parts import SlideMasterPart

logger = logging.getLogger(__name__)

__all__ = [
    'Presentation',
]

ThemeName = NewType('ThemeName', str)


class Presentation:
    """幻灯片的演示文稿对象

    19.2.1.26 presentation

    该元素在其中指定了基本的表示范围属性
    """

    def __init__(self, package: Any, part: PresentaionPart) -> None:
        """
        封装演示文稿部件

        19.2.1.26 presentation - 根节点

        提供必要数据的直接访问方式，避免纷繁的数据解析逻辑。

        其中一些属性是选择性的提供接口，未提供快捷访问的属性属于忽略的属性
        """


        self.package: PPTxPackage = package
        self.part = part
        self.oxml = part.oxml

    def close(self):
        """删除本次的解析包"""

        logger.info(f'本次包引用次数: {sys.getrefcount(self.package) = }')

        del self.package

    @lazyproperty
    def preset_shapes(self):
        """预置的形状合集"""

        return PresetShapes()

    @lazyproperty
    def properties(self):
        """演示文稿特性部件

        13.3.7 Presentation Properties Part

        参考: https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-13/#1337-演示属性部件
        """

        part = PMLPartFinder.presentation_pr(self.part.rels)

        return PresentationProperties(part)

    @lazyproperty
    def theme(self):
        """加载使用的主题

        通过隐式关系包含零个或一个主题部件

        参考: https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-14/#1427-主题部件
        """

        from ecma376_office.dml.theme import Theme

        part = DMLPartFinder.theme_one(self.part.rels)

        if part is None:
            return None

        # logger.debug(f"演示文稿 采用主题: {part.theme_name}({part.part_name})")
        return Theme(part.theme_name, part)

    @lazyproperty
    def table_style(self):
        """表格的样式部件

        通过隐式关系包含表格样式部件, 但不能超过1个。

        参考: https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-14/#1429-表格样式部件
        """

        from ecma376_office.dml.style.table import TableStyles

        part = DMLPartFinder.table_style(self.part.rels)

        if part is None:
            return None

        logger.debug(f'演示文稿 采用表格样式: {part.default_style_name}({part.part_name})')
        return TableStyles(part.default_style_name, part)

    @lazyproperty
    def view_properties(self):
        """视窗特性

        通过隐式关系 应包含零个或一个“视窗特性”部件 (View Properties part)

        参考: https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-13/#13313-视图属性部件
        """

        part = PMLPartFinder.view_pr(self.part.rels)

        if part is None:
            return None

        logger.debug(f'演示文稿 采用视窗特性以及类型: {part.oxml.last_view}({part.part_name})')
        return ViewProperties(part)

    @lazyproperty
    def default_text_style(self) -> Optional[TextListStyle]:
        """默认文本样式"""

        if self.oxml.default_text_style is None:
            return None

        style = self.oxml.default_text_style

        # logger.debug(f"演示文稿 采用默认文本样式: {style.default_paragraph_properties = }")
        return TextListStyle(style)

    @property
    def is_rtl(self):
        """否为从右到左的视图模式"""

        return self.oxml.right_to_left

    @property
    def is_save_subset_fonts(self):
        """是否在保存字体字符集时是保存的子集"""

        return self.oxml.save_subset_fonts

    @property
    def is_show_title_sld(self):
        """是否在标题幻灯片上显示页眉和页脚占位符"""

        return self.oxml.show_special_pls_on_title_slide

    @property
    def first_slide_num(self):
        """第一张幻灯片编号"""

        return self.oxml.first_slide_num

    @property
    def slide_count(self) -> int:
        """幻灯片数量"""

        slide_id_lst = self.oxml.slide_id_lst

        if slide_id_lst is None:
            return 0

        # 统计子标签数量
        return slide_id_lst.countchildren()  # type: ignore

        # return len(slide_id_lst.slide_ids)

    @lazyproperty
    def slides(self) -> list[Slide]:
        """幻灯片合集

        这里返回的Slide实例是封装后的，要访问原始的数据，请访问slide的oxml属性。
        """

        slide_id_lst = self.oxml.slide_id_lst

        if slide_id_lst is None:
            return []

        slide_lst = []

        for idx, s in enumerate(slide_id_lst.slide_ids, start=1):
            slide_part = PMLPartFinder.slide(self.part.rels, s.relationship_id)
            slide_lst.append(Slide(idx, s.id.value or 1, slide_part, self))

        return slide_lst

    @property
    def slide_master_count(self) -> int:
        """幻灯片母板数量

        包应包含一个或多个幻灯片母版部件([§13.3.9])，每个部件都应是演示部件([§13.3.6])的显式关系的目标，以及任何幻灯片布局部件([§13.3.9])的隐式关系（其中幻灯片布局是基于此幻灯片母版定义的）。 每一个幻灯片母板部件([§13.3.9])也可以选择成为幻灯片布局部件([§13.3.9])中关系的目标。
        """

        if self.oxml.slide_master_id_lst is None:
            logger.warning('pptx文件未包含一个模板')
            return 1  # 每个包应至少包含一个，即便为None

        return len(self.oxml.slide_master_id_lst.slide_master_ids)

    @lazyproperty
    def slide_masters(self) -> dict[Optional[int], SlideMaster]:
        """幻灯片母板合集

        母板应该至少有一个

        这里返回的SlideMaster实例是封装后的，要访问原始的数据，请访问slideMaster的oxml属性。
        """


        s_master_id_lst = self.oxml.slide_master_id_lst

        if s_master_id_lst is None:  # 每个pptx应该至少有一个母板，取关系部件中的第一个母板
            relationships = PMLPartFinder.slide_master_relationship(self.part.rels)

            if len(relationships) > 1:
                logger.debug('不应出现的现象: 幻灯片母板数量大于1')

            index = 1
            relationship = relationships[0]
            master_rid = relationship.rId
            master_part: SlideMasterPart = relationship.target_part  # type: ignore

            return {None: SlideMaster(index, self, master_rid, master_part)}

        # 母板字典
        masters = {}

        for index, s in enumerate(s_master_id_lst.slide_master_ids, start=1):
            master_id = s.id.value if s.id is not None else None
            masters[master_id] = SlideMaster(
                index,
                self,
                s.relationship_id,
                PMLPartFinder.slide_master(self.part.rels, s.relationship_id),
                master_id=master_id,
            )

        return masters

    @lazyproperty
    def slide_size(self) -> Optional[tuple[Emu, Emu, ST_SlideSizeType]]:
        """返回幻灯片的尺寸大小以及类型

        分别对应， 宽,高,类型

        例如: (12192000, 6858000, cust)"""

        sldsz = self.oxml.slide_size

        if sldsz is None:
            return None

        return (Emu(sldsz.cx.value), Emu(sldsz.cy.value), sldsz.type)

    @property
    def smart_tag(self):
        """智能标签

        暂无需求
        """
        # 暂无需求

        return self.oxml.smart_tags
