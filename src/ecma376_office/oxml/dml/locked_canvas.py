"""
对应xsd: dml-lockedCanvas.xsd

前缀: lc

命名空间: http://purl.oclc.org/ooxml/drawingml/lockedCanvas

<?xml version="1.0" encoding="utf-8"?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"
  xmlns="http://purl.oclc.org/ooxml/drawingml/lockedCanvas"
  xmlns:a="http://purl.oclc.org/ooxml/drawingml/main"
  xmlns:r="http://purl.oclc.org/ooxml/officeDocument/relationships"
  elementFormDefault="qualified"
  targetNamespace="http://purl.oclc.org/ooxml/drawingml/lockedCanvas">
  <xsd:import namespace="http://purl.oclc.org/ooxml/drawingml/main" schemaLocation="dml-main.xsd"/>
  <xsd:element name="lockedCanvas" type="a:CT_GvmlGroupShape"/>
</xsd:schema>
"""

from __future__ import annotations

import logging
from typing import TypeVar

from ecma376_office.oxml.base import OxmlBaseElement, lookup
from ecma376_office.oxml.dml.main import CT_GvmlGroupShape as a_CT_GvmlGroupShape

namespace_lc = 'http://purl.oclc.org/ooxml/drawingml/diagram'

logger = logging.getLogger(__name__)

ns_map = {
    'lc': 'http://purl.oclc.org/ooxml/drawingml/lockedCanvas',  # 当前命名空间
    'a': 'http://purl.oclc.org/ooxml/drawingml/main',
    'r': 'http://purl.oclc.org/ooxml/officeDocument/relationships',
}


def qn(tag: str):
    """将 dc:creator 这种的标签,转换为 {http://purl.org/dc/elements/1.1/}creator 这样的形式"""

    global ns_map

    if ':' not in tag:
        return tag

    ns_prefix, ns = tag.split(':')

    return f'{{{ns_map[ns_prefix]}}}{ns}'


SubBaseElement = TypeVar('SubBaseElement', bound=OxmlBaseElement)


dml_locked_canvas_namespace = lookup.get_namespace(namespace_lc)
dml_locked_canvas_namespace[None] = OxmlBaseElement


dml_locked_canvas_namespace['lockedCanvas'] = a_CT_GvmlGroupShape  # 根节点之一

# 公共元素:
