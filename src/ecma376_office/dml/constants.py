"""
DML 包所需的常量值
"""

from enum import StrEnum

from ecma376_office.constants import RELATIONSHIP_TYPE_BASE


class CONTENT_TYPE(StrEnum):  # noqa: N801
    """
    各个部件的内容类型
    """

    # -------------------------------------------------------------------------------------------
    # https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-15/#152-部件概览

    # 14.2.1 图表部件
    Chart = 'application/vnd.openxmlformats-officedocument.drawingml.viewProps+xml'

    # 14.2.2 图表绘制部件
    ChartDrawing = 'application/vnd.openxmlformats-officedocument.drawingml.chartshapes+xml'

    # 14.2.3 绘制颜色部件
    DiagramColors = 'application/vnd.openxmlformats-officedocument.drawingml.diagramColors+xml'

    # 14.2.4 绘制数据部件
    DiagramData = 'application/vnd.openxmlformats-officedocument.drawingml.diagramData+xml'

    # 14.2.5 绘制布局定义部件
    DiagramLayoutDefinition = 'application/vnd.openxmlformats-officedocument.drawingml.diagramLayout+xml'

    # 14.2.6 绘制样式部件
    DiagrameStyle = 'application/vnd.openxmlformats-officedocument.drawingml.diagramStyle+xml'

    # 14.2.7 主题部件
    Theme = 'application/vnd.openxmlformats-officedocument.theme+xml'

    # 14.2.8 主题覆盖部件
    ThemeOverride = 'application/vnd.openxmlformats-officedocument.themeOverride+xml'

    # 14.2.9 表格样式
    TableStyles = 'application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml'
    # -------------------------------------------------------------------------------------------


class NAMESPACE(StrEnum):
    """OPC XML 命名空间的常量值"""

    # -------------------------------------------------------------------------------------------
    # https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-15/#152-部件概览

    # 14.2.1 图表部件
    Chart = 'http://purl.oclc.org/ooxml/drawingml/chart'

    # 14.2.2 图表绘制部件
    ChartDrawing = 'http://purl.oclc.org/ooxml/drawingml/chart'

    # 14.2.3 绘制颜色部件
    DiagramColors = 'http://purl.oclc.org/ooxml/drawingml/diagram'

    # 14.2.4 绘制数据部件
    DiagramData = 'http://purl.oclc.org/ooxml/drawingml/diagram'

    # 14.2.5 绘制布局定义部件
    DiagramLayoutDefinition = 'http://purl.oclc.org/ooxml/drawingml/diagram'

    # 14.2.6 绘制样式部件
    DiagrameStyle = 'http://purl.oclc.org/ooxml/drawingml/diagram'

    # 14.2.7 主题部件
    Theme = 'http://purl.oclc.org/ooxml/drawingml/main'

    # 14.2.8 主题覆盖部件
    ThemeOverride = 'http://purl.oclc.org/ooxml/drawingml/main'

    # 14.2.9 表格样式
    TableStyles = 'http://purl.oclc.org/ooxml/drawingml/main'
    # -------------------------------------------------------------------------------------------


class RELATIONSHIP_TYPE(str, RELATIONSHIP_TYPE_BASE):
    """OPC 关系类型"""

    # -------------------------------------------------------------------------------------------
    # https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-15/#152-部件概览

    # 14.2.1 图表部件
    # Chart = "http://purl.oclc.org/ooxml/officeDocument/relationships/chart"
    Chart = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/chart'

    # 14.2.2 图表绘制部件
    ChartDrawing = 'http://purl.oclc.org/ooxml/officeDocument/relationships/chartUserShapes'

    # 14.2.3 绘制颜色部件
    # DiagramColors = (
    #     "http://purl.oclc.org/ooxml/officeDocument/relationships/diagramColors"
    # )
    DiagramColors = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/diagramColors'

    # 14.2.4 绘制数据部件
    # DiagramData = "http://purl.oclc.org/ooxml/officeDocument/relationships/diagramData"
    DiagramData = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/diagramData'

    # 14.2.5 绘制布局定义部件
    # DiagramLayoutDefinition = (
    #     "http://purl.oclc.org/ooxml/officeDocument/relationships/diagramLayout"
    # )
    DiagramLayoutDefinition = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/diagramLayout'

    # 14.2.6 绘制样式部件
    # DiagrameStyle = (
    #     "http://purl.oclc.org/ooxml/officeDocument/relationships/diagramQuickStyle"
    # )
    DiagrameStyle = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/diagramQuickStyle'

    # 14.2.7 主题部件
    # Theme = "http://purl.oclc.org/ooxml/officeDocument/relationships/theme"
    Theme = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme'

    # 14.2.8 主题覆盖部件
    # ThemeOverride = "http://purl.oclc.org/ooxml/officeDocument/relationships/themeOverride"
    ThemeOverride = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/themeOverride'

    # 14.2.9 表格样式
    # TableStyles = "http://purl.oclc.org/ooxml/officeDocument/relationships/tableStyles"
    TableStyles = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/tableStyles'

    # -------------------------------------------------------------------------------------------
