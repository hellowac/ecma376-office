"""
pptx 文档xsd转换成python类对象的模块

对应xsd: dml-main.xsd

前缀: ''

命名空间: http://purl.oclc.org/ooxml/presentationml/main

相关命名空间:

    p: http://purl.oclc.org/ooxml/presentationml/main

    a: http://purl.oclc.org/ooxml/drawingml/main

    r: http://purl.oclc.org/ooxml/officeDocument/relationships

    s: http://purl.oclc.org/ooxml/officeDocument/sharedTypes

对应Reference: 21.1 DrawingML - Main
"""

from __future__ import annotations

import logging
from typing import AnyStr, Optional, Self, TypeVar, Union

from ecma376_office.oxml import utils
from ecma376_office.oxml.base import OxmlBaseElement, ST_BaseEnumType, ST_BaseType, lookup
from ecma376_office.oxml.dml.main import CT_AnimationElementChoice as a_CT_AnimationElementChoice
from ecma376_office.oxml.dml.main import (
    CT_AnimationGraphicalObjectBuildProperties as a_CT_AnimationGraphicalObjectBuildProperties,
)
from ecma376_office.oxml.dml.main import CT_AudioCD as a_CT_AudioCD
from ecma376_office.oxml.dml.main import CT_AudioFile as a_CT_AudioFile
from ecma376_office.oxml.dml.main import CT_BlipFillProperties as a_CT_BlipFillProperties
from ecma376_office.oxml.dml.main import CT_Color as a_CT_Color
from ecma376_office.oxml.dml.main import CT_ColorMapping as a_CT_ColorMapping
from ecma376_office.oxml.dml.main import CT_ColorMappingOverride as a_CT_ColorMappingOverride
from ecma376_office.oxml.dml.main import CT_ColorMRU as a_CT_ColorMRU
from ecma376_office.oxml.dml.main import CT_EffectContainer as a_CT_EffectContainer
from ecma376_office.oxml.dml.main import CT_EffectList as a_CT_EffectList
from ecma376_office.oxml.dml.main import CT_EmbeddedWAVAudioFile as a_CT_EmbeddedWAVAudioFile
from ecma376_office.oxml.dml.main import CT_GradientFillProperties as a_CT_GradientFillProperties
from ecma376_office.oxml.dml.main import CT_GraphicalObject as a_CT_GraphicalObject
from ecma376_office.oxml.dml.main import CT_GroupFillProperties as a_CT_GroupFillProperties
from ecma376_office.oxml.dml.main import CT_GroupShapeProperties as a_CT_GroupShapeProperties
from ecma376_office.oxml.dml.main import CT_NoFillProperties as a_CT_NoFillProperties
from ecma376_office.oxml.dml.main import CT_NonVisualConnectorProperties as a_CT_NonVisualConnectorProperties
from ecma376_office.oxml.dml.main import CT_NonVisualDrawingProps as a_CT_NonVisualDrawingProps
from ecma376_office.oxml.dml.main import CT_NonVisualDrawingShapeProps as a_CT_NonVisualDrawingShapeProps
from ecma376_office.oxml.dml.main import CT_NonVisualGraphicFrameProperties as a_CT_NonVisualGraphicFrameProperties
from ecma376_office.oxml.dml.main import CT_NonVisualGroupDrawingShapeProps as a_CT_NonVisualGroupDrawingShapeProps
from ecma376_office.oxml.dml.main import CT_NonVisualPictureProperties as a_CT_NonVisualPictureProperties
from ecma376_office.oxml.dml.main import CT_PatternFillProperties as a_CT_PatternFillProperties
from ecma376_office.oxml.dml.main import CT_Point2D as a_CT_Point2D
from ecma376_office.oxml.dml.main import CT_PositiveSize2D as a_CT_PositiveSize2D
from ecma376_office.oxml.dml.main import CT_QuickTimeFile as a_CT_QuickTimeFile
from ecma376_office.oxml.dml.main import CT_Scale2D as a_CT_Scale2D
from ecma376_office.oxml.dml.main import CT_ShapeProperties as a_CT_ShapeProperties
from ecma376_office.oxml.dml.main import CT_ShapeStyle as a_CT_ShapeStyle
from ecma376_office.oxml.dml.main import CT_SolidColorFillProperties as a_CT_SolidColorFillProperties
from ecma376_office.oxml.dml.main import CT_StyleMatrixReference as a_CT_StyleMatrixReference
from ecma376_office.oxml.dml.main import CT_TextBody as a_CT_TextBody
from ecma376_office.oxml.dml.main import CT_TextFont as a_CT_TextFont
from ecma376_office.oxml.dml.main import CT_TextListStyle as a_CT_TextListStyle
from ecma376_office.oxml.dml.main import CT_Transform2D as a_CT_Transform2D
from ecma376_office.oxml.dml.main import CT_VideoFile as a_CT_VideoFile
from ecma376_office.oxml.dml.main import EG_EffectProperties as a_EG_EffectProperties
from ecma376_office.oxml.dml.main import EG_FillProperties as a_EG_FillProperties
from ecma376_office.oxml.dml.main import EG_Media as a_EG_media
from ecma376_office.oxml.dml.main import ST_Angle as a_ST_Angle
from ecma376_office.oxml.dml.main import ST_BlackWhiteMode as a_ST_BlackWhiteMode
from ecma376_office.oxml.dml.main import ST_Coordinate32 as a_ST_Coordinate32
from ecma376_office.oxml.dml.main import ST_DrawingElementId as a_ST_DrawingElementId
from ecma376_office.oxml.dml.main import ST_FixedPercentage as a_ST_FixedPercentage
from ecma376_office.oxml.dml.main import ST_Percentage as a_ST_Percentage
from ecma376_office.oxml.dml.main import ST_PositiveCoordinate32 as a_ST_PositiveCoordinate32
from ecma376_office.oxml.dml.main import ST_PositiveFixedPercentage as a_ST_PositiveFixedPercentage
from ecma376_office.oxml.dml.main import ST_ShapeID as a_ST_ShapeID
from ecma376_office.oxml.dml.main import to_ST_Angle as a_to_ST_Angle
from ecma376_office.oxml.dml.main import to_ST_Coordinate32 as a_to_ST_Coordinate32
from ecma376_office.oxml.dml.main import to_ST_FixedPercentage as a_to_ST_FixedPercentage
from ecma376_office.oxml.dml.main import to_ST_Percentage as a_to_ST_Percentage
from ecma376_office.oxml.dml.main import to_ST_PositiveCoordinate32 as a_to_ST_PositiveCoordinate32
from ecma376_office.oxml.dml.main import to_ST_PositiveFixedPercentage as a_to_ST_PositiveFixedPercentage
from ecma376_office.oxml.exceptions import OxmlAttributeValidateError, OxmlElementValidateError
from ecma376_office.oxml.shared.common_simple_types import ST_ConformanceClass as s_ST_ConformanceClass
from ecma376_office.oxml.shared.common_simple_types import ST_PositivePercentage as s_ST_PositivePercentage
from ecma376_office.oxml.shared.common_simple_types import to_ST_PositivePercentage as s_to_ST_PositivePercentage
from ecma376_office.oxml.shared.relationship_reference import ST_RelationshipId as r_ST_RelationshipId
from ecma376_office.oxml.xsd_types import XSD_DateTime, to_xsd_datetime

# namespace_p = "http://purl.oclc.org/ooxml/presentationml/main"
namespace_p = 'http://schemas.openxmlformats.org/presentationml/2006/main'

# namespace_a = "http://purl.oclc.org/ooxml/drawingml/main"
namespace_a = 'http://schemas.openxmlformats.org/drawingml/2006/main'

# namespace_r = "http://purl.oclc.org/ooxml/officeDocument/relationships"
namespace_r = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

# namespace_s = "http://purl.oclc.org/ooxml/officeDocument/sharedTypes"
namespace_s = 'http://schemas.openxmlformats.org/officeDocument/2006/sharedTypes'

# 替代内容的命名空间,
# 参考标准的第三部分:
# https://hellowac.github.io/ecma-376-zh-cn/ecma-part3-refrence/
namespace_mc = 'http://schemas.openxmlformats.org/markup-compatibility/2006'

logger = logging.getLogger(__name__)

ns_map = {
    'p': namespace_p,  # 当前命名空间
    'a': namespace_a,
    'r': namespace_r,
    's': namespace_s,
    'mc': namespace_mc,
}


def qn(tag: str):
    """将 dc:creator 这种的标签,转换为 {http://purl.org/dc/elements/1.1/}creator 这样的形式"""

    global ns_map

    if ':' not in tag:
        return tag

    ns_prefix, ns = tag.split(':')

    return f'{{{ns_map[ns_prefix]}}}{ns}'


SubBaseElement = TypeVar('SubBaseElement', bound=OxmlBaseElement)


class ST_TransitionSideDirectionType(ST_BaseEnumType):
    """过渡侧向类型

    19.7.53 ST_TransitionSideDirectionType (Transition Side Direction Type)

    这个简单的类型定义了一组幻灯片过渡方向。

    此简单类型仅限于下表中列出的值：

    l (Left) -  指定过渡方向为向左

    u (Up) -  指定过渡方向为向上

    r (Right) - 指定过渡方向为向右

    d (Down) - 指定过渡方向为向下
    """

    Left = 'l'  # 指定过渡方向为向左
    Up = 'u'  # # 指定过渡方向为向上
    Right = 'r'  # 指定过渡方向为向右
    Down = 'd'  # 指定过渡方向为向下


class ST_TransitionCornerDirectionType(ST_BaseEnumType):
    """过渡角方向型

    19.7.50 ST_TransitionCornerDirectionType (Transition Corner Direction Type)

    这种简单的类型指定幻灯片过渡的对角线方向。
    """

    LeftUp = 'lu'  # 指定幻灯片过渡方向为左上
    RightUp = 'ru'  # 指定幻灯片过渡方向为右上
    LeftDown = 'ld'  # 指定幻灯片过渡方向为左下
    RightDown = 'rd'  # 指定幻灯片过渡方向为右下


class ST_TransitionInOutDirectionType(ST_BaseEnumType):
    """过渡输入/输出方向类型

    19.7.52 ST_TransitionInOutDirectionType (Transition In/Out Direction Type)

    这个简单的类型指定幻灯片过渡是否应该进入或退出。
    """

    In = 'in'  # 指定幻灯片过渡应进入
    Out = 'out'  # 指定幻灯片过渡应该消失


class CT_SideDirectionTransition(OxmlBaseElement):
    """
    aaa
    """

    @property
    def direction(self) -> ST_TransitionSideDirectionType:
        """
        aaa
        """

        val = self.attrib.get('dir')

        if val is None:
            return ST_TransitionSideDirectionType.Left

        return ST_TransitionSideDirectionType(val)


class CT_CornerDirectionTransition(OxmlBaseElement):
    """
    aaa
    """

    @property
    def direction(self) -> ST_TransitionCornerDirectionType:
        """
        aaa
        """

        val = self.attrib.get('dir')

        if val is None:
            return ST_TransitionCornerDirectionType.LeftUp

        return ST_TransitionCornerDirectionType(val)


# <xsd:union memberTypes="ST_TransitionSideDirectionType ST_TransitionCornerDirectionType"/>
class ST_TransitionEightDirectionType(ST_BaseEnumType):
    """
    过渡八方向

    19.7.51 ST_TransitionEightDirectionType (Transition Eight Direction)

    这个简单的类型指定动画的方向。

    这个简单类型是以下类型的联合：

    - ST_TransitionCornerDirectionType 简单类型 (§19.7.50)。

    - ST_TransitionSideDirectionType 简单类型 (§19.7.53)。
    """

    Left = 'l'  # 指定过渡方向为向左
    Up = 'u'  # # 指定过渡方向为向上
    Right = 'r'  # 指定过渡方向为向右
    Down = 'd'  # 指定过渡方向为向下

    LeftUp = 'lu'  # 指定幻灯片过渡方向为左上
    RightUp = 'ru'  # 指定幻灯片过渡方向为右上
    LeftDown = 'ld'  # 指定幻灯片过渡方向为左下
    RightDown = 'rd'  # 指定幻灯片过渡方向为右下


class CT_EightDirectionTransition(OxmlBaseElement):
    """
    aaa
    """

    @property
    def direction(self) -> ST_TransitionEightDirectionType:
        """
        aaa
        """

        val = self.attrib.get('dir')

        if val is None:
            return ST_TransitionEightDirectionType.Left

        return ST_TransitionEightDirectionType(val)


class ST_Direction(ST_BaseEnumType):
    """
    aaa
    """

    Horz = 'horz'
    Vert = 'vert'


class CT_OrientationTransition(OxmlBaseElement):
    """
    aaa
    """

    @property
    def direction(self) -> ST_Direction:
        """
        aaa
        """

        val = self.attrib.get('dir')

        if val is None:
            return ST_Direction.Horz

        return ST_Direction(val)


class CT_InOutTransition(OxmlBaseElement):
    """
    aaa
    """

    @property
    def direction(self) -> ST_TransitionInOutDirectionType:
        """
        aaa
        """

        val = self.attrib.get('dir')

        if val is None:
            return ST_TransitionInOutDirectionType.Out

        return ST_TransitionInOutDirectionType(val)


class CT_OptionalBlackTransition(OxmlBaseElement):
    """
    aaa
    """

    @property
    def thru_blk(self) -> bool:
        """
        aaa
        """

        val = self.attrib.get('thruBlk')

        return utils.XsdBool(val, none=False)


class CT_SplitTransition(OxmlBaseElement):
    """
    aaa
    """

    @property
    def orient(self) -> ST_Direction:
        """
        aaa
        """

        val = self.attrib.get('orient')

        if val is None:
            return ST_Direction.Horz

        return ST_Direction(val)

    @property
    def direction(self) -> ST_TransitionInOutDirectionType:
        """
        aaa
        """

        val = self.attrib.get('dir')

        if val is None:
            return ST_TransitionInOutDirectionType.Out

        return ST_TransitionInOutDirectionType(val)


class CT_WheelTransition(OxmlBaseElement):
    """
    aaa
    """

    @property
    def spokes(self) -> int:
        """
        aaa
        """

        val = self.attrib.get('spokes')

        if val is None:
            return 4

        return utils.XsdUnsignedInt(val)


class CT_TransitionStartSoundAction(OxmlBaseElement):
    """
    aaa
    """

    @property
    def sound(self) -> a_CT_EmbeddedWAVAudioFile:
        """
        aaa
        """

        return getattr(self, qn('p:snd'))

    @property
    def loop(self) -> bool:
        """
        aaa
        """

        val = self.attrib.get('loop')

        return utils.XsdBool(val, none=False)


class CT_TransitionSoundAction(OxmlBaseElement):
    """
    aaa
    """

    @property
    def sound(self) -> CT_TransitionStartSoundAction | CT_Empty:
        """
        aaa
        """

        tags = (
            qn('p:stSnd'),  # CT_TransitionStartSoundAction
            qn('p:endSnd'),  # CT_Empty
        )

        return self.choice_require_one_child(*tags)  # type: ignore


class ST_TransitionSpeed(ST_BaseEnumType):
    """
    aaa
    """

    Slow = 'slow'
    Medium = 'med'
    Fast = 'fast'


class CT_SlideTransition(OxmlBaseElement):
    """幻灯片布局的幻灯片过渡

    19.3.1.50 transition

    此元素指定用于从上一张幻灯片过渡到当前幻灯片的幻灯片过渡类型。 也就是说，转换信息存储在转换完成后出现的幻灯片上。
    """

    @property
    def transition(
        self,
    ) -> Optional[
        CT_OrientationTransition | CT_Empty | CT_EightDirectionTransition | CT_OptionalBlackTransition | CT_SideDirectionTransition | CT_SplitTransition | CT_CornerDirectionTransition | CT_WheelTransition | CT_InOutTransition
    ]:
        """幻灯片过渡动画

        注意不仅要根据类型判断，还要根据标签名判断

        <xsd:choice minOccurs="0" maxOccurs="1">
            <xsd:element name="blinds" type="CT_OrientationTransition"/>
            ...
        </xsd:choice>
        """

        tags = (
            qn('p:blinds'),  # CT_OrientationTransition
            qn('p:checker'),  # CT_OrientationTransition
            qn('p:circle'),  # CT_Empty
            qn('p:dissolve'),  # CT_Empty
            qn('p:comb'),  # CT_OrientationTransition
            qn('p:cover'),  # CT_EightDirectionTransition
            qn('p:cut'),  # CT_OptionalBlackTransition
            qn('p:diamond'),  # CT_Empty
            qn('p:fade'),  # CT_OptionalBlackTransition
            qn('p:newsflash'),  # CT_Empty
            qn('p:plus'),  # CT_Empty
            qn('p:pull'),  # CT_EightDirectionTransition
            qn('p:push'),  # CT_SideDirectionTransition
            qn('p:random'),  # CT_Empty
            qn('p:randomBar'),  # CT_OrientationTransition
            qn('p:split'),  # CT_SplitTransition
            qn('p:strips'),  # CT_CornerDirectionTransition
            qn('p:wedge'),  # CT_Empty
            qn('p:wheel'),  # CT_WheelTransition
            qn('p:wipe'),  # CT_SideDirectionTransition
            qn('p:zoom'),  # CT_InOutTransition
        )

        return self.choice_one_child(*tags)  # type: ignore

    @property
    def sound_ac(self) -> Optional[CT_TransitionSoundAction]:
        """
        aaa
        """

        return getattr(self, qn('p:sndAc'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionListModify]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)

    @property
    def speed(self) -> ST_TransitionSpeed:
        """过渡速度

        指定从当前幻灯片过渡到下一张幻灯片时要使用的过渡速度.
        """

        val = self.attrib.get('spd')

        if val is None:
            return ST_TransitionSpeed.Fast

        return ST_TransitionSpeed(val)

    @property
    def adv_click(self) -> bool:
        """单击前进

        指定鼠标单击是否使幻灯片前进。 如果未指定此属性，则假定值为 true.
        """

        val = self.attrib.get('advClick')

        return utils.XsdBool(val, none=False)

    @property
    def adv_tm(self) -> Optional[int]:
        """时间过后前进

        指定转换应开始的时间（以毫秒为单位）。 此设置可以与 advClick 属性结合使用。 如果未指定此属性，则假定不会发生自动前进.
        """

        val = self.attrib.get('advTm')

        if val is None:
            return None

        return utils.XsdUnsignedInt(val)


class ST_TLTimeIndefinite(ST_BaseEnumType):
    """
    aaa
    """

    Indefinite = 'indefinite'


class ST_TLTime(ST_BaseType[AnyStr, Union[int, ST_TLTimeIndefinite]]):
    """
    aaa

    <xsd:union memberTypes="xsd:unsignedInt ST_TLTimeIndefinite"/>

    """

    def _validate(self: Self) -> None:
        val = utils.AnyStrToStr(self._val)

        if not val.isdigit() and not ST_TLTimeIndefinite.have_value(val):
            msg = f'预期外的值: {val}'
            raise OxmlAttributeValidateError(msg)

        if val.isdigit():
            self._python_val = utils.XsdUnsignedInt(val)

        else:
            self._python_val = ST_TLTimeIndefinite(val)


# <xsd:restriction base="xsd:unsignedInt"/>
class ST_TLTimeNodeID(ST_BaseType[AnyStr, int]):
    """
    aaa

    <xsd:restriction base="xsd:unsignedInt"/>
    """

    def _validate(self: Self) -> None:
        self._python_val = utils.XsdUnsignedInt(self._val)


class CT_TLIterateIntervalTime(OxmlBaseElement):
    """
    aaa
    """

    @property
    def value(self) -> ST_TLTime:
        """
        aaa
        """
        return ST_TLTime(self.attrib['val'])


class CT_TLIterateIntervalPercentage(OxmlBaseElement):
    """
    aaa
    """

    @property
    def value(self) -> s_ST_PositivePercentage:
        """
        aaa
        """
        return s_to_ST_PositivePercentage(str(self.attrib['val']))


class ST_IterateType(ST_BaseEnumType):
    """
    aaa
    """

    Element = 'el'  # 按元素迭代。
    Word = 'wd'  # 按字母迭代。
    Letter = 'lt'  # 按单词迭代


class CT_TLIterateData(OxmlBaseElement):
    """
    aaa
    """

    @property
    def time(self) -> CT_TLIterateIntervalTime | CT_TLIterateIntervalPercentage:
        """
        aaa

        <xsd:choice minOccurs="1" maxOccurs="1">
        """

        tags = (
            qn('p:tmAbs'),  # CT_TLIterateIntervalTime
            qn('p:tmPct'),  # CT_TLIterateIntervalPercentage
        )

        return self.choice_require_one_child(*tags)  # type: ignore

    @property
    def type(self) -> ST_IterateType:
        """
        aaa
        """

        val = self.attrib.get('type')

        if val is None:
            return ST_IterateType.Element

        return ST_IterateType(val)

    @property
    def backwords(self) -> bool:
        """
        aaa
        """

        val = self.attrib.get('backwords')

        return utils.XsdBool(val, none=False)


class CT_TLSubShapeId(OxmlBaseElement):
    """
    aaa
    """

    @property
    def shape_id(self) -> a_ST_ShapeID:
        """
        aaa
        """

        val = self.attrib['spid']

        return a_ST_ShapeID(utils.AnyStrToStr(val))  # type: ignore


class CT_TLTextTargetElement(OxmlBaseElement):
    """
    aaa
    """

    @property
    def range(self) -> Optional[CT_IndexRange]:
        """
        aaa

        <xsd:choice minOccurs="0" maxOccurs="1">
        """

        tags = (
            qn('p:charRg'),  # CT_IndexRange
            qn('p:pRg'),  # CT_IndexRange
        )

        return self.choice_one_child(*tags)  # type: ignore


class ST_TLChartSubelementType(ST_BaseEnumType):
    """图表子元素类型

    19.7.31 ST_TLChartSubelementType (Chart Subelement Type)

    此简单类型定义由图表的子元素表示的动画目标元素。
    """

    GridLegend = 'gridLegend'  # Grid Legend 背景元素（网格和图例）
    Series = 'series'  # Data Series  系列
    Category = 'category'  # Category Axis  类别
    PtInSeries = 'ptInSeries'  # Single Point in Data Series 元素系列
    PtInCategory = 'ptInCategory'  # Single Point in Category 类别元素


class CT_TLOleChartTargetElement(OxmlBaseElement):
    """
    aaa
    """

    @property
    def type(self) -> ST_TLChartSubelementType:
        """
        aaa
        """

        return ST_TLChartSubelementType(self.attrib['type'])

    @property
    def level(self) -> int:
        """
        aaa
        """

        val = self.attrib.get('lvl')

        if val is None:
            return 0

        return utils.XsdUnsignedInt(val)


class CT_TLShapeTargetElement(OxmlBaseElement):
    """
    aaa
    """

    @property
    def element(
        self,
    ) -> Optional[
        CT_Empty | CT_TLSubShapeId | CT_TLOleChartTargetElement | CT_TLTextTargetElement | a_CT_AnimationElementChoice
    ]:
        """
        aaa

        <xsd:choice minOccurs="0" maxOccurs="1">
        """

        tags = (
            qn('p:bg'),  # CT_Empty
            qn('p:subSp'),  # CT_TLSubShapeId
            qn('p:oleChartEl'),  # CT_TLSubShapeId
            qn('p:txEl'),  # CT_TLTextTargetElement
            qn('p:graphicEl'),  # a_CT_AnimationElementChoice
        )

        return self.choice_one_child(*tags)  # type: ignore

    @property
    def shape_id(self) -> a_ST_DrawingElementId:
        """
        aaa
        """

        val = self.attrib['spid']

        return a_ST_DrawingElementId(int(val))


class CT_TLTimeTargetElement(OxmlBaseElement):
    """
    aaa
    """

    @property
    def target(
        self,
    ) -> CT_Empty | a_CT_EmbeddedWAVAudioFile | CT_TLShapeTargetElement | CT_TLSubShapeId:
        """
        aaa

        <xsd:choice minOccurs="1" maxOccurs="1">
        """

        tags = (
            qn('p:sldTgt'),  # CT_Empty
            qn('p:sndTgt'),  # a_CT_EmbeddedWAVAudioFile
            qn('p:spTgt'),  # CT_TLShapeTargetElement
            qn('p:inkTgt'),  # CT_TLSubShapeId
            qn('p:sldTgt'),  # aaaaaaaaaa
        )

        return self.choice_require_one_child(*tags)  # type: ignore


class CT_TLTriggerTimeNodeID(OxmlBaseElement):
    """
    aaa
    """

    @property
    def value(self) -> ST_TLTimeNodeID:
        """
        aaa
        """

        return ST_TLTimeNodeID(self.attrib['val'])


class ST_TLTriggerRuntimeNode(ST_BaseEnumType):
    """
    aaa
    """

    First = 'first'
    Last = 'last'
    All = 'all'


class CT_TLTriggerRuntimeNode(OxmlBaseElement):
    """
    aaa
    """

    @property
    def value(self) -> ST_TLTriggerRuntimeNode:
        """
        aaa
        """

        return ST_TLTriggerRuntimeNode(self.attrib['val'])


class ST_TLTriggerEvent(ST_BaseEnumType):
    """
    aaa
    """

    OnBegin = 'onBegin'
    OnEnd = 'onEnd'
    Begin = 'begin'
    End = 'end'
    OnClick = 'onClick'
    OnDblClick = 'onDblClick'
    OnMouseOver = 'onMouseOver'
    OnMouseOut = 'onMouseOut'
    OnNext = 'onNext'
    OnPrev = 'onPrev'
    OnStopAudio = 'onStopAudio'


class CT_TLTimeCondition(OxmlBaseElement):
    """
    aaa
    """

    @property
    def time_node(
        self,
    ) -> Optional[CT_TLTimeTargetElement | CT_TLTriggerTimeNodeID | CT_TLTriggerRuntimeNode]:
        """
        aaa

        <xsd:choice minOccurs="0" maxOccurs="1">
        """

        tags = (
            qn('p:tgtEl'),  # CT_TLTimeTargetElement
            qn('p:tn'),  # CT_TLTriggerTimeNodeID
            qn('p:rtn'),  # CT_TLTriggerRuntimeNode
        )

        return self.choice_one_child(*tags)  # type: ignore

    @property
    def event(self) -> Optional[ST_TLTriggerEvent]:
        """
        aaa
        """

        val = self.attrib.get('evt')

        if val is not None:
            return ST_TLTriggerEvent(val)

        return None

    @property
    def delay(self) -> Optional[ST_TLTime]:
        """
        aaa
        """

        val = self.attrib.get('delay')

        if val is not None:
            return ST_TLTime(val)

        return None


class CT_TLTimeConditionList(OxmlBaseElement):
    """
    aaa
    """

    @property
    def condition(self) -> list[CT_TLTimeCondition]:
        """
        aaa
        """

        return list(self.iterchildren(qn('p:cond')))



