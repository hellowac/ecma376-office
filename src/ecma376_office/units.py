from typing import NewType

Angle = NewType('Angle', float)  # 角度, 旋转角度
""" 角度, 旋转角度, 阴影角度, ... """


DEGREE_INCREMENTS = 60000
THREE_SIXTY = 360 * DEGREE_INCREMENTS


def to_angle(value: float) -> Angle:
    """转换为角度"""

    rot = value % THREE_SIXTY
    return Angle(float(rot) / DEGREE_INCREMENTS)


Percent = NewType('Percent', float)
"""百分比值的数字化, 0-1 之间 """


class Length(int):
    """
    Base class for length classes Inches, Emu, Cm, Mm, Pt, and Px. Provides
    properties for converting length values to convenient units.

    长度单位类的基类，包括Inches（英寸）、Emu、Cm（厘米）、Mm（毫米）、Pt（点）和Px（像素）。提供将长度值转换为便捷单位的属性。

    wps 中 1磅约等于 0.3528 毫米 , 参考: https://www.wps.cn/learning/room/d/316973

    那么 2磅 约等于 0.7036 毫米, Mm(0.7036).emu
    """

    _EMUS_PER_INCH = 914400
    _EMUS_PER_CENTIPOINT = 127
    _EMUS_PER_CM = 360000
    _EMUS_PER_MM = 36000
    _EMUS_PER_PT = 12700
    # https://stackoverflow.com/questions/66541210/convert-google-slides-emu-units-to-pixels-api
    # https://stackoverflow.com/questions/20194403/openxml-distance-size-units
    # https://github.com/scanny/python-pptx/issues/116
    _EMUS_PER_PX = 9525

    def __new__(cls, emu):
        return int.__new__(cls, emu)

    @property
    def inches(self):
        """
        Floating point length in inches

        以英寸为单位的浮点长度
        """
        return self / float(self._EMUS_PER_INCH)

    @property
    def centipoints(self):
        """
        Integer length in hundredths of a point (1/7200 inch). Used
        internally because PowerPoint stores font size in centipoints.

        以百分之一点(1/7200 英寸)为单位的整数长度。
        在内部使用，因为 PowerPoint 以厘点存储字体大小。

        难道就是1磅的大小 ？
        """
        return self // self._EMUS_PER_CENTIPOINT

    @property
    def cm(self):
        """
        Floating point length in centimeters

        以厘米为单位的浮点长度
        """
        return self / float(self._EMUS_PER_CM)

    @property
    def emu(self):
        """
        Integer length in English Metric Units

        英制单位的整数长度
        """
        return self

    @property
    def mm(self):
        """
        Floating point length in millimeters

        浮点长度（以毫米为单位）
        """
        return self / float(self._EMUS_PER_MM)

    @property
    def pt(self):
        """
        Floating point length in points

        浮点长度（以点为单位）
        """
        return self / float(self._EMUS_PER_PT)

    @property
    def px(self):
        """

        浮点长度（以像素为单位）

        参考官方讨论:
        https://github.com/scanny/python-pptx/issues/116

        在*nix系统上, 72 像素等于 1英寸。
        """
        return self / float(self._EMUS_PER_PX)


class Inches(Length):
    """
    # Convenience constructor for length in inches

    以英寸为单位的长度的便捷构造函数
    """

    def __new__(cls, inches):
        emu = int(inches * Length._EMUS_PER_INCH)
        return Length.__new__(cls, emu)


class Centipoints(Length):
    """
    Convenience constructor for length in hundredths of a point

    以百分之一点为单位的长度的便捷构造函数

    内部使用， 代表1磅的单位等于多横扫EMU
    """

    def __new__(cls, centipoints):
        emu = int(centipoints * Length._EMUS_PER_CENTIPOINT)
        return Length.__new__(cls, emu)


class Cm(Length):
    """
    Convenience constructor for length in centimeters

    以厘米为单位的长度的便捷构造函数
    """

    def __new__(cls, cm):
        emu = int(cm * Length._EMUS_PER_CM)
        return Length.__new__(cls, emu)


class Emu(Length):
    """
    Convenience constructor for length in english metric units

    以英制公制单位表示长度的便捷构造函数
    """

    def __new__(cls, emu):
        return Length.__new__(cls, int(emu))


class Mm(Length):
    """
    Convenience constructor for length in millimeters

    以毫米为单位的长度的便捷构造函数
    """

    def __new__(cls, mm):
        emu = int(mm * Length._EMUS_PER_MM)
        return Length.__new__(cls, emu)


class Pt(Length):
    """
    Convenience value class for specifying a length in points

    用于指定长度（以点为单位）的便捷值类

    也就是wps中的 磅 单位， 1磅 = 12700 EMU

    更多单位参考: https://www.runoob.com/w3cnote/px-pt-em-convert-table.html
    """

    def __new__(cls, points):
        emu = int(points * Length._EMUS_PER_PT)
        return Length.__new__(cls, emu)


class Px(Length):
    """用于指定长度（以像素为单位）的便捷值类"""

    def __new__(cls, points):
        # 72 像素等于1英寸
        emu = int(points * Length._EMUS_PER_PX)
        return Length.__new__(cls, emu)
