from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from ecma376_office.descriptor import lazyproperty
from ecma376_office.dml.style.blip import BlipEffect
from ecma376_office.dml.style.color import ColorTypes, color_factory
from ecma376_office.dml.style.effect import effect_factory
from ecma376_office.dml.style.fill import SolidColorFill, fill_factory
from ecma376_office.dml.style.line import LineStyle
from ecma376_office.oxml.dml.main import (
    CT_Color,
    CT_Hyperlink,
    CT_LineProperties,
    CT_PresetTextShape,
    CT_RegularTextRun,
    CT_TextAutonumberBullet,
    CT_TextBlipBullet,
    CT_TextBody,
    CT_TextBodyProperties,
    CT_TextBulletColorFollowText,
    CT_TextBulletSizeFollowText,
    CT_TextBulletSizePercent,
    CT_TextBulletSizePoint,
    CT_TextBulletTypefaceFollowText,
    CT_TextCharacterProperties,
    CT_TextCharBullet,
    CT_TextField,
    CT_TextFont,
    CT_TextLineBreak,
    CT_TextListStyle,
    CT_TextNoAutofit,
    CT_TextNoBullet,
    CT_TextNormalAutofit,
    CT_TextParagraph,
    CT_TextParagraphProperties,
    CT_TextShapeAutofit,
    CT_TextSpacingPercent,
    CT_TextSpacingPoint,
    CT_TextUnderlineFillFollowText,
    CT_TextUnderlineFillGroupWrapper,
    CT_TextUnderlineLineFollowText,
    ST_TextIndent,
    ST_TextMargin,
)
from ecma376_office.units import Emu

if TYPE_CHECKING:
    from ecma376_office.pml.shapes import NormalShape


class TextListStyle:
    """文本列表样式"""

    def __init__(self, oxml: CT_TextListStyle) -> None:
        """文本列表样式"""

        self.oxml = oxml

    @property
    def have_children(self):
        """子元素数量"""

        return self.oxml.have_chilren

    @property
    def default_paragraph_style(self):
        """默认段落样式"""

        pr = self.oxml.default_paragraph_properties

        if pr is not None:
            return TextParagraphProperties(pr)

        return None

    @property
    def level1_style(self):
        """默认级别1段落样式"""

        pr = self.oxml.level_1_paragraph_properties

        if pr is not None:
            return TextParagraphProperties(pr)

        return None

    @property
    def level2_style(self):
        """默认级别2段落样式"""

        pr = self.oxml.level_2_paragraph_properties

        if pr is not None:
            return TextParagraphProperties(pr)

        return None

    @property
    def level3_style(self):
        """默认级别3段落样式"""

        pr = self.oxml.level_3_paragraph_properties

        if pr is not None:
            return TextParagraphProperties(pr)

        return None

    @property
    def level4_style(self):
        """默认级别4段落样式"""

        pr = self.oxml.level_4_paragraph_properties

        if pr is not None:
            return TextParagraphProperties(pr)

        return None

    @property
    def level5_style(self):
        """默认级别5段落样式"""

        pr = self.oxml.level_5_paragraph_properties

        if pr is not None:
            return TextParagraphProperties(pr)

        return None

    @property
    def level6_style(self):
        """默认级别6段落样式"""

        pr = self.oxml.level_6_paragraph_properties

        if pr is not None:
            return TextParagraphProperties(pr)

        return None

    @property
    def level7_style(self):
        """默认级别7段落样式"""

        pr = self.oxml.level_7_paragraph_properties

        if pr is not None:
            return TextParagraphProperties(pr)

        return None

    @property
    def level8_style(self):
        """默认级别8段落样式"""

        pr = self.oxml.level_8_paragraph_properties

        if pr is not None:
            return TextParagraphProperties(pr)

        return None

    @property
    def level9_style(self):
        """默认级别9段落样式"""

        pr = self.oxml.level_9_paragraph_properties

        if pr is not None:
            return TextParagraphProperties(pr)

        return None

    def get_level_style(self, lvl: int):
        """根据级别获取对应的 text_lst_style"""
        return {
            0: self.level1_style,
            1: self.level2_style,
            2: self.level3_style,
            3: self.level4_style,
            4: self.level5_style,
            5: self.level6_style,
            6: self.level7_style,
            7: self.level8_style,
            8: self.level9_style,
        }[lvl]


# ---------------------- 正文内容及特性(属性)----------------------


class TextBody:
    """形状文本主体

    20.1.2.2.40 txBody

    该元素指定相应形状中是否存在要包含的文本。 所有可见文本和可见文本相关属性都包含在此元素内。 可以有多个段落，段落内可以有多个文本段.

    21.1.2.1 正文格式

    作为形状中可用的最高级别的格式设置，主体属性允许对整个文本区域进行操作。 这意味着相关形状的所有段落和文本运行都将包含在此处，因此遵循此处定义的文本正文样式。
    """

    def __init__(self, parent: Any, oxml: CT_TextBody) -> None:
        """文本框封装类

        形状文本主体

        20.1.2.2.40 txBody

        该元素指定相应形状中是否存在要包含的文本。 所有可见文本和可见文本相关属性都包含在此元素内。 可以有多个段落，段落内可以有多个文本段.

        21.1.2.1 正文格式

        作为形状中可用的最高级别的格式设置，主体属性允许对整个文本区域进行操作。 这意味着相关形状的所有段落和文本运行都将包含在此处，因此遵循此处定义的文本正文样式。
        """


        self.shape: NormalShape = parent
        self.oxml = oxml

    @lazyproperty
    def properties(self):
        """文本主体特性(属性)"""

        return TextBodyProperties(self.oxml.body_properties)

    @lazyproperty
    def text_list_style(self):
        """文本列表样式"""

        if self.oxml.text_list_style is None:
            return None

        return TextListStyle(self.oxml.text_list_style)

    @lazyproperty
    def paragraphs(self):
        """文本段落列表"""

        return [TextParagraph(paragraph) for paragraph in self.oxml.text_paragraphs]

    def to_json(self, slide: Any):
        """将本对象转化为json"""

        return {
            'type': 'textbox',
            'properties': self.properties.to_json(),
            'paragraphs': [paragraph.to_json(slide) for paragraph in self.paragraphs],
        }


