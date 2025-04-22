"""内置XSD类型"""

from datetime import datetime
from typing import AnyStr, NewType, Optional

from lxml import etree, objectify

from ecma376_office.oxml.exceptions import OxmlAttributeValidateError, OxmlElementValidateError
from ecma376_office.oxml.utils import AnyStrToStr

# 别名
# 参考:https://hellowac.github.io/mypy-zh-cn/more_types.html#newtype类型
XSD_AnyURI = NewType('XSD_AnyURI', str)
XSD_ID = NewType('XSD_ID', str)
XSD_String = NewType('XSD_String', str)
XSD_Token = NewType('XSD_Token', str)
XSD_DateTime = NewType('XSD_DateTime', datetime)
XSD_Base64Binary = NewType('XSD_Base64Binary', str)
XSD_Byte = NewType('XSD_Byte', bytes)
XSD_Short = NewType('XSD_Short', int)
XSD_Int = NewType('XSD_Int', int)
XSD_Long = NewType('XSD_Long', int)
XSD_UnsignedByte = NewType('XSD_UnsignedByte', bytes)
XSD_UnsignedShort = NewType('XSD_UnsignedShort', int)
XSD_UnsignedInt = NewType('XSD_UnsignedInt', int)
XSD_UnsignedLong = NewType('XSD_UnsignedLong', int)
XSD_Float = NewType('XSD_Float', float)
XSD_Decimal = NewType('XSD_Decimal', float)
XSD_Double = NewType('XSD_Double', float)
XSD_Boolean = NewType('XSD_Boolean', bool)

# 转换方法


def to_xsd_datetime(xml_val: Optional[AnyStr]) -> Optional[XSD_DateTime]:
    val = AnyStrToStr(xml_val)

    if not val:
        return None

    return XSD_DateTime(datetime.strptime(val, '%Y-%m-%dT%H:%M:%SZ'))


def to_xsd_bool(val: Optional[str | bytes], none: bool = False) -> XSD_Boolean:
    """将 xsd:boolean 的值转为 True 或 False

    none: 对应 val 为 None 时, 应返回的值(默认值)
    """

    if val is None:
        return XSD_Boolean(none)

    _val = val.decode() if isinstance(val, bytes) else val

    if _val not in {'1', '0', 'true', 'false'}:
        msg = f'预期外的值: {_val}'
        raise OxmlAttributeValidateError(msg)

    return XSD_Boolean(_val in {'1', 'true'})


def to_xsd_unsigned_int(xml_val: AnyStr) -> XSD_UnsignedInt:
    """转为 int"""

    val = AnyStrToStr(xml_val)

    int_val = int(val)

    if not (0 <= int_val <= 4294967295):
        msg = f'预期外的值: {int_val}'
        raise OxmlAttributeValidateError(msg)

    return XSD_UnsignedInt(int_val)


def to_xsd_unsigned_byte(xml_val: AnyStr) -> XSD_UnsignedByte:
    """转为 int"""

    if isinstance(xml_val, bytes):
        return XSD_UnsignedByte(xml_val)

    return XSD_UnsignedByte(xml_val.encode())


def to_xsd_byte(xml_val: AnyStr) -> XSD_Byte:
    """转为 byte"""

    if isinstance(xml_val, bytes):
        return XSD_Byte(xml_val)

    return XSD_Byte(xml_val.encode())


def to_xsd_double(xml_val: AnyStr) -> XSD_Double:
    """转为 byte"""

    if isinstance(xml_val, bytes):
        return XSD_Double(float(xml_val.decode()))

    return XSD_Double(float(xml_val))


##


def oxml_tostring(
    elm: etree.ElementBase,
    encoding: str = 'unicode',
    pretty_print: bool = False,
    standalone: bool = False,
):
    """将元素转为字符串

    参考: https://lxml.de/apidoc/lxml.etree.html

    Args:

        elm (_type_): 要转为str的元素

        encoding (str, optional): 编码. 默认为 "unicode".

        pretty_print (bool, optional): 美化输出. 默认为 False.

        standalone (bool, optional): 独立xml声明. 默认为 False.
    """
    # 如果 xsi 参数未设置为 False，则 PowerPoint 将不会在没有修复步骤的情况下加载；
    # 如果省略此参数（或设置为 True），deannotate 会删除 core.xml 中的一些原始 xsi:type 标记

    objectify.deannotate(elm, xsi=False, cleanup_namespaces=True)
    return etree.tostring(elm, encoding=encoding, pretty_print=pretty_print, standalone=standalone)


# ===========================================================================
# 自定义元素类的基类
# ===========================================================================


class XsdOxmlBaseElement(objectify.ObjectifiedElement):
    """
    所有自定义元素类的基类，用于在一处向所有类添加标准化行为。
    """

    @property
    def xml(self):
        """
        返回此元素的 XML 字符串，适合测试目的。 打印优化，易于阅读，并且顶部没有 XML 声明。
        """

        return oxml_tostring(self, encoding='unicode', pretty_print=True)

    @property
    def local_tagname(self):
        """本地标签名

        返回不包含命名空间前缀的标签名
        """

        i = self.tag.find('}')
        return self.tag[i + 1 :]

    def __str__(self):
        return f'{self.text or ""}'

    def __repr__(self):
        return f'{self.text or ""}'


