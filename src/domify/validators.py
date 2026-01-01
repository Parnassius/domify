from __future__ import annotations

from collections.abc import Callable, Iterable
from functools import partial
from typing import TypeVar, cast

from domify.base_element import _T_attribute

_T = TypeVar("_T")


def _attribute_to_string(x: _T_attribute, case_insensitive: bool) -> str:
    x = str(x)
    if case_insensitive:
        x = x.lower()
    return x


def attribute_all(
    *funcs: Callable[[_T_attribute], bool],
) -> Callable[[_T_attribute], bool]:
    return lambda x: all(f(x) for f in funcs)


def attribute_any(
    *funcs: Callable[[_T_attribute], bool],
) -> Callable[[_T_attribute], bool]:
    return lambda x: any(f(x) for f in funcs)


def attribute_bool(x: _T_attribute) -> bool:
    return isinstance(x, bool)


def _attribute_number(
    x: _T_attribute,
    *,
    is_float: bool,
    le: int | None = None,
    ge: int | None = None,
    lt: int | None = None,
    gt: int | None = None,
) -> bool:
    if not isinstance(x, (float, int) if is_float else int):
        return False
    x = cast("float | int", x)
    return (
        (le is None or x <= le)
        and (ge is None or x >= ge)
        and (lt is None or x < lt)
        and (gt is None or x > gt)
    )


attribute_int = partial(_attribute_number, is_float=False)
attribute_int_ge_zero = partial(attribute_int, ge=0)
attribute_int_gt_zero = partial(attribute_int, gt=0)

attribute_float = partial(_attribute_number, is_float=True)
attribute_float_gt_zero = partial(attribute_float, gt=0)


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
    if values is not None and not set(parts) <= set(values):  # noqa: SIM103
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
