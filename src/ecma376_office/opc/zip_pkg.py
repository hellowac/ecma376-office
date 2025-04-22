"""
为 物理 的 OPC 包 提供通用接口， 这里针对 zip 文件
"""

import logging
from typing import AnyStr, BinaryIO
from zipfile import ZIP_DEFLATED, ZipFile

from ecma376_office.packuri import PackURI

logger = logging.getLogger(__name__)


class PhysPkgReader:
    """
    物理OPC包读取器对象的工厂类。
    """

    def __new__(cls, pkg_file: str):
        return ZipPkgReader(pkg_file)


class PhysPkgWriter:
    """
    物理OPC包写入器对象的工厂类。
    """

    def __new__(cls, pkg_file: str):
        return ZipPkgWriter(pkg_file)


class ZipPkgReader:
    """
    实现 |PhysPkgReader| zip 文件 OPC 包的接口。
    """

    _CONTENT_TYPES_MEMBERNAME = '[Content_Types].xml'

    def __init__(self, pkg_file: str | BinaryIO):
        super().__init__()
        self._zipf = ZipFile(pkg_file, 'r')  # type: ignore
        self._znamelist = self._zipf.namelist()

    def exists(self, pack_uri: PackURI | str):
        """检查文件是否存在"""

        return pack_uri in self._znamelist

    def blob_for(self, pack_uri: PackURI):
        """
        返回对应于 *pack_uri* 的 blob。 引发 |ValueError| 如果 zip 存档中不存在匹配的成员。
        """
        return self._zipf.read(pack_uri.member_name)

    def close(self):
        """
        关闭 zip 存档，释放它正在使用的所有资源。
        """
        self._zipf.close()

    @property
    def content_types_xml(self):
        """
        从 zip 包中返回 `[Content_Types].xml` 字节流
        """
        return self._zipf.read(self._CONTENT_TYPES_MEMBERNAME)

    def rels_xml_for(self, source_uri: PackURI):
        """
        返回带有 *source_uri* 的源的关系(rels)项 XML
        """

        # 某个uri的关系xml部件路径
        member_name = source_uri.rels_uri.member_name

        # logger.info(f"{source_uri = } 的 关系xml 路径为: {member_name}")

        return self._zipf.read(member_name)


class ZipPkgWriter:
    """
    实现 |PhysPkgWriter| zip 文件 OPC 包的接口。
    """

    def __init__(self, pkg_file):
        super().__init__()
        self._zipf = ZipFile(pkg_file, 'w', compression=ZIP_DEFLATED)

    def close(self):
        """
        关闭 zip 存档，刷新所有挂起的物理写入并释放其正在使用的所有资源。
        """
        self._zipf.close()

    def write(self, pack_uri: PackURI, blob: AnyStr):
        """
        将 *blob* 写入此 zip 包，成员名称对应于 *pack_uri*。
        """
        self._zipf.writestr(pack_uri.member_name, blob)
