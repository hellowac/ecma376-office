from __future__ import annotations

import logging
from typing import TYPE_CHECKING, NamedTuple

logger = logging.getLogger(__name__)

from ecma376_office.units import Emu

if TYPE_CHECKING:
    from ecma376_office.oxml.dml.main import CT_GroupTransform2D, CT_Transform2D


class TransformOff(NamedTuple):
    """几何图形位置偏移信息"""

    x: Emu
    """ X轴偏移 """

    y: Emu
    """ Y轴偏移 """


class TransformExt(NamedTuple):
    """几何图形范围信息"""

    cx: Emu
    """ 宽度信息 """

    cy: Emu
    """ 高度信息 """


class TransformChOff(NamedTuple):
    """几何组图形位置偏移信息"""

    x: Emu
    """ X轴子图形偏移 """

    y: Emu
    """ Y轴子图形偏移 """


class TransformChExt(NamedTuple):
    """几何组图形范围信息"""

    cx: Emu
    """ 子图形宽度信息 """

    cy: Emu
    """ 子图形高度信息 """


class ShapeTransform2D(NamedTuple):
    """图形通用的关于定位和宽高的定义"""

    off: TransformOff
    """ 图形偏移信息 """

    ext: TransformExt
    """ 图形范围信息 """

    flipH: bool
    """ 是否水平翻转 """

    flipV: bool
    """ 是否垂直翻转 """

    rot: float
    """ 旋转的角度 """


class GroupShapeTransform2D(NamedTuple):
    """图形通用的关于组合图形定位和宽高的定义"""

    off: TransformOff
    """ 组合图形偏移信息 """

    ext: TransformExt
    """ 组合图形范围信息 """

    chOff: TransformChOff
    """ 子图形偏移信息 """

    chExt: TransformChExt
    """ 子图形范围信息 """

    flipH: bool
    """ 是否水平翻转 """

    flipV: bool
    """ 是否垂直翻转 """

    rot: float
    """ 旋转的角度 """


def init_2d_xfrm():
    """初始化2dXfrm"""

    offset = TransformOff(Emu(0), Emu(0))
    extent = TransformExt(Emu(0), Emu(0))

    return ShapeTransform2D(offset, extent, False, False, 0)


def init_group_2d_xfrm():
    """初始化2dXfrm"""

    offset = TransformOff(Emu(0), Emu(0))
    extent = TransformExt(Emu(0), Emu(0))
    ch_offset = TransformChOff(Emu(0), Emu(0))
    ch_extent = TransformChExt(Emu(0), Emu(0))

    return GroupShapeTransform2D(offset, extent, ch_offset, ch_extent, False, False, 0)


def to_2d_xfrm(oxml: CT_Transform2D) -> ShapeTransform2D:
    """单个图形的变换"""

    offset = TransformOff(Emu(0), Emu(0))

    if oxml.offset is not None:
        offset = TransformOff(Emu(oxml.offset.x_val or 0), Emu(oxml.offset.y_val or 0))

    extent = TransformExt(Emu(0), Emu(0))

    if oxml.ext is not None:
        extent = TransformExt(Emu(oxml.ext.cx_val), Emu(oxml.ext.cy_val))

    return ShapeTransform2D(offset, extent, oxml.flip_H, oxml.flip_V, oxml.rotate)


def to_group_2d_xfrm(oxml: CT_GroupTransform2D) -> GroupShapeTransform2D:
    """组合图形的变换"""

    offset = TransformOff(Emu(0), Emu(0))

    if oxml.offset is not None:
        offset = TransformOff(Emu(oxml.offset.x_val or 0), Emu(oxml.offset.y_val or 0))

    extent = TransformExt(Emu(0), Emu(0))

    # logger.info(f"{type(oxml) = }")

    # logger.info(oxml.xml)

    if oxml.ext is not None:
        extent = TransformExt(Emu(oxml.ext.cx_val), Emu(oxml.ext.cy_val))

    ch_offset = TransformChOff(Emu(0), Emu(0))

    if oxml.child_offset is not None:
        ch_offset = TransformChOff(
            Emu(oxml.child_offset.x_val or 0),
            Emu(oxml.child_offset.y_val or 0),
        )

    ch_extent = TransformChExt(Emu(0), Emu(0))

    if oxml.child_extend is not None:
        ch_extent = TransformChExt(
            Emu(oxml.child_extend.cx_val),
            Emu(oxml.child_extend.cy_val),
        )

    return GroupShapeTransform2D(offset, extent, ch_offset, ch_extent, oxml.flip_H, oxml.flip_V, oxml.rotate)


