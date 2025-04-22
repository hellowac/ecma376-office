"""视频部件的封装"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ecma376_office.shared.parts import VideoPart


class Video:
    """视频部件的封装"""

    def __init__(self, part: VideoPart) -> None:
        self.part = part
