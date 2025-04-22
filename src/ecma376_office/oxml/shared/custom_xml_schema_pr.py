"""
对应xsd: shared-customXmlSchemaProperties.xsd

<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"
  xmlns="http://schemas.openxmlformats.org/schemaLibrary/2006/main"
  targetNamespace="http://schemas.openxmlformats.org/schemaLibrary/2006/main"
  attributeFormDefault="qualified" elementFormDefault="qualified">
  ...
</xsd:schema>

23. 自定义 XML Schema参考

此命名空间定义一组属性，这些属性定义与存储在 Office Open XML 文档内容中的一个或多个自定义 XML 架构关联的位置和属性。 与文档的自定义 XML 标记关联的一组架构统称为该文档的schema库。 然后，schema库存储文档的自定义 XML 标记中使用的一组唯一 XML 命名空间，并允许应用程序使用适当的元数据“标记(tag)”这些命名空间。
"""

from __future__ import annotations

import logging
from typing import Optional

from ecma376_office.oxml import utils
from ecma376_office.oxml.base import OxmlBaseElement, lookup
from ecma376_office.oxml.xsd_types import XSD_String, XSD_Token

namespace_xp = 'http://schemas.openxmlformats.org/schemaLibrary/2006/main'

logger = logging.getLogger(__name__)

ns_map = {
    'xp': namespace_xp,  # 当前命名空间
}


def qn(tag: str):
    """将 dc:creator 这种的标签,转换为 {http://purl.org/dc/elements/1.1/}creator 这样的形式"""

    global ns_map

    if ':' not in tag:
        return tag

    ns_prefix, ns = tag.split(':')

    return f'{{{ns_map[ns_prefix]}}}{ns}'


class CT_Schema(OxmlBaseElement):
    """自定义XML schema 参考

    23.2.1 schema (Custom XML Schema Reference)

    该元素指定与单个 XML 命名空间关联的属性，应为其加载所有已知的 XML 模式，以便验证存储在该文档中的自定义 XML 标记。 可以适当地使用这些属性来定位与文档一起使用的自定义 XML 模式。 ECMA-376 不需要任何特定的 XML 模式语言。
    """

    def uri(self) -> XSD_String:
        """自定义 XML Schema 的命名空间

        指定与此架构引用关联的 XML 架构的目标命名空间.
        """

        val = self.attrib.get('uri', '')

        return XSD_String(utils.AnyStrToStr(val))  # type: ignore

    def manifest_location(self) -> Optional[XSD_String]:
        """补充 XML 文件位置

        指定补充 XML 文件的位置，加载此文档时可以下载并解析该文件，以提供其他应用程序定义的功能。 该文件的内容是应用程序定义的.
        """

        val = self.attrib.get('manifestLocation')

        if val is None:
            return None

        return XSD_String(utils.AnyStrToStr(val))  # type: ignore

    def schema_location(self) -> Optional[XSD_String]:
        """自定义 XML Schema 位置

        指定加载此文档时应下载和解析的 XML 架构文件的位置。
        """

        val = self.attrib.get('schemaLocation')

        if val is None:
            return None

        return XSD_String(utils.AnyStrToStr(val))  # type: ignore

    def schema_language(self) -> Optional[XSD_Token]:
        """Schema 语言

        指定模式语言的媒体类型或根命名空间.

        例如:

        <sl:schema … schemaLanguage="http:/relaxng.org/ns/structure/1.0" />
        """

        val = self.attrib.get('schemaLanguage')

        if val is None:
            return None

        return XSD_Token(utils.AnyStrToStr(val))  # type: ignore


class CT_SchemaLibrary(OxmlBaseElement):
    """自定义 XML schema补充数据

    23.2.2 schemaLibrary (嵌入式自定义 XML schema补充数据)

    此元素指定与当前 Office Open XML 文档中的自定义 XML 标记的内容关联的 XML 命名空间集。
    文档中引用的每个唯一命名空间都可以在此元素中由单个模式元素引用，而不管构成该命名空间的组成 XML 模式的数量如何。
    """

    def schema_lst(self) -> list[CT_Schema]:
        """schema 列表"""

        return self.findall(qn('xp:schema'))  # type: ignore


shared_custom_schema_pr_namespace = lookup.get_namespace(namespace_xp)
shared_custom_schema_pr_namespace[None] = OxmlBaseElement
shared_custom_schema_pr_namespace['schema'] = CT_Schema
shared_custom_schema_pr_namespace['schemaLibrary'] = CT_SchemaLibrary
