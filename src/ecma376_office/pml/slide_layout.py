"""
幻灯片母板封装类
"""

from typing import TYPE_CHECKING, Any, Optional

from ecma376_office.descriptor import lazyproperty
from ecma376_office.dml.chart import DiagrameChart
from ecma376_office.dml.diagrame import DiagrameColors, DiagrameData, DiagrameStyle, DiagramLayout
from ecma376_office.dml.style.color import ColorMapping

# 封装后的
from ecma376_office.dml.theme import ThemeOverride

# oxml
from ecma376_office.oxml.dml.main import CT_EmptyElement
from ecma376_office.pml.background import BackGround
from ecma376_office.pml.parts import SlideLayoutPart
from ecma376_office.pml.timing import Animation
from ecma376_office.shared.image import Image
from ecma376_office.utils import DMLPartFinder, SharedPartFinder

if TYPE_CHECKING:
    from ecma376_office.pml.slide_master import SlideMaster


class SlideLayout:
    """幻灯片布局(版式)封装类

    19.3.1.39 sldLayout (Slide Layout)

    该元素指定幻灯片布局的实例。 幻灯片布局实质上包含可应用于任何现有幻灯片的模板幻灯片设计。 当应用于现有幻灯片时，所有相应的内容都应映射到新的幻灯片布局。
    """

    def __init__(self, index: int, layout_id: Optional[int], master: Any, part: SlideLayoutPart) -> None:
        """幻灯片布局(版式)封装类

        19.3.1.39 sldLayout (Slide Layout)

        该元素指定幻灯片布局的实例。 幻灯片布局实质上包含可应用于任何现有幻灯片的模板幻灯片设计。 当应用于现有幻灯片时，所有相应的内容都应映射到新的幻灯片布局。
        """


        self.index = index  # 幻灯片布局的按顺序编号, 从1开始
        self._layout_id = layout_id
        self._master: SlideMaster = master
        self.part = part
        self.oxml = part.oxml

    @property
    def presentation(self):
        return self._master.presentation

    @property
    def slide_type(self):
        return 'slideLayout'

    @property
    def id(self):
        """幻灯片布局 ID

        用于识别不同的幻灯片布局设计

        为None 时, 表示数据中没有ID，是唯一的一个布局？

        文档里面也没有说明
        """

        return self._layout_id

    @property
    def name(self):
        """布局名称"""

        return self.oxml.common_slide_data.name

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
        """本幻灯片布局使用的幻灯片母板"""

        return self._master

    @property
    def layout(self):
        """采用的布局, 返回本身，为了链式调用"""

        return self

    @property
    def show_master_shape(self) -> bool:
        """展示母板图形"""

        return self.oxml.show_master_shape

    @property
    def show_master_ph_anim(self) -> bool:
        """显示母板占位符形状动画"""

        return self.oxml.show_master_ph_anim

    @lazyproperty
    def background(self):
        """布局背景"""

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
    def theme_override(self) -> Optional[ThemeOverride]:
        """主题覆盖样式

        通过隐式 包含零个或一个主题覆盖部件

        覆盖 主题中的 配色方案(color scheme)、字体方案(font scheme)和格式方案(format scheme)（后者也称为效果(effects)）

        参考: https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-14/#1428-主题覆盖部件
        """

        part = DMLPartFinder.theme_override_one(self.part.rels)

        if part is None:
            return None

        return ThemeOverride(part)

    @lazyproperty
    def color_map_override(self):
        """颜色映射覆盖

        即获取主题颜色时，相对于演示文稿的主题中的颜色映射，优先取ppt的颜色映射。

        如果为None， 则表示使用演示文稿中的颜色映射覆盖
        """

        color_map = self.oxml.color_map_override

        if color_map is None:
            return None  # 使用上一级的配色方案

        if isinstance(color_map.color_mapping, CT_EmptyElement):
            # tag名称 = masterClrMapping

            return None  # 使用上一级的配色方案

        # 应为: CT_ColorMapping
        mapping = color_map.color_mapping
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
    def animation(self) -> Optional[Animation]:
        """幻灯片布局的幻灯片计时信息

        此元素指定处理相应幻灯片中所有动画和定时事件的计时信息。 该信息通过计时元素内的时间节点进行跟踪。 有关这些时间节点的细节以及如何定义它们的更多信息可以在PresentationML框架的动画部分中找到。
        """

        if self.oxml.timing is not None:
            return Animation(self.oxml.timing)

        return None

    @property
    def transition(self):
        """幻灯片布局的幻灯片过渡

        此元素指定用于从上一张幻灯片过渡到当前幻灯片的幻灯片过渡类型。 也就是说，转换信息存储在转换完成后出现的幻灯片上。
        """

        return self.oxml.transition

    @property
    def header_footer(self):
        """幻灯片母版的页眉/页脚信息

        此元素指定幻灯片的页眉和页脚信息。 页眉和页脚由文本占位符组成，这些文本应在所有幻灯片和幻灯片类型中保持一致，例如日期和时间、幻灯片编号以及自定义页眉和页脚文本。
        """

        return self.oxml.header_footer

    @property
    def matching_name(self):
        """匹配名称

        指定用于代替 cSld 元素中的 name 属性的名称。 这用于布局匹配以响应布局变化和模板应用。
        """

        return self.oxml.matching_name

    @property
    def type(self):
        """幻灯片布局类型

        指定此幻灯片使用的幻灯片布局类型。
        """

        return self.oxml.type

    @property
    def preserve(self):
        """保留幻灯片布局

        指定当删除遵循该布局的所有幻灯片时是否删除相应的幻灯片布局。
        如果未指定此属性，则生成应用程序应假定值为 false。
        这意味着如果演示文稿中没有与该幻灯片相关的幻灯片，该幻灯片实际上将被删除。
        """

        return self.oxml.preserve

    @property
    def user_drawn(self):
        """是否为用户绘制

        指定相应的对象是否已由用户绘制，因此不应被删除。
        这允许标记包含用户绘制数据的幻灯片。
        """

        return self.oxml.user_drawn

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
