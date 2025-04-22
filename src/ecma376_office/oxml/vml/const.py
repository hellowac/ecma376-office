"""名空空间前缀 参考: ecma-376 第一版

http://www.datypic.com/sc/ooxml/ss.html

| File Name                                 | Prefix              | Namespace                                                                 |
| ----------------------------------------- | ------------------- | ------------------------------------------------------------------------- |
| dml-audioVideo.xsd                        | a                   | http://schemas.openxmlformats.org/drawingml/2006/main                     |
| dml-baseStylesheet.xsd                    | a                   | http://schemas.openxmlformats.org/drawingml/2006/main                     |
| dml-baseTypes.xsd                         | a                   | http://schemas.openxmlformats.org/drawingml/2006/main                     |
| dml-chart.xsd                             | draw-chart          | http://schemas.openxmlformats.org/drawingml/2006/chart                    |
| dml-chartDrawing.xsd                      | cdr                 | http://schemas.openxmlformats.org/drawingml/2006/chartDrawing             |
| dml-compatibility.xsd                     | draw-compat         | http://schemas.openxmlformats.org/drawingml/2006/compatibility            |
| dml-diagramColorTransform.xsd             | draw-diag           | http://schemas.openxmlformats.org/drawingml/2006/diagram                  |
| dml-diagramDataModel.xsd                  | draw-diag           | http://schemas.openxmlformats.org/drawingml/2006/diagram                  |
| dml-diagramDefinition.xsd                 | draw-diag           | http://schemas.openxmlformats.org/drawingml/2006/diagram                  |
| dml-diagramElementPropertySet.xsd         | draw-diag           | http://schemas.openxmlformats.org/drawingml/2006/diagram                  |
| dml-diagramLayoutVariables.xsd            | draw-diag           | http://schemas.openxmlformats.org/drawingml/2006/diagram                  |
| dml-diagramStyleDefinition.xsd            | draw-diag           | http://schemas.openxmlformats.org/drawingml/2006/diagram                  |
| dml-diagramTypes.xsd                      | draw-diag           | http://schemas.openxmlformats.org/drawingml/2006/diagram                  |
| dml-documentProperties.xsd                | a                   | http://schemas.openxmlformats.org/drawingml/2006/main                     |
| dml-graphicalObject.xsd                   | a                   | http://schemas.openxmlformats.org/drawingml/2006/main                     |
| dml-graphicalObjectAnimation.xsd          | a                   | http://schemas.openxmlformats.org/drawingml/2006/main                     |
| dml-graphicalObjectFormat.xsd             | a                   | http://schemas.openxmlformats.org/drawingml/2006/main                     |
| dml-gvml.xsd                              | a                   | http://schemas.openxmlformats.org/drawingml/2006/main                     |
| dml-lockedCanvas.xsd                      | draw-lc             | http://schemas.openxmlformats.org/drawingml/2006/lockedCanvas             |
| dml-picture.xsd                           | draw-pic            | http://schemas.openxmlformats.org/drawingml/2006/picture                  |
| dml-shape3DCamera.xsd                     | a                   | http://schemas.openxmlformats.org/drawingml/2006/main                     |
| dml-shape3DLighting.xsd                   | a                   | http://schemas.openxmlformats.org/drawingml/2006/main                     |
| dml-shape3DScene.xsd                      | a                   | http://schemas.openxmlformats.org/drawingml/2006/main                     |
| dml-shape3DScenePlane.xsd                 | a                   | http://schemas.openxmlformats.org/drawingml/2006/main                     |
| dml-shape3DStyles.xsd                     | a                   | http://schemas.openxmlformats.org/drawingml/2006/main                     |
| dml-shapeEffects.xsd                      | a                   | http://schemas.openxmlformats.org/drawingml/2006/main                     |
| dml-shapeGeometry.xsd                     | a                   | http://schemas.openxmlformats.org/drawingml/2006/main                     |
| dml-shapeLineProperties.xsd               | a                   | http://schemas.openxmlformats.org/drawingml/2006/main                     |
| dml-shapeMiscellaneous.xsd                | a                   | http://schemas.openxmlformats.org/drawingml/2006/main                     |
| dml-shapeProperties.xsd                   | a                   | http://schemas.openxmlformats.org/drawingml/2006/main                     |
| dml-shapeStyle.xsd                        | a                   | http://schemas.openxmlformats.org/drawingml/2006/main                     |
| dml-spreadsheetDrawing.xsd                | draw-ssdraw         | http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing       |
| dml-styleDefaults.xsd                     | a                   | http://schemas.openxmlformats.org/drawingml/2006/main                     |
| dml-stylesheet.xsd                        | a                   | http://schemas.openxmlformats.org/drawingml/2006/main                     |
| dml-table.xsd                             | a                   | http://schemas.openxmlformats.org/drawingml/2006/main                     |
| dml-tableStyle.xsd                        | a                   | http://schemas.openxmlformats.org/drawingml/2006/main                     |
| dml-text.xsd                              | a                   | http://schemas.openxmlformats.org/drawingml/2006/main                     |
| dml-textBullet.xsd                        | a                   | http://schemas.openxmlformats.org/drawingml/2006/main                     |
| dml-textCharacter.xsd                     | a                   | http://schemas.openxmlformats.org/drawingml/2006/main                     |
| dml-textParagraph.xsd                     | a                   | http://schemas.openxmlformats.org/drawingml/2006/main                     |
| dml-textRun.xsd                           | a                   | http://schemas.openxmlformats.org/drawingml/2006/main                     |
| dml-wordprocessingDrawing.xsd             | wp                  | http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing    |
| pml-animationInfo.xsd                     | p                   | http://schemas.openxmlformats.org/presentationml/2006/main                |
| pml-baseTypes.xsd                         | p                   | http://schemas.openxmlformats.org/presentationml/2006/main                |
| pml-comments.xsd                          | p                   | http://schemas.openxmlformats.org/presentationml/2006/main                |
| pml-embedding.xsd                         | p                   | http://schemas.openxmlformats.org/presentationml/2006/main                |
| pml-presentation.xsd                      | p                   | http://schemas.openxmlformats.org/presentationml/2006/main                |
| pml-presentationProperties.xsd            | p                   | http://schemas.openxmlformats.org/presentationml/2006/main                |
| pml-slide.xsd                             | p                   | http://schemas.openxmlformats.org/presentationml/2006/main                |
| pml-slideSynchronizationData.xsd          | p                   | http://schemas.openxmlformats.org/presentationml/2006/main                |
| pml-userDefinedTags.xsd                   | p                   | http://schemas.openxmlformats.org/presentationml/2006/main                |
| pml-viewProperties.xsd                    | p                   | http://schemas.openxmlformats.org/presentationml/2006/main                |
| shared-additionalCharacteristics.xsd      | characteristics     | http://schemas.openxmlformats.org/officeDocument/2006/characteristics     |
| shared-bibliography.xsd                   | bibliography        | http://schemas.openxmlformats.org/officeDocument/2006/bibliography        |
| shared-customXmlDataProperties.xsd        | customXml           | http://schemas.openxmlformats.org/officeDocument/2006/customXml           |
| shared-customXmlSchemaProperties.xsd      | sl                  | http://schemas.openxmlformats.org/schemaLibrary/2006/main                 |
| shared-documentPropertiesCustom.xsd       | custom-properties   | http://schemas.openxmlformats.org/officeDocument/2006/custom-properties   |
| shared-documentPropertiesExtended.xsd     | extended-properties | http://schemas.openxmlformats.org/officeDocument/2006/extended-properties |
| shared-documentPropertiesVariantTypes.xsd | docPropsVTypes      | http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes      |
| shared-math.xsd                           | m                   | http://schemas.openxmlformats.org/officeDocument/2006/math                |
| shared-relationshipReference.xsd          | r                   | http://schemas.openxmlformats.org/officeDocument/2006/relationships       |
| sml-autoFilter.xsd                        | ssml                | http://schemas.openxmlformats.org/spreadsheetml/2006/main                 |
| sml-baseTypes.xsd                         | ssml                | http://schemas.openxmlformats.org/spreadsheetml/2006/main                 |
| sml-calculationChain.xsd                  | ssml                | http://schemas.openxmlformats.org/spreadsheetml/2006/main                 |
| sml-comments.xsd                          | ssml                | http://schemas.openxmlformats.org/spreadsheetml/2006/main                 |
| sml-customXmlMappings.xsd                 | ssml                | http://schemas.openxmlformats.org/spreadsheetml/2006/main                 |
| sml-externalConnections.xsd               | ssml                | http://schemas.openxmlformats.org/spreadsheetml/2006/main                 |
| sml-pivotTable.xsd                        | ssml                | http://schemas.openxmlformats.org/spreadsheetml/2006/main                 |
| sml-pivotTableShared.xsd                  | ssml                | http://schemas.openxmlformats.org/spreadsheetml/2006/main                 |
| sml-queryTable.xsd                        | ssml                | http://schemas.openxmlformats.org/spreadsheetml/2006/main                 |
| sml-sharedStringTable.xsd                 | ssml                | http://schemas.openxmlformats.org/spreadsheetml/2006/main                 |
| sml-sharedWorkbookRevisions.xsd           | ssml                | http://schemas.openxmlformats.org/spreadsheetml/2006/main                 |
| sml-sharedWorkbookUserNames.xsd           | ssml                | http://schemas.openxmlformats.org/spreadsheetml/2006/main                 |
| sml-sheet.xsd                             | ssml                | http://schemas.openxmlformats.org/spreadsheetml/2006/main                 |
| sml-sheetMetadata.xsd                     | ssml                | http://schemas.openxmlformats.org/spreadsheetml/2006/main                 |
| sml-singleCellTable.xsd                   | ssml                | http://schemas.openxmlformats.org/spreadsheetml/2006/main                 |
| sml-styles.xsd                            | ssml                | http://schemas.openxmlformats.org/spreadsheetml/2006/main                 |
| sml-supplementaryWorkbooks.xsd            | ssml                | http://schemas.openxmlformats.org/spreadsheetml/2006/main                 |
| sml-table.xsd                             | ssml                | http://schemas.openxmlformats.org/spreadsheetml/2006/main                 |
| sml-volatileDependencies.xsd              | ssml                | http://schemas.openxmlformats.org/spreadsheetml/2006/main                 |
| sml-workbook.xsd                          | ssml                | http://schemas.openxmlformats.org/spreadsheetml/2006/main                 |
| vml-main.xsd                              | v                   | urn:schemas-microsoft-com:vml                                             |
| vml-officeDrawing.xsd                     | o                   | urn:schemas-microsoft-com:office:office                                   |
| vml-presentationDrawing.xsd               | ppt                 | urn:schemas-microsoft-com:office:powerpoint                               |
| vml-spreadsheetDrawing.xsd                | x                   | urn:schemas-microsoft-com:office:excel                                    |
| vml-wordprocessingDrawing.xsd             | wvml                | urn:schemas-microsoft-com:office:word                                     |
| wml.xsd                                   | w                   | http://schemas.openxmlformats.org/wordprocessingml/2006/main              |

"""