class TextBodyProperties:
    """正文特性(属性)

    21.1.2.1.1 bodyPr

    此元素定义形状内文本正文的正文特性(属性)

    样例: 考虑一个带有文本正文的形状，该文本正文具有一些与其关联的格式属性。 对于文本正文属性的格式设置，应按如下方式使用 bodyPr 元素:

    <p:sp>
        …
        <p:txBody>
            <a:bodyPr>
                (text body properties)
            </a:bodyPr>
            …
        </p:txBody>
    </p:sp>
    """

    def __init__(self, oxml: CT_TextBodyProperties) -> None:
        """正文特性(属性)

        21.1.2.1.1 bodyPr

        此元素定义形状内文本正文的正文特性(属性)

        样例: 考虑一个带有文本正文的形状，该文本正文具有一些与其关联的格式属性。 对于文本正文属性的格式设置，应按如下方式使用 bodyPr 元素:

        <p:sp>
            …
            <p:txBody>
                <a:bodyPr>
                    (text body properties)
                </a:bodyPr>
                …
            </p:txBody>
        </p:sp>
        """

        self.oxml = oxml

    @property
    def preset_text_warp(self):
        """预设文本变形(扭曲)

        20.1.9.19 prstTxWarp (预设文本扭曲)

        该元素指定何时应使用预设的几何形状来变换一段文本。 此操作的正式名称为文本扭曲。 生成应用程序应该能够渲染 ST_TextShapeType 列表中枚举的所有预设几何图形。
        """

        if self.oxml.preset_text_warp is None:
            return None

        return PresetTextShape(self.oxml.preset_text_warp)

    @property
    def text_autofit(self):
        """文本自适应类型"""

        if self.oxml.text_autofit is None:
            return None

        return text_autofit_factory(self.oxml.text_autofit)

    @property
    def scene_3d(self):
        """3D 场景特性(属性)

        20.1.4.1.26 scene3d (3D Scene Properties)

        该元素定义了应用于对象的可选场景级 3D 属性。

        注意: 暂时无用
        """
        return self.oxml.scene_3d

    @property
    def text_3d(self):
        """3D图形属性"""

        return self.oxml.text_3d

    @property
    def rotate(self):
        """rot (旋转角度)

        指定应用于边界框内文本的旋转。 如果未指定，则使用伴随形状的旋转。 如果指定了，则其应用将独立于形状。 也就是说，除了文本本身应用旋转之外，形状还可以应用旋转。 如果省略该属性，则隐含值为 0。
        """

        return self.oxml.rotate

    @property
    def is_paragraph_spacing(self):
        """是否遵守用户定义的前后段落间距

        spcFirstLastPara (段落间距)

        指定是否遵守用户定义的前后段落间距。 虽然段落之间的间距很有帮助，但能够设置一个标志来确定是否在文本正文的边缘（即文本正文中的第一个和最后一个段落）遵循此间距也很有用。 更准确地说，由于这是文本主体级别的属性，因此它应该只影响给定文本主体的第一段之前的段落间距和最后一段的之后段落间距。 如果省略此属性，则隐含值为 0 或 false.
        """

        return self.oxml.spc_first_last_para

    @property
    def vert_overflow_type(self):
        """vertOverflow (文本垂直溢出)

        确定文本是否可以垂直流出边界框。 这用于确定如果形状内的文本对于其包含的边界框来说太大，会发生什么情况。 如果省略该属性，则隐含溢出值。
        """

        return self.oxml.vert_overflow

    @property
    def horz_overflow(self):
        """horzOverflow (文本水平溢出)

        确定文本是否可以水平流出边界框。 这用于确定如果形状内的文本对于其包含的边界框来说太大，会发生什么情况。 如果省略该属性，则隐含溢出值。
        """

        return self.oxml.horz_overflow

    @property
    def vert_type(self):
        """vert (竖排文字)

        确定给定文本正文中的文本是否应垂直显示。 如果省略此属性，则隐含水平值，或不隐含垂直文本。
        """

        return self.oxml.vert

    @property
    def wrap_type(self):
        """wrap (文本包裹类型)

        指定用于此文本正文的换行选项。 如果省略此属性，则隐含 square 值，该值使用边界文本框包裹文本。
        """

        return self.oxml.wrap

    @property
    def left_inset(self):
        """lIns (左边距)

        指定边界矩形的左边距。 边距仅用作形状内文本框的内部边距。 如果省略此属性，则隐含值 91440 或 0.1 英寸。
        """

        return self.oxml.left_ins

    @property
    def top_inset(self):
        """tIns (上边距)

        指定边界矩形的顶部边距。 边距仅用作形状内文本框的内部边距。 如果省略此属性，则隐含值 45720 或 0.05 英寸。
        """

        return self.oxml.top_ins

    @property
    def right_inset(self):
        """rIns (右边距)

        指定边界矩形的右边距。 边距仅用作形状内文本框的内部边距。 如果省略此属性，则隐含值 91440 或 0.1 英寸。
        """

        return self.oxml.right_ins

    @property
    def bottom_inset(self):
        """bIns (下边距)

        指定边界矩形的底部边距。 边距仅用作形状内文本框的内部边距。

        如果省略此属性，则隐含值 45720 或 0.05 英寸。
        """

        return self.oxml.bottom_ins

    @property
    def num_col(self):
        """边框中文本的列数

        numCol (列数)

        指定边框中文本的列数。 当应用于文本串时，此属性采用文本边框的宽度并将其除以指定的列数。 然后，这些列被视为溢出容器，因为当前一列已填充文本时，下一列将充当附加文本的存储库。 当所有列都已填充且文本仍然保留时，将使用为此文本正文设置的溢出属性，并重新排列文本以为其他文本腾出空间。 如果省略该属性，则隐含值为 1。
        """

        return self.oxml.num_col

    @property
    def space_with_columns(self):
        """spcCol (列之间的空间)

        指定文本区域中文本列之间的间距。 这仅适用于存在多于 1 列的情况。 如果省略该属性，则隐含值为 0。
        """

        return self.oxml.spc_col

    @property
    def rtl_col(self):
        """rtlCol (列从右到左)

        指定是按从右到左还是从左到右的顺序使用列。 此属性的用法仅设置列顺序，该顺序用于确定下一个溢出文本应转到哪一列。 如果省略此属性，则隐含值 0 或 false，在这种情况下，文本从最左边的列开始并向右流动。
        """

        return self.oxml.rtl_col

    @property
    def from_word_art(self):
        """文本框中的文本是从艺术字对象转换而来的文本

        fromWordArt (来自艺术字)

        指定此文本框中的文本是从艺术字对象转换而来的文本。 这更多的是一个向后兼容性属性，从跟踪的角度来看，它对应用程序很有用。 艺术字是应用文本效果的前一种方式，因此该属性在文档转换场景中非常有用。 如果省略此属性，则隐含值 0 或 false。
        """

        return self.oxml.from_word_art

    @property
    def anchor_type(self):
        """anchor (锚)

        指定 txBody 在形状内的锚定位置。 如果省略此属性，则隐含 t 或 top 值。

        也就是垂直对齐方式
        """

        return self.oxml.anchor

    @property
    def is_anchor_center(self):
        """anchorCtr (锚定中心)

        指定文本框的居中位置。 它的基本工作方式是确定文本的最小可能“边界框”，然后相应地将该“边界框”居中。 这与段落对齐不同，段落对齐在文本的“边界框”内对齐文本。 该标志与所有不同类型的锚定兼容。 如果省略此属性，则隐含值 0 或 false。
        """

        return self.oxml.anchor_center

    @property
    def is_force_aa(self):
        """forceAA (强制抗锯齿)

        Force Anti-Alias

        无论字体大小如何，强制文本呈现抗锯齿效果。 某些字体的边缘可能会出现颗粒状，除非它们经过抗锯齿处理。 因此，此属性允许指定哪些文本正文应始终消除锯齿，哪些不应消除锯齿。 如果省略此属性，则隐含值 0 或 false。
        """

        return self.oxml.force_aa

    @property
    def is_up_right(self):
        """upright (文字直立)

        指定文本是否应保持直立，无论对其应用的变换以及伴随的形状变换如何。 如果省略此属性，则隐含值为 0 或 false.
        """

        return self.oxml.up_right

    @property
    def is_compat_line_space(self):
        """compatLnSpc (兼容的行距)

        Compatible Line Spacing

        指定使用字体场景以简单的方式决定此文本正文的行距。 如果省略此属性，则隐含值 0 或 false。
        """

        return self.oxml.compat_line_space

    def to_json(self):
        """将本对象转化为json"""

        autofit = 'no'

        if self.text_autofit is None:
            autofit = 'no'

        elif isinstance(self.text_autofit, TextNoAutofit):
            autofit = 'no'  # 不自动适应

        elif isinstance(self.text_autofit, TextShapeAutofit):
            autofit = 'shape'  # 随形状自动适应

        else:
            autofit = self.text_autofit.to_json()

        return {
            'type': 'textbox_properties',  # 文本框属性
            'autofit': autofit,  # 文本自适应方式
            'rotate': self.rotate,  # 文本旋转角度
            'vert_overflow_type': self.vert_overflow_type.value,  # 文本是否可以垂直流出边界框以及处理方式
            'horz_overflow': self.horz_overflow.value,  # 文本是否可以水平流出边界框以及处理方式
            'vert_type': self.vert_type.value,  # 文本是否为竖排文字以及类型
            'wrap_type': self.wrap_type.value,  # 文本包裹类型
            'left_inset': self.left_inset,  # 左内边距 如果省略此属性，则隐含值 91440 或 0.1 英寸。
            'top_inset': self.top_inset,  # 上内边距 如果省略此属性，则隐含值 45720 或 0.05 英寸。
            'right_inset': self.right_inset,  # 右内边距  如果省略此属性，则隐含值 91440 或 0.1 英寸。
            'bottom_inset': self.bottom_inset,  # 下内边距, 如果省略此属性，则隐含值 45720 或 0.05 英寸。
            'num_col': self.num_col,  # 边框中文本的列数
            'space_with_columns': self.space_with_columns,  # 列之间的间距,  这仅适用于存在多于 1 列的情况。
            'rtl_col': self.rtl_col,  # 列从右到左, 指定是按从右到左还是从左到右的顺序使用列。
            'is_up_right': self.is_up_right,  # 文字直立 指定文本是否应保持直立，
            'is_compat_line_space': self.is_compat_line_space,  # 指定使用字体场景以简单的方式决定此文本正文的行距。 如果省略此属性，则隐含值 0 或 false。
        }


# ---------------------- 段落内容及特性(属性)----------------------


class TextParagraph:
    """文本段落

    21.1.2.2.6 p

    此元素指定包含的文本正文中是否存在文本段落。 段落是文本正文中最高级别的文本分隔机制。 段落可以包含与该段落关联的文本段落属性。 如果未列出任何属性，则使用 defPPr 元素中指定的属性。
    """

    def __init__(self, oxml: CT_TextParagraph) -> None:
        """文本段落

        21.1.2.2.6 p

        此元素指定包含的文本正文中是否存在文本段落。 段落是文本正文中最高级别的文本分隔机制。 段落可以包含与该段落关联的文本段落属性。 如果未列出任何属性，则使用 defPPr 元素中指定的属性。
        """

        self.oxml = oxml

    @property
    def paragraph_properites(self):
        """文本段落特性

        21.1.2.2.7 pPr

        此元素包含包含段落的所有段落级别文本属性。 这些段落属性应覆盖与相关段落关联的所有冲突属性。

        [Note: 要解决冲突的段落属性，应首先从 pPr 元素开始检查段落属性的线性层次结构。 这里的规则是在更接近实际文本的级别定义的属性应优先。 也就是说，如果 pPr 和 lvl1pPr 元素之间存在冲突属性，则 pPr 属性应优先，因为在属性层次结构中它更接近所表示的实际文本。 end note]
        """

        if self.oxml.paragraph_properites is None:
            return None

        return TextParagraphProperties(self.oxml.paragraph_properites)

    @property
    def text_runs(self):
        """文本run列表"""

        return [text_run_factory(run) for run in self.oxml.text_run_lst]

    @property
    def end_para_run_pr(self):
        """段落结尾的运行特性

        21.1.2.2.3 endParaRPr

        此元素指定在指定的最后一个运行之后插入另一个运行时要使用的文本运行属性。 这有效地保存了运行属性状态，以便在用户输入其他文本时可以应用它。 如果省略此元素，则应用程序可以确定要应用哪些默认属性。 建议在段落内的文本列表末尾指定此元素，以便维护有序列表。
        """

        if self.oxml.end_paraRPr is None:
            return None

        return TextCharacterProperties(self.oxml.end_paraRPr)

    def to_json(self, slide: Any):
        """将本对象转化为json"""

        properties = None

        if self.paragraph_properites is not None:
            properties = self.paragraph_properites.to_json(slide)

        runs = []

        for run in self.text_runs:
            if isinstance(run, RegularTextRun):
                runs.append(run.to_json(slide))

            elif isinstance(run, TextLineBreak):
                runs.append('\n')
            else:
                continue

        return {
            'type': 'textPragraph',
            'properties': properties,
            'runs': runs,
        }


