"""
对应xsd: dml-picture.xsd

前缀: pic

命名空间: http://purl.oclc.org/ooxml/drawingml/picture

<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"
  xmlns="http://purl.oclc.org/ooxml/drawingml/picture"
  xmlns:a="http://purl.oclc.org/ooxml/drawingml/main" elementFormDefault="qualified"
  targetNamespace="http://purl.oclc.org/ooxml/drawingml/picture">
  <xsd:import namespace="http://purl.oclc.org/ooxml/drawingml/main" schemaLocation="dml-main.xsd"/>

  ...

</xsd:schema>
"""

from __future__ import annotations

import logging
from typing import TypeVar

from ecma376_office.oxml.base import OxmlBaseElement, lookup
from ecma376_office.oxml.dml.main import CT_BlipFillProperties as a_CT_BlipFillProperties
from ecma376_office.oxml.dml.main import CT_NonVisualDrawingProps as a_CT_NonVisualDrawingProps
from ecma376_office.oxml.dml.main import CT_NonVisualPictureProperties as a_CT_NonVisualPictureProperties
from ecma376_office.oxml.dml.main import CT_ShapeProperties as a_CT_ShapeProperties

# namespace_pic = "http://purl.oclc.org/ooxml/drawingml/picture"
namespace_pic = 'http://schemas.openxmlformats.org/drawingml/2006/picture'

# namespace_a = "http://purl.oclc.org/ooxml/drawingml/main"
namespace_a = 'http://schemas.openxmlformats.org/drawingml/2006/main'

logger = logging.getLogger(__name__)

ns_map = {
    'pic': namespace_pic,  # 当前命名空间
    'a': namespace_a,
}


def qn(tag: str):
    """将 dc:creator 这种的标签,转换为 {http://purl.org/dc/elements/1.1/}creator 这样的形式"""

    global ns_map

    if ':' not in tag:
        return tag

    ns_prefix, ns = tag.split(':')

    return f'{{{ns_map[ns_prefix]}}}{ns}'


SubBaseElement = TypeVar('SubBaseElement', bound=OxmlBaseElement)


class CT_PictureNonVisual(OxmlBaseElement):
    """20.2.2.4 nvPicPr (非视觉图片属性)

    该元素指定图片的非视觉属性。 这允许存储不影响图片外观的附加信息。

    考虑以下 DrawingML。

    <pic:pic>
        …
        <pic:nvPicPr>
        …
        </pic:nvPicPr>
        …
    </pic:pic>

    [Note: 该元素内容模型 (CT_PictureNonVisual) 的 W3C XML 架构定义位于 §A.4.2 中。 end note]
    """

    @property
    def c_nv_pr(self) -> a_CT_NonVisualDrawingProps:
        """20.2.2.3 cNvPr (非可视绘图属性)

        该元素指定非可视画布属性。 这允许存储不影响图片外观的附加信息。

        考虑以下 DrawingML。

        <pic:pic>
            …
            <pic:nvPicPr>
                <p:cNvPr id="4" name="Lilly.jpg"/>
            </pic:nvPicPr>
            …
        </pic:pic>
        """
        return getattr(self, qn('pic:cNvPr'))

    @property
    def c_nv_pic_pr(self) -> a_CT_NonVisualPictureProperties:
        """20.2.2.2 cNvPicPr (非视觉绘图属性)

        该元素指定图片画布的非视觉属性。 生成应用程序将使用这些属性来确定如何更改所讨论的图片对象的某些属性。

        考虑以下 DrawingML。

        <pic:pic>
            …
            <pic:nvPicPr>
                <pic:cNvPr id="4" name="Lilly.jpg"/>
                <pic:cNvPicPr>
                    <a:picLocks noChangeAspect="1"/>
                </p:cNvPicPr>
                <pic:nvPr/>
            </pic:nvPicPr>
            …
        </pic:pic>
        """
        return getattr(self, qn('pic:cNvPicPr'))


class CT_Picture(OxmlBaseElement):
    """20.2.2.5 pic (图片)

    该元素指定文档中是否存在图片对象。

    考虑以下 DrawingML，它指定文档中是否存在图片。 该图片可以具有非视觉属性、图片填充以及附加的形状属性。

    <pic:pic>
        <pic:nvPicPr>
            <pic:cNvPr id="4" name="lake.JPG" descr="Picture of a Lake" />
            <pic:cNvPicPr>
                <a:picLocks noChangeAspect="1"/>
            </pic:cNvPicPr>
            <pic:nvPr/>
        </pic:nvPicPr>
        <pic:blipFill>
        …
        </pic:blipFill>
        <pic:spPr>
        …
        </pic:spPr>
    </pic:pic>

    [Note: 该元素内容模型 (CT_Picture) 的 W3C XML 模式定义位于 §A.4.2 中。 end note]
    """

    @property
    def nv_pic_pr(self) -> CT_PictureNonVisual:
        """20.2.2.4 nvPicPr (非视觉图片属性)

        该元素指定图片的非视觉属性。 这允许存储不影响图片外观的附加信息。

        考虑以下 DrawingML。

        <pic:pic>
            …
            <pic:nvPicPr>
            …
            </pic:nvPicPr>
            …
        </pic:pic>

        [Note: 该元素内容模型 (CT_PictureNonVisual) 的 W3C XML 架构定义位于 §A.4.2 中。 end note]
        """
        return getattr(self, qn('pic:nvPicPr'))

    @property
    def blip_fill(self) -> a_CT_BlipFillProperties:
        """20.2.2.1 blipFill (图片填充)

        该元素指定图片对象具有的图片填充类型。 由于默认情况下图片已具有图片填充，因此可以为图片对象指定两种填充。 下面显示了一个示例。

        考虑下面应用了斑点填充的图片。 用于填充该图片对象的图像具有透明像素而不是白色像素。

        <pic:pic>
            …
            <pic:blipFill>
                <a:blip r:embed="rId2"/>
                    <a:stretch>
                        <a:fillRect/>
                    </a:stretch>
            </pic:blipFill>
            …
        </pic:pic>

        上面的图片对象显示为这种填充类型的示例。
        """
        return getattr(self, qn('pic:blipFill'))

    @property
    def sp_pr(self) -> a_CT_ShapeProperties:
        """20.2.2.6 spPr (形状属性)

        spPr (Shape Properties)

        该元素指定可应用于图片的视觉形状属性。 这些属性与允许描述形状的视觉属性相同，但在这里用于描述文档中图片的视觉外观。 这允许图片同时具有形状的属性以及 pic 元素下允许的图片特定属性。
        """
        return getattr(self, qn('pic:spPr'))


dml_picture_namespace = lookup.get_namespace(namespace_pic)
dml_picture_namespace[None] = OxmlBaseElement


dml_picture_namespace['pic'] = CT_Picture  # 根节点之一
# dml_main_namespace["userShapes"] = cdr_CT_Drawing  # 根节点之一


dml_picture_namespace['cNvPr'] = a_CT_NonVisualDrawingProps
dml_picture_namespace['cNvPicPr'] = a_CT_NonVisualPictureProperties
dml_picture_namespace['nvPicPr'] = CT_PictureNonVisual
dml_picture_namespace['blipFill'] = a_CT_BlipFillProperties
dml_picture_namespace['spPr'] = a_CT_ShapeProperties

# 公共元素:
