from __future__ import annotations

import logging
from typing import (
    TYPE_CHECKING,
    Optional,
    Self,
    TypeAlias,
    TypeVar,
)

from ecma376_office.descriptor import lazyproperty

if TYPE_CHECKING:
    from ecma376_office.oxml.xsd_types import XSD_ID, XSD_AnyURI
    from ecma376_office.packuri import PackURI

# 泛型
T = TypeVar('T')

AnyURI = str
AnyContentType: TypeAlias = str

logger = logging.getLogger(__name__)


class Part:
    """
    封装部件的基类。 提供通用属性和方法，但旨在在客户端代码中进行子类化以实现特定的部件行为。
    """

    def __init__(
        self,
        part_name: PackURI,
        content_type: AnyContentType,
        blob: bytes = b'',
        rels_blob: Optional[bytes] = None,
        is_external: bool = False,
    ):
        from ecma376_office.relationship import RelationshipCollection

        self._part_name = part_name
        self._content_type = content_type
        self._blob = blob
        self._relationship_collect = RelationshipCollection(part_name.baseURI, rels_blob)
        self._rels_blob = rels_blob
        self._is_external = is_external

    @classmethod
    def load(
        cls,
        part_name: PackURI,
        content_type: AnyContentType,
        blob: bytes = b'',
        rels_blob: Optional[bytes] = None,
        is_external: bool = False,
    ) -> Self:
        return cls(part_name, content_type, blob, rels_blob, is_external)

    @property
    def blob(self):
        """
        该包部件的内容作为字节序列。 可以是文本或二进制。
        """
        return self._blob

    @property
    def content_type(self):
        """
        该部件的内容类型。
        """
        return self._content_type

    @property
    def part_name(self):
        """
        包含该部件名称的 PackURI 实例。
        """
        return self._part_name

    @property
    def filename(self):
        """
        包含该部件名称的 PackURI 实例。
        """
        # logger.info(f"{self._part_name =}")
        return self._part_name.filename

    @lazyproperty
    def oxml(self):
        """返回对象化的xml对象，并且带类型注解"""

        from ecma376_office.oxml.base import oxml_fromstring

        return oxml_fromstring(self._blob)

    @property
    def rels(self):
        """
        包含该部件所有关系(Relationships) 的 RelationshipCollection 实例。
        """
        return self._relationship_collect

    def _add_relationship(
        self,
        reltype: XSD_AnyURI,
        target: Part | PackURI,
        rId: XSD_ID,
        external: bool = False,
    ):
        """
        返回新添加的 Relationship 实例， 该实例基于 关系类型(reltype), 以及 target 和 rId 参数

        如果 external 为 True， 即包外的关系， 目标模式(Target model) 将被设置为 ST_TargetMode.EXTERNAL
        """

        return self._relationship_collect.add_relationship(reltype, target, rId, external)

    def _after_unmarshal(self):
        """
        解组后处理的入口点，例如解析部件XML。 可能会被子类覆盖而不将调用转发给父类。
        """
        # 不要在这里放置任何代码，如果没有被子类覆盖，只需捕获调用

    def _before_marshal(self):
        """
        预序列化处理的入口点，例如在必要时完成部件命名。 可能会被子类覆盖而不将调用转发给超级类。
        """
        # 不要在这里放置任何代码，如果没有被子类覆盖，只需捕获调用


# 实现特定部件的具体部件
SpecificPart = TypeVar('SpecificPart', bound=Part, covariant=True)


PART_TYPE_MAP: dict[AnyURI, type[Part]] = {}


def PartFactory(
    partname: PackURI,
    content_type: AnyContentType,
    blob: bytes,
    rels_blob: Optional[bytes],
    is_external: bool,
):
    """
    为客户端代码提供一种指定 |Part| 子类的方法 由 |Unmarshaller| 构建, 基于其内容类型。
    """

    if content_type in PART_TYPE_MAP:
        CustomPartClass = PART_TYPE_MAP[content_type]

        # logger.info(f"部件名称: {partname} 内容类型: {content_type} => {CustomPartClass}")
        return CustomPartClass.load(partname, content_type, blob, rels_blob, is_external)

    # logger.info(f"部件名称: {partname} 内容类型: {content_type} => {Part}")

    return Part(partname, content_type, blob, rels_blob, is_external)
