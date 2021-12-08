# pylint: disable=missing-function-docstring

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base_element import _T_attribute


def attribute_bool(x: "_T_attribute") -> bool:
    return isinstance(x, bool)


def attribute_int(x: "_T_attribute") -> bool:
    return isinstance(x, int)


def attribute_int_ge_zero(x: "_T_attribute") -> bool:
    return isinstance(x, int) and x >= 0


def attribute_int_gt_zero(x: "_T_attribute") -> bool:
    return isinstance(x, int) and x > 0


def attribute_float(x: "_T_attribute") -> bool:
    return isinstance(x, (float, int))


def attribute_float_gt_zero(x: "_T_attribute") -> bool:
    return isinstance(x, (float, int)) and x > 0


def attribute_str(x: "_T_attribute") -> bool:
    return not isinstance(x, bool)


def attribute_unique_set(x: "_T_attribute", sep: str = " ") -> bool:
    if isinstance(x, bool):
        return False
    parts = str(x).split(sep)
    return len(parts) == len(set(parts))
