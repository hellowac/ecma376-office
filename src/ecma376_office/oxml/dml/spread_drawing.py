"""
对应xsd: dml-spreadsheetDrawing.xsd

前缀: xdr

命名空间: http://purl.oclc.org/ooxml/drawingml/spreadsheetDrawing

<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"
  xmlns:a="http://purl.oclc.org/ooxml/drawingml/main"
  xmlns="http://purl.oclc.org/ooxml/drawingml/spreadsheetDrawing"
  xmlns:r="http://purl.oclc.org/ooxml/officeDocument/relationships"
  targetNamespace="http://purl.oclc.org/ooxml/drawingml/spreadsheetDrawing"
  elementFormDefault="qualified">
  <xsd:import namespace="http://purl.oclc.org/ooxml/drawingml/main" schemaLocation="dml-main.xsd"/>
  <xsd:import schemaLocation="shared-relationshipReference.xsd"
    namespace="http://purl.oclc.org/ooxml/officeDocument/relationships"/>

  ...

</xsd:schema>
"""

from __future__ import annotations

import logging
from typing import (
    AnyStr,
    NewType,
    Optional,
    TypeVar,
)

from ecma376_office.oxml.base import OxmlBaseElement, ST_BaseEnumType, lookup
from ecma376_office.oxml.dml.main import CT_BlipFillProperties as a_CT_BlipFillProperties
from ecma376_office.oxml.dml.main import CT_GraphicalObject as a_CT_GraphicalObject
from ecma376_office.oxml.dml.main import CT_GroupShapeProperties as a_CT_GroupShapeProperties
from ecma376_office.oxml.dml.main import CT_NonVisualConnectorProperties as a_CT_NonVisualConnectorProperties
from ecma376_office.oxml.dml.main import CT_NonVisualDrawingProps as a_CT_NonVisualDrawingProps
from ecma376_office.oxml.dml.main import CT_NonVisualDrawingShapeProps as a_CT_NonVisualDrawingShapeProps
from ecma376_office.oxml.dml.main import CT_NonVisualGraphicFrameProperties as a_CT_NonVisualGraphicFrameProperties
from ecma376_office.oxml.dml.main import CT_NonVisualGroupDrawingShapeProps as a_CT_NonVisualGroupDrawingShapeProps
from ecma376_office.oxml.dml.main import CT_NonVisualPictureProperties as a_CT_NonVisualPictureProperties
from ecma376_office.oxml.dml.main import CT_Point2D as a_CT_Point2D
from ecma376_office.oxml.dml.main import CT_PositiveSize2D as a_CT_PositiveSize2D
from ecma376_office.oxml.dml.main import CT_ShapeProperties as a_CT_ShapeProperties
from ecma376_office.oxml.dml.main import CT_ShapeStyle as a_CT_ShapeStyle
from ecma376_office.oxml.dml.main import CT_TextBody as a_CT_TextBody
from ecma376_office.oxml.dml.main import CT_Transform2D as a_CT_Transform2D
from ecma376_office.oxml.dml.main import ST_Coordinate as a_ST_Coordinate
from ecma376_office.oxml.dml.main import to_ST_Coordinate as a_to_ST_Coordinate
from ecma376_office.oxml.exceptions import OxmlAttributeValidateError
from ecma376_office.oxml.shared.relationship_reference import ST_RelationshipId as r_ST_RelationshipId
from ecma376_office.oxml.xsd_types import to_xsd_bool

namespace_xdr = 'http://purl.oclc.org/ooxml/drawingml/spreadsheetDrawing'

logger = logging.getLogger(__name__)

ns_map = {
    'xdr': 'http://purl.oclc.org/ooxml/drawingml/spreadsheetDrawing',  # 当前命名空间
    'a': 'http://purl.oclc.org/ooxml/drawingml/main',
    'r': 'http://purl.oclc.org/ooxml/officeDocument/relationships',
}