class TextParagraphProperties:
    """文本段落属性(属性)

    21.1.2.2.7 pPr (Text Paragraph Properties)

    此元素包含包含段落的所有段落级别文本属性。 这些段落属性应覆盖与相关段落关联的所有冲突属性。

    [注意: 要解决冲突的段落属性，应首先从 pPr 元素开始检查段落属性的线性层次结构。
    这里的规则是在更接近实际文本的级别定义的属性应优先。
    也就是说，如果 pPr 和 lvl1pPr 元素之间存在冲突属性，则 pPr 属性应优先，
    因为在属性层次结构中它更接近所表示的实际文本。 ]
    """

    def __init__(self, oxml: CT_TextParagraphProperties) -> None:
        """文本段落属性(属性)

        21.1.2.2.7 pPr (Text Paragraph Properties)

        此元素包含包含段落的所有段落级别文本属性。 这些段落属性应覆盖与相关段落关联的所有冲突属性。

        [注意: 要解决冲突的段落属性，应首先从 pPr 元素开始检查段落属性的线性层次结构。
        这里的规则是在更接近实际文本的级别定义的属性应优先。
        也就是说，如果 pPr 和 lvl1pPr 元素之间存在冲突属性，则 pPr 属性应优先，
        因为在属性层次结构中它更接近所表示的实际文本。 ]
        """

        self.oxml = oxml

    @property
    def line_spacing(self):
        """行间距

        21.1.2.2.5 lnSpc (Line Spacing)

        此元素指定段落内要使用的垂直行距。
        这可以通过两种不同的方式指定: 百分比间距和字体点间距。
        如果省略此元素，则两行文本之间的间距应由一行内最大文本片段的磅值确定。
        """

        if self.oxml.line_spacing is None:
            return None

        return text_spacing_factory(self.oxml.line_spacing.spacing)

    @property
    def spacing_before(self):
        """段前间距

        21.1.2.2.10 spcBef (Space Before)

        此元素指定段落之前存在的垂直空白量。该间距通过子元素 spcPct 和 spcPts 以百分比或点数指定。
        """

        if self.oxml.spacing_before is None:
            return None

        return text_spacing_factory(self.oxml.spacing_before.spacing)

    @property
    def spacing_after(self):
        """段后间距

        21.1.2.2.9 spcAft (Space After)

        该元素指定段落之后出现的垂直空白量。该间距通过子元素 spcPct 和 spcPts 以百分比或点数指定。
        """

        if self.oxml.spacing_after is None:
            return None

        return text_spacing_factory(self.oxml.spacing_after.spacing)

    @property
    def text_bullet_color(self):
        """项目列表符号颜色类型

        21.1.2.4.4 buClr (指定颜色) -> CT_Color

            此元素指定给定段落中项目符号字符使用的颜色。 使用数字 RGB 颜色格式指定颜色。

        21.1.2.4.5 buClrTx (跟随文字)

            此元素指定段落项目符号的颜色应与包含每个项目符号的文本颜色相同。
        """

        if self.oxml.text_bullet_color is None:
            return None

        return text_bullet_color_factory(self.oxml.text_bullet_color)

    @property
    def text_bullet_size(self):
        """项目列表符号大小类型

        1. 跟随文本大小
        2. 根据字体大小确定的百分比大小
        3. 以磅为单位的点大小

        <xsd:group ref="EG_TextBulletSize" minOccurs="0" maxOccurs="1"/>
        """

        if self.oxml.text_bullet_size is None:
            return None

        return text_bullet_size_factory(self.oxml.text_bullet_size)

    @property
    def text_bullet_typeface(self):
        """项目列表符号字体类型

        <xsd:group ref="EG_TextBulletTypeface" minOccurs="0" maxOccurs="1"/>
        """

        if self.oxml.text_bullet_typeface is None:
            return None

        return text_bullet_typeface_factory(self.oxml.text_bullet_typeface)

    @property
    def text_bullet(self):
        """文本项目符号类型

        1. 无项目符号
        2. 自动编号项目符号
        3. 字符项目符号
        4. 图片项目符号

        <xsd:group ref="EG_TextBullet" minOccurs="0" maxOccurs="1"/>
        """

        return text_bullet_factory(self.oxml.text_bullet)

    @property
    def tab_lst(self):
        """制表位列表 tabLst

        21.1.2.2.14 tabLst

        此元素指定要在段落中使用的所有制表位的列表。 在描述文档中的任何自定义制表位时应使用这些制表符。 如果未指定这些，则应使用生成应用程序的默认制表位。
        """

        if self.oxml.tab_lst is None:
            return None

        return self.oxml.tab_lst

    @property
    def default_run_pr(self):
        """默认文本运行特性

        21.1.2.3.2 defRPr

        此元素包含包含段落内的文本运行的所有默认运行级别文本属性。 当 rPr 元素中尚未定义覆盖属性时，将使用这些属性。
        """

        if self.oxml.default_RPr is None:
            return None

        return TextCharacterProperties(self.oxml.default_RPr)

    @property
    def ext_lst(self):
        """扩展列表"""

        return self.oxml.ext_lst

    @property
    def margin_left(self):
        """左边距

        Left Margin

        指定段落的左边距。 这是除了文本正文插入之外指定的，并且仅适用于该文本段落。
        也就是说，文本正文插入和 marL 属性相对于文本位置是相加的。
        如果省略此属性，则隐含值 347663。
        """

        return self.oxml.margin_left

    @property
    def margin_right(self):
        """右边距

        Right Margin

        指定段落的右边距。 这是除了文本正文插入之外指定的，并且仅适用于该文本段落。
        也就是说，文本正文插入和 marR 属性相对于文本位置是相加的。
        如果省略该属性，则隐含值为 0。
        """

        return self.oxml.margin_right

    @property
    def level(self):
        """段落级别

        Level

        指定该段落所遵循的特定级别文本属性。
        此属性的值为数字，并根据 lstStyle 元素中列出的相应级别段落属性来设置文本格式。
        由于定义了九个单独的级别属性，因此该标记的有效范围为 0-8 = 9 个可用值。
        """

        return self.oxml.level

    @property
    def indent(self):
        """缩进

        Indent

        指定应用于段落中第一行文本的缩进大小。 缩进 0 被认为与 marL 属性位于同一位置。 如果省略此属性，则隐含值 -342900。
        """

        return self.oxml.indent

    @property
    def alignment(self):
        """对齐方式

        Alignment

        指定要应用于段落的对齐方式。 可能的值包括左、右、居中、对齐和分布。 如果省略此属性，则隐含 left 值。
        """

        return self.oxml.alignment

    @property
    def default_tab_size(self):
        """默认制表符大小

        Default Tab Size

        指定该段落中制表符的默认大小。 该属性应用于描述段落内制表符的间距，而不是前导缩进制表符。
        对于缩进选项卡，有 marL 和 indent 属性可以帮助实现这一点。
        """

        return self.oxml.default_tab_size

    @property
    def right_to_left(self):
        """从右到左

        Right To Left

        指定文本的流动方向是从右到左还是从左到右。 如果省略此属性，则隐含值 0 或从左到右。
        """

        return self.oxml.right_to_left

    @property
    def ea_line_break(self):
        """东亚字体行折断

        East Asian Line Break

        指定是否可以将东亚单词分成两半并换行到下一行而不添加连字符。
        为了确定东亚单词是否可以被分解，演示应用程序将使用此处的避头尾设置。
        当某个单词不能在没有连字符的情况下分成多个部分时，专门使用此属性。
        也就是说，它不存在于正常的可分解东亚单词的存在中，但是当出现不应因换行而被分解的特殊情况单词时出现。

        如果省略此属性，则隐含值 1 或 true。
        """

        return self.oxml.ea_line_break

    @property
    def font_align(self):
        """字体对齐类型

        Font Alignment

        确定实际单词在文本行上的垂直位置。 这涉及字符相对于基线的垂直放置。
        例如，将文本锚定到顶部基线、锚定到底部基线、居中等。要了解此属性及其用途，了解什么是基线将很有帮助。
        描述这些不同情况的图表如下所示。 如果省略此属性，则隐含 base 值。
        """

        return self.oxml.font_align

    @property
    def latin_line_break(self):
        """拉丁字体行折断

        Latin Line Break

        指定是否可以将拉丁语单词分成两半并换行到下一行而不添加连字符。
        当某个单词不能在没有连字符的情况下分成多个部分时，专门使用此属性。
        它不存在于正常的可分解拉丁单词中，但当出现特殊情况单词时，不应因换行而被分解。
        如果省略此属性，则隐含值 1 或 true。
        """

        return self.oxml.latin_line_break

    @property
    def hanging_punct(self):
        """悬挂标点符号

        Hanging Punctuation

        指定标点符号是强制放置在文本行上还是放置在不同的文本行上。
        也就是说，如果一串文本末尾有标点符号，应该将其转移到单独的行，那么它实际上会被转移。
        true 值允许悬挂标点符号，强制标点符号不被保留，而 false 值允许标点符号被保留到下一个文本行。

        如果省略此属性，则隐含值 0 或 false。
        """

        return self.oxml.hanging_punct

    def to_json(self, slide: Any):
        """将本对象转化为json"""

        return {
            'line_spacing': self._ts2px(self.line_spacing),  # 行间距
            'spacing_before': self._ts2px(self.spacing_before),  # 段前间距
            'spacing_after': self._ts2px(self.spacing_after),  # 段后间距
            'text_bullet_color': self._ts2clr(self.text_bullet_color, slide),  # 项目列表符号颜色类型
            'text_bullet_size': self._ts2sz(self.text_bullet_size),  # 项目符号大小
            'text_bullet_typeface': self._ts2tfc(self.text_bullet_typeface),  # 项目符号字体类型
            'text_bullet': self._ts2blt(self.text_bullet),  # 项目符号类型
            # "tab_lst": self.tab_lst, # 制表位列表
            'default_run_pr': self.default_run_pr.to_json(slide) if self.default_run_pr is not None else None,
            'margin_left': self._ts2mg(self.margin_left, default_emu=347663),  # 段落 左边距
            'margin_right': self._ts2mg(self.margin_right, default_emu=0),  # 段落 右边距
            'level': self.level,  # 段落级别
            'indent': self._ts2ind(self.indent, default_emu=-342900),  # 缩进
            'alignment': self.alignment.value if self.alignment is not None else None,  # 对齐方式
            'default_tab_size': self.default_tab_size,  # 默认制表符大小
            'right_to_left': self.right_to_left,  # 从右到左
            'font_align': self.font_align,  # 字体对齐类型
        }

    @staticmethod
    def _ts2px(unit: Optional[TextSpacingPercent | TextSpacingPoint]):
        """间距类型转像素"""
        if unit is None:
            return '0px'

        if isinstance(unit, TextSpacingPercent):
            return f'{unit * 100}%'

        return f'{Emu(unit).px}px'

    @staticmethod
    def _ts2clr(clr: ColorTypes | TextBulletColorFollowText, slide: Any):
        """转换颜色类型"""

        if isinstance(clr, TextBulletColorFollowText):
            return 'fllow_text'

        from ecma376_office.dml.tool.color import ColorTool

        return ColorTool.color_html(clr, slide)

    @staticmethod
    def _ts2sz(
        unit: Optional[TextBulletSizeFollowText | TextBulletSizePercent | TextBulletSizePoint],
    ):
        """转换项目符号大小"""

        if unit is None or isinstance(unit, TextBulletSizeFollowText):
            return 'fllow_text'

        if isinstance(unit, TextBulletSizePercent):
            return f'{unit * 100}%'

        return f'{Emu(unit).px}px'

    @staticmethod
    def _ts2tfc(unit: Optional[TextBulletTypefaceFollowText | TextFont]):
        """转换项目符号字体类型"""

        if unit is None or isinstance(unit, TextBulletTypefaceFollowText):
            return 'fllow_text'

        return unit.typeface  # 字体名称

    @staticmethod
    def _ts2blt(
        unit: Optional[TextNoBullet | TextAutonumberBullet | TextCharBullet | TextBlipBullet],
    ):
        """转换项目符号"""

        if unit is None or isinstance(unit, TextNoBullet):
            return None

        if isinstance(unit, TextAutonumberBullet):
            return unit.type

        if isinstance(unit, TextCharBullet):
            return unit

        return None

    @staticmethod
    def _ts2mg(mg: Optional[ST_TextMargin], default_emu: int):
        """转换段落边距"""

        if mg is None:
            return f'{Emu(default_emu).px}px'

        return f'{Emu(mg).px}px'

    @staticmethod
    def _ts2ind(mg: Optional[ST_TextIndent], default_emu: int):
        """转换段落缩进"""

        if mg is None:
            return f'{Emu(default_emu).px}px'

        return f'{Emu(mg).px}px'


