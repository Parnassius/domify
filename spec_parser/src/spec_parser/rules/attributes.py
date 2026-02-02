# ruff: noqa: E501

from __future__ import annotations

import re
import sys

from bs4.element import Tag

from spec_parser import util


def parse(content: Tag) -> str:
    content_text = content.text.strip()
    value: str
    possible_values: list[str]

    if content_text == "Boolean attribute":
        value = "v.attribute_bool"
    elif content_text == "Valid integer":
        value = "v.attribute_int"
    elif content_text == "Valid non-negative integer":
        value = "v.attribute_int_ge_zero"
    elif content_text == "Valid non-negative integer greater than zero":
        value = "v.attribute_int_gt_zero"
    elif match := re.fullmatch(
        r"Valid non-negative integer between (\d+) and (\d+)", content_text, re.ASCII
    ):
        value = f"partial(v.attribute_int, ge={match[1]}, le={match[2]})"
    elif content_text in (
        "Valid floating-point number",
        "Valid floating-point number*",
    ):
        value = "v.attribute_float"
    elif (
        content_text
        in (
            "Unordered set of unique space-separated tokens*",
            "Unordered set of unique space-separated tokens consisting of IDs*",  # TODO
            "Unordered set of unique space-separated tokens consisting of valid absolute URLs*",  # TODO
            "Unordered set of unique space-separated tokens consisting of valid absolute URLs, defined property names, or text*",  # TODO
        )
    ):
        value = "v.attribute_unique_set"
    elif (
        content_text
        == "Ordered set of unique space-separated tokens, none of which are identical to another, each consisting of one code point in length"
    ):
        value = "v.attribute_all(v.attribute_unique_set, lambda x: max(len(t) for t in str(x).split()) <= 1)"
    elif content_text == 'Valid floating-point number greater than zero, or "any"':
        value = (
            "v.attribute_any(v.attribute_float_gt_zero, v.attribute_str_literal('any'))"
        )
    elif content_text == 'ASCII case-insensitive match for "UTF-8"':
        value = "v.attribute_str_literal_ci('utf-8')"
    elif content_text.startswith(
        "Unordered set of unique space-separated tokens, ASCII case-insensitive, consisting of\n"
    ):
        possible_values = [x.text for x in content.find_all("code")]
        value = (
            "v.attribute_unique_set_literal_ci("
            + ",".join(f"'{x.lower()}'" for x in possible_values)
            + ")"
        )
    elif content_text in (
        '"module"; "importmap"; "speculationrules"; a valid MIME type string that is not a JavaScript MIME type essence match',
        "Autofill field name and related tokens*",
        "Comma-separated list of image candidate strings",
        "CSS <color>",
        "CSS declarations*",
        "Event handler content attribute",
        "ID of the element to toggle, show or, hide",
        "ID*",
        'Preload destination, for rel="preload"; module preload destination, for rel="modulepreload"',
        "Regular expression matching the JavaScript Pattern production",
        "Referrer policy",
        "Serialized permissions policy",
        "Set of comma-separated tokens* consisting of valid MIME type strings with no parameters or audio/*, video/*, or image/*",
        "Set of space-separated tokens",
        "Set of space-separated tokens consisting of valid non-empty URLs",
        "Text",
        "Text*",
        "The source of an iframe srcdoc document*",
        '"toggle-popover";\n          "show-popover";\n          "hide-popover";\n          "close";\n          "request-close";\n          "show-modal";\n          a custom command keyword',
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
        "Valid navigable target name or keyword",
        "Valid non-empty URL potentially surrounded by spaces",
        "Valid source size list",
        "Valid URL potentially surrounded by spaces",
        "Varies*",
    ):
        value = "v.attribute_str"
    elif content_text == "input type keyword":
        value = "{" + ",".join(f"'{x}'" for x in util.get_input_type_keywords()) + "}"
    elif not any(content.find_all("a", recursive=False)) and (
        possible_code_values := content.find_all("code")
    ):
        possible_values = [x.text for x in possible_code_values]
        possible_string_values = (
            x.strip('";\n ') for x in content.find_all(string=True, recursive=False)
        )
        if "the empty string" in possible_string_values:
            possible_values.append("")
        value = "{" + ",".join(f"'{x}'" for x in possible_values) + "}"
    else:
        value = "v.attribute_str"
        print(f"Unhandled attribute value: {content_text}")
        sys.exit(1)

    return value