NameSpace_a = 'http://schemas.openxmlformats.org/drawingml/2006/main'
NameSpace_draw_chart = 'http://schemas.openxmlformats.org/drawingml/2006/chart'
NameSpace_cdr = 'http://schemas.openxmlformats.org/drawingml/2006/chartDrawing'
NameSpace_draw_compat = 'http://schemas.openxmlformats.org/drawingml/2006/compatibility'
NameSpace_draw_diag = 'http://schemas.openxmlformats.org/drawingml/2006/diagram'
NameSpace_draw_lc = 'http://schemas.openxmlformats.org/drawingml/2006/lockedCanvas'
NameSpace_draw_pic = 'http://schemas.openxmlformats.org/drawingml/2006/picture'
NameSpace_draw_ssdraw = 'http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing'
NameSpace_wp = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
NameSpace_p = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NameSpace_characteristics = 'http://schemas.openxmlformats.org/officeDocument/2006/characteristics'
NameSpace_bibliography = 'http://schemas.openxmlformats.org/officeDocument/2006/bibliography'
NameSpace_customXml = 'http://schemas.openxmlformats.org/officeDocument/2006/customXml'
NameSpace_sl = 'http://schemas.openxmlformats.org/schemaLibrary/2006/main'
NameSpace_custom_properties = 'http://schemas.openxmlformats.org/officeDocument/2006/custom-properties'
NameSpace_extended_properties = 'http://schemas.openxmlformats.org/officeDocument/2006/extended-properties'
NameSpace_docPropsVTypes = 'http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes'
NameSpace_m = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
NameSpace_r = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NameSpace_ssml = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
NameSpace_w = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NameSpace_v = 'urn:schemas-microsoft-com:vml'
NameSpace_o = 'urn:schemas-microsoft-com:office:office'
NameSpace_ppt = 'urn:schemas-microsoft-com:office:powerpoint'
NameSpace_x = 'urn:schemas-microsoft-com:office:excel'
NameSpace_wvml = 'urn:schemas-microsoft-com:office:word'
NameSpace_mc = 'http://schemas.openxmlformats.org/markup-compatibility/2006'

NS_MAP = {
    'a': NameSpace_a,
    'draw-chart': NameSpace_draw_chart,
    'cdr': NameSpace_cdr,
    'draw-compat': NameSpace_draw_compat,
    'draw-diag': NameSpace_draw_diag,
    'draw-lc': NameSpace_draw_lc,
    'draw-pic': NameSpace_draw_pic,
    'draw-ssdraw': NameSpace_draw_ssdraw,
    'wp': NameSpace_wp,
    'p': NameSpace_p,
    'characteristics': NameSpace_characteristics,
    'bibliography': NameSpace_bibliography,
    'customXml': NameSpace_customXml,
    'sl': NameSpace_sl,
    'custom-properties': NameSpace_custom_properties,
    'extended-properties': NameSpace_extended_properties,
    'docPropsVTypes': NameSpace_docPropsVTypes,
    'm': NameSpace_m,
    'r': NameSpace_r,
    'ssml': NameSpace_ssml,
    'w': NameSpace_w,
    'v': NameSpace_v,
    'o': NameSpace_o,
    'x': NameSpace_x,
    'ppt': NameSpace_ppt,
    'wvml': NameSpace_wvml,
    # 兼容性
    'mc': NameSpace_mc,
}
