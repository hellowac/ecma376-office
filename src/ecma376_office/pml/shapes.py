from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, NamedTuple, Optional, Union

from ecma376_office.dml.media import AudioFile, VideoFile, media_factory
from ecma376_office.dml.style import ShapeStyle
from ecma376_office.dml.style.blip import BlipEffect
from ecma376_office.dml.style.effect import effect_factory
from ecma376_office.dml.style.fill import BlipFill, fill_factory
from ecma376_office.dml.style.line import LineStyle
from ecma376_office.dml.text import TextBody
from ecma376_office.exceptions import XfrmNotExistsError
from ecma376_office.oxml.dml.main import (
    CT_CustomGeometry2D,
    CT_PresetGeometry2D,
    CT_RegularTextRun,
    CT_TextLineBreak,
    ST_ShapeType,
)
from ecma376_office.oxml.pml.core import (
    CT_Connector,
    CT_GraphicalObjectFrame,
    CT_GroupShape,
    CT_MC_AlternateContent,
    CT_Picture,
    CT_Rel,
    CT_Shape,
    qn,
)
from ecma376_office.pml.placeholder import to_placeholder_info
from ecma376_office.pml.slide_layout import SlideLayout
from ecma376_office.pml.slide_master import SlideMaster
from ecma376_office.pml.transforms import (
    GroupShapeTransform2D,
    ShapeTransform2D,
    to_2d_xfrm,
    to_abs_group_xfrm,
    to_abs_xfrm,
    to_group_2d_xfrm,
)
from ecma376_office.units import Emu, Pt

if TYPE_CHECKING:
    from ecma376_office.pml.slide import Slide

logger = logging.getLogger(__name__)


class Point(NamedTuple):
    """坐标轴当中的一个点"""

    x: float  # x轴坐标
    y: float  # y轴坐标


@dataclass
class SvgViewBox:
    """用户坐标范围类"""

    x: float  # 左上角x轴
    y: float  # 左上角y轴
    w: float  # 范围宽度, 为0则不显示
    h: float  # 范围高度, 为0则不显示

    @property
    def center(self) -> Point:
        """该用户坐标的中心点的坐标"""

        # 范围的绝对宽高
        distance_x = abs(self.w) + abs(self.x)
        distance_y = abs(self.h) + abs(self.y)

        # 终点坐标
        end_x = self.x + self.w
        end_y = self.y + self.h

        # 终点坐标减去 1/2 的宽高
        center_x = end_x - (distance_x / 2)
        center_y = end_y - (distance_y / 2)

        return Point(center_x, center_y)


