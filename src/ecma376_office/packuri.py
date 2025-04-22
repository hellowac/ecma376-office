"""
提供 PackURI 值类型以及一些有用的已知值，例如 PACKAGE_URI。
"""

import logging
import posixpath
from typing import AnyStr

logger = logging.getLogger(__name__)


class PackURI(str):
    """
    提供对 Pack URI 组件（例如 baseURI 和文件名切片）的访问。 否则行为如 |str| 。
    """

    def __new__(cls, pack_uri_str: str):
        if pack_uri_str[0] != '/':
            tmpl = "PackURI 必须以斜杠(/)开头，得到 '%s'"
            raise ValueError(tmpl % pack_uri_str)

        return str.__new__(cls, pack_uri_str)

    def __str__(self) -> str:
        return super().__str__()

    def __hash__(self) -> int:
        return super().__hash__()

    @staticmethod
    def from_rel_ref(baseURI: AnyStr, relative_ref: AnyStr):
        """
        返回 |PackURI| 包含通过将 *relative_ref* 转换为 *baseURI* 形成的绝对包 URI 的实例。
        """

        joined_uri = posixpath.join(baseURI, relative_ref)  # type: ignore
        abs_uri = posixpath.abspath(joined_uri)

        # logger.info(f"{baseURI = } {relative_ref =} => {abs_uri =}")
        return PackURI(str(abs_uri))

    @property
    def baseURI(self):
        """
        该包 URI 的基本 URI，粗略地说，是目录部分。

        例如。 '/ppt/slides/slide1.xml' 的 baseURI 为 '/ppt/slides'。

        对于包伪部件名称“/”，baseURI 为“/”。
        """
        return posixpath.split(self)[0]

    @property
    def ext(self):
        """
        此包 URI 的扩展名，

        例如 '.xml' 代表 '/ppt/slides/slide1.xml'。

        请注意，包含句点，与 posixpath.ext 的行为一致。
        """
        return posixpath.splitext(self)[1]

    @property
    def filename(self):
        """
        此包 URI 的 “文件名” 部分，

        例如 '/ppt/slides/slide1.xml' 的文件名为 'slide1.xml'

        对于包伪部分名称“/”，文件名是 “” 。
        """
        return posixpath.split(self)[1]

    @property
    def member_name(self):
        """
        去掉前导斜杠的包 URI，该形式用作包项的 Zip 文件成员名。

        对于包伪部分名称“/”，返回“” 。

        """
        return self[1:]

    def relative_ref(self, baseURI: str):
        """
        返回包含来自 *baseURI* 的包项的相对引用路径。

        例如。 PackURI('/ppt/slideLayouts/slideLayout1.xml')

        将为 baseURI '/ppt/slides' 返回 '../slideLayouts/slideLayout1.xml'。

        """
        # python 2.6 中 posixpath 错误的解决方法，当 *start* （第二个）参数为根（'/'）时，不会生成正确的相对路径
        return self[1:] if baseURI == '/' else posixpath.relpath(self, baseURI)


    @property
    def rels_uri(self):
        """
        与当前 pack URI 对应的 .rels 部件的 pack URI。

        仅当包 URI 是部件名称或包伪部件名称“/”时，才会生成合理的输出。
        """
        rels_filename = f'{self.filename}.rels'
        rels_uri_str = posixpath.join(self.baseURI, '_rels', rels_filename)
        return PackURI(rels_uri_str)


PACKAGE_URI = PackURI('/')
CONTENT_TYPES_URI = PackURI('/[Content_Types].xml')
