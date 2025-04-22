from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple, Optional

if TYPE_CHECKING:
    from ecma376_office.oxml.pml.core import CT_Placeholder, ST_Direction, ST_PlaceholderSize, ST_PlaceholderType


class PlaceHolderInfo(NamedTuple):
    """占位符形状

    19.3.1.36 ph (占位符形状)

    参考: https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter19/slides/#193136-ph-占位符形状
    """

    has_custom_prompt: bool
    """占位符是否有自定义提示

    指定相应的占位符是否应该有自定义提示.
    """

    index: int
    """占位符索引

    指定占位符索引。 在应用模板或更改布局以将一个模板/母版上的占位符与另一个模板/母版上的占位符匹配时使用此选项.
    """

    orient: ST_Direction
    """占位符方向

    指定占位符的方向.
    """

    size: ST_PlaceholderSize
    """占位符大小

    指定占位符的大小.
    """

    type: ST_PlaceholderType
    """占位符类型

    指定占位符要包含的内容类型.

    可能的值包括

    - body（包含正文文本，允许在幻灯片、布局、幻灯片母板模板、备注和备注母板模板中使用；可以是水平或垂直的）
    - chart（包含图表或图形，允许在幻灯片和布局中使用）
    - clipArt（包含单个剪贴画图像，允许在幻灯片和布局中使用）
    - ctrTitle（包含一个标题，应居中显示在幻灯片上，允许在幻灯片和布局中使用）
    - dgm（包含图表，允许在幻灯片和布局中使用）
    - dt（包含日期和时间，允许在幻灯片、布局、幻灯片母板模板、备注、备注母板模板和讲义母板模板中使用）
    - ftr（包含用作页脚的文本，允许在幻灯片、布局、幻灯片母板模板、备注、备注母板模板和讲义母板模板中使用）
    - hdr（包含用作页眉的文本，允许在备注、备注母板模板和讲义母板模板中使用）
    - media（包含多媒体内容，如音频或电影，允许在幻灯片和布局中使用）
    - obj（包含任何内容类型，允许在幻灯片和布局中使用）
    - pic（包含图片，允许在幻灯片和布局中使用）
    - sldImg（包含幻灯片的图像，允许在备注和备注母板模板中使用）
    - sldNum（包含幻灯片的编号，允许在幻灯片、布局、幻灯片母板模板、备注、备注母板模板和讲义母板模板中使用）
    - subTitle（包含副标题，允许在幻灯片和布局中使用）
    - tbl（包含表格，允许在幻灯片和布局中使用）
    - title（包含幻灯片标题，允许在幻灯片、布局和幻灯片母板模板中使用；可以是水平或垂直的）
    """


def to_placeholder_info(oxml: Optional[CT_Placeholder]) -> Optional[PlaceHolderInfo]:
    """返回占位符信息"""

    if oxml is None:
        return None

    return PlaceHolderInfo(oxml.has_custom_prompt, oxml.idx, oxml.orient, oxml.size, oxml.type)