# ---------------------- 文本run特性及属性----------------------


class RegularTextRun:
    """系列文本

    21.1.2.3.8 r (Text Run)

    该元素指定包含文本正文中是否存在一系列文本。 run 元素是文本正文中最低级别的文本分隔机制。
    文本运行可以包含与该运行关联的文本运行属性。
    如果未列出任何属性，则使用 defRPr 元素中指定的属性。

    例如:

    <a:r>
        <a:rPr b="1"></a:rPr>
        <a:t>Some text</a:t>
    </a:r>
    """

    def __init__(self, oxml: CT_RegularTextRun) -> None:
        """系列文本

        21.1.2.3.8 r (Text Run)

        该元素指定包含文本正文中是否存在一系列文本。 run 元素是文本正文中最低级别的文本分隔机制。
        文本运行可以包含与该运行关联的文本运行属性。
        如果未列出任何属性，则使用 defRPr 元素中指定的属性。

        例如:

        <a:r>
            <a:rPr b="1"></a:rPr>
            <a:t>Some text</a:t>
        </a:r>
        """

        self.oxml = oxml

    @property
    def character_pr(self):
        """文本属性

        21.1.2.3.9 rPr (Text Run Properties)

        此元素包含包含段落内的文本运行的所有运行级别文本属性。

        例如:

        <a:rPr u="sng"/>
        """

        if self.oxml.text_character_pr is None:
            return None

        return TextCharacterProperties(self.oxml.text_character_pr)

    @property
    def text(self):
        """文本字符串

        21.1.2.3.11 t (Text String)

        此元素指定此文本运行的实际文本。 这是使用所有指定的正文、段落和运行属性格式化的文本。 该元素应出现在一系列文本中。
        """

        return self.oxml.t

    def to_json(self, slide: Any):
        """将本对象转化为json"""

        return {
            'character_pr': self.character_pr.to_json(slide) if self.character_pr is not None else None,
            'text': self.text,
        }


class TextLineBreak:
    """文本换行

    21.1.2.2.1 br

        此元素指定段落内两行文本之间是否存在垂直换行符。 除了指定两次文本之间的垂直间距之外，此元素还可以具有通过 rPr 子元素指定的运行(run)特性。 这设置了换行符的文本格式，以便以后在此处插入文本时可以使用正确的格式生成新的运行(run)。
    """

    def __init__(self, oxml: CT_TextLineBreak) -> None:
        """系列文本

        21.1.2.3.8 r (Text Run)

        该元素指定包含文本正文中是否存在一系列文本。 run 元素是文本正文中最低级别的文本分隔机制。
        文本运行可以包含与该运行关联的文本运行属性。
        如果未列出任何属性，则使用 defRPr 元素中指定的属性。

        例如:

        <a:r>
            <a:rPr b="1"></a:rPr>
            <a:t>Some text</a:t>
        </a:r>
        """

        self.oxml = oxml

    @property
    def character_pr(self):
        """文本属性

        21.1.2.3.9 rPr (Text Run Properties)

        此元素包含包含段落内的文本运行的所有运行级别文本属性。

        例如:

        <a:rPr u="sng"/>
        """

        if self.oxml.text_character_pr is None:
            return None

        return TextCharacterProperties(self.oxml.text_character_pr)


