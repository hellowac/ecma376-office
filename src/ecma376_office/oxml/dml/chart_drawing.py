"""
对应xsd: dml-chartdrawing.xsd

前缀: cp

命名空间: http://purl.oclc.org/ooxml/drawingml/chartDrawing

<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"
  xmlns:a="http://purl.oclc.org/ooxml/drawingml/main"
  xmlns="http://purl.oclc.org/ooxml/drawingml/chartDrawing"
  targetNamespace="http://purl.oclc.org/ooxml/drawingml/chartDrawing"
  elementFormDefault="qualified">
  <xsd:import namespace="http://purl.oclc.org/ooxml/drawingml/main" schemaLocation="dml-main.xsd"/>

  ...

</xsd:schema>
"""

from __future__ import annotations

import logging
from typing import (
    Any,
    NewType,
    TypeVar,
)

from ecma376_office.oxml import utils
from ecma376_office.oxml.base import OxmlBaseElement, lookup
from ecma376_office.oxml.dml.main import CT_BlipFillProperties as a_CT_BlipFillProperties
from ecma376_office.oxml.dml.main import CT_GraphicalObject as a_CT_GraphicalObject
from ecma376_office.oxml.dml.main import CT_GroupShapeProperties as a_CT_GroupShapeProperties
from ecma376_office.oxml.dml.main import CT_NonVisualConnectorProperties as a_CT_NonVisualConnectorProperties
from ecma376_office.oxml.dml.main import CT_NonVisualDrawingProps as a_CT_NonVisualDrawingProps
from ecma376_office.oxml.dml.main import CT_NonVisualDrawingShapeProps as a_CT_NonVisualDrawingShapeProps
from ecma376_office.oxml.dml.main import CT_NonVisualGraphicFrameProperties as a_CT_NonVisualGraphicFrameProperties
from ecma376_office.oxml.dml.main import CT_NonVisualGroupDrawingShapeProps as a_CT_NonVisualGroupDrawingShapeProps
from ecma376_office.oxml.dml.main import CT_NonVisualPictureProperties as a_CT_NonVisualPictureProperties
from ecma376_office.oxml.dml.main import CT_PositiveSize2D as a_CT_PositiveSize2D
from ecma376_office.oxml.dml.main import CT_ShapeProperties as a_CT_ShapeProperties
from ecma376_office.oxml.dml.main import CT_ShapeStyle as a_CT_ShapeStyle
from ecma376_office.oxml.dml.main import CT_TextBody as a_CT_TextBody
from ecma376_office.oxml.dml.main import CT_Transform2D as a_CT_Transform2D
from ecma376_office.oxml.xsd_types import to_xsd_bool

# namespace_cp = "http://purl.oclc.org/ooxml/drawingml/chartDrawing"
namespace_cdr = 'http://schemas.openxmlformats.org/drawingml/2006/chartDrawing'

# namespace_a = "http://purl.oclc.org/ooxml/drawingml/main"
namespace_a = 'http://schemas.openxmlformats.org/drawingml/2006/main'

# namespace_r = "http://purl.oclc.org/ooxml/officeDocument/relationships"
namespace_r = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

# namespace_s = "http://purl.oclc.org/ooxml/officeDocument/sharedTypes"
namespace_s = 'http://schemas.openxmlformats.org/officeDocument/2006/sharedTypes'

logger = logging.getLogger(__name__)

ns_map = {
    'cdr': namespace_cdr,  # 当前命名空间
    'a': namespace_a,
    'r': namespace_r,
    's': namespace_s,
}


def qn(tag: str):
    """将 dc:creator 这种的标签,转换为 {http://purl.org/dc/elements/1.1/}creator 这样的形式"""

    global ns_map

    if ':' not in tag:
        return tag

    ns_prefix, ns = tag.split(':')

    return f'{{{ns_map[ns_prefix]}}}{ns}'


SubBaseElement = TypeVar('SubBaseElement', bound=OxmlBaseElement)