def qn(tag: str):
    """将 dc:creator 这种的标签,转换为 {http://purl.org/dc/elements/1.1/}creator 这样的形式"""

    global ns_map

    if ':' not in tag:
        return tag

    ns_prefix, ns = tag.split(':')

    return f'{{{ns_map[ns_prefix]}}}{ns}'


SubBaseElement = TypeVar('SubBaseElement', bound=OxmlBaseElement)


class CT_AnchorClientData(OxmlBaseElement):
    @property
    def f_locks_with_sheet(self) -> bool:
        _val = self.attrib.get('fLocksWithSheet', 'true')

        return to_xsd_bool(_val)

    @property
    def f_prints_with_sheet(self) -> bool:
        _val = self.attrib.get('fPrintsWithSheet', 'true')

        return to_xsd_bool(_val)


class CT_ShapeNonVisual(OxmlBaseElement):
    @property
    def c_nv_pr(self) -> a_CT_NonVisualDrawingProps:
        return getattr(self, qn('xdr:cNvPr'))

    @property
    def c_nv_sp_pr(self) -> a_CT_NonVisualDrawingShapeProps:
        return getattr(self, qn('xdr:cNvSpPr'))


class CT_Shape(OxmlBaseElement):
    @property
    def nv_sp_pr(self) -> CT_ShapeNonVisual:
        return getattr(self, qn('xdr:nvSpPr'))

    @property
    def sp_pr(self) -> a_CT_ShapeProperties:
        return getattr(self, qn('xdr:spPr'))

    @property
    def style(self) -> Optional[a_CT_ShapeStyle]:
        return getattr(self, qn('xdr:style'), None)

    @property
    def tx_body(self) -> Optional[a_CT_TextBody]:
        return getattr(self, qn('xdr:txBody'), None)

    @property
    def macro(self) -> Optional[str]:
        _val = self.attrib.get('macro', '')

        if _val is None:
            return None

        return str(_val)

    @property
    def textlink(self) -> Optional[str]:
        _val = self.attrib.get('textlink', '')

        if _val is None:
            return None

        return str(_val)

    @property
    def f_locks_text(self) -> bool:
        _val = self.attrib.get('fLocksText', 'true')

        return to_xsd_bool(_val)

    @property
    def f_published(self) -> bool:
        _val = self.attrib.get('fPublished', 'false')

        return to_xsd_bool(_val)


class CT_ConnectorNonVisual(OxmlBaseElement):
    @property
    def c_nv_pr(self) -> a_CT_NonVisualDrawingProps:
        return getattr(self, qn('xdr:cNvPr'))

    @property
    def c_nv_cxn_sp_pr(self) -> a_CT_NonVisualConnectorProperties:
        return getattr(self, qn('xdr:cNvCxnSpPr'))


class CT_Connector(OxmlBaseElement):
    @property
    def nv_cxn_sp_pr(self) -> CT_ConnectorNonVisual:
        return getattr(self, qn('xdr:nvCxnSpPr'))

    @property
    def sp_pr(self) -> a_CT_ShapeProperties:
        return getattr(self, qn('xdr:spPr'))

    @property
    def style(self) -> Optional[a_CT_ShapeStyle]:
        return getattr(self, qn('xdr:style'), None)

    @property
    def macro(self) -> Optional[str]:
        _val = self.attrib.get('macro', '')

        if _val is None:
            return None

        return str(_val)

    @property
    def f_published(self) -> bool:
        _val = self.attrib.get('fPublished', 'false')

        return to_xsd_bool(_val)


class CT_PictureNonVisual(OxmlBaseElement):
    @property
    def c_nv_pr(self) -> a_CT_NonVisualDrawingProps:
        return getattr(self, qn('xdr:cNvPr'))

    @property
    def c_nv_pic_pr(self) -> a_CT_NonVisualPictureProperties:
        return getattr(self, qn('xdr:cNvPicPr'))


