"""针对图片部件的封装"""

from __future__ import annotations

import hashlib
from io import BytesIO
from typing import TYPE_CHECKING

from PIL import Image as PIL_Image

if TYPE_CHECKING:
    from ecma376_office.shared.parts import ImagePart


class Image:
    """Immutable value object representing an image such as a JPEG, PNG, or GIF.

    表示图像(例如 JPEG、PNG 或 GIF)的不可变值对象。
    """

    def __init__(self, part: ImagePart):
        super().__init__()
        self.part = part

    @property
    def blob(self) -> bytes:
        """
        The binary image bytestream of this image.

        该图像的二进制图像字节流。
        """
        return self.part.blob

    @property
    def content_type(self):
        """
        该图像的 MIME 类型，例如 ``'图像/jpeg'``。
        """
        return self.part.content_type

    @property
    def dpi(self):
        """

        一个 (horz_dpi, vert_dpi) 2 元组，指定该图像的每英寸点数分辨率。
        如果图像文件中未指定 dpi，则使用默认值 (72, 72)。
        """

        def int_dpi(dpi):
            """
            返回对应于 *dpi* 的整数每英寸点数值。 如果 *dpi* 为 |None|（非数字类型），小于 1 或大于 2048, 则返回 72。
            """
            try:
                int_dpi = int(round(float(dpi)))
                if int_dpi < 1 or int_dpi > 2048:
                    int_dpi = 72
            except (TypeError, ValueError):
                int_dpi = 72
            return int_dpi

        def normalize_pil_dpi(pil_dpi):
            """
            返回对应于 *pil_dpi* 的 (horz_dpi, vert_dpi) 2 元组，
            即 PIL 图像的 ``info`` 字典中 'dpi' 键的值。
            如果“dpi”键不存在或包含无效值, 则返回“(72, 72)”。
            """
            if isinstance(pil_dpi, tuple):
                return (int_dpi(pil_dpi[0]), int_dpi(pil_dpi[1]))
            return (72, 72)

        return normalize_pil_dpi(self._pil_props[2])

    @property
    def ext(self):
        """
        该图像的规范文件扩展名，例如 ``'png'``。

        返回的扩展名全部为小写，并且是该图像内容类型的规范扩展名，无论其文件名中使用了什么扩展名（如果有）。
        """
        ext_map = {
            'BMP': 'bmp',
            'GIF': 'gif',
            'JPEG': 'jpg',
            'PNG': 'png',
            'TIFF': 'tiff',
            'WMF': 'wmf',
        }
        format = self._format
        # logger.info(f"{format =}")
        if format not in ext_map:
            tmpl = "unsupported image format, expected one of: %s, got '%s'"
            raise ValueError(tmpl % (ext_map.keys(), format))
        return ext_map[format]

    @property
    def filename(self) -> str:
        """
        如果从文件系统加载，则加载此图像的路径中的文件名。 |None| 如果加载时没有使用文件名，例如从内存流加载时。
        """
        return self.part.filename

    @property
    def sha1(self):
        """
        图像 blob 的 SHA1 哈希摘要
        """
        return hashlib.sha1(self.part.blob).hexdigest()

    @property
    def size(self):
        """
        一个（宽度，高度）二元组，指定该图像的尺寸（以像素为单位）。
        """
        return self._pil_props[1]

    @property
    def _format(self):
        """
        该图像的 PIL 图像格式，例如 “PNG”。
        """
        return self._pil_props[0]

    @property
    def _pil_props(self):
        """
        包含使用 Pillow(Python 成像库,或“PIL”)从此图像中提取的有用图像属性的元组。
        """
        stream = BytesIO(self.part.blob)
        pil_image = PIL_Image.open(stream)
        format = pil_image.format
        width_px, height_px = pil_image.size
        dpi = pil_image.info.get('dpi')
        # pil_image.save("asdfasdf11111111111.png", format="png")
        stream.close()
        return (format, (width_px, height_px), dpi)