def to_abs_xfrm(xfrm: ShapeTransform2D, parent_xfrm: GroupShapeTransform2D):
    """图形的相对定位转换为绝对定位

    计算图形解开组合后的定位和宽高

    参考: https://stackoverflow.com/questions/60770606/how-to-get-the-absolute-position-of-child-shapes-by-using-apache-poi
    """
    xfrm = xfrm

    # 缩放因子
    # scale_factor_x = (
    #     parent_xfrm.ext.cx / parent_xfrm.chExt.cx
    #     if parent_xfrm.chExt and parent_xfrm.chExt.cx != 0
    #     else 1
    # )
    # scale_factor_y = (
    #     parent_xfrm.ext.cy / parent_xfrm.chExt.cy
    #     if parent_xfrm.chExt and parent_xfrm.chExt.cy != 0
    #     else 1
    # )

    if parent_xfrm.chExt.cx != 0 and parent_xfrm.ext.cx != 0:
        scale_factor_x = parent_xfrm.ext.cx / parent_xfrm.chExt.cx
    else:
        scale_factor_x = 1

    if parent_xfrm.chExt.cy != 0 and parent_xfrm.ext.cy != 0:
        scale_factor_y = parent_xfrm.ext.cy / parent_xfrm.chExt.cy
    else:
        scale_factor_y = 1

    # 当宽度=子宽度=0时无法正确计算出缩放因子，采用另一个的。
    if parent_xfrm.chExt.cx == parent_xfrm.ext.cx == 0:
        scale_factor_x = scale_factor_y

    elif parent_xfrm.chExt.cy == parent_xfrm.ext.cy == 0:
        scale_factor_y = scale_factor_x

    # 计算应用缩放因子后的坐标
    # 相对定位 = (缩放的相对于父级的定位 - 子图形的缩放相对定位 ) * 缩放因子
    # 减去重合的部分
    relative_offset_x = (xfrm.off.x - (parent_xfrm.chOff.x if parent_xfrm.chOff else 0)) * scale_factor_x
    relative_offset_y = (xfrm.off.y - (parent_xfrm.chOff.y if parent_xfrm.chOff else 0)) * scale_factor_y

    # 绝对定位 = 相对定位 + 父级的绝对定位
    off_x = relative_offset_x + parent_xfrm.off.x
    off_y = relative_offset_y + parent_xfrm.off.y

    # 计算应用缩放因子后的宽高
    ext_cx = xfrm.ext.cx * scale_factor_x
    ext_cy = xfrm.ext.cy * scale_factor_y

    # 组合的子图形大小和偏移

    # 解组合后的xfrm
    return ShapeTransform2D(
        off=TransformOff(x=Emu(off_x), y=Emu(off_y)),
        ext=TransformExt(cx=Emu(ext_cx), cy=Emu(ext_cy)),
        flipH=xfrm.flipH,
        flipV=xfrm.flipV,
        rot=xfrm.rot,
    )