class CT_TimeNodeList(OxmlBaseElement):
    """
    aaa
    """

    @property
    def time_node(
        self,
    ) -> list[
        CT_TLTimeNodeParallel | CT_TLTimeNodeSequence | CT_TLTimeNodeExclusive | CT_TLAnimateBehavior | CT_TLAnimateColorBehavior | CT_TLAnimateEffectBehavior | CT_TLAnimateMotionBehavior | CT_TLAnimateRotationBehavior | CT_TLAnimateScaleBehavior | CT_TLCommandBehavior | CT_TLSetBehavior | CT_TLMediaNodeAudio | CT_TLMediaNodeVideo
    ]:
        """
        时间节点

        <xsd:choice minOccurs="1" maxOccurs="unbounded">
        """

        tags = (
            qn('p:par'),
            qn('p:seq'),
            qn('p:excl'),
            qn('p:anim'),
            qn('p:animClr'),
            qn('p:animEffect'),
            qn('p:animMotion'),
            qn('p:animRot'),
            qn('p:animScale'),
            qn('p:cmd'),
            qn('p:set'),
            qn('p:audio'),
            qn('p:video'),
        )

        return self.choice_and_more(*tags)  # type: ignore


class ST_TLTimeNodePresetClassType(ST_BaseEnumType):
    """
    aaa
    """

    Enter = 'entr'
    Exit = 'exit'
    Emph = 'emph'
    Path = 'path'
    Verb = 'verb'
    Mediacall = 'mediacall'


class ST_TLTimeNodeRestartType(ST_BaseEnumType):
    """
    aaa
    """

    Always = 'always'
    WhenNotActive = 'whenNotActive'
    Never = 'never'


class ST_TLTimeNodeFillType(ST_BaseEnumType):
    """
    aaa
    """

    Remove = 'remove'
    Freeze = 'freeze'
    Hold = 'hold'
    Transition = 'transition'


class ST_TLTimeNodeSyncType(ST_BaseEnumType):
    """
    aaa
    """

    CanSlip = 'canSlip'
    Locked = 'locked'


class ST_TLTimeNodeMasterRelation(ST_BaseEnumType):
    """
    aaa
    """

    SameClick = 'sameClick'
    LastClick = 'lastClick'
    NextClick = 'nextClick'


class ST_TLTimeNodeType(ST_BaseEnumType):
    """
    aaa
    """

    ClickEffect = 'clickEffect'
    WithEffect = 'withEffect'
    AfterEffect = 'afterEffect'
    MainSeq = 'mainSeq'
    InteractiveSeq = 'interactiveSeq'
    ClickPar = 'clickPar'
    WithGroup = 'withGroup'
    AfterGroup = 'afterGroup'
    TmRoot = 'tmRoot'


class CT_TLCommonTimeNodeData(OxmlBaseElement):
    """
    aaa
    """

    @property
    def start_cond_lst(self) -> Optional[CT_TLTimeConditionList]:
        """
        aaa
        """

        return getattr(self, qn('p:stCondLst'), None)

    @property
    def end_cond_lst(self) -> Optional[CT_TLTimeConditionList]:
        """
        aaa
        """

        return getattr(self, qn('p:endCondLst'), None)

    @property
    def end_sync(self) -> Optional[CT_TLTimeCondition]:
        """
        aaa
        """

        return getattr(self, qn('p:endSync'), None)

    @property
    def iterate(self) -> Optional[CT_TLIterateData]:
        """
        aaa
        """

        return getattr(self, qn('p:iterate'), None)

    @property
    def child_tn_lst(self) -> Optional[CT_TimeNodeList]:
        """
        aaa
        """

        return getattr(self, qn('p:childTnLst'), None)

    @property
    def subling_tn_lst(self) -> Optional[CT_TimeNodeList]:
        """
        aaa
        """

        return getattr(self, qn('p:subTnLst'), None)

    @property
    def id(self) -> Optional[ST_TLTimeNodeID]:
        """
        aaa
        """

        val = self.attrib.get('id')

        if val is None:
            return None

        return ST_TLTimeNodeID(val)

    @property
    def preset_id(self) -> Optional[int]:
        """
        aaa
        """

        val = self.attrib.get('presetID')

        if val is None:
            return None

        return int(val)

    @property
    def preset_class(self) -> Optional[ST_TLTimeNodePresetClassType]:
        """
        aaa
        """

        val = self.attrib.get('presetClass')

        if val is None:
            return None

        return ST_TLTimeNodePresetClassType(val)

    @property
    def preset_subtype(self) -> Optional[int]:
        """
        aaa
        """

        val = self.attrib.get('presetSubtype')

        if val is None:
            return None

        return int(val)

    @property
    def duration(self) -> Optional[ST_TLTime]:
        """
        aaa
        """

        val = self.attrib.get('dur')

        if val is None:
            return None

        return ST_TLTime(val)

    @property
    def repeat_count(self) -> ST_TLTime:
        """
        aaa
        """

        val = self.attrib.get('repeatCount')

        if val is None:
            val = '1000'

        return ST_TLTime(val)

    @property
    def repeat_duration(self) -> Optional[ST_TLTime]:
        """
        aaa
        """

        val = self.attrib.get('repeatDur')

        if val is None:
            return None

        return ST_TLTime(val)

    @property
    def speed(self) -> a_ST_Percentage:
        """
        aaa
        """

        val = self.attrib.get('spd')

        if val is None:
            val = '100%'

        return a_to_ST_Percentage(str(val))

    @property
    def accel(self) -> a_ST_PositiveFixedPercentage:
        """
        aaa
        """

        val = self.attrib.get('accel')

        if val is None:
            val = '0%'

        return a_to_ST_PositiveFixedPercentage(str(val))

    @property
    def decel(self) -> a_ST_PositiveFixedPercentage:
        """
        aaa
        """

        val = self.attrib.get('decel')

        if val is None:
            val = '0%'

        return a_to_ST_PositiveFixedPercentage(str(val))

    @property
    def auto_rev(self) -> bool:
        """
        aaa
        """

        val = self.attrib.get('autoRev')

        return utils.XsdBool(val, none=False)

    @property
    def restart(self) -> Optional[ST_TLTimeNodeRestartType]:
        """
        aaa
        """

        val = self.attrib.get('restart')

        if val is None:
            return None

        return ST_TLTimeNodeRestartType(val)

    @property
    def fill(self) -> Optional[ST_TLTimeNodeFillType]:
        """
        aaa
        """

        val = self.attrib.get('fill')

        if val is None:
            return None

        return ST_TLTimeNodeFillType(val)

    @property
    def sync_behavior(self) -> Optional[ST_TLTimeNodeSyncType]:
        """
        aaa
        """

        val = self.attrib.get('syncBehavior')

        if val is None:
            return None

        return ST_TLTimeNodeSyncType(val)

    @property
    def time_filter(self) -> Optional[str]:
        """
        aaa
        """

        val = self.attrib.get('tmFilter')

        if val is None:
            return None

        return utils.AnyStrToStr(val)  # type: ignore

    @property
    def event_filter(self) -> Optional[str]:
        """
        aaa
        """

        val = self.attrib.get('evtFilter')

        if val is None:
            return None

        return utils.AnyStrToStr(val)  # type: ignore

    @property
    def display(self) -> Optional[bool]:
        """
        aaa
        """

        val = self.attrib.get('display')

        if val is None:
            return None

        return utils.XsdBool(val)

    @property
    def master_rel(self) -> Optional[ST_TLTimeNodeMasterRelation]:
        """
        aaa
        """

        val = self.attrib.get('masterRel')

        if val is None:
            return None

        return ST_TLTimeNodeMasterRelation(val)

    @property
    def bld_level(self) -> Optional[int]:
        """
        aaa
        """

        val = self.attrib.get('bldLvl')

        if val is None:
            return None

        return int(val)

    @property
    def group_id(self) -> Optional[int]:
        """
        aaa
        """

        val = self.attrib.get('grpId')

        if val is None:
            return None

        return utils.XsdUnsignedInt(val)

    @property
    def after_effect(self) -> Optional[bool]:
        """
        aaa
        """

        val = self.attrib.get('afterEffect')

        if val is None:
            return None

        return utils.XsdBool(val)

    @property
    def node_type(self) -> Optional[ST_TLTimeNodeType]:
        """
        aaa
        """

        val = self.attrib.get('nodeType')

        if val is None:
            return None

        return ST_TLTimeNodeType(val)

    @property
    def node_ph(self) -> Optional[bool]:
        """
        aaa
        """

        val = self.attrib.get('nodePh')

        if val is None:
            return None

        return utils.XsdBool(val)


class CT_TLTimeNodeParallel(OxmlBaseElement):
    """
    aaa
    """

    @property
    def common_time_node(self) -> CT_TLCommonTimeNodeData:
        """
        aaa
        """

        return getattr(self, qn('p:cTn'))


class ST_TLNextActionType(ST_BaseEnumType):
    """
    aaa
    """

    none = 'none'
    Seek = 'seek'


class ST_TLPreviousActionType(ST_BaseEnumType):
    """
    aaa
    """

    none = 'none'
    SkipTimed = 'skipTimed'


class CT_TLTimeNodeSequence(OxmlBaseElement):
    """
    aaa
    """

    @property
    def common_time_node(self) -> CT_TLCommonTimeNodeData:
        """
        aaa
        """

        return getattr(self, qn('p:cTn'))

    @property
    def prev_cond_lst(self) -> Optional[CT_TLTimeConditionList]:
        """
        aaa
        """

        return getattr(self, qn('p:prevCondLst'), None)

    @property
    def next_cond_lst(self) -> Optional[CT_TLTimeConditionList]:
        """
        aaa
        """

        return getattr(self, qn('p:nextCondLst'), None)

    @property
    def concurrent(self) -> Optional[bool]:
        """
        aaa
        """

        val = self.attrib.get('concurrent')

        if val is None:
            return val

        return utils.XsdBool(val)

    @property
    def prev_ac(self) -> Optional[ST_TLPreviousActionType]:
        """
        aaa
        """

        val = self.attrib.get('prevAc')

        if val is None:
            return val

        return ST_TLPreviousActionType(val)

    @property
    def next_ac(self) -> Optional[ST_TLNextActionType]:
        """
        aaa
        """

        val = self.attrib.get('nextAc')

        if val is None:
            return val

        return ST_TLNextActionType(val)


class CT_TLTimeNodeExclusive(OxmlBaseElement):
    """
    aaa
    """

    @property
    def common_time_node(self) -> CT_TLCommonTimeNodeData:
        """
        aaa
        """

        return getattr(self, qn('p:cTn'))


class CT_TLBehaviorAttributeNameList(OxmlBaseElement):
    """
    aaa
    """

    @property
    def attr_names(self) -> list[str]:
        """
        aaa

        <xsd:element name="attrName" type="xsd:string" minOccurs="1" maxOccurs="unbounded"/>
        """

        return [e.text or '' for e in self.iterchildren(qn('p:attrName'))]


class ST_TLBehaviorAdditiveType(ST_BaseEnumType):
    """
    aaa
    """

    Base = 'base'
    Sum = 'sum'
    Repl = 'repl'
    Mult = 'mult'
    none = 'none'


class ST_TLBehaviorAccumulateType(ST_BaseEnumType):
    """
    aaa
    """

    Always = 'always'
    none = 'none'


class ST_TLBehaviorTransformType(ST_BaseEnumType):
    """
    aaa
    """

    Pt = 'pt'
    Img = 'img'


class ST_TLBehaviorOverrideType(ST_BaseEnumType):
    """
    aaa
    """

    Normal = 'normal'
    ChildStyle = 'childStyle'


class CT_TLCommonBehaviorData(OxmlBaseElement):
    """
    aaa
    """

    @property
    def common_time_node(self) -> CT_TLCommonTimeNodeData:
        """
        aaa
        """

        return getattr(self, qn('p:cTn'))

    @property
    def target_ele(self) -> CT_TLTimeTargetElement:
        """
        aaa
        """

        return getattr(self, qn('p:tgtEl'))

    @property
    def attr_name_lst(self) -> Optional[CT_TLBehaviorAttributeNameList]:
        """
        aaa
        """

        return getattr(self, qn('p:attrNameLst'), None)

    @property
    def additive(self) -> Optional[ST_TLBehaviorAdditiveType]:
        """
        aaa
        """

        val = self.attrib.get('additive')

        if val is None:
            return None

        return ST_TLBehaviorAdditiveType(val)

    @property
    def accumulate(self) -> Optional[ST_TLBehaviorAccumulateType]:
        """
        aaa
        """

        val = self.attrib.get('accumulate')

        if val is None:
            return None

        return ST_TLBehaviorAccumulateType(val)

    @property
    def xfrm_type(self) -> Optional[ST_TLBehaviorTransformType]:
        """
        aaa
        """

        val = self.attrib.get('xfrmType')

        if val is None:
            return None

        return ST_TLBehaviorTransformType(val)

    @property
    def from_(self) -> Optional[str]:
        """
        aaa
        """

        val = self.attrib.get('from')

        if val is None:
            return None

        return utils.AnyStrToStr(val)  # type: ignore

    @property
    def to(self) -> Optional[str]:
        """
        aaa
        """

        val = self.attrib.get('to')

        if val is None:
            return None

        return utils.AnyStrToStr(val)  # type: ignore

    @property
    def by(self) -> Optional[str]:
        """
        aaa
        """

        val = self.attrib.get('by')

        if val is None:
            return None

        return utils.AnyStrToStr(val)  # type: ignore

    @property
    def rctx(self) -> Optional[str]:
        """
        aaa
        """

        val = self.attrib.get('rctx')

        if val is None:
            return None

        return utils.AnyStrToStr(val)  # type: ignore

    @property
    def override(self) -> Optional[ST_TLBehaviorOverrideType]:
        """
        aaa
        """

        val = self.attrib.get('override')

        if val is None:
            return None

        return ST_TLBehaviorOverrideType(val)  # type: ignore


class CT_TLAnimVariantBooleanVal(OxmlBaseElement):
    """
    aaa
    """

    @property
    def value(self) -> bool:
        """
        aaa
        """

        return utils.XsdBool(self.attrib['val'])


class CT_TLAnimVariantIntegerVal(OxmlBaseElement):
    """
    aaa
    """

    @property
    def value(self) -> int:
        """
        aaa
        """

        return int(self.attrib['val'])


class CT_TLAnimVariantFloatVal(OxmlBaseElement):
    """
    aaa
    """

    @property
    def value(self) -> float:
        """
        aaa
        """

        return float(self.attrib['val'])


class CT_TLAnimVariantStringVal(OxmlBaseElement):
    """
    aaa
    """

    @property
    def value(self) -> str:
        """
        aaa
        """

        return utils.AnyStrToStr(self.attrib['val'])  # type: ignore


class CT_TLAnimVariant(OxmlBaseElement):
    """
    aaa
    """

    @property
    def value(
        self,
    ) -> CT_TLAnimVariantBooleanVal | CT_TLAnimVariantIntegerVal | CT_TLAnimVariantFloatVal | CT_TLAnimVariantStringVal | a_CT_Color:
        tags = (
            qn('p:boolVal'),  # CT_TLAnimVariantBooleanVal
            qn('p:intVal'),  # CT_TLAnimVariantIntegerVal
            qn('p:fltVal'),  # CT_TLAnimVariantFloatVal
            qn('p:strVal'),  # CT_TLAnimVariantStringVal
            qn('p:clrVal'),  # a_CT_Color
        )

        return self.choice_require_one_child(*tags)  # type: ignore


# <xsd:union memberTypes="a:ST_PositiveFixedPercentage ST_TLTimeIndefinite"/>
class ST_TLTimeAnimateValueTime(ST_BaseType[AnyStr, Union[a_ST_PositiveFixedPercentage, ST_TLTimeIndefinite]]):
    def _validate(self: Self) -> None:
        val = utils.AnyStrToStr(self._val)

        if ST_TLTimeIndefinite.have_value(val):
            self._python_val = ST_TLTimeIndefinite(val)

        self._python_val = a_to_ST_PositiveFixedPercentage(val)


class CT_TLTimeAnimateValue(OxmlBaseElement):
    """
    aaa
    """

    @property
    def value(self) -> Optional[CT_TLAnimVariant]:
        return getattr(self, qn('p:val'), None)

    @property
    def time(self) -> ST_TLTimeAnimateValueTime:
        """
        aaa
        """

        val = self.attrib.get('tm')

        if val is None:
            return ST_TLTimeAnimateValueTime(ST_TLTimeIndefinite.Indefinite.value)

        return ST_TLTimeAnimateValueTime(val)

    @property
    def formula(self) -> str:
        """
        aaa
        """

        val = self.attrib.get('fmla')

        if val is None:
            return ''

        return utils.AnyStrToStr(val)  # type: ignore


class CT_TLTimeAnimateValueList(OxmlBaseElement):
    """
    aaa
    """

    @property
    def time_animate_value(self) -> list[CT_TLTimeAnimateValue]:
        """
        aaa
        """

        return self.findall(qn('p:tav'))  # type: ignore


class ST_TLAnimateBehaviorCalcMode(ST_BaseEnumType):
    """
    aaa
    """

    Discrete = 'discrete'
    Lin = 'lin'
    Fmla = 'fmla'


class ST_TLAnimateBehaviorValueType(ST_BaseEnumType):
    """
    aaa
    """

    String = 'str'
    Number = 'num'
    Color = 'clr'


class CT_TLAnimateBehavior(OxmlBaseElement):
    """
    aaa
    """

    @property
    def common_behavior(self) -> CT_TLCommonBehaviorData:
        """
        aaa
        """

        return getattr(self, qn('p:cBhvr'))

    @property
    def time_animate_value_lst(self) -> Optional[CT_TLTimeAnimateValueList]:
        """
        aaa
        """

        return getattr(self, qn('p:tavLst'), None)

    @property
    def by(self) -> Optional[str]:
        """
        aaa
        """

        val = self.attrib.get('by')

        if val is None:
            return None

        return utils.AnyStrToStr(val)  # type: ignore

    @property
    def from_(self) -> Optional[str]:
        """
        aaa
        """

        val = self.attrib.get('from')

        if val is None:
            return None

        return utils.AnyStrToStr(val)  # type: ignore

    @property
    def to(self) -> Optional[str]:
        """
        aaa
        """

        val = self.attrib.get('to')

        if val is None:
            return None

        return utils.AnyStrToStr(val)  # type: ignore

    @property
    def calc_mode(self) -> Optional[ST_TLAnimateBehaviorCalcMode]:
        """
        aaa
        """

        val = self.attrib.get('calcmode')

        if val is None:
            return None

        return ST_TLAnimateBehaviorCalcMode(val)

    @property
    def value_type(self) -> Optional[ST_TLAnimateBehaviorValueType]:
        """
        aaa
        """

        val = self.attrib.get('valueType')

        if val is None:
            return None

        return ST_TLAnimateBehaviorValueType(val)  # type: ignore


class CT_TLByRgbColorTransform(OxmlBaseElement):
    """
    aaa
    """

    @property
    def red_percent(self) -> a_ST_FixedPercentage:
        """
        aaa
        """

        return a_to_ST_FixedPercentage(str(self.attrib['r']))

    @property
    def green_percent(self) -> a_ST_FixedPercentage:
        """
        aaa
        """

        return a_to_ST_FixedPercentage(str(self.attrib['g']))

    @property
    def blue_percent(self) -> a_ST_FixedPercentage:
        """
        aaa
        """

        return a_to_ST_FixedPercentage(str(self.attrib['b']))


class CT_TLByHslColorTransform(OxmlBaseElement):
    """HSL值

    19.5.46 hsl (HSL)

    此元素指定要添加到彩色动画的增量 HSL（色调、饱和度、亮度）值。
    """

    @property
    def hue(self) -> a_ST_Angle:
        """色调

        Hue

        将色调指定为角度。 值范围为 [0, 360] 度
        """

        val = self.attrib['h']

        return a_to_ST_Angle(str(val))

    @property
    def saturation(self) -> a_ST_FixedPercentage:
        """饱和度

        Saturation

        将饱和度指定为百分比。 这些值的范围是 [-100%, 100%]。
        """

        return a_to_ST_FixedPercentage(str(self.attrib['s']))

    @property
    def lightness(self) -> a_ST_FixedPercentage:
        """亮度

        Lightness

        将亮度指定为百分比。 这些值的范围是 [-100%, 100%]。
        """

        return a_to_ST_FixedPercentage(str(self.attrib['l']))


class CT_TLByAnimateColorTransform(OxmlBaseElement):
    """
    aaa
    """

    @property
    def transform(self) -> CT_TLByRgbColorTransform | CT_TLByHslColorTransform:
        """
        aaa
        """

        tags = (
            qn('p:rgb'),  # CT_TLByRgbColorTransform
            qn('p:hsl'),  # CT_TLByHslColorTransform
        )

        return self.choice_require_one_child(*tags)  # type: ignore


class ST_TLAnimateColorSpace(ST_BaseEnumType):
    """
    aaa
    """

    RGB = 'rgb'
    HSL = 'hsl'


class ST_TLAnimateColorDirection(ST_BaseEnumType):
    """
    aaa
    """

    CW = 'cw'
    CCW = 'ccw'


class CT_TLAnimateColorBehavior(OxmlBaseElement):
    """
    aaa
    """

    @property
    def common_behavior(self) -> CT_TLCommonBehaviorData:
        """
        aaa
        """

        return getattr(self, qn('p:cBhvr'))

    @property
    def by(self) -> Optional[CT_TLByAnimateColorTransform]:
        """
        aaa
        """

        return getattr(self, qn('p:by'), None)

    @property
    def from_(self) -> Optional[a_CT_Color]:
        """
        aaa
        """

        return getattr(self, qn('p:from'), None)

    @property
    def to(self) -> Optional[a_CT_Color]:
        """
        aaa
        """

        return getattr(self, qn('p:to'), None)

    @property
    def color_space(self) -> Optional[ST_TLAnimateColorSpace]:
        """
        aaa
        """

        val = self.attrib.get('clrSpc')

        if val is None:
            return None

        return ST_TLAnimateColorSpace(val)

    @property
    def direction(self) -> Optional[ST_TLAnimateColorDirection]:
        """
        aaa
        """

        val = self.attrib.get('dir')

        if val is None:
            return None

        return ST_TLAnimateColorDirection(val)


class ST_TLAnimateEffectTransition(ST_BaseEnumType):
    """
    aaa
    """

    In = 'in'
    Out = 'out'
    none = 'none'


class CT_TLAnimateEffectBehavior(OxmlBaseElement):
    """动画效果

    19.5.3 animEffect (Animate Effect)

    此动画行为提供了对元素进行图像变换/过滤效果的能力。
    一些视觉效果本质上是动态的，并且具有在一段时间内从 0 到 1 的动画进度，以在隐藏状态和可见状态之间进行视觉转换。
    其他滤镜是静态的，并应用模糊或阴影等本质上不基于时间的效果。
    """

    @property
    def common_behavior(self) -> CT_TLCommonBehaviorData:
        """
        aaa
        """

        return getattr(self, qn('p:cBhvr'))

    @property
    def progress(self) -> Optional[CT_TLAnimVariant]:
        """
        aaa
        """

        return getattr(self, qn('p:progress'), None)

    @property
    def transition(self) -> ST_TLAnimateEffectTransition:
        """过渡

        Transition

        此属性指定是否将元素转入或转出，或者将其视为静态过滤器。 值为“none”、“in”和“out”，默认值为“in”。

        当指定“in”值时，该元素在动画开始时不可见，并在持续时间结束时完全可见。
        当指定“out”时，元素在效果开始时可见，但在效果结束时不可见。
        此可见性是对设置 CSS 可见性或显示属性的效果的补充。
        """

        val = self.attrib.get('transition')

        if val is None:
            return ST_TLAnimateEffectTransition.In

        return ST_TLAnimateEffectTransition(val)

    @property
    def filter(self) -> Optional[str]:
        """筛选

        Filter

        该属性指定用于效果的动画类型和子类型。
        允许列出多个动画，以便在无法呈现替代动画（最左边）的情况下，可以使用后备动画。
        也就是说，渲染应用程序从左到右解析列表，直到找到支持的动画。

        用于过滤器属性值的语法如下: “type(subtype);type(subtype)”。
        子类型可以是字符串值（例如“fromLeft”）或数字值，具体取决于指定的类型。

        保留的动画类型（子类型）：

        - blinds(horizontal)
        - blinds(vertical)
        - box(in)
        - box(out)
        - checkerboard(across)
        - checkerboard(down)
        - circle
        - diamond
        - dissolve
        - slide(fromTop)
        - slide(fromBottom)
        - slide(fromLeft)
        - slide(fromRight)
        - plus(in)
        - plus(out)
        - barn(inVertical)
        - barn(inHorizontal)
        - barn(outVertical)
        - barn(outHorizontal)
        - randomBars(horizontal)
        - randomBars(vertical)
        - strips(downLeft)
        - strips(upLeft)
        - strips(downRight)
        - strips(upRight)
        - wedge
        - wheel(1)
        - wheel(2)
        - wheel(3)
        - wheel(4)
        - wheel(8)
        - wipe(right)
        - wipe(left)
        - wipe(down)
        - wipe(up)

        [注：以上效果图仅用于示例目的。 任何动画的精确渲染都是由渲染应用程序决定的。 因此，根据实现的不同，相同的动画可以有多种变化。 上述每个渲染的更多详细信息可以在过渡 (§19.3.1.50) 中找到。 ]

        示例:

        <p:animEffect transition="in" filter="blinds(horizontal);blinds(vertical)">
        """

        val = self.attrib.get('filter')

        if val is None:
            return None

        return utils.AnyStrToStr(val)  # type: ignore

    @property
    def property_lst(self) -> Optional[str]:
        """属性列表

        Property List

        该属性指定与指定效果一致的属性列表。
        尽管允许有多种动画类型，但此属性允许设置特定的属性设置，以便描述更广泛的动画类型。

        prLst 属性值使用的语法如下: “name:value;name:value”。
        当过滤器属性中列出多个动画类型时，渲染应用程序会尝试应用每个属性值，即使某些属性值可能不适用于该属性值。

        保留名称（值）：

        - opacity(不透明度) (0.0 - 1.0之间的浮点值)

        参考:

        <p:animEffect filter="image" prLst="opacity: 0.5">
        """

        val = self.attrib.get('prLst')

        if val is None:
            return None

        return utils.AnyStrToStr(val)  # type: ignore


class ST_TLAnimateMotionBehaviorOrigin(ST_BaseEnumType):
    Parent = 'parent'
    Layout = 'layout'


class ST_TLAnimateMotionPathEditMode(ST_BaseEnumType):
    Relative = 'relative'
    Fixed = 'fixed'


class CT_TLPoint(OxmlBaseElement):
    """
    aaa
    """

    @property
    def x(self) -> a_ST_Percentage:
        """
        aaa
        """

        return a_to_ST_Percentage(str(self.attrib['x']))

    @property
    def y(self) -> a_ST_Percentage:
        """
        aaa
        """

        return a_to_ST_Percentage(str(self.attrib['y']))