class TextField:
    """文本字段(域)

    21.1.2.2.4 fld (Text Field)

    该元素指定一个文本字段，其中包含应用程序应定期更新的生成文本。
    每一段文本在生成时都会被赋予一个唯一的标识号，用于引用特定的字段。
    创建时，文本字段指示应用于更新该字段的文本类型。
    使用此更新类型是为了使所有未创建此文本字段的应用程序仍然可以知道应使用哪种类型的文本进行更新。
    因此，新应用程序可以将更新类型附加到文本字段 id 以进行持续更新。

    示例:
    <p:sp>
        <p:nvSpPr>
            <p:cNvPr id="2" name="日期占位符 1"/>
            <p:cNvSpPr>
                <a:spLocks noGrp="1"/>
            </p:cNvSpPr>
            <p:nvPr>
                <p:ph type="dt" sz="half" idx="10"/>
            </p:nvPr>
        </p:nvSpPr>
        <p:spPr/>
        <p:txBody>
            <a:bodyPr/>
            <a:lstStyle/>
            <a:p>
                <a:fld id="{079355E2-E30C-42ED-A639-75E2D8516D21}" type="datetime1">
                    <a:rPr lang="zh-CN" altLang="en-US" smtClean="0"/>
                </a:fld>
                <a:endParaRPr lang="zh-CN" altLang="en-US"/>
            </a:p>
        </p:txBody>
    </p:sp>
    """

    def __init__(self, oxml: CT_TextField) -> None:
        """文本字段(域)

        21.1.2.2.4 fld (Text Field)

        该元素指定一个文本字段，其中包含应用程序应定期更新的生成文本。
        每一段文本在生成时都会被赋予一个唯一的标识号，用于引用特定的字段。
        创建时，文本字段指示应用于更新该字段的文本类型。
        使用此更新类型是为了使所有未创建此文本字段的应用程序仍然可以知道应使用哪种类型的文本进行更新。
        因此，新应用程序可以将更新类型附加到文本字段 id 以进行持续更新。
        """

        self.oxml = oxml

    @property
    def character_pr(self):
        """文本属性

        21.1.2.3.9 rPr (Text Run Properties)

        此元素包含包含段落内的文本运行的所有运行级别文本属性。

        例如:

        <a:rPr u="sng"/>
        """

        if self.oxml.text_character_pr is None:
            return None

        return TextCharacterProperties(self.oxml.text_character_pr)

    @property
    def paragraph_pr(self):
        """文本段落属性"""

        if self.oxml.text_paragraph_pr is None:
            return None

        return TextParagraphProperties(self.oxml.text_paragraph_pr)

    @property
    def text(self):
        """文本"""

        return self.oxml.t

    @property
    def id(self):
        """字段ID

        Field ID

        指定此文档唯一的、主机指定的用于标识字段的标记。
        该标记在创建文本字段时生成，并作为相同标记保留在文件中，直到删除文本字段。
        任何应用程序都应在将新标记分配给文本字段之前检查文档是否存在冲突标记。
        """

        return self.oxml.id

    @property
    def type(self):
        """文本类型

        Field Type

        指定应用于更新此文本字段的文本类型。
        这用于通知渲染应用程序应该使用什么文本来更新此文本字段。
        此属性没有特定的语法限制。 生成应用程序可以使用它来表示在渲染演示文稿之前应更新的任何文本。

        保留值:

        slidenum - 演示幻灯片编号(presentation slide number)

        datetime - 渲染应用程序的默认日期时间格式(default date time format for the rendering application)

        datetime1 - MM/DD/YYYY 日期时间格式 [示例: 10/12/2007 ] (MM/DD/YYYY date time format [Example: 10/12/2007 end example])

        datetime2 - Day, Month DD, YYYY 日期时间格式 [示例: Friday, October 12, 2007 ] (Day, Month DD, YYYY date time format [Example: Friday, October 12, 2007 end example])

        datetime3 - DD Month YYYY 日期时间格式 [示例: 12 October 2007 ]

        datetime4 - Month DD, YYYY 日期时间格式 [示例: October 12, 2007 ]

        datetime5 - DD-Mon-YY 日期时间格式 [示例: 12-Oct-07 ]

        datetime6 - Month YY 日期时间格式 [示例: October 07 ]

        datetime7 - Mon-YY 日期时间格式 [示例: Oct-07 ]

        datetime8 - MM/DD/YYYY hh:mm AM/PM 日期时间格式 [示例: 10/12/2007 4:28 PM ]

        datetime9 - MM/DD/YYYY hh:mm:ss AM/PM 日期时间格式 [示例: 10/12/2007 4:28:34 PM ]

        datetime10 - hh:mm 日期时间格式 [示例: 16:28 ]

        datetime11 - hh:mm:ss 日期时间格式 [示例: 16:28:34 ]

        datetime12 - hh:mm AM/PM 日期时间格式 [示例: 4:28 PM ]

        datetime13 - hh:mm:ss: AM/PM 日期时间格式 [示例: 4:28:34 PM ]
        """

        return self.oxml.type


def text_run_factory(oxml: CT_RegularTextRun | CT_TextLineBreak | CT_TextField):
    """文本自适应工厂函数"""

    if isinstance(oxml, CT_RegularTextRun):
        return RegularTextRun(oxml)

    if isinstance(oxml, CT_TextLineBreak):
        return TextLineBreak(oxml)

    return TextField(oxml)


