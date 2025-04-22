"""
对应xsd: dml-chart.xsd

前缀: c

命名空间: http://purl.oclc.org/ooxml/drawingml/chart

<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:a="http://purl.oclc.org/ooxml/drawingml/main"
    xmlns:r="http://purl.oclc.org/ooxml/officeDocument/relationships"
    xmlns="http://purl.oclc.org/ooxml/drawingml/chart"
    xmlns:cdr="http://purl.oclc.org/ooxml/drawingml/chartDrawing"
    xmlns:s="http://purl.oclc.org/ooxml/officeDocument/sharedTypes"
    targetNamespace="http://purl.oclc.org/ooxml/drawingml/chart"
    elementFormDefault="qualified"
    attributeFormDefault="unqualified"
    blockDefault="#all">
    <xsd:import namespace="http://purl.oclc.org/ooxml/officeDocument/relationships"
        schemaLocation="shared-relationshipReference.xsd"/>
    <xsd:import namespace="http://purl.oclc.org/ooxml/drawingml/main"
        schemaLocation="dml-main.xsd"/>
    <xsd:import namespace="http://purl.oclc.org/ooxml/drawingml/chartDrawing"
        schemaLocation="dml-chartDrawing.xsd"/>
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
from ecma376_office.oxml.dml.chart_drawing import CT_Drawing as cdr_CT_Drawing
from ecma376_office.oxml.dml.main import CT_ColorMapping as a_CT_ColorMapping
from ecma376_office.oxml.dml.main import CT_ShapeProperties as a_CT_ShapeProperties
from ecma376_office.oxml.dml.main import CT_TextBody as a_CT_TextBody
from ecma376_office.oxml.exceptions import OxmlAttributeValidateError, OxmlElementValidateError
from ecma376_office.oxml.shared.common_simple_types import ST_PositiveUniversalMeasure as s_ST_PositiveUniversalMeasure
from ecma376_office.oxml.shared.common_simple_types import (
    to_ST_PositiveUniversalMeasure as to_s_ST_PositiveUniversalMeasure,
)
from ecma376_office.oxml.shared.relationship_reference import ST_RelationshipId as r_ST_RelationshipId
from ecma376_office.oxml.xsd_types import XSD_Token, to_xsd_bool, to_xsd_double, to_xsd_unsigned_int

logger = logging.getLogger(__name__)

# namespace_a = "http://purl.oclc.org/ooxml/drawingml/main"
namespace_a = 'http://schemas.openxmlformats.org/drawingml/2006/main'

# namespace_c = "http://purl.oclc.org/ooxml/drawingml/chart"
namespace_c = 'http://schemas.openxmlformats.org/drawingml/2006/chart'

# namespace_cp = "http://purl.oclc.org/ooxml/drawingml/chartDrawing"
namespace_cdr = 'http://schemas.openxmlformats.org/drawingml/2006/chartDrawing'

# namespace_r = "http://purl.oclc.org/ooxml/officeDocument/relationships"
namespace_r = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

# namespace_s = "http://purl.oclc.org/ooxml/officeDocument/sharedTypes"
namespace_s = 'http://schemas.openxmlformats.org/officeDocument/2006/sharedTypes'

logger = logging.getLogger(__name__)


ns_map = {
    'a': namespace_a,
    'c': namespace_c,  # 当前命名空间
    'r': namespace_r,
    'cdr': namespace_cdr,
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


class CT_Boolean(OxmlBaseElement):
    """布尔值

    21.2.2.1 applyToEnd (末尾应用)

    21.2.2.2 applyToFront (前面应用)

    21.2.2.3 applyToSides (侧面应用)

    21.2.2.6 auto (自动分类轴)

    21.2.2.7 autoTitleDeleted (自动标题已删除)

    21.2.2.8 autoUpdate (自动更新)

    21.2.2.19 bubble3D (3D气泡图)

    21.2.2.28 chartObject (图表对象)

    21.2.2.37 data (数据无法更改)

    21.2.2.38 date1904 (1904日期系统)

    21.2.2.40 delete (删除)

    21.2.2.43 dispEq (显示方程)

    21.2.2.44 dispRSqr (显示 R 平方值)

    21.2.2.72 formatting (格式)

    21.2.2.86 invertIfNegative (如果为负则反转)

    21.2.2.105 marker (显示标记)

    21.2.2.118 noEndCap (无端盖)

    21.2.2.119 noMultiLvlLbl (无多级标签)

    21.2.2.132 overlay (覆盖)

    21.2.2.146 plotVisOnly (绘图仅可见)

    21.2.2.155 rAngAx (直角坐标轴)

    21.2.2.159 roundedCorners (圆角)

    21.2.2.165 selection (选择保护)

    21.2.2.178 showBubbleSize (显示气泡大小)

    21.2.2.179 showCatName (显示类别名称)

    21.2.2.180 showDLblsOverMax (显示超过最大值的数据标签)

    21.2.2.181 showHorzBorder (显示水平边框)

    21.2.2.182 showKeys (显示图例键)

    21.2.2.183 showLeaderLines (显示引导线)

    21.2.2.184 showLegendKey (显示图例键)

    21.2.2.185 showNegBubbles (显示负气泡)

    21.2.2.186 showOutline (显示轮廓边框)

    21.2.2.187 showPercent (显示百分比)

    21.2.2.188 showSerName (显示系列名称)

    21.2.2.189 showVal (显示值)

    21.2.2.190 showVertBorder (显示垂直边框)

    21.2.2.194 smooth (平滑)

    21.2.2.219 userInterface (用户接口)

    21.2.2.227 varyColors (按点改变颜色)

    21.2.2.230 wireframe (线框)
    """

    @property
    def val(self):
        val = self.attrib.get('val')

        return to_xsd_bool(val, none=True)


class CT_Double(OxmlBaseElement):
    """21.2.2.12 backward (Backward)

    21.2.2.34 crossesAt (穿越值)

    21.2.2.36 custUnit (定制显示单元)

    21.2.2.73 forward (Forward)

    21.2.2.78 h (高度)

    21.2.2.85 intercept (截距)

    21.2.2.107 max (最大值)

    21.2.2.108 min (最小值)

    21.2.2.195 splitPos (分割位置)

    21.2.2.225 val (误差条值)

    21.2.2.229 w (宽度)

    21.2.2.232 x (Left)

    21.2.2.235 y (Top)
    """

    @property
    def val(self):
        val = self.attrib['val']

        return to_xsd_double(val)  # type: ignore


class CT_UnsignedInt(OxmlBaseElement):
    """21.2.2.9 axId (轴 ID)

    21.2.2.31 crossAx (交叉轴 ID)

    21.2.2.61 explosion (爆炸)

    21.2.2.70 fmtId (格式ID)

    21.2.2.84 idx (索引)

    21.2.2.128 order (排序)

    21.2.2.152 ptCount (点数量)

    21.2.2.163 secondPiePt (第二个饼图点)
    """

    @property
    def val(self):
        val = self.attrib['val']

        return to_xsd_unsigned_int(val)  # type: ignore


class CT_RelId(OxmlBaseElement):
    """21.2.2.221 userShapes (图表绘制部分参考)

    21.2.2.26 chart (引用图表部件)
    """

    @property
    def r_id(self):
        val = self.attrib[qn('r:id')]

        return r_ST_RelationshipId(utils.AnyStrToStr(val))  # type: ignore


class CT_Extension(OxmlBaseElement):
    """21.2.2.62 ext (扩展)


    <xsd:sequence>
      <xsd:any processContents="lax"/>
    </xsd:sequence>
    """

    @property
    def uri(self):
        return XSD_Token(str(self.attrib['uri']))


class CT_ExtensionList(OxmlBaseElement):
    """21.2.2.64 extLst (图表可扩展性)

    <xsd:sequence>
      <xsd:element name="ext" type="CT_Extension" minOccurs="0" maxOccurs="unbounded"/>
    </xsd:sequence>
    """

    @property
    def ext_lst(self) -> list[CT_Extension]:
        return self.findall(qn('c:ext'))  # type: ignore


class CT_NumVal(OxmlBaseElement):
    """21.2.2.150 pt (数字点)

    该元素指定特定数据点的数据。
    """

    @property
    def v(self) -> str:
        """21.2.2.222 v (数值)

        该元素指定一个数值。

        21.2.2.223 v (文本值)

        此元素指定类别轴标签或系列名称的文本值。
        """

        ele: OxmlBaseElement = getattr(self, qn('c:v'))

        return str(ele.text)

    @property
    def idx(self):
        """系列在集合中的索引"""

        val = self.attrib[qn('c:idx')]

        return to_xsd_unsigned_int(val)  # type: ignore

    @property
    def format_code(self):
        """表示要应用的格式代码的字符串。

        有关详细信息，请参阅 SpreadsheetML numFmt 元素的 (§18.8.30) formatCode 属性。
        """

        val = self.attrib.get(qn('c:formatCode'))

        if val is None:
            return None

        return to_xsd_unsigned_int(val)  # type: ignore


class CT_NumData(OxmlBaseElement):
    """21.2.2.120 numCache (数字缓存)

    此元素指定图表上显示的系列的最后数据。

    21.2.2.122 numLit (数字 列表)

    该元素指定用于父元素的一组数字。
    """

    @property
    def format_code(self):
        """21.2.2.71 formatCode (格式代码)

        该元素指定一个表示要应用的格式代码的字符串。 有关详细信息，请参阅 SpreadsheetML numFmt 元素的 (§18.8.30) formatCode 属性。
        """
        ele = getattr(self, qn('c:formatCode'))

        if ele is None:
            return None

        return ele.text

    @property
    def pt_count(self) -> CT_UnsignedInt:
        """21.2.2.152 ptCount (点数量)

        该元素包含缓存中值的数量。
        """
        return getattr(self, qn('c:ptCount'))


    @property
    def pt_lst(self) -> list[CT_NumVal]:
        """21.2.2.150 pt (数字点) 列表

        该元素指定特定数据点的数据。
        """
        return self.findall(qn('c:pt'))  # type: ignore

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展列表"""
        return getattr(self, qn('c:extLst'))



class CT_NumRef(OxmlBaseElement):
    """21.2.2.123 numRef (编号引用)

    该元素指定对数值数据的引用以及最后使用的值的缓存。
    """

    @property
    def f(self) -> str:
        """21.2.2.65 f (公式)

        该元素指定对此图表中包含的数据源的引用。 这只应由电子表格应用程序使用。 演示文稿或文字处理应用程序应使用 externalData 元素。

        此引用采用书籍、工作表和单元格引用或书籍、可选工作表和定义的名称引用的形式。 此引用不包含等号。 (单元格引用定义在 §18.17. 链接和外部参考在 §18.17.2.3. 中详细描述 )
        """
        return getattr(self, qn('c:f')).text

    @property
    def num_cache(self) -> Optional[CT_NumData]:
        """21.2.2.120 numCache (数字缓存)

        此元素指定图表上显示的系列的最后数据。
        """
        return getattr(self, qn('c:numCache'))


    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展列表"""
        return getattr(self, qn('c:extLst'))



class CT_NumDataSource(OxmlBaseElement):
    """21.2.2.147 plus (加)

    21.2.2.113 minus (减)

    21.2.2.22 bubbleSize (气泡大小)

    21.2.2.237 yVal (Y Values)

    21.2.2.224 val (值集合)
    """

    @property
    def num_ref(self) -> Optional[CT_NumRef]:
        """21.2.2.123 numRef (编号引用)

        该元素指定对数值数据的引用以及最后使用的值的缓存。
        """

        return getattr(self, qn('c:numRef'), None)

    @property
    def num_lit(self) -> Optional[CT_NumData]:
        """21.2.2.122 numLit (数字 列表)

        该元素指定用于父元素的一组数字。
        """

        return getattr(self, qn('c:numLit'), None)

    @property
    def num(self):
        """21.2.2.123 numRef (编号引用)

        该元素指定对数值数据的引用以及最后使用的值的缓存。

        21.2.2.122 numLit (数字 列表)

        该元素指定用于父元素的一组数字。
        """

        ref = self.num_ref

        if ref is None:
            ref = self.num_lit

        if ref is None:
            msg = '应至少有线个元素.'
            raise OxmlElementValidateError(msg)

        return ref


class CT_StrVal(OxmlBaseElement):
    """21.2.2.151 pt (弦点)

    该元素指定特定数据点的字符串数据。
    """

    @property
    def v(self):
        ele = getattr(self, qn('c:v'))

        return ele.text

    @property
    def idx(self):
        """Index

        一组点的基于 0 的索引。 表示该数据所属的数据点编号。
        """

        # val = self.attrib[qn("c:idx")]
        val = self.attrib['idx']

        return to_xsd_unsigned_int(val)  # type: ignore


class CT_StrData(OxmlBaseElement):
    """21.2.2.199 strCache (字符串缓存)

    该元素指定用于图表的最后一个字符串数据。

    21.2.2.200 strLit (字符串字面量)

    该元素指定用于图表的一组字符串
    """

    @property
    def pt_count(self) -> CT_UnsignedInt:
        """21.2.2.152 ptCount (点数量)

        该元素包含缓存中值的数量。
        """
        return getattr(self, qn('c:ptCount'))

    @property
    def pt_lst(self) -> list[CT_StrVal]:
        """21.2.2.151 pt (弦点)

        该元素指定特定数据点的字符串数据。
        """
        return self.findall(qn('c:pt'))  # type: ignore

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展属性"""

        return getattr(self, qn('c:extLst'))



