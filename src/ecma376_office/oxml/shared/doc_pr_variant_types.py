"""
对应xsd: shared-documentPropertiesVariantTypes.xsd

<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"
  xmlns="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"
  xmlns:s="http://schemas.openxmlformats.org/officeDocument/2006/sharedTypes"
  targetNamespace="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"
  blockDefault="#all" elementFormDefault="qualified">
  <xsd:import namespace="http://schemas.openxmlformats.org/officeDocument/2006/sharedTypes"
    schemaLocation="shared-commonSimpleTypes.xsd"/>

  ...

</xsd:schema>
"""

from __future__ import annotations

import logging
from typing import NewType, TypeVar

from ecma376_office.oxml.base import OxmlBaseElement, ST_BaseEnumType, lookup
from ecma376_office.oxml.shared.common_simple_types import ST_Guid as s_ST_Guid
from ecma376_office.oxml.xsd_types import (
    CT_XSD_Base64,
    CT_XSD_Boolean,
    CT_XSD_Byte,
    CT_XSD_Datetime,
    CT_XSD_Decimal,
    CT_XSD_Double,
    CT_XSD_Float,
    CT_XSD_Int,
    CT_XSD_Long,
    CT_XSD_Short,
    CT_XSD_String,
    CT_XSD_UnsignedByte,
    CT_XSD_UnsignedInt,
    CT_XSD_UnsignedLong,
    CT_XSD_UnsignedShort,
)

namespace_vt = 'http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes'

namespace_s = 'http://schemas.openxmlformats.org/officeDocument/2006/sharedTypes'

logger = logging.getLogger(__name__)

