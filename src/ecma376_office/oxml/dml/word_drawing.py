"""
对应xsd: dml-wordprocessingDrawing.xsd

前缀: wp

命名空间: http://purl.oclc.org/ooxml/drawingml/wordprocessingDrawing

<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"
  xmlns:a="http://purl.oclc.org/ooxml/drawingml/main"
  xmlns:w="http://purl.oclc.org/ooxml/wordprocessingml/main"
  xmlns:dpct="http://purl.oclc.org/ooxml/drawingml/picture"
  xmlns:r="http://purl.oclc.org/ooxml/officeDocument/relationships"
  xmlns="http://purl.oclc.org/ooxml/drawingml/wordprocessingDrawing"
  targetNamespace="http://purl.oclc.org/ooxml/drawingml/wordprocessingDrawing"
  elementFormDefault="qualified">
  <xsd:import namespace="http://purl.oclc.org/ooxml/drawingml/main" schemaLocation="dml-main.xsd"/>
  <xsd:import schemaLocation="wml.xsd" namespace="http://purl.oclc.org/ooxml/wordprocessingml/main"/>
  <xsd:import namespace="http://purl.oclc.org/ooxml/drawingml/picture" schemaLocation="dml-picture.xsd"/>
  <xsd:import namespace="http://purl.oclc.org/ooxml/officeDocument/relationships" schemaLocation="shared-relationshipReference.xsd"/>

  ...

</xsd:schema>
"""

from __future__ import annotations

import logging
from typing import (
    TYPE_CHECKING,
    NewType,
    Optional,
    TypeVar,
)

from ecma376_office.oxml import utils
from ecma376_office.oxml.base import OxmlBaseElement, ST_BaseEnumType, lookup
from ecma376_office.oxml.dml.main import CT_BackgroundFormatting as a_CT_BackgroundFormatting
from ecma376_office.oxml.dml.main import CT_GraphicalObject as a_CT_GraphicalObject
from ecma376_office.oxml.dml.main import CT_GroupShapeProperties as a_CT_GroupShapeProperties
from ecma376_office.oxml.dml.main import CT_NonVisualConnectorProperties as a_CT_NonVisualConnectorProperties
from ecma376_office.oxml.dml.main import CT_NonVisualContentPartProperties as a_CT_NonVisualContentPartProperties
from ecma376_office.oxml.dml.main import CT_NonVisualDrawingProps as a_CT_NonVisualDrawingProps
from ecma376_office.oxml.dml.main import CT_NonVisualDrawingShapeProps as a_CT_NonVisualDrawingShapeProps
from ecma376_office.oxml.dml.main import CT_NonVisualGraphicFrameProperties as a_CT_NonVisualGraphicFrameProperties
from ecma376_office.oxml.dml.main import CT_NonVisualGroupDrawingShapeProps as a_CT_NonVisualGroupDrawingShapeProps
from ecma376_office.oxml.dml.main import CT_OfficeArtExtensionList as a_CT_OfficeArtExtensionList
from ecma376_office.oxml.dml.main import CT_Point2D as a_CT_Point2D
from ecma376_office.oxml.dml.main import CT_PositiveSize2D as a_CT_PositiveSize2D
from ecma376_office.oxml.dml.main import CT_ShapeProperties as a_CT_ShapeProperties
from ecma376_office.oxml.dml.main import CT_ShapeStyle as a_CT_ShapeStyle
from ecma376_office.oxml.dml.main import CT_TextBodyProperties as a_CT_TextBodyProperties
from ecma376_office.oxml.dml.main import CT_Transform2D as a_CT_Transform2D
from ecma376_office.oxml.dml.main import CT_WholeE2oFormatting as a_CT_WholeE2oFormatting
from ecma376_office.oxml.dml.main import ST_BlackWhiteMode as a_ST_BlackWhiteMode
from ecma376_office.oxml.dml.main import ST_Coordinate as a_ST_Coordinate
from ecma376_office.oxml.dml.main import to_ST_Coordinate as a_to_ST_Coordinate
from ecma376_office.oxml.shared.relationship_reference import ST_RelationshipId as r_ST_RelationshipId
from ecma376_office.oxml.xsd_types import to_xsd_bool

if TYPE_CHECKING:
    from ecma376_office.oxml.dml.picture import CT_Picture as wpct_CT_Picture
    from ecma376_office.oxml.wml.main import CT_P as w_CT_P
    from ecma376_office.oxml.wml.main import CT_AltChunk as w_CT_AltChunk
    from ecma376_office.oxml.wml.main import CT_Bookmark as w_CT_Bookmark
    from ecma376_office.oxml.wml.main import CT_CustomXmlBlock as w_CT_CustomXmlBlock
    from ecma376_office.oxml.wml.main import CT_Markup as w_CT_Markup
    from ecma376_office.oxml.wml.main import CT_MarkupRange as w_CT_MarkupRange
    from ecma376_office.oxml.wml.main import CT_MoveBookmark as w_CT_MoveBookmark
    from ecma376_office.oxml.wml.main import CT_Perm as w_CT_Perm
    from ecma376_office.oxml.wml.main import CT_PermStart as w_CT_PermStart
    from ecma376_office.oxml.wml.main import CT_ProofErr as w_CT_ProofErr
    from ecma376_office.oxml.wml.main import CT_RunTrackChange as w_CT_RunTrackChange
    from ecma376_office.oxml.wml.main import CT_SdtBlock as w_CT_SdtBlock
    from ecma376_office.oxml.wml.main import CT_TrackChange as w_CT_TrackChange
    from ecma376_office.oxml.wml.main import m_CT_OMath as w_m_CT_OMath
    from ecma376_office.oxml.wml.main import m_CT_OMathPara as w_m_CT_OMathPara

logger = logging.getLogger(__name__)


# namespace_a = "http://purl.oclc.org/ooxml/drawingml/main"
namespace_a = 'http://schemas.openxmlformats.org/drawingml/2006/main'

# namespace_wp = "http://purl.oclc.org/ooxml/drawingml/wordprocessingDrawing"
namespace_wp = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'

# namespace_w = "http://purl.oclc.org/ooxml/wordprocessingml/main"
namespace_w = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

# namespace_wpct = "http://purl.oclc.org/ooxml/drawingml/picture"
namespace_wpct = 'http://schemas.openxmlformats.org/drawingml/2006/picture'

# namespace_r = "http://purl.oclc.org/ooxml/officeDocument/relationships"
namespace_r = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

ns_map = {
    'wp': namespace_wp,  # 当前命名空间
    'a': namespace_a,
    'w': namespace_w,
    'wpct': namespace_wpct,
    'r': namespace_r,
}


def qn(tag: str):
    """将 dc:creator 这种的标签,转换为 {http://purl.org/dc/elements/1.1/}creator 这样的形式"""

    global ns_map

    if ':' not in tag:
        return tag

    ns_prefix, ns = tag.split(':')

    return f'{{{ns_map[ns_prefix]}}}{ns}'


SubBaseElement = TypeVar('SubBaseElement', bound=OxmlBaseElement)


class CT_EffectExtent(OxmlBaseElement):
    """20.4.2.6 effectExtent (对象范围（包括效果）)¶

    effectExtent (Object Extents Including Effects)

    该元素指定了要添加到图像的每个边缘（顶部、底部、左侧、右侧）以补偿应用于DrawingML对象的任何绘制效果的附加范围。

    extent元素（[§20.4.2.7]）指定了实际DrawingML对象的大小；然而，可以应用改变其整体大小的效果于对象上[示例：反射和/或阴影效果。结束示例]。每个形状边缘的附加大小将存储在此元素上，并用于计算没有包装多边形的包装类型的适当包装以及内联对象的适当行高。
    """

    @property
    def left(self) -> a_ST_Coordinate:
        """l（左侧边缘的额外长度）

        指定以EMUs为单位添加到绘图对象底部边缘以确定其包括效果的实际底部边缘的额外长度。

        [示例：考虑以下绘图对象图像：

        123

        该图像在四个边上都有效果，导致以下标记：

        <wp:effectExtent l="504825" t="447675" r="771525" b="809625" />

        l属性值504825指定必须在图像底部添加504825个额外的EMUs以补偿图像上的效果。结束示例]

        此属性的可能值由ST_Coordinate简单类型（[§20.1.10.16]）定义。
        """

        val = self.attrib[qn('wp:l')]

        return a_to_ST_Coordinate(str(val))

    @property
    def top(self) -> a_ST_Coordinate:
        """t（顶部边缘的额外长度）

        指定以EMUs为单位添加到绘图对象底部边缘以确定其包括效果的实际底部边缘的额外长度。

        [示例：考虑以下绘图对象图像：

        123

        该图像在四个边上都有效果，导致以下标记：

        <wp:effectExtent l="504825" t="447675" r="771525" b="809625" />

        t属性值447675指定必须在图像底部添加447675个额外的EMUs以补偿图像上的效果。结束示例]

        此属性的可能值由ST_Coordinate简单类型（[§20.1.10.16]）定义。
        """

        val = self.attrib[qn('wp:t')]

        return a_to_ST_Coordinate(str(val))

    @property
    def right(self) -> a_ST_Coordinate:
        """r（右侧边缘的额外长度）

        指定以EMUs为单位添加到绘图对象底部边缘以确定其包括效果的实际底部边缘的额外长度。

        [示例：考虑以下绘图对象图像：

        123

        该图像在四个边上都有效果，导致以下标记：

        <wp:effectExtent l="504825" t="447675" r="771525" b="809625" />

        r属性值771525指定必须在图像底部添加771525个额外的EMUs以补偿图像上的效果。结束示例]

        此属性的可能值由ST_Coordinate简单类型（[§20.1.10.16]）定义。
        """

        val = self.attrib[qn('wp:r')]

        return a_to_ST_Coordinate(str(val))

    @property
    def bottom(self) -> a_ST_Coordinate:
        """b（底部边缘的额外长度）

        指定以EMUs为单位添加到绘图对象底部边缘以确定其包括效果的实际底部边缘的额外长度。

        [示例：考虑以下绘图对象图像：

        123

        该图像在四个边上都有效果，导致以下标记：

        <wp:effectExtent l="504825" t="447675" r="771525" b="809625" />

        b属性值809625指定必须在图像底部添加809625个额外的EMUs以补偿图像上的效果。结束示例]

        此属性的可能值由ST_Coordinate简单类型（[§20.1.10.16]）定义。
        """

        val = self.attrib[qn('wp:b')]

        return a_to_ST_Coordinate(str(val))


class ST_WrapDistance(int):
    """20.4.3.6 ST_WrapDistance (文本偏移距离)

    ST_WrapDistance (Distance from Text)

    这个简单类型表示一维距离，用于将对象从以EMUs为单位存储的文本偏移。

    [示例：考虑一个浮动的DrawingML对象，其左边缘与最近的文本之间必须有三分之一英寸的空白。可以将此设置指定如下：

    <wp:anchor … >
        …
        <wp:wrapThrough distL="457200" … />
    </wp:anchor>

    distL属性指定填充距离必须为457200 EMUs或三分之一英寸。示例结束]

    这个简单类型的内容是W3C XML Schema无符号整数（unsignedInt）数据类型的限制。
    """



class CT_Inline(OxmlBaseElement):
    """20.4.2.8 inline (内联DrawingML对象)¶

    inline (Inline DrawingML Object)

    此元素指定文档中位于此位置的DrawingML对象是内联对象。在WordprocessingML文档中，绘图对象可以存在两种状态：

    - 内联(Inline) - 绘图对象与文本一起排列，并影响其所在行的行高和布局（类似于相同大小的字符字形）。
    - 浮动(Floating) - 绘图对象在文本中锚定，但可以在文档中相对于页面进行绝对定位。

    当此元素封装DrawingML对象的信息时，所有子元素都应指定此对象与文本的位置。

    [示例：考虑一个WordprocessingML文档，其中内联DrawingML对象必须是段落中第一个运行内容。该段落的内容应指定如下：

    <w:p>
        <w:r>
            <w:drawing>
                <wp:inline>
                    …
                </wp:inline>
            </w:drawing>
        </w:r>
    </w:p>

    当内联元素作为绘图元素的子元素出现时，指定此DrawingML对象必须与该段落的文本在同一行中排列，并根据需要修改行高等。示例结束]
    """

    @property
    def extent(self) -> a_CT_PositiveSize2D:
        """20.4.2.7 extent (绘图对象尺寸)

        extent (Drawing Object Size)

        该元素指定了文档中父级DrawingML对象的范围（即其最终的高度和宽度）。

        [示例：考虑一个在WordprocessingML文档中出现的DrawingML图片，其高度和宽度相等。该对象将被指定如下：

        <wp:anchor relativeHeight="10" allowOverlap="true">
            …
            <wp:extent cx="1828800" cy="1828800"/>
            …
        </wp:anchor>

        extent元素通过其属性指定了该对象的高度和宽度为1828800 EMUs（英制度量单位）。示例结束]
        """
        return getattr(self, qn('wp:extent'))

    @property
    def effect_extent(self) -> Optional[CT_EffectExtent]:
        """20.4.2.6 effectExtent (对象范围（包括效果）)¶

        effectExtent (Object Extents Including Effects)

        该元素指定了要添加到图像的每个边缘（顶部、底部、左侧、右侧）以补偿应用于DrawingML对象的任何绘制效果的附加范围。

        extent元素（[§20.4.2.7]）指定了实际DrawingML对象的大小；然而，可以应用改变其整体大小的效果于对象上[示例：反射和/或阴影效果。结束示例]。每个形状边缘的附加大小将存储在此元素上，并用于计算没有包装多边形的包装类型的适当包装以及内联对象的适当行高。
        """
        return getattr(self, qn('wp:effectExtent'), None)

    @property
    def doc_pr(self) -> a_CT_NonVisualDrawingProps:
        """20.4.2.5 docPr (绘图对象非可视属性)¶

        docPr (Drawing Object Non-Visual Properties)

        该元素指定了父级 DrawingML 对象的非可见对象属性。这些属性是作为该元素的子元素指定的。

        [示例：考虑一个在 WordprocessingML 文档中定义的 DrawingML 对象，如下所示：

        <wp:inline>
            …
            <wp:docPr id="1" name="示例对象">
                <a:hlinkClick … />
                <a:hlinkHover … />
            </wp:docPr>
        </wp:inline>

        docPr 元素包含了该对象的一组常见非可见属性。结束示例]
        """
        return getattr(self, qn('wp:docPr'))

    @property
    def c_nv_graphic_frame_pr(self) -> Optional[a_CT_NonVisualGraphicFrameProperties]:
        """20.4.2.4 cNvGraphicFramePr (常见 DrawingML 非可视属性)¶

        cNvGraphicFramePr (Common DrawingML Non-Visual Properties)

        该元素指定了父 DrawingML 对象的常见非可视属性。这些属性被指定为该元素的子元素。

        【示例：考虑一个在 WordprocessingML 文档中定义的 DrawingML 对象，如下所示：

        <wp:inline>
            …
            <wp:cNvGraphicFramePr>
                <a:graphicFrameLocks … />
            </wp:cNvGraphicFramePr>
        </wp:inline>

        cNvGraphicFramePr 元素包含了一组由 DrawingML 定义的常见非可视属性。示例结束】
        """
        return getattr(self, qn('wp:cNvGraphicFramePr'))

    @property
    def graphic(self) -> a_CT_GraphicalObject:
        """20.1.2.2.16 graphic (图形对象)

        graphic (Graphic Object)

        该元素指定单个图形对象的存在。 当文档作者希望保留某种图形对象时，应该引用此元素。 该图形对象的规范完全由文档作者提供，并在 GraphicData 子元素中引用.

        [Note: 该元素内容模型 (CT_GraphicalObject) 的 W3C XML 架构定义位于 §A.4.1 中。 end note]

        <xsd:element ref="a:graphic" minOccurs="1" maxOccurs="1"/>"""

        return getattr(self, qn('a:graphic'))

    @property
    def dist_t(self) -> Optional[ST_WrapDistance]:
        """distT（距离顶边缘的距离）

        指定在显示文档内容时，此绘图对象的顶边缘与文档中任何后续文本之间应保持的最小距离。

        距离以EMUs（英制度量单位）为单位进行测量。

        如果此对象是内联对象（即具有内联父元素），则在与文本一起显示对象时，此值不会产生任何效果，但如果对象随后更改为浮动，则可以保持和使用此值。如果作为子元素存在的包装元素[示例：wrapThrough或wrapSquare结束示例]也具有距离文本，则应忽略此值。

        [示例：考虑一个浮动的DrawingML对象，其顶边缘与最近的文本之间必须有半英寸的填充。可以如下指定此设置：

        <wp:anchor distT="457200" … >
        …
        </wp:anchor>

        distT属性指定填充距离必须为457200 EMUs或四分之一英寸。结束示例]

        此属性的可能值由ST_WrapDistance简单类型（[§20.4.3.6]）定义。
        """
        _val = self.attrib.get('distT')

        if _val is None:
            return None

        return ST_WrapDistance(_val)  # type: ignore

    @property
    def dist_b(self) -> Optional[ST_WrapDistance]:
        """distB（底边距离文本的距离）

        指定在显示此绘图对象时，该对象的底边与文档中任何后续文本之间应保持的最小距离。

        距离以EMUs（英制度量单位）为单位进行测量。

        如果此对象是内联对象（即具有内联父元素），则在与文本一起显示对象时，此值不会产生任何效果，但如果对象随后更改为浮动，则可以保持和使用此值。如果作为子元素存在的包装元素[示例：wrapThrough或wrapSquare结束示例]也具有距离文本，则将忽略此值。

        [示例：考虑一个浮动的DrawingML对象，其底边与最近的文本之间必须有半英寸的填充。可以如下指定此设置：


        <wp:anchor distB="457200" … >
        …
        </wp:anchor>

        distB属性指定填充距离必须为457200 EMUs或半英寸。结束示例]

        此属性的可能值由ST_WrapDistance简单类型（[§20.4.3.6]）定义。
        """
        _val = self.attrib.get('distB')

        if _val is None:
            return None

        return ST_WrapDistance(_val)  # type: ignore

    @property
    def dist_l(self) -> Optional[ST_WrapDistance]:
        """distL（左边距离文本的距离）

        指定在显示此绘图对象时，该对象的左边与文档中任何后续文本之间应保持的最小距离。

        距离以EMUs（英制度量单位）为单位进行测量。

        如果此对象是内联对象（即具有内联父元素），则在与文本一起显示对象时，此值不会产生任何效果，但如果对象随后更改为浮动，则可以保持和使用此值。如果作为子元素存在的包装元素[示例：wrapThrough或wrapSquare结束示例]也具有距离文本，则将忽略此值。

        [示例：考虑一个浮动的DrawingML对象，其左边与最近的文本之间必须有四分之一英寸的填充。可以如下指定此设置：


        <wp:anchor distL="228600" … >
        …
        </wp:anchor>

        distL属性指定填充距离必须为228600 EMUs或四分之一英寸。结束示例]

        此属性的可能值由ST_WrapDistance简单类型（[§20.4.3.6]）定义。
        """
        _val = self.attrib.get('distL')

        if _val is None:
            return None

        return ST_WrapDistance(_val)  # type: ignore

    @property
    def dist_r(self) -> Optional[ST_WrapDistance]:
        """distR（距离右边缘的距离）

        指定在显示文档内容时，此绘图对象的右边缘与文档中任何后续文本之间应保持的最小距离。

        距离以EMUs（英制度量单位）为单位进行测量。

        如果此对象是内联对象（即具有内联父元素），则在与文本一起显示对象时，此值不会产生任何效果，但如果对象随后更改为浮动，则可以保持和使用此值。如果作为子元素存在的包装元素[示例：wrapThrough或wrapSquare结束示例]也具有距离文本，则应忽略此值。

        [示例：考虑一个浮动的DrawingML对象，其右边缘与最近的文本之间必须有四分之一英寸的填充。可以如下指定此设置：

        <wp:anchor distR="228600" … >
        …
        </wp:anchor>

        distR属性指定填充距离必须为228600 EMUs或四分之一英寸。结束示例]

        此属性的可能值由ST_WrapDistance简单类型（[§20.4.3.6]）定义。
        """
        _val = self.attrib.get('distR')

        if _val is None:
            return None

        return ST_WrapDistance(_val)  # type: ignore


class ST_WrapText(ST_BaseEnumType):
    """20.4.3.7 ST_WrapText (文本环绕位置设置)¶

    ST_WrapText (Text Wrapping Location)

    这种简单类型指定了文本如何围绕对象的左侧和右侧环绕的可能设置。

    [示例：考虑一个浮动的DrawingML对象，必须允许文本仅围绕其左侧环绕。可以如下指定此设置:

    <wp:anchor … >
        …
        <wp:wrapTight wrapText="left" … />
    </wp:anchor>

    left的wrapText属性值指定了文本只能围绕对象的左侧。示例结束]

    这种简单类型的内容是W3C XML模式令牌数据类型的限制。
    """

    BothSides = 'bothSides'
    """bothSides (两侧)

    指定文本应围绕对象的两侧环绕。
    """

    Left = 'left'
    """left (仅左侧)

    指定文本应仅围绕对象的左侧环绕。
    """

    Right = 'right'
    """right (仅右侧)

    指定文本应仅围绕对象的右侧环绕。
    """

    Largest = 'largest'
    """largest (仅最大边)

    指定文本应仅围绕对象的最大边缘环绕。

    如果对象位于页面的确切中心，则文本将环绕发现文本的一侧：

    - 如果与对象相交的第一行文本使用从左到右的阅读顺序，则文本将环绕到对象的左侧。
    - 如果与对象相交的第一行文本使用从右到左的阅读顺序，则文本将环绕到对象的右侧。
    """


class CT_WrapPath(OxmlBaseElement):
    """20.4.2.16 wrapPolygon (环绕多边形)¶

    wrapPolygon (Wrapping Polygon)

    该元素指定了用于确定文档中指定对象周围文本可以环绕的范围的包裹多边形。该多边形由以下内容定义：

    - start元素定义包裹多边形的起点坐标
    - 两个或更多的lineTo元素定义包裹多边形的点

    如果子元素集合不能形成一个封闭的多边形（最后一个lineTo元素没有返回到start元素指定的位置），则需要推断一个额外的线段来封闭包裹多边形。

    【示例：考虑以下用于DrawingML对象的基本包裹多边形：

    <wp:wrapPolygon>
        <wp:start x="0" y="0" />
        <wp:lineTo x="0" y="100" />
        <wp:lineTo x="100" y="100" />
        <wp:lineTo x="100" y="0" />
        <wp:lineTo x="0" y="0" />
    </wp:wrapPolygon>

    wrapPolygon元素定义了对象的文本包裹多边形（在本例中为一个正方形的四个点）。示例结束】
    """

    @property
    def start(self) -> a_CT_Point2D:
        """20.4.2.14 start (环绕多边形起点)¶

        start (Wrapping Polygon Start)

        此元素指定了绘图对象的包裹多边形的起始点。该点应为父对象包裹多边形的起始和终止点。

        该元素上的属性应指定该点相对于实际对象左上角的位置。

        【示例：考虑以下绘图对象的基本包裹多边形：

        <wp:wrapPolygon>
            <wp:start x="0" y="0" />
            <wp:lineTo x="0" y="100" />
            <wp:lineTo x="100" y="100" />
            <wp:lineTo x="100" y="0" />
            <wp:lineTo x="0" y="0" />
        </wp:wrapPolygon>

        start元素定义了包裹多边形的起始和结束点（在本例中为包裹正方形的四个点）。示例结束】
        """
        return getattr(self, qn('wp:start'))

    @property
    def lineTo(self) -> list[a_CT_Point2D]:
        """
        20.4.2.9 lineTo (包裹多边形线结束位置)¶

        lineTo (Wrapping Polygon Line End Position)

        该元素指定了绘图对象包裹多边形上的一个点。该点应为包裹多边形中前一个start或lineTo元素开始的边的终点，并且应为同一多边形上下一条边的起点。

        该元素上的属性应指定该点相对于实际对象左上角的位置。

        【示例：考虑以下绘图对象的基本包裹多边形：


        <wp:wrapPolygon>
            <wp:start x="0" y="0" />
            <wp:lineTo x="0" y="100" />
            <wp:lineTo x="100" y="100" />
            <wp:lineTo x="100" y="0" />
            <wp:lineTo x="0" y="0" />
        </wp:wrapPolygon>
        lineTo元素定义了包裹多边形的每个点（在本例中为包裹正方形的四个点）。示例结束】

        <xsd:element name="lineTo" type="a:CT_Point2D" minOccurs="2" maxOccurs="unbounded"/>
        """

        return self.findall(qn('wp:lineTo'))  # type: ignore

    @property
    def edited(self) -> Optional[bool]:
        """edited（已编辑的包裹点）

        命名空间：http://purl.oclc.org/ooxml/drawingml/main

        指定包裹多边形的包裹点已被编辑，并且在下次打开文档时将重新计算结果范围。

        【示例：考虑以下用于DrawingML对象的基本包裹多边形：


        <wp:wrapPolygon edited="true">
            <wp:start x="0" y="0" />
            <wp:lineTo x="0" y="100" />
            <wp:lineTo x="50" y="50" />
            <wp:lineTo x="0" y="0" />
        </wp:wrapPolygon>

        edited属性指定这些包裹点自上次呈现文档以来已更改。示例结束】

        此属性的可能值由W3C XML Schema布尔数据类型定义。
        """
        _val = self.attrib.get('edited')

        if _val is None:
            return None

        return to_xsd_bool(_val)


class CT_WrapNone(OxmlBaseElement):
    """20.4.2.15 wrapNone (无文字环绕)¶

    wrapNone (No Text Wrapping)

    该元素指定父级DrawingML对象不应根据其显示位置在宿主WordprocessingML文档的内容中引起任何文本换行。实际上，此设置将将对象放置在两个位置之一：

    如果父元素上的behindDoc属性为true，则对象将被定位在文本后面，就像通常显示的那样。

    如果父元素上的behindDoc属性为false，则对象将被定位在文本前面，就像通常显示的那样。

    [示例：考虑一个必须显示在页面上任何文本前面的DrawingML图片。可以按以下方式指定此对象：

    <wp:anchor relativeHeight="10" behindDoc="false">
        …
        <wp:wrapNone/>
    </wp:anchor>

    wrapNone元素指定DrawingML对象不能引起任何文本换行，并且由于behindDoc属性为false，因此对象必须显示在文档的文本前面。示例结束]
    """



