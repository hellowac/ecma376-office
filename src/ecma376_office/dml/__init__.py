# DML 相关的部件注册

from ecma376_office.dml.constants import CONTENT_TYPE as CT
from ecma376_office.dml.parts import (
    ChartDrawingPart,
    ChartPart,
    DiagramColorsPart,
    DiagramDataPart,
    DiagrameStylePart,
    DiagramLayoutDefinitionPart,
    TableStylesPart,
    ThemeOverridePart,
    ThemePart,
)
from ecma376_office.part import PART_TYPE_MAP

PART_TYPE_MAP.update({
    CT.Chart: ChartPart,
    CT.ChartDrawing: ChartDrawingPart,
    CT.DiagramColors: DiagramColorsPart,
    CT.DiagramData: DiagramDataPart,
    CT.DiagramLayoutDefinition: DiagramLayoutDefinitionPart,
    CT.DiagrameStyle: DiagrameStylePart,
    CT.Theme: ThemePart,
    CT.ThemeOverride: ThemeOverridePart,
    CT.TableStyles: TableStylesPart,
})
