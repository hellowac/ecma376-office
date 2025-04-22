"""
对应xsd: opc-coreProperties.xsd

命名空间: http://schemas.openxmlformats.org/package/2006/metadata/core-properties
"""

import logging
from typing import Optional

from ecma376_office.oxml.base import OxmlBaseElement, lookup
from ecma376_office.oxml.utils import AnyStrToStr
from ecma376_office.oxml.xsd_types import XSD_DateTime, to_xsd_datetime

namespace_cp = 'http://schemas.openxmlformats.org/package/2006/metadata/core-properties'
namespace_dc = 'http://purl.org/dc/elements/1.1/'
namespace_dcterms = 'http://purl.org/dc/terms/'

logger = logging.getLogger(__name__)

ns_map = {
    'cp': namespace_cp,  # 当前命名空间
    'dc': namespace_dc,
    'dcterms': namespace_dcterms,
}


def qn(tag: str):
    """将 dc:creator 这种的标签,转换为 {http://purl.org/dc/elements/1.1/}creator 这样的形式"""

    global ns_map

    if ':' not in tag:
        return tag

    ns_prefix, ns = tag.split(':')

    return f'{{{ns_map[ns_prefix]}}}{ns}'


class CT_Keyword(OxmlBaseElement):
    """
    ``<coreProperties>`` 元素, OPC包的核心属性的 CT_Keyword 类型

    参考: https://hellowac.github.io/ecma-376-zh-cn/ecma-part2-refrence/#8344-本文档中定义的核心属性元素
    """

    @property
    def lang(self) -> Optional[str]:
        """语言


        <xs:attribute ref="xml:lang" use="optional"/>
        """

        val = self.attrib.get('lang')

        if val is not None:
            return AnyStrToStr(val)

        return None


class CT_Keywords(OxmlBaseElement):
    """关键字集

    参考: https://hellowac.github.io/ecma-376-zh-cn/ecma-part2-refrence/#8344-本文档中定义的核心属性元素
    """

    @property
    def keyword_lst(self) -> list[CT_Keyword]:
        """
        ``<CT_Keywords>`` 元素, value 子元素序列

        <xs:element name="value" minOccurs="0" maxOccurs="unbounded" type="CT_Keyword"/>
        """

        return self.findall(qn('cp:value'))


class CT_CoreProperties(OxmlBaseElement):
    """OPC包的核心属性

    参考: https://hellowac.github.io/ecma-376-zh-cn/ecma-part2-refrence/#8344-本文档中定义的核心属性元素
    """

    @property
    def category(self) -> Optional[str]:
        """包内容的分类。"""

        element = self.find(qn('cp:category'))

        if element is not None:
            return element.text

        return None

    @property
    def content_status(self) -> Optional[str]:
        """包内容的状态。"""

        element = self.find(qn('cp:contentStatus'))

        if element is not None:
            return element.text

        return None

    @property
    def created(self) -> Optional[XSD_DateTime]:
        """资源的创建日期"""

        element = self.find(qn('cp:created'))

        if element is not None:
            return to_xsd_datetime(element.text)

        return None

    @property
    def creator(self) -> Optional[str]:
        """主要负责制作资源内容的实体。"""

        element = self.find(qn('dc:creator'))

        if element is not None:
            return element.text

        return None

    @property
    def description(self) -> Optional[str]:
        """对资源内容的解释。"""

        element = self.find(qn('dc:description'))

        if element is not None:
            return element.text

        return None

    @property
    def identifier(self):
        """在给定上下文中对资源的明确引用。"""

        element = self.find(qn('dc:identifier'))

        if element is not None:
            return element.text

        return None

    @property
    def keywords(self) -> Optional[CT_Keywords]:
        """用于支持搜索和索引的一组分隔关键字。

        这通常是属性中其他地方不可用的术语列表。
        """

        return self.find(qn('cp:keywords'))


    @property
    def language(self) -> Optional[str]:
        """资源知识内容的语言。

        请注意，IETF RFC 3066 提供了有关编码来表示语言的指南。
        """

        element = self.find(qn('dc:language'))

        if element is not None:
            return element.text

        return None

    @property
    def last_modified_by(self) -> Optional[str]:
        """执行最后一次修改的用户。 识别是特定于环境的。"""

        element = self.find(qn('cp:lastModifiedBy'))

        if element is not None:
            return element.text

        return None

    @property
    def last_printed(self) -> Optional[XSD_DateTime]:
        """上次打印的日期和时间。"""

        element = self.find(qn('cp:lastPrinted'))

        if element is not None:
            return to_xsd_datetime(element.text)

        return None

    @property
    def modified(self) -> Optional[str]:
        """更改资源的日期。"""

        element = self.find(qn('dcterms:modified'))

        if element is not None:
            return element.text

        return None

    @property
    def revision(self) -> Optional[str]:
        """修订号。"""

        element = self.find(qn('cp:revision'))

        if element is not None:
            return element.text

        return None

    @property
    def subject(self) -> Optional[str]:
        """资源内容的主题。"""

        element = self.find(qn('dc:subject'))

        if element is not None:
            return element.text

        return None

    @property
    def title(self) -> Optional[str]:
        """为资源指定的名称。"""

        element = self.find(qn('dc:title'))

        if element is not None:
            return element.text

        return None

    @property
    def version(self):
        """修订号。"""

        element = self.find(qn('cp:version'))

        if element is not None:
            return element.text

        return None


core_properties_namespace = lookup.get_namespace(namespace_cp)
core_properties_namespace[None] = OxmlBaseElement
core_properties_namespace['coreProperties'] = CT_CoreProperties
core_properties_namespace['keywords'] = CT_Keywords
core_properties_namespace['value'] = CT_Keyword
# content_type_namespace["Types"] = CT_Types

logger.info('初始化核心属性类成功')