class CT_WrapSquare(OxmlBaseElement):
    """20.4.2.17 wrapSquare (方形环绕)¶

    wrapSquare (Square Wrapping)

    此元素指定文本应该围绕一个虚拟矩形框住该对象。包围矩形的边界应由范围确定，包括将effectExtent元素作为此元素的子元素（如果存在）或父元素上存在的effectExtent。

    【示例：考虑一个使用方形包围并定义如下的DrawingML对象：


    <wp:anchor … >
        …
        <wp:wrapSquare wrapText="bothSides" />
    </wp:anchor>

    wrapSquare元素指定文本必须围绕该对象周围的一个矩形的两侧包裹，该矩形包括其效果范围。结束示例】
    """

    @property
    def effect_extent(self) -> Optional[CT_EffectExtent]:
        """20.4.2.6 effectExtent (对象范围（包括效果）)¶

        effectExtent (Object Extents Including Effects)

        该元素指定了要添加到图像的每个边缘（顶部、底部、左侧、右侧）以补偿应用于DrawingML对象的任何绘制效果的附加范围。

        extent元素（[§20.4.2.7]）指定了实际DrawingML对象的大小；然而，可以应用改变其整体大小的效果于对象上[示例：反射和/或阴影效果。结束示例]。每个形状边缘的附加大小将存储在此元素上，并用于计算没有包装多边形的包装类型的适当包装以及内联对象的适当行高。
        """
        return getattr(self, qn('wp:effectExtent'), None)

    @property
    def wrap_text(self) -> ST_WrapText:
        """wrapText（文本环绕位置）

        指定文本如何环绕对象的左侧和右侧。

        [示例：考虑一个浮动的DrawingML对象，其只允许文本环绕其左侧。此设置将如下所示：

        <wp:anchor … >
            …
            <wp:wrapSquare wrapText="left" … />
        </wp:anchor>

        wrapText属性值left指定文本只能环绕对象的左侧。示例结束]

        此属性的可能值由ST_WrapText简单类型（[§20.4.3.7]）定义。
        """
        _val = self.attrib['wrapText']

        return ST_WrapText(utils.AnyStrToStr(_val))  # type: ignore

    @property
    def dist_t(self) -> Optional[ST_WrapDistance]:
        """distT（距离文本的距离（顶部））

        指定在显示文档内容时，此绘图对象的顶边缘与文档中任何后续文本之间必须保持的最小距离。

        距离以EMUs（英制度量单位）为单位进行测量。

        [示例：考虑一个浮动的DrawingML对象，其顶边缘与最近的文本之间必须有半英寸的填充。此设置将如下所示：

        <wp:anchor … >
            …
            <wp:wrapSquare distT="457200" … />
        </wp:anchor>

        distT属性指定填充距离必须为457200 EMUs或半英寸。示例结束]

        此属性的可能值由ST_WrapDistance简单类型（[§20.4.3.6]）定义。
        """
        _val = self.attrib.get('distT')

        if _val is None:
            return None

        return ST_WrapDistance(utils.AnyStrToStr(_val))  # type: ignore

    @property
    def dist_b(self) -> Optional[ST_WrapDistance]:
        """distB（距离底部文本的距离）

        指定在此绘图对象在文档内容中显示时，该绘图对象的底部边缘与任何后续文本之间应保持的最小距离。

        距离以EMUs（英制度量单位）为单位进行测量。

        【示例：考虑一个浮动的DrawingML对象，其底部边缘与最近的文本之间必须有半英寸的填充。可以如下指定此设置：


        <wp:anchor … >
            …
            <wp:wrapSquare distB="457200" … />
        </wp:anchor>

        distB属性指定填充距离必须为457200 EMUs或半英寸。示例结束】

        此属性的可能值由ST_WrapDistance简单类型（[§20.4.3.6]）定义。
        """
        _val = self.attrib.get('distB')

        if _val is None:
            return None

        return ST_WrapDistance(utils.AnyStrToStr(_val))  # type: ignore

    @property
    def dist_l(self) -> Optional[ST_WrapDistance]:
        """distL（距离左侧文本的距离）

        指定在此绘图对象在文档内容中显示时，该绘图对象的左侧边缘与任何后续文本之间应保持的最小距离。

        距离以EMUs（英制度量单位）为单位进行测量。

        【示例：考虑一个浮动的DrawingML对象，其左侧边缘与最近的文本之间必须有半英寸的填充。可以如下指定此设置：

        <wp:anchor … >
            …
            <wp:wrapSquare distL="457200" … />
        </wp:anchor>

        distL属性指定填充距离必须为457200 EMUs或半英寸。示例结束】

        此属性的可能值由ST_WrapDistance简单类型（[§20.4.3.6]）定义。
        """
        _val = self.attrib.get('distL')

        if _val is None:
            return None

        return ST_WrapDistance(utils.AnyStrToStr(_val))  # type: ignore

    @property
    def dist_r(self) -> Optional[ST_WrapDistance]:
        """distR（距离右边缘的距离）

        指定在显示文档内容时，此绘图对象的右边缘与文档中任何后续文本之间必须保持的最小距离。

        距离以EMUs（英制度量单位）为单位进行测量。

        [示例：考虑一个浮动的DrawingML对象，其右边缘与最近的文本之间必须有半英寸的填充。此设置将如下所示：

        <wp:anchor … >
            …
            <wp:wrapSquare distR="457200" … />
        </wp:anchor>

        distR属性指定填充距离必须为457200 EMUs或半英寸。示例结束]

        此属性的可能值由ST_WrapDistance简单类型（[§20.4.3.6]）定义。
        """
        _val = self.attrib.get('distR')

        if _val is None:
            return None

        return ST_WrapDistance(utils.AnyStrToStr(_val))  # type: ignore


class CT_WrapTight(OxmlBaseElement):
    """20.4.2.19 wrapTight (Tight 环绕)

    wrapTight (Tight Wrapping)

    该元素指定文本应该围绕由子元素wrapPolygon定义的包围多边形包围此对象。当该元素指定一个包围多边形时，它不允许文本在对象的最大左右范围内换行。
    """

    @property
    def wrap_polygon(self) -> CT_WrapPath:
        """20.4.2.16 wrapPolygon (环绕多边形)¶

        wrapPolygon (Wrapping Polygon)

        该元素指定了用于确定文档中指定对象周围文本可以环绕的范围的包裹多边形。该多边形由以下内容定义：

        - start元素定义包裹多边形的起点坐标
        - 两个或更多的lineTo元素定义包裹多边形的点

        如果子元素集合不能形成一个封闭的多边形（最后一个lineTo元素没有返回到start元素指定的位置），则需要推断一个额外的线段来封闭包裹多边形。

        【示例：考虑以下用于DrawingML对象的基本包裹多边形：

        <wp:wrapPolygon>
            <wp:start x="0" y="0" />
            <wp:lineTo x="0" y="100" />
            <wp:lineTo x="100" y="100" />
            <wp:lineTo x="100" y="0" />
            <wp:lineTo x="0" y="0" />
        </wp:wrapPolygon>

        wrapPolygon元素定义了对象的文本包裹多边形（在本例中为一个正方形的四个点）。示例结束】
        """
        return getattr(self, qn('wp:wrapPolygon'))

    @property
    def wrap_text(self) -> ST_WrapText:
        """wrapText（文本环绕位置）

        指定文本如何环绕对象的左侧和右侧。

        [示例：考虑一个浮动的DrawingML对象，其只允许文本环绕其左侧。可以如下指定此设置：

        <wp:anchor … >
            …
            <wp:wrapThrough wrapText="left" … />
        </wp:anchor>

        wrapText属性值left指定文本只能环绕对象的左侧。示例结束]

        此属性的可能值由ST_WrapText简单类型（[§20.4.3.7]）定义。
        """
        _val = self.attrib['wrapText']

        return ST_WrapText(utils.AnyStrToStr(_val))  # type: ignore

    @property
    def dist_l(self) -> Optional[ST_WrapDistance]:
        """distL（距离左边缘的距离）

        指定在此绘图对象在文档中显示时，该对象的左边缘与文档中任何后续文本之间必须保持的最小距离。

        距离以EMU（英制度量单位）为单位进行测量。

        [示例：考虑一个浮动的DrawingML对象，其左边缘与最近的文本之间必须有半英寸的填充。可以如下指定此设置：


        <wp:anchor … >
            …
            <wp:wrapTight distL="457200" … />
        </wp:anchor>

        distL属性指定填充距离必须为457200 EMU或半英寸。示例结束]

        此属性的可能值由ST_WrapDistance简单类型（[§20.4.3.6]）定义。
        """
        _val = self.attrib.get('distL')

        if _val is None:
            return None

        return ST_WrapDistance(utils.AnyStrToStr(_val))  # type: ignore

    @property
    def dist_r(self) -> Optional[ST_WrapDistance]:
        """distR（距离右边缘的距离）

        指定在此绘图对象在文档中显示时，该对象的右边缘与文档中任何后续文本之间必须保持的最小距离。

        距离以EMU（英制度量单位）为单位进行测量。

        [示例：考虑一个浮动的DrawingML对象，其右边缘与最近的文本之间必须有半英寸的填充。可以如下指定此设置：

        <wp:anchor … >
            …
            <wp:wrapThrough distR="457200" … />
        </wp:anchor>

        distR属性指定填充距离必须为457200 EMU或半英寸。示例结束]

        此属性的可能值由ST_WrapDistance简单类型（[§20.4.3.6]）定义。
        """
        _val = self.attrib.get('distR')

        if _val is None:
            return None

        return ST_WrapDistance(utils.AnyStrToStr(_val))  # type: ignore


class CT_WrapThrough(OxmlBaseElement):
    """20.4.2.18 wrapThrough (Through 环绕)

    wrapThrough (Through Wrapping)

    该元素指定文本应该围绕由子元素wrapPolygon定义的包围多边形包围此对象。当该元素指定一个包围多边形时，它应该允许文本在对象的最大左右范围内换行。
    """

    @property
    def wrap_polygon(self) -> CT_WrapPath:
        """20.4.2.16 wrapPolygon (环绕多边形)¶

        wrapPolygon (Wrapping Polygon)

        该元素指定了用于确定文档中指定对象周围文本可以环绕的范围的包裹多边形。该多边形由以下内容定义：

        - start元素定义包裹多边形的起点坐标
        - 两个或更多的lineTo元素定义包裹多边形的点

        如果子元素集合不能形成一个封闭的多边形（最后一个lineTo元素没有返回到start元素指定的位置），则需要推断一个额外的线段来封闭包裹多边形。

        【示例：考虑以下用于DrawingML对象的基本包裹多边形：

        <wp:wrapPolygon>
            <wp:start x="0" y="0" />
            <wp:lineTo x="0" y="100" />
            <wp:lineTo x="100" y="100" />
            <wp:lineTo x="100" y="0" />
            <wp:lineTo x="0" y="0" />
        </wp:wrapPolygon>

        wrapPolygon元素定义了对象的文本包裹多边形（在本例中为一个正方形的四个点）。示例结束】
        """
        return getattr(self, qn('wp:wrapPolygon'))

    @property
    def wrap_text(self) -> ST_WrapText:
        """wrapText（文本环绕位置）

        指定文本如何环绕对象的左侧和右侧。

        [示例：考虑一个浮动的DrawingML对象，其只允许文本环绕其左侧。可以如下指定此设置：

        <wp:anchor … >
            …
            <wp:wrapThrough wrapText="left" … />
        </wp:anchor>

        wrapText属性值为left，指定文本只能环绕对象的左侧。示例结束]

        此属性的可能值由ST_WrapText简单类型（[§20.4.3.7]）定义。
        """
        _val = self.attrib['wrapText']

        return ST_WrapText(utils.AnyStrToStr(_val))  # type: ignore

    @property
    def dist_l(self) -> Optional[ST_WrapDistance]:
        """distL（距离左边缘的距离）

        指定在此绘图对象在文档中显示时，该对象的左边缘与文档中任何后续文本之间必须保持的最小距离。

        距离以 EMU（英制度量单位）为单位进行测量。

        [示例：考虑一个浮动的DrawingML对象，其左边缘与最近的文本之间必须有半英寸的填充。可以如下指定此设置：


        <wp:anchor … >
            …
            <wp:wrapThrough distL="457200" … />
        </wp:anchor>

        distL属性指定填充距离必须为457200 EMU或半英寸。示例结束]

        此属性的可能值由ST_WrapDistance简单类型（[§20.4.3.6]）定义。
        """
        _val = self.attrib.get('distL')

        if _val is None:
            return None

        return ST_WrapDistance(utils.AnyStrToStr(_val))  # type: ignore

    @property
    def dist_r(self) -> Optional[ST_WrapDistance]:
        """distR（距离右边缘的距离）

        指定在此绘图对象在文档中显示时，该对象的右边缘与文档中任何后续文本之间必须保持的最小距离。

        距离以 EMU（英制度量单位）为单位进行测量。

        [示例：考虑一个浮动的DrawingML对象，其右边缘与最近的文本之间必须有半英寸的填充。可以如下指定此设置：

        <wp:anchor … >
            …
            <wp:wrapThrough distR="457200" … />
        </wp:anchor>

        distR属性指定填充距离必须为457200 EMU或半英寸。示例结束]

        此属性的可能值由ST_WrapDistance简单类型（[§20.4.3.6]）定义。
        """
        _val = self.attrib.get('distR')

        if _val is None:
            return None

        return ST_WrapDistance(utils.AnyStrToStr(_val))  # type: ignore


