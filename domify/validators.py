from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING, Callable, Iterable

if TYPE_CHECKING:
    from domify.base_element import _T_attribute


def _attribute_to_string(x: _T_attribute, case_insensitive: bool) -> str:
    x = str(x)
    if case_insensitive:
        x = x.lower()
    return x


def attribute_all(
    *funcs: Callable[[_T_attribute], bool]
) -> Callable[[_T_attribute], bool]:
    return lambda x: all(f(x) for f in funcs)


def attribute_any(
    *funcs: Callable[[_T_attribute], bool]
) -> Callable[[_T_attribute], bool]:
    return lambda x: any(f(x) for f in funcs)


def attribute_bool(x: _T_attribute) -> bool:
    return isinstance(x, bool)


def attribute_int(x: _T_attribute) -> bool:
    return isinstance(x, int)


def attribute_int_ge_zero(x: _T_attribute) -> bool:
    return isinstance(x, int) and x >= 0


def attribute_int_gt_zero(x: _T_attribute) -> bool:
    return isinstance(x, int) and x > 0


def attribute_float(x: _T_attribute) -> bool:
    return isinstance(x, (float, int))


def attribute_float_gt_zero(x: _T_attribute) -> bool:
    return isinstance(x, (float, int)) and x > 0


def attribute_str(
    x: _T_attribute,
    *,
    values: Iterable[str] | None = None,
    case_insensitive: bool = False,
) -> bool:
    if isinstance(x, bool):
        return False
    if values:
        x = _attribute_to_string(x, case_insensitive)
        if x not in values:
            return False
    return True


attribute_str_ci = partial(attribute_str, case_insensitive=True)


def attribute_str_literal(
    *values: str, case_insensitive: bool = False
) -> Callable[[_T_attribute], bool]:
    return partial(attribute_str, values=values, case_insensitive=case_insensitive)


attribute_str_literal_ci = partial(attribute_str_literal, case_insensitive=True)


def attribute_unique_set(
    x: _T_attribute,
    *,
    values: Iterable[str] | None = None,
    sep: str = " ",
    case_insensitive: bool = False,
) -> bool:
    if isinstance(x, bool):
        return False
    x = _attribute_to_string(x, case_insensitive)
    parts = x.split(sep)
    if len(parts) != len(set(parts)):
        return False
    if values is not None and not set(parts) <= set(values):
        return False
    return True


attribute_unique_set_ci = partial(attribute_unique_set, case_insensitive=True)


def attribute_unique_set_literal(
    *values: str, sep: str = " ", case_insensitive: bool = False
) -> Callable[[_T_attribute], bool]:
    return partial(
        attribute_unique_set, values=values, sep=sep, case_insensitive=case_insensitive
    )


attribute_unique_set_literal_ci = partial(
    attribute_unique_set_literal, case_insensitive=True
)