def to_abs_group_xfrm(xfrm: GroupShapeTransform2D, parent_xfrm: GroupShapeTransform2D):
    """图形的相对定位转换为绝对定位

    计算图形解开组合后的定位和宽高

    参考: https://stackoverflow.com/questions/60770606/how-to-get-the-absolute-position-of-child-shapes-by-using-apache-poi
    """
    xfrm = xfrm

    # 缩放因子 宽高
    # scale_factor_x = (
    #     parent_xfrm.ext.cx / parent_xfrm.chExt.cx
    #     if parent_xfrm.chExt and parent_xfrm.chExt.cx != 0
    #     else 1
    # )
    # scale_factor_y = (
    #     parent_xfrm.ext.cy / parent_xfrm.chExt.cy
    #     if parent_xfrm.chExt and parent_xfrm.chExt.cy != 0
    #     else 1
    # )

    if parent_xfrm.chExt.cx != 0 and parent_xfrm.ext.cx != 0:
        scale_factor_x = parent_xfrm.ext.cx / parent_xfrm.chExt.cx
    else:
        scale_factor_x = 1

    if parent_xfrm.chExt.cy != 0 and parent_xfrm.ext.cy != 0:
        scale_factor_y = parent_xfrm.ext.cy / parent_xfrm.chExt.cy
    else:
        scale_factor_y = 1

    # 当宽度=子宽度=0时无法正确计算出缩放因子，采用另一个的。
    if parent_xfrm.chExt.cx == parent_xfrm.ext.cx == 0:
        scale_factor_x = scale_factor_y

    elif parent_xfrm.chExt.cy == parent_xfrm.ext.cy == 0:
        scale_factor_y = scale_factor_x

    # 计算应用缩放因子后的坐标
    # 相对定位 = (缩放的相对于父级的定位 - 子图形的缩放相对定位 ) * 缩放因子
    # 减去重合的部分
    relative_offset_x = (xfrm.off.x - (parent_xfrm.chOff.x if parent_xfrm.chOff else 0)) * scale_factor_x
    relative_offset_y = (xfrm.off.y - (parent_xfrm.chOff.y if parent_xfrm.chOff else 0)) * scale_factor_y

    # 绝对定位 = 相对定位 + 父级的绝对定位
    off_x = relative_offset_x + parent_xfrm.off.x
    off_y = relative_offset_y + parent_xfrm.off.y

    # 计算应用缩放因子后的宽高
    ext_cx = xfrm.ext.cx * scale_factor_x
    ext_cy = xfrm.ext.cy * scale_factor_y

    # 组合的子图形大小和偏移

    # 缩放因子 x = (图形本身的宽高 / (子组合图形偏移 + 子组合图形宽高))
    # child_all_width = xfrm.chOff.x + xfrm.chExt.cx
    # child_all_height = xfrm.chOff.y + xfrm.chExt.cy
    # child_scale_factor_x = (
    #     (parent_xfrm.ext.cx / child_all_width) if child_all_width != 0 else 1
    # )
    # child_scale_factor_y = (
    #     (parent_xfrm.ext.cy / child_all_height) if child_all_height != 0 else 1
    # )

    # 求子图形组的未缩放的定位+宽高

    # child_off_x = child_scale_factor_x * relative_offset_x  # xfrm.chOff.x
    # child_off_y = child_scale_factor_y * relative_offset_y  # xfrm.chOff.y

    # child_ext_cx = child_scale_factor_x * ext_cx  # xfrm.ext.cx
    # child_ext_cy = child_scale_factor_y * ext_cy  # xfrm.ext.cy

    # 解组合后的xfrm
    return GroupShapeTransform2D(
        off=TransformOff(x=Emu(off_x), y=Emu(off_y)),
        ext=TransformExt(cx=Emu(ext_cx), cy=Emu(ext_cy)),
        # chOff=TransformChOff(Emu(child_off_x), Emu(child_off_y)),
        # chExt=TransformChExt(Emu(child_ext_cx), Emu(child_ext_cy)),
        chOff=xfrm.chOff,  # 直接用当前组合图形的chOff
        chExt=xfrm.chExt,  # 直接用当前组合图形的chExt
        flipH=xfrm.flipH,
        flipV=xfrm.flipV,
        rot=xfrm.rot,
    )


def to_abs_group_xfrm_back(xfrm: GroupShapeTransform2D, parent_xfrm: GroupShapeTransform2D):
    """图形的相对定位转换为绝对定位

    计算图形解开组合后的定位和宽高

    参考: https://stackoverflow.com/questions/60770606/how-to-get-the-absolute-position-of-child-shapes-by-using-apache-poi
    """
    xfrm = xfrm

    # 缩放因子
    scale_factor_x = parent_xfrm.ext.cx / parent_xfrm.chExt.cx if parent_xfrm.chExt and parent_xfrm.chExt.cx != 0 else 1
    scale_factor_y = parent_xfrm.ext.cy / parent_xfrm.chExt.cy if parent_xfrm.chExt and parent_xfrm.chExt.cy != 0 else 1

    # 计算应用缩放因子后的坐标
    # 相对定位 = (缩放的相对于父级的定位 - 子图形的缩放相对定位 ) * 缩放因子
    # 减去重合的部分
    relative_offset_x = (xfrm.off.x - (parent_xfrm.chOff.x if parent_xfrm.chOff else 0)) * scale_factor_x
    relative_offset_y = (xfrm.off.y - (parent_xfrm.chOff.y if parent_xfrm.chOff else 0)) * scale_factor_y

    # 绝对定位 = 相对定位 + 父级的绝对定位
    off_x = relative_offset_x + parent_xfrm.off.x
    off_y = relative_offset_y + parent_xfrm.off.y

    # 计算应用缩放因子后的宽高
    ext_cx = xfrm.ext.cx * scale_factor_x
    ext_cy = xfrm.ext.cy * scale_factor_y

    # 组合的子图形大小和偏移

    # 解组合后的xfrm
    return GroupShapeTransform2D(
        off=TransformOff(x=Emu(off_x), y=Emu(off_y)),
        ext=TransformExt(cx=Emu(ext_cx), cy=Emu(ext_cy)),
        chOff=xfrm.chOff,  # 直接用当前组合图形的chOff
        chExt=xfrm.chExt,  # 直接用当前组合图形的chExt
        flipH=xfrm.flipH,
        flipV=xfrm.flipV,
        rot=xfrm.rot,
    )