class TextCharacterProperties:
    """文本字符特性(属性)

    21.1.2.2.3 endParaRPr (End Paragraph Run Properties)

    此元素指定在指定的最后一个运行之后插入另一个运行时要使用的文本运行属性。
    这有效地保存了运行属性状态，以便在用户输入其他文本时可以应用它。
    如果省略此元素，则应用程序可以确定要应用哪些默认属性。
    建议在段落内的文本列表末尾指定此元素，以便维护有序列表。

    21.1.2.3.9 rPr (Text Run Properties)

    此元素包含包含段落内的文本运行的所有运行级别文本属性。

    21.1.2.3.2 defRPr (默认文本运行特性)

    此元素包含包含段落内的文本运行的所有默认运行级别文本属性。 当 rPr 元素中尚未定义覆盖属性时，将使用这些属性。
    """

    def __init__(self, oxml: CT_TextCharacterProperties) -> None:
        """文本字符特性(属性)"""

        self.oxml = oxml

    @property
    def line_properties(self):
        """线条特性(属性)

        20.1.2.2.24 ln

        此元素指定可应用于许多不同对象（例如形状和文本）的轮廓样式。 该
        线允许指定许多不同类型的轮廓，包括甚至线虚线和斜角。
        """

        if self.oxml.line_properties is None:
            return None

        return LineStyle(self.oxml.line_properties)

    @property
    def fill(self):
        """填充样式

        <xsd:group ref="EG_FillProperties" minOccurs="0" maxOccurs="1"/>
        """

        return fill_factory(self.oxml.fill)

    @property
    def effect(self):
        """效果样式

        <xsd:group ref="EG_EffectProperties" minOccurs="0" maxOccurs="1"/>
        """

        return effect_factory(self.oxml.effect)

    @property
    def highlight(self):
        """高亮颜色

        21.1.2.3.4 highlight

        该元素指定一系列文本的突出显示颜色。
        """

        if self.oxml.highlight is None:
            return None

        return color_factory(self.oxml.highlight.color)

    @property
    def text_underline_line(self):
        """下划线的线样式

        <xsd:group ref="EG_TextUnderlineLine" minOccurs="0" maxOccurs="1"/>
        """

        if self.oxml.text_underline_line is None:
            return None

        return text_underline_factory(self.oxml.text_underline_line)

    @property
    def text_underline_fill(self):
        """下划线的填充样式

        <xsd:group ref="EG_TextUnderlineLine" minOccurs="0" maxOccurs="1"/>
        """

        if self.oxml.text_underline_fill is None:
            return None

        return text_underline_fill_factory(self.oxml.text_underline_fill)

    @property
    def latin_font(self):
        """拉丁字体

        21.1.2.3.7 latin

        此元素指定将拉丁字体用于特定的文本运行。 该字体由与其他字体非常相似的字体属性指定，但被明确分类为拉丁字体。
        """

        if self.oxml.latin_font is None:
            return None

        return TextFont(self.oxml.latin_font)

    @property
    def ea_font(self):
        """东亚字体

        21.1.2.3.3 ea

        此元素指定将东亚字体用于特定的文本运行。 该字体指定的字体属性与其他字体非常相似，但被明确分类为东亚字体。
        """

        if self.oxml.ea_font is None:
            return None

        return TextFont(self.oxml.ea_font)

    @property
    def cs_font(self):
        """复杂脚本字体

        21.1.2.3.1 cs

        该元素指定将复杂的脚本字体用于特定的文本运行。 该字体由与其他字体非常相似的字体属性指定，但被明确分类为复杂脚本字体。

        如果指定的字体在用于渲染的系统上不可用，则可以利用该元素的属性来选择替代字体。
        """

        if self.oxml.cs_font is None:
            return None

        return TextFont(self.oxml.cs_font)

    @property
    def sym_font(self):
        """符号字体

        21.1.2.3.10 sym

        此元素指定用于特定文本运行的符号字体。 该字体由与其他字体非常相似的字体属性指定，但被专门分类为符号字体。
        """

        if self.oxml.sym_font is None:
            return None

        return TextFont(self.oxml.sym_font)

    @property
    def hlink_click(self):
        """单击超链接

        21.1.2.3.5 hlinkClick

        指定要应用于一系列文本的单击超链接信息。 单击超链接文本时，将获取链接。
        """

        if self.oxml.hlink_click is None:
            return None

        return TextHyperlink(self.oxml.hlink_click)

    @property
    def hlink_mouse_over(self):
        """鼠标悬停超链接

        21.1.2.3.6 hlinkMouseOver

        指定要应用于文本串的鼠标悬停超链接信息。 当鼠标悬停在此超链接文本上时，将获取链接。
        """

        if self.oxml.hlink_mouse_over is None:
            return None

        return TextHyperlink(self.oxml.hlink_mouse_over)

    @property
    def rtl(self):
        """Run从右向左

        21.1.2.2.8 rtl

        该元素指定该运行(run)的内容是否应具有从右到左的特征。 具体来说，当该元素的 val 属性为 true（或等效属性）时，将应用以下行为:

        - Formatting – 当显示本次运行的内容时，所有字符都将被视为复杂的脚本字符。 这意味着 cs 元素 ([§21.1.2.3.1]) 的值应用于确定字体。
        - Character Directionality Override – 当显示此运行的内容时，此属性充当按如下方式分类的字符的从右到左覆盖（使用 Unicode 字符数据库）:
            - 构成数字一部分时，除欧洲数字、欧洲数字终止符、普通数字分隔符、阿拉伯数字和（对于希伯来语文本）欧洲数字分隔符之外的弱类型
            - 中性类型 / Neutral types
        - [Rationale: 此覆盖允许应用程序存储和利用超出从 Unicode 双向算法隐式导出的信息的更高级别信息。 例如，如果字符串“第一秒”出现在文档内从右到左的段落中，则 Unicode 算法在显示时将始终导致“第一秒”（因为中性字符被强分类字符包围）。 但是，如果使用从右到左的输入法（例如希伯来语键盘）输入空格，则可以使用此属性将该字符分类为 RTL，从而允许以从右到左的方式显示“第二个第一” 段落，因为用户明确要求在从右到左的上下文中提供空格。 end rationale]

        此元素提供用于将单个字符的 (Unicode) 分类解析为 L、R、AN 或 EN 的信息。 一旦确定，该行的显示应遵循 Unicode 双向算法在重新排序已解析级别时的建议。

        此属性不得与强从左到右的文本一起使用。 该条件下的任何行为均未指定。 关闭此属性后，不应将其与强从右到左的文本一起使用。 该条件下的任何行为均未指定。

        如果此元素不存在，则默认值是保留样式层次结构中上一级别所应用的格式。 如果此元素从未应用于样式层次结构，则从右到左的特征不应应用于此运行的内容。
        """

        if self.oxml.rtl is None:
            return None

        return self.oxml.rtl.value

    @property
    def ext_lst(self):
        """扩展列表"""

        return self.oxml.ext_lst

    @property
    def kumimoji(self):
        """继续垂直

        指定垂直文本中包含的数字是否与文本垂直连续，或者是否水平显示而周围的字符继续垂直。 如果省略此属性，则假定值为 0 或 false。
        """

        return self.oxml.kumimoji

    @property
    def language(self):
        """语言ID / Language ID

        指定生成应用程序显示用户界面控件时要使用的语言。 如果省略此属性，则生成应用程序可以选择其选择的语言。
        """

        return self.oxml.language

    @property
    def alt_language(self):
        """替代语言 / Alternative Language

        指定生成应用程序显示用户界面控件时要使用的备用语言。 如果省略此属性，则此处使用 lang 属性。
        """

        return self.oxml.alt_language

    @property
    def font_size(self):
        """字体大小 / Font Size

        sz

        指定文本串中文本的大小。 整点以 100 为增量指定，从 100 开始，点大小为 1。

        例如，

        - 字体点大小 12 将是 1200，
        - 字体点大小 12.5 将是 1250。

        如果省略此属性，则比中的值 应使用 defRPr 中的值。
        """

        return self.oxml.font_size

    @property
    def blod(self):
        """粗体 / Bold

        指定文本串是否设置为粗体文本。 如果省略此属性，则假定值为 0 或 false。
        """

        return self.oxml.blod

    @property
    def italic(self):
        """斜体 / Italics

        指定文本串是否设置为斜体文本格式。 如果省略此属性，则假定值为 0 或 false。
        """

        return self.oxml.italic

    @property
    def underline_type(self):
        """下划线类型

        下划线 / Underline

        指定文本串的格式是否为带下划线的文本。 如果省略此属性，则假定没有下划线。
        """

        return self.oxml.underline_type

    @property
    def strike(self):
        """删除线 / Strikethrough

        指定一系列文本的格式是否为删除线文本。 如果省略此属性，则假定没有删除线。
        """

        return self.oxml.strike

    @property
    def kerning(self):
        """字距调整

        Kerning

        指定在此文本运行中进行字符字距调整的最小字体大小。
        整点以 100 为增量指定，从 100 开始，点大小为 1。
        例如，字体点大小 12 将是 1200，字体点大小 12.5 将是 1250。
        如果省略此属性，则会出现字距调整 所有字体大小均降至 0 磅字体。
        """

        return self.oxml.kerning

    @property
    def capitalization(self):
        """大写

        Capitalization

        指定要应用于文本串的大写。 这是仅渲染的修改，不会影响存储在文本运行中的实际字符。
        此属性也不同于切换功能，在切换功能中，存储在文本串中的实际字符会发生更改。
        """

        return self.oxml.capitalization

    @property
    def spacing(self):
        """字符间距

        Spacing

        指定文本串中字符之间的间距。 此间距以数字形式指定，并且应由生成应用程序在整个文本运行中一致应用。
        整点以 100 为增量指定，从 100 开始，点大小为 1。例如，字体点大小 12 将是 1200，字体点大小 12.5 将是 1250。

        如果省略此属性，则值为 0 或者假设没有调整。
        """

        return self.oxml.spacing

    @property
    def normalize_heights(self):
        """标准化高度

        Normalize Heights

        指定是否已检查文本运行中的智能标记。 此属性的作用与用于检查拼写、语法等的 dirty 属性剂量非常相似。
        此处的 true 值指示生成应用程序应检查此文本运行是否有智能标记。 如果省略此属性，则假定值为 0 或 false。
        """

        return self.oxml.normalize_heights

    @property
    def baseline(self):
        """基线

        Baseline

        指定上标和下标字体的基线。 使用百分比指定大小，其中 1% 等于字体大小的 1%，100% 等于字体大小的 100%。
        """

        return self.oxml.baseline

    @property
    def no_proof(self):
        """无需打样

        No Proofing

        指定用户已选择不检查错误的一系列文本。 因此，如果文本中存在拼写、语法等错误，生成应用程序应忽略它们。
        """

        return self.oxml.no_proof

    @property
    def dirty(self):
        """标记为脏数据

        Dirty

        指定自上次运行校对工具以来文本运行的内容已更改。 实际上，这会标记要由生成应用程序再次检查拼写、语法等错误的文本。
        """

        return self.oxml.dirty

    @property
    def error(self):
        """拼写错误

        Spelling Error

        指定当检查该文本运行的拼写、语法等时确实发现了错误。 这允许生成应用程序有效地保存文档内的错误状态，而不必在打开文档时执行全通过检查。
        """

        return self.oxml.error

    @property
    def smart_clean(self):
        """智能标签清洁

        SmartTag Clean

        指定是否已检查文本运行中的智能标记。 此属性的作用与用于检查拼写、语法等的 dirty 属性剂量非常相似。
        此处的 true 值指示生成应用程序应检查此文本运行是否有智能标记。
        如果省略此属性，则假定值为 0 或 false。
        """

        return self.oxml.smart_clean

    @property
    def smart_id(self):
        """智能标签 ID

        SmartTag ID

        指定一系列文本的智能标记标识符。 该ID在整个演示过程中是唯一的，用于引用有关智能标签的相应辅助信息。
        [注意: 有关智能标记的完整定义（在整个 Office Open XML 中语义相同），请参阅§17.5.1。 ]
        """

        return self.oxml.smart_id

    @property
    def bookmark(self):
        """书签链接目标

        Bookmark Link Target

        指定用于引用文档内自定义 XML 部件中正确链接属性的链接目标名称。
        """

        return self.oxml.bookmark

    def to_json(self, slide: Any):
        """将本对象转化为json"""

        from ecma376_office.dml.tool.color import ColorTool

        fill = None
        if isinstance(self.fill, SolidColorFill):
            fill = ColorTool.color_html(self.fill.color, slide, 'black')

        highlight = ColorTool.color_html(self.highlight, slide, 'black')

        return {
            'type': 'text_char_pr',
            'fill': fill,  # 填充颜色， 也就是字体颜色
            'highlight': highlight,  # 高亮颜色
            'underline': self.text_underline_line is not None,  # 是否有下划线
            'rtl': bool(self.rtl),  # 文本是否从右相左
            'kumimoji': bool(
                self.kumimoji
            ),  # 指定垂直文本中包含的数字是否与文本垂直连续，或者是否水平显示而周围的字符继续垂直。
            'language': self.language,
            'font_size': f'{self.font_size % 100}px' if self.font_size is not None else None,
            'blod': bool(self.blod),  # 是否为粗体
            'italic': bool(self.italic),  # 是否为斜体
            'underline_type': self.underline_type,  # 下划线类型, 为None则表示没有下划线
            'strike': bool(self.strike),  # 是否有删除线
            'kerning': f'{self.kerning % 100}px' if self.kerning is not None else None,  # 字距调整
            'capitalization': bool(self.capitalization),  # 是否为大写
            'spacing': f'{self.spacing % 100}px' if self.spacing is not None else '0px',  # 字间距
            'normalize_heights': bool(self.normalize_heights),  # 标准化高度 指定是否已检查文本运行中的智能标记。
            'baseline': self.baseline,  # 基线
            'no_proof': self.no_proof,  # 无需打样
            'dirty': self.dirty,  # 脏数据, 指定自上次运行校对工具以来文本运行的内容已更改。
            'error': self.error,  # 指定当检查该文本运行的拼写、语法等时确实发现了错误。
        }


# ---------------------- 文本行间距类型 ----------------------


class TextSpacingPercent(float):  # 0-1 之间的百分比
    """0-1 之间的百分比"""



class TextSpacingPoint(int):
    """文本间距点数"""



def text_spacing_factory(oxml: CT_TextSpacingPercent | CT_TextSpacingPoint):
    """文本间距工厂函数"""

    if isinstance(oxml, CT_TextSpacingPercent):
        return TextSpacingPercent(oxml.value)  # 0-1 之间的百分比

    return TextSpacingPoint(int(oxml.value))


# ---------------------- 文本项目列表符号颜色类型 ----------------------


class TextBulletColorFollowText(str):
    """21.1.2.4.5 buClrTx (跟随文字)

    此元素指定段落项目符号的颜色应与包含每个项目符号的文本颜色相同。
    """