class CT_Picture(OxmlBaseElement):
    @property
    def nv_pic_pic(self) -> CT_PictureNonVisual:
        return getattr(self, qn('xdr:nvPicPr'))

    @property
    def blip_fill(self) -> a_CT_BlipFillProperties:
        return getattr(self, qn('xdr:blipFill'))

    @property
    def sp_pr(self) -> a_CT_ShapeProperties:
        return getattr(self, qn('xdr:spPr'))

    @property
    def style(self) -> Optional[a_CT_ShapeStyle]:
        return getattr(self, qn('xdr:style'), None)

    @property
    def macro(self) -> Optional[str]:
        _val = self.attrib.get('macro', '')

        if _val is None:
            return None

        return str(_val)

    @property
    def f_published(self) -> bool:
        _val = self.attrib.get('fPublished', 'false')

        return to_xsd_bool(_val)


class CT_GraphicalObjectFrameNonVisual(OxmlBaseElement):
    @property
    def c_nv_pr(self) -> a_CT_NonVisualDrawingProps:
        return getattr(self, qn('xdr:cNvPr'))

    @property
    def c_nv_graphic_frame_pr(self) -> a_CT_NonVisualGraphicFrameProperties:
        return getattr(self, qn('xdr:cNvGraphicFramePr'))


class CT_GraphicalObjectFrame(OxmlBaseElement):
    @property
    def nv_graphic_frame_pr(self) -> CT_GraphicalObjectFrameNonVisual:
        return getattr(self, qn('xdr:nvGraphicFramePr'))

    @property
    def xfrm(self) -> a_CT_Transform2D:
        return getattr(self, qn('xdr:xfrm'))

    @property
    def graphic(self) -> a_CT_GraphicalObject:
        """<xsd:element ref="a:graphic" minOccurs="1" maxOccurs="1"/>"""

        return getattr(self, qn('a:graphic'))

    @property
    def macro(self) -> Optional[str]:
        _val = self.attrib.get('macro', '')

        if _val is None:
            return None

        return str(_val)

    @property
    def f_published(self) -> bool:
        _val = self.attrib.get('fPublished', 'false')

        return to_xsd_bool(_val)


class CT_GroupShapeNonVisual(OxmlBaseElement):
    @property
    def c_nv_pr(self) -> a_CT_NonVisualDrawingProps:
        return getattr(self, qn('xdr:cNvPr'))

    @property
    def c_nv_grp_sp_pr(self) -> a_CT_NonVisualGroupDrawingShapeProps:
        return getattr(self, qn('xdr:cNvGrpSpPr'))


class CT_GroupShape(OxmlBaseElement):
    @property
    def nv_grp_sp_pr(self) -> CT_GroupShapeNonVisual:
        return getattr(self, qn('xdr:nvGrpSpPr'))

    @property
    def grp_sp_pr(self) -> a_CT_GroupShapeProperties:
        return getattr(self, qn('xdr:grpSpPr'))

    @property
    def shapes(
        self,
    ) -> list[CT_Shape | CT_GroupShape | CT_GraphicalObjectFrame | CT_Connector | CT_Picture]:
        tags = (
            qn('xdr:sp'),  # CT_Shape
            qn('xdr:grpSp'),  # CT_GroupShape
            qn('xdr:graphicFrame'),  # CT_GraphicalObjectFrame
            qn('xdr:cxnSp'),  # CT_Connector
            qn('xdr:pic'),  # CT_Picture
        )

        return self.choice_and_more(*tags)  # type: ignore


class EG_ObjectChoices(OxmlBaseElement):
    tags = (
        qn('xdr:sp'),  # CT_Shape
        qn('xdr:grpSp'),  # CT_GroupShape
        qn('xdr:graphicFrame'),  # CT_GraphicalObjectFrame
        qn('xdr:cxnSp'),  # CT_Connector
        qn('xdr:pic'),  # CT_Picture
        qn('xdr:contentPart'),  # CT_Rel
    )


