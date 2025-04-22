"""
对应xsd: opc-relationships.xsd

命名空间: http://schemas.openxmlformats.org/package/2006/relationships
"""

import logging

from ecma376_office.oxml.base import OxmlBaseElement, ST_BaseEnumType, lookup
from ecma376_office.oxml.xsd_types import XSD_ID, XSD_AnyURI

namespace_rs = 'http://schemas.openxmlformats.org/package/2006/relationships'

logger = logging.getLogger(__name__)

ns_map = {
    'rs': namespace_rs,  # 当前命名空间
}


def qn(tag: str):
    """将 dc:creator 这种的标签,转换为 {http://purl.org/dc/elements/1.1/}creator 这样的形式"""

    global ns_map

    if ':' not in tag:
        return tag

    ns_prefix, ns = tag.split(':')

    return f'{{{ns_map[ns_prefix]}}}{ns}'


class ST_TargetMode(ST_BaseEnumType):
    """参考:

    1. https://hellowac.github.io/ecma-376-zh-cn/ecma-part2-refrence/#6534-关系元素
    2. https://hellowac.github.io/ecma-376-zh-cn/xsd/opc/opc-relationships/
    """

    External = 'External'  # 外部资源
    Internal = 'Internal'  # 内部资源


class CT_Relationship(OxmlBaseElement):
    """关系

    6.5.3.4 关系元素

    关系元素(Relationship element)应表示一种关系。 关系的源(source of a relationship)应是包含此关系元素的关系部分与之关联的包或部件。

    参考: https://hellowac.github.io/ecma-376-zh-cn/ecma-part2-refrence/#6534-关系元素
    """

    @property
    def rId(self) -> XSD_ID:
        """关系标识符

        该属性指定关系的标识符(identifier)。 Id 属性的值在关系部件中应该是唯一的(unique)。

        该属性是必需的(required)。

        例如:

        Id="A5FFC797514BC"

        该属性的值范围应由 W3C XML Schema数据类型的xsd:ID简单类型定义。
        """
        return XSD_ID(self.attrib['Id']) 

    @property
    def reltype(self) -> XSD_AnyURI:
        """关系类型

        relationship type

        该属性指定关系的关系类型(relationship type)。

        该属性是必需的(required)。

        可以比较关系类型以确定两个关系元素(Relationship elements)是否属于同一类型。

        此比较的执行方式与比较标识 XML 命名空间的 URI 时的方式相同：

        两个 URI 被视为字符串，并且当且仅当字符串具有相同的字符序列时才被视为相同。
        比较区分大小写，并且不会进行或撤消转义。
        """
        return XSD_AnyURI(self.attrib['Type'])  

    @property
    def target(self) -> XSD_AnyURI:
        """目标

        Target

        该属性指定关系的目标(target)。

        该属性是必需的(required)。

        - 如果 TargetMode 属性的值为 Internal，则 Target 属性应是对部件的相对引用。
        - 如果 TargetMode 属性的值为 External，则 Target 属性应为相对引用或绝对IRI。

        用于解析相对引用的基本 IRI 在 6.4 中定义。

        该属性的值范围应由 W3C XML Schema数据类型的 xsd:anyURI 简单类型定义。
        """
        return XSD_AnyURI(self.attrib['Target'])  

    @property
    def target_mode(self) -> ST_TargetMode:
        """目标模式

        TargetMode

        该属性指定关系的目标模式(target mode)。

        该属性是可选的(optional)，默认值为Internal。

        此属性的可能值为 Internal 和 External，由简单类型 ST_TargetMode 定义，
        该类型在模式(schema) opcrelationships.xsd(C.5) 中定义。
        """
        return ST_TargetMode(self.get('TargetMode', ST_TargetMode.Internal))


class CT_Relationships(OxmlBaseElement):
    """关系集

    参考: https://hellowac.github.io/ecma-376-zh-cn/xsd/opc/opc-relationships/
    """

    @property
    def relationships(self) -> list[CT_Relationship]:
        """返回所有的关系"""

        # print([el.tag for el in self.iterchildren()])

        # 直接访问子节点时，继承默认的命名空间
        # return self.Relationship  # type: ignore

        # 否则，需要指定命名空间
        # return self.iterchildren(tag=f"{{{namespace_pr}}}Relationship")  # type: ignore

        # res: List[CT_Relationship] = getattr(self, "Relationship")
        return self.findall(qn('rs:Relationship'))


relationship_namespace = lookup.get_namespace(namespace_rs)
relationship_namespace[None] = OxmlBaseElement
relationship_namespace['Relationship'] = CT_Relationship
relationship_namespace['Relationships'] = CT_Relationships
