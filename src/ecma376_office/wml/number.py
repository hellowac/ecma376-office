import functools
import logging
from typing import TYPE_CHECKING, Any, Optional

from ecma376_office.oxml.wml.main import CT_AbstractNum, CT_Lvl, CT_Numbering, CT_NumPr, ST_NumberFormat
from ecma376_office.wml.parts import NumberingDefinitionsPart

if TYPE_CHECKING:
    from ecma376_office.wml.wordprocessing import WordProcessing

logger = logging.getLogger(__name__)

__all__ = [
    'Numbering',
]


class Numbering:
    def __init__(self, main_doc: Any, part: NumberingDefinitionsPart) -> None:
        """
        封装word主文档样式表部件操作类
        """


        self.main_doc: WordProcessing = main_doc
        self.part = part
        self.oxml = part.oxml
        self.abstract_num_map = self._build_num_map(part.oxml)
        self.abstract_map = self._build_abstract_num_map(part.oxml)

    def __del__(self):
        """清除缓存"""
        logger.info('清除docx编号的缓存')
        # self.get_numbering_text.cache_clear()
        self.get_lvl_style.cache_clear()
        self.abstract_map.clear()
        self.abstract_num_map.clear()

    def _build_num_map(self, oxml: CT_Numbering):
        """构建编号定义的字典"""

        return {int(num.numId): int(num.abstractNumId.val_dec_num) for num in oxml.num}

    def _build_abstract_num_map(self, oxml: CT_Numbering):
        """构建抽象编号定义的字典"""

        return {int(num.abstractNumId): AbstractNum(num) for num in oxml.abstractNum}

    # 这儿不能用缓存，编号需要实时计算结果
    # @functools.lru_cache
    def get_numbering_text(self, numPr: CT_NumPr):
        """获取抽象编号定义中指定级别的编号定义"""

        lvl_id = numPr.ilvl.val_dec_num if numPr.ilvl is not None else 0
        num_id = numPr.numId.val_dec_num if numPr.numId is not None else 0

        # logger.info(f"{num_id = } {lvl_id =}")

        abstract_num_id = self.abstract_num_map[num_id]

        # 获取对应的抽象编号实例获取编号文本。
        return self.abstract_map[abstract_num_id].get_numbering_text(lvl_id)

    @functools.lru_cache
    def get_lvl_style(self, numPr: CT_NumPr):
        lvl_id = numPr.ilvl.val_dec_num if numPr.ilvl is not None else 0
        num_id = int(numPr.numId.val_dec_num) if numPr.numId is not None else 0

        abstract_num_id = self.abstract_num_map.get(num_id)

        if abstract_num_id is None:
            return None

        try:
            return self.abstract_map[abstract_num_id].lvl_lst[lvl_id].oxml

        # 有些docx不规范，根本没有!
        except IndexError:
            return None


class AbstractNum:
    """抽象编号类"""

    def __init__(self, oxml: CT_AbstractNum):
        self.oxml = oxml
        self.lvl_lst = [NumLvl(lvl) for lvl in oxml.lvl]

    @property
    def absNumId(self):
        return int(self.oxml.abstractNumId)

    @property
    def multi_level_type(self):
        """抽象编号定义类型

        这个元素指定了由给定抽象编号类型定义的编号类型。此信息仅用于由消费者确定此编号定义的用户界面行为，并不用于限制列表的行为（即，将多个级别标记为单级别的列表不会阻止使用第2至第9级别）。

        如果省略此元素，则假定列表为消费者所需的任何编号类型。
        """

        return self.oxml.multiLevelType.val if self.oxml.multiLevelType is not None else None

    def get_numbering_text(self, ilvl: int):
        """获取指定编号级别的文本

        ilvl: 0～8 ， 表示第1至9的级别
        """

        global format_func_map  # 生命全局变量

        final_lvl = self.lvl_lst[ilvl]
        numformat_func = format_func_map.get(final_lvl.numFmt, Format_decimal)

        # 获取各个级别的编号的格式化后的字符
        formated_num_arr: list[str] = []

        for idx in range(ilvl + 1):
            current_lvl = self.lvl_lst[idx]

            # 小于当前级别的其他级别的编号取当前值.
            if idx < ilvl:
                current_num = current_lvl.current_num
            elif idx == ilvl:
                current_num = current_lvl.next_num
                # 初始化大于当级别的其他编号级别的索引.
                self.re_init_other_lvl_num(idx)
            else:  # idx > ilvl
                current_num = current_lvl.next_num

            show_num_format = numformat_func(current_num)

            formated_num_arr.append(show_num_format)

        # 将各个级别的编号占位符，替换为实际的格式化后的字符.
        # (%4)
        # %1.%2.%3.%4.%5.%6.
        num_templ = final_lvl.lvl_text or ''

        for idx in range(ilvl + 1):
            if num_templ != '':
                num_templ = num_templ.replace(f'%{idx + 1}', formated_num_arr[idx])
            else:
                num_templ += f'{formated_num_arr[idx]}.'

        return num_templ

    def re_init_other_lvl_num(self, ltidx: int):
        """重新初始化大于当前级别的lvl的索引"""

        for idx in range(ltidx + 1, len(self.lvl_lst)):
            # 置为None, 获取值时重新初始化
            self.lvl_lst[idx]._current_num = None


