"""
幻灯片封装类
"""

import logging
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
from ecma376_office.pml.parts import SlidePart
from ecma376_office.pml.timing import Animation
from ecma376_office.shared.image import Image
from ecma376_office.utils import DMLPartFinder, PMLPartFinder, SharedPartFinder

if TYPE_CHECKING:
    from ecma376_office.pml.presentation import Presentation

logger = logging.getLogger('eduai_office')


class Slide:
    """幻灯片封装类

    19.3.1.38 sld

    此元素是幻灯片部件 (§13.3.8) 的根元素,并指定幻灯片的实例。

    幻灯片中包含描述演示文稿幻灯片中的对象及其相应格式的所有元素。

    子元素描述常见的幻灯片元素,例如形状及其附加的文本主体、特定于该幻灯片的过渡和时间以及特定于该幻灯片的颜色信息。
    """

    def __init__(self, index: int, slide_id: int, part: SlidePart, presentation: Any) -> None:
        """幻灯片封装类

        19.3.1.38 sld

        此元素是幻灯片部件 (§13.3.8) 的根元素,并指定幻灯片的实例。

        幻灯片中包含描述演示文稿幻灯片中的对象及其相应格式的所有元素。

        子元素描述常见的幻灯片元素,例如形状及其附加的文本主体、特定于该幻灯片的过渡和时间以及特定于该幻灯片的颜色信息。"""


        self.index = index  # 幻灯片的按顺序编号, 从1开始
        """幻灯片的按顺序编号, 从1开始"""

        self.id = slide_id  # 幻灯片标识ID
        """幻灯片标识ID"""

        self.presentation: Presentation = presentation  # 幻灯片关系ID
        self.part = part
        self.oxml = part.oxml

        _master, _layout = self.update_layout_info()
        self._master = _master
        self._layout = _layout

    def update_layout_info(self):
        """更新当前幻灯片的布局和母板信息"""

        _layout_part = PMLPartFinder.slide_layout(self.part.rels)

        for master in self.presentation.slide_masters.values():
            if master.layouts is not None:
                for layout in master.layouts.values():
                    if layout.part.part_name == _layout_part.part_name:
                        # logger.debug(
                        #     f"slide {self.id} 找到了对应的母板 {master_id} 和 布局 {layout_id} => {_layout_part.part_name}"
                        # )
                        return master, layout

        # 永远都不应该抛出这个异常, 因为一个幻灯片永远都会引用一个布局和母板。
        msg = '获取幻灯片的布局(layout) 和 母板(Master) 失败'
        raise ValueError(msg)

    @property
    def slide_type(self):
        return 'slide'

    @property
    def master(self):
        """本幻灯片采用的母板"""

        return self._master

    @property
    def layout(self):
        """本幻灯片采用的布局"""

        return self._layout

    @property
    def show_master_shape(self) -> bool:
        """展示母板图形"""

        return self.oxml.show_master_shape

    @property
    def show_master_ph_anim(self) -> bool:
        """显示母板占位符形状动画"""

        return self.oxml.show_master_ph_anim

    @property
    def theme_override(self) -> Optional[ThemeOverride]:
        """主题覆盖样式

        通过隐式 包含零个或一个主题覆盖部件

        覆盖 主题中的 配色方案(color scheme)、字体方案(font scheme)和格式方案(format scheme)(后者也称为效果(effects))

        参考: https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-14/#1428-主题覆盖部件
        """

        part = DMLPartFinder.theme_override_one(self.part.rels)

        if part is None:
            return None

        return ThemeOverride(part)

    @lazyproperty
    def color_map_override(self):
        """颜色映射覆盖

        即获取主题颜色时,相对于演示文稿的主题中的颜色映射,优先取ppt的颜色映射。

        如果为None, 则表示使用演示文稿中的颜色映射覆盖
        """

        color_map = self.oxml.color_map_override

        if color_map is None:
            return None  # 使用演示文稿中的配色方案

        if isinstance(color_map.color_mapping, CT_EmptyElement):
            # tag名称 = masterClrMapping

            return None  # 使用演示文稿中的配色方案

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

    # 特别的数据

    @property
    def is_show(self) -> bool:
        """是否显示幻灯片"""

        return self.oxml.show

    @lazyproperty
    def shape_tree(self):
        """该幻灯片所有的形状合集"""

        # 防止循环引用
        from ecma376_office.pml.shapes import ShapeTree

        return ShapeTree(self, self.oxml.common_slide_data.shape_tree)

    @lazyproperty
    def background(self):
        """幻灯片背景"""

        background = self.oxml.common_slide_data.background

        if background is None:
            return None

        return BackGround(background)

    @property
    def cust_data(self):
        """自定义数据

        未封装
        """

        return self.oxml.common_slide_data.cust_data_lst

    @property
    def controls(self):
        """控件列表

        未封装
        """

        return self.oxml.common_slide_data.controls

    @property
    def name(self):
        """名称"""

        return self.oxml.common_slide_data.name

    @property
    def animation(self) -> Optional[Animation]:
        """动画数据"""

        if self.oxml.timing is not None:
            return Animation(self.oxml.timing)

        return None

    @property
    def transition(self):
        """过渡信息"""

        return self.oxml.transition

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
