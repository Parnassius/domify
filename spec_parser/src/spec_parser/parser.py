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
        table = title.find_next_sibling("table")
        for row in table.find("tbody").children:
            for element in row.contents[0].find_all("code"):
                if element.string in ("math", "svg"):
                    continue
                element_data = ElementData()
                element_data.description = row.contents[1].text
                element_data.is_empty = row.contents[4].string == "empty"
                element_data.global_attributes = bool(
                    row.contents[5].find("a", string="globals")
                )
                element_data.any_attribute = "any" in [
                    x.strip(";* \n")
                    for x in row.contents[5].contents
                    if isinstance(x, str)
                ]
                element_data.element_attributes = {
                    x.string: None
                    for x in sorted(
                        row.contents[5].find_all("code"), key=lambda x: x.string
                    )
                }

                self._elements[element.string] = element_data

    def _get_attributes(self) -> None:
        soup = util.request_cache("indices")

        title = soup.find("h3", id=re.compile(r"^attributes"))
        tables = [title.find_next_sibling("table")]
        tables.append(tables[0].find_next_sibling("table"))  # event handlers
        for table in tables:
            for row in table.find("tbody").children:
                attribute = row.contents[0].find("code").string
                value = rules.attributes.parse(row.contents[3])

                if row.contents[1].find("a", string="HTML elements"):
                    self._global_attributes[attribute] = value
                else:
                    for element in row.contents[1].find_all("code"):
                        attributes = self._elements[element.string].element_attributes
                        if attribute not in attributes:
                            if self._global_attributes.get(attribute) == value:
                                continue
                            if element.string == "picture" and attribute in (
                                "height",
                                "width",
                            ):
                                continue

                            if element.string == "template" and attribute in (
                                "shadowrootmode",
                                "shadowrootdelegatesfocus",
                                "shadowrootclonable",
                            ):
                                pass
                            elif (
                                element.string == "body" and attribute == "onpagereveal"
                            ):
                                pass
                            elif element.string == "bdo" and attribute == "dir":
                                # Global attribute with different semantics
                                pass
                            else:
                                print(
                                    f"Missing attribute {attribute} in {element.string}"
                                )
                                sys.exit(1)

                        attributes[attribute] = value

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
