"""
参考文档: https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/annexL/vml/ VML 简介.

以及ECMA-376 第一版 的 关于 vml 的文档.

- https://c-rex.net/samples/ooxml/e1/Part3/OOXML_P3_Primer_Introduction_topic_ID0EZA3O.html
- https://c-rex.net/samples/ooxml/e1/Part4/OOXML_P4_DOCX_VML_topic_ID0EZAUTB.html

本模块针对 vml-main.xsd 文档中定义的数据模型，

因为 vml 相对与 DrawingML 落后，所以该 vml 已不推荐.

在线 vml-main.xsd schema 参考: http://www.datypic.com/sc/ooxml/s-vml-main.xsd.html
"""

from __future__ import annotations

import logging
from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
)

from ecma376_office.oxml.base import OxmlBaseElement, ST_BaseEnumType, lookup
from ecma376_office.oxml.vml.const import NS_MAP as ns_map
from ecma376_office.oxml.vml.const import NameSpace_v as namespace_v

if TYPE_CHECKING:
    from ecma376_office.oxml.vml.drawing import (
        CT_Callout,
        CT_ClipPath,
        CT_Complex,
        CT_Diagram,
        CT_Extrusion,
        CT_Ink,
        CT_Lock,
        CT_SignatureLine,
        CT_Skew,
        CT_StrokeChild,
    )
    from ecma376_office.oxml.wml.main import CT_TxbxContent

logger = logging.getLogger(__name__)


def qn(tag: str):
    """将 dc:creator 这种的标签,转换为 {http://purl.org/dc/elements/1.1/}creator 这样的形式"""

    global ns_map

    if ':' not in tag:
        return tag

    ns_prefix, ns = tag.split(':')

    return f'{{{ns_map[ns_prefix]}}}{ns}'


class CT_Empty(OxmlBaseElement):
    """17.17.4 布尔属性 (CT_OnOff)

    此通用复杂类型指定了在整个 WordprocessingML 中使用的布尔属性。
    """

    @property
    def is_empty(self):
        return True


class AG_Id(OxmlBaseElement):
    """Unique Identifier

    <xsd:attributeGroup name="AG_Id">
        <xsd:attribute name="id" type="xsd:string" use="optional">
            <xsd:annotation>
            <xsd:documentation>Unique Identifier</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:attributeGroup>
    """

    @property
    def id(self) -> Optional[str]:
        """Unique Identifier

        Specifies a unique identifier that can be used to reference a VML object.

        Default is no value.

        [Example:

            <v:shape ... id="myShape" ... >
            </v:shape>

        end example]

        The possible values for this attribute are defined by the XML Schema string datatype.
        """

        val = self.attrib.get(qn('v:adj'))

        if val is not None:
            return str(val)
        return None


class AG_Style(OxmlBaseElement):
    """Shape Styling Properties

    <xsd:attributeGroup name="AG_Style">
        <xsd:attribute name="style" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Shape Styling Properties</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:attributeGroup>
    """

    @property
    def style(self) -> Optional[str]:
        """Shape Styling Properties

        指定了形状的 CSS2 样式属性。这使用了在 "Cascading Style Sheets, Level 2 规范" 中的 "视觉格式化模型" 部分描述的语法，这是万维网联盟的一个推荐标准，可以在这里找到：http://www.w3.org/TR/REC-CSS2。 这里不重复每个属性的完整描述，但是定义了每个属性在 VML 中的处理方式。允许的属性包括：

        Specifies the CSS2 styling properties of the shape. This uses the syntax described in the "Visual formatting model" of the Cascading Style Sheets, Level 2 specification, a Recommendation of the World Wide Web Consortium available here: http://www.w3.org/TR/REC-CSS2. Full descriptions of each property are not repeated here, but the VML treatment of each property is defined. Allowed properties include:

        flip

            指定形状的方向被翻转。默认值无。允许的值有：

            - x - 沿y轴翻转，反转x坐标。
            - y - 沿x轴翻转，反转y坐标。
            - xy - 沿y轴和x轴翻转。
            - yx - 沿x轴和y轴翻转。

            Specifies that the orientation of a shape is flipped. Default is no value. Allowed values are:

            - x - Flip along the y-axis, reversing the x-coordinates.
            - y - Flip along the x-axis, reversing the y-coordinates.
            - xy - Flip along both the y- and x-axis.
            - yx - Flip along both the x- and y-axis.

        height

            指定形状的容器块的高度。默认值为0。它以CSS单位指定，或者对于组中的元素，以父元素坐标系中的单位指定。允许的值包括：

            - auto - 页面流程中元素的默认位置。
            - <units> - 一个带有绝对单位指示符（厘米cm、毫米mm、英寸in、磅pt、派卡pc或像素px）或相对单位指示符（em或ex）的数字。如果没有给出单位，则假定为像素（px）。
            - <percentage> - 以父对象高度的百分比表示的值。

            Specifies the height of the containing block of the shape. Default is 0. It is specified in CSS units or, for elements in a group, in the coordinate system of the parent element. Allowed values are:

            - auto - Default position of an element in the flow of the page.
            - <units>- A number with an absolute units designator (cm, mm, in, pt, pc, or px) or a relative units designator (em or ex). If no units are given, pixels (px) is assumed.
            - <percentage>- Value expressed as a percentage of the parent object's height.

        left

            指定形状的容器块相对于页面流程中其左侧元素的左位置。默认值为0。它以CSS单位指定，或者对于组中的元素，以父元素坐标系中的单位指定。此属性不应用于内联锚定的形状。允许的值包括：

            - auto - 页面流程中元素的默认位置。
            - <units> - 一个带有绝对单位指示符（厘米cm、毫米mm、英寸in、磅pt、派卡pc或像素px）或相对单位指示符（em或ex）的数字。如果没有给出单位，则假定为像素（px）。
            - <percentage> - 以父对象宽度的百分比表示的值。

        width

            指定形状的容器块的宽度。默认值为0。它以CSS单位指定，或者对于组中的元素，以父元素坐标系中的单位指定。允许的值包括：

            - auto - 页面流程中元素的默认位置。
            - <units> - 一个带有绝对单位指示符（厘米cm、毫米mm、英寸in、磅pt、派卡pc或像素px）或相对单位指示符（em或ex）的数字。如果没有指定单位，则默认为像素（px）。
            - <percentage> - 以父对象宽度的百分比表示的值。

            Specifies the width of the containing block of the shape. Default is 0. It is specified in CSS units or, for elements in a group, in the coordinate system of the parent element. Allowed values are:

            - auto - Default position of an element in the flow of the page.
            - <units>- A number with an absolute units designator (cm, mm, in, pt, pc, or px) or a relative units designator (em or ex). If no units are given, pixels (px) is assumed.
            - <percentage>- Value expressed as a percentage of the parent object's width.

        ...

        The following properties are only used by the textbox element (§6.1.2.22):

        direction

            Specifies the direction of the text in the textbox. Default is ltr. This property is superceded by the mso-direction-alt property if that is specified. Allowed values are:

            - ltr - Test is displayed left-to-right.
            - rtl - Test is displayed right-to-left.

        ...

        The following properties are only used by the textpath element (§6.1.2.23):

        font

            Specifies a compound value of font settings. Default is no value. The values are the same as those of the CSS font property. The order of definitions in the string is: font-style, font-variant, font- weight, font-size, line-height, font-family.

        ...

        The line (§6.1.2.12), polyline (§6.1.2.15) and curve (§6.1.2.3) elements ignore the following properties:

        - top
        - left
        - width
        - height

        The following properties are not inherited by an element that references a shapetype element (§6.1.2.20) via the id attribute:

        - flip
        - height
        - left
        - margin-left
        - margin-top
        - position
        - rotation
        - top
        - visibility
        - width
        - z-index

        The possible values for this attribute are defined by the XML Schema string datatype.
        """

        val = self.attrib.get(qn('style'))

        if val is not None:
            return str(val)
        return None


class AG_Type(OxmlBaseElement):
    """

    <xsd:attributeGroup name="AG_Type">
        <xsd:attribute name="type" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Shape Type Reference</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:attributeGroup>
    """

    @property
    def type(self):
        """Shape Type Reference"""

        val = self.attrib.get(qn('v:type'))

        if val is not None:
            return str(val)
        return None


class AG_Adj(OxmlBaseElement):
    """Adjustment Parameters

    <xsd:attributeGroup name="AG_Adj">
        <xsd:attribute name="adj" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Adjustment Parameters</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:attributeGroup>
    """

    @property
    def adj(self) -> Optional[str]:
        """Adjustment Parameters

        指定一个由逗号分隔的参数列表或调整值，用于定义参数化公式的值。可以省略值。最多可以有8个调整值。每个值使用“#”后跟一个数字来引用，该数字对应于调整值列表中该值的从零开始的索引。例如，“#2”引用了adj列表中的第二个值。

        [示例：以下形状使用公式定义一个简单的矩形。adj值通过f元素的eqn属性（§6.1.2.4）引用，然后由path元素（§6.1.2.14）引用。]

        Specifies a comma-delimited list of parameters, or adjustment values, used to define values for a parameterized formula. Values may be omitted. There can be up to 8 adjust values. Each value is referenced using # followed by a number corresponding to the zero- based index for that value in the list of adjustment values. For example, #2 references the second value in the adj list.

        [Example: The following shape uses formulas to define a simple rectangle. The adj values are referenced by the eqn attribute of the f element (§6.1.2.4) and in turn referenced by the path element (§6.1.2.14).

            <v:shape
                coordorigin="0 0" coordsize="200 200"
                style="position:relative;top:30;left:30;width:20;height:20"
                adj="1, 1, 1, 200, 200, 200, 200, 1">
                <v:path v="m @0,@1 l @2,@3, @4,@5, @6,@7 x e"/>
                <v:formulas>
                    <v:f eqn="val #0"/>
                    <v:f eqn="val #1"/>
                    <v:f eqn="val #2"/>
                    <v:f eqn="val #3"/>
                    <v:f eqn="val #4"/>
                    <v:f eqn="val #5"/>
                    <v:f eqn="val #6"/>
                    <v:f eqn="val #7"/>
                </v:formulas>
            </v:shape>

        This is the equivalent of:

            <v:shape
                coordorigin="0 0" coordsize="200 200"
                style="position:relative;top:30;left:30;width:20;height:20"
                path="m 1,1 l 1,200, 200,200, 200,1 x e">
            </v:shape>

        end example]

        The possible values for this attribute are defined by the XML Schema string datatype.
        """
        val = self.attrib.get(qn('v:adj'))

        if val is not None:
            return str(val)
        return None


class AG_Path(OxmlBaseElement):
    """Edge Path

    <xsd:attributeGroup name="AG_Path">
        <xsd:attribute name="path" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Edge Path</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:attributeGroup>
    """

    @property
    def path(self) -> Optional[str]:
        val = self.attrib.get(qn('v:path'))

        if val is not None:
            return str(val)
        return None


