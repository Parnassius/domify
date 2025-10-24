from __future__ import annotations

import warnings
from collections.abc import Iterable, Iterator
from contextvars import ContextVar
from html import escape
from types import TracebackType
from typing import Callable, ClassVar, Literal, TypeVar, Union, cast, overload

from domify import exc
from domify import validators as v

_T_BaseElement = TypeVar("_T_BaseElement", bound="BaseElement")
_T_attribute = Union[str, float, bool]
_T_child = Union["BaseElement", str, float]
_T_attributes_dict = dict[str, Union[set[str], Callable[[_T_attribute], bool]]]


class BaseElement:
    """Base class representing an element"""

    is_empty = False
    global_attributes: ClassVar[_T_attributes_dict] = {}
    element_attributes: ClassVar[_T_attributes_dict] = {}
    any_attribute = False

    _default_prepend_doctype = False

    _stack_var: ContextVar[list[list[BaseElement]] | None] = ContextVar(
        "stack", default=None
    )

    def __init__(
        self,
        *args: _T_child,
        _prepend_doctype: bool | None = None,
        **kwargs: _T_attribute | None,
    ) -> None:
        """
        Args:
            *args: The element's children. A `TextNode` is automatically created when
                passing anything other than a subclass of `BaseElement`.
            _prepend_doctype: Whether a `DOCTYPE` declaration should be prepended.
                Defaults to the value of the class attribute `_default_prepend_doctype`
                (`True` for `html_elements.Html`, `False` for everything else).
            **kwargs: The element's attributes. Trailing underscores are automatically
                stripped, to avoid clashing with reserved keywords when setting
                attributes like `class` and `for`. Any other underscore is replaced by
                a dash, to allow setting `data` and `aria` attributes. `True` and
                `False` can be used for boolean attributes.

        Raises:
            EmptyElementChildrenError: If the element is an empty one and at least a
                child argument is passed.
        """
        if self.is_empty and args:
            raise exc.EmptyElementChildrenError

        if _prepend_doctype is None:
            _prepend_doctype = self._default_prepend_doctype
        self._prepend_doctype = _prepend_doctype
        self._attributes: dict[str, str | Literal[True]] = {}
        self._children: list[BaseElement] = []

        self._add_to_stack(self)

        for child in args:
            self._add_child(child)

        for key, val in kwargs.items():
            if val is None:
                continue
            self._set_attribute(key, val)

    @property
    def _stack(self) -> list[list[BaseElement]]:
        stack = self._stack_var.get()
        if stack is None:
            stack = []
            self._stack_var.set(stack)
        return stack

    def _add_to_stack(self, element: BaseElement) -> None:
        if self._stack:
            self._stack[-1].append(element)

    def _remove_from_stack(self, element: BaseElement) -> None:
        if self._stack and element in self._stack[-1]:
            self._stack[-1].remove(element)
        self._maybe_clear_stack()

    def _maybe_clear_stack(self) -> None:
        if not self._stack:
            self._stack_var.set(None)

    @property
    def name(self) -> str:
        """
        Returns:
            The lowercase name of the element, with trailing underscores removed.
        """
        return type(self).__name__.rstrip("_").lower()

    # Attributes
    def get_classes(self) -> list[str]:
        """Get the current element's classes

        Returns:
            The current element's classes as a list of strings.
        """
        classes = self._attributes.get("class", True)
        if classes is True:
            return []
        return [x for x in classes.split(" ") if x]

    def add_class(self, *args: str) -> None:
        """Add one or more classes to the the current element

        Args:
            args: The class (or classes) to add.
        """
        classes = self.get_classes()
        for cls in args:
            if cls not in classes:
                classes.append(cls)
        self._attributes["class"] = " ".join(classes)

    def remove_class(self, *args: str) -> None:
        """Remove one or more classes from the the current element

        Args:
            args: The class (or classes) to remove.
        """
        classes = self.get_classes()
        for cls in args:
            classes.remove(cls)
        self._attributes["class"] = " ".join(classes)

    @property
    def all_attributes(self) -> _T_attributes_dict:
        """
        Returns:
            A dict containing both global and element-specific attributes
        """
        return {**self.global_attributes, **self.element_attributes}

    def _set_attribute(self, key: str, val: _T_attribute) -> None:
        key = self._clean_attribute_key(key)
        if (
            not self.any_attribute
            and not key.startswith(("data-", "aria-"))
            and key not in self.all_attributes
        ):
            warnings.warn(exc.InvalidAttributeWarning(self, key), stacklevel=3)
        elif not self._validate_attribute(key, val):
            warnings.warn(
                exc.InvalidAttributeValueWarning(self, key, str(val)), stacklevel=3
            )

        if val is False:
            return
        if val is not True and not isinstance(val, str):
            val = str(val)
        self._attributes[key] = val

    @staticmethod
    def _clean_attribute_key(key: str) -> str:
        return key.rstrip("_").replace("_", "-")

    def _validate_attribute(self, key: str, val: _T_attribute) -> bool:
        expected_value = self.all_attributes.get(key)
        if expected_value is None:
            return True
        if isinstance(expected_value, set):
            if val in expected_value:
                return True
            if {"", key} < expected_value:
                return v.attribute_bool(val)
            return False
        return expected_value(val)

    # Children
    @overload
    def add(self, child: _T_BaseElement) -> _T_BaseElement: ...

    @overload
    def add(self, child: _T_child) -> BaseElement: ...

    def add(self, child: _T_child) -> BaseElement:
        """Add a child to the current element

        Args:
            child: The child. A `TextNode` is automatically created when passing
                anything other than a subclass of `BaseElement`.

        Returns:
            The child, already converted to a `TextNode` if required.
        """
        return self._add_child(child)

    @overload
    def insert(self, idx: int, child: _T_BaseElement) -> _T_BaseElement: ...

    @overload
    def insert(self, idx: int, child: _T_child) -> BaseElement: ...

    def insert(self, idx: int, child: _T_child) -> BaseElement:
        """Insert a child before the index specified

        Args:
            idx: The index.
            child: The child. A `TextNode` is automatically created when passing
                anything other than a subclass of `BaseElement`.

        Returns:
            The child, already converted to a `TextNode` if required.
        """
        return self._add_child(child, idx=idx)

    def _add_child(
        self,
        child: _T_child,
        *,
        idx: int | None = None,
        idx_replace: bool = False,
        exit_context_manager: bool = False,
    ) -> BaseElement:
        if not isinstance(child, BaseElement):
            child = TextNode(child)
        if idx is None:
            self._children.append(child)
        elif idx_replace:
            self._children[idx] = child
        else:
            self._children.insert(idx, child)
        if not exit_context_manager:
            self._remove_from_stack(child)
        return child

    # Render
    def _render(self) -> list[str]:
        if type(self) is BaseElement:
            return [str(child) for child in self._children]

        data = []
        if self._prepend_doctype:
            data.append("<!DOCTYPE html>")
        attrs = []
        for key, val in self._attributes.items():
            if val is True:
                attrs.append(f" {key}")
            else:
                attrs.append(f' {key}="{escape(val, True)}"')

        data.append(f"<{self.name}{''.join(attrs)}>")
        if not self.is_empty:
            data.extend(str(child) for child in self._children)
            data.append(f"</{self.name}>")

        return data

    # Dunder methods
    @overload
    def __getitem__(self, key: str) -> str | bool: ...

    @overload
    def __getitem__(self, key: int) -> BaseElement: ...

    @overload
    def __getitem__(
        self, key: slice[int | None, int | None, int | None]
    ) -> list[BaseElement]: ...

    def __getitem__(
        self, key: str | int | slice[int | None, int | None, int | None]
    ) -> str | bool | BaseElement | list[BaseElement]:
        if isinstance(key, str):
            return self._attributes.get(key, False)
        return self._children[key]

    @overload
    def __setitem__(self, key: str, val: _T_attribute) -> None: ...

    @overload
    def __setitem__(self, key: int, val: _T_child) -> None: ...

    @overload
    def __setitem__(
        self, key: slice[int | None, int | None, int | None], val: Iterable[_T_child]
    ) -> None: ...

    def __setitem__(
        self,
        key: str | int | slice[int | None, int | None, int | None],
        val: _T_attribute | _T_child | Iterable[_T_child],
    ) -> None:
        if isinstance(key, str):
            val = cast("_T_attribute", val)
            self._set_attribute(key, val)
        elif isinstance(key, int):
            val = cast("_T_child", val)
            self._add_child(val, idx=key, idx_replace=True)
        else:
            val = cast("Iterable[_T_child]", val)
            children = [
                TextNode(child) if not isinstance(child, BaseElement) else child
                for child in val
            ]
            self._children[key] = children
            for child in children:
                self._remove_from_stack(child)

    def __delitem__(
        self, key: str | int | slice[int | None, int | None, int | None]
    ) -> None:
        if isinstance(key, str):
            del self._attributes[key]
        else:
            del self._children[key]

    def __add__(self, other: _T_child) -> BaseElement:
        return BaseElement(self, other)

    def __radd__(self, other: _T_child) -> BaseElement:
        return BaseElement(other, self)

    def __enter__(self: _T_BaseElement) -> _T_BaseElement:
        self._stack.append([])
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        for child in self._stack.pop():
            self._add_child(child, exit_context_manager=True)
        self._maybe_clear_stack()

    def __len__(self) -> int:
        return len(self._children)  # pragma: no cover

    def __iter__(self) -> Iterator[BaseElement]:
        return self._children.__iter__()  # pragma: no cover

    def __bool__(self) -> bool:
        return True  # pragma: no cover

    def __str__(self) -> str:
        return "".join(self._render())


class TextNode(BaseElement):
    """Class representing a text node"""

    def __init__(self, text: str | float) -> None:
        """
        Args:
            text: The content of the text node.
        """
        if not isinstance(text, str):
            text = str(text)
        self.text = text

        super().__init__()

    def _render(self) -> list[str]:
        return [escape(self.text)]


class RawTextNode(TextNode):
    """Class representing a text node, without escaping the content"""

    def _render(self) -> list[str]:
        return [self.text]