class NumLvl:
    """编号具体定义类"""

    def __init__(self, oxml: CT_Lvl):
        self.oxml = oxml
        self.iLvl = self.oxml.ilvl
        self._current_num: Optional[int] = None

    @property
    def current_num(self):
        """获取当前的编号"""

        # 初始化为指定的开始值
        if self._current_num is None:
            self._current_num = self.start

        return self._current_num

    @property
    def next_num(self):
        """获取下一个的编号"""

        # 初始化为指定的开始值
        if self._current_num is None:
            self._current_num = self.start
            return self._current_num

        self._current_num += 1
        return self._current_num

    @property
    def ilvl(self):
        """当前编号级别

        指定由这组编号属性定义的编号级别定义。

        此覆盖是文档中列表级别数量的零起始索引。

        【示例：值为 2 表示文档中的第三个列表级别。示例结束】
        """

        return int(self.oxml.ilvl)

    @property
    def tentative(self):
        """是否为临时编号

        指定给定编号级别已由生产者保存，但未在父文档中使用。这意味着该编号级别可以由未来的消费者重新定义，而不会更改文档的实际内容。

        对于此属性值，值为 1 或 true 表示该编号级别未在当前文档内容中使用。

        对于此属性值，值为 0 或 false 表示该编号级别已在父文档中使用，且不能重新定义而不更改其内容。这是此属性的默认值，在省略此属性时隐含。
        """

        return self.oxml.tentative if self.oxml.tentative is not None else False

    @property
    def start(self):
        """起始值

        该元素指定父编号级别在给定编号级别定义中使用的编号的起始值。当此级别在文档中首次启动时，以及每当通过 lvlRestart 元素（§17.9.10）中设置的属性重新启动时，将使用此值。
        """
        return int(self.oxml.start.val_dec_num) if self.oxml.start is not None else 0

    @property
    def numFmt(self):
        return self.oxml.numFmt.val if self.oxml.numFmt is not None else ST_NumberFormat.decimal  # 十进制级别

    @property
    def is_Lgl(self):
        """使用阿拉伯数字显示所有级别, 针对法律条款

        此元素指定是否应将给定编号级别的所有显示级别的文本使用十进制数格式显示，而不论该级别在列表中的实际编号格式如何。【注意：这种编号样式通常称为法律编号样式。注意结束】

        如果存在此元素，那么在显示此级别的编号格式时，lvlTxt 元素（§17.9.11）中的所有编号级别都将转换为其十进制等价物。如果省略此元素，那么每个级别将使用该级别的 numFmt（§17.9.17）显示。
        """

        return self.oxml.isLgl.is_on if self.oxml.isLgl is not None else False

    @property
    def lvl_text(self):
        """编号级别文本

        该元素指定了在显示具有给定编号级别的段落时应显示的文本内容。

        [示例：考虑以下用于编号级别的 WordprocessingML：

        <w:lvl w:ilvl="1">
            …
            <w:lvlText w:val="字符串A %2 字符串B %1 字符串C %3"/> …
        </w:lvl>
        """

        return self.oxml.lvlText.val if self.oxml.lvlText is not None else None


# @functools.lru_cache
def Format_none(idx: int):
    """对应 ST_NumberFormat.none 的编号方式的实现 （无编号）

    指定序列不显示任何编号。"""
    return ''


# @functools.lru_cache
def Format_decimal(idx: int):
    return str(idx)


def Format_decimalEnclosedFullstop(idx: int):
    """对应 ST_NumberFormat.decimalEnclosedFullstop 的编号方式的实现"""

    num_map = (
        '⒈',
        '⒉',
        '⒊',
        '⒋',
        '⒌',
        '⒍',
        '⒎',
        '⒏',
        '⒐',
        '⒑',
        '⒒',
        '⒓',
        '⒔',
        '⒕',
        '⒖',
        '⒗',
        '⒘',
        '⒙',
        '⒚',
        '⒛',
    )

    num = idx

    num_arr: list[str] = []

    while num > 10:
        num_arr.append(num_map[num % 10])
        num = int(num / 10)

    num_arr.append(num_map[num % 10])

    return ''.join(num_arr)