class CT_TLAnimateMotionBehavior(OxmlBaseElement):
    """
    aaa
    """

    @property
    def common_behavior(self) -> CT_TLCommonBehaviorData:
        """
        aaa
        """

        return getattr(self, qn('p:cBhvr'))

    @property
    def by(self) -> Optional[CT_TLPoint]:
        """
        aaa
        """

        return getattr(self, qn('p:by'), None)

    @property
    def from_(self) -> Optional[CT_TLPoint]:
        """
        aaa
        """

        return getattr(self, qn('p:from'), None)

    @property
    def to(self) -> Optional[CT_TLPoint]:
        """
        aaa
        """

        return getattr(self, qn('p:to'), None)

    @property
    def r_ctr(self) -> Optional[CT_TLPoint]:
        """
        aaa
        """

        return getattr(self, qn('p:rCtr'), None)

    @property
    def origin(self) -> Optional[ST_TLAnimateMotionBehaviorOrigin]:
        """
        aaa
        """

        val = self.attrib.get('origin')

        if val is None:
            return None

        return ST_TLAnimateMotionBehaviorOrigin(val)

    @property
    def path(self) -> Optional[str]:
        """
        aaa
        """

        val = self.attrib.get('path')

        if val is None:
            return None

        return utils.AnyStrToStr(val)  # type: ignore

    @property
    def path_edit_mode(self) -> Optional[ST_TLAnimateMotionPathEditMode]:
        """
        aaa
        """

        val = self.attrib.get('pathEditMode')

        if val is None:
            return None

        return ST_TLAnimateMotionPathEditMode(val)

    @property
    def rotate_angle(self) -> Optional[a_ST_Angle]:
        """
        aaa
        """

        val = self.attrib.get('rAng')

        if val is None:
            return None

        return a_to_ST_Angle(str(val))

    @property
    def pts_types(self) -> Optional[str]:
        """
        aaa
        """

        val = self.attrib.get('ptsTypes')

        if val is None:
            return None

        return utils.AnyStrToStr(val)  # type: ignore


class CT_TLAnimateRotationBehavior(OxmlBaseElement):
    """
    aaa
    """

    @property
    def common_behavior(self) -> CT_TLCommonBehaviorData:
        """
        aaa
        """

        return getattr(self, qn('p:cBhvr'))

    @property
    def by(self) -> Optional[a_ST_Angle]:
        """
        aaa
        """

        val = self.attrib.get('by')

        if val is None:
            return None

        return a_to_ST_Angle(str(val))

    @property
    def from_(self) -> Optional[a_ST_Angle]:
        """
        aaa
        """

        val = self.attrib.get('from')

        if val is None:
            return None

        return a_to_ST_Angle(str(val))

    @property
    def to(self) -> Optional[a_ST_Angle]:
        """
        aaa
        """

        val = self.attrib.get('to')

        if val is None:
            return None

        return a_to_ST_Angle(str(val))


class CT_TLAnimateScaleBehavior(OxmlBaseElement):
    """
    aaa
    """

    @property
    def common_behavior(self) -> CT_TLCommonBehaviorData:
        """
        aaa
        """

        return getattr(self, qn('p:cBhvr'))

    @property
    def by(self) -> Optional[CT_TLPoint]:
        """
        aaa
        """

        return getattr(self, qn('p:by'), None)

    @property
    def from_(self) -> Optional[CT_TLPoint]:
        """
        aaa
        """

        return getattr(self, qn('p:from'), None)

    @property
    def to(self) -> Optional[CT_TLPoint]:
        """
        aaa
        """

        return getattr(self, qn('p:to'), None)

    @property
    def zoom_contents(self) -> Optional[bool]:
        """
        aaa
        """

        val = self.attrib.get('zoomContents')

        if val is None:
            return None

        return utils.XsdBool(val)


class ST_TLCommandType(ST_BaseEnumType):
    Event = 'evt'
    Call = 'call'
    Verb = 'verb'


class CT_TLCommandBehavior(OxmlBaseElement):
    """
    aaa
    """

    @property
    def common_behavior(self) -> CT_TLCommonBehaviorData:
        """
        aaa
        """

        return getattr(self, qn('p:cBhvr'))

    @property
    def type(self) -> Optional[ST_TLCommandType]:
        """
        aaa
        """

        val = self.attrib.get('type')

        if val is None:
            return None

        return ST_TLCommandType(val)

    @property
    def command(self) -> Optional[str]:
        """
        aaa
        """

        val = self.attrib.get('cmd')

        if val is None:
            return None

        return utils.AnyStrToStr(val)  # type: ignore


class CT_TLSetBehavior(OxmlBaseElement):
    """
    aaa
    """

    @property
    def common_behavior(self) -> CT_TLCommonBehaviorData:
        """
        aaa
        """

        return getattr(self, qn('p:cBhvr'))

    @property
    def to(self) -> Optional[CT_TLAnimVariant]:
        """
        aaa
        """

        return getattr(self, qn('p:to'), None)


class CT_TLCommonMediaNodeData(OxmlBaseElement):
    """
    aaa
    """

    @property
    def common_time_node(self) -> CT_TLCommonTimeNodeData:
        """
        aaa
        """

        return getattr(self, qn('p:cBhvr'))

    @property
    def target_el(self) -> CT_TLTimeTargetElement:
        """
        aaa
        """

        return getattr(self, qn('p:tgtEl'))

    @property
    def vol(self) -> a_ST_PositiveFixedPercentage:
        """
        aaa
        """

        val = self.attrib.get('vol')

        if val is None:
            val = '50%'

        return a_to_ST_PositiveFixedPercentage(str(val))

    @property
    def mute(self) -> bool:
        """
        aaa
        """

        val = self.attrib.get('mute')

        return utils.XsdBool(val, none=False)

    @property
    def num_sld(self) -> int:
        """
        aaa
        """

        val = self.attrib.get('numSld')

        if val is None:
            return 1

        return utils.XsdUnsignedInt(val)

    @property
    def show_when_stopped(self) -> bool:
        """
        aaa
        """

        val = self.attrib.get('showWhenStopped')

        return utils.XsdBool(val, none=True)


class CT_TLMediaNodeAudio(OxmlBaseElement):
    """
    aaa
    """

    @property
    def common_media_node(self) -> CT_TLCommonMediaNodeData:
        """
        aaa
        """

        return getattr(self, qn('p:cMediaNode'))

    @property
    def is_narration(self) -> bool:
        """
        aaa
        """

        val = self.attrib.get('isNarration')

        return utils.XsdBool(val, none=False)


class CT_TLMediaNodeVideo(OxmlBaseElement):
    """
    aaa
    """

    @property
    def common_media_node(self) -> CT_TLCommonMediaNodeData:
        """
        aaa
        """

        return getattr(self, qn('p:cMediaNode'))

    @property
    def full_screen(self) -> bool:
        """
        aaa
        """

        val = self.attrib.get('fullScrn')

        return utils.XsdBool(val, none=False)


class AG_TLBuild(OxmlBaseElement):
    """
    aaa
    """

    @property
    def shape_id(self) -> a_ST_DrawingElementId:
        """
        aaa
        """

        val = utils.AnyStrToStr(self.attrib['spid'])  # type: ignore

        return a_ST_DrawingElementId(int(val))

    @property
    def group_id(self) -> int:
        """
        aaa
        """

        return utils.XsdUnsignedInt(self.attrib['grpId'])

    @property
    def ui_expand(self) -> bool:
        """
        aaa
        """

        val = self.attrib.get('uiExpand')

        return utils.XsdBool(val, none=False)


class CT_TLTemplate(OxmlBaseElement):
    """
    aaa
    """

    @property
    def time_node_lst(self) -> CT_TimeNodeList:
        """
        aaa
        """

        return getattr(self, qn('p:tnLst'))

    @property
    def level(self) -> int:
        """
        aaa
        """

        val = self.attrib['lvl']

        if val is None:
            return 0

        return utils.XsdUnsignedInt(val)


class CT_TLTemplateList(OxmlBaseElement):
    """
    aaa
    """

    @property
    def template_lst(self) -> list[CT_TLTemplate]:
        """
        aaa
        """

        tmpls = self.findall(qn('p:tmpl'))

        if len(tmpls) > 9:
            msg = '最大元素数量应为9'
            raise OxmlElementValidateError(msg)

        return tmpls  # type: ignore


class ST_TLParaBuildType(ST_BaseEnumType):
    """
    aaa
    """

    AllAtOnce = 'allAtOnce'
    P = 'p'
    Cust = 'cust'
    Whole = 'whole'


class CT_TLBuildParagraph(AG_TLBuild):
    """构建段落

    19.5.16 bldP (Build Paragraph)

    此元素指定如何构建段落级别属性。
    """

    @property
    def template_lst(self) -> Optional[CT_TLTemplateList]:
        """
        aaa
        """

        return getattr(self, qn('p:tmplLst'), None)

    @property
    def build(self) -> ST_TLParaBuildType:
        """
        aaa
        """

        val = self.attrib.get('build')

        if val is None:
            return ST_TLParaBuildType.Whole

        return ST_TLParaBuildType(val)

    @property
    def build_level(self) -> int:
        val = self.attrib.get('bldLvl')

        if val is None:
            return 1

        return utils.XsdUnsignedInt(val)

    @property
    def anim_bg(self) -> bool:
        val = self.attrib.get('animBg')

        return utils.XsdBool(val, none=False)

    @property
    def auto_update_anim_bg(self) -> bool:
        val = self.attrib.get('autoUpdateAnimBg')

        return utils.XsdBool(val, none=True)

    @property
    def reverse(self) -> bool:
        """逆转

        Reverse

        此属性仅在段落类型构建中受支持。 这指定了相对于容器中元素的顺序的构建方向。
        当此项设置为“true”时，段落的动画将以与段落本身的顺序相反的顺序保留，以便最后一个段落首先进行动画处理。
        默认值为“False”。
        """
        val = self.attrib.get('rev')

        return utils.XsdBool(val, none=False)

    @property
    def adv_auto(self) -> ST_TLTime:
        val = self.attrib.get('advAuto')

        if val is None:
            val = ST_TLTimeIndefinite.Indefinite.value

        return ST_TLTime(val)


class ST_TLDiagramBuildType(ST_BaseEnumType):
    """
    aaa
    """

    Whole = 'whole'
    DepthByNode = 'depthByNode'
    DepthByBranch = 'depthByBranch'
    BreadthByNode = 'breadthByNode'
    BreadthByLvl = 'breadthByLvl'
    Cw = 'cw'
    CwIn = 'cwIn'
    CwOut = 'cwOut'
    Ccw = 'ccw'
    CcwIn = 'ccwIn'
    CcwOut = 'ccwOut'
    InByRing = 'inByRing'
    OutByRing = 'outByRing'
    Up = 'up'
    Down = 'down'
    AllAtOnce = 'allAtOnce'
    Cust = 'cust'


class CT_TLBuildDiagram(AG_TLBuild):
    """
    aaa
    """

    @property
    def build(self) -> ST_TLDiagramBuildType:
        """
        aaa
        """

        val = self.attrib.get('bld')

        if val is None:
            return ST_TLDiagramBuildType.Whole

        return ST_TLDiagramBuildType(val)


class ST_TLOleChartBuildType(ST_BaseEnumType):
    """
    aaa
    """

    AllAtOnce = 'allAtOnce'
    Series = 'series'
    Category = 'category'
    SeriesEl = 'seriesEl'
    CategoryEl = 'categoryEl'


class CT_TLOleBuildChart(AG_TLBuild):
    """
    aaa
    """

    @property
    def build(self) -> ST_TLOleChartBuildType:
        """
        aaa
        """

        val = self.attrib.get('bld')

        if val is None:
            return ST_TLOleChartBuildType.AllAtOnce

        return ST_TLOleChartBuildType(val)

    @property
    def anim_bg(self) -> bool:
        val = self.attrib.get('animBg')

        return utils.XsdBool(val, none=True)


class CT_TLGraphicalObjectBuild(AG_TLBuild):
    """
    aaa
    """

    @property
    def build(self) -> CT_Empty | a_CT_AnimationGraphicalObjectBuildProperties:
        """
        aaa
        """

        tags = (
            qn('p:bldAsOne'),  # CT_Empty
            qn('p:bldSub'),  # a_CT_AnimationGraphicalObjectBuildProperties
        )

        return self.choice_require_one_child(*tags)  # type: ignore


class CT_BuildList(OxmlBaseElement):
    """
    aaa
    """

    @property
    def build_lst(
        self,
    ) -> list[
        CT_TLBuildParagraph | CT_TLBuildDiagram | CT_TLOleBuildChart | CT_TLGraphicalObjectBuild
    ]:
        tags = (
            qn('p:bldP'),  # CT_TLBuildParagraph
            qn('p:bldDgm'),  # CT_TLBuildDiagram
            qn('p:bldOleChart'),  # CT_TLOleBuildChart
            qn('p:bldGraphic'),  # CT_TLGraphicalObjectBuild
        )

        return self.choice_and_more(*tags)  # type: ignore


class CT_SlideTiming(OxmlBaseElement):
    """幻灯片布局的幻灯片计时信息

    19.3.1.48 timing

    此元素指定处理相应幻灯片中所有动画和定时事件的计时信息。 该信息通过计时元素内的时间节点进行跟踪。 有关这些时间节点的细节以及如何定义它们的更多信息可以在PresentationML框架的动画部分中找到。
    """

    @property
    def time_node_lst(self) -> Optional[CT_TimeNodeList]:
        """时间节点列表"""

        return getattr(self, qn('p:tnLst'), None)

    @property
    def build_lst(self) -> Optional[CT_BuildList]:
        """构建列表"""

        return getattr(self, qn('p:bldLst'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionListModify]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)


class CT_Empty(OxmlBaseElement):
    """
    aaa
    """



class ST_Name(ST_BaseType[AnyStr, str]):
    """
    aaa
    """

    def _validate(self: Self) -> None:
        self._python_val = utils.AnyStrToStr(self._val)


class ST_Index(ST_BaseType[AnyStr, int]):
    """
    aaa
    """

    def _validate(self: Self) -> None:
        value = utils.AnyStrToStr(self._val)

        self._python_val = utils.XsdUnsignedInt(value)


class CT_IndexRange(OxmlBaseElement):
    """幻灯片范围

    19.2.1.38 sldRg

    此元素指定在 html 发布属性和显示属性中使用的幻灯片范围。

    [Note: 这里使用的索引与它们引用的演示文稿幻灯片编号直接相关。 即幻灯片范围必须大于或等于 1，并且小于或等于演示文稿文档中幻灯片的数量。 end note]
    """

    @property
    def start(self) -> ST_Index:
        """该属性定义索引范围的开始."""

        return ST_Index(self.attrib['st'])

    @property
    def end(self) -> ST_Index:
        """该属性定义索引范围的结尾."""

        return ST_Index(self.attrib['end'])


class CT_SlideRelationshipListEntry(OxmlBaseElement):
    """演示文稿幻灯片

    19.2.1.31 sld

    该元素指定幻灯片列表中的一张幻灯片。 幻灯片列表用于指定幻灯片的顺序。
    """

    @property
    def relationship_id(self) -> r_ST_RelationshipId:
        """关系ID"""

        val = utils.AnyStrToStr(self.attrib[qn('r:id')])  # type: ignore

        return r_ST_RelationshipId(val)


class CT_SlideRelationshipList(OxmlBaseElement):
    """演示文稿幻灯片列表

    19.2.1.35 sldLst

    该元素指定演示幻灯片的列表。 演示幻灯片包含特定于单个幻灯片的信息，例如特定于幻灯片的形状和文本信息。
    """

    @property
    def slide_lst(self) -> list[CT_SlideRelationshipListEntry]:
        """演示文稿幻灯片列表

        19.2.1.31 sld

        该元素指定幻灯片列表中的一张幻灯片。 幻灯片列表用于指定幻灯片的顺序。
        """

        return self.findall(qn('p:sld'))  # type: ignore


class CT_CustomShowId(OxmlBaseElement):
    """自定义放映

    19.2.1.5 custShow

    此元素指定自定义演示，它是演示文稿中包含的一组幻灯片的有序列表。

    自定义显示元素允许指定与幻灯片本身存储顺序不同的演示顺序。
    """

    @property
    def id(self) -> int:
        return utils.XsdUnsignedInt(utils.AnyStrToStr(self.attrib['id']))  # type: ignore


class EG_SlideListChoice(OxmlBaseElement):
    """元素组合

    幻灯片列表选择项
    """

    slide_list_choice_tags = (
        qn('p:sldAll'),  # CT_Empty
        qn('p:sldRg'),  # CT_IndexRange
        qn('p:custShow'),  # CT_CustomShowId
    )

    # Union[CT_Empty, CT_IndexRange, CT_CustomShowId]


class CT_CustomerData(OxmlBaseElement):
    """自定义客户数据

    19.3.1.17 custData

    该元素指定客户数据，允许在演示文稿中指定和保留客户特定数据.
    """

    @property
    def relationship_id(self) -> r_ST_RelationshipId:
        """关系ID"""

        val = utils.AnyStrToStr(self.attrib[qn('r:id')])  # type: ignore

        return r_ST_RelationshipId(val)


class CT_TagsData(OxmlBaseElement):
    """客户数据标签

    19.3.1.47 tags

    该元素以标签的形式指定客户数据的存在。 这允许在PresentationML框架内存储客户数据。 虽然这与 ext 标签类似，可以用来存储信息，但该标签主要侧重于引用演示文稿文档的其他部件。 这是通过所有指定标签所需的关系标识属性来完成的。
    """

    @property
    def relationship_id(self) -> r_ST_RelationshipId:
        """关系标识符"""

        val = utils.AnyStrToStr(self.attrib[qn('r:id')])  # type: ignore

        return r_ST_RelationshipId(val)


class CT_CustomerDataList(OxmlBaseElement):
    """自定义客户资料清单

    19.3.1.18 custDataLst

    该元素允许在PresentationML 框架内指定客户定义的数据。 可以在此列表中定义对自定义数据或标签的引用。
    """

    def custom_data(self) -> Optional[CT_CustomerData]:
        """自定义客户数据

        19.3.1.17 custData

        该元素指定客户数据，允许在演示文稿中指定和保留客户特定数据.
        """

        return getattr(self, qn('p:custData'), None)

    def tags(self) -> Optional[CT_TagsData]:
        """客户数据标签

        19.3.1.47 tags

        该元素以标签的形式指定客户数据的存在。 这允许在PresentationML框架内存储客户数据。 虽然这与 ext 标签类似，可以用来存储信息，但该标签主要侧重于引用演示文稿文档的其他部件。 这是通过所有指定标签所需的关系标识属性来完成的。
        """

        return getattr(self, qn('p:tags'), None)


class CT_Extension(OxmlBaseElement):
    """扩展列表

    19.2.1.11 ext

    此元素指定用于将来对 DrawingML 当前版本进行扩展的扩展。 这允许为生成应用程序的更高版本指定当前未知的元素。

    [Note: 该元素无意将过渡模式重新引入严格一致性类。 end note]

    <xsd:complexType name="CT_Extension">
        <xsd:sequence>
            <xsd:any processContents="lax" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
        <xsd:attribute name="uri" type="xsd:token" use="required"/>
    </xsd:complexType>
    """

    @property
    def child_elements(self):
        """子元素节点

        参考: https://stackoverflow.com/questions/27420156/processcontents-strict-vs-lax-vs-skip-for-xsdany
        """
        return self.iterchildren()

    @property
    def uri(self) -> str:
        """统一资源标识符"""

        val = self.attrib['uri']

        return utils.AnyStrToStr(val)  # type: ignore


class EG_ExtensionList(OxmlBaseElement):
    """扩展列表"""

    @property
    def extensions(self) -> list[CT_Extension]:
        """扩展列表

        19.2.1.11 ext

        此元素指定用于将来对 DrawingML 当前版本进行扩展的扩展。 这允许为生成应用程序的更高版本指定当前未知的元素。

        [Note: 该元素无意将过渡模式重新引入严格一致性类。 end note]
        """

        return self.findall(qn('p:ext'))  # type: ignore


class CT_ExtensionList(EG_ExtensionList):
    """
    aaa
    """



class CT_ExtensionListModify(EG_ExtensionList):
    """带有修改标志的扩展列表

    19.3.1.20 extLst

    该元素指定具有修改能力的扩展列表，其中定义了元素类型 ext 的所有未来扩展。 扩展列表以及相应的未来扩展用于扩展PresentationML框架的存储功能。 这允许各种新类型的数据本地存储在框架内。

    [Note: 使用此 extLst 元素允许生成应用程序存储此扩展属性是否已被修改. end note]
    """

    @property
    def mod(self) -> bool:
        """修改/Modify

        此属性指定此元素中包含的数据是否已被修改，因此应由生成应用程序再次处理.
        """

        val = self.attrib.get('mod')

        return utils.XsdBool(val, none=False)


class CT_CommentAuthor(OxmlBaseElement):
    """评论作者"""

    @property
    def ext_lst(self) -> Optional[CT_ExtensionListModify]:
        """带有修改标志的扩展列表

        19.3.1.20 extLst

        该元素指定具有修改能力的扩展列表，其中定义了元素类型 ext 的所有未来扩展。 扩展列表以及相应的未来扩展用于扩展PresentationML框架的存储功能。 这允许各种新类型的数据本地存储在框架内。

        [Note: 使用此 extLst 元素允许生成应用程序存储此扩展属性是否已被修改. end note]
        """

        return getattr(self, qn('p:extLst'), None)

    @property
    def id(self) -> int:
        """
        aaa
        """

        val = self.attrib['id']

        return utils.XsdUnsignedInt(val)

    @property
    def name(self) -> ST_Name:
        """
        aaa
        """

        val = self.attrib['name']

        return ST_Name(val)

    @property
    def initials(self) -> ST_Name:
        """
        aaa
        """

        val = self.attrib['initials']

        return ST_Name(val)

    @property
    def last_idx(self) -> int:
        """
        aaa
        """

        val = self.attrib['lastIdx']

        return utils.XsdUnsignedInt(val)

    @property
    def color_idx(self) -> int:
        """
        aaa
        """

        val = self.attrib['clrIdx']

        return utils.XsdUnsignedInt(val)


class CT_CommentAuthorList(OxmlBaseElement):
    """评论作者名单

    19.4.3 cmAuthorLst (List of Comment Authors)

    该元素指定当前文档中带有注释的作者列表。
    文档中的每条评论均应引用此列表中的作者。
    cmAuthorLst 中的 cmAuthor 元素不得与同一 cmAuthorLst 中的任何其他 cmAuthor 元素具有相同的名称属性值和相同的缩写属性值。

    参考:

    <p:cmAuthorLst>
        <p:cmAuthor id="0" name="Julie Lee" initials="JL" lastIdx="1" clrIdx="0"/>
        <p:cmAuthor id="1" name="Fred Jones" initials="FJ" lastIdx="2" clrIdx="1"/>
    </p:cmAuthorLst>
    """

    @property
    def comment_authors(self) -> list[CT_CommentAuthor]:
        """
        aaa
        """

        return self.findall(qn('p:cmAuthor'))  # type: ignore


class CT_Comment(OxmlBaseElement):
    """
    aaa
    """

    @property
    def point(self) -> a_CT_Point2D:
        """
        aaa
        """

        return getattr(self, qn('p:pos'))

    @property
    def txt(self) -> str:
        """

        aaa

        <xsd:element name="text" type="xsd:string" minOccurs="1" maxOccurs="1"/>
        """

        return getattr(self, qn('p:text')).text

    @property
    def ext_lst(self) -> Optional[CT_ExtensionListModify]:
        """
        aaa
        """

        return getattr(self, qn('p:extLst'), None)

    @property
    def author_id(self) -> int:
        """
        aaa
        """

        val = self.attrib['authorId']

        return utils.XsdUnsignedInt(utils.AnyStrToStr(val))  # type: ignore

    @property
    def date_time(self) -> Optional[XSD_DateTime]:
        """
        aaa
        """

        val = self.attrib.get('dt')

        if val is None:
            return None

        return XSD_DateTime(to_xsd_datetime(val))  # type: ignore

    @property
    def idx(self) -> ST_Index:
        """
        aaa
        """

        val = self.attrib['idx']

        return ST_Index(val)


class CT_CommentList(OxmlBaseElement):
    """评论列表

    19.4.4 cmLst (Comment List)

    该元素指定特定幻灯片的评论列表。

    示例: 一张幻灯片包含两条评论，每条评论均由不同的作者留下。 此示例表明，如果两条评论由不同作者创建，则它们可以具有相同的索引。

    <p:cmLst>
        <p:cm authorId="0" dt="2006-08-28T17:26:44.129" idx="1">
            <p:pos x="10" y="10"/>
            <p:text>Add diagram to clarify.</p:text>
        </p:cm>
        <p:cm authorId="1" dt="2006-08-28T17:44:19.679" idx="1">
            <p:pos x="1426" y="660"/>
            <p:text>Clean up this text.</p:text>
        </p:cm>
    </p:cmLst>
    """

    @property
    def comments(self) -> list[CT_Comment]:
        """
        aaa
        """

        return self.findall(qn('p:cm'))  # type: ignore


class AG_Ole(OxmlBaseElement):
    """
    aaa
    """

    @property
    def name(self) -> str:
        val = self.attrib.get('name')

        if val is None:
            return ''

        return utils.AnyStrToStr(val)  # type: ignore

    @property
    def show_as_icon(self) -> bool:
        val = self.attrib.get('showAsIcon')

        return utils.XsdBool(val, none=False)

    @property
    def relationship_id(self) -> Optional[r_ST_RelationshipId]:
        val = self.attrib.get(qn('r:id'))

        if val is None:
            return None

        val = utils.AnyStrToStr(val)  # type: ignore

        return r_ST_RelationshipId(val)

    @property
    def image_width(self) -> Optional[a_ST_PositiveCoordinate32]:
        """
        aaa
        """
        val = self.attrib.get('imgW')

        if val is None:
            return None

        return a_to_ST_PositiveCoordinate32(val)  # type: ignore

    @property
    def image_height(self) -> Optional[a_ST_PositiveCoordinate32]:
        """
        aaa
        """
        val = self.attrib.get('imgH')

        if val is None:
            return None

        return a_to_ST_PositiveCoordinate32(val)  # type: ignore


class ST_OleObjectFollowColorScheme(ST_BaseEnumType):
    """
    aaa
    """

    Null = 'none'
    Full = 'full'
    TextAndBackground = 'textAndBackground'


class CT_OleObjectEmbed(OxmlBaseElement):
    """
    aaa
    """

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """
        aaa
        """

        return getattr(self, qn('p:extLst'), None)

    @property
    def follow_color_scheme(self) -> ST_OleObjectFollowColorScheme:
        """
        aaa
        """

        val = self.attrib.get('followColorScheme')

        if val is None:
            return ST_OleObjectFollowColorScheme.Null

        return ST_OleObjectFollowColorScheme(val)


class CT_OleObjectLink(OxmlBaseElement):
    """
    aaa
    """

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """
        aaa
        """

        return getattr(self, qn('p:extLst'), None)

    @property
    def update_automatic(self) -> bool:
        """
        aaa
        """

        val = self.attrib.get('updateAutomatic')

        return utils.XsdBool(val, none=False)


class CT_OleObject(AG_Ole):
    """
    aaa
    """

    @property
    def ole_obj(self) -> CT_OleObjectEmbed | CT_OleObjectLink:
        """
        aaa
        """

        tags = (
            qn('p:embed'),  # CT_OleObjectEmbed
            qn('p:link'),  # CT_OleObjectLink
        )

        return self.choice_require_one_child(tags)  # type: ignore

    @property
    def picture(self) -> Optional[CT_Picture]:
        """图片

        19.3.1.37 pic

        该元素指定文档中是否存在图片对象。
        """

        return getattr(self, qn('p:pic'), None)

    @property
    def grog_id(self) -> Optional[str]:
        """
        aaa
        """

        val = self.attrib.get('progId')

        if val is None:
            return None

        return utils.AnyStrToStr(val)  # type: ignore


