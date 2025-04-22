"""
对应xsd: dml-diagram.xsd

前缀: cp

命名空间: http://purl.oclc.org/ooxml/drawingml/chartDrawing

<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns="http://purl.oclc.org/ooxml/drawingml/diagram"
    xmlns:a="http://purl.oclc.org/ooxml/drawingml/main"
    xmlns:r="http://purl.oclc.org/ooxml/officeDocument/relationships"
    xmlns:s="http://purl.oclc.org/ooxml/officeDocument/sharedTypes"
    targetNamespace="http://purl.oclc.org/ooxml/drawingml/diagram"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified">

    <xsd:import namespace="http://purl.oclc.org/ooxml/officeDocument/relationships"
        schemaLocation="shared-relationshipReference.xsd"/>
    <xsd:import namespace="http://purl.oclc.org/ooxml/drawingml/main" schemaLocation="dml-main.xsd"/>
    <xsd:import namespace="http://purl.oclc.org/ooxml/officeDocument/sharedTypes"
        schemaLocation="shared-commonSimpleTypes.xsd"/>

    ...

</xsd:schema>
"""

from __future__ import annotations

import logging
from typing import (
    Any,
    AnyStr,
    NewType,
    Optional,
    TypeVar,
    Union,
)

from ecma376_office.oxml import utils
from ecma376_office.oxml.base import OxmlBaseElement, ST_BaseEnumType, lookup
from ecma376_office.oxml.dml.main import CT_BackgroundFormatting as a_CT_BackgroundFormatting
from ecma376_office.oxml.dml.main import CT_FlatText as a_CT_FlatText
from ecma376_office.oxml.dml.main import CT_HslColor as a_CT_HslColor
from ecma376_office.oxml.dml.main import CT_OfficeArtExtensionList as a_CT_OfficeArtExtensionList
from ecma376_office.oxml.dml.main import CT_PresetColor as a_CT_PresetColor
from ecma376_office.oxml.dml.main import CT_Scene3D as a_CT_Scene3D
from ecma376_office.oxml.dml.main import CT_SchemeColor as a_CT_SchemeColor
from ecma376_office.oxml.dml.main import CT_ScRgbColor as a_CT_ScRgbColor
from ecma376_office.oxml.dml.main import CT_Shape3D as a_CT_Shape3D
from ecma376_office.oxml.dml.main import CT_ShapeProperties as a_CT_ShapeProperties
from ecma376_office.oxml.dml.main import CT_ShapeStyle as a_CT_ShapeStyle
from ecma376_office.oxml.dml.main import CT_SRgbColor as a_CT_SRgbColor
from ecma376_office.oxml.dml.main import CT_SystemColor as a_CT_SystemColor
from ecma376_office.oxml.dml.main import CT_TextBody as a_CT_TextBody
from ecma376_office.oxml.dml.main import CT_WholeE2oFormatting as a_CT_WholeE2oFormatting
from ecma376_office.oxml.dml.main import EG_ColorChoice as a_EG_ColorChoice
from ecma376_office.oxml.dml.main import EG_Text3D as a_EG_Text3D
from ecma376_office.oxml.dml.main import ST_ShapeType as a_ST_ShapeType
from ecma376_office.oxml.exceptions import OxmlAttributeValidateError
from ecma376_office.oxml.shared.common_simple_types import ST_Guid as s_ST_Guid
from ecma376_office.oxml.shared.common_simple_types import ST_Percentage as s_ST_Percentage
from ecma376_office.oxml.shared.common_simple_types import to_ST_Percentage as s_to_ST_Percentage
from ecma376_office.oxml.shared.relationship_reference import ST_RelationshipId as r_ST_RelationshipId
from ecma376_office.oxml.xsd_types import XSD_AnyURI, to_xsd_bool, to_xsd_unsigned_int

# namespace_cp = "http://purl.oclc.org/ooxml/drawingml/diagram"
namespace_dgm = 'http://schemas.openxmlformats.org/drawingml/2006/diagram'

namespace_a = 'http://schemas.openxmlformats.org/drawingml/2006/main'

namespace_r = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

namespace_s = 'http://schemas.openxmlformats.org/officeDocument/2006/sharedTypes'

logger = logging.getLogger(__name__)