class CT_XSD_Base64(XsdOxmlBaseElement):
    """

    表示 xsd:base64Binary
    """

    @property
    def value(self) -> XSD_Base64Binary:
        """
        aaa
        """

        return XSD_Base64Binary(AnyStrToStr(self.text))


class CT_XSD_Byte(XsdOxmlBaseElement):
    """

    表示 xsd:byte
    """

    @property
    def value(self) -> XSD_Byte:
        """
        aaa
        """

        val = self.text

        if val is None:
            return XSD_Byte(b'')

        return XSD_Byte(val.encode())


class CT_XSD_Short(XsdOxmlBaseElement):
    """

    表示 xsd:short
    """

    @property
    def value(self) -> XSD_Short:
        """
        aaa
        """

        val = self.text

        if val is None:
            return XSD_Short(0)

        return XSD_Short(int(val))


class CT_XSD_Int(XsdOxmlBaseElement):
    """

    表示 xsd:int
    """

    @property
    def value(self) -> XSD_Int:
        """
        aaa
        """

        val = self.text

        if val is None:
            return XSD_Int(0)

        return XSD_Int(int(val))


class CT_XSD_Long(XsdOxmlBaseElement):
    """

    表示 xsd:long
    """

    @property
    def value(self) -> XSD_Long:
        """
        aaa
        """

        val = self.text

        if val is None:
            return XSD_Long(0)

        return XSD_Long(int(val))


class CT_XSD_UnsignedByte(XsdOxmlBaseElement):
    """

    表示 xsd:unsignedByte
    """

    @property
    def value(self) -> XSD_UnsignedByte:
        """
        aaa
        """

        val = self.text

        if val is None:
            return XSD_UnsignedByte(b'')

        return XSD_UnsignedByte(val.encode())


class CT_XSD_UnsignedShort(XsdOxmlBaseElement):
    """

    表示 xsd:unsignedShort

    这里转换可能有问题，遇到再说
    """

    @property
    def value(self) -> XSD_UnsignedShort:
        """
        aaa
        """

        val = self.text

        if val is None:
            return XSD_UnsignedShort(0)

        return XSD_UnsignedShort(int(val))


class CT_XSD_UnsignedInt(XsdOxmlBaseElement):
    """

    表示 xsd:int
    """

    @property
    def value(self) -> XSD_UnsignedInt:
        val = self.text

        if val is None:
            return XSD_UnsignedInt(0)

        return XSD_UnsignedInt(int(val))


class CT_XSD_UnsignedLong(XsdOxmlBaseElement):
    """

    表示 xsd:int
    """

    @property
    def value(self) -> XSD_UnsignedLong:
        val = self.text

        if val is None:
            return XSD_UnsignedLong(0)

        return XSD_UnsignedLong(int(val))


class CT_XSD_Float(XsdOxmlBaseElement):
    """

    表示 xsd:float
    """

    @property
    def value(self) -> XSD_Float:
        """
        aaa
        """

        val = self.text

        if val is None:
            return XSD_Float(0)

        return XSD_Float(float(val))


class CT_XSD_Double(XsdOxmlBaseElement):
    """

    表示 xsd:doubule
    """

    @property
    def value(self) -> XSD_Double:
        """
        aaa
        """

        val = self.text

        if val is None:
            return XSD_Double(0)

        return XSD_Double(float(val))


class CT_XSD_Decimal(XsdOxmlBaseElement):
    """

    表示 xsd:int
    """

    @property
    def value(self) -> XSD_Decimal:
        """
        aaa
        """

        val = self.text

        if val is None:
            return XSD_Decimal(0)

        return XSD_Decimal(float(val))


class CT_XSD_String(XsdOxmlBaseElement):
    """

    表示 xsd:string
    """

    @property
    def value(self) -> XSD_String:
        """
        aaa
        """

        val = self.text

        if val is None:
            return XSD_String('')

        return XSD_String(val)


class CT_XSD_Datetime(XsdOxmlBaseElement):
    """

    表示 xsd:int
    """

    @property
    def value(self) -> XSD_DateTime:
        """
        aaa
        """

        val = self.text

        if val is None:
            msg = '日期时间应不为空'
            raise OxmlElementValidateError(msg)

        dt = to_xsd_datetime(val)

        if dt is not None:
            return dt

        msg = '日期时间应不为空'
        raise OxmlElementValidateError(msg)


class CT_XSD_Boolean(XsdOxmlBaseElement):
    """

    表示 xsd:int
    """

    @property
    def value(self) -> XSD_Boolean:
        """
        aaa
        """

        val = self.text

        return XSD_Boolean(to_xsd_bool(val, none=False))