def text_bullet_color_factory(oxml: CT_TextBulletColorFollowText | CT_Color):
    """项目列表符号颜色类型工厂函数

    21.1.2.4.4 buClr (指定颜色) -> CT_Color

        此元素指定给定段落中项目符号字符使用的颜色。 使用数字 RGB 颜色格式指定颜色。

    21.1.2.4.5 buClrTx (跟随文字)

        此元素指定段落项目符号的颜色应与包含每个项目符号的文本颜色相同。
    """

    if isinstance(oxml, CT_TextBulletColorFollowText):
        return TextBulletColorFollowText(1)

    # 21.1.2.4.4 buClr (指定颜色) -> CT_Color
    # 此元素指定给定段落中项目符号字符使用的颜色。 使用数字 RGB 颜色格式指定颜色。
    return color_factory(oxml.color)


# ---------------------- 文本项目列表符号尺寸类型----------------------


class TextBulletSizeFollowText(str):
    """1.1.2.4.11 buSzTx (项目符号大小跟随文本)

    此元素指定段落项目符号的大小应与包含每个项目符号的文本运行的磅值相同。
    """


class TextBulletSizePercent(float):  # 0 - 1
    """21.1.2.4.9 buSzPct (项目符号大小百分比)

    此元素指定给定段落内的项目符号字符所使用的周围文本的大小（以百分比表示）.

    value:

    项目符号应占文本大小的百分比

    指定该项目符号应占文本大小的百分比。 该属性不应低于25%且不应高于400%。
    """


class TextBulletSizePoint(float):  # emu 单位
    """项目符号大小Points

    21.1.2.4.10 buSzPts

    此元素指定给定段落内项目符号字符使用的大小（以磅为单位）。

    使用点指定大小，其中 100 等于 1 点字体，1200 等于 12 点字体。

    value:

    以点大小指定项目符号的大小

    以点大小指定项目符号的大小。 整点以 100 为增量指定，从 100 开始，点大小为 1。例如，字体点大小 12 将是 1200，字体点大小 12.5 将是 1250。
    """


def text_bullet_size_factory(
    oxml: CT_TextBulletSizeFollowText | CT_TextBulletSizePercent | CT_TextBulletSizePoint,
):
    """项目符号大小工厂函数"""
    if isinstance(oxml, CT_TextBulletSizeFollowText):
        return TextBulletSizeFollowText(1)

    if isinstance(oxml, CT_TextBulletSizePercent):
        return TextBulletSizePercent(oxml.value)

    return TextBulletSizePoint(oxml.value)


# ---------------------- 文本项目列表符号字体类型----------------------


class TextBulletTypefaceFollowText(str):
    """字体跟随文本

    21.1.2.4.7 buFontTx (跟随文字)

    此元素指定段落项目符号的字体应与包含每个项目符号的文本的字体相同。
    """


class TextFont:
    """文本字体

    21.1.2.3.1 cs (复杂脚本字体)

        该元素指定将复杂的脚本字体用于特定的文本运行。 该字体由与其他字体非常相似的字体属性指定，但被明确分类为复杂脚本字体。

    21.1.2.3.3 ea (东亚字体)

        此元素指定将东亚字体用于特定的文本运行。 该字体指定的字体属性与其他字体非常相似，但被明确分类为东亚字体。

    21.1.2.3.7 latin (拉丁字体)

        此元素指定将拉丁字体用于特定的文本运行。 该字体由与其他字体非常相似的字体属性指定，但被明确分类为拉丁字体。

    21.1.2.3.10 sym (符号字体)

        此元素指定用于特定文本运行的符号字体。 该字体由与其他字体非常相似的字体属性指定，但被专门分类为符号字体。

    21.1.2.4.6 buFont (特定字体)

        此元素指定给定段落内项目符号字符使用的字体。 字体是使用在生成应用程序中注册的字体来指定的。
    """

    def __init__(self, oxml: CT_TextFont) -> None:
        """文本字体

        21.1.2.3.1 cs (复杂脚本字体)

            该元素指定将复杂的脚本字体用于特定的文本运行。 该字体由与其他字体非常相似的字体属性指定，但被明确分类为复杂脚本字体。

        21.1.2.3.3 ea (东亚字体)

            此元素指定将东亚字体用于特定的文本运行。 该字体指定的字体属性与其他字体非常相似，但被明确分类为东亚字体。

        21.1.2.3.7 latin (拉丁字体)

            此元素指定将拉丁字体用于特定的文本运行。 该字体由与其他字体非常相似的字体属性指定，但被明确分类为拉丁字体。

        21.1.2.3.10 sym (符号字体)

            此元素指定用于特定文本运行的符号字体。 该字体由与其他字体非常相似的字体属性指定，但被专门分类为符号字体。

        21.1.2.4.6 buFont (特定字体)

            此元素指定给定段落内项目符号字符使用的字体。 字体是使用在生成应用程序中注册的字体来指定的。
        """

        self.oxml = oxml

    @property
    def typeface(self):
        """文本字体名称

        Text Typeface

        指定要使用的字体或字体名称。 字体是渲染演示文稿时应使用的特定字体的字符串名称。 如果该字体在生成应用程序的字体列表中不可用，则应利用字体替换逻辑来选择替代字体。
        """

        return self.oxml.typeface

    @property
    def panose(self):
        """帕诺塞设置

        Panose Setting

        使用 ISO/IEC 14496-22 §5.2.7.17 中定义的机制指定当前字体的 Panose-1 分类号。
        """

        return self.oxml.panose

    @property
    def pitch_family(self):
        """类似字体家族

        Similar Font Family

        指定字体间距以及相应字体的字体系列.

        该信息是通过查询存在的字体来确定的，并且在字体不可用时不得修改。 该信息可用于字体替换逻辑，以在该字体不可用时找到适当的替换字体。
        """

        return self.oxml.pitch_family

    @property
    def charset(self):
        """相似的字符集

        Similar Character Set

        指定父字体支持的字符集。 该信息可用于字体替换逻辑，以在该字体不可用时找到适当的替换字体。 该信息是通过查询存在的字体来确定的，并且在字体不可用时不得修改。

        该属性的值应解释如下：

        - 0x00: 指定 ANSI 字符集. (IANA 名称 iso-8859-1)
        - 0x01: 指定默认字符集.
        - 0x02: 指定符号字符集。 该值指定应该使用字体的 Unicode 专用区域（U+FF00 到 U+FFFF）中的字符来显示 U+0000 到 U+00FF 范围内的字符。
        - 0x4D: 指定 Macintosh（标准罗马）字符集. (IANA 名称 macintosh)
        - 0x80: 指定 JIS 字符集. (IANA 名称 shift_jis)
        - 0x81: 指定朝鲜文字(Hangul)符集. (IANA 名称 ks_c_5601-1987)
        - 0x82: 指定 Johab 字符集. (IANA 名称 KS C-5601-1992)
        - 0x86: 指定 GB-2312 字符集. (IANA 名称 GBK)
        - 0x88: 指定中文大五字符集. (IANA name Big5)
        - 0xA1: 指定希腊字符集. (IANA 名称 windows-1253)
        - 0xA2: 指定土耳其语字符集. (IANA 名称 iso-8859-9)
        - 0xA3: 指定越南语字符集. (IANA 名称 windows-1258)
        - 0xB1: 指定希伯来语字符集. (IANA 名称 windows-1255)
        - 0xB2: 指定阿拉伯字符集. (IANA 名称 windows-1256)
        - 0xBA: 指定波罗的海字符集. (IANA 名称 windows-1257)
        - 0xCC: 指定俄语字符集. (IANA 名称 windows-1251)
        - 0xDE: 指定泰语字符集. (IANA 名称 windows-874)
        - 0xEE: 指定东欧字符集. (IANA 名称 windows1250)
        - 0xFF: 指定 ECMA-376 未定义的 OEM 字符集。
        - Any other value: 应用程序定义的，可以忽略。
        """

        return self.oxml.charset


def text_bullet_typeface_factory(
    oxml: CT_TextBulletTypefaceFollowText | CT_TextFont,
):
    """文本项目符号字体类型"""

    if isinstance(oxml, CT_TextBulletTypefaceFollowText):
        return TextBulletTypefaceFollowText(1)

    # 21.1.2.4.6 buFont (特定字体)

    # 此元素指定给定段落内项目符号字符使用的字体。 字体是使用在生成应用程序中注册的字体来指定的。

    return TextFont(oxml)


# ---------------------- 文本项目符号类型----------------------


class TextNoBullet(str):
    """无项目符号

    21.1.2.4.8 buNone

    此元素指定应用该元素的段落不应用项目符号格式。 也就是说，在指定此元素的段落中不应找到项目符号。
    """


class TextAutonumberBullet:
    """自动编号项目符号

    21.1.2.4.1 buAutoNum

    此元素指定应将自动编号的项目符号点应用于段落。 这些不仅仅是用作要点的数字，而是基于 buAutoNum 属性和段落级别自动分配的数字。
    """

    def __init__(self, oxml: CT_TextAutonumberBullet) -> None:
        self.oxml = oxml

    @property
    def type(self):
        """项目符号自动编号类型

        Bullet Autonumbering Type

        指定要使用的编号方案。 这允许描述除严格数字之外的格式。 例如，一组项目符号可以用一系列罗马数字来表示，而不是标准的 1、2、3 等。 号码设定。
        """

        return self.oxml.type

    @property
    def start_at(self):
        """开始编号

        Start Numbering At

        指定给定的自动编号项目符号序列的开始编号。 当编号按字母顺序排列时，数字应映射到适当的字母。 例如，1 映射到“a”，2 映射到“b”，依此类推。 如果数字大于 26，则应使用多个字母。 例如，27 应表示为“aa”，类似地，53 应表示为“aaa”。
        """

        return self.oxml.start_at


