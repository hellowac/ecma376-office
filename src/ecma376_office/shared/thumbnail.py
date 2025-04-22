"""针对缩略图部件的封装"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ecma376_office.shared.parts import ThumbnailPart


class Thumbnail:
    """抽象概念的缩略图封装"""

    def __init__(self, part: ThumbnailPart) -> None:
        self.part = part