class NormalShape:
    """常规形状

    可能是内置形状，也可能是自定义形状

    19.3.1.43 sp

    该元素指定单个形状的存在。 形状可以是使用 DrawingML 框架定义的预设几何图形或自定义几何图形。 除了几何形状之外，每个形状还可以附加视觉和非视觉属性。 文本和相应的样式信息也可以附加到形状。 该形状与形状树或组形状元素中的所有其他形状一起指定。

    [Note: 形状是在幻灯片上指定文本的首选机制. end note]
    """

    def __init__(
        self,
        slide: Slide | SlideLayout | SlideMaster,
        oxml: CT_Shape,
        parent: GroupShape | ShapeTree,
    ) -> None:
        """常规形状

        可能是内置形状，也可能是自定义形状

        19.3.1.43 sp

        该元素指定单个形状的存在。 形状可以是使用 DrawingML 框架定义的预设几何图形或自定义几何图形。 除了几何形状之外，每个形状还可以附加视觉和非视觉属性。 文本和相应的样式信息也可以附加到形状。 该形状与形状树或组形状元素中的所有其他形状一起指定。

        [Note: 形状是在幻灯片上指定文本的首选机制. end note]
        """
        self.slide = slide
        self.oxml = oxml
        self.parent = parent

        self._svg_viewbox: Optional[SvgViewBox] = None

    @property
    def is_from_master(self):
        """是否来自母板"""
        return isinstance(self.slide, SlideMaster)

    @property
    def is_from_layout(self):
        """是否来自母板"""
        return isinstance(self.slide, SlideLayout)

    @property
    def id(self):
        """形状ID"""

        return self.oxml.nv_sp_pr.c_nv_pr.id

    @property
    def name(self):
        """形状名称"""

        return self.oxml.nv_sp_pr.c_nv_pr.name

    @property
    def desc(self):
        """形状的替代文本"""

        return self.oxml.nv_sp_pr.c_nv_pr.desc

    @property
    def is_hidden(self):
        """形状的替代文本"""

        return self.oxml.nv_sp_pr.c_nv_pr.hidden

    @property
    def title(self):
        """形状的标题"""

        return self.oxml.nv_sp_pr.c_nv_pr.title

    @property
    def placeholder_info(self):
        """占位符信息"""

        return to_placeholder_info(self.oxml.nv_sp_pr.nv_pr.placeholder)

    @property
    def viewbox(self):
        """获取当前图形的用户坐标系"""

        if self._svg_viewbox is None:
            # 当在svg中绘制时的用户坐标
            # 默认线宽/高 2磅
            line_width = Pt(2).emu

            if self.line_style:
                line_width = self.line_style.width

            w = self.abs_w or line_width
            h = self.abs_h or line_width

            self._svg_viewbox = SvgViewBox(0, 0, w, h)

        return self._svg_viewbox

    @viewbox.setter
    def viewbox(self, box: SvgViewBox):
        """设置当前图形的用户坐标系

        针对 line 类型的图形，在有箭头符号时， 会重新计算 viewbox 的大小和尺寸。
        """

        self._svg_viewbox = box

    @property
    def xfrm(self) -> ShapeTransform2D:
        """图形变换信息

        https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter19/slides/#193136-ph-占位符形状
        """

        if self.oxml.sp_pr.xfrm is not None:
            return to_2d_xfrm(self.oxml.sp_pr.xfrm)

        if self.placeholder_info is not None:
            ph_id = self.placeholder_info.index
            ph_type = self.placeholder_info.type

            # 当前幻灯片为幻灯片时，获取使用布局的位置
            if self.slide.slide_type == 'slide' and isinstance(self.slide.layout, SlideLayout):
                # 先假设同一类型的占为符有多个，根据type和idx匹配
                for layout_ph_sp in self.slide.layout.shape_tree.shapes:
                    if (
                        layout_ph_sp.placeholder_info is not None
                        and ph_id == layout_ph_sp.placeholder_info.index
                        and ph_type == layout_ph_sp.placeholder_info.type
                    ):
                        return layout_ph_sp.xfrm  # type: ignore

                # 如果不是多个同一类型的占位符，则根据类型匹配
                for layout_ph_sp in self.slide.layout.shape_tree.shapes:
                    if layout_ph_sp.placeholder_info is not None and ph_type == layout_ph_sp.placeholder_info.type:
                        return layout_ph_sp.xfrm  # type: ignore

            # 当前幻灯片为布局时，获取使用母板的位置
            elif self.slide.slide_type == 'slideLayout' and isinstance(self.slide.master, SlideMaster):
                for master_ph_sp in self.slide.master.shape_tree.shapes:
                    if (
                        master_ph_sp.placeholder_info is not None
                        and ph_id == master_ph_sp.placeholder_info.index
                        and ph_type == master_ph_sp.placeholder_info.type
                    ):
                        return master_ph_sp.xfrm  # type: ignore

                # 如果不是多个同一类型的占位符，则根据类型匹配
                for master_ph_sp in self.slide.master.shape_tree.shapes:
                    if master_ph_sp.placeholder_info is not None and ph_type == master_ph_sp.placeholder_info.type:
                        return master_ph_sp.xfrm  # type: ignore

        msg = f'[{self.slide.slide_type}-{self.slide.index}-{self.name}]获取位置失败(xfrm)'
        raise XfrmNotExistsError(msg)

    @property
    def abs_xfrm(self):
        """图形绝对位置变换信息"""

        if isinstance(self.parent, ShapeTree):
            return self.xfrm

        return to_abs_xfrm(self.xfrm, self.parent.abs_xfrm)

    @property
    def x(self):
        """图形的x轴位置, 未经过任何处理"""

        return self.xfrm.off.x

    @property
    def y(self):
        """图形的y轴位置, 未经过任何处理"""

        return self.xfrm.off.y

    @property
    def w(self):
        """图形的宽度, 未经过任何处理"""

        return self.xfrm.ext.cx

    @property
    def h(self):
        """图形的高度, 未经过任何处理"""

        return self.xfrm.ext.cy

    @property
    def abs_x(self):
        """图形的x轴绝对位置, 相对于幻灯片左上角(0,0)"""

        return self.abs_xfrm.off.x

    @property
    def abs_y(self):
        """图形的y轴绝对位置, 相对于幻灯片左上角(0,0)"""

        return self.abs_xfrm.off.y

    @property
    def abs_w(self):
        """图形的绝对宽度,  解组合后的，未经过缩放的宽度"""

        return self.abs_xfrm.ext.cx

    @property
    def abs_h(self):
        """图形的绝对高度,  解组合后的，未经过缩放的高度"""

        return self.abs_xfrm.ext.cy

    @property
    def relative_x(self):
        """图形的x轴相对父级的位置, 针对组合中的图形"""

        if isinstance(self.parent, ShapeTree):
            return self.abs_x

        return Emu(self.abs_x - self.parent.abs_x)

    @property
    def relative_y(self):
        """图形的y轴相对父级的位置, 针对组合中的图形"""

        if isinstance(self.parent, ShapeTree):
            return self.abs_y

        return Emu(self.abs_y - self.parent.abs_y)

    @property
    def flip_v(self):
        """图形是否垂直翻转"""

        return self.xfrm.flipV

    @property
    def flip_h(self):
        """图形是否水平翻转"""

        return self.xfrm.flipH

    @property
    def rotate(self):
        """图形渲染角度， 默认为 0"""

        return self.xfrm.rot

    @property
    def style(self):
        """形状的样式"""

        if self.oxml.style is not None:
            return ShapeStyle(self, self.oxml.style)

        return None

    @property
    def line_style(self):
        """形状线条的样式"""

        line = self.oxml.sp_pr.line

        if line is None:
            return None

        return LineStyle(line)

    @property
    def fill_style(self):
        """形状的填充样式"""

        fill = self.oxml.sp_pr.fill

        return fill_factory(fill)

    @property
    def effect_style(self):
        """形状的效果"""

        effect = self.oxml.sp_pr.effect

        if effect is None:
            return None

        return effect_factory(effect)

    @property
    def no_change_aspect(self):
        """是否禁止更改宽高比

        20.1.2.2.34 spLocks (形状锁)
        """

        shape_locks = self.oxml.nv_sp_pr.c_nv_sp_pr.shape_locks

        if shape_locks is None:
            return False

        return shape_locks.no_change_aspect

    @property
    def is_text_box(self):
        """是否为文本框"""

        return self.oxml.nv_sp_pr.c_nv_sp_pr.text_box


    @property
    def is_preset_shape(self):
        """是否为预置图形 并且不是 文本框

        如果形状具有 ``<a:prstGeom>`` 元素并且在 cNvSpPr 上没有 txBox="1" 属性，则该形状是自动形状。
        """
        prstGeom = self.oxml.sp_pr.geometry

        # logger.info(f"[{self.name}] {type(prstGeom) = }")

        if prstGeom is None:
            return False

        # logger.info(f"[{self.name}] {type(prstGeom) = }")

        is_preset_geom = isinstance(prstGeom, CT_PresetGeometry2D)
        # is_text_box = self.oxml.nv_sp_pr.c_nv_sp_pr.text_box

        # if is_preset_geom and not is_text_box:
        #     return True

        return bool(is_preset_geom)

    @property
    def preset_shape_type(self) -> ST_ShapeType:
        """是否为预置图形 并且不是 文本框

        如果形状具有 ``<a:prstGeom>`` 元素并且在 cNvSpPr 上没有 txBox="1" 属性，则该形状是自动形状。
        """

        if not self.is_preset_shape:
            msg = f'[slide-{self.slide.index}][{self.name}]该图形不是预置图形, 请先通过 is_preset_shape 判断 再获取预制图形类型'
            raise ValueError(
                msg
            )

        prstGeom = self.oxml.sp_pr.geometry

        return prstGeom.preset  # type: ignore

    @property
    def is_custom_shape(self):
        """是否为自定义图形

        如果形状具有 ``<a:prstGeom>`` 元素并且实例为 CT_
        """
        prstGeom = self.oxml.sp_pr.geometry

        if prstGeom is None:
            return False

        return isinstance(prstGeom, CT_CustomGeometry2D)


    @property
    def is_pure_graph(self):
        """是否为纯绘制图形, 也就是svg要表示的图形

        1. 不是文本框
        2. 没有任何文本标签
        3. 填充不是图片填充
        """

        if self.is_text_box:
            # logger.info(f"======================")
            # logger.info(f"{self.is_text_box =}")
            return False

        text_body = self.oxml.text_body

        if text_body is not None:
            for paragraph in text_body.text_paragraphs:
                # for text_run in paragraph.text_run_lst:
                #     text_run.text

                if len(paragraph.text_run_lst) > 0:
                    # logger.info(f"======================")
                    # logger.info(paragraph.xml)
                    return False

        # 图片填充并且不为空
        return not (isinstance(self.fill_style, BlipFill) and self.fill_style.blip and self.fill_style.blip.r_embed)

    @property
    def text_body(self):
        """文本框"""

        if self.oxml.text_body is None:
            return None

        return TextBody(self, self.oxml.text_body)

    @property
    def text(self):
        """形状文本"""

        text_body = self.oxml.text_body

        txts = []

        if text_body is not None:
            for paragraph in text_body.text_paragraphs:
                for text_run in paragraph.text_run_lst:
                    if isinstance(text_run, CT_RegularTextRun):
                        txts.append(text_run.t)

                    elif isinstance(text_run, CT_TextLineBreak):
                        continue

                    else:
                        txts.append(text_run.t or '')

        return ''.join(txts)

    @property
    def has_text(self):
        """是否有文本

        1. 不是文本框
        2. 没有任何文本标签
        """

        if self.is_text_box:
            return True

        return bool(self.text) is True