class TextCharBullet(str):
    """字符项目符号

    21.1.2.4.3 buChar

    该元素指定将一个字符应用于一组项目符号。 这些项目符号可以是系统能够支持的任何字体的任何字符。 如果没有与此元素一起指定项目符号字体，则使用段落字体。
    """


class TextBlipBullet(BlipEffect):
    """图片项目符号

    21.1.2.4.2 buBlip

    此元素指定将图片应用于一组项目符号。 该元素允许使用任何标准图片格式图形来代替典型的项目符号字符。 这使得项目符号成为生成应用程序想要应用的任何东西的可能性。
    """



def text_bullet_factory(
    oxml: Optional[
        CT_TextNoBullet | CT_TextAutonumberBullet | CT_TextCharBullet | CT_TextBlipBullet
    ],
):
    """文本项目符号类型"""

    if oxml is None:
        return None

    if isinstance(oxml, CT_TextNoBullet):
        return TextNoBullet(1)

    if isinstance(oxml, CT_TextAutonumberBullet):
        return TextAutonumberBullet(oxml)

    if isinstance(oxml, CT_TextCharBullet):
        return TextCharBullet(oxml.char)

    # CT_TextBlipBullet

    return TextBlipBullet(oxml.blip)


# ---------------------- 文本下划线类型----------------------


class TextUnderlineLineFollowText:
    """下划线跟随文本

    21.1.2.3.15 uLnTx

    此元素指定文本串的下划线的笔划样式应与其包含的文本串相同。

    """

    def __init__(self, oxml: CT_TextUnderlineLineFollowText) -> None:
        self.oxml = oxml


def text_underline_factory(
    oxml: CT_TextUnderlineLineFollowText | CT_LineProperties,
):
    """文本下划线类型工厂函数"""

    if isinstance(oxml, CT_LineProperties):
        return LineStyle(oxml)

    return TextUnderlineLineFollowText(oxml)


# ---------------------- 文本下划线填充类型----------------------


class TextUnderlineFillFollowText:
    def __init__(self, oxml: CT_TextUnderlineFillFollowText) -> None:
        self.oxml = oxml


def text_underline_fill_factory(
    oxml: CT_TextUnderlineFillFollowText | CT_TextUnderlineFillGroupWrapper,
):
    """文本下划线填充类型工厂函数"""

    if isinstance(oxml, CT_TextUnderlineFillGroupWrapper):
        return fill_factory(oxml.fill)

    return TextUnderlineFillFollowText(oxml)


# ---------------------- 文本超链接----------------------


class TextHyperlink:
    """文本超链接

    超链接

    17.16.22 hyperlink (Hyperlink)
    18.3.1.47 hyperlink (Hyperlink)
    20.1.2.2.23 hlinkHover (Hyperlink for Hover)
    21.1.2.3.5 hlinkClick (Click Hyperlink)
    21.1.2.3.6 hlinkMouseOver (Mouse-Over Hyperlink)
    """

    def __init__(self, oxml: CT_Hyperlink) -> None:
        self.oxml = oxml

    @property
    def sound(self):
        """声音文件连接"""

        return self.oxml.sound

    @property
    def ext_lst(self):
        """扩展列表"""

        return self.oxml.ext_lst

    @property
    def r_id(self):
        """绘图对象超链接目标

        Drawing Object Hyperlink Target

        指定在此幻灯片关系文件中查找时包含此超链接目标的关系 ID。 该属性不能省略。
        """

        return self.oxml.r_id

    @property
    def invalid_url(self):
        """无效的网址 / Invalid URL

        当生成应用程序确定 URL 无效时指定该 URL。 也就是说，生成应用程序仍然可以存储 URL，但已知该 URL 不正确。
        """

        return self.oxml.invalid_url

    @property
    def action(self):
        """动作设定

        Action Setting

        指定激活此超链接时要执行的操作。 这可用于指定要导航到的幻灯片或要运行的代码脚本。
        """

        return self.oxml.action

    @property
    def target_frame(self):
        """目标框架 / Target Frame

        指定打开此超链接时要使用的目标框架。 当超链接被激活时，该属性用于确定是否启动新窗口以供查看或是否可以使用现有窗口。 如果省略此属性，则会打开一个新窗口。
        """

        return self.oxml.target_frame

    @property
    def tooltip(self):
        """超链接工具提示 / Hyperlink Tooltip

        指定当鼠标悬停在超链接文本上时应显示的工具提示。 如果省略此属性，则可以显示超链接文本本身。
        """

        return self.oxml.tooltip

    @property
    def history(self):
        """添加超链接到页面历史记录

        Add Hyperlink to Page History

        指定导航到此 URI 时是否将此 URI 添加到历史记录中。 这允许观看该演示文稿而无需在观看机器上存储历史信息。 如果省略此属性，则假定值为 1 或 true。

        <xsd:attribute name="history" type="xsd:boolean" use="optional" default="true"/>
        """

        return self.oxml.history

    @property
    def highlight_click(self):
        """突出显示单击

        Highlight Click

        指定此属性是否已在本文档中使用。 也就是说，当超链接已被访问时，将利用该属性，以便生成应用程序可以确定该文本的颜色。 如果省略此属性，则隐含值 0 或 false。
        """

        return self.oxml.highlight_click

    @property
    def end_sound(self):
        """结束声音

        End Sounds

        指定相关 URL 是否应在单击该 URL 时停止正在播放的所有声音.
        """

        return self.oxml.end_sound

    def to_json(self):
        """将本对象转化为json"""

        return {
            'properties': '',
        }


# ---------------------- 文本自适应类型----------------------


class TextNoAutofit(str):
    """不自动调整(适应)

    21.1.2.1.2 noAutofit

    此元素指定文本正文中的文本不应自动适合边界框。 自动调整是指缩放文本框中的文本以使其保留在文本框中。 如果省略此元素，则暗示 noAutofit 或 auto-fit off.
    """



class TextNormalAutofit:
    """文本正常自动调整(适应)

    21.1.2.1.3 normAutofit

    此元素指定文本正文中的文本通常应自动适合边界框。 自动调整是指缩放文本框中的文本以使其保留在文本框中。 如果省略此元素，则暗示 noAutofit 或 auto-fit off。
    """

    def __init__(self, oxml: CT_TextNormalAutofit) -> None:
        """文本正常自动调整(适应)

        21.1.2.1.3 normAutofit

        此元素指定文本正文中的文本通常应自动适合边界框。 自动调整是指缩放文本框中的文本以使其保留在文本框中。 如果省略此元素，则暗示 noAutofit 或 auto-fit off。
        """

        self.oxml = oxml

    @property
    def font_scale(self):
        """字体比例

        指定文本正文中每次运行缩放到的原始字体大小的百分比。 为了在边界框中自动调整文本，有时需要将字体大小减小一定的百分比。 使用此属性，可以根据提供的值缩放文本框中的字体。 值为 100% 会将文本缩放到 100%，而值为 1% 会将文本缩放到 1%。 如果省略此属性，则暗示值为 100%。
        """
        return self.oxml.font_scale

    @property
    def line_space_reduction(self):
        """减少行距

        指定文本正文中每个段落的行间距减少的百分比量。 通过从原始行距值中减去它来应用减少。 使用此属性，文本行之间的垂直间距可以按百分比缩放。 值为 100% 时，行间距会减少 100%，而值为 1% 时，行间距会减少百分之一。 如果省略此属性，则暗示值为 0%。

        [Note: 该属性仅适用于具有百分比行间距的段落. end note]
        """

        return self.oxml.line_space_reduction

    def to_json(self):
        """本对象转化为json"""

        return {
            'font_scale': self.font_scale,  # 字体缩放比例
            'line_space_reduction': self.line_space_reduction,  # 减少行距
        }


class TextShapeAutofit(str):
    """文本随形状自动调整适应

    21.1.2.1.4 spAutoFit

    此元素指定形状应自动调整以完全包含其中描述的文本。 自动调整是指缩放形状内的文本以包含其中的所有文本。 如果省略此元素，则暗示 noAutofit 或 auto-fit off。
    """


def text_autofit_factory(
    oxml: CT_TextNoAutofit | CT_TextNormalAutofit | CT_TextShapeAutofit,
):
    """文本自适应工厂函数"""

    if isinstance(oxml, CT_TextNoAutofit):
        return TextNoAutofit(1)

    if isinstance(oxml, CT_TextShapeAutofit):
        return TextShapeAutofit(1)

    return TextNormalAutofit(oxml)


# ---------------------- 文本变形(扭曲) ----------------------


class PresetTextShape:
    """预设文本及格式

    20.1.9.19 prstTxWarp

    该元素指定何时应使用预设的几何形状来变换一段文本。 此操作的正式名称为文本扭曲。 生成应用程序应该能够渲染 ST_TextShapeType 列表中枚举的所有预设几何图形。
    """

    def __init__(self, oxml: CT_PresetTextShape) -> None:
        """预设文本及格式

        20.1.9.19 prstTxWarp

        该元素指定何时应使用预设的几何形状来变换一段文本。 此操作的正式名称为文本扭曲。 生成应用程序应该能够渲染 ST_TextShapeType 列表中枚举的所有预设几何图形。
        """

        self.oxml = oxml


# ---------------------- 3d场景属性 ----------------------