class CT_Rel(OxmlBaseElement):
    @property
    def r_id(self) -> r_ST_RelationshipId:
        _val = self.attrib[qn('r:id')]

        return r_ST_RelationshipId(_val)  # type: ignore


ST_ColID = NewType('ST_ColID', int)


def to_ST_ColID(val: AnyStr):
    intval = int(val)

    if intval < 0:
        msg = f'预期外的值: {intval}'
        raise OxmlAttributeValidateError(msg)


ST_RowID = NewType('ST_RowID', int)

to_ST_RowID = to_ST_ColID


class CT_Marker(OxmlBaseElement):
    @property
    def col(self) -> ST_ColID:
        val = getattr(self, qn('xdr:col')).text

        return to_ST_ColID(val)  # type: ignore

    @property
    def col_off(self) -> a_ST_Coordinate:
        val = getattr(self, qn('xdr:colOff')).text

        return a_to_ST_Coordinate(val)  # type: ignore

    @property
    def row(self) -> ST_RowID:
        val = getattr(self, qn('xdr:row')).text

        return to_ST_RowID(val)  # type: ignore

    @property
    def row_off(self) -> a_ST_Coordinate:
        val = getattr(self, qn('xdr:rowOff')).text

        return a_to_ST_Coordinate(val)  # type: ignore


class ST_EditAs(ST_BaseEnumType):
    TwoCell = 'twoCell'
    OneCell = 'oneCell'
    Absolute = 'absolute'


class CT_TwoCellAnchor(EG_ObjectChoices):
    @property
    def from_(self) -> CT_Marker:
        return getattr(self, qn('xdr:from'))

    @property
    def to(self) -> CT_Marker:
        return getattr(self, qn('xdr:to'))

    @property
    def shape(
        self,
    ) -> list[
        CT_Shape | CT_GroupShape | CT_GraphicalObjectFrame | CT_Connector | CT_Picture | CT_Rel
    ]:
        return self.choice_and_more(*self.tags)  # type: ignore

    @property
    def client_data(self) -> CT_AnchorClientData:
        return getattr(self, qn('xdr:clientData'))

    @property
    def edit_as(self) -> ST_EditAs:
        _val = self.attrib.get('editAs', 'twoCell')

        return ST_EditAs(_val)


class CT_OneCellAnchor(OxmlBaseElement):
    @property
    def from_(self) -> CT_Marker:
        return getattr(self, qn('xdr:from'))

    @property
    def to(self) -> CT_Marker:
        return getattr(self, qn('xdr:to'))

    @property
    def shape(
        self,
    ) -> list[
        CT_Shape | CT_GroupShape | CT_GraphicalObjectFrame | CT_Connector | CT_Picture | CT_Rel
    ]:
        return self.choice_and_more(*self.tags)  # type: ignore

    @property
    def client_data(self) -> CT_AnchorClientData:
        return getattr(self, qn('xdr:clientData'))


class CT_AbsoluteAnchor(OxmlBaseElement):
    @property
    def pos(self) -> a_CT_Point2D:
        return getattr(self, qn('xdr:pos'))

    @property
    def ext(self) -> a_CT_PositiveSize2D:
        return getattr(self, qn('xdr:ext'))

    @property
    def shape(
        self,
    ) -> list[
        CT_Shape | CT_GroupShape | CT_GraphicalObjectFrame | CT_Connector | CT_Picture | CT_Rel
    ]:
        return self.choice_and_more(*self.tags)  # type: ignore

    @property
    def client_data(self) -> CT_AnchorClientData:
        return getattr(self, qn('xdr:clientData'))


