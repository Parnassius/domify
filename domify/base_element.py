import sys
import warnings
from contextvars import ContextVar
from html import escape
from types import TracebackType
from typing import (
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Set,
    Type,
    TypeVar,
    Union,
    cast,
    overload,
)

from . import exc

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


_T_BaseElement = TypeVar("_T_BaseElement", bound="BaseElement")
_T_attribute = Union[str, float, bool]
_T_child = Union["BaseElement", str, float]
_T_attributes_dict = Dict[str, Union[Set[str], Callable[[_T_attribute], bool]]]


class BaseElement:
    """Base class representing an element"""

    is_empty = False
    global_attributes: _T_attributes_dict = {}
    element_attributes: _T_attributes_dict = {}
    any_attribute = False

    _stack_var: ContextVar[Optional[List[List["BaseElement"]]]] = ContextVar(
        "stack", default=None
    )

    def __init__(self, *args: _T_child, **kwargs: Optional[_T_attribute]) -> None:
        """
        Args:
            *args: The element's children. A `TextNode` is automatically created when
                passing anything other than a subclass of `BaseElement`.
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
            raise exc.EmptyElementChildrenError()

        self.attributes: Dict[str, Union[str, Literal[True]]] = {}
        self.children: List["BaseElement"] = []

        self._add_to_stack(self)

        for child in args:
            self._add_child(child)

        for key, val in kwargs.items():
            if val is None:
                continue
            self._set_attribute(key, val)

    @property
    def _stack(self) -> List[List["BaseElement"]]:
        stack = self._stack_var.get()
        if stack is None:
            stack = []
            self._stack_var.set(stack)
        return stack

    def _add_to_stack(self, element: "BaseElement") -> None:
        if self._stack:
            self._stack[-1].append(element)

    def _remove_from_stack(self, element: "BaseElement") -> None:
        if self._stack:
            self._stack[-1].remove(element)
        self._maybe_clear_stack()

    def _maybe_clear_stack(self) -> None:
        if not self._stack:
            self._stack_var.set(None)

    # Attributes
    def get_classes(self) -> List[str]:
        """Get the current element's classes

        Returns:
            The current element's classes as a list of strings.
        """
        classes = self.attributes.get("class", True)
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
        self.attributes["class"] = " ".join(classes)

    def remove_class(self, *args: str) -> None:
        """Remove one or more classes from the the current element

        Args:
            args: The class (or classes) to remove.
        """
        classes = self.get_classes()
        for cls in args:
            classes.remove(cls)
        self.attributes["class"] = " ".join(classes)

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
        self.attributes[key] = val

    @staticmethod
    def _clean_attribute_key(key: str) -> str:
        return key.rstrip("_").replace("_", "-")

    def _validate_attribute(self, key: str, val: _T_attribute) -> bool:
        expected_value = self.all_attributes.get(key)
        if expected_value is None:
            return True
        if isinstance(expected_value, set):
            return val in expected_value
        return expected_value(val)

    # Children
    @overload
    def add(self, child: _T_BaseElement) -> _T_BaseElement:
        ...

    @overload
    def add(self, child: _T_child) -> "BaseElement":
        ...

    def add(self, child: _T_child) -> "BaseElement":
        """Add a child to the current element

        Args:
            child: The child. A `TextNode` is automatically created when passing
                anything other than a subclass of `BaseElement`.

        Returns:
            The child, already converted to a `TextNode` if required.
        """
        return self._add_child(child)

    def _add_child(
        self,
        child: _T_child,
        *,
        idx: Optional[int] = None,
        exit_context_manager: bool = False,
    ) -> "BaseElement":
        if not isinstance(child, BaseElement):
            child = TextNode(child)
        if idx is None:
            self.children.append(child)
        else:
            self.children[idx] = child
        if not exit_context_manager:
            self._remove_from_stack(child)
        return child

    # Render
    def _render(self) -> List[str]:
        data = []
        name = type(self).__name__.rstrip("_").lower()
        attrs = []
        for key, val in self.attributes.items():
            if val is True:
                attrs.append(f" {key}")
            else:
                attrs.append(f' {key}="{escape(val, True)}"')

        data.append(f"<{name}{''.join(attrs)}>")
        if not self.is_empty:
            for child in self.children:
                data.append(str(child))
            data.append(f"</{name}>")

        return data

    # Dunder methods
    @overload
    def __getitem__(self, key: str) -> Union[str, bool]:
        ...

    @overload
    def __getitem__(self, key: int) -> "BaseElement":
        ...

    def __getitem__(
        self, key: Union[str, int]
    ) -> Union[Union[str, bool], "BaseElement"]:
        if isinstance(key, str):
            return self.attributes.get(key, False)
        return self.children[key]

    @overload
    def __setitem__(self, key: str, val: _T_attribute) -> None:
        ...

    @overload
    def __setitem__(self, key: int, val: _T_child) -> None:
        ...

    def __setitem__(
        self, key: Union[str, int], val: Union[_T_attribute, _T_child]
    ) -> None:
        if isinstance(key, str):
            val = cast(_T_attribute, val)
            self._set_attribute(key, val)
        else:
            self._add_child(val, idx=key)

    def __delitem__(self, key: Union[str, int]) -> None:
        if isinstance(key, str):
            del self.attributes[key]
        else:
            del self.children[key]

    def __add__(self, other: _T_child) -> "BaseElement":
        return _FakeContainerElement(self, other)

    def __radd__(self, other: _T_child) -> "BaseElement":
        return _FakeContainerElement(other, self)

    def __enter__(self: _T_BaseElement) -> _T_BaseElement:
        self._stack.append([])
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        for child in self._stack.pop():
            self._add_child(child, exit_context_manager=True)
        self._maybe_clear_stack()

    def __len__(self) -> int:
        return len(self.children)  # pragma: no cover

    def __iter__(self) -> Iterator["BaseElement"]:
        return self.children.__iter__()  # pragma: no cover

    def __bool__(self) -> bool:
        return True  # pragma: no cover

    def __str__(self) -> str:
        return "".join(self._render())


class _FakeContainerElement(BaseElement):
    def _render(self) -> List[str]:
        return [str(child) for child in self.children]


class TextNode(BaseElement):
    """Class representing a text node"""

    def __init__(self, text: Union[str, float]) -> None:
        """
        Args:
            text: The content of the text node.
        """
        if not isinstance(text, str):
            text = str(text)
        self.text = text

        super().__init__()

    def _render(self) -> List[str]:
        return [escape(self.text)]


class RawTextNode(TextNode):
    """Class representing a text node, without escaping the content"""

    def _render(self) -> List[str]:
        return [self.text]
