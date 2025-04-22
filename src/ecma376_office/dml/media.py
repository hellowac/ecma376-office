"""媒体对象封装类"""

from __future__ import annotations

import hashlib
import logging
from io import BytesIO
from typing import TYPE_CHECKING, Any, Optional

from mutagen.mp3 import MP3, MPEGInfo

from ecma376_office.oxml.dml.main import (
    CT_AudioCD,
    CT_AudioFile,
    CT_EmbeddedWAVAudioFile,
    CT_QuickTimeFile,
    CT_VideoFile,
)
from ecma376_office.utils import SharedPartFinder

if TYPE_CHECKING:
    from ecma376_office.pml.shapes import PictureShape
    from ecma376_office.pml.slide import Slide
    from ecma376_office.pml.slide_layout import SlideLayout
    from ecma376_office.pml.slide_master import SlideMaster

MediaTypes = Optional[
    CT_AudioCD | CT_EmbeddedWAVAudioFile | CT_AudioFile | CT_VideoFile | CT_QuickTimeFile
]

logger = logging.getLogger(__name__)


class MediaBase:
    """媒体基类"""

    def __init__(self, slide: Any, shape: Any) -> None:

        self.slide: Slide | SlideLayout | SlideMaster = slide
        self.shape: PictureShape = shape


class AudioCD(MediaBase):
    """CD 中的音频

    20.1.3.1

    Audio from CD

    该元素指定 CD 中是否存在音频。 该元素在对象的非视觉属性中指定。 音频应附加到对象，因为这是它在文档中的表示方式。 然而，声音的实际播放是在计时元素下指定的计时节点列表内完成的。
    """

    def __init__(self, slide: Any, shape: Any, oxml: CT_AudioCD) -> None:
        super().__init__(slide, shape)
        self.oxml = oxml

    # 暂未完全实现API


class EmbeddedWAVAudioFile(MediaBase):
    """嵌入的 WAV 音频文件

    19.5.68
    """

    def __init__(self, slide: Any, shape: Any, oxml: CT_EmbeddedWAVAudioFile) -> None:
        super().__init__(slide, shape)
        self.oxml = oxml

    # 暂未完全实现API


class AudioFile(MediaBase):
    """文件中的音频

    20.1.3.2

    Audio from File
    """

    def __init__(self, slide: Any, shape: Any, oxml: CT_AudioFile) -> None:
        super().__init__(slide, shape)
        self.oxml = oxml
        self._part = SharedPartFinder.audio_one(self.slide.part.rels, self.oxml.r_link)

    @property
    def content_type(self):
        """文件内容类型"""

        if self._part is None:
            return None

        return self.oxml.content_type

    @property
    def blob(self):
        if self._part is None:
            return b''

        if isinstance(self._part, str):
            return b''

        return self._part.blob

    @property
    def sha1(self):
        """返回此视频文件的哈希值"""

        if self._part is None:
            return None

        return hashlib.sha1(self.blob).hexdigest()

    @property
    def filename(self):
        if self._part is None:
            return None

        if isinstance(self._part, str):
            return self._part

        return self._part.filename

    @property
    def size(self):
        if not self.blob:
            return '0MB'

        return f'{len(self.blob) / (1024 * 1024)}MB'


    @property
    def ext(self):
        """扩展名"""
        if self.filename is None:
            return None

        # xxx.mp4 -> mp4
        return self.filename.rsplit('.', 1)[1]

    @property
    def mpeg_info(self) -> Optional[MPEGInfo]:
        """mpeg信息"""

        if len(self.blob) > 0:
            stream = BytesIO(self.blob)
            stream.seek(0)

            return MP3(stream).info  # type: ignore

        return None


class VideoFile(MediaBase):
    """文件中的视频

    20.1.3.6

    Video from File
    """

    def __init__(self, slide: Any, shape: Any, oxml: CT_VideoFile) -> None:
        super().__init__(slide, shape)
        self.oxml = oxml
        self._part = SharedPartFinder.video_one(self.slide.part.rels, self.oxml.r_link)

    @property
    def is_external(self):
        """是否为外部文件"""

        if self._part is None:
            return True

        if isinstance(self._part, str):
            return True

        return self._part._is_external

    @property
    def content_type(self):
        """文件内容类型"""

        if self._part is None:
            return None

        return self.oxml.content_type

    @property
    def blob(self):
        if self._part is None:
            return b''

        if isinstance(self._part, str):
            return b''

        return self._part.blob

    @property
    def sha1(self):
        """返回此视频文件的哈希值"""

        if self._part is None:
            return None

        return hashlib.sha1(self.blob).hexdigest()

    @property
    def filename(self):
        if self._part is None:
            return None

        if isinstance(self._part, str):
            return self._part

        return self._part.filename

    @property
    def size(self):
        if not self.blob:
            return '0MB'

        return f'{len(self.blob) / (1024 * 1024)}MB'


    @property
    def ext(self):
        """扩展名"""
        if self.filename is None:
            return None

        # xxx.mp4 -> mp4
        return self.filename.rsplit('.', 1)[1]


class QuickTimeFile(MediaBase):
    """来自文件的 QuickTime

    20.1.3.4

    QuickTime from File
    """

    def __init__(self, slide: Any, shape: Any, oxml: CT_QuickTimeFile) -> None:
        super().__init__(slide, shape)
        self.oxml = oxml

    # 暂未完全实现API


def media_factory(slide: Any, shape: Any, oxml: MediaTypes):
    """媒体对象工厂函数"""

    if oxml is None:
        return None

    if isinstance(oxml, CT_AudioCD):
        return AudioCD(slide, shape, oxml)

    if isinstance(oxml, CT_EmbeddedWAVAudioFile):
        return EmbeddedWAVAudioFile(slide, shape, oxml)

    if isinstance(oxml, CT_AudioFile):
        return AudioFile(slide, shape, oxml)

    if isinstance(oxml, CT_VideoFile):
        return VideoFile(slide, shape, oxml)

    if isinstance(oxml, CT_QuickTimeFile):
        return QuickTimeFile(slide, shape, oxml)
    return None