class CT_StrRef(OxmlBaseElement):
    """21.2.2.201 strRef (字符串参考)

    此元素指定对单个数据标签或标题的数据的引用，以及最后使用的值的缓存。
    """

    @property
    def f(self):
        """21.2.2.65 f (公式)

        该元素指定对此图表中包含的数据源的引用。 这只应由电子表格应用程序使用。 演示文稿或文字处理应用程序应使用 externalData 元素。

        此引用采用书籍、工作表和单元格引用或书籍、可选工作表和定义的名称引用的形式。 此引用不包含等号。 (单元格引用定义在 §18.17. 链接和外部参考在 §18.17.2.3. 中详细描述 )

        <c:cat>
            <c:strRef>
                <c:f>Sheet1!$A$1:$C$1</c:f>
                <c:strCache>
                …
                </c:strCache>
            </c:strRef>
        </c:cat>

        上面的示例显示了用于字符串缓存的公式引用。 在本例中，公式元素引用的系列名称位于单元格 A1、B1 和 C1 中。
        """
        return getattr(self, qn('c:f')).text

    @property
    def str_cache(self) -> Optional[CT_StrData]:
        """21.2.2.199 strCache (字符串缓存)

        该元素指定用于图表的最后一个字符串数据。
        """
        return getattr(self, qn('c:strCache'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展列表"""
        return getattr(self, qn('c:extLst'))



class CT_Tx(OxmlBaseElement):
    """21.2.2.214 tx (图表文本)

    此元素指定要在图表上使用的文本，包括富文本格式。
    """

    @property
    def str_rich(self) -> CT_StrRef | a_CT_TextBody:
        """21.2.2.201 strRef (字符串参考)

        此元素指定对单个数据标签或标题的数据的引用，以及最后使用的值的缓存。

        21.2.2.156 rich (富文本)

        该元素包含一个带有富文本格式的字符串。
        """

        tags = (
            qn('c:strRef'),  # CT_StrRef
            qn('c:rich'),  # a:CT_TextBody
        )

        return self.choice_require_one_child(*tags)  # type: ignore


class CT_TextLanguageID(OxmlBaseElement):
    """21.2.2.87 lang (编辑语言)

    此元素指定上次修改此图表时使用的主要编辑语言。
    """

    @property
    def val(self) -> str:
        return utils.AnyStrToStr(self.attrib['val'])  # type: ignore


class CT_Lvl(OxmlBaseElement):
    """21.2.2.99 lvl (级别)

    此元素指定类别轴的单级标签的数据。
    """

    @property
    def pt_lst(self) -> list[CT_StrVal]:
        return self.findall(qn('c:pt'))  # type: ignore


class CT_MultiLvlStrData(OxmlBaseElement):
    """21.2.2.114 multiLvlStrCache (多级字符串缓存)

    此元素指定类别轴图表上显示的最后数据。
    """

    @property
    def pt_count(self) -> Optional[CT_UnsignedInt]:
        return getattr(self, qn('c:ptCount'), None)

    @property
    def lvl_lst(self) -> list[CT_Lvl]:
        return self.findall(qn('c:lvl'))  # type: ignore

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class CT_MultiLvlStrRef(OxmlBaseElement):
    """21.2.2.115 multiLvlStrRef (多级字符串引用)

    此元素指定对类别轴数据的引用以及最后使用的值的缓存。
    """

    @property
    def f(self):
        return getattr(self, qn('c:f')).text

    @property
    def multi_lvl_str_cache(self) -> Optional[CT_StrData]:
        return getattr(self, qn('c:multiLvlStrCache'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class CT_AxDataSource(OxmlBaseElement):
    """21.2.2.234 xVal (X Values)

    该元素指定用于定义图表上数据标记位置的 x 值。

    21.2.2.24 cat (类别轴数据)

    该元素指定用于类别轴的数据。
    """

    @property
    def multi_lvl_str_ref(self) -> Optional[CT_MultiLvlStrRef]:
        """21.2.2.115 multiLvlStrRef (多级字符串引用)

        此元素指定对类别轴数据的引用以及最后使用的值的缓存。
        """

        return getattr(self, qn('c:multiLvlStrRef'), None)

    @property
    def num_ref(self) -> Optional[CT_NumRef]:
        """21.2.2.123 numRef (编号引用)

        该元素指定对数值数据的引用以及最后使用的值的缓存。
        """

        return getattr(self, qn('c:numRef'), None)

    @property
    def num_lit(self) -> Optional[CT_NumData]:
        """21.2.2.122 numLit (数字 文字)

        该元素指定用于父元素的一组数字。
        """

        return getattr(self, qn('c:numLit'), None)

    @property
    def str_ref(self) -> Optional[CT_StrRef]:
        """21.2.2.201 strRef (字符串参考)

        此元素指定对单个数据标签或标题的数据的引用，以及最后使用的值的缓存。
        """

        return getattr(self, qn('c:strRef'), None)

    @property
    def str_lit(self) -> Optional[CT_StrData]:
        """21.2.2.200 strLit (字符串字面量)

        该元素指定用于图表的一组字符串
        """

        return getattr(self, qn('c:strLit'), None)

    @property
    def data_ref(self):
        """数据引用

        21.2.2.115 multiLvlStrRef (多级字符串引用)

        21.2.2.123 numRef (编号引用)

        21.2.2.122 numLit (数字 文字)

        21.2.2.201 strRef (字符串参考)

        21.2.2.200 strLit (字符串字面量)
        """

        ref = self.multi_lvl_str_ref

        if ref is None:
            ref = self.num_ref

        if ref is None:
            ref = self.num_lit

        if ref is None:
            ref = self.str_ref

        if ref is None:
            ref = self.str_lit

        if ref is None:
            msg = '应至少包含一个元素'
            raise OxmlElementValidateError(msg)

        return ref


class CT_SerTx(OxmlBaseElement):
    """21.2.2.215 tx (系列文本)

    此元素指定系列名称的文本，不带富文本格式。
    """

    @property
    def str_ref(self) -> CT_StrRef | str:
        """
        21.2.2.201 strRef (字符串参考)

        此元素指定对单个数据标签或标题的数据的引用，以及最后使用的值的缓存。
        """
        tags = (
            qn('c:strRef'),  # CT_StrRef
            qn('c:v'),  # s:ST_Xstring
        )

        ele = self.choice_require_one_child(*tags)

        if ele.local_tagname == 'v':  # type: ignore
            return ele.text  # type: ignore

        return ele  # type: ignore


class ST_LayoutTarget(ST_BaseEnumType):
    """21.2.3.21 ST_LayoutTarget (布局目标)

    这个简单的类型指定了布局绘图区域的可能方法。
    """

    Inner = 'inner'
    """指定绘图区域大小应确定绘图区域的大小，不包括刻度线和轴标签。

    """
    Outer = 'outer'
    """指定绘图区域大小应确定绘图区域、刻度线和轴标签的大小。

    """


class CT_LayoutTarget(OxmlBaseElement):
    """21.2.2.89 layoutTarget (布局目标)

    该元素指定是否按内部（不包括轴和轴标签）或外部（包括轴和轴标签）布局绘图区域。
    """

    @property
    def val(self):
        """Layout Target Value

        指定布局目标值。
        """
        val = self.attrib.get('val')

        if val is None:
            return ST_LayoutTarget.Outer

        return ST_LayoutTarget(val)


class ST_LayoutMode(ST_BaseEnumType):
    """21.2.3.20 ST_LayoutMode (布局模式)

    这个简单的类型指定了存储图表元素位置的可能方法。
    """

    Edge = 'edge'
    """指定宽度或高度应解释为图表元素的右侧或底部。"""

    Factor = 'factor'
    """指定宽度或高度应解释为图表元素的宽度或高度。"""


class CT_LayoutMode(OxmlBaseElement):
    """21.2.2.81 hMode (高度模式)

    该元素指定如何解释此手动布局的高度元素。

    21.2.2.231 wMode (宽度类型)

    此元素指定如何解释此手动布局的 Width 元素。

    21.2.2.233 xMode (Left Mode)

    此元素指定如何解释此手动布局的 Left 元素。

    21.2.2.236 yMode (Top Mode)

    此元素指定如何解释此手动布局的顶部元素。
    """

    @property
    def val(self):
        """指定宽度的布局模式。"""
        val = self.attrib.get('val')

        if val is None:
            return ST_LayoutMode.Factor

        return ST_LayoutMode(val)


class CT_ManualLayout(OxmlBaseElement):
    """21.2.2.104 manualLayout (手动布局)

    该元素指定图表元素的确切位置。
    """

    @property
    def layout_target(self) -> Optional[CT_LayoutTarget]:
        return getattr(self, qn('c:layoutTarget'), None)


    @property
    def x_mode(self) -> Optional[CT_LayoutMode]:
        ele = getattr(self, qn('c:xMode'), None)

        if ele is None:
            return None

        return ele

    @property
    def y_mode(self) -> Optional[CT_LayoutMode]:
        ele = getattr(self, qn('c:yMode'), None)

        if ele is None:
            return None

        return ele

    @property
    def w_mode(self) -> Optional[CT_LayoutMode]:
        ele = getattr(self, qn('c:wMode'), None)

        if ele is None:
            return None

        return ele

    @property
    def h_mode(self) -> Optional[CT_LayoutMode]:
        ele = getattr(self, qn('c:hMode'), None)

        if ele is None:
            return None

        return ele

    @property
    def x(self) -> Optional[CT_Double]:
        ele = getattr(self, qn('c:x'), None)

        if ele is None:
            return None

        return ele

    @property
    def y(self) -> Optional[CT_Double]:
        ele = getattr(self, qn('c:y'), None)

        if ele is None:
            return None

        return ele

    @property
    def w(self) -> Optional[CT_Double]:
        ele = getattr(self, qn('c:w'), None)

        if ele is None:
            return None

        return ele

    @property
    def h(self) -> Optional[CT_Double]:
        ele = getattr(self, qn('c:h'), None)

        if ele is None:
            return None

        return ele

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class CT_Layout(OxmlBaseElement):
    """21.2.2.88 layout (布局)

    此元素指定图表元素如何放置在图表上。
    """

    @property
    def manual_layout(self) -> Optional[CT_ManualLayout]:
        return getattr(self, qn('c:manualLayout'), None)


    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class CT_Title(OxmlBaseElement):
    """21.2.2.210 title (标题)

    该元素指定一个标题。
    """

    @property
    def tx(self) -> Optional[CT_Tx]:
        """21.2.2.214 tx (图表文本)

        此元素指定要在图表上使用的文本，包括富文本格式。
        """
        return getattr(self, qn('c:tx'), None)

    @property
    def layout(self) -> Optional[CT_Layout]:
        """21.2.2.88 layout (布局)

        此元素指定图表元素如何放置在图表上。
        """
        return getattr(self, qn('c:layout'), None)

    @property
    def overlay(self) -> Optional[CT_Boolean]:
        """21.2.2.132 overlay (覆盖)

        该元素指定应允许其他图表元素与该图表元素重叠。
        """
        return getattr(self, qn('c:overlay'), None)

    @property
    def sp_pr(self) -> Optional[a_CT_ShapeProperties]:
        """21.2.2.197 spPr (形状属性)

        此元素指定父图表元素的格式。 不支持 custGeom、prstGeom、scene3d 和 xfrm 元素。 不支持 bwMode 属性。
        """
        return getattr(self, qn('c:spPr'), None)

    @property
    def tx_pr(self) -> Optional[a_CT_TextBody]:
        """21.2.2.216 txPr (文本属性)

        该元素指定文本格式。 不支持 lstStyle 元素。
        """
        return getattr(self, qn('c:txPr'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展元素列表"""
        return getattr(self, qn('c:extLst'))



ST_RotX = NewType('ST_RotX', int)
"""21.2.3.38 ST_RotX (X 轴旋转角度)

这个简单类型指定其内容包含 -90 到 90 之间的整数，其内容是以度为单位的角度。

此简单类型的内容是 W3C XML Schema 字节数据类型的限制。

这个简单类型还指定了以下限制：

    - 此简单类型的最小值大于或等于 -90。
    - 此简单类型的最大值小于或等于 90。
"""


def to_ST_RotX(val: AnyStr):
    _val = utils.AnyStrToStr(val)

    intval = int(_val)

    if not (-90 <= intval <= 90):
        msg = f'预期外的值: {val}'
        raise OxmlAttributeValidateError(msg)

    return intval


class CT_RotX(OxmlBaseElement):
    """21.2.2.157 rotX (X轴旋转角度)

    该元素指定3D图表在X方向上旋转的角度。
    """

    @property
    def val(self):
        """指定3D图表在X方向上旋转的角度。应包含一个介于-90和90之间的整数。"""

        val = self.attrib.get('val', '0')

        return to_ST_RotX(val)  # type: ignore


ST_HPercentWithSymbol = NewType('ST_HPercentWithSymbol', str)
"""21.2.3.52 ST_HPercentWithSymbol (高度百分比（带符号）)

这个简单类型指定其内容包含在5%到500%之间的百分比。

简单类型的内容应与以下正则表达式模式匹配：

0*(([5-9])|([1-9][0-9])|([1-4][0-9][0-9])|500)%.
"""


ST_HPercentUShort = NewType('ST_HPercentUShort', int)


def to_ST_HPercentUShort(val: AnyStr):
    _val = utils.AnyStrToStr(val)

    intval = int(_val)

    if not (5 <= intval <= 500):
        msg = f'预期外的值: {val}'
        raise OxmlAttributeValidateError(msg)

    return intval


ST_HPercent = Union[str, int]
"""21.2.3.19 ST_HPercent (身高百分比)

此简单类型指定其内容包含 5% 到 500% 之间的百分比。

这个简单类型是以下类型的联合：

- ST_HPercentWithSymbol 简单类型 (§21.2.3.52).
"""
# <xsd:union memberTypes="ST_HPercentWithSymbol ST_HPercentUShort"/>


def to_ST_HPercent(val: AnyStr) -> ST_HPercent:
    str_val = utils.AnyStrToStr(val)

    if str_val.endswith('%'):
        return ST_HPercentWithSymbol(str_val)

    return to_ST_HPercentUShort(val)


class CT_HPercent(OxmlBaseElement):
    """21.2.2.83 hPercent (高度百分比)

    此元素将 3D 图表的高度指定为图表宽度的百分比。
    """

    @property
    def val(self):
        """指定该属性的内容包含 5% 到 500% 之间的高度百分比。"""
        val = self.attrib.get('val', '100%')

        return to_ST_HPercent(val)  # type: ignore


ST_RotY = NewType('ST_RotY', int)
"""21.2.3.39 ST_RotY (Y 轴旋转角度)

这个简单类型指定其内容包含 0 到 360 之间的整数，其内容是角度（以度为单位）。

此简单类型的内容是 W3C XML Schema unsignedShort 数据类型的限制。

这个简单类型还指定了以下限制：

- 此简单类型的最小值大于或等于 0。
- 此简单类型的最大值小于或等于 360。
"""


def to_ST_RotY(val: AnyStr):
    intval = int(utils.AnyStrToStr(val))

    if not (0 <= intval <= 360):
        msg = f'预期外的值: {val}'
        raise OxmlAttributeValidateError(msg)

    return ST_RotY(intval)


class CT_RotY(OxmlBaseElement):
    """21.2.2.158 rotY (Y轴旋转角度)

    该元素指定3D图表在Y方向上旋转的角度。
    """

    @property
    def val(self):
        """指定3D图表在Y方向上旋转的角度。应包含一个介于0和360之间的整数。"""

        return to_ST_RotY(self.attrib.get('val', '0'))  # type: ignore


ST_DepthPercent = Union[str, int]
"""21.2.3.9 ST_DepthPercent (深度百分比)

此简单类型指定其内容包含 20% 到 2000% 之间的百分比。

这个简单类型是以下类型的联合：

- ST_DepthPercentWithSymbol 简单类型 (§21.2.3.51).
"""


ST_DepthPercentWithSymbol = NewType('ST_DepthPercentWithSymbol', str)
"""21.2.3.51 ST_DepthPercentWithSymbol (深度百分比（带符号）)

这个简单类型指定其内容包含20%到2000%之间的百分比。

简单类型的内容应与以下正则表达式模式匹配：

0*(([2-9][0-9])|([1-9][0-9][0-9])|(1[0-9][0-9][0-9])|2000)%.
"""


ST_DepthPercentUShort = NewType('ST_DepthPercentUShort', int)


def to_ST_DepthPercentUShort(val: AnyStr):
    _val = utils.AnyStrToStr(val)

    intval = int(_val)

    if not (20 <= intval <= 2000):
        msg = f'预期外的值: {val}'
        raise OxmlAttributeValidateError(msg)

    return intval


class CT_DepthPercent(OxmlBaseElement):
    """21.2.2.41 depthPercent (深度百分比)

    该元素指定3D图表的深度，以图表宽度的百分比表示（介于20%和2000%之间）。
    """

    @property
    def val(self) -> ST_DepthPercent:
        """指定了由父XML元素定义的属性的百分比值。"""
        return self.attrib.get('val', '0')  # type: ignore


ST_Perspective = NewType('ST_Perspective', int)
"""21.2.3.34 ST_Perspective (透视)

这个简单类型指定其内容包含0到100之间的整数，其内容是百分比。

此简单类型的内容是 W3C XML 架构 unsignedByte 数据类型的限制。

这个简单类型还指定了以下限制：

- 此简单类型的最小值大于或等于 0。
- 此简单类型的最大值小于或等于 240。
"""


def to_ST_Perspective(val: AnyStr):
    _val = utils.AnyStrToStr(val)

    intval = int(_val)

    if not (0 <= intval <= 240):
        msg = f'预期外的值: {val}'
        raise OxmlAttributeValidateError(msg)

    return intval


class CT_Perspective(OxmlBaseElement):
    """21.2.2.136 perspective (看法)

    该元素指定 3D 图表的视角。 如果 Right Angle Axes 为 true，则忽略此元素。
    """

    @property
    def val(self):
        """指定 3D 图表的视角。 应包含 0 到 240 之间的整数，单位为二分之一度。"""

        return to_ST_Perspective(self.attrib.get('val', '30'))  # type: ignore


class CT_View3D(OxmlBaseElement):
    """21.2.2.228 view3D (3D 视图)

    该元素指定图表的 3D 视图。
    """

    @property
    def rot_x(self) -> Optional[CT_RotX]:
        return getattr(self, qn('c:rotX'), None)

    @property
    def h_percent(self) -> Optional[CT_HPercent]:
        return getattr(self, qn('c:hPercent'), None)

    @property
    def rot_y(self) -> Optional[CT_RotY]:
        return getattr(self, qn('c:rotY'), None)

    @property
    def depth_percent(self) -> Optional[CT_DepthPercent]:
        return getattr(self, qn('c:depthPercent'), None)

    @property
    def r_ang_ax(self) -> Optional[CT_Boolean]:
        return getattr(self, qn('c:rAngAx'), None)

    @property
    def perspective(self) -> Optional[CT_Perspective]:
        return getattr(self, qn('c:perspective'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class CT_Surface(OxmlBaseElement):
    """21.2.2.191 sideWall (侧壁)

    该元素指定侧壁。

    21.2.2.69 floor (下限)

    该元素指定 3D 图表的下限。

    21.2.2.11 backWall (后墙)

    该元素指定图表的后墙。
    """

    @property
    def thickness(self) -> Optional[CT_Thickness]:
        return getattr(self, qn('c:thickness'), None)

    @property
    def sp_pr(self) -> Optional[a_CT_ShapeProperties]:
        return getattr(self, qn('c:spPr'), None)

    @property
    def picture_options(self) -> Optional[CT_PictureOptions]:
        return getattr(self, qn('c:pictureOptions'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



# <xsd:union memberTypes="ST_ThicknessPercent xsd:unsignedInt"/>
ST_Thickness = Union[str, int]
"""21.2.3.59 ST_Thickness (厚度百分比)

这个简单类型指定其内容包含百分比。

这个简单类型是以下类型的联合：

- ST_ThicknessPercent simple type (§21.2.3.60).
"""


def to_ST_Thickness(val: AnyStr) -> ST_Thickness:
    strval = utils.AnyStrToStr(val)

    if strval.endswith('%'):
        return to_ST_ThicknessPercent(val)

    return int(strval)


ST_ThicknessPercent = NewType('ST_ThicknessPercent', str)
"""21.2.3.60 ST_ThicknessPercent (厚度百分比)

这个简单类型指定其内容包含百分比。

简单类型的内容应与以下正则表达式模式匹配: ([0-9]+)%.
"""


def to_ST_ThicknessPercent(val: AnyStr):
    strval = utils.AnyStrToStr(val)

    return ST_ThicknessPercent(strval)


class CT_Thickness(OxmlBaseElement):
    """21.2.2.206 thickness (厚度)

    该元素指定墙壁或地板的厚度占绘图体积最大尺寸的百分比。

    指定该属性的内容包含百分比。

    该数字的内容根据父 XML 元素的上下文进行解释。
    """

    @property
    def val(self):
        return to_ST_Thickness(self.attrib['val'])  # type: ignore


class CT_DTable(OxmlBaseElement):
    """21.2.2.54 dTable (数据表)

    该元素指定了一个数据表。
    """

    @property
    def show_horz_border(self) -> Optional[CT_Boolean]:
        return getattr(self, qn('c:showHorzBorder'), None)

    @property
    def show_vert_border(self) -> Optional[CT_Boolean]:
        return getattr(self, qn('c:showVertBorder'), None)

    @property
    def show_outline(self) -> Optional[CT_Boolean]:
        return getattr(self, qn('c:showOutline'), None)

    @property
    def show_keys(self) -> Optional[CT_Boolean]:
        return getattr(self, qn('c:showKeys'), None)

    @property
    def sp_pr(self) -> Optional[a_CT_ShapeProperties]:
        return getattr(self, qn('c:spPr'), None)

    @property
    def tx_pr(self) -> Optional[a_CT_TextBody]:
        return getattr(self, qn('c:txPr'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



ST_GapAmount = Union[str, int]
"""21.2.3.16 ST_GapAmount (间隙百分比)

此简单类型指定其内容包含 0% 到 500% 之间的百分比。

这个简单类型是以下类型的联合：

ST_GapAmountPercent 简单类型 (§21.2.3.53).
"""


def to_ST_GapAmount(val: AnyStr):
    strval = utils.AnyStrToStr(val)

    if strval.endswith('%'):
        return ST_GapAmountPercent(strval)

    return int(strval)


ST_GapAmountPercent = NewType('ST_GapAmountPercent', str)
"""21.2.3.53 ST_GapAmountPercent (差额百分比)

此简单类型指定其内容包含 0% 到 500% 之间的百分比。

简单类型的内容应与以下正则表达式模式匹配：

0*(([0-9])|([1-9][0-9])|([1-4][0-9][0-9])|500)%.
"""


def to_ST_GapAmountPercent(val: AnyStr):
    return utils.AnyStrToStr(val)



ST_GapAmountUShort = NewType('ST_GapAmountUShort', int)


def to_ST_GapAmountUShort(val: AnyStr):
    _val = utils.AnyStrToStr(val)

    intval = int(_val)

    if not (0 <= intval <= 500):
        msg = f'预期外的值: {val}'
        raise OxmlAttributeValidateError(msg)

    return ST_GapAmountUShort(intval)


class CT_GapAmount(OxmlBaseElement):
    @property
    def val(self):
        return to_ST_GapAmount(self.attrib.get('val', '150%'))  # type: ignore


ST_Overlap = Union[str, int]
"""21.2.3.31 ST_Overlap (重叠)

此简单类型指定其内容包含 -100% 到 100% 之间的百分比。

这个简单类型是以下类型的联合：

ST_OverlapPercent 简单类型 (§21.2.3.57).
"""


def to_ST_Overlap(val: AnyStr):
    strval = utils.AnyStrToStr(val)

    if strval.endswith('%'):
        return ST_OverlapPercent(strval)

    return int(strval)


ST_OverlapPercent = NewType('ST_OverlapPercent', str)
"""21.2.3.57 ST_OverlapPercent (重叠百分比)

此简单类型指定其内容包含 -100% 到 100% 之间的百分比。

简单类型的内容应与以下正则表达式模式匹配：

(-?0*(([0-9])|([1-9][0-9])|100))%.
"""


def to_ST_OverlapPercent(val: AnyStr):
    strval = utils.AnyStrToStr(val)

    return ST_OverlapPercent(strval)


ST_OverlapByte = NewType('ST_OverlapByte', int)


def to_ST_OverlapByte(val: AnyStr):
    _val = utils.AnyStrToStr(val)

    intval = int(_val)

    if not (-100 <= intval <= 100):
        msg = f'预期外的值: {val}'
        raise OxmlAttributeValidateError(msg)

    return ST_OverlapByte(intval)


class CT_Overlap(OxmlBaseElement):
    @property
    def val(self):
        return to_ST_Overlap(self.attrib.get('val', '0%'))  # type: ignore


ST_BubbleScale = Union[str, int]
"""21.2.3.5 ST_BubbleScale (气泡缩放)

此简单类型指定其内容包含 0% 到 300% 之间的百分比。

这个简单类型是以下类型的联合：

ST_BubbleScalePercent 简单类型 (§21.2.3.58).
"""


def to_ST_BubbleScale(val: AnyStr):
    strval = utils.AnyStrToStr(val)

    if strval.endswith('%'):
        return ST_BubbleScalePercent(strval)

    return ST_BubbleScaleUInt(int(strval))


ST_BubbleScalePercent = NewType('ST_BubbleScalePercent', str)
"""21.2.3.58 ST_BubbleScalePercent (气泡比例百分比)

此简单类型指定其内容包含 0% 到 300% 之间的百分比。

简单类型的内容应与以下正则表达式模式匹配：

0*(([0-9])|([1-9][0-9])|([1-2][0-9][0-9])|300)%.
"""


def to_ST_BubbleScalePercent(val: AnyStr):
    strval = utils.AnyStrToStr(val)

    return ST_BubbleScalePercent(strval)


ST_BubbleScaleUInt = NewType('ST_BubbleScaleUInt', int)


def to_ST_BubbleScaleUInt(val: AnyStr):
    _val = utils.AnyStrToStr(val)

    intval = int(_val)

    if not (0 <= intval <= 300):
        msg = f'预期外的值: {val}'
        raise OxmlAttributeValidateError(msg)

    return ST_BubbleScaleUInt(intval)


class CT_BubbleScale(OxmlBaseElement):
    """21.2.2.21 bubbleScale (气泡缩放)

    该元素指定气泡图的比例因子。 该元素可以是 0 到 300 之间的百分比值，对应于默认大小的百分比。
    """

    @property
    def val(self):
        """指定如何缩放气泡图上的气泡。"""
        return to_ST_BubbleScale(self.attrib.get('val', '100%'))  # type: ignore


class ST_SizeRepresents(ST_BaseEnumType):
    """21.2.3.43 ST_SizeRepresents (尺寸表示)

    这种简单的类型指定了将数据表示为气泡图大小的可能方法。
    """

    Area = 'area'
    """指定气泡面积应与气泡大小值成比例。"""

    Width = 'w'
    """指定气泡的半径应与气泡大小值成比例。"""


class CT_SizeRepresents(OxmlBaseElement):
    """21.2.2.193 sizeRepresents (尺寸代表)

    该元素指定气泡大小值在图表上的表示方式。
    """

    @property
    def val(self):
        """指定气泡大小如何表示值。"""

        val = self.attrib.get('val')

        if val is None:
            return ST_SizeRepresents.Area

        return ST_SizeRepresents(val)


ST_FirstSliceAng = NewType('ST_FirstSliceAng', int)
"""21.2.3.15 ST_FirstSliceAng (第一切片角)

此简单类型指定其内容包含 0 到 360 之间的整数。

此简单类型的内容是 W3C XML Schema unsignedShort 数据类型的限制。

这个简单类型还指定了以下限制：

- 此简单类型的最小值大于或等于 0。
- 此简单类型的最大值小于或等于 360。
"""


def to_ST_FirstSliceAng(val: AnyStr):
    strval = utils.AnyStrToStr(val)
    intval = int(strval)

    if not (0 <= intval <= 360):
        msg = f'预期外的值: {val}'
        raise OxmlAttributeValidateError(msg)

    return ST_BubbleScaleUInt(intval)


class CT_FirstSliceAng(OxmlBaseElement):
    """21.2.2.68 firstSliceAng (第一切片角)

    此元素指定第一个饼图或圆环图切片的角度，以度为单位（从上顺时针方向）。
    """

    @property
    def val(self):
        """指定第一个切片的角度。"""

        return to_ST_FirstSliceAng(self.attrib.get('val', '0'))  # type: ignore


ST_HoleSize = Union[str, int]
"""21.2.3.18 ST_HoleSize (孔尺寸)

此简单类型指定其内容包含 1% 到 90% 之间的百分比。

这个简单类型是以下类型的联合：

- ST_HoleSizePercent 简单类型 (§21.2.3.55).
"""


def to_ST_HoleSize(val: AnyStr):
    strval = utils.AnyStrToStr(val)

    if strval.endswith('%'):
        return ST_HoleSizePercent(strval)

    return ST_HoleSizeUByte(int(strval))


ST_HoleSizePercent = NewType('ST_HoleSizePercent', str)
"""21.2.3.55 ST_HoleSizePercent (孔径百分比)

此简单类型指定其内容包含 1% 到 90% 之间的百分比。

简单类型的内容应与以下正则表达式模式匹配：

0*([1-9]|([1-8][0-9])|90)%.
"""


def to_ST_HoleSizePercent(val: AnyStr):
    strval = utils.AnyStrToStr(val)

    return ST_HoleSizePercent(strval)


ST_HoleSizeUByte = NewType('ST_HoleSizeUByte', int)


def to_ST_HoleSizeUByte(val: AnyStr):
    strval = utils.AnyStrToStr(val)
    intval = int(strval)

    if not (1 <= intval <= 90):
        msg = f'预期外的值: {val}'
        raise OxmlAttributeValidateError(msg)

    return ST_HoleSizeUByte(intval)


class CT_HoleSize(OxmlBaseElement):
    @property
    def val(self):
        return to_ST_HoleSizeUByte(self.attrib.get('val', '10%'))  # type: ignore


class ST_SplitType(ST_BaseEnumType):
    """21.2.3.45 ST_SplitType (分割类型)

    这个简单的类型指定了分割饼图或饼图条的可能方法。

    此简单类型的内容是 W3C XML 架构字符串数据类型的限制。

    此简单类型仅限于下表中列出的值：
    """

    Auto = 'auto'
    """指定应使用此图表类型的默认机制来分割数据点。"""

    Cust = 'cust'
    """指定应根据自定义拆分值在饼图和第二个图表之间拆分数据点。"""

    Percent = 'percent'
    """通过将百分比小于分割位置百分比的点放入第二个图表中，指定应在饼图和第二个图表之间分割数据点。"""

    Pos = 'pos'
    """通过将数据点的最后一个分割位置放入第二个图表中，指定应在饼图和第二个图表之间分割数据点."""

    Val = 'val'
    """通过将值小于分割位置的数据点放入第二个图表中，指定应在饼图和第二个图表之间分割数据点."""


class CT_SplitType(OxmlBaseElement):
    """21.2.2.196 splitType (分割类型)

    此元素指定如何确定哪些数据点位于饼图或饼图条形图的第二个饼图或条形图中。
    """

    @property
    def val(self):
        """指定如何分割第一个饼图和第二个饼图或条形图之间的数据点。"""

        val = self.attrib.get('val')

        if val is None:
            return ST_SplitType.Auto

        return ST_SplitType(val)


class CT_CustSplit(OxmlBaseElement):
    """21.2.2.35 custSplit (自定义拆分)

    该元素包含有关具有自定义分割的饼图或柱状图的自定义分割信息。
    """

    @property
    def second_pie_pt(self) -> list[CT_UnsignedInt]:
        return self.findall(qn('c:secondPiePt'))  # type: ignore


ST_SecondPieSize = Union[str, int]
"""21.2.3.41 ST_SecondPieSize (第二饼图尺寸)

这个简单类型指定其内容包含5%到200%之间的百分比，其内容由百分比组成。

这个简单类型是以下类型的联合：

ST_SecondPieSizePercent 简单类型 (§21.2.3.55).
"""


def to_ST_SecondPieSize(val: AnyStr):
    strval = utils.AnyStrToStr(val)

    if strval.endswith('%'):
        return ST_SecondPieSizePercent(strval)

    return ST_SecondPieSizeUShort(int(strval))


ST_SecondPieSizePercent = NewType('ST_SecondPieSizePercent', str)
"""21.2.3.54 ST_SecondPieSizePercent (第二个饼图大小百分比)

此简单类型指定其内容包含 5% 到 200% 之间的百分比。

简单类型的内容应与以下正则表达式模式匹配：

0* (([5-9])|([1-9][0-9])|(1[0-9][0-9])|200)%.
"""


def to_ST_SecondPieSizePercent(val: AnyStr):
    strval = utils.AnyStrToStr(val)

    return ST_SecondPieSizePercent(strval)


ST_SecondPieSizeUShort = NewType('ST_SecondPieSizeUShort', int)


def to_ST_SecondPieSizeUShort(val: AnyStr):
    strval = utils.AnyStrToStr(val)
    intval = int(strval)

    if not (5 <= intval <= 200):
        msg = f'预期外的值: {val}'
        raise OxmlAttributeValidateError(msg)

    return ST_SecondPieSizeUShort(intval)


class CT_SecondPieSize(OxmlBaseElement):
    @property
    def val(self):
        return to_ST_SecondPieSize(self.attrib.get('val', '75%'))  # type: ignore


class CT_NumFmt(OxmlBaseElement):
    """21.2.2.121 numFmt (数字格式)

    该元素指定父元素的数字格式。
    """

    @property
    def format_code(self):
        """该元素指定一个表示要应用的格式代码的字符串。 有关详细信息，请参阅 SpreadsheetML numFmt 元素的 (§18.8.30) formatCode 属性。"""

        ele = getattr(self, qn('c:formatCode'))

        return ele.text

    @property
    def source_linked(self):
        """为父 XML 元素定义的属性指定布尔值。

        值 1 或 true 指定应用该属性。 这是该属性的默认值，当父元素存在时隐含该值，但该属性被省略。

        值 0 或 false 指定不应用该属性。
        """

        val = self.attrib.get('sourceLinked')

        return to_xsd_bool(val)


class ST_LblAlgn(ST_BaseEnumType):
    """21.2.3.22 ST_LblAlgn (标签对齐)

    这个简单的类型指定了对齐刻度标签的可能方法。
    """

    Center = 'ctr'
    """指定文本应居中。"""

    Left = 'l'
    """指定文本应左对齐。"""

    Right = 'r'
    """指定文本右对齐。"""


class CT_LblAlgn(OxmlBaseElement):
    """21.2.2.90 lblAlgn (标签对齐)

    该元素指定轴上刻度标签的文本对齐方式。
    """

    @property
    def val(self):
        """指定标签对齐方式。"""

        _val = self.attrib['val']

        return ST_LblAlgn(_val)


class ST_DLblPos(ST_BaseEnumType):
    """21.2.3.11 ST_DLblPos (数据标签位置)

    这种简单的类型指定数据标签的可能位置。
    """

    BestFit = 'bestFit'
    """指定数据标签应显示在最佳位置。"""

    Bottom = 'b'
    """指定数据标签应显示在数据标记下方。"""

    Center = 'ctr'
    """指定数据标签应显示在数据标记的中心。"""

    InBase = 'inBase'
    """指定数据标签应显示在数据标记的底部内。"""

    InEnd = 'inEnd'
    """指定数据标签应显示在数据标记的末尾内。"""

    Left = 'l'
    """指定数据标签应显示在数据标记的左侧。"""

    OutEnd = 'outEnd'
    """指定数据标签应显示在数据标记末尾之外。"""

    Right = 'r'
    """指定数据标签应显示在数据标记的右侧。"""

    Top = 't'
    """指定数据标签应显示在数据标记上方。"""


class CT_DLblPos(OxmlBaseElement):
    """21.2.2.48 dLblPos (数据标签位置)

    指定数据标签在图表上的位置。
    """

    @property
    def val(self):
        _val = self.attrib['val']

        return ST_DLblPos(_val)


class EG_DLblShared(OxmlBaseElement):
    tags = (
        qn('c:numFmt'),  # CT_NumFmt
        qn('c:spPr'),  # a_CT_ShapeProperties
        qn('c:txPr'),  # a_CT_TextBody
        qn('c:DLblPos'),  # CT_DLblPos
        qn('c:showLegendKey'),  # CT_Boolean
        qn('c:showVal'),  # CT_Boolean
        qn('c:showCatName'),  # CT_Boolean
        qn('c:showSerName'),  # CT_Boolean
        qn('c:showPercent'),  # CT_Boolean
        qn('c:showBubbleSize'),  # CT_Boolean
        qn('c:separator'),  # xsd:string
    )

    @property
    def num_format(self) -> Optional[CT_NumFmt]:
        """21.2.2.121 numFmt (数字格式)

        该元素指定父元素的数字格式。
        """
        return getattr(self, qn('c:numFmt'), None)

    @property
    def sp_pr(self) -> Optional[a_CT_ShapeProperties]:
        """21.2.2.197 spPr (形状属性)

        此元素指定父图表元素的格式。 不支持 custGeom、prstGeom、scene3d 和 xfrm 元素。 不支持 bwMode 属性。
        """
        return getattr(self, qn('c:spPr'), None)

    @property
    def tx_pr(self) -> Optional[a_CT_TextBody]:
        """21.2.2.216 txPr (文本属性)

        该元素指定文本格式。 不支持 lstStyle 元素。
        """
        return getattr(self, qn('c:txPr'), None)

    @property
    def dlbl_pos(self) -> Optional[CT_DLblPos]:
        """21.2.2.48 dLblPos (数据标签位置)

        该元素指定了数据标签的位置。
        """
        return getattr(self, qn('c:DLblPos'), None)

    @property
    def show_legend_key(self) -> Optional[CT_Boolean]:
        """21.2.2.184 showLegendKey (显示图例键)

        该元素指定图例键应显示在数据标签中。
        """
        return getattr(self, qn('c:showLegendKey'), None)

    @property
    def show_val(self) -> Optional[CT_Boolean]:
        """21.2.2.189 showVal (显示值)

        该元素指定该值应显示在数据标签中。
        """
        return getattr(self, qn('c:showVal'), None)

    @property
    def show_cat_name(self) -> Optional[CT_Boolean]:
        """21.2.2.179 showCatName (显示类别名称)

        该元素指定类别名称应显示在数据标签中。
        """
        return getattr(self, qn('c:showCatName'), None)

    @property
    def show_ser_name(self) -> Optional[CT_Boolean]:
        """21.2.2.188 showSerName (显示系列名称)

        该元素指定系列名称应显示在数据标签中。
        """
        return getattr(self, qn('c:showSerName'), None)

    @property
    def show_per_name(self) -> Optional[CT_Boolean]:
        """21.2.2.187 showPercent (显示百分比)

        该元素指定百分比应显示在数据标签中。
        """
        return getattr(self, qn('c:showPercent'), None)

    @property
    def show_bubble_size(self) -> Optional[CT_Boolean]:
        """21.2.2.178 showBubbleSize (显示气泡大小)

        该元素指定应在数据标签中显示气泡大小。
        """
        return getattr(self, qn('c:showBubbleSize'), None)

    @property
    def separator(self) -> Optional[str]:
        """21.2.2.166 separator (分隔符)

        该元素指定用于分隔数据标签部分的文本。默认情况下为逗号，但对于仅显示类别名称和百分比的饼图，应使用换行符代替。
        """
        ele: Optional[OxmlBaseElement] = getattr(self, qn('c:separator'), None)

        if ele is None:
            return None

        return ele.text


class Group_DLbl(EG_DLblShared):
    tags = (
        qn('c:layout'),  # CT_Layout
        qn('c:tx'),  # CT_Tx
    )

    @property
    def layout(self) -> Optional[CT_Layout]:
        """21.2.2.88 layout (布局)

        此元素指定图表元素如何放置在图表上。
        """
        return getattr(self, qn('c:layout'), None)

    @property
    def tx(self) -> Optional[CT_Tx]:
        """21.2.2.214 tx (图表文本)

        此元素指定要在图表上使用的文本，包括富文本格式。
        """
        return getattr(self, qn('c:tx'), None)


class CT_DLbl(Group_DLbl):
    """21.2.2.47 dLbl (数据标签)

    该元素指定了一个数据标签。
    """

    @property
    def idx(self) -> CT_UnsignedInt:
        """21.2.2.84 idx (索引)

        该元素指定包含元素的索引。 该索引应确定该元素适用于父集合的哪个子集合。
        """
        return getattr(self, qn('c:idx'))

    @property
    def delete(self) -> Optional[CT_Boolean]:
        """21.2.2.40 delete (删除)

        该元素指定其包含元素指定的图表元素将从图表中删除。

        如果应用程序在用户指定应从图表中删除这些元素后仍默认添加它们，则应将其设置为true。

        注意: xsd定义为:

        <xsd:choice>
            <xsd:element name="delete" type="CT_Boolean" minOccurs="1" maxOccurs="1"/>
            <xsd:group ref="Group_DLbl" minOccurs="1" maxOccurs="1"/>
        </xsd:choice>

        即意味着，当delete元素存在时, 继承自 Group_DLbl 中的子元素就会没有
        """
        return getattr(self, qn('c:delete'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """ " 扩展元素列表"""
        return getattr(self, qn('c:extLst'))



class Group_DLbls(EG_DLblShared):
    @property
    def show_leader_lines(self) -> Optional[CT_Boolean]:
        """21.2.2.183 showLeaderLines (显示引导线)

        该元素指定数据标签应显示引导线
        """
        return getattr(self, qn('c:showLeaderLines'), None)

    @property
    def leader_lines(self) -> Optional[CT_ChartLines]:
        """21.2.2.92 leaderLines (引导线)

        该元素指定数据标签的引导线。
        """
        return getattr(self, qn('c:leaderLines'), None)


class CT_DLbls(Group_DLbls):
    """21.2.2.49 dLbls (数据标签合集)

    该元素作为根元素，用于指定整个系列或整个图表的数据标签设置。它包含子元素，用于指定具体的格式和定位设置。
    """

    @property
    def dlbl(self) -> list[CT_DLbl]:
        """21.2.2.47 dLbl (数据标签)

        该元素指定了一个数据标签。
        """
        return self.findall(qn('c:dLbl'))  # type: ignore

    @property
    def delete(self) -> Optional[CT_Boolean]:
        """21.2.2.40 delete (删除)

        该元素指定其包含元素指定的图表元素将从图表中删除。

        如果应用程序在用户指定应从图表中删除这些元素后仍默认添加它们，则应将其设置为true。

        注意: xsd定义为:

        <xsd:choice>
            <xsd:element name="delete" type="CT_Boolean" minOccurs="1" maxOccurs="1"/>
            <xsd:group ref="Group_DLbls" minOccurs="1" maxOccurs="1"/>
        </xsd:choice>

        即意味着，当delete元素存在时, 继承自 Group_DLbl 中的子元素就会没有
        """
        return getattr(self, qn('c:delete'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展元素列表"""

        return getattr(self, qn('c:extLst'))



class ST_MarkerStyle(ST_BaseEnumType):
    """21.2.3.27 ST_MarkerStyle (标记样式)

    此图显示了每种标记样式。 黑色用作线条颜色，红色用作填充颜色。 破折号和点的高度是标记高度的 ⅕。 点的宽度是标记宽度的 ½。 破折号和点也有填充，但标记需要做得相当大才能可见。
    """

    Circle = 'circle'
    """指定应在每个数据点处绘制一个圆。"""

    Dash = 'dash'
    """指定应在每个数据点处绘制破折号。"""

    Diamond = 'diamond'
    """指定应在每个数据点处绘制菱形。"""

    Dot = 'dot'
    """指定应在每个数据点处绘制一个点。"""

    none = 'none'
    """指定在每个数据点处不应绘制任何内容。"""

    Picture = 'picture'
    """指定应在每个数据点绘制图片。"""

    Plus = 'plus'
    """指定应在每个数据点处绘制加号。"""

    Square = 'square'
    """指定应在每个数据点处绘制一个正方形。"""

    Star = 'star'
    """指定应在每个数据点绘制一颗星。"""

    Triangle = 'triangle'
    """指定应在每个数据点处绘制一个三角形。"""

    X = 'x'
    """指定应在每个数据点处绘制 X。"""

    Auto = 'auto'


class CT_MarkerStyle(OxmlBaseElement):
    """21.2.2.205 symbol (标记)

    该元素指定用于数据点的标记。
    """

    @property
    def val(self):
        """指定标记样式。"""

        _val = self.attrib['val']

        return ST_MarkerStyle(_val)


ST_MarkerSize = NewType('ST_MarkerSize', int)
"""21.2.3.26 ST_MarkerSize (标记尺寸)

这个简单类型指定其内容包含 2 到 72 之间的整数，其内容是以点为单位的大小。

此简单类型的内容是 W3C XML 架构 unsignedByte 数据类型的限制。

这个简单类型还指定了以下限制：

- 此简单类型的最小值大于或等于 2。
- 此简单类型的最大值小于或等于 72。
"""


def to_ST_MarkerSize(val: AnyStr):
    intval = int(utils.AnyStrToStr(val))

    if not (2 <= intval <= 72):
        msg = f'预期外的值: {intval}'
        raise OxmlAttributeValidateError(msg)

    return ST_MarkerSize(intval)


class CT_MarkerSize(OxmlBaseElement):
    """21.2.2.192 size (尺寸)

    该元素指定标记的大小（以磅（point）为单位）。
    """

    @property
    def val(self):
        """指定标记的大小（以磅（points）为单位）。 应包含 2 到 72 之间的整数。"""
        _val = self.attrib.get('val', '5')

        return to_ST_MarkerSize(_val)  # type: ignore


class CT_Marker(OxmlBaseElement):
    """21.2.2.106 marker (标记)

    该元素指定数据标记。
    """

    @property
    def symbol(self) -> Optional[CT_MarkerStyle]:
        """21.2.2.205 symbol (标记)

        该元素指定用于数据点的标记。
        """
        return getattr(self, qn('c:symbol'), None)

    @property
    def size(self) -> Optional[CT_MarkerSize]:
        """21.2.2.192 size (尺寸)

        该元素指定标记的大小（以磅（point）为单位）。

        """
        return getattr(self, qn('c:size'), None)

    @property
    def sp_pr(self) -> Optional[a_CT_ShapeProperties]:
        """21.2.2.197 spPr (形状属性)

        此元素指定父图表元素的格式。 不支持 custGeom、prstGeom、scene3d 和 xfrm 元素。 不支持 bwMode 属性。
        """
        return getattr(self, qn('c:spPr'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展列表"""
        return getattr(self, qn('c:extLst'))



class CT_DPt(OxmlBaseElement):
    """21.2.2.52 dPt (数据点)

    该元素指定一个单独的数据点。
    """

    @property
    def idx(self) -> CT_UnsignedInt:
        """21.2.2.84 idx (索引)

        该元素指定包含元素的索引。 该索引应确定该元素适用于父集合的哪个子集合。
        """
        return getattr(self, qn('c:idx'))

    @property
    def invert_if_gegative(self) -> Optional[CT_Boolean]:
        """21.2.2.86 invertIfNegative (如果为负则反转)

        该元素指定如果值为负数，父元素应反转其颜色。
        """
        return getattr(self, qn('c:invertIfNegative'), None)

    @property
    def marker(self) -> Optional[CT_Marker]:
        """21.2.2.106 marker (标记)

        该元素指定数据标记。
        """
        return getattr(self, qn('c:marker'), None)

    @property
    def bubble_3d(self) -> Optional[CT_Boolean]:
        """21.2.2.19 bubble3D (3D气泡图)

        该元素指定气泡图应用了 3D 效果。
        """
        return getattr(self, qn('c:bubble3D'), None)

    @property
    def explosion(self) -> Optional[CT_UnsignedInt]:
        """21.2.2.61 explosion (爆炸)

        该元素指定数据点应从饼图中心移动的量。
        """
        return getattr(self, qn('c:explosion'), None)

    @property
    def sp_pr(self) -> Optional[a_CT_ShapeProperties]:
        """21.2.2.197 spPr (形状属性)

        此元素指定父图表元素的格式。 不支持 custGeom、prstGeom、scene3d 和 xfrm 元素。 不支持 bwMode 属性。
        """
        return getattr(self, qn('c:spPr'), None)

    @property
    def picture_options(self) -> Optional[CT_PictureOptions]:
        """21.2.2.138 pictureOptions (图片选项)

        此元素指定要在数据点、系列、墙壁或地板上使用的图片。
        """
        return getattr(self, qn('c:pictureOptions'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展列表"""
        return getattr(self, qn('c:extLst'))



class ST_TrendlineType(ST_BaseEnumType):
    """21.2.3.50 ST_TrendlineType (趋势线类型)

    这种简单类型指定可用于图表中系列的所有趋势线样式。
    """

    Exp = 'exp'
    """指定趋势线应为指数曲线，形式为 y = abx。"""

    Linear = 'linear'
    """指定趋势线应为形如 y = mx + b 的直线。"""

    Log = 'log'
    """指定趋势线应为形如 y = a log x + b 的对数曲线，其中 log 是自然对数。"""

    MovingAvg = 'movingAvg'
    """指定趋势线应为周期为Period的移动平均线。"""

    Poly = 'poly'
    """指定趋势线应为阶数为Order的多项式曲线，形式为y = ax6 + bx5 + cx4 + dx3 + ex2 + fx + g。"""

    Power = 'power'
    """指定趋势线应为幂曲线，形式为 y = axb。"""


class CT_TrendlineType(OxmlBaseElement):
    """21.2.2.213 trendlineType (趋势线类型)

    该元素指定趋势线的样式。
    """

    @property
    def val(self):
        """指定趋势线样式。"""
        _val = self.attrib.get('val', 'linear')

        return ST_TrendlineType(_val)  # type: ignore


ST_Order = NewType('ST_Order', int)
"""21.2.3.29 ST_Order (排序)

该简单类型指定其内容包含 2 到 6 之间的整数，其内容是趋势线多项式的阶数。

此简单类型的内容是 W3C XML 架构 unsignedByte 数据类型的限制。

这个简单类型还指定了以下限制：

- 此简单类型的最小值大于或等于 2。
- 此简单类型的最大值小于或等于 6。
"""


def to_ST_Order(val: AnyStr):
    intval = int(utils.AnyStrToStr(val))

    if not (2 <= intval <= 6):
        msg = f'预期外的值: {val}'
        raise OxmlAttributeValidateError(msg)

    return ST_Order(intval)


class CT_Order(OxmlBaseElement):
    """21.2.2.129 order (多项式趋势线阶数)

    该元素指定多项式趋势线的阶数。 对于其他趋势线类型，它会被忽略。
    """

    @property
    def val(self):
        """指定该属性的内容包含 2 到 6 之间的整数。"""
        _val = self.attrib.get('val', '2')

        return to_ST_Order(_val)  # type: ignore


ST_Period = NewType('ST_Period', int)
"""21.2.3.33 ST_Period (周期)

此简单类型指定其内容包含大于或等于 2 的整数。

此简单类型的内容是 W3C XML Schema unsignedInt 数据类型的限制。

这个简单类型还指定了以下限制：

此简单类型的最小值大于或等于 2。
"""


def to_ST_Period(val: AnyStr):
    intval = int(utils.AnyStrToStr(val))

    if intval < 2:
        msg = f'预期外的值: {val}'
        raise OxmlAttributeValidateError(msg)

    return ST_Period(intval)


class CT_Period(OxmlBaseElement):
    """21.2.2.135 period (周期)

    该元素指定移动平均趋势线的趋势线周期。 对于其他趋势线变体，它会被忽略。
    """

    @property
    def val(self):
        """指定移动平均趋势线的趋势线周期。 应包含 2 到 255 之间的整数。"""

        _val = self.attrib.get('val', '2')

        return to_ST_Period(_val)  # type: ignore


class CT_TrendlineLbl(OxmlBaseElement):
    """21.2.2.212 trendlineLbl (趋势线标签)

    该元素指定趋势线的标签。
    """

    @property
    def layout(self) -> Optional[CT_Layout]:
        return getattr(self, qn('c:layout'), None)

    @property
    def tx(self) -> Optional[CT_Tx]:
        return getattr(self, qn('c:tx'), None)

    @property
    def num_fmt(self) -> Optional[CT_NumFmt]:
        return getattr(self, qn('c:numFmt'), None)

    @property
    def sp_Pr(self) -> Optional[a_CT_ShapeProperties]:
        return getattr(self, qn('c:spPr'), None)

    @property
    def tx_pr(self) -> Optional[a_CT_TextBody]:
        return getattr(self, qn('c:txPr'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class CT_Trendline(OxmlBaseElement):
    """21.2.2.211 trendline (趋势线)

    该元素指定趋势线。
    """

    @property
    def name(self):
        """21.2.2.116 name (趋势线名称)

        该元素指定趋势线的名称。
        """
        ele: Optional[OxmlBaseElement] = getattr(self, qn('c:name'), None)

        if ele is None:
            return ''

        return ele.text

    @property
    def sp_Pr(self) -> Optional[a_CT_ShapeProperties]:
        """21.2.2.197 spPr (形状属性)

        此元素指定父图表元素的格式。

        不支持 custGeom、prstGeom、scene3d 和 xfrm 元素。

        不支持 bwMode 属性。
        """
        return getattr(self, qn('c:spPr'), None)

    @property
    def trendline_type(self) -> CT_TrendlineType:
        """21.2.2.213 trendlineType (趋势线类型)

        该元素指定趋势线的样式。
        """
        return getattr(self, qn('c:trendlineType'))


    @property
    def order(self) -> Optional[CT_Order]:
        """21.2.2.129 order (多项式趋势线阶数)

        该元素指定多项式趋势线的阶数。 对于其他趋势线类型，它会被忽略。
        """
        return getattr(self, qn('c:order'), None)

    @property
    def period(self) -> Optional[CT_Period]:
        """21.2.2.135 period (周期)

        该元素指定移动平均趋势线的趋势线周期。 对于其他趋势线变体，它会被忽略。
        """
        return getattr(self, qn('c:period'), None)

    @property
    def forward(self) -> Optional[CT_Double]:
        """21.2.2.73 forward (Forward)

        此元素指定趋势线在正在趋势化的系列数据之后延伸的类别数（或散点图上的单位数）。

        在散点图和非散点图上，该值应为任何非负值。
        """
        return getattr(self, qn('c:forward'), None)

    @property
    def backward(self) -> Optional[CT_Double]:
        """21.2.2.12 backward (Backward)

        此元素指定趋势线在正在趋势化的系列数据之前延伸的类别数（或散点图上的单位数）。

        在散点图和非散点图上，该值应为任何非负值。
        """
        return getattr(self, qn('c:backward'), None)

    @property
    def intercept(self) -> Optional[CT_Double]:
        """21.2.2.85 intercept (截距)

        该元素指定趋势线与 y 轴相交的值。 仅当趋势线类型为 exp、线性(linear)或 poly 时才支持此属性。
        """
        return getattr(self, qn('c:intercept'), None)

    @property
    def disp_rs_qr(self) -> Optional[CT_Double]:
        """21.2.2.44 dispRSqr (显示 R 平方值)

        该元素指定趋势线的R平方值在图表上显示（与方程式在同一标签中）。
        """
        return getattr(self, qn('c:dispRSqr'), None)

    @property
    def disp_eq(self) -> Optional[CT_Double]:
        """21.2.2.43 dispEq (显示方程)

        该元素指定在图表上显示趋势线的方程（与R平方值在同一标签中）。
        """
        return getattr(self, qn('c:dispEq'), None)

    @property
    def trendline_lbl(self) -> Optional[CT_TrendlineLbl]:
        """21.2.2.212 trendlineLbl (趋势线标签)

        该元素指定趋势线的标签。
        """
        return getattr(self, qn('c:trendlineLbl'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展元素列表"""
        return getattr(self, qn('c:extLst'))



class ST_ErrDir(ST_BaseEnumType):
    """21.2.3.13 ST_ErrDir (误差线方向)

    这个简单的类型指定了误差线的可能方向。
    """

    X = 'x'
    """指定误差线应显示在 x 方向。"""

    Y = 'y'
    """指定误差线应显示在 y 方向"""


class CT_ErrDir(OxmlBaseElement):
    """21.2.2.57 errDir (错误条方向)

    该元素指定误差线的方向。
    """

    @property
    def val(self):
        """指定误差线的方向。"""

        _val = self.attrib['val']

        return ST_ErrDir(_val)  # type: ignore


class ST_ErrBarType(ST_BaseEnumType):
    """21.2.3.12 ST_ErrBarType (误差线类型)

    这个简单的类型指定了绘制误差线的可能方法。
    """

    Both = 'both'
    """指定误差线应在正方向和负方向显示。"""

    Minus = 'minus'
    """指定误差线仅在负方向显示。"""

    Plus = 'plus'
    """指定误差线仅在正方向显示。"""


class CT_ErrBarType(OxmlBaseElement):
    """21.2.2.56 errBarType (错误条类型)

    该元素指定误差线的样式 - 正向、负向或两者皆有。
    """

    @property
    def val(self):
        """指定误差线的样式。"""
        _val = self.attrib.get('val', 'both')

        return ST_ErrBarType(_val)  # type: ignore


class ST_ErrValType(ST_BaseEnumType):
    """21.2.3.14 ST_ErrValType (错误值类型)

    这个简单的类型指定了确定误差线长度的可能方法
    """

    Cust = 'cust'
    """指定误差线的长度应由加号和减号元素确定。"""

    FixedVal = 'fixedVal'
    """指定误差条的长度应为由误差条值确定的固定值。"""

    Percentage = 'percentage'
    """指定误差线的长度应为数据的误差线值百分比。"""

    StdDev = 'stdDev'
    """指定误差条的长度应为数据的误差条值标准差。"""

    StErr = 'stdErr'
    """指定误差条的长度应为数据的误差条值标准误差。"""


class CT_ErrValType(OxmlBaseElement):
    """21.2.2.58 errValType (误差条数值类型)

    该元素指定用于确定误差线长度的值的类型。
    """

    @property
    def val(self):
        """指定误差线的值类型。"""

        _val = self.attrib.get('val', 'fixedVal')

        return ST_ErrValType(_val)  # type: ignore


class CT_ErrBars(OxmlBaseElement):
    """21.2.2.55 errBars (错误线)

    该元素指定误差线。errValType元素控制使用哪个元素：minus、plus或val。
    """

    @property
    def err_dir(self) -> Optional[CT_ErrDir]:
        """21.2.2.57 errDir (错误条方向)

        该元素指定误差线的方向。
        """
        return getattr(self, qn('c:errDir'), None)

    @property
    def err_bar_type(self) -> Optional[CT_ErrBarType]:
        """21.2.2.56 errBarType (错误条类型)

        该元素指定误差线的样式 - 正向、负向或两者皆有。
        """
        return getattr(self, qn('c:errBarType'), None)

    @property
    def err_val_type(self) -> Optional[CT_ErrValType]:
        """21.2.2.58 errValType (误差条数值类型)

        该元素指定用于确定误差线长度的值的类型。
        """
        return getattr(self, qn('c:errValType'), None)

    @property
    def no_end_cap(self) -> Optional[CT_Boolean]:
        """21.2.2.118 noEndCap (无端盖)

        该元素指定误差条上不绘制端盖。
        """
        return getattr(self, qn('c:noEndCap'), None)

    @property
    def plus(self) -> Optional[CT_NumDataSource]:
        """21.2.2.147 plus (加)

        该元素指定正方向的误差条值。 仅当 errValType 为自定义时才应使用它。
        """
        return getattr(self, qn('c:plus'), None)

    @property
    def minus(self) -> Optional[CT_NumDataSource]:
        """21.2.2.113 minus (减)

        该元素指定负方向的误差条值。 仅当 errValType 为自定义时才应使用它。
        """
        return getattr(self, qn('c:minus'), None)

    @property
    def val(self) -> Optional[CT_Double]:
        """21.2.2.225 val (误差条值)

        该元素指定与 errBar 元素一起使用的值以确定误差线的长度。
        """
        return getattr(self, qn('c:val'), None)

    @property
    def sp_pr(self) -> Optional[a_CT_ShapeProperties]:
        """21.2.2.197 spPr (形状属性)

        此元素指定父图表元素的格式。 不支持 custGeom、prstGeom、scene3d 和 xfrm 元素。 不支持 bwMode 属性。
        """
        return getattr(self, qn('c:spPr'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展列表"""
        return getattr(self, qn('c:extLst'))



class CT_UpDownBar(OxmlBaseElement):
    """21.2.2.217 upBars (向上柱状图)

    该元素指定图表上的上升条。
    """

    @property
    def sp_pr(self) -> Optional[a_CT_ShapeProperties]:
        return getattr(self, qn('c:spPr'), None)


class CT_UpDownBars(OxmlBaseElement):
    """21.2.2.218 upDownBars (上下柱状图)

    该元素指定向上和向下条形。
    """

    @property
    def gap_width(self) -> Optional[CT_GapAmount]:
        return getattr(self, qn('c:gapWidth'), None)

    @property
    def up_bars(self) -> Optional[CT_UpDownBar]:
        return getattr(self, qn('c:upBars'), None)

    @property
    def down_bars(self) -> Optional[CT_UpDownBar]:
        return getattr(self, qn('c:downBars'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class EG_SerShared(OxmlBaseElement):
    """系列 共享元素"""

    @property
    def idx(self) -> CT_UnsignedInt:
        """21.2.2.84 idx (索引)

        该元素指定包含元素的索引。 该索引应确定该元素适用于父集合的哪个子集合。
        """
        return getattr(self, qn('c:idx'))

    @property
    def order(self) -> CT_UnsignedInt:
        """
        21.2.2.128 order (排序) CT_UnsignedInt

        该元素指定集合中系列的顺序。 它是从 0 开始的。
        """
        return getattr(self, qn('c:order'))

    @property
    def tx(self) -> Optional[CT_SerTx]:
        """21.2.2.215 tx (系列文本) CT_SerTx

        此元素指定系列名称的文本，不带富文本格式。
        """
        return getattr(self, qn('c:tx'), None)

    @property
    def sp_pr(self) -> Optional[a_CT_ShapeProperties]:
        """21.2.2.197 spPr (形状属性)

        此元素指定父图表元素的格式。 不支持 custGeom、prstGeom、scene3d 和 xfrm 元素。 不支持 bwMode 属性。
        """
        return getattr(self, qn('c:spPr'), None)


class CT_LineSer(EG_SerShared):
    """21.2.2.171 ser (折线图系列)

    该元素指定折线图上的一系列。
    """

    @property
    def marker(self) -> Optional[CT_Marker]:
        """21.2.2.106 marker (标记)

        该元素指定数据标记。
        """
        return getattr(self, qn('c:marker'), None)

    @property
    def dpt(self) -> list[CT_DPt]:
        """21.2.2.52 dPt (数据点)

        该元素指定一个单独的数据点。
        """
        return self.findall(qn('c:dPt'))  # type: ignore

    @property
    def dlbls(self) -> Optional[CT_DLbls]:
        """21.2.2.49 dLbls (数据标签合集)

        该元素作为根元素，用于指定整个系列或整个图表的数据标签设置。它包含子元素，用于指定具体的格式和定位设置。
        """
        return getattr(self, qn('c:dLbls'), None)

    @property
    def trendline(self) -> list[CT_Trendline]:
        """21.2.2.211 trendline (趋势线)

        该元素指定趋势线。
        """
        return self.findall(qn('c:trendline'))  # type: ignore

    @property
    def err_bars(self) -> Optional[CT_ErrBars]:
        """21.2.2.55 errBars (错误线)

        该元素指定误差线。errValType元素控制使用哪个元素：minus、plus或val。
        """
        return getattr(self, qn('c:errBars'), None)

    @property
    def categries(self) -> Optional[CT_AxDataSource]:
        """21.2.2.24 cat (类别轴数据)

        该元素指定用于类别轴的数据。
        """
        return getattr(self, qn('c:cat'), None)

    @property
    def values(self) -> Optional[CT_NumDataSource]:
        """21.2.2.224 val (值集合)

        该元素指定用于定义图表上数据标记位置的数据值。
        """
        return getattr(self, qn('c:val'), None)

    @property
    def smooth(self) -> Optional[CT_Boolean]:
        """21.2.2.194 smooth (平滑)

        该元素指定连接图表上的点的线应使用 Catmull-Rom 样条线进行平滑。
        """
        return getattr(self, qn('c:smooth'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展列表"""
        return getattr(self, qn('c:extLst'))



class CT_ScatterSer(EG_SerShared):
    """21.2.2.167 ser (散点图系列)

    该元素指定了散点图上的一系列数据。
    """

    @property
    def marker(self) -> Optional[CT_Marker]:
        """21.2.2.106 marker (标记)

        该元素指定数据标记。
        """
        return getattr(self, qn('c:marker'), None)

    @property
    def dpt(self) -> list[CT_DPt]:
        """21.2.2.52 dPt (数据点)

        该元素指定一个单独的数据点。
        """
        return self.findall(qn('c:dPt'))  # type: ignore

    @property
    def dlbls(self) -> Optional[CT_DLbls]:
        """21.2.2.49 dLbls (数据标签合集)

        该元素作为根元素，用于指定整个系列或整个图表的数据标签设置。它包含子元素，用于指定具体的格式和定位设置。
        """
        return getattr(self, qn('c:dLbls'), None)

    @property
    def trendline(self) -> list[CT_Trendline]:
        """21.2.2.211 trendline (趋势线)

        该元素指定趋势线。
        """
        return self.findall(qn('c:trendline'))  # type: ignore

    @property
    def err_bars(self) -> Optional[CT_ErrBars]:
        """21.2.2.55 errBars (错误线)

        该元素指定误差线。errValType元素控制使用哪个元素：minus、plus或val。
        """
        return getattr(self, qn('c:errBars'), None)

    @property
    def x_val(self) -> Optional[CT_AxDataSource]:
        """21.2.2.234 xVal (X Values)

        该元素指定用于定义图表上数据标记位置的 x 值。
        """
        return getattr(self, qn('c:xVal'), None)

    @property
    def y_val(self) -> Optional[CT_AxDataSource]:
        """21.2.2.237 yVal (Y Values)

        该元素指定用于定义图表上数据标记位置的 y 值。
        """
        return getattr(self, qn('c:yVal'), None)

    @property
    def smooth(self) -> Optional[CT_Boolean]:
        """21.2.2.194 smooth (平滑)

        该元素指定连接图表上的点的线应使用 Catmull-Rom 样条线进行平滑。
        """
        return getattr(self, qn('c:smooth'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展元素列表"""
        return getattr(self, qn('c:extLst'))



class CT_RadarSer(EG_SerShared):
    """21.2.2.169 ser (雷达图系列)

    这个元素指定了雷达图上的一系列数据。
    """

    @property
    def marker(self) -> Optional[CT_Marker]:
        """21.2.2.106 marker (标记)

        该元素指定数据标记。
        """
        return getattr(self, qn('c:marker'), None)

    @property
    def dpt(self) -> list[CT_DPt]:
        """21.2.2.52 dPt (数据点)

        该元素指定一个单独的数据点。
        """
        return self.findall(qn('c:dPt'))  # type: ignore

    @property
    def dlbls(self) -> Optional[CT_DLbls]:
        """21.2.2.49 dLbls (数据标签合集)

        该元素作为根元素，用于指定整个系列或整个图表的数据标签设置。它包含子元素，用于指定具体的格式和定位设置。
        """
        return getattr(self, qn('c:dLbls'), None)

    @property
    def cat(self) -> Optional[CT_AxDataSource]:
        """21.2.2.24 cat (类别轴数据)

        该元素指定用于类别轴的数据。
        """
        return getattr(self, qn('c:cat'), None)

    @property
    def val(self) -> Optional[CT_NumDataSource]:
        """21.2.2.224 val (值集合)

        该元素指定用于定义图表上数据标记位置的数据值。
        """
        return getattr(self, qn('c:val'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展元素列表"""
        return getattr(self, qn('c:extLst'))



class CT_BarSer(EG_SerShared):
    """21.2.2.170 ser (柱状图系列)

    该元素指定了柱状图上的一系列数据。
    """

    @property
    def invert_if_gegative(self) -> Optional[CT_Boolean]:
        """21.2.2.86 invertIfNegative (如果为负则反转)

        该元素指定如果值为负数，父元素应反转其颜色。
        """
        return getattr(self, qn('c:invertIfNegative'), None)

    @property
    def picture_options(self) -> Optional[CT_PictureOptions]:
        """21.2.2.138 pictureOptions (图片选项)

        此元素指定要在数据点、系列、墙壁或地板上使用的图片。
        """
        return getattr(self, qn('c:pictureOptions'), None)

    @property
    def dpt(self) -> list[CT_DPt]:
        """21.2.2.52 dPt (数据点)

        该元素指定一个单独的数据点。
        """
        return self.findall(qn('c:dPt'))  # type: ignore

    @property
    def dlbls(self) -> Optional[CT_DLbls]:
        """21.2.2.49 dLbls (数据标签合集)

        该元素作为根元素，用于指定整个系列或整个图表的数据标签设置。它包含子元素，用于指定具体的格式和定位设置。
        """
        return getattr(self, qn('c:dLbls'), None)

    @property
    def trendline(self) -> list[CT_Trendline]:
        """21.2.2.211 trendline (趋势线)

        该元素指定趋势线。
        """
        return self.findall(qn('c:trendline'))  # type: ignore

    @property
    def err_bars(self) -> Optional[CT_ErrBars]:
        """21.2.2.55 errBars (错误线)

        该元素指定误差线。errValType元素控制使用哪个元素：minus、plus或val。
        """
        return getattr(self, qn('c:errBars'), None)

    @property
    def categries(self) -> Optional[CT_AxDataSource]:
        """21.2.2.24 cat (类别轴数据)

        该元素指定用于类别轴的数据。
        """

        return getattr(self, qn('c:cat'), None)

    @property
    def val(self) -> Optional[CT_NumDataSource]:
        """21.2.2.224 val (值集合)

        该元素指定用于定义图表上数据标记位置的数据值。
        """
        return getattr(self, qn('c:val'), None)

    @property
    def shape(self) -> Optional[CT_Shape]:
        """21.2.2.177 shape (形状)

        该元素指定系列或 3-D 条形图的形状。
        """
        return getattr(self, qn('c:shape'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展元素列表"""
        return getattr(self, qn('c:extLst'))



class CT_AreaSer(EG_SerShared):
    """21.2.2.168 ser (面积图系列)

    该元素指定了区域图上的一系列数据。
    """

    @property
    def picture_options(self) -> Optional[CT_PictureOptions]:
        """21.2.2.138 pictureOptions (图片选项)

        此元素指定要在数据点、系列、墙壁或地板上使用的图片。
        """
        return getattr(self, qn('c:pictureOptions'), None)

    @property
    def dpt(self) -> list[CT_DPt]:
        """21.2.2.52 dPt (数据点)

        该元素指定一个单独的数据点。
        """
        return self.findall(qn('c:dPt'))  # type: ignore

    @property
    def dlbls(self) -> Optional[CT_DLbls]:
        """21.2.2.49 dLbls (数据标签合集)

        该元素作为根元素，用于指定整个系列或整个图表的数据标签设置。它包含子元素，用于指定具体的格式和定位设置。
        """
        return getattr(self, qn('c:dLbls'), None)

    @property
    def trendline(self) -> list[CT_Trendline]:
        """21.2.2.211 trendline (趋势线)

        该元素指定趋势线。
        """
        return self.findall(qn('c:trendline'))  # type: ignore

    @property
    def err_bars(self) -> Optional[CT_ErrBars]:
        """21.2.2.55 errBars (错误线)

        该元素指定误差线。errValType元素控制使用哪个元素：minus、plus或val。
        """
        return getattr(self, qn('c:errBars'), None)

    @property
    def cat(self) -> Optional[CT_AxDataSource]:
        """21.2.2.24 cat (类别轴数据)

        该元素指定用于类别轴的数据。
        """
        return getattr(self, qn('c:cat'), None)

    @property
    def val(self) -> Optional[CT_NumDataSource]:
        """21.2.2.224 val (值集合)

        该元素指定用于定义图表上数据标记位置的数据值。
        """
        return getattr(self, qn('c:val'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展元素列表"""
        return getattr(self, qn('c:extLst'))



class CT_PieSer(EG_SerShared):
    """21.2.2.172 ser (饼图系列)

    该元素指定圆环图或饼图上的一系列。
    """

    @property
    def explosion(self) -> Optional[CT_UnsignedInt]:
        """21.2.2.61 explosion (爆炸)

        该元素指定数据点应从饼图中心移动的量。
        """
        return getattr(self, qn('c:explosion'), None)

    @property
    def dpt(self) -> list[CT_DPt]:
        """21.2.2.52 dPt (数据点)

        该元素指定一个单独的数据点。
        """
        return self.findall(qn('c:dPt'))  # type: ignore

    @property
    def dlbls(self) -> Optional[CT_DLbls]:
        """21.2.2.49 dLbls (数据标签合集)

        该元素作为根元素，用于指定整个系列或整个图表的数据标签设置。它包含子元素，用于指定具体的格式和定位设置。
        """
        return getattr(self, qn('c:dLbls'), None)

    @property
    def cat(self) -> Optional[CT_AxDataSource]:
        """21.2.2.24 cat (类别轴数据)

        该元素指定用于类别轴的数据。
        """
        return getattr(self, qn('c:cat'), None)

    @property
    def val(self) -> Optional[CT_NumDataSource]:
        """21.2.2.224 val (值集合)

        该元素指定用于定义图表上数据标记位置的数据值。
        """
        return getattr(self, qn('c:val'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展元素列表"""
        return getattr(self, qn('c:extLst'))



class CT_BubbleSer(EG_SerShared):
    """21.2.2.174 ser (气泡图系列)

    该元素指定气泡图上的一系列。
    """

    @property
    def invert_if_gegative(self) -> Optional[CT_Boolean]:
        """21.2.2.86 invertIfNegative (如果为负则反转)

        该元素指定如果值为负数，父元素应反转其颜色。
        """
        return getattr(self, qn('c:invertIfNegative'), None)

    @property
    def dpt(self) -> list[CT_DPt]:
        """21.2.2.52 dPt (数据点)

        该元素指定一个单独的数据点。
        """
        return self.findall(qn('c:dPt'))  # type: ignore

    @property
    def dlbls(self) -> Optional[CT_DLbls]:
        """21.2.2.49 dLbls (数据标签合集)

        该元素作为根元素，用于指定整个系列或整个图表的数据标签设置。它包含子元素，用于指定具体的格式和定位设置。
        """
        return getattr(self, qn('c:dLbls'), None)

    @property
    def trendline(self) -> list[CT_Trendline]:
        """21.2.2.211 trendline (趋势线)

        该元素指定趋势线。
        """
        return self.findall(qn('c:trendline'))  # type: ignore

    @property
    def err_bars(self) -> Optional[CT_ErrBars]:
        """21.2.2.55 errBars (错误线)

        该元素指定误差线。errValType元素控制使用哪个元素:minus、plus或val。
        """
        return getattr(self, qn('c:errBars'), None)

    @property
    def x_val(self) -> Optional[CT_AxDataSource]:
        """21.2.2.234 xVal (X Values)

        该元素指定用于定义图表上数据标记位置的 x 值。
        """
        return getattr(self, qn('c:xVal'), None)

    @property
    def y_val(self) -> Optional[CT_NumDataSource]:
        """21.2.2.237 yVal (Y Values)

        该元素指定用于定义图表上数据标记位置的 y 值。
        """
        return getattr(self, qn('c:yVal'), None)

    @property
    def bubble_size(self) -> Optional[CT_NumDataSource]:
        """21.2.2.22 bubbleSize (气泡大小)

        该元素指定气泡图上气泡大小的数据。
        """
        return getattr(self, qn('c:bubbleSize'), None)

    @property
    def bubble_3d(self) -> Optional[CT_Boolean]:
        """21.2.2.19 bubble3D (3D气泡图)

        该元素指定气泡图应用了 3D 效果。
        """
        return getattr(self, qn('c:bubble3D'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展元素列表"""
        return getattr(self, qn('c:extLst'))



class CT_SurfaceSer(EG_SerShared):
    """21.2.2.173 ser (曲面图系列)

    该元素指定曲面图上的一系列。
    """

    @property
    def cat(self) -> Optional[CT_AxDataSource]:
        """21.2.2.24 cat (类别轴数据)

        该元素指定用于类别轴的数据。
        """
        return getattr(self, qn('c:cat'), None)

    @property
    def val(self) -> Optional[CT_NumDataSource]:
        """21.2.2.224 val (值集合)

        该元素指定用于定义图表上数据标记位置的数据值。
        """
        return getattr(self, qn('c:val'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class ST_Grouping(ST_BaseEnumType):
    """21.2.3.17 ST_Grouping (分组)

    这个简单的类型指定条形图的可能分组。
    """

    PercentStacked = 'percentStacked'
    """指定图表系列沿值轴彼此相邻绘制并缩放至总计 100%。"""

    Standard = 'standard'
    """指定在值轴上绘制图表系列。"""

    Stacked = 'stacked'
    """指定图表系列在值轴上彼此相邻绘制。"""


class CT_Grouping(OxmlBaseElement):
    """21.2.2.76 grouping (分组)

    此元素指定柱形图、折线图或面积图的分组类型。
    """

    @property
    def val(self):
        """指定分组值。"""

        _val = self.attrib.get('val', 'standard')

        return ST_Grouping(_val)


class CT_ChartLines(OxmlBaseElement):
    """
    21.2.2.53 dropLines (下拉线)

    该元素指定了下拉线。

    21.2.2.80 hiLowLines (高低线)

    该元素指定系列的高低线。

    21.2.2.92 leaderLines (引导线)

    该元素指定数据标签的引导线。

    21.2.2.100 majorGridlines (主要网格线)

    该元素指定主要网格线。

    21.2.2.109 minorGridlines (次要网格线)

    该元素指定次网格线。

    21.2.2.176 serLines (系列线)

    该元素指定图表的系列线。
    """

    @property
    def sp_pr(self) -> Optional[a_CT_ShapeProperties]:
        """21.2.2.197 spPr (形状属性)

        此元素指定父图表元素的格式。 不支持 custGeom、prstGeom、scene3d 和 xfrm 元素。 不支持 bwMode 属性。
        """
        return getattr(self, qn('c:spPr'), None)


class EG_LineChartShared(OxmlBaseElement):
    tags = (
        qn('c:grouping'),  # CT_Grouping
        qn('c:varyColors'),  # CT_Boolean
        qn('c:ser'),  # CT_LineSer
        qn('c:dLbls'),  # CT_DLbls
        qn('c:dropLines'),  # CT_ChartLines
    )

    @property
    def grouping(self) -> CT_Grouping:
        """ "21.2.2.76 grouping (分组)

        此元素指定柱形图、折线图或面积图的分组类型。
        """
        return getattr(self, qn('c:grouping'))

    @property
    def vary_colors(self) -> Optional[CT_Boolean]:
        """21.2.2.227 varyColors (按点改变颜色)

        该元素指定系列中的每个数据标记具有不同的颜色。
        """
        return getattr(self, qn('c:varyColors'))

    @property
    def series(self) -> list[CT_LineSer]:
        """21.2.2.171 ser (折线图系列)

        该元素指定折线图上的一系列。
        """
        return getattr(self, qn('c:ser'))

    @property
    def dlbls(self) -> Optional[CT_DLbls]:
        """21.2.2.49 dLbls (数据标签合集)

        该元素作为根元素，用于指定整个系列或整个图表的数据标签设置。它包含子元素，用于指定具体的格式和定位设置。
        """
        return getattr(self, qn('c:dLbls'), None)

    @property
    def drop_lines(self) -> Optional[CT_ChartLines]:
        """21.2.2.53 dropLines (下拉线)

        该元素指定了下拉线。
        """
        return getattr(self, qn('c:dropLines'), None)


class CT_LineChart(EG_LineChartShared):
    """21.2.2.97 lineChart (折线图)

    该元素包含二维折线图系列。
    """

    @property
    def hi_low_lines(self) -> Optional[CT_ChartLines]:
        """21.2.2.80 hiLowLines (高低线)

        该元素指定系列的高低线。
        """
        return getattr(self, qn('c:hiLowLines'), None)

    @property
    def up_down_bars(self) -> Optional[CT_UpDownBars]:
        """21.2.2.218 upDownBars (上下柱状图)

        该元素指定向上和向下条形。
        """
        return getattr(self, qn('c:upDownBars'), None)

    @property
    def marker(self) -> Optional[CT_Boolean]:
        """21.2.2.105 marker (显示标记)

        该元素是一个布尔值，如果为 true，则指定应显示标记。
        """
        return getattr(self, qn('c:marker'), None)

    @property
    def smooth(self) -> Optional[CT_Boolean]:
        """21.2.2.194 smooth (平滑)

        该元素指定连接图表上的点的线应使用 Catmull-Rom 样条线进行平滑。
        """
        return getattr(self, qn('c:smooth'), None)

    @property
    def ax_id(self) -> tuple[CT_UnsignedInt, CT_UnsignedInt]:
        """21.2.2.9 axId (轴 ID)

        当指定为 valAx、dateAx、catAx 或 serAx 的子元素时，此元素指定轴的标识符。

        当指定为图表的子元素时，此元素指定定义图表坐标空间的轴的标识符。

        <xsd:element name="axId" type="CT_UnsignedInt" minOccurs="2" maxOccurs="2"/>
        """

        eles = self.findall(qn('c:axId'))

        if len(eles) != 2:
            msg = f'预期外的元素数量: {len(eles)}, 需要为 2'
            raise OxmlElementValidateError(msg)

        return eles[0], eles[1]  # type: ignore

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展列表"""
        return getattr(self, qn('c:extLst'))



class CT_Line3DChart(EG_LineChartShared):
    """21.2.2.96 line3DChart (3D 折线图)

    该元素包含 3D 折线图系列。
    """

    @property
    def gap_amount(self) -> Optional[CT_GapAmount]:
        return getattr(self, qn('c:gapDepth'), None)

    @property
    def ax_id(self) -> tuple[CT_UnsignedInt, CT_UnsignedInt, CT_UnsignedInt]:
        """
        <xsd:element name="axId" type="CT_UnsignedInt" minOccurs="3" maxOccurs="3"/>
        """

        eles = self.findall(qn('c:axId'))

        if len(eles) != 3:
            msg = f'预期外的元素数量: {len(eles)}, 需要为 3'
            raise OxmlElementValidateError(msg)

        return eles[0], eles[1], eles[2]  # type: ignore

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class CT_StockChart(OxmlBaseElement):
    """21.2.2.198 stockChart (股票图表)

    该元素包含股票图表系列的集合。
    """

    @property
    def series(self) -> list[CT_LineSer]:
        """
        <xsd:element name="ser" type="CT_LineSer" minOccurs="3" maxOccurs="4"/>
        """

        ele_lst = self.findall(qn('c:ser'))

        if not (3 <= len(ele_lst) <= 4):
            msg = f'预期外的元素数量: {len(ele_lst)}, 需要为 3或4'
            raise OxmlElementValidateError(msg)

        return ele_lst  # type: ignore

    @property
    def dlbls(self) -> Optional[CT_DLbls]:
        """21.2.2.49 dLbls (数据标签合集)

        该元素作为根元素，用于指定整个系列或整个图表的数据标签设置。它包含子元素，用于指定具体的格式和定位设置。
        """
        return getattr(self, qn('c:dLbls'), None)

    @property
    def drop_lines(self) -> Optional[CT_ChartLines]:
        return getattr(self, qn('c:dropLines'), None)

    @property
    def hi_low_lines(self) -> Optional[CT_ChartLines]:
        return getattr(self, qn('c:hiLowLines'), None)

    @property
    def up_down_bars(self) -> Optional[CT_UpDownBars]:
        return getattr(self, qn('c:upDownBars'), None)

    @property
    def ax_id(self) -> tuple[CT_UnsignedInt, CT_UnsignedInt]:
        """
        <xsd:element name="axId" type="CT_UnsignedInt" minOccurs="2" maxOccurs="2"/>
        """

        eles = self.findall(qn('c:axId'))

        if len(eles) != 2:
            msg = f'预期外的元素数量: {len(eles)}, 需要为 2'
            raise OxmlElementValidateError(msg)

        return eles[0], eles[1]  # type: ignore

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class ST_ScatterStyle(ST_BaseEnumType):
    """21.2.3.40 ST_ScatterStyle (散点图样式)

    这个简单的类型指定了散点图的可能样式。
    """

    none = 'none'
    """指定散点图上的点不得用直线连接，且不得绘制标记。"""

    Line = 'line'
    """指定散点图上的点应以直线连接，但不应绘制标记。"""

    LineMarker = 'lineMarker'
    """指定散点图上的点用直线连接并绘制标记。"""

    Marker = 'marker'
    """指定散点图上的点不应用线条连接，并且应绘制标记。"""

    Smooth = 'smooth'
    """指定散点图上的点应使用平滑线连接，并且不应绘制标记。"""

    SmoothMarker = 'smoothMarker'
    """指定散点图上的点应使用平滑线连接并绘制标记。"""


class CT_ScatterStyle(OxmlBaseElement):
    """21.2.2.162 scatterStyle (散射样式)

    该元素指定散点图中线条的类型。
    """

    @property
    def val(self):
        """指定散点图的样式。"""

        _val = self.attrib.get('val', 'marker')
        return ST_ScatterStyle(_val)


class CT_ScatterChart(OxmlBaseElement):
    """21.2.2.161 scatterChart (散点图)

    该元素包含了该图表的散点图系列。
    """

    @property
    def scatter_style(self) -> CT_ScatterStyle:
        return getattr(self, qn('c:scatterStyle'))

    @property
    def vary_colors(self) -> Optional[CT_Boolean]:
        return getattr(self, qn('c:varyColors'))

    @property
    def series(self) -> list[CT_ScatterSer]:
        return getattr(self, qn('c:ser'))

    @property
    def dlbls(self) -> Optional[CT_DLbls]:
        """21.2.2.49 dLbls (数据标签合集)

        该元素作为根元素，用于指定整个系列或整个图表的数据标签设置。它包含子元素，用于指定具体的格式和定位设置。
        """
        return getattr(self, qn('c:dLbls'), None)

    @property
    def ax_id(self) -> tuple[CT_UnsignedInt, CT_UnsignedInt]:
        """
        <xsd:element name="axId" type="CT_UnsignedInt" minOccurs="2" maxOccurs="2"/>
        """

        eles = self.findall(qn('c:axId'))

        if len(eles) != 2:
            msg = f'预期外的元素数量: {len(eles)}, 需要为 2'
            raise OxmlElementValidateError(msg)

        return eles[0], eles[1]  # type: ignore

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class ST_RadarStyle(ST_BaseEnumType):
    """21.2.3.37 ST_RadarStyle (雷达样式)

    这个简单的类型指定了雷达图的可能样式。
    """

    Standard = 'standard'
    """指定雷达图应有线条，但没有标记，也没有填充。"""

    Marker = 'marker'
    """指定雷达图应有线条和标记，但没有填充。"""

    Filled = 'filled'
    """指定雷达图应填充并有线条但没有标记。"""


class CT_RadarStyle(OxmlBaseElement):
    """21.2.2.154 radarStyle (雷达样式)

    该元素指定应绘制的雷达图类型。
    """

    @property
    def val(self):
        """指定雷达图的样式。"""

        _val = self.attrib.get('val', 'standard')
        return ST_RadarStyle(_val)


class CT_RadarChart(OxmlBaseElement):
    """21.2.2.153 radarChart (雷达图)

    该元素包含了该图表上的雷达图系列。
    """

    @property
    def radar_style(self) -> CT_RadarStyle:
        return getattr(self, qn('c:radarStyle'))

    @property
    def vary_colors(self) -> Optional[CT_Boolean]:
        return getattr(self, qn('c:varyColors'))

    @property
    def series(self) -> list[CT_RadarSer]:
        return getattr(self, qn('c:ser'))

    @property
    def dlbls(self) -> Optional[CT_DLbls]:
        """21.2.2.49 dLbls (数据标签合集)

        该元素作为根元素，用于指定整个系列或整个图表的数据标签设置。它包含子元素，用于指定具体的格式和定位设置。
        """
        return getattr(self, qn('c:dLbls'), None)

    @property
    def ax_id(self) -> tuple[CT_UnsignedInt, CT_UnsignedInt]:
        """
        <xsd:element name="axId" type="CT_UnsignedInt" minOccurs="2" maxOccurs="2"/>
        """

        eles = self.findall(qn('c:axId'))

        if len(eles) != 2:
            msg = f'预期外的元素数量: {len(eles)}, 需要为 2'
            raise OxmlElementValidateError(msg)

        return eles[0], eles[1]  # type: ignore

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class ST_BarGrouping(ST_BaseEnumType):
    """21.2.3.4 ST_BarGrouping (柱状(条形)图分组)

    这个简单的类型指定条形图的可能分组。
    """

    PercentStacked = 'percentStacked'
    """指定图表系列沿值轴彼此相邻绘制并缩放至总计 100%。"""

    Clustered = 'clustered'
    """指定图表系列沿类别轴彼此相邻绘制。"""

    Standard = 'standard'
    """指定图表系列在深度轴上彼此相邻绘制。"""

    Stacked = 'stacked'
    """指定图表系列在值轴上彼此相邻绘制。"""


class CT_BarGrouping(OxmlBaseElement):
    """21.2.2.77 grouping (条形图分组)

    该元素指定条形图的分组类型。
    """

    @property
    def val(self):
        """指定条形分组值。"""
        _val = self.attrib.get('val', 'clustered')
        return ST_BarGrouping(_val)


class ST_BarDir(ST_BaseEnumType):
    """21.2.3.3 ST_BarDir (柱状(条形)图方向)

    这种简单的类型指定条形图的可能方向。
    """

    Bar = 'bar'
    """指定图表是条形图 - 数据标记是水平矩形。"""

    Col = 'col'
    """指定图表是柱形图 - 数据标记是垂直矩形。"""


class CT_BarDir(OxmlBaseElement):
    """21.2.2.17 barDir (条形方向)

    该元素指定系列是形成条形图（水平）还是柱形图（垂直）
    """

    @property
    def val(self):
        """指定系列的方向。"""

        _val = self.attrib.get('val', 'col')
        return ST_BarDir(_val)


class ST_Shape(ST_BaseEnumType):
    """21.2.3.42 ST_Shape (形状)

    这个简单的类型指定了 3D 数据标记的可能形状。
    """

    Cone = 'cone'
    """指定图表应绘制为圆锥体，圆锥体的底部位于地板上，圆锥体的点位于数据标记的顶部。"""

    ConeToMax = 'coneToMax'
    """指定图表应使用截锥体绘制，以便锥体的点将是最大数据值。"""

    Box = 'box'
    """指定应使用方框形状绘制图表。"""

    Cylinder = 'cylinder'
    """指定图表应绘制为圆柱体。"""

    Pyramid = 'pyramid'
    """指定图表应绘制为矩形金字塔，金字塔的底部位于地板上，金字塔的点位于数据标记的顶部。"""

    PyramidToMax = 'pyramidToMax'
    """指定图表应使用截锥体绘制，以便锥体的点将是最大数据值。"""


class CT_Shape(OxmlBaseElement):
    """21.2.2.177 shape (形状)

    该元素指定系列或 3-D 条形图的形状。
    """

    @property
    def val(self):
        """指定系列的形状。"""
        _val = self.attrib.get('val', 'box')
        return ST_Shape(_val)


class EG_BarChartShared(OxmlBaseElement):
    tags = (
        qn('c:barDir'),  # CT_BarDir
        qn('c:grouping'),  # CT_BarGrouping
        qn('c:varyColors'),  # CT_Boolean
        qn('c:ser'),  # CT_BarSer
        qn('c:dLbls'),  # CT_DLbls
    )

    @property
    def bar_dir(self) -> CT_BarDir:
        return getattr(self, qn('c:barDir'))

    @property
    def grouping(self) -> Optional[CT_BarGrouping]:
        return getattr(self, qn('c:grouping'), None)

    @property
    def vary_colors(self) -> Optional[CT_Boolean]:
        return getattr(self, qn('c:varyColors'), None)

    @property
    def series(self) -> list[CT_BarSer]:
        return self.findall(qn('c:ser'))  # type: ignore

    @property
    def dlbls(self) -> Optional[CT_DLbls]:
        """21.2.2.49 dLbls (数据标签合集)

        该元素作为根元素，用于指定整个系列或整个图表的数据标签设置。它包含子元素，用于指定具体的格式和定位设置。
        """
        return getattr(self, qn('c:dLbls'), None)


class CT_BarChart(EG_BarChartShared):
    """21.2.2.16 barChart (条形图)

    此元素包含此图表上的二维条形图或柱形图系列。
    """

    @property
    def gap_width(self) -> Optional[CT_GapAmount]:
        return getattr(self, qn('c:gapWidth'), None)

    @property
    def overlap(self) -> Optional[CT_Overlap]:
        return getattr(self, qn('c:overlap'), None)

    @property
    def ser_lines(self) -> list[CT_ChartLines]:
        return self.findall(qn('c:serLines'))  # type: ignore

    @property
    def ax_id(self) -> tuple[CT_UnsignedInt, CT_UnsignedInt]:
        """
        <xsd:element name="axId" type="CT_UnsignedInt" minOccurs="2" maxOccurs="2"/>
        """

        eles = self.findall(qn('c:axId'))

        if len(eles) != 2:
            msg = f'预期外的元素数量: {len(eles)}, 需要为 2'
            raise OxmlElementValidateError(msg)

        return eles[0], eles[1]  # type: ignore

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class CT_Bar3DChart(EG_BarChartShared):
    """21.2.2.15 bar3DChart (3D 条形图)

    此元素包含此图表上的 3D 条形图或柱形图系列。
    """

    @property
    def gap_width(self) -> Optional[CT_GapAmount]:
        return getattr(self, qn('c:gapWidth'), None)

    @property
    def gap_depth(self) -> Optional[CT_GapAmount]:
        return getattr(self, qn('c:gapDepth'), None)

    @property
    def shape(self) -> Optional[CT_Shape]:
        return getattr(self, qn('c:shape'), None)

    @property
    def ax_id(self) -> tuple[CT_UnsignedInt, CT_UnsignedInt]:
        """
        <xsd:element name="axId" type="CT_UnsignedInt" minOccurs="2" maxOccurs="2"/>
        """

        eles = self.findall(qn('c:axId'))

        if len(eles) != 2:
            msg = f'预期外的元素数量: {len(eles)}, 需要为 2'
            raise OxmlElementValidateError(msg)

        return eles[0], eles[1]  # type: ignore

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class EG_AreaChartShared(OxmlBaseElement):
    tags = (
        qn('c:grouping'),  # CT_Grouping
        qn('c:varyColors'),  # CT_Boolean
        qn('c:ser'),  # CT_BarSer
        qn('c:dLbls'),  # CT_DLbls
        qn('c:dropLines'),  # CT_ChartLines
    )

    @property
    def grouping(self) -> Optional[CT_Grouping]:
        return getattr(self, qn('c:grouping'), None)

    @property
    def vary_colors(self) -> Optional[CT_Boolean]:
        return getattr(self, qn('c:varyColors'), None)

    @property
    def series(self) -> list[CT_BarSer]:
        return self.findall(qn('c:ser'))  # type: ignore

    @property
    def dlbls(self) -> Optional[CT_DLbls]:
        """21.2.2.49 dLbls (数据标签合集)

        该元素作为根元素，用于指定整个系列或整个图表的数据标签设置。它包含子元素，用于指定具体的格式和定位设置。
        """
        return getattr(self, qn('c:dLbls'), None)

    @property
    def drop_lines(self) -> Optional[CT_ChartLines]:
        return getattr(self, qn('c:dropLines'), None)


class CT_AreaChart(EG_AreaChartShared):
    """21.2.2.5 areaChart (面积图)

    此元素指定此图表上的二维区域系列。
    """

    @property
    def ax_id(self) -> tuple[CT_UnsignedInt, CT_UnsignedInt]:
        """
        <xsd:element name="axId" type="CT_UnsignedInt" minOccurs="2" maxOccurs="2"/>
        """

        eles = self.findall(qn('c:axId'))

        if len(eles) != 2:
            msg = f'预期外的元素数量: {len(eles)}, 需要为 2'
            raise OxmlElementValidateError(msg)

        return eles[0], eles[1]  # type: ignore

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class CT_Area3DChart(EG_AreaChartShared):
    """21.2.2.4 area3DChart (3D 面积图)

    该元素指定该图表上的 3D 区域系列。
    """

    @property
    def gap_depth(self) -> Optional[CT_GapAmount]:
        return getattr(self, qn('c:gapDepth'), None)

    @property
    def ax_id(self) -> list[CT_UnsignedInt]:
        """
        <xsd:element name="axId" type="CT_UnsignedInt" minOccurs="2" maxOccurs="3"/>
        """

        eles = self.findall(qn('c:axId'))

        if len(eles) not in {2, 3}:
            msg = f'预期外的元素数量: {len(eles)}, 需要为 2或3'
            raise OxmlElementValidateError(msg)

        return eles  # type: ignore

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class EG_PieChartShared(OxmlBaseElement):
    tags = (
        qn('c:varyColors'),  # CT_Boolean
        qn('c:ser'),  # CT_BarSer
        qn('c:dLbls'),  # CT_DLbls
    )

    @property
    def vary_colors(self) -> Optional[CT_Boolean]:
        return getattr(self, qn('c:varyColors'), None)

    @property
    def series(self) -> list[CT_BarSer]:
        return self.findall(qn('c:ser'))  # type: ignore

    @property
    def dlbls(self) -> Optional[CT_DLbls]:
        """21.2.2.49 dLbls (数据标签合集)

        该元素作为根元素，用于指定整个系列或整个图表的数据标签设置。它包含子元素，用于指定具体的格式和定位设置。
        """
        return getattr(self, qn('c:dLbls'), None)


class CT_PieChart(EG_PieChartShared):
    """21.2.2.141 pieChart (饼图)

    该元素包含该图表的二维饼图系列。
    """

    @property
    def first_slice_ang(self) -> Optional[CT_FirstSliceAng]:
        return getattr(self, qn('c:firstSliceAng'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class CT_Pie3DChart(EG_PieChartShared):
    """21.2.2.140 pie3DChart (3D饼图)

    此元素包含此图表的 3D 饼图系列。
    """

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class CT_DoughnutChart(EG_PieChartShared):
    """21.2.2.50 doughnutChart (甜甜圈图表)

    该元素包含甜甜圈图系列。
    """

    @property
    def first_slice_ang(self) -> Optional[CT_FirstSliceAng]:
        return getattr(self, qn('c:firstSliceAng'), None)

    @property
    def hole_size(self) -> Optional[CT_HoleSize]:
        return getattr(self, qn('c:holeSize'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class ST_OfPieType(ST_BaseEnumType):
    """21.2.3.28 ST_OfPieType (饼中饼或饼中条类型)

    这个简单类型指定饼图或饼图条形图的可能模式。
    """

    Pie = 'pie'
    """指定图表是饼图的饼图，而不是饼图的条形图。"""

    Bar = 'bar'
    """指定图表是条形饼图，而不是饼形饼图。"""


class CT_OfPieType(OxmlBaseElement):
    """21.2.2.127 ofPieType (饼中饼或饼中条类型)

    该元素指定该图表是饼图还是条形图。
    """

    def val(self):
        """指定饼图或饼图条形图的类型。"""

        _val = self.attrib.get('val', 'pie')

        return ST_OfPieType(_val)


class CT_OfPieChart(EG_PieChartShared):
    """21.2.2.126 ofPieChart (饼图或饼图条形图)

    此元素包含此图表上的饼图或饼图系列。 仅显示第一个系列。 splitType 元素应确定 splitPos 和 custSplit 元素是否适用。
    """

    @property
    def of_pie_type(self) -> CT_OfPieType:
        return getattr(self, qn('c:ofPieType'))

    @property
    def gap_width(self) -> Optional[CT_GapAmount]:
        return getattr(self, qn('c:gapWidth'), None)

    @property
    def split_type(self) -> Optional[CT_SplitType]:
        return getattr(self, qn('c:splitType'), None)

    @property
    def split_pos(self) -> Optional[CT_Double]:
        return getattr(self, qn('c:splitPos'), None)

    @property
    def cust_split(self) -> Optional[CT_CustSplit]:
        return getattr(self, qn('c:custSplit'), None)

    @property
    def second_pie_size(self) -> Optional[CT_SecondPieSize]:
        return getattr(self, qn('c:secondPieSize'), None)

    @property
    def ser_lines(self) -> list[CT_ChartLines]:
        return self.findall(qn('c:serLines'))  # type: ignore

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class CT_BubbleChart(OxmlBaseElement):
    """21.2.2.20 bubbleChart (气泡图)

    该元素包含该图表上的气泡系列。
    """

    @property
    def vary_colors(self) -> Optional[CT_Boolean]:
        return getattr(self, qn('c:varyColors'), None)

    @property
    def series(self) -> list[CT_BubbleSer]:
        return self.findall(qn('c:ser'))  # type: ignore

    @property
    def dlbls(self) -> Optional[CT_DLbls]:
        """21.2.2.49 dLbls (数据标签合集)

        该元素作为根元素，用于指定整个系列或整个图表的数据标签设置。它包含子元素，用于指定具体的格式和定位设置。
        """
        return getattr(self, qn('c:dLbls'), None)

    @property
    def bubble_3d(self) -> Optional[CT_Boolean]:
        return getattr(self, qn('c:bubble3D'), None)

    @property
    def bubble_scale(self) -> Optional[CT_BubbleScale]:
        return getattr(self, qn('c:bubbleScale'), None)

    @property
    def show_neg_bubbles(self) -> Optional[CT_Boolean]:
        return getattr(self, qn('c:showNegBubbles'), None)

    @property
    def size_represents(self) -> Optional[CT_SizeRepresents]:
        return getattr(self, qn('c:sizeRepresents'), None)

    @property
    def ax_id(self) -> tuple[CT_UnsignedInt, CT_UnsignedInt]:
        """
        <xsd:element name="axId" type="CT_UnsignedInt" minOccurs="2" maxOccurs="2"/>
        """

        eles = self.findall(qn('c:axId'))

        if len(eles) != 2:
            msg = f'预期外的元素数量: {len(eles)}, 需要为 2'
            raise OxmlElementValidateError(msg)

        return eles[0], eles[1]  # type: ignore

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class CT_BandFmt(OxmlBaseElement):
    """21.2.2.13 bandFmt (带格式)

    该元素指定曲面图的格式带。
    """

    @property
    def idx(self) -> CT_UnsignedInt:
        """21.2.2.84 idx (索引)

        该元素指定包含元素的索引。 该索引应确定该元素适用于父集合的哪个子集合。
        """
        return getattr(self, qn('c:idx'))

    @property
    def sp_pr(self) -> Optional[a_CT_ShapeProperties]:
        return getattr(self, qn('c:spPr'), None)


class CT_BandFmts(OxmlBaseElement):
    """21.2.2.14 bandFmts (带格式集合)

    此元素包含表面图表的格式化带的集合，索引从低到高。
    """

    @property
    def band_format(self) -> list[CT_BandFmt]:
        return self.findall(qn('c:bandFmt'))  # type: ignore


class EG_SurfaceChartShared(OxmlBaseElement):
    tags = (
        qn('c:wireframe'),  # CT_Boolean
        qn('c:ser'),  # CT_SurfaceSer
        qn('c:bandFmts'),  # CT_BandFmts
    )

    @property
    def wire_frame(self) -> Optional[CT_Boolean]:
        return getattr(self, qn('c:wireframe'), None)

    @property
    def series(self) -> list[CT_SurfaceSer]:
        return self.findall(qn('c:ser'))  # type: ignore

    @property
    def band_fmts(self) -> Optional[CT_BandFmts]:
        return getattr(self, qn('c:bandFmts'), None)


class CT_SurfaceChart(EG_SurfaceChartShared):
    """21.2.2.204 surfaceChart (曲面图)

    该元素包含一组二维等值线图。
    """

    @property
    def ax_id(self) -> list[CT_UnsignedInt]:
        """
        <xsd:element name="axId" type="CT_UnsignedInt" minOccurs="2" maxOccurs="2"/>
        """

        eles = self.findall(qn('c:axId'))

        if len(eles) not in {2, 3}:
            msg = f'预期外的元素数量: {len(eles)}, 需要为 2或3'
            raise OxmlElementValidateError(msg)

        return eles  # type: ignore

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class CT_Surface3DChart(EG_SurfaceChartShared):
    """21.2.2.203 surface3DChart (3D 曲面图)

    该元素包含一组 3-D 表面系列。
    """

    @property
    def ax_id(self) -> tuple[CT_UnsignedInt, CT_UnsignedInt, CT_UnsignedInt]:
        """
        <xsd:element name="axId" type="CT_UnsignedInt" minOccurs="3" maxOccurs="3"/>
        """

        eles = self.findall(qn('c:axId'))

        if len(eles) != 3:
            msg = f'预期外的元素数量: {len(eles)}, 需要为 3'
            raise OxmlElementValidateError(msg)

        return eles[0], eles[1], eles[2]  # type: ignore

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class ST_AxPos(ST_BaseEnumType):
    """21.2.3.2 ST_AxPos (轴位置)

    这个简单的类型指定轴的可能位置。
    """

    Bottom = 'b'
    """指定轴应显示在绘图区域的底部。"""

    Left = 'l'
    """指定轴应显示在绘图区域的左侧。"""

    Right = 'r'
    """指定轴应显示在绘图区域的右侧。"""

    Top = 't'
    """指定轴应显示在绘图区域的顶部。"""


class CT_AxPos(OxmlBaseElement):
    """21.2.2.10 axPos (轴位置)

    该元素指定图表上轴的位置。
    """

    @property
    def val(self):
        """指定图表上轴的位置。"""
        _val = self.attrib['val']
        return ST_AxPos(_val)


class ST_Crosses(ST_BaseEnumType):
    """21.2.3.8 ST_Crosses (交叉点)

    这个简单类型指定轴可能的交叉点。
    """

    AutoZero = 'autoZero'
    """类别轴与值轴的零点（如果可能）、最小值（如果最小值大于零）或最大值（如果最大值小于零）交叉。"""

    Max = 'max'
    """轴在最大值处相交"""

    Min = 'min'
    """轴在图表的最小值处交叉。"""


class CT_Crosses(OxmlBaseElement):
    """21.2.2.33 crosses (十字架)

    该元素指定了该轴如何与垂直轴相交。
    """

    @property
    def val(self):
        """指定轴与其垂直轴相交的位置。"""
        _val = self.attrib['val']
        return ST_Crosses(_val)


class ST_CrossBetween(ST_BaseEnumType):
    """21.2.3.7 ST_CrossBetween (交叉之间)

    这个简单类型指定轴可能的交叉状态。
    """

    Between = 'between'
    """指定值轴应与数据标记之间的类别轴交叉。"""

    MidCat = 'midCat'
    """指定值轴应在类别的中点与类别轴交叉。"""


class CT_CrossBetween(OxmlBaseElement):
    """21.2.2.32 crossBetween (交叉中间)

    该元素指定值轴是否在类别轴的类别之间交叉。

    如果未指定，则应用程序应选择适当的行为。
    """

    @property
    def val(self):
        """指定值轴是在类别之间还是在类别上交叉类别轴。"""
        _val = self.attrib['val']
        return ST_CrossBetween(_val)


class ST_TickMark(ST_BaseEnumType):
    """21.2.3.48 ST_TickMark (刻度线)

    这个简单的类型指定刻度线的可能位置。
    """

    Cross = 'cross'
    """指定刻度线应穿过轴。"""

    In = 'in'
    """指定刻度线应位于绘图区域内。"""

    none = 'none'
    """指定不得有刻度线。"""

    Out = 'out'
    """指定刻度线应位于绘图区域之外。"""


class CT_TickMark(OxmlBaseElement):
    """21.2.2.110 minorTickMark (次要刻度线)

    该元素指定轴的小刻度线。

    21.2.2.101 majorTickMark (主要刻度线)

    该元素指定主要刻度线。
    """

    @property
    def val(self):
        """指定次刻度标记位置。"""
        _val = self.attrib.get('val', 'cross')
        return ST_TickMark(_val)


class ST_TickLblPos(ST_BaseEnumType):
    """21.2.3.47 ST_TickLblPos (刻度标签位置)

    这个简单的类型指定刻度标签的可能位置。
    """

    High = 'high'
    """指定轴标签应位于垂直轴的高端。"""

    Low = 'low'
    """指定轴标签应位于垂直轴的低端。"""

    NextTo = 'nextTo'
    """指定轴标签应位于轴旁边。"""

    none = 'none'
    """指定不绘制轴标签。"""


class CT_TickLblPos(OxmlBaseElement):
    """21.2.2.207 tickLblPos (刻度标签位置)

    该元素指定刻度标签在轴上的位置。
    """

    @property
    def val(self):
        """指定刻度标签位置。"""
        _val = self.attrib.get('val', 'nextTo')
        return ST_TickLblPos(_val)


ST_Skip = NewType('ST_Skip', int)
"""21.2.3.44 ST_Skip (跳过)

此简单类型指定其内容包含大于或等于 1 的整数。

此简单类型的内容是 W3C XML Schema unsignedInt 数据类型的限制。

这个简单类型还指定了以下限制：

- 此简单类型的最小值大于或等于 1。
"""


def to_ST_Skip(val: AnyStr):
    intval = int(utils.AnyStrToStr(val))

    if intval < 1:
        msg = f'预期外的值: {val}'
        raise OxmlAttributeValidateError(msg)

    return ST_Skip(intval)


class CT_Skip(OxmlBaseElement):
    """21.2.2.208 tickLblSkip (勾选标签跳过)

    此元素指定在绘制的标签之间跳过多少个刻度标签。

    21.2.2.209 tickMarkSkip (跳过刻度线)

    该元素指定在绘制下一个刻度线之前应跳过多少个刻度线。
    """

    @property
    def val(self):
        """指定在绘制的标签之间要跳过的刻度标签数量。 应包含大于或等于 1 的整数。"""
        _val = self.attrib['val']

        return to_ST_Skip(_val)  # type: ignore


class ST_TimeUnit(ST_BaseEnumType):
    """21.2.3.49 ST_TimeUnit (时间单位)

    这个简单的类型指定一个时间单位。
    """

    Days = 'days'
    """指定图表数据应以天为单位显示。"""

    Months = 'months'
    """指定图表数据应以月为单位显示。"""

    Years = 'years'
    """指定图表数据应以年为单位显示。"""


class CT_TimeUnit(OxmlBaseElement):
    """21.2.2.18 baseTimeUnit (基准时间单位)

    该元素指定日期轴上表示的最小时间单位。

    21.2.2.102 majorTimeUnit (主要时间单位)

    该元素指定主要刻度线的时间单位。

    21.2.2.111 minorTimeUnit (次要时间单位)

    该元素指定小刻度线的时间单位。
    """

    @property
    def val(self):
        """指定刻度线的时间单位。"""
        _val = self.attrib.get('val', 'days')
        return ST_TimeUnit(_val)


ST_AxisUnit = NewType('ST_AxisUnit', int)
"""21.2.3.1 ST_AxisUnit (轴单位)

此简单类型指定其内容包含正浮点数。

此简单类型的内容是 W3C XML Schema 双数据类型的限制。

这个简单类型还指定了以下限制：

此简单类型的最小值大于 0。
"""


def to_ST_AxisUnit(val: Any):
    intval = int(utils.AnyStrToStr(val))

    if intval < 0:
        msg = f'预期外的值: {val}'
        raise OxmlAttributeValidateError(msg)

    return ST_Skip(intval)


class CT_AxisUnit(OxmlBaseElement):
    """21.2.2.103 majorUnit (主要单位)

    该元素指定主要刻度之间的距离。

    21.2.2.112 minorUnit (次要单位)

    该元素指定小刻度线之间的距离。
    """

    @property
    def val(self):
        """指定主要刻度之间的距离。 应包含正浮点数。"""
        _val = self.attrib['val']

        return to_ST_AxisUnit(_val)  # type: ignore


class ST_BuiltInUnit(ST_BaseEnumType):
    """21.2.3.6 ST_BuiltInUnit (内置单位)

    这种简单类型指定轴的内置显示单位。
    """

    Hundreds = 'hundreds'
    """指定图表上的值应除以 100。"""

    Thousands = 'thousands'
    """指定图表上的值应除以 1,000。"""

    TenThousands = 'tenThousands'
    """指定图表上的值应除以 10,000。"""

    HundredThousands = 'hundredThousands'
    """指定图表上的值应除以 100,000。"""

    Millions = 'millions'
    """指定图表上的值应除以 1,000,000。"""

    TenMillions = 'tenMillions'
    """指定图表上的值应除以 10,000,000。"""

    HundredMillions = 'hundredMillions'
    """指定图表上的值应除以 100,000,000。"""

    Billions = 'billions'
    """指定图表上的值应除以 1,000,000,000。"""

    Trillions = 'trillions'
    """指定图表上的值应除以 1,000,000,000,000。"""


class CT_BuiltInUnit(OxmlBaseElement):
    """21.2.2.23 builtInUnit (内置显示单位值)

    该元素指定显示单位是内置值之一。
    """

    @property
    def val(self):
        """指定应用于轴的显示单位缩放。"""

        _val = self.attrib.get('val', 'thousands')
        return ST_BuiltInUnit(_val)


class ST_PictureFormat(ST_BaseEnumType):
    """21.2.3.35 ST_PictureFormat (图片格式)

    这种简单的类型指定了将图片放置在数据点、系列、墙壁或地板上的可能方法。
    """

    Stretch = 'stretch'
    """指定图片应进行各向异性拉伸以填充数据点、系列、墙壁或地板。"""

    Stack = 'stack'
    """指定图片应堆叠。"""

    StackScale = 'stackScale'
    """指定图片缩放后堆叠，使其高度为一个图片堆叠单元。 不适用于墙壁或地板。"""


class CT_PictureFormat(OxmlBaseElement):
    """21.2.2.137 pictureFormat (图片格式)

    该元素指定图片在数据点、系列、墙壁或地板上的拉伸和堆叠。
    """

    @property
    def val(self):
        """指定图片的拉伸和堆叠。"""
        _val = self.attrib['val']
        return ST_PictureFormat(_val)


ST_PictureStackUnit = NewType('ST_PictureStackUnit', int)
"""21.2.3.36 ST_PictureStackUnit (图片堆栈单元)

此简单类型指定其内容包含大于零的浮点数。

此简单类型的内容是 W3C XML Schema 双数据类型的限制。

这个简单类型还指定了以下限制：

- 此简单类型的最小值大于 0。
"""


def to_ST_PictureStackUnit(val: Any):
    intval = int(utils.AnyStrToStr(val))

    if intval < 0:
        msg = f'预期外的值: {val}'
        raise OxmlAttributeValidateError(msg)

    return ST_PictureStackUnit(intval)


class CT_PictureStackUnit(OxmlBaseElement):
    """21.2.2.139 pictureStackUnit (图片堆栈单元)

    该元素指定图表上每张图片的单位。 仅当图片格式为“堆栈”和“缩放”时，此元素才适用。
    """

    @property
    def val(self):
        """指定图表上每张图片的单位。 应包含浮点数。"""

        _val = self.attrib['val']
        return to_ST_PictureStackUnit(_val)


class CT_PictureOptions(OxmlBaseElement):
    """21.2.2.138 pictureOptions (图片选项)

    此元素指定要在数据点、系列、墙壁或地板上使用的图片。
    """

    @property
    def apply_to_front(self) -> Optional[CT_Boolean]:
        return getattr(self, qn('c:applyToFront'), None)

    @property
    def apply_to_slides(self) -> Optional[CT_Boolean]:
        return getattr(self, qn('c:applyToSides'), None)

    @property
    def apply_to_end(self) -> Optional[CT_Boolean]:
        return getattr(self, qn('c:applyToEnd'), None)

    @property
    def picture_format(self) -> Optional[CT_PictureFormat]:
        return getattr(self, qn('c:pictureFormat'), None)

    @property
    def picture_stack_unit(self) -> Optional[CT_PictureStackUnit]:
        return getattr(self, qn('c:pictureStackUnit'), None)


class CT_DispUnitsLbl(OxmlBaseElement):
    """21.2.2.46 dispUnitsLbl (显示单元标签)

    该元素指定了指定图表中值轴的显示单位标签。
    """

    @property
    def layout(self) -> Optional[CT_Layout]:
        """21.2.2.88 layout (布局)

        此元素指定图表元素如何放置在图表上。
        """
        return getattr(self, qn('c:layout'), None)

    @property
    def tx(self) -> Optional[CT_Tx]:
        """21.2.2.214 tx (图表文本)

        此元素指定要在图表上使用的文本，包括富文本格式。
        """
        return getattr(self, qn('c:tx'), None)

    @property
    def sp_pr(self) -> Optional[a_CT_ShapeProperties]:
        """21.2.2.197 spPr (形状属性)

        此元素指定父图表元素的格式。 不支持 custGeom、prstGeom、scene3d 和 xfrm 元素。 不支持 bwMode 属性。
        """
        return getattr(self, qn('c:spPr'), None)

    @property
    def tx_pr(self) -> Optional[a_CT_TextBody]:
        """21.2.2.216 txPr (文本属性)

        该元素指定文本格式。 不支持 lstStyle 元素。
        """
        return getattr(self, qn('c:txPr'), None)


class CT_DispUnits(OxmlBaseElement):
    """21.2.2.45 dispUnits (显示单元)

    该元素指定了值轴的显示单位的缩放值。
    """

    @property
    def unit(self) -> CT_Double | CT_BuiltInUnit:
        ele: CT_Double | CT_BuiltInUnit = getattr(self, qn('c:custUnit'))  # CT_Double

        if ele is None:
            ele = getattr(self, qn('c:builtInUnit'))  # CT_BuiltInUnit

        if ele is None:
            msg = '至少需要一个节点, custUnit 或 builtInUnit'
            raise OxmlElementValidateError(msg)

        return ele

    @property
    def disp_units_lbl(self) -> Optional[CT_DispUnitsLbl]:
        return getattr(self, qn('c:dispUnitsLbl'))

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class ST_Orientation(ST_BaseEnumType):
    """21.2.3.30 ST_Orientation (方向)

    这种简单的类型指定了将图片放置在数据点、系列、墙壁或地板上的可能方法。
    """

    MaxMin = 'maxMin'
    """指定轴上的值应反转，以便它们从最大值变为最小值。"""

    MinMax = 'minMax'
    """指定轴值应按通常的顺序，从最小值到最大值。"""


class CT_Orientation(OxmlBaseElement):
    """21.2.2.130 orientation (轴方向)

    该元素指定图片在数据点、系列、墙壁或地板上的拉伸和堆叠。
    """

    @property
    def val(self):
        """指定轴的方向。"""
        _val = self.attrib.get('val', 'minMax')
        return ST_Orientation(_val)


ST_LogBase = NewType('ST_LogBase', int)
"""21.2.3.25 ST_LogBase (对数底)

此简单类型指定其内容包含大于或等于 2 的浮点数。

此简单类型的内容是 W3C XML Schema 双数据类型的限制。

这个简单类型还指定了以下限制：

- 此简单类型的最大值小于或等于 1000。
- 此简单类型的最小值大于或等于 2。
"""


def to_ST_LogBase(val: Any):
    _val = utils.AnyStrToStr(val)

    intval = int(_val)

    if not (2 <= intval <= 1000):
        msg = '预期外的值, 应 <=2 并且 >=1000'
        raise OxmlAttributeValidateError(msg)

    return ST_LogBase(intval)


class CT_LogBase(OxmlBaseElement):
    """21.2.2.98 logBase (对数底)

    该元素指定对数轴的对数底。
    """

    @property
    def val(self):
        """指定对数轴的对数底。 应包含大于或等于 2 的浮点值。"""
        _val = self.attrib['val']
        return to_ST_LogBase(_val)


class CT_Scaling(OxmlBaseElement):
    """21.2.2.160 scaling (缩放)

    该元素包含额外的轴设置。
    """

    @property
    def log_base(self) -> Optional[CT_LogBase]:
        """21.2.2.98 logBase (对数底)

        该元素指定对数轴的对数底。
        """
        return getattr(self, qn('c:logBase'), None)

    @property
    def orientation(self) -> Optional[CT_Orientation]:
        """21.2.2.130 orientation (轴方向)

        该元素指定图片在数据点、系列、墙壁或地板上的拉伸和堆叠。
        """
        return getattr(self, qn('c:orientation'), None)

    @property
    def max(self) -> Optional[CT_Double]:
        """21.2.2.107 max (最大值)

        该元素指定轴的最大值。
        """
        return getattr(self, qn('c:max'), None)

    @property
    def min(self) -> Optional[CT_Double]:
        """21.2.2.108 min (最小值)

        该元素指定轴的最小值。
        """
        return getattr(self, qn('c:min'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展元素列表"""
        return getattr(self, qn('c:extLst'))



ST_LblOffset = Union[str, int]
"""21.2.3.23 ST_LblOffset (标签偏移)

此简单类型指定其内容包含默认值的百分比，介于 0% 和 1000% 之间。

这个简单类型是以下类型的联合：

ST_LblOffsetPercent 简单类型 (§21.2.3.56)
"""
# <xsd:union memberTypes="ST_LblOffsetPercent ST_LblOffsetUShort"/>


ST_LblOffsetPercent = NewType('ST_LblOffsetPercent', str)
"""21.2.3.56 ST_LblOffsetPercent (标签偏移百分比)

此简单类型指定其内容包含 0% 到 1000% 之间的百分比。

简单类型的内容应与以下正则表达式模式匹配：

0*(([0-9])|([1-9][0-9])|([1-9][0-9][0-9])|1000)%.
"""


def to_ST_LblOffsetPercent(val: Any):
    return ST_LblOffsetPercent(utils.AnyStrToStr(val))


ST_LblOffsetUShort = NewType('ST_LblOffsetUShort', int)


def to_ST_LblOffsetUShort(val: Any):
    _val = int(utils.AnyStrToStr(val))

    if not (0 <= _val <= 1000):
        msg = '预期外的值, 应在范围: 0-1000内'
        raise OxmlAttributeValidateError(msg)

    return ST_LblOffsetUShort(_val)


class CT_LblOffset(OxmlBaseElement):
    """21.2.2.91 lblOffset (标签偏移)

    该元素指定标签距轴的距离。
    """

    @property
    def val(self):
        """指定标签距轴的距离。 应包含 0% 到 1000% 之间的百分比。"""

        _val = utils.AnyStrToStr(self.attrib.get('val', '100%'))  # type: ignore

        if _val.endswith('%'):
            return to_ST_LblOffsetPercent(_val)

        return to_ST_LblOffsetUShort(_val)


class EG_AxShared(OxmlBaseElement):
    """轴共享标签"""

    @property
    def ax_id(self) -> CT_UnsignedInt:
        """21.2.2.9 axId (轴 ID)

        当指定为 valAx、dateAx、catAx 或 serAx 的子元素时，此元素指定轴的标识符。

        当指定为图表的子元素时，此元素指定定义图表坐标空间的轴的标识符。
        """
        return getattr(self, qn('c:axId'))

    @property
    def scaling(self) -> CT_Scaling:
        """21.2.2.160 scaling (缩放)

        该元素包含额外的轴设置。
        """
        return getattr(self, qn('c:scaling'))

    @property
    def delete(self) -> Optional[CT_Boolean]:
        """21.2.2.40 delete (删除)

        该元素指定其包含元素指定的图表元素将从图表中删除。

        如果应用程序在用户指定应从图表中删除这些元素后仍默认添加它们，则应将其设置为true。
        """
        return getattr(self, qn('c:delete'), None)

    @property
    def ax_pos(self) -> CT_AxPos:
        """21.2.2.10 axPos (轴位置)

        该元素指定图表上轴的位置。
        """
        return getattr(self, qn('c:axPos'))

    @property
    def major_gridlines(self) -> Optional[CT_ChartLines]:
        """21.2.2.100 majorGridlines (主要网格线)

        该元素指定主要网格线。
        """
        return getattr(self, qn('c:majorGridlines'), None)

    @property
    def minor_gridlines(self) -> Optional[CT_ChartLines]:
        """21.2.2.109 minorGridlines (次要网格线)

        该元素指定次网格线。
        """
        return getattr(self, qn('c:minorGridlines'), None)

    @property
    def title(self) -> Optional[CT_Title]:
        """21.2.2.210 title (标题)

        该元素指定一个标题。
        """
        return getattr(self, qn('c:title'), None)

    @property
    def num_fmt(self) -> Optional[CT_NumFmt]:
        """21.2.2.121 numFmt (数字格式)

        该元素指定父元素的数字格式。
        """
        return getattr(self, qn('c:numFmt'), None)

    @property
    def major_tick_mark(self) -> Optional[CT_TickMark]:
        """21.2.2.101 majorTickMark (主要刻度线)

        该元素指定主要刻度线。
        """
        return getattr(self, qn('c:majorTickMark'), None)

    @property
    def minor_tick_mark(self) -> Optional[CT_TickMark]:
        """21.2.2.110 minorTickMark (次要刻度线)

        该元素指定轴的小刻度线。
        """
        return getattr(self, qn('c:minorTickMark'), None)

    @property
    def tick_lbl_pos(self) -> Optional[CT_TickLblPos]:
        """21.2.2.207 tickLblPos (刻度标签位置)

        该元素指定刻度标签在轴上的位置。
        """
        return getattr(self, qn('c:tickLblPos'), None)

    @property
    def sp_pr(self) -> Optional[a_CT_ShapeProperties]:
        """21.2.2.197 spPr (形状属性)

        此元素指定父图表元素的格式。

        不支持 custGeom、prstGeom、scene3d 和 xfrm 元素。 不支持 bwMode 属性。
        """
        return getattr(self, qn('c:spPr'), None)

    @property
    def tx_pr(self) -> Optional[a_CT_TextBody]:
        """21.2.2.216 txPr (文本属性)

        该元素指定文本格式。 不支持 lstStyle 元素。
        """
        return getattr(self, qn('c:txPr'), None)

    @property
    def cross_ax(self) -> CT_UnsignedInt:
        """21.2.2.31 crossAx (交叉轴 ID)

        该元素指定了该轴所穿越的轴的ID。例如，一个分类轴可能会穿越一个值轴，而分类轴的crossAx属性将包含值轴的ID。
        """
        return getattr(self, qn('c:crossAx'))

    @property
    def cross(self) -> Optional[CT_Crosses | CT_Double]:
        """21.2.2.33 crosses (十字架)

        该元素指定了该轴如何与垂直轴相交。

        21.2.2.34 crossesAt (穿越值)

        该元素指定了垂直轴与轴线相交的位置。单位取决于轴的类型。

        当作为valAx的子元素指定时，该值是值轴上的十进制数。

        当作为dateAx的子元素指定时，日期被定义为相对于当前日期系统的基准日期的整数天数。

        当作为catAx的子元素指定时，该值是一个整数类别编号，从1开始作为第一个类别。
        """

        tags = (
            qn('c:crosses'),
            qn('c:crossesAt'),
        )

        return self.choice_one_child(*tags)  # type: ignore


class CT_CatAx(EG_AxShared):
    """21.2.2.25 catAx (类别轴数据)

    该元素指定图表的类别轴。
    """

    @property
    def auto(self) -> Optional[CT_Boolean]:
        """21.2.2.6 auto (自动分类轴)

        此元素指定该轴是基于用于轴标签的数据的日期轴或文本轴，而不是特定的选择。
        """
        return getattr(self, qn('c:auto'), None)

    @property
    def lbl_algn(self) -> Optional[CT_LblAlgn]:
        """21.2.2.90 lblAlgn (标签对齐)

        该元素指定轴上刻度标签的文本对齐方式。
        """
        return getattr(self, qn('c:lblAlgn'), None)

    @property
    def lbl_offset(self) -> Optional[CT_LblOffset]:
        """21.2.2.91 lblOffset (标签偏移)

        该元素指定标签距轴的距离。
        """
        return getattr(self, qn('c:lblOffset'), None)

    @property
    def tick_lbl_skip(self) -> Optional[CT_Skip]:
        """21.2.2.208 tickLblSkip (勾选标签跳过)

        此元素指定在绘制的标签之间跳过多少个刻度标签。
        """
        return getattr(self, qn('c:tickLblSkip'), None)

    @property
    def tick_mark_skip(self) -> Optional[CT_Skip]:
        """21.2.2.209 tickMarkSkip (跳过刻度线)

        该元素指定在绘制下一个刻度线之前应跳过多少个刻度线。
        """
        return getattr(self, qn('c:tickMarkSkip'), None)

    @property
    def no_multi_lvl_lbl(self) -> Optional[CT_Boolean]:
        """21.2.2.119 noMultiLvlLbl (无多级标签)

        该元素指定标签应显示为平面文本。 如果不包含此元素或设置为 false，则标签应绘制为层次结构。
        """
        return getattr(self, qn('c:noMultiLvlLbl'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展元素列表"""
        return getattr(self, qn('c:extLst'))



class CT_DateAx(EG_AxShared):
    """21.2.2.39 dateAx (日期轴)

    该元素指定图表的日期轴。
    """

    @property
    def auto(self) -> Optional[CT_Boolean]:
        """21.2.2.6 auto (自动分类轴)

        此元素指定该轴是基于用于轴标签的数据的日期轴或文本轴，而不是特定的选择。
        """
        return getattr(self, qn('c:auto'), None)

    @property
    def lbl_offset(self) -> Optional[CT_LblOffset]:
        return getattr(self, qn('c:lblOffset'), None)

    @property
    def base_time_unit(self) -> Optional[CT_TimeUnit]:
        return getattr(self, qn('c:baseTimeUnit'), None)

    @property
    def major_unit(self) -> Optional[CT_AxisUnit]:
        return getattr(self, qn('c:majorUnit'), None)

    @property
    def major_time_unit(self) -> Optional[CT_TimeUnit]:
        return getattr(self, qn('c:majorTimeUnit'), None)

    @property
    def minor_unit(self) -> Optional[CT_AxisUnit]:
        return getattr(self, qn('c:minorUnit'), None)

    @property
    def minor_time_unit(self) -> Optional[CT_TimeUnit]:
        return getattr(self, qn('c:minorTimeUnit'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class CT_SerAx(EG_AxShared):
    """21.2.2.175 serAx (系列轴)

    该元素指定图表的系列轴。
    """

    @property
    def tick_lbl_skip(self) -> Optional[CT_Skip]:
        return getattr(self, qn('c:tickLblSkip'), None)

    @property
    def tick_mark_skip(self) -> Optional[CT_Skip]:
        return getattr(self, qn('c:tickMarkSkip'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class CT_ValAx(EG_AxShared):
    """21.2.2.226 valAx (值轴)

    该元素指定一个值轴。
    """

    @property
    def cross_between(self) -> Optional[CT_CrossBetween]:
        """21.2.2.32 crossBetween (交叉中间)

        该元素指定值轴是否在类别轴的类别之间交叉。

        如果未指定，则应用程序应选择适当的行为。
        """
        return getattr(self, qn('c:crossBetween'), None)

    @property
    def major_unit(self) -> Optional[CT_AxisUnit]:
        """21.2.2.103 majorUnit (主要单位)

        该元素指定主要刻度之间的距离。
        """
        return getattr(self, qn('c:majorUnit'), None)

    @property
    def minor_unit(self) -> Optional[CT_AxisUnit]:
        """21.2.2.112 minorUnit (次要单位)

        该元素指定小刻度线之间的距离。
        """
        return getattr(self, qn('c:minorUnit'), None)

    @property
    def disp_units_lbl(self) -> Optional[CT_DispUnitsLbl]:
        """21.2.2.46 dispUnitsLbl (显示单元标签)

        该元素指定了指定图表中值轴的显示单位标签。
        """
        return getattr(self, qn('c:dispUnitsLbl'))

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展元素列表"""
        return getattr(self, qn('c:extLst'))



class CT_PlotArea(OxmlBaseElement):
    """21.2.2.145 plotArea (绘图区域)

    该元素指定图表的绘图区域。
    """

    @property
    def layout(self) -> Optional[CT_Layout]:
        """21.2.2.88 layout (布局)

        此元素指定图表元素如何放置在图表上。
        """
        return getattr(self, qn('c:layout'))

    @property
    def chart(
        self,
    ) -> list[
        CT_AreaChart | CT_Area3DChart | CT_LineChart | CT_Line3DChart | CT_StockChart | CT_RadarChart | CT_ScatterChart | CT_PieChart | CT_Pie3DChart | CT_DoughnutChart | CT_BarChart | CT_Bar3DChart | CT_OfPieChart | CT_SurfaceChart | CT_Surface3DChart | CT_BubbleChart
    ]:
        """具体的图表"""
        tags = (
            qn('c:areaChart'),  # CT_AreaChart
            qn('c:area3DChart'),  # CT_Area3DChart
            qn('c:lineChart'),  # CT_LineChart
            qn('c:line3DChart'),  # CT_Line3DChart
            qn('c:stockChart'),  # CT_StockChart
            qn('c:radarChart'),  # CT_RadarChart
            qn('c:scatterChart'),  # CT_ScatterChart
            qn('c:pieChart'),  # CT_PieChart
            qn('c:pie3DChart'),  # CT_Pie3DChart
            qn('c:doughnutChart'),  # CT_DoughnutChart
            qn('c:barChart'),  # CT_BarChart
            qn('c:bar3DChart'),  # CT_Bar3DChart
            qn('c:ofPieChart'),  # CT_OfPieChart
            qn('c:surfaceChart'),  # CT_SurfaceChart
            qn('c:surface3DChart'),  # CT_Surface3DChart
            qn('c:bubbleChart'),  # CT_BubbleChart
        )

        return list(self.iterchildren(*tags))  # type: ignore

    @property
    def ax(self) -> list[CT_ValAx | CT_CatAx | CT_DateAx | CT_SerAx]:
        """值轴列表"""
        tags = (
            qn('c:valAx'),  # CT_ValAx
            qn('c:catAx'),  # CT_CatAx
            qn('c:dateAx'),  # CT_DateAx
            qn('c:serAx'),  # CT_SerAx
        )

        return list(self.iterchildren(*tags))  # type: ignore

    @property
    def d_table(self) -> Optional[CT_DTable]:
        """21.2.2.54 dTable (数据表)

        该元素指定了一个数据表。
        """
        return getattr(self, qn('c:dTable'), None)

    @property
    def sp_pr(self) -> Optional[a_CT_ShapeProperties]:
        """21.2.2.197 spPr (形状属性)

        此元素指定父图表元素的格式。 不支持 custGeom、prstGeom、scene3d 和 xfrm 元素。 不支持 bwMode 属性。
        """
        return getattr(self, qn('c:spPr'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展列表"""
        return getattr(self, qn('c:extLst'))



class CT_PivotFmt(OxmlBaseElement):
    """21.2.2.142 pivotFmt (透视格式)

    此元素包含一组要应用于基于数据透视表的图表的格式设置。
    """

    @property
    def idx(self) -> CT_UnsignedInt:
        """21.2.2.84 idx (索引)

        该元素指定包含元素的索引。 该索引应确定该元素适用于父集合的哪个子集合。
        """
        return getattr(self, qn('c:idx'))

    @property
    def sp_pr(self) -> Optional[a_CT_ShapeProperties]:
        return getattr(self, qn('c:spPr'), None)

    @property
    def tx_pr(self) -> Optional[a_CT_TextBody]:
        return getattr(self, qn('c:txPr'), None)

    @property
    def marker(self) -> Optional[CT_Marker]:
        """21.2.2.106 marker (标记)

        该元素指定数据标记。
        """
        return getattr(self, qn('c:marker'), None)

    @property
    def dlbl(self) -> Optional[CT_DLbl]:
        return getattr(self, qn('c:dLbl'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class CT_PivotFmts(OxmlBaseElement):
    """21.2.2.143 pivotFmts (透视格式集合)

    此元素包含表面图表的格式化带的集合，索引从低到高。
    """

    @property
    def pivot_fmt(self) -> list[CT_PivotFmt]:
        return self.findall(qn('c:pivotFmt'))  # type: ignore


class ST_LegendPos(ST_BaseEnumType):
    """21.2.3.24 ST_LegendPos (图例位置)

    这个简单的类型指定图例的可能位置。
    """

    Bottom = 'b'
    """指定图例应绘制在图表底部。"""

    TopRight = 'tr'
    """指定图例应绘制在图表的右上角。"""

    Left = 'l'
    """指定图例应绘制在图表的左侧。"""

    Right = 'r'
    """指定图例应绘制在图表的右侧。"""

    Top = 't'
    """指定图例应绘制在图表的顶部。"""


class CT_LegendPos(OxmlBaseElement):
    """21.2.2.95 legendPos (图例位置)

    该元素指定图例的位置。
    """

    @property
    def val(self):
        """指定图例的位置。"""
        _val = self.attrib.get('val', 'r')

        return ST_LegendPos(_val)


class EG_LegendEntryData(OxmlBaseElement):
    @property
    def tx_pr(self) -> Optional[a_CT_TextBody]:
        return getattr(self, qn('c:txPr'), None)


class CT_LegendEntry(EG_LegendEntryData):
    """21.2.2.94 legendEntry (图例条目)

    该元素指定图例条目。
    """

    @property
    def idx(self) -> CT_UnsignedInt:
        """21.2.2.84 idx (索引)

        该元素指定包含元素的索引。 该索引应确定该元素适用于父集合的哪个子集合。
        """
        return getattr(self, qn('c:idx'))

    @property
    def delete(self) -> CT_Boolean | a_CT_TextBody:
        ele = getattr(self, qn('c:delete'), None)  # CT_Boolean

        if ele is None:
            ele = getattr(self, qn('txPr'), None)  # a_CT_TextBody

        if ele is None:
            msg = '应至少有1个元素， delete 或 txPr'
            raise OxmlElementValidateError(msg)

        return ele

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class CT_Legend(OxmlBaseElement):
    """21.2.2.93 legend (图例)

    该元素指定图例。
    """

    @property
    def legend_pos(self) -> Optional[CT_LegendPos]:
        return getattr(self, qn('c:legendPos'), None)

    @property
    def legend_entry(self) -> list[CT_LegendEntry]:
        return self.findall(qn('c:legendEntry'))  # type: ignore

    @property
    def layout(self) -> Optional[CT_Layout]:
        return getattr(self, qn('c:layout'), None)


    @property
    def overlay(self) -> Optional[CT_Boolean]:
        return getattr(self, qn('c:overlay'), None)


    @property
    def sp_pr(self) -> Optional[a_CT_ShapeProperties]:
        return getattr(self, qn('c:spPr'), None)


    @property
    def tx_pr(self) -> Optional[a_CT_TextBody]:
        return getattr(self, qn('c:txPr'), None)


    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class ST_DispBlanksAs(ST_BaseEnumType):
    """21.2.3.10 ST_DispBlanksAs (将空白显示为)

    这个简单的类型指定了显示空白的可能方式。
    """

    Span = 'span'
    """指定空白值应用一条线跨越."""

    Gap = 'gap'
    """指定空白值应保留为间隙."""

    Zero = 'zero'
    """指定空白值应被视为零."""


class CT_DispBlanksAs(OxmlBaseElement):
    """21.2.2.42 dispBlanksAs (显示空白为)

    该元素指定了图表上空白单元格的绘制方式。
    """

    @property
    def val(self):
        """指定了图表上空白单元格的绘制方式。"""

        _val = self.attrib.get('val', 'zero')

        return ST_DispBlanksAs(_val)


class CT_Chart(OxmlBaseElement):
    """21.2.2.27 chart (图表)

    该元素指定图表。
    """

    @property
    def title(self) -> Optional[CT_Title]:
        """21.2.2.210 title (标题)

        该元素指定一个标题。
        """
        return getattr(self, qn('c:title'), None)

    @property
    def auto_title_deleted(self) -> Optional[CT_Boolean]:
        """21.2.2.7 autoTitleDeleted (自动标题已删除)

        该元素指定该图表不应显示标题。
        """
        return getattr(self, qn('c:autoTitleDeleted'), None)

    @property
    def pivot_fmts(self) -> Optional[CT_PivotFmts]:
        """21.2.2.143 pivotFmts (透视格式集合)

        此元素包含表面图表的格式化带的集合，索引从低到高。
        """
        return getattr(self, qn('c:pivotFmts'), None)

    @property
    def view_3d(self) -> Optional[CT_View3D]:
        """21.2.2.228 view3D (3D 视图)

        该元素指定图表的 3D 视图。
        """
        return getattr(self, qn('c:view3D'), None)

    @property
    def floor(self) -> Optional[CT_Surface]:
        """21.2.2.69 floor (下限)

        该元素指定 3D 图表的下限。
        """
        return getattr(self, qn('c:floor'), None)

    @property
    def side_wall(self) -> Optional[CT_Surface]:
        """21.2.2.191 sideWall (侧壁)

        该元素指定侧壁。
        """
        return getattr(self, qn('c:sideWall'), None)

    @property
    def back_wall(self) -> Optional[CT_Surface]:
        """21.2.2.11 backWall (后墙)

        该元素指定图表的后墙。
        """
        return getattr(self, qn('c:backWall'), None)

    @property
    def plot_area(self) -> CT_PlotArea:
        """21.2.2.145 plotArea (绘图区域)

        该元素指定图表的绘图区域。
        """
        return getattr(self, qn('c:plotArea'))

    @property
    def legend(self) -> Optional[CT_Legend]:
        """21.2.2.93 legend (图例)

        该元素指定图例。
        """
        return getattr(self, qn('c:legend'), None)

    @property
    def plot_vis_only(self) -> Optional[CT_Boolean]:
        """21.2.2.146 plotVisOnly (绘图仅可见)

        此元素指定仅应在图表上绘制可见单元格。
        """
        return getattr(self, qn('c:plotVisOnly'), None)

    @property
    def disp_blanks_as(self) -> Optional[CT_DispBlanksAs]:
        """21.2.2.42 dispBlanksAs (显示为空白)

        该元素指定了图表上空白单元格的绘制方式。
        """
        return getattr(self, qn('c:dispBlanksAs'), None)

    @property
    def show_dLbls_over_max(self) -> Optional[CT_Boolean]:
        """21.2.2.180 showDLblsOverMax (显示超过最大值的数据标签)

        该元素指定应显示的超过图表最大值的数据标签。
        """
        return getattr(self, qn('c:showDLblsOverMax'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展列表"""

        return getattr(self, qn('c:extLst'))



ST_Style = NewType('ST_Style', int)
"""21.2.3.46 ST_Style (样式)

此简单类型指定其内容包含 1 到 48 之间的整数。该值通过下面描述的表格确定所有图表元素的默认格式。

默认字体是文档主题定义的小字体。 每个元素的默认字体大小是图表的字体大小，但标题除外，它始终是图表字体大小的 120%。 如果图表未设置字体大小，则默认字体大小为 10。轴标题和图表标题默认为粗体，而所有其他图表元素均为正常。 默认字体颜色与轴和主网格线线条颜色相同。

默认线条样式、填充样式和效果样式由下表确定。 每个默认值都包含主题线条、填充或效果（无、微妙、中等或强烈）以及应用该线条、填充或效果时要使用的颜色。 在某些情况下，主题格式和颜色都会因样式而异，而在其他情况下则不然。 默认线宽由主题确定，但数据点的线除外，它乘以表中给出的线宽值。
"""


def to_ST_Style(val: Any):
    intval = int(utils.AnyStrToStr(val))

    if not (1 <= intval <= 48):
        msg = f'预期外的值: {intval}'
        raise OxmlAttributeValidateError(msg)

    return val


class CT_Style(OxmlBaseElement):
    """21.2.2.202 style (样式)

    该元素指定应应用于图表的样式。
    """

    @property
    def val(self):
        """指定图表样式。"""

        _val = self.attrib['val']

        return to_ST_Style(_val)


class CT_PivotSource(OxmlBaseElement):
    """21.2.2.144 pivotSource (透视源)

    此元素指定数据透视图的源数据透视表。
    """

    @property
    def name(self) -> str:
        ele: OxmlBaseElement = getattr(self, qn('c:name'))

        return ele.text or ''

    @property
    def fmt_id(self) -> CT_UnsignedInt:
        return getattr(self, qn('c:fmtId'))

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        return getattr(self, qn('c:extLst'))



class CT_Protection(OxmlBaseElement):
    """21.2.2.149 protection (保护)

    该元素指定对图表的保护。 如果图表位于受保护的工作表或图表工作表上，则这些设置应控制用户与图表交互的方式。
    """

    @property
    def chart_object(self) -> Optional[CT_Boolean]:
        return getattr(self, qn('c:chartObject'))

    @property
    def data(self) -> Optional[CT_Boolean]:
        return getattr(self, qn('c:data'))

    @property
    def formatting(self) -> Optional[CT_Boolean]:
        return getattr(self, qn('c:formatting'))

    @property
    def selection(self) -> Optional[CT_Boolean]:
        return getattr(self, qn('c:selection'))

    @property
    def user_interface(self) -> Optional[CT_Boolean]:
        return getattr(self, qn('c:userInterface'))


class CT_HeaderFooter(OxmlBaseElement):
    """21.2.2.79 headerFooter (页眉和页脚)

    此元素指定在打印图表时要使用的页眉和页脚。（有关更多信息，请参见§18.3.1.46。）
    """

    @property
    def odd_header(self) -> str:
        ele: OxmlBaseElement = getattr(self, qn('c:oddHeader'))

        return ele.text or ''

    @property
    def odd_footer(self) -> str:
        ele: OxmlBaseElement = getattr(self, qn('c:oddFooter'))

        return ele.text or ''

    @property
    def even_header(self) -> str:
        ele: OxmlBaseElement = getattr(self, qn('c:evenHeader'))

        return ele.text or ''

    @property
    def even_footer(self) -> str:
        ele: OxmlBaseElement = getattr(self, qn('c:evenFooter'))

        return ele.text or ''

    @property
    def first_header(self) -> str:
        ele: OxmlBaseElement = getattr(self, qn('c:firstHeader'))

        return ele.text or ''

    @property
    def first_footer(self) -> str:
        ele: OxmlBaseElement = getattr(self, qn('c:firstFooter'))

        return ele.text or ''

    @property
    def align_with_margins(self) -> str:
        """指定页眉和页脚应与图表的左右边距对齐。

        值为1或true指定应用该属性。这是该属性的默认值，在父元素存在但该属性被省略时，会被隐含应用。

        值为0或false指定不应用该属性。
        """

        _val = self.attrib.get('alignWithMargins', 'true')

        return to_xsd_bool(_val)  # type: ignore

    @property
    def different_odd_even(self) -> str:
        """指定奇数页和偶数页的页眉和页脚不同。

        一个值为1或true表示属性已应用。这是该属性的默认值，在父元素存在但该属性被省略时，会被隐含使用。

        一个值为0或false表示属性未应用。
        """
        _val = self.attrib.get('differentOddEven', 'false')

        return to_xsd_bool(_val)  # type: ignore

    @property
    def different_first(self) -> str:
        """指定首页面的页眉和页脚与其他页面不同。

        值为1或true指定应用该属性。这是该属性的默认值，在父元素存在但该属性被省略时，会被隐含应用。

        值为0或false指定不应用该属性。
        """

        _val = self.attrib.get('differentFirst', 'false')

        return to_xsd_bool(_val)  # type: ignore


class CT_PageMargins(OxmlBaseElement):
    """21.2.2.133 pageMargins (页边距)

    该元素指定图表的页边距。
    """

    @property
    def left(self) -> float:
        """指定左页边距（以英寸为单位）。"""

        _val = self.attrib['l']

        return to_xsd_double(_val)  # type: ignore

    @property
    def right(self) -> float:
        """指定右页边距（以英寸为单位）。"""
        _val = self.attrib['r']

        return to_xsd_double(_val)  # type: ignore

    @property
    def top(self) -> float:
        """指定顶页边距（以英寸为单位）。"""
        _val = self.attrib['t']

        return to_xsd_double(_val)  # type: ignore

    @property
    def bottom(self) -> float:
        """指定底部页边距（以英寸为单位）。"""

        _val = self.attrib['b']

        return to_xsd_double(_val)  # type: ignore

    @property
    def header(self) -> float:
        """指定页眉边距（以英寸为单位）。"""
        _val = self.attrib['header']

        return to_xsd_double(_val)  # type: ignore

    @property
    def footer(self) -> float:
        """指定页脚边距（以英寸为单位）。"""
        _val = self.attrib['footer']

        return to_xsd_double(_val)  # type: ignore


class ST_PageSetupOrientation(ST_BaseEnumType):
    """21.2.3.32 ST_PageSetupOrientation (打印页面方向)

    此简单类型指定此图表应显示的打印页面的页面方向。
    """

    Default = 'default'
    """指定页面方向应为系统的默认方向。"""

    Portrait = 'portrait'
    """指定打印页面应为纵向。"""

    Landscape = 'landscape'
    """指定打印页面应为横向。"""


class CT_ExternalData(OxmlBaseElement):
    """21.2.2.63 externalData (外部数据关系)

    该元素指定与该图表数据的关系。

    数据可以链接起来，指向另一个文件中的电子表格。 或者，可以将数据嵌入并包含在包含图表的同一 xml 包内的单独部分中。 在这种情况下，它应以 Office Open XML 格式存储为嵌入式电子表格对象。

    电子表格应用程序不使用它，因为电子表格应用程序可以通过公式 <f> 元素维护其自己对电子表格中数据的引用。
    """

    @property
    def auto_update(self) -> Optional[CT_Boolean]:
        return getattr(self, qn('c:autoUpdate'), None)

    @property
    def r_id(self) -> float:
        """
        指定此图表的关系的关系ID。此属性明确指定的关系应为类型 http://schemas.openxmlformats.org/officeDocument/2006/relationships/package, 或 http://schemas.openxmlformats.org/officeDocument/2006/relationships/oleObject.
        """
        _val = self.attrib[qn('r:id')]

        return utils.AnyStrToStr(_val)  # type: ignore


class CT_PageSetup(OxmlBaseElement):
    """21.2.2.134 pageSetup (页面设置)

    该元素定义图表的页面设置。
    """

    @property
    def paper_size(self):
        """根据下表指定纸张尺寸。

        ....

        参考文档.
        """
        _val = self.attrib.get('paperSize', '1')

        return to_xsd_unsigned_int(_val)  # type: ignore

    @property
    def paper_height(self) -> Optional[s_ST_PositiveUniversalMeasure]:
        """自定义纸张的高度为数字，后跟单位标识符。 [Example: 297mm, 11in end example]

        当指定 paperHeight 和 paperWidth 时，应忽略 paperSize。
        """
        _val = self.attrib.get('paperHeight')

        if _val is None:
            return None

        return to_s_ST_PositiveUniversalMeasure(_val)  # type: ignore

    @property
    def paper_width(self) -> Optional[s_ST_PositiveUniversalMeasure]:
        """自定义纸张的宽度为数字，后跟单位标识符。 [Example: 21cm, 8.5in end example]

        当指定 paperHeight 和 paperWidth 时，应忽略 paperSize。

        """
        _val = self.attrib.get('paperWidth')

        if _val is None:
            return None

        return to_s_ST_PositiveUniversalMeasure(_val)  # type: ignore

    @property
    def first_page_number(self) -> Optional[s_ST_PositiveUniversalMeasure]:
        """指定页码。"""

        _val = self.attrib.get('firstPageNumber', '1')

        return to_s_ST_PositiveUniversalMeasure(_val)  # type: ignore

    @property
    def orientation(self) -> Optional[ST_PageSetupOrientation]:
        """指定纸张的方向。"""

        _val = self.attrib.get('orientation', 'default')

        return ST_PageSetupOrientation(_val)

    @property
    def black_and_white(self):
        """指定页面应以黑白打印。"""

        _val = self.attrib.get('blackAndWhite', 'false')

        return to_xsd_bool(_val)

    @property
    def draft(self):
        """指定页面应以草稿模式打印。"""

        _val = self.attrib.get('draft', 'false')

        return to_xsd_bool(_val)

    @property
    def use_first_page_number(self):
        """指定使用首页页码而不是自动生成页码。"""

        _val = self.attrib.get('useFirstPageNumber', 'false')

        return to_xsd_bool(_val)

    @property
    def horizontal_dpi(self):
        """指定要打印的水平分辨率（以每英寸点数为单位）。"""

        _val = self.attrib.get('horizontalDpi', '600')

        return int(utils.AnyStrToStr(_val))  # type: ignore

    @property
    def vertical_dpi(self):
        """指定要打印的垂直分辨率（以每英寸点数为单位）。"""

        _val = self.attrib.get('verticalDpi', '600')

        return int(utils.AnyStrToStr(_val))  # type: ignore

    @property
    def copies(self):
        """指定应打印的份数。"""

        _val = self.attrib.get('copies', '1')

        return to_xsd_unsigned_int(_val)  # type: ignore


class CT_PrintSettings(OxmlBaseElement):
    """21.2.2.148 printSettings (打印设置)

    该元素指定图表的打印设置。
    """

    @property
    def headerFooter(self) -> Optional[CT_HeaderFooter]:
        return getattr(self, qn('c:headerFooter'), None)

    @property
    def page_margins(self) -> Optional[CT_PageMargins]:
        return getattr(self, qn('c:pageMargins'), None)

    @property
    def page_setup(self) -> Optional[CT_PageSetup]:
        return getattr(self, qn('c:pageSetup'), None)

    @property
    def legacy_drawing_hf(self) -> Optional[CT_RelId]:
        return getattr(self, qn('c:legacyDrawingHF'), None)


class CT_ChartSpace(OxmlBaseElement):
    """21.2.2.29 chartSpace (图表空间)

    该元素指定单个图表的整体设置，并且是图表部分的根节点。
    """

    @property
    def date1904(self) -> Optional[CT_Boolean]:
        """21.2.2.38 date1904 (1904日期系统)

        该元素指定图表使用1904日期系统。如果使用1904日期系统，则所有日期和时间都应指定为自1903年12月31日以来的天数的十进制数。如果不使用1904日期系统，则所有日期和时间都应指定为自1899年12月31日以来的天数的十进制数。
        """
        return getattr(self, qn('c:date1904'), None)

    @property
    def lang(self) -> Optional[CT_TextLanguageID]:
        """21.2.2.87 lang (编辑语言)

        此元素指定上次修改此图表时使用的主要编辑语言。
        """
        return getattr(self, qn('c:lang'), None)

    @property
    def rounded_corners(self) -> Optional[CT_Boolean]:
        """21.2.2.159 roundedCorners (圆角)

        该元素指定图表区域应具有圆角。
        """
        return getattr(self, qn('c:roundedCorners'), None)

    @property
    def style(self) -> Optional[CT_Style]:
        """21.2.2.202 style (样式)

        该元素指定应应用于图表的样式。
        """
        return getattr(self, qn('c:style'), None)

    @property
    def clr_map_ovr(self) -> Optional[a_CT_ColorMapping]:
        """21.2.2.30 clrMapOvr (颜色映射覆盖)

        该元素表示颜色映射信息。如果用户在复制粘贴后选择保留源格式，则用于覆盖应用程序的颜色映射。
        """
        return getattr(self, qn('c:clrMapOvr'), None)

    @property
    def pivot_source(self) -> Optional[CT_PivotSource]:
        """21.2.2.144 pivotSource (透视源)

        此元素指定数据透视图的源数据透视表。
        """
        return getattr(self, qn('c:pivotSource'), None)

    @property
    def protection(self) -> Optional[CT_Protection]:
        """21.2.2.149 protection (保护)

        该元素指定对图表的保护。 如果图表位于受保护的工作表或图表工作表上，则这些设置应控制用户与图表交互的方式。
        """
        return getattr(self, qn('c:protection'), None)

    @property
    def chart(self) -> CT_Chart:
        """21.2.2.27 chart (图表)

        该元素指定图表。
        """
        return getattr(self, qn('c:chart'))

    @property
    def sp_pr(self) -> Optional[a_CT_ShapeProperties]:
        """21.2.2.197 spPr (形状属性)

        此元素指定父图表元素的格式。

        不支持 custGeom、prstGeom、scene3d 和 xfrm 元素。

        不支持 bwMode 属性。
        """
        return getattr(self, qn('c:spPr'), None)

    @property
    def tx_pr(self) -> Optional[a_CT_TextBody]:
        """21.2.2.216 txPr (文本属性)

        该元素指定文本格式。 不支持 lstStyle 元素。
        """
        return getattr(self, qn('c:txPr'), None)

    @property
    def external_data(self) -> Optional[CT_ExternalData]:
        """21.2.2.63 externalData (外部数据关系)

        该元素指定与该图表数据的关系。

        数据可以链接起来，指向另一个文件中的电子表格。 或者，可以将数据嵌入并包含在包含图表的同一 xml 包内的单独部分中。 在这种情况下，它应以 Office Open XML 格式存储为嵌入式电子表格对象。

        电子表格应用程序不使用它，因为电子表格应用程序可以通过公式 <f> 元素维护其自己对电子表格中数据的引用。
        """
        return getattr(self, qn('c:externalData'), None)

    @property
    def print_settings(self) -> Optional[CT_PrintSettings]:
        """21.2.2.148 printSettings (打印设置)

        该元素指定图表的打印设置。
        """
        return getattr(self, qn('c:printSettings'), None)

    @property
    def user_shapes(self) -> Optional[CT_RelId]:
        """21.2.2.220 userShapes (用户形状)

        该元素应指定图表顶部绘制的形状。
        """

        return getattr(self, qn('c:userShapes'), None)

    @property
    def ext_lst(self) -> Optional[CT_ExtensionList]:
        """扩展列表"""

        return getattr(self, qn('c:extLst'))



dml_chart_namespace = lookup.get_namespace(namespace_c)
dml_chart_namespace[None] = OxmlBaseElement


dml_chart_namespace['ext'] = CT_Extension
dml_chart_namespace['v'] = OxmlBaseElement  # str

dml_chart_namespace['formatCode'] = OxmlBaseElement  # str
dml_chart_namespace['ptCount'] = CT_UnsignedInt
dml_chart_namespace['pt'] = CT_NumVal
dml_chart_namespace['extLst'] = CT_ExtensionList

dml_chart_namespace['f'] = OxmlBaseElement  # str
dml_chart_namespace['numCache'] = CT_NumData

dml_chart_namespace['numRef'] = CT_NumRef
dml_chart_namespace['numLit'] = CT_NumData
dml_chart_namespace['strCache'] = CT_StrData

dml_chart_namespace['rich'] = a_CT_TextBody

dml_chart_namespace['pt'] = CT_StrVal  # 有冲突
dml_chart_namespace['lvl'] = CT_Lvl
dml_chart_namespace['multiLvlStrCache'] = CT_MultiLvlStrData
dml_chart_namespace['multiLvlStrRef'] = CT_MultiLvlStrRef
dml_chart_namespace['numRef'] = CT_NumRef
dml_chart_namespace['numLit'] = CT_NumData
dml_chart_namespace['strRef'] = CT_StrRef
dml_chart_namespace['strLit'] = CT_StrData

dml_chart_namespace['layoutTarget'] = CT_LayoutTarget
dml_chart_namespace['xMode'] = CT_LayoutMode
dml_chart_namespace['yMode'] = CT_LayoutMode
dml_chart_namespace['wMode'] = CT_LayoutMode
dml_chart_namespace['hMode'] = CT_LayoutMode
dml_chart_namespace['x'] = CT_Double
dml_chart_namespace['y'] = CT_Double
dml_chart_namespace['w'] = CT_Double
dml_chart_namespace['h'] = CT_Double

dml_chart_namespace['manualLayout'] = CT_ManualLayout

# dml_chart_namespace["tx"] = CT_Tx # 有冲突
# dml_chart_namespace["tx"] = CT_SerTx  # 有冲突


class Common_CT_Tx(CT_Tx, CT_SerTx): ...


dml_chart_namespace['tx'] = Common_CT_Tx

dml_chart_namespace['layout'] = CT_Layout
dml_chart_namespace['overlay'] = CT_Boolean
dml_chart_namespace['spPr'] = a_CT_ShapeProperties
dml_chart_namespace['txPr'] = a_CT_TextBody

dml_chart_namespace['rotX'] = CT_RotX
dml_chart_namespace['hPercent'] = CT_HPercent
dml_chart_namespace['rotY'] = CT_RotY
dml_chart_namespace['depthPercent'] = CT_DepthPercent
dml_chart_namespace['rAngAx'] = CT_Boolean
dml_chart_namespace['perspective'] = CT_Perspective

dml_chart_namespace['thickness'] = CT_Thickness
dml_chart_namespace['pictureOptions'] = CT_PictureOptions
dml_chart_namespace['showHorzBorder'] = CT_Boolean
dml_chart_namespace['showVertBorder'] = CT_Boolean
dml_chart_namespace['showOutline'] = CT_Boolean
dml_chart_namespace['showKeys'] = CT_Boolean

dml_chart_namespace['secondPiePt'] = CT_UnsignedInt
dml_chart_namespace['numFmt'] = CT_NumFmt

dml_chart_namespace['showLegendKey'] = CT_Boolean
dml_chart_namespace['showVal'] = CT_Boolean
dml_chart_namespace['showCatName'] = CT_Boolean
dml_chart_namespace['showSerName'] = CT_Boolean
dml_chart_namespace['showPercent'] = CT_Boolean
dml_chart_namespace['showBubbleSize'] = CT_Boolean
dml_chart_namespace['separator'] = OxmlBaseElement  # str

dml_chart_namespace['idx'] = CT_UnsignedInt
dml_chart_namespace['delete'] = CT_Boolean

dml_chart_namespace['showLeaderLines'] = CT_Boolean
dml_chart_namespace['leaderLines'] = CT_ChartLines

dml_chart_namespace['symbol'] = CT_MarkerStyle
dml_chart_namespace['size'] = CT_MarkerSize
dml_chart_namespace['invertIfNegative'] = CT_Boolean
dml_chart_namespace['bubble3D'] = CT_Boolean
dml_chart_namespace['explosion'] = CT_UnsignedInt
dml_chart_namespace['name'] = OxmlBaseElement  # str
dml_chart_namespace['trendlineType'] = CT_TrendlineType

dml_chart_namespace['order'] = CT_Order
dml_chart_namespace['period'] = CT_Period
dml_chart_namespace['forward'] = CT_Double
dml_chart_namespace['backward'] = CT_Double
dml_chart_namespace['intercept'] = CT_Double


dml_chart_namespace['dispRSqr'] = CT_Boolean
dml_chart_namespace['dispEq'] = CT_Boolean
dml_chart_namespace['trendlineLbl'] = CT_TrendlineLbl

dml_chart_namespace['errDir'] = CT_ErrDir
dml_chart_namespace['errBarType'] = CT_ErrBarType
dml_chart_namespace['errValType'] = CT_ErrValType

dml_chart_namespace['noEndCap'] = CT_Boolean
dml_chart_namespace['plus'] = CT_NumDataSource
dml_chart_namespace['minus'] = CT_NumDataSource

dml_chart_namespace['upBars'] = CT_UpDownBar
dml_chart_namespace['downBars'] = CT_UpDownBar

dml_chart_namespace['dPt'] = CT_DPt

dml_chart_namespace['dLbl'] = CT_DLbl
dml_chart_namespace['dLbls'] = CT_DLbls
dml_chart_namespace['dLblPos'] = CT_DLblPos
dml_chart_namespace['trendline'] = CT_Trendline


dml_chart_namespace['errBars'] = CT_ErrBars
dml_chart_namespace['cat'] = CT_AxDataSource
dml_chart_namespace['val'] = CT_Double  # 有冲突
dml_chart_namespace['val'] = CT_NumDataSource  # 有冲突
dml_chart_namespace['smooth'] = CT_Boolean

dml_chart_namespace['xVal'] = CT_AxDataSource
dml_chart_namespace['yVal'] = CT_NumDataSource

dml_chart_namespace['bubbleSize'] = CT_NumDataSource
dml_chart_namespace['bubble3D'] = CT_Boolean

dml_chart_namespace['grouping'] = CT_Grouping  # 有冲突
dml_chart_namespace['varyColors'] = CT_Boolean


dml_chart_namespace['dropLines'] = CT_ChartLines
dml_chart_namespace['hiLowLines'] = CT_ChartLines
# dml_chart_namespace["marker"] = CT_Marker # 有冲突
# dml_chart_namespace["marker"] = CT_Boolean  # 有冲突


class CT_CommonMarker(CT_Marker, CT_Boolean): ...


dml_chart_namespace['marker'] = CT_CommonMarker  # 有冲突

dml_chart_namespace['axId'] = CT_UnsignedInt

dml_chart_namespace['gapWidth'] = CT_GapAmount
dml_chart_namespace['gapDepth'] = CT_GapAmount
dml_chart_namespace['upDownBars'] = CT_UpDownBars
dml_chart_namespace['scatterStyle'] = CT_ScatterStyle

# dml_chart_namespace["ser"] = CT_LineSer  # 有冲突
# dml_chart_namespace["ser"] = CT_ScatterSer  # 有冲突
# dml_chart_namespace["ser"] = CT_RadarSer  # 有冲突
# dml_chart_namespace["ser"] = CT_BarSer  # 有冲突
# dml_chart_namespace["ser"] = CT_AreaSer  # 有冲突
# dml_chart_namespace["ser"] = CT_PieSer  # 有冲突
# dml_chart_namespace["ser"] = CT_BubbleSer  # 有冲突
# dml_chart_namespace["ser"] = CT_SurfaceSer  # 有冲突


class CT_AllSer(
    CT_LineSer,
    CT_ScatterSer,
    CT_RadarSer,
    CT_BarSer,
    CT_AreaSer,
    CT_PieSer,
    CT_BubbleSer,
    CT_SurfaceSer,
): ...


# 公共类，ser 关键字有冲突
dml_chart_namespace['ser'] = CT_AllSer  # 有冲突

dml_chart_namespace['radarStyle'] = CT_RadarStyle

dml_chart_namespace['barDir'] = CT_BarDir
dml_chart_namespace['grouping'] = CT_BarGrouping  # 有冲突

dml_chart_namespace['overlap'] = CT_Overlap
dml_chart_namespace['serLines'] = CT_ChartLines

dml_chart_namespace['firstSliceAng'] = CT_FirstSliceAng
dml_chart_namespace['holeSize'] = CT_HoleSize
dml_chart_namespace['ofPieType'] = CT_OfPieType
dml_chart_namespace['splitType'] = CT_SplitType

dml_chart_namespace['splitPos'] = CT_Double
dml_chart_namespace['custSplit'] = CT_CustSplit
dml_chart_namespace['secondPieSize'] = CT_SecondPieSize

dml_chart_namespace['bubbleScale'] = CT_BubbleScale
dml_chart_namespace['showNegBubbles'] = CT_Boolean
dml_chart_namespace['sizeRepresents'] = CT_SizeRepresents
dml_chart_namespace['bandFmt'] = CT_BandFmt
dml_chart_namespace['wireframe'] = CT_Boolean

dml_chart_namespace['bandFmts'] = CT_BandFmts

dml_chart_namespace['applyToFront'] = CT_Boolean
dml_chart_namespace['applyToSides'] = CT_Boolean
dml_chart_namespace['applyToEnd'] = CT_Boolean
dml_chart_namespace['pictureFormat'] = CT_PictureFormat
dml_chart_namespace['pictureStackUnit'] = CT_PictureStackUnit

dml_chart_namespace['custUnit'] = CT_Double
dml_chart_namespace['builtInUnit'] = CT_BuiltInUnit
dml_chart_namespace['dispUnitsLbl'] = CT_DispUnitsLbl

dml_chart_namespace['logBase'] = CT_LogBase
dml_chart_namespace['orientation'] = CT_Orientation

dml_chart_namespace['max'] = CT_Double
dml_chart_namespace['min'] = CT_Double

dml_chart_namespace['scaling'] = CT_Scaling
dml_chart_namespace['delete'] = CT_Boolean
dml_chart_namespace['axPos'] = CT_AxPos
dml_chart_namespace['majorGridlines'] = CT_ChartLines
dml_chart_namespace['minorGridlines'] = CT_ChartLines
dml_chart_namespace['title'] = CT_Title
dml_chart_namespace['majorTickMark'] = CT_TickMark
dml_chart_namespace['minorTickMark'] = CT_TickMark
dml_chart_namespace['tickLblPos'] = CT_TickLblPos
dml_chart_namespace['crossAx'] = CT_UnsignedInt
dml_chart_namespace['crosses'] = CT_Crosses
dml_chart_namespace['crossesAt'] = CT_Double

dml_chart_namespace['auto'] = CT_Boolean
dml_chart_namespace['lblAlgn'] = CT_LblAlgn
dml_chart_namespace['lblOffset'] = CT_LblOffset
dml_chart_namespace['tickLblSkip'] = CT_Skip
dml_chart_namespace['tickMarkSkip'] = CT_Skip
dml_chart_namespace['noMultiLvlLbl'] = CT_Boolean

dml_chart_namespace['baseTimeUnit'] = CT_TimeUnit
dml_chart_namespace['majorUnit'] = CT_AxisUnit
dml_chart_namespace['majorTimeUnit'] = CT_TimeUnit
dml_chart_namespace['minorUnit'] = CT_AxisUnit
dml_chart_namespace['minorTimeUnit'] = CT_TimeUnit
dml_chart_namespace['tickLblSkip'] = CT_Skip
dml_chart_namespace['tickMarkSkip'] = CT_Skip
dml_chart_namespace['crossBetween'] = CT_CrossBetween
dml_chart_namespace['dispUnits'] = CT_DispUnits

dml_chart_namespace['areaChart'] = CT_AreaChart
dml_chart_namespace['area3DChart'] = CT_Area3DChart
dml_chart_namespace['lineChart'] = CT_LineChart
dml_chart_namespace['line3DChart'] = CT_Line3DChart
dml_chart_namespace['stockChart'] = CT_StockChart
dml_chart_namespace['radarChart'] = CT_RadarChart

dml_chart_namespace['scatterChart'] = CT_ScatterChart
dml_chart_namespace['pieChart'] = CT_PieChart
dml_chart_namespace['pie3DChart'] = CT_Pie3DChart
dml_chart_namespace['doughnutChart'] = CT_DoughnutChart
dml_chart_namespace['barChart'] = CT_BarChart
dml_chart_namespace['bar3DChart'] = CT_Bar3DChart
dml_chart_namespace['ofPieChart'] = CT_OfPieChart
dml_chart_namespace['surfaceChart'] = CT_SurfaceChart
dml_chart_namespace['surface3DChart'] = CT_Surface3DChart
dml_chart_namespace['bubbleChart'] = CT_BubbleChart


dml_chart_namespace['valAx'] = CT_ValAx
dml_chart_namespace['catAx'] = CT_CatAx
dml_chart_namespace['dateAx'] = CT_DateAx
dml_chart_namespace['serAx'] = CT_SerAx

dml_chart_namespace['dTable'] = CT_DTable

dml_chart_namespace['pivotFmt'] = CT_PivotFmt
dml_chart_namespace['legend'] = CT_Legend
dml_chart_namespace['legendPos'] = CT_LegendPos
dml_chart_namespace['legendEntry'] = CT_LegendEntry
dml_chart_namespace['autoTitleDeleted'] = CT_Boolean
dml_chart_namespace['view3D'] = CT_View3D
dml_chart_namespace['floor'] = CT_Surface
dml_chart_namespace['sideWall'] = CT_Surface
dml_chart_namespace['backWall'] = CT_Surface

dml_chart_namespace['plotArea'] = CT_PlotArea
dml_chart_namespace['plotVisOnly'] = CT_Boolean
dml_chart_namespace['dispBlanksAs'] = CT_DispBlanksAs
dml_chart_namespace['showDLblsOverMax'] = CT_Boolean
dml_chart_namespace['fmtId'] = CT_UnsignedInt

dml_chart_namespace['chartObject'] = CT_Boolean
dml_chart_namespace['data'] = CT_Boolean
dml_chart_namespace['formatting'] = CT_Boolean
dml_chart_namespace['selection'] = CT_Boolean
dml_chart_namespace['userInterface'] = CT_Boolean

dml_chart_namespace['oddHeader'] = OxmlBaseElement  # str
dml_chart_namespace['oddFooter'] = OxmlBaseElement  # str
dml_chart_namespace['evenHeader'] = OxmlBaseElement  # str
dml_chart_namespace['evenFooter'] = OxmlBaseElement  # str
dml_chart_namespace['firstHeader'] = OxmlBaseElement  # str
dml_chart_namespace['firstFooter'] = OxmlBaseElement  # str

dml_chart_namespace['autoUpdate'] = CT_Boolean
dml_chart_namespace['headerFooter'] = CT_HeaderFooter

dml_chart_namespace['pageMargins'] = CT_PageMargins
dml_chart_namespace['pageSetup'] = CT_PageSetup
dml_chart_namespace['legacyDrawingHF'] = CT_RelId

dml_chart_namespace['date1904'] = CT_Boolean
dml_chart_namespace['lang'] = CT_TextLanguageID
dml_chart_namespace['roundedCorners'] = CT_Boolean

dml_chart_namespace['clrMapOvr'] = a_CT_ColorMapping
dml_chart_namespace['pivotSource'] = CT_PivotSource
dml_chart_namespace['protection'] = CT_Protection
dml_chart_namespace['chart'] = CT_Chart

dml_chart_namespace['externalData'] = CT_ExternalData
dml_chart_namespace['printSettings'] = CT_PrintSettings
dml_chart_namespace['userShapes'] = CT_RelId  # 冲突

dml_chart_namespace['chartSpace'] = CT_ChartSpace  # 根节点之一
dml_chart_namespace['userShapes'] = cdr_CT_Drawing  # 根节点之一 冲突
# dml_chart_namespace["chart"] = CT_RelId  # 根节点之一
