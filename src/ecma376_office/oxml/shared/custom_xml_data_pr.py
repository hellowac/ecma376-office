"""
对应xsd: shared-customXmlDataProperties.xsd

<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns="http://schemas.openxmlformats.org/officeDocument/2006/customXml"
    xmlns:s="http://schemas.openxmlformats.org/officeDocument/2006/sharedTypes"
    targetNamespace="http://schemas.openxmlformats.org/officeDocument/2006/customXml"
    elementFormDefault="qualified" attributeFormDefault="qualified" blockDefault="#all">
    <xsd:import namespace="http://schemas.openxmlformats.org/officeDocument/2006/sharedTypes"
        schemaLocation="shared-commonSimpleTypes.xsd"/>
    ...
</xsd:schema>
"""

from __future__ import annotations

import logging
from typing import Optional, TypeVar

from ecma376_office.oxml import utils
from ecma376_office.oxml.base import OxmlBaseElement, lookup
from ecma376_office.oxml.shared.common_simple_types import ST_Guid as s_ST_Guid
from ecma376_office.oxml.utils import AnyStrToStr

namespace_ds = 'http://schemas.openxmlformats.org/officeDocument/2006/customXml'

namespace_s = 'http://schemas.openxmlformats.org/officeDocument/2006/sharedTypes'

logger = logging.getLogger(__name__)

ns_map = {
    'ds': namespace_ds,  # 当前命名空间
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


class CT_DatastoreSchemaRef(OxmlBaseElement):
    """关联的XML模式

    22.5.2.2 schemaRef (关联的XML模式)

    此元素指定与自定义 XML 数据部分关联的单个 XML 架构。 该 XML 模式使用其目标名称空间进行标识，并且可以通过处理该文件内容的应用程序可用的任何方式进行定位。

    如果自定义 XML 部分在打开时无法使用指定的 XML 架构进行验证，则在随后保存文件时可以忽略此引用。

    例如: 对于自定义 XML 部件属性部件，请考虑以下内容:

    <ds:datastoreItem ds:itemID="{A67AC88A-A164-4ADE-8889-8826CE44DE6E}">
        <ds:schemaRefs>
            <ds:schemaRef ds:uri="http://www.example.com/exampleSchema" />
        </ds:schemaRefs>
    </ds:datastoreItem>

    schemaRef 元素包含对目标名称空间为 http://www.example.com/exampleSchema 的模式的单个 XML 模式引用, 然后，应用程序可以使用任何可用的方式找到并利用该名称空间的模式。
    """

    def uri(self) -> str:
        """关联 XML 模式(schema)的目标命名空间

        指定与此架构引用关联的 XML 架构的目标命名空间.
        """

        val = self.attrib['uri']

        return utils.AnyStrToStr(val)  # type: ignore


class CT_DatastoreSchemaRefs(OxmlBaseElement):
    """XML 模式(Schema)集

    此元素指定与父自定义 XML 部件关联的 XML 模式(Schema)集。
    可以引用任意数量的 XML 模式，然后使用该模式集合来验证相应自定义 XML 部件的内容。

    如果存在此元素，则应使用其中提供的一组 XML 模式来验证相应自定义 XML 部件的内容
    （包括明确不存在任何子元素，以指定不应使用任何自定义 XML 模式，即使其中一个是预置的）。

    如果省略此元素，则应用程序可以使用任何所需的方式确定用于验证此部分内容的 XML 模式集
    """

    def schema_ref_lst(self) -> list[CT_DatastoreSchemaRef]:
        """xml schema 集"""

        return self.findall(qn('ds:schemaRef'))  # type: ignore


class CT_DatastoreItem(OxmlBaseElement):
    """自定义XML数据项

    22.5.2.1 datastoreItem (自定义XML数据属性)

    此元素指定 Office Open XML 文档内单个自定义 XML 部分的属性。 此元素中指定的属性集附加到指定与此部分的关系的自定义 XML 部件。

    例如:

    <ds:datastoreItem ds:itemID="{A67AC88A-A164-4ADE-8889-8826CE44DE6E}">
        <ds:schemaRefs>
            <ds:schemaRef ds:uri="http://www.example.com/exampleSchema" />
        </ds:schemaRefs>
    </ds:datastoreItem>
    """

    def schema_refs(self) -> Optional[CT_DatastoreSchemaRefs]:
        """XML 模式(Schema)集"""

        return self.find(qn('ds:schemaRefs'))  # type: ignore

    def item_id(self) -> s_ST_Guid:
        """自定义 XML 数据 ID

        指定全局唯一标识符 (GUID)，用于唯一标识 Office Open XML 文档中的单个自定义 XML 部分.

        每个 itemID 值在本文档中的所有自定义 XML 数据部分中应是唯一的。 如果文档包含重复的 itemID 值，则应保留第一个值，并重新分配后续值.

        例如: 对于自定义 XML 部件属性部件，请考虑以下内容

        <w:datastoreItem w:itemID="{A67AC88A-A164-4ADE-8889-8826CE44DE6E}">
        …
        </w:datastoreItem>
        """

        val = self.attrib['itemID']

        return s_ST_Guid(AnyStrToStr(val))  # type: ignore


shared_cust_data_pr_namespace = lookup.get_namespace(namespace_ds)
shared_cust_data_pr_namespace[None] = OxmlBaseElement
shared_cust_data_pr_namespace['schemaRef'] = CT_DatastoreSchemaRef
shared_cust_data_pr_namespace['schemaRefs'] = CT_DatastoreSchemaRefs
shared_cust_data_pr_namespace['datastoreItem'] = CT_DatastoreItem
