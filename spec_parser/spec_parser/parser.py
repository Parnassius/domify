import re
from dataclasses import dataclass, field
from os.path import dirname, join
from typing import Dict

from . import rules, util
from .file_writer import FileWriter


@dataclass
class ElementData:
    description: str = ""
    is_empty: bool = False
    global_attributes: bool = False
    element_attributes: Dict[str, str] = field(default_factory=dict)
    any_attribute: bool = False


class Parser:
    def __init__(self) -> None:
        self._elements: Dict[str, ElementData] = {}
        self._global_attributes: Dict[str, str] = {}

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
                        if element["id"].endswith("-element"):
                            continue
                        if self._global_attributes.get(attribute) == value:
                            continue
                        self._elements[element.string].element_attributes[
                            attribute
                        ] = value

    def _write_data(self) -> None:
        f = FileWriter(
            join(dirname(__file__), "..", "..", "domify", "html_elements.py")
        )
        f.add_class(
            "HtmlElement",
            "Base class for html elements, contains global attributes.",
            global_attributes=(self._global_attributes, "_T_attributes_dict", False),
        )
        for element_name, element_data in self._elements.items():
            if not element_data.global_attributes:
                raise Exception(f"Element without global attributes: {element_name}")
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