class AG_Fill(OxmlBaseElement):
    """

    <xsd:attributeGroup name="AG_Fill">
        <xsd:attribute name="filled" type="ST_TrueFalse" use="optional">
            <xsd:annotation>
                <xsd:documentation>Shape Fill Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="fillcolor" type="ST_ColorType" use="optional">
            <xsd:annotation>
                <xsd:documentation>Fill Color</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:attributeGroup>
    """

    @property
    def filled(self) -> Optional[ST_TrueFalse]:
        """Shape Fill Toggle"""

        val = self.attrib.get(qn('v:filled'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def fillcolor(self) -> Optional[ST_ColorType]:
        """Fill Color"""

        val = self.attrib.get(qn('v:fillcolor'))

        if val is not None:
            return ST_ColorType(val)
        return None


class AG_Chromakey(OxmlBaseElement):
    """
    <xsd:attributeGroup name="AG_Chromakey">
        <xsd:attribute name="chromakey" type="ST_ColorType" use="optional">
            <xsd:annotation>
                <xsd:documentation>Image Transparency Color</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:attributeGroup>
    """

    @property
    def chromakey(self) -> Optional[ST_ColorType]:
        """Image Transparency Color

        Specifies a color value that will be transparent and show anything behind the shape.

        Default is no value.

        [Example:

            <v:image ... chromakey="white" ...>
            </v:image>

        end example]

        The possible values for this attribute are defined by the ST_ColorType simple type (§6.1.3.1).
        """

        val = self.attrib.get(qn('v:chromakey'))

        if val is not None:
            return ST_ColorType(val)
        return None


class AG_Ext(OxmlBaseElement):
    """
    <xsd:attributeGroup name="AG_Ext">
        <xsd:attribute name="ext" form="qualified" type="ST_Ext">
            <xsd:annotation>
                <xsd:documentation>VML Extension Handling Behavior</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:attributeGroup>
    """

    @property
    def ext(self) -> Optional[ST_Ext]:
        """VML Extension Handling Behavior"""

        val = self.attrib.get(qn('v:ext'))

        if val is not None:
            return ST_Ext(val)
        return None


class AG_CoreAttributes(AG_Id, AG_Style):
    """
    <xsd:attributeGroup name="AG_CoreAttributes">
        <xsd:attributeGroup ref="AG_Id" />
        <xsd:attributeGroup ref="AG_Style" />
        <xsd:attribute name="href" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Hyperlink Target</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="target" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Hyperlink Display Target</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="class" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>CSS Reference</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="title" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Shape Title</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="alt" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Alternate Text</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="coordsize" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Coordinate Space Size</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="coordorigin" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Coordinate Space Origin</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="wrapcoords" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Shape Bounding Polygon</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="print" type="ST_TrueFalse" use="optional">
            <xsd:annotation>
                <xsd:documentation>Print Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:attributeGroup>
    """

    @property
    def href(self) -> Optional[str]:
        """Hyperlink Target"""

        val = self.attrib.get(qn('v:href'))

        if val is not None:
            return str(val)
        return None

    @property
    def target(self) -> Optional[str]:
        """Hyperlink Display Target"""

        val = self.attrib.get(qn('v:target'))

        if val is not None:
            return str(val)
        return None

    @property
    def class_(self) -> Optional[str]:
        """CSS Reference"""

        val = self.attrib.get(qn('v:class'))

        if val is not None:
            return str(val)
        return None

    @property
    def title(self) -> Optional[str]:
        """Shape Title"""

        val = self.attrib.get(qn('v:title'))

        if val is not None:
            return str(val)
        return None

    @property
    def alt(self) -> Optional[str]:
        """Alternate Text

        Specifies alternative text describing the graphical object. This text should provide a brief description of the shape for use by accessibility tools. Default is no value.

        [Example: The alt text describes the basic shape:

        <v:shape ... fillcolor="red"
        alt="Red rectangle">
        </v:shape>

        The alt text describes the contents of a shape displaying an image:

        <v:shape ... alt="Picture of a sunset">
        </v:shape>

        end example]

        The possible values for this attribute are defined by the XML Schema string datatype.
        """

        val = self.attrib.get(qn('v:alt'))

        if val is not None:
            return str(val)
        return None

    @property
    def coordsize(self) -> Optional[str]:
        """Coordinate Space Size"""

        val = self.attrib.get(qn('v:coordsize'))

        if val is not None:
            return str(val)
        return None

    @property
    def coordorigin(self) -> Optional[str]:
        """Coordinate Space Origin"""

        val = self.attrib.get(qn('v:coordorigin'))

        if val is not None:
            return str(val)
        return None

    @property
    def wrapcoords(self) -> Optional[str]:
        """Shape Bounding Polygon"""

        val = self.attrib.get(qn('v:wrapcoords'))

        if val is not None:
            return str(val)
        return None

    @property
    def print(self) -> Optional[ST_TrueFalse]:
        """Print Toggle"""

        val = self.attrib.get(qn('v:print'))

        if val is not None:
            return ST_TrueFalse(val)
        return None


class AG_OfficeShapeAttributes(OxmlBaseElement):
    """
    <xsd:attributeGroup name="AG_OfficeShapeAttributes">
        <xsd:attribute ref="o:spt">
            <xsd:annotation>
                <xsd:documentation>Optional Number</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:connectortype">
            <xsd:annotation>
                <xsd:documentation>Shape Connector Type</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:bwmode">
            <xsd:annotation>
                <xsd:documentation>Black-and-White Mode</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:bwpure">
            <xsd:annotation>
                <xsd:documentation>Pure Black-and-White Mode</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:bwnormal">
            <xsd:annotation>
                <xsd:documentation>Normal Black-and-White Mode</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:forcedash">
            <xsd:annotation>
                <xsd:documentation>Force Dashed Outline</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:oleicon">
            <xsd:annotation>
                <xsd:documentation>Embedded Object Icon Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:ole">
            <xsd:annotation>
                <xsd:documentation>Embedded Object Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:preferrelative">
            <xsd:annotation>
                <xsd:documentation>Relative Resize Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:cliptowrap">
            <xsd:annotation>
                <xsd:documentation>Clip to Wrapping Polygon</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:clip">
            <xsd:annotation>
                <xsd:documentation>Clipping Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:attributeGroup>
    """

    @property
    def o_spt(self) -> Optional[float]:
        """Optional Number"""
        val = self.attrib.get(qn('o:spt'))

        if val is not None:
            return float(val)
        return None

    @property
    def o_connectortype(self):
        """Shape Connector Type"""

        from ecma376_office.oxml.vml.drawing import ST_ConnectorType

        val = self.attrib.get(qn('o:connectortype'))

        if val is not None:
            return ST_ConnectorType(val)
        return None

    @property
    def o_bwmode(self):
        """Black-and-White Mode"""

        from ecma376_office.oxml.vml.drawing import ST_BWMode

        val = self.attrib.get(qn('o:bwmode'))

        if val is not None:
            return ST_BWMode(val)
        return None

    @property
    def o_bwpure(self):
        """Pure Black-and-White Mode"""

        from ecma376_office.oxml.vml.drawing import ST_BWMode

        val = self.attrib.get(qn('o:bwpure'))

        if val is not None:
            return ST_BWMode(val)
        return None

    @property
    def o_bwnormal(self):
        """Normal Black-and-White Mode"""

        from ecma376_office.oxml.vml.drawing import ST_BWMode

        val = self.attrib.get(qn('o:bwnormal'))

        if val is not None:
            return ST_BWMode(val)
        return None

    @property
    def o_forcedash(self):
        """Force Dashed Outline"""

        from ecma376_office.oxml.vml.drawing import ST_TrueFalse

        val = self.attrib.get(qn('o:forcedash'))
        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def o_oleicon(self):
        """Embedded Object Icon Toggle"""

        from ecma376_office.oxml.vml.drawing import ST_TrueFalse

        val = self.attrib.get(qn('o:oleicon'))
        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def o_ole(self):
        """Embedded Object Toggle"""
        from ecma376_office.oxml.vml.drawing import ST_TrueFalseBlank

        val = self.attrib.get(qn('o:ole'))

        if val is not None:
            return ST_TrueFalseBlank(val)
        return None

    @property
    def o_preferrelative(self):
        """Relative Resize Toggle"""

        from ecma376_office.oxml.vml.drawing import ST_TrueFalse

        val = self.attrib.get(qn('o:preferrelative'))
        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def o_cliptowrap(self):
        """Clip to Wrapping Polygon"""

        from ecma376_office.oxml.vml.drawing import ST_TrueFalse

        val = self.attrib.get(qn('o:cliptowrap'))
        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def o_clip(self):
        """Clipping Toggle"""

        from ecma376_office.oxml.vml.drawing import ST_TrueFalse

        val = self.attrib.get(qn('o:clip'))
        if val is not None:
            return ST_TrueFalse(val)
        return None


class AG_ShapeAttributes(AG_Chromakey, AG_Fill):
    """
    <xsd:attributeGroup name="AG_ShapeAttributes">
        <xsd:attributeGroup ref="AG_Chromakey" />
        <xsd:attributeGroup ref="AG_Fill" />
        <xsd:attribute name="opacity" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Fill Color Opacity</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="stroked" type="ST_TrueFalse" use="optional">
            <xsd:annotation>
                <xsd:documentation>Shape Stroke Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="strokecolor" type="ST_ColorType" use="optional">
            <xsd:annotation>
                <xsd:documentation>Shape Stroke Color</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="strokeweight" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Shape Stroke Weight</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="insetpen" type="ST_TrueFalse" use="optional">
            <xsd:annotation>
                <xsd:documentation>Inset Border From Path</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:attributeGroup>
    """

    @property
    def opacity(self) -> Optional[str]:
        """Fill Color Opacity"""

        val = self.attrib.get(qn('v:opacity'))

        if val is not None:
            return str(val)
        return None

    @property
    def stroked(self) -> Optional[ST_TrueFalse]:
        """Shape Stroke Toggle"""

        val = self.attrib.get(qn('v:stroked'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def strokecolor(self) -> Optional[ST_ColorType]:
        """Shape Stroke Color"""

        val = self.attrib.get(qn('v:strokecolor'))

        if val is not None:
            return ST_ColorType(val)
        return None

    @property
    def strokeweight(self) -> Optional[str]:
        """Shape Stroke Weight"""

        val = self.attrib.get(qn('v:strokeweight'))

        if val is not None:
            return str(val)
        return None

    @property
    def insetpen(self) -> Optional[ST_TrueFalse]:
        """Inset Border From Path"""

        val = self.attrib.get(qn('v:insetpen'))

        if val is not None:
            return ST_TrueFalse(val)
        return None


class AG_OfficeCoreAttributes(OxmlBaseElement):
    """
    <xsd:attributeGroup name="AG_OfficeCoreAttributes">
        <xsd:attribute ref="o:spid">
            <xsd:annotation>
                <xsd:documentation>Optional String</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:oned">
            <xsd:annotation>
                <xsd:documentation>Shape Handle Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:regroupid">
            <xsd:annotation>
                <xsd:documentation>Regroup ID</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:doubleclicknotify">
            <xsd:annotation>
                <xsd:documentation>Double-click Notification Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:button">
            <xsd:annotation>
                <xsd:documentation>Button Behavior Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:userhidden">
            <xsd:annotation>
                <xsd:documentation>Hide Script Anchors</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:bullet">
            <xsd:annotation>
                <xsd:documentation>Graphical Bullet</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:hr">
            <xsd:annotation>
                <xsd:documentation>Horizontal Rule Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:hrstd">
            <xsd:annotation>
                <xsd:documentation>Horizontal Rule Standard Display Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:hrnoshade">
            <xsd:annotation>
                <xsd:documentation>Horizontal Rule 3D Shading Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:hrpct">
            <xsd:annotation>
                <xsd:documentation>Horizontal Rule Length Percentage</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:hralign">
            <xsd:annotation>
                <xsd:documentation>Horizontal Rule Alignment</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:allowincell">
            <xsd:annotation>
                <xsd:documentation>Allow in Table Cell</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:allowoverlap">
            <xsd:annotation>
                <xsd:documentation>Allow Shape Overlap</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:userdrawn">
            <xsd:annotation>
                <xsd:documentation>Exists In Master Slide</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:bordertopcolor">
            <xsd:annotation>
                <xsd:documentation>Border Top Color</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:borderleftcolor">
            <xsd:annotation>
                <xsd:documentation>Border Left Color</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:borderbottomcolor">
            <xsd:annotation>
                <xsd:documentation>Bottom Border Color</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:borderrightcolor">
            <xsd:annotation>
                <xsd:documentation>Border Right Color</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:dgmlayout">
            <xsd:annotation>
                <xsd:documentation>Diagram Node Layout Identifier</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:dgmnodekind">
            <xsd:annotation>
                <xsd:documentation>Diagram Node Identifier</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:dgmlayoutmru">
            <xsd:annotation>
                <xsd:documentation>Diagram Node Recent Layout Identifier</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:insetmode">
            <xsd:annotation>
                <xsd:documentation>Text Inset Mode</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:attributeGroup>
    """

    @property
    def o_spid(self) -> Optional[str]:
        """Optional String"""

        val = self.attrib.get(qn('o:spid'))

        if val is not None:
            return str(val)
        return None

    @property
    def o_oned(self):
        """Shape Handle Toggle"""

        from ecma376_office.oxml.vml.drawing import ST_TrueFalse

        val = self.attrib.get(qn('o:oned'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def o_regroupid(self) -> Optional[int]:
        """Regroup ID"""

        val = self.attrib.get(qn('o:regroupid'))

        if val is not None:
            return int(val)
        return None

    @property
    def o_doubleclicknotify(self):
        """Double-click Notification Toggle"""

        from ecma376_office.oxml.vml.drawing import ST_TrueFalse

        val = self.attrib.get(qn('o:doubleclicknotify'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def o_button(self):
        """Button Behavior Toggle

        Specifies whether a shape will exhibit button press behavior on click. Default is false.

        [Example:

        <v:shape ... o:button="true" ... >
        </v:shape>

        end example]

        The possible values for this attribute are defined by the ST_TrueFalse simple type (§6.2.3.23).
        """

        from ecma376_office.oxml.vml.drawing import ST_TrueFalse

        val = self.attrib.get(qn('o:button'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def o_userhidden(self):
        """Hide Script Anchors"""

        from ecma376_office.oxml.vml.drawing import ST_TrueFalse

        val = self.attrib.get(qn('o:userhidden'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def o_bullet(self):
        """Graphical Bullet

        Specifies whether the shape is a graphical bullet. Default is false.

        [Example:

        <v:shape ... o:bullet="true" ... >
        </v:shape>

        end example]

        The possible values for this attribute are defined by the ST_TrueFalse simple type (§6.2.3.23).
        """

        from ecma376_office.oxml.vml.drawing import ST_TrueFalse

        val = self.attrib.get(qn('o:bullet'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def o_hr(self):
        """Horizontal Rule Toggle"""

        from ecma376_office.oxml.vml.drawing import ST_TrueFalse

        val = self.attrib.get(qn('o:hr'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def o_hrstd(self):
        """Horizontal Rule Standard Display Toggle"""

        from ecma376_office.oxml.vml.drawing import ST_TrueFalse

        val = self.attrib.get(qn('o:hrstd'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def o_hrnoshade(self):
        """Horizontal Rule 3D Shading Toggle"""

        from ecma376_office.oxml.vml.drawing import ST_TrueFalse

        val = self.attrib.get(qn('o:hrnoshade'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def o_hrpct(self) -> Optional[float]:
        """Horizontal Rule Length Percentage"""

        val = self.attrib.get(qn('o:hrpct'))

        if val is not None:
            return float(val)
        return None

    @property
    def o_hralign(self):
        """Horizontal Rule Alignment"""

        from ecma376_office.oxml.vml.drawing import ST_HrAlign

        val = self.attrib.get(qn('o:hralign'))

        if val is not None:
            return ST_HrAlign(val)

        return ST_HrAlign('left')

    @property
    def o_allowincell(self):
        """Allow in Table Cell

        Specifies whether a shape can be placed in a table. Default is false.

        [Example:

            <v:shape ... o:allowincell="true" ... >
            </v:shape>

        end example]

        The possible values for this attribute are defined by the ST_TrueFalse simple type (§6.2.3.23).
        """

        from ecma376_office.oxml.vml.drawing import ST_TrueFalse

        val = self.attrib.get(qn('o:allowincell'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def o_allowoverlap(self):
        """Allow Shape Overlap

        Specifies whether a shape can overlap another shape. Default is true. If false, the shape will shift left or right so as not to overlap another shape, similar to the behavior of the HTML float attribute.

        [Example:

            <v:shape ... o:allowoverlap="false" ... >
            </v:shape>

        end example]

        The possible values for this attribute are defined by the ST_TrueFalse simple type (§6.2.3.23).
        """

        from ecma376_office.oxml.vml.drawing import ST_TrueFalse

        val = self.attrib.get(qn('o:allowoverlap'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def o_userdrawn(self):
        """Exists In Master Slide"""

        from ecma376_office.oxml.vml.drawing import ST_TrueFalse

        val = self.attrib.get(qn('o:userdrawn'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def o_bordertopcolor(self) -> Optional[str]:
        """Border Top Color

        Specifies the top border color of an inline shape. Default is no value.

        [Example:

        <v:shape ... o:bordertopcolor="red" ... >
        </v:shape>

        end example]

        The possible values for this attribute are defined by the XML Schema string datatype.
        """

        val = self.attrib.get(qn('o:bordertopcolor'))

        if val is not None:
            return str(val)
        return None

    @property
    def o_borderleftcolor(self) -> Optional[str]:
        """Border Left Color

        Specifies the left border color of an inline shape. Default is no value.

        [Example:

            <v:shape ... o:borderleftcolor="red" ... >
            </v:shape>

        end example]

        The possible values for this attribute are defined by the XML Schema string datatype.
        """

        val = self.attrib.get(qn('o:borderleftcolor'))

        if val is not None:
            return str(val)
        return None

    @property
    def o_borderbottomcolor(self) -> Optional[str]:
        """Bottom Border Color

        Specifies the bottom border color of an inline shape. Default is no value.

        [Example:

            <v:shape ... o:borderbottomcolor="red" ... >
            </v:shape>

        end example]

        The possible values for this attribute are defined by the XML Schema string datatype.
        """

        val = self.attrib.get(qn('o:borderbottomcolor'))

        if val is not None:
            return str(val)
        return None

    @property
    def o_borderrightcolor(self) -> Optional[str]:
        """Border Right Color

        Specifies the right border color of an inline shape. Default is no value.

        [Example:

            <v:shape ... o:borderrightcolor="red" ... >
            </v:shape>

        end example]

        The possible values for this attribute are defined by the XML Schema string datatype.
        """

        val = self.attrib.get(qn('o:borderrightcolor'))

        if val is not None:
            return str(val)
        return None

    @property
    def o_dgmlayout(self) -> Optional[int]:
        """Diagram Node Layout Identifier"""

        val = self.attrib.get(qn('o:dgmlayout'))

        if val is not None:
            return int(val)
        return None

    @property
    def o_dgmnodekind(self) -> Optional[int]:
        """Diagram Node Identifier"""

        val = self.attrib.get(qn('o:dgmnodekind'))

        if val is not None:
            return int(val)
        return None

    @property
    def o_dgmlayoutmru(self) -> Optional[int]:
        """Diagram Node Recent Layout Identifier"""

        val = self.attrib.get(qn('o:dgmlayoutmru'))

        if val is not None:
            return int(val)
        return None

    @property
    def o_insetmode(self):
        """Text Inset Mode"""

        from ecma376_office.oxml.vml.drawing import ST_InsetMode

        val = self.attrib.get(qn('o:insetmode'))

        if val is not None:
            return ST_InsetMode(val)

        return ST_InsetMode('custom')


class AG_AllCoreAttributes(AG_CoreAttributes, AG_OfficeCoreAttributes):
    """
    <xsd:attributeGroup name="AG_AllCoreAttributes">
        <xsd:attributeGroup ref="AG_CoreAttributes" />
        <xsd:attributeGroup ref="AG_OfficeCoreAttributes" />
    </xsd:attributeGroup>
    """



class AG_AllShapeAttributes(AG_ShapeAttributes, AG_OfficeShapeAttributes):
    """

    <xsd:attributeGroup name="AG_AllShapeAttributes">
        <xsd:attributeGroup ref="AG_ShapeAttributes" />
        <xsd:attributeGroup ref="AG_OfficeShapeAttributes" />
    </xsd:attributeGroup>
    """



class AG_ImageAttributes(OxmlBaseElement):
    """
    <xsd:attributeGroup name="AG_ImageAttributes">
        <xsd:attribute name="src" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Image Source</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="cropleft" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Image Left Crop</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="croptop" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Image Top Crop</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="cropright" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Image Right Crop</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="cropbottom" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Image Bottom Crop</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="gain" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Image Intensity</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="blacklevel" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Image Brightness</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="gamma" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Image Gamma Correction</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="grayscale" type="ST_TrueFalse" use="optional">
            <xsd:annotation>
                <xsd:documentation>Image Grayscale Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="bilevel" type="ST_TrueFalse" use="optional">
            <xsd:annotation>
                <xsd:documentation>Image Bilevel Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:attributeGroup>
    """

    @property
    def src(self) -> Optional[str]:
        """Image Source

        Specifies the URL of the image to use.

        [Example:

        <v:image ... src="myimage.gif" ...>
        </v:image>

        end example]

        The possible values for this attribute are defined by the XML Schema string datatype.
        """
        val = self.attrib.get(qn('v:src'))

        if val is not None:
            return str(val)
        return None

    @property
    def cropleft(self) -> Optional[str]:
        """Image Left Crop

        Specifies how much to crop the image from the left in as a fraction of picture size.

        Default is 0. This numeric value may also be specified in 1/65536-ths if a trailing "f" is supplied. For example, a value of "52429f" represents 52429/65536 or 0.8.

        [Example:

            <v:image ... cropleft="10%" ...>
            </v:image>

        end example]

        The possible values for this attribute are defined by the XML Schema string datatype.
        """
        val = self.attrib.get(qn('v:cropleft'))

        if val is not None:
            return str(val)
        return None

    @property
    def croptop(self) -> Optional[str]:
        """Image Top Crop

        Specifies how much to crop the image from the top down as a fraction of picture size.

        Default is 0. This numeric value may also be specified in 1/65536-ths if a trailing "f" is supplied. For example, a value of "52429f" represents 52429/65536 or 0.8.

        [Example:

        <v:image ... croptop="10%" ...>
        </v:image>

        end example]

        The possible values for this attribute are defined by the XML Schema string datatype.
        """
        val = self.attrib.get(qn('v:croptop'))

        if val is not None:
            return str(val)
        return None

    @property
    def cropright(self) -> Optional[str]:
        """Image Right Crop

        Specifies how much to crop the image from the right in as a fraction of picture size.

        Default is 0. This numeric value may also be specified in 1/65536-ths if a trailing "f" is supplied. For example, a value of "52429f" represents 52429/65536 or 0.8.

        [Example:

            <v:image ... cropright="10%" ...>
            </v:image>

        end example]

        The possible values for this attribute are defined by the XML Schema string datatype.
        """
        val = self.attrib.get(qn('v:cropright'))

        if val is not None:
            return str(val)
        return None

    @property
    def cropbottom(self) -> Optional[str]:
        """Image Bottom Crop

        Specifies the how much to crop the image from the bottom up as a fraction of picture size. Default is 0. This numeric value may also be specified in 1/65536-ths if a trailing "f" is supplied. For example, a value of "52429f" represents 52429/65536 or 0.8.

        [Example:

        <v:image ... cropbottom="10%" ...>
        </v:image>

        end example]

        The possible values for this attribute are defined by the XML Schema string datatype.
        """
        val = self.attrib.get(qn('v:cropbottom'))

        if val is not None:
            return str(val)
        return None

    @property
    def gain(self) -> Optional[str]:
        """Image Intensity

        Specifies an adjustment for the intensity of all colors. Essentially sets how bright white will be. Default is 1.

        [Example:

            <v:image ... gain="0.5" ...>
            </v:image>

        end example]

        The possible values for this attribute are defined by the XML Schema string datatype.
        """
        val = self.attrib.get(qn('v:gain'))

        if val is not None:
            return str(val)
        return None

    @property
    def blacklevel(self) -> Optional[str]:
        """Image Brightness

        Specifies the image brightness. Default is 0.

        [Example:

            <v:image ... blacklevel="0.1" ...>
            </v:image>

        end example]

        The possible values for this attribute are defined by the XML Schema string datatype.
        """
        val = self.attrib.get(qn('v:blacklevel'))

        if val is not None:
            return str(val)
        return None

    @property
    def gamma(self) -> Optional[str]:
        """Image Gamma Correction

        Specifies the gamma correction. Default is 1.

        Gamma correction is a factor by which the intended target display gamma differs from the sRGB profile. It can be used to correct for images not prepared for sRGB displays and to adjust overall image contrast. Decreasing it below 1 gives a higher contrast image.

        [Example:

            <v:image ... gamma="0.5" ...>
            </v:image>

        end example]

        The possible values for this attribute are defined by the XML Schema string datatype.
        """
        val = self.attrib.get(qn('v:gamma'))

        if val is not None:
            return str(val)
        return None

    @property
    def grayscale(self) -> Optional[ST_TrueFalse]:
        """Image Grayscale Toggle

        Specifies to display the image in grayscale. Default is false.

        [Example:

        <v:image ... gamma="0.5" ...>
        </v:image>

        end example]

        The possible values for this attribute are defined by the ST_TrueFalse simple type (§6.1.3.14).
        """
        val = self.attrib.get(qn('v:grayscale'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def bilevel(self) -> Optional[ST_TrueFalse]:
        """Image Bilevel Toggle

        Specifies that all colors in the picture shall be converted to either 0 or full intensity component values. This converts a color bitmap to 8 colors and a grayscale bitmap to black and white. Default is false.

        [Example:

            <v:image ... bilevel="true" ...>
            </v:image>

        end example]

        The possible values for this attribute are defined by the ST_TrueFalse simple type (§6.1.3.14).

        """
        val = self.attrib.get(qn('v:bilevel'))

        if val is not None:
            return ST_TrueFalse(val)
        return None


class AG_StrokeAttributes(OxmlBaseElement):
    """
    <xsd:attributeGroup name="AG_StrokeAttributes">
        <xsd:attribute name="on" type="ST_TrueFalse" use="optional">
            <xsd:annotation>
                <xsd:documentation>Stroke Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="weight" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Stroke Weight</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="color" type="ST_ColorType" use="optional">
            <xsd:annotation>
                <xsd:documentation>Stroke Color</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="opacity" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Stroke Opacity</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="linestyle" type="ST_StrokeLineStyle" use="optional">
            <xsd:annotation>
                <xsd:documentation>Stroke Line Style</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="miterlimit" type="xsd:decimal" use="optional">
            <xsd:annotation>
                <xsd:documentation>Miter Joint Limit</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="joinstyle" type="ST_StrokeJoinStyle" use="optional">
            <xsd:annotation>
                <xsd:documentation>Line End Join Style</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="endcap" type="ST_StrokeEndCap" use="optional">
            <xsd:annotation>
                <xsd:documentation>Line End Cap</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="dashstyle" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Stroke Dash Pattern</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="filltype" type="ST_FillType" use="optional">
            <xsd:annotation>
                <xsd:documentation>Stroke Image Style</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="src" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Stroke Image Location</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="imageaspect" type="ST_ImageAspect" use="optional">
            <xsd:annotation>
                <xsd:documentation>Stroke Image Aspect Ratio</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="imagesize" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Stroke Image Size</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="imagealignshape" type="ST_TrueFalse" use="optional">
            <xsd:annotation>
                <xsd:documentation>Stoke Image Alignment</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="color2" type="ST_ColorType" use="optional">
            <xsd:annotation>
                <xsd:documentation>Stroke Alternate Pattern Color</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="startarrow" type="ST_StrokeArrowType" use="optional">
            <xsd:annotation>
                <xsd:documentation>Line Start Arrowhead</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="startarrowwidth" type="ST_StrokeArrowWidth" use="optional">
            <xsd:annotation>
                <xsd:documentation>Line Start Arrowhead Width</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="startarrowlength" type="ST_StrokeArrowLength" use="optional">
            <xsd:annotation>
                <xsd:documentation>Line Start Arrowhead Length</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="endarrow" type="ST_StrokeArrowType" use="optional">
            <xsd:annotation>
                <xsd:documentation>Line End Arrowhead</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="endarrowwidth" type="ST_StrokeArrowWidth" use="optional">
            <xsd:annotation>
                <xsd:documentation>Line End Arrowhead Width</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="endarrowlength" type="ST_StrokeArrowLength" use="optional">
            <xsd:annotation>
                <xsd:documentation>Line End Arrowhead Length</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:href">
            <xsd:annotation>
                <xsd:documentation>Original Image Reference</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:althref">
            <xsd:annotation>
                <xsd:documentation>Alternate Image Reference</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:title">
            <xsd:annotation>
                <xsd:documentation>Stroke Title</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:forcedash">
            <xsd:annotation>
                <xsd:documentation>Force Dashed Outline</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="r:id" use="optional">
            <xsd:annotation>
                <xsd:documentation>Relationship</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="insetpen" type="ST_TrueFalse" use="optional">
            <xsd:annotation>
                <xsd:documentation>Inset Border From Path</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:relid">
            <xsd:annotation>
                <xsd:documentation>Relationship to Part</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:attributeGroup>
    """

    @property
    def on(self) -> Optional[ST_TrueFalse]:
        """Stroke Toggle"""
        val = self.attrib.get(qn('v:on'))
        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def weight(self) -> Optional[str]:
        """Stroke Weight"""
        val = self.attrib.get(qn('v:weight'))
        if val is not None:
            return str(val)
        return None

    @property
    def color(self) -> Optional[ST_ColorType]:
        """Stroke Color"""
        val = self.attrib.get(qn('v:color'))
        if val is not None:
            return ST_ColorType(val)
        return None

    @property
    def opacity(self) -> Optional[str]:
        """Stroke Opacity"""
        val = self.attrib.get(qn('v:opacity'))
        if val is not None:
            return str(val)
        return None

    @property
    def linestyle(self) -> Optional[ST_StrokeLineStyle]:
        """Stroke Line Style"""
        val = self.attrib.get(qn('v:linestyle'))
        if val is not None:
            return ST_StrokeLineStyle(val)
        return None

    @property
    def miterlimit(self) -> Optional[float]:
        """Miter Joint Limit"""

        val = self.attrib.get(qn('v:miterlimit'))

        if val is not None:
            return float(val)
        return None

    @property
    def joinstyle(self) -> Optional[ST_StrokeJoinStyle]:
        """Line End Join Style"""
        val = self.attrib.get(qn('v:joinstyle'))
        if val is not None:
            return ST_StrokeJoinStyle(val)
        return None

    @property
    def endcap(self) -> Optional[ST_StrokeEndCap]:
        """Line End Cap"""
        val = self.attrib.get(qn('v:endcap'))
        if val is not None:
            return ST_StrokeEndCap(val)
        return None

    @property
    def dashstyle(self) -> Optional[str]:
        """Stroke Dash Pattern"""
        val = self.attrib.get(qn('v:dashstyle'))
        if val is not None:
            return str(val)
        return None

    @property
    def filltype(self) -> Optional[ST_FillType]:
        """Stroke Image Style"""
        val = self.attrib.get(qn('v:filltype'))
        if val is not None:
            return ST_FillType(val)
        return None

    @property
    def src(self) -> Optional[str]:
        """Stroke Image Location"""
        val = self.attrib.get(qn('v:src'))
        if val is not None:
            return str(val)
        return None

    @property
    def imageaspect(self) -> Optional[ST_ImageAspect]:
        """Stroke Image Aspect Ratio"""
        val = self.attrib.get(qn('v:imageaspect'))
        if val is not None:
            return ST_ImageAspect(val)
        return None

    @property
    def imagesize(self) -> Optional[str]:
        """Stroke Image Size"""
        val = self.attrib.get(qn('v:imagesize'))
        if val is not None:
            return str(val)
        return None

    @property
    def imagealignshape(self) -> Optional[ST_TrueFalse]:
        """Stoke Image Alignment"""
        val = self.attrib.get(qn('v:imagealignshape'))
        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def color2(self) -> Optional[ST_ColorType]:
        """Stroke Alternate Pattern Color"""
        val = self.attrib.get(qn('v:color2'))
        if val is not None:
            return ST_ColorType(val)
        return None

    @property
    def startarrow(self) -> Optional[ST_StrokeArrowType]:
        """Line Start Arrowhead"""
        val = self.attrib.get(qn('v:startarrow'))
        if val is not None:
            return ST_StrokeArrowType(val)
        return None

    @property
    def startarrowwidth(self) -> Optional[ST_StrokeArrowWidth]:
        """Line Start Arrowhead Width"""
        val = self.attrib.get(qn('v:startarrowwidth'))
        if val is not None:
            return ST_StrokeArrowWidth(val)
        return None

    @property
    def startarrowlength(self) -> Optional[ST_StrokeArrowLength]:
        """Line Start Arrowhead Length"""
        val = self.attrib.get(qn('v:startarrowlength'))
        if val is not None:
            return ST_StrokeArrowLength(val)
        return None

    @property
    def endarrow(self) -> Optional[ST_StrokeArrowType]:
        """Line End Arrowhead"""
        val = self.attrib.get(qn('v:endarrow'))
        if val is not None:
            return ST_StrokeArrowType(val)
        return None

    @property
    def endarrowwidth(self) -> Optional[ST_StrokeArrowWidth]:
        """Line End Arrowhead Width"""
        val = self.attrib.get(qn('v:endarrowwidth'))
        if val is not None:
            return ST_StrokeArrowWidth(val)
        return None

    @property
    def endarrowlength(self) -> Optional[ST_StrokeArrowLength]:
        """Line End Arrowhead Length"""
        val = self.attrib.get(qn('v:endarrowlength'))
        if val is not None:
            return ST_StrokeArrowLength(val)
        return None

    @property
    def o_href(self) -> Optional[str]:
        """Original Image Reference"""

        val = self.attrib.get(qn('o:href'))
        if val is not None:
            return str(val)
        return None

    @property
    def o_althref(self) -> Optional[str]:
        """Alternate Image Reference"""

        val = self.attrib.get(qn('o:althref'))
        if val is not None:
            return str(val)
        return None

    @property
    def o_title(self) -> Optional[str]:
        """Stroke Title"""

        val = self.attrib.get(qn('o:title'))
        if val is not None:
            return str(val)
        return None

    @property
    def o_forcedash(self):
        """Force Dashed Outline"""

        from ecma376_office.oxml.vml.drawing import ST_TrueFalse

        val = self.attrib.get(qn('o:forcedash'))
        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def r_id(self) -> Optional[Any]:
        """Relationship"""

        val = self.attrib.get(qn('r:id'))
        if val is not None:
            return str(val)
        return None

    @property
    def insetpen(self) -> Optional[ST_TrueFalse]:
        """Inset Border From Path"""
        val = self.attrib.get(qn('v:insetpen'))
        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def o_relid(self):
        """Relationship to Part"""

        from ecma376_office.oxml.vml.drawing import ST_RelationshipId

        val = self.attrib.get(qn('o:relid'))
        if val is not None:
            return ST_RelationshipId(val)
        return None


class EG_ShapeElements(OxmlBaseElement):
    """

    <xsd:group name="EG_ShapeElements">
        <xsd:choice>
            <xsd:element ref="path" />
            <xsd:element ref="formulas" />
            <xsd:element ref="handles" />
            <xsd:element ref="fill" />
            <xsd:element ref="stroke" />
            <xsd:element ref="shadow" />
            <xsd:element ref="textbox" />
            <xsd:element ref="textpath" />
            <xsd:element ref="imagedata" />
            <xsd:element ref="o:skew" />
            <xsd:element ref="o:extrusion" />
            <xsd:element ref="o:callout" />
            <xsd:element ref="o:lock" />
            <xsd:element ref="o:clippath" />
            <xsd:element ref="o:signatureline" />
            <xsd:element ref="wvml:wrap" />
            <xsd:element ref="wvml:anchorlock" />
            <xsd:element ref="wvml:bordertop" />
            <xsd:element ref="wvml:borderbottom" />
            <xsd:element ref="wvml:borderleft" />
            <xsd:element ref="wvml:borderright" />
            <xsd:element ref="x:ClientData" minOccurs="0" />
            <xsd:element ref="p:textdata" minOccurs="0" />
        </xsd:choice>
    </xsd:group>
    """

    @property
    def path(self) -> Optional[CT_Path]:
        """6.1.2.14 path (Shape Path)

        此元素定义了构成形状的路径。这是通过包含丰富笔触移动命令的字符串来完成的。此元素还描述了拉伸点、内嵌文本框矩形位置和连接点位置。拉伸定义和公式元素（§6.1.2.6）允许设计师更精确地控制路径的缩放方式。例如，它们允许定义一个真正的圆角矩形，即使矩形进行各向异性缩放，角落仍然保持圆形。

        This element defines the path that makes up the shape. This is done through a string that contains a rich set of pen movement commands. This element also describes the limo-stretch point, inscribed textbox rectangle locations and connection site locations. The limo-stretch definition and the formulas element (§6.1.2.6) allow greater designer control of how the path scales. They allow, for example, definition of a true rounded corner rectangle where the corners remain circular even though the rectangle is scaled anisotropically.

        Parent Elements

            arc (§6.1.2.1); background (§2.2.1); curve (§6.1.2.3); group (§6.1.2.7); image (§6.1.2.10); line (§6.1.2.12); object (§2.3.3.19); oval (§6.1.2.13); pict (§2.3.3.21); pict (§2.9.23); polyline (§6.1.2.15); rect (§6.1.2.16); roundrect (§6.1.2.17); shape (§6.1.2.19); shapetype (§6.1.2.20)
        """
        return getattr(self, qn('v:path'), None)

    @property
    def formulas(self) -> Optional[CT_Formulas]:
        """6.1.2.6 formulas (Set of Formulas)

        This element defines a set of formulas whose calculated values are referenced by other attributes. Each formula is contained in a child f element (§6.1.2.4).

        Parent Elements

            arc (§6.1.2.1); background (§2.2.1); curve (§6.1.2.3); group (§6.1.2.7); image (§6.1.2.10); line (§6.1.2.12);object (§2.3.3.19); oval (§6.1.2.13); pict (§2.3.3.21); pict (§2.9.23); polyline (§6.1.2.15); rect (§6.1.2.16);roundrect (§6.1.2.17); shape (§6.1.2.19); shapetype (§6.1.2.20)
        """
        return getattr(self, qn('v:formulas'), None)

    @property
    def handles(self) -> Optional[CT_Handles]:
        """6.1.2.9 handles (Set of Handles)

        This element defines a set of user interface elements which can vary a shape's adj values. All dependent formulas and attributes are recalculated. Each handle is defined by a child h element.

        Parent Elements

            arc (§6.1.2.1); background (§2.2.1); curve (§6.1.2.3); group (§6.1.2.7); image (§6.1.2.10); line (§6.1.2.12); object (§2.3.3.19); oval (§6.1.2.13); pict (§2.3.3.21); pict (§2.9.23); polyline (§6.1.2.15); rect (§6.1.2.16); roundrect (§6.1.2.17); shape (§6.1.2.19); shapetype (§6.1.2.20)


        """
        return getattr(self, qn('v:handles'), None)

    @property
    def fill(self) -> Optional[Any]:
        """6.1.2.5 fill (Shape Fill Properties)

        This element specifies how the path should be filled if something beyond a solid color fill is desired. The attributes of the fill element can be used to describe a powerful set of image- or gradient-based fill patterns. Extensions to the VML fill definition are encoded as sub-elements of fill.

        Parent Elements

            arc (§6.1.2.1); background (§2.2.1); background (§6.1.2.2); curve (§6.1.2.3); group (§6.1.2.7); image (§6.1.2.10); line (§6.1.2.12); object (§2.3.3.19); oval (§6.1.2.13); pict (§2.3.3.21); pict (§2.9.23); polyline (§6.1.2.15); rect (§6.1.2.16); roundrect (§6.1.2.17); shape (§6.1.2.19); shapedefaults (§6.2.2.27); shapetype (§6.1.2.20)
        """
        return getattr(self, qn('v:fill'), None)

    @property
    def stroke(self) -> Optional[CT_Fill]:
        """6.1.2.21 stroke (Line Stroke Settings)

        This element describes how to draw the path if something beyond solid line with a solid color is desired. The attributes of the stroke element can be used to describe a powerful set of stroke properties. Extensions to the VML stroke definition are encoded as sub-elements of stroke.

        [Example:

        <v:polyline points="0pt,0pt,50pt,0pt,50pt,35pt,15pt,35pt,
            15pt,15pt,75pt,15pt">
            <v:stroke startarrow="classic" endarrow="classic"
                startarrowwidth="wide" endarrowwidth="wide" dashstyle="dashdot"
                weight="2pt" color="teal" linestyle="thinThin"/>
        </v:polyline>

        end example]

        Parent Elements

            arc (§6.1.2.1); background (§2.2.1); curve (§6.1.2.3); group (§6.1.2.7); image (§6.1.2.10); line (§6.1.2.12); object (§2.3.3.19); oval (§6.1.2.13); pict (§2.3.3.21); pict (§2.9.23); polyline (§6.1.2.15); rect (§6.1.2.16); roundrect (§6.1.2.17); shape (§6.1.2.19); shapedefaults (§6.2.2.27); shapetype (§6.1.2.20)
        """
        return getattr(self, qn('v:stroke'), None)

    @property
    def shadow(self) -> Optional[CT_Shadow]:
        """6.1.2.18 shadow (Shadow Effect)

        This element adds shadow effects to a shape. The on attribute must be true for the shadow to be displayed.

        [Example:

        <v:shadow on="true" type="perspective"
            matrix="1.25,-2,,1.5,,.000001"
            offset="38pt,-6pt">
        </v:shadow>

        end example]

        Parent Elements

            arc (§6.1.2.1); background (§2.2.1); curve (§6.1.2.3); group (§6.1.2.7); image (§6.1.2.10); line (§6.1.2.12); object (§2.3.3.19); oval (§6.1.2.13); pict (§2.3.3.21); pict (§2.9.23); polyline (§6.1.2.15); rect (§6.1.2.16); roundrect (§6.1.2.17); shape (§6.1.2.19); shapedefaults (§6.2.2.27); shapetype (§6.1.2.20)
        """
        return getattr(self, qn('v:shadow'), None)

    @property
    def textbox(self) -> Optional[CT_Textbox]:
        """6.1.2.22 textbox (Text Box)

        This element is used to define text that appears inside the shape. This text may contain rich formatting and is rendered to fit inside the textboxrect defined by the path element (§6.1.2.14).

        [Example:

        <v:shape style="width=200;height=200" coordsize="400,400"
            fillcolor="yellow" strokecolor="maroon"
            path="m 119,0 l 148,86 238,86 166,140 192,226 119,175 46,226
            72,140 0,86 90,86 x e">
            <v:textbox inset="32pt,35pt,,">VML</v:textbox>
        </v:shape>

        end example]

        Parent Elements

            arc (§6.1.2.1); background (§2.2.1); curve (§6.1.2.3); group (§6.1.2.7); image (§6.1.2.10); line (§6.1.2.12); object (§2.3.3.19); oval (§6.1.2.13); pict (§2.3.3.21); pict (§2.9.23); polyline (§6.1.2.15); rect (§6.1.2.16); roundrect (§6.1.2.17); shape (§6.1.2.19); shapedefaults (§6.2.2.27); shapetype (§6.1.2.20)
        """
        return getattr(self, qn('v:textbox'), None)

    @property
    def textpath(self) -> Optional[CT_TextPath]:
        """6.1.2.23 textpath (Text Layout Path)

        This element is used to define a vector path based on the text data, font and font styles supplied. The path which results is then mapped into the region defined by the v attribute of the shape's path (§6.1.2.14).

        [Example:

        <v:curve from="50,100" to="400,100"
            control1="200,200" control2="300,200">
            <v:stroke color="blue"/>
            <v:fill color="yellow" color2="green" type="gradient"/>
            <v:path textpathok="true"/>
            <v:textpath on="true" style="font:normal normal normal 36pt Arial"
                fitpath="true" string="Hello, VML!"/>
        </v:curve>

        end example]

        Parent Elements

            arc (§6.1.2.1); background (§2.2.1); curve (§6.1.2.3); group (§6.1.2.7); image (§6.1.2.10); line (§6.1.2.12); object (§2.3.3.19); oval (§6.1.2.13); pict (§2.3.3.21); pict (§2.9.23); polyline (§6.1.2.15); rect (§6.1.2.16); roundrect (§6.1.2.17); shape (§6.1.2.19); shapetype (§6.1.2.20)
        """
        return getattr(self, qn('v:textpath'), None)

    @property
    def imagedata(self) -> Optional[CT_ImageData]:
        """
        6.1.2.11 imagedata (Image Data)

        此元素用于绘制从外部源加载的图像。有一个隐含的矩形，其大小与图像相同。任何描边或填充都应用于这个隐含的矩形。描边绘制在图像的顶部。填充位于图像后面，因此只有在图像的透明区域才能看到。图像透明度要么编码在文件中，要么通过使用色键属性的颜色值来定义。与图像元素（§6.1.2.10）不同，imagedata元素必须有一个父元素。

        This element is used to draw an image that has been loaded from an external source. There is an implied rectangle that is the same size as the image. Any stroke or fill is applied to this implied rectangle. The stroke is drawn on top of the image. The fill is behind the image and therefore only visible through transparent areas of the image. Image transparency is either encoded in the file or defined via a color value using the chromakey attribute. Unlike the image element (§6.1.2.10), the imagedata element must have a parent element.

        [Example:

            <v:shape style="position:relative;top:1;left:1;width:50;height:50"
                path="m 0,0 l 1000,0 1000,1000 0,1000 x e" fillcolor="blue">
                <v:imagedata src="myimage.gif"/>
            </v:shape>

        Parent Elements:

            arc (§6.1.2.1); background (§2.2.1); curve (§6.1.2.3); group (§6.1.2.7); image (§6.1.2.10); line (§6.1.2.12); object (§2.3.3.19); oval (§6.1.2.13); pict (§2.3.3.21); pict (§2.9.23); polyline (§6.1.2.15); rect (§6.1.2.16); roundrect (§6.1.2.17); shape (§6.1.2.19); shapetype (§6.1.2.20)
        """
        return getattr(self, qn('v:imagedata'), None)

    @property
    def o_skew(self):

        ele: Optional[CT_Skew] = getattr(self, qn('o:skew'), None)
        return ele

    @property
    def o_extrusion(self):

        ele: Optional[CT_Extrusion] = getattr(self, qn('o:extrusion'), None)
        return ele

    @property
    def o_callout(self):

        ele: Optional[CT_Callout] = getattr(self, qn('o:callout'), None)
        return ele

    @property
    def o_lock(self):

        ele: Optional[CT_Lock] = getattr(self, qn('o:lock'), None)
        return ele

    @property
    def o_clippath(self):

        ele: Optional[CT_ClipPath] = getattr(self, qn('o:clippath'), None)
        return ele

    @property
    def o_signatureline(self):

        ele: Optional[CT_SignatureLine] = getattr(self, qn('o:signatureline'), None)
        return ele

    @property
    def wvml_wrap(self) -> Optional[Any]:
        return getattr(self, qn('wvml:wrap'), None)

    @property
    def wvml_anchorlock(self) -> Optional[Any]:
        """
        6.3.2.1 anchorlock (Anchor Location Is Locked)

        此元素指定在应用程序编辑此文档内容时，此对象的锚点位置在运行时不应被修改。[指导：应用程序可能具有基于用户交互自动重新定位VML对象锚点的行为 - 例如，根据需要将其从一页移动到另一页。此元素应告诉应用程序不要执行任何此类行为。结束指导]

        如果省略此元素，则父VML对象的锚点将不会被锁定。

        This element specifies that the anchor location for this object shall not be modified at runtime when an application edits the contents of this document. [Guidance: An application might have automatic behaviors which reposition the anchor for a VML object based on user interaction - for example, moving it from one page to another as needed. This element shall tell applications not to perform any such behaviors. end guidance]

        If this element is omitted, then the anchor shall not be locked for the parent VML object.

        [Example: Consider a floating VML object which shall have its anchor locked at the current location. This setting would be specified as follows:

        ```xml
        <wd:anchorLock/>
        ```

        The anchorLock element's presence specifies that the VML object's current anchor location shall not be changed by applications editing this content. end example].

        Parent Elements:

            arc (§6.1.2.1); curve (§6.1.2.3); group (§6.1.2.7); image (§6.1.2.10); line (§6.1.2.12); oval (§6.1.2.13); polyline (§6.1.2.15); rect (§6.1.2.16); roundrect (§6.1.2.17); shape (§6.1.2.19); shapetype (§6.1.2.20)

            The following XML Schema fragment defines the contents of this element:

            <complexType name="CT_AnchorLock"/>

        """
        return getattr(self, qn('wvml:anchorlock'), None)

    @property
    def wvml_bordertop(self) -> Optional[Any]:
        return getattr(self, qn('wvml:bordertop'), None)

    @property
    def wvml_borderbottom(self) -> Optional[Any]:
        return getattr(self, qn('wvml:borderbottom'), None)

    @property
    def wvml_borderleft(self) -> Optional[Any]:
        return getattr(self, qn('wvml:borderleft'), None)

    @property
    def wvml_borderright(self) -> Optional[Any]:
        return getattr(self, qn('wvml:borderright'), None)

    @property
    def x_ClientData(self) -> Optional[Any]:
        return getattr(self, qn('x:ClientData'), None)

    @property
    def p_textdata(self) -> Optional[Any]:
        return getattr(self, qn('p:textdata'), None)


class CT_Shape(
    EG_ShapeElements,
    AG_AllCoreAttributes,
    AG_AllShapeAttributes,
    AG_Type,
    AG_Adj,
    AG_Path,
):
    """http://www.datypic.com/sc/ooxml/e-v_shape.html

    6.1.2.19 shape (Shape Definition)

    此元素用于描述形状，是VML中的核心对象。此元素可以独立出现，也可以在组元素（§6.1.2.7）内出现。如果使用类型属性引用了shapetype元素（§6.1.2.20），则在形状中指定的任何属性都将覆盖在shapetype中找到的属性。

    This element is used to describe a shape, the core object in VML. This element may appear by itself or within a group element (§6.1.2.7). If a shapetype element (§6.1.2.20) is referenced using the type attribute, any attributes specified in the shape will override those found in the shapetype.

    [Example:

        <v:shape style="position:absolute;top:50;left:20;width:50;height:50"
            path="m 0,0 l 0,1000 1000,1000 1000,0 x e">
            <v:shadow on="true" type="perspective"
            matrix="1.25,-2,,1.5,,.000001" offset="38pt,-6pt"/>
        </v:shape>

        <v:shape style="position:absolute;top:50;left:20;width:50;height:50"
            fillcolor="yellow" path="m 0,0 l 0,1000 1000,1000 1000,0 x e">
            <v:extrusion on="true" lightposition="0,-2000,10000"/>
        </v:shape>

    Parent Elements

        background (§2.2.1); group (§6.1.2.7); object (§2.3.3.19); pict (§2.3.3.21); pict (§2.9.23)

    Child Elements

        | Child Elements                         | Subclause |
        | -------------------------------------- | --------- |
        | anchorlock (Anchor Location Is Locked) | §6.3.2.1  |
        | borderbottom (Bottom Border)           | §6.3.2.2  |
        | borderleft (Left Border)               | §6.3.2.3  |
        | borderright (Right Border)             | §6.3.2.4  |
        | bordertop (Top Border)                 | §6.3.2.5  |
        | callout (Callout)                      | §6.2.2.2  |
        | ClientData (Attached Object Data)      | §6.4.2.12 |
        | clippath (Shape Clipping Path)         | §6.2.2.3  |
        | extrusion (3D Extrusion)               | §6.2.2.10 |
        | fill (Shape Fill Properties)           | §6.1.2.5  |
        | formulas (Set of Formulas)             | §6.1.2.6  |
        | handles (Set of Handles)               | §6.1.2.9  |
        | imagedata (Image Data)                 | §6.1.2.11 |
        | ink (Ink)                              | §6.2.2.14 |
        | iscomment (Ink Annotation Flag)        | §6.5.2.1  |
        | lock (Shape Protections)               | §6.2.2.17 |
        | path (Shape Path)                      | §6.1.2.14 |
        | shadow (Shadow Effect)                 | §6.1.2.18 |
        | signatureline (Digital Signature Line) | §6.2.2.29 |
        | skew (Skew Transform)                  | §6.2.2.30 |
        | stroke (Line Stroke Settings)          | §6.1.2.21 |
        | textbox (Text Box)                     | §6.1.2.22 |
        | textdata (VML Diagram Text)            | §6.5.2.2  |
        | textpath (Text Layout Path)            | §6.1.2.23 |
        | wrap (Text Wrapping)                   | §6.3.2.6  |

    xsd:

        <xsd:complexType name="CT_Shape">
            <xsd:choice maxOccurs="unbounded">
                <xsd:group ref="EG_ShapeElements" />
                <xsd:element ref="o:ink" />
                <xsd:element ref="p:iscomment" />
            </xsd:choice>
            <xsd:attributeGroup ref="AG_AllCoreAttributes" />
            <xsd:attributeGroup ref="AG_AllShapeAttributes" />
            <xsd:attributeGroup ref="AG_Type" />
            <xsd:attributeGroup ref="AG_Adj" />
            <xsd:attributeGroup ref="AG_Path" />
            <xsd:attribute ref="o:gfxdata">
                <xsd:annotation>
                    <xsd:documentation>Encoded Package</xsd:documentation>
                </xsd:annotation>
            </xsd:attribute>
            <xsd:attribute name="equationxml" type="xsd:string" use="optional">
                <xsd:annotation>
                    <xsd:documentation>Storage for Alternate Math Content</xsd:documentation>
                </xsd:annotation>
            </xsd:attribute>
        </xsd:complexType>
    """

    @property
    def ink(self):

        ele: Optional[CT_Ink] = getattr(self, qn('o:ink'), None)

        return ele

    @property
    def iscomment(self) -> Optional[OxmlBaseElement]:
        return getattr(self, qn('p:iscomment'), None)

    @property
    def o_gfxdata(self) -> Optional[str]:
        """Encoded Package

        <xsd:attribute name="gfxdata" type="xsd:base64Binary" />
        """

        val = self.attrib.get(qn('o:gfxdata'))

        if val is not None:
            return str(val)
        return None

    @property
    def equationxml(self) -> Optional[str]:
        """Storage for Alternate Math Content"""

        val = self.attrib.get(qn('v:equationxml'))

        if val is not None:
            return str(val)
        return None


class CT_Shapetype(EG_ShapeElements, AG_AllCoreAttributes, AG_AllShapeAttributes, AG_Adj, AG_Path):
    """Shape Template

    <xsd:complexType name="CT_Shapetype">
        <xsd:sequence>
            <xsd:group ref="EG_ShapeElements" minOccurs="0" maxOccurs="unbounded" />
            <xsd:element ref="o:complex" minOccurs="0" />
        </xsd:sequence>
        <xsd:attributeGroup ref="AG_AllCoreAttributes" />
        <xsd:attributeGroup ref="AG_AllShapeAttributes" />
        <xsd:attributeGroup ref="AG_Adj" />
        <xsd:attributeGroup ref="AG_Path" />
        <xsd:attribute ref="o:master">
            <xsd:annotation>
                <xsd:documentation>Master Element Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:complexType>
    """

    @property
    def o_complex(self):

        ele: Optional[CT_Complex] = getattr(self, qn('o:complex'))
        return ele

    @property
    def equationxml(self) -> Optional[str]:
        """Master Element Toggle"""

        val = self.attrib.get(qn('o:master'))

        if val is not None:
            return str(val)
        return None


class CT_Group(EG_ShapeElements, AG_AllCoreAttributes, AG_Fill):
    """Shape Group

    <xsd:complexType name="CT_Group">
        <xsd:choice maxOccurs="unbounded">
            <xsd:group ref="EG_ShapeElements" />
            <xsd:element ref="group" />
            <xsd:element ref="shape" />
            <xsd:element ref="shapetype" />
            <xsd:element ref="arc" />
            <xsd:element ref="curve" />
            <xsd:element ref="image" />
            <xsd:element ref="line" />
            <xsd:element ref="oval" />
            <xsd:element ref="polyline" />
            <xsd:element ref="rect" />
            <xsd:element ref="roundrect" />
            <xsd:element ref="o:diagram" />
        </xsd:choice>
        <xsd:attributeGroup ref="AG_AllCoreAttributes" />
        <xsd:attributeGroup ref="AG_Fill" />
        <xsd:attribute name="editas" type="ST_EditAs" use="optional">
            <xsd:annotation>
                <xsd:documentation>Group Diagram Type</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:tableproperties">
            <xsd:annotation>
                <xsd:documentation>Table Properties</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:tablelimits">
            <xsd:annotation>
                <xsd:documentation>Table Row Height Limits</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:complexType>
    """

    @property
    def group(self) -> Optional[CT_Group]:
        return getattr(self, qn('v:group'), None)

    @property
    def shape(self) -> Optional[CT_Shape]:
        return getattr(self, qn('v:shape'), None)

    @property
    def shapetype(self) -> Optional[CT_Shapetype]:
        return getattr(self, qn('v:shapetype'), None)

    @property
    def arc(self) -> Optional[CT_Arc]:
        return getattr(self, qn('v:arc'), None)

    @property
    def curve(self) -> Optional[CT_Curve]:
        return getattr(self, qn('v:curve'), None)

    @property
    def image(self) -> Optional[CT_Image]:
        return getattr(self, qn('v:image'), None)

    @property
    def line(self) -> Optional[CT_Line]:
        return getattr(self, qn('v:line'), None)

    @property
    def oval(self) -> Optional[CT_Oval]:
        return getattr(self, qn('v:oval'), None)

    @property
    def polyline(self) -> Optional[CT_PolyLine]:
        return getattr(self, qn('v:polyline'), None)

    @property
    def rect(self) -> Optional[CT_Rect]:
        return getattr(self, qn('v:rect'), None)

    @property
    def roundrect(self) -> Optional[CT_RoundRect]:
        return getattr(self, qn('v:roundrect'), None)

    @property
    def o_diagram(self):

        ele: Optional[CT_Diagram] = getattr(self, qn('o:diagram'), None)

        return ele

    @property
    def editas(self) -> Optional[ST_EditAs]:
        """Group Diagram Type"""

        val = self.attrib.get(qn('v:editas'))

        if val is not None:
            return ST_EditAs(val)
        return None

    @property
    def o_tableproperties(self) -> Optional[str]:
        """Table Properties"""

        val = self.attrib.get(qn('o:tableproperties'))

        if val is not None:
            return str(val)
        return None

    @property
    def o_tablelimits(self) -> Optional[str]:
        """Table Row Height Limits"""

        val = self.attrib.get(qn('o:tablelimits'))

        if val is not None:
            return str(val)
        return None


class CT_Background(AG_Id, AG_Fill):
    """Document Background

    <xsd:complexType name="CT_Background">
        <xsd:sequence>
            <xsd:element ref="fill" minOccurs="0" />
        </xsd:sequence>
        <xsd:attributeGroup ref="AG_Id" />
        <xsd:attributeGroup ref="AG_Fill" />
        <xsd:attribute ref="o:bwmode">
            <xsd:annotation>
                <xsd:documentation>Black-and-White Mode</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:bwpure">
            <xsd:annotation>
                <xsd:documentation>Pure Black-and-White Mode</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:bwnormal">
            <xsd:annotation>
                <xsd:documentation>Normal Black-and-White Mode</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:targetscreensize">
            <xsd:annotation>
                <xsd:documentation>Target Screen Size</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:complexType>
    """

    @property
    def fill(self) -> Optional[CT_Fill]:
        return getattr(self, qn('v:fill'))

    @property
    def o_bwmode(self):
        """Black-and-White Mode"""

        from ecma376_office.oxml.vml.drawing import ST_BWMode

        val = self.attrib.get(qn('o:bwmode'))

        if val is not None:
            return ST_BWMode(val)
        return None

    @property
    def o_bwpure(self):
        """Pure Black-and-White Mode"""

        from ecma376_office.oxml.vml.drawing import ST_BWMode

        val = self.attrib.get(qn('o:bwpure'))

        if val is not None:
            return ST_BWMode(val)
        return None

    @property
    def o_bwnormal(self):
        """Normal Black-and-White Mode"""

        from ecma376_office.oxml.vml.drawing import ST_BWMode

        val = self.attrib.get(qn('o:bwnormal'))

        if val is not None:
            return ST_BWMode(val)
        return None

    @property
    def o_targetscreensize(self):
        """Target Screen Size"""

        from ecma376_office.oxml.vml.drawing import ST_ScreenSize

        val = self.attrib.get(qn('o:targetscreensize'))

        if val is not None:
            return ST_ScreenSize(val)
        return None


class CT_Fill(AG_Id):
    """

    <xsd:complexType name="CT_Fill">
        <xsd:sequence>
            <xsd:element ref="o:fill" minOccurs="0" />
        </xsd:sequence>
        <xsd:attributeGroup ref="AG_Id" />
        <xsd:attribute name="type" type="ST_FillType" use="optional">
            <xsd:annotation>
                <xsd:documentation>Fill Type</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="on" type="ST_TrueFalse" use="optional">
            <xsd:annotation>
                <xsd:documentation>Fill Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="color" type="ST_ColorType" use="optional">
            <xsd:annotation>
                <xsd:documentation>Primary Color</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="opacity" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Primary Color Opacity</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="color2" type="ST_ColorType" use="optional">
            <xsd:annotation>
                <xsd:documentation>Secondary Color</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="src" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Fill Image Source</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:href">
            <xsd:annotation>
                <xsd:documentation>Hyperlink Target</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:althref">
            <xsd:annotation>
                <xsd:documentation>Alternate Image Reference Location</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="size" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Fill Image Size</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="origin" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Fill Image Origin</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="position" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Fill Image Position</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="aspect" type="ST_ImageAspect" use="optional">
            <xsd:annotation>
                <xsd:documentation>Image Aspect Ratio</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="colors" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Intermediate Colors</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="angle" type="xsd:decimal" use="optional">
            <xsd:annotation>
                <xsd:documentation>Gradient Angle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="alignshape" type="ST_TrueFalse" use="optional">
            <xsd:annotation>
                <xsd:documentation>Align Image With Shape</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="focus" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Gradient Center</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="focussize" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Radial Gradient Size</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="focusposition" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Radial Gradient Center</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="method" type="ST_FillMethod" use="optional">
            <xsd:annotation>
                <xsd:documentation>Gradient Fill Method</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:detectmouseclick">
            <xsd:annotation>
                <xsd:documentation>Detect Mouse Click</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:title">
            <xsd:annotation>
                <xsd:documentation>Title</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:opacity2">
            <xsd:annotation>
                <xsd:documentation>Secondary Color Opacity</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="recolor" type="ST_TrueFalse" use="optional">
            <xsd:annotation>
                <xsd:documentation>Recolor Fill as Picture</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="rotate" type="ST_TrueFalse" use="optional">
            <xsd:annotation>
                <xsd:documentation>Rotate Fill with Shape</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="r:id" use="optional">
            <xsd:annotation>
                <xsd:documentation>Relationship to Part</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:relid" use="optional">
            <xsd:annotation>
                <xsd:documentation>Relationship to Part</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:complexType>
    """

    @property
    def o_fill(self):
        ele: Optional[CT_Fill] = getattr(self, qn('o:fill'), None)

        return ele

    @property
    def type(self) -> Optional[ST_FillType]:
        """Fill Type"""

        val = self.attrib.get(qn('v:type'))
        if val is not None:
            return ST_FillType(val)
        return None

    @property
    def on(self) -> Optional[ST_TrueFalse]:
        """Fill Toggle"""

        val = self.attrib.get(qn('v:on'))
        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def color(self) -> Optional[ST_ColorType]:
        """Primary Color"""

        val = self.attrib.get(qn('v:color'))
        if val is not None:
            return ST_ColorType(val)
        return None

    @property
    def opacity(self) -> Optional[str]:
        """Primary Color Opacity"""

        val = self.attrib.get(qn('v:opacity'))
        if val is not None:
            return str(val)
        return None

    @property
    def color2(self) -> Optional[ST_ColorType]:
        """Secondary Color"""

        val = self.attrib.get(qn('v:color2'))
        if val is not None:
            return ST_ColorType(val)
        return None

    @property
    def src(self) -> Optional[str]:
        """Fill Image Source"""

        val = self.attrib.get(qn('v:src'))
        if val is not None:
            return str(val)
        return None

    @property
    def o_href(self) -> Optional[str]:
        """Hyperlink Target"""

        val = self.attrib.get(qn('o:href'))

        if val is not None:
            return str(val)
        return None

    @property
    def o_althref(self) -> Optional[str]:
        """Alternate Image Reference Location"""

        val = self.attrib.get(qn('o:althref'))

        if val is not None:
            return str(val)
        return None

    @property
    def size(self) -> Optional[str]:
        """Fill Image Size"""

        val = self.attrib.get(qn('v:size'))
        if val is not None:
            return str(val)
        return None

    @property
    def origin(self) -> Optional[str]:
        """Fill Image Origin"""

        val = self.attrib.get(qn('v:origin'))
        if val is not None:
            return str(val)
        return None

    @property
    def position(self) -> Optional[str]:
        """Fill Image Position"""

        val = self.attrib.get(qn('v:position'))
        if val is not None:
            return str(val)
        return None

    @property
    def aspect(self) -> Optional[ST_ImageAspect]:
        """Image Aspect Ratio"""

        val = self.attrib.get(qn('v:aspect'))
        if val is not None:
            return ST_ImageAspect(val)
        return None

    @property
    def colors(self) -> Optional[str]:
        """Intermediate Colors"""

        val = self.attrib.get(qn('v:colors'))
        if val is not None:
            return str(val)
        return None

    @property
    def angle(self) -> Optional[str]:
        """Gradient Angle"""

        val = self.attrib.get(qn('v:angle'))
        if val is not None:
            return str(val)
        return None

    @property
    def alignshape(self) -> Optional[ST_TrueFalse]:
        """Align Image With Shape"""

        val = self.attrib.get(qn('v:alignshape'))
        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def focus(self) -> Optional[str]:
        """Gradient Center"""

        val = self.attrib.get(qn('v:focus'))
        if val is not None:
            return str(val)
        return None

    @property
    def focussize(self) -> Optional[str]:
        """Radial Gradient Size"""

        val = self.attrib.get(qn('v:focussize'))
        if val is not None:
            return str(val)
        return None

    @property
    def focusposition(self) -> Optional[str]:
        """Radial Gradient Center"""

        val = self.attrib.get(qn('v:focusposition'))
        if val is not None:
            return str(val)
        return None

    @property
    def method(self) -> Optional[ST_FillMethod]:
        """Gradient Fill Method"""

        val = self.attrib.get(qn('v:method'))
        if val is not None:
            return ST_FillMethod(val)
        return None

    @property
    def o_detectmouseclick(self):
        """Detect Mouse Click"""

        from ecma376_office.oxml.vml.drawing import ST_TrueFalse

        val = self.attrib.get(qn('o:detectmouseclick'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def o_title(self) -> Optional[str]:
        """Title"""

        val = self.attrib.get(qn('o:title'))

        if val is not None:
            return str(val)
        return None

    @property
    def o_opacity2(self) -> Optional[str]:
        """Secondary Color Opacity"""

        val = self.attrib.get(qn('o:opacity2'))

        if val is not None:
            return str(val)
        return None

    @property
    def recolor(self) -> Optional[ST_TrueFalse]:
        """Recolor Fill as Picture"""

        val = self.attrib.get(qn('v:recolor'))
        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def rotate(self) -> Optional[ST_TrueFalse]:
        """Rotate Fill with Shape"""

        val = self.attrib.get(qn('v:rotate'))
        if val is not None:
            return ST_TrueFalse(val)
        return None

    def r_id(self) -> Optional[str]:
        """Relationship to Part"""

        val = self.attrib.get(qn('r:id'))

        if val is not None:
            return str(val)
        return None

    def o_relid(self):
        """Relationship to Part"""

        from ecma376_office.oxml.vml.drawing import ST_RelationshipId

        val = self.attrib.get(qn('o:relid'))
        if val is not None:
            return ST_RelationshipId(val)
        return None


class CT_Formulas(OxmlBaseElement):
    """

    <xsd:complexType name="CT_Formulas">
        <xsd:sequence>
            <xsd:element name="f" type="CT_F" minOccurs="0" maxOccurs="unbounded">
                <xsd:annotation>
                    <xsd:documentation>Single Formula</xsd:documentation>
                </xsd:annotation>
            </xsd:element>
        </xsd:sequence>
    </xsd:complexType>
    """

    @property
    def f_lst(self) -> list[CT_F]:
        return self.findall(qn('v:f'))  # type: ignore


class CT_F(OxmlBaseElement):
    """

    <xsd:complexType name="CT_F">
        <xsd:attribute name="eqn" type="xsd:string">
            <xsd:annotation>
                <xsd:documentation>Equation</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:complexType>
    """

    @property
    def eqn(self) -> Optional[str]:
        val = self.attrib.get(qn('v:eqn'))

        if val is not None:
            return str(val)
        return None


class CT_Handles(OxmlBaseElement):
    """

    <xsd:complexType name="CT_Handles">
        <xsd:sequence>
            <xsd:element name="h" type="CT_H" minOccurs="0" maxOccurs="unbounded">
                <xsd:annotation>
                    <xsd:documentation>Shape Handle</xsd:documentation>
                </xsd:annotation>
            </xsd:element>
        </xsd:sequence>
    </xsd:complexType>
    """

    @property
    def h_lst(self) -> list[CT_H]:
        """Shape Handle"""

        return self.findall(qn('v:h'))  # type: ignore


class CT_H(OxmlBaseElement):
    """

    <xsd:complexType name="CT_H">
        <xsd:attribute name="position" type="xsd:string">
            <xsd:annotation>
                <xsd:documentation>Handle Position</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="polar" type="xsd:string">
            <xsd:annotation>
                <xsd:documentation>Handle Polar Center</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="map" type="xsd:string">
            <xsd:annotation>
                <xsd:documentation>Handle Coordinate Mapping</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="invx" type="ST_TrueFalse">
            <xsd:annotation>
                <xsd:documentation>Invert Handle's X Position</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="invy" type="ST_TrueFalse">
            <xsd:annotation>
                <xsd:documentation>Invert Handle's Y Position</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="switch" type="ST_TrueFalseBlank">
            <xsd:annotation>
                <xsd:documentation>Handle Inversion Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="xrange" type="xsd:string">
            <xsd:annotation>
                <xsd:documentation>Handle X Position Range</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="yrange" type="xsd:string">
            <xsd:annotation>
                <xsd:documentation>Handle Y Position Range</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="radiusrange" type="xsd:string">
            <xsd:annotation>
                <xsd:documentation>Handle Polar Radius Range</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:complexType>
    """

    @property
    def position(self) -> str:
        """Handle Position"""

        return str(self.attrib[qn('v:position')])

    @property
    def polar(self) -> str:
        """Handle Polar Center"""

        return str(self.attrib[qn('v:polar')])

    @property
    def map(self) -> str:
        """Handle Coordinate Mapping"""

        return str(self.attrib[qn('v:map')])

    @property
    def invx(self) -> ST_TrueFalse:
        """Invert Handle's X Position"""

        return ST_TrueFalse(self.attrib[qn('v:invx')])

    @property
    def invy(self) -> ST_TrueFalse:
        """Invert Handle's Y Position"""

        return ST_TrueFalse(self.attrib[qn('v:invy')])

    @property
    def switch(self) -> ST_TrueFalseBlank:
        """Handle Inversion Toggle"""

        return ST_TrueFalseBlank(self.attrib[qn('v:switch')])

    @property
    def xrange(self) -> str:
        """Handle X Position Range"""

        return str(self.attrib[qn('v:xrange')])

    @property
    def yrange(self) -> str:
        """Handle Y Position Range"""

        return str(self.attrib[qn('v:yrange')])

    @property
    def radiusrange(self) -> str:
        """Handle Polar Radius Range"""

        return str(self.attrib[qn('v:radiusrange')])


class CT_ImageData(AG_Id, AG_ImageAttributes, AG_Chromakey):
    """
    6.1.2.11 imagedata (Image Data)

    此元素用于绘制从外部源加载的图像。有一个隐含的矩形，其大小与图像相同。任何描边或填充都应用于这个隐含的矩形。描边绘制在图像的顶部。填充位于图像后面，因此只有在图像的透明区域才能看到。图像透明度要么编码在文件中，要么通过使用色键属性的颜色值来定义。与图像元素（§6.1.2.10）不同，imagedata元素必须有一个父元素。

    This element is used to draw an image that has been loaded from an external source. There is an implied rectangle that is the same size as the image. Any stroke or fill is applied to this implied rectangle. The stroke is drawn on top of the image. The fill is behind the image and therefore only visible through transparent areas of the image. Image transparency is either encoded in the file or defined via a color value using the chromakey attribute. Unlike the image element (§6.1.2.10), the imagedata element must have a parent element.

    [Example:

        <v:shape style="position:relative;top:1;left:1;width:50;height:50"
            path="m 0,0 l 1000,0 1000,1000 0,1000 x e" fillcolor="blue">
            <v:imagedata src="myimage.gif"/>
        </v:shape>

    Parent Elements:

        arc (§6.1.2.1); background (§2.2.1); curve (§6.1.2.3); group (§6.1.2.7); image (§6.1.2.10); line (§6.1.2.12); object (§2.3.3.19); oval (§6.1.2.13); pict (§2.3.3.21); pict (§2.9.23); polyline (§6.1.2.15); rect (§6.1.2.16); roundrect (§6.1.2.17); shape (§6.1.2.19); shapetype (§6.1.2.20)

    <xsd:complexType name="CT_ImageData">
        <xsd:attributeGroup ref="AG_Id" />
        <xsd:attributeGroup ref="AG_ImageAttributes" />
        <xsd:attributeGroup ref="AG_Chromakey" />
        <xsd:attribute name="embosscolor" type="ST_ColorType" use="optional">
            <xsd:annotation>
                <xsd:documentation>Embossed Color</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="recolortarget" type="ST_ColorType">
            <xsd:annotation>
                <xsd:documentation>Black Recoloring Color</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:href">
            <xsd:annotation>
                <xsd:documentation>Original Image Reference</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:althref">
            <xsd:annotation>
                <xsd:documentation>Alternate Image Reference</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:title">
            <xsd:annotation>
                <xsd:documentation>Image Data Title</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:oleid">
            <xsd:annotation>
                <xsd:documentation>Image Embedded Object ID</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:detectmouseclick">
            <xsd:annotation>
                <xsd:documentation>Detect Mouse Click</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:movie">
            <xsd:annotation>
                <xsd:documentation>Movie Reference</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:relid">
            <xsd:annotation>
                <xsd:documentation>Relationship to Part</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="r:id">
            <xsd:annotation>
                <xsd:documentation>Explicit Relationship to Image Data</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="r:pict">
            <xsd:annotation>
                <xsd:documentation>Explicit Relationship to Alternate Image Data</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="r:href">
            <xsd:annotation>
                <xsd:documentation>Explicit Relationship to Hyperlink Target</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:complexType>
    """

    @property
    def embosscolor(self) -> Optional[ST_ColorType]:
        """Embossed Color

        Specifies the color to use to create an embossed effect in the image. Default is no value.
        This can be set to a percentage of the shadow color to create an embossed picture effect.

        The possible values for this attribute are defined by the ST_ColorType simple type (§6.1.3.1).
        """
        val = self.attrib.get(qn('v:embosscolor'))
        if val is not None:
            return ST_ColorType(val)
        return None

    @property
    def recolortarget(self) -> Optional[ST_ColorType]:
        """Black Recoloring Color

        Specifies the color to which black should be recolored.

        [Example:

            <v:imagedata r:id="rId4" recolortarget="red">
            </v:imagedata>

        end example]

        The possible values for this attribute are defined by the ST_ColorType simple type (§6.1.3.1).
        """

        val = self.attrib.get(qn('v:recolortarget'))
        if val is not None:
            return ST_ColorType(val)
        return None

    @property
    def o_href(self) -> Optional[str]:
        """Original Image Reference

        Specifies the URL to the original image file. Used only if the picture has been linked and embedded. Default is no value.

        [Example:

        <v:fill ... o:href="myimage.gif" ... >
        </v:fill>

        end example]

        The possible values for this attribute are defined by the XML Schema string datatype.
        """
        val = self.attrib.get(qn('o:href'))
        if val is not None:
            return str(val)
        return None

    @property
    def o_althref(self) -> Optional[str]:
        """Alternate Image Reference

        Defines an alternate reference for an image in Macintosh PICT format.

        [Example:

        <v:imagedata ... althref="myimage.pcz" ... >
        </v:imagedata>

        end example

        The possible values for this attribute are defined by the XML Schema string datatype.
        """
        val = self.attrib.get(qn('o:althref'))
        if val is not None:
            return str(val)
        return None

    @property
    def o_title(self) -> Optional[str]:
        """Image Data Title

        Specifies the title of an embedded image. This is typically set to the comment property of the image, which is often blank.

        [Example:

            <v:fill ... o:title="alt text" ... >
            </v:fill>

        end example]

        The possible values for this attribute are defined by the XML Schema string datatype.
        """
        val = self.attrib.get(qn('o:title'))
        if val is not None:
            return str(val)
        return None

    @property
    def o_oleid(self) -> Optional[float]:
        """Image Embedded Object ID

        Specifies the embedded object ID of an image.

        The possible values for this attribute are defined by the XML Schema float datatype.
        """
        val = self.attrib.get(qn('o:oleid'))
        if val is not None:
            return float(val)
        return None

    @property
    def o_detectmouseclick(self):
        """Detect Mouse Click

        Specifies whether a mouse click is detected on the fill of a shape.

        The possible values for this attribute are defined by the ST_TrueFalse simple type (§6.2.3.23).
        """

        from ecma376_office.oxml.vml.drawing import ST_TrueFalse

        val = self.attrib.get(qn('o:detectmouseclick'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def o_movie(self) -> Optional[float]:
        """Movie Reference

        Specifies a pointer to a movie image. This is a data block that contains a pointer to a pointer to movie data.

        [Example:

            <v:imagedata ... o:movie="1434" ...>
            </v:imagedata>

        end example]

        The possible values for this attribute are defined by the XML Schema float datatype.
        """
        val = self.attrib.get(qn('o:movie'))
        if val is not None:
            return float(val)
        return None

    @property
    def o_relid(self):
        """Relationship to Part

        Specifies the relationship ID of the relationship to the image. The specified relationship shall be of type http://schemas.openxmlformats.org/officeDocument/2006/relationships/image or the document shall be considered non-conformant.

        [Example: The markup specifies the associated relationship part with relationship ID rId10 contains the corresponding relationship information:

        <v:imagedata ... o:relid="rId10" ...>
        </v:imagedata>

        end example]

        The possible values for this attribute are defined by the ST_RelationshipId simple type (§6.2.3.20).
        """

        from ecma376_office.oxml.vml.drawing import ST_RelationshipId

        val = self.attrib.get(qn('o:relid'))
        if val is not None:
            return ST_RelationshipId(val)
        return None

    @property
    def r_id(self) -> Optional[str]:
        """Explicit Relationship to Image Data

        Specifies the relationship ID of the relationship to the image used for this VML object. The specified relationship shall be of type http://schemas.openxmlformats.org/officeDocument/2006/relationships/image or the document shall be considered non-conformant.

        [Example: The markup specifies the associated relationship part with relationship ID rId10 contains the corresponding relationship information for the image data:

        < ... r:id="rId10" />

        end example]

        The possible values for this attribute are defined by the ST_RelationshipId simple type (§7.8.2.1).
        """
        val = self.attrib.get(qn('r:id'))
        if val is not None:
            return str(val)
        return None

    @property
    def r_pict(self) -> Optional[str]:
        """Explicit Relationship to Alternate Image Data

        Specifies the relationship ID of the relationship to an alternate format image used for this VML object. The specified relationship shall be of type http://schemas.openxmlformats.org/officeDocument/2006/relationships/image or the document shall be considered non-conformant.

        If this attribute is specified, the application should attempt to display the image defined by the relationship. If the application cannot display the format of that image, the r:id attribute is used.

        [Example: The markup specifies the associated relationship part with relationship ID rId7 contains the corresponding relationship information for the image data. The relationship part with relationship ID rId10 is used if the application cannot display the image referenced by rId7.:

        < ... r:id="rId10" r:pict="rId7"/>

        end example]

        The possible values for this attribute are defined by the ST_RelationshipId simple type (§7.8.2.1).
        """
        val = self.attrib.get(qn('r:pict'))
        if val is not None:
            return str(val)
        return None

    @property
    def r_href(self) -> Optional[str]:
        """Explicit Relationship to Hyperlink Target

        Specifies the relationship ID of the relationship to the hyperlink used for this VML object.

        The specified relationship shall be of type http://schemas.openxmlformats.org/officeDocument/2006/relationships/image or the document shall be considered non-conformant. [Example: The markup specifies the associated relationship part with relationship ID

        [Example: The markup specifies the associated relationship part with relationship ID rId10 contains the corresponding relationship information for the image data:

        < ... r:href="rId5" />

        end example]

        The possible values for this attribute are defined by the ST_RelationshipId simple type (§7.8.2.1).
        """
        val = self.attrib.get(qn('r:href'))
        if val is not None:
            return str(val)
        return None


class CT_Path(AG_Id):
    """Shape Path

    <xsd:complexType name="CT_Path">
        <xsd:attributeGroup ref="AG_Id" />
        <xsd:attribute name="v" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Path Definition</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="limo" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Limo Stretch Point</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="textboxrect" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Text Box Bounding Box</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="fillok" type="ST_TrueFalse" use="optional">
            <xsd:annotation>
                <xsd:documentation>Shape Fill Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="strokeok" type="ST_TrueFalse" use="optional">
            <xsd:annotation>
                <xsd:documentation>Stroke Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="shadowok" type="ST_TrueFalse" use="optional">
            <xsd:annotation>
                <xsd:documentation>Shadow Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="arrowok" type="ST_TrueFalse" use="optional">
            <xsd:annotation>
                <xsd:documentation>Arrowhead Display Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="gradientshapeok" type="ST_TrueFalse" use="optional">
            <xsd:annotation>
                <xsd:documentation>Gradient Shape Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="textpathok" type="ST_TrueFalse" use="optional">
            <xsd:annotation>
                <xsd:documentation>Text Path Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="insetpenok" type="ST_TrueFalse" use="optional">
            <xsd:annotation>
                <xsd:documentation>Inset Stroke From Path Flag</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:connecttype">
            <xsd:annotation>
                <xsd:documentation>Connection Point Type</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:connectlocs">
            <xsd:annotation>
                <xsd:documentation>Connection Points</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:connectangles">
            <xsd:annotation>
                <xsd:documentation>Connection Point Connect Angles</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:extrusionok">
            <xsd:annotation>
                <xsd:documentation>Extrusion Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:complexType>
    """

    @property
    def v(self) -> Optional[str]:
        """Path Definition"""

        val = self.attrib.get(qn('v:v'))

        if val is not None:
            return str(val)
        return None

    @property
    def limo(self) -> Optional[str]:
        """Limo Stretch Point"""

        val = self.attrib.get(qn('v:limo'))

        if val is not None:
            return str(val)
        return None

    @property
    def textboxrect(self) -> Optional[str]:
        """Text Box Bounding Box"""

        val = self.attrib.get(qn('v:textboxrect'))

        if val is not None:
            return str(val)
        return None

    @property
    def fillok(self) -> Optional[ST_TrueFalse]:
        """Shape Fill Toggle"""

        val = self.attrib.get(qn('v:fillok'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def strokeok(self) -> Optional[ST_TrueFalse]:
        """Stroke Toggle"""

        val = self.attrib.get(qn('v:strokeok'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def shadowok(self) -> Optional[ST_TrueFalse]:
        """Shadow Toggle"""

        val = self.attrib.get(qn('v:shadowok'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def arrowok(self) -> Optional[ST_TrueFalse]:
        """Arrowhead Display Toggle"""

        val = self.attrib.get(qn('v:arrowok'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def gradientshapeok(self) -> Optional[ST_TrueFalse]:
        """Gradient Shape Toggle"""

        val = self.attrib.get(qn('v:gradientshapeok'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def textpathok(self) -> Optional[ST_TrueFalse]:
        """Text Path Toggle"""

        val = self.attrib.get(qn('v:textpathok'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def insetpenok(self) -> Optional[ST_TrueFalse]:
        """Inset Stroke From Path Flag"""

        val = self.attrib.get(qn('v:insetpenok'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def o_connecttype(self):
        """Connection Point Type"""

        from ecma376_office.oxml.vml.drawing import ST_ConnectType

        val = self.attrib.get(qn('o:connecttype'))

        if val is not None:
            return ST_ConnectType(val)
        return None

    @property
    def o_connectlocs(self) -> Optional[str]:
        """Connection Points"""

        val = self.attrib.get(qn('o:connectlocs'))

        if val is not None:
            return str(val)
        return None

    @property
    def o_connectangles(self) -> Optional[str]:
        """Connection Point Connect Angles"""

        val = self.attrib.get(qn('o:connectangles'))

        if val is not None:
            return str(val)
        return None

    @property
    def o_extrusionok(self):
        """Extrusion Toggle"""

        from ecma376_office.oxml.vml.drawing import ST_TrueFalse

        val = self.attrib.get(qn('o:extrusionok'))

        if val is not None:
            return ST_TrueFalse(val)
        return None


class CT_Textbox(AG_Id, AG_Style):
    """Text Box

    <xsd:complexType name="CT_Textbox">
        <xsd:choice>
            <xsd:element ref="w:txbxContent" minOccurs="0" />
            <xsd:any namespace="##local" processContents="skip" />
        </xsd:choice>
        <xsd:attributeGroup ref="AG_Id" />
        <xsd:attributeGroup ref="AG_Style" />
        <xsd:attribute name="inset" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Text Box Inset</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:singleclick">
            <xsd:annotation>
                <xsd:documentation>Text Box Single-Click Selection Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute ref="o:insetmode">
            <xsd:annotation>
                <xsd:documentation>Text Inset Mode</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:complexType>
    """

    @property
    def txbx_content(self):

        ele: Optional[CT_TxbxContent] = getattr(self, qn('w:txbxContent'), None)

        return ele

    @property
    def inset(self) -> Optional[str]:
        """Text Box Inset"""

        val = self.attrib.get(qn('v:inset'))

        if val is not None:
            return str(val)
        return None

    @property
    def o_singleclick(self) -> Optional[str]:
        """Text Box Single-Click Selection Toggle"""

        val = self.attrib.get(qn('o:singleclick'))

        if val is not None:
            return str(val)
        return None

    @property
    def o_insetmode(self):
        """Text Inset Mode"""

        from ecma376_office.oxml.vml.drawing import ST_InsetMode

        val = self.attrib.get(qn('o:insetmode'))

        if val is not None:
            return ST_InsetMode(val)

        return ST_InsetMode('custom')


class CT_Shadow(AG_Id):
    """Shadow Effect

    <xsd:complexType name="CT_Shadow">
        <xsd:attributeGroup ref="AG_Id" />
        <xsd:attribute name="on" type="ST_TrueFalse" use="optional">
            <xsd:annotation>
                <xsd:documentation>Shadow Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="type" type="ST_ShadowType" use="optional">
            <xsd:annotation>
                <xsd:documentation>Shadow Type</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="obscured" type="ST_TrueFalse" use="optional">
            <xsd:annotation>
                <xsd:documentation>Shadow Transparency</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="color" type="ST_ColorType" use="optional">
            <xsd:annotation>
                <xsd:documentation>Shadow Primary Color</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="opacity" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Shadow Opacity</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="offset" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Shadow Primary Offset</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="color2" type="ST_ColorType" use="optional">
            <xsd:annotation>
                <xsd:documentation>Shadow Secondary Color</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="offset2" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Shadow Secondary Offset</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="origin" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Shadow Origin</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="matrix" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Shadow Perspective Matrix</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:complexType>
    """

    @property
    def on(self) -> Optional[ST_TrueFalse]:
        """Shadow Toggle"""

        val = self.attrib.get(qn('v:on'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def type(self) -> Optional[ST_ShadowType]:
        """Shadow Type"""

        val = self.attrib.get(qn('v:type'))

        if val is not None:
            return ST_ShadowType(val)
        return None

    @property
    def obscured(self) -> Optional[ST_TrueFalse]:
        """Shadow Transparency"""

        val = self.attrib.get(qn('v:obscured'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def color(self) -> Optional[ST_ColorType]:
        """Shadow Primary Color"""

        val = self.attrib.get(qn('v:color'))

        if val is not None:
            return ST_ColorType(val)
        return None

    @property
    def opacity(self) -> Optional[str]:
        """Shadow Opacity"""

        val = self.attrib.get(qn('v:opacity'))

        if val is not None:
            return str(val)
        return None

    @property
    def offset(self) -> Optional[str]:
        """Shadow Primary Offset"""

        val = self.attrib.get(qn('v:offset'))

        if val is not None:
            return str(val)
        return None

    @property
    def color2(self) -> Optional[ST_ColorType]:
        """Shadow Secondary Color"""

        val = self.attrib.get(qn('v:color2'))

        if val is not None:
            return ST_ColorType(val)
        return None

    @property
    def offset2(self) -> Optional[str]:
        """Shadow Secondary Offset"""

        val = self.attrib.get(qn('v:offset2'))

        if val is not None:
            return str(val)
        return None

    @property
    def origin(self) -> Optional[str]:
        """Shadow Origin"""

        val = self.attrib.get(qn('v:origin'))

        if val is not None:
            return str(val)
        return None

    @property
    def matrix(self) -> Optional[str]:
        """Shadow Perspective Matrix"""

        val = self.attrib.get(qn('v:matrix'))

        if val is not None:
            return str(val)
        return None


class CT_Stroke(AG_Id, AG_StrokeAttributes):
    """Shadow Effect

    <xsd:complexType name="CT_Stroke">
        <xsd:sequence>
            <xsd:element ref="o:left" minOccurs="0" />
            <xsd:element ref="o:top" minOccurs="0" />
            <xsd:element ref="o:right" minOccurs="0" />
            <xsd:element ref="o:bottom" minOccurs="0" />
            <xsd:element ref="o:column" minOccurs="0" />
        </xsd:sequence>
        <xsd:attributeGroup ref="AG_Id" />
        <xsd:attributeGroup ref="AG_StrokeAttributes" />
    </xsd:complexType>
    """

    @property
    def o_left(self):

        ele: Optional[CT_StrokeChild] = getattr(self, qn('o:left'))

        return ele

    @property
    def o_top(self):

        ele: Optional[CT_StrokeChild] = getattr(self, qn('o:top'))
        return ele

    @property
    def o_right(self):

        ele: Optional[CT_StrokeChild] = getattr(self, qn('o:right'))
        return ele

    @property
    def o_bottom(self):

        ele: Optional[CT_StrokeChild] = getattr(self, qn('o:bottom'))
        return ele

    @property
    def o_column(self):

        ele: Optional[CT_StrokeChild] = getattr(self, qn('o:column'))
        return ele


class CT_TextPath(AG_Id, AG_Style):
    """Shadow Effect

    <xsd:complexType name="CT_TextPath">
        <xsd:attributeGroup ref="AG_Id" />
        <xsd:attributeGroup ref="AG_Style" />
        <xsd:attribute name="on" type="ST_TrueFalse" use="optional">
            <xsd:annotation>
                <xsd:documentation>Text Path Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="fitshape" type="ST_TrueFalse" use="optional">
            <xsd:annotation>
                <xsd:documentation>Shape Fit Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="fitpath" type="ST_TrueFalse" use="optional">
            <xsd:annotation>
                <xsd:documentation>Path Fit Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="trim" type="ST_TrueFalse" use="optional">
            <xsd:annotation>
                <xsd:documentation>Text Path Trim Toggle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="xscale" type="ST_TrueFalse" use="optional">
            <xsd:annotation>
                <xsd:documentation>Text X-Scaling</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="string" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Text Path Text</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:complexType>
    """

    @property
    def on(self) -> Optional[ST_TrueFalse]:
        """Text Path Toggle"""
        val = self.attrib.get(qn('v:on'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def fitshape(self) -> Optional[ST_TrueFalse]:
        """Shape Fit Toggle"""
        val = self.attrib.get(qn('v:fitshape'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def fitpath(self) -> Optional[ST_TrueFalse]:
        """Path Fit Toggle"""
        val = self.attrib.get(qn('v:fitpath'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def trim(self) -> Optional[ST_TrueFalse]:
        """Text Path Trim Toggle"""
        val = self.attrib.get(qn('v:trim'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def xscale(self) -> Optional[ST_TrueFalse]:
        """Text X-Scaling"""
        val = self.attrib.get(qn('v:xscale'))

        if val is not None:
            return ST_TrueFalse(val)
        return None

    @property
    def string(self) -> Optional[str]:
        """Text Path Text"""
        val = self.attrib.get(qn('v:string'))

        if val is not None:
            return str(val)
        return None


class CT_Arc(EG_ShapeElements, AG_AllCoreAttributes, AG_AllShapeAttributes):
    """Arc Segment

    <xsd:complexType name="CT_Arc">
        <xsd:sequence>
            <xsd:group ref="EG_ShapeElements" minOccurs="0" maxOccurs="unbounded" />
        </xsd:sequence>
        <xsd:attributeGroup ref="AG_AllCoreAttributes" />
        <xsd:attributeGroup ref="AG_AllShapeAttributes" />
        <xsd:attribute name="startAngle" type="xsd:decimal" use="optional">
            <xsd:annotation>
                <xsd:documentation>Starting Angle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="endAngle" type="xsd:decimal" use="optional">
            <xsd:annotation>
                <xsd:documentation>Ending Angle</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:complexType>
    """

    @property
    def startAngle(self) -> Optional[float]:
        """Starting Angle"""

        val = self.attrib.get(qn('v:startAngle'))

        if val is not None:
            return float(val)
        return None

    @property
    def endAngle(self) -> Optional[float]:
        """Ending Angle"""

        val = self.attrib.get(qn('v:endAngle'))

        if val is not None:
            return float(val)
        return None


class CT_Curve(EG_ShapeElements, AG_AllCoreAttributes, AG_AllShapeAttributes):
    """Bezier Curve

    <xsd:complexType name="CT_Curve">
        <xsd:sequence>
            <xsd:group ref="EG_ShapeElements" minOccurs="0" maxOccurs="unbounded" />
        </xsd:sequence>
        <xsd:attributeGroup ref="AG_AllCoreAttributes" />
        <xsd:attributeGroup ref="AG_AllShapeAttributes" />
        <xsd:attribute name="from" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Curve Starting Point</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="control1" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>First Curve Control Point</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="control2" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Second Curve Control Point</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="to" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Curve Ending Point</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:complexType>
    """

    @property
    def from_(self) -> Optional[str]:
        """Curve Starting Point"""

        val = self.attrib.get(qn('v:from'))

        if val is not None:
            return str(val)
        return None

    @property
    def control1(self) -> Optional[str]:
        """First Curve Control"""

        val = self.attrib.get(qn('v:control1'))

        if val is not None:
            return str(val)
        return None

    @property
    def control2(self) -> Optional[str]:
        """Second Curve Control Point"""

        val = self.attrib.get(qn('v:control2'))

        if val is not None:
            return str(val)
        return None

    @property
    def to(self) -> Optional[str]:
        """Curve Ending Point"""

        val = self.attrib.get(qn('v:to'))

        if val is not None:
            return str(val)
        return None


class CT_Image(EG_ShapeElements, AG_AllCoreAttributes, AG_AllShapeAttributes, AG_ImageAttributes):
    """Image File

    <xsd:complexType name="CT_Image">
        <xsd:sequence>
            <xsd:group ref="EG_ShapeElements" minOccurs="0" maxOccurs="unbounded" />
        </xsd:sequence>
        <xsd:attributeGroup ref="AG_AllCoreAttributes" />
        <xsd:attributeGroup ref="AG_AllShapeAttributes" />
        <xsd:attributeGroup ref="AG_ImageAttributes" />
    </xsd:complexType>
    """



class CT_Line(EG_ShapeElements, AG_AllCoreAttributes, AG_ShapeAttributes):
    """Line

    <xsd:complexType name="CT_Line">
        <xsd:sequence>
            <xsd:group ref="EG_ShapeElements" minOccurs="0" maxOccurs="unbounded" />
        </xsd:sequence>
        <xsd:attributeGroup ref="AG_AllCoreAttributes" />
        <xsd:attributeGroup ref="AG_AllShapeAttributes" />
        <xsd:attribute name="from" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Line Start</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="to" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Line End Point</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:complexType>
    """

    @property
    def from_(self) -> Optional[str]:
        """Line Start"""

        val = self.attrib.get(qn('v:from'))

        if val is not None:
            return str(val)
        return None

    @property
    def to(self) -> Optional[str]:
        """Line End Point"""

        val = self.attrib.get(qn('v:to'))

        if val is not None:
            return str(val)
        return None


class CT_Oval(EG_ShapeElements, AG_AllCoreAttributes, AG_AllShapeAttributes):
    """Oval

    <xsd:complexType name="CT_Oval">
        <xsd:choice maxOccurs="unbounded">
            <xsd:group ref="EG_ShapeElements" minOccurs="0" maxOccurs="unbounded" />
        </xsd:choice>
        <xsd:attributeGroup ref="AG_AllCoreAttributes" />
        <xsd:attributeGroup ref="AG_AllShapeAttributes" />
    </xsd:complexType>
    """



class CT_PolyLine(EG_ShapeElements, AG_AllCoreAttributes, AG_AllShapeAttributes):
    """Multiple Path Line

    <xsd:complexType name="CT_PolyLine">
        <xsd:choice minOccurs="0" maxOccurs="unbounded">
            <xsd:group ref="EG_ShapeElements" />
            <xsd:element ref="o:ink" />
        </xsd:choice>
        <xsd:attributeGroup ref="AG_AllCoreAttributes" />
        <xsd:attributeGroup ref="AG_AllShapeAttributes" />
        <xsd:attribute name="points" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Points for Compound Line</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:complexType>
    """

    @property
    def o_ink(self):

        ele: Optional[CT_Ink] = getattr(self, qn('o:ink'), None)

        return ele

    @property
    def points(self) -> Optional[str]:
        """Points for Compound Line"""

        val = self.attrib.get(qn('v:points'))

        if val is not None:
            return str(val)
        return None


class CT_Rect(EG_ShapeElements, AG_AllCoreAttributes, AG_AllShapeAttributes):
    """Rectangle

    <xsd:complexType name="CT_Rect">
        <xsd:choice maxOccurs="unbounded">
            <xsd:group ref="EG_ShapeElements" minOccurs="0" maxOccurs="unbounded" />
        </xsd:choice>
        <xsd:attributeGroup ref="AG_AllCoreAttributes" />
        <xsd:attributeGroup ref="AG_AllShapeAttributes" />
    </xsd:complexType>
    """



class CT_RoundRect(EG_ShapeElements, AG_AllCoreAttributes, AG_AllShapeAttributes):
    """Rounded Rectangle

    <xsd:complexType name="CT_RoundRect">
        <xsd:choice maxOccurs="unbounded">
            <xsd:group ref="EG_ShapeElements" minOccurs="0" maxOccurs="unbounded" />
        </xsd:choice>
        <xsd:attributeGroup ref="AG_AllCoreAttributes" />
        <xsd:attributeGroup ref="AG_AllShapeAttributes" />
        <xsd:attribute name="arcsize" type="xsd:string" use="optional">
            <xsd:annotation>
                <xsd:documentation>Rounded Corner Arc Size</xsd:documentation>
            </xsd:annotation>
        </xsd:attribute>
    </xsd:complexType>
    """

    @property
    def arcsize(self) -> Optional[str]:
        """Rounded Corner Arc Size"""

        val = self.attrib.get(qn('v:arcsize'))

        if val is not None:
            return str(val)
        return None


class ST_Ext(ST_BaseEnumType):
    """VML Extension Handling Behaviors

    <xsd:simpleType name="ST_Ext">
        <xsd:annotation>
            <xsd:documentation>VML Extension Handling Behaviors</xsd:documentation>
        </xsd:annotation>
        <xsd:restriction base="xsd:string">
            <xsd:enumeration value="view">
                <xsd:annotation>
                    <xsd:documentation>Not renderable</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="edit">
                <xsd:annotation>
                    <xsd:documentation>Editable</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="backwardCompatible">
                <xsd:annotation>
                    <xsd:documentation>Renderable</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
        </xsd:restriction>
    </xsd:simpleType>
    """

    view = 'view'
    """ Not renderable """

    edit = 'edit'
    """ Editable """

    backwardCompatible = 'backwardCompatible'
    """ Renderable """


class ST_TrueFalse(ST_BaseEnumType):
    """Boolean Value

    <xsd:simpleType name="ST_TrueFalse">
        <xsd:annotation>
            <xsd:documentation>Boolean Value</xsd:documentation>
        </xsd:annotation>
        <xsd:restriction base="xsd:string">
            <xsd:enumeration value="t">
                <xsd:annotation>
                    <xsd:documentation>True</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="f">
                <xsd:annotation>
                    <xsd:documentation>False</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="true">
                <xsd:annotation>
                    <xsd:documentation>True</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="false">
                <xsd:annotation>
                    <xsd:documentation>False</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
        </xsd:restriction>
    </xsd:simpleType>
    """

    t = 't'
    """True"""

    f = 'f'
    """False"""

    true = 'true'
    """True"""

    false = 'false'
    """False"""


class ST_ColorType(str):
    """Color Type

    <xsd:simpleType name="ST_ColorType">
        <xsd:annotation>
            <xsd:documentation>Color Type</xsd:documentation>
        </xsd:annotation>
        <xsd:restriction base="xsd:string" />
    </xsd:simpleType>
    """



class ST_FillType(ST_BaseEnumType):
    """Shape Fill Type

    <xsd:simpleType name="ST_FillType">
        <xsd:annotation>
            <xsd:documentation>Shape Fill Type</xsd:documentation>
        </xsd:annotation>
        <xsd:restriction base="xsd:string">
            <xsd:enumeration value="solid">
                <xsd:annotation>
                    <xsd:documentation>Solid Fill</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="gradient">
                <xsd:annotation>
                    <xsd:documentation>Linear Gradient</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="gradientRadial">
                <xsd:annotation>
                    <xsd:documentation>Radial Gradient</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="tile">
                <xsd:annotation>
                    <xsd:documentation>Tiled Image</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="pattern">
                <xsd:annotation>
                    <xsd:documentation>Image Pattern</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="frame">
                <xsd:annotation>
                    <xsd:documentation>Stretch Image to Fit</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
        </xsd:restriction>
    </xsd:simpleType>
    """

    solid = 'solid'
    """Solid Fill"""

    gradient = 'gradient'
    """Linear Gradient"""

    gradientRadial = 'gradientRadial'
    """Radial Gradient"""

    tile = 'tile'
    """Tiled Image"""

    pattern = 'pattern'
    """Image Pattern"""

    frame = 'frame'
    """Stretch Image to Fit"""


class ST_FillMethod(ST_BaseEnumType):
    """Gradient Fill Computation Type

    <xsd:simpleType name="ST_FillMethod">
        <xsd:annotation>
            <xsd:documentation>Gradient Fill Computation Type</xsd:documentation>
        </xsd:annotation>
        <xsd:restriction base="xsd:string">
            <xsd:enumeration value="none">
                <xsd:annotation>
                    <xsd:documentation>No Gradient Fill</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="linear">
                <xsd:annotation>
                    <xsd:documentation>Linear Fill</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="sigma">
                <xsd:annotation>
                    <xsd:documentation>Sigma Fill</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="any">
                <xsd:annotation>
                    <xsd:documentation>Application Default Fill</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="linear sigma">
                <xsd:annotation>
                    <xsd:documentation>Linear Sigma Fill</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
        </xsd:restriction>
    </xsd:simpleType>
    """

    none = 'none'
    """No Gradient Fill"""

    linear = 'linear'
    """Linear Fill"""

    sigma = 'sigma'
    """Sigma Fill"""

    any = 'any'
    """Application Default Fill"""

    linear_sigma = 'linear sigma'
    """Linear Sigma Fill"""


class ST_ShadowType(ST_BaseEnumType):
    """Shadow Type

    <xsd:simpleType name="ST_ShadowType">
        <xsd:annotation>
            <xsd:documentation>Shadow Type</xsd:documentation>
        </xsd:annotation>
        <xsd:restriction base="xsd:string">
            <xsd:enumeration value="single">
                <xsd:annotation>
                    <xsd:documentation>Single Shadow</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="double">
                <xsd:annotation>
                    <xsd:documentation>Double Shadow</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="emboss">
                <xsd:annotation>
                    <xsd:documentation>Embossed Shadow</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="perspective">
                <xsd:annotation>
                    <xsd:documentation>Perspective Shadow</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
        </xsd:restriction>
    </xsd:simpleType>
    """

    single = 'single'
    """Single Shadow"""

    double = 'double'
    """Double Shadow"""

    emboss = 'emboss'
    """Embossed Shadow"""

    perspective = 'perspective'
    """Perspective Shadow"""


class ST_StrokeLineStyle(ST_BaseEnumType):
    """Stroke Line Style

    <xsd:simpleType name="ST_StrokeLineStyle">
        <xsd:annotation>
            <xsd:documentation>Stroke Line Style</xsd:documentation>
        </xsd:annotation>
        <xsd:restriction base="xsd:string">
            <xsd:enumeration value="single">
                <xsd:annotation>
                    <xsd:documentation>Single Line</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="thinThin">
                <xsd:annotation>
                    <xsd:documentation>Two Thin Lines</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="thinThick">
                <xsd:annotation>
                    <xsd:documentation>Thin Line Outside Thick Line</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="thickThin">
                <xsd:annotation>
                    <xsd:documentation>Thick Line Outside Thin Line</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="thickBetweenThin">
                <xsd:annotation>
                    <xsd:documentation>Thck Line Between Thin Lines</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
        </xsd:restriction>
    </xsd:simpleType>
    """

    single = 'single'
    """Single Line"""

    thinThin = 'thinThin'
    """Two Thin Lines"""

    thinThick = 'thinThick'
    """Thin Line Outside Thick Line"""

    thickThin = 'thickThin'
    """Thick Line Outside Thin Line"""

    thickBetweenThin = 'thickBetweenThin'
    """Thck Line Between Thin Lines"""


class ST_StrokeJoinStyle(ST_BaseEnumType):
    """Line Join Type

    <xsd:simpleType name="ST_StrokeJoinStyle">
        <xsd:annotation>
            <xsd:documentation>Line Join Type</xsd:documentation>
        </xsd:annotation>
        <xsd:restriction base="xsd:string">
            <xsd:enumeration value="round">
                <xsd:annotation>
                    <xsd:documentation>Round Joint</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="bevel">
                <xsd:annotation>
                    <xsd:documentation>Bevel Joint</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="miter">
                <xsd:annotation>
                    <xsd:documentation>Miter Joint</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
        </xsd:restriction>
    </xsd:simpleType>
    """

    round = 'round'
    """Round Joint"""

    bevel = 'bevel'
    """Bevel Joint"""

    miter = 'miter'
    """Miter Joint"""


class ST_StrokeEndCap(ST_BaseEnumType):
    """Stroke End Cap Type

    <xsd:simpleType name="ST_StrokeEndCap">
        <xsd:annotation>
            <xsd:documentation>Stroke End Cap Type</xsd:documentation>
        </xsd:annotation>
        <xsd:restriction base="xsd:string">
            <xsd:enumeration value="flat">
                <xsd:annotation>
                    <xsd:documentation>Flat End</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="square">
                <xsd:annotation>
                    <xsd:documentation>Square End</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="round">
                <xsd:annotation>
                    <xsd:documentation>Round End</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
        </xsd:restriction>
    </xsd:simpleType>
    """

    flat = 'flat'
    """Flat End"""

    square = 'square'
    """Square End"""

    round = 'round'
    """Round End"""


class ST_StrokeArrowLength(ST_BaseEnumType):
    """Stroke Arrowhead Length

    <xsd:simpleType name="ST_StrokeArrowLength">
        <xsd:annotation>
            <xsd:documentation>Stroke Arrowhead Length</xsd:documentation>
        </xsd:annotation>
        <xsd:restriction base="xsd:string">
            <xsd:enumeration value="short">
                <xsd:annotation>
                    <xsd:documentation>Short Arrowhead</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="medium">
                <xsd:annotation>
                    <xsd:documentation>Medium Arrowhead</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="long">
                <xsd:annotation>
                    <xsd:documentation>Long Arrowhead</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
        </xsd:restriction>
    </xsd:simpleType>
    """

    short = 'short'
    """Short Arrowhead"""

    medium = 'medium'
    """Medium Arrowhead"""

    long = 'long'
    """Long Arrowhead"""


class ST_StrokeArrowWidth(ST_BaseEnumType):
    """Stroke Arrowhead Width

    <xsd:simpleType name="ST_StrokeArrowWidth">
        <xsd:annotation>
            <xsd:documentation>Stroke Arrowhead Width</xsd:documentation>
        </xsd:annotation>
        <xsd:restriction base="xsd:string">
            <xsd:enumeration value="narrow">
                <xsd:annotation>
                    <xsd:documentation>Narrow Arrowhead</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="medium">
                <xsd:annotation>
                    <xsd:documentation>Medium Arrowhead</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="wide">
                <xsd:annotation>
                    <xsd:documentation>Wide Arrowhead</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
        </xsd:restriction>
    </xsd:simpleType>
    """

    narrow = 'narrow'
    """Narrow Arrowhead"""

    medium = 'medium'
    """Medium Arrowhead"""

    wide = 'wide'
    """Wide Arrowhead"""


class ST_StrokeArrowType(ST_BaseEnumType):
    """Stroke Arrowhead Type

    <xsd:simpleType name="ST_StrokeArrowType">
        <xsd:annotation>
            <xsd:documentation>Stroke Arrowhead Type</xsd:documentation>
        </xsd:annotation>
        <xsd:restriction base="xsd:string">
            <xsd:enumeration value="none">
                <xsd:annotation>
                    <xsd:documentation>No Arrowhead</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="block">
                <xsd:annotation>
                    <xsd:documentation>Block Arrowhead</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="classic">
                <xsd:annotation>
                    <xsd:documentation>Classic Arrowhead</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="oval">
                <xsd:annotation>
                    <xsd:documentation>Oval Arrowhead</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="diamond">
                <xsd:annotation>
                    <xsd:documentation>Diamond Arrowhead</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="open">
                <xsd:annotation>
                    <xsd:documentation>Open Arrowhead</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
        </xsd:restriction>
    </xsd:simpleType>
    """

    none = 'none'
    """No Arrowhead"""

    block = 'block'
    """Block Arrowhead"""

    classic = 'classic'
    """Classic Arrowhead"""

    oval = 'oval'
    """Oval Arrowhead"""

    diamond = 'diamond'
    """Diamond Arrowhead"""

    open = 'open'
    """Open Arrowhead"""


class ST_ImageAspect(ST_BaseEnumType):
    """Image Scaling Behavior

    <xsd:simpleType name="ST_ImageAspect">
        <xsd:annotation>
            <xsd:documentation>Image Scaling Behavior</xsd:documentation>
        </xsd:annotation>
        <xsd:restriction base="xsd:string">
            <xsd:enumeration value="ignore">
                <xsd:annotation>
                    <xsd:documentation>Ignore Aspect Ratio</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="atMost">
                <xsd:annotation>
                    <xsd:documentation>At Most</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="atLeast">
                <xsd:annotation>
                    <xsd:documentation>At Least</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
        </xsd:restriction>
    </xsd:simpleType>
    """

    ignore = 'ignore'
    """Ignore Aspect Ratio"""

    atMost = 'atMost'
    """At Most"""

    atLeast = 'atLeast'
    """At Least"""


class ST_TrueFalseBlank(ST_BaseEnumType):
    """Boolean Value with Blank [False] State

    <xsd:simpleType name="ST_TrueFalseBlank">
        <xsd:annotation>
            <xsd:documentation>Boolean Value with Blank [False] State</xsd:documentation>
        </xsd:annotation>
        <xsd:restriction base="xsd:string">
            <xsd:enumeration value="t">
                <xsd:annotation>
                    <xsd:documentation>Logical True</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="f">
                <xsd:annotation>
                    <xsd:documentation>Logical False</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="true">
                <xsd:annotation>
                    <xsd:documentation>Logical True</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="false">
                <xsd:annotation>
                    <xsd:documentation>Logical False</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="">
                <xsd:annotation>
                    <xsd:documentation>Blank – Logical False</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
        </xsd:restriction>
    </xsd:simpleType>
    """

    t = 't'
    """Logical True"""

    f = 'f'
    """Logical False"""

    true = 'true'
    """Logical True"""

    false = 'false'
    """Logical False"""

    blank = ''
    """Blank – Logical False"""


class ST_EditAs(ST_BaseEnumType):
    """Shape Grouping Types

    <xsd:simpleType name="ST_EditAs">
        <xsd:annotation>
            <xsd:documentation>Shape Grouping Types</xsd:documentation>
        </xsd:annotation>
        <xsd:restriction base="xsd:string">
            <xsd:enumeration value="canvas">
                <xsd:annotation>
                    <xsd:documentation>Shape Canvas</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="orgchart">
                <xsd:annotation>
                    <xsd:documentation>Organization Chart Diagram</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="radial">
                <xsd:annotation>
                    <xsd:documentation>Radial Diagram</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="cycle">
                <xsd:annotation>
                    <xsd:documentation>Cycle Diagram</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="stacked">
                <xsd:annotation>
                    <xsd:documentation>Pyramid Diagram</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="venn">
                <xsd:annotation>
                    <xsd:documentation>Venn Diagram</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
            <xsd:enumeration value="bullseye">
                <xsd:annotation>
                    <xsd:documentation>Bullseye Diagram</xsd:documentation>
                </xsd:annotation>
            </xsd:enumeration>
        </xsd:restriction>
    </xsd:simpleType>
    """

    canvas = 'canvas'
    """Shape Canvas"""

    orgchart = 'orgchart'
    """Organization Chart Diagram"""

    radial = 'radial'
    """Radial Diagram"""

    cycle = 'cycle'
    """Cycle Diagram"""

    stacked = 'stacked'
    """Pyramid Diagram"""

    venn = 'venn'
    """Venn Diagram"""

    bullseye = 'bullseye'
    """Bullseye Diagram"""


vml_main_namespace = lookup.get_namespace(namespace_v)
vml_main_namespace[None] = OxmlBaseElement

vml_main_namespace['shape'] = CT_Shape  # Shape Definition
vml_main_namespace['shapetype'] = CT_Shapetype  # Shape Template
vml_main_namespace['group'] = CT_Group  # Shape Group
vml_main_namespace['background'] = CT_Background  # Document Background
vml_main_namespace['fill'] = CT_Fill  # Shape Fill Properties
vml_main_namespace['formulas'] = CT_Formulas  # Set of Formulas
vml_main_namespace['handles'] = CT_Handles  # Set of Handles
vml_main_namespace['imagedata'] = CT_ImageData  # Image Data
vml_main_namespace['path'] = CT_Path  # Shape Path
vml_main_namespace['textbox'] = CT_Textbox  # Text Box
vml_main_namespace['shadow'] = CT_Shadow  # Shadow Effect
vml_main_namespace['stroke'] = CT_Stroke  # Line Stroke Settings
vml_main_namespace['textpath'] = CT_TextPath  # Text Layout Path

vml_main_namespace['h'] = CT_H  # Set of Handles
vml_main_namespace['f'] = CT_F  # Text Layout Path

vml_main_namespace['arc'] = CT_Arc  # Arc Segment
vml_main_namespace['curve'] = CT_Curve  # Bezier Curve
vml_main_namespace['image'] = CT_Image  # Image File
vml_main_namespace['line'] = CT_Line  # Line
vml_main_namespace['oval'] = CT_Oval  # Oval
vml_main_namespace['polyline'] = CT_PolyLine  # Multiple Path Line
vml_main_namespace['rect'] = CT_Rect  # Rectangle
vml_main_namespace['roundrect'] = CT_RoundRect  # Rounded Rectangle