ns_map = {
    'dgm': namespace_dgm,  # 当前命名空间
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


class CT_CTName(OxmlBaseElement):
    """21.4.4.11 title (标题)

    颜色定义标题的名称或标题.
    """

    @property
    def lang(self):
        """Language

        颜色变换定义的标题或描述的自然语言.

        此属性的可能值由 W3C XML 架构字符串数据类型定义。
        """
        _val = self.attrib.get('lang', '')

        return utils.AnyStrToStr(_val)  # type: ignore

    @property
    def val(self):
        """Description Value

        用于描述颜色变换定义的字符串。
        """
        _val = self.attrib['val']

        return utils.AnyStrToStr(_val)  # type: ignore


class CT_CTDescription(OxmlBaseElement):
    """21.4.4.6 desc (描述)

    该元素包含颜色定义的描述。 该描述可用于描述与特定颜色变换定义相关联的质量。
    """

    @property
    def lang(self):
        """语言 / Language

        颜色变换定义的自然语言。
        """
        _val = self.attrib.get('lang', '')

        return utils.AnyStrToStr(_val)  # type: ignore

    @property
    def val(self):
        """描述 值 / Description Value

        用作颜色变换定义描述的字符串。
        """
        _val = self.attrib['val']

        return utils.AnyStrToStr(_val)  # type: ignore


class CT_CTCategory(OxmlBaseElement):
    """21.4.4.1 cat (颜色变换类别)

    该元素指定用户界面中要显示颜色变换的类别。
    """

    @property
    def type(self):
        """类别类型 / Category Type

        用于组织用户界面中颜色变换的类别类型。
        """
        _val = self.attrib['type']

        return XSD_AnyURI(utils.AnyStrToStr(_val))  # type: ignore

    @property
    def pri(self):
        """优先级 / Priority

        此颜色变化的类别内的优先级决定了它在用户界面中的显示顺序。 较低的数字将显示在列表的开头。
        """
        _val = self.attrib['pri']

        return to_xsd_unsigned_int(_val)  # type: ignore


class CT_CTCategories(OxmlBaseElement):
    """21.4.4.2 catLst (颜色变换类别列表)

    该元素定义颜色变换类别的列表。 该列表可用于填充用户界面组件，这些组件可以将颜色转换分成类别。
    """

    @property
    def cat(self) -> list[CT_CTCategory]:
        """21.4.4.1 cat (颜色变换类别)

        该元素指定用户界面中要显示颜色变换的类别。
        """

        return self.findall(qn('dgm:cat'))  # type: ignore


class ST_ClrAppMethod(ST_BaseEnumType):
    """21.4.7.16 ST_ClrAppMethod (色彩应用方法类型)

    这种简单的类型定义了将给定颜色集应用于图表中的一组节点或项目的方式。
    """

    Span = 'span'
    """跨度 / Span

    如果 A 和 B 是存在的颜色，则颜色会在整个图表中从 A 插值到 B。
    """

    Cycle = 'cycle'
    """循环 / Cycle

    如果 A 和 B 是存在的颜色，则颜色适用于从 A 到 B 到 A 的颜色。
    """

    Repeat = 'Repeat'
    """重复 / Repeat

    如果 A 到 B 是存在的颜色，则颜色适用于从 A 到 B 到 A 到 B 的颜色。
    """


class ST_HueDir(ST_BaseEnumType):
    """色相方向

    21.4.7.38 ST_HueDir

    当给定两种颜色进行插值时，可以沿着色轮的两个方向之一来执行插值。 这个简单的类型定义了那个方向。
    """

    Cw = 'cw'
    """顺时针色调方向 / Clockwise Hue Direction

    顺时针方向的色调插值。
    """

    Ccw = 'ccw'
    """逆时针色相方向 / Counterclockwise Hue Direction

    逆时针方向的色调插值。
    """


class CT_Colors(a_EG_ColorChoice):
    """21.4.4.7 effectClrLst (效果颜色列表)

    此元素定义应用于颜色变换中的效果的颜色列表。

    21.4.4.8 fillClrLst (填充颜色列表)

    21.4.4.9 linClrLst (线条颜色列表)

    21.4.4.12 txEffectClrLst (文字效果颜色列表)

    21.4.4.13 txFillClrLst (文本填充颜色列表)

    21.4.4.14 txLinClrLst (文本行颜色列表)
    """

    @property
    def colors(
        self,
    ) -> list[
        a_CT_ScRgbColor | a_CT_SRgbColor | a_CT_HslColor | a_CT_SystemColor | a_CT_SchemeColor | a_CT_PresetColor
    ]:
        """颜色列表"""
        return self.choice_and_more(*self.color_tags)  # type: ignore

    @property
    def meth(self):
        """色彩应用方法类型 / Color Application Method Type

        用于应用颜色变换的方法。
        """
        _val = self.attrib.get('meth', 'span')

        return ST_ClrAppMethod(_val)

    @property
    def hue_dir(self):
        """色相方向 / Hue Direction

        色调偏移（如果已定义）围绕色轮发生的方向.
        """
        _val = self.attrib.get('hueDir', 'cw')

        return ST_HueDir(_val)


class CT_CTStyleLabel(OxmlBaseElement):
    """21.4.4.10 styleLbl (样式label)

    该元素定义样式标签。 样式标签用于定义应用于图中给定节点的颜色变换。
    """

    @property
    def fill_clr_lst(self) -> Optional[CT_Colors]:
        """21.4.4.8 fillClrLst (填充颜色列表)"""
        return getattr(self, qn('dgm:fillClrLst'))

    @property
    def line_clr_lst(self) -> Optional[CT_Colors]:
        """21.4.4.9 linClrLst (线条颜色列表)"""

        return getattr(self, qn('dgm:linClrLst'))

    @property
    def effect_clr_lst(self) -> Optional[CT_Colors]:
        """21.4.4.7 effectClrLst (效果颜色列表)

        此元素定义应用于颜色变换中的效果的颜色列表。
        """

        return getattr(self, qn('dgm:effectClrLst'))

    @property
    def tx_line_clr_lst(self) -> Optional[CT_Colors]:
        """21.4.4.14 txLinClrLst (文本行颜色列表)"""

        return getattr(self, qn('dgm:txLinClrLst'))

    @property
    def tx_fill_clr_lst(self) -> Optional[CT_Colors]:
        """21.4.4.13 txFillClrLst (文本填充颜色列表)"""

        return getattr(self, qn('dgm:txFillClrLst'))

    @property
    def tx_effect_clr_lst(self) -> Optional[CT_Colors]:
        """21.4.4.12 txEffectClrLst (文字效果颜色列表)"""

        return getattr(self, qn('dgm:txEffectClrLst'))

    @property
    def ext_lst(self) -> Optional[a_CT_OfficeArtExtensionList]:
        return getattr(self, qn('dgm:extLst'))

    @property
    def name(self):
        """Name

        为样式标签指定的名称。 布局节点可以引用此名称，以便将样式标签应用到布局节点。
        """
        _val = self.attrib['name']

        return utils.AnyStrToStr(_val)  # type: ignore


class CT_ColorTransform(OxmlBaseElement):
    """21.4.4.3 colorsDef (颜色变换定义)

    该元素是颜色变换的根元素。 该元素中包含所有可用的颜色变换本身以及与定义通用颜色变换特性和属性相关联的其他元素和属性。

    """

    @property
    def title(self) -> list[CT_CTName]:
        """21.4.4.11 title (标题)

        颜色定义标题的名称或标题.
        """

        return self.findall(qn('dgm:title'))  # type: ignore

    @property
    def desc(self) -> list[CT_CTDescription]:
        """21.4.4.6 desc (描述)

        该元素包含颜色定义的描述。 该描述可用于描述与特定颜色变换定义相关联的质量。
        """
        return self.findall(qn('dgm:desc'))  # type: ignore

    @property
    def cat_list(self) -> list[CT_CTCategories]:
        return self.findall(qn('dgm:catLst'))  # type: ignore

    @property
    def style_lbl(self) -> list[CT_CTStyleLabel]:
        return self.findall(qn('dgm:styleLbl'))  # type: ignore

    @property
    def ext_lst(self) -> Optional[a_CT_OfficeArtExtensionList]:
        return getattr(self, qn('dgm:extLst'))

    @property
    def unique_id(self):
        """唯一id / Unique ID

        与颜色变换定义关联的唯一 ID.
        """
        _val = self.attrib.get('uniqueId', '')

        return utils.AnyStrToStr(_val)  # type: ignore

    @property
    def min_var(self):
        """最低版本 / Minimum Version

        可支持此颜色转换的最低产品版本.
        """
        _val = self.attrib.get('minVer', '')

        return utils.AnyStrToStr(_val)  # type: ignore


class CT_ColorTransformHeader(OxmlBaseElement):
    """21.4.4.4 colorsDefHdr (颜色变换定义标题)

    该元素指定与颜色变换定义关联的标头信息。 应用程序使用标头信息来预处理所需的数据，以帮助解决与颜色变换定义的初始完全加载相关的可能的性能问题。
    """

    @property
    def title(self) -> list[CT_CTName]:
        """21.4.4.11 title (标题)

        颜色定义标题的名称或标题.
        """
        return self.findall(qn('dgm:title'))  # type: ignore

    @property
    def desc(self) -> list[CT_CTDescription]:
        """21.4.4.6 desc (描述)

        该元素包含颜色定义的描述。 该描述可用于描述与特定颜色变换定义相关联的质量。
        """
        return self.findall(qn('dgm:desc'))  # type: ignore

    @property
    def cat_list(self) -> list[CT_CTCategories]:
        return self.findall(qn('dgm:catLst'))  # type: ignore

    @property
    def ext_lst(self) -> Optional[a_CT_OfficeArtExtensionList]:
        return getattr(self, qn('dgm:extLst'))

    @property
    def unique_id(self):
        _val = self.attrib['uniqueId']

        return utils.AnyStrToStr(_val)  # type: ignore

    @property
    def min_var(self):
        _val = self.attrib.get('minVer', '')

        return utils.AnyStrToStr(_val)  # type: ignore

    @property
    def res_id(self):
        _val = self.attrib.get('resId', '0')

        return int(_val)  # type: ignore


class CT_ColorTransformHeaderLst(OxmlBaseElement):
    """21.4.4.5 colorsDefHdrLst (颜色转换标题列表)

    该元素只是颜色变换定义标题的列表，用于将多个标题合并到一个组中。
    """

    @property
    def colors_def_hdr(self) -> list[CT_ColorTransformHeader]:
        return self.findall(qn('dgm:colorsDefHdr'))  # type: ignore


class ST_PtType(ST_BaseEnumType):
    """21.4.7.51 ST_PtType (点类型)

    这个简单的类型定义了可用于在DiagramML 中创建图表的不同点类型。
    """

    Node = 'node'
    """Node

    节点点类型指定基本点类型。
    """

    Asst = 'asst'
    """Assistant Element

    该点类型在层次图中用于表示辅助元素。
    """

    Doc = 'doc'
    """Document

    该点类型指定文档类型点。 该点类型可以被认为是与文档本身关联的根节点。
    """

    Pres = 'pres'
    """Presentation

    指定呈现点类型。
    """

    ParTrans = 'parTrans'
    """Parent Transition

    该点类型指定父过渡元素。
    """

    SibTrans = 'sibTrans'
    """Sibling Transition

    该点类型指定同级过渡元素。
    """


class CT_Pt(OxmlBaseElement):
    """点

    21.4.3.5 pt

    该元素定义了DiagramML 中的一个点。 DiagramML 中的点被定义为保存与图中特定点或节点关联的数据。 图中节点之间的转换以及节点本身被定义为不同类型的点。 点不仅负责保存与图中节点关联的数据，还负责保存对与特定节点关联的文本和形状进行的自定义属性。

    """

    @property
    def pr_set(self) -> Optional[CT_ElemPropSet]:
        """属性集

        21.4.3.4 prSet

        该元素包含在DiagramML 中的某些元素中使用的属性和自定义。 这些属性可分为以下几类：

        - 演示属性 - presLayoutVars、样式、presAssocId、presName、presStyleLbl、presStyleIdx、presStyleCnt
        - 文档属性 - loTypeId、loCatId、qsTypeId、qaCatId、csTypeId、coherent3DOff
        - 语义元素属性 - phldrT、phldr
        - 自定义属性 - custAng、custFlipVert、custFlipHor、custSzX、custSzY、custScaleX、custScaleY、custT、custLinFactX、custLinFactY、custLinFactNeighborX、custLinFactNeighborY、custRadScaleRad、custRadScaleInc

        考虑在 DrawingML 中针对文档点类型使用 prSet 的基本示例:

        <prSet loTypeId="urn:microsoft.com/office/officeart/2005/8/layout/default"
        loCatId="list"
        qsTypeId="urn:microsoft.com/office/officeart/2005/8/quickstyle/3d1" qsCatId="3D"
        csTypeId="urn:microsoft.com/office/officeart/2005/8/colors/colorful2"
        csCatId="colorful" phldr="1"/>

        在此示例中，我们定义布局标识符、布局类别、快速样式标识符、快速样式类别以及颜色样式和颜色样式类别.
        """
        return getattr(self, qn('dgm:prSet'), None)

    @property
    def sp_pr(self) -> Optional[a_CT_ShapeProperties]:
        """形状属性

        21.4.3.7 spPr

        此元素指定图表数据中单个形状的属性，如使用 DrawingML 子元素定义的那样。
        """
        return getattr(self, qn('dgm:spPr'), None)

    @property
    def t(self) -> Optional[a_CT_TextBody]:
        """正文

        21.4.3.8 t

        包含默认正文、段落和字符属性的文本正文。 应该有一个段落并且没有文字。
        第一个段落和除第一个段落之外的段落中的任何运行都将被忽略。
        """
        return getattr(self, qn('dgm:t'), None)

    @property
    def ext_lst(self) -> Optional[a_CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('dgm:extLst'))

    @property
    def model_id(self) -> ST_ModelId:
        """模型标识符 / Model Identifier

        数据模型中元素的唯一标识符。 该标识符仅相对于包含的数据模型应该是唯一的。

        考虑以下 cxnId 示例:

        <dgm:pt modelId="5" type="parTrans" cxnId="9">
            <dgm:prSet/>
            <dgm:spPr/>
        </dgm:pt>

        在本例中，我们定义点类型为 5。
        """
        _val = str(self.attrib['modelId'])

        if _val.isdigit():
            return int(_val)

        return s_ST_Guid(_val)

    @property
    def type(self):
        """点类型 / Point Type

        点的类型。

        考虑以下 cxnId 示例:

        <dgm:pt modelId="5" type="parTrans" cxnId="9">
            <dgm:prSet/>
            <dgm:spPr/>
        </dgm:pt>

        在此示例中，点类型被定义为 parTrans 点类型。
        """
        _val = self.attrib.get('type', 'node')

        return ST_PtType(_val)

    @property
    def cxn_id(self) -> ST_ModelId:
        """连接标识符 / Connection Identifier

        表示转换节点的连接的模型标识符。
        """
        _val = str(self.attrib.get('ST_ModelId', '0'))

        if _val.isdigit():
            return int(_val)

        return s_ST_Guid(_val)


class CT_PtList(OxmlBaseElement):
    """点列表

    21.4.3.6 ptLst

    该元素仅保存数据模型中的点列表。

    考虑以下在 DiagramML 中非常简单的点列表的示例:

    <dgm:ptLst>
        <dgm:pt modelId="0" type="doc"/>
        <dgm:pt modelId="1"/>
        <dgm:pt modelId="2"/>
        <dgm:pt modelId="3"/>
        <dgm:pt modelId="4"/>
        <dgm:pt modelId="5"/>
        <dgm:pt modelId="6"/>
    </dgm:ptLst>

    在此示例中，我们定义一个文档类型点和五个节点类型点.
    """

    @property
    def pt(self) -> list[CT_Pt]:
        """点

        21.4.3.5 pt

        该元素定义了DiagramML 中的一个点。 DiagramML 中的点被定义为保存与图中特定点或节点关联的数据。 图中节点之间的转换以及节点本身被定义为不同类型的点。 点不仅负责保存与图中节点关联的数据，还负责保存对与特定节点关联的文本和形状进行的自定义属性。
        """
        return self.findall(qn('dgm:pt'))  # type: ignore


class ST_CxnType(ST_BaseEnumType):
    """21.4.7.23 ST_CxnType (连接类型)

    这个简单类型定义了可以在两个节点之间定义的不同类型的关系。
    """

    ParOf = 'parOf'
    """父级 / Parent Of

    这定义了父子关系，即节点 X 是节点 Y 的父节点。
    """

    PresOf = 'presOf'
    """介绍 / Presentation Of

    表示类型关系。 这种类型的关系的存在是为了实际呈现数据。
    """

    PresParOf = 'presParOf'
    """演示文稿父级 / Presentation Parent Of

    定义表示节点的父节点的关系。
    """

    UnknownRelationship = 'unknownRelationship'
    """关系类型未知。"""


class CT_Cxn(OxmlBaseElement):
    """连接

    21.4.3.2 cxn

    该元素定义两点之间的连接。 连接定义了图中两点之间的关系。
    """

    @property
    def ext_lst(self) -> Optional[a_CT_OfficeArtExtensionList]:
        return getattr(self, qn('dgm:extLst'))

    @property
    def model_id(self):
        _val = self.attrib['modelId']

        return ST_ModelId(_val)  # type: ignore

    @property
    def type(self):
        _val = self.attrib.get('type', 'parOf')

        return ST_CxnType(_val)  # type: ignore

    @property
    def src_id(self):
        _val = self.attrib['srcId']

        return ST_ModelId(_val)  # type: ignore

    @property
    def dest_id(self):
        _val = self.attrib['destId']

        return ST_ModelId(_val)  # type: ignore

    @property
    def src_ord(self):
        _val = self.attrib['srcOrd']

        return to_xsd_unsigned_int(_val)  # type: ignore

    @property
    def dest_ord(self):
        _val = self.attrib['destOrd']

        return to_xsd_unsigned_int(_val)  # type: ignore

    @property
    def par_trans_id(self):
        _val = self.attrib.get('parTransId', '0')

        return ST_ModelId(_val)  # type: ignore

    @property
    def sib_trans_id(self):
        _val = self.attrib.get('sibTransId', '0')

        return ST_ModelId(_val)  # type: ignore

    @property
    def pres_id(self):
        _val = self.attrib.get('presId', '')

        return utils.AnyStrToStr(_val)  # type: ignore


class CT_CxnList(OxmlBaseElement):
    """连接列表

    21.4.3.3 cxnLst

    该元素定义一组连接。 可以为任何数据模型定义一个连接列表，其中包含图中定义的点之间的所有连接。

    考虑以下 DiagramML 中的 cxnLst 示例:

    <cxnLst>
        <cxn modelId="7" srcId="0" destId="1" srcOrd="0" destOrd="0"/>
        <cxn modelId="8" srcId="0" destId="2" srcOrd="1" destOrd="0"/>
        <cxn modelId="9" srcId="0" destId="3" srcOrd="2" destOrd="0"/>
        <cxn modelId="10" srcId="0" destId="4" srcOrd="3" destOrd="0"/>
        <cxn modelId="11" srcId="0" destId="5" srcOrd="4" destOrd="0"/>
        <cxn modelId="12" srcId="0" destId="6" srcOrd="5" destOrd="0"/>
    </cxnLst>

    在此示例中，我们看到 cxnLst 元素中定义了 6 个 cxn 元素（§21.4.3.2）。 在此示例中，在图中的点 0 和所有其他点之间定义了关系。
    """

    @property
    def cxn(self) -> list[CT_Cxn]:
        """连接

        21.4.3.2 cxn

        该元素定义两点之间的连接。 连接定义了图中两点之间的关系。
        """
        return self.findall(qn('dgm:cxn'))  # type: ignore


class CT_DataModel(OxmlBaseElement):
    """数据模型

    21.4.2.10 dataModel

    这个图表实例的数据。可以是样本数据模型，也可以是用户输入的数据。
    """

    @property
    def pt_lst(self) -> Optional[CT_PtList]:
        """点列表

        21.4.3.6 ptLst

        该元素仅保存数据模型中的点列表。

        考虑以下在 DiagramML 中非常简单的点列表的示例:

        <dgm:ptLst>
            <dgm:pt modelId="0" type="doc"/>
            <dgm:pt modelId="1"/>
            <dgm:pt modelId="2"/>
            <dgm:pt modelId="3"/>
            <dgm:pt modelId="4"/>
            <dgm:pt modelId="5"/>
            <dgm:pt modelId="6"/>
        </dgm:ptLst>

        在此示例中，我们定义一个文档类型点和五个节点类型点.
        """
        return getattr(self, qn('dgm:ptLst'), None)

    @property
    def cxn_lst(self) -> Optional[CT_CxnList]:
        """连接列表

        21.4.3.3 cxnLst

        该元素定义一组连接。 可以为任何数据模型定义一个连接列表，其中包含图中定义的点之间的所有连接。

        考虑以下 DiagramML 中的 cxnLst 示例:

        <cxnLst>
            <cxn modelId="7" srcId="0" destId="1" srcOrd="0" destOrd="0"/>
            <cxn modelId="8" srcId="0" destId="2" srcOrd="1" destOrd="0"/>
            <cxn modelId="9" srcId="0" destId="3" srcOrd="2" destOrd="0"/>
            <cxn modelId="10" srcId="0" destId="4" srcOrd="3" destOrd="0"/>
            <cxn modelId="11" srcId="0" destId="5" srcOrd="4" destOrd="0"/>
            <cxn modelId="12" srcId="0" destId="6" srcOrd="5" destOrd="0"/>
        </cxnLst>

        在此示例中，我们看到 cxnLst 元素中定义了 6 个 cxn 元素（§21.4.3.2）。 在此示例中，在图中的点 0 和所有其他点之间定义了关系。
        """
        return getattr(self, qn('dgm:cxnLst'), None)

    @property
    def bg(self) -> Optional[a_CT_BackgroundFormatting]:
        """背景格式

        21.4.3.1 bg

        此元素定义可应用于整个图表的背景形状的格式。 背景形状可以保存格式选项，就像普通形状可以在 DrawingML 中保存一样。
        """
        return getattr(self, qn('dgm:bg'))

    @property
    def whole(self) -> Optional[a_CT_WholeE2oFormatting]:
        """整个E2O格式化

        21.4.3.9 whole

        适用于整个图表对象（而不仅仅是背景）的格式包括线条和效果属性。
        """
        return getattr(self, qn('dgm:whole'), None)

    @property
    def ext_lst(self) -> Optional[a_CT_OfficeArtExtensionList]:
        """扩展列表"""

        return getattr(self, qn('dgm:extLst'))


class AG_IteratorAttributes(OxmlBaseElement):
    @property
    def axis_type(self) -> ST_AxisTypes:
        """Axis

        指定从数据模型中选择数据的轴。
        """
        _val = self.attrib.get('axis', 'none')

        return [ST_AxisType(_val)]

    @property
    def pt_type(self) -> ST_ElementTypes:
        """Data Point Type

        指定要选择的数据点的类型。
        """
        _val = self.attrib.get('ptType', 'all')

        return [ST_ElementType(_val)]

    @property
    def hide_last_trans(self) -> ST_Booleans:
        """隐藏上次转换 / Hide Last Transition

        在支持转换的算法中，此属性指定不渲染最后一个转换。 这允许图表以节点开始和结束.
        """
        _val = self.attrib.get('hideLastTrans', 'true')

        return [bool(_val)]  # type: ignore

    @property
    def st(self) -> ST_Ints:
        """Start

        指定数据集中的起始位置。
        """
        _val = self.attrib.get('st', '1')

        return [int(_val)]  # type: ignore

    @property
    def cnt(self) -> ST_UnsignedInts:
        """Count

        指定数据集中使用的项目数。
        """
        _val = self.attrib.get('cnt', '0')

        return [int(_val)]  # type: ignore

    @property
    def step(self) -> ST_Ints:
        """Step

        指定要在数据集中使用的步骤。 值为 2 的步骤返回集合中的所有其他项目.
        """
        _val = self.attrib.get('step', '1')

        return [int(_val)]  # type: ignore


class AG_ConstraintAttributes(OxmlBaseElement):
    @property
    def type(self) -> ST_ConstraintType:
        """约束类型 / Constraint Type

        指定应用于此布局节点的约束条件。
        """
        _val = self.attrib['type']

        return ST_ConstraintType(_val)

    @property
    def for_(self) -> ST_ConstraintRelationship:
        """For

        指定布局节点的轴，以应用约束或规则。
        """
        _val = self.attrib.get('for', 'self')

        return ST_ConstraintRelationship(_val)

    @property
    def for_name(self) -> str:
        """For Name

        指定要应用约束或规则的布局节点的名称。
        """
        _val = self.attrib.get('forName', '')

        return utils.AnyStrToStr(_val)  # type: ignore

    @property
    def pt_type(self) -> ST_ElementTypes:
        """数据点类型 / Data Point Type

        指定要选择的数据点类型。
        """
        _val = self.attrib.get('ptType', 'all')

        return [ST_ElementType(_val)]


class AG_ConstraintRefAttributes(OxmlBaseElement):
    @property
    def ref_type(self) -> ST_ConstraintType:
        """Reference Type

        指定引用约束的类型。
        """
        _val = self.attrib.get('refType', 'none')

        return ST_ConstraintType(_val)

    @property
    def ref_for(self) -> ST_ConstraintRelationship:
        """Reference For

        约束引用的 for 值。
        """
        _val = self.attrib.get('refFor', 'self')

        return ST_ConstraintRelationship(_val)

    @property
    def ref_for_name(self) -> str:
        """Reference For Name

        参考约束引用的布局节点的名称。
        """
        _val = self.attrib.get('refForName', '')

        return utils.AnyStrToStr(_val)  # type: ignore

    @property
    def ref_pt_type(self) -> ST_ElementType:
        """Reference Point Type

        引用约束中使用的点类型。
        """
        _val = self.attrib.get('refPtType', 'all')

        return ST_ElementType(_val)


class CT_Constraint(AG_ConstraintAttributes, AG_ConstraintRefAttributes):
    """21.4.2.8 constr (约束)

    该元素用于指定布局定义中节点的大小、位置、文本值以及节点之间的布局依赖关系。
    """

    @property
    def ext_lst(self) -> Optional[a_CT_OfficeArtExtensionList]:
        """扩展列表"""
        return getattr(self, qn('dgm:extLst'))

    @property
    def op(self) -> ST_BoolOperator:
        """操作 / Operator

        运算符约束用于评估条件。
        """
        _val = self.attrib.get('op', 'none')

        return ST_BoolOperator(_val)

    @property
    def val(self) -> float:
        """Value

        指定一个绝对值，而不是引用另一个约束。
        """
        _val = self.attrib.get('val', '0')

        return float(utils.AnyStrToStr(_val))  # type: ignore

    @property
    def fact(self) -> float:
        """因子 / Factor

        用于参考约束或规则中的因子，以便通过定义的因子修改参考值。
        """
        _val = self.attrib.get('fact', '1')

        return float(utils.AnyStrToStr(_val))  # type: ignore


class CT_Constraints(OxmlBaseElement):
    """21.4.2.9 constrLst (约束列表)

    这个元素只是一个约束列表。
    """

    @property
    def constr(self) -> list[CT_Constraint]:
        """约束合集"""
        return self.findall(qn('dgm:constr'))  # type: ignore


class CT_NumericRule(AG_ConstraintAttributes):
    """21.4.2.24 rule (规则)

    该元素允许指定更改现有约束值的规则。

    检查是否为NaN, https://stackoverflow.com/questions/944700/how-to-check-for-nan-values
    """

    @property
    def ext_lst(self) -> Optional[a_CT_OfficeArtExtensionList]:
        return getattr(self, qn('dgm:extLst'))

    @property
    def val(self) -> float:
        """Value

        指定绝对值而不是引用另一个约束。
        """
        # >>> import math
        # >>> math.isnan(float('NaN'))
        # True

        _val = self.attrib.get('val', 'NaN')

        return float(utils.AnyStrToStr(_val))  # type: ignore

    @property
    def fact(self) -> float:
        """因子 / Factor

        在参考约束或规则中使用的因子，以便通过定义的因子修改参考值。
        """
        # >>> import math
        # >>> math.isnan(float('NaN'))
        # True

        _val = self.attrib.get('fact', 'NaN')

        return float(utils.AnyStrToStr(_val))  # type: ignore

    @property
    def max(self) -> float:
        """Max Value

        设置约束的最大值，以便规则不能再将约束增加到超出该值。
        """
        # >>> import math
        # >>> math.isnan(float('NaN'))
        # True

        _val = self.attrib.get('max', 'NaN')

        return float(utils.AnyStrToStr(_val))  # type: ignore


class CT_Rules(OxmlBaseElement):
    """21.4.2.25 ruleLst (规则列表)

    该元素只是一个规则列表。

    该元素允许指定更改现有约束值的规则。
    """

    @property
    def rule(self) -> list[CT_NumericRule]:
        return self.findall(qn('dgm:rule'))  # type: ignore


class CT_PresentationOf(AG_IteratorAttributes):
    """21.4.2.21 presOf (Presentation Of)

    该元素指定要映射到包含布局节点的特定数据模型点。 该属性负责定义数据到图中布局节点的映射。
    """

    @property
    def ext_lst(self) -> Optional[a_CT_OfficeArtExtensionList]:
        return getattr(self, qn('dgm:extLst'))


class ST_OutputShapeType(ST_BaseEnumType):
    """输出形状类型

    21.4.7.48 ST_OutputShapeType

    专门用于 DrawingML 图表的形状。
    """

    none = 'none'
    """None

    无.
    """
    Conn = 'conn'
    """Connection

    连接形状类型。
    """


ST_LayoutShapeType = Union[a_ST_ShapeType, ST_OutputShapeType]
"""布局形状类型

21.4.7.41 ST_LayoutShapeType

所有可用的形状类型。

这个简单类型是以下类型的联合：

    - ST_OutputShapeType 简单类型 (§21.4.7.48).
    - ST_ShapeType 简单类型 (§20.1.10.56).

<xsd:simpleType name="ST_LayoutShapeType" final="restriction">
    <xsd:union memberTypes="a:ST_ShapeType ST_OutputShapeType"/>
</xsd:simpleType>
"""

ST_Index1 = NewType('ST_Index1', int)
"""基于1的索引

21.4.7.39 ST_Index1

从 1 开始的索引。

此简单类型的内容是 W3C XML Schema unsignedInt 数据类型的限制。

这个简单类型还指定了以下限制：

    - 此简单类型的最小值大于或等于 1。
"""


def to_ST_Index1(val: AnyStr):
    intval = int(utils.AnyStrToStr(val))

    if intval < 1:
        msg = f'预期外的值: {val}, 应大于等于1'
        raise OxmlAttributeValidateError(msg)

    return ST_Index1(intval)


class CT_Adj(OxmlBaseElement):
    """21.4.2.1 adj (形状手柄)

    调整形状的数值。这些数值可用于修改各种自动形状上支持的调整手柄。只能设置初始值，不能使用约束和规则进行修改。
    """

    @property
    def idx(self) -> ST_Index1:
        """调整手柄索引 / Adjust Handle Index

        调整值索引。不同的形状支持不同的调整手柄。
        """
        _val = self.attrib['idx']

        return ST_Index1(_val)  # type: ignore

    @property
    def val(self) -> float:
        """数值 / Value

        一个绝对值。
        """
        _val = self.attrib['val']

        return float(_val)


class CT_AdjLst(OxmlBaseElement):
    """21.4.2.2 adjLst (形状手柄列表)

    该元素只是形状手柄的列表。
    """

    @property
    def adj(self) -> list[CT_Adj]:
        return self.findall(qn('dgm:CT_Adj'))  # type: ignore


class CT_Shape(OxmlBaseElement):
    """21.4.2.27 shape (形状)

    由包含的布局节点显示的形状。 并非所有布局节点都显示形状.
    """

    @property
    def adj_lst(self) -> Optional[CT_AdjLst]:
        """形状手柄列表"""
        return getattr(self, qn('dgm:adjLst'))

    @property
    def ext_lst(self) -> Optional[a_CT_OfficeArtExtensionList]:
        """扩展列表"""
        return getattr(self, qn('dgm:extLst'))

    @property
    def rot(self) -> float:
        """旋转 / Rotation

        将形状旋转指定的度数。
        """
        _val = self.attrib.get('rot', '0')

        return float(_val)  # type: ignore

    @property
    def type(self):
        """形状类型 / Shape Type

        指定形状的类型。
        """
        _val = self.attrib.get('type', 'none')

        if a_ST_ShapeType.have_value(_val):
            return a_ST_ShapeType(_val)

        if ST_OutputShapeType.have_value(_val):
            return ST_OutputShapeType(_val)
        return None

    @property
    def blip(self) -> Optional[r_ST_RelationshipId]:
        """与图像部件的关系 / Relationship to Image Part

        指定与图像的显式关系的关系 ID，该图像应用作此形状内容的图像。
        """
        _val = self.attrib.get(qn('r:blip'))

        if _val is None:
            return None

        return r_ST_RelationshipId(_val)  # type: ignore

    @property
    def z_order_off(self) -> int:
        """Z 顺序偏移 / Z-Order Offset

        使形状偏离其默认 z 顺序堆叠，该堆叠基于布局节点在 XML 中出现的顺序。
        """
        _val = self.attrib.get('zOrderOff', '0')

        return int(_val)  # type: ignore

    @property
    def hide_geom(self) -> int:
        """隐藏几何图形 / Hide Geometry

        当设置为“true”时，隐藏形状的几何形状。 文字仍然可见。
        """
        _val = self.attrib.get('hideGeom')

        return to_xsd_bool(_val, none=False)

    @property
    def lk_tx_entry(self) -> int:
        """防止文本编辑 / Prevent Text Editing

        防止在此形状上进行文本编辑。
        """
        _val = self.attrib.get('lkTxEntry')

        return to_xsd_bool(_val, none=False)

    @property
    def blip_phldr(self) -> int:
        """图片占位符 / Image Placeholder

        指定是否使用图像占位符。
        """
        _val = self.attrib.get('blipPhldr')

        return to_xsd_bool(_val, none=False)


class CT_Parameter(OxmlBaseElement):
    """21.4.2.20 param (参数)

    parameter 元素修改算法的默认行为。
    """

    @property
    def type(self) -> ST_ParameterId:
        """Parameter Type

        指定正在修改的参数。
        """

        _val = self.attrib['type']

        return ST_ParameterId(_val)

    @property
    def val(self) -> ST_ParameterVal:
        """Value

        指定要赋予 type 属性定义的参数类型的实际值。
        """

        _val = utils.AnyStrToStr(self.attrib['val'])  # type: ignore

        if _val.isdigit():
            return int(_val)

        try:
            return float(_val)
        except Exception:
            pass

        try:
            return bool(_val)
        except Exception:
            pass

        if ST_DiagramHorizontalAlignment.have_value(_val):
            return ST_DiagramHorizontalAlignment(_val)

        if ST_VerticalAlignment.have_value(_val):
            return ST_VerticalAlignment(_val)

        if ST_ChildDirection.have_value(_val):
            return ST_ChildDirection(_val)

        if ST_ChildAlignment.have_value(_val):
            return ST_ChildAlignment(_val)

        if ST_SecondaryChildAlignment.have_value(_val):
            return ST_SecondaryChildAlignment(_val)

        if ST_LinearDirection.have_value(_val):
            return ST_LinearDirection(_val)

        if ST_SecondaryLinearDirection.have_value(_val):
            return ST_SecondaryLinearDirection(_val)

        if ST_StartingElement.have_value(_val):
            return ST_StartingElement(_val)

        if ST_BendPoint.have_value(_val):
            return ST_BendPoint(_val)

        if ST_ConnectorRouting.have_value(_val):
            return ST_ConnectorRouting(_val)

        if ST_ArrowheadStyle.have_value(_val):
            return ST_ArrowheadStyle(_val)

        if ST_ConnectorDimension.have_value(_val):
            return ST_ConnectorDimension(_val)

        if ST_RotationPath.have_value(_val):
            return ST_RotationPath(_val)

        if ST_CenterShapeMapping.have_value(_val):
            return ST_CenterShapeMapping(_val)

        if ST_NodeHorizontalAlignment.have_value(_val):
            return ST_NodeHorizontalAlignment(_val)

        if ST_NodeVerticalAlignment.have_value(_val):
            return ST_NodeVerticalAlignment(_val)

        if ST_FallbackDimension.have_value(_val):
            return ST_FallbackDimension(_val)

        if ST_TextDirection.have_value(_val):
            return ST_TextDirection(_val)

        if ST_PyramidAccentPosition.have_value(_val):
            return ST_PyramidAccentPosition(_val)

        if ST_PyramidAccentTextMargin.have_value(_val):
            return ST_PyramidAccentTextMargin(_val)

        if ST_TextBlockDirection.have_value(_val):
            return ST_TextBlockDirection(_val)

        if ST_TextAnchorHorizontal.have_value(_val):
            return ST_TextAnchorHorizontal(_val)

        if ST_TextAnchorVertical.have_value(_val):
            return ST_TextAnchorVertical(_val)

        if ST_DiagramTextAlignment.have_value(_val):
            return ST_DiagramTextAlignment(_val)

        if ST_AutoTextRotation.have_value(_val):
            return ST_AutoTextRotation(_val)

        if ST_GrowDirection.have_value(_val):
            return ST_GrowDirection(_val)

        if ST_FlowDirection.have_value(_val):
            return ST_FlowDirection(_val)

        if ST_ContinueDirection.have_value(_val):
            return ST_ContinueDirection(_val)

        if ST_Breakpoint.have_value(_val):
            return ST_Breakpoint(_val)

        if ST_Offset.have_value(_val):
            return ST_Offset(_val)

        if ST_HierarchyAlignment.have_value(_val):
            return ST_HierarchyAlignment(_val)

        if ST_ConnectorPoint.have_value(_val):
            return ST_ConnectorPoint(_val)

        return _val


class CT_Algorithm(OxmlBaseElement):
    """21.4.2.3 alg (算法)

    包含的布局节点使用的算法。该算法定义了布局节点的行为，以及嵌套布局节点的行为和布局。
    """

    @property
    def adj_lst(self) -> list[CT_Parameter]:
        """形状手柄列表"""
        return self.findall(qn('dgm:param'))  # type: ignore

    @property
    def ext_lst(self) -> Optional[a_CT_OfficeArtExtensionList]:
        """扩展列表"""
        return getattr(self, qn('dgm:extLst'))

    @property
    def type(self) -> ST_AlgorithmType:
        """算法类型 / Algorithm Type

        指定算法类型。
        """
        _val = self.attrib['type']

        return ST_AlgorithmType(_val)

    @property
    def rev(self):
        """修订号 / Revision Number

        算法的修订号。
        """
        _val = self.attrib.get('rev', '0')

        return to_xsd_unsigned_int(_val)  # type: ignore


class CT_LayoutNode(OxmlBaseElement):
    """21.4.2.19 layoutNode (布局节点)

    布局节点是图表的基本构建块。 布局节点负责定义形状在图表中的排列方式以及数据如何映射到图表中的特定形状。

    考虑以下在 DrawingML 图中定义的基本布局节点的示例：

    <layoutNode name="node">
        <varLst>
            <bulletEnabled val="1"/>
        </varLst>
        <presOf axis="desOrSelf" ptType="node"/>
        <alg type="tx"/>
        <shape type="rect"
            xmlns:r="http://purl.oclc.org/ooxml/officeDocument/relationships" r:blip="">
            <adjLst/>
        </shape>
        <constrLst/>
        <ruleLst>
            <rule type="primFontSz" forName="" val="2" fact="NaN" max="NaN"/>
        </ruleLst>
    </layoutNode>

    在此示例中，我们定义一个布局节点，其中包含文本并且是一个矩形。
    """

    @property
    def elements(
        self,
    ) -> list[
        CT_Algorithm | CT_Shape | CT_PresentationOf | CT_Constraints | CT_Rules | CT_LayoutVariablePropertySet | CT_ForEach | CT_LayoutNode | CT_Choose | a_CT_OfficeArtExtensionList
    ]:
        """元素节点"""
        tags = (
            qn('dgm:alg'),  # CT_Algorithm
            qn('dgm:shape'),  # CT_Shape
            qn('dgm:presOf'),  # CT_PresentationOf
            qn('dgm:constrLst'),  # CT_Constraints
            qn('dgm:ruleLst'),  # CT_Rules
            qn('dgm:varLst'),  # CT_LayoutVariablePropertySet
            qn('dgm:forEach'),  # CT_ForEach
            qn('dgm:layoutNode'),  # CT_LayoutNode
            qn('dgm:choose'),  # CT_Choose
            qn('dgm:extLst'),  # a:CT_OfficeArtExtensionList
        )

        return self.choice_and_more(*tags)  # type: ignore

    @property
    def name(self):
        """Name

        布局节点的唯一标识符。
        """
        _val = self.attrib.get('name', '')

        return utils.AnyStrToStr(_val)  # type: ignore

    @property
    def style_lbl(self):
        """Style Label

        指定应将样式或颜色变体中的哪个格式选项应用于此布局节点。
        """
        _val = self.attrib.get('styleLbl', '')

        return utils.AnyStrToStr(_val)  # type: ignore

    @property
    def ch_order(self):
        """Child Order

        指定给定布局节点的子布局节点的顺序。
        """
        _val = self.attrib.get('chOrder', 'b')

        return ST_ChildOrderType(_val)  # type: ignore

    @property
    def move_with(self):
        """Move With

        引用此布局节点随之移动的另一个布局节点。
        """
        _val = self.attrib.get('moveWith', '')

        return utils.AnyStrToStr(_val)  # type: ignore


class CT_ForEach(AG_IteratorAttributes):
    """21.4.2.14 forEach (For Each)

    一个循环结构，类似于编程语言中的for循环，用于定义哪些数据模型点使用此布局节点。

    考虑以下在DrawingML图表中使用forEach的示例。:

    <forEach name="Name5" ref="" axis="ch" ptType="node">
        <layoutNode name="node1" styleLbl="" moveWith="">
            <alg type="sp"/>
            <shape xmlns:r="http://purl.oclc.org/ooxml/officeDocument/relationships" r:blip="">
                <adjLst/>
            </shape>
            <constrLst/>
        </layoutNode>
    </forEach>

    在这个例子中，forEach元素为图表中的每个关联数据模型点创建一个布局节点，由名称节点1引用。在这个特定的实例中，forEach为当前点节点的每个子节点创建布局节点。
    """

    def elements(
        self,
    ) -> list[
        CT_Algorithm | CT_Shape | CT_PresentationOf | CT_Constraints | CT_Rules | CT_ForEach | CT_LayoutNode | CT_Choose | a_CT_OfficeArtExtensionList
    ]:
        tags = (
            qn('dgm:alg'),  # CT_Algorithm
            qn('dgm:shape'),  # CT_Shape
            qn('dgm:presOf'),  # CT_PresentationOf
            qn('dgm:constrLst'),  # CT_Constraints
            qn('dgm:ruleLst'),  # CT_Rules
            qn('dgm:forEach'),  # CT_ForEach
            qn('dgm:layoutNode'),  # CT_LayoutNode
            qn('dgm:choose'),  # CT_Choose
            qn('dgm:extLst'),  # a:CT_OfficeArtExtensionList
        )

        return self.choice_and_more(*tags)  # type: ignore

    @property
    def name(self):
        """Name

        布局节点的唯一标识符。
        """
        _val = self.attrib.get('name', '')

        return utils.AnyStrToStr(_val)  # type: ignore

    @property
    def ref(self):
        """Reference

        当在for-each元素上使用时，会导致指定的for-each元素被使用。
        """
        _val = self.attrib.get('ref', '')

        return utils.AnyStrToStr(_val)  # type: ignore


class CT_When(AG_IteratorAttributes):
    """21.4.2.15 if (If)

    就像编程语言中的 if 语句一样，包装要在其属性定义的条件下使用的元素。

    考虑以下在 Choose 语句上下文中的 DrawingML 图中的 if 元素示例:

    <choose name="Name1">
        <if name="Name2" func="var" arg="dir" op="equ" val="norm">
            <alg type="snake">
                <param type="grDir" val="tL" />
                <param type="flowDir" val="row" />
                <param type="contDir" val="sameDir" />
                <param type="off" val="ctr" />
            </alg>
        </if>
        <else name="Name3">
            <alg type="snake">
                <param type="grDir" val="tR" />
                <param type="flowDir" val="row" />
                <param type="contDir" val="sameDir" />
                <param type="off" val="ctr" />
            </alg>
        </else>
    </choose>

    在此示例中，if 元素用于定义当图处于法线方向时与蛇算法相关的一组参数.
    """

    def elements(
        self,
    ) -> list[
        CT_Algorithm | CT_Shape | CT_PresentationOf | CT_Constraints | CT_Rules | CT_ForEach | CT_LayoutNode | CT_Choose | a_CT_OfficeArtExtensionList
    ]:
        """子元素列表"""
        tags = (
            qn('dgm:alg'),  # CT_Algorithm
            qn('dgm:shape'),  # CT_Shape
            qn('dgm:presOf'),  # CT_PresentationOf
            qn('dgm:constrLst'),  # CT_Constraints
            qn('dgm:ruleLst'),  # CT_Rules
            qn('dgm:forEach'),  # CT_ForEach
            qn('dgm:layoutNode'),  # CT_LayoutNode
            qn('dgm:choose'),  # CT_Choose
            qn('dgm:extLst'),  # a:CT_OfficeArtExtensionList
        )

        return self.choice_and_more(*tags)  # type: ignore

    @property
    def name(self):
        """Name

        布局节点的唯一标识符。

        用于评估 if 条件的函数。
        """
        _val = self.attrib.get('name', '')

        return utils.AnyStrToStr(_val)  # type: ignore

    @property
    def func(self):
        """Function

        用于评估 if 条件的函数。

        考虑以下在 DrawingML 中使用 func 的示例:

        <if name="Name2" func="var" arg="dir" op="equ" val="norm">
            …
        </if>

        在此示例中，func 设置为 var。
        """
        _val = self.attrib['func']

        return ST_FunctionType(_val)  # type: ignore

    @property
    def arg(self):
        """Argument

        指定用作 if 元素中测试的一部分的变量。 除非将函数属性设置为“var”，否则将被忽略。
        """
        _val = self.attrib.get('arg', 'none')

        return ST_FunctionArgument(_val)  # type: ignore

    @property
    def op(self):
        """Operator

        用于评估条件的运算符。
        """
        _val = self.attrib['op']

        return ST_FunctionOperator(_val)  # type: ignore

    @property
    def val(self):
        """Value

        绝对值。
        """
        _val = self.attrib['val']

        return ST_FunctionValue(_val)  # type: ignore


class CT_Otherwise(OxmlBaseElement):
    """21.4.2.12 else (Else)

    这个元素类似于编程语言中的else语句，它将要在if条件不为真时使用的元素包裹起来。

    考虑以下在choose语句上下文中的DrawingML图表中的else元素示例。:

    <choose name="Name1">
        <if name="Name2" func="var" arg="dir" op="equ" val="norm">
            <alg type="snake">
                <param type="grDir" val="tL" />
                <param type="flowDir" val="row" />
                <param type="contDir" val="sameDir" />
                <param type="off" val="ctr" />
            </alg>
        </if>
        <else name="Name3">
            <alg type="snake">
                <param type="grDir" val="tR" />
                <param type="flowDir" val="row" />
                <param type="contDir" val="sameDir" />
                <param type="off" val="ctr" />
            </alg>
        </else>
    </choose>

    在这个例子中，使用else元素来定义与蛇算法相关的一组参数，当图表被反转时。
    """

    def elements(
        self,
    ) -> list[
        CT_Algorithm | CT_Shape | CT_PresentationOf | CT_Constraints | CT_Rules | CT_ForEach | CT_LayoutNode | CT_Choose | a_CT_OfficeArtExtensionList
    ]:
        tags = (
            qn('dgm:alg'),  # CT_Algorithm
            qn('dgm:shape'),  # CT_Shape
            qn('dgm:presOf'),  # CT_PresentationOf
            qn('dgm:constrLst'),  # CT_Constraints
            qn('dgm:ruleLst'),  # CT_Rules
            qn('dgm:forEach'),  # CT_ForEach
            qn('dgm:layoutNode'),  # CT_LayoutNode
            qn('dgm:choose'),  # CT_Choose
            qn('dgm:extLst'),  # a:CT_OfficeArtExtensionList
        )

        return self.choice_and_more(*tags)  # type: ignore

    @property
    def name(self):
        """名称 / Name

        与选择语句相关的唯一名称。

        考虑以下在DrawingML图表中的else元素示例。:

        <else name="Name1">
            …
        </else>

        在这个例子中，else元素被命名为Name1。
        """
        _val = self.attrib.get('name', '')

        return utils.AnyStrToStr(_val)  # type: ignore


class CT_Choose(OxmlBaseElement):
    """21.4.2.6 choose (选择元素)

    选择元素将if/else块包装成一个选择块。

    考虑以下DrawingML图表中选择元素的示例：

    <choose name="Name1">
        <if name="Name2" func="var" arg="dir" op="equ" val="norm">
            <alg type="snake">
                <param type="grDir" val="tL" />
                <param type="flowDir" val="row" />
                <param type="contDir" val="sameDir" />
                <param type="off" val="ctr" />
            </alg>
        </if>
        <else name="Name3">
            <alg type="snake">
                <param type="grDir" val="tR" />
                <param type="flowDir" val="row" />
                <param type="contDir" val="sameDir" />
                <param type="off" val="ctr" />
            </alg>
        </else>
    </choose>

    在这个例子中，使用一个选择元素来定义与蛇算法相关的两组不同的参数，这取决于用户希望算法流动的方向（从右到左或从左到右）。
    """

    @property
    def if_(self) -> list[CT_When]:
        return self.findall(qn('dgm:if'))  # type: ignore

    @property
    def else_(self) -> Optional[CT_Otherwise]:
        return self.findall(qn('dgm:else'))  # type: ignore

    @property
    def name(self):
        """名称 / Name

        与选择语句相关联的唯一名称。
        """
        _val = self.attrib.get('name', '')

        return utils.AnyStrToStr(_val)  # type: ignore


class CT_SampleData(OxmlBaseElement):
    """21.4.2.7 clrData (颜色转换示例数据)

    该元素定义了在用户界面控件中用于显示给定图表的颜色转换的示例数据。这个示例数据预定义了一个数据模型，与布局定义结合使用，以创建一个图表，可以将颜色转换应用并显示给用户，作为颜色转换的示例。

    考虑以下绘图ML图表中clrData元素的示例：

    <clrData>
        <dataModel>
            <ptLst>
                <pt modelId="0" type="doc" />
                <pt modelId="1" />
                <pt modelId="2" />
                <pt modelId="3" />
                <pt modelId="4" />
                <pt modelId="5" />
                <pt modelId="6" />
            </ptLst>
            <cxnLst>
                <cxn modelId="7" srcId="0" destId="1" srcOrd="0" destOrd="0" />
                <cxn modelId="8" srcId="0" destId="2" srcOrd="1" destOrd="0" />
                <cxn modelId="9" srcId="0" destId="3" srcOrd="2" destOrd="0" />
                <cxn modelId="10" srcId="0" destId="4" srcOrd="3" destOrd="0" />
                <cxn modelId="11" srcId="0" destId="5" srcOrd="4" destOrd="0" />
                <cxn modelId="12" srcId="0" destId="6" srcOrd="5" destOrd="0" />
            </cxnLst>
            <bg />
            <whole />
        </dataModel>
    </clrData>

    在这个例子中，我们定义了6个点，它们都与第七个文档类型点相连接。
    """

    @property
    def if_(self) -> list[CT_DataModel]:
        return self.findall(qn('dgm:dataModel'))  # type: ignore

    @property
    def use_def(self):
        """使用默认数据模型 / Use Default

        如果该属性的值为true，则忽略clrData元素中定义的数据模型，并使用默认数据模型。
        """
        _val = self.attrib.get('useDef', 'false')

        return to_xsd_bool(_val)


class CT_Category(OxmlBaseElement):
    """21.4.2.4 cat (类别)

    该元素指定了用户界面中的一个类别，该布局定义将显示给用户。

    考虑以下绘图ML图示中的cat的示例：

    <catLst>
        <cat type="relationship" pri="19000" />
    </catLst>

    在这个例子中，我们定义了一个名为"relationship"的单一类别，其优先级为19000。
    """

    @property
    def type(self):
        """类别类型 / Category Type

        指定与元素关联的类别类型。
        """
        _val = self.attrib['type']

        return XSD_AnyURI(utils.AnyStrToStr(_val))  # type: ignore

    @property
    def pri(self):
        """优先级 / Priority

        该图表中的类别优先级决定了其在用户界面中显示的顺序。较小的数字会显示在列表的开头。
        """
        _val = self.attrib['pri']

        return to_xsd_unsigned_int(_val)  # type: ignore


class CT_Categories(OxmlBaseElement):
    """21.4.2.5 catLst (类别列表)

    这个元素只是一个cat元素的列表。
    """

    def cate(self) -> list[CT_Category]:
        return self.findall(qn('dgm:cat'))  # type: ignore


class CT_Name(OxmlBaseElement):
    """21.4.2.30 title (标题)

    图表布局的标题.
    """

    @property
    def lang(self) -> str:
        """Language

        指定此布局定义的标题或描述的语言。
        """
        _val = self.attrib.get('lang', '')

        return str(_val)

    @property
    def val(self) -> str:
        """Value

        指定此布局定义的标题或描述。
        """
        _val = self.attrib['val']

        return str(_val)


class CT_Description(OxmlBaseElement):
    """21.4.2.11 desc (描述)

    该元素保存了布局定义的描述。描述可以用来描述与特定布局定义相关联的特性。
    """

    @property
    def lang(self) -> str:
        """语言 / Language

        标题或描述的自然语言布局定义。
        """
        _val = self.attrib.get('lang', '')

        return str(_val)

    @property
    def val(self) -> str:
        """值 / Value

        用作布局定义描述的字符串。
        """
        _val = self.attrib['val']

        return str(_val)


class CT_DiagramDefinition(OxmlBaseElement):
    """21.4.2.16 layoutDef (布局定义)

    该元素是用于定义布局定义的根元素。 布局定义是通过一组嵌套的布局节点来定义的。 布局定义负责定义图表的外观。
    """

    @property
    def title(self) -> list[CT_Name]:
        return self.findall(qn('dgm:title'))  # type: ignore

    @property
    def desc(self) -> list[CT_Description]:
        return self.findall(qn('dgm:desc'))  # type: ignore

    @property
    def cat_lst(self) -> list[CT_Categories]:
        return self.findall(qn('dgm:catLst'))  # type: ignore

    @property
    def samp_data(self) -> list[CT_SampleData]:
        return self.findall(qn('dgm:sampData'))  # type: ignore

    @property
    def style_data(self) -> list[CT_SampleData]:
        return self.findall(qn('dgm:styleData'))  # type: ignore

    @property
    def clr_data(self) -> list[CT_SampleData]:
        return self.findall(qn('dgm:clrData'))  # type: ignore

    @property
    def layout_node(self) -> list[CT_LayoutNode]:
        return self.findall(qn('dgm:layoutNode'))  # type: ignore

    @property
    def ext_lst(self) -> Optional[a_CT_OfficeArtExtensionList]:
        return getattr(self, qn('dgm:extLst'))

    @property
    def unique_id(self) -> str:
        """Unique Identifier

        此布局定义的唯一标识符。
        """
        _val = self.attrib.get('uniqueId', '')

        return str(_val)

    @property
    def min_ver(self) -> Optional[str]:
        """Minimum Version

        可以支持此布局定义的最低产品版本。
        """
        _val = self.attrib.get('minVer')

        if _val is not None:
            return str(_val)

        return None

    @property
    def def_style(self) -> str:
        """Default Style

        此属性定义对要应用于图表的默认样式的引用。
        """
        _val = self.attrib.get('defStyle', '')

        return str(_val)


class CT_DiagramDefinitionHeader(OxmlBaseElement):
    """21.4.2.17 layoutDefHdr (布局定义标题)

    该元素是表示应用程序预加载有关布局定义的信息所需的最少知识的标头信息。 这种预加载允许稍后进行布局定义的实际加载，这有助于解决应用程序可能存在的任何性能问题。

    考虑以下 DrawingML 图中的layoutDefHdr 示例:

    <layoutDefHdr uniqueId="urn:layout/default">
        <title val="Basic Block List" />
        <desc val="" />
        <catLst>
        <cat type="list" pri="1000" />
        </catLst>
    </layoutDefHdr>

    在此示例中，我们为 urn:layout:default 的 uniqueId 引用的图表定义标题以及类别和优先级.
    """

    @property
    def title(self) -> list[CT_Name]:
        return self.findall(qn('dgm:title'))  # type: ignore

    @property
    def desc(self) -> list[CT_Description]:
        return self.findall(qn('dgm:desc'))  # type: ignore

    @property
    def cat_lst(self) -> list[CT_Categories]:
        return self.findall(qn('dgm:catLst'))  # type: ignore

    @property
    def ext_lst(self) -> Optional[a_CT_OfficeArtExtensionList]:
        return getattr(self, qn('dgm:extLst'))

    @property
    def unique_id(self) -> str:
        """Unique Identifier

        此布局定义的唯一标识符。
        """
        _val = self.attrib.get('uniqueId', '')

        return str(_val)

    @property
    def min_ver(self) -> Optional[str]:
        """Minimum Version

        可以支持此布局定义的最低产品版本。
        """
        _val = self.attrib.get('minVer')

        if _val is not None:
            return str(_val)

        return None

    @property
    def def_style(self) -> str:
        """Default Style

        此属性定义对要应用于图表的默认样式的引用。
        """
        _val = self.attrib.get('defStyle', '')

        return str(_val)

    @property
    def res_id(self) -> int:
        """Resource Identifier

        内部使用的资源 ID。
        """
        _val = self.attrib.get('resId', '0')

        return int(_val)  # type: ignore


class CT_DiagramDefinitionHeaderLst(OxmlBaseElement):
    """21.4.2.18 layoutDefHdrLst (图表布局标题列表)

    该元素只是布局定义标题的列表。 此标题列表在内部用作将所有布局定义标题分组到单个结构中的方法。
    """

    @property
    def layout_def_hdr(self) -> list[CT_DiagramDefinitionHeader]:
        """布局定义列表

        该元素是表示应用程序预加载有关布局定义的信息所需的最少知识的标头信息。 这种预加载允许稍后进行布局定义的实际加载，这有助于解决应用程序可能存在的任何性能问题。
        """
        return self.findall(qn('dgm:layoutDefHdr'))  # type: ignore


class CT_RelIds(OxmlBaseElement):
    """21.4.2.22 relIds (与图表部分的显式关系)

    此元素指定用于显式引用 DrawingML 图表的四个组成部分中的每一个的关系 ID：

    - 图表颜色（cs 属性）
    - 图表数据（dm 属性）
    - 图表布局定义（lo 属性）
    - 图表样式（qs 属性）
    """

    @property
    def layout_def_hdr(self) -> list[CT_DiagramDefinitionHeader]:
        return self.findall(qn('dgm:layoutDefHdr'))  # type: ignore

    @property
    def r_dm(self) -> str:
        """与图表数据部分的显式关系 / Explicit Relationship to Diagram Data Part

        指定与此图使用的图数据部分的显式关系的关系 ID。

        此关系的类型应为 http://schemas.openxmlformats.org/officeDocument/2006/relationships/diagramData，否则文档应被视为不合格.
        """
        _val = self.attrib[qn('r:dm')]

        return r_ST_RelationshipId(str(_val))

    @property
    def r_lo(self) -> str:
        """与图布局定义部分的显式关系 / Explicit Relationship to Diagram Layout Definition Part

        指定与此图使用的图布局定义部分的显式关系的关系 ID。

        此关系的类型应为 http://schemas.openxmlformats.org/officeDocument/2006/relationships/diagramLayout，否则文档应被视为不合格。
        """
        _val = self.attrib[qn('r:lo')]

        return r_ST_RelationshipId(str(_val))

    @property
    def r_qs(self) -> str:
        """与样式定义部分的显式关系 / Explicit Relationship to Style Definition Part

        指定与该图使用的图表样式部分的显式关系的关系 ID。

        T他的关系应为 http://schemas.openxmlformats.org/officeDocument/2006/relationships/diagramQuickStyle 类型，否则该文档应被视为不合格。
        """
        _val = self.attrib[qn('r:qs')]

        return r_ST_RelationshipId(str(_val))

    @property
    def r_cs(self) -> str:
        """与图表颜色部分的明确关系 / Explicit Relationship to Diagram Colors Part

        指定与此图使用的图颜色部分的显式关系的关系 ID。

        此关系的类型应为 http://schemas.openxmlformats.org/officeDocument/2006/relationships/diagramColors，否则文档应被视为不合格.
        """
        _val = self.attrib[qn('r:cs')]

        return r_ST_RelationshipId(str(_val))


ST_ModelId = Union[int, s_ST_Guid]
"""21.4.7.43 ST_ModelId (模型标识符)

数据模型中元素的唯一 ID。 模型标识符可以是长整型或引导型。

这个简单类型是以下类型的联合：

    - ST_Guid 简单类型 (§22.9.2.4).
    - W3C XML Schema int 数据类型.
"""

ST_PrSetCustVal = Union[s_ST_Percentage, int]
"""21.4.7.66 ST_PrSetCustVal (属性设置自定义值)

此简单类型定义 DrawingML 中某些元素的自定义百分比值。

这个简单类型是以下类型的联合：

    - The ST_Percentage simple type (§22.9.2.9).
"""


class CT_ElemPropSet(OxmlBaseElement):
    """属性集

    21.4.3.4 prSet

    该元素包含在DiagramML 中的某些元素中使用的属性和自定义。 这些属性可分为以下几类：

    - 演示属性 - presLayoutVars、样式、presAssocId、presName、presStyleLbl、presStyleIdx、presStyleCnt
    - 文档属性 - loTypeId、loCatId、qsTypeId、qaCatId、csTypeId、coherent3DOff
    - 语义元素属性 - phldrT、phldr
    - 自定义属性 - custAng、custFlipVert、custFlipHor、custSzX、custSzY、custScaleX、custScaleY、custT、custLinFactX、custLinFactY、custLinFactNeighborX、custLinFactNeighborY、custRadScaleRad、custRadScaleInc

    考虑在 DrawingML 中针对文档点类型使用 prSet 的基本示例:

    <prSet loTypeId="urn:microsoft.com/office/officeart/2005/8/layout/default"
    loCatId="list"
    qsTypeId="urn:microsoft.com/office/officeart/2005/8/quickstyle/3d1" qsCatId="3D"
    csTypeId="urn:microsoft.com/office/officeart/2005/8/colors/colorful2"
    csCatId="colorful" phldr="1"/>

    在此示例中，我们定义布局标识符、布局类别、快速样式标识符、快速样式类别以及颜色样式和颜色样式类别.
    """

    @property
    def pres_layout_vars(self) -> list[CT_LayoutVariablePropertySet]:
        """演示文稿布局变量

        21.4.5.4 presLayoutVars

        该元素指定了布局属性集。 这组属性决定了有关图表布局的不同方面。 与用户界面的启用或禁用方面相关的所有元素也在此处定义。
        """
        return self.findall(qn('dgm:presLayoutVars'))  # type: ignore

    @property
    def style(self) -> list[a_CT_ShapeStyle]:
        """形状样式

        21.4.2.28 style

        此元素指定形状的样式信息，由其 DrawingML 子元素定义。
        """
        return self.findall(qn('dgm:style'))  # type: ignore

    @property
    def pres_assoc_id(self) -> Optional[ST_ModelId]:
        """表示元素标识符 / Presentation Element Identifier

        与此表示元素关联的点。 该标识符与 presName 一起使用来创建用于表示元素索引的唯一键。
        """
        _val = self.attrib.get('presAssocID')

        if _val is None:
            return None

        val = utils.AnyStrToStr(_val)  # type: ignore

        if val.isdigit():
            return int(val)

        return s_ST_Guid(val)

    @property
    def pres_name(self) -> Optional[str]:
        """演示名称 / Presentation Name

        此演示元素的布局节点名称。 该名称与 presAssocID 一起使用来创建用于表示元素索引的唯一键。
        """
        _val = self.attrib.get('presName')

        if _val is None:
            return None

        return utils.AnyStrToStr(_val)  # type: ignore

    @property
    def pres_style_lbl(self) -> Optional[str]:
        """演示风格标签 / Presentation Style Label

        指定此表示元素的布局节点样式标签。
        """
        _val = self.attrib.get('presStyleLbl')

        if _val is None:
            return None

        return utils.AnyStrToStr(_val)  # type: ignore

    @property
    def pres_style_idx(self) -> Optional[int]:
        """演示样式索引 / Presentation Style Index

        指定此表示元素的布局节点样式索引。

        """

        _val = self.attrib.get('presStyleIdx')

        if _val is None:
            return None

        return int(_val)

    @property
    def pres_style_cnt(self) -> Optional[int]:
        """演示风格计数 / Presentation Style Count

        指定此呈现元素的布局节点样式计数。
        """
        _val = self.attrib.get('presStyleCnt')

        if _val is None:
            return None

        return int(_val)

    @property
    def lo_type_id(self) -> Optional[str]:
        """当前图类型 / Current Diagram Type

        指定当前应用于图表的布局的标识符.
        """
        _val = self.attrib.get('loTypeId')

        if _val is None:
            return None

        return str(_val)

    @property
    def lo_cat_id(self) -> Optional[str]:
        """当前图类别 / Current Diagram Category

        指定应用于图表的布局类别的当前标识符.
        """
        _val = self.attrib.get('loCatId')

        if _val is None:
            return None

        return str(_val)

    @property
    def qs_type_id(self) -> Optional[str]:
        """当前样式类型 / Current Style Type

        指定当前应用的快速样式的标识符。
        """
        _val = self.attrib.get('qsTypeId')

        if _val is None:
            return None

        return str(_val)

    @property
    def qs_cat_id(self) -> Optional[str]:
        """当前风格类别 / Current Style Category

        指定当前应用的快速样式的类别标识符。
        """
        _val = self.attrib.get('qsCatId')

        if _val is None:
            return None

        return str(_val)

    @property
    def cs_type_id(self) -> Optional[str]:
        """颜色转换类型标识符 / Color Transform Type Identifier

        该属性指定当前应用的颜色变换的标识符.
        """
        _val = self.attrib.get('csTypeId')

        if _val is None:
            return None

        return str(_val)

    @property
    def cs_cat_id(self) -> Optional[str]:
        """颜色变换类别

        该属性指定当前颜色变换类别的标识符.
        """
        _val = self.attrib.get('csCatId')

        if _val is None:
            return None

        return str(_val)

    @property
    def coherent_3d_off(self) -> Optional[bool]:
        """连贯的 3D 行为 / Coherent 3D Behavior

        启用或禁用指定此属性的样式的连贯 3D 行为.
        """
        _val = self.attrib.get('coherent3DOff')

        if _val is None:
            return None

        return to_xsd_bool(_val)

    @property
    def phldr_t(self) -> Optional[str]:
        """占位符文本 / Placeholder Text

        如果占位符标志设置为 true，则用于在元素中显示的文本。 如果未设置此属性，则使用默认占位符文本。
        """
        _val = self.attrib.get('phldrT')

        if _val is None:
            return None

        return str(_val)

    @property
    def phldr(self) -> Optional[bool]:
        """占位符 / Placeholder

        指示该点是占位符或样本项。
        """
        _val = self.attrib.get('phldr')

        if _val is None:
            return None

        return to_xsd_bool(_val)

    @property
    def cust_ang(self) -> Optional[int]:
        """自定义旋转 / Custom Rotation

        指定自定义旋转的量。
        """
        _val = self.attrib.get('custAng')

        if _val is None:
            return None

        return int(_val)

    @property
    def cust_flip_vert(self) -> Optional[bool]:
        """自定义垂直翻转 / Custom Vertical Flip

        指定是否应用自定义垂直翻转。
        """
        _val = self.attrib.get('custFlipVert')

        if _val is None:
            return None

        return to_xsd_bool(_val)

    @property
    def cust_flip_hor(self) -> Optional[bool]:
        """自定义水平翻转 / Custom Horizontal Flip

        指定是否应用自定义水平翻转。
        """
        _val = self.attrib.get('custFlipHor')

        if _val is None:
            return None

        return to_xsd_bool(_val)

    @property
    def cust_sz_x(self) -> Optional[int]:
        """固定宽度覆盖 / Fixed Width Override

        指定形状的固定宽度覆盖。
        """
        _val = self.attrib.get('custSzX')

        if _val is None:
            return None

        return int(_val)

    @property
    def cust_sz_y(self) -> Optional[int]:
        """固定高度覆盖

        指定形状的固定高度覆盖。
        """
        _val = self.attrib.get('custSzY')

        if _val is None:
            return None

        return int(_val)

    @property
    def cust_scale_x(self) -> Optional[ST_PrSetCustVal]:
        """宽度比例 / Width Scale

        指定宽度缩放的量。
        """
        _val = self.attrib.get('custScaleX')

        if _val is None:
            return None

        if _val.isdigit():
            return int(_val)

        return s_to_ST_Percentage(_val)  # type: ignore

    @property
    def cust_scale_y(self) -> Optional[ST_PrSetCustVal]:
        """高度比例 / Height Scale

        指定高度缩放的量。
        """
        _val = self.attrib.get('custScaleY')

        if _val is None:
            return None

        if _val.isdigit():
            return int(_val)

        return s_to_ST_Percentage(_val)  # type: ignore

    @property
    def cust_t(self) -> Optional[bool]:
        """文字已更改 / Text Changed

        指定文本是否已自定义，从而允许布局忽略文本可用的自动格式设置选项.
        """
        _val = self.attrib.get('custT')

        if _val is None:
            return None

        return to_xsd_bool(_val)

    @property
    def cust_lin_fact_x(self) -> Optional[ST_PrSetCustVal]:
        """自定义因子宽度 / Custom Factor Width

        指定用于偏移形状的当前形状宽度的百分比.
        """

        _val = self.attrib.get('custLinFactX')

        if _val is None:
            return None

        if _val.isdigit():
            return int(_val)

        return s_to_ST_Percentage(_val)  # type: ignore

    @property
    def cust_lin_fact_y(self) -> Optional[ST_PrSetCustVal]:
        """定制因素高度 / Custom Factor Height

        指定用于偏移形状的当前形状高度的百分比.
        """
        _val = self.attrib.get('custLinFactY')

        if _val is None:
            return None

        if _val.isdigit():
            return int(_val)

        return s_to_ST_Percentage(_val)  # type: ignore

    @property
    def cust_lin_fact_neighbor_x(self) -> Optional[ST_PrSetCustVal]:
        """相邻偏移宽度 / Neighbor Offset Width

        指定用于偏移形状的相邻宽度的百分比。
        """
        _val = self.attrib.get('custLinFactNeighborX')

        if _val is None:
            return None

        if _val.isdigit():
            return int(_val)

        return s_to_ST_Percentage(_val)  # type: ignore

    @property
    def cust_lin_fact_neighbor_y(self) -> Optional[ST_PrSetCustVal]:
        """相邻偏移高度 / Neighbor Offset Height

        指定用于偏移形状的邻居高度的百分比。
        """
        _val = self.attrib.get('custLinFactNeighborY')

        if _val is None:
            return None

        if _val.isdigit():
            return int(_val)

        return s_to_ST_Percentage(_val)  # type: ignore

    @property
    def cust_rad_scale_rad(self) -> Optional[ST_PrSetCustVal]:
        """半径比例 / Radius Scale

        指定半径已缩放的程度。
        """
        _val = self.attrib.get('custRadScaleRad')

        if _val is None:
            return None

        if _val.isdigit():
            return int(_val)

        return s_to_ST_Percentage(_val)  # type: ignore

    @property
    def cust_rad_scale_inc(self) -> Optional[ST_PrSetCustVal]:
        """包括角度缩放量 / Include Angle Scale

        指定包含角度的缩放量。
        """
        _val = self.attrib.get('custRadScaleInc')

        if _val is None:
            return None

        if _val.isdigit():
            return int(_val)

        return s_to_ST_Percentage(_val)  # type: ignore


class ST_Direction(ST_BaseEnumType):
    """21.4.7.26 ST_Direction (图方向定义)

    这个简单的类型定义了图表在应用程序中显示时方向的可能值。
    """

    Norm = 'norm'
    """常规方向 / Normal Direction

    该值指定不应切换图表的方向。
    """

    Rev = 'rev'
    """反方向 / Reversed Direction

    该值指定应切换图表的方向。
    """


class ST_HierBranchStyle(ST_BaseEnumType):
    """层次结构分支样式定义

    21.4.7.37 ST_HierBranchStyle

    这个简单类型指定层次结构图的分支样式的可能值。
    """

    Left = 'l'
    """Left

    分支样式从左侧脱落。
    """

    Right = 'r'
    """Right

    分支样式从右侧脱落。
    """

    Hang = 'hang'
    """Hanging

    分支样式悬挂在父级上。
    """

    Std = 'std'
    """Standard

    将使用标准分支样式。
    """

    Init = 'init'
    """Initial

    这意味着该值尚未设置。
    """


class ST_AnimOneStr(ST_BaseEnumType):
    """21.4.7.3 ST_AnimOneStr (一对一动画值定义)

    这个简单的类型定义了用于 UI 中的逐一动画的字符串的可能值。 默认值为一。
    """

    none = 'none'
    """禁用一对一 / Disable One-by-One

    该值指定消费者应禁用一项一项的动画。
    """

    One = 'one'
    """一对一 / One By One

    该值指定用户界面中的一对一动画字符串应为“One By One”。
    """

    Branch = 'branch'
    """按分支一对一 / By Branch One By One

    该值指定用户界面中的一一动画字符串应为“By Branch One By One”。
    """


class ST_AnimLvlStr(ST_BaseEnumType):
    """21.4.7.2 ST_AnimLvlStr (动画级别字符串定义)

    这个简单的类型指定了消费者应该为该图的关卡动画显示的字符串的可能值。
    """

    none = 'none'
    """立即禁用级别 / Disable Level At Once

    该值指定消费者应立即禁用级别动画。
    """

    Lvl = 'lvl'
    """按关卡动画 / By Level Animation

    该值指定使用者应显示该图的“按级别”动画类型。
    """

    Center = 'ctr'
    """自中心动画 / From Center Animation

    该值指定消费者应允许该图的“从中心一次”或“从中心逐一”动画样式。
    """


class CT_OrgChart(OxmlBaseElement):
    """显示组织图表用户接口

    21.4.6.8 orgChart

    此元素用于指示何时显示与组织结构图专门关联的用户界面控件，例如能够将助手添加到选定的节点。

    考虑以下在 DiagramML 中使用的 orgChart 示例:

    <varLst>
        <orgChart val="true" />
        <chPref val="1" />
        <dir val="norm" />
        <animOne val="branch" />
        <animLvl val="lvl" />
        <resizeHandles val="rel" />
    </varLst>

    在此示例中，我们将 orgChart 值设置为 true，表示在使用包含图时将启用组织结构图特定的用户界面控件。
    """

    @property
    def val(self) -> bool:
        """显示组织图表用户接口值 / Show Organization Chart User Interface Value

        此属性值指定何时显示该图的“插入助手”用户界面控件和“更改布局”用户界面。
        """
        _val = self.attrib.get('val', 'false')

        return to_xsd_bool(_val)


ST_NodeCount = NewType('ST_NodeCount', int)
"""节点数量定义

21.4.7.44 ST_NodeCount

这个简单的类型定义了图中属性的节点数。 值 -1 表示该值无界。

此简单类型的内容是 W3C XML Schema int 数据类型的限制。

这个简单类型还指定了以下限制：

    - 此简单类型的最小值大于或等于 -1。
"""


def to_ST_NodeCount(val: Any):
    intval = int(val)

    if intval < -1:
        msg = f'预期外的值: {val}'
        raise OxmlAttributeValidateError(msg)

    return ST_NodeCount(intval)


class CT_ChildMax(OxmlBaseElement):
    """最大子节点数

    21.4.6.4 chMax

    此元素用于指示何时启用和禁用与向图表添加新形状相关的用户界面组件。 该元素定义了图表可以直接通过用户界面支持的最大节点数。

    考虑以下在 DiagramML 中使用 chMax 的示例:

    <varLst>
        <chMax val="5"/>
        <dir val="norm"/>
        <resizeHandles val="exact" />
    </varLst>

    在此示例中，我们将用户界面定义为只能插入五个节点。
    """

    @property
    def val(self) -> ST_NodeCount:
        """最大子节点值 / Maximum Children Value

        该属性指示在禁用用户界面之前该节点可以拥有的最大子节点数。 值 -1 表示子级的数量无限。 默认值为-1。
        """
        _val = self.attrib.get('val', '-1')

        return to_ST_NodeCount(_val)


class CT_ChildPref(OxmlBaseElement):
    """首选子节点数量

    21.4.6.5 chPref

    该变量表示当前节点希望拥有的子节点数量. [Note: 例如，这可用于指导默认情况下向层次结构中各个级别的图表添加多少形状。 end note]

    考虑以下在 DiagramML 中使用 chPref 的示例:

    <varLst>
        <chMax val="3" />
        <chPref val="1" />
        <dir val="norm" />
        <animLvl val="lvl" />
        <resizeHandles val="rel" />
    </varLst>

    在该示例中，chPref被设置为单个节点并且相关联的用户界面可以在插入单个节点之后禁用其他节点的插入。
    """

    @property
    def val(self) -> ST_NodeCount:
        """首选子节点数量 / Preferred Number of CHildren Value

        该属性指示当前节点希望拥有的子节点的数量。 值 -1 表示子级的数量无限。 默认值为-1。
        """
        _val = self.attrib.get('val', '-1')

        return to_ST_NodeCount(_val)


class CT_BulletEnabled(OxmlBaseElement):
    """显示插入节点

    21.4.6.3 bulletEnabled

    该元素用于指示是否启用与在数据模型中插入节点相关联的用户界面组件。

    考虑以下在DiagramML 中的bulletEnabled 示例:

    <varLst>
        <bulletEnabled val="true" />
    </varLst>

    在此示例中，当焦点位于包含的布局节点内时，将启用用户界面中的插入按钮。
    """

    @property
    def val(self) -> bool:
        """显示插入节点值 / Show Insert Node Value

        该属性用于指示是否应启用用于插入节点的用户界面。 true 值表示应启用用户界面.
        """
        _val = self.attrib.get('val', 'false')

        return to_xsd_bool(_val)


class CT_Direction(OxmlBaseElement):
    """图表方向

    21.4.6.6 dir

    该元素指示图表是否应切换方向。 该元素提供了考虑 LTR 或 RTL 方向的图表定义不同行为的能力。
    """

    @property
    def val(self) -> ST_Direction:
        """图表方向值 / Diagram Direction Value

        该变量指示图表是否应切换方向。
        """
        _val = self.attrib.get('val', 'norm')

        return ST_Direction(_val)


class CT_HierBranchStyle(OxmlBaseElement):
    """组织图表分支样式

    21.4.6.7 hierBranch

    此元素定义组织结构图中分支的布局样式。

    考虑以下在 DiagramML 中使用 hierBranch 的示例:

    <varLst>
        <hierBranch val="init" />
    </varLst>

    在此示例中，hierBranch 的值被定义为 init，它是一种未设置状态或初始状态。
    """

    @property
    def val(self) -> ST_HierBranchStyle:
        """组织图表分支样式值 / Organization Chart Branch Style Value

        该属性的值指示组织结构图中分支的布局样式。 默认值为标准。
        """
        _val = self.attrib.get('val', 'std')

        return ST_HierBranchStyle(_val)


class CT_AnimOne(OxmlBaseElement):
    """一对一动画字符串

    21.4.6.2 animOne

    该变量用于指示用户界面中用于一对一动画的字符串。 这主要在定义层次图时使用，以指定动画应用于图的不同级别的不同方式。

    考虑以下分层类型图中使用的 animOne 示例:

    <varLst>
        <chPref val="1" />
        <dir val="norm" />
        <animOne val="branch" />
        <animLvl val="lvl" />
        <resizeHandles val="exact" />
    </varLst>

    在此示例中，我们看到 animOne 元素被定义为每个分支的图表动画.
    """

    @property
    def val(self) -> ST_AnimOneStr:
        """一对一动画值 / One By One Animation Value

        指定用于图表的一对一动画的类型.
        """
        _val = self.attrib.get('val', 'one')

        return ST_AnimOneStr(_val)


class CT_AnimLvl(OxmlBaseElement):
    """级别动画

    21.4.6.1 animLvl

    该变量用于指示在用户界面中向用户显示的按级别字符串的动画。

    考虑以下在 DiagramML 中使用的 animLvl 示例:

    <varLst>
        <chMax val="1" />
        <dir val="norm" />
        <animLvl val="ctr" />
        <resizeHandles val="exact" />
    </varLst>

    在此示例中，我们看到 animLvl 设置为 ctr。 这是在径向类型图中定义的，它允许用户指定动画从图的中心开始。
    """

    @property
    def val(self) -> ST_AnimLvlStr:
        """级别动画值 / Level Animation Value

        该属性指示用于用户界面中级别动画的字符串.
        """
        _val = self.attrib.get('val', 'none')

        return ST_AnimLvlStr(_val)


class ST_ResizeHandlesStr(ST_BaseEnumType):
    """21.4.7.54 ST_ResizeHandlesStr (调整手柄大小)

    这个简单的类型定义了在图表中调整形状大小时可能的行为。 由于形状的大小在图中其他节点的整体布局中起着重要作用，因此可以通过两种方式在节点上调整大小。
    """

    Exact = 'exact'
    """Exact

    该值指定形状的大小发生调整，并且大小完全符合用户定义的大小，这会导致图表中的所有其他形状相应地缩小或增大。"""

    Rel = 'rel'
    """Relative

    该值指定调整大小操作是相对发生的。 这意味着在调整大小操作之前和之后节点之间的相对大小差异保持不变。
    """


class CT_ResizeHandles(OxmlBaseElement):
    """形状调整大小样式

    21.4.2.23 resizeHandles

    此元素定义在图表中调整形状大小时的行为。 由于形状的大小在图中其他节点的整体布局中起着重要作用，因此可以通过两种方式在节点上调整大小。
    """

    def val(self) -> ST_ResizeHandlesStr:
        """形状调整大小样式类型 / Shape Resize Style Type

        指定在图表中调整形状大小时形状的行为。

        如果未指定该属性，则默认值为 rel。
        """
        _val = self.attrib.get('val', 'rel')

        return ST_ResizeHandlesStr(_val)


class CT_LayoutVariablePropertySet(OxmlBaseElement):
    """演示文稿布局变量

    21.4.5.4 presLayoutVars

    该元素指定了布局属性集。 这组属性决定了有关图表布局的不同方面。 与用户界面的启用或禁用方面相关的所有元素也在此处定义。
    """

    @property
    def org_chart(self) -> Optional[CT_OrgChart]:
        """显示组织图表用户接口

        21.4.6.8 orgChart

        此元素用于指示何时显示与组织结构图专门关联的用户界面控件，例如能够将助手添加到选定的节点。

        考虑以下在 DiagramML 中使用的 orgChart 示例:

        <varLst>
            <orgChart val="true" />
            <chPref val="1" />
            <dir val="norm" />
            <animOne val="branch" />
            <animLvl val="lvl" />
            <resizeHandles val="rel" />
        </varLst>

        在此示例中，我们将 orgChart 值设置为 true，表示在使用包含图时将启用组织结构图特定的用户界面控件。
        """
        return getattr(self, qn('dgm:orgChart'))

    @property
    def ch_max(self) -> Optional[CT_ChildMax]:
        """最大子节点数

        21.4.6.4 chMax

        此元素用于指示何时启用和禁用与向图表添加新形状相关的用户界面组件。 该元素定义了图表可以直接通过用户界面支持的最大节点数。

        考虑以下在 DiagramML 中使用 chMax 的示例:

        <varLst>
            <chMax val="5"/>
            <dir val="norm"/>
            <resizeHandles val="exact" />
        </varLst>

        在此示例中，我们将用户界面定义为只能插入五个节点。
        """
        return getattr(self, qn('dgm:chMax'))

    @property
    def ch_pref(self) -> Optional[CT_ChildPref]:
        """首选子节点数量

        21.4.6.5 chPref

        该变量表示当前节点希望拥有的子节点数量. [Note: 例如，这可用于指导默认情况下向层次结构中各个级别的图表添加多少形状。 end note]

        考虑以下在 DiagramML 中使用 chPref 的示例:

        <varLst>
            <chMax val="3" />
            <chPref val="1" />
            <dir val="norm" />
            <animLvl val="lvl" />
            <resizeHandles val="rel" />
        </varLst>

        在该示例中，chPref被设置为单个节点并且相关联的用户界面可以在插入单个节点之后禁用其他节点的插入。
        """
        return getattr(self, qn('dgm:chPref'))

    @property
    def bullet_enabled(self) -> Optional[CT_BulletEnabled]:
        """显示插入节点

        21.4.6.3 bulletEnabled

        该元素用于指示是否启用与在数据模型中插入节点相关联的用户界面组件。

        考虑以下在DiagramML 中的bulletEnabled 示例:

        <varLst>
            <bulletEnabled val="true" />
        </varLst>

        在此示例中，当焦点位于包含的布局节点内时，将启用用户界面中的插入按钮。
        """
        return getattr(self, qn('dgm:bulletEnabled'))

    @property
    def dir(self) -> Optional[CT_Direction]:
        """图表方向

        21.4.6.6 dir

        该元素指示图表是否应切换方向。 该元素提供了考虑 LTR 或 RTL 方向的图表定义不同行为的能力。
        """
        return getattr(self, qn('dgm:dir'))

    @property
    def hier_branch(self) -> Optional[CT_HierBranchStyle]:
        """组织图表分支样式

        21.4.6.7 hierBranch

        此元素定义组织结构图中分支的布局样式。

        考虑以下在 DiagramML 中使用 hierBranch 的示例:

        <varLst>
            <hierBranch val="init" />
        </varLst>

        在此示例中，hierBranch 的值被定义为 init，它是一种未设置状态或初始状态。
        """
        return getattr(self, qn('dgm:hierBranch'))

    @property
    def anim_one(self) -> Optional[CT_AnimOne]:
        """一对一动画字符串

        21.4.6.2 animOne

        该变量用于指示用户界面中用于一对一动画的字符串。 这主要在定义层次图时使用，以指定动画应用于图的不同级别的不同方式。

        考虑以下分层类型图中使用的 animOne 示例:

        <varLst>
            <chPref val="1" />
            <dir val="norm" />
            <animOne val="branch" />
            <animLvl val="lvl" />
            <resizeHandles val="exact" />
        </varLst>

        在此示例中，我们看到 animOne 元素被定义为每个分支的图表动画.
        """
        return getattr(self, qn('dgm:animOne'))

    @property
    def anim_lvl(self) -> Optional[CT_AnimLvl]:
        """级别动画

        21.4.6.1 animLvl

        该变量用于指示在用户界面中向用户显示的按级别字符串的动画。

        考虑以下在 DiagramML 中使用的 animLvl 示例:

        <varLst>
            <chMax val="1" />
            <dir val="norm" />
            <animLvl val="ctr" />
            <resizeHandles val="exact" />
        </varLst>

        在此示例中，我们看到 animLvl 设置为 ctr。 这是在径向类型图中定义的，它允许用户指定动画从图的中心开始。
        """
        return getattr(self, qn('dgm:animLvl'))

    @property
    def resize_handles(self) -> Optional[CT_ResizeHandles]:
        """形状调整大小样式

        21.4.2.23 resizeHandles

        此元素定义在图表中调整形状大小时的行为。 由于形状的大小在图中其他节点的整体布局中起着重要作用，因此可以通过两种方式在节点上调整大小。
        """
        return getattr(self, qn('dgm:resizeHandles'))


class CT_SDName(OxmlBaseElement):
    """21.4.5.11 title (标题)

    该元素定义样式定义标题的标题。 标题只是样式定义的名称。
    """

    @property
    def lang(self) -> str:
        """自然语言 / Natural Language

        此快速样式的标题或描述的自然语言.
        """
        _val = self.attrib.get('lang', '')

        return utils.AnyStrToStr(_val)  # type: ignore

    @property
    def val(self) -> str:
        """描述 值 / Description Value

        用于描述的字符串。
        """
        _val = self.attrib['val']

        return utils.AnyStrToStr(_val)  # type: ignore


class CT_SDDescription(OxmlBaseElement):
    """21.4.5.3 desc (样式标签描述)

    该元素定义样式标签定义的描述。 描述只是一个描述样式标签定义特征的字符串。
    """

    @property
    def lang(self) -> str:
        """自然语言 / Natural Language

        此快速样式的标题或描述的自然语言。
        """
        _val = self.attrib.get('lang', '')

        return utils.AnyStrToStr(_val)  # type: ignore

    @property
    def val(self) -> str:
        """Description Value

        用于描述的字符串。
        """
        _val = self.attrib['val']

        return utils.AnyStrToStr(_val)  # type: ignore


class CT_SDCategory(OxmlBaseElement):
    """21.4.5.1 cat (类别)

    用户界面中此快速样式显示在用户界面中的类别。
    """

    @property
    def type(self) -> str:
        """类别类型 / Category Type

        类别类型。 这用于组织用户界面中的快速样式.
        """
        _val = self.attrib['type']

        return XSD_AnyURI(str(_val))

    @property
    def pri(self) -> int:
        """优先级 / Priority

        此样式的类别内的优先级决定了它在用户界面中的显示顺序。 较低的数字显示在列表的开头.
        """
        _val = self.attrib['pri']

        return to_xsd_unsigned_int(_val)  # type: ignore


class CT_SDCategories(OxmlBaseElement):
    """21.4.5.2 catLst (类别列表)

    该元素只是一个类别列表。
    """

    @property
    def cat(self) -> list[CT_SDCategory]:
        return self.findall(qn('dgm:cat'))  # type: ignore


class CT_TextProps(a_EG_Text3D):
    """21.4.5.12 txPr (文本属性)

    此元素定义可以通过样式标签应用于文本的特殊文本格式。
    """

    @property
    def text_3d(self) -> Optional[a_CT_Shape3D | a_CT_FlatText]:
        """
        aaa

        <xsd:group ref="EG_Text3D" minOccurs="0" maxOccurs="1"/>
        """

        return self.choice_one_child(*self.text3d_tags)  # type: ignore


class CT_StyleLabel(OxmlBaseElement):
    """21.4.5.10 styleLbl (样式label)

    该元素定义应用于图中节点的实际样式。该样式是从布局节点内引用的。 样式标签包含格式（不定义颜色），例如与形状关联的 3D 属性和文本属性。

    考虑以下 DiagramML 中的 styleLbl 示例:

    <styleLbl name="node0">
        <scene3d>
            <camera prst="orthographicFront" />
            <lightRig rig="flat" dir="t" />
        </scene3d>
        <sp3d prstMaterial="flat">
            <bevelT w="120900" h="88900" />
            <bevelB w="88900" h="31750" prst="angle" />
        </sp3d>
        <txPr />
        <style>
            <lnRef idx="0">
                <scrgbClr r="0" g="0" b="0" />
            </lnRef>
            <fillRef idx="3">
                <scrgbClr r="0" g="0" b="0" />
            </fillRef>
            <effectRef idx="2">
                <scrgbClr r="0" g="0" b="0" />
            </effectRef>
            <fontRef idx="minor">
                <schemeClr val="lt1" />
            </fontRef>
        </style>
    </styleLbl>

    在此示例中，我们看到定义了一个 styleLbl，它设置场景的 3D 属性、形状 3D 属性、线条、填充、效果和字体属性。
    """

    @property
    def scene_3d(self) -> Optional[a_CT_Scene3D]:
        return getattr(self, qn('dgm:scene3d'), None)

    @property
    def sp_3d(self) -> Optional[a_CT_Shape3D]:
        return getattr(self, qn('dgm:sp3d'), None)

    @property
    def tx_pr(self) -> Optional[CT_TextProps]:
        return getattr(self, qn('dgm:txPr'), None)

    @property
    def style(self) -> Optional[a_CT_ShapeStyle]:
        return getattr(self, qn('dgm:style'), None)

    @property
    def ext_lst(self) -> Optional[a_CT_OfficeArtExtensionList]:
        return getattr(self, qn('dgm:extLst'), None)

    @property
    def name(self) -> str:
        _val = self.attrib['name']

        return utils.AnyStrToStr(_val)  # type: ignore


class CT_StyleDefinition(OxmlBaseElement):
    """21.4.5.7 styleDef (样式定义)

    该元素是样式定义的根标记。

    考虑以下 DiagramML 中的 styleDef 示例:

    <dgm:styleDef xmlns:dgm="http://schemas.openxmlformats.org/drawingml/2006/diagram" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" uniqueId="urn:microsoft.com/office/officeart/2005/8/quickstyle/3d1" minVer="12.0">
        <dgm:title lang="" val="3-D Style 1" />
        <dgm:desc lang="" val="3-D Style 1" />
        <dgm:catLst>
            <dgm:cat type="3D" pri="11100" />
        </dgm:catLst>
        <dgm:scene3d>
            <a:camera prst="orthographicFront" />
            <a:lightRig rig="threePt" dir="t" />
        </dgm:scene3d>
        <dgm:style>…</dgm:style>
        <dgm:styleLbl name="node0">
            <dgm:scene3d>
                <a:camera prst="orthographicFront" />
                <a:lightRig rig="flat" dir="t" />
            </dgm:scene3d>
            <dgm:sp3d prstMaterial="flat">
                <a:bevelT w="120900" h="88900" />
                <a:bevelB w="88900" h="31750" prst="angle" />
            </dgm:sp3d>
            <dgm:txPr />
            <dgm:style>
                <a:lnRef idx="0">
                    <a:scrgbClr r="0" g="0" b="0" />
                </a:lnRef>
                <a:fillRef idx="3">
                    <a:scrgbClr r="0" g="0" b="0" />
                </a:fillRef>
                <a:effectRef idx="2">
                    <a:scrgbClr r="0" g="0" b="0" />
                </a:effectRef>
                <a:fontRef idx="minor">
                    <a:schemeClr val="lt1" />
                </a:fontRef>
            </dgm:style>
        </dgm:styleLbl>…</dgm:styleDef>

    在此示例中，我们看到 styleDef 与许多属性一起定义。
    """

    @property
    def title(self) -> list[CT_SDName]:
        return self.findall(qn('dgm:title'))  # type: ignore

    @property
    def desc(self) -> list[CT_SDDescription]:
        return self.findall(qn('dgm:desc'))  # type: ignore

    @property
    def cat_lst(self) -> list[CT_SDCategories]:
        return self.findall(qn('dgm:catLst'))  # type: ignore

    @property
    def scene_3d(self) -> list[a_CT_Scene3D]:
        return self.findall(qn('dgm:scene3d'))  # type: ignore

    @property
    def style_lbl(self) -> list[CT_StyleLabel]:
        return self.findall(qn('dgm:styleLbl'))  # type: ignore

    @property
    def ext_lst(self) -> Optional[a_CT_OfficeArtExtensionList]:
        return getattr(self, qn('dgm:extLst'), None)

    @property
    def unique_id(self) -> str:
        """Unique Style ID

        标识样式的唯一 ID。
        """
        _val = self.attrib.get('uniqueId', '')

        return str(_val)

    @property
    def min_ver(self) -> Optional[str]:
        """Minimum Version

        能够支持这种快速风格的最低产品版本.
        """
        _val = self.attrib.get('minVer')

        if _val is None:
            return None

        return str(_val)


class CT_StyleDefinitionHeader(OxmlBaseElement):
    """21.4.5.8 styleDefHdr (样式定义标头)

    该元素指定与样式定义关联的标头信息。 应用程序使用标头信息来预处理所需的数据，以帮助解决与颜色变换定义的初始完全加载相关的可能的性能问题。

    考虑以下 DiagramML 中 styleDefHdr 元素的示例:

    <styleDefHdr uniqueId="urn:quicktyle/3d1">
        <title val="3D" />
        <desc val="" />
        <catLst>
            <cat type="3D" pri="10100" />
        </catLst>
    </styleDefHdr >

    在此示例中，我们看到一个样式定义标头，它定义了一组样式定义的标题和类别。
    """

    @property
    def title(self) -> list[CT_SDName]:
        return self.findall(qn('dgm:title'))  # type: ignore

    @property
    def desc(self) -> list[CT_SDDescription]:
        return self.findall(qn('dgm:desc'))  # type: ignore

    @property
    def cat_lst(self) -> list[CT_SDCategories]:
        return self.findall(qn('dgm:catLst'))  # type: ignore

    @property
    def ext_lst(self) -> Optional[a_CT_OfficeArtExtensionList]:
        return getattr(self, qn('dgm:extLst'), None)

    @property
    def unique_id(self) -> str:
        """唯一样式ID / Unique Style ID

        该属性定义了关联样式定义的唯一标识符。
        """
        _val = self.attrib.get('uniqueId', '')

        return str(_val)

    @property
    def min_ver(self) -> Optional[str]:
        """Minimum Version

        能够支持这种快速风格的最低产品版本。
        """
        _val = self.attrib.get('minVer')

        if _val is None:
            return None

        return str(_val)

    @property
    def res_id(self) -> int:
        """资源ID / Resource ID

        该属性是将标头与实际样式定义部分相关联的 id。
        """
        _val = self.attrib.get('resId', '0')

        return int(_val)  # type: ignore


class CT_StyleDefinitionHeaderLst(OxmlBaseElement):
    """21.4.5.9 styleDefHdrLst (样式定义标头列表)

    该元素只是样式定义标题的列表，用于将多个标题合并为一组。
    """

    @property
    def style_def_hdr(self) -> list[CT_StyleDefinitionHeader]:
        return self.findall(qn('dgm:styleDefHdr'))  # type: ignore


class ST_AlgorithmType(ST_BaseEnumType):
    """21.4.7.1 ST_AlgorithmType (算法类型)

    可用算法的类型。
    """

    Composite = 'composite'
    """复合算法 / Composite

    复合算法指定所有子布局节点的大小和位置。 您可以使用它来创建具有预定布局的图形，或者与其他算法结合使用来创建更复杂的形状。
    """

    Conn = 'conn'
    """连接器算法 / Connector Algorithm

    连接器算法对布局节点之间的连接线、箭头和形状进行布局和布线。
    """

    Cycle = 'cycle'
    """循环算法 / Cycle Algorithm

    循环算法使用等角间距围绕圆或圆的一部分布置子布局节点。
    """

    HierChild = 'hierChild'
    """层次子算法 / Hierarchy Child Algorithm

    层次结构子算法与 hierRoot 算法配合使用来创建层次结构树布局。 该算法将其子布局节点对齐并定位在 hierRoot 布局节点下的线性路径中。
    """

    HierRoot = 'hierRoot'
    """层次根算法 / Hierarchy Root Algorithm

    层次结构根算法与 hierChild 算法一起创建层次结构树布局。 hierRoot 算法相对于 hierChild 布局节点对齐和定位 hierRoot 布局节点。
    """

    Pyra = 'pyra'
    """金字塔算法 / Pyramid Algorithm

    金字塔算法沿垂直路径布置子布局节点，并与梯形形状一起创建金字塔。
    """

    Lin = 'lin'
    """线性算法 / Linear Algorithm

    线性算法沿线性路径布置子布局节点。
    """

    Sp = 'sp'
    """空间算法 / Space Algorithm

    空间算法用于指定其他布局节点之间的最小空间，或作为对布局节点的大小和位置不执行任何操作的指示。
    """

    Tx = 'tx'
    """文本算法 / Text Algorithm

    文本算法调整文本大小以适合形状并控制其边距和对齐方式。
    """

    Snake = 'snake'
    """蛇算法 / Snake Algorithm

    蛇算法沿二维线性路径布置子布局节点，允许线性流继续跨多行或多列。
    """


class ST_AxisType(ST_BaseEnumType):
    """21.4.7.6 ST_AxisType (轴类型)

    这个简单类型定义了与当前上下文节点相关的不同节点集。
    """

    Self = 'self'
    """自身节点 / Self

    指定调用上下文节点。
    """

    Ch = 'ch'
    """子节点 / Child

    指定当前上下文节点的一组子节点。
    """

    Des = 'des'
    """后代 / Descendant

    指定当前上下文节点下的所有节点的集合。
    """

    DesOrSelf = 'desOrSelf'
    """后代或自己 / Descendant or Self

    指定当前上下文节点下的所有节点的集合，包括上下文节点。
    """

    Par = 'par'
    """父级 / Parent

    指定父节点。
    """

    Ancst = 'ancst'
    """祖先 / Ancestor

    指定当前上下文节点和根节点之间的一组节点，包括根节点。
    """

    AncstOrSelf = 'ancstOrSelf'
    """祖先或自己 / Ancestor or Self

    指定当前上下文节点和根节点之间的一组节点，包括根节点和上下文节点。
    """

    FollowSib = 'followSib'
    """关注兄弟姐妹 / Follow Sibling

    指定上下文节点之后的对等节点集。
    """

    PrecedSib = 'precedSib'
    """前任兄弟节点 / Preceding Sibling

    指定在上下文节点之前是对等节点的节点集。
    """

    Follow = 'follow'
    """跟随 / Follow

    指定上下文节点之后的对等节点以及这些对等节点的所有后代的节点集。
    """

    Preced = 'preced'
    """前节点 / Preceding

    指定上下文节点之前的对等节点以及这些对等节点的所有后代的节点集。
    """

    Root = 'root'
    """根节点 / Root

    指定图的最顶层节点。
    """

    none = 'none'
    """无 / None

    指定无节点。
    """


ST_AxisTypes = list[ST_AxisType]
"""21.4.7.7 ST_AxisTypes (轴类型列表)

这个简单类型表示轴类型列表
"""


class ST_BoolOperator(ST_BaseEnumType):
    """21.4.7.10 ST_BoolOperator (布尔约束)

    这种简单类型指定了可应用于比较约束的布尔运算。
    """

    none = 'none'
    """无 / None

    指定非布尔运算符
    """

    Equ = 'equ'
    """等于 / Equal

    相等操作。
    """

    Gte = 'gte'
    """大于或等于 / Greater Than or Equal to

    指定大于或等于布尔运算符。
    """

    Lte = 'lte'
    """小于或等于 / Less Than or Equal to

    指定小于或等于布尔运算符。
    """


class ST_ChildOrderType(ST_BaseEnumType):
    """21.4.7.15 ST_ChildOrderType (子节点排序)

    这个简单类型指定给定布局节点的子顺序。
    """

    Bottom = 'b'
    """子节点沿底部顺序排列。
    """

    Top = 't'
    """子节点沿顶部顺序排列。
    """


class ST_ConstraintType(ST_BaseEnumType):
    """21.4.7.21 ST_ConstraintType (约束类型)

    这个简单的类型定义了可用的可能约束的列表。
    """

    none = 'none'
    """未知的约束。
    """

    AlignOff = 'alignOff'
    """对齐偏移 / Alignment Offset

    该值定义节点的对齐偏移量。
    """

    BegMarg = 'begMarg'
    """起始边距 / Beginning Margin

    指定起始边距。
    """

    BendDist = 'bendDist'
    """弯曲距离 / Bending Distance

    指定从连接器起点到连接器折弯的距离
    """

    BegPad = 'begPad'
    """起始内边距 / Beginning Padding

    指定起始内边距
    """

    Bottom = 'b'
    """底部 / Bottom

    节点的底部。
    """

    BMarg = 'bMarg'
    """下边距 / Bottom Margin

    指定下边距。
    """

    BOff = 'bOff'
    """底部偏移 / Bottom Offset

    指定底部偏移。
    """

    CtrX = 'ctrX'
    """中心高度 / Center Height

    指定高度的中心。
    """

    CtrXOff = 'ctrXOff'
    """Center X Offset

    指定中心 x 坐标偏移。
    """

    CtrY = 'ctrY'
    """

    指定宽度的中心。
    """

    CtrYOff = 'ctrYOff'
    """指定中心 y 坐标偏移。
    """

    ConnDist = 'connDist'
    """连接距离 / Connection Distance

    指定连接距离
    """

    Diam = 'diam'
    """指定直径。
    """

    EndMarg = 'endMarg'
    """指定结束边距。
    """

    EndPad = 'endPad'
    """指定结束内边距
    """

    H = 'h'
    """指定高度。
    """

    HArH = 'hArH'
    """指定连接器箭头部分的高度
    """

    HOff = 'hOff'
    """指定偏移高度的量。
    """

    L = 'l'
    """指定左约束。
    """

    LMarg = 'lMarg'
    """指定左边距。
    """

    LOff = 'lOff'
    """指定左偏移量。
    """

    R = 'r'
    """指定右边的约束。
    """

    RMarg = 'rMarg'
    """指定右边距约束。
    """

    ROff = 'rOff'
    """指定右偏移约束。
    """

    PrimFontSz = 'primFontSz'
    """主要字体大小。
    """

    PyraAcctRatio = 'pyraAcctRatio'
    """指定为最短距离的飞出保留的图表宽度的分数。
    """

    SecFontSz = 'secFontSz'
    """次要字体大小。
    """

    SibSp = 'sibSp'
    """指定同级形状之间的最小距离。
    """

    SecSibSp = 'secSibSp'
    """次要兄弟节点间距。
    """

    Sp = 'sp'
    """指定定义的间距。
    """

    StemThick = 'stemThick'
    """指定箭杆的粗细。
    """

    T = 't'
    """指定顶部约束。
    """

    TMarg = 'tMarg'
    """顶部边距约束。
    """

    TOff = 'tOff'
    """顶部偏移约束。
    """

    UserA = 'userA'
    UserB = 'userB'
    UserC = 'userC'
    UserD = 'userD'
    UserE = 'userE'
    UserF = 'userF'
    UserG = 'userG'
    UserH = 'userH'
    UserI = 'userI'
    UserJ = 'userJ'
    UserK = 'userK'
    UserL = 'userL'
    UserM = 'userM'
    UserN = 'userN'
    UserO = 'userO'
    UserP = 'userP'
    UserQ = 'userQ'
    UserR = 'userR'
    UserS = 'userS'
    UserT = 'userT'
    UserU = 'userU'
    UserV = 'userV'
    UserW = 'userW'
    UserX = 'userX'
    UserY = 'userY'
    UserZ = 'userZ'

    W = 'w'
    """宽度参数。"""

    WArH = 'wArH'
    """指定连接器箭头部分的宽度。"""

    WOff = 'wOff'
    """将宽度偏移指定量。"""


class ST_ConstraintRelationship(ST_BaseEnumType):
    """21.4.7.20 ST_ConstraintRelationship (约束关系)

    这个简单类型指定了存在且可以使用的约束关系的类型。
    """

    Self = 'self'
    """自身 / Self

    布局节点映射到当前数据点。
    """

    Ch = 'ch'
    """子节点 / Child

    约束应该引用子节点。
    """

    Des = 'des'
    """后代节点 / Descendant

    布局节点可以映射到数据点的后代。
    """


class ST_ElementType(ST_BaseEnumType):
    """21.4.7.27 ST_ElementType (数据点类型)

    这个简单的类型定义了支持的不同类型的数据点。
    """

    All = 'all'
    """定义为利用所有节点。
    """

    Doc = 'doc'
    """指定文档级别的节点。
    """

    Node = 'node'
    """作为其他数据节点的子节点的数据节点。
    """

    Norm = 'norm'
    """选择正常元素。
    """

    NonNorm = 'nonNorm'
    """选择非正规元素。
    """

    Asst = 'asst'
    """辅助节点。
    """

    NonAsst = 'nonAsst'
    """选择所有非辅助节点。
    """

    ParTrans = 'parTrans'
    """与父节点关联的转换。
    """

    Pres = 'pres'
    """这是指表示节点。
    """

    SibTrans = 'sibTrans'
    """仅在数据节点之间使用同级转换。 这些过渡表示节点之间的兄弟关系，并且经常映射到绘图中形状之间的箭头。 sibTrans 值有时用于在节点之间创建空白
    """


ST_ElementTypes = list[ST_ElementType]
"""21.4.7.28 ST_ElementTypes (图表布局节点类型列表)

图表布局节点类型的列表。
"""


class ST_ParameterId(ST_BaseEnumType):
    """参数标识符

    21.4.7.49 ST_ParameterId

    这种简单类型定义了可以修改的算法参数，以便调整布局节点中使用的算法的行为。
    """

    BegPts = 'begPts'
    """Beginning Points

    起点
    """

    BegSty = 'begSty'
    """Beginning Arrowhead Style

    开始箭头样式
    """

    BendPt = 'bendPt'
    """Bend Point

    弯曲点。
    """

    Bkpt = 'bkpt'
    """Breakpoint

    指定图表开始蜿蜒的点。 值 bal 指定蛇行从偶数行和列开始。
    值固定指定蛇行从固定点开始。 值 endCnv 指定当行中没有更多空间容纳形状时开始蜿蜒。
    """

    BkPtFixedVal = 'bkPtFixedVal'
    """Breakpoint Fixed Value

    如果 bkpt=fixed，则指定蛇应断裂的位置。
    """

    ConnRout = 'connRout'
    """Connection Route

    连接的路线。
    """

    ChDir = 'chDir'
    """Child Direction

    子节点的方向.
    """

    ChAlign = 'chAlign'
    """Child Alignment

    指定子项的对齐方式。
    """

    CtrShpMap = 'ctrShpMap'
    """Center Shape Mapping

    指定相对于中心圆的节点放置位置。
    """

    ContDir = 'contDir'
    """Continue Direction

    指定后续行或列的方向. [Example: 如果算法最初从左到右放置节点，则 revDir 将节点从右到左放置在下一行中。 但是，如果算法使用 contDir，则下一行的节点将从左到右排列。 end example]
    """

    Dim = 'dim'
    """Connector Dimension

    指定连接器尺寸。
    """

    DstNode = 'dstNode'
    """Destination Node

    指定从中结束连接的布局节点的名称.
    """

    EndPts = 'endPts'
    """End Points

    指定端点。
    """

    EndSty = 'endSty'
    """End Style

    指定结束样式。
    """

    HorzAlign = 'horzAlign'
    """Horizontal Alignment

    对齐为父节点保留的空间内的所有子节点，并在 x 方向调整子节点位置。
    """

    VertAlign = 'vertAlign'
    """Vertical Alignment

    对齐为父节点保留的空间内的所有子节点，并调整 y 方向的子节点位置。
    """

    SecChAlign = 'secChAlign'
    """Secondary Child Alignment

    次要子节点对齐。
    """

    LinDir = 'linDir'
    """Linear Direction

    指定线性方向。
    """

    SecLinDir = 'secLinDir'
    """Secondary Linear Direction

    次要线性方向。
    """

    StElem = 'stElem'
    """Start Element

    指定用作循环中第一个形状的布局节点的点类型。
    """

    RotPath = 'rotPath'
    """ Rotation Path

    指定的旋转路径。
    """

    NodeHorzAlign = 'nodeHorzAlign'
    """Node Horizontal Alignment

    指定子节点如何在画布范围内对齐。 [Example: 您可以对齐所有子节点的顶部，但将所有子节点置于画布的中心。 end example]
    """

    NodeVertAlign = 'nodeVertAlign'
    """Node Vertical Alignment

    指定子节点如何在画布范围内对齐。 与 nodeHorzAlign 相同，但在 y 方向。
    """

    Fallback = 'fallback'
    """Fallback Scale

    1D 指定Fallback。 它仅在一维上缩放。

    2D 指定Fallback。 它在两个维度上的缩放比例相同。
    """

    TxDir = 'txDir'
    """Text Direction

    指定第一个节点的文本开始的位置。
    """

    PyraAcctPos = 'pyraAcctPos'
    """Pyramid Accent Position

    指定弹出孙子的位置。
    """

    PyraAcctTxMar = 'pyraAcctTxMar'
    """Pyramid Accent Text Margin

    指定子文本（孙节点）一侧边缘的位置。 如果值为step，则文本位于金字塔的边缘。 如果值为 stack，则文本对齐。
    """

    TxBlDir = 'txBlDir'
    """Text Block Direction

    指定文本块是垂直还是水平。
    """

    TxAnchorHorz = 'txAnchorHorz'
    """Text Anchor Horizontal

    指定形状内文本区域的 y 轴位置。
    """

    TxAnchorVert = 'txAnchorVert'
    """Text Anchor Vertical

    指定形状内文本区域的 x 轴位置。
    """

    TxAnchorHorzCh = 'txAnchorHorzCh'
    """Text Anchor Horizontal With Children

    指定如果形状中存在子节点，则定义可以允许在 x 轴上锚定不同的文本。
    """

    TxAnchorVertCh = 'txAnchorVertCh'
    """Text Anchor Vertical With Children

    指定如果形状中存在子节点，则定义可以允许在 y 轴上锚定不同的文本。
    """

    ParTxLTRAlign = 'parTxLTRAlign'
    """Parent Text Left-to-Right Alignment

    指定当形状只有父文本时父文本的段落对齐方式。 当文本方向为从左到右时，适用此参数。
    """

    ParTxRTLAlign = 'parTxRTLAlign'
    """Parent Text Right-to-Left Alignment

    指定当形状只有父文本时父文本的段落对齐方式。 当文本方向为从右到左时，适用此参数。
    """

    ShpTxLTRAlignCh = 'shpTxLTRAlignCh'
    """Shape Text Left-to-Right Alignment

    当形状同时包含父文本和子文本时，指定形状内所有文本的段落对齐方式。 当文本方向为从左到右时，适用此参数。
    """

    ShpTxRTLAlignCh = 'shpTxRTLAlignCh'
    """Shape Text Right-to-Left Alignment

    当形状同时包含父文本和子文本时，指定形状内所有文本的段落对齐方式。 当文本方向为从右到左时，适用此参数。
    """

    AutoTxRot = 'autoTxRot'
    """Auto Text Rotation

    自动文本旋转。
    """

    GrDir = 'grDir'
    """Grow Directio

    定蛇从哪个角生长。 [Example: 如果算法使用左上角值，则蛇从左上角开始生长。 end example]
    """

    FlowDir = 'flowDir'
    """Flow Direction

    指定节点是按行还是按列排列。
    """

    Off = 'off'
    """Offset

    指定偏移量。
    """

    HierAlign = 'hierAlign'
    """Hierarchy Alignment

    层次结构的对齐。
    """

    StBulletLvl = 'stBulletLvl'
    """Start Bullets At Level

    指定项目符号是从顶层 (1) 开始还是从子级 (2) 开始。
    """

    StAng = 'stAng'
    """Start Angle

    指定放置第一个形状的角度。 角度以度为单位，从周期中心笔直向上的线顺时针测量。
    """

    SpanAng = 'spanAng'
    """Span Angle

    指定循环跨越的角度。 最终的 shapealign 文本放置在 stAng+spanAng 处，除非 spanAng=360。

    在这种情况下，算法会放置文本以使形状不重叠。
    """

    Ar = 'ar'
    """Aspect Ratio

    指定确定子约束时要使用的复合节点的纵横比（宽度与高度）。 值 0 表示保留宽度和高度约束不变。 该算法可以暂时缩小一个维度以达到该比率。
    """

    LnSpPar = 'lnSpPar'

    LnSpAfParP = 'lnSpAfParP'
    """Line Spacing After Parent Paragraph

    父级之后的行距。
    """

    LnSpCh = 'lnSpCh'
    """Line Spacing Children

    子级的行距 lnSpPar (Parent Line Spacing) 父级的行距。
    """

    LnSpAfChP = 'lnSpAfChP'
    """Line Spacing After Children Paragraph

    子项之后的行间距。
    """

    RtShortDist = 'rtShortDist'
    """Route Shortest Distance

    如果为 true，则连接器将通过点之间的最短距离进行布线。
    """

    AlignTx = 'alignTx'
    """文本对齐 / Text Alignment

    This值定义文本在节点中的对齐方式。
    """

    PyraLvlNode = 'pyraLvlNode'
    """Pyramid Level Node

    如果金字塔有复合子节点，请指定构成金字塔本身的复合子节点的名称。 如果节点指定梯形形状，它将修改调整手柄以构造金字塔。
    """

    PyraAcctBkgdNode = 'pyraAcctBkgdNode'
    """Pyramid Accent Background Node

    如果金字塔有复合子节点，请指定构成子弹出形状的复合子节点的名称。 如果节点指定非等距梯形自动形状的形状，它会修改调整手柄以使弹出按钮与金字塔侧面齐平。
    """

    PyraAcctTxNode = 'pyraAcctTxNode'
    """Pyramid Accent Text Node

    如果金字塔有复合子节点，则指定应保存子文本的子节点。
    """

    SrcNode = 'srcNode'
    """Source Node

    指定从中启动连接的布局节点的名称。
    """


ST_Ints = list[int]
"""整型列表

21.4.7.40 ST_Ints

整数列表。
"""

ST_UnsignedInts = list[int]
"""21.4.7.63 ST_UnsignedInts (无符号整数列表)

无符号整数列表。
"""

ST_Booleans = list[bool]
"""21.4.7.9 ST_Booleans (布尔列表.)

布尔值列表。
"""


class ST_FunctionType(ST_BaseEnumType):
    """21.4.7.33 ST_FunctionType (功能类型)

    这个简单类型定义了可供使用的可用条件表达式函数类型集。
    """

    Cnt = 'cnt'
    """指定计数。
    """

    Pos = 'pos'
    """检索指定节点集中节点的位置。
    """

    RevPos = 'revPos'
    """反转位置功能。
    """

    PosEven = 'posEven'
    """如果指定节点位于数据模型中的偶数位置，则返回 1。
    """

    PosOdd = 'posOdd'
    """如果指定节点位于数据模型中的奇数位置，则返回 1。
    """

    Var = 'var'
    """用于引用变量。
    """

    Depth = 'depth'
    """指定深度。
    """

    MaxDepth = 'maxDepth'
    """定义最大深度。
    """


class ST_FunctionOperator(ST_BaseEnumType):
    """21.4.7.32 ST_FunctionOperator (函数运算符)

    这个简单类型定义了可用于执行操作的条件表达式函数。
    """

    Equ = 'equ'
    """等函数运算符。
    """

    Neq = 'neq'
    """指定不等于函数运算符。
    """

    Gt = 'gt'
    """指定大于函数运算符。
    """

    Lt = 'lt'
    """指定小于函数运算符。
    """

    Gte = 'gte'
    """指定大于或等于函数运算符。
    """

    Lte = 'lte'
    """指定小于或等于函数运算符。
    """


class ST_DiagramHorizontalAlignment(ST_BaseEnumType):
    """21.4.7.24 ST_DiagramHorizontalAlignment (水平对齐)

    这个简单的类型定义了水平对齐方式。
    """

    Left = 'l'
    """指定左对齐。
    """

    Center = 'ctr'
    """指定中心对齐方式。
    """

    Right = 'r'
    """指定右对齐。
    """

    none = 'none'
    """指定未定义对齐方式。
    """


class ST_VerticalAlignment(ST_BaseEnumType):
    """21.4.7.65 ST_VerticalAlignment (垂直对齐)

    这个简单的类型定义了不同的垂直对齐参数。
    """

    Top = 't'
    """指定顶部对齐。
    """

    Mid = 'mid'
    """指定居中对齐。
    """

    Bottom = 'b'
    """Bottom

    指定底部对齐。
    """

    none = 'none'
    """指定不垂直对齐。
    """


class ST_ChildDirection(ST_BaseEnumType):
    """21.4.7.14 ST_ChildDirection (子节点方向)

    这个简单类型定义了与特定父节点相关的子节点的布局方向。
    """

    Horz = 'horz'
    """水平 / Horizontal

    指定子节点水平布局。
    """

    Vert = 'vert'
    """垂直 / Vertical

    指定子节点垂直排列。
    """


class ST_ChildAlignment(ST_BaseEnumType):
    """21.4.7.13 ST_ChildAlignment (子节点对齐)

    这个简单的类型定义了如何在其分配的空间中对齐节点。
    """

    Top = 't'
    """指定将节点对齐到顶部。
    """

    Bottom = 'b'
    """指定将节点与底部对齐。    """

    Left = 'l'
    """指定将节点左对齐。
    """

    Right = 'r'
    """指定将节点右对齐。
    """


class ST_SecondaryChildAlignment(ST_BaseEnumType):
    """21.4.7.56 ST_SecondaryChildAlignment (次级子节点对齐方式)

    这个简单类型定义了层次结构算法的两个悬挂布局类型的不同对齐属性。
    """

    none = 'none'
    """指定不对齐。
    """

    Top = 't'
    """指定子节点应顶部对齐。
    """

    Bottom = 'b'
    """指定子节点应底部对齐。
    """

    Left = 'l'
    """指定子节点应左对齐。
    """

    Right = 'r'
    """指定子节点应右对齐。
    """


class ST_LinearDirection(ST_BaseEnumType):
    """线形方向

    21.4.7.42 ST_LinearDirection

    这个简单的类型定义了新节点的增长方向。
    """

    FromL = 'fromL'
    """From Left

    指定从左侧开始增长。
    """

    FromR = 'fromR'
    """From Right

    指定从右侧开始增长。
    """

    FromT = 'fromT'
    """From Top

    指定从顶部开始增长
    """

    FromB = 'fromB'
    """From Bottom

    指定从底部开始增长。
    """


class ST_SecondaryLinearDirection(ST_BaseEnumType):
    """21.4.7.57 ST_SecondaryLinearDirection (次线性方向)

    这种简单的类型为层次结构算法中双悬挂布局中的节点定义了不同的方向。
    """

    none = 'none'
    """None

    不指定方向。
    """

    FromL = 'fromL'
    """From Left

    指定节点从左侧开始向右移动。
    """

    FromR = 'fromR'
    """From Right

    指定节点从右侧开始并向左移动。
    """

    FromT = 'fromT'
    """From Top

    指定节点从顶部开始向下移动。
    """

    FromB = 'fromB'
    """From Bottom

    指定节点从底部开始向上移动。
    """


class ST_StartingElement(ST_BaseEnumType):
    """21.4.7.58 ST_StartingElement (起始元素)

    这个简单的类型定义循环算法中第一个节点的行为。
    """

    Node = 'node'
    """Node

    指定应首先放置一个节点。
    """

    Trans = 'trans'
    """Transition

    指定应首先放置过渡。
    """


class ST_RotationPath(ST_BaseEnumType):
    """21.4.7.55 ST_RotationPath (旋转路径)

    这个简单的类型定义了循环算法中节点的旋转属性。
    """

    none = 'none'
    """None

    指定节点不应旋转。
    """

    AlongPath = 'alongPath'
    """Along Path

    指定节点应根据其沿循环的位置进行旋转。
    """


class ST_CenterShapeMapping(ST_BaseEnumType):
    """21.4.7.12 ST_CenterShapeMapping (中心形状映射)

    这个简单的类型定义了循环算法的行为。
    """

    none = 'none'
    """无 / None

    指定循环图的正常布局。
    """

    FNode = 'fNode'
    """第一个节点 / First Node

    指定始终位于循环图中心的节点。
    """


class ST_BendPoint(ST_BaseEnumType):
    """21.4.7.8 ST_BendPoint (弯曲点)

    这种简单的类型定义了两个节点之间的连接中发生弯曲的位置。
    """

    Beg = 'beg'
    """开始 / Beginning

    弯曲发生在连接的开始处。
    """

    Def = 'def'
    """默认 / Default

    使用默认弯曲。 默认情况下，连接在中心弯曲。
    """

    End = 'end'
    """结尾 / End

    弯曲发生在连接的末端。
    """


class ST_ConnectorRouting(ST_BaseEnumType):
    """21.4.7.19 ST_ConnectorRouting (连接器布线)

    这个简单类型定义了两个节点之间的连接路由应该如何从节点 1 进展到节点 2。
    """

    Stra = 'stra'
    """直线 / Straight

    指定直线。
    """

    Bend = 'bend'
    """弯曲 / Bending

    指定以直角弯曲的弯曲连接。
    """

    Curve = 'curve'
    """曲线 / Curve

    指定弯曲的连接。
    """

    LongCurve = 'longCurve'
    """长曲线 / Long Curve

    指定半径大于简单弯曲连接的弯曲连接。
    """


class ST_ArrowheadStyle(ST_BaseEnumType):
    """21.4.7.4 ST_ArrowheadStyle (箭头样式)

    这个简单类型为连接器定义了不同的箭头样式类型。
    """

    Auto = 'auto'
    """自动 / Auto

    指定算法定义是否在连接器上使用箭头.
    """

    Arr = 'arr'
    """箭头呈现 / Arrowhead Present

    指定连接器上使用箭头.
    """

    NoArr = 'noArr'
    """无箭头 / No Arrowhead

    指定连接器上不使用箭头.
    """


class ST_ConnectorDimension(ST_BaseEnumType):
    """21.4.7.17 ST_ConnectorDimension (连接器尺寸)

    bbb
    """

    OneD = '1D'
    """1 维度 / 1 Dimension

    指定一维连接，或者更确切地说是一条线。
    """

    TwoD = '2D'
    """2 维度 / 2 Dimensions

    指定具有宽度和高度的二维连接。
    """

    Cust = 'cust'
    """自定义 / Custom

    指定自定义连接类型。
    """


class ST_ConnectorPoint(ST_BaseEnumType):
    """21.4.7.18 ST_ConnectorPoint (连接点)

    这种简单的类型定义了节点上可用的不同连接站点。
    """

    Auto = 'auto'
    """自动 / Auto

    指定算法确定要使用的最佳连接站点。
    """

    BCtr = 'bCtr'
    """底部中心 / Bottom Center

    指定要使用底部中心连接站点。
    """

    Ctr = 'ctr'
    """中心 / Center

    指定要使用中心连接站点。
    """

    MidL = 'midL'
    """中左 / Middle Left

    指定要使用中间左侧的连接站点。
    """

    MidR = 'midR'
    """中右 / Middle Right

    指定要使用右中连接位置。
    """

    TCtr = 'tCtr'
    """顶部中心 / Top Center

    指定要使用顶部中心连接站点。
    """

    BL = 'bL'
    """左下方 / Bottom Left

    指定要使用底部左侧的连接站点。
    """

    BR = 'bR'
    """右下角 / Bottom Right

    指定要使用右下角的连接站点。
    """

    TL = 'tL'
    """左上方 / Top Left

    指定要使用左上角的连接站点。
    """

    TR = 'tR'
    """右上 / Top Right

    指定要使用右上角的连接站点。
    """

    Radial = 'radial'
    """径向 / Radial

    指定沿径向路径的连接以支持循环图中连接的使用。
    """


class ST_NodeHorizontalAlignment(ST_BaseEnumType):
    """节点水平对齐

    21.4.7.45 ST_NodeHorizontalAlignment

    这个简单的类型定义了节点的水平对齐方式。


    """

    Left = 'l'
    """Left

    指定左对齐。
    """

    Center = 'ctr'
    """Center

    指定中心对齐方式。
    """

    Right = 'r'
    """Right

    指定右对齐。
    """


class ST_NodeVerticalAlignment(ST_BaseEnumType):
    """节点垂直对齐

    21.4.7.46 ST_NodeVerticalAlignment

    这个简单的类型定义了节点的垂直对齐方式。
    """

    Top = 't'
    """Top

    指定顶部对齐方式。
    """

    Mid = 'mid'
    """Middle

    指定中间对齐方式。
    """

    Bottom = 'b'
    """Bottom

    指定底部对齐方式。
    """


class ST_FallbackDimension(ST_BaseEnumType):
    """21.4.7.29 ST_FallbackDimension (fallback维度)

    指定节点可以自动增长或收缩的维度。
    """

    OneD = '1D'
    """1 维度 / 1 Dimension

    指定节点可以按其高度或宽度增大或缩小，但不能同时增大或缩小.
    """

    TwoD = '2D'
    """2 维度 / 2 Dimensions

    指定节点可以按高度和宽度增大或缩小。
    """


class ST_TextDirection(ST_BaseEnumType):
    """21.4.7.62 ST_TextDirection (文字方向)

    这种简单的类型定义了节点内附加文本增长的不同方式。
    """

    FromT = 'fromT'
    """From Top

    指定附加文本从顶部增长。
    """

    FromB = 'fromB'
    """From Bottom

    指定附加文本从底部增长。
    """


class ST_PyramidAccentPosition(ST_BaseEnumType):
    """21.4.7.52 ST_PyramidAccentPosition (金字塔重音位置)

    这种简单的类型定义了可以与金字塔算法相关联的重音形状的不同定位。
    """

    Bef = 'bef'
    """Before

    指定将强调形状放置在金字塔的左侧。
    """

    Aft = 'aft'
    """Pyramid Accent After

    指定将强调形状放置在金字塔的右侧。
    """


class ST_PyramidAccentTextMargin(ST_BaseEnumType):
    """金字塔重音文字边距

    21.4.7.53 ST_PyramidAccentTextMargin

    这种简单的类型定义了为金字塔算法以重音形状布局文本的不同方式。
    """

    Step = 'step'
    """Step

    指定所有重音形状文本都相对于金字塔。
    """

    Stack = 'stack'
    """Stack

    指定所有重音形状文本均左对齐。
    """


class ST_TextBlockDirection(ST_BaseEnumType):
    """21.4.7.61 ST_TextBlockDirection (文本块方向)

    这种简单的类型为节点内的文本定义了不同的布局选项。
    """

    Horz = 'horz'
    """Horizontal

    指定文本是水平的。
    """

    Vert = 'vert'
    """Vertical Direction

    指定文本是垂直的。
    """


class ST_TextAnchorHorizontal(ST_BaseEnumType):
    """21.4.7.59 ST_TextAnchorHorizontal (水平文本锚点)

    这种简单的类型定义文本的水平锚点。
    """

    none = 'none'
    """None

    指定没有水平文本锚点。
    """

    Center = 'ctr'
    """Center

    指定要锚定到中心的文本。
    """


class ST_TextAnchorVertical(ST_BaseEnumType):
    """21.4.7.60 ST_TextAnchorVertical (文本锚点垂直)

    这种简单的类型定义文本的垂直锚点。
    """

    Top = 't'
    """指定要锚定到顶部的文本。
    """

    Mid = 'mid'
    """指定要锚定到中间的文本。
    """

    Bottom = 'b'
    """指定要锚定到底部的文本。

    """


class ST_DiagramTextAlignment(ST_BaseEnumType):
    """21.4.7.25 ST_DiagramTextAlignment (文本对齐)

    这个简单的类型定义节点内文本的对齐类型。
    """

    Left = 'l'
    """指定左对齐文本。
    """

    Center = 'ctr'
    """指定居中对齐的文本。
    """

    Right = 'r'
    """指定右对齐文本。
    """


class ST_AutoTextRotation(ST_BaseEnumType):
    """21.4.7.5 ST_AutoTextRotation (自动文本旋转)

    此简单类型定义当布局期间算法旋转形状时文本如何在形状内旋转。
    """

    none = 'none'
    """aaa

    bbb
    """

    Upr = 'upr'
    """aaa

    bbb
    """

    Grav = 'grav'
    """重力 / Gravity

    指定当文本的角度达到阈值 90 度和 180 度时，文本旋转 180 度。
    """


class ST_GrowDirection(ST_BaseEnumType):
    """21.4.7.35 ST_GrowDirection (增长方向)

    这个简单的类型定义了蛇算法中节点的不同起始位置。
    """

    TL = 'tL'
    """指定节点的放置从左上角开始。
    """

    TR = 'tR'
    """指定节点的位置位于右上角。
    """

    BL = 'bL'
    """指定节点的放置从左下角开始。
    """

    BR = 'bR'
    """指定节点的放置从右下角开始。
    """


class ST_FlowDirection(ST_BaseEnumType):
    """21.4.7.30 ST_FlowDirection (流动方向)

    这个简单的类型定义了如何将新节点的进展输入到图中。
    """

    Row = 'row'
    """行 / Row

    指定布局以基于行的方式发生。 这意味着在从上到下移动之前从左到右布置节点。
    """

    Col = 'col'
    """列 / Column

    指定布局以基于列的方式出现。 这意味着先从上到下布置节点，然后再从左到右移动。
    """


class ST_ContinueDirection(ST_BaseEnumType):
    """21.4.7.22 ST_ContinueDirection (继续方向)

    这个简单类型指定了蛇算法中将附加节点添加到新行或新列的方向的行为。
    """

    RevDir = 'revDir'
    """反向 / Reverse Direction

    指定在后续行或列上遵循该方向。
    """

    SameDir = 'sameDir'
    """同一方向 / Same Direction

    指定在后续行或列上保持该方向。
    """


class ST_Breakpoint(ST_BaseEnumType):
    """21.4.7.11 ST_Breakpoint (断点)

    这个简单的类型定义了蛇算法在什么时候发生节点缠绕。
    """

    EndCnv = 'endCnv'
    """画布结尾 / End of Canvas

    指定在填充当前列或行的空间后将节点添加到下一列或行。
    """

    Bal = 'bal'
    """均衡 / Balanced

    指定每行和每列的节点数应该相等。
    """

    Fixed = 'fixed'
    """Fixed

    指定在列或行中使用用户定义的节点数。
    """


class ST_Offset(ST_BaseEnumType):
    """偏移

    21.4.7.47 ST_Offset

    这个简单类型定义蛇算法中的后续行或列是否相对于前一行或列偏移。
    """

    Ctr = 'ctr'
    """Center

    指定无偏移。
    """

    Off = 'off'
    """Offset

    指定节点相对于前一行或前列移动一定量。
    """


class ST_HierarchyAlignment(ST_BaseEnumType):
    """21.4.7.36 ST_HierarchyAlignment (层次结构对齐)

    这种简单类型定义了层次图中子节点及其后代相对于父节点的不同相对位置。
    """

    TL = 'tL'
    """指定子节点和后代节点放置在父节点上方，并且该集合左对齐。
    """

    TR = 'tR'
    """指定子节点和后代节点放置在父节点上方，并且该集合右对齐。
    """

    TCtrCh = 'tCtrCh'
    """指定子节点放置在父节点之上并且该集合居中对齐。
    """

    TCtrDes = 'tCtrDes'
    """指定后代节点放置在父节点上方并且该集合居中对齐。
    """

    BL = 'bL'
    """Bottom Left

    指定子节点和后代节点放置在父节点下方，并且该集合左对齐。
    """

    BR = 'bR'
    """Bottom Right

    指定子节点和后代节点放置在父节点下方，并且该集合右对齐。
    """

    BCtrCh = 'bCtrCh'
    """底部中心子节点 / Bottom Center Child

    指定子节点放置在父节点下方，并且它们与父节点居中对齐。
    """

    BCtrDes = 'bCtrDes'
    """Bottom Center Descendant

    指定后代节点放置在父节点下方，并且它们与父节点居中对齐。
    """

    LT = 'lT'
    """指定子节点和后代节点放置在父节点的左侧，并且该集合顶部对齐。

    """

    LB = 'lB'
    """Left Bottom

    指定子节点和后代节点放置在父节点的左侧，并且该集合底部对齐。
    """

    LCtrCh = 'lCtrCh'
    """Left Center Child

    指定子节点放置在父节点的左侧，并且该集合居中对齐。
    """

    LCtrDes = 'lCtrDes'
    """Left Center Descendant

    指定后代节点放置在父节点的左侧，并且该集合居中对齐
    """

    RT = 'rT'
    """指定子节点和后代节点放置在父节点的右侧，并且该集合顶部对齐。
    """

    RB = 'rB'
    """指定子节点和后代节点放置在父节点的右侧，并且该集合底部对齐。
    """

    RCtrCh = 'rCtrCh'
    """指定子节点放置在父节点的右侧，并且该集合居中对齐。
    """

    RCtrDes = 'rCtrDes'
    """指定后代节点放置在父节点的右侧，并且该集合居中对齐。
    """


ST_FunctionValue = Union[
    int,
    bool,
    ST_Direction,
    ST_HierBranchStyle,
    ST_AnimOneStr,
    ST_AnimLvlStr,
    ST_ResizeHandlesStr,
]
"""21.4.7.34 ST_FunctionValue (函数值)

条件表达式函数值。

这个简单类型是以下类型的联合：

    - ST_AnimLvlStr 简单类型 (§21.4.7.2).
    - ST_AnimOneStr 简单类型 (§21.4.7.3).
    - ST_Direction 简单类型 (§21.4.7.26).
    - ST_HierBranchStyle 简单类型 (§21.4.7.37).
    - ST_ResizeHandlesStr 简单类型 (§21.4.7.54).
    - W3C XML Schema boolean 数据类型.
    - W3C XML Schema int 数据类型.
"""


class ST_VariableType(ST_BaseEnumType):
    """21.4.7.64 ST_VariableType (变量类型)

    条件表达式变量类型。
    """

    none = 'none'
    """Unknown

    未知的变量类型。
    """

    OrgChart = 'orgChart'
    """Organizational Chart Algorithm

    布置组织结构图的算法。
    """

    ChMax = 'chMax'
    """Child Max

    子节点的最大数量。
    """

    ChPref = 'chPref'
    """Child Preference

    首选子节点数量。
    """

    BulEnabled = 'bulEnabled'
    """Bullets Enabled

    指定启用项目符号。
    """

    Dir = 'dir'
    """Direction

    指定图的方向。
    """

    HierBranch = 'hierBranch'
    """Hierarchy Branch

    层次结构分支。
    """

    AnimOne = 'animOne'
    """Animate One

    将 animate 指定为一个。
    """

    AnimLvl = 'animLvl'
    """Animation Level

    指定动画级别
    """

    ResizeHandles = 'resizeHandles'
    """Resize Handles

    指定调整大小手柄。
    """


ST_FunctionArgument = ST_VariableType
"""21.4.7.31 ST_FunctionArgument (函数参数)

条件表达式函数参数。
"""


ST_ParameterVal = Union[
    ST_DiagramHorizontalAlignment,
    ST_VerticalAlignment,
    ST_ChildDirection,
    ST_ChildAlignment,
    ST_SecondaryChildAlignment,
    ST_LinearDirection,
    ST_SecondaryLinearDirection,
    ST_StartingElement,
    ST_BendPoint,
    ST_ConnectorRouting,
    ST_ArrowheadStyle,
    ST_ConnectorDimension,
    ST_RotationPath,
    ST_CenterShapeMapping,
    ST_NodeHorizontalAlignment,
    ST_NodeVerticalAlignment,
    ST_FallbackDimension,
    ST_TextDirection,
    ST_PyramidAccentPosition,
    ST_PyramidAccentTextMargin,
    ST_TextBlockDirection,
    ST_TextAnchorHorizontal,
    ST_TextAnchorVertical,
    ST_DiagramTextAlignment,
    ST_AutoTextRotation,
    ST_GrowDirection,
    ST_FlowDirection,
    ST_ContinueDirection,
    ST_Breakpoint,
    ST_Offset,
    ST_HierarchyAlignment,
    int,
    float,
    bool,
    str,
    ST_ConnectorPoint,
]
"""21.4.7.50 ST_ParameterVal (参数值)

指定图表可以使用的参数类型列表。

这个简单类型是以下类型的联合：

    - ST_ArrowheadStyle 简单类型 (§21.4.7.4).
    - ST_AutoTextRotation 简单类型 (§21.4.7.5).
    - ST_BendPoint 简单类型 (§21.4.7.8).
    - ST_Breakpoint 简单类型 (§21.4.7.11).
    - ...
"""

dml_diagram_namespace = lookup.get_namespace(namespace_dgm)
dml_diagram_namespace[None] = OxmlBaseElement


# dml_chart_drawing_namespace["chartSpace"] = CT_ChartSpace  # 根节点之一
# dml_main_namespace["userShapes"] = cdr_CT_Drawing  # 根节点之一


dml_diagram_namespace['fillClrLst'] = CT_Colors
dml_diagram_namespace['linClrLst'] = CT_Colors
dml_diagram_namespace['effectClrLst'] = CT_Colors
dml_diagram_namespace['txLinClrLst'] = CT_Colors
dml_diagram_namespace['txFillClrLst'] = CT_Colors
dml_diagram_namespace['txEffectClrLst'] = CT_Colors

dml_diagram_namespace['extLst'] = a_CT_OfficeArtExtensionList

dml_diagram_namespace['title'] = CT_CTName
dml_diagram_namespace['desc'] = CT_CTDescription
dml_diagram_namespace['cat'] = CT_CTCategory
dml_diagram_namespace['catLst'] = CT_CTCategories
dml_diagram_namespace['styleLbl'] = CT_CTStyleLabel

dml_diagram_namespace['colorsDef'] = CT_ColorTransform

dml_diagram_namespace['colorsDefHdr'] = CT_ColorTransformHeader
dml_diagram_namespace['colorsDefHdrLst'] = CT_ColorTransformHeaderLst
dml_diagram_namespace['prSet'] = CT_ElemPropSet
dml_diagram_namespace['spPr'] = a_CT_ShapeProperties
dml_diagram_namespace['t'] = a_CT_TextBody

dml_diagram_namespace['pt'] = CT_Pt

dml_diagram_namespace['cxn'] = CT_Cxn

dml_diagram_namespace['ptLst'] = CT_PtList
dml_diagram_namespace['cxnLst'] = CT_CxnList
dml_diagram_namespace['bg'] = a_CT_BackgroundFormatting
dml_diagram_namespace['whole'] = a_CT_WholeE2oFormatting

dml_diagram_namespace['constr'] = CT_Constraint
dml_diagram_namespace['rule'] = CT_NumericRule
dml_diagram_namespace['adj'] = CT_Adj
dml_diagram_namespace['adjLst'] = CT_AdjLst
dml_diagram_namespace['param'] = CT_Parameter

dml_diagram_namespace['alg'] = CT_Algorithm
dml_diagram_namespace['shape'] = CT_Shape

dml_diagram_namespace['presOf'] = CT_PresentationOf
dml_diagram_namespace['constrLst'] = CT_Constraints
dml_diagram_namespace['ruleLst'] = CT_Rules
dml_diagram_namespace['varLst'] = CT_LayoutVariablePropertySet
dml_diagram_namespace['forEach'] = CT_ForEach
dml_diagram_namespace['layoutNode'] = CT_LayoutNode
dml_diagram_namespace['layoutDef'] = CT_DiagramDefinition
dml_diagram_namespace['layoutDefHdr'] = CT_DiagramDefinitionHeader
dml_diagram_namespace['layoutDefHdrLst'] = CT_DiagramDefinitionHeaderLst
dml_diagram_namespace['choose'] = CT_Choose

dml_diagram_namespace['if'] = CT_When
dml_diagram_namespace['else'] = CT_Otherwise

dml_diagram_namespace['dataModel'] = CT_DataModel
dml_diagram_namespace['sampData'] = CT_SampleData

dml_diagram_namespace['styleData'] = CT_SampleData
dml_diagram_namespace['clrData'] = CT_SampleData

dml_diagram_namespace['relIds'] = CT_RelIds
dml_diagram_namespace['presLayoutVars'] = CT_LayoutVariablePropertySet
dml_diagram_namespace['style'] = a_CT_ShapeStyle


dml_diagram_namespace['orgChart'] = CT_OrgChart
dml_diagram_namespace['chMax'] = CT_ChildMax
dml_diagram_namespace['chPref'] = CT_ChildPref
dml_diagram_namespace['bulletEnabled'] = CT_BulletEnabled
dml_diagram_namespace['dir'] = CT_Direction
dml_diagram_namespace['hierBranch'] = CT_HierBranchStyle
dml_diagram_namespace['animOne'] = CT_AnimOne
dml_diagram_namespace['animLvl'] = CT_AnimLvl
dml_diagram_namespace['resizeHandles'] = CT_ResizeHandles


dml_diagram_namespace['cat'] = CT_SDCategory  # 有冲突
dml_diagram_namespace['scene3d'] = a_CT_Scene3D

dml_diagram_namespace['sp3d'] = a_CT_Shape3D
dml_diagram_namespace['txPr'] = CT_TextProps

dml_diagram_namespace['title'] = CT_SDName  # 有冲突
dml_diagram_namespace['desc'] = CT_SDDescription  # 有冲突
dml_diagram_namespace['catLst'] = CT_SDCategories  # 有冲突

dml_diagram_namespace['styleDef'] = CT_StyleDefinition


dml_diagram_namespace['styleDefHdr'] = CT_StyleDefinitionHeader
dml_diagram_namespace['styleDefHdrLst'] = CT_StyleDefinitionHeaderLst