# @functools.lru_cache
def Format_decimalEnclosedParen(idx: int):
    """对应 ST_NumberFormat.decimalEnclosedParen 的编号方式的实现"""

    num_map = (
        '⑴',
        '⑵',
        '⑶',
        '⑷',
        '⑸',
        '⑹',
        '⑺',
        '⑻',
        '⑼',
        '⑽',
        '⑾',
        '⑿',
        '⒀',
        '⒁',
        '⒂',
        '⒃',
        '⒄',
        '⒅',
        '⒆',
        '⒇',
    )

    num = idx

    num_arr: list[str] = []

    while num > 10:
        num_arr.append(num_map[num % 10])
        num = int(num / 10)

    num_arr.append(num_map[num % 10])

    return ''.join(num_arr)


# @functools.lru_cache
def Format_chineseCounting(idx: int):
    """对应 ST_NumberFormat.chineseCounting 的编号方式的实现

    0 -> 〇
    1 -> 一
    2 -> 二
    3 -> 三
    ...
    9 -> 九
    10 -> 一〇
    """

    num_map = ('〇', '一', '二', '三', '四', '五', '六', '七', '八', '九')

    num = idx

    num_arr: list[str] = []

    while num > 10:
        num_arr.append(num_map[num % 10])
        num = int(num / 10)

    num_arr.append(num_map[num % 10])

    return ''.join(num_arr)


def Format_chineseCountingThousand(idx: int):
    """对应 ST_NumberFormat.chineseCountingThousand 的编号方式的实现

    0 -> 〇
    1 -> 一
    2 -> 二
    3 -> 三
    ...
    9 -> 九
    10 -> 一〇
    """

    num_map = ('〇', '一', '二', '三', '四', '五', '六', '七', '八', '九')

    num = idx

    num_arr: list[str] = []

    while num > 10:
        num_arr.append(num_map[num % 10])
        num = int(num / 10)

    num_arr.append(num_map[num % 10])

    return ''.join(num_arr)


def Format_chineseLegalSimplified(idx: int):
    """对应 ST_NumberFormat.chineseLegalSimplified 的编号方式的实现

    0 -> 零
    1 -> 壹
    2 -> 贰
    3 -> 叁
    ...
    9 -> 玖
    10 -> 拾
    """

    num_map = ('零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖')

    num = idx

    num_arr: list[str] = []

    while num > 10:
        num_arr.append(num_map[num % 10])
        num = int(num / 10)

    num_arr.append(num_map[num % 10])

    return ''.join(num_arr)


def Format_decimalEnclosedCircle(idx: int):
    """对应 ST_NumberFormat.decimalEnclosedCircle 和 decimalEnclosedCircleChinese 的编号方式的实现

    0 -> ⓪
    1 -> ①
    2 -> ②
    3 -> ③
    ...
    9 -> ⑨
    10 -> ⑩
    """

    num_map = (
        '⓪',
        '①',
        '②',
        '③',
        '④',
        '⑤',
        '⑥',
        '⑦',
        '⑧',
        '⑨',
        '⑩',
        '⑪',
        '⑫',
        '⑬',
        '⑭',
        '⑮',
        '⑯',
        '⑰',
        '⑱',
        '⑲',
        '⑳',
    )

    num = idx

    num_arr: list[str] = []

    while num > 10:
        num_arr.append(num_map[num % 10])
        num = int(num / 10)

    num_arr.append(num_map[num % 10])

    return ''.join(num_arr)


format_func_map = {
    ST_NumberFormat.decimal: Format_decimal,
    ST_NumberFormat.decimalEnclosedFullstop: Format_decimalEnclosedFullstop,
    ST_NumberFormat.decimalEnclosedParen: Format_decimalEnclosedParen,
    ST_NumberFormat.chineseCounting: Format_chineseCounting,
    ST_NumberFormat.chineseCountingThousand: Format_chineseCountingThousand,
    ST_NumberFormat.chineseLegalSimplified: Format_chineseLegalSimplified,
    ST_NumberFormat.decimalEnclosedCircle: Format_decimalEnclosedCircle,
    ST_NumberFormat.decimalEnclosedCircleChinese: Format_decimalEnclosedCircle,
    ST_NumberFormat.none: Format_none,
    # 其他未实现的索引编号的默认格式化编号函数
    None: Format_decimal,
}
