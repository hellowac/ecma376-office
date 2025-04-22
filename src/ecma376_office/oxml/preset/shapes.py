"""预置图形解析类"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional, TypeVar

from ecma376_office.oxml.base import OxmlBaseElement, lookup
from ecma376_office.oxml.utils import AnyStrToStr

if TYPE_CHECKING:
    from ecma376_office.oxml.dml.main import CT_AdjustHandleList as a_CT_AdjustHandleList
    from ecma376_office.oxml.dml.main import CT_GeomGuideList as a_CT_GeomGuideList
    from ecma376_office.oxml.dml.main import CT_GeomRect as a_CT_GeomRect
    from ecma376_office.oxml.dml.main import CT_Path2DList as a_CT_Path2DList

namespace_drawml = 'http://www.ecma-international.org/flat/publications/standards/Ecma-376/drawingml/'


namespace_a = 'http://schemas.openxmlformats.org/drawingml/2006/main'

logger = logging.getLogger(__name__)

ns_map = {
    'drawml': namespace_drawml,  # 当前命名空间
    'a': namespace_a,
}


def qn(tag: str):
    """将 dc:creator 这种的标签,转换为 {http://purl.org/dc/elements/1.1/}creator 这样的形式"""

    global ns_map

    if ':' not in tag:
        return tag

    ns_prefix, ns = tag.split(':')

    return f'{{{ns_map[ns_prefix]}}}{ns}'


SubBaseElement = TypeVar('SubBaseElement', bound=OxmlBaseElement)


class CT_PresetShapeDefinitions(OxmlBaseElement):
    """根节点"""

    @property
    def preset_shapes(self) -> list[CT_PresetShape]:
        """预定义图形列表"""

        return self.findall(qn('drawml:presetShape'))  


class CT_PresetShape(OxmlBaseElement):
    """`drawml:PresetShape` element class.

    oxml.shapes.autoshape.CT_CustomGeometry2D

    参考: https://learn.microsoft.com/zh-cn/dotnet/api/documentformat.openxml.drawing.customgeometry?view=openxml-2.8.1
    """

    @property
    def name(self) -> str:
        """图形名称"""

        return AnyStrToStr(self.attrib['name'])  

    @property
    def av_lst(self) -> Optional[a_CT_GeomGuideList]:
        """形状调整值列表"""

        return self.find(qn('a:avLst'))  

    @property
    def gd_lst(self) -> Optional[a_CT_GeomGuideList]:
        """形状调整值列表"""

        return self.find(qn('a:gdLst')) 

    @property
    def ah_lst(self) -> Optional[a_CT_AdjustHandleList]:
        """形状调整手柄列表"""

        return self.find(qn('a:ahLst'))  

    @property
    def rect(self) -> Optional[a_CT_GeomRect]:
        """形状文本矩形"""

        return self.find(qn('a:rect'))  

    @property
    def path_lst(self) -> a_CT_Path2DList:
        """形状路径列表"""

        return self.find(qn('a:pathLst')) 


presetshape_namespace = lookup.get_namespace(namespace_drawml)
presetshape_namespace[None] = OxmlBaseElement

# 根节点
presetshape_namespace['presetShapeDefinitions'] = CT_PresetShapeDefinitions
presetshape_namespace['presetShape'] = CT_PresetShape
