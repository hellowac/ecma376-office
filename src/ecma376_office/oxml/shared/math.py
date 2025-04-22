"""
对应xsd: shared-math.xsd


<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns="http://schemas.openxmlformats.org/officeDocument/2006/math"
    xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
    xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    xmlns:s="http://schemas.openxmlformats.org/officeDocument/2006/sharedTypes"
    elementFormDefault="qualified" attributeFormDefault="qualified" blockDefault="#all"
    targetNamespace="http://schemas.openxmlformats.org/officeDocument/2006/math">
    <xsd:import namespace="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
        schemaLocation="wml.xsd"/>
    <xsd:import namespace="http://schemas.openxmlformats.org/officeDocument/2006/sharedTypes"
        schemaLocation="shared-commonSimpleTypes.xsd"/>
    <xsd:import namespace="http://www.w3.org/XML/1998/namespace"/>

  ...

</xsd:schema>
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Optional, TypeVar

from ecma376_office.oxml.base import OxmlBaseElement, ST_BaseEnumType, lookup
from ecma376_office.oxml.shared.common_simple_types import ST_OnOff as s_ST_OnOff
from ecma376_office.oxml.shared.common_simple_types import ST_TwipsMeasure as s_ST_TwipsMeasure
from ecma376_office.oxml.shared.common_simple_types import ST_XAlign as s_ST_XAlign
from ecma376_office.oxml.shared.common_simple_types import ST_YAlign as s_ST_YAlign
from ecma376_office.oxml.shared.common_simple_types import to_ST_TwipsMeasure as s_to_ST_TwipsMeasure

if TYPE_CHECKING:
    from ecma376_office.oxml.wml.main import CT_Bookmark as w_CT_Bookmark
    from ecma376_office.oxml.wml.main import CT_CustomXmlRun as w_CT_CustomXmlRun
    from ecma376_office.oxml.wml.main import CT_Hyperlink as w_CT_Hyperlink
    from ecma376_office.oxml.wml.main import CT_Markup as w_CT_Markup
    from ecma376_office.oxml.wml.main import CT_MarkupRange as w_CT_MarkupRange
    from ecma376_office.oxml.wml.main import CT_MoveBookmark as w_CT_MoveBookmark
    from ecma376_office.oxml.wml.main import CT_Perm as w_CT_Perm
    from ecma376_office.oxml.wml.main import CT_PermStart as w_CT_PermStart
    from ecma376_office.oxml.wml.main import CT_ProofErr as w_CT_ProofErr
    from ecma376_office.oxml.wml.main import CT_RPr as w_CT_RPr
    from ecma376_office.oxml.wml.main import CT_RunTrackChange as w_CT_RunTrackChange
    from ecma376_office.oxml.wml.main import CT_SdtRun as w_CT_SdtRun
    from ecma376_office.oxml.wml.main import CT_SimpleField as w_CT_SimpleField
    from ecma376_office.oxml.wml.main import CT_SmartTagRun as w_CT_SmartTagRun
    from ecma376_office.oxml.wml.main import CT_TrackChange as w_CT_TrackChange

namespace_m = 'http://schemas.openxmlformats.org/officeDocument/2006/math'

namespace_w = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

namespace_s = 'http://schemas.openxmlformats.org/officeDocument/2006/sharedTypes'

logger = logging.getLogger(__name__)

ns_map = {
    'm': namespace_m,  # 当前命名空间
    'w': namespace_w,
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

# 还未定义模型


class ST_Integer255(int):
    """
    <xsd:simpleType name="ST_Integer255">
        <xsd:restriction base="xsd:integer">
            <xsd:minInclusive value="1"/>
            <xsd:maxInclusive value="255"/>
        </xsd:restriction>
    </xsd:simpleType>
    """



class CT_Integer255(OxmlBaseElement):
    @property
    def val(self) -> ST_Integer255:
        return ST_Integer255(self.attrib['val'])


class ST_Integer2(int):
    """

    <xsd:simpleType name="ST_Integer2">
        <xsd:restriction base="xsd:integer">
            <xsd:minInclusive value="-2"/>
            <xsd:maxInclusive value="2"/>
        </xsd:restriction>
    </xsd:simpleType>
    """



class CT_Integer2(OxmlBaseElement):
    @property
    def val(self) -> ST_Integer2:
        return ST_Integer2(self.attrib['val'])


class ST_SpacingRule(int):
    """

    <xsd:simpleType name="ST_SpacingRule">
        <xsd:restriction base="xsd:integer">
            <xsd:minInclusive value="0"/>
            <xsd:maxInclusive value="4"/>
        </xsd:restriction>
    </xsd:simpleType>
    """



class CT_SpacingRule(OxmlBaseElement):
    @property
    def val(self) -> ST_SpacingRule:
        return ST_SpacingRule(self.attrib['val'])


class ST_UnSignedInteger(int):
    """

    <xsd:simpleType name="ST_UnSignedInteger">
        <xsd:restriction base="xsd:unsignedInt"/>
    </xsd:simpleType>
    """



class CT_UnSignedInteger(OxmlBaseElement):
    @property
    def val(self) -> ST_UnSignedInteger:
        return ST_UnSignedInteger(self.attrib['val'])


class ST_Char(str):
    """

    <xsd:simpleType name="ST_Char">
        <xsd:restriction base="xsd:string">
            <xsd:maxLength value="1"/>
        </xsd:restriction>
    </xsd:simpleType>
    """



class CT_Char(OxmlBaseElement):
    @property
    def val(self) -> ST_Char:
        return ST_Char(self.attrib['val'])


class CT_OnOff(OxmlBaseElement):
    @property
    def val(self) -> Optional[s_ST_OnOff]:
        _val = self.attrib.get('val')

        if _val is not None:
            return s_ST_OnOff(self.attrib['val'])
        return None


class CT_String(OxmlBaseElement):
    @property
    def val(self) -> Optional[str]:
        _val = self.attrib.get('val')

        if _val is not None:
            return str(self.attrib['val'])
        return None


class CT_XAlign(OxmlBaseElement):
    @property
    def val(self) -> s_ST_XAlign:
        return s_ST_XAlign(self.attrib['val'])


class CT_YAlign(OxmlBaseElement):
    @property
    def val(self) -> s_ST_YAlign:
        return s_ST_YAlign(self.attrib['val'])


class ST_Shp(ST_BaseEnumType):
    Centered = 'centered'
    Match = 'match'


class CT_Shp(OxmlBaseElement):
    @property
    def val(self) -> ST_Shp:
        return ST_Shp(self.attrib['val'])


class ST_FType(ST_BaseEnumType):
    bar = 'bar'
    skw = 'skw'
    lin = 'lin'
    noBar = 'noBar'


class CT_FType(OxmlBaseElement):
    @property
    def val(self) -> ST_FType:
        return ST_FType(self.attrib['val'])


class ST_LimLoc(ST_BaseEnumType):
    undOvr = 'undOvr'
    subSup = 'subSup'


class CT_LimLoc(OxmlBaseElement):
    @property
    def val(self) -> ST_LimLoc:
        return ST_LimLoc(self.attrib['val'])


class ST_TopBot(ST_BaseEnumType):
    top = 'top'
    bot = 'bot'


class CT_TopBot(OxmlBaseElement):
    @property
    def val(self) -> ST_TopBot:
        return ST_TopBot(self.attrib['val'])


class ST_Script(ST_BaseEnumType):
    roman = 'roman'
    script = 'script'
    fraktur = 'fraktur'
    double_struck = 'double-struck'
    sans_serif = 'sans-serif'
    monospace = 'monospace'


class CT_Script(OxmlBaseElement):
    @property
    def val(self) -> Optional[ST_Script]:
        _val = self.attrib.get('val')

        if _val is not None:
            return ST_Script(self.attrib['val'])
        return None


class ST_Style(ST_BaseEnumType):
    p = 'p'
    b = 'b'
    i = 'i'
    bi = 'bi'


class CT_Style(OxmlBaseElement):
    @property
    def val(self) -> Optional[ST_Style]:
        _val = self.attrib.get('val')

        if _val is not None:
            return ST_Style(self.attrib['val'])
        return None


class CT_ManualBreak(OxmlBaseElement):
    @property
    def alnAt(self) -> Optional[ST_Integer255]:
        _val = self.attrib.get('alnAt')

        if _val is not None:
            return ST_Integer255(self.attrib['val'])
        return None


class EG_ScriptStyle(OxmlBaseElement):
    script_style_seq_tags = (
        qn('m:scr'),  # CT_Script
        qn('m:sty'),  # CT_Style
    )

    @property
    def scr(self) -> Optional[CT_Script]:
        return getattr(self, qn('m:scr'), None)

    @property
    def sty(self) -> Optional[CT_Style]:
        return getattr(self, qn('m:sty'), None)


class CT_RPR(EG_ScriptStyle):
    """

    <xsd:complexType name="CT_RPR">
        <xsd:sequence>
            <xsd:element name="lit" minOccurs="0" type="CT_OnOff"/>
            <xsd:choice>
                <xsd:element name="nor" minOccurs="0" type="CT_OnOff"/>
                <xsd:sequence>
                    <xsd:group ref="EG_ScriptStyle"/>
                </xsd:sequence>
            </xsd:choice>
            <xsd:element name="brk" minOccurs="0" type="CT_ManualBreak"/>
            <xsd:element name="aln" minOccurs="0" type="CT_OnOff"/>
        </xsd:sequence>
    </xsd:complexType>
    """

    @property
    def lit(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:lit'), None)

    @property
    def nor(self) -> Optional[CT_OnOff]:
        """

        nor 和 scr, sty 元素只能二选一
        """

        return getattr(self, qn('m:nor'), None)

    @property
    def brk(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:brk'), None)

    @property
    def aln(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:aln'), None)


class CT_Text(OxmlBaseElement):
    """

    <xsd:complexType name="CT_Text">
        <xsd:simpleContent>
            <xsd:extension base="s:ST_String">
                <xsd:attribute ref="xml:space" use="optional"/>
            </xsd:extension>
        </xsd:simpleContent>
    </xsd:complexType>
    """

    @property
    def space(self) -> Optional[str]:
        _val = self.attrib.get(qn('xml:space'))

        if _val is not None:
            return str(_val)
        return None


class CT_R(OxmlBaseElement):
    """

    <xsd:complexType name="CT_R">
        <xsd:sequence>
            <xsd:element name="rPr" type="CT_RPR" minOccurs="0"/>
            <xsd:group ref="w:EG_RPr" minOccurs="0"/>
            <xsd:choice minOccurs="0" maxOccurs="unbounded">
                <xsd:group ref="w:EG_RunInnerContent"/>
                <xsd:element name="t" type="CT_Text" minOccurs="0"/>
            </xsd:choice>
        </xsd:sequence>
    </xsd:complexType>
    """

    @property
    def rPr(self) -> Optional[CT_RPR]:
        return getattr(self, qn('m:rPr'), None)

    @property
    def run_content(self):

        tags = (
            qn('w:rPr'),  # w_CT_RPr
            qn('m:t'),  # CT_Text
        )

        elts: list[w_CT_RPr | CT_Text] = self.choice_and_more(*tags)

        return elts


class CT_CtrlPr(OxmlBaseElement):
    @property
    def run_content(self):
        from ecma376_office.oxml.wml.main import CT_MathCtrlDel as w_CT_MathCtrlDel
        from ecma376_office.oxml.wml.main import CT_MathCtrlIns as w_CT_MathCtrlIns
        from ecma376_office.oxml.wml.main import EG_RPrMath as w_EG_RPrMath

        elts: Optional[w_CT_RPr | w_CT_MathCtrlIns | w_CT_MathCtrlDel] = self.choice_and_more(
            *w_EG_RPrMath.rpr_math_tags
        )  # type: ignore

        return elts


class CT_AccPr(OxmlBaseElement):
    @property
    def chr(self) -> Optional[CT_Char]:
        return getattr(self, qn('m:chr'), None)

    @property
    def ctrlPr(self) -> Optional[CT_CtrlPr]:
        return getattr(self, qn('m:ctrlPr'), None)


class CT_Acc(OxmlBaseElement):
    @property
    def accPr(self) -> Optional[CT_AccPr]:
        return getattr(self, qn('m:accPr'), None)

    @property
    def e(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:e'), None)


class CT_BarPr(OxmlBaseElement):
    @property
    def pos(self) -> Optional[CT_TopBot]:
        return getattr(self, qn('m:pos'), None)

    @property
    def ctrlPr(self) -> Optional[CT_CtrlPr]:
        return getattr(self, qn('m:ctrlPr'), None)


class CT_Bar(OxmlBaseElement):
    @property
    def barPr(self) -> Optional[CT_BarPr]:
        return getattr(self, qn('m:barPr'), None)

    @property
    def e(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:e'), None)


class CT_BoxPr(OxmlBaseElement):
    @property
    def opEmu(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:opEmu'), None)

    @property
    def noBreak(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:noBreak'), None)

    @property
    def diff(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:diff'), None)

    @property
    def brk(self) -> Optional[CT_ManualBreak]:
        return getattr(self, qn('m:brk'), None)

    @property
    def aln(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:aln'), None)

    @property
    def ctrlPr(self) -> Optional[CT_CtrlPr]:
        return getattr(self, qn('m:ctrlPr'), None)


class CT_Box(OxmlBaseElement):
    @property
    def boxPr(self) -> Optional[CT_BoxPr]:
        return getattr(self, qn('m:barPr'), None)

    @property
    def e(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:e'), None)


class CT_BorderBoxPr(OxmlBaseElement):
    @property
    def hideTop(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:hideTop'), None)

    @property
    def hideBot(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:hideBot'), None)

    @property
    def hideLeft(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:hideLeft'), None)

    @property
    def hideRight(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:hideRight'), None)

    @property
    def strikeH(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:strikeH'), None)

    @property
    def strikeV(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:strikeV'), None)

    @property
    def strikeBLTR(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:strikeBLTR'), None)

    @property
    def strikeTLBR(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:strikeTLBR'), None)

    @property
    def ctrlPr(self) -> Optional[CT_CtrlPr]:
        return getattr(self, qn('m:ctrlPr'), None)


class CT_BorderBox(OxmlBaseElement):
    @property
    def borderBoxPr(self) -> Optional[CT_BorderBoxPr]:
        return getattr(self, qn('m:borderBoxPr'), None)

    @property
    def e(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:e'), None)


class CT_DPr(OxmlBaseElement):
    @property
    def begChr(self) -> Optional[CT_Char]:
        return getattr(self, qn('m:begChr'), None)

    @property
    def sepChr(self) -> Optional[CT_Char]:
        return getattr(self, qn('m:sepChr'), None)

    @property
    def endChr(self) -> Optional[CT_Char]:
        return getattr(self, qn('m:endChr'), None)

    @property
    def grow(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:grow'), None)

    @property
    def shp(self) -> Optional[CT_Shp]:
        return getattr(self, qn('m:shp'), None)

    @property
    def ctrlPr(self) -> Optional[CT_CtrlPr]:
        return getattr(self, qn('m:ctrlPr'), None)


class CT_D(OxmlBaseElement):
    @property
    def dPr(self) -> Optional[CT_DPr]:
        return getattr(self, qn('m:dPr'), None)

    @property
    def e(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:e'), None)


class CT_EqArrPr(OxmlBaseElement):
    @property
    def baseJc(self) -> Optional[CT_YAlign]:
        return getattr(self, qn('m:baseJc'), None)

    @property
    def maxDist(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:maxDist'), None)

    @property
    def objDist(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:objDist'), None)

    @property
    def rSpRule(self) -> Optional[CT_SpacingRule]:
        return getattr(self, qn('m:rSpRule'), None)

    @property
    def rSp(self) -> Optional[CT_UnSignedInteger]:
        return getattr(self, qn('m:rSp'), None)

    @property
    def ctrlPr(self) -> Optional[CT_CtrlPr]:
        return getattr(self, qn('m:ctrlPr'), None)


class CT_EqArr(OxmlBaseElement):
    @property
    def eqArrPr(self) -> Optional[CT_EqArrPr]:
        return getattr(self, qn('m:eqArrPr'), None)

    @property
    def e(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:e'), None)


class CT_FPr(OxmlBaseElement):
    @property
    def type(self) -> Optional[CT_FType]:
        return getattr(self, qn('m:type'), None)

    @property
    def ctrlPr(self) -> Optional[CT_CtrlPr]:
        return getattr(self, qn('m:ctrlPr'), None)


class CT_F(OxmlBaseElement):
    @property
    def fPr(self) -> Optional[CT_FPr]:
        return getattr(self, qn('m:fPr'), None)

    @property
    def num(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:num'), None)

    @property
    def den(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:den'), None)


class CT_FuncPr(OxmlBaseElement):
    @property
    def ctrlPr(self) -> Optional[CT_CtrlPr]:
        return getattr(self, qn('m:ctrlPr'), None)


class CT_Func(OxmlBaseElement):
    @property
    def funcPr(self) -> Optional[CT_FuncPr]:
        return getattr(self, qn('m:funcPr'), None)

    @property
    def fName(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:fName'), None)

    @property
    def e(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:e'), None)


class CT_GroupChrPr(OxmlBaseElement):
    @property
    def chr(self) -> Optional[CT_Char]:
        return getattr(self, qn('m:chr'), None)

    @property
    def pos(self) -> Optional[CT_TopBot]:
        return getattr(self, qn('m:pos'), None)

    @property
    def vertJc(self) -> Optional[CT_TopBot]:
        return getattr(self, qn('m:vertJc'), None)

    @property
    def ctrlPr(self) -> Optional[CT_CtrlPr]:
        return getattr(self, qn('m:ctrlPr'), None)


class CT_GroupChr(OxmlBaseElement):
    @property
    def groupChrPr(self) -> Optional[CT_GroupChrPr]:
        return getattr(self, qn('m:fungroupChrPrcPr'), None)

    @property
    def e(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:e'), None)


class CT_LimLowPr(OxmlBaseElement):
    @property
    def ctrlPr(self) -> Optional[CT_CtrlPr]:
        return getattr(self, qn('m:ctrlPr'), None)


class CT_LimLow(OxmlBaseElement):
    @property
    def limLowPr(self) -> Optional[CT_LimLowPr]:
        return getattr(self, qn('m:limLowPr'), None)

    @property
    def e(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:e'), None)

    @property
    def lim(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:lim'), None)


class CT_LimUppPr(OxmlBaseElement):
    @property
    def ctrlPr(self) -> Optional[CT_CtrlPr]:
        return getattr(self, qn('m:ctrlPr'), None)


class CT_LimUpp(OxmlBaseElement):
    @property
    def limUppPr(self) -> Optional[CT_LimUppPr]:
        return getattr(self, qn('m:limLowPr'), None)

    @property
    def e(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:e'), None)

    @property
    def lim(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:lim'), None)


class CT_MCPr(OxmlBaseElement):
    @property
    def count(self) -> Optional[CT_Integer255]:
        return getattr(self, qn('m:count'), None)

    @property
    def mcJc(self) -> Optional[CT_XAlign]:
        return getattr(self, qn('m:mcJc'), None)


class CT_MC(OxmlBaseElement):
    @property
    def mcPr(self) -> Optional[CT_MCPr]:
        return getattr(self, qn('m:mcPr'), None)


class CT_MCS(OxmlBaseElement):
    @property
    def mc(self) -> Optional[CT_MC]:
        return getattr(self, qn('m:mc'), None)


class CT_MPr(OxmlBaseElement):
    @property
    def baseJc(self) -> Optional[CT_YAlign]:
        return getattr(self, qn('m:baseJc'), None)

    @property
    def plcHide(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:plcHide'), None)

    @property
    def rSpRule(self) -> Optional[CT_SpacingRule]:
        return getattr(self, qn('m:rSpRule'), None)

    @property
    def cGpRule(self) -> Optional[CT_SpacingRule]:
        return getattr(self, qn('m:cGpRule'), None)

    @property
    def rSp(self) -> Optional[CT_UnSignedInteger]:
        return getattr(self, qn('m:rSp'), None)

    @property
    def cSp(self) -> Optional[CT_UnSignedInteger]:
        return getattr(self, qn('m:cSp'), None)

    @property
    def cGp(self) -> Optional[CT_UnSignedInteger]:
        return getattr(self, qn('m:cGp'), None)

    @property
    def mcs(self) -> Optional[CT_MCS]:
        return getattr(self, qn('m:mcs'), None)

    @property
    def ctrlPr(self) -> Optional[CT_CtrlPr]:
        return getattr(self, qn('m:ctrlPr'), None)


class CT_MR(OxmlBaseElement):
    @property
    def e(self) -> list[CT_OMathArg]:
        return self.findall(qn('m:e'))  # type: ignore


class CT_M(OxmlBaseElement):
    @property
    def mPr(self) -> Optional[CT_MPr]:
        return getattr(self, qn('m:mPr'), None)

    @property
    def mr(self) -> Optional[CT_MR]:
        return getattr(self, qn('m:mr'), None)


class CT_NaryPr(OxmlBaseElement):
    @property
    def chr(self) -> Optional[CT_Char]:
        return getattr(self, qn('m:chr'), None)

    @property
    def limLoc(self) -> Optional[CT_LimLoc]:
        return getattr(self, qn('m:limLoc'), None)

    @property
    def grow(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:grow'), None)

    @property
    def subHide(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:subHide'), None)

    @property
    def supHide(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:supHide'), None)

    @property
    def ctrlPr(self) -> Optional[CT_CtrlPr]:
        return getattr(self, qn('m:ctrlPr'), None)


class CT_Nary(OxmlBaseElement):
    @property
    def naryPr(self) -> Optional[CT_NaryPr]:
        return getattr(self, qn('m:naryPr'), None)

    @property
    def sub(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:sub'), None)

    @property
    def sup(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:sup'), None)

    @property
    def e(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:e'), None)


class CT_PhantPr(OxmlBaseElement):
    @property
    def show(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:show'), None)

    @property
    def zeroWid(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:zeroWid'), None)

    @property
    def zeroAsc(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:zeroAsc'), None)

    @property
    def zeroDesc(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:zeroDesc'), None)

    @property
    def transp(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:transp'), None)

    @property
    def ctrlPr(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:ctrlPr'), None)


class CT_Phant(OxmlBaseElement):
    @property
    def phantPr(self) -> Optional[CT_PhantPr]:
        return getattr(self, qn('m:phantPr'), None)

    @property
    def e(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:e'), None)


class CT_RadPr(OxmlBaseElement):
    @property
    def degHide(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:degHide'), None)

    @property
    def ctrlPr(self) -> Optional[CT_CtrlPr]:
        return getattr(self, qn('m:ctrlPr'), None)


class CT_Rad(OxmlBaseElement):
    @property
    def radPr(self) -> Optional[CT_RadPr]:
        return getattr(self, qn('m:radPr'), None)

    @property
    def deg(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:deg'), None)

    @property
    def e(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:e'), None)


class CT_SPrePr(OxmlBaseElement):
    @property
    def ctrlPr(self) -> Optional[CT_CtrlPr]:
        return getattr(self, qn('m:ctrlPr'), None)


class CT_SPre(OxmlBaseElement):
    @property
    def sPrePr(self) -> Optional[CT_SPrePr]:
        return getattr(self, qn('m:sPrePr'), None)

    @property
    def sub(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:sub'), None)

    @property
    def sup(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:sup'), None)

    @property
    def e(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:e'), None)


class CT_SSubPr(OxmlBaseElement):
    @property
    def ctrlPr(self) -> Optional[CT_CtrlPr]:
        return getattr(self, qn('m:ctrlPr'), None)


class CT_SSub(OxmlBaseElement):
    @property
    def sSubPr(self) -> Optional[CT_SSubPr]:
        return getattr(self, qn('m:sSubPr'), None)

    @property
    def e(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:e'), None)

    @property
    def sub(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:sub'), None)


class CT_SSubSupPr(OxmlBaseElement):
    @property
    def alnScr(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:alnScr'), None)

    @property
    def ctrlPr(self) -> Optional[CT_CtrlPr]:
        return getattr(self, qn('m:ctrlPr'), None)


class CT_SSubSup(OxmlBaseElement):
    @property
    def sSubSupPr(self) -> Optional[CT_SSubSupPr]:
        return getattr(self, qn('m:sSubSupPr'), None)

    @property
    def e(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:e'), None)

    @property
    def sub(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:sub'), None)

    @property
    def sup(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:sup'), None)


class CT_SSupPr(OxmlBaseElement):
    @property
    def ctrlPr(self) -> Optional[CT_CtrlPr]:
        return getattr(self, qn('m:ctrlPr'), None)


class CT_SSup(OxmlBaseElement):
    @property
    def sSupPr(self) -> Optional[CT_SSupPr]:
        return getattr(self, qn('m:sSupPr'), None)

    @property
    def e(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:e'), None)

    @property
    def sup(self) -> Optional[CT_OMathArg]:
        return getattr(self, qn('m:sup'), None)


class EG_OMathMathElements(OxmlBaseElement):
    # Union[CT_LimLow, CT_R, CT_Bar, CT_Nary, CT_EqArr, CT_Phant, CT_D, CT_SSup, CT_SSubSup, CT_Acc, CT_LimUpp, CT_Rad, CT_BorderBox, CT_GroupChr, CT_Box, CT_SSub, CT_M, CT_SPre, CT_Func, CT_F]
    omath_elements_choice_tags = (
        qn('m:acc'),  # CT_Acc
        qn('m:bar'),  # CT_Bar
        qn('m:box'),  # CT_Box
        qn('m:borderBox'),  # CT_BorderBox
        qn('m:d'),  # CT_D
        qn('m:eqArr'),  # CT_EqArr
        qn('m:f'),  # CT_F
        qn('m:func'),  # CT_Func
        qn('m:groupChr'),  # CT_GroupChr
        qn('m:limLow'),  # CT_LimLow
        qn('m:limUpp'),  # CT_LimUpp
        qn('m:m'),  # CT_M
        qn('m:nary'),  # CT_Nary
        qn('m:phant'),  # CT_Phant
        qn('m:rad'),  # CT_Rad
        qn('m:sPre'),  # CT_SPre
        qn('m:sSub'),  # CT_SSub
        qn('m:sSubSup'),  # CT_SSubSup
        qn('m:sSup'),  # CT_SSup
        qn('m:r'),  # CT_R
    )


class EG_OMathElements(OxmlBaseElement):
    """

    <xsd:group name="EG_PContentMath">
        <xsd:choice>
            <xsd:group ref="EG_PContentBase" minOccurs="0" maxOccurs="unbounded"/>
            <xsd:group ref="EG_ContentRunContentBase" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:choice>
    </xsd:group>
    """

    # from ..wml.main import EG_PContentMath

    # Union[CT_LimLow, CT_R, CT_Bar, CT_Nary, CT_EqArr, CT_Phant, CT_D, CT_SSup, CT_SSubSup, CT_Acc, CT_LimUpp, CT_Rad, CT_BorderBox, CT_GroupChr, CT_Box, CT_SSub, CT_M, CT_SPre, CT_Func, CT_F, w_CT_Markup, w_CT_RunTrackChange, w_CT_SimpleField, w_CT_Perm, w_CT_SmartTagRun, w_CT_Bookmark, w_CT_PermStart, w_CT_SdtRun, w_CT_MoveBookmark, w_CT_ProofErr, w_CT_CustomXmlRun, w_CT_Hyperlink, w_CT_TrackChange, w_CT_MarkupRange, CT_OMathPara, CT_OMath]
    omath_elements_choice_tags = (
        EG_OMathMathElements.omath_elements_choice_tags
        + (
            qn('w:customXml'),  # w_CT_CustomXmlRun
            qn('w:fldSimple'),  # w_CT_SimpleField
            qn('w:hyperlink'),  # w_CT_Hyperlink
        )
        + (
            qn('w:smartTag'),  # w_CT_SmartTagRun
            qn('w:sdt'),  # w_CT_SdtRun
        )
        + (
            qn('w:proofErr'),  # w_CT_ProofErr
            qn('w:permStart'),  # w_CT_PermStart
            qn('w:permEnd'),  # w_CT_Perm
            qn('w:proofErr'),  # w_CT_ProofErr
        )
        + (
            qn('w:bookmarkStart'),  # w_CT_Bookmark
            qn('w:bookmarkEnd'),  # w_CT_MarkupRange
            qn('w:moveFromRangeStart'),  # w_CT_MoveBookmark
            qn('w:moveFromRangeEnd'),  # w_CT_MarkupRange
            qn('w:moveToRangeStart'),  # w_CT_MoveBookmark
            qn('w:moveToRangeEnd'),  # w_CT_MarkupRange
            qn('w:commentRangeStart'),  # w_CT_MarkupRange
            qn('w:commentRangeEnd'),  # w_CT_MarkupRange
            qn('w:customXmlInsRangeStart'),  # w_CT_TrackChange
            qn('w:customXmlInsRangeEnd'),  # w_CT_Markup
            qn('w:customXmlDelRangeStart'),  # w_CT_TrackChange
            qn('w:customXmlDelRangeEnd'),  # w_CT_Markup
            qn('w:customXmlMoveFromRangeStart'),  # w_CT_TrackChange
            qn('w:customXmlMoveFromRangeEnd'),  # w_CT_Markup
            qn('w:customXmlMoveToRangeStart'),  # w_CT_TrackChange
            qn('w:customXmlMoveToRangeEnd'),  # w_CT_Markup
        )
        + (
            qn('w:ins'),  # w_CT_RunTrackChange
            qn('w:del'),  # w_CT_RunTrackChange
            qn('w:moveFrom'),  # w_CT_RunTrackChange
            qn('w:moveTo'),  # w_CT_RunTrackChange
        )
        + (
            qn('m:oMathPara'),  # CT_OMathPara
            qn('m:oMath'),  # CT_OMath
        )
    )


"""
,"""


class CT_OMathArgPr(OxmlBaseElement):
    @property
    def argSz(self) -> Optional[CT_Integer2]:
        return getattr(self, qn('m:argSz'), None)


class CT_OMathArg(OxmlBaseElement):
    @property
    def argPr(self) -> Optional[CT_OMathArgPr]:
        return getattr(self, qn('m:argPr'), None)

    @property
    def omath_elts(self) -> list[Any]:
        return self.choice_and_more(*EG_OMathElements.omath_elements_choice_tags)

    @property
    def ctrlPr(self) -> Optional[CT_CtrlPr]:
        return getattr(self, qn('m:ctrlPr'), None)


class ST_Jc(ST_BaseEnumType):
    left = 'left'
    right = 'right'
    center = 'center'
    centerGroup = 'centerGroup'


class CT_OMathJc(OxmlBaseElement):
    @property
    def val(self) -> Optional[ST_Jc]:
        _val = self.attrib.get('val')

        if _val is not None:
            return ST_Jc(str(_val))
        return None


class CT_OMathParaPr(OxmlBaseElement):
    @property
    def jc(self) -> Optional[CT_OMathJc]:
        return getattr(self, qn('m:jc'), None)


class CT_TwipsMeasure(OxmlBaseElement):
    @property
    def val(self) -> s_ST_TwipsMeasure:
        return s_to_ST_TwipsMeasure(str(self.attrib['val']))


class ST_BreakBin(ST_BaseEnumType):
    before = 'before'
    after = 'after'
    repeat = 'repeat'


class CT_BreakBin(OxmlBaseElement):
    @property
    def val(self) -> Optional[ST_BreakBin]:
        _val = self.attrib.get('val')

        if _val is not None:
            return ST_BreakBin(str(_val))
        return None


class ST_BreakBinSub(ST_BaseEnumType):
    jj = '--'
    ja = '-+'
    aj = '+-'


class CT_BreakBinSub(OxmlBaseElement):
    @property
    def val(self) -> Optional[ST_BreakBinSub]:
        _val = self.attrib.get('val')

        if _val is not None:
            return ST_BreakBinSub(str(_val))
        return None


class CT_MathPr(OxmlBaseElement):
    @property
    def mathFont(self) -> Optional[CT_String]:
        return getattr(self, qn('m:mathFont'), None)

    @property
    def brkBin(self) -> Optional[CT_BreakBin]:
        return getattr(self, qn('m:brkBin'), None)

    @property
    def brkBinSub(self) -> Optional[CT_BreakBinSub]:
        return getattr(self, qn('m:brkBinSub'), None)

    @property
    def smallFrac(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:smallFrac'), None)

    @property
    def dispDef(self) -> Optional[CT_OnOff]:
        return getattr(self, qn('m:dispDef'), None)

    @property
    def lMargin(self) -> Optional[CT_TwipsMeasure]:
        return getattr(self, qn('m:lMargin'), None)

    @property
    def rMargin(self) -> Optional[CT_TwipsMeasure]:
        return getattr(self, qn('m:rMargin'), None)

    @property
    def defJc(self) -> Optional[CT_OMathJc]:  # noqa: N802
        return getattr(self, qn('m:defJc'), None)

    @property
    def preSp(self) -> Optional[CT_TwipsMeasure]:
        return getattr(self, qn('m:preSp'), None)

    @property
    def postSp(self) -> Optional[CT_TwipsMeasure]:
        return getattr(self, qn('m:postSp'), None)

    @property
    def interSp(self) -> Optional[CT_TwipsMeasure]:
        return getattr(self, qn('m:interSp'), None)

    @property
    def intraSp(self) -> Optional[CT_TwipsMeasure]:
        return getattr(self, qn('m:intraSp'), None)

    @property
    def intLim(self) -> Optional[CT_LimLoc]:
        return getattr(self, qn('m:intLim'), None)

    @property
    def naryLim(self) -> Optional[CT_LimLoc]:
        return getattr(self, qn('m:naryLim'), None)

    @property
    def wrap(self) -> Optional[CT_TwipsMeasure | CT_OnOff]:
        tags = (
            qn('m:wrapIndent'),  # CT_TwipsMeasure
            qn('m:wrapRight'),  # CT_OnOff
        )
        return self.choice_one_child(*tags)  # type: ignore


class CT_OMathPara(OxmlBaseElement):
    @property
    def oMathParaPr(self) -> Optional[CT_OMathParaPr]:
        return getattr(self, qn('m:oMathParaPr'), None)

    @property
    def oMath(self) -> list[CT_OMath]:
        return self.findall(qn('m:oMath'))  # type: ignore


class CT_OMath(OxmlBaseElement):
    @property
    def omath_elts(self):


        elts: list[
            CT_LimLow | CT_R | CT_Bar | CT_Nary | CT_EqArr | CT_Phant | CT_D | CT_SSup | CT_SSubSup | CT_Acc | CT_LimUpp | CT_Rad | CT_BorderBox | CT_GroupChr | CT_Box | CT_SSub | CT_M | CT_SPre | CT_Func | CT_F | w_CT_Markup | w_CT_RunTrackChange | w_CT_SimpleField | w_CT_Perm | w_CT_SmartTagRun | w_CT_Bookmark | w_CT_PermStart | w_CT_SdtRun | w_CT_MoveBookmark | w_CT_ProofErr | w_CT_CustomXmlRun | w_CT_Hyperlink | w_CT_TrackChange | w_CT_MarkupRange | CT_OMathPara | CT_OMath
        ] = self.choice_and_more(*EG_OMathElements.omath_elements_choice_tags)  # type: ignore

        return elts


shared_math_namespace = lookup.get_namespace(namespace_m)
shared_math_namespace[None] = OxmlBaseElement
shared_math_namespace['oMath'] = CT_OMath
shared_math_namespace['oMathPara'] = CT_OMathPara
shared_math_namespace['oMathParaPr'] = CT_OMathParaPr
shared_math_namespace['mathPr'] = CT_MathPr
shared_math_namespace['naryLim'] = CT_LimLoc
shared_math_namespace['intLim'] = CT_LimLoc
shared_math_namespace['wrapRight'] = CT_OnOff
shared_math_namespace['wrapIndent'] = CT_TwipsMeasure
shared_math_namespace['intraSp'] = CT_TwipsMeasure
shared_math_namespace['interSp'] = CT_TwipsMeasure
shared_math_namespace['postSp'] = CT_TwipsMeasure
shared_math_namespace['preSp'] = CT_TwipsMeasure
shared_math_namespace['jc'] = CT_OMathJc
shared_math_namespace['defJc'] = CT_OMathJc
shared_math_namespace['rMargin'] = CT_TwipsMeasure
shared_math_namespace['lMargin'] = CT_TwipsMeasure
shared_math_namespace['dispDef'] = CT_OnOff
shared_math_namespace['smallFrac'] = CT_OnOff
shared_math_namespace['brkBin'] = CT_BreakBin
shared_math_namespace['brkBinSub'] = CT_BreakBinSub
shared_math_namespace['mathFont'] = CT_String
shared_math_namespace['ctrlPr'] = CT_CtrlPr
shared_math_namespace['argPr'] = CT_OMathArgPr
shared_math_namespace['argSz'] = CT_Integer2
shared_math_namespace['r'] = CT_R
shared_math_namespace['sSup'] = CT_SSup
shared_math_namespace['acc'] = CT_Acc
shared_math_namespace['bar'] = CT_Bar
shared_math_namespace['box'] = CT_Box
shared_math_namespace['borderBox'] = CT_BorderBox
shared_math_namespace['d'] = CT_D
shared_math_namespace['eqArr'] = CT_EqArr
shared_math_namespace['f'] = CT_F
shared_math_namespace['func'] = CT_Func
shared_math_namespace['groupChr'] = CT_GroupChr
shared_math_namespace['limLow'] = CT_LimLow
shared_math_namespace['limUpp'] = CT_LimUpp
shared_math_namespace['m'] = CT_M
shared_math_namespace['nary'] = CT_Nary
shared_math_namespace['phant'] = CT_Phant
shared_math_namespace['rad'] = CT_Rad
shared_math_namespace['sPre'] = CT_SPre
shared_math_namespace['sSub'] = CT_SSub
shared_math_namespace['sSubSup'] = CT_SSubSup
shared_math_namespace['sSupPr'] = CT_SSupPr
shared_math_namespace['num'] = CT_OMathArg
shared_math_namespace['den'] = CT_OMathArg
shared_math_namespace['fName'] = CT_OMathArg
shared_math_namespace['lim'] = CT_OMathArg
shared_math_namespace['sub'] = CT_OMathArg
shared_math_namespace['sup'] = CT_OMathArg
shared_math_namespace['deg'] = CT_OMathArg
shared_math_namespace['e'] = CT_OMathArg
shared_math_namespace['lit'] = CT_OnOff
shared_math_namespace['alnScr'] = CT_OnOff
shared_math_namespace['degHide'] = CT_OnOff
shared_math_namespace['show'] = CT_OnOff
shared_math_namespace['zeroWid'] = CT_OnOff
shared_math_namespace['zeroAsc'] = CT_OnOff
shared_math_namespace['zeroDesc'] = CT_OnOff
shared_math_namespace['transp'] = CT_OnOff
shared_math_namespace['grow'] = CT_OnOff
shared_math_namespace['subHide'] = CT_OnOff
shared_math_namespace['supHide'] = CT_OnOff
shared_math_namespace['plcHide'] = CT_OnOff
shared_math_namespace['maxDist'] = CT_OnOff
shared_math_namespace['objDist'] = CT_OnOff
shared_math_namespace['hideTop'] = CT_OnOff
shared_math_namespace['hideBot'] = CT_OnOff
shared_math_namespace['hideLeft'] = CT_OnOff
shared_math_namespace['hideRight'] = CT_OnOff
shared_math_namespace['strikeH'] = CT_OnOff
shared_math_namespace['strikeV'] = CT_OnOff
shared_math_namespace['strikeBLTR'] = CT_OnOff
shared_math_namespace['strikeTLBR'] = CT_OnOff
shared_math_namespace['opEmu'] = CT_OnOff
shared_math_namespace['noBreak'] = CT_OnOff
shared_math_namespace['diff'] = CT_OnOff
shared_math_namespace['aln'] = CT_OnOff
shared_math_namespace['scr'] = CT_Script
shared_math_namespace['sty'] = CT_Style
shared_math_namespace['sSubSupPr'] = CT_SSubSupPr
shared_math_namespace['sSubPr'] = CT_SSubPr
shared_math_namespace['sPrePr'] = CT_SPrePr
shared_math_namespace['radPr'] = CT_RadPr
shared_math_namespace['phantPr'] = CT_PhantPr
shared_math_namespace['naryPr'] = CT_NaryPr
shared_math_namespace['limLoc'] = CT_LimLoc
shared_math_namespace['mr'] = CT_MR
shared_math_namespace['mPr'] = CT_MPr
shared_math_namespace['groupChrPr'] = CT_GroupChrPr
shared_math_namespace['cGpRule'] = CT_SpacingRule
shared_math_namespace['cSp'] = CT_UnSignedInteger
shared_math_namespace['cGp'] = CT_UnSignedInteger
shared_math_namespace['count'] = CT_Integer255
shared_math_namespace['limUppPr'] = CT_LimUppPr
shared_math_namespace['mc'] = CT_MC
shared_math_namespace['mcJc'] = CT_XAlign
shared_math_namespace['mcs'] = CT_MCS
shared_math_namespace['mcPr'] = CT_MCPr
shared_math_namespace['limLowPr'] = CT_LimLowPr
shared_math_namespace['vertJc'] = CT_TopBot
shared_math_namespace['pos'] = CT_TopBot
shared_math_namespace['funcPr'] = CT_FuncPr
shared_math_namespace['fPr'] = CT_FPr
shared_math_namespace['type'] = CT_FType
shared_math_namespace['eqArrPr'] = CT_EqArrPr
shared_math_namespace['baseJc'] = CT_YAlign
shared_math_namespace['rSpRule'] = CT_SpacingRule
shared_math_namespace['rSp'] = CT_UnSignedInteger
shared_math_namespace['dPr'] = CT_DPr
shared_math_namespace['borderBoxPr'] = CT_BorderBoxPr
shared_math_namespace['boxPr'] = CT_BoxPr
shared_math_namespace['brk'] = CT_ManualBreak
shared_math_namespace['barPr'] = CT_BarPr
shared_math_namespace['chr'] = CT_Char
shared_math_namespace['begChr'] = CT_Char
shared_math_namespace['sepChr'] = CT_Char
shared_math_namespace['endChr'] = CT_Char
shared_math_namespace['accPr'] = CT_AccPr
shared_math_namespace['rPr'] = CT_RPR
shared_math_namespace['shp'] = CT_Shp
shared_math_namespace['t'] = CT_Text
