from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base_element import BaseElement


class EmptyElementChildrenError(Exception):
    """Trying to add a children to a empty element"""


class InvalidAttributeWarning(UserWarning):
    """Invalid element attribute"""

    def __init__(self, element: "BaseElement", attribute: str) -> None:
        self.element = type(element).__name__
        self.attribute = attribute
        super().__init__(
            f"Attribute `{self.attribute}` not allowed on element `{self.element}`"
        )


class InvalidAttributeValueWarning(UserWarning):
    """Invalid attribute value"""

    def __init__(self, element: "BaseElement", attribute: str, value: str) -> None:
        self.element = type(element).__name__
        self.attribute = attribute
        self.value = value
        super().__init__(
            f"Bad value `{self.value}` "
            f"for attribute `{self.attribute}` "
            f"on element `{self.element}'"
        )