class CT_Control(AG_Ole):
    """
    aaa
    """

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('p:extLst'), None)

    @property
    def picture(self) -> Optional[CT_Picture]:
        """图片

        19.3.1.37 pic

        该元素指定文档中是否存在图片对象。
        """

        return getattr(self, qn('p:pic'), None)


class CT_ControlList(OxmlBaseElement):
    """控件列表

    该元素指定相应幻灯片的嵌入控件列表。 自定义嵌入控件可以嵌入到幻灯片上。
    """

    @property
    def controls(self) -> list[CT_Control]:
        """控件"""

        return self.findall(qn('p:control'))  # type: ignore


class ST_SlideId(ST_BaseType[AnyStr, int]):
    """
    幻灯片标识符
    """

    def _validate(self: Self) -> None:
        val = utils.XsdUnsignedInt(utils.AnyStrToStr(self._val))

        if not (256 <= val < 2147483648):
            msg = f'预期外的值: {val}'
            raise ValueError(msg)

        self._python_val = val


class CT_SlideIdListEntry(OxmlBaseElement):
    """幻灯片ID

    19.2.1.33 sldId

    此元素指定相应演示文稿中可用的演示文稿幻灯片。 幻灯片包含特定于单个幻灯片的信息，例如特定于幻灯片的形状和文本信息。
    """

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)

    @property
    def id(self) -> ST_SlideId:
        """幻灯片标识符

        指定包含在整个演示文稿中唯一的值的幻灯片标识符.
        """

        return ST_SlideId(self.attrib['id'])

    @property
    def relationship_id(self) -> r_ST_RelationshipId:
        """关系ID

        指定与相应关系文件结合使用的关系标识符，以解析定义此幻灯片的 sld 元素的演示文稿中的位置.
        """

        val = utils.AnyStrToStr(self.attrib[qn('r:id')])  # type: ignore

        return r_ST_RelationshipId(val)


class CT_SlideIdList(OxmlBaseElement):
    """幻灯片ID列表

    19.2.1.34 sldIdLst

    此元素指定相应演示文稿中可用幻灯片的标识信息列表。 幻灯片包含特定于单个幻灯片的信息，例如幻灯片特定的形状和文本信息。
    """

    @property
    def slide_ids(self) -> list[CT_SlideIdListEntry]:
        """幻灯片ID

        19.2.1.33 sldId

        此元素指定相应演示文稿中可用的演示文稿幻灯片。 幻灯片包含特定于单个幻灯片的信息，例如特定于幻灯片的形状和文本信息。
        """

        return self.findall(qn('p:sldId'))  # type: ignore


class ST_SlideMasterId(ST_BaseType[AnyStr, int]):
    """
    aaa
    """

    def _validate(self: Self) -> None:
        """
        <xsd:minInclusive value="2147483648"/>
        """

        val = utils.XsdUnsignedInt(utils.AnyStrToStr(self._val))

        if not val >= 2147483648:
            msg = f'预期外的值: {val}'
            raise ValueError(msg)

        self._python_val = val


class CT_SlideMasterIdListEntry(OxmlBaseElement):
    """幻灯片母板ID

    19.2.1.36 sldMasterId

    此元素指定相应演示文稿中可用的幻灯片母版。 幻灯片母版是专门设计为所有相关子布局幻灯片的模板的幻灯片。
    """

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)

    @property
    def id(self) -> Optional[ST_SlideMasterId]:
        """幻灯片母板标识符

        Slide Master Identifier

        指定幻灯片母版标识符，该标识符将包含在整个演示文稿中唯一的值.
        """

        val = self.attrib.get('id')

        if val is None:
            return None

        return ST_SlideMasterId(val)

    @property
    def relationship_id(self) -> r_ST_RelationshipId:
        """关系ID

        Relationship ID

        指定与相应关系文件结合使用的关系标识符，以解析定义此幻灯片母版的 sldMaster 元素的演示文稿中的位置.
        """

        val = utils.AnyStrToStr(self.attrib[qn('r:id')])  # type: ignore

        return r_ST_RelationshipId(val)


class CT_SlideMasterIdList(OxmlBaseElement):
    """幻灯片母板ID列表

    19.2.1.37 sldMasterIdLst

    此元素指定相应演示文稿中可用的幻灯片母版幻灯片的标识信息列表。 幻灯片母版是专门设计为所有相关子布局幻灯片的模板的幻灯片。
    """

    @property
    def slide_master_ids(self) -> list[CT_SlideMasterIdListEntry]:
        """幻灯片母板ID列表

        19.2.1.36 sldMasterId 幻灯片母板ID

        此元素指定相应演示文稿中可用的幻灯片母版。 幻灯片母版是专门设计为所有相关子布局幻灯片的模板的幻灯片。
        """

        return self.findall(qn('p:sldMasterId'))  # type: ignore


class CT_NotesMasterIdListEntry(OxmlBaseElement):
    """注释母版ID

    19.2.1.20 notesMasterId

    该元素指定相应演示文稿中可用的注释母版。 注释母版是专门为打印幻灯片以及任何附加注释而设计的幻灯片。
    """

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)

    @property
    def relationship_id(self) -> r_ST_RelationshipId:
        """关系标识符

        Relationship Identifier
        """

        val = utils.AnyStrToStr(self.attrib[qn('r:id')])  # type: ignore

        return r_ST_RelationshipId(val)


class CT_NotesMasterIdList(OxmlBaseElement):
    """注释母版幻灯片的标识ID列表

    19.2.1.21 notesMasterIdLst

    此元素指定相应演示文稿中可用的注释母版幻灯片的标识信息列表。 注释母版是专门为打印幻灯片以及任何附加注释而设计的幻灯片。
    """

    @property
    def notes_master_id(self) -> Optional[CT_NotesMasterIdListEntry]:
        """注释母版ID列表

        19.2.1.20 notesMasterId

        该元素指定相应演示文稿中可用的注释母版。 注释母版是专门为打印幻灯片以及任何附加注释而设计的幻灯片。
        """
        return getattr(self, qn('p:notesMasterId'), None)


class CT_HandoutMasterIdListEntry(OxmlBaseElement):
    """讲义母板ID

    19.2.1.14 handoutMasterId

    该元素指定相应演示文稿中可用的讲义母版。 讲义母版是专门为打印讲义而设计的幻灯片。
    """

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)

    @property
    def relationship_id(self) -> r_ST_RelationshipId:
        """关系标识符

        Relationship Identifier
        """

        return r_ST_RelationshipId(utils.AnyStrToStr(self.attrib[qn('r:id')]))  # type: ignore


class CT_HandoutMasterIdList(OxmlBaseElement):
    """讲义母板ID列表

    19.2.1.15 handoutMasterIdLst

    此元素指定相应演示文稿中可用的讲义母版幻灯片的标识信息列表。 讲义母版是专门为打印讲义而设计的幻灯片。
    """

    @property
    def handout_master_id(self) -> Optional[CT_HandoutMasterIdListEntry]:
        """讲义母板ID列表

        19.2.1.14 handoutMasterId

        该元素指定相应演示文稿中可用的讲义母版。 讲义母版是专门为打印讲义而设计的幻灯片。
        """
        return getattr(self, qn('p:handoutMasterId'), None)


class CT_EmbeddedFontDataId(OxmlBaseElement):
    """
    aaa
    """

    @property
    def relationship_id(self) -> r_ST_RelationshipId:
        """
        aaa
        """

        return r_ST_RelationshipId(utils.AnyStrToStr(self.attrib[qn('r:id')]))  # type: ignore


class CT_EmbeddedFontListEntry(OxmlBaseElement):
    """嵌入字体

    19.2.1.9 embeddedFont

    该元素指定嵌入字体。 一旦指定，该字体就可以在演示文稿中使用。

    在字体规范中，指定字体可以有常规、粗体、斜体和粗斜体版本。

    每个字体的实际字体数据都是使用包含所有可用字体链接的关系文件来引用的。

    该字体数据包含要在每个版本的字体中可用的每个字符的字体信息。

    [Note: 并非必须存储字体的所有字符。 由生成应用程序来确定将哪些字符存储在相应的字体数据文件中。 end note]
    """

    @property
    def font(self) -> a_CT_TextFont:
        """嵌入字体

        19.2.1.13 font

        该元素指定描述嵌入字体的特定属性。 一旦指定，该字体就可以在演示文稿中使用。

        在字体规范中，指定字体可以有常规、粗体、斜体和粗斜体版本。

        每个字体的实际字体数据都是使用包含所有可用字体链接的关系文件来引用的。

        该字体数据包含要在每个版本的字体中可用的每个字符的字体信息。

        字体替换逻辑：

        如果指定的字体在用于渲染的系统上不可用，则将利用该元素的属性来选择替代字体。

        [Note: 并非必须存储字体的所有字符。 由生成应用程序来确定将哪些字符存储在相应的字体数据文件中。 end note]

        如果引用嵌入字体（例如第 21.1.2.3.7 节中指定的 latin 元素）的文本正文的标记中的属性与此嵌入字体元素的相应实例的标记中的属性之间存在歧义，则 确定是否使用该嵌入字体是依赖于应用程序的行为。 如果此嵌入字体元素实例的标记中的属性与第 15.2.13 节中指定的相应嵌入字体部分中的属性之间存在歧义，则确定是否使用该嵌入字体是依赖于应用程序的行为。
        """

        return getattr(self, qn('p:font'))

    @property
    def regular(self) -> Optional[CT_EmbeddedFontDataId]:
        """常规嵌入字体

        19.2.1.29 regula

        该元素指定链接到父字体的常规嵌入字体。 一旦指定，给定字体名称的常规版本就可以在演示文稿中使用。 实际的字体数据是使用包含所有可用字体链接的关系文件来引用的。 该字体数据包含每个可用字符的字体信息。

        [Note: 并非必须存储字体的所有字符。 由生成应用程序来确定将哪些字符存储在相应的字体数据文件中。 end note]
        """

        return getattr(self, qn('p:regular'), None)

    @property
    def bold(self) -> Optional[CT_EmbeddedFontDataId]:
        """粗体嵌入字体

        19.2.1.1 bold

        此元素指定链接到父字体的粗体嵌入字体。 一旦指定，给定字体名称的粗体版本即可在演示文稿中使用。

        实际的字体数据是使用包含所有可用字体链接的关系文件来引用的。 该字体数据包含每个可用字符的字体信息。
        """

        return getattr(self, qn('p:bold'), None)

    @property
    def italic(self) -> Optional[CT_EmbeddedFontDataId]:
        """斜体嵌入字体

        19.2.1.16 italic

        该元素指定链接到父字体的斜体嵌入字体。 一旦指定，给定字体名称的斜体版本即可在演示文稿中使用。

        实际的字体数据是使用包含所有可用字体链接的关系文件来引用的。 该字体数据包含每个可用字符的字体信息。
        """

        return getattr(self, qn('p:italic'), None)

    @property
    def bold_italic(self) -> Optional[CT_EmbeddedFontDataId]:
        """粗体斜体嵌入字体

        19.2.1.2 boldItalic

        该元素指定链接到父字体的粗体斜体嵌入字体。 一旦指定，给定字体名称的粗体斜体版本即可在演示文稿中使用。

        实际的字体数据是使用包含所有可用字体链接的关系文件来引用的。 该字体数据包含每个可用字符的字体信息。
        """

        return getattr(self, qn('p:boldItalic'), None)


class CT_EmbeddedFontList(OxmlBaseElement):
    """嵌入字体列表

    19.2.1.10 embeddedFontLst

    该元素指定嵌入在相应演示文稿中的字体列表。 这些字体的字体数据与其他文档部分一起存储在文档容器内。 实际的字体数据在embeddedFont 元素中引用。
    """

    @property
    def embedded_fonts(self) -> list[CT_EmbeddedFontListEntry]:
        """嵌入字体列表

        19.2.1.9 embeddedFont (嵌入字体)

        该元素指定嵌入字体。 一旦指定，该字体就可以在演示文稿中使用。

        在字体规范中，指定字体可以有常规、粗体、斜体和粗斜体版本。

        每个字体的实际字体数据都是使用包含所有可用字体链接的关系文件来引用的。

        该字体数据包含要在每个版本的字体中可用的每个字符的字体信息。
        """

        return self.findall(qn('p:embeddedFont'))  # type: ignore


class CT_SmartTags(OxmlBaseElement):
    """智能标签

    19.2.1.40 smartTags

    此元素指定此文档中存在对智能标记的引用。 [注意：有关智能标记的完整定义（在整个 Office Open XML 中语义相同），请参阅§17.5.1。 尾注] 为了表示智能标记在各个文本运行中的位置，为智能标记应用的每个运行指定了智能标记标识符属性。 这些在 DrawingML 内的运行属性中进一步指定。

    Example:

    <p:presentation>
        …
        <p:smartTags r:id="rId1"/>
    </p:presentation>

    smartTags 元素的存在表明PresentationML 包中存在智能标签信息。 然后检查各个运行的 smtId 属性值，以确定智能标记可能应用的位置，例如:

    <p:txBody>
        <a:bodyPr/>
        <a:lstStyle/>
        <a:p>
            <a:r>
                <a:rPr lang="en-US" dirty="0" smtId="1"/>
                <a:t>CNTS</a:t>
            </a:r>
            <a:endParaRPr lang="en-US" dirty="0"/>
        </a:p>
    </p:txBody>

    在上面的示例中，为该文本运行指定了智能标记标识符 1，以表示应检查文本中的智能标记信息。
    """

    @property
    def relationship_id(self) -> r_ST_RelationshipId:
        """关系ID f f

        关系标识符 / Relationship Identifier

        指定与相应关系文件结合使用的关系标识符，以解析此智能标记的位置.
        """

        val = utils.AnyStrToStr(self.attrib[qn('r:id')])  # type: ignore

        return r_ST_RelationshipId(val)


class CT_CustomShow(OxmlBaseElement):
    """自定义放映列表

    19.2.1.6 custShow

    此元素指定自定义放映，定义幻灯片显示的特定幻灯片顺序。这允许呈现同一组幻灯片的许多变体。
    """

    @property
    def slide_lst(self) -> Optional[CT_SlideRelationshipList]:
        """演示文稿幻灯片列表

        19.2.1.35 sldLst

        该元素指定演示幻灯片的列表。 演示幻灯片包含特定于单个幻灯片的信息，例如特定于幻灯片的形状和文本信息。
        """

        return getattr(self, qn('p:sldLst'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)

    @property
    def name(self) -> ST_Name:
        """自定义放映名称"""

        return ST_Name(self.attrib['name'])

    @property
    def id(self) -> int:
        """自定义放映ID"""

        return int(self.attrib['id'])


class CT_CustomShowList(OxmlBaseElement):
    """自定义放映列表

    19.2.1.7 custShowLst

    此元素指定相应演示文稿中可用的所有自定义节目的列表。 自定义放映是定义的幻灯片序列，允许以任意顺序显示幻灯片和演示文稿。
    """

    @property
    def cust_show_lst(self) -> list[CT_CustomShow]:
        """自定义放映列表

        19.2.1.6 custShow

        此元素指定自定义放映，定义幻灯片显示的特定幻灯片顺序。这允许呈现同一组幻灯片的许多变体。
        """

        return self.findall(qn('p:custShow'))  # type: ignore


class ST_PhotoAlbumLayout(ST_BaseEnumType):
    """
    aaa
    """

    FitToSlide = 'fitToSlide'
    OnePic = '1pic'
    TwoPic = '2pic'
    FourPic = '4pic'
    OnePicTitle = '1picTitle'
    ThowPicTitle = '2picTitle'
    FourPicTitle = '4picTitle'


class ST_PhotoAlbumFrameShape(ST_BaseEnumType):
    """
    aaa
    """

    FrameStyle1 = 'frameStyle1'
    FrameStyle2 = 'frameStyle2'
    FrameStyle3 = 'frameStyle3'
    FrameStyle4 = 'frameStyle4'
    FrameStyle5 = 'frameStyle5'
    FrameStyle6 = 'frameStyle6'
    FrameStyle7 = 'frameStyle7'


class CT_PhotoAlbum(OxmlBaseElement):
    """相册信息

    19.2.1.24 photoAlbum

    该元素指定相应的演示文稿包含相册。 相册指定演示文稿中分布在一张或多张幻灯片上的图像列表，所有幻灯片共享一致的布局。 相册中的每张图片都采用一致的风格。 此功能使应用程序能够一起管理所有图像并作为一组修改它们的顺序、布局和格式。

    该元素不会对单个相册图像强制执行指定的属性； 相反，它指定默认情况下应应用于所有相册图像及其包含的幻灯片的通用设置。 作为相册一部分的图像通过图片定义中是否存在 isPhoto 元素来标识。
    """

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)

    @property
    def black_white(self) -> bool:
        """黑与白"""

        val = self.attrib.get('bw')

        return utils.XsdBool(val, none=False)

    @property
    def show_captions(self) -> bool:
        """显示/隐藏字幕"""

        val = self.attrib.get('showCaptions')

        return utils.XsdBool(val, none=False)

    @property
    def layout(self) -> ST_PhotoAlbumLayout:
        """相册布局类型"""

        val = self.attrib.get('layout')

        if val is None:
            return ST_PhotoAlbumLayout.FitToSlide

        return ST_PhotoAlbumLayout(val)

    @property
    def frame(self) -> ST_PhotoAlbumFrameShape:
        """框架类型."""

        val = self.attrib.get('frame')

        if val is None:
            return ST_PhotoAlbumFrameShape.FrameStyle1

        return ST_PhotoAlbumFrameShape(val)


class ST_SlideSizeCoordinate(ST_BaseType[AnyStr, int]):
    """
    幻灯片尺寸坐标
    """

    def _validate(self: Self) -> None:
        val = utils.XsdUnsignedInt(utils.AnyStrToStr(self._val))

        if not (914400 <= val < 51206400):
            msg = f'预期外的值: {val}'
            raise ValueError(msg)

        self._python_val = val


class ST_SlideSizeType(ST_BaseEnumType):
    """
    aaa
    """

    Screen4x3 = 'screen4x3'
    Letter = 'letter'
    A4 = 'A4'
    ThirtyFiveMm = '35mm'
    Overhead = 'overhead'
    Banner = 'banner'
    Custom = 'custom'
    Ledger = 'ledger'
    A3 = 'A3'
    B4ISO = 'B4ISO'
    B5ISO = 'B5ISO'
    B4JIS = 'B4JIS'
    B5JIS = 'B5JIS'
    HagakiCard = 'hagakiCard'
    Screen16x9 = 'screen16x9'
    Screen16x10 = 'screen16x10'


class CT_SlideSize(OxmlBaseElement):
    """演示文稿幻灯片的尺寸

    19.2.1.39 sldSz

    该元素指定演示文稿幻灯片表面的大小。 演示幻灯片中的对象可以在这些范围之外指定，但这是演示或打印幻灯片时显示的背景表面的大小。

    考虑以下对演示文稿幻灯片大小的指定。

    <p:presentation xmlns:a="…" xmlns:r="…" xmlns:p="…" embedTrueTypeFonts="1">
        …
        <p:sldSz cx="9144000" cy="6858000" type="screen4x3"/>
        …
    </p:presentation>

    """

    @property
    def cx(self) -> ST_SlideSizeCoordinate:
        """范围长度

        也就是 宽度  Extent Length

        指定 EMU 中矩形范围的长度。 该矩形应指示显示的对象的大小（对原始对象进行任何缩放的结果）.
        """
        val = self.attrib['cx']

        return ST_SlideSizeCoordinate(val)

    @property
    def cy(self) -> ST_SlideSizeCoordinate:
        """范围高度

        Extent Width

        指定 EMU 中范围矩形的宽度。 该矩形应指示显示的对象的大小（对原始对象进行任何缩放的结果）。
        """
        val = self.attrib['cy']

        return ST_SlideSizeCoordinate(val)

    @property
    def type(self) -> ST_SlideSizeType:
        """尺寸类型

        指定应使用的幻灯片尺寸类型。 这特别确定了本次演示的预期交付平台.

        默认为cust
        """

        val = self.attrib.get('type')

        if val is None:
            return ST_SlideSizeType.Custom

        return ST_SlideSizeType(val)


class CT_Kinsoku(OxmlBaseElement):
    """避头尾设置

    19.2.1.17 kinsoku

    此元素指定演示文稿范围的避头尾设置，用于定义相应演示文稿中东亚文本的换行行为。
    """

    @property
    def language(self) -> Optional[str]:
        """语言/Language"""

        val = self.attrib.get('lang')

        if val is None:
            return None

        return utils.AnyStrToStr(val)  # type: ignore

    @property
    def inval_st_chars(self) -> Optional[str]:
        """无效的避头尾起始字符/Invalid Kinsoku Start Characters"""

        val = self.attrib.get('invalStChars')

        if val is None:
            return None

        return utils.AnyStrToStr(val)  # type: ignore

    @property
    def inval_end_chars(self) -> Optional[str]:
        """无效的避头尾结束字符/Invalid Kinsoku End Characters"""

        val = self.attrib.get('invalEndChars')

        if val is None:
            return None

        return utils.AnyStrToStr(val)  # type: ignore


class ST_BookmarkIdSeed(ST_BaseType[AnyStr, int]):
    """
    aaa
    """

    def _validate(self: Self) -> None:
        val = utils.XsdUnsignedInt(utils.AnyStrToStr(self._val))

        if 1 <= val < 2147483648:
            self._python_val = val

        msg = f'预期外的值: {val}'
        raise ValueError(msg)


class CT_ModifyVerifier(OxmlBaseElement):
    """19.2.1.19 modifyVerifier (修改验证器)

    此元素指定已应用于PresentationML 文档的写保护设置。 写保护是指不得修改文档内容，并且不得使用相同的文件名重新保存文档的模式。

    如果存在，应用程序应需要密码才能修改文档。 如果提供的密码与该属性中的哈希值不匹配，则应启用写保护。 如果省略该元素，则不对当前文档应用写保护。 由于此保护不会对文档进行加密，因此恶意应用程序可能会规避其使用。

    提供给算法的密码是 UTF-16LE 编码的字符串； 长度超过 510 个八位位组的字符串将被截断为 510 个八位位组。 如果编码密码中存在前导 BOM 字符 (U+FEFF)，则会在哈希计算之前将其删除。 该元素的属性指定用于验证用户提供的密码的算法。
    """

    @property
    def algorithm_name(self) -> Optional[str]:
        """
        加密算法名称
        """

        val = self.attrib.get('algorithmName')

        if val is None:
            return None

        return utils.AnyStrToStr(val)  # type: ignore

    @property
    def hash_value(self) -> Optional[str]:
        """
        密码哈希值

        指定编辑此图表表所需的密码的哈希值。 该值应与使用前面属性和父 XML 元素指定的算法对用户提供的密码进行哈希处理后得到的哈希值进行比较，如果两个值匹配，则不再强制实施保护。.

        如果省略此值，则reservationPassword属性应包含工作簿的密码散列.

        <xsd:attribute name="hashValue" type="xsd:base64Binary" use="optional"/>
        """

        val = self.attrib.get('hashValue')

        if val is None:
            return None

        return utils.AnyStrToStr(val)  # type: ignore

    @property
    def salt_value(self) -> Optional[str]:
        """码验证器的盐值

        指定在使用前面的属性值定义的散列算法对用户提供的密码进行散列以生成 hashValue 属性之前添加到用户提供的密码的盐，并且在尝试生成散列之前也应将其添加到用户提供的密码的前面 比较值。 盐是一个随机字符串，在对其进行哈希处理之前添加到用户提供的密码中，以防止恶意方预先计算所有可能的密码/哈希组合并简单地使用这些预先计算的值（通常称为 “字典攻击”）.

        如果省略此属性，则在对用户提供的密码进行哈希处理以与存储的哈希值进行比较之前，不应在用户提供的密码前添加盐。.

        <xsd:attribute name="saltValue" type="xsd:base64Binary" use="optional"/>
        """

        val = self.attrib.get('saltValue')

        if val is None:
            return None

        return utils.AnyStrToStr(val)  # type: ignore

    @property
    def spin_value(self) -> Optional[int]:
        """运行哈希算法的迭代

        指定在尝试比较哈希函数时应迭代运行的次数（使用每次迭代的结果加上包含迭代编号作为下一次迭代的输入的 4 字节值（从 0 开始，小端）来运行） 用户提供的密码以及存储在 hashValue 属性中的值.

        [Rationale: 多次运行算法会相应增加穷举搜索攻击的成本。 存储该值允许迭代次数随着时间的推移而增加，以适应更快的硬件（因此能够在更短的时间内运行更多迭代）。 end rationale]
        """

        val = self.attrib.get('spinValue')

        if val is None:
            return None

        return utils.XsdUnsignedInt(val)  # type: ignore


