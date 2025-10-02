from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from spec_parser import rules, util
from spec_parser.file_writer import FileWriter


@dataclass
class ElementData:
    description: str = ""
    is_empty: bool = False
    global_attributes: bool = False
    element_attributes: dict[str, str | None] = field(default_factory=dict)
    any_attribute: bool = False


class Parser:
    def __init__(self) -> None:
        self._elements: dict[str, ElementData] = {}
        self._global_attributes: dict[str, str | None] = {}

        self._get_elements()
        self._get_attributes()

        self._write_data()

    def _get_elements(self) -> None:
        soup = util.request_cache("indices")

        title = soup.find("h3", id=re.compile(r"^elements"))
        assert title is not None
        table = title.find_next_sibling("table")
        assert table is not None
        for row in table.select(":scope > tbody > tr"):
            for element in row.select(":scope > th code"):
                if element.text in ("math", "svg"):
                    continue
                tds = row.find_all("td", recursive=False)
                element_data = ElementData()
                element_data.description = tds[0].text
                element_data.is_empty = tds[3].text == "empty"
                element_data.global_attributes = bool(
                    tds[4].find("a", string="globals")  # type: ignore[call-overload]
                )
                element_data.any_attribute = "any" in [
                    x.strip(";* \n") for x in tds[4].find_all(string=True)
                ]
                element_data.element_attributes = {
                    x.text: None
                    for x in sorted(tds[4].find_all("code"), key=lambda x: x.text)
                }

                self._elements[element.text] = element_data

    def _get_attributes(self) -> None:
        soup = util.request_cache("indices")

        title = soup.find("h3", id=re.compile(r"^attributes"))
        assert title is not None
        attributes_table = title.find_next_sibling("table")
        assert attributes_table is not None
        event_handler_table = attributes_table.find_next_sibling("table")
        assert event_handler_table is not None
        for table in (attributes_table, event_handler_table):
            for row in table.select(":scope > tbody > tr"):
                for attribute in row.select(":scope > th code"):
                    tds = row.find_all("td", recursive=False)
                    value = rules.attributes.parse(tds[2])

                    if tds[0].find("a", string="HTML elements"):  # type: ignore[call-overload]
                        self._global_attributes[attribute.text] = value
                    else:
                        for element in tds[0].find_all("code"):
                            attributes = self._elements[element.text].element_attributes
                            if attribute.text not in attributes:
                                if self._global_attributes.get(attribute.text) == value:
                                    continue
                                if element.text == "picture" and attribute.text in (
                                    "height",
                                    "width",
                                ):
                                    continue

                                if element.text == "bdo" and attribute.text == "dir":
                                    # Global attribute with different semantics
                                    pass
                                elif (
                                    element.text == "dialog"
                                    and attribute.text == "closedby"
                                ):
                                    pass
                                else:
                                    print(
                                        f"Missing attribute {attribute.text} "
                                        f"in {element.text}"
                                    )
                                    sys.exit(1)

                            attributes[attribute.text] = value

    def _write_data(self) -> None:
        f = FileWriter(
            Path(__file__).parent.parent.parent.parent
            / "src"
            / "domify"
            / "html_elements.py"
        )
        f.add_class(
            "HtmlElement",
            "Base class for html elements, contains global attributes.",
            global_attributes=(self._global_attributes, "_T_attributes_dict", False),
        )
        for element_name, element_data in self._elements.items():
            if not element_data.global_attributes:
                print(f"Element without global attributes: {element_name}")
                sys.exit(1)
            f.add_class(
                element_name.capitalize(),
                element_data.description,
                is_empty=(element_data.is_empty, False),
                element_attributes=(
                    element_data.element_attributes,
                    "_T_attributes_dict",
                    False,
                ),
                any_attribute=(element_data.any_attribute, False),
                _default_prepend_doctype=(element_name == "html", False),
            )
        f.write()


def parse() -> None:
    Parser()
