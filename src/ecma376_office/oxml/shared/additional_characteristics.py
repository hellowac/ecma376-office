"""
对应xsd: shared-additionalCharacteristics.xsd

前缀: ''

命名空间: http://purl.oclc.org/ooxml/officeDocument/characteristics

<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"
  xmlns="http://schemas.openxmlformats.org/officeDocument/2006/characteristics"
  targetNamespace="http://schemas.openxmlformats.org/officeDocument/2006/characteristics"
  elementFormDefault="qualified">
  ...
</xsd:schema>
"""

from __future__ import annotations

import logging
from typing import Optional, TypeVar

from ecma376_office.oxml.base import OxmlBaseElement, ST_BaseEnumType, lookup
from ecma376_office.oxml.utils import AnyStrToStr
from ecma376_office.oxml.xsd_types import XSD_AnyURI

# namespace_ac = "http://purl.oclc.org/ooxml/officeDocument/characteristics"
namespace_ac = 'http://schemas.openxmlformats.org/officeDocument/2006/characteristics'

logger = logging.getLogger(__name__)

ns_map = {
    'ac': namespace_ac,  # 当前命名空间
}


def qn(tag: str):
    """将 dc:creator 这种的标签,转换为 {http://purl.org/dc/elements/1.1/}creator 这样的形式"""

    global ns_map

    if ':' not in tag:
        return tag

    ns_prefix, ns = tag.split(':')

    return f'{{{ns_map[ns_prefix]}}}{ns}'


SubBaseElement = TypeVar('SubBaseElement', bound=OxmlBaseElement)


class ST_Relation(ST_BaseEnumType):
    """特性关系类型

    22.7.3.1 ST_Relation (特性关系类型)

    这种简单类型指定特性的名称和值属性之间可能的关系.

    此简单类型的内容是 W3C XML Schema 字符串数据类型的限制.

    此简单类型仅限于下表中列出的值:

    - eq (Equal To)	等于
    - ge (Greater Than or Equal to)	大于或等于。
    - gt (Greater Than)	大于.
    - le (Less Than or Equal To)	小于或等于。
    - lt (Less Than)	小于.

    [Note: 此简单类型的内容模型 (ST_Relation) 的 W3C XML 模式定义位于 [§A.6.7] 中。 end note]

    """

    Ge = 'ge'
    Le = 'le'
    Gt = 'gt'
    Lt = 'lt'
    Eq = 'eq'


class CT_Characteristic(OxmlBaseElement):
    """单一特性

    22.7.2.2 characteristic (单一特性)

    该元素指定一个单一特性。 特性的类型由名称属性定义。
    """

    @property
    def name(self) -> str:
        """
        特性名称

        指定特性的名称。 name 属性的值没有限制，但每个名称应通过词汇属性与特定词汇相关联.

        参考文档.
        """

        val = self.attrib['name']

        return AnyStrToStr(val)  # type: ignore

    @property
    def relation(self) -> ST_Relation:
        """关系

        值与名称的关系

        指定应如何在此特性的上下文中解释值属性的内容.

        例如: 以下内容将指定应用程序支持从 0 到 10,000 列，并且应相应地解释列范围:

        <additionalCharacteristics>
            <characteristic name="numColumns" relation="le" val="10000"/>
            <characteristic name="numColumns" relation="ge" val="0"/>
        </additionalCharacteristics>

        该属性的可能值由 ST_Relation 简单类型 ([§22.7.3.1]) 定义。
        """

        val = self.attrib['relation']

        return ST_Relation(val)

    @property
    def value(self) -> str:
        """特性值

        指定特性的值.
        """

        val = self.attrib['val']

        return str(val)  # type: ignore

    @property
    def vocabulary(self) -> Optional[XSD_AnyURI]:
        """特性语法

        Characteristic Grammar

        指定一个 URI，该 URI 定义了用于解释名称属性值的特性语法.

        如果省略此属性，则应使用默认语法（如上面定义）.

        此属性的可能值由 W3C XML 架构 anyURI 数据类型定义.
        """

        val = self.attrib.get('vocabulary')

        if val is None:
            return None

        return XSD_AnyURI(AnyStrToStr(val))  # type: ignore


class CT_AdditionalCharacteristics(OxmlBaseElement):
    """附加特性集

    22.7.2.1 additionalCharacteristics (附加特性集)
    """

    @property
    def characteristic_lst(self) -> list[CT_Characteristic]:
        """
        附加特性列表

        <xsd:sequence>
            <xsd:element name="characteristic" type="CT_Characteristic" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:sequence>
        """

        return self.findall(qn('ac:characteristic'))  # type: ignore


shared_additional_character_namespace = lookup.get_namespace(namespace_ac)
shared_additional_character_namespace[None] = OxmlBaseElement
shared_additional_character_namespace['characteristic'] = CT_Characteristic
shared_additional_character_namespace['additionalCharacteristics'] = CT_AdditionalCharacteristics
