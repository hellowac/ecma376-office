"""
对应xsd: shared-documentPropertiesCustom.xsd

前缀: 'cp'

命名空间: http://purl.oclc.org/ooxml/officeDocument/customProperties

<?xml version="1.0" encoding="utf-8"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"
  xmlns="http://schemas.openxmlformats.org/officeDocument/2006/custom-properties"
  xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"
  xmlns:s="http://schemas.openxmlformats.org/officeDocument/2006/sharedTypes"
  targetNamespace="http://schemas.openxmlformats.org/officeDocument/2006/custom-properties"
  blockDefault="#all" elementFormDefault="qualified">
  <xsd:import namespace="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"
    schemaLocation="shared-documentPropertiesVariantTypes.xsd"/>
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

namespace_cp = 'http://schemas.openxmlformats.org/officeDocument/2006/custom-properties'

namespace_vt = 'http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes'

namespace_s = 'http://schemas.openxmlformats.org/officeDocument/2006/sharedTypes'

logger = logging.getLogger(__name__)

ns_map = {
    'cp': namespace_cp,  # 当前命名空间
    'vt': namespace_vt,
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


class CT_Property(OxmlBaseElement):
    """属性

    22.3.2.2 property (Custom File Property)

    该元素指定单个自定义文件属性。
    自定义文件属性类型是通过文件属性变体类型命名空间中的子元素定义的。
    可以通过设置适当的变体类型子元素值来设置自定义文件属性值。
    """

    @property
    def propert_(
        self,
    ) -> OxmlBaseElement:
        """
        属性值

        <xsd:choice minOccurs="1" maxOccurs="1">
            <xsd:element ref="vt:vector"/>
            <xsd:element ref="vt:array"/>
            <xsd:element ref="vt:blob"/>
            <xsd:element ref="vt:oblob"/>
            ...
        </xsd:choice>
        """

        tags = (
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

        return self.choice_require_one_child(*tags)  # type: ignore

    @property
    def format_id(self) -> s_ST_Guid:
        """格式ID

        Format ID

        将自定义属性与 OLE 属性唯一关联。

        该属性的值是一个全局唯一标识符，其形式为 {HHHHHHHHHHHH-HHHH-HHHH-HHHHHHHH}，其中每个 H 都是十六进制。

        该属性的可能值由 ST_Guid 简单类型定义 ([§22.9.2.4]).
        """

        val = self.attrib['fmtid']

        return s_ST_Guid(utils.AnyStrToStr(val))  # type: ignore

    @property
    def pid(self) -> int:
        """属性ID

        Property ID

        将自定义属性与 OLE 属性唯一关联.

        此属性的可能值由 W3C XML Schema int 数据类型定义.
        """

        val = self.attrib['pid']

        return int(val)

    @property
    def name(self) -> Optional[str]:
        """自定义文件属性名称

        Custom File Property Name

        指定此自定义文件属性的名称.

        此属性的可能值由 W3C XML 架构字符串数据类型定义。
        """

        val = self.attrib.get('name')

        if val is None:
            return None

        return utils.AnyStrToStr(val)  # type: ignore

    @property
    def link_target(self) -> Optional[str]:
        """书签链接目标

        Bookmark Link Target

        指定当前文档中书签的名称（对于 WordprocessingML），或者表或命名单元格（对于 SpreadsheetML），应从中提取此自定义文档属性的值。

        如果存在此属性，则此元素下的任何值都应被视为缓存，并在保存时替换为此书签的值（如果存在）。 如果书签不存在，则该链接应被视为已损坏，并且应保留缓存的值.

        此属性的可能值由 W3C XML 架构字符串数据类型定义。
        """

        val = self.attrib.get('linkTarget')

        if val is None:
            return None

        return utils.AnyStrToStr(val)  # type: ignore


class CT_Properties(OxmlBaseElement):
    """

    22.3.2.1 Properties (自定义文件属性)

    自定义文件属性部分的父元素.

    该元素内容模型 (CT_Properties) 的 W3C XML 模式定义位于 §A.6.3 中。
    """

    @property
    def property_lst(self) -> list[CT_Property]:
        """自定义文件属性列表"""

        return self.findall(qn('cp:property'))  # type: ignore


shared_doc_custom_pr_namespace = lookup.get_namespace(namespace_cp)
shared_doc_custom_pr_namespace[None] = OxmlBaseElement
shared_doc_custom_pr_namespace['property'] = CT_Property
shared_doc_custom_pr_namespace['Properties'] = CT_Properties