class GraphFrameShape:
    """图框形状

    19.3.1.21 graphicFrame

    包含由外部源生成的图形，并且需要一个容器来在幻灯片表面上显示
    """

    def __init__(
        self,
        slide: Slide | SlideLayout | SlideMaster,
        oxml: CT_GraphicalObjectFrame,
        parent: GroupShape | ShapeTree,
    ) -> None:
        """图框形状

        19.3.1.21 graphicFrame

        包含由外部源生成的图形，并且需要一个容器来在幻灯片表面上显示
        """

        self.slide = slide
        self.oxml = oxml
        self.parent = parent

    @property
    def is_from_master(self):
        """是否来自母板"""
        return isinstance(self.slide, SlideMaster)

    @property
    def is_from_layout(self):
        """是否来自母板"""
        return isinstance(self.slide, SlideLayout)

    @property
    def id(self):
        """形状ID"""

        return self.oxml.nv_graphic_frame_pr.c_nv_pr.id

    @property
    def name(self):
        """形状名称"""

        return self.oxml.nv_graphic_frame_pr.c_nv_pr.name

    @property
    def desc(self):
        """形状的替代文本"""

        return self.oxml.nv_graphic_frame_pr.c_nv_pr.desc

    @property
    def is_hidden(self):
        """形状的替代文本"""

        return self.oxml.nv_graphic_frame_pr.c_nv_pr.hidden

    @property
    def title(self):
        """形状的标题"""

        return self.oxml.nv_graphic_frame_pr.c_nv_pr.title

    @property
    def placeholder_info(self):
        """占位符信息"""

        return to_placeholder_info(self.oxml.nv_graphic_frame_pr.nv_pr.placeholder)

    @property
    def xfrm(self) -> ShapeTransform2D:
        """图形变换信息"""

        if self.oxml.xfrm is not None:
            return to_2d_xfrm(self.oxml.xfrm)

        if self.placeholder_info is not None:
            ph_id = self.placeholder_info.index
            ph_type = self.placeholder_info.type

            # 当前幻灯片为幻灯片时，获取使用布局的位置
            if self.slide.slide_type == 'slide' and isinstance(self.slide.layout, SlideLayout):
                for layout_ph_sp in self.slide.layout.shape_tree.shapes:
                    if (
                        layout_ph_sp.placeholder_info is not None
                        and ph_id == layout_ph_sp.placeholder_info.index
                        and ph_type == layout_ph_sp.placeholder_info.type
                    ):
                        return layout_ph_sp.xfrm  # type: ignore

            # 当前幻灯片为布局时，获取使用母板的位置
            elif self.slide.slide_type == 'slideLayout' and isinstance(self.slide.master, SlideMaster):
                for master_ph_sp in self.slide.master.shape_tree.shapes:
                    if (
                        master_ph_sp.placeholder_info is not None
                        and ph_id == master_ph_sp.placeholder_info.index
                        and ph_type == master_ph_sp.placeholder_info.type
                    ):
                        return master_ph_sp.xfrm  # type: ignore

        msg = f'[{self.slide.slide_type}-{self.slide.index}-{self.name}]获取位置失败(xfrm)'
        raise XfrmNotExistsError(msg)

    @property
    def abs_xfrm(self):
        """图形绝对位置变换信息"""

        if isinstance(self.parent, ShapeTree):
            return self.xfrm

        return to_abs_xfrm(self.xfrm, self.parent.abs_xfrm)

    @property
    def x(self):
        """图形的x轴位置, 未经过任何处理"""

        return self.xfrm.off.x

    @property
    def y(self):
        """图形的y轴位置, 未经过任何处理"""

        return self.xfrm.off.y

    @property
    def w(self):
        """图形的宽度, 未经过任何处理"""

        return self.xfrm.ext.cx

    @property
    def h(self):
        """图形的高度, 未经过任何处理"""

        return self.xfrm.ext.cy

    @property
    def abs_x(self):
        """图形的x轴绝对位置, 相对于幻灯片左上角(0,0)"""

        return self.abs_xfrm.off.x

    @property
    def abs_y(self):
        """图形的y轴绝对位置, 相对于幻灯片左上角(0,0)"""

        return self.abs_xfrm.off.y

    @property
    def abs_w(self):
        """图形的绝对宽度,  解组合后的，未经过缩放的宽度"""

        return self.abs_xfrm.ext.cx

    @property
    def abs_h(self):
        """图形的绝对高度,  解组合后的，未经过缩放的高度"""

        return self.abs_xfrm.ext.cy

    @property
    def relative_x(self):
        """图形的x轴相对父级的位置, 针对组合中的图形"""

        if isinstance(self.parent, ShapeTree):
            return self.abs_x

        return Emu(self.abs_x - self.parent.abs_x)

    @property
    def relative_y(self):
        """图形的y轴相对父级的位置, 针对组合中的图形"""

        if isinstance(self.parent, ShapeTree):
            return self.abs_y

        return Emu(self.abs_y - self.parent.abs_y)

    @property
    def flip_v(self):
        """图形是否垂直翻转"""

        return self.xfrm.flipV

    @property
    def flip_h(self):
        """图形是否水平翻转"""

        return self.xfrm.flipH

    @property
    def rotate(self):
        """图形渲染角度， 默认为 0"""

        return self.xfrm.rot

    @property
    def is_pure_graph(self):
        """是否为纯绘制图形, 也就是svg要表示的图形

        1. 不是文本框
        2. 没有任何文本标签
        """

        return False

    # ------ 绘制数据 ----

    @property
    def graphic_data(self):
        """绘制数据"""
        return self.oxml.graphic.graphic_data

    @property
    def text_body(self):
        """文本框"""

        return None


