"""预置图形解析类"""

from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING

from ecma376_office.oxml.base import oxml_fromstring

if TYPE_CHECKING:
    from ecma376_office.oxml.preset.shapes import CT_PresetShape, CT_PresetShapeDefinitions

logger = logging.getLogger(__name__)


class PresetShapes:
    """预定义图形映射类 -- 单例模式"""

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        """会加载预定义的图形规则"""
        self.shapes: dict[str, CT_PresetShape] = {}

        preset_xml = os.path.join(os.path.dirname(__file__), 'presetShapeDefinitions.xml')

        with open(preset_xml, 'rb') as defs:
            definitions: CT_PresetShapeDefinitions = oxml_fromstring(defs.read())

            for defn in definitions.preset_shapes:
                self.shapes[defn.name] = defn

    def lookup(self, name: str):
        """获取指定名称的几何图形定义"""

        return self.shapes[name]