class CT_WrapTopBottom(OxmlBaseElement):
    """20.4.2.20 wrapTopAndBottom (顶部和底部包装)

    wrapTopAndBottom (Top and Bottom Wrapping)

    此元素指定文本应该围绕此对象的顶部和底部换行，但不围绕其左侧或右侧边缘。

    [示例：考虑一个使用顶部和底部换行的DrawingML对象，定义如下：

    <wp:anchor … >
        …
        <wp:wrapTopAndBottom />
    </wp:anchor>

    wrapTopAndBottom元素指定文本不能围绕此对象的任何一侧换行。示例结束]
    """

    @property
    def effect_extent(self) -> Optional[CT_EffectExtent]:
        """20.4.2.6 effectExtent (对象范围（包括效果）)¶

        effectExtent (Object Extents Including Effects)

        该元素指定了要添加到图像的每个边缘（顶部、底部、左侧、右侧）以补偿应用于DrawingML对象的任何绘制效果的附加范围。

        extent元素（[§20.4.2.7]）指定了实际DrawingML对象的大小；然而，可以应用改变其整体大小的效果于对象上[示例：反射和/或阴影效果。结束示例]。每个形状边缘的附加大小将存储在此元素上，并用于计算没有包装多边形的包装类型的适当包装以及内联对象的适当行高。
        """
        return getattr(self, qn('wp:effectExtent'))

    @property
    def dist_t(self) -> Optional[ST_WrapDistance]:
        """distT（顶边上的文本距离）

        指定在此图形对象在文档内容中显示时，该绘图对象的顶边与文档中任何后续文本之间必须保持的最小距离。

        距离以EMU（英制度量单位）为单位。

        [示例：考虑一个浮动的DrawingML对象，其顶边与最近的文本之间必须有半英寸的填充。设置如下所示：


        <wp:anchor … >
            …
            <wp:wrapThrough distR="457200" … />
        </wp:anchor>

        distT属性指定填充距离必须为457200 EMU或半英寸。示例结束]

        此属性的可能值由ST_WrapDistance简单类型（[§20.4.3.6]）定义。
        """
        _val = self.attrib.get('distT')

        if _val is None:
            return None

        return ST_WrapDistance(utils.AnyStrToStr(_val))  # type: ignore

    @property
    def dist_b(self) -> Optional[ST_WrapDistance]:
        """distB（底边上的文本距离）

        指定在此图形对象在文档内容中显示时，该绘图对象的底边与文档中任何后续文本之间必须保持的最小距离。

        距离以EMU（英制度量单位）为单位。

        [示例：考虑一个浮动的DrawingML对象，其底边与最近的文本之间必须有半英寸的填充。设置如下所示：

        <wp:anchor … >
            …
            <wp:wrapTopAndBottom distB="457200" … />
        </wp:anchor>

        distB属性指定填充距离必须为457200 EMU或半英寸。示例结束]

        此属性的可能值由ST_WrapDistance简单类型（[§20.4.3.6]）定义。
        """
        _val = self.attrib.get('distB')

        if _val is None:
            return None

        return ST_WrapDistance(utils.AnyStrToStr(_val))  # type: ignore


class EG_WrapType(OxmlBaseElement):
    """文本环绕类型"""

    wrap_tags = (
        qn('wp:wrapNone'),  # CT_WrapNone
        qn('wp:wrapSquare'),  # CT_WrapSquare
        qn('wp:wrapTight'),  # CT_WrapTight
        qn('wp:wrapThrough'),  # CT_WrapThrough
        qn('wp:wrapTopAndBottom'),  # CT_WrapTopBottom
    )


ST_PositionOffset = NewType('ST_PositionOffset', int)
"""20.4.3.3 ST_PositionOffset (绝对位置偏置值)¶

ST_PositionOffset (Absolute Position Offset Value)

这个简单类型表示一维距离，用于将对象从其存储在EMUs中的基本定位位置偏移。

[示例：考虑一个必须距离页面顶部一英寸，并且距离页面左边缘的一半英寸显示的DrawingML图片。此对象将被指定如下：

<wp:anchor … >
    <wp:positionH relativeFrom="page">
        <wp:posOffset>914400</wp:posOffset>
    </wp:positionH>
    <wp:positionV relativeFrom="page">
        <wp:posOffset>457200</wp:posOffset>
    </wp:positionV>
</wp:anchor>

posOffset元素指定了对象相对于页面左上角的绝对定位，单位为EMUs。示例结束]

这个简单类型的内容是对W3C XML Schema int数据类型的限制。

[Note: The W3C XML Schema definition of this simple type’s content model (ST_PositionOffset) is located in §A.4.4. end note]
"""


class ST_AlignH(ST_BaseEnumType):
    """20.4.3.1 ST_AlignH (相对水平对齐位置)¶

    ST_AlignH (Relative Horizontal Alignment Positions)

    这个简单类型包含了可能的设置，用于指定一个DrawingML对象在水平方向上相对于父元素定义的水平对齐基准的对齐方式。

    [示例：考虑一个在WordprocessingML文档中相对于页面边缘对齐的图片 - 水平方向上相对于页面的左侧，垂直方向上相对于页面的顶部。这个对齐方式可以如下指定：

    <wp:anchor … >
        <wp:positionH relativeFrom="page">
            <wp:align>left</wp:align>
        </wp:positionH>
        …
    </wp:anchor>

    值为left的align元素指定了对于父元素定义的水平定位（在本例中，相对于页面定位），图片必须对齐到页面的左边缘。示例结束]

    这个简单类型的内容是对W3C XML Schema token数据类型的限制。
    """

    Left = 'left'
    """left（左对齐）

    指定对象相对于水平对齐基准左对齐。

    [示例：相对于边距左对齐。示例结束]
    """

    Right = 'right'
    """right（右对齐）

    指定对象相对于水平对齐基准右对齐。

    [示例：相对于边距右对齐。示例结束]
    """

    Center = 'center'
    """center（居中对齐）

    指定对象相对于水平对齐基准居中对齐。

    [示例：在页面上居中对齐。示例结束]
    """

    Inside = 'inside'
    """inside（内部）

    指定对象在水平对齐基准内部。

    [示例：在外边距内部。示例结束]
    """

    Outside = 'outside'
    """outside（外部）

    指定对象在水平对齐基准外部。

    [示例：在左边距外部。示例结束]
    """


class ST_RelFromH(ST_BaseEnumType):
    """20.4.3.4 ST_RelFromH (水平相对位置)¶

    ST_RelFromH (Horizontal Relative Positioning)

    这个简单类型指定了对象的相对水平定位是基于哪个基准进行计算的可能值。

    [示例：考虑一个必须显示在页面底部中心的DrawingML图片。该对象可以按照以下方式指定：

    <wp:anchor … >
        <wp:positionH relativeFrom="page">
            <wp:align>center</wp:align>
        </wp:positionH>
        …
    </wp:anchor>

    relativeFrom属性指定了对象的水平定位是相对于页面的。示例结束]

    这个简单类型的内容是对W3C XML Schema token数据类型的限制。
    """

    Margin = 'margin'
    """margin (页面边距)

    指定水平定位相对于页面边距。
    """

    Page = 'page'
    """page (页面边缘)

    指定水平定位相对于页面边缘。
    """

    Column = 'column'
    """column (列)

    指定水平定位相对于包含其锚点的列的范围。
    """

    Character = 'character'
    """character (字符)

    指定水平定位相对于其所在内容的锚点位置。
    """

    LeftMargin = 'leftMargin'
    """leftMargin (左边距)

    指定水平定位相对于页面的左边距。
    """

    RightMargin = 'rightMargin'
    """rightMargin (右边距)

    指定水平定位相对于页面的右边距。
    """

    InsideMargin = 'insideMargin'
    """insideMargin (内边距)

    指定水平定位相对于当前页面的内边距（奇数页的左边距，偶数页的右边距）。
    """

    OutsideMargin = 'outsideMargin'
    """outsideMargin (外边距)

    指定水平定位相对于当前页面的外边距（奇数页的右边距，偶数页的左边距）。
    """


class CT_PosH(OxmlBaseElement):
    """20.4.2.10 positionH (水平定位)¶

    positionH (Horizontal Positioning)

    该元素指定了WordprocessingML文档中浮动DrawingML对象的水平定位。该定位由两部分组成：

    定位基准（Positioning Base） - 该元素上的relativeFrom属性指定了计算定位所需的文档部分。
    定位（Positioning） - 该元素的子元素（align或posOffset）指定了对象相对于基准的定位方式。
    【示例：考虑一个DrawingML图片，必须在打印页面的中心显示，并根据需要修改文本流。该对象的指定如下：

    <wp:anchor … >
        <wp:positionH relativeFrom="margin">
            <wp:align>center</wp:align>
        </wp:positionH>
        <wp:positionV relativeFrom="margin">
            <wp:align>center</wp:align>
        </wp:positionV>
    </wp:anchor>

    positionH元素指定了对象相对于页边距的水平定位，通过relativeFrom属性；并且通过align元素指定了相对于页边距的居中对齐。示例结束】

    xsd定义有问题?

    <xsd:complexType name="CT_PosH">
        <xsd:sequence>
        <xsd:choice minOccurs="1" maxOccurs="1">
            <xsd:element name="align" type="ST_AlignH" minOccurs="1" maxOccurs="1"/>
            <xsd:element name="posOffset" type="ST_PositionOffset" minOccurs="1" maxOccurs="1"/>
        </xsd:choice>
        </xsd:sequence>
        <xsd:attribute name="relativeFrom" type="ST_RelFromH" use="required"/>
    </xsd:complexType>
    """

    @property
    def aligment(self) -> ST_AlignH | int:
        _val = getattr(self, qn('wp:align'))

        if _val is not None:
            return ST_AlignH(_val.text)

        _val = getattr(self, qn('wp:posOffset'))
        return ST_PositionOffset(_val.text)

    @property
    def relative_from(self) -> ST_RelFromH:
        """relativeFrom（水平位置相对基准）

        指定计算该对象的相对水平定位时所使用的基准。

        【示例：考虑一个必须在页面底部中心显示的DrawingML图片。该对象的指定如下：

        <wp:anchor … >
            <wp:positionH relativeFrom="page">
                <wp:align>center</wp:align>
            </wp:positionH>
            …
        </wp:anchor>

        relativeFrom属性指定了对象相对于页面的水平定位。示例结束】

        该属性的可能值由ST_RelFromH简单类型（§20.4.3.4）定义。
        """
        _val = self.attrib['relativeFrom']

        return ST_RelFromH(_val)


class ST_AlignV(ST_BaseEnumType):
    """20.4.3.2 ST_AlignV (垂直对齐定义)¶

    ST_AlignV (Vertical Alignment Definition)

    这个简单类型包含了可能的设置，用于指定一个DrawingML对象相对于父元素定义的垂直对齐基准的垂直对齐方式。

    [示例：考虑一个在WordprocessingML文档中相对于页面边缘对齐的图片 - 水平对齐于页面的左侧，垂直对齐于页面的顶部。这个对齐方式可以如下指定：

    <wp:anchor … >
        <wp:positionV relativeFrom="page">
            <wp:align>top</wp:align>
        </wp:positionH>
        …
        </wp:anchor>
    </wp:anchor>

    值为top的align元素指定了对于父元素定义的垂直定位（在本例中，相对于页面的定位），图片必须对齐于页面的顶边。示例结束]

    这个简单类型的内容是对W3C XML Schema token数据类型的限制。
    """

    Top = 'top'
    """top (顶部)

    指定对象应该位于垂直对齐基准的顶部。

    [示例：页面的顶部。示例结束]
    """

    Bottom = 'bottom'
    """bottom (底部)

    指定对象应该位于垂直对齐基准的底部。

    [示例：页面的底部。示例结束]
    """

    Center = 'center'
    """center (居中对齐)

    指定对象应该相对于垂直对齐基准居中对齐。

    [示例：页面居中。示例结束]
    """

    Inside = 'inside'
    """inside (内部)

    指定对象应该位于水平对齐基准的内部。

    [示例：顶部边距内部。示例结束]


    """

    Outside = 'outside'
    """outside (外部)

    指定对象应该位于垂直对齐基准的外部。

    [示例：顶部边距外部。示例结束]
    """


class ST_RelFromV(ST_BaseEnumType):
    """20.4.3.5 ST_RelFromV (垂直相对定位)

    ST_RelFromV (Vertical Relative Positioning)

    这个简单类型指定了对象的相对垂直定位是基于哪个基准进行计算的可能值。

    [示例：考虑一个必须显示在页面底部中心的DrawingML图片。该对象可以按照以下方式指定：

    <wp:anchor … >
        <wp:positionV relativeFrom="page">
            <wp:align>bottom</wp:align>
        </wp:positionV>
        …
    </wp:anchor>

    relativeFrom属性指定了对象相对于页面的水平定位。示例结束]

    这个简单类型的内容是对W3C XML Schema token数据类型的限制。
    """

    Margin = 'margin'
    """margin (页面页边距)

    指定垂直定位相对于页面的页边距。
    """

    Page = 'page'
    """page (页面边缘)

    指定垂直定位相对于页面的边缘。
    """

    Paragraph = 'paragraph'
    """paragraph (段落)

    指定垂直定位相对于包含绘图锚点的段落。
    """

    Line = 'line'
    """line (行)

    指定垂直定位相对于包含锚点字符的行。
    """

    TopMargin = 'topMargin'
    """topMargin (顶部页边距)

    指定垂直定位相对于当前页面的顶部页边距。
    """

    BottomMargin = 'bottomMargin'
    """bottomMargin (底部页边距)

    指定垂直定位相对于当前页面的底部页边距。


    """

    InsideMargin = 'insideMargin'
    """insideMargin (内部页边距)

    指定垂直定位相对于当前页面的内部页边距。


    """

    OutsideMargin = 'outsideMargin'
    """outsideMargin (外部页边距)

    指定垂直定位相对于当前页面的外部页边距。
    """


class CT_PosV(OxmlBaseElement):
    """20.4.2.11 positionV (垂直定位)¶

    positionV (Vertical Positioning)

    该元素指定了WordprocessingML文档中浮动DrawingML对象的垂直定位。该定位分为两个部分：

    - 定位基准（Positioning Base） - 该元素上的relativeFrom属性指定了计算定位所需的文档部分。
    - 定位（Positioning） - 该元素的子元素（align或posOffset）指定了对象相对于该基准的定位方式。

    [示例：考虑一个DrawingML图片，必须在打印页面的中心显示，并根据需要修改文本流。可以按以下方式指定该对象：

    <wp:anchor … >
        <wp:positionH relativeFrom="margin">
            <wp:align>center</wp:align>
        </wp:positionH>
        <wp:positionV relativeFrom="margin">
            <wp:align>center</wp:align>
        </wp:positionV>
    </wp:anchor>

    positionV元素指定了对象相对于页边距的垂直定位，通过relativeFrom属性指定；并且通过align元素指定相对于页边距的对齐方式。示例结束]
    """

    @property
    def aligment(self) -> ST_AlignV | int:
        """对齐方式"""

        _val = getattr(self, qn('wp:align'))

        if _val is not None:
            return ST_AlignV(_val.text)

        _val = getattr(self, qn('wp:posOffset'))
        return ST_PositionOffset(_val.text)

    @property
    def relative_from(self) -> ST_RelFromH:
        """relativeFrom（水平位置相对基准）

        指定计算该对象的相对垂直定位时所使用的基准。

        [示例：考虑一个DrawingML图片，必须在页面边距的底部中心显示。可以按以下方式指定该对象：

        <wp:anchor … >
            …
            <wp:positionV relativeFrom="margin">
                <wp:align>bottom</wp:align>
            </wp:positionV>
        </wp:anchor>

        relativeFrom属性指定了对象相对于页边距的水平定位。示例结束]

        该属性的可能值由ST_RelFromV简单类型（[§20.4.3.5]）定义。
        """
        _val = self.attrib['relativeFrom']

        return ST_RelFromH(_val)


class CT_Anchor(EG_WrapType):
    """20.4.2.3 anchor (浮动 DrawingML 对象的锚点)

    anchor (Anchor for Floating DrawingML Object)

    此元素指定文档中位于此位置的DrawingML对象为浮动对象。在WordprocessingML文档中，绘图对象可以存在两种状态：

    - 内联 - 绘图对象与文本一起排列，并影响其所在行的行高和布局（类似于字符字形的大小）。
    - 浮动 - 绘图对象在文本中锚定，但可以相对于页面进行绝对定位。

    当此元素封装DrawingML对象的信息时，所有子元素都应指定此对象作为浮动对象在页面上的定位。

    [示例：考虑一个WordprocessingML文档，其中浮动DrawingML对象的锚点必须是段落中的第一个运行内容。该段落的内容应按以下方式指定：

    <w:p>
        <w:r>
            <w:drawing>
                <wp:anchor … >
                …
                </wp:anchor>
            </w:drawing>
        </w:r>
    </w:p>

    当锚点元素作为绘图元素的子元素出现时，指定该DrawingML对象必须根据其子元素的值作为浮动对象进行定位。示例结束]
    """

    @property
    def simple_pos(self) -> a_CT_Point2D:
        """20.4.2.13 simplePos (简单定位坐标)¶

        simplePos (Simple Positioning Coordinates)

        该元素指定了DrawingML对象相对于其页面左上角的坐标位置，当在锚点元素（§20.4.2.3）上指定了simplePos属性时。

        【示例：考虑一个浮动的DrawingML对象，必须使用简单定位将其定位在页面的左上角。可以如下指定此设置：

        <wp:anchor simplePos="true" … >
            <wp:simplePos x="0" y="0" />
            …
        </wp:anchor>

        simplePos属性的值为true，指定了DrawingML对象的当前位置必须由simplePos元素决定，因此放置在0,0位置。示例结束】
        """

        return getattr(self, qn('wp:simplePos'))

    @property
    def position_h(self) -> CT_PosH:
        """20.4.2.10 positionH (水平定位)¶

        positionH (Horizontal Positioning)

        该元素指定了WordprocessingML文档中浮动DrawingML对象的水平定位。该定位由两部分组成：

        定位基准（Positioning Base） - 该元素上的relativeFrom属性指定了计算定位所需的文档部分。
        定位（Positioning） - 该元素的子元素（align或posOffset）指定了对象相对于基准的定位方式。
        【示例：考虑一个DrawingML图片，必须在打印页面的中心显示，并根据需要修改文本流。该对象的指定如下：

        <wp:anchor … >
            <wp:positionH relativeFrom="margin">
                <wp:align>center</wp:align>
            </wp:positionH>
            <wp:positionV relativeFrom="margin">
                <wp:align>center</wp:align>
            </wp:positionV>
        </wp:anchor>

        positionH元素指定了对象相对于页边距的水平定位，通过relativeFrom属性；并且通过align元素指定了相对于页边距的居中对齐。示例结束】
        """
        return getattr(self, qn('wp:positionH'))

    @property
    def position_v(self) -> CT_PosV:
        """20.4.2.11 positionV (垂直定位)

        positionV (Vertical Positioning)

        该元素指定了WordprocessingML文档中浮动DrawingML对象的垂直定位。该定位分为两个部分：

        - 定位基准（Positioning Base） - 该元素上的relativeFrom属性指定了计算定位所需的文档部分。
        - 定位（Positioning） - 该元素的子元素（align或posOffset）指定了对象相对于该基准的定位方式。

        [示例：考虑一个DrawingML图片，必须在打印页面的中心显示，并根据需要修改文本流。可以按以下方式指定该对象：

        <wp:anchor … >
            <wp:positionH relativeFrom="margin">
                <wp:align>center</wp:align>
            </wp:positionH>
            <wp:positionV relativeFrom="margin">
                <wp:align>center</wp:align>
            </wp:positionV>
        </wp:anchor>

        positionV元素指定了对象相对于页边距的垂直定位，通过relativeFrom属性指定；并且通过align元素指定相对于页边距的对齐方式。示例结束]
        """
        return getattr(self, qn('wp:positionV'))

    @property
    def extent(self) -> a_CT_PositiveSize2D:
        """20.4.2.7 extent (绘图对象尺寸)¶

        extent (Drawing Object Size)

        该元素指定了文档中父级DrawingML对象的范围（即其最终的高度和宽度）。

        [示例：考虑一个在WordprocessingML文档中出现的DrawingML图片，其高度和宽度相等。该对象将被指定如下：

        <wp:anchor relativeHeight="10" allowOverlap="true">
            …
            <wp:extent cx="1828800" cy="1828800"/>
            …
        </wp:anchor>

        extent元素通过其属性指定了该对象的高度和宽度为1828800 EMUs（英制度量单位）。示例结束]
        """
        return getattr(self, qn('wp:extent'))

    @property
    def effect_extent(self) -> Optional[CT_EffectExtent]:
        """20.4.2.6 effectExtent (对象范围（包括效果）)¶

        effectExtent (Object Extents Including Effects)

        该元素指定了要添加到图像的每个边缘（顶部、底部、左侧、右侧）以补偿应用于DrawingML对象的任何绘制效果的附加范围。

        extent元素（[§20.4.2.7]）指定了实际DrawingML对象的大小；然而，可以应用改变其整体大小的效果于对象上[示例：反射和/或阴影效果。结束示例]。每个形状边缘的附加大小将存储在此元素上，并用于计算没有包装多边形的包装类型的适当包装以及内联对象的适当行高。
        """
        return getattr(self, qn('wp:effectExtent'), None)

    @property
    def wrap_type(
        self,
    ) -> CT_WrapNone | CT_WrapSquare | CT_WrapTight | CT_WrapThrough | CT_WrapTopBottom:
        """文字环绕类型

        - CT_WrapNone: 20.4.2.15 wrapNone (无文字环绕)
        - CT_WrapSquare: 20.4.2.17 wrapSquare (方形环绕)
        - CT_WrapTight: 20.4.2.19 wrapTight (Tight 环绕)
        - CT_WrapThrough: 20.4.2.18 wrapThrough (Through 环绕)
        - CT_WrapTopBottom: 20.4.2.20 wrapTopAndBottom (顶部和底部包装)

        """
        return self.choice_and_more(*self.wrap_tags)  # type: ignore

    @property
    def doc_pr(self) -> a_CT_NonVisualDrawingProps:
        """20.4.2.5 docPr (绘图对象非可视属性)¶

        docPr (Drawing Object Non-Visual Properties)

        该元素指定了父级 DrawingML 对象的非可见对象属性。这些属性是作为该元素的子元素指定的。

        [示例：考虑一个在 WordprocessingML 文档中定义的 DrawingML 对象，如下所示：

        <wp:inline>
            …
            <wp:docPr id="1" name="示例对象">
                <a:hlinkClick … />
                <a:hlinkHover … />
            </wp:docPr>
        </wp:inline>

        docPr 元素包含了该对象的一组常见非可见属性。结束示例]
        """
        return getattr(self, qn('wp:docPr'))

    @property
    def c_nv_graphic_frame_pr(self) -> Optional[a_CT_NonVisualGraphicFrameProperties]:
        """20.4.2.4 cNvGraphicFramePr (常见 DrawingML 非可视属性)¶

        cNvGraphicFramePr (Common DrawingML Non-Visual Properties)

        该元素指定了父 DrawingML 对象的常见非可视属性。这些属性被指定为该元素的子元素。

        【示例：考虑一个在 WordprocessingML 文档中定义的 DrawingML 对象，如下所示：

        <wp:inline>
            …
            <wp:cNvGraphicFramePr>
                <a:graphicFrameLocks … />
            </wp:cNvGraphicFramePr>
        </wp:inline>

        cNvGraphicFramePr 元素包含了一组由 DrawingML 定义的常见非可视属性。示例结束】
        """
        return getattr(self, qn('wp:cNvGraphicFramePr'))

    @property
    def graphic(self) -> a_CT_GraphicalObject:
        """20.4.2.31 graphicFrame (绘制对象容器)¶

        graphicFrame (Graphical object container)

        该元素指定了WordprocessingML中用于绘制(graphical)对象的容器。

        <xsd:element ref="a:graphic" minOccurs="1" maxOccurs="1"/>"""

        return getattr(self, qn('a:graphic'))

    @property
    def dist_t(self) -> Optional[ST_WrapDistance]:
        """distT（距离顶部文本的距离）

        指定在文档内容中显示该绘图对象时，该对象的顶部边缘与文档中任何后续文本之间必须保持的最小距离。

        距离以EMUs（英语度量单位）进行测量。

        如果此对象是内联对象（即具有内联父元素），则当将对象与文本一起显示时，此值不会产生任何效果，但是如果随后将对象更改为浮动对象，则此值可以得到保持和使用。如果作为子元素存在的包装元素[示例：wrapThrough或wrapSquare结束示例]也具有与文本的距离，则该值将被忽略。

        [示例：考虑一个浮动的DrawingML对象，其顶部边缘和最近文本之间必须有半英寸的填充。指定此设置如下所示：

        <wp:anchor distT="457200" … >
        …
        </wp:anchor>

        distT属性指定填充距离必须为457200 EMUs或四分之一英寸。结束示例]

        此属性的可能值由ST_WrapDistance简单类型（[§20.4.3.6]）定义。
        """
        _val = self.attrib.get('distT')

        if _val is None:
            return None

        return ST_WrapDistance(_val)  # type: ignore

    @property
    def dist_b(self) -> Optional[ST_WrapDistance]:
        """distB（距离底部文本的距离）

        指定在显示此绘图对象时，该对象的底部边缘与文档中任何后续文本之间应保持的最小距离。

        距离以EMU（英制度量单位）为单位进行测量。

        如果此对象是内联对象（即具有内联父元素），则在与文本一起显示对象时，此值不会产生任何效果，但如果对象随后更改为浮动，则可以保持和使用此值。如果作为子元素存在的包装元素[示例：wrapThrough或wrapSquare示例结束]也具有距离文本，则应忽略此值。

        [示例：考虑一个浮动的DrawingML对象，其底部边缘与最近的文本之间必须有半英寸的填充。可以如下指定此设置：

        <wp:anchor distB="457200" … >
            …
        </wp:anchor>

        distB属性指定填充距离必须为457200 EMU或半英寸。示例结束]

        此属性的可能值由ST_WrapDistance简单类型（[§20.4.3.6]）定义。
        """
        _val = self.attrib.get('distB')

        if _val is None:
            return None

        return ST_WrapDistance(_val)  # type: ignore

    @property
    def dist_l(self) -> Optional[ST_WrapDistance]:
        """distL（距离左侧文本的距离）

        指定在显示此绘图对象时，该对象的左边缘与文档中任何后续文本之间应保持的最小距离。

        距离以EMU（英制度量单位）为单位进行测量。

        如果此对象是内联对象（即具有内联父元素），则在与文本一起显示对象时，此值不会产生任何效果，但如果对象随后更改为浮动，则可以保持和使用此值。如果作为子元素存在的包装元素[示例：wrapThrough或wrapSquare示例结束]也具有距离文本，则应忽略此值。

        [示例：考虑一个浮动的DrawingML对象，其左边缘与最近的文本之间必须有四分之一英寸的填充。可以如下指定此设置：

        <wp:anchor distL="228600" … >
        …
        </wp:anchor>

        distL属性指定填充距离必须为228600 EMU或四分之一英寸。示例结束]

        此属性的可能值由ST_WrapDistance简单类型（[§20.4.3.6]）定义。
        """
        _val = self.attrib.get('distL')

        if _val is None:
            return None

        return ST_WrapDistance(_val)  # type: ignore

    @property
    def dist_r(self) -> Optional[ST_WrapDistance]:
        """distR（距离右侧文本的距离）

        指定在文档内容中显示该绘图对象时，该对象的右边缘与文档中任何后续文本之间必须保持的最小距离。

        距离以EMUs（英语度量单位）进行测量。

        如果此对象是内联对象（即具有内联父元素），则当将对象与文本一起显示时，此值不会产生任何效果，但是如果随后将对象更改为浮动对象，则此值可以得到保持和使用。如果作为子元素存在的包装元素[示例：wrapThrough或wrapSquare结束示例]也具有与文本的距离，则该值将被忽略。

        [示例：考虑一个浮动的DrawingML对象，其右边缘和最近文本之间必须有四分之一英寸的填充。指定此设置如下所示：


        <wp:anchor distR="228600" … >
        …
        </wp:anchor>
        distR属性指定填充距离必须为228600 EMUs或四分之一英寸。结束示例]

        此属性的可能值由ST_WrapDistance简单类型（[§20.4.3.6]）定义。
        """
        _val = self.attrib.get('distR')

        if _val is None:
            return None

        return ST_WrapDistance(_val)  # type: ignore

    @property
    def simplepos(self) -> Optional[bool]:
        """simplePos（页面定位）

        指定该对象应使用simplePos子元素（§20.4.2.13）中的定位信息进行定位。当指定了此定位时，通过将其左上角点放置在该元素指定的x-y坐标上，将对象定位在页面上。

        如果省略此元素，则即使存在simplePos元素中的简单定位信息，该对象也不会使用它。

        [示例：考虑一个浮动的DrawingML对象，必须使用简单定位在页面的左上角定位。可以如下指定此设置：

        <wp:anchor simplePos="true" … >
            <wp:simplePos x="0" y="0" />
            …
        </wp:anchor>

        simplePos属性的值为true，指定了DrawingML对象的当前位置必须由simplePos元素决定，因此放置在0,0处。示例结束]

        此属性的可能值由W3C XML Schema布尔数据类型定义。
        """
        _val = self.attrib.get('simplePos')

        if _val is None:
            return None

        return to_xsd_bool(_val)

    @property
    def relative_height(self) -> int:
        """relativeHeight（相对Z轴顺序位置）

        指定此文档中所有DrawingML对象的相对Z轴顺序。每个浮动的DrawingML对象都应具有一个Z轴顺序值，该值确定当任何两个对象相交时显示哪个对象。较高的值表示较高的Z轴顺序；较低的值表示较低的Z轴顺序。

        此属性仅指示与文档中具有相同behindDoc属性值的其他对象的Z轴顺序。所有behindDoc值为false的对象将显示在behindDoc值为true的元素上方。

        [示例：考虑以下两个浮动的DrawingML对象：

        <wp:anchor relativeHeight="5" … >
            …
        </wp:anchor>
        …
        <wp:anchor relativeHeight="8" … >
            …
        </wp:anchor>

        第二个对象的relativeHeight属性为8，指定第二个DrawingML对象必须具有比第一个对象更高的Z轴顺序，并且在两者重叠时显示。结束示例]

        此属性的可能值由W3C XML Schema unsignedInt数据类型定义。
        """
        _val = self.attrib['relativeHeight']

        return int(_val)

    @property
    def behind_doc(self) -> bool:
        """behindDoc（显示在文档文字后面）

        指定当文档显示时，此浮动的DrawingML对象是否显示在文档文字的后面。当一个DrawingML对象显示在WordprocessingML文档中时，该对象可以与文档中的文字相交。该属性确定在重叠情况下文本或对象的呈现顺序。

        [示例：考虑一个浮动的DrawingML对象，它必须显示在文档内容中与其相交的任何文字之上。应设置如下内容：

        <wp:anchor behindDoc="false" … >
            …
        </wp:anchor>

        behindDoc属性的值为false，指定该DrawingML对象在文档中显示时显示在文本的上方。结束示例]

        此属性的可能值由W3C XML Schema布尔数据类型定义。
        """
        _val = self.attrib['behindDoc']

        return to_xsd_bool(_val)

    @property
    def locked(self) -> bool:
        """locked（锁定锚点）

        指定在应用程序编辑此文档的内容时，此对象的锚点位置不得在运行时修改。[指导：应用程序可能具有根据用户交互重新定位DrawingML对象锚点的自动行为，例如根据需要将其从一页移动到另一页。此元素必须告诉应用程序不执行任何此类行为。结束指导]

        [示例：考虑一个浮动的DrawingML对象，必须将其锚点锁定在当前位置。可以如下指定此设置：

        <wp:anchor locked="true" … >
        …
        </wp:anchor>

        locked属性的值为true，指定了DrawingML对象的当前锚点位置不能被编辑此内容的应用程序更改。结束示例]

        此属性的可能值由W3C XML Schema布尔数据类型定义。
        """
        _val = self.attrib['locked']

        return to_xsd_bool(_val)

    @property
    def layout_in_cell(self) -> bool:
        """layoutInCell（单元格布局）

        指定浮动的DrawingML对象是否显示。当一个DrawingML对象在WordprocessingML文档中显示时，该对象可以被隐藏（即存在但不可见）。此属性应确定对象是被渲染还是被隐藏。[注意：应用程序可以具有允许查看该对象的设置。结尾注意]

        指定当其锚点位于表格单元格中，并且指定的位置导致与文档中显示的表格单元格相交时，此DrawingML对象的行为。其行为如下：

        - 当此属性的值为true时，对象将被定位在现有单元格内，使得单元格根据需要调整大小。这意味着所有定位都相对于单元格，而不是表格出现的行。
        - 当此属性的值为false时，对象将按指定位置定位，但表格将根据需要调整大小和/或在文档中重新定位以容纳对象。这意味着所有定位都相对于表格出现的行，而不是锚点所在的单元格。
        """
        _val = self.attrib['layoutInCell']

        return to_xsd_bool(_val)

    @property
    def hidden(self) -> Optional[bool]:
        """hidden（隐藏）

        指定浮动的DrawingML对象是否显示。当一个DrawingML对象在WordprocessingML文档中显示时，该对象可以被隐藏（即存在但不可见）。此属性应确定对象是被渲染还是被隐藏。[注意：应用程序可以具有允许查看该对象的设置。结尾注意]

        如果省略此属性，则父DrawingML对象将被显示（即不隐藏）。

        [示例：考虑一个必须在文档内容中隐藏的浮动DrawingML对象。此设置将如下指定：


        <wp:anchor hidden="true" … >
        …
        </wp:anchor>

        hidden属性的值为true，表示当文档显示时，DrawingML对象被隐藏而不显示。结束示例]

        此属性的可能值由W3C XML Schema布尔数据类型定义。
        """
        _val = self.attrib.get('hidden')

        if _val is None:
            return None

        return to_xsd_bool(_val)

    @property
    def allow_overlap(self) -> bool:
        """allowOverlap（允许重叠）

        指定显示时与另一DrawingML对象相交的DrawingML对象是否允许重叠另一对象的内容。如果一个DrawingML对象不允许与其他DrawingML对象重叠，那么在显示时必须根据需要重新定位以避免重叠。

        [示例：考虑一个文档中有两个DrawingML对象，允许彼此重叠。在每个对象的锚定标记内部，应指定如下内容：


        <wp:anchor allowOverlap="true" … >
        …
        </wp:anchor>

        allowOverlap属性的值为true，指定此对象在文档中显示时必须允许与其他对象重叠。结束示例]

        此属性的可能值由W3C XML Schema布尔数据类型定义。
        """
        _val = self.attrib['allowOverlap']

        return to_xsd_bool(_val)


