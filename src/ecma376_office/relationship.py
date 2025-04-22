from typing import AnyStr, Optional

from ecma376_office.constants import RELATIONSHIP_TYPE_BASE as RT_BASE
from ecma376_office.oxml.xsd_types import XSD_ID, XSD_AnyURI
from ecma376_office.packuri import PackURI
from ecma376_office.part import SpecificPart


class Relationship:
    """
    部件的关系对象
    """

    def __init__(
        self,
        rId: XSD_ID,
        reltype: XSD_AnyURI,
        target: SpecificPart | PackURI,
        baseURI: PackURI,
        external: bool = False,
    ):
        """target 为 AnyURI的实例时，表示时外部资源， 为Part的实例时，表示是包内部资源"""
        self._rId = rId
        self._reltype = reltype
        self._target = target
        self._baseURI = baseURI
        self._is_external = bool(external)

    @property
    def is_external(self):
        return self._is_external

    @property
    def reltype(self):
        return self._reltype

    @property
    def rId(self):
        return self._rId

    @property
    def target(self):
        return self._target

    @property
    def target_part(self):
        # if self._is_external:
        if isinstance(self._target, PackURI):
            # "target_part property on _Relationship is undefined when target mode is External"
            msg = '当目标模式为外部时，_Relationship 上的 target_part 属性未定义'
            raise ValueError(msg)

        return self._target

    @property
    def target_ref(self):
        # if self._is_external:
        if isinstance(self._target, PackURI):  # 为AnyURI的实例即表明是外部
            return self._target
        return self._target.part_name.relative_ref(self._baseURI)


class RelationshipCollection:
    """
    |Relationship| 的集合对象 实例，具有列表语义。
    """

    def __init__(self, baseURI: PackURI, rels_blob: Optional[bytes] = None):
        self._baseURI = baseURI
        self._rels_blob = rels_blob
        self._relationships: list[Relationship] = []
        self._iter_idx = 0

    def __getitem__(self, key: AnyStr) -> Relationship:
        """
        通过下标实现访问，例如 ``rels[9]``。

        它还通过 rId 实现关系的字典式查找，例如 ``rels['rId1']``。
        """
        if isinstance(key, (str, bytes)):
            for rel in self._relationships:
                if rel.rId == key:
                    return rel
            msg = f"RelationshipCollection 中没有 rId 为 '{key!r}' 的关系"
            raise KeyError(msg)
        return self._relationships.__getitem__(key)

    def __len__(self):
        """Implements len() built-in on this object"""
        return self._relationships.__len__()

    def add_relationship(
        self,
        reltype: XSD_AnyURI,
        target: SpecificPart | PackURI,
        rId: XSD_ID,
        external: bool = False,
    ):
        """
        返回新添加的 Relationship 实例。
        """
        rel = Relationship(rId, reltype, target, self._baseURI, external)
        self._relationships.append(rel)
        return rel

    def get_rel_by_type(self, reltype: RT_BASE):
        """
        从集合中返回类型为 *reltype* 的单一关系。 引发 |KeyError| 如果没有找到匹配关系。 引发 |ValueError| 如果找到多个匹配关系。
        """

        matching = [rel for rel in self._relationships if rel.reltype == reltype]

        if len(matching) == 0:
            return None

            # raise KeyError(f"集合中没有类型为: '{reltype}'的关系")

        if len(matching) > 1:
            msg = f"集合中关系类型为: '{reltype}' 的大于1"
            raise ValueError(msg)

        return matching[0]

    def get_rel_by_type_and_id(self, reltype: RT_BASE, rid: str):
        """根据关系类型和ID返某个关系"""

        matching = [rel for rel in self._relationships if rel.reltype == reltype and rel.rId == rid]

        if len(matching) == 0:
            return None

            # raise KeyError(f"集合中没有类型为: '{reltype}'的关系")

        if len(matching) > 1:
            msg = f"集合中关系类型为: '{reltype}' 和 '{rid}' 的大于1"
            raise ValueError(msg)

        return matching[0]

    def get_rels_by_type(self, reltype: RT_BASE):
        """
        从集合中返回类型为 *reltype* 的单一关系。 引发 |KeyError| 如果没有找到匹配关系。 引发 |ValueError| 如果找到多个匹配关系。
        """

        return [rel for rel in self._relationships if rel.reltype == reltype]


    @property
    def xml(self):
        """
        将此关系集合序列化为适合存储为 OPC 包中的 .rels 文件的 XML。
        """

        return self._rels_blob