class ConnectorShape:
    """连接形状

    19.3.1.19 cxnSp

    该元素指定用于连接两个 sp 元素的连接形状。 使用 cxnSp 指定连接后，生成应用程序将确定连接器采用的确切路径。 也就是说，连接器路由算法由生成的应用程序决定，因为所需的路径可能会根据应用程序的特定需求而有所不同。
    """

    def __init__(
        self,
        slide: Slide | SlideLayout | SlideMaster,
        oxml: CT_Connector,
        parent: GroupShape | ShapeTree,
    ) -> None:
        """连接形状

        19.3.1.19 cxnSp

        该元素指定用于连接两个 sp 元素的连接形状。 使用 cxnSp 指定连接后，生成应用程序将确定连接器采用的确切路径。 也就是说，连接器路由算法由生成的应用程序决定，因为所需的路径可能会根据应用程序的特定需求而有所不同。
        """
        self.slide = slide
        self.oxml = oxml
        self.parent = parent

        self._svg_viewbox: Optional[SvgViewBox] = None

    @property
    def is_from_master(self):
        """是否来自母板"""
        return isinstance(self.slide, SlideMaster)

    @property
    def is_from_layout(self):
        """是否来自母板"""
        return isinstance(self.slide, SlideLayout)

    @property
    def id(self):
        """形状ID"""

        return self.oxml.nv_cxn_sp_pr.c_nv_pr.id

    @property
    def name(self):
        """形状名称"""

        return self.oxml.nv_cxn_sp_pr.c_nv_pr.name

    @property
    def desc(self):
        """形状的替代文本"""

        return self.oxml.nv_cxn_sp_pr.c_nv_pr.desc

    @property
    def is_hidden(self):
        """形状的替代文本"""

        return self.oxml.nv_cxn_sp_pr.c_nv_pr.hidden

    @property
    def title(self):
        """形状的标题"""

        return self.oxml.nv_cxn_sp_pr.c_nv_pr.title

    @property
    def placeholder_info(self):
        """占位符信息"""

        return to_placeholder_info(self.oxml.nv_cxn_sp_pr.nv_pr.placeholder)

    @property
    def viewbox(self):
        """获取当前图形的用户坐标系"""

        if self._svg_viewbox is None:
            # 当在svg中绘制时的用户坐标
            # 默认线宽/高 2磅
            line_width = Pt(2).emu

            if self.line_style:
                line_width = self.line_style.width

            w = self.abs_w or line_width
            h = self.abs_h or line_width

            self._svg_viewbox = SvgViewBox(0, 0, w, h)

        return self._svg_viewbox

    @viewbox.setter
    def viewbox(self, box: SvgViewBox):
        """设置当前图形的用户坐标系

        针对 line 类型的图形，在有箭头符号时， 会重新计算 viewbox 的大小和尺寸。
        """

        self._svg_viewbox = box

    @property
    def xfrm(self) -> ShapeTransform2D:
        if self.oxml.sp_pr.xfrm is not None:
            return to_2d_xfrm(self.oxml.sp_pr.xfrm)

        if self.placeholder_info is not None:
            ph_id = self.placeholder_info.index
            ph_type = self.placeholder_info.type

            # 当前幻灯片为幻灯片时，获取使用布局的位置
            if self.slide.slide_type == 'slide' and isinstance(self.slide.layout, SlideLayout):
                for layout_ph_sp in self.slide.layout.shape_tree.shapes:
                    if (
                        layout_ph_sp.placeholder_info is not None
                        and ph_id == layout_ph_sp.placeholder_info.index
                        and ph_type == layout_ph_sp.placeholder_info.type
                    ):
                        return layout_ph_sp.xfrm  # type: ignore

            # 当前幻灯片为布局时，获取使用母板的位置
            elif self.slide.slide_type == 'slideLayout' and isinstance(self.slide.master, SlideMaster):
                for master_ph_sp in self.slide.master.shape_tree.shapes:
                    if (
                        master_ph_sp.placeholder_info is not None
                        and ph_id == master_ph_sp.placeholder_info.index
                        and ph_type == master_ph_sp.placeholder_info.type
                    ):
                        return master_ph_sp.xfrm  # type: ignore

        msg = f'[{self.slide.slide_type}-{self.slide.index}-{self.name}]获取位置失败(xfrm)'
        raise XfrmNotExistsError(msg)

    @property
    def abs_xfrm(self):
        """图形绝对位置变换信息"""

        if isinstance(self.parent, ShapeTree):
            return self.xfrm

        return to_abs_xfrm(self.xfrm, self.parent.abs_xfrm)

    @property
    def x(self):
        """图形的x轴位置, 未经过任何处理"""

        return self.xfrm.off.x

    @property
    def y(self):
        """图形的y轴位置, 未经过任何处理"""

        return self.xfrm.off.y

    @property
    def w(self):
        """图形的宽度, 未经过任何处理"""

        return self.xfrm.ext.cx

    @property
    def h(self):
        """图形的高度, 未经过任何处理"""

        return self.xfrm.ext.cy

    @property
    def abs_x(self):
        """图形的x轴绝对位置, 相对于幻灯片左上角(0,0)"""

        return self.abs_xfrm.off.x

    @property
    def abs_y(self):
        """图形的y轴绝对位置, 相对于幻灯片左上角(0,0)"""

        return self.abs_xfrm.off.y

    @property
    def abs_w(self):
        """图形的绝对宽度,  解组合后的，未经过缩放的宽度"""

        return self.abs_xfrm.ext.cx

    @property
    def abs_h(self):
        """图形的绝对高度,  解组合后的，未经过缩放的高度"""

        return self.abs_xfrm.ext.cy

    @property
    def relative_x(self):
        """图形的x轴相对父级的位置, 针对组合中的图形"""

        if isinstance(self.parent, ShapeTree):
            return self.abs_x

        return Emu(self.abs_x - self.parent.abs_x)

    @property
    def relative_y(self):
        """图形的y轴相对父级的位置, 针对组合中的图形"""

        if isinstance(self.parent, ShapeTree):
            return self.abs_y

        return Emu(self.abs_y - self.parent.abs_y)

    @property
    def flip_v(self):
        """图形是否垂直翻转"""

        return self.xfrm.flipV

    @property
    def flip_h(self):
        """图形是否水平翻转"""

        return self.xfrm.flipH

    @property
    def rotate(self):
        """图形渲染角度， 默认为 0"""

        return self.xfrm.rot

    @property
    def style(self):
        """形状的样式"""

        if self.oxml.style is not None:
            return ShapeStyle(self, self.oxml.style)

        return None

    @property
    def is_preset_shape(self):
        """是否为预置图形

        连接器图形应该永远都是内置图形并且拥有 prst 属性，并且为 ShapeType.Line

        """
        prstGeom = self.oxml.sp_pr.geometry

        if prstGeom is None:
            return False

        return isinstance(prstGeom, CT_PresetGeometry2D)

        # if is_preset_geom and prstGeom.preset != ST_ShapeType.Line:
        #     logger.warn(f"连接器的形状，预置图形不是: {ST_ShapeType.Line = }")
        #     return False


    @property
    def preset_shape_type(self) -> ST_ShapeType:
        """是否为预置图形 并且不是 文本框

        如果形状具有 ``<a:prstGeom>`` 元素并且在 cNvSpPr 上没有 txBox="1" 属性，则该形状是自动形状。
        """

        if not self.is_preset_shape:
            msg = f'[slide-{self.slide.index}][{self.name}]该图形不是预置图形, 请先通过 is_preset_shape 判断 再获取预制图形类型'
            raise ValueError(
                msg
            )

        prstGeom = self.oxml.sp_pr.geometry

        return prstGeom.preset  # type: ignore

    @property
    def line_style(self):
        """形状线条的样式"""

        line = self.oxml.sp_pr.line

        if line is None:
            return None

        return LineStyle(line)

    @property
    def fill_style(self):
        """形状的填充样式"""

        fill = self.oxml.sp_pr.fill

        return fill_factory(fill)

    @property
    def is_pure_graph(self):
        """是否为纯绘制图形, 也就是svg要表示的图形

        1. 不是文本框
        2. 没有任何文本标签
        """

        return True

    @property
    def text_body(self):
        """文本框"""

        return None


class PictureShape:
    """图片形状

    19.3.1.37 pic

    该元素指定文档中是否存在图片对象。
    """

    def __init__(
        self,
        slide: Slide | SlideLayout | SlideMaster,
        oxml: CT_Picture,
        # GraphFrameShape 表明时ole标签中的图片
        parent: GroupShape | ShapeTree | GraphFrameShape,
        true_id: Optional[int] = None,
    ) -> None:
        """图片形状

        19.3.1.37 pic

        该元素指定文档中是否存在图片对象。
        """

        self.slide = slide
        self.oxml = oxml
        self.parent = parent

        # 参考: 19.3.2.4 oleObj (嵌入式对象和控件的全局元素)
        # https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter19/slides/#19324-oleobj-嵌入式对象和控件的全局元素
        # 可能是由兼容性标签构造的图片对象，所以这里要传入真实的ID
        self.true_id = true_id

    @property
    def is_from_master(self):
        """是否来自母板"""
        return isinstance(self.slide, SlideMaster)

    @property
    def is_from_layout(self):
        """是否来自母板"""
        return isinstance(self.slide, SlideLayout)

    @property
    def id(self):
        """形状ID"""

        # 参考: 19.3.2.4 oleObj (嵌入式对象和控件的全局元素)
        # https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter19/slides/#19324-oleobj-嵌入式对象和控件的全局元素
        # 可能是由兼容性标签构造的图片对象，所以这里要返回真实的ID
        if self.true_id is not None:
            return self.true_id

        return self.oxml.nv_pic_pr.c_nv_pr.id

    @property
    def name(self):
        """形状名称"""

        return self.oxml.nv_pic_pr.c_nv_pr.name

    @property
    def desc(self):
        """形状的替代文本"""

        return self.oxml.nv_pic_pr.c_nv_pr.desc

    @property
    def is_hidden(self):
        """形状的替代文本"""

        return self.oxml.nv_pic_pr.c_nv_pr.hidden

    @property
    def title(self):
        """形状的标题"""

        return self.oxml.nv_pic_pr.c_nv_pr.title

    @property
    def placeholder_info(self):
        """占位符信息"""

        return to_placeholder_info(self.oxml.nv_pic_pr.nv_pr.placeholder)

    @property
    def xfrm(self) -> ShapeTransform2D:
        """图形变换信息"""

        if self.oxml.sp_pr.xfrm is not None:
            return to_2d_xfrm(self.oxml.sp_pr.xfrm)

        if self.placeholder_info is not None:
            ph_id = self.placeholder_info.index
            ph_type = self.placeholder_info.type

            # 当前幻灯片为幻灯片时，获取使用布局的位置
            if self.slide.slide_type == 'slide' and isinstance(self.slide.layout, SlideLayout):
                for layout_ph_sp in self.slide.layout.shape_tree.shapes:
                    if (
                        layout_ph_sp.placeholder_info is not None
                        and ph_id == layout_ph_sp.placeholder_info.index
                        and ph_type == layout_ph_sp.placeholder_info.type
                    ):
                        return layout_ph_sp.xfrm  # type: ignore

            # 当前幻灯片为布局时，获取使用母板的位置
            elif self.slide.slide_type == 'slideLayout' and isinstance(self.slide.master, SlideMaster):
                for master_ph_sp in self.slide.master.shape_tree.shapes:
                    if (
                        master_ph_sp.placeholder_info is not None
                        and ph_id == master_ph_sp.placeholder_info.index
                        and ph_type == master_ph_sp.placeholder_info.type
                    ):
                        return master_ph_sp.xfrm  # type: ignore

        msg = f'[{self.slide.slide_type}-{self.slide.index}-{self.name}]获取位置失败(xfrm)'
        raise XfrmNotExistsError(msg)

    @property
    def abs_xfrm(self):
        """图形绝对位置变换信息"""

        if isinstance(self.parent, ShapeTree):
            return self.xfrm

        # 说明时ole标签中的形状
        if isinstance(self.parent, GraphFrameShape):
            return self.parent.abs_xfrm

        return to_abs_xfrm(self.xfrm, self.parent.abs_xfrm)

    @property
    def x(self):
        """图形的x轴位置, 未经过任何处理"""

        return self.xfrm.off.x

    @property
    def y(self):
        """图形的y轴位置, 未经过任何处理"""

        return self.xfrm.off.y

    @property
    def w(self):
        """图形的宽度, 未经过任何处理"""

        return self.xfrm.ext.cx

    @property
    def h(self):
        """图形的高度, 未经过任何处理"""

        return self.xfrm.ext.cy

    @property
    def abs_x(self):
        """图形的x轴绝对位置, 相对于幻灯片左上角(0,0)"""

        return self.abs_xfrm.off.x

    @property
    def abs_y(self):
        """图形的y轴绝对位置, 相对于幻灯片左上角(0,0)"""

        return self.abs_xfrm.off.y

    @property
    def abs_w(self):
        """图形的绝对宽度,  解组合后的，未经过缩放的宽度"""

        return self.abs_xfrm.ext.cx

    @property
    def abs_h(self):
        """图形的绝对高度,  解组合后的，未经过缩放的高度"""

        return self.abs_xfrm.ext.cy

    @property
    def relative_x(self):
        """图形的x轴相对父级的位置, 针对组合中的图形"""

        if isinstance(self.parent, ShapeTree):
            return self.abs_x

        return Emu(self.abs_x - self.parent.abs_x)

    @property
    def relative_y(self):
        """图形的y轴相对父级的位置, 针对组合中的图形"""

        if isinstance(self.parent, ShapeTree):
            return self.abs_y

        return Emu(self.abs_y - self.parent.abs_y)

    @property
    def flip_v(self):
        """图形是否垂直翻转"""

        return self.xfrm.flipV

    @property
    def flip_h(self):
        """图形是否水平翻转"""

        return self.xfrm.flipH

    @property
    def rotate(self):
        """图形渲染角度， 默认为 0"""

        return self.xfrm.rot

    @property
    def media(self):
        """媒体文件"""

        return media_factory(self.slide, self, self.oxml.nv_pic_pr.nv_pr.media)

    @property
    def is_meidia_video(self):
        """是否为媒体文件中的视频文件"""

        return isinstance(self.media, VideoFile)

    @property
    def is_meidia_audio(self):
        """是否为媒体文件中的音频文件"""

        return isinstance(self.media, AudioFile)

    @property
    def line_style(self):
        """形状线条的样式"""

        line = self.oxml.sp_pr.line

        if line is None:
            return None

        return LineStyle(line)

    @property
    def effect_style(self):
        """形状的效果"""

        effect = self.oxml.sp_pr.effect

        if effect is None:
            return None

        return effect_factory(effect)

    @property
    def blip_effect(self):
        """图片填充的效果"""

        blip = self.oxml.blip_fill.blip

        if blip is not None:
            return BlipEffect(blip)

        return None

    @property
    def is_preset_shape(self):
        """是否为预置图形

        如果形状具有 ``<a:prstGeom>`` 元素, 则该形状是预制形状。
        """
        prstGeom = self.oxml.sp_pr.geometry

        if prstGeom is None:
            return False

        return isinstance(prstGeom, CT_PresetGeometry2D)


    @property
    def preset_shape_type(self) -> ST_ShapeType:
        """是否为预置图形 并且不是 文本框

        如果形状具有 ``<a:prstGeom>`` 元素并且在 cNvSpPr 上没有 txBox="1" 属性，则该形状是自动形状。
        """

        if not self.is_preset_shape:
            msg = '该图形不是预置图形, 请先通过 is_preset_shape 判断 再获取预制图形类型'
            raise ValueError(msg)

        prstGeom = self.oxml.sp_pr.geometry

        return prstGeom.preset  # type: ignore

    @property
    def is_pure_graph(self):
        """是否为纯绘制图形, 也就是svg要表示的图形

        1. 不是文本框
        2. 没有任何文本标签
        """

        return False

    @property
    def image(self):
        """

        具体的图片文件 使用 slide 的 get_image(rid) 方法.
        """

        # 图片关系ID
        blip = self.oxml.blip_fill.blip

        if blip is None:
            return None

        rid = blip.r_embed

        return self.slide.get_image(rid)

    @property
    def image_rlink(self):
        """图片文件参考连接, 指外部图片参考链接"""

        blip = self.oxml.blip_fill.blip

        if blip is None:
            return None

        return blip.r_link

    @property
    def locks(self):
        """图片的锁定信息"""

        return self.oxml.nv_pic_pr.c_nv_pic_pr.picture_locks

    @property
    def no_change_aspect(self) -> bool:
        """禁止更改宽高比, 默认 False"""

        if self.locks is not None:
            return self.locks.no_change_aspect

        return False

    @property
    def no_crop(self) -> bool:
        """不允许裁减

        指定生成应用程序不应允许裁剪相应的图片。 如果未指定此属性，则假定值为 false。
        """

        if self.locks is not None:
            return self.locks.no_crop

        return False

    @property
    def crop_info(self):
        """图片裁减信息"""

        if self.no_crop:
            msg = f'[{self.name}] 的 图片不允许裁减'
            raise AttributeError(msg)

        return self.oxml.blip_fill.src_rect

    @property
    def text_body(self):
        """文本框"""

        return None