class CT_ShapeNonVisual(OxmlBaseElement):
    """21.3.2.19 nvSpPr (非视觉形状属性)

    该元素指定了形状的所有非可视属性。该元素是非可视标识属性、形状属性和与形状相关联的应用程序属性的容器。这样可以存储不影响形状外观的附加信息。
    """

    @property
    def c_nv_pr(self) -> a_CT_NonVisualDrawingProps:
        return getattr(self, qn('cdr:cNvPr'))

    @property
    def c_nv_sp_pr(self) -> a_CT_NonVisualDrawingShapeProps:
        return getattr(self, qn('cdr:cNvSpPr'))


class CT_Shape(OxmlBaseElement):
    """21.3.2.22 sp (形状)

    该元素指定了一个形状的存在。一个形状可以是预设的，也可以是使用DrawingML框架定义的自定义几何图形。除了几何图形之外，每个形状还可以附加可视和非可视属性。文本和相应的样式信息也可以附加到形状上。该形状与其他形状一起在形状树或组形状元素中指定。
    """

    @property
    def nv_sp_pr(self) -> CT_ShapeNonVisual:
        return getattr(self, qn('cdr:nvSpPr'))

    @property
    def sp_pr(self) -> a_CT_ShapeProperties:
        return getattr(self, qn('cdr:spPr'))

    @property
    def style(self) -> a_CT_ShapeStyle:
        return getattr(self, qn('cdr:style'))

    @property
    def tx_body(self) -> a_CT_TextBody:
        return getattr(self, qn('cdr:txBody'))

    @property
    def macro(self) -> str:
        """参考自定义函数 / Reference to Custom Function

        该元素指定与图表关联的自定义函数。 [Example: 宏脚本、插件功能等等。 end example]

        该字符串的格式应由应用程序定义，如果不理解应该忽略。
        """
        _val = self.attrib.get('macro', '')

        return utils.AnyStrToStr(_val)  # type: ignore

    @property
    def textlink(self) -> str:
        """文本链接 / Text Link

        指定此形状中包含的文本是否与电子表格中的单元格链接。也就是说，形状中的文本具有引用的电子表格单元格中定义的值。
        """
        _val = self.attrib.get('textlink', '')

        return utils.AnyStrToStr(_val)  # type: ignore

    @property
    def f_locks_text(self) -> bool:
        """锁定文本 / Lock Text

        指定是否允许在电子表格上保护的工作表中编辑此形状内的文本。这允许在电子表格文档中基于每个形状指定锁定或“保护(protected)”的文本。如果未指定此属性，则假定为0或false。
        """
        _val = self.attrib.get('fLocksText', 'true')

        return to_xsd_bool(_val)  # type: ignore

    @property
    def f_published(self) -> str:
        """发布到服务器 / Publish to Server

        指定形状在将工作表发送到电子表格服务器时是否应发布。这适用于与文档服务器进行接口时使用。
        """
        _val = self.attrib.get('fPublished', 'false')

        return utils.AnyStrToStr(_val)  # type: ignore


class CT_ConnectorNonVisual(OxmlBaseElement):
    """21.3.2.15 nvCxnSpPr (连接器非视觉属性)

    该元素指定了连接形状的所有非可视属性。该元素是非可视标识属性、形状属性和应用属性的容器，这些属性与连接形状相关联。这样可以存储不影响连接形状外观的附加信息。
    """

    @property
    def c_nv_pr(self) -> a_CT_NonVisualDrawingProps:
        return getattr(self, qn('cdr:cNvPr'))

    @property
    def c_nv_cxn_sp_pr(self) -> a_CT_NonVisualConnectorProperties:
        return getattr(self, qn('cdr:cNvCxnSpPr'))


class CT_Connector(OxmlBaseElement):
    """21.3.2.9 cxnSp (连接形状)

    该元素指定了用于连接两个sp元素的连接形状。一旦使用cxnSp指定了连接，生成应用程序将决定连接器的确切路径。也就是说，连接器的路由算法由生成应用程序决定，因为所需路径可能因应用程序的具体需求而不同。
    """

    @property
    def nv_cxn_sp_pr(self) -> CT_ConnectorNonVisual:
        return getattr(self, qn('cdr:nvCxnSpPr'))

    @property
    def sp_pr(self) -> a_CT_ShapeProperties:
        return getattr(self, qn('cdr:spPr'))

    @property
    def style(self) -> a_CT_ShapeStyle:
        return getattr(self, qn('cdr:style'))

    @property
    def macro(self) -> str:
        """Reference to Custom Function

        该元素指定与图表关联的自定义函数。 [Example: 宏脚本、插件功能等等。 end example]
        """
        _val = self.attrib.get('macro', '')

        return utils.AnyStrToStr(_val)  # type: ignore

    @property
    def f_published(self) -> str:
        """Publish to Server

        指定形状是否在将工作表发送到电子表格服务器时一同发布。这适用于与文档服务器进行接口时使用。
        """
        _val = self.attrib.get('fPublished', 'false')

        return utils.AnyStrToStr(_val)  # type: ignore