ns_map = {
    'vt': namespace_vt,  # 当前命名空间
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


class ST_VectorBaseType(ST_BaseEnumType):
    """
    ST_VectorBaseType 简单类型将向量的 baseType 属性的允许值定义为：variant、i1、i2、i4、i8、ui1、ui2、ui4、ui8、r4、r8、lpstr、lpwstr、bstr、date、filetime、bool、cy 、error 和 clsid。

    此简单类型的内容是 W3C XML 架构字符串数据类型的限制。
    """

    Variant = 'variant'
    I1 = 'i1'
    I2 = 'i2'
    I4 = 'i4'
    I8 = 'i8'
    Ui1 = 'ui1'
    Ui2 = 'ui2'
    Ui4 = 'ui4'
    Ui8 = 'ui8'
    R4 = 'r4'
    R8 = 'r8'
    Lpstr = 'lpstr'
    Lpwstr = 'lpwstr'
    Bstr = 'bstr'
    Date = 'date'
    Filetime = 'filetime'
    Bool = 'bool'
    Cy = 'cy'
    Error = 'error'
    Clsid = 'clsid'


class ST_ArrayBaseType(ST_BaseEnumType):
    """数组基本类型

    ST_ArrayBaseType 简单类型将数组的 baseType 属性的允许值定义为：variant、i1、i2、i4、int、ui1、ui2、ui4、uint、r4、r8、decimal、bstr、date、bool、cy 和 error。

    此简单类型的内容是 W3C XML 架构字符串数据类型的限制。
    """

    Variant = 'variant'
    I1 = 'i1'
    I2 = 'i2'
    I4 = 'i4'
    Int = 'int'
    Ui1 = 'ui1'
    Ui2 = 'ui2'
    Ui4 = 'ui4'
    Uint = 'uint'
    R4 = 'r4'
    R8 = 'r8'
    Decimal = 'decimal'
    Bstr = 'bstr'
    Date = 'date'
    Bool = 'bool'
    Cy = 'cy'
    Error = 'error'


# <xsd:pattern value="\s*[0-9]*\.[0-9]{4}\s*"/>
ST_Cy = NewType('ST_Cy', str)
ST_Cy.__doc__ = r"""
ST_Cy 简单类型将 cy 元素定义为小数点后恰好四位数字的货币变体类型。

此简单类型的内容是 W3C XML 架构字符串数据类型的限制。

这个简单类型还指定了以下限制：

该简单类型的内容应与以下正则表达式模式匹配: \s*[0-9]*\.[0-9]{4}\s*.
"""

# <xsd:pattern value="\s*0x[0-9A-Za-z]{8}\s*"/>
ST_Error = NewType('ST_Error', str)
ST_Error.__doc__ = r"""错误状态代码

ST_Error 简单类型定义了 0xHHHHHHHH 形式的 32 位错误状态代码变体类型。 每个H代表一个十六进制。

此简单类型的内容是 W3C XML 架构字符串数据类型的限制。

这个简单类型还指定了以下限制：

该简单类型的内容应与以下正则表达式模式匹配: \s*0x[0-9A-Zaz]{8}\s*.
"""


class CT_Empty(OxmlBaseElement):
    """空元素"""


class CT_Null(OxmlBaseElement):
    """Null元素"""


class CT_Vector(OxmlBaseElement):
    """向量

    Vector

    该元素定义向量变体类型。 矢量内容应具有由 baseType 属性指定的统一类型。 向量的内容是使用适当变体类型的重复子元素来定义的。

    例如: lpstr 变体类型的向量:

    <vt:vector baseType="lpstr">
        <vt:lpstr>One</vt:lpstr>
        <vt:lpstr>Two</vt:lpstr>
        <vt:lpstr>Three</vt:lpstr>
    </vt:vector>
    """

    @property
    def variant(self) -> list[CT_Variant]:
        """变体

        该元素可以包含任意变体类型的 1 个子元素。 该元素仅作为向量或数组变体类型的子元素有效。
        """
        return self.findall(qn('vt:variant'))

    @property
    def i1(self) -> list[CT_XSD_Byte]:
        """1-字节 有符号整数

        该元素指定 8 字节有符号整数变量类型。
        """
        return self.findall(qn('vt:i1'))

    @property
    def i2(self) -> list[CT_XSD_Short]:
        """2-字节 有符号整数

        该元素指定 8 字节有符号整数变量类型。
        """
        return self.findall(qn('vt:i2'))

    @property
    def i4(self) -> list[CT_XSD_Int]:
        """4-字节 有符号整数

        该元素指定 8 字节有符号整数变量类型。
        """
        return self.findall(qn('vt:i4'))

    @property
    def i8(self) -> list[CT_XSD_Long]:
        """8-字节 有符号整数

        该元素指定 8 字节有符号整数变量类型。
        """

        return self.findall(qn('vt:i8'))

    @property
    def ui1(self) -> list[CT_XSD_UnsignedByte]:
        """1-字节 无符号整数

        该元素指定 1 字节无符号整数变量类型。
        """

        return self.findall(qn('vt:ui1'))

    @property
    def ui2(self) -> list[CT_XSD_UnsignedShort]:
        """2-字节 无符号整数

        该元素指定 2 字节无符号整数变量类型。
        """

        return self.findall(qn('vt:ui2'))

    @property
    def ui4(self) -> list[CT_XSD_UnsignedInt]:
        """4-字节 无符号整数

        该元素指定 4 字节无符号整数变量类型。
        """

        return self.findall(qn('vt:ui4'))

    @property
    def ui8(self) -> list[CT_XSD_UnsignedLong]:
        """8-字节 无符号整数

        该元素指定 8 字节无符号整数变量类型。
        """

        return self.findall(qn('vt:ui8'))

    @property
    def r4(self) -> list[CT_XSD_Float]:
        """4字节实数

        该元素指定 4 字节实数变量类型。
        """
        return self.findall(qn('vt:r4'))

    @property
    def r8(self) -> list[CT_XSD_Double]:
        """8字节实数

        该元素指定 8 字节实数变量类型。
        """

        return self.findall(qn('vt:r8'))

    @property
    def lpstr(self) -> list[CT_XSD_String]:
        """

        该元素指定字符串变体类型。
        对于 XML 1.0 规范定义的无法在 XML 中表示的所有字符，将使用 Unicode 数字字符表示转义字符格式 xHHHH 对这些字符进行转义，其中 H 表示字符值中的十六进制字符。

        例如: XML 1.0 文档中不允许使用 Unicode 字符 8，因此必须将其转义为 x0008
        """

        return self.findall(qn('vt:lpstr'))

    @property
    def lpwstr(self) -> list[CT_XSD_String]:
        """变体字符串

        该元素指定字符串变体类型。
        对于 XML 1.0 规范定义的无法在 XML 中表示的所有字符，将使用 Unicode 数字字符表示转义字符格式 xHHHH 对这些字符进行转义，
        其中 H 表示字符值中的十六进制字符。

        例如: XML 1.0 文档中不允许使用 Unicode 字符 8，因此必须将其转义为 _x0008_
        """

        return self.findall(qn('vt:lpwstr'))

    @property
    def bstr(self) -> list[CT_XSD_String]:
        """基本字符串

        Basic String

        该元素定义了一个二进制基本字符串变体类型，它可以存储任何有效的 Unicode 字符。
        不能直接在 XML 中表示的 Unicode 字符（如 XML 1.0 规范所定义）应使用 Unicode 数字字符表示转义字符格式 xHHHH 进行转义，
        其中 H 表示字符值中的十六进制字符。

        例如: XML 1.0 文档中不允许使用 Unicode 字符 8，因此应将其转义为 _x0008_

        要存储转义序列的文字形式，初始下划线本身应被转义（即存储为 _x005F_）

        例如: 字符串文字_x0008_ 将存储为 _x005F_x0008_
        """

        return self.findall(qn('vt:bstr'))

    @property
    def date(self) -> list[CT_XSD_Datetime]:
        """日期和时间

        Date and Time

        此元素指定 RFC 3339 中定义的日期时间类型的日期变体类型。

        此元素的可能值由 W3C XML 架构 dateTime 数据类型定义。
        """

        return self.findall(qn('vt:date'))

    @property
    def filetime(self) -> list[CT_XSD_Datetime]:
        """文件时间

        File Time

        此元素指定 RFC 3339 中定义的日期时间类型的文件时间变体类型。

        此元素的可能值由 W3C XML 架构 dateTime 数据类型定义。
        """

        return self.findall(qn('vt:filetime'))

    @property
    def bool(self) -> list[CT_XSD_Boolean]:
        """
        该元素指定布尔变量类型。

        该元素的可能值由 W3C XML 架构布尔数据类型定义。
        """

        return self.findall(qn('vt:bool'))

    @property
    def cy(self) -> list[ST_Cy]:
        """货币

        Currency

        该元素指定小数点后恰好四位数字的货币变体类型。

        该元素的可能值由 ST_Cy 简单类型 ([§22.4.3.2]) 定义。
        """

        return [ST_Cy(ele.text) for ele in self.findall(qn('vt:cy'))]

    @property
    def error(self) -> list[OxmlBaseElement]:
        """错误状态代码

        Error Status Code

        错误元素指定 0xHHHHHHHH 形式的 32 位错误状态代码变量类型。 每个H代表一个十六进制数字。

        该元素的可能值由 ST_Error 简单类型（[§22.4.3.3]）定义。
        """

        return self.findall(qn('vt:error'))

    @property
    def clsid(self) -> list[s_ST_Guid]:
        """class id

        该元素指定类 ID 变体类型。 该值应为全局唯一标识符，格式为： {HHHHHHHH-HHHH-HHHH-HHHH-HHHHHHHH}.

        该元素的可能值由 ST_Guid 简单类型 ([§22.9.2.4]) 定义。
        """

        return self.findall(qn('vt:clsid'))

    def items(self, base_type_value: str) -> list[SubBaseElement]:
        """
        获取vector数组中的单个项的合集
        """

        return getattr(self, base_type_value)

    @property
    def base_type(self) -> ST_VectorBaseType:
        """向量基本类型

        baseType 属性指定向量的基本变体类型.

        允许的值为: variant、i1、i2、i4、i8、ui1、ui2、ui4、ui8、r4、r8、lpstr、lpwstr、bstr、date、filetime、bool、cy、error 和 clsid.

        该属性的可能值由 ST_VectorBaseType 简单类型定义 ([§22.4.3.4]).
        """

        val = self.attrib['baseType']

        return ST_VectorBaseType(val)

    @property
    def size(self) -> int:
        """向量大小

        改值指定子元素的个数
        """

        val = self.attrib['size']

        return int(val)


class CT_Array(OxmlBaseElement):
    """数组

    22.4.2.1 array (数组)

    数组元素定义数组变体类型。 数组内容应具有由 baseType 属性指定的统一类型。 数组的内容是使用适当变体类型的重复子元素来定义的。

    可以通过使用“,”分隔符在 lBound 和 uBound 属性中指定每个维度的长度来定义多维数组。 多维数组的子元素按照声明维度的顺序沿每个维度进行索引。

    换句话说，数组应填充如下：

    - 第一个索引应增加到其最大值 [Example: [0,0,0] 至 [max,0,0] end example]
    - 第二个索引应增加到其最大值 [Example: [0,1,0] 至 [0,max,0] endexample]
    - 应填充后续索引，直到添加所有提供的值
    - 数组中的所有其他值均应为空值（i.e: 不应假定默认值）

    例如:

    “i4”类型的 2x3 变体类型数组指定如下：

    <vt:array lBounds="0,0" uBounds="1,2" baseType="i4">
        <vt:i4>0</vt:i4>
        <vt:i4>1</vt:i4>
        <vt:i4>2</vt:i4>
        <vt:i4>3</vt:i4>
        <vt:i4>4</vt:i4>
    </vt:array>

    得到数组: [0,0] = 0, [1,0] = 1, [0,1] = 2, [1,1] = 3, [0,2] = 4.
    """

    @property
    def value_lst(
        self,
    ) -> list[SubBaseElement]:
        """
        数组元素列表
        """

        tags = (
            qn('vt:variant'),
            qn('vt:i1'),
            qn('vt:i2'),
            qn('vt:i4'),
            qn('vt:int'),
            qn('vt:ui1'),
            qn('vt:ui2'),
            qn('vt:ui4'),
            qn('vt:uint'),
            qn('vt:r4'),
            qn('vt:r8'),
            qn('vt:decimal'),
            qn('vt:bstr'),
            qn('vt:date'),
            qn('vt:bool'),
            qn('vt:error'),
            qn('vt:cy'),
        )

        return self.choice_one_list_child(*tags)

    @property
    def l_bounds(self) -> int:
        """数组下限属性

        Array Lower Bounds Attribute

        lBounds 属性以以下格式指定数组的下限：#, #, # … #，其中每个 # 代表一个整数。

        此属性的可能值由 W3C XML Schema int 数据类型定义。
        """

        val = self.attrib['lBounds']

        return int(val)

    @property
    def u_bounds(self) -> int:
        """数组上限属性

        Array Upper Bounds Attribute

        uBounds 属性以以下格式指定数组的上限：#, #, # … #，其中每个 # 代表一个整数.

        此属性的可能值由 W3C XML Schema int 数据类型定义。
        """

        val = self.attrib['uBounds']

        return int(val)

    @property
    def base_type(self) -> ST_ArrayBaseType:
        """数组基本类型

        Array Base Type

        baseType 属性指定数组的基本变体类型.

        允许的值为: variant、i1、i2、i4、int、ui1、ui2、ui4、uint、r4、r8、decimal、bstr、date、bool、cy 和 error.

        该属性的可能值由 ST_ArrayBaseType 简单类型定义 ([§22.4.3.1]).
        """

        val = self.attrib['baseType']

        return ST_ArrayBaseType(val)


class CT_Variant(OxmlBaseElement):
    """变体

    该元素可以包含任意变体类型的 1 个子元素。 该元素仅作为向量或数组变体类型的子元素有效。
    """

    @property
    def variant_value(
        self,
    ) -> (
        CT_Variant
        | CT_Vector
        | CT_Array
        | CT_XSD_Base64
        | CT_Empty
        | CT_Null
        | CT_XSD_Byte
        | CT_XSD_Short
        | CT_XSD_Int
        | CT_XSD_Long
        | CT_XSD_UnsignedByte
        | CT_XSD_UnsignedShort
        | CT_XSD_UnsignedInt
        | CT_XSD_UnsignedLong
        | CT_XSD_Float
        | CT_XSD_Double
        | CT_XSD_Decimal
        | CT_XSD_String
        | CT_XSD_Datetime
        | CT_XSD_Boolean
        | OxmlBaseElement
        | CT_Vstream
    ):
        """
        变体值

        <xsd:choice minOccurs="1" maxOccurs="1">
        """

        tags = (
            qn('vt:variant'),
            qn('vt:vector'),
            qn('vt:array'),
            qn('vt:blob'),
            qn('vt:oblob'),
            qn('vt:empty'),
            qn('vt:null'),
            qn('vt:i1'),
            qn('vt:i2'),
            qn('vt:i4'),
            qn('vt:i8'),
            qn('vt:int'),
            qn('vt:ui1'),
            qn('vt:ui2'),
            qn('vt:ui4'),
            qn('vt:ui8'),
            qn('vt:uint'),
            qn('vt:r4'),
            qn('vt:r8'),
            qn('vt:decimal'),
            qn('vt:lpstr'),
            qn('vt:lpwstr'),
            qn('vt:bstr'),
            qn('vt:date'),
            qn('vt:filetime'),
            qn('vt:bool'),
            qn('vt:cy'),
            qn('vt:error'),
            qn('vt:stream'),
            qn('vt:ostream'),
            qn('vt:storage'),
            qn('vt:ostorage'),
            qn('vt:vstream'),
            qn('vt:clsid'),
        )

        return self.choice_one_child(*tags)


class CT_Vstream(OxmlBaseElement):
    """二进制版本化流

    该元素指定二进制版本化流变体类型。

    该类型定义如下：具有 GUID 版本（版本属性）的流元素内容。
    """

    @property
    def version(self) -> s_ST_Guid:
        """版本

        <xsd:extension base="xsd:base64Binary">
            <xsd:attribute name="version" type="s:ST_Guid"/>
        </xsd:extension>
        """

        val = self.attrib.get('version')

        return s_ST_Guid(val)


shared_doc_pr_variant_namespace = lookup.get_namespace(namespace_vt)
shared_doc_pr_variant_namespace[None] = OxmlBaseElement
shared_doc_pr_variant_namespace['variant'] = CT_Variant
shared_doc_pr_variant_namespace['vector'] = CT_Vector
shared_doc_pr_variant_namespace['array'] = CT_Array
shared_doc_pr_variant_namespace['blob'] = CT_XSD_Base64
shared_doc_pr_variant_namespace['oblob'] = CT_XSD_Base64
shared_doc_pr_variant_namespace['empty'] = CT_Empty
shared_doc_pr_variant_namespace['null'] = CT_Null
shared_doc_pr_variant_namespace['i1'] = CT_XSD_Byte
shared_doc_pr_variant_namespace['i2'] = CT_XSD_Short
shared_doc_pr_variant_namespace['i4'] = CT_XSD_Int
shared_doc_pr_variant_namespace['i8'] = CT_XSD_Long
shared_doc_pr_variant_namespace['int'] = CT_XSD_Int
shared_doc_pr_variant_namespace['ui1'] = CT_XSD_UnsignedByte
shared_doc_pr_variant_namespace['ui2'] = CT_XSD_UnsignedShort
shared_doc_pr_variant_namespace['ui4'] = CT_XSD_UnsignedInt
shared_doc_pr_variant_namespace['ui8'] = CT_XSD_UnsignedLong
shared_doc_pr_variant_namespace['uint'] = CT_XSD_UnsignedInt
shared_doc_pr_variant_namespace['r4'] = CT_XSD_Float
shared_doc_pr_variant_namespace['r8'] = CT_XSD_Double
shared_doc_pr_variant_namespace['decimal'] = CT_XSD_Decimal
shared_doc_pr_variant_namespace['lpstr'] = CT_XSD_String
shared_doc_pr_variant_namespace['lpwstr'] = CT_XSD_String
shared_doc_pr_variant_namespace['bstr'] = CT_XSD_String
shared_doc_pr_variant_namespace['date'] = CT_XSD_Datetime
shared_doc_pr_variant_namespace['filetime'] = CT_XSD_Datetime
shared_doc_pr_variant_namespace['bool'] = CT_XSD_Boolean
# shared_bibliography_namespace["cy"] = ST_Cy
shared_doc_pr_variant_namespace['cy'] = OxmlBaseElement
# shared_bibliography_namespace["error"] = ST_Error
shared_doc_pr_variant_namespace['error'] = OxmlBaseElement
shared_doc_pr_variant_namespace['stream'] = CT_XSD_Base64
shared_doc_pr_variant_namespace['ostream'] = CT_XSD_Base64
shared_doc_pr_variant_namespace['storage'] = CT_XSD_Base64
shared_doc_pr_variant_namespace['ostorage'] = CT_XSD_Base64
shared_doc_pr_variant_namespace['vstream'] = CT_Vstream
# shared_bibliography_namespace["clsid"] = s_ST_Guid
shared_doc_pr_variant_namespace['clsid'] = CT_XSD_String