class CT_TxbxContent(OxmlBaseElement):
    """20.4.2.38 txbxContent (富文本框内容容器)

    txbxContent (Rich Text Box Content Container)

    该元素指定其内容应为任何丰富的WordprocessingML内容，并且此内容是使用DrawingML语法定义的绘图对象的丰富内容。

    如果该元素的内容之一包含以下任何内容，则应将文档视为不符合规范：

    - 引用其他WordprocessingML文档故事（注释、脚注、尾注）
    - 矢量标记语言（VML）
    - 附加的txbxContent元素（作为嵌套DrawingML对象的一部分）

    <xsd:complexType name="CT_TxbxContent">
        <xsd:group ref="w:EG_BlockLevelElts" minOccurs="1" maxOccurs="unbounded"/>
    </xsd:complexType>
    """

    @property
    def block_level_elts(self):
        """该子元素是wml中的一个联合列表类型..."""

        from ecma376_office.oxml.wml.main import EG_BlockLevelElts

        return self.choice_and_more(*EG_BlockLevelElts.block_level_elts_choice_tags)

    @property
    def bookmarkStart(self):

        ele: Optional[w_CT_Bookmark] = getattr(self, qn('w:bookmarkStart'), None)

        return ele

    @property
    def bookmarkEnd(self):

        ele: Optional[w_CT_MarkupRange] = getattr(self, qn('w:bookmarkEnd'), None)

        return ele

    @property
    def moveFromRangeStart(self):

        ele: Optional[w_CT_MoveBookmark] = getattr(self, qn('w:moveFromRangeStart'), None)

        return ele

    @property
    def moveFromRangeEnd(self):

        ele: Optional[w_CT_MarkupRange] = getattr(self, qn('w:moveFromRangeEnd'), None)

        return ele

    @property
    def moveToRangeStart(self):

        ele: Optional[w_CT_MoveBookmark] = getattr(self, qn('w:moveToRangeStart'), None)

        return ele

    @property
    def moveToRangeEnd(self):

        ele: Optional[w_CT_MarkupRange] = getattr(self, qn('w:moveToRangeEnd'), None)

        return ele

    @property
    def commentRangeStart(self):

        ele: Optional[w_CT_MarkupRange] = getattr(self, qn('w:commentRangeStart'), None)

        return ele

    @property
    def commentRangeEnd(self):

        ele: Optional[w_CT_MarkupRange] = getattr(self, qn('w:commentRangeEnd'), None)

        return ele

    @property
    def customXmlInsRangeStart(self):

        ele: Optional[w_CT_TrackChange] = getattr(self, qn('w:customXmlInsRangeStart'), None)

        return ele

    @property
    def customXmlInsRangeEnd(self):

        ele: Optional[w_CT_Markup] = getattr(self, qn('w:customXmlInsRangeEnd'), None)

        return ele

    @property
    def customXmlDelRangeStart(self):

        ele: Optional[w_CT_TrackChange] = getattr(self, qn('w:customXmlDelRangeStart'), None)

        return ele

    @property
    def customXmlDelRangeEnd(self):

        ele: Optional[w_CT_Markup] = getattr(self, qn('w:customXmlDelRangeEnd'), None)

        return ele

    @property
    def customXmlMoveFromRangeStart(self):

        ele: Optional[w_CT_TrackChange] = getattr(self, qn('w:customXmlMoveFromRangeStart'), None)

        return ele

    @property
    def customXmlMoveFromRangeEnd(self):

        ele: Optional[w_CT_Markup] = getattr(self, qn('w:customXmlMoveFromRangeEnd'), None)

        return ele

    @property
    def customXmlMoveToRangeStart(self):

        ele: Optional[w_CT_TrackChange] = getattr(self, qn('w:customXmlMoveToRangeStart'), None)

        return ele

    @property
    def customXmlMoveToRangeEnd(self):

        ele: Optional[w_CT_Markup] = getattr(self, qn('w:customXmlMoveToRangeEnd'), None)

        return ele

    @property
    def oMathPara(self):

        ele: Optional[w_m_CT_OMathPara] = getattr(self, qn('m:oMathPara'), None)

        return ele

    @property
    def oMath(self):

        ele: Optional[w_m_CT_OMath] = getattr(self, qn('m:oMath'), None)

        return ele

    @property
    def proofErr(self):

        ele: Optional[w_CT_ProofErr] = getattr(self, qn('w:proofErr'), None)

        return ele

    @property
    def permStart(self):

        ele: Optional[w_CT_PermStart] = getattr(self, qn('w:permStart'), None)

        return ele

    @property
    def permEnd(self):

        ele: Optional[w_CT_Perm] = getattr(self, qn('w:permEnd'), None)

        return ele

    @property
    def ins(self):

        ele: Optional[w_CT_RunTrackChange] = getattr(self, qn('w:ins'), None)

        return ele

    @property
    def delete(self):

        ele: Optional[w_CT_RunTrackChange] = getattr(self, qn('w:del'), None)

        return ele

    @property
    def moveFrom(self):

        ele: Optional[w_CT_RunTrackChange] = getattr(self, qn('w:moveFrom'), None)

        return ele

    @property
    def moveTo(self):

        ele: Optional[w_CT_RunTrackChange] = getattr(self, qn('w:moveTo'), None)

        return ele

    @property
    def customXml(self):

        ele: Optional[w_CT_CustomXmlBlock] = getattr(self, qn('w:customXml'), None)

        return ele

    @property
    def sdt(self):

        ele: Optional[w_CT_SdtBlock] = getattr(self, qn('w:sdt'), None)

        return ele

    @property
    def p_lst(self):

        ele: Optional[w_CT_P] = self.findall(qn('w:p'))  # type: ignore

        return ele

    @property
    def tbl_lst(self):

        ele: Optional[w_CT_P] = self.findall(qn('w:tbl'))  # type: ignore

        return ele

    @property
    def altChunk(self):

        ele: Optional[w_CT_AltChunk] = self.findall(qn('w:altChunk'))  # type: ignore

        return ele