class EG_Anchor(OxmlBaseElement):
    tags = (
        qn('xdr:twoCellAnchor'),  # CT_TwoCellAnchor
        qn('xdr:oneCellAnchor'),  # CT_OneCellAnchor
        qn('xdr:absoluteAnchor'),  # CT_AbsoluteAnchor
    )

    @property
    def two_cell_anchor(self) -> CT_TwoCellAnchor:
        return getattr(self, qn('xdr:twoCellAnchor'))

    @property
    def one_cell_anchor(self) -> CT_OneCellAnchor:
        return getattr(self, qn('xdr:oneCellAnchor'))

    @property
    def absolute_anchor(self) -> CT_AbsoluteAnchor:
        return getattr(self, qn('xdr:absoluteAnchor'))


class CT_Drawing(EG_Anchor):
    @property
    def anchor(
        self,
    ) -> list[CT_TwoCellAnchor | CT_OneCellAnchor | CT_AbsoluteAnchor]:
        return self.choice_and_more(*self.tags)  # type: ignore


dml_xdr_namespace = lookup.get_namespace(namespace_xdr)
dml_xdr_namespace[None] = OxmlBaseElement


dml_xdr_namespace['wsDr'] = CT_Drawing  # 根节点之一
# dml_main_namespace["userShapes"] = cdr_CT_Drawing  # 根节点之一

dml_xdr_namespace['from'] = CT_Marker
dml_xdr_namespace['to'] = CT_Marker

dml_xdr_namespace['cNvPr'] = a_CT_NonVisualDrawingProps
dml_xdr_namespace['cNvSpPr'] = a_CT_NonVisualDrawingShapeProps
dml_xdr_namespace['cNvCxnSpPr'] = a_CT_NonVisualConnectorProperties
dml_xdr_namespace['cNvPicPr'] = a_CT_NonVisualPictureProperties
dml_xdr_namespace['cNvGraphicFramePr'] = a_CT_NonVisualGraphicFrameProperties
dml_xdr_namespace['cNvGrpSpPr'] = a_CT_NonVisualGroupDrawingShapeProps

dml_xdr_namespace['nvSpPr'] = CT_ShapeNonVisual
dml_xdr_namespace['nvPicPr'] = CT_PictureNonVisual
dml_xdr_namespace['nvGraphicFramePr'] = CT_GraphicalObjectFrameNonVisual
dml_xdr_namespace['nvGrpSpPr'] = CT_GroupShapeNonVisual

dml_xdr_namespace['sp'] = CT_Shape
dml_xdr_namespace['grpSp'] = CT_GroupShape
dml_xdr_namespace['graphicFrame'] = CT_GraphicalObjectFrame
dml_xdr_namespace['cxnSp'] = CT_Connector
dml_xdr_namespace['pic'] = CT_Picture
dml_xdr_namespace['contentPart'] = CT_Rel

dml_xdr_namespace['spPr'] = a_CT_ShapeProperties
dml_xdr_namespace['grpSpPr'] = a_CT_GroupShapeProperties

dml_xdr_namespace['style'] = a_CT_ShapeStyle
dml_xdr_namespace['txBody'] = a_CT_TextBody

dml_xdr_namespace['blipFill'] = a_CT_BlipFillProperties
dml_xdr_namespace['xfrm'] = a_CT_Transform2D


dml_xdr_namespace['col'] = ST_ColID
dml_xdr_namespace['colOff'] = a_ST_Coordinate
dml_xdr_namespace['row'] = ST_RowID
dml_xdr_namespace['rowOff'] = a_ST_Coordinate
dml_xdr_namespace['clientData'] = CT_AnchorClientData

dml_xdr_namespace['ext'] = a_CT_PositiveSize2D

dml_xdr_namespace['pos'] = a_CT_Point2D
dml_xdr_namespace['twoCellAnchor'] = CT_TwoCellAnchor
dml_xdr_namespace['oneCellAnchor'] = CT_OneCellAnchor
dml_xdr_namespace['absoluteAnchor'] = CT_AbsoluteAnchor

# 公共元素:
