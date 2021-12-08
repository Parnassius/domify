import re
from dataclasses import dataclass, field
from os.path import dirname, join
from typing import Dict, List

import requests
from bs4 import BeautifulSoup  # type: ignore[import]

from .file_writer import FileWriter


@dataclass
class ElementData:
    description: str = ""
    is_empty: bool = False
    global_attributes: bool = False
    element_attributes: Dict[str, str] = field(default_factory=dict)
    any_attribute: bool = False


class Parser:
    SPEC_URL = "https://html.spec.whatwg.org/"

    def __init__(self) -> None:
        html = requests.get(f"{self.SPEC_URL}multipage/indices.html").text
        self.soup = BeautifulSoup(html, "html5lib")

        self._elements: Dict[str, ElementData] = {}
        self._global_attributes: Dict[str, str] = {}

        self._get_elements()
        self._get_attributes()

        self._write_data()

    def _get_elements(self) -> None:
        title = self.soup.find("h3", id=re.compile(r"^elements"))
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

    def _get_input_type_keywords(self) -> List[str]:
        html = requests.get(f"{self.SPEC_URL}multipage/input.html").text
        soup = BeautifulSoup(html, "html5lib")

        table = soup.find(id="attr-input-type-keywords")
        keywords = [
            row.contents[0].find("code").string for row in table.find("tbody").children
        ]
        return keywords

    def _get_attributes(self) -> None:
        title = self.soup.find("h3", id=re.compile(r"^attributes"))
        tables = [title.find_next_sibling("table")]
        tables.append(tables[0].find_next_sibling("table"))  # event handlers
        for table in tables:
            for row in table.find("tbody").children:
                attribute = row.contents[0].find("code").string
                value_ = row.contents[3]
                value = "''"
                if value_.text.strip() == "Boolean attribute":
                    value = "v.bool_validator"
                elif value_.text.strip() == "Valid integer":
                    value = "v.int_validator"
                elif value_.text.strip() == "Valid non-negative integer":
                    value = "v.int_ge_zero_validator"
                elif (
                    value_.text.strip()
                    == "Valid non-negative integer greater than zero"
                ):
                    value = "v.int_gt_zero_validator"
                elif value_.text.strip() in (
                    "Valid floating-point number",
                    "Valid floating-point number*",
                ):
                    value = "v.float_validator"
                elif value_.text.strip() in (
                    "Unordered set of unique space-separated tokens*",
                    "Unordered set of unique space-separated tokens consisting of IDs*",  # TODO
                    "Unordered set of unique space-separated tokens consisting of valid absolute URLs*",  # TODO
                    "Unordered set of unique space-separated tokens consisting of valid absolute URLs, defined property names, or text*",  # TODO
                ):
                    value = "v.unique_set_validator"
                elif (
                    value_.text.strip()
                    == "Ordered set of unique space-separated tokens, none of which are identical to another, each consisting of one code point in length"
                ):
                    value = "lambda x: v.unique_set_validator(x) and max(len(t) for t in str(x).split()) <= 1"
                elif (
                    value_.text.strip()
                    == 'Valid floating-point number greater than zero, or "any"'
                ):
                    value = "lambda x: v.float_gt_zero_validator(x) or x in {'any'}"
                elif value_.text.strip() == 'ASCII case-insensitive match for "UTF-8"':
                    value = "lambda x: str(x).upper() == 'UTF-8'"
                elif (
                    value_.text.strip()
                    == 'Unordered set of unique space-separated tokens, ASCII case-insensitive, consisting of\n          "allow-forms",\n          "allow-modals",\n          "allow-orientation-lock",\n          "allow-pointer-lock",\n          "allow-popups",\n          "allow-popups-to-escape-sandbox",\n          "allow-presentation",\n          "allow-same-origin",\n          "allow-scripts" and\n          "allow-top-navigation"'
                ):
                    possible_values = value_.find_all("code")
                    value = (
                        "lambda x: v.unique_set_validator(str(x).lower()) and set(str(x).lower().split()) <= {"
                        + ",".join(f"'{x.text}'" for x in possible_values)
                        + "}"
                    )
                elif value_.text.strip() in (
                    '"module"; a valid MIME type string that is not a JavaScript MIME type essence match',
                    "Autofill field name and related tokens*",
                    "Comma-separated list of image candidate strings",
                    "CSS <color>",
                    "CSS declarations*",
                    "Event handler content attribute",
                    "ID*",
                    'Potential destination, for rel="preload"; script-like destination, for rel="modulepreload"',
                    "Regular expression matching the JavaScript Pattern production",
                    "Referrer policy",
                    "Serialized permissions policy",
                    "Set of comma-separated tokens* consisting of valid MIME type strings with no parameters or audio/*, video/*, or image/*",
                    "Set of space-separated tokens",
                    "Set of space-separated tokens consisting of valid non-empty URLs",
                    "Text",
                    "Text*",
                    "The source of an iframe srcdoc document*",
                    "Unordered set of unique space-separated tokens, ASCII case-insensitive, consisting of sizes*",
                    "Valid BCP 47 language tag",
                    "Valid BCP 47 language tag or the empty string",
                    "Valid browsing context name or keyword",
                    "Valid custom element name of a defined customized built-in element",
                    "Valid date string with optional time",
                    "Valid hash-name reference*",
                    "Valid list of floating-point numbers*",
                    "Valid media query list",
                    "Valid MIME type string",
                    "Valid month string,\n          valid date string,\n          valid yearless date string,\n          valid time string,\n          valid local date and time string,\n          valid time-zone offset string,\n          valid global date and time string,\n          valid week string,\n          valid non-negative integer, or\n          valid duration string",
                    "Valid non-empty URL potentially surrounded by spaces",
                    "Valid source size list",
                    "Valid URL potentially surrounded by spaces",
                    "Varies*",
                ):
                    value = "v.str_validator"
                elif value_.text.strip() == "input type keyword":
                    value = (
                        "{"
                        + ",".join(f"'{x}'" for x in self._get_input_type_keywords())
                        + "}"
                    )
                elif not any(x for x in value_.children if x.name == "a") and (
                    possible_values := value_.find_all("code")
                ):
                    value = "{" + ",".join(f"'{x.text}'" for x in possible_values) + "}"
                else:
                    raise Exception("Unhandled attribute value")

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
