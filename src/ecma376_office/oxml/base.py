"""
直接操作 Open XML 并提供对 XML 元素的直接面向对象访问的类。
"""

import logging
from enum import Enum
from typing import Any, AnyStr, Generic, Optional, Self, TypeVar

from lxml import etree, objectify

from ecma376_office.oxml.exceptions import OxmlElementValidateError

logger = logging.getLogger(__name__)


# 配置 lxml.objectified XML解析器
# https://lxml.de/objectify.html#how-data-types-are-matched
oxml_parser = etree.XMLParser(remove_blank_text=True)

# 默认基于objectify后备查找方案
# https://lxml.de/apidoc/lxml.objectify.html#lxml.objectify.ObjectifyElementClassLookup
fallback_lookup = objectify.ObjectifyElementClassLookup()


class honk(objectify.ObjectifiedElement):
    @property
    def honking(self):
        return self.get('honking') == 'true'


# https://lxml.de/apidoc/lxml.etree.html#lxml.etree.CustomElementClassLookup
class MyLookup(objectify.ObjectifyElementClassLookup):
    # class MyLookup(etree.CustomElementClassLookup):
    """自定义类查找"""

    def lookup(self, node_type, document: etree._Document, namespace: str, name):
        from ecma376_office.oxml.dml.main import namespace_a

        logger.debug(f'{node_type = } {document =} {namespace = } {name= }')

        if node_type == 'element' and namespace == namespace_a and name == 'tint':
            logger.debug(f'{node_type = } {document =} {namespace = } {name= } + {"*" * 100}')
            return honk  # 这里更有选择性一点......
        return None  # 传递给（默认）后备


# 设置后备查找方案
# https://lxml.de/apidoc/lxml.etree.html#lxml.etree.ElementNamespaceClassLookup
lookup = etree.ElementNamespaceClassLookup(fallback_lookup)
# lookup = etree.ElementNamespaceClassLookup(MyLookup())

# 设置类的查找方案
oxml_parser.set_element_class_lookup(lookup)  # 默认后备查找


# ===========================================================================
# 函数
# ===========================================================================

T = TypeVar('T', bound=objectify.ObjectifiedElement)
PythonValueType = TypeVar('PythonValueType')
XMLValueType = TypeVar('XMLValueType')


def oxml_fromstring(text: AnyStr) -> Any:
    """``etree.fromstring()`` 使用 oxml 解析器的替换, 返回的类应该为ObjectifiedElement类的子类"""

    return objectify.fromstring(text, oxml_parser)


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


class OxmlBaseElement(objectify.ObjectifiedElement):
    """
    所有自定义元素类的基类，用于在一处向所有类添加标准化行为。
    """

    @property
    def have_chilren(self) -> bool:
        """
        返回此元素的是否不存在子元素
        """

        children = self.getchildren()  # type: ignore

        return len(children) > 0

    @property
    def xml(self) -> AnyStr:
        """
        返回此元素的 XML 字符串，适合测试目的。 打印优化，易于阅读，并且顶部没有 XML 声明。
        """

        return oxml_tostring(self, encoding='unicode', pretty_print=True)  # type: ignore

    @property
    def local_tagname(self):
        """本地标签名

        返回不包含命名空间前缀的标签名
        """

        i = self.tag.find('}')
        return self.tag[i + 1 :]

    def choice_require_one_child(self, *tag_names: str):
        """查找一个元素必须存在的元素

        针对xsd定义:

        <xsd:choice minOccurs="1" maxOccurs="1">
            <xsd:element ref="variant"/>
            <xsd:element ref="vector"/>
            <xsd:element ref="array"/>
            ...
        </xsd:choice>
        """

        for tagname in tag_names:
            child = self.find(tagname)  # type: ignore
            if child is not None:
                return child

        msg = f'缺少一个必须的元素: {tag_names = }'
        raise OxmlElementValidateError(msg)

    def choice_one_child(self, *tag_names: str):
        """查找一个元素可选存在的元素

        针对xsd定义:

        <xsd:choice minOccurs="0" maxOccurs="1">
            <xsd:element ref="variant"/>
            <xsd:element ref="vector"/>
            <xsd:element ref="array"/>
            ...
        </xsd:choice>
        """

        for tagname in tag_names:
            child = self.find(tagname)  # type: ignore
            if child is not None:
                return child
        return None

    def choice_one_list_child(self, *tag_names):
        """查找一个元素必须存在的元素

        针对xsd定义:

        <xsd:choice minOccurs="1" maxOccurs="unbounded">
            <xsd:element ref="variant"/>
            <xsd:element ref="i1"/>
            <xsd:element ref="i2"/>
            <xsd:element ref="i4"/>
            <xsd:element ref="int"/>
            ...
        </xsd:choice>
        """

        for tagname in tag_names:
            child_lst = self.findall(tagname)  # type: ignore
            if len(child_lst) > 0:
                return child_lst

        return []

    def choice_and_more(self, *tagnames: str) -> list[Any]:
        """选择多个标签，并且数量大于1

        针对:

        <xsd:group ref="EG_FillProperties" minOccurs="3" maxOccurs="unbounded"/>
        """

        return list(self.iterchildren(*tagnames, reversed=False))


# ===========================================================================
# 自定简单类型的基类
# ===========================================================================


class ST_BaseType(Generic[XMLValueType, PythonValueType]):
    """简单类型的基类"""

    def __init__(self, val: XMLValueType, *, python_value: Optional[PythonValueType] = None) -> None:
        self._val = val
        self._python_val = python_value
        self._xml_val: XMLValueType

    @property
    def value(self: Self):
        """返回校验后的值 python中的值"""

        # 保证调用此钩子，进行值的校验
        #
        self._validate()

        # if not self._python_val:
        #     raise OxmlAttributeValidateError(f"python值为空")

        return self._python_val

    @property
    def xml_value(self: Self):
        """返回校验后的值 xml序列化中的值"""

        # 保证调用此钩子，进行值的校验
        #
        self._validate()

        return self._xml_val

    def _validate(self: Self) -> None:
        """到python中的value值 子类应该复写此类"""

    def _validate_xml(self: Self) -> None:
        """到xml 中的value值 子类应该复写此类"""


class ST_BaseEnumType(Enum):
    """参考:

    合法的枚举成员和属性

    https://docs.python.org/zh-cn/3.10/library/enum.html#allowed-members-and-attributes-of-enumerations
    """

    @classmethod
    def have_value(cls, value: Any):
        """判断是否拥有某个值"""

        return value in [e.value for e in cls]