class CT_TextboxInfo(OxmlBaseElement):
    """20.4.2.37 txbx (形状的文字内容)

    txbx (Textual contents of shape)

    这个元素指定了一个形状的文本内容，这个形状是同一个文本框故事(text box story)中第一个形状的系列。这个元素应该仅出现在引用同一个文本框故事的一系列CT_WordprocessingShape元素中的第一个CT_WordprocessingShape元素中。这个元素应该只出现在引用同一个文本框故事的一系列CT_WordprocessingShape元素中的第一个CT_WordprocessingShape元素中。

    """

    @property
    def txbx_content(self) -> CT_TxbxContent:
        """20.4.2.38 txbxContent (富文本框内容容器)

        txbxContent (Rich Text Box Content Container)

        该元素指定其内容应为任何丰富的WordprocessingML内容，并且此内容是使用DrawingML语法定义的绘图对象的丰富内容。

        如果该元素的内容之一包含以下任何内容，则应将文档视为不符合规范：

        - 引用其他WordprocessingML文档故事（注释、脚注、尾注）
        - 矢量标记语言（VML）
        - 附加的txbxContent元素（作为嵌套DrawingML对象的一部分）
        """
        return getattr(self, qn('wp:txbxContent'))

    @property
    def ext_lst(self) -> Optional[a_CT_OfficeArtExtensionList]:
        return getattr(self, qn('wp:extLst'))

    @property
    def id(self) -> int:
        """id（标识）

        指定了由txbx元素开始的文本框故事的标识。这个值应该在文档中对于每个txbx元素是唯一的。

        这个属性的可能取值由W3C XML Schema的unsignedShort数据类型定义。
        """
        _val = self.attrib.get('id', '0')

        return int(_val)  # type: ignore


class CT_LinkedTextboxInformation(OxmlBaseElement):
    """20.4.2.34 linkedTxbx (形状的文字内容)¶

    linkedTxbx (Textual contents of shape)

    此元素指定形状的文本内容，该形状不是同一文本框故事的一系列形状中的第一个形状。
    """

    @property
    def ext_lst(self) -> Optional[a_CT_OfficeArtExtensionList]:
        return getattr(self, qn('wp:extLst'))

    @property
    def id(self) -> int:
        """id (ID)

        指定由txbx元素开始的文本框故事的标识。该值对于每个txbx元素在文档中应是唯一的。

        该属性的可能值由W3C XML Schema中的unsignedShort数据类型定义。
        """
        _val = self.attrib['id']

        return int(_val)  # type: ignore

    @property
    def seq(self) -> int:
        """seq (序列索引)

        指定所属形状在给定文本框故事中的位置。

        该属性的可能值由W3C XML Schema中的unsignedShort数据类型定义。
        """
        _val = self.attrib['seq']

        return int(_val)  # type: ignore


class CT_WordprocessingShape(OxmlBaseElement):
    """20.4.2.42 wsp (WordprocessingML 形状)¶

    wsp (WordprocessingML Shape)

    这个元素在WordprocessingML中指定了一个形状。

     <xsd:complexType name="CT_WordprocessingShape">
        <xsd:sequence minOccurs="1" maxOccurs="1">
            <xsd:element name="cNvPr" type="a:CT_NonVisualDrawingProps" minOccurs="0" maxOccurs="1"/>
            <xsd:choice minOccurs="1" maxOccurs="1">
                <xsd:element name="cNvSpPr" type="a:CT_NonVisualDrawingShapeProps" minOccurs="1"
                maxOccurs="1"/>
                <xsd:element name="cNvCnPr" type="a:CT_NonVisualConnectorProperties" minOccurs="1"
                maxOccurs="1"/>
            </xsd:choice>
            <xsd:element name="spPr" type="a:CT_ShapeProperties" minOccurs="1" maxOccurs="1"/>
            <xsd:element name="style" type="a:CT_ShapeStyle" minOccurs="0" maxOccurs="1"/>
            <xsd:element name="extLst" type="a:CT_OfficeArtExtensionList" minOccurs="0" maxOccurs="1"/>
            <xsd:choice minOccurs="0" maxOccurs="1">
                <xsd:element name="txbx" type="CT_TextboxInfo" minOccurs="1" maxOccurs="1"/>
                <xsd:element name="linkedTxbx" type="CT_LinkedTextboxInformation" minOccurs="1"
                maxOccurs="1"/>
            </xsd:choice>
            <xsd:element name="bodyPr" type="a:CT_TextBodyProperties" minOccurs="1" maxOccurs="1"/>
        </xsd:sequence>
        <xsd:attribute name="normalEastAsianFlow" type="xsd:boolean" use="optional" default="false"/>
    </xsd:complexType>
    """

    @property
    def c_nv_pr(self) -> Optional[a_CT_NonVisualDrawingProps]:
        """20.4.2.27 cNvPr (非可视绘图属性)¶

        cNvPr (Non-Visual Drawing Properties)

        该元素指定了非可视画布属性。这允许存储不影响图片外观的附加信息。

        [示例：考虑以下WordprocessingDrawingML：


        <wsp>
        …
        <cNvPr id="4" name="Lilly_by_Lisher.jpg"/>
        …
        </wsp>

        示例结束]
        """
        return getattr(self, qn('wp:cNvPr'), None)

    @property
    def c_nv_sp_pr(
        self,
    ) -> a_CT_NonVisualDrawingShapeProps | a_CT_NonVisualConnectorProperties:
        """形状的非可视属性

        - 形状的属性 CT_NonVisualDrawingShapeProps

            20.4.2.28 cNvSpPr (形状的非可视绘图属性)

        - 连接线的属性 CT_NonVisualConnectorProperties

            20.4.2.23 cNvCnPr (非可视连接器形状绘图属性)
        """
        tags = (
            qn('wp:cNvSpPr'),  # a_CT_NonVisualDrawingShapeProps
            qn('wp:cNvCnPr'),  # a_CT_NonVisualConnectorProperties
        )

        return self.choice_require_one_child(*tags)  # type: ignore

    @property
    def sp_pr(self) -> a_CT_ShapeProperties:
        """20.4.2.35 spPr (形状属性)¶

        spPr (Shape Properties)

        这个元素指定可以应用到形状的可视形状属性。这些属性包括形状填充、轮廓、几何结构、效果和三维方向。
        """
        return getattr(self, qn('wp:spPr'))

    @property
    def style(self) -> a_CT_ShapeStyle:
        """20.4.2.36 style (形状样式)¶

        style (Shape Style)

        这个元素指定了形状的样式信息。它用于根据主题的样式矩阵所定义的预设样式来定义形状的外观。
        """

        return getattr(self, qn('wp:style'))

    @property
    def ext_lst(self) -> Optional[a_CT_OfficeArtExtensionList]:
        return getattr(self, qn('wp:extLst'))

    @property
    def txbx(
        self,
    ) -> Optional[CT_TextboxInfo | CT_LinkedTextboxInformation]:
        """文本框信息"""
        tags = (
            qn('wp:txbx'),  # CT_TextboxInfo
            qn('wp:linkedTxbx'),  # CT_LinkedTextboxInformation
        )

        return self.choice_one_child(*tags)  # type: ignore

    @property
    def body_pr(self) -> a_CT_TextBodyProperties:
        """20.4.2.22 bodyPr (正文格式)¶

        bodyPr (Body Properties)

        该元素定义了形状内文本主体的属性。
        """
        return getattr(self, qn('wp:bodyPr'))

    @property
    def normal_east_asian_flow(self) -> bool:
        """normalEastAsianFlow（东亚文本流）

        指定形状的文本内容的文字流是否应忽略bodyPr元素的vert属性指定的文字流值。

        如果此属性设置为TRUE，则文字流遵循ST_TextDirection（[§17.18.93]）的值“tbV”所指定的方式。

        此属性的可能取值由W3C XML Schema布尔数据类型定义。
        """
        _val = self.attrib.get('normalEastAsianFlow', 'false')

        return to_xsd_bool(_val)


class CT_GraphicFrame(OxmlBaseElement):
    """20.4.2.31 graphicFrame (绘制对象容器)¶

    graphicFrame (Graphical object container)

    该元素指定了WordprocessingML中用于绘制(graphical)对象的容器。

    [Note: The W3C XML Schema definition of this element’s content model (CT_GraphicFrame) is located in §A.4.5. end note]
    """

    @property
    def c_nv_pr(self) -> a_CT_NonVisualDrawingProps:
        """20.4.2.27 cNvPr (非可视绘图属性)¶

        cNvPr (Non-Visual Drawing Properties)

        该元素指定了非可视画布属性。这允许存储不影响图片外观的附加信息。

        [示例：考虑以下WordprocessingDrawingML：

        <wsp>
            …
            <cNvPr id="4" name="Lilly_by_Lisher.jpg"/>
            …
        </wsp>

        示例结束]
        """
        return getattr(self, qn('wp:cNvPr'))

    @property
    def c_nv_fr_pr(self) -> a_CT_NonVisualGraphicFrameProperties:
        """20.4.2.25 cNvFrPr (非可视图形框架绘图属性)¶

        cNvFrPr (Non-Visual Graphic Frame Drawing Properties)

        该元素指定了图形框的非可视绘制属性。这些非可视属性是生成应用程序在渲染时会使用的属性。
        """
        return getattr(self, qn('wp:cNvFrPr'))

    @property
    def xfrm(self) -> Optional[a_CT_Transform2D]:
        """20.4.2.43 xfrm (图形框架的2D变换)¶

        xfrm (2D Transform for Graphic Frames)

        这个元素指定了一个图形框架的二维变换。
        """
        return getattr(self, qn('wp:xfrm'), None)

    @property
    def graphic(self) -> a_CT_GraphicalObject:
        """图形对象

        20.1.2.2.16 graphic (Graphic Object)

        该元素指定单个图形对象的存在。 当文档作者希望保留某种图形对象时，应该引用此元素。 该图形对象的规范完全由文档作者提供并在 graphicData 子元素中引用。
        """
        """<xsd:element ref="a:graphic" minOccurs="1" maxOccurs="1"/>"""

        return getattr(self, qn('a:graphic'))

    @property
    def ext_lst(self) -> Optional[a_CT_OfficeArtExtensionList]:
        return getattr(self, qn('wp:extLst'))


class CT_WordprocessingContentPartNonVisual(OxmlBaseElement):
    @property
    def c_nv_pr(self) -> Optional[a_CT_NonVisualDrawingProps]:
        """20.4.2.27 cNvPr (非可视绘图属性)¶

        cNvPr (Non-Visual Drawing Properties)

        该元素指定了非可视画布属性。这允许存储不影响图片外观的附加信息。

        [示例：考虑以下WordprocessingDrawingML：

        <wsp>
            …
            <cNvPr id="4" name="Lilly_by_Lisher.jpg"/>
            …
        </wsp>

        示例结束]
        """
        return getattr(self, qn('wp:cNvPr'), None)

    @property
    def c_nv_contentpart_pr(self) -> Optional[a_CT_NonVisualContentPartProperties]:
        """20.4.2.24 cNvContentPartPr (非视觉内容部件绘图属性)¶

        cNvContentPartPr (Non-Visual Content Part Drawing Properties)

        该元素指定内容部分的非可视绘图属性。这允许存储不影响内容部分外观的附加信息。
        """

        return getattr(self, qn('wp:cNvContentPartPr'), None)


