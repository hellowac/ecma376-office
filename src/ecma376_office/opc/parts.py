import hashlib
import logging
from typing import TYPE_CHECKING

from ecma376_office.part import Part

if TYPE_CHECKING:
    from ecma376_office.oxml.opc.core_properties import CT_CoreProperties

logger = logging.getLogger(__name__)


class ImagePart(Part):
    """
    图像部件。

    图像部分通常具有与正则表达式“ppt/media/image[1-9][0-9]*.*”匹配的部分名称。
    """

    @property
    def desc(self):
        """
        使用路径创建的图像将具有该文件名； 使用类似文件的对象创建的对象将具有通用名称。
        """
        # 如果原始文件名未知，则返回通用文件名
        if self.part_name.filename is None:
            return f'image.{self.ext}'
        return self.part_name.filename

    @property
    def ext(self):
        """
        返回该图像的文件扩展名，例如 ``'png'``。
        """
        return self.part_name.ext

    @property
    def image(self):
        """包含此图像部件中的图像的对象。"""

        # 防止循环引用
        from ecma376_office.shared.image import Image

        return Image(self)

    @property
    def sha1(self):
        """
        该图像部件的图像二进制的 SHA1 哈希摘要，例如：

        ``'1be010ea47803b00e140b852765cdf84f491da47'``.
        """
        return hashlib.sha1(self._blob).hexdigest()

    @property
    def px_size(self):
        """
        一个（宽度，高度）二元组，表示该图像的尺寸（以像素为单位）。
        """

        # 防止循环引用
        from ecma376_office.shared.image import Image

        return Image(self).size


class CorePropertiesPart(Part):
    """核心属性部件"""

    @property
    def oxml(self):

        oxml: CT_CoreProperties = super().oxml

        return oxml