class CT_Presentation(OxmlBaseElement):
    """演示文稿

    19.2.1.26 presentation (Presentation)

    该元素指定了在演示文稿范围内的基本属性。

    This element specifies within it fundamental presentation-wide properties.

    示例: 考虑以下包含一个幻灯片母版和两张幻灯片的演示文稿。 除了这些常用元素之外，还可以指定其他属性，例如幻灯片大小、注释大小和默认文本样式。

    <p:presentation
        xmlns:a="…"
        xmlns:r="…"
        xmlns:p="…">
        <p:sldMasterIdLst>
            <p:sldMasterId id="2147483648" r:id="rId1"/>
        </p:sldMasterIdLst>
        <p:sldIdLst>
            <p:sldId id="256" r:id="rId3"/>
            <p:sldId id="257" r:id="rId4"/>
        </p:sldIdLst>
        <p:sldSz cx="9144000" cy="6858000" type="screen4x3"/>
        <p:notesSz cx="6858000" cy="9144000"/>

        <p:defaultTextStyle>
        …
        </p:defaultTextStyle>
    </p:presentation>
    """

    @property
    def slide_master_id_lst(self) -> Optional[CT_SlideMasterIdList]:
        """可用的幻灯片母版ID列表

        19.2.1.37 sldMasterIdLst

        此元素指定相应演示文稿中可用的幻灯片母版幻灯片的标识信息列表。 幻灯片母版是专门设计为所有相关子布局幻灯片的模板的幻灯片。
        """

        return getattr(self, qn('p:sldMasterIdLst'), None)

    @property
    def notes_master_id_lst(self) -> Optional[CT_NotesMasterIdList]:
        """注释母版幻灯片的标识ID列表

        19.2.1.21 notesMasterIdLst

        此元素指定相应演示文稿中可用的注释母版幻灯片的标识信息列表。 注释母版是专门为打印幻灯片以及任何附加注释而设计的幻灯片。
        """

        return getattr(self, qn('p:notesMasterIdLst'), None)

    @property
    def handout_master_id_lst(self) -> Optional[CT_HandoutMasterIdList]:
        """讲义母板ID列表

        19.2.1.15 handoutMasterIdLst

        此元素指定相应演示文稿中可用的讲义母版幻灯片的标识信息列表。 讲义母版是专门为打印讲义而设计的幻灯片。
        """

        return getattr(self, qn('p:handoutMasterIdLst'), None)

    @property
    def slide_id_lst(self) -> Optional[CT_SlideIdList]:
        """幻灯片ID列表

        19.2.1.34 sldIdLst

        此元素指定相应演示文稿中可用幻灯片的标识信息列表。 幻灯片包含特定于单个幻灯片的信息，例如幻灯片特定的形状和文本信息。
        """

        return getattr(self, qn('p:sldIdLst'), None)

    @property
    def slide_size(self) -> Optional[CT_SlideSize]:
        """演示文稿幻灯片的尺寸

        19.2.1.39 sldSz

        该元素指定演示文稿幻灯片表面的大小。 演示幻灯片中的对象可以在这些范围之外指定，但这是演示或打印幻灯片时显示的背景表面的大小。
        """

        return getattr(self, qn('p:sldSz'), None)

    @property
    def notes_size(self) -> Optional[a_CT_PositiveSize2D]:
        """笔记和讲义的尺寸大小

        19.2.1.22 notesSz

        此元素指定用于笔记幻灯片和讲义幻灯片的幻灯片表面的大小。 笔记幻灯片中的对象可以在这些范围之外指定，但笔记幻灯片在呈现或打印时具有指定大小的背景表面。 此元素旨在指定应用程序可能选择生成的任何特殊格式的打印输出（例如大纲讲义）中适合的内容区域。
        """

        return getattr(self, qn('p:notesSz'), None)

    @property
    def smart_tags(self) -> Optional[CT_SmartTags]:
        """对智能标记的引用

        19.2.1.40 smartTags

        此元素指定此文档中存在对智能标记的引用。 [注意：有关智能标记的完整定义（在整个 Office Open XML 中语义相同），请参阅§17.5.1。 尾注] 为了表示智能标记在各个文本运行中的位置，为智能标记应用的每个运行指定了智能标记标识符属性。 这些在 DrawingML 内的运行属性中进一步指定。
        """

        return getattr(self, qn('p:smartTags'), None)

    @property
    def embedded_font_lst(self) -> Optional[CT_EmbeddedFontList]:
        """嵌入字体列表

        19.2.1.10 embeddedFontLst

        该元素指定嵌入在相应演示文稿中的字体列表。 这些字体的字体数据与其他文档部分一起存储在文档容器内。 实际的字体数据在embeddedFont 元素中引用。
        """

        return getattr(self, qn('p:embeddedFontLst'), None)

    @property
    def cust_show_lst(self) -> Optional[CT_CustomShowList]:
        """自定义放映列表

        19.2.1.7 custShowLst

        此元素指定相应演示文稿中可用的所有自定义节目的列表。 自定义放映是定义的幻灯片序列，允许以任意顺序显示幻灯片和演示文稿。
        """

        return getattr(self, qn('p:custShowLst'), None)

    @property
    def photo_album(self) -> Optional[CT_PhotoAlbum]:
        """相册信息

        19.2.1.24 photoAlbum

        该元素指定相应的演示文稿包含相册。 相册指定演示文稿中分布在一张或多张幻灯片上的图像列表，所有幻灯片共享一致的布局。 相册中的每张图片都采用一致的风格。 此功能使应用程序能够一起管理所有图像并作为一组修改它们的顺序、布局和格式。

        该元素不会对单个相册图像强制执行指定的属性； 相反，它指定默认情况下应应用于所有相册图像及其包含的幻灯片的通用设置。 作为相册一部分的图像通过图片定义中是否存在 isPhoto 元素来标识。
        """

        return getattr(self, qn('p:photoAlbum'), None)

    @property
    def cust_data_lst(self) -> Optional[CT_CustomerDataList]:
        """自定义数据列表

        19.3.1.18 custDataLst

        该元素允许在PresentationML 框架内指定客户定义的数据。 可以在此列表中定义对自定义数据或标签的引用。
        """

        return getattr(self, qn('p:custDataLst'), None)

    @property
    def kinsoku(self) -> Optional[CT_Kinsoku]:
        """避头尾设置

        19.2.1.17 kinsoku

        此元素指定演示文稿范围的避头尾设置，用于定义相应演示文稿中东亚文本的换行行为。
        """

        return getattr(self, qn('p:kinsoku'), None)

    @property
    def default_text_style(self) -> Optional[a_CT_TextListStyle]:
        """演示文稿默认文本样式

        19.2.1.8 defaultTextStyle

        该元素指定演示文稿中使用的默认文本样式

        如果该幻灯片未与母版幻灯片关联，或者没有为演示文稿幻灯片中的文本指定样式信息，则在插入新幻灯片时可以引用此处定义的文本样式。

        <xsd:element name="defaultTextStyle" type="a:CT_TextListStyle" minOccurs="0" maxOccurs="1"/>
        """

        # 即便类型属于 a:CT_TextListStyle 但名称还在当前命名空间中！！！
        return getattr(self, qn('p:defaultTextStyle'), None)

    @property
    def modify_verifier(self) -> Optional[CT_ModifyVerifier]:
        """
        修改验证器

        19.2.1.19 modifyVerifier

        此元素指定已应用于PresentationML 文档的写保护设置。 写保护是指不得修改文档内容，并且不得使用相同的文件名重新保存文档的模式。

        如果存在，应用程序应需要密码才能修改文档。 如果提供的密码与该属性中的哈希值不匹配，则应启用写保护。 如果省略该元素，则不对当前文档应用写保护。 由于此保护不会对文档进行加密，因此恶意应用程序可能会规避其使用。

        提供给算法的密码是 UTF-16LE 编码的字符串； 长度超过 510 个八位位组的字符串将被截断为 510 个八位位组。 如果编码密码中存在前导 BOM 字符 (U+FEFF)，则会在哈希计算之前将其删除。 该元素的属性指定用于验证用户提供的密码的算法。
        """

        return getattr(self, qn('p:modifyVerifier'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展列表

        该元素指定扩展列表，在其中定义元素类型 ext 的所有未来扩展。 扩展列表以及相应的未来扩展用于扩展PresentationML框架的存储功能。 这允许各种新类型的数据本地存储在框架内。
        """

        return getattr(self, qn('p:extLst'), None)

    @property
    def server_zoom(self) -> a_ST_Percentage:
        """服务器缩放

        Server Zoom

        指定将演示文稿嵌入到另一个文档中时要使用的缩放比例。 嵌入的幻灯片将按此百分比缩放。
        """

        val = self.attrib.get('serverZoom', '50%')

        return a_to_ST_Percentage(str(val))

    @property
    def first_slide_num(self) -> int:
        """第一张幻灯片编号

        First Slide Number

        指定演示文稿中的第一张幻灯片编号。
        """

        val = self.attrib.get('firstSlideNum')

        if val is None:
            return 1

        return int(val)

    @property
    def show_special_pls_on_title_slide(self) -> bool:
        """在标题上显示页眉和页脚占位符

        Show Header and Footer Placeholders on Titles

        指定是否在标题幻灯片上显示页眉和页脚占位符。
        """

        val = self.attrib.get('showSpecialPlsOnTitleSld')

        return utils.XsdBool(val, none=True)

    @property
    def right_to_left(self) -> bool:
        """从右到左视窗

        Right-To-Left Views

        指定用户界面的当前视图是从右到左还是从左到右。
        如果该值设置为 true，则视图为从右到左，否则为从左到右。
        """

        val = self.attrib.get('rtl')

        return utils.XsdBool(val, none=False)

    @property
    def remove_personal_info_on_save(self) -> bool:
        """保存时删除个人信息

        Remove Personal Information on Save

        指定保存演示文档时是否自动删除个人信息。
        """

        val = self.attrib.get('removePersonalInfoOnSave')

        return utils.XsdBool(val, none=False)

    @property
    def compat_mode(self) -> bool:
        """兼容模式

        Compatibility Mode

        指定生成的应用程序是否处于兼容模式，该模式用于通知用户在使用旧格式时出现任何内容或功能丢失。
        """

        val = self.attrib.get('compatMode')

        return utils.XsdBool(val, none=False)

    @property
    def strict_first_and_last_chars(self) -> bool:
        """严格的第一个和最后一个字符

        Strict First and Last Characters

        指定是否对日语文本的起始行和结束行使用严格字符。
        """

        val = self.attrib.get('strictFirstAndLastChars')

        return utils.XsdBool(val, none=True)

    @property
    def embed_true_type_fonts(self) -> bool:
        """嵌入 True Type 字体

        Embed True Type Fonts

        指定生成应用程序是否应自动嵌入 True Type 字体。
        """

        val = self.attrib.get('embedTrueTypeFonts')

        return utils.XsdBool(val, none=False)

    @property
    def save_subset_fonts(self) -> bool:
        """保存字体子集

        Save Subset Fonts

        指定在嵌入字体时仅保存演示文稿中使用的字符子集。
        """

        val = self.attrib.get('saveSubsetFonts')

        return utils.XsdBool(val, none=False)

    @property
    def auto_compress_pictures(self) -> bool:
        """自动压缩图片

        Automatically Compress Pictures

        指定生成应用程序是否应自动压缩此演示文稿的所有图片。
        """

        val = self.attrib.get('autoCompressPictures')

        return utils.XsdBool(val, none=True)

    @property
    def bookmark_id_seed(self) -> ST_BookmarkIdSeed:
        """书签 ID 种子

        Bookmark ID Seed

        指定用于生成书签 ID 的种子，以确保 ID 在整个文档中保持唯一。
        该值指定用作下一个创建的新书签的 ID 的数字。
        """

        val = self.attrib.get('bookmarkIdSeed')

        if val is None:
            val = '1'

        return ST_BookmarkIdSeed(val)

    @property
    def conformance(self) -> s_ST_ConformanceClass:
        """文档一致性类别

        Document Conformance Class

        指定PresentationML 文档符合的一致性类别(§2.1)。

        如果省略该属性，则其默认值是过渡性的。

        [示例: 考虑以下PresentationML 演示文稿部件标签:

        <p:presentation conformance="strict">
        …
        </p:presentation>

        该文档的一致性属性值为 strict，因此它符合 PML Strict 一致性类别。]

        """

        val = self.attrib.get('conformance')

        if val is None:
            val = '1'

        return s_ST_ConformanceClass(val)  # type: ignore


class CT_HtmlPublishProperties(EG_SlideListChoice):
    """
    aaa
    """

    def slide_list_choice(self) -> CT_Empty | CT_IndexRange | CT_CustomShowId:
        """
        aaa

        <xsd:group ref="EG_SlideListChoice" minOccurs="1" maxOccurs="1"/>
        """

        return self.choice_require_one_child(*self.slide_list_choice_tags)  # type: ignore

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """
        aaa
        """

        return getattr(self, qn('p:extLst'), None)

    @property
    def show_speaker_notes(self) -> bool:
        """
        aaa
        """

        val = self.attrib.get('showSpeakerNotes')

        return utils.XsdBool(val, none=True)

    @property
    def target(self) -> Optional[str]:
        """
        aaa
        """

        val = self.attrib.get('target')

        if val is None:
            return None

        return utils.AnyStrToStr(val)  # type: ignore

    @property
    def title(self) -> Optional[str]:
        """
        aaa
        """

        val = self.attrib.get('target')

        if val is None:
            return ''

        return utils.AnyStrToStr(val)  # type: ignore

    @property
    def relationship_id(self) -> r_ST_RelationshipId:
        """
        aaa
        """

        val = utils.AnyStrToStr(self.attrib[qn('r:id')])  # type: ignore

        return r_ST_RelationshipId(val)


class ST_PrintWhat(ST_BaseEnumType):
    """
    aaa
    """

    Slides = 'slides'
    Handouts1 = 'handouts1'
    Handouts2 = 'handouts2'
    Handouts3 = 'handouts3'
    Handouts4 = 'handouts4'
    Handouts6 = 'handouts6'
    Handouts9 = 'handouts9'
    Notes = 'notes'
    Outline = 'outline'


class ST_PrintColorMode(ST_BaseEnumType):
    """
    aaa
    """

    BlackAndWhite = 'bw'
    Gray = 'gray'
    Color = 'clr'


class CT_PrintProperties(OxmlBaseElement):
    """打印特性

    19.2.1.28 prnPr (打印属性)

    该元素指定与该演示文稿文档关联的默认打印属性。
    """

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)

    @property
    def print_whate(self) -> ST_PrintWhat:
        """打印输出

        指定内容布局方面的默认打印输出.
        """

        val = self.attrib.get('prnWhat')

        if val is None:
            return ST_PrintWhat.Slides

        return ST_PrintWhat(val)

    @property
    def color_mode(self) -> ST_PrintColorMode:
        """打印色彩模式

        指定打印时要使用的颜色模式
        """

        val = self.attrib.get('clrMode')

        if val is None:
            return ST_PrintColorMode.Color

        return ST_PrintColorMode(val)

    @property
    def hidden_slides(self) -> bool:
        """打印隐藏幻灯片

        指定是否应打印隐藏的幻灯片.
        """

        val = self.attrib.get('hiddenSlides')

        return utils.XsdBool(val, none=False)

    @property
    def scale_to_fit_paper(self) -> bool:
        """打印时缩放以适合纸张

        指定是否应缩放打印输出以适合所使用的纸张
        """

        val = self.attrib.get('scaleToFitPaper')

        return utils.XsdBool(val, none=False)

    @property
    def frame_slides(self) -> bool:
        """打印时框架滑动

        指定打印时是否应将幻灯片加框。 加框后，会为每张幻灯片打印轮廓边框.
        """

        val = self.attrib.get('frameSlides')

        return utils.XsdBool(val, none=False)


class CT_ShowInfoBrowse(OxmlBaseElement):
    """
    aaa
    """

    @property
    def show_scrollbar(self) -> bool:
        """
        aaa
        """

        val = self.attrib.get('showScrollbar')

        return utils.XsdBool(val, none=True)


class CT_ShowInfoKiosk(OxmlBaseElement):
    """
    aaa
    """

    @property
    def restart(self) -> int:
        """
        aaa
        """

        val = self.attrib.get('restart')

        if val is None:
            val = '300000'

        return utils.XsdUnsignedInt(val)


class EG_ShowType(OxmlBaseElement):
    """元素组合, 放映类型"""

    show_type_tags = (
        qn('p:present'),  # CT_Empty  # 19.2.1.25 present (演示者幻灯片放映模式)
        qn('p:browse'),  # CT_ShowInfoBrowse
        qn('p:kiosk'),  # CT_ShowInfoKiosk
    )

    # Optional[Union[CT_Empty, CT_ShowInfoBrowse, CT_ShowInfoKiosk]]


class CT_ShowProperties(EG_ShowType, EG_SlideListChoice):
    """演示文稿级别的放映属性

    19.2.1.30 showPr

    该元素充当父元素，其中包含所有演示范围的显示属性。 所有属性及其相应的设置都在子元素中定义。
    """

    def show_type(
        self,
    ) -> Optional[CT_Empty | CT_ShowInfoBrowse | CT_ShowInfoKiosk]:
        """
        aaa

        <xsd:group ref="EG_ShowType" minOccurs="0" maxOccurs="1"/>
        """

        return self.choice_one_child(*self.show_type_tags)  # type: ignore

    def slide_list_choice(
        self,
    ) -> Optional[CT_Empty | CT_IndexRange | CT_CustomShowId]:
        """
        aaa

        <xsd:group ref="EG_SlideListChoice" minOccurs="0" maxOccurs="1"/>
        """

        return self.choice_one_child(*self.slide_list_choice_tags)  # type: ignore

    @property
    def pen_color(self) -> Optional[a_CT_Color]:
        """
        aaa
        """

        return getattr(self, qn('p:penClr'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)

    @property
    def loop(self) -> bool:
        """循环幻灯片放映

        指定幻灯片放映是否应设置为在末尾循环播放。
        """

        val = self.attrib.get('loop')

        return utils.XsdBool(val, none=False)

    @property
    def show_narration(self) -> bool:
        """在幻灯片放映中显示旁白

        指定演示时是否应播放幻灯片旁白.
        """

        val = self.attrib.get('showNarration')

        return utils.XsdBool(val, none=False)

    @property
    def show_nnimation(self) -> bool:
        """在幻灯片放映中显示动画

        指定演示时是否应显示幻灯片放映动画
        """

        val = self.attrib.get('showAnimation')

        return utils.XsdBool(val, none=True)

    @property
    def use_timings(self) -> bool:
        """在幻灯片放映中使用计时

        指定在演示时是否应使用幻灯片过渡计时来推进幻灯片.
        """

        val = self.attrib.get('useTimings')

        return utils.XsdBool(val, none=True)


class CT_PresentationProperties(OxmlBaseElement):
    """演示文稿维度的属性

    19.2.1.27 presentationPr (Presentation-wide Properties)

    该元素充当父元素，其中包含额外的演示文稿范围内的文档属性。 所有属性及其相应的设置都在其子元素中定义。
    """

    @property
    def print_properties(self) -> Optional[CT_PrintProperties]:
        """打印特性

        19.2.1.28 prnPr (打印属性)

        该元素指定与该演示文稿文档关联的默认打印属性。
        """

        return getattr(self, qn('p:prnPr'), None)

    @property
    def show_properties(self) -> Optional[CT_ShowProperties]:
        """演示文稿级别的放映属性

        19.2.1.30 showPr

        该元素充当父元素，其中包含所有演示范围的显示属性。 所有属性及其相应的设置都在子元素中定义。
        """

        return getattr(self, qn('p:showPr'), None)

    @property
    def color_mru(self) -> Optional[a_CT_ColorMRU]:
        """彩色MRU

        19.2.1.4 clrMru

        这指定了演示文稿中最近使用的用户选择的颜色。 此列表包含演示文稿主题颜色之外的自定义用户选择颜色，使应用程序能够公开这些附加颜色选择以便于重用。 列表中的第一项是最近使用的颜色。
        """

        return getattr(self, qn('p:clrMru'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)


class CT_HeaderFooter(OxmlBaseElement):
    """幻灯片母版的页眉/页脚信息

    19.3.1.25 hf

    此元素指定幻灯片的页眉和页脚信息。 页眉和页脚由文本占位符组成，这些文本应在所有幻灯片和幻灯片类型中保持一致，例如日期和时间、幻灯片编号以及自定义页眉和页脚文本。
    """

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)

    @property
    def slide_num(self) -> bool:
        """幻灯片编号占位符

        指定是否启用幻灯片编号占位符。 如果未指定此属性，则生成应用程序应假定值为 true.
        """

        val = self.attrib.get('sldNum')

        return utils.XsdBool(val, none=True)

    @property
    def header(self) -> bool:
        """标题占位符

        指定是否为此母版启用标头占位符。 如果未指定此属性，则生成应用程序应假定值为 true.
        """

        val = self.attrib.get('hdr')

        return utils.XsdBool(val, none=True)

    @property
    def footer(self) -> bool:
        """页脚占位符

        指定是否为此母版启用页脚占位符。 如果未指定此属性，则生成应用程序应假定值为 true.
        """

        val = self.attrib.get('ftr')

        return utils.XsdBool(val, none=True)

    @property
    def dt(self) -> bool:
        """日期/时间占位符

        指定是否为此母版启用日期/时间占位符。 如果未指定此属性，则生成应用程序应假定值为 true.
        """

        val = self.attrib.get('dt')

        return utils.XsdBool(val, none=True)


class ST_PlaceholderType(ST_BaseEnumType):
    """指定占位符应包含的内容类型。"""

    Title = 'title'
    """包含幻灯片标题，允许在幻灯片、布局和幻灯片母板模板中使用；可以是水平或垂直的"""

    Body = 'body'
    """包含正文文本，允许在幻灯片、布局、幻灯片母板模板、备注和备注母板模板中使用；可以是水平或垂直的"""

    CtrTitle = 'ctrTitle'
    """包含一个标题，应居中显示在幻灯片上，允许在幻灯片和布局中使用"""

    SubTitle = 'subTitle'
    """包含副标题，允许在幻灯片和布局中使用"""

    Dt = 'dt'
    """包含日期和时间，允许在幻灯片、布局、幻灯片母板模板、备注、备注母板模板和讲义母板模板中使用"""

    SldNum = 'sldNum'
    """包含幻灯片的编号，允许在幻灯片、布局、幻灯片母板模板、备注、备注母板模板和讲义母板模板中使用"""

    Ftr = 'ftr'
    """包含用作页脚的文本，允许在幻灯片、布局、幻灯片母板模板、备注、备注母板模板和讲义母板模板中使用"""

    Hdr = 'hdr'
    """包含用作页眉的文本，允许在备注、备注母板模板和讲义母板模板中使用"""

    Obj = 'obj'
    """包含任何内容类型，允许在幻灯片和布局中使用"""

    Chart = 'chart'
    """包含图表或图形，允许在幻灯片和布局中使用"""

    Tbl = 'tbl'
    """包含表格，允许在幻灯片和布局中使用"""

    ClipArt = 'clipArt'
    """包含单个剪贴画图像，允许在幻灯片和布局中使用"""

    Dgm = 'dgm'
    """包含图表，允许在幻灯片和布局中使用"""

    Media = 'media'
    """包含多媒体内容，如音频或电影，允许在幻灯片和布局中使用"""

    SldImg = 'sldImg'
    """包含幻灯片的图像，允许在备注和备注母板模板中使用"""

    Pic = 'pic'
    """包含图片，允许在幻灯片和布局中使用"""


class ST_PlaceholderSize(ST_BaseEnumType):
    """占位符大小

    19.7.9 ST_PlaceholderSize

    这种简单的类型有助于存储占位符的大小。 该尺寸是相对于母版上的正文占位符来描述的。

    此简单类型的内容是 W3C XML 架构令牌数据类型的限制。

    此简单类型仅限于下表中列出的值：

    - full (全部)	指定占位符应采用母版上正文占位符的完整大小。
    - half (一半)	指定占位符应采用母版上主体占位符大小的一半。 垂直或水平半尺寸？ 需要一张图片。
    - quarter (四分之一)	指定占位符应采用母版上正文占位符大小的四分之一。 图片会有帮助
    """

    Full = 'full'
    Half = 'half'
    Quarter = 'quarter'


class CT_Placeholder(OxmlBaseElement):
    """占位符形状

    19.3.1.36 ph

    该元素指定相应的形状应由生成应用程序表示为占位符。 当生成应用程序将形状视为占位符时，它可以具有特殊属性来提醒用户可以将内容输入到形状中。 允许使用不同的占位符类型，并且可以使用此元素的占位符类型属性来指定不同的占位符类型。

    """

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)

    @property
    def type(self) -> ST_PlaceholderType:
        """占位符类型

        指定占位符要包含的内容类型.
        """

        val = self.attrib.get('type')

        if val is None:
            return ST_PlaceholderType.Body  # 默认为正文

        return ST_PlaceholderType(val)

    @property
    def orient(self) -> ST_Direction:
        """占位符方向

        指定占位符的方向.
        """

        val = self.attrib.get('orient')

        if val is None:
            return ST_Direction.Horz

        return ST_Direction(val)

    @property
    def size(self) -> ST_PlaceholderSize:
        """占位符大小

        指定占位符的大小.
        """

        val = self.attrib.get('sz')

        if val is None:
            return ST_PlaceholderSize.Full

        return ST_PlaceholderSize(val)

    @property
    def idx(self) -> int:
        """占位符索引

        指定占位符索引。 在应用模板或更改布局以将一个模板/母版上的占位符与另一个模板/母版上的占位符匹配时使用此选项.
        """

        val = self.attrib.get('idx')

        if val is None:
            val = '0'

        return utils.XsdUnsignedInt(val)

    @property
    def has_custom_prompt(self) -> bool:
        """占位符有自定义提示

        指定相应的占位符是否应该有自定义提示.
        """

        val = self.attrib.get('hasCustomPrompt')

        return utils.XsdBool(val, none=False)


class CT_ApplicationNonVisualDrawingProps(a_EG_media):
    """非视觉属性

    19.3.1.33 nvPr

    该元素指定对象的非视觉属性。 这些属性包括与对象相关联的多媒体内容以及指示如何在不同上下文中使用或显示该对象的属性。
    """

    @property
    def placeholder(self) -> Optional[CT_Placeholder]:
        """占位符

        19.3.1.36 ph (占位符形状)

        该元素指定相应的形状应由生成应用程序表示为占位符。 当生成应用程序将形状视为占位符时，它可以具有特殊属性来提醒用户可以将内容输入到形状中。 允许使用不同的占位符类型，并且可以使用此元素的占位符类型属性来指定不同的占位符类型。
        """

        return getattr(self, qn('p:ph'), None)

    @property
    def media(
        self,
    ) -> Optional[
        a_CT_AudioCD | a_CT_EmbeddedWAVAudioFile | a_CT_AudioFile | a_CT_VideoFile | a_CT_QuickTimeFile
    ]:
        """aaa

        <xsd:group ref="a:EG_Media" minOccurs="0" maxOccurs="1"/>
        """

        return self.choice_one_child(*self.media_tags)  # type: ignore

    @property
    def cust_data_lst(self) -> Optional[CT_CustomerDataList]:
        """自定义数据列表"""

        return getattr(self, qn('p:custDataLst'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)

    @property
    def is_photo(self) -> bool:
        """是否为相册

        指定图片是否属于相册，因此在生成应用程序中编辑相册时应将其包含在内.
        """

        val = self.attrib.get('isPhoto')

        return utils.XsdBool(val, none=False)

    @property
    def user_drawn(self) -> bool:
        """是否为用户绘制的

        指定相应的对象是否已由用户绘制，因此不应被删除。 这允许标记包含用户绘制数据的幻灯片.
        """

        val = self.attrib.get('userDrawn')

        return utils.XsdBool(val, none=False)


class CT_ShapeNonVisual(OxmlBaseElement):
    """形状的非视觉属性

    19.3.1.34 nvSpPr

    该元素指定形状的所有非视觉属性。 该元素是与形状关联的非视觉识别属性、形状属性和应用程序属性的容器。 这允许存储不影响形状外观的附加信息。
    """

    @property
    def c_nv_pr(self) -> a_CT_NonVisualDrawingProps:
        """非可视绘图属性

        20.1.2.2.8 cNvPr

        该元素指定非可视画布属性。 这允许存储不影响图片外观的附加信息。
        """

        return getattr(self, qn('p:cNvPr'))

    @property
    def c_nv_sp_pr(self) -> a_CT_NonVisualDrawingShapeProps:
        """形状的非可视绘图属性

        19.3.1.13 cNvSpPr

        该元素指定形状的非可视绘图属性。 生成应用程序将使用这些属性来确定如何处理形状
        """

        return getattr(self, qn('p:cNvSpPr'))

    @property
    def nv_pr(self) -> CT_ApplicationNonVisualDrawingProps:
        """非视觉属性

        19.3.1.33 nvPr

        该元素指定对象的非视觉属性。 这些属性包括与对象相关联的多媒体内容以及指示如何在不同上下文中使用或显示该对象的属性。
        """

        return getattr(self, qn('p:nvPr'))


class CT_Shape(OxmlBaseElement):
    """形状

    19.3.1.43 sp

    该元素指定单个形状的存在。 形状可以是使用 DrawingML 框架定义的预设几何图形或自定义几何图形。 除了几何形状之外，每个形状还可以附加视觉和非视觉属性。 文本和相应的样式信息也可以附加到形状。 该形状与形状树或组形状元素中的所有其他形状一起指定。

    [Note: 形状是在幻灯片上指定文本的首选机制. end note]
    """

    @property
    def nv_sp_pr(self) -> CT_ShapeNonVisual:
        """形状的非视觉属性

        19.3.1.34 nvSpPr

        该元素指定形状的所有非视觉属性。 该元素是与形状关联的非视觉识别属性、形状属性和应用程序属性的容器。 这允许存储不影响形状外观的附加信息。
        """

        return getattr(self, qn('p:nvSpPr'))

    @property
    def sp_pr(self) -> a_CT_ShapeProperties:
        """形状特性

        19.3.1.44 spPr

        此元素指定可应用于形状的视觉形状属性。 这些属性包括形状填充、轮廓、几何形状、效果和 3D 方向。
        """

        return getattr(self, qn('p:spPr'))

    @property
    def style(self) -> Optional[a_CT_ShapeStyle]:
        """形状样式

        19.3.1.46 style

        该元素指定形状的样式信息。 这用于根据主题的样式矩阵定义的预设样式来定义形状的外观。
        """

        return getattr(self, qn('p:style'), None)

    @property
    def text_body(self) -> Optional[a_CT_TextBody]:
        """形状文本正文

        19.3.1.51 txBody

        该元素指定相应形状中是否存在要包含的文本。 所有可见文本和可见文本相关属性都包含在此元素内。 可以有多个段落，并且段落内可以有多个文本段。
        """

        return getattr(self, qn('p:txBody'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionListModify]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)

    @property
    def use_bg_fill(self) -> bool:
        """使用背景填充

        指定形状填充应设置为幻灯片背景表面的形状填充.

        [Note: 此属性不会将形状的填充设置为透明，而是将其设置为用直接位于其后面的幻灯片背景部分进行填充. end note]
        """

        val = self.attrib.get('useBgFill')

        return utils.XsdBool(val, none=False)


class CT_ConnectorNonVisual(OxmlBaseElement):
    """连接形状的非视觉属性

    19.3.1.29 nvCxnSpPr

    该元素指定连接形状的所有非视觉属性。 该元素是与连接形状关联的非视觉识别属性、形状属性和应用程序属性的容器。 这允许存储不影响连接形状外观的附加信息。
    """

    @property
    def c_nv_pr(self) -> a_CT_NonVisualDrawingProps:
        """非可视绘图属性

        20.1.2.2.8 cNvPr

        该元素指定非可视画布属性。 这允许存储不影响图片外观的附加信息。
        """

        return getattr(self, qn('p:cNvPr'))

    @property
    def c_nv_cxn_sp_pr(self) -> a_CT_NonVisualConnectorProperties:
        """非可视连接器形状绘图属性

        19.3.1.8 cNvCxnSpPr

        此元素指定特定于连接器形状的非可视绘图属性。 这包括指定连接器形状所连接的形状的信息。
        """

        return getattr(self, qn('p:cNvCxnSpPr'))

    @property
    def nv_pr(self) -> CT_ApplicationNonVisualDrawingProps:
        """非视觉属性

        19.3.1.33 nvPr

        该元素指定对象的非视觉属性。 这些属性包括与对象相关联的多媒体内容以及指示如何在不同上下文中使用或显示该对象的属性。
        """

        return getattr(self, qn('p:nvPr'))


class CT_Connector(OxmlBaseElement):
    """连接形状

    19.3.1.19 cxnSp

    该元素指定用于连接两个 sp 元素的连接形状。 使用 cxnSp 指定连接后，生成应用程序将确定连接器采用的确切路径。 也就是说，连接器路由算法由生成的应用程序决定，因为所需的路径可能会根据应用程序的特定需求而有所不同。
    """

    @property
    def nv_cxn_sp_pr(self) -> CT_ConnectorNonVisual:
        """连接形状的非视觉属性

        19.3.1.29 nvCxnSpPr

        该元素指定连接形状的所有非视觉属性。 该元素是与连接形状关联的非视觉识别属性、形状属性和应用程序属性的容器。 这允许存储不影响连接形状外观的附加信息。
        """

        return getattr(self, qn('p:nvCxnSpPr'))

    @property
    def sp_pr(self) -> a_CT_ShapeProperties:
        """
        形状特性

        19.3.1.44 spPr

        此元素指定可应用于形状的视觉形状属性。 这些属性包括形状填充、轮廓、几何形状、效果和 3D 方向。
        """

        return getattr(self, qn('p:spPr'))

    @property
    def style(self) -> Optional[a_CT_ShapeStyle]:
        """形状样式

        19.3.1.46 style

        该元素指定形状的样式信息。 这用于根据主题的样式矩阵定义的预设样式来定义形状的外观。
        """

        return getattr(self, qn('p:style'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionListModify]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)


class CT_PictureNonVisual(OxmlBaseElement):
    """图片的非视觉属性

    19.3.1.32 nvPicPr

    该元素指定图片的所有非视觉属性。 该元素是与图片关联的非视觉识别属性、形状属性和应用程序属性的容器。 这允许存储不影响图片外观的附加信息。
    """

    @property
    def c_nv_pr(self) -> a_CT_NonVisualDrawingProps:
        """非可视绘图属性

        20.1.2.2.8 cNvPr

        该元素指定非可视画布属性。 这允许存储不影响图片外观的附加信息。
        """

        return getattr(self, qn('p:cNvPr'))

    @property
    def c_nv_pic_pr(self) -> a_CT_NonVisualPictureProperties:
        """非视觉绘图属性

        19.3.1.11 cNvPicPr

        该元素指定图片画布的非视觉属性。 生成应用程序将使用这些属性来确定如何更改所讨论的图片对象的某些属性。
        """

        return getattr(self, qn('p:cNvPicPr'))

    @property
    def nv_pr(self) -> CT_ApplicationNonVisualDrawingProps:
        """非视觉属性

        19.3.1.33 nvPr

        该元素指定对象的非视觉属性。 这些属性包括与对象相关联的多媒体内容以及指示如何在不同上下文中使用或显示该对象的属性。
        """

        return getattr(self, qn('p:nvPr'))


class CT_Picture(OxmlBaseElement):
    """图片

    19.3.1.37 pic

    该元素指定文档中是否存在图片对象。
    """

    @property
    def nv_pic_pr(self) -> CT_PictureNonVisual:
        """图片的非视觉属性

        19.3.1.32 nvPicPr

        该元素指定图片的所有非视觉属性。 该元素是与图片关联的非视觉识别属性、形状属性和应用程序属性的容器。 这允许存储不影响图片外观的附加信息。
        """

        return getattr(self, qn('p:nvPicPr'))

    @property
    def blip_fill(self) -> a_CT_BlipFillProperties:
        """图片填充

        19.3.1.4 blipFill

        该元素指定图片对象具有的图片填充类型。 由于默认情况下图片已具有图片填充，因此可以为图片对象指定两种填充。
        """

        return getattr(self, qn('p:blipFill'))

    @property
    def sp_pr(self) -> a_CT_ShapeProperties:
        """形状特性

        19.3.1.44 spPr

        此元素指定可应用于形状的视觉形状属性。 这些属性包括形状填充、轮廓、几何形状、效果和 3D 方向。
        """

        return getattr(self, qn('p:spPr'))

    @property
    def style(self) -> a_CT_ShapeStyle:
        """形状样式

        19.3.1.46 style

        该元素指定形状的样式信息。 这用于根据主题的样式矩阵定义的预设样式来定义形状的外观。
        """

        return getattr(self, qn('p:style'))

    @property
    def ext_lst(self) -> Optional[CT_ExtensionListModify]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)


class CT_GraphicalObjectFrameNonVisual(OxmlBaseElement):
    """图形框架的非视觉属性

    19.3.1.30 nvGraphicFramePr

    该元素指定图形框架的所有非视觉属性。 该元素是与图形框架关联的非视觉识别属性、形状属性和应用程序属性的容器。 这允许存储不影响图形框架的外观的附加信息。
    """

    @property
    def c_nv_pr(self) -> a_CT_NonVisualDrawingProps:
        """非可视绘图属性

        19.3.1.12 cNvPr

        该元素指定非可视画布属性。 这允许存储不影响图片外观的附加信息。
        """

        return getattr(self, qn('p:cNvPr'))

    @property
    def c_nv_graphic_frame_pr(self) -> a_CT_NonVisualGraphicFrameProperties:
        """非可视图形框架绘图属性

        19.3.1.9 cNvGraphicFramePr

        该元素指定图形框架的非可视绘图属性。 这些非视觉属性是生成应用程序在渲染幻灯片表面时将使用的属性。
        """

        return getattr(self, qn('p:cNvGraphicFramePr'))

    @property
    def nv_pr(self) -> CT_ApplicationNonVisualDrawingProps:
        """非视觉属性

        19.3.1.33 nvPr

        该元素指定对象的非视觉属性。 这些属性包括与对象相关联的多媒体内容以及指示如何在不同上下文中使用或显示该对象的属性。
        """

        return getattr(self, qn('p:nvPr'))


class CT_GraphicalObjectFrame(OxmlBaseElement):
    """图框

    19.3.1.21 graphicFrame

    该元素指定图形框架的存在。 该框架包含由外部源生成的图形，并且需要一个容器来在幻灯片表面上显示。
    """

    @property
    def nv_graphic_frame_pr(self) -> CT_GraphicalObjectFrameNonVisual:
        """图形框架的非视觉属性

        19.3.1.30 nvGraphicFramePr

        该元素指定图形框架的所有非视觉属性。 该元素是与图形框架关联的非视觉识别属性、形状属性和应用程序属性的容器。 这允许存储不影响图形框架的外观的附加信息。
        """

        return getattr(self, qn('p:nvGraphicFramePr'))

    @property
    def xfrm(self) -> a_CT_Transform2D:
        """图形框架的 2D 变换

        19.3.1.53 xfrm

        该元素指定要应用于相应图形框架的变换。 此变换应用于图形框架，就像应用于形状或组形状一样。
        """

        return getattr(self, qn('p:xfrm'))

    @property
    def graphic(self) -> a_CT_GraphicalObject:
        """图形对象

        20.1.2.2.16 graphic

        该元素指定单个图形对象的存在。 当文档作者希望保留某种图形对象时，应该引用此元素。
        该图形对象的规范完全由文档作者提供，并在 GraphicData 子元素中引用.
        """

        # return getattr(self, qn("p:graphic"))
        return getattr(self, qn('a:graphic'))

    @property
    def ext_lst(self) -> Optional[CT_ExtensionListModify]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)

    @property
    def bw_mode(self) -> Optional[a_ST_BlackWhiteMode]:
        """黑白模式

        指定如何使用颜色、黑色或白色或灰度来渲染图形对象.

        [Note: 这并不意味着图形对象本身仅存储黑白或灰度信息。 该属性设置图形对象使用的渲染模式. end note]
        """

        val = self.attrib.get('bwMode')

        if val is None:
            return None

        return a_ST_BlackWhiteMode(val)


class CT_GroupShapeNonVisual(OxmlBaseElement):
    """组合形状的非视觉属性

    19.3.1.31 nvGrpSpPr

    该元素指定组形状的所有非视觉属性。 该元素是与组形状关联的非视觉识别属性、形状属性和应用程序属性的容器。 这允许存储不影响组形状外观的附加信息。
    """

    @property
    def c_nv_pr(self) -> a_CT_NonVisualDrawingProps:
        """非可视绘图属性

        20.1.2.2.8 cNvPr

        该元素指定非可视画布属性。 这允许存储不影响图片外观的附加信息。
        """

        return getattr(self, qn('p:cNvPr'))

    @property
    def c_nv_grp_sp_pr(self) -> a_CT_NonVisualGroupDrawingShapeProps:
        """非可视组形状绘图属性

        20.1.2.2.6 cNvGrpSpPr

        此元素指定组形状的非可视绘图属性。 这些非视觉属性是生成应用程序在渲染幻灯片表面时将使用的属性。
        """

        return getattr(self, qn('p:cNvGrpSpPr'))

    @property
    def nv_pr(self) -> CT_ApplicationNonVisualDrawingProps:
        """非视觉属性

        19.3.1.33 nvPr

        该元素指定对象的非视觉属性。 这些属性包括与对象相关联的多媒体内容以及指示如何在不同上下文中使用或显示该对象的属性。
        """

        return getattr(self, qn('p:nvPr'))


class CT_GroupShape(OxmlBaseElement):
    """组合形状

    19.3.1.22 grpSp

    该元素指定一个组形状，表示组合在一起的许多形状。 该形状应被视为规则形状，但不是由单个几何形状来描述，而是由其中包含的所有形状几何形状组成。 在组形状中，组成该组的每个形状都按照通常的方式指定。 然而，对元素进行分组的想法是，单个变换可以同时应用于多个形状。
    """

    @property
    def nv_grp_sp_pr(self) -> CT_GroupShapeNonVisual:
        """组合形状的非视觉属性

        19.3.1.31 nvGrpSpPr

        该元素指定组形状的所有非视觉属性。 该元素是与组形状关联的非视觉识别属性、形状属性和应用程序属性的容器。 这允许存储不影响组形状外观的附加信息。
        """

        return getattr(self, qn('p:nvGrpSpPr'))

    @property
    def grp_sp_pr(self) -> a_CT_GroupShapeProperties:
        """组合形状特性

        19.3.1.23 grpSpPr

        该元素指定相应组内所有形状所共有的属性。 如果组形状属性和单个形状属性之间存在任何冲突属性，则应优先考虑单个形状属性。
        """

        return getattr(self, qn('p:grpSpPr'))

    @property
    def shape_lst(
        self,
    ) -> list[
        CT_Shape | CT_GroupShape | CT_GraphicalObjectFrame | CT_Connector | CT_Picture | CT_Rel | CT_MC_AlternateContent
    ]:
        """
        aaa

        <xsd:choice minOccurs="0" maxOccurs="unbounded">
        """

        tags = (
            qn('p:sp'),  # CT_Shape
            qn('p:grpSp'),  # CT_GroupShape
            qn('p:graphicFrame'),  # CT_GraphicalObjectFrame
            qn('p:cxnSp'),  # CT_Connector
            qn('p:pic'),  # CT_Picture
            qn('p:contentPart'),  # CT_Rel
            qn('mc:AlternateContent'),  # CT_MC_AlternateContent
        )

        return self.choice_and_more(*tags)  # type: ignore

    @property
    def ext_lst(self) -> Optional[CT_ExtensionListModify]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)


class CT_Rel(OxmlBaseElement):
    """内容部分

    19.3.1.14 contentPart

    此元素指定对 XML 内容的引用，其格式未由 ECMA-376 定义。

    这部分允许本机使用其他常用的交换格式，例如：

    - MathML (http://www.w3.org/TR/MathML2/)
    - SMIL (http://www.w3.org/TR/REC-smil/)
    - SVG (http://www.w3.org/TR/SVG11/)
    """

    @property
    def relationship_id(self) -> r_ST_RelationshipId:
        """关系ID

        指定内容部件的关系 ID.
        """

        val = utils.AnyStrToStr(self.attrib[qn('r:id')])  # type: ignore

        return r_ST_RelationshipId(val)


class EG_TopLevelSlide(OxmlBaseElement):
    """顶级幻灯片的标签合集"""

    @property
    def color_map(self) -> a_CT_ColorMapping:
        """配色方案

        19.3.1.6 clrMap

        此元素指定将一种颜色方案定义转换为另一种颜色方案定义的映射层。 每个属性代表一个在这个master中可以引用的颜色名称，其值为主题中对应的颜色。
        """

        return getattr(self, qn('p:clrMap'))


class EG_ChildSlide(OxmlBaseElement):
    """幻灯片公共元素"""

    @property
    def color_map_override(self) -> Optional[a_CT_ColorMappingOverride]:
        """颜色映射覆盖方案

        19.3.1.7 clrMapOvr

        该元素提供了一种机制，用于覆盖 ClrMap 元素中列出的颜色方案。

        如果 masterClrMapping 元素存在，则使用 master 定义的配色方案。

        如果 overrideClrMapping 元素存在，它将定义特定于父笔记幻灯片、演示文稿幻灯片或幻灯片布局的新配色方案。
        """

        return getattr(self, qn('p:clrMapOvr'), None)


class AG_ChildSlide(OxmlBaseElement):
    """子幻灯片属性

    19.3.1.26 notes (Notes Slide)

    19.3.1.39 sldLayout (Slide Layout)
    """

    @property
    def show_master_shape(self) -> bool:
        """显示母板形状

        Show Master Shapes

        指定母板(master)幻灯片上的形状是否在幻灯片上显示

        Specifies if shapes on the master slide should be shown on slides or not.
        """

        val = self.attrib.get('showMasterSp')

        return utils.XsdBool(val, none=True)

    @property
    def show_master_ph_anim(self) -> bool:
        """显示母板占位符形状动画

        Show Master Placeholder Animations

        指定是否显示母版幻灯片的占位符上的动画。

        Specifies whether or not to display animations on placeholders from the master slide.
        """

        val = self.attrib.get('showMasterPhAnim')

        return utils.XsdBool(val, none=True)


class CT_BackgroundProperties(a_EG_FillProperties, a_EG_EffectProperties):
    """背景特性

    19.3.1.2 bgPr

    该元素指定用于渲染幻灯片背景的视觉效果。 这包括构成幻灯片背景的任何填充、图像或效果。
    """

    @property
    def fill(
        self,
    ) -> a_CT_NoFillProperties | a_CT_SolidColorFillProperties | a_CT_GradientFillProperties | a_CT_BlipFillProperties | a_CT_PatternFillProperties | a_CT_GroupFillProperties:
        """
        填充样式

        <xsd:group ref="a:EG_FillProperties" minOccurs="1" maxOccurs="1"/>
        """

        return self.choice_require_one_child(*self.fill_pr_tags)  # type: ignore

    @property
    def effect(self) -> Optional[a_CT_EffectList | a_CT_EffectContainer]:
        """
        效果样式

        <xsd:group ref="a:EG_EffectProperties" minOccurs="0" maxOccurs="1"/>
        """

        return self.choice_one_child(*self.effect_pr_tags)  # type: ignore

    @property
    def ext_lst(self) -> Optional[CT_ExtensionListModify]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)

    @property
    def shade_to_title(self) -> bool:
        """阴影到标题

        指定幻灯片的背景是否为标题背景类型的阴影。 这种渐变填充位于幻灯片背景上，并根据幻灯片标题占位符的位置而变化。
        """

        val = self.attrib.get('shadeToTitle')

        return utils.XsdBool(val, none=False)


class EG_Background(OxmlBaseElement):
    """背景通用属性

    <xsd:group name="EG_Background">
        <xsd:choice> <!--maxOccurs 和 minOccurs 默认为 1-->
            <xsd:element name="bgPr" type="CT_BackgroundProperties"/>
            <xsd:element name="bgRef" type="a:CT_StyleMatrixReference"/>
        </xsd:choice>
    </xsd:group>
    """

    @property
    def background_pr(
        self,
    ) -> CT_BackgroundProperties | a_CT_StyleMatrixReference:
        """背景特性

        19.3.1.2 bgPr

        该元素指定用于渲染幻灯片背景的视觉效果。 这包括构成幻灯片背景的任何填充、图像或效果。

        19.3.1.3 bgRef 背景样式参考

        该元素指定幻灯片背景使用样式矩阵中定义的填充样式。

        idx 属性指的是背景填充样式或演示文稿样式矩阵中的填充样式的索引，由 fmtScheme 元素定义。

        值 0 或 1000 表示无背景，值 1-999 指 fillStyleLst 元素内的填充样式的索引，

        值 1001 及以上指 bgFillStyleLst 元素内的背景填充样式的索引。

        值 1001 对应于第一个背景填充样式，1002 对应于第二个背景填充样式，依此类推。
        """

        tags = (
            qn('p:bgPr'),  # CT_BackgroundProperties
            qn('p:bgRef'),  # a_CT_StyleMatrixReference
        )

        return self.choice_one_child(*tags)  # type: ignore


class CT_Background(EG_Background):
    """幻灯片背景

    19.3.1.1 bg

    此元素指定幻灯片的背景
    """

    @property
    def bw_mode(self) -> a_ST_BlackWhiteMode:
        """黑白模式

        指定应仅使用黑色和白色来渲染背景。 也就是说，在渲染图片时，背景的颜色信息应该转换为黑色或白色.

        [Note: 渲染此背景时不使用灰色，仅使用纯黑和纯白. end note]
        """

        val = self.attrib.get('bwMode')

        if val is None:
            return a_ST_BlackWhiteMode.White

        return a_ST_BlackWhiteMode(val)


class CT_CommonSlideData(OxmlBaseElement):
    """通用幻灯片数据

    19.3.1.16 cSld

    此元素指定与所有幻灯片类型相关的幻灯片信息的容器。 所有幻灯片共享一组独立于幻灯片类型的通用属性； 任何特定幻灯片的这些属性的描述都存储在幻灯片的 cSld 容器中。 特定于父元素指示的幻灯片类型的幻灯片数据存储在其他地方。

    [Note: cSld 中的实际数据仅描述特定的父幻灯片； 它只是所有幻灯片中通用的存储信息类型。 end note]
    """

    @property
    def background(self) -> Optional[CT_Background]:
        """幻灯片背景

        19.3.1.1 bg

        此元素指定幻灯片的背景外观信息。 幻灯片背景覆盖整个幻灯片，在不存在对象的情况下可见，并作为透明对象的背景。
        """

        return getattr(self, qn('p:bg'), None)

    @property
    def shape_tree(self) -> CT_GroupShape:
        """形状树

        19.3.1.45 spTree

        此元素指定可以在给定幻灯片上引用的所有基于形状的对象（无论是否分组）。 由于幻灯片中的大多数对象都是形状，因此这代表了幻灯片中的大部分内容。 文本和效果附加到 spTree 元素中包含的形状。
        """

        return getattr(self, qn('p:spTree'))

    @property
    def cust_data_lst(self) -> Optional[CT_CustomerDataList]:
        """自定义数据列表

        19.3.1.18 custDataLst

        该元素允许在PresentationML 框架内指定客户定义的数据。 可以在此列表中定义对自定义数据或标签的引用。
        """

        return getattr(self, qn('p:custDataLst'), None)

    @property
    def controls(self) -> Optional[CT_ControlList]:
        """控件列表

        19.3.1.15 controls

        该元素指定相应幻灯片的嵌入控件列表。 自定义嵌入控件可以嵌入到幻灯片上。
        """

        return getattr(self, qn('p:controls'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)

    @property
    def name(self) -> str:
        """幻灯片名称

        该属性用于进一步标识公共幻灯片数据的这种唯一配置。 这可能用于帮助区分不同的幻灯片布局或各种其他幻灯片类型.

        默认值: ''
        """

        val = self.attrib.get('name')

        if val is None:
            val = ''

        return utils.AnyStrToStr(val)  # type: ignore


class CT_Slide(EG_ChildSlide, AG_ChildSlide):
    """演示幻灯片

    19.3.1.38 sld (Presentation Slide)

    此元素是幻灯片部件 (§13.3.8) 的根元素，并指定幻灯片的实例。
    幻灯片中包含描述演示文稿幻灯片中的对象及其相应格式的所有元素。
    子元素描述常见的幻灯片元素，例如形状及其附加的文本主体、特定于该幻灯片的过渡和时间以及特定于该幻灯片的颜色信息。

    [示例: 考虑下面的基本幻灯片。

    <p:sld>
        <p:cSld>
            <p:spTree>
            …
            </p:spTree>
        </p:cSld>
        <p:clrMapOver>
        …
        </p:clrMapOver>
        <p:transition>
        …
        </p:transition>
        <p:timing>
        …
        </p:timing>
    </p:sld>

    此示例显示了一张幻灯片，其内容位于形状树中、本地颜色映射覆盖以及带有关联计时信息的幻灯片过渡。 ]
    """

    @property
    def common_slide_data(self) -> CT_CommonSlideData:
        """通用幻灯片数据

        19.3.1.16 cSld

        此元素指定与所有幻灯片类型相关的幻灯片信息的容器。 所有幻灯片共享一组独立于幻灯片类型的通用属性； 任何特定幻灯片的这些属性的描述都存储在幻灯片的 cSld 容器中。 特定于父元素指示的幻灯片类型的幻灯片数据存储在其他地方。

        [Note: cSld 中的实际数据仅描述特定的父幻灯片； 它只是所有幻灯片中通用的存储信息类型。 end note]
        """

        return getattr(self, qn('p:cSld'))

    @property
    def transition(self) -> Optional[CT_SlideTransition]:
        """幻灯片布局的幻灯片过渡

        19.3.1.50 transition

        此元素指定用于从上一张幻灯片过渡到当前幻灯片的幻灯片过渡类型。 也就是说，转换信息存储在转换完成后出现的幻灯片上。
        """

        return getattr(self, qn('p:transition'), None)

    @property
    def timing(self) -> Optional[CT_SlideTiming]:
        """幻灯片布局的幻灯片计时信息

        19.3.1.48 timing

        此元素指定处理相应幻灯片中所有动画和定时事件的计时信息。 该信息通过计时元素内的时间节点进行跟踪。 有关这些时间节点的细节以及如何定义它们的更多信息可以在PresentationML框架的动画部分中找到。
        """

        return getattr(self, qn('p:timing'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionListModify]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)

    @property
    def show(self) -> bool:
        """是否显示"""

        val = self.attrib.get('show')

        return utils.XsdBool(val, none=True)


class ST_SlideLayoutType(ST_BaseEnumType):
    """
    aaa
    """

    Title = 'title'
    Tx = 'tx'
    TwoColTx = 'twoColTx'
    Tbl = 'tbl'
    TxAndChart = 'txAndChart'
    ChartAndTx = 'chartAndTx'
    Dgm = 'dgm'
    Chart = 'chart'
    TxAndClipArt = 'txAndClipArt'
    ClipArtAndTx = 'clipArtAndTx'
    TitleOnly = 'titleOnly'
    Blank = 'blank'
    TxAndObj = 'txAndObj'
    ObjAndTx = 'objAndTx'
    ObjOnly = 'objOnly'
    Obj = 'obj'
    TxAndMedia = 'txAndMedia'
    MediaAndTx = 'mediaAndTx'
    ObjOverTx = 'objOverTx'
    TxOverObj = 'txOverObj'
    TxAndTwoObj = 'txAndTwoObj'
    TwoObjAndTx = 'twoObjAndTx'
    TwoObjOverTx = 'twoObjOverTx'
    FourObj = 'fourObj'
    VertTx = 'vertTx'
    ClipArtAndVertTx = 'clipArtAndVertTx'
    VertTitleAndTx = 'vertTitleAndTx'
    VertTitleAndTxOverChart = 'vertTitleAndTxOverChart'
    TwoObj = 'twoObj'
    ObjAndTwoObj = 'objAndTwoObj'
    TwoObjAndObj = 'twoObjAndObj'
    Cust = 'cust'
    SecHead = 'secHead'
    TwoTxTwoObj = 'twoTxTwoObj'
    ObjTx = 'objTx'
    PicTx = 'picTx'


class CT_SlideLayout(EG_ChildSlide, AG_ChildSlide):
    """幻灯片布局

    19.3.1.39 sldLayout (Slide Layout)

    该元素指定幻灯片布局的实例。 幻灯片布局实质上包含可应用于任何现有幻灯片的模板幻灯片设计。
    当应用于现有幻灯片时，所有相应的内容都应映射到新的幻灯片布局。
    """

    @property
    def common_slide_data(self) -> CT_CommonSlideData:
        """通用幻灯片数据

        19.3.1.16 cSld

        此元素指定与所有幻灯片类型相关的幻灯片信息的容器。 所有幻灯片共享一组独立于幻灯片类型的通用属性； 任何特定幻灯片的这些属性的描述都存储在幻灯片的 cSld 容器中。 特定于父元素指示的幻灯片类型的幻灯片数据存储在其他地方。

        [Note: cSld 中的实际数据仅描述特定的父幻灯片； 它只是所有幻灯片中通用的存储信息类型。 end note]
        """

        return getattr(self, qn('p:cSld'))

    @property
    def transition(self) -> Optional[CT_SlideTransition]:
        """幻灯片布局的幻灯片过渡

        19.3.1.50 transition

        此元素指定用于从上一张幻灯片过渡到当前幻灯片的幻灯片过渡类型。 也就是说，转换信息存储在转换完成后出现的幻灯片上。
        """
        return getattr(self, qn('p:transition'), None)

    @property
    def timing(self) -> Optional[CT_SlideTiming]:
        """幻灯片布局的幻灯片计时信息

        19.3.1.48 timing

        此元素指定处理相应幻灯片中所有动画和定时事件的计时信息。 该信息通过计时元素内的时间节点进行跟踪。 有关这些时间节点的细节以及如何定义它们的更多信息可以在PresentationML框架的动画部分中找到。
        """
        return getattr(self, qn('p:timing'), None)

    @property
    def header_footer(self) -> Optional[CT_HeaderFooter]:
        """幻灯片母版的页眉/页脚信息

        19.3.1.25 hf

        此元素指定幻灯片的页眉和页脚信息。 页眉和页脚由文本占位符组成，这些文本应在所有幻灯片和幻灯片类型中保持一致，例如日期和时间、幻灯片编号以及自定义页眉和页脚文本。
        """
        return getattr(self, qn('p:hf'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionListModify]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)

    @property
    def matching_name(self) -> str:
        """匹配名称

        Matching Name

        指定用于代替 cSld 元素中的 name 属性的名称。 这用于布局匹配以响应布局变化和模板应用。
        """
        val = self.attrib.get('matchingName')

        if val is None:
            return ''

        return utils.AnyStrToStr(val)  # type: ignore

    @property
    def type(self) -> ST_SlideLayoutType:
        """幻灯片布局类型

        Slide Layout Type

        指定此幻灯片使用的幻灯片布局类型。
        """
        val = self.attrib.get('type')

        if val is None:
            return ST_SlideLayoutType.Cust

        return ST_SlideLayoutType(val)

    @property
    def preserve(self) -> bool:
        """保留幻灯片布局

        Preserve Slide Layout

        指定当删除遵循该布局的所有幻灯片时是否删除相应的幻灯片布局。
        如果未指定此属性，则生成应用程序应假定值为 false。
        这意味着如果演示文稿中没有与该幻灯片相关的幻灯片，该幻灯片实际上将被删除。
        """
        val = self.attrib.get('preserve')

        return utils.XsdBool(val, none=False)

    @property
    def user_drawn(self) -> bool:
        """是否为用户绘制

        Is User Drawn

        指定相应的对象是否已由用户绘制，因此不应被删除。 这允许标记包含用户绘制数据的幻灯片。
        """
        val = self.attrib.get('userDrawn')

        return utils.XsdBool(val, none=False)


class CT_SlideMasterTextStyles(OxmlBaseElement):
    """幻灯片母版文本样式

    19.3.1.52 txStyles

    此元素指定幻灯片母版中的文本样式。 该元素内包含标题文本、正文文本和其他幻灯片文本的样式信息。 该元素仅在幻灯片母版中使用，因此可以设置相应演示文稿幻灯片的文本样式。
    """

    @property
    def title_style(self) -> Optional[a_CT_TextListStyle]:
        """幻灯片母版标题文本样式

        19.3.1.49 titleStyle

            此元素指定母版幻灯片中标题文本的文本格式样式。 此格式适用于相关演示文稿幻灯片中的所有标题文本。 文本格式是通过利用 DrawingML 框架来指定的，就像在常规演示幻灯片中一样。 在标题样式中可以定义许多不同的样式类型，因为幻灯片标题中存储了不同类型的文本。
        """

        return getattr(self, qn('p:titleStyle'), None)

    @property
    def body_style(self) -> Optional[a_CT_TextListStyle]:
        """幻灯片母版正文文本样式

        19.3.1.5 bodyStyle

            此元素指定母版幻灯片中所有正文文本的文本格式样式。 此格式适用于与该母版相关的演示文稿幻灯片中的所有正文文本。 文本格式是通过利用 DrawingML 框架来指定的，就像在常规演示幻灯片中一样。 在 bodyStyle 元素中可以定义许多不同的样式类型，因为幻灯片正文中存储了不同类型的文本。
        """
        return getattr(self, qn('p:bodyStyle'), None)

    @property
    def other_style(self) -> Optional[a_CT_TextListStyle]:
        """幻灯片母版其他文本样式

        19.3.1.35 otherStyle

        此元素指定母版幻灯片中所有其他文本的文本格式样式。 此格式适用于相关演示文稿幻灯片中 titleStyle 或 bodyStyle 元素未涵盖的所有文本。 文本格式是通过利用 DrawingML 框架来指定的，就像在常规演示幻灯片中一样。 在 otherStyle 元素中，可以定义许多不同的样式类型，因为幻灯片中存储了不同类型的文本。

        [Note: otherStyle 元素用于指定幻灯片形状内而非文本框中文本的文本格式。 文本框样式是在 bodyStyle 元素内处理的. end note]
        """

        return getattr(self, qn('p:otherStyle'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionListModify]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)


class ST_SlideLayoutId(ST_BaseType[AnyStr, int]):
    """幻灯片布局 ID

    19.7.14 ST_SlideLayoutId

    这个简单的类型设置幻灯片布局 id 值的范围。 该布局 ID 用于识别不同的幻灯片布局设计.

    此简单类型的内容是 W3C XML Schema unsignedInt 数据类型的限制。

    这个简单类型还指定了以下限制：

        此简单类型的最小值大于或等于 2147483648.
    """

    def _validate(self: Self) -> None:
        val = int(utils.AnyStrToStr(self._val))

        if not val >= 2147483648:
            msg = '逾期外的值'
            raise OxmlAttributeValidateError(msg)

        self._python_val = val


class CT_SlideLayoutIdListEntry(OxmlBaseElement):
    """幻灯片布局 ID

    19.3.1.40 sldLayoutId

    此元素指定幻灯片母版中使用的每个幻灯片布局的关系信息。 幻灯片母版具有内部使用的关系标识符来确定应使用的幻灯片布局。 然后，为了确定这些幻灯片布局应该是什么，请使用 sldLayoutIdLst 中的 sldLayoutId 元素。
    """

    @property
    def ext_lst(self) -> Optional[CT_ExtensionListModify]:
        """扩展列表"""
        return getattr(self, qn('p:extLst'), None)

    @property
    def id(self) -> Optional[ST_SlideLayoutId]:
        """幻灯片布局 ID

        这个简单的类型设置幻灯片布局 id 值的范围。 该布局 ID 用于识别不同的幻灯片布局设计.

        此简单类型的内容是 W3C XML Schema unsignedInt 数据类型的限制。

        这个简单类型还指定了以下限制：

            此简单类型的最小值大于或等于 2147483648.
        """
        val = self.attrib.get('id')

        if val is None:
            return val

        return ST_SlideLayoutId(val)

    @property
    def relationship_id(self) -> r_ST_RelationshipId:
        """关系ID

        指定生成应用程序可用于解析在创建幻灯片时使用哪种幻灯片布局的关系 ID 值。 此关系 ID 在主幻灯片的关系文件中使用，以公开演示文稿中相应布局文件的位置.
        """

        val = utils.AnyStrToStr(self.attrib[qn('r:id')])  # type: ignore

        return r_ST_RelationshipId(val)


class CT_SlideLayoutIdList(OxmlBaseElement):
    """幻灯片布局列表

    19.3.1.41 sldLayoutIdLst

    该元素指定幻灯片布局标识列表是否存在。 此列表包含在幻灯片母版中，用于确定幻灯片母版文件中正在使用哪些布局。 幻灯片布局列表中的每个布局都有其自己的标识号和关系标识符，它们在演示文稿文档和使用它的特定主幻灯片中唯一地标识它。
    """

    @property
    def slide_layout_id_lst(self) -> list[CT_SlideLayoutIdListEntry]:
        """幻灯片布局 ID 列表

        19.3.1.40 sldLayoutId

        此元素指定幻灯片母版中使用的每个幻灯片布局的关系信息。 幻灯片母版具有内部使用的关系标识符来确定应使用的幻灯片布局。 然后，为了确定这些幻灯片布局应该是什么，请使用 sldLayoutIdLst 中的 sldLayoutId 元素。
        """

        return self.findall(qn('p:sldLayoutId'))  # type: ignore


class CT_SlideMaster(EG_TopLevelSlide):
    """幻灯片母版

    19.3.1.42 sldMaster (Slide Master)

    此元素指定幻灯片母版幻灯片的实例。
    幻灯片母版幻灯片中包含描述演示文稿幻灯片中的对象及其相应格式的所有元素。

    幻灯片母版幻灯片中有两个主要元素。

    cSld 元素指定常见的幻灯片元素，例如形状及其附加的文本主体。
    然后 txStyles 元素指定每个形状中文本的格式。

    幻灯片母版幻灯片中的其他属性指定演示文稿幻灯片中的其他属性，
    例如颜色信息、页眉和页脚，以及所有相应演示文稿幻灯片的计时和过渡信息。

    """

    @property
    def common_slide_data(self) -> CT_CommonSlideData:
        """通用幻灯片数据

        19.3.1.16 cSld

        此元素指定与所有幻灯片类型相关的幻灯片信息的容器。 所有幻灯片共享一组独立于幻灯片类型的通用属性； 任何特定幻灯片的这些属性的描述都存储在幻灯片的 cSld 容器中。 特定于父元素指示的幻灯片类型的幻灯片数据存储在其他地方。

        [Note: cSld 中的实际数据仅描述特定的父幻灯片； 它只是所有幻灯片中通用的存储信息类型。 end note]
        """

        return getattr(self, qn('p:cSld'))

    @property
    def slide_layout_id_lst(self) -> Optional[CT_SlideLayoutIdList]:
        """幻灯片布局列表

        19.3.1.41 sldLayoutIdLst

        该元素指定幻灯片布局标识列表是否存在。 此列表包含在幻灯片母版中，用于确定幻灯片母版文件中正在使用哪些布局。 幻灯片布局列表中的每个布局都有其自己的标识号和关系标识符，它们在演示文稿文档和使用它的特定主幻灯片中唯一地标识它。
        """

        return getattr(self, qn('p:sldLayoutIdLst'), None)

    @property
    def transition(self) -> Optional[CT_SlideTransition]:
        """幻灯片布局的幻灯片过渡

        19.3.1.50 transition

        此元素指定用于从上一张幻灯片过渡到当前幻灯片的幻灯片过渡类型。 也就是说，转换信息存储在转换完成后出现的幻灯片上。
        """

        return getattr(self, qn('p:transition'), None)

    @property
    def timing(self) -> Optional[CT_SlideTiming]:
        """幻灯片布局的幻灯片计时信息

        19.3.1.48 timing

        此元素指定处理相应幻灯片中所有动画和定时事件的计时信息。 该信息通过计时元素内的时间节点进行跟踪。 有关这些时间节点的细节以及如何定义它们的更多信息可以在PresentationML框架的动画部分中找到。
        """

        return getattr(self, qn('p:timing'), None)

    @property
    def header_footer(self) -> Optional[CT_HeaderFooter]:
        """幻灯片母版的页眉/页脚信息

        19.3.1.25 hf

        此元素指定幻灯片的页眉和页脚信息。 页眉和页脚由文本占位符组成，这些文本应在所有幻灯片和幻灯片类型中保持一致，例如日期和时间、幻灯片编号以及自定义页眉和页脚文本。
        """

        return getattr(self, qn('p:hf'), None)

    @property
    def text_styles(self) -> Optional[CT_SlideMasterTextStyles]:
        """幻灯片母版文本样式

        19.3.1.52 txStyles

        此元素指定幻灯片母版中的文本样式。 该元素内包含标题文本、正文文本和其他幻灯片文本的样式信息。 该元素仅在幻灯片母版中使用，因此可以设置相应演示文稿幻灯片的文本样式。
        """

        return getattr(self, qn('p:txStyles'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionListModify]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)

    @property
    def preserve(self) -> bool:
        """保留幻灯片母版

        Preserve Slide Master

        指定当删除遵循该布局的所有幻灯片时是否删除相应的幻灯片布局。

        如果未指定此属性，则生成应用程序应假定值为 false。 这意味着如果演示文稿中没有与该幻灯片相关的幻灯片，该幻灯片实际上将被删除。
        """

        val = self.attrib.get('preserve')

        return utils.XsdBool(val, none=False)


class CT_HandoutMaster(EG_TopLevelSlide):
    """讲义母板

    19.3.1.24 handoutMaster (Handout Master)

    此元素指定讲义母版幻灯片的实例。
    讲义母版幻灯片中包含描述讲义幻灯片中的对象及其相应格式的所有元素。
    在讲义母版幻灯片中，cSld 元素指定常见的幻灯片元素，例如形状及其附加的文本正文。
    讲义母版幻灯片中还有其他属性，但 cSld 涵盖了讲义母版幻灯片的大部分预期用途。
    """

    @property
    def common_slide_data(self) -> CT_CommonSlideData:
        """通用幻灯片数据

        19.3.1.16 cSld

        此元素指定与所有幻灯片类型相关的幻灯片信息的容器。 所有幻灯片共享一组独立于幻灯片类型的通用属性； 任何特定幻灯片的这些属性的描述都存储在幻灯片的 cSld 容器中。 特定于父元素指示的幻灯片类型的幻灯片数据存储在其他地方。

        [Note: cSld 中的实际数据仅描述特定的父幻灯片； 它只是所有幻灯片中通用的存储信息类型。 end note]
        """

        return getattr(self, qn('p:cSld'))

    @property
    def header_footer(self) -> Optional[CT_HeaderFooter]:
        """幻灯片母版的页眉/页脚信息

        19.3.1.25 hf

        此元素指定幻灯片的页眉和页脚信息。 页眉和页脚由文本占位符组成，这些文本应在所有幻灯片和幻灯片类型中保持一致，例如日期和时间、幻灯片编号以及自定义页眉和页脚文本。
        """

        return getattr(self, qn('p:hf'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionListModify]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)


class CT_NotesMaster(EG_TopLevelSlide):
    """笔记母板

    19.3.1.27 notesMaster (Notes Master)

    此元素指定笔记母版幻灯片的实例。
    笔记主幻灯片中包含描述笔记幻灯片中的对象及其相应格式的所有元素。
    在笔记母版幻灯片中，cSld 元素指定常见的幻灯片元素，例如形状及其附加的文本正文。
    笔记母版幻灯片中还有其他属性，但 cSld 涵盖了笔记母版幻灯片的大部分预期用途。

    """

    @property
    def common_slide_data(self) -> CT_CommonSlideData:
        """通用幻灯片数据

        19.3.1.16 cSld

        此元素指定与所有幻灯片类型相关的幻灯片信息的容器。 所有幻灯片共享一组独立于幻灯片类型的通用属性； 任何特定幻灯片的这些属性的描述都存储在幻灯片的 cSld 容器中。 特定于父元素指示的幻灯片类型的幻灯片数据存储在其他地方。

        [Note: cSld 中的实际数据仅描述特定的父幻灯片； 它只是所有幻灯片中通用的存储信息类型。 end note]
        """

        return getattr(self, qn('p:cSld'))

    @property
    def header_footer(self) -> Optional[CT_HeaderFooter]:
        """幻灯片母版的页眉/页脚信息

        19.3.1.25 hf

        此元素指定幻灯片的页眉和页脚信息。 页眉和页脚由文本占位符组成，这些文本应在所有幻灯片和幻灯片类型中保持一致，例如日期和时间、幻灯片编号以及自定义页眉和页脚文本。
        """

        return getattr(self, qn('p:hf'), None)

    @property
    def notes_style(self) -> Optional[a_CT_TextListStyle]:
        """笔记文本样式

        19.3.1.28 notesStyle

        此元素指定注释幻灯片中所有其他文本的文本格式样式。 此格式适用于相应注释幻灯片中的所有文本。 文本格式是通过利用 DrawingML 框架来指定的，就像在常规演示幻灯片中一样。 在notesStyle元素中可以定义许多不同的样式类型，因为注释幻灯片中存储了不同类型的文本。
        """

        return getattr(self, qn('p:notesStyle'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionListModify]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)


class CT_NotesSlide(EG_ChildSlide, AG_ChildSlide):
    """笔记幻灯片

    19.3.1.26 notes (Notes Slide)

    该元素指定注释幻灯片及其相应数据的存在。
    注释幻灯片中包含所有常见的幻灯片元素以及特定于注释元素的附加属性。

    示例: 考虑下面的PresentationML笔记幻灯片

    <p:notes>
        <p:cSld>
        …
        </p:cSld>
        …
    </p:notes>

    在上面的示例中，注释元素指定了注释幻灯片及其所有部分的存在。
    请注意 cSld 元素，它指定可以出现在任何幻灯片类型上的通用元素，然后任何元素指定此注释幻灯片的其他非通用属性。
    """

    @property
    def common_slide_data(self) -> CT_CommonSlideData:
        """通用幻灯片数据

        19.3.1.16 cSld

        此元素指定与所有幻灯片类型相关的幻灯片信息的容器。 所有幻灯片共享一组独立于幻灯片类型的通用属性； 任何特定幻灯片的这些属性的描述都存储在幻灯片的 cSld 容器中。 特定于父元素指示的幻灯片类型的幻灯片数据存储在其他地方。

        [Note: cSld 中的实际数据仅描述特定的父幻灯片； 它只是所有幻灯片中通用的存储信息类型。 end note]
        """

        return getattr(self, qn('p:cSld'))

    @property
    def ext_lst(self) -> Optional[CT_ExtensionListModify]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)


class CT_SlideSyncProperties(OxmlBaseElement):
    """幻灯片同步属性

    19.6.1 sldSyncPr (Slide Synchronization Properties)

    此元素指定将原始幻灯片与其所有复制实例相关联所需的信息。
    """

    @property
    def ext_lst(self) -> Optional[CT_ExtensionListModify]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)

    @property
    def server_slide_id(self) -> str:
        """服务器的幻灯片文件 ID

        Server's Slide File ID

        一个字符串，当与幻灯片同步数据部件的外部关系的目标配对时，唯一标识原始幻灯片。
        """

        val = self.attrib['serverSldId']

        return utils.AnyStrToStr(val)  # type: ignore

    @property
    def server_slide_modified_time(self) -> XSD_DateTime:
        """服务器幻灯片文件的修改日期/时间

        Server's Slide File's modification date/time

        原始幻灯片在其位置（由幻灯片同步数据部件的外部关系的目标定义）最后修改的日期和时间。
        """

        val = self.attrib['serverSldModifiedTime']

        return XSD_DateTime(to_xsd_datetime(val))  # type: ignore

    @property
    def client_inserted_time(self) -> XSD_DateTime:
        """客户幻灯片插入日期/时间

        Client Slide Insertion date/time

        当前演示文稿中原始幻灯片上次更新的日期和时间。

        日期/时间以 ISO 8601 格式存储。

        [注意: 该值可用于通知用户上次同步的时间，以及确定下次检查更新版本的时间。]
        """

        val = self.attrib['clientInsertedTime']

        return XSD_DateTime(to_xsd_datetime(val))  # type: ignore


class CT_StringTag(OxmlBaseElement):
    """可编程扩展性标签

    19.3.3.1 tag

    该元素指定用于存储遗留变量的可编程扩展性标签。
    """

    @property
    def name(self) -> str:
        """名称

        指定与该特定可编程标签关联的名称.
        """
        val = self.attrib['name']

        return utils.AnyStrToStr(val)  # type: ignore

    @property
    def value(self) -> str:
        """值

        指定与该特定可编程标签关联的值.
        """
        val = self.attrib['val']

        return utils.AnyStrToStr(val)  # type: ignore


class CT_TagList(OxmlBaseElement):
    """可编程标签列表

    19.3.3.2 tagLst (Programmable Tag List)

    此元素指定用于存储旧文件格式变量的可编程扩展性标记的列表。
    """

    @property
    def tags(self) -> list[CT_StringTag]:
        """可编程扩展性标签

        19.3.3.1 tag

        该元素指定用于存储遗留变量的可编程扩展性标签。
        """

        return self.findall(qn('p:tag'))  # type: ignore


class ST_SplitterBarState(ST_BaseEnumType):
    """
    aaa
    """

    Minimized = 'minimized'
    Restored = 'restored'
    Maximized = 'maximized'


class ST_ViewType(ST_BaseEnumType):
    """
    aaa
    """

    SldView = 'sldView'
    SldMasterView = 'sldMasterView'
    NotesView = 'notesView'
    HandoutView = 'handoutView'
    NotesMasterView = 'notesMasterView'
    OutlineView = 'outlineView'
    SldSorterView = 'sldSorterView'
    SldThumbnailView = 'sldThumbnailView'


class CT_NormalViewPortion(OxmlBaseElement):
    """
    aaa
    """

    @property
    def size(self) -> a_ST_PositiveFixedPercentage:
        val = self.attrib['sz']

        return a_to_ST_PositiveFixedPercentage(str(val))

    @property
    def auto_adjust(self) -> bool:
        val = self.attrib.get('autoAdjust')

        return utils.XsdBool(val, none=True)


class CT_NormalViewProperties(OxmlBaseElement):
    """
    aaa
    """

    @property
    def restore_left(self) -> CT_NormalViewPortion:
        """
        aaa
        """

        return getattr(self, qn('p:restoredLeft'))

    @property
    def restore_top(self) -> CT_NormalViewPortion:
        """
        aaa
        """

        return getattr(self, qn('p:restoredTop'))

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """
        aaa
        """

        return getattr(self, qn('p:extLst'), None)

    @property
    def show_outline_icons(self) -> bool:
        """
        aaa
        """

        val = self.attrib.get('showOutlineIcons')

        return utils.XsdBool(val, none=True)

    @property
    def snap_vert_splitter(self) -> bool:
        """
        aaa
        """

        val = self.attrib.get('snapVertSplitter')

        return utils.XsdBool(val, none=False)

    @property
    def vert_bar_state(self) -> ST_SplitterBarState:
        """
        aaa
        """

        val = self.attrib.get('vertBarState')

        if val is None:
            return ST_SplitterBarState.Restored

        return ST_SplitterBarState(val)

    @property
    def horz_bar_state(self) -> ST_SplitterBarState:
        """
        aaa
        """

        val = self.attrib.get('horzBarState')

        if val is None:
            return ST_SplitterBarState.Restored

        return ST_SplitterBarState(val)

    @property
    def prefer_single_view(self) -> bool:
        """
        aaa
        """

        val = self.attrib.get('preferSingleView')

        return utils.XsdBool(val, none=False)


class CT_CommonViewProperties(OxmlBaseElement):
    """
    aaa
    """

    @property
    def scale(self) -> a_CT_Scale2D:
        """
        aaa
        """

        return getattr(self, qn('p:scale'))

    @property
    def origin(self) -> a_CT_Point2D:
        """
        aaa
        """

        return getattr(self, qn('p:origin'))

    @property
    def var_scale(self) -> bool:
        """
        aaa
        """

        val = self.attrib.get('varScale')

        return utils.XsdBool(val, none=False)


class CT_NotesTextViewProperties(OxmlBaseElement):
    """
    aaa
    """

    @property
    def common_view_properties(self) -> CT_CommonViewProperties:
        """
        aaa
        """

        return getattr(self, qn('p:cViewPr'))

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """
        aaa
        """

        return getattr(self, qn('p:extLst'))


class CT_OutlineViewSlideEntry(OxmlBaseElement):
    """
    aaa
    """

    @property
    def relationship_id(self) -> r_ST_RelationshipId:
        """
        aaa
        """

        val = utils.AnyStrToStr(self.attrib[qn('r:id')])  # type: ignore

        return r_ST_RelationshipId(val)

    @property
    def collapse(self) -> bool:
        """
        aaa
        """

        val = self.attrib.get('collapse')

        return utils.XsdBool(val, none=False)


class CT_OutlineViewSlideList(OxmlBaseElement):
    """
    aaa
    """

    @property
    def slides(self) -> list[CT_OutlineViewSlideEntry]:
        """
        aaa
        """

        return self.findall(qn('p:sld'))  # type: ignore


class CT_OutlineViewProperties(OxmlBaseElement):
    """
    aaa
    """

    @property
    def commone_view_properties(self) -> CT_CommonViewProperties:
        """
        aaa
        """

        return getattr(self, qn('p:cViewPr'))

    @property
    def slide_lst(self) -> Optional[CT_OutlineViewSlideList]:
        """
        aaa
        """

        return getattr(self, qn('p:sldLst'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """
        aaa
        """

        return getattr(self, qn('p:extLst'), None)


class CT_SlideSorterViewProperties(OxmlBaseElement):
    """
    aaa
    """

    @property
    def commone_view_properties(self) -> CT_CommonViewProperties:
        """
        aaa
        """

        return getattr(self, qn('p:cViewPr'))

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """
        aaa
        """

        return getattr(self, qn('p:extLst'), None)

    @property
    def show_formatting(self) -> bool:
        """
        aaa
        """

        val = self.attrib.get('showFormatting')

        return utils.XsdBool(val, none=True)


class CT_Guide(OxmlBaseElement):
    """
    aaa
    """

    @property
    def orient(self) -> ST_Direction:
        """
        aaa
        """

        val = self.attrib.get('orient')

        if val is None:
            return ST_Direction.Vert

        return ST_Direction(val)

    @property
    def position(self) -> a_ST_Coordinate32:
        """
        aaa
        """

        val = self.attrib.get('pos')

        if val is None:
            val = '0'

        return a_to_ST_Coordinate32(val)  # type: ignore


class CT_GuideList(OxmlBaseElement):
    """
    aaa
    """

    @property
    def guides(self) -> list[CT_Guide]:
        """
        aaa
        """

        return self.findall(qn('p:guide'))  # type: ignore


class CT_CommonSlideViewProperties(OxmlBaseElement):
    """
    aaa
    """

    @property
    def commone_view_properties(self) -> CT_CommonViewProperties:
        """
        aaa
        """

        return getattr(self, qn('p:cViewPr'))

    @property
    def guide_lst(self) -> Optional[CT_GuideList]:
        """
        aaa
        """

        return getattr(self, qn('p:guideLst'), None)

    @property
    def snap_to_grid(self) -> bool:
        """
        aaa
        """

        val = self.attrib.get('showFormatting')

        return utils.XsdBool(val, none=True)

    @property
    def snap_to_objects(self) -> bool:
        """
        aaa
        """

        val = self.attrib.get('snapToObjects')

        return utils.XsdBool(val, none=False)

    @property
    def show_guides(self) -> bool:
        """
        aaa
        """

        val = self.attrib.get('showGuides')

        return utils.XsdBool(val, none=False)


class CT_SlideViewProperties(OxmlBaseElement):
    """
    aaa
    """

    @property
    def common_slide_view_properties(self) -> CT_CommonSlideViewProperties:
        """
        aaa
        """

        return getattr(self, qn('p:cSldViewPr'))

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """
        aaa
        """

        return getattr(self, qn('p:extLst'), None)


class CT_NotesViewProperties(OxmlBaseElement):
    """
    aaa
    """

    @property
    def common_slide_view_properties(self) -> CT_CommonSlideViewProperties:
        """
        aaa
        """

        return getattr(self, qn('p:cSldViewPr'))

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """
        aaa
        """

        return getattr(self, qn('p:extLst'), None)


class CT_ViewProperties(OxmlBaseElement):
    """演示文稿级别的视图属性

    19.2.2.18 viewPr (Presentation-wide View Properties)

    该元素充当父元素，其中包含所有演示文稿范围内的视图属性。 所有属性及其相应的设置都在子元素中定义。
    """

    @property
    def normal_view_properties(self) -> Optional[CT_NormalViewProperties]:
        """
        aaa
        """

        return getattr(self, qn('p:normalViewPr'), None)

    @property
    def slide_view_properties(self) -> Optional[CT_SlideViewProperties]:
        """
        aaa
        """

        return getattr(self, qn('p:slideViewPr'), None)

    @property
    def outline_view_properties(self) -> Optional[CT_OutlineViewProperties]:
        """
        aaa
        """

        return getattr(self, qn('p:outlineViewPr'), None)

    @property
    def notes_text_view_properties(self) -> Optional[CT_NotesTextViewProperties]:
        """
        aaa
        """

        return getattr(self, qn('p:notesTextViewPr'), None)

    @property
    def sorter_view_pr(self) -> Optional[CT_SlideSorterViewProperties]:
        """
        aaa
        """

        return getattr(self, qn('p:sorterViewPr'), None)

    @property
    def notes_view_properties(self) -> Optional[CT_NotesViewProperties]:
        """
        aaa
        """

        return getattr(self, qn('p:notesViewPr'), None)

    @property
    def grid_spacing(self) -> Optional[a_CT_PositiveSize2D]:
        """
        aaa
        """

        return getattr(self, qn('p:gridSpacing'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展列表"""

        return getattr(self, qn('p:extLst'), None)

    @property
    def last_view(self) -> ST_ViewType:
        """最后视图类型

        Last View

        指定上次保存演示文稿文档时使用的查看模式。
        """

        val = self.attrib.get('lastView')

        if val is None:
            return ST_ViewType.SldView

        return ST_ViewType(val)

    @property
    def show_comments(self) -> bool:
        """显示评论

        Show Comments

        指定是否应显示幻灯片注释。
        """

        val = self.attrib.get('showComments')

        return utils.XsdBool(val, none=True)


# class CT_MC_Choice(OxmlBaseElement):
#     """选择标签

#     https://hellowac.github.io/ecma-376-zh-cn/ecma-part3-refrence/#76-choice-%E5%85%83%E7%B4%A0
#     """

#     @property
#     def require(self) -> str:
#         """必须条件:

#         https://hellowac.github.io/ecma-376-zh-cn/ecma-part3-refrence/#76-choice-%E5%85%83%E7%B4%A0
#         """

#         r = self.attrib.get("Requires", "")

#         return str(r)

#     @property
#     def graphe_frame(self) -> CT_GraphicalObjectFrame:
#         return getattr(self, qn("p:graphicFrame"))


# class CT_MC_Fallback(OxmlBaseElement):
#     """后退标签

#     https://hellowac.github.io/ecma-376-zh-cn/ecma-part3-refrence/#77-fallback-%E5%85%83%E7%B4%A0
#     """

#     @property
#     def picture(self) -> CT_Picture:
#         """替代的图片"""

#         return getattr(self, qn("p:pic"))


# class CT_MC_AlternateContent(OxmlBaseElement):
#     """替代内容标签"""

#     @property
#     def choice(self) -> CT_MC_Choice:
#         """选择标签

#         https://hellowac.github.io/ecma-376-zh-cn/ecma-part3-refrence/#76-choice-元素
#         """
#         return getattr(self, qn("mc:Choice"))

#     @property
#     def fallback(self) -> CT_MC_Choice:
#         """后退标签

#         https://hellowac.github.io/ecma-376-zh-cn/ecma-part3-refrence/#77-fallback-元素
#         """
#         return getattr(self, qn("mc:Fallback"))


# 兼容性文档定义
"""
<a:graphicData uri="http://schemas.openxmlformats.org/presentationml/2006/ole">
    <mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">
        <mc:Choice Requires="v">
            <p:oleObj spid="_x0000_s17449" name="" r:id="rId1" imgW="1245235" imgH="213995" progId="Equation.3">
                <p:embed/>
            </p:oleObj>
        </mc:Choice>
        <mc:Fallback>
            <p:oleObj name="" r:id="rId1" imgW="1245235" imgH="213995" progId="Equation.3">
                <p:embed/>
                <p:pic>
                    ...
                </p:pic>
            </p:oleObj>
        </mc:Fallback>
    </mc:AlternateContent>
</a:graphicData>
"""


class CT_MC_AlternateContent(OxmlBaseElement):
    """
    AlternateContent 元素应是本地名称为 "AlternateContent "的 "标记兼容 "命名空间中的一个元素。AlternateContent 元素不得有非限定属性，但可以有限定属性。每个限定属性的命名空间要么是标记兼容命名空间，要么是该 AlternateContent 元素或其某个祖先的 Ignorable 属性声明为可忽略的命名空间。

    参考: https://hellowac.github.io/ecma-376-zh-cn/ecma-part3-refrence/#75-alternatecontent-元素
    """

    @property
    def choice(self) -> CT_MC_Choice:
        """choice 元素应是本地名称为 "Choice"的 "标记兼容 "命名空间中的一个元素。choice 元素的父元素应是 AlternateContent 元素。

        参考: https://hellowac.github.io/ecma-376-zh-cn/ecma-part3-refrence/#76-choice-元素
        """
        return getattr(self, qn('mc:Choice'))

    @property
    def fallback(self) -> CT_MC_Fallback:
        """fallback 元素应是本地名称为 "Fallback"的 "标记兼容" 命名空间中的一个元素。回退元素的父元素应为 AlternateContent 元素。

        参考: https://hellowac.github.io/ecma-376-zh-cn/ecma-part3-refrence/#77-fallback-元素
        """
        return getattr(self, qn('mc:Fallback'))


class CT_MC_Choice(OxmlBaseElement):
    """choice 元素应是本地名称为 "Choice"的 "标记兼容 "命名空间中的一个元素。choice 元素的父元素应是 AlternateContent 元素。

    choice 元素必须有一个本地名称为 "Requires "的非限定属性，且不得有其他非限定属性。Requires 属性的值应是一个或多个命名空间前缀的以空白为分隔符的列表，可选择带前导和/或尾部空白。

    [Note: 除了空列表外，与 Requires 属性相关的语法限制与与 MustUnderstand 属性相关的语法限制相同。 end note]

    选择元素可以有限定属性。每个限定属性的命名空间必须是标记兼容命名空间或已声明为可忽略的命名空间。

    参考: https://hellowac.github.io/ecma-376-zh-cn/ecma-part3-refrence/#76-choice-元素
    """

    @property
    def requires(self) -> str:
        return str(self.attrib.get('Requires', ''))

    @property
    def p_oleObj(self):
        """19.3.2.4 oleObj (嵌入式对象和控件的全局元素)

        该元素指定用于嵌入对象和控件的全局元素。

        当 oleObject 元素包含 pic 子元素时，在决定使用哪个标识符时，应忽略 pic/nvPicPr/cNvPr@id 属性指定的标识符，并使用 GraphicFrame/nvGraphicFramePr/cNvPr@id 属性指定的标识符 OLE 对象。
        """

        ele: CT_OleObject = getattr(self, qn('p:oleObj'))

        return ele


class CT_MC_Fallback(OxmlBaseElement):
    """fallback 元素应是本地名称为 "Fallback"的 "标记兼容" 命名空间中的一个元素。回退元素的父元素应为 AlternateContent 元素。

    fallback元素 不得有非限定属性。回退元素可以有限定属性。每个限定属性的命名空间必须是 "标记兼容 "命名空间或已声明为可忽略的命名空间。

    参考: https://hellowac.github.io/ecma-376-zh-cn/ecma-part3-refrence/#77-fallback-元素
    """

    @property
    def requires(self) -> Optional[str]:
        """
        "Requires"的非限定属性，且不得有其他非限定属性。

        Requires 属性的值应是一个或多个命名空间前缀的以空白为分隔符的列表，可选择带前导和/或尾部空白。
        """
        req = self.attrib.get('Requires')

        if req is not None:
            return str(req)
        return None

    @property
    def p_oleObj(self):
        """19.3.2.4 oleObj (嵌入式对象和控件的全局元素)

        该元素指定用于嵌入对象和控件的全局元素。

        当 oleObject 元素包含 pic 子元素时，在决定使用哪个标识符时，应忽略 pic/nvPicPr/cNvPr@id 属性指定的标识符，并使用 GraphicFrame/nvGraphicFramePr/cNvPr@id 属性指定的标识符 OLE 对象。
        """

        ele: CT_OleObject = getattr(self, qn('p:oleObj'))

        return ele


pml_mc_namesapce = lookup.get_namespace(namespace_mc)

pml_mc_namesapce[None] = OxmlBaseElement
pml_mc_namesapce['AlternateContent'] = CT_MC_AlternateContent
pml_mc_namesapce['Choice'] = CT_MC_Choice
pml_mc_namesapce['Fallback'] = CT_MC_Fallback


pml_core_namespace = lookup.get_namespace(namespace_p)
pml_core_namespace[None] = OxmlBaseElement
pml_core_namespace['text'] = OxmlBaseElement
pml_core_namespace['attrName'] = OxmlBaseElement
pml_core_namespace['extLst'] = CT_ExtensionListModify

# ---
pml_core_namespace['stSnd'] = CT_TransitionStartSoundAction
pml_core_namespace['endSnd'] = CT_Empty

pml_core_namespace['blinds'] = CT_OrientationTransition
pml_core_namespace['checker'] = CT_OrientationTransition
pml_core_namespace['circle'] = CT_Empty
pml_core_namespace['dissolve'] = CT_Empty
pml_core_namespace['comb'] = CT_OrientationTransition
pml_core_namespace['cover'] = CT_EightDirectionTransition
pml_core_namespace['cut'] = CT_OptionalBlackTransition
pml_core_namespace['diamond'] = CT_Empty
pml_core_namespace['fade'] = CT_OptionalBlackTransition
pml_core_namespace['newsflash'] = CT_Empty
pml_core_namespace['plus'] = CT_Empty
pml_core_namespace['pull'] = CT_EightDirectionTransition
pml_core_namespace['push'] = CT_SideDirectionTransition
pml_core_namespace['random'] = CT_Empty
pml_core_namespace['randomBar'] = CT_OrientationTransition
pml_core_namespace['split'] = CT_SplitTransition
pml_core_namespace['strips'] = CT_CornerDirectionTransition
pml_core_namespace['wedge'] = CT_Empty
pml_core_namespace['wheel'] = CT_WheelTransition
pml_core_namespace['wipe'] = CT_SideDirectionTransition
pml_core_namespace['zoom'] = CT_InOutTransition
pml_core_namespace['sndAc'] = CT_TransitionSoundAction

pml_core_namespace['tmAbs'] = CT_TLIterateIntervalTime
pml_core_namespace['tmPct'] = CT_TLIterateIntervalPercentage

pml_core_namespace['charRg'] = CT_IndexRange
pml_core_namespace['pRg'] = CT_IndexRange

pml_core_namespace['bg'] = CT_Empty
pml_core_namespace['subSp'] = CT_TLSubShapeId
pml_core_namespace['oleChartEl'] = CT_TLOleChartTargetElement
pml_core_namespace['txEl'] = CT_TLTextTargetElement
pml_core_namespace['graphicEl'] = a_CT_AnimationElementChoice

pml_core_namespace['sldTgt'] = CT_Empty
pml_core_namespace['sndTgt'] = a_CT_EmbeddedWAVAudioFile
pml_core_namespace['spTgt'] = CT_TLShapeTargetElement
pml_core_namespace['inkTgt'] = CT_TLSubShapeId

pml_core_namespace['tgtEl'] = CT_TLTimeTargetElement
pml_core_namespace['tn'] = CT_TLTriggerTimeNodeID
pml_core_namespace['rtn'] = CT_TLTriggerRuntimeNode

pml_core_namespace['cond'] = CT_TLTimeCondition

pml_core_namespace['par'] = CT_TLTimeNodeParallel
pml_core_namespace['seq'] = CT_TLTimeNodeSequence
pml_core_namespace['excl'] = CT_TLTimeNodeExclusive
pml_core_namespace['anim'] = CT_TLAnimateBehavior
pml_core_namespace['animClr'] = CT_TLAnimateColorBehavior
pml_core_namespace['animEffect'] = CT_TLAnimateEffectBehavior
pml_core_namespace['animMotion'] = CT_TLAnimateMotionBehavior
pml_core_namespace['animRot'] = CT_TLAnimateRotationBehavior
pml_core_namespace['animScale'] = CT_TLAnimateScaleBehavior
pml_core_namespace['cmd'] = CT_TLCommandBehavior
pml_core_namespace['set'] = CT_TLSetBehavior
pml_core_namespace['audio'] = CT_TLMediaNodeAudio
pml_core_namespace['video'] = CT_TLMediaNodeVideo

pml_core_namespace['stCondLst'] = CT_TLTimeConditionList
pml_core_namespace['endCondLst'] = CT_TLTimeConditionList
pml_core_namespace['endSync'] = CT_TLTimeCondition
pml_core_namespace['iterate'] = CT_TLIterateData
pml_core_namespace['childTnLst'] = CT_TimeNodeList
pml_core_namespace['subTnLst'] = CT_TimeNodeList

pml_core_namespace['cTn'] = CT_TLCommonTimeNodeData
pml_core_namespace['prevCondLst'] = CT_TLTimeConditionList
pml_core_namespace['nextCondLst'] = CT_TLTimeConditionList

pml_core_namespace['attrNameLst'] = CT_TLBehaviorAttributeNameList

pml_core_namespace['boolVal'] = CT_TLAnimVariantBooleanVal
pml_core_namespace['intVal'] = CT_TLAnimVariantIntegerVal
pml_core_namespace['fltVal'] = CT_TLAnimVariantFloatVal
pml_core_namespace['strVal'] = CT_TLAnimVariantStringVal
pml_core_namespace['clrVal'] = a_CT_Color

pml_core_namespace['val'] = CT_TLAnimVariant
pml_core_namespace['cBhvr'] = CT_TLCommonBehaviorData
pml_core_namespace['from'] = a_CT_Color  # 冲突 from
pml_core_namespace['to'] = a_CT_Color  # 冲突 to

pml_core_namespace['tav'] = CT_TLTimeAnimateValue
pml_core_namespace['tavLst'] = CT_TLTimeAnimateValueList

pml_core_namespace['rgb'] = CT_TLByRgbColorTransform
pml_core_namespace['hsl'] = CT_TLByHslColorTransform

pml_core_namespace['by'] = CT_TLByAnimateColorTransform  # 冲突1 CT_TLAnimateColorBehavior
pml_core_namespace['progress'] = CT_TLAnimVariant

pml_core_namespace['by'] = CT_TLPoint  # 冲突1 CT_TLAnimateMotionBehavior
pml_core_namespace['from'] = CT_TLPoint  # 冲突 from
pml_core_namespace['to'] = CT_TLPoint  # 冲突 to
pml_core_namespace['rCtr'] = CT_TLPoint

pml_core_namespace['to'] = CT_TLAnimVariant  # 冲突 to
pml_core_namespace['cMediaNode'] = CT_TLCommonMediaNodeData
pml_core_namespace['tnLst'] = CT_TimeNodeList
pml_core_namespace['tmpl'] = CT_TLTemplate
pml_core_namespace['tmplLst'] = CT_TLTemplateList

pml_core_namespace['bldAsOne'] = CT_Empty
pml_core_namespace['bldSub'] = a_CT_AnimationGraphicalObjectBuildProperties
pml_core_namespace['bldP'] = CT_TLBuildParagraph
pml_core_namespace['bldDgm'] = CT_TLBuildDiagram
pml_core_namespace['bldOleChart'] = CT_TLOleBuildChart
pml_core_namespace['bldGraphic'] = CT_TLGraphicalObjectBuild

pml_core_namespace['bldLst'] = CT_BuildList
pml_core_namespace['sld'] = CT_SlideRelationshipListEntry

pml_core_namespace['sldAll'] = CT_Empty
pml_core_namespace['sldRg'] = CT_IndexRange
pml_core_namespace['custShow'] = CT_CustomShowId  # 冲突3

pml_core_namespace['custData'] = CT_CustomerData
pml_core_namespace['tags'] = CT_TagsData
pml_core_namespace['ext'] = CT_Extension
pml_core_namespace['extLst'] = CT_ExtensionList

pml_core_namespace['cmAuthor'] = CT_CommentAuthor
pml_core_namespace['cmAuthorLst'] = CT_CommentAuthorList
pml_core_namespace['cm'] = CT_Comment
pml_core_namespace['pos'] = a_CT_Point2D
pml_core_namespace['cmLst'] = CT_CommentList

pml_core_namespace['embed'] = CT_OleObjectEmbed
pml_core_namespace['link'] = CT_OleObjectLink

pml_core_namespace['oleObj'] = CT_OleObject

pml_core_namespace['control'] = CT_Control
pml_core_namespace['controls'] = CT_ControlList

pml_core_namespace['sldId'] = CT_SlideIdListEntry
pml_core_namespace['sldMasterId'] = CT_SlideMasterIdListEntry
pml_core_namespace['notesMasterId'] = CT_NotesMasterIdListEntry
pml_core_namespace['handoutMasterId'] = CT_HandoutMasterIdListEntry

pml_core_namespace['font'] = a_CT_TextFont
pml_core_namespace['regular'] = CT_EmbeddedFontDataId
pml_core_namespace['bold'] = CT_EmbeddedFontDataId
pml_core_namespace['italic'] = CT_EmbeddedFontDataId
pml_core_namespace['boldItalic'] = CT_EmbeddedFontDataId

pml_core_namespace['embeddedFont'] = CT_EmbeddedFontListEntry
pml_core_namespace['sldLst'] = CT_SlideRelationshipList  # 冲突5

pml_core_namespace['custShow'] = CT_CustomShow  # 冲突3 父级类型: CT_CustomShowList

pml_core_namespace['sldMasterIdLst'] = CT_SlideMasterIdList
pml_core_namespace['notesMasterIdLst'] = CT_NotesMasterIdList
pml_core_namespace['handoutMasterIdLst'] = CT_HandoutMasterIdList

pml_core_namespace['sldIdLst'] = CT_SlideIdList
pml_core_namespace['sldSz'] = CT_SlideSize
pml_core_namespace['notesSz'] = a_CT_PositiveSize2D
pml_core_namespace['smartTags'] = CT_SmartTags
pml_core_namespace['embeddedFontLst'] = CT_EmbeddedFontList
pml_core_namespace['custShowLst'] = CT_CustomShowList
pml_core_namespace['photoAlbum'] = CT_PhotoAlbum
pml_core_namespace['custDataLst'] = CT_CustomerDataList
pml_core_namespace['kinsoku'] = CT_Kinsoku
pml_core_namespace['defaultTextStyle'] = a_CT_TextListStyle
pml_core_namespace['modifyVerifier'] = CT_ModifyVerifier

pml_core_namespace['presentation'] = CT_Presentation
pml_core_namespace['presentationPr'] = CT_PresentationProperties

pml_core_namespace['present'] = CT_Empty
pml_core_namespace['browse'] = CT_ShowInfoBrowse
pml_core_namespace['kiosk'] = CT_ShowInfoKiosk

pml_core_namespace['prnPr'] = CT_PrintProperties
pml_core_namespace['showPr'] = CT_ShowProperties
pml_core_namespace['clrMru'] = a_CT_ColorMRU

pml_core_namespace['ph'] = CT_Placeholder
pml_core_namespace['audioCd'] = a_CT_AudioCD
pml_core_namespace['wavAudioFile'] = a_CT_EmbeddedWAVAudioFile
pml_core_namespace['audioFile'] = a_CT_AudioFile
pml_core_namespace['videoFile'] = a_CT_VideoFile
pml_core_namespace['quickTimeFile'] = a_CT_QuickTimeFile
pml_core_namespace['nvPr'] = CT_ApplicationNonVisualDrawingProps

pml_core_namespace['spPr'] = a_CT_ShapeProperties
pml_core_namespace['grpSpPr'] = a_CT_GroupShapeProperties
pml_core_namespace['nvSpPr'] = CT_ShapeNonVisual
pml_core_namespace['cNvPr'] = a_CT_NonVisualDrawingProps
pml_core_namespace['cNvGrpSpPr'] = a_CT_NonVisualGroupDrawingShapeProps
pml_core_namespace['cNvCxnSpPr'] = a_CT_NonVisualConnectorProperties
pml_core_namespace['cNvSpPr'] = a_CT_NonVisualDrawingShapeProps
pml_core_namespace['nvCxnSpPr'] = CT_ConnectorNonVisual
pml_core_namespace['nvPicPr'] = CT_PictureNonVisual

pml_core_namespace['nvGraphicFramePr'] = CT_GraphicalObjectFrameNonVisual
pml_core_namespace['cNvGraphicFramePr'] = a_CT_NonVisualGraphicFrameProperties
pml_core_namespace['nvGrpSpPr'] = CT_GroupShapeNonVisual

pml_core_namespace['sp'] = CT_Shape
pml_core_namespace['grpSp'] = CT_GroupShape
pml_core_namespace['graphicFrame'] = CT_GraphicalObjectFrame
pml_core_namespace['cxnSp'] = CT_Connector
pml_core_namespace['pic'] = CT_Picture
pml_core_namespace['contentPart'] = CT_Rel

pml_core_namespace['bgPr'] = CT_BackgroundProperties

pml_core_namespace['bg'] = CT_Background
pml_core_namespace['spTree'] = CT_GroupShape

pml_core_namespace['sld'] = CT_Slide  # 冲突4
pml_core_namespace['cSld'] = CT_CommonSlideData

pml_core_namespace['transition'] = CT_SlideTransition
pml_core_namespace['timing'] = CT_SlideTiming


pml_core_namespace['hf'] = CT_HeaderFooter
pml_core_namespace['sldLayout'] = CT_SlideLayout

pml_core_namespace['sldLayoutId'] = CT_SlideLayoutIdListEntry
pml_core_namespace['sldLayoutIdLst'] = CT_SlideLayoutIdList
pml_core_namespace['txStyles'] = CT_SlideMasterTextStyles

pml_core_namespace['sldMaster'] = CT_SlideMaster
pml_core_namespace['handoutMaster'] = CT_HandoutMaster

pml_core_namespace['notesMaster'] = CT_NotesMaster
pml_core_namespace['notes'] = CT_NotesSlide

pml_core_namespace['sldSyncPr'] = CT_SlideSyncProperties
pml_core_namespace['tag'] = CT_StringTag
pml_core_namespace['tagLst'] = CT_TagList

pml_core_namespace['restoredLeft'] = CT_NormalViewPortion
pml_core_namespace['restoredTop'] = CT_NormalViewPortion

pml_core_namespace['cViewPr'] = CT_CommonViewProperties
# pml_core_namespace["sld"] = CT_OutlineViewSlideEntry # 冲突4 父级: CT_OutlineViewSlideList
# pml_core_namespace["sldLst"] = CT_OutlineViewSlideList  # 冲突5 父级: CT_OutlineViewProperties

pml_core_namespace['guide'] = CT_Guide
pml_core_namespace['guideLst'] = CT_GuideList

pml_core_namespace['cSldViewPr'] = CT_CommonSlideViewProperties
pml_core_namespace['normalViewPr'] = CT_NormalViewProperties
pml_core_namespace['slideViewPr'] = CT_SlideViewProperties
pml_core_namespace['outlineViewPr'] = CT_OutlineViewProperties
pml_core_namespace['notesTextViewPr'] = CT_NotesTextViewProperties
pml_core_namespace['sorterViewPr'] = CT_SlideSorterViewProperties
pml_core_namespace['notesViewPr'] = CT_NotesViewProperties
pml_core_namespace['viewPr'] = CT_ViewProperties

# 属于dml中

pml_core_namespace['cNvPicPr'] = a_CT_NonVisualPictureProperties
pml_core_namespace['blipFill'] = a_CT_BlipFillProperties
pml_core_namespace['style'] = a_CT_ShapeStyle
pml_core_namespace['snd'] = a_CT_EmbeddedWAVAudioFile
pml_core_namespace['txBody'] = a_CT_TextBody
pml_core_namespace['xfrm'] = a_CT_Transform2D

pml_core_namespace['graphicEl'] = a_CT_AnimationElementChoice
pml_core_namespace['sndTgt'] = a_CT_EmbeddedWAVAudioFile
pml_core_namespace['clrVal'] = a_CT_Color
pml_core_namespace['from'] = a_CT_Color
pml_core_namespace['to'] = a_CT_Color
pml_core_namespace['penClr'] = a_CT_Color
pml_core_namespace['bldSub'] = a_CT_AnimationGraphicalObjectBuildProperties
pml_core_namespace['pos'] = a_CT_Point2D  # 有冲突 CT_Comment
pml_core_namespace['font'] = a_CT_TextFont  # pml 冲突 父级类型: CT_EmbeddedFontListEntry
pml_core_namespace['notesSz'] = a_CT_PositiveSize2D
pml_core_namespace['gridSpacing'] = a_CT_PositiveSize2D
pml_core_namespace['defaultTextStyle'] = a_CT_TextListStyle
pml_core_namespace['clrMru'] = a_CT_ColorMRU
pml_core_namespace['clrMapOvr'] = a_CT_ColorMappingOverride
pml_core_namespace['bgRef'] = a_CT_StyleMatrixReference
pml_core_namespace['titleStyle'] = a_CT_TextListStyle
pml_core_namespace['bodyStyle'] = a_CT_TextListStyle
pml_core_namespace['otherStyle'] = a_CT_TextListStyle
pml_core_namespace['notesStyle'] = a_CT_TextListStyle
pml_core_namespace['scale'] = a_CT_Scale2D
pml_core_namespace['origin'] = a_CT_Point2D
pml_core_namespace['clrMap'] = a_CT_ColorMapping

# 属于dml中的媒体类型
pml_core_namespace['audioCd'] = a_CT_AudioCD
pml_core_namespace['wavAudioFile'] = a_CT_EmbeddedWAVAudioFile
pml_core_namespace['audioFile'] = a_CT_AudioFile
pml_core_namespace['videoFile'] = a_CT_VideoFile
pml_core_namespace['quickTimeFile'] = a_CT_QuickTimeFile