class ContentPartShape:
    """内容部分

    此元素指定对 XML 内容的引用，其格式未由 ECMA-376 定义。
    """

    def __init__(
        self,
        slide: Slide | SlideLayout | SlideMaster,
        oxml: CT_Rel,
        parent: GroupShape | ShapeTree,
    ) -> None:
        """图片形状

        此元素指定对 XML 内容的引用，其格式未由 ECMA-376 定义。

        这部分允许本机使用其他常用的交换格式，例如：

        - MathML (http://www.w3.org/TR/MathML2/)
        - SMIL (http://www.w3.org/TR/REC-smil/)
        - SVG (http://www.w3.org/TR/SVG11/)
        """

        self.slide = slide
        self.oxml = oxml
        self.parent = parent

    @property
    def is_from_master(self):
        """是否来自母板"""
        return isinstance(self.slide, SlideMaster)

    @property
    def is_from_layout(self):
        """是否来自母板"""
        return isinstance(self.slide, SlideLayout)

    @property
    def id(self):
        """唯一ID"""

        return f'ContentPart(rid={self.oxml.relationship_id})'

    @property
    def name(self):
        """关系ID"""

        return f'ContentPart(rid={self.oxml.relationship_id})'

    @property
    def is_hidden(self):
        """是否隐藏, 为了兼容"""

        return False

    @property
    def relationship_id(self):
        """关系ID"""

        return self.oxml.relationship_id

    @property
    def placeholder_info(self):
        """占位符信息"""

        return to_placeholder_info(None)

    @property
    def xfrm(self):
        """位置信息"""

        msg = f'[{self.slide.slide_type}-{self.slide.index}-{self.name}]获取位置失败(xfrm)'
        raise XfrmNotExistsError(msg)

    def abs_xfrm(self):
        """图形绝对位置变换信息"""

        return None

    @property
    def line_style(self):
        """形状线条的样式"""

        return None

    @property
    def is_pure_graph(self):
        """是否为纯绘制图形, 也就是svg要表示的图形

        1. 不是文本框
        2. 没有任何文本标签
        """

        return False

    @property
    def text_body(self):
        """文本框"""

        return None


