"""oxml 工具模块"""

from __future__ import annotations

from typing import Any, AnyStr, Optional

from ecma376_office.oxml.exceptions import OxmlAttributeValidateError


def XsdBool(val: Optional[str | bytes], none: bool = False):
    """将 xsd:boolean 的值转为 True 或 False

    none: 对应 val 为 None 时, 应返回的值(默认值)
    """

    if val is None:
        return none

    _val = val.decode() if isinstance(val, bytes) else val

    if _val not in {'1', '0', 'true', 'false'}:
        msg = f'预期外的值: {_val}'
        raise OxmlAttributeValidateError(msg)

    return _val in {'1', 'true'}


def AnyStrToStr(val: Optional[AnyStr] = None) -> str:
    """
    将str或byts 转为 str
    """
    if isinstance(val, bytes):
        return val.decode()

    return val or ''


def XsdUnsignedInt(val: Any) -> int:
    """转为 int"""

    int_val = int(val)

    # int_val = int_val << 32

    if not (0 <= int_val <= 4294967295):
        msg = f'预期外的值: {int_val}'
        raise OxmlAttributeValidateError(msg)

    return int_val
