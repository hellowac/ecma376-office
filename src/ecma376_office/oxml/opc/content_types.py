"""
对应xsd: opc-relationships.xsd

命名空间: http://schemas.openxmlformats.org/package/2006/relationships
"""

import logging
from typing import NewType

from ecma376_office.oxml.base import OxmlBaseElement, lookup
from ecma376_office.oxml.xsd_types import XSD_AnyURI

namespace_ct = 'http://schemas.openxmlformats.org/package/2006/content-types'


logger = logging.getLogger(__name__)

ns_map = {
    'ct': namespace_ct,  # 当前命名空间
}


def qn(tag: str):
    """将 dc:creator 这种的标签,转换为 {http://purl.org/dc/elements/1.1/}creator 这样的形式"""

    global ns_map

    if ':' not in tag:
        return tag

    ns_prefix, ns = tag.split(':')

    return f'{{{ns_map[ns_prefix]}}}{ns}'


# <xs:pattern value="([!$&amp;'\(\)\*\+,:=]|(%[0-9a-fA-F][0-9a-fA-F])|[:@]|[a-zA-Z0-9\-_~])+"/>
ST_Extension = NewType('ST_Extension', str)


# <xs:pattern value="(((([\p{IsBasicLatin}-[\p{Cc}&#127;\(\)&lt;&gt;@,;:\\&quot;/\[\]\?=\{\}\s\t]])+))/((([\p{IsBasicLatin}-[\p{Cc}&#127;\(\)&lt;&gt;@,;:\\&quot;/\[\]\?=\{\}\s\t]])+))((\s+)*;(\s+)*(((([\p{IsBasicLatin}-[\p{Cc}&#127;\(\)&lt;&gt;@,;:\\&quot;/\[\]\?=\{\}\s\t]])+))=((([\p{IsBasicLatin}-[\p{Cc}&#127;\(\)&lt;&gt;@,;:\\&quot;/\[\]\?=\{\}\s\t]])+)|(&quot;(([\p{IsLatin-1Supplement}\p{IsBasicLatin}-[\p{Cc}&#127;&quot;\n\r]]|(\s+))|(\\[\p{IsBasicLatin}]))*&quot;))))*)" />
ST_ContentType = NewType('ST_ContentType', str)


class CT_Default(OxmlBaseElement):
    """默认内容类型

    7.2.3.2.3 Types元素

    指定要应用于具有指定扩展名的部分的默认内容类型。
    """

    @property
    def content_type(self) -> ST_ContentType:
        """内容类型

        该属性使用 RFC 7231, 3.1.1.1 中定义的语法指定媒体类型(media type)。

        该属性是必需的(required)。

        指定的媒体类型应适用于任何匹配的部分（除非被Override元素覆盖）。

        该属性的可能值由简单类型 ST_ContentType定义，
        该类型在模式 opc-contentTypes.xsd (C.2) 中定义。
        """
        return ST_ContentType(self.attrib['ContentType'])  # type: ignore

    @property
    def extension(self):
        """文件扩展名

        该属性指定一个字符串作为文件扩展名。

        该属性是必需的(required)。

        Default 元素应匹配名称以句点（“.”）结尾的任何部分，后跟该属性的值。

        该属性的可能值由简单类型 ST_Extension 定义，
        该类型在模式 opc-contentTypes.xsd (C.2) 中定义。
        """
        return ST_Extension(self.attrib['Extension'])  # type: ignore


class CT_Override(OxmlBaseElement):
    """覆盖或指定一部分文件的内容类型

    Override元素应为默认映射未覆盖或不一致的部分指定媒体类型。
    """

    @property
    def content_type(self):
        """媒体类型

        该属性使用 RFC 7231, 3.1.1.1 中定义的语法指定媒体类型。

        该属性是必需的(required)。

        指定的媒体类型应适用于属性 PartName 中命名的部分。

        该属性的可能值由简单类型 ST_Extension 定义，该类型在模式 opc-contentTypes.xsd (C.2) 中定义。
        """
        return ST_ContentType(self.attrib['ContentType'])  # type: ignore

    @property
    def part_name(self) -> XSD_AnyURI:
        """部件名称

        该属性指定部件名称。

        该属性是必需的(required)。

        Override元素应匹配名称等于该属性值的部分。

        该属性的值范围应由 W3C XML 模式数据类型的 xsd:anyURI 简单类型定义。
        """
        return XSD_AnyURI(self.attrib['PartName'])  # type: ignore


class CT_Types(OxmlBaseElement):
    """
    ``<Types>`` 元素，[Content_Types].xml 中默认和覆盖元素的容器元素。

    参考: https://hellowac.github.io/ecma-376-zh-cn/xsd/opc/opc-contentTypes/
    """

    @property
    def defaults(self) -> list[CT_Default]:
        """默认内容类型集"""

        return self.findall(qn('ct:Default'))  # type: ignore

    @property
    def overrides(self) -> list[CT_Override]:
        """覆盖内容类型集"""

        return self.findall(qn('ct:Override'))  # type: ignore


content_type_namespace = lookup.get_namespace(namespace_ct)
content_type_namespace[None] = OxmlBaseElement
content_type_namespace['Default'] = CT_Default
content_type_namespace['Override'] = CT_Override
content_type_namespace['Types'] = CT_Types
