from bs4.element import Tag  # type: ignore[import]

from spec_parser import util


def parse(content: Tag) -> str:
    content_text = content.text.strip()
    value: str

    if content_text == "Boolean attribute":
        value = "v.bool_validator"
    elif content_text == "Valid integer":
        value = "v.int_validator"
    elif content_text == "Valid non-negative integer":
        value = "v.int_ge_zero_validator"
    elif content_text == "Valid non-negative integer greater than zero":
        value = "v.int_gt_zero_validator"
    elif content_text in (
        "Valid floating-point number",
        "Valid floating-point number*",
    ):
        value = "v.float_validator"
    elif content_text in (
        "Unordered set of unique space-separated tokens*",
        "Unordered set of unique space-separated tokens consisting of IDs*",  # TODO
        "Unordered set of unique space-separated tokens consisting of valid absolute URLs*",  # TODO
        "Unordered set of unique space-separated tokens consisting of valid absolute URLs, defined property names, or text*",  # TODO
    ):
        value = "v.unique_set_validator"
    elif (
        content_text
        == "Ordered set of unique space-separated tokens, none of which are identical to another, each consisting of one code point in length"
    ):
        value = "lambda x: v.unique_set_validator(x) and max(len(t) for t in str(x).split()) <= 1"
    elif content_text == 'Valid floating-point number greater than zero, or "any"':
        value = "lambda x: v.float_gt_zero_validator(x) or x in {'any'}"
    elif content_text == 'ASCII case-insensitive match for "UTF-8"':
        value = "lambda x: str(x).upper() == 'UTF-8'"
    elif (
        content_text
        == 'Unordered set of unique space-separated tokens, ASCII case-insensitive, consisting of\n          "allow-forms",\n          "allow-modals",\n          "allow-orientation-lock",\n          "allow-pointer-lock",\n          "allow-popups",\n          "allow-popups-to-escape-sandbox",\n          "allow-presentation",\n          "allow-same-origin",\n          "allow-scripts" and\n          "allow-top-navigation"'
    ):
        possible_values = content.find_all("code")
        value = (
            "lambda x: v.unique_set_validator(str(x).lower()) and set(str(x).lower().split()) <= {"
            + ",".join(f"'{x.text}'" for x in possible_values)
            + "}"
        )
    elif content_text in (
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
    elif content_text == "input type keyword":
        value = "{" + ",".join(f"'{x}'" for x in util.get_input_type_keywords()) + "}"
    elif not any(x for x in content.children if x.name == "a") and (
        possible_values := content.find_all("code")
    ):
        value = "{" + ",".join(f"'{x.text}'" for x in possible_values) + "}"
    else:
        value = "v.str_validator"
        print("Unhandled attribute value:", content_text)

    return value
