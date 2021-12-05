from bs4.element import Tag

from spec_parser import util


def parse(element: Tag) -> str | None:
    siblings = []
    for part in element.next_siblings:
        if isinstance(part, str):
            siblings.append(part.strip().rstrip(";"))
        else:
            tag_string = part.string
            if tag_string:
                tag_string = tag_string.strip()
            siblings.append((part, tag_string))

    value: str | None = None
    match siblings:
        case ["(if it is a descendant of a", _, "element)", *_]:
            # TODO: descendant
            pass
        case ["(if the", (_, attribute), "attribute is present)", *_]:
            value = f"x['{attribute}'] is not False"
        case [
            "(if the",
            (_, attribute),
            "attribute is",
            (_, "not"),
            "in the",
            (_, state),
            "state)",
            *_,
        ]:
            value = f"x['{attribute}'] != '{state.lower()}'"
        case [
            "(if the element's children include at least one",
            (_, child),
            "element)",
            *_,
        ]:
            value = f"'{child}' in (child.name for child in x)"
        case ["(if the element's children include at least one name-value group)", *_]:
            assert element.string == "dl"
            value = (
                "("
                " 'dt' in (child.name for child in x) "
                " or 'dt' in (child.name for child in itertools.chain(*(div for div in x if div.name == 'div'))) "
                ") and ("
                " 'dd' in (child.name for child in x) "
                " or 'dd' in (child.name for child in itertools.chain(*(div for div in x if div.name == 'div'))) "
                ")"
            )
        case ["(if it is", (_, "allowed in the body"), ")", *_]:
            assert element.string == "link"
            value = (
                "x['itemprop'] is not False or "
                + "(isinstance(x['rel'], str) and set(x['rel'].lower().split()) <= {"
                + ",".join(f"'{x}'" for x in util.get_link_body_ok_keywords())
                + "})"
            )
        case [
            "(if it is a",
            (Tag(contents=[a, _, b, *_]), _),
            ")",
            *_,
        ] if a.strip() == "hierarchically correct" and b.strip() == "element":
            assert element.string == "main"
        case _:
            print("Unhandled category rule:", element.string)

    return value