class GroupShape:
    """组合形状

    19.3.1.22 grpSp

    该元素指定一个组形状，表示组合在一起的许多形状。 该形状应被视为规则形状，但不是由单个几何形状来描述，而是由其中包含的所有形状几何形状组成。 在组形状中，组成该组的每个形状都按照通常的方式指定。 然而，对元素进行分组的想法是，单个变换可以同时应用于多个形状。
    """

    def __init__(
        self,
        slide: Slide | SlideLayout | SlideMaster,
        oxml: CT_GroupShape,
        parent: GroupShape | ShapeTree,
    ) -> None:
        """组合形状

        19.3.1.22 grpSp

        该元素指定一个组形状，表示组合在一起的许多形状。 该形状应被视为规则形状，但不是由单个几何形状来描述，而是由其中包含的所有形状几何形状组成。 在组形状中，组成该组的每个形状都按照通常的方式指定。 然而，对元素进行分组的想法是，单个变换可以同时应用于多个形状。
        """

        self.slide = slide
        self.oxml = oxml
        self.parent = parent

    def __iter__(self):
        return self.oxml.shape_lst

    @property
    def is_from_master(self):
        """是否来自母板"""
        return isinstance(self.slide, SlideMaster)

    @property
    def is_from_layout(self):
        """是否来自母板"""
        return isinstance(self.slide, SlideLayout)

    @property
    def id(self):
        """形状ID"""

        return self.oxml.nv_grp_sp_pr.c_nv_pr.id

    @property
    def name(self):
        """形状名称"""

        return self.oxml.nv_grp_sp_pr.c_nv_pr.name

    @property
    def desc(self):
        """形状的替代文本"""

        return self.oxml.nv_grp_sp_pr.c_nv_pr.desc

    @property
    def is_hidden(self):
        """形状的替代文本"""

        return self.oxml.nv_grp_sp_pr.c_nv_pr.hidden

    @property
    def title(self):
        """形状的标题"""

        return self.oxml.nv_grp_sp_pr.c_nv_pr.title

    @property
    def placeholder_info(self):
        """占位符信息"""

        return to_placeholder_info(self.oxml.nv_grp_sp_pr.nv_pr.placeholder)

    @property
    def xfrm(self) -> GroupShapeTransform2D:
        """图形变换信息"""

        if self.oxml.grp_sp_pr.xfrm is not None:
            return to_group_2d_xfrm(self.oxml.grp_sp_pr.xfrm)

        if self.placeholder_info is not None:
            ph_id = self.placeholder_info.index
            ph_type = self.placeholder_info.type

            # 当前幻灯片为幻灯片时，获取使用布局的位置
            if self.slide.slide_type == 'slide' and isinstance(self.slide.layout, SlideLayout):
                for layout_ph_sp in self.slide.layout.shape_tree.shapes:
                    if (
                        layout_ph_sp.placeholder_info is not None
                        and ph_id == layout_ph_sp.placeholder_info.index
                        and ph_type == layout_ph_sp.placeholder_info.type
                    ):
                        return layout_ph_sp.xfrm  # type: ignore

            # 当前幻灯片为布局时，获取使用母板的位置
            elif self.slide.slide_type == 'slideLayout' and isinstance(self.slide.master, SlideMaster):
                for master_ph_sp in self.slide.master.shape_tree.shapes:
                    if (
                        master_ph_sp.placeholder_info is not None
                        and ph_id == master_ph_sp.placeholder_info.index
                        and ph_type == master_ph_sp.placeholder_info.type
                    ):
                        return master_ph_sp.xfrm  # type: ignore

        msg = f'[{self.slide.slide_type}-{self.slide.index}-{self.name}]获取位置失败(xfrm)'
        raise XfrmNotExistsError(msg)

    @property
    def abs_xfrm(self):
        """图形绝对位置变换信息"""

        if isinstance(self.parent, ShapeTree):
            # 图形树的xfrm就是绝对位置的变换信息
            return self.xfrm

        return to_abs_group_xfrm(self.xfrm, self.parent.abs_xfrm)

    @property
    def x(self):
        """图形的x轴位置, 未经过任何处理"""

        return self.xfrm.off.x

    @property
    def y(self):
        """图形的y轴位置, 未经过任何处理"""

        return self.xfrm.off.y

    @property
    def w(self):
        """图形的宽度, 未经过任何处理"""

        return self.xfrm.ext.cx

    @property
    def h(self):
        """图形的高度, 未经过任何处理"""

        return self.xfrm.ext.cy

    @property
    def abs_x(self):
        """图形的x轴绝对位置, 相对于幻灯片左上角(0,0)"""

        return self.abs_xfrm.off.x

    @property
    def abs_y(self):
        """图形的y轴绝对位置, 相对于幻灯片左上角(0,0)"""

        return self.abs_xfrm.off.y

    @property
    def abs_w(self):
        """图形的绝对宽度,  解组合后的，未经过缩放的宽度"""

        return self.abs_xfrm.ext.cx

    @property
    def abs_h(self):
        """图形的绝对高度,  解组合后的，未经过缩放的高度"""

        return self.abs_xfrm.ext.cy

    @property
    def relative_x(self):
        """图形的x轴相对父级的位置, 针对组合中的图形"""

        if isinstance(self.parent, ShapeTree):
            return self.abs_x

        return Emu(self.abs_x - self.parent.abs_x)

    @property
    def relative_y(self):
        """图形的y轴相对父级的位置, 针对组合中的图形"""

        if isinstance(self.parent, ShapeTree):
            return self.abs_y

        return Emu(self.abs_y - self.parent.abs_y)

    @property
    def flip_v(self):
        """图形是否垂直翻转"""

        return self.xfrm.flipV

    @property
    def flip_h(self):
        """图形是否水平翻转"""

        return self.xfrm.flipH

    @property
    def rotate(self):
        """图形渲染角度， 默认为 0"""

        return self.xfrm.rot

    @property
    def scale_factor_x(self):
        """x轴缩放因子"""

        xfrm = self.xfrm

        return (xfrm.ext.cx / xfrm.chExt.cx) if xfrm.chExt.cx != 0 else 1.0

    @property
    def scale_factor_y(self):
        """y轴缩放因子"""

        xfrm = self.xfrm

        return (xfrm.ext.cy / xfrm.chExt.cy) if xfrm.chExt.cy != 0 else 1.0

    @property
    def style(self):
        """形状的样式"""

        return None

    @property
    def line_style(self):
        """形状线条的样式

        组合图形没有线条样式
        """

        return None

    @property
    def fill_style(self):
        """形状的填充样式"""

        fill = self.oxml.grp_sp_pr.fill

        return fill_factory(fill)

    @property
    def effect_style(self):
        """形状的效果"""

        effect = self.oxml.grp_sp_pr.effect

        if effect is None:
            return None

        return effect_factory(effect)

    @property
    def shapes(self):
        """返回该组的子形状"""
        for ct_shape in self.oxml.shape_lst:
            if isinstance(ct_shape, CT_GroupShape):
                yield GroupShape(self.slide, ct_shape, self)

            elif isinstance(ct_shape, CT_Shape):
                yield NormalShape(self.slide, ct_shape, self)

            elif isinstance(ct_shape, CT_GraphicalObjectFrame):
                yield GraphFrameShape(self.slide, ct_shape, self)

            elif isinstance(ct_shape, CT_Connector):
                yield ConnectorShape(self.slide, ct_shape, self)

            elif isinstance(ct_shape, CT_Picture):
                yield PictureShape(self.slide, ct_shape, self)

            elif isinstance(ct_shape, CT_Rel):
                yield ContentPartShape(self.slide, ct_shape, self)

    @property
    def text_body(self):
        """文本框"""

        return None