class CT_PictureNonVisual(OxmlBaseElement):
    """21.3.2.18 nvPicPr (非视觉图片属性)

    该元素指定图片的非可视属性。这允许存储与图片外观无关的附加信息。
    """

    @property
    def c_nv_pr(self) -> a_CT_NonVisualDrawingProps:
        return getattr(self, qn('cdr:cNvPr'))

    @property
    def c_nv_pic_pr(self) -> a_CT_NonVisualPictureProperties:
        return getattr(self, qn('cdr:cNvPicPr'))


class CT_Picture(OxmlBaseElement):
    """21.3.2.20 pic (图片)

    该元素指定文档中图片对象的存在。
    """

    @property
    def nv_pic_pr(self) -> CT_PictureNonVisual:
        return getattr(self, qn('cdr:nvPicPr'))

    @property
    def blip_fill(self) -> a_CT_BlipFillProperties:
        return getattr(self, qn('cdr:blipFill'))

    @property
    def sp_pr(self) -> a_CT_ShapeProperties:
        return getattr(self, qn('cdr:spPr'))

    @property
    def style(self) -> a_CT_ShapeStyle:
        return getattr(self, qn('cdr:style'))

    @property
    def macro(self) -> str:
        """Reference to Custom Function

        该元素指定与图表关联的自定义函数。 [Example: 宏脚本、插件功能等等。 end example]
        """
        _val = self.attrib.get('macro', '')

        return utils.AnyStrToStr(_val)  # type: ignore

    @property
    def f_published(self) -> str:
        """Publish to Server

        指定形状在将工作表发送到电子表格服务器时是否应发布。这适用于与文档服务器进行接口时使用。
        """
        _val = self.attrib.get('fPublished', 'false')

        return utils.AnyStrToStr(_val)  # type: ignore


class CT_GraphicFrameNonVisual(OxmlBaseElement):
    """21.3.2.16 nvGraphicFramePr (非可视图形框架属性)

    该元素指定了图形框架的所有非可视属性。该元素是非可视标识属性、形状属性和应用属性的容器，这些属性与图形框架相关联。这样可以存储不影响图形框架外观的附加信息。
    """

    @property
    def c_nv_pr(self) -> a_CT_NonVisualDrawingProps:
        return getattr(self, qn('cdr:cNvPr'))

    @property
    def c_nv_graphic_frame_pr(self) -> a_CT_NonVisualGraphicFrameProperties:
        return getattr(self, qn('cdr:cNvGraphicFramePr'))


class CT_GraphicFrame(OxmlBaseElement):
    """21.3.2.12 graphicFrame (图框)

    该元素指定了一个图形框架的存在。该框架包含了由外部来源生成的图形，并需要一个容器来在幻灯片表面上显示。
    """

    @property
    def nv_graphic_frame_pr(self) -> CT_GraphicFrameNonVisual:
        return getattr(self, qn('cdr:nvGraphicFramePr'))

    @property
    def xfrm(self) -> a_CT_Transform2D:
        return getattr(self, qn('cdr:xfrm'))

    def graphic(self) -> a_CT_GraphicalObject:
        """<xsd:element ref="a:graphic" minOccurs="1" maxOccurs="1"/>"""
        return getattr(self, qn('a:graphic'))

    @property
    def macro(self) -> str:
        """参考自定义函数 / Reference to Custom Function

        该元素指定与图表关联的自定义函数。 [Example: A macro script, add-in function, and so on. end example]
        """
        _val = self.attrib.get('macro', '')

        return utils.AnyStrToStr(_val)  # type: ignore

    @property
    def f_published(self) -> str:
        """发布到服务器 / Publish To Server

        指定形状是否在将工作表发送到电子表格服务器时一同发布。这适用于与文档服务器进行接口时使用。
        """
        _val = self.attrib.get('fPublished', 'false')

        return utils.AnyStrToStr(_val)  # type: ignore