class CT_WordprocessingContentPart(OxmlBaseElement):
    """20.4.2.29 contentPart (内容部件)¶

    contentPart (Content Part)

    该元素指定了对由ECMA-376未定义的格式的XML内容的引用。[注：此部分允许原生使用其他常用的交换格式，例如：

    - MathML（http://www.w3.org/TR/MathML2/）
    - SMIL（http://www.w3.org/TR/REC-smil/）
    - SVG（http://www.w3.org/TR/SVG11/）

    注解结束]

    此元素指定的显式关系的关系类型应为http://purl.oclc.org/ooxml/officeDocument/relationships/customXml，并且具有TargetMode属性值为Internal。如果应用程序无法处理目标部分指定的内容类型的内容，则应继续处理文件。如果可能，还应提供一些指示未知内容未导入的指示。
    """

    @property
    def c_nv_contentpart_pr(self) -> Optional[a_CT_NonVisualContentPartProperties]:
        """20.4.2.27 cNvPr (非可视绘图属性)¶

        cNvPr (Non-Visual Drawing Properties)

        该元素指定了非可视画布属性。这允许存储不影响图片外观的附加信息。

        [示例：考虑以下WordprocessingDrawingML：

        <wsp>
            …
            <cNvPr id="4" name="Lilly_by_Lisher.jpg"/>
            …
        </wsp>

        示例结束]
        """
        return getattr(self, qn('wp:cNvPr'), None)

    @property
    def xfrm(self) -> Optional[a_CT_Transform2D]:
        """20.4.2.43 xfrm (图形框架的2D变换)¶

        xfrm (2D Transform for Graphic Frames)

        这个元素指定了一个图形框架的二维变换。
        """
        return getattr(self, qn('wp:xfrm'), None)

    @property
    def ext_lst(self) -> Optional[a_CT_OfficeArtExtensionList]:
        return getattr(self, qn('wp:extLst'))

    @property
    def bw_mode(self) -> Optional[a_ST_BlackWhiteMode]:
        """bwMode（黑白模式）

        指定如何解释内容部分中包含的颜色信息，以实现内容部分的彩色、黑白或灰度渲染。此属性仅指定应用于内容部分的渲染模式；它不影响实际颜色信息的持久化方式。

        此属性的可能值由ST_BlackWhiteMode简单类型（§20.1.10.10）定义。
        """
        _val = self.attrib.get('bwMode')

        if _val is None:
            return None

        return a_ST_BlackWhiteMode(_val)

    @property
    def r_id(self) -> r_ST_RelationshipId:
        """id（与部分的关系）

        命名空间：http://purl.oclc.org/ooxml/officeDocument/relationships

        指定与特定部件的关系ID。

        指定的关系应与父元素所需的关系类型匹配：

        - http://purl.oclc.org/ooxml/officeDocument/customXml 用于 contentPart 元素
        - http://purl.oclc.org/ooxml/officeDocument/relationships/footer 用于 footerReference 元素
        - http://purl.oclc.org/ooxml/officeDocument/relationships/header 用于 headerReference 元素
        - http://purl.oclc.org/ooxml/officeDocument/relationships/font 用于 embedBold、embedBoldItalic、embedItalic 或 embedRegular 元素
        - http://purl.oclc.org/ooxml/officeDocument/relationships/printerSettings 用于 printerSettings 元素
        - http://purl.oclc.org/ooxml/officeDocument/relationships/hyperlink 用于 longDesc 或 hyperlink 元素

        [示例：考虑一个具有以下id属性的XML元素：

        <… r:id="rId10" />

        该标记指定了与关系ID rId1相关联的关系部分，其中包含了父XML元素的相应关系信息。示例结束]
        """
        _val = self.attrib[qn('r:id')]

        return r_ST_RelationshipId(str(_val))


class CT_WordprocessingGroup(OxmlBaseElement):
    """20.4.2.39 wgp (WordprocessingML 形状组合)¶

    wgp (WordprocessingML Shape Group)

    此元素指定 WordprocessingML 中的形状组合。

    20.4.2.32 grpSp (组合形状)¶

    grpSp (Group Shape)

    该元素指定了一个表示多个形状组合在一起的组合形状。这个形状应该被视为一个普通形状，但不同于由单个几何描述的形状，它由包含在其中的所有形状几何组成。在组合形状中，组成组合的每个形状都像通常一样被指定。然而，组合元素的理念是可以同时应用于多个形状的单个变换。
    """

    @property
    def c_nv_pr(self) -> Optional[a_CT_NonVisualDrawingProps]:
        """20.4.2.27 cNvPr (非可视绘图属性)¶

        cNvPr (Non-Visual Drawing Properties)

        该元素指定了非可视画布属性。这允许存储不影响图片外观的附加信息。

        [示例：考虑以下WordprocessingDrawingML：

        <wsp>
            …
            <cNvPr id="4" name="Lilly_by_Lisher.jpg"/>
            …
        </wsp>

        示例结束]
        """
        return getattr(self, qn('wp:cNvPr'), None)

    @property
    def c_nv_grp_sp_pr(self) -> Optional[a_CT_NonVisualGroupDrawingShapeProps]:
        """20.4.2.26 cNvGrpSpPr (非可视组合形状绘图属性)¶

        cNvGrpSpPr (Non-Visual Group Shape Drawing Properties)

        该元素指定了组合形状的非可视绘图属性。这些非可视属性是生成应用程序在渲染时会使用的属性。
        """
        return getattr(self, qn('wp:cNvGrpSpPr'), None)

    @property
    def grp_sp_pr(self) -> a_CT_GroupShapeProperties:
        """20.4.2.33 grpSpPr (组合形状属性)¶

        grpSpPr (Group Shape Properties)

        该元素指定了在相应组中的所有形状之间共享的属性。如果组形状属性和各个形状属性之间存在冲突，则应以各个形状属性为优先。
        """

        return getattr(self, qn('wp:grpSpPr'))

    @property
    def shapes(
        self,
    ) -> list[
        CT_WordprocessingShape | CT_WordprocessingGroup | CT_GraphicFrame | wpct_CT_Picture | CT_WordprocessingContentPart
    ]:
        """
        形状合集

        <xsd:choice minOccurs="0" maxOccurs="unbounded">
            <xsd:element ref="wsp"/>
            <xsd:element name="grpSp" type="CT_WordprocessingGroup"/>
            <xsd:element name="graphicFrame" type="CT_GraphicFrame"/>
            <xsd:element ref="dpct:pic"/>
            <xsd:element name="contentPart" type="CT_WordprocessingContentPart"/>
        </xsd:choice>
        """

        tags = (
            qn('wp:wsp'),  # CT_WordprocessingShape
            qn('wp:grpSp'),  # CT_WordprocessingGroup
            qn('wp:graphicFrame'),  # CT_GraphicFrame
            qn('dpct:pic'),  # wpct_CT_Picture
            qn('wp:contentPart'),  # CT_WordprocessingContentPart
        )

        return self.choice_and_more(*tags)  # type: ignore

    @property
    def ext_lst(self) -> Optional[a_CT_OfficeArtExtensionList]:
        return getattr(self, qn('wp:extLst'))


class CT_WordprocessingCanvas(OxmlBaseElement):
    """20.4.2.41 wpc (WordprocessingML Drawing Canvas)¶

    wpc (WordprocessingML Drawing Canvas)

    这个元素指定了WordprocessingML中的绘图画布。绘图画布是形状的逻辑分组。[注意：绘图画布通常用于批量操作中的形状分组。结束注意]

    [Note: The W3C XML Schema definition of this element’s content model (CT_ WordprocessingCanvas) is located in §A.4.5. end note]
    """

    @property
    def bg(self) -> Optional[a_CT_BackgroundFormatting]:
        """20.4.2.21 bg (背景格式)¶

        bg (Background Formatting)

        这个元素定义了可以应用于文档背景形状的格式。背景形状可以包含与普通形状在DrawingML中一样的格式选项。
        """
        return getattr(self, qn('wp:bg'), None)

    @property
    def whole(self) -> Optional[a_CT_WholeE2oFormatting]:
        """20.4.2.40 whole (整个E2O格式)¶

        whole (Whole E2O Formatting)

        适用于整个图表对象而非仅限于背景的格式设置包括线条和效果属性。
        """

        return getattr(self, qn('wp:whole'), None)

    def shapes(
        self,
    ) -> list[
        CT_WordprocessingShape | wpct_CT_Picture | CT_WordprocessingContentPart | CT_WordprocessingGroup | CT_GraphicFrame
    ]:
        """
        形状合集

        <xsd:choice minOccurs="0" maxOccurs="unbounded">
            <xsd:element ref="wsp"/>
            <xsd:element ref="dpct:pic"/>
            <xsd:element name="contentPart" type="CT_WordprocessingContentPart"/>
            <xsd:element ref="wgp"/>
            <xsd:element name="graphicFrame" type="CT_GraphicFrame"/>
        </xsd:choice>
        """

        tags = (
            qn('wp:wsp'),  # CT_WordprocessingShape
            qn('dpct:pic'),  # wpct_CT_Picture
            qn('wp:contentPart'),  # CT_WordprocessingContentPart
            qn('wp:wgp'),  # CT_WordprocessingGroup
            qn('wp:graphicFrame'),  # CT_GraphicFrame
        )

        return self.choice_and_more(*tags)  # type: ignore

    @property
    def ext_lst(self) -> Optional[a_CT_OfficeArtExtensionList]:
        return getattr(self, qn('wp:extLst'))


dml_wp_namespace = lookup.get_namespace(namespace_wp)
dml_wp_namespace[None] = OxmlBaseElement


dml_wp_namespace['wpc'] = CT_WordprocessingCanvas  # 根节点之一
dml_wp_namespace['wgp'] = CT_WordprocessingGroup  # 根节点之一
dml_wp_namespace['wsp'] = CT_WordprocessingShape  # 根节点之一
dml_wp_namespace['inline'] = CT_Inline  # 根节点之一
dml_wp_namespace['anchor'] = CT_Anchor  # 根节点之一、

dml_wp_namespace['extent'] = a_CT_PositiveSize2D
dml_wp_namespace['effectExtent'] = CT_EffectExtent

dml_wp_namespace['docPr'] = a_CT_NonVisualDrawingProps
dml_wp_namespace['cNvGraphicFramePr'] = a_CT_NonVisualGraphicFrameProperties

dml_wp_namespace['graphic'] = a_CT_GraphicalObject

dml_wp_namespace['start'] = a_CT_Point2D
dml_wp_namespace['lineTo'] = a_CT_Point2D

dml_wp_namespace['wrapPolygon'] = CT_WrapPath
dml_wp_namespace['wrapNone'] = CT_WrapNone
dml_wp_namespace['wrapSquare'] = CT_WrapSquare
dml_wp_namespace['wrapTight'] = CT_WrapTight
dml_wp_namespace['wrapThrough'] = CT_WrapThrough
dml_wp_namespace['wrapTopAndBottom'] = CT_WrapTopBottom

dml_wp_namespace['align'] = OxmlBaseElement  # ST_AlignH
dml_wp_namespace['posOffset'] = OxmlBaseElement  # ST_PositionOffset

dml_wp_namespace['simplePos'] = a_CT_Point2D
dml_wp_namespace['positionH'] = CT_PosH
dml_wp_namespace['positionV'] = CT_PosV
dml_wp_namespace['extent'] = a_CT_PositiveSize2D

dml_wp_namespace['txbxContent'] = CT_TxbxContent
dml_wp_namespace['extLst'] = a_CT_OfficeArtExtensionList

dml_wp_namespace['cNvPr'] = a_CT_NonVisualDrawingProps
dml_wp_namespace['cNvSpPr'] = a_CT_NonVisualDrawingShapeProps
dml_wp_namespace['cNvCnPr'] = a_CT_NonVisualConnectorProperties
dml_wp_namespace['cNvFrPr'] = a_CT_NonVisualGraphicFrameProperties
dml_wp_namespace['cNvContentPartPr'] = a_CT_NonVisualContentPartProperties
dml_wp_namespace['cNvGrpSpPr'] = a_CT_NonVisualGroupDrawingShapeProps

dml_wp_namespace['spPr'] = a_CT_ShapeProperties
dml_wp_namespace['grpSpPr'] = a_CT_GroupShapeProperties

dml_wp_namespace['grpSp'] = CT_WordprocessingGroup
dml_wp_namespace['graphicFrame'] = CT_GraphicFrame
dml_wp_namespace['contentPart'] = CT_WordprocessingContentPart

dml_wp_namespace['style'] = a_CT_ShapeStyle
dml_wp_namespace['txbx'] = CT_TextboxInfo
dml_wp_namespace['linkedTxbx'] = CT_LinkedTextboxInformation
dml_wp_namespace['bodyPr'] = a_CT_TextBodyProperties

dml_wp_namespace['xfrm'] = a_CT_Transform2D
dml_wp_namespace['bg'] = a_CT_BackgroundFormatting
dml_wp_namespace['whole'] = a_CT_WholeE2oFormatting
