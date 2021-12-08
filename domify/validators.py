# pylint: disable=missing-function-docstring

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base_element import _T_attribute


def bool_validator(x: "_T_attribute") -> bool:
    return isinstance(x, bool)


def int_validator(x: "_T_attribute") -> bool:
    return isinstance(x, int)


def int_ge_zero_validator(x: "_T_attribute") -> bool:
    return isinstance(x, int) and x >= 0


def int_gt_zero_validator(x: "_T_attribute") -> bool:
    return isinstance(x, int) and x > 0


def float_validator(x: "_T_attribute") -> bool:
    return isinstance(x, (float, int))


def float_gt_zero_validator(x: "_T_attribute") -> bool:
    return isinstance(x, (float, int)) and x > 0


def str_validator(x: "_T_attribute") -> bool:
    return not isinstance(x, bool)


def unique_set_validator(x: "_T_attribute", sep: str = " ") -> bool:
    if isinstance(x, bool):
        return False
    parts = str(x).split(sep)
    return len(parts) == len(set(parts))