class CT_GroupShapeNonVisual(OxmlBaseElement):
    """21.3.2.17 nvGrpSpPr (非视觉组合形状属性)

    该元素指定了组合形状的所有非可视属性。该元素是非可视标识属性、形状属性和应用属性的容器，这些属性与组合形状相关联。这样可以存储不影响组合形状外观的附加信息。
    """

    @property
    def c_nv_pr(self) -> a_CT_NonVisualDrawingProps:
        return getattr(self, qn('cdr:cNvPr'))

    @property
    def c_nv_grp_sp_pr(self) -> a_CT_NonVisualGroupDrawingShapeProps:
        return getattr(self, qn('cdr:cNvGrpSpPr'))


class CT_GroupShape(OxmlBaseElement):
    """21.3.2.13 grpSp (组合形状)

    该元素指定了一个表示多个形状组合在一起的组合形状。这个形状应该被视为一个普通形状，但不同于由单个几何描述的形状，它由包含在其中的所有形状几何组成。在组合形状中，组成组合的每个形状都像通常一样被指定。然而，组合元素的理念是可以同时应用于多个形状的单个变换。
    """

    @property
    def nv_grp_sp_pr(self) -> CT_GroupShapeNonVisual:
        return getattr(self, qn('cdr:nvGrpSpPr'))

    @property
    def grp_sp_pr(self) -> a_CT_GroupShapeProperties:
        return getattr(self, qn('cdr:grpSpPr'))

    @property
    def shape(
        self,
    ) -> list[CT_Shape | CT_GroupShape | CT_GraphicFrame | CT_Connector | CT_Picture]:
        tags = (
            qn('c:sp'),  # CT_Shape
            qn('c:grpSp'),  # CT_GroupShape
            qn('c:graphicFrame'),  # CT_GraphicFrame
            qn('c:cxnSp'),  # CT_Connector
            qn('c:pic'),  # CT_Picture
        )

        return self.choice_and_more(*tags)  # type: ignore


class EG_ObjectChoices(OxmlBaseElement):
    @property
    def shape(
        self,
    ) -> CT_Shape | CT_GroupShape | CT_GraphicFrame | CT_Connector | CT_Picture:
        tags = (
            qn('c:sp'),  # CT_Shape
            qn('c:grpSp'),  # CT_GroupShape
            qn('c:graphicFrame'),  # CT_GraphicFrame
            qn('c:cxnSp'),  # CT_Connector
            qn('c:pic'),  # CT_Picture
        )

        return self.choice_one_child(*tags)  # type: ignore


ST_MarkerCoordinate = NewType('ST_MarkerCoordinate', float)


def to_ST_MarkerCoordinate(val: Any):
    _val = utils.AnyStrToStr(val)

    return ST_MarkerCoordinate(float(_val))


class CT_Marker(OxmlBaseElement):
    """21.3.2.25 to (结束锚点)

    该元素指定了绘图元素的第二个锚点。它用于将形状的底部和右侧锚定在电子表格中。也就是说，当相应的图表被调整时，形状也会被调整。
    """

    @property
    def x(self) -> ST_MarkerCoordinate:
        return getattr(self, qn('cdr:x'))

    @property
    def y(self) -> ST_MarkerCoordinate:
        return getattr(self, qn('cdr:y'))


class CT_RelSizeAnchor(EG_ObjectChoices):
    """21.3.2.21 relSizeAnchor (相对锚定形状尺寸)

    该元素指定了在图表中描述的形状应该基于相对锚点进行大小调整。这是通过两个元素实现的。from元素指定了形状边界框的左上角在RTL（从右到左）实现中的位置。然后，to元素指定了形状边界框的右下角在RTL（从右到左）实现中的位置，从而确定了形状的大小。
    """

    @property
    def source(self) -> CT_Marker:
        """from"""

        return getattr(self, qn('cdr:from'))

    @property
    def to(self) -> CT_Marker:
        return getattr(self, qn('cdr:to'))


