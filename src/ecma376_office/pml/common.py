import logging
from enum import Enum
from typing import Union

from ecma376_office.pml.slide import Slide
from ecma376_office.pml.slide_layout import SlideLayout
from ecma376_office.pml.slide_master import SlideMaster

logger = logging.getLogger(__name__)

SlideTypes = Union[Slide, SlideLayout, SlideMaster]

# --------------- 主题处理相关工具类 ---------------


class BackGroundFrom(Enum):
    """背景来自于"""

    Null = None
    Slide = 'slide'
    SlideLayout = 'slideLayout'
    SlideMaster = 'slideMaster'


class SlideTool:
    """幻灯片工具"""

    @classmethod
    def choice_background(cls, slide: Slide):
        """选择一个背景"""

        logger.debug('获取slide背景')
        background = slide.background
        background_from: BackGroundFrom = BackGroundFrom.Slide

        if background is None and slide.layout is not None:
            logger.debug('尝试获取 slide layout背景')
            background = slide.layout.background
            background_from = BackGroundFrom.SlideLayout

        if background is None and slide.master is not None:
            logger.debug('尝试获取master背景')
            background = slide.master.background
            background_from = BackGroundFrom.SlideMaster

        logger.debug(f'获取到背景, 来自: {background_from.value}')

        return background, background_from


class ThemeTool:
    """主题工具类"""

    @classmethod
    def choice_theme(cls, slide: SlideTypes):
        """选择合适的 theme

        theme 分别有两个地方引用: slide master, presentation

        优先 取 slide master 中 的 theme_override
        """
        # 取 theme
        theme = None

        if isinstance(slide, (Slide, SlideLayout)):
            theme = cls._choice_theme_from_master(slide.master)

        elif isinstance(slide, SlideMaster):
            theme = cls._choice_theme_from_master(slide)

        if theme is None:
            # 应该永远都不会抛这个错, 一个演示文稿应该至少有一个主题
            msg = f'获取主题失败: {theme = }'
            raise ValueError(msg)

        return theme

    @classmethod
    def _choice_theme_from_master(cls, slide: SlideMaster):
        # 取 theme
        theme = slide.theme

        if theme is None:
            theme = slide.presentation.theme

        return theme

    @classmethod
    def choice_theme_override(cls, slide: SlideTypes):
        """选择合适的 theme_override

        theme_override 也分别有两个地方引用: slide layout, slide master

        优先 取 slide layout 中 的 theme_override

        如果 theme_override 为 None 则说明 使用主题定义的样式，不需要覆盖
        """

        if isinstance(slide, Slide):
            return cls._choice_theme_override_from_layout(slide.layout)

        if isinstance(slide, SlideLayout):
            return cls._choice_theme_override_from_layout(slide)

        if isinstance(slide, SlideMaster):
            return cls._choice_theme_override_from_master(slide)
        return None

    @classmethod
    def _choice_theme_override_from_layout(cls, slide: SlideLayout):
        over = slide.theme_override

        if over is None:
            over = cls._choice_theme_override_from_master(slide.master)

        return over

    @classmethod
    def _choice_theme_override_from_master(cls, slide: SlideMaster):
        return slide.theme_override

    @classmethod
    def choice_format_scheme(cls, slide: SlideTypes):
        """选择合适的 format_scheme - 格式方案（也称为效果方案）

        theme 分别有两个地方引用: slide master, presentation

        theme_override 也分别有两个地方引用: slide layout, slide master

        取 format_scheme 时，优先从 theme_override 中获取， 其次才从 theme 中 获取
        """

        # 取 theme_override
        theme_override = cls.choice_theme_override(slide)
        format_scheme = None

        if theme_override is not None:
            # 取 theme_override 中 format_scheme
            logger.info('获取theme_override中的format_scheme')
            format_scheme = theme_override.format_scheme

        if format_scheme is None:
            logger.info('获取theme中的format_scheme')
            format_scheme = cls.choice_theme(slide).format_scheme

        if format_scheme is None:
            # 应该永远走不到这儿，演示文稿应至少保证存在一个
            msg = '获取 format_scheme - 格式方案（也称为效果方案）失败'
            raise ValueError(msg)

        return format_scheme

    @classmethod
    def choice_font_scheme(cls, slide: SlideTypes):
        """选择合适的 font_scheme - 字体方案

        theme 分别有两个地方引用: slide master, presentation

        theme_override 也分别有两个地方引用: slide layout, slide master

        取 font_scheme 时，优先从 theme_override 中获取， 其次才从 theme 中 获取
        """

        # 取 theme_override
        theme_override = cls.choice_theme_override(slide)
        font_scheme = None

        if theme_override is not None:
            # 取 theme_override 中 font_scheme
            font_scheme = theme_override.font_scheme

        else:
            font_scheme = cls.choice_theme(slide).font_scheme

        if font_scheme is None:
            # 应该永远走不到这儿，演示文稿应至少保证存在一个
            msg = '获取 font_scheme - 字体方案 失败'
            raise ValueError(msg)

        return font_scheme

    @classmethod
    def choice_color_schema(cls, slide: SlideTypes):
        """选择合适的 color_scheme - 颜色方案

        theme 分别有两个地方引用: slide master, presentation

        theme_override 也分别有两个地方引用: slide layout, slide master

        取 color_scheme 时，优先从 theme_override 中获取， 其次才从 theme 中 获取
        """

        # 取 theme_override
        theme_override = cls.choice_theme_override(slide)
        color_scheme = None

        if theme_override is not None:
            # 取 theme_override 中 color_scheme
            color_scheme = theme_override.color_scheme

        else:
            color_scheme = cls.choice_theme(slide).color_scheme

        if color_scheme is None:
            # 应该永远走不到这儿，演示文稿应至少保证存在一个
            msg = '获取 color_scheme - 颜色方案 失败'
            raise ValueError(msg)

        return color_scheme

    @classmethod
    def choice_color_map(cls, slide: SlideTypes):
        """选择合适的 color_map - 颜色映射

        有好几个地方都定义有color_map, 分别时: slide, slide layout, slide master, notes master

        所以查找的时候，优先从下向上查找
        """

        if isinstance(slide, Slide):
            return cls._choice_color_map_from_slide(slide)

        if isinstance(slide, SlideLayout):
            return cls._choice_color_map_from_layout(slide)

        return cls._choice_color_map_from_master(slide)

    @classmethod
    def _choice_color_map_from_slide(cls, slide: Slide):
        color_map = slide.color_map_override

        # 取layout的color_map
        if color_map is None:
            color_map = cls._choice_color_map_from_layout(slide.layout)

        return color_map

    @classmethod
    def _choice_color_map_from_layout(cls, slide: SlideLayout):
        color_map = slide.color_map_override

        # 取master的color_map
        if color_map is None:
            color_map = cls._choice_color_map_from_master(slide.master)

        return color_map

    @classmethod
    def _choice_color_map_from_master(cls, slide: SlideMaster):
        color_map = slide.color_map

        # logger.debug(f"choice 的 最终 color_map 为 {color_map =}")

        if color_map is None:
            # 应该永远都不会抛这个错, 演示文稿 至少应保证有一个color_map
            msg = 'schem color 的颜色映射为None'
            raise ValueError(msg)

        return color_map


# --------------- 颜色处理相关工具类 ---------------