class ShapeTree:
    """封装slide元素下的根形状树"""

    def __init__(self, slide: Any, oxml: CT_GroupShape) -> None:  # .slide.Slide
        """slide形状树

        此元素指定对 XML 内容的引用，其格式未由 ECMA-376 定义。

        这部分允许本机使用其他常用的交换格式，例如：

        - MathML (http://www.w3.org/TR/MathML2/)
        - SMIL (http://www.w3.org/TR/REC-smil/)
        - SVG (http://www.w3.org/TR/SVG11/)
        """

        self.slide: Slide | SlideLayout | SlideMaster = slide
        self.oxml = oxml

    @property
    def is_from_master(self):
        """是否来自母板"""
        return isinstance(self.slide, SlideMaster)

    @property
    def is_from_layout(self):
        """是否来自母板"""
        return isinstance(self.slide, SlideLayout)

    @property
    def shapes(self):
        """返回该组的子形状"""
        for ct_shape in self.oxml.shape_lst:
            # logger.info(f"形状树子形状: {type(ct_shape) = }")
            if isinstance(ct_shape, CT_GroupShape):
                yield GroupShape(self.slide, ct_shape, self)

            elif isinstance(ct_shape, CT_Shape):
                yield NormalShape(self.slide, ct_shape, self)

            elif isinstance(ct_shape, CT_GraphicalObjectFrame):
                yield GraphFrameShape(self.slide, ct_shape, self)

            elif isinstance(ct_shape, CT_Connector):
                yield ConnectorShape(self.slide, ct_shape, self)

            elif isinstance(ct_shape, CT_Picture):
                yield PictureShape(self.slide, ct_shape, self)

            elif isinstance(ct_shape, CT_Rel):
                yield ContentPartShape(self.slide, ct_shape, self)

            elif isinstance(ct_shape, CT_MC_AlternateContent):
                ele = self.choice_mc_alternateContent(ct_shape)

                if ele is not None:
                    yield ele

                else:
                    continue

    def choice_mc_alternateContent(self, ele: CT_MC_AlternateContent):
        """解析嵌入的对象"""

        # namespace_p
        # 优先从fallback 元素中获取对象，这个是对旧的版本软件做的兼容。
        shape = getattr(ele.fallback, qn('p:sp'), None)  # <p:sp/>

        if ele.fallback and getattr(ele.fallback, 'picture', None) is not None:
            return PictureShape(self.slide, ele.fallback.picture, self)  # type: ignore

        if shape is not None:
            logger.info('获取的到嵌入的shape对象: shape')
            return NormalShape(self.slide, shape, self)

        logger.info('未获取到嵌入对象:')
        logger.info(ele.xml)

        return None


ShapeTypes = Union[
    NormalShape,
    GraphFrameShape,
    ConnectorShape,
    PictureShape,
    ContentPartShape,
    GroupShape,
]