class CT_AbsSizeAnchor(EG_ObjectChoices):
    """21.3.2.1 absSizeAnchor (绝对锚形状尺寸)

    该元素指定了在图表中描述的形状应该基于相对锚点进行调整大小。这是通过两个元素实现的。from元素指定了形状边界框的左上角在RTL（从右到左）实现中的位置。然后，ext元素指定了形状边界框的右下角在RTL（从右到左）实现中的位置，从而确定了形状的大小。
    """

    @property
    def source(self) -> CT_Marker:
        """from"""

        return getattr(self, qn('cdr:from'))

    @property
    def ext(self) -> a_CT_PositiveSize2D:
        return getattr(self, qn('cdr:ext'))


class EG_Anchor(OxmlBaseElement):
    """
    <xsd:group name="EG_Anchor">
        <xsd:choice>
            <xsd:element name="relSizeAnchor" type="CT_RelSizeAnchor"/>
            <xsd:element name="absSizeAnchor" type="CT_AbsSizeAnchor"/>
        </xsd:choice>
    </xsd:group>
    """

    tags = (
        qn('cdr:relSizeAnchor'),  # CT_RelSizeAnchor
        qn('cdr:absSizeAnchor'),  # CT_AbsSizeAnchor
    )


class CT_Drawing(OxmlBaseElement):
    @property
    def anchor(self) -> list[CT_RelSizeAnchor | CT_AbsSizeAnchor]:
        return self.choice_and_more(*EG_Anchor.tags)  # type: ignore


dml_chart_drawing_namespace = lookup.get_namespace(namespace_cdr)
dml_chart_drawing_namespace[None] = OxmlBaseElement


dml_chart_drawing_namespace['chartSpace'] = CT_ShapeNonVisual

dml_chart_drawing_namespace['cNvPr'] = a_CT_NonVisualDrawingProps
dml_chart_drawing_namespace['cNvSpPr'] = a_CT_NonVisualDrawingShapeProps
dml_chart_drawing_namespace['cNvCxnSpPr'] = a_CT_NonVisualConnectorProperties
dml_chart_drawing_namespace['cNvPicPr'] = a_CT_NonVisualPictureProperties
dml_chart_drawing_namespace['cNvGraphicFramePr'] = a_CT_NonVisualGraphicFrameProperties
dml_chart_drawing_namespace['cNvGrpSpPr'] = a_CT_NonVisualGroupDrawingShapeProps


dml_chart_drawing_namespace['nvSpPr'] = CT_ShapeNonVisual
dml_chart_drawing_namespace['nvPicPr'] = CT_PictureNonVisual
dml_chart_drawing_namespace['nvGraphicFramePr'] = CT_GraphicFrameNonVisual

dml_chart_drawing_namespace['sp'] = CT_Shape
dml_chart_drawing_namespace['grpSp'] = CT_GroupShape
dml_chart_drawing_namespace['graphicFrame'] = CT_GraphicFrame
dml_chart_drawing_namespace['cxnSp'] = CT_Connector
dml_chart_drawing_namespace['pic'] = CT_Picture
dml_chart_drawing_namespace['spPr'] = a_CT_ShapeProperties
dml_chart_drawing_namespace['grpSpPr'] = a_CT_GroupShapeProperties
dml_chart_drawing_namespace['xfrm'] = a_CT_Transform2D

dml_chart_drawing_namespace['style'] = a_CT_ShapeStyle
dml_chart_drawing_namespace['txBody'] = a_CT_TextBody

dml_chart_drawing_namespace['nvCxnSpPr'] = CT_ConnectorNonVisual

dml_chart_drawing_namespace['blipFill'] = a_CT_BlipFillProperties


# dml_chart_drawing_namespace["x"] = ST_MarkerCoordinate
# dml_chart_drawing_namespace["y"] = ST_MarkerCoordinate

dml_chart_drawing_namespace['from'] = CT_Marker
dml_chart_drawing_namespace['to'] = CT_Marker
dml_chart_drawing_namespace['ext'] = a_CT_PositiveSize2D

dml_chart_drawing_namespace['relSizeAnchor'] = CT_RelSizeAnchor
dml_chart_drawing_namespace['absSizeAnchor'] = CT_AbsSizeAnchor

dml_chart_drawing_namespace['aaaa'] = CT_Drawing  # 根节点之一


# 公共元素:
