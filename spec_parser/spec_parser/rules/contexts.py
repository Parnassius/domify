from bs4.element import Tag

from spec_parser import util


def parse(element: str, x: Tag, page: str, el: str) -> list[str]:
    soup = util.request_cache(page)

    value_rules = []

    for dd in soup.find(id=f"{el}:concept-element-contexts").parent.next_siblings:
        if dd.name != "dd":
            break

        contents = []
        for part in dd.contents:
            if isinstance(part, str):
                contents.append(part.strip())
            else:
                tag_string = part.string
                if tag_string:
                    tag_string = tag_string.strip()
                contents.append((part, tag_string))

        match contents:
            case [
                "After",
                _,
                "or",
                _,
                "elements inside",
                (Tag(contents=[Tag() as context]), _),
                "elements.",
            ]:
                # TODO: siblings
                if context["href"] == x["href"]:
                    pass
            case [
                "After",
                _,
                "or",
                _,
                "elements inside",
                (Tag(contents=[Tag() as context]), _),
                "elements that are children of a",
                _,
                "element.",
            ]:
                # TODO: siblings and child of child
                if context["href"] == x["href"]:
                    pass
            case [
                "As a child of a",
                (Tag(contents=[Tag() as context]), _),
                "element that doesn't have a",
                (_, attribute),
                "attribute.",
            ]:
                # TODO: parent attribute
                if context["href"] == x["href"]:
                    pass
            case [
                "Before",
                _,
                "or",
                _,
                "elements inside",
                (Tag(contents=[Tag() as context]), _),
                "elements.",
            ]:
                # TODO: siblings
                if context["href"] == x["href"]:
                    pass
            case [
                "Before",
                _,
                "or",
                _,
                "elements inside",
                (Tag(contents=[Tag() as context]), _),
                "elements that are children of a",
                _,
                "element.",
            ]:
                # TODO: siblings and child of child
                if context["href"] == x["href"]:
                    pass
            case [
                "In a",
                (Tag(contents=[Tag() as context]), _),
                "element of an",
                (_, "HTML document"),
                ", if there are no ancestor",
                _,
                "elements.",
            ]:
                # TODO: ancestor
                if context["href"] == x["href"]:
                    pass
            case [
                "In a",
                (Tag(contents=[Tag() as context]), _),
                "element that is a child of a",
                _,
                "element.",
            ]:
                # TODO: child of child
                if context["href"] == x["href"]:
                    pass
            case [
                "If the",
                (_, attribute),
                "attribute is present, or if the element's",
                (_, "http-equiv"),
                "attribute is in the",
                (_, "Encoding declaration state"),
                ": in a",
                (Tag(contents=[Tag() as context]), _),
                "element.",
            ]:
                if context["href"] == x["href"]:
                    value_rules.append(
                        f"x['{attribute}'] is not False or v.attribute_encoding_declaration_state(x['content'])"
                    )
            case [
                "If the",
                (_, attribute),
                "attribute is present: where",
                (context, _),
                "is expected.",
            ]:
                if context["href"] == x["href"]:
                    value_rules.append(f"x['{attribute}'] is not False")
            case [
                "If the",
                (_, "http-equiv"),
                "attribute is present but not in the",
                (_, "Encoding declaration state"),
                ": in a",
                (Tag(contents=[Tag() as context]), _),
                "element.",
            ]:
                if context["href"] == x["href"]:
                    value_rules.append(
                        "x['http-equiv'] is not False and not v.attribute_encoding_declaration_state(x['content'])"
                    )
            case [
                "If the",
                (_, "http-equiv"),
                "attribute is present but not in the",
                (_, "Encoding declaration state"),
                ": in a",
                (Tag(contents=[Tag() as context]), _),
                "element that is a child of a",
                _,
                "element.",
            ]:
                # TODO: child of child
                if context["href"] == x["href"]:
                    value_rules.append(
                        "x['http-equiv'] is not False and not v.attribute_encoding_declaration_state(x['content'])"
                    )
            case [
                "If the element is",
                (_, "allowed in the body"),
                ": where",
                (context, _),
                "is expected.",
            ]:
                assert element.string == "link"
                if context["href"] == x["href"]:
                    value_rules.append(
                        "x['itemprop'] is not False or "
                        + "(isinstance(x['rel'], str) and set(x['rel'].lower().split()) <= {"
                        + ",".join(f"'{x}'" for x in util.get_link_body_ok_keywords())
                        + "})"
                    )
            case ["Inside", (Tag(contents=[Tag() as context]), _), "elements."]:
                if context["href"] == x["href"]:
                    pass
            case ["Where", (context, _), "are expected."]:
                if context["href"] == x["href"]:
                    pass
            case ["Where", (context, _), "is expected."]:
                if context["href"] == x["href"]:
                    pass
            case [
                "Where",
                (context, _),
                "is expected, but only if it is a",
                (Tag(contents=[a, _, b]), _),
                ".",
            ] if a.strip() == "hierarchically correct" and b.strip() == "element":
                if context["href"] == x["href"]:
                    assert element == "main"
            case [
                "Where",
                (context, _),
                "is expected, but only if there is a",
                _,
                "element ancestor.",
            ]:
                # TODO: ancestor
                if context["href"] == x["href"]:
                    assert element == "area"
            case [
                "Where",
                (context, _),
                "is expected in",
                (_, "HTML documents"),
                ", if there are no ancestor",
                _,
                "elements.",
            ]:
                # TODO: ancestor
                if context["href"] == x["href"]:
                    assert element == "noscript"
            case _:
                print("Unhandled context rule:", element)

    return value_rules
