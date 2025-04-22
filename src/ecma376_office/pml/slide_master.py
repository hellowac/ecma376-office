"""
幻灯片母板封装类
"""

import logging
from typing import TYPE_CHECKING, Any, Optional

from ecma376_office.descriptor import lazyproperty
from ecma376_office.dml.chart import DiagrameChart
from ecma376_office.dml.diagrame import DiagrameColors, DiagrameData, DiagrameStyle, DiagramLayout
from ecma376_office.dml.style.color import ColorMapping
from ecma376_office.dml.text import TextListStyle

# 封装后的
from ecma376_office.dml.theme import Theme, ThemeOverride
from ecma376_office.oxml.pml.core import CT_SlideMaster, CT_SlideMasterTextStyles
from ecma376_office.pml.background import BackGround
from ecma376_office.pml.parts import SlideMasterPart
from ecma376_office.pml.slide_layout import SlideLayout
from ecma376_office.pml.timing import Animation
from ecma376_office.shared.image import Image
from ecma376_office.utils import DMLPartFinder, PMLPartFinder, SharedPartFinder

if TYPE_CHECKING:
    from ecma376_office.pml.presentation import Presentation

logger = logging.getLogger(__name__)


class SlideMaster:
    """幻灯片封装类

    19.3.1.42 sldMaster (Slide Master)

    此元素指定幻灯片母版幻灯片的实例。
    幻灯片母版幻灯片中包含描述演示文稿幻灯片中的对象及其相应格式的所有元素。

    幻灯片母版幻灯片中有两个主要元素。

    cSld 元素指定常见的幻灯片元素,例如形状及其附加的文本主体。
    然后 txStyles 元素指定每个形状中文本的格式。

    幻灯片母版幻灯片中的其他属性指定演示文稿幻灯片中的其他属性,
    例如颜色信息、页眉和页脚,以及所有相应演示文稿幻灯片的计时和过渡信息。
    """

    def __init__(
        self,
        index: int,
        presentation: Any,
        rel_id: str,
        part: SlideMasterPart,
        master_id: Optional[int] = None,
    ) -> None:
        """幻灯片封装类

        19.3.1.42 sldMaster (Slide Master)

        此元素指定幻灯片母版幻灯片的实例。
        幻灯片母版幻灯片中包含描述演示文稿幻灯片中的对象及其相应格式的所有元素。

        幻灯片母版幻灯片中有两个主要元素。

        cSld 元素指定常见的幻灯片元素,例如形状及其附加的文本主体。
        然后 txStyles 元素指定每个形状中文本的格式。

        幻灯片母版幻灯片中的其他属性指定演示文稿幻灯片中的其他属性,
        例如颜色信息、页眉和页脚,以及所有相应演示文稿幻灯片的计时和过渡信息。
        """


        self.index = index  # 幻灯片母板的按顺序编号, 从1开始
        self.id = master_id  # 为None 时 表示 是取的默认母板,也就是第一个母板。
        self.relationship_id = rel_id  # 幻灯片母板关系ID
        self.part = part
        self.presentation: Presentation = presentation
        self.oxml: CT_SlideMaster = part.oxml

    @property
    def slide_type(self):
        return 'slideMaster'

    @property
    def name(self):
        """母板名称"""

        self.oxml.common_slide_data.name

    @property
    def part_name(self):
        """部件名称"""

        return self.part.part_name

    @property
    def file_name(self):
        """部件名称"""

        return self.part.part_name.filename

    @property
    def master(self):
        """本母板使用的幻灯片母板, 就是自身, 为了链式调用做兼容"""

        return self

    @property
    def layout(self):
        """采用的布局, 返回本身,为了链式调用"""

        return self

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
    def theme_override(self) -> Optional[ThemeOverride]:
        """主题覆盖样式

        通过隐式 包含零个或一个主题覆盖部件

        覆盖 主题中的 配色方案(color scheme)、字体方案(font scheme)和格式方案(format scheme)（后者也称为效果(effects)）

        参考: https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-13/#13310-幻灯片母版部件
        """

        part = DMLPartFinder.theme_override_one(self.part.rels)

        if part is None:
            return None

        return ThemeOverride(part)

    @lazyproperty
    def background(self):
        """母板背景"""

        bg = self.oxml.common_slide_data.background

        if bg is not None:
            return BackGround(bg)

        return None

    @lazyproperty
    def shape_tree(self):
        """该母板所有的形状合集"""

        # 防止循环引用
        from ecma376_office.pml.shapes import ShapeTree

        return ShapeTree(self, self.oxml.common_slide_data.shape_tree)

    @lazyproperty
    def color_map(self):
        """颜色映射"""

        mapping = self.oxml.color_map

        return ColorMapping(
            mapping,
            mapping.bg1,
            mapping.tx1,
            mapping.bg2,
            mapping.tx2,
            mapping.accent1,
            mapping.accent2,
            mapping.accent3,
            mapping.accent4,
            mapping.accent5,
            mapping.accent6,
            mapping.hlink,
            mapping.folHlink,
        )

    @lazyproperty
    def layouts(self) -> Optional[dict[Optional[int], SlideLayout]]:
        """使用此母板的布局

        通过显式关系观念多个布局

        参考: https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-13/#13310-幻灯片母版部件
        """

        lst = self.oxml.slide_layout_id_lst

        if lst is None:
            return None

        layout_dict: dict[Optional[int], SlideLayout] = {}

        for index, layout_id in enumerate(lst.slide_layout_id_lst, start=1):
            layout_part = PMLPartFinder.slide_layout(self.part.rels, layout_id.relationship_id)

            if layout_id.id is None:
                layout_dict[None] = SlideLayout(index, None, self, layout_part)
            else:
                layout_dict[layout_id.id.value] = SlideLayout(index, layout_id.id.value, self, layout_part)

        return layout_dict

    @property
    def transition(self):
        """过渡信息"""

        return self.oxml.transition

    @lazyproperty
    def animation(self) -> Optional[Animation]:
        """动画数据"""

        if self.oxml.timing is not None:
            return Animation(self.oxml.timing)

        return None

    @property
    def header_footer(self):
        """幻灯片母版的页眉/页脚信息

        此元素指定幻灯片的页眉和页脚信息。 页眉和页脚由文本占位符组成,这些文本应在所有幻灯片和幻灯片类型中保持一致,例如日期和时间、幻灯片编号以及自定义页眉和页脚文本。
        """

        return self.oxml.header_footer

    @lazyproperty
    def text_styles(self):
        """母版文本样式

        19.3.1.52 txStyles

        此元素指定幻灯片母版中的文本样式。 该元素内包含标题文本、正文文本和其他幻灯片文本的样式信息。 该元素仅在幻灯片母版中使用,因此可以设置相应演示文稿幻灯片的文本样式。
        """

        style = self.oxml.text_styles

        if style is None:
            return None

        return MasterTextStyle(style)

    @property
    def preserve(self):
        """保留幻灯片母版

        指定当删除遵循该布局的所有幻灯片时是否删除相应的幻灯片布局。
        如果未指定此属性,则生成应用程序应假定值为 false。
        这意味着如果演示文稿中没有与该幻灯片相关的幻灯片,该幻灯片实际上会被删除。
        """

        return self.oxml.preserve

    def get_image(self, rid: str):
        """获取跟当前幻灯片关联的图片文件"""

        part = SharedPartFinder.image_one(self.part.rels, rid)

        if part is None or isinstance(part, str):
            return None

        return Image(part)

    def get_graphic_data(self, rid: str):
        """获取跟当前幻灯片关联的smart图形数据文件"""

        part = DMLPartFinder.diagrame_data_one(self.part.rels, rid)

        return DiagrameData(part)

    def get_graphic_layout(self, rid: str):
        """获取跟当前幻灯片关联的smart图形布局文件"""

        part = DMLPartFinder.diagrame_layout_definition_one(self.part.rels, rid)

        return DiagramLayout(part)

    def get_graphic_style(self, rid: str):
        """获取跟当前幻灯片关联的smart图形样式文件"""

        part = DMLPartFinder.diagrame_style_one(self.part.rels, rid)

        return DiagrameStyle(part)

    def get_graphic_color(self, rid: str):
        """获取跟当前幻灯片关联的smart图形颜色文件"""

        part = DMLPartFinder.diagrame_colors_one(self.part.rels, rid)

        return DiagrameColors(part)

    def get_chart_data(self, rid: str):
        """获取跟当前幻灯片关联的chart图形数据文件"""

        part = DMLPartFinder.chart_one(self.part.rels, rid)

        return DiagrameChart(part)


class MasterTextStyle:
    """母板文本样式"""

    def __init__(self, oxml: CT_SlideMasterTextStyles) -> None:
        """幻灯片母版文本样式

        指定幻灯片母版中的文本样式。 该元素内包含标题文本、正文文本和其他幻灯片文本的样式信息。

        该元素仅在幻灯片母版中使用,因此也可以指定相应演示文稿幻灯片的文本样式。
        """
        self.oxml = oxml

    @property
    def title_style(self):
        """标题文本样式"""

        if self.oxml.title_style is not None:
            return TextListStyle(self.oxml.title_style)

        return None

    @property
    def body_style(self):
        """正文文本样式"""

        if self.oxml.body_style is not None:
            return TextListStyle(self.oxml.body_style)

        return None

    @property
    def other_style(self):
        """其他文本样式"""

        if self.oxml.other_style is not None:
            return TextListStyle(self.oxml.other_style)

        return None
