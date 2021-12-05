# pylint: disable=too-many-lines

import itertools

from . import validators as v
from .base_element import BaseElement
from .base_element import RawTextNode as RawTextNode  # pylint: disable=unused-import
from .base_element import TextNode as TextNode  # pylint: disable=unused-import
from .base_element import _T_categories_dict, _T_contexts_dict

# begin automatic


class HtmlElement(BaseElement):
    """
    Base class for html elements, contains global attributes.
    """

    global_attributes = {
        "accesskey": v.attribute_all(
            v.attribute_unique_set, lambda x: max(len(t) for t in str(x).split()) <= 1
        ),
        "autocapitalize": {"on", "off", "none", "sentences", "words", "characters"},
        "autofocus": v.attribute_bool,
        "class": v.attribute_str,
        "contenteditable": {"true", "false"},
        "dir": {"ltr", "rtl", "auto"},
        "draggable": {"true", "false"},
        "enterkeyhint": {"enter", "done", "go", "next", "previous", "search", "send"},
        "hidden": v.attribute_bool,
        "id": v.attribute_str,
        "inputmode": {
            "none",
            "text",
            "tel",
            "email",
            "url",
            "numeric",
            "decimal",
            "search",
        },
        "is": v.attribute_str,
        "itemid": v.attribute_str,
        "itemprop": v.attribute_unique_set,
        "itemref": v.attribute_unique_set,
        "itemscope": v.attribute_bool,
        "itemtype": v.attribute_unique_set,
        "lang": v.attribute_str,
        "nonce": v.attribute_str,
        "slot": v.attribute_str,
        "spellcheck": {"true", "false"},
        "style": v.attribute_str,
        "tabindex": v.attribute_int,
        "title": v.attribute_str,
        "translate": {"yes", "no"},
        "onauxclick": v.attribute_str,
        "onblur": v.attribute_str,
        "oncancel": v.attribute_str,
        "oncanplay": v.attribute_str,
        "oncanplaythrough": v.attribute_str,
        "onchange": v.attribute_str,
        "onclick": v.attribute_str,
        "onclose": v.attribute_str,
        "oncontextlost": v.attribute_str,
        "oncontextmenu": v.attribute_str,
        "oncontextrestored": v.attribute_str,
        "oncopy": v.attribute_str,
        "oncuechange": v.attribute_str,
        "oncut": v.attribute_str,
        "ondblclick": v.attribute_str,
        "ondrag": v.attribute_str,
        "ondragend": v.attribute_str,
        "ondragenter": v.attribute_str,
        "ondragleave": v.attribute_str,
        "ondragover": v.attribute_str,
        "ondragstart": v.attribute_str,
        "ondrop": v.attribute_str,
        "ondurationchange": v.attribute_str,
        "onemptied": v.attribute_str,
        "onended": v.attribute_str,
        "onerror": v.attribute_str,
        "onfocus": v.attribute_str,
        "onformdata": v.attribute_str,
        "oninput": v.attribute_str,
        "oninvalid": v.attribute_str,
        "onkeydown": v.attribute_str,
        "onkeypress": v.attribute_str,
        "onkeyup": v.attribute_str,
        "onload": v.attribute_str,
        "onloadeddata": v.attribute_str,
        "onloadedmetadata": v.attribute_str,
        "onloadstart": v.attribute_str,
        "onmousedown": v.attribute_str,
        "onmouseenter": v.attribute_str,
        "onmouseleave": v.attribute_str,
        "onmousemove": v.attribute_str,
        "onmouseout": v.attribute_str,
        "onmouseover": v.attribute_str,
        "onmouseup": v.attribute_str,
        "onpaste": v.attribute_str,
        "onpause": v.attribute_str,
        "onplay": v.attribute_str,
        "onplaying": v.attribute_str,
        "onprogress": v.attribute_str,
        "onratechange": v.attribute_str,
        "onreset": v.attribute_str,
        "onresize": v.attribute_str,
        "onscroll": v.attribute_str,
        "onsecuritypolicyviolation": v.attribute_str,
        "onseeked": v.attribute_str,
        "onseeking": v.attribute_str,
        "onselect": v.attribute_str,
        "onslotchange": v.attribute_str,
        "onstalled": v.attribute_str,
        "onsubmit": v.attribute_str,
        "onsuspend": v.attribute_str,
        "ontimeupdate": v.attribute_str,
        "ontoggle": v.attribute_str,
        "onvolumechange": v.attribute_str,
        "onwaiting": v.attribute_str,
        "onwheel": v.attribute_str,
    }


class A(HtmlElement):
    """
    Hyperlink
    """

    element_attributes = {
        "download": v.attribute_str,
        "href": v.attribute_str,
        "hreflang": v.attribute_str,
        "ping": v.attribute_str,
        "referrerpolicy": v.attribute_str,
        "rel": v.attribute_unique_set,
        "target": v.attribute_str,
        "type": v.attribute_str,
    }
    element_categories: _T_categories_dict = {
        "flow": None,
        "interactive": lambda x: (x["href"] is not False),
        "palpable": None,
        "phrasing": None,
    }
    allowed_contexts = {"phrasing": None}


class Abbr(HtmlElement):
    """
    Abbreviation
    """

    element_categories = {"flow": None, "palpable": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Address(HtmlElement):
    """
    Contact information for a page or article element
    """

    element_categories = {"flow": None, "palpable": None}
    allowed_contexts = {"flow": None}


class Area(HtmlElement):
    """
    Hyperlink or dead area on an image map
    """

    is_empty = True
    element_attributes = {
        "alt": v.attribute_str,
        "coords": v.attribute_str,
        "download": v.attribute_str,
        "href": v.attribute_str,
        "ping": v.attribute_str,
        "referrerpolicy": v.attribute_str,
        "rel": v.attribute_unique_set,
        "shape": {"circle", "default", "poly", "rect"},
        "target": v.attribute_str,
    }
    element_categories = {"flow": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Article(HtmlElement):
    """
    Self-contained syndicatable or reusable composition
    """

    element_categories = {"flow": None, "palpable": None, "sectioning": None}
    allowed_contexts = {"flow": None}


class Aside(HtmlElement):
    """
    Sidebar for tangentially related content
    """

    element_categories = {"flow": None, "palpable": None, "sectioning": None}
    allowed_contexts = {"flow": None}


class Audio(HtmlElement):
    """
    Audio player
    """

    element_attributes = {
        "autoplay": v.attribute_bool,
        "controls": v.attribute_bool,
        "crossorigin": {"anonymous", "use-credentials"},
        "loop": v.attribute_bool,
        "muted": v.attribute_bool,
        "preload": {"none", "metadata", "auto"},
        "src": v.attribute_str,
    }
    element_categories: _T_categories_dict = {
        "embedded": None,
        "flow": None,
        "interactive": lambda x: (x["controls"] is not False),
        "palpable": lambda x: (x["controls"] is not False),
        "phrasing": None,
    }
    allowed_contexts = {"phrasing": None}


class B(HtmlElement):
    """
    Keywords
    """

    element_categories = {"flow": None, "palpable": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Base(HtmlElement):
    """
    Base URL and default target browsing context for hyperlinks and forms
    """

    is_empty = True
    element_attributes = {"href": v.attribute_str, "target": v.attribute_str}
    element_categories = {"metadata": None}
    allowed_contexts = {"_head": None}


class Bdi(HtmlElement):
    """
    Text directionality isolation
    """

    element_categories = {"flow": None, "palpable": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Bdo(HtmlElement):
    """
    Text directionality formatting
    """

    element_categories = {"flow": None, "palpable": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Blockquote(HtmlElement):
    """
    A section quoted from another source
    """

    element_attributes = {"cite": v.attribute_str}
    element_categories = {"flow": None, "palpable": None, "sectioning-root": None}
    allowed_contexts = {"flow": None}


class Body(HtmlElement):
    """
    Document body
    """

    element_attributes = {
        "onafterprint": v.attribute_str,
        "onbeforeprint": v.attribute_str,
        "onbeforeunload": v.attribute_str,
        "onhashchange": v.attribute_str,
        "onlanguagechange": v.attribute_str,
        "onmessage": v.attribute_str,
        "onmessageerror": v.attribute_str,
        "onoffline": v.attribute_str,
        "ononline": v.attribute_str,
        "onpagehide": v.attribute_str,
        "onpageshow": v.attribute_str,
        "onpopstate": v.attribute_str,
        "onrejectionhandled": v.attribute_str,
        "onstorage": v.attribute_str,
        "onunhandledrejection": v.attribute_str,
        "onunload": v.attribute_str,
    }
    element_categories = {"sectioning-root": None}
    allowed_contexts = {"_html": None}


class Br(HtmlElement):
    """
    Line break, e.g. in poem or postal address
    """

    is_empty = True
    element_categories = {"flow": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Button(HtmlElement):
    """
    Button control
    """

    element_attributes = {
        "disabled": v.attribute_bool,
        "form": v.attribute_str,
        "formaction": v.attribute_str,
        "formenctype": {
            "application/x-www-form-urlencoded",
            "multipart/form-data",
            "text/plain",
        },
        "formmethod": {"GET", "POST", "dialog"},
        "formnovalidate": v.attribute_bool,
        "formtarget": v.attribute_str,
        "name": v.attribute_str,
        "type": {"submit", "reset", "button"},
        "value": v.attribute_str,
    }
    element_categories = {
        "autocapitalize-inheriting": None,
        "flow": None,
        "form-associated": None,
        "interactive": None,
        "labelable": None,
        "listed": None,
        "palpable": None,
        "phrasing": None,
        "submittable": None,
    }
    allowed_contexts = {"phrasing": None}


class Canvas(HtmlElement):
    """
    Scriptable bitmap canvas
    """

    element_attributes = {
        "height": v.attribute_int_ge_zero,
        "width": v.attribute_int_ge_zero,
    }
    element_categories = {
        "embedded": None,
        "flow": None,
        "palpable": None,
        "phrasing": None,
    }
    allowed_contexts = {"phrasing": None}


class Caption(HtmlElement):
    """
    Table caption
    """

    allowed_contexts = {"_table": None}


class Cite(HtmlElement):
    """
    Title of a work
    """

    element_categories = {"flow": None, "palpable": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Code(HtmlElement):
    """
    Computer code
    """

    element_categories = {"flow": None, "palpable": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Col(HtmlElement):
    """
    Table column
    """

    is_empty = True
    element_attributes = {"span": v.attribute_int_gt_zero}
    allowed_contexts = {"_colgroup": None}


class Colgroup(HtmlElement):
    """
    Group of columns in a table
    """

    element_attributes = {"span": v.attribute_int_gt_zero}
    allowed_contexts = {"_table": None}


class Data(HtmlElement):
    """
    Machine-readable equivalent
    """

    element_attributes = {"value": v.attribute_str}
    element_categories = {"flow": None, "palpable": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Datalist(HtmlElement):
    """
    Container for options for combo box control
    """

    element_categories = {"flow": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Dd(HtmlElement):
    """
    Content for corresponding dt element(s)
    """

    allowed_contexts = {"_div": None, "_dl": None}


class Del(HtmlElement):
    """
    A removal from the document
    """

    element_attributes = {"cite": v.attribute_str, "datetime": v.attribute_str}
    element_categories = {"flow": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Details(HtmlElement):
    """
    Disclosure control for hiding details
    """

    element_attributes = {"open": v.attribute_bool}
    element_categories = {
        "flow": None,
        "interactive": None,
        "palpable": None,
        "sectioning-root": None,
    }
    allowed_contexts = {"flow": None}


class Dfn(HtmlElement):
    """
    Defining instance
    """

    element_categories = {"flow": None, "palpable": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Dialog(HtmlElement):
    """
    Dialog box or window
    """

    element_attributes = {"open": v.attribute_bool}
    element_categories = {"flow": None, "sectioning-root": None}
    allowed_contexts = {"flow": None}


class Div(HtmlElement):
    """
    Generic flow container, or container for name-value groups in dl elements
    """

    element_categories = {"flow": None, "palpable": None}
    allowed_contexts = {"_dl": None, "flow": None}


class Dl(HtmlElement):
    """
    Association list consisting of zero or more name-value groups
    """

    element_categories: _T_categories_dict = {
        "flow": None,
        "palpable": lambda x: (
            (
                "dt" in (child.name for child in x)
                or "dt"
                in (
                    child.name
                    for child in itertools.chain(
                        *(div for div in x if div.name == "div")
                    )
                )
            )
            and (
                "dd" in (child.name for child in x)
                or "dd"
                in (
                    child.name
                    for child in itertools.chain(
                        *(div for div in x if div.name == "div")
                    )
                )
            )
        ),
    }
    allowed_contexts = {"flow": None}


class Dt(HtmlElement):
    """
    Legend for corresponding dd element(s)
    """

    allowed_contexts = {"_div": None, "_dl": None}


class Em(HtmlElement):
    """
    Stress emphasis
    """

    element_categories = {"flow": None, "palpable": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Embed(HtmlElement):
    """
    Plugin
    """

    is_empty = True
    element_attributes = {
        "height": v.attribute_int_ge_zero,
        "src": v.attribute_str,
        "type": v.attribute_str,
        "width": v.attribute_int_ge_zero,
    }
    any_attribute = True
    element_categories = {
        "embedded": None,
        "flow": None,
        "interactive": None,
        "palpable": None,
        "phrasing": None,
    }
    allowed_contexts = {"phrasing": None}


class Fieldset(HtmlElement):
    """
    Group of form controls
    """

    element_attributes = {
        "disabled": v.attribute_bool,
        "form": v.attribute_str,
        "name": v.attribute_str,
    }
    element_categories = {
        "autocapitalize-inheriting": None,
        "flow": None,
        "form-associated": None,
        "listed": None,
        "palpable": None,
        "sectioning-root": None,
    }
    allowed_contexts = {"flow": None}


class Figcaption(HtmlElement):
    """
    Caption for figure
    """

    allowed_contexts = {"_figure": None}


class Figure(HtmlElement):
    """
    Figure with optional caption
    """

    element_categories = {"flow": None, "palpable": None, "sectioning-root": None}
    allowed_contexts = {"flow": None}


class Footer(HtmlElement):
    """
    Footer for a page or section
    """

    element_categories = {"flow": None, "palpable": None}
    allowed_contexts = {"flow": None}


class Form(HtmlElement):
    """
    User-submittable form
    """

    element_attributes = {
        "accept-charset": v.attribute_str_literal_ci("utf-8"),
        "action": v.attribute_str,
        "autocomplete": {"on", "off"},
        "enctype": {
            "application/x-www-form-urlencoded",
            "multipart/form-data",
            "text/plain",
        },
        "method": {"GET", "POST", "dialog"},
        "name": v.attribute_str,
        "novalidate": v.attribute_bool,
        "target": v.attribute_str,
    }
    element_categories = {"flow": None, "palpable": None}
    allowed_contexts = {"flow": None}


class H1(HtmlElement):
    """
    Section heading
    """

    element_categories = {"flow": None, "heading": None, "palpable": None}
    allowed_contexts = {"_legend": None, "_summary": None, "flow": None}


class H2(HtmlElement):
    """
    Section heading
    """

    element_categories = {"flow": None, "heading": None, "palpable": None}
    allowed_contexts = {"_legend": None, "_summary": None, "flow": None}


class H3(HtmlElement):
    """
    Section heading
    """

    element_categories = {"flow": None, "heading": None, "palpable": None}
    allowed_contexts = {"_legend": None, "_summary": None, "flow": None}


class H4(HtmlElement):
    """
    Section heading
    """

    element_categories = {"flow": None, "heading": None, "palpable": None}
    allowed_contexts = {"_legend": None, "_summary": None, "flow": None}


class H5(HtmlElement):
    """
    Section heading
    """

    element_categories = {"flow": None, "heading": None, "palpable": None}
    allowed_contexts = {"_legend": None, "_summary": None, "flow": None}


class H6(HtmlElement):
    """
    Section heading
    """

    element_categories = {"flow": None, "heading": None, "palpable": None}
    allowed_contexts = {"_legend": None, "_summary": None, "flow": None}


class Head(HtmlElement):
    """
    Container for document metadata
    """

    allowed_contexts = {"_html": None}


class Header(HtmlElement):
    """
    Introductory or navigational aids for a page or section
    """

    element_categories = {"flow": None, "palpable": None}
    allowed_contexts = {"flow": None}


class Hgroup(HtmlElement):
    """
    heading group
    """

    element_categories = {"flow": None, "heading": None, "palpable": None}
    allowed_contexts = {"_legend": None, "_summary": None, "flow": None}


class Hr(HtmlElement):
    """
    Thematic break
    """

    is_empty = True
    element_categories = {"flow": None}
    allowed_contexts = {"flow": None}


class Html(HtmlElement):
    """
    Root element
    """

    _default_prepend_doctype = True


class I(HtmlElement):
    """
    Alternate voice
    """

    element_categories = {"flow": None, "palpable": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Iframe(HtmlElement):
    """
    Nested browsing context
    """

    is_empty = True
    element_attributes = {
        "allow": v.attribute_str,
        "allowfullscreen": v.attribute_bool,
        "height": v.attribute_int_ge_zero,
        "loading": {"lazy", "eager"},
        "name": v.attribute_str,
        "referrerpolicy": v.attribute_str,
        "sandbox": v.attribute_unique_set_literal_ci(
            "allow-forms",
            "allow-modals",
            "allow-orientation-lock",
            "allow-pointer-lock",
            "allow-popups",
            "allow-popups-to-escape-sandbox",
            "allow-presentation",
            "allow-same-origin",
            "allow-scripts",
            "allow-top-navigation",
        ),
        "src": v.attribute_str,
        "srcdoc": v.attribute_str,
        "width": v.attribute_int_ge_zero,
    }
    element_categories = {
        "embedded": None,
        "flow": None,
        "interactive": None,
        "palpable": None,
        "phrasing": None,
    }
    allowed_contexts = {"phrasing": None}


class Img(HtmlElement):
    """
    Image
    """

    is_empty = True
    element_attributes = {
        "alt": v.attribute_str,
        "crossorigin": {"anonymous", "use-credentials"},
        "decoding": {"sync", "async", "auto"},
        "height": v.attribute_int_ge_zero,
        "ismap": v.attribute_bool,
        "loading": {"lazy", "eager"},
        "referrerpolicy": v.attribute_str,
        "sizes": v.attribute_str,
        "src": v.attribute_str,
        "srcset": v.attribute_str,
        "usemap": v.attribute_str,
        "width": v.attribute_int_ge_zero,
    }
    element_categories: _T_categories_dict = {
        "embedded": None,
        "flow": None,
        "form-associated": None,
        "interactive": lambda x: (x["usemap"] is not False),
        "palpable": None,
        "phrasing": None,
    }
    allowed_contexts = {"_picture": None, "phrasing": None}


class Input(HtmlElement):
    """
    Form control
    """

    is_empty = True
    element_attributes = {
        "accept": v.attribute_str,
        "alt": v.attribute_str,
        "autocomplete": v.attribute_str,
        "checked": v.attribute_bool,
        "dirname": v.attribute_str,
        "disabled": v.attribute_bool,
        "form": v.attribute_str,
        "formaction": v.attribute_str,
        "formenctype": {
            "application/x-www-form-urlencoded",
            "multipart/form-data",
            "text/plain",
        },
        "formmethod": {"GET", "POST", "dialog"},
        "formnovalidate": v.attribute_bool,
        "formtarget": v.attribute_str,
        "height": v.attribute_int_ge_zero,
        "list": v.attribute_str,
        "max": v.attribute_str,
        "maxlength": v.attribute_int_ge_zero,
        "min": v.attribute_str,
        "minlength": v.attribute_int_ge_zero,
        "multiple": v.attribute_bool,
        "name": v.attribute_str,
        "pattern": v.attribute_str,
        "placeholder": v.attribute_str,
        "readonly": v.attribute_bool,
        "required": v.attribute_bool,
        "size": v.attribute_int_gt_zero,
        "src": v.attribute_str,
        "step": v.attribute_any(
            v.attribute_float_gt_zero, v.attribute_str_literal("any")
        ),
        "type": {
            "hidden",
            "text",
            "search",
            "tel",
            "url",
            "email",
            "password",
            "date",
            "month",
            "week",
            "time",
            "datetime-local",
            "number",
            "range",
            "color",
            "checkbox",
            "radio",
            "file",
            "submit",
            "image",
            "reset",
            "button",
        },
        "value": v.attribute_str,
        "width": v.attribute_int_ge_zero,
    }
    element_categories: _T_categories_dict = {
        "autocapitalize-inheriting": None,
        "flow": None,
        "form-associated": None,
        "interactive": lambda x: (x["type"] != "hidden"),
        "labelable": None,
        "listed": None,
        "palpable": lambda x: (x["type"] != "hidden"),
        "phrasing": None,
        "resettable": None,
        "submittable": None,
    }
    allowed_contexts = {"phrasing": None}


class Ins(HtmlElement):
    """
    An addition to the document
    """

    element_attributes = {"cite": v.attribute_str, "datetime": v.attribute_str}
    element_categories = {"flow": None, "palpable": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Kbd(HtmlElement):
    """
    User input
    """

    element_categories = {"flow": None, "palpable": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Label(HtmlElement):
    """
    Caption for a form control
    """

    element_attributes = {"for": v.attribute_str}
    element_categories = {
        "flow": None,
        "form-associated": None,
        "interactive": None,
        "palpable": None,
        "phrasing": None,
    }
    allowed_contexts = {"phrasing": None}


class Legend(HtmlElement):
    """
    Caption for fieldset
    """

    allowed_contexts = {"_fieldset": None}


class Li(HtmlElement):
    """
    List item
    """

    element_attributes = {"value": v.attribute_int}
    allowed_contexts = {"_menu": None, "_ol": None, "_ul": None}


class Link(HtmlElement):
    """
    Link metadata
    """

    is_empty = True
    element_attributes = {
        "as": v.attribute_str,
        "color": v.attribute_str,
        "crossorigin": {"anonymous", "use-credentials"},
        "disabled": v.attribute_bool,
        "href": v.attribute_str,
        "hreflang": v.attribute_str,
        "imagesizes": v.attribute_str,
        "imagesrcset": v.attribute_str,
        "integrity": v.attribute_str,
        "media": v.attribute_str,
        "referrerpolicy": v.attribute_str,
        "rel": v.attribute_unique_set,
        "sizes": v.attribute_str,
        "type": v.attribute_str,
    }
    element_categories: _T_categories_dict = {
        "flow": lambda x: (
            x["itemprop"] is not False
            or (
                isinstance(x["rel"], str)
                and set(x["rel"].lower().split())
                <= {
                    "dns-prefetch",
                    "modulepreload",
                    "pingback",
                    "preconnect",
                    "prefetch",
                    "preload",
                    "prerender",
                    "stylesheet",
                }
            )
        ),
        "metadata": None,
        "phrasing": lambda x: (
            x["itemprop"] is not False
            or (
                isinstance(x["rel"], str)
                and set(x["rel"].lower().split())
                <= {
                    "dns-prefetch",
                    "modulepreload",
                    "pingback",
                    "preconnect",
                    "prefetch",
                    "preload",
                    "prerender",
                    "stylesheet",
                }
            )
        ),
    }
    allowed_contexts: _T_contexts_dict = {
        "_head": None,
        "_noscript": None,
        "phrasing": lambda x: (
            x["itemprop"] is not False
            or (
                isinstance(x["rel"], str)
                and set(x["rel"].lower().split())
                <= {
                    "dns-prefetch",
                    "modulepreload",
                    "pingback",
                    "preconnect",
                    "prefetch",
                    "preload",
                    "prerender",
                    "stylesheet",
                }
            )
        ),
    }


class Main(HtmlElement):
    """
    Container for the dominant contents of the document
    """

    element_categories = {"flow": None, "palpable": None}
    allowed_contexts = {"flow": None}


class Map(HtmlElement):
    """
    Image map
    """

    element_attributes = {"name": v.attribute_str}
    element_categories = {"flow": None, "palpable": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Mark(HtmlElement):
    """
    Highlight
    """

    element_categories = {"flow": None, "palpable": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Menu(HtmlElement):
    """
    Menu of commands
    """

    element_categories: _T_categories_dict = {
        "flow": None,
        "palpable": lambda x: ("li" in (child.name for child in x)),
    }
    allowed_contexts = {"flow": None}


class Meta(HtmlElement):
    """
    Text metadata
    """

    is_empty = True
    element_attributes = {
        "charset": {"utf-8"},
        "content": v.attribute_str,
        "http-equiv": {
            "content-type",
            "default-style",
            "refresh",
            "x-ua-compatible",
            "content-security-policy",
        },
        "media": v.attribute_str,
        "name": v.attribute_str,
    }
    element_categories: _T_categories_dict = {
        "flow": lambda x: (x["itemprop"] is not False),
        "metadata": None,
        "phrasing": lambda x: (x["itemprop"] is not False),
    }
    allowed_contexts: _T_contexts_dict = {
        "_head": None,
        "_noscript": lambda x: (
            x["http-equiv"] is not False
            and not v.attribute_encoding_declaration_state(x["content"])
        ),
        "phrasing": lambda x: (x["itemprop"] is not False),
    }


class Meter(HtmlElement):
    """
    Gauge
    """

    element_attributes = {
        "high": v.attribute_float,
        "low": v.attribute_float,
        "max": v.attribute_float,
        "min": v.attribute_float,
        "optimum": v.attribute_float,
        "value": v.attribute_float,
    }
    element_categories = {
        "flow": None,
        "labelable": None,
        "palpable": None,
        "phrasing": None,
    }
    allowed_contexts = {"phrasing": None}


class Nav(HtmlElement):
    """
    Section with navigational links
    """

    element_categories = {"flow": None, "palpable": None, "sectioning": None}
    allowed_contexts = {"flow": None}


class Noscript(HtmlElement):
    """
    Fallback content for script
    """

    element_categories = {"flow": None, "metadata": None, "phrasing": None}
    allowed_contexts = {"_head": None, "phrasing": None}


class Object(HtmlElement):
    """
    Image, nested browsing context, or plugin
    """

    element_attributes = {
        "data": v.attribute_str,
        "form": v.attribute_str,
        "height": v.attribute_int_ge_zero,
        "name": v.attribute_str,
        "type": v.attribute_str,
        "width": v.attribute_int_ge_zero,
    }
    element_categories = {
        "embedded": None,
        "flow": None,
        "form-associated": None,
        "listed": None,
        "palpable": None,
        "phrasing": None,
    }
    allowed_contexts = {"phrasing": None}


class Ol(HtmlElement):
    """
    Ordered list
    """

    element_attributes = {
        "reversed": v.attribute_bool,
        "start": v.attribute_int,
        "type": {"1", "a", "A", "i", "I"},
    }
    element_categories: _T_categories_dict = {
        "flow": None,
        "palpable": lambda x: ("li" in (child.name for child in x)),
    }
    allowed_contexts = {"flow": None}


class Optgroup(HtmlElement):
    """
    Group of options in a list box
    """

    element_attributes = {"disabled": v.attribute_bool, "label": v.attribute_str}
    allowed_contexts = {"_select": None}


class Option(HtmlElement):
    """
    Option in a list box or combo box control
    """

    element_attributes = {
        "disabled": v.attribute_bool,
        "label": v.attribute_str,
        "selected": v.attribute_bool,
        "value": v.attribute_str,
    }
    allowed_contexts = {"_datalist": None, "_optgroup": None, "_select": None}


class Output(HtmlElement):
    """
    Calculated output value
    """

    element_attributes = {
        "for": v.attribute_unique_set,
        "form": v.attribute_str,
        "name": v.attribute_str,
    }
    element_categories = {
        "autocapitalize-inheriting": None,
        "flow": None,
        "form-associated": None,
        "labelable": None,
        "listed": None,
        "palpable": None,
        "phrasing": None,
        "resettable": None,
    }
    allowed_contexts = {"phrasing": None}


class P(HtmlElement):
    """
    Paragraph
    """

    element_categories = {"flow": None, "palpable": None}
    allowed_contexts = {"flow": None}


class Param(HtmlElement):
    """
    Parameter for object
    """

    is_empty = True
    element_attributes = {"name": v.attribute_str, "value": v.attribute_str}
    allowed_contexts = {"_object": None}


class Picture(HtmlElement):
    """
    Image
    """

    element_attributes = {"media": v.attribute_str, "width": v.attribute_int_ge_zero}
    element_categories = {"embedded": None, "flow": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Pre(HtmlElement):
    """
    Block of preformatted text
    """

    element_categories = {"flow": None, "palpable": None}
    allowed_contexts = {"flow": None}


class Progress(HtmlElement):
    """
    Progress bar
    """

    element_attributes = {"max": v.attribute_float, "value": v.attribute_float}
    element_categories = {
        "flow": None,
        "labelable": None,
        "palpable": None,
        "phrasing": None,
    }
    allowed_contexts = {"phrasing": None}


class Q(HtmlElement):
    """
    Quotation
    """

    element_attributes = {"cite": v.attribute_str}
    element_categories = {"flow": None, "palpable": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Rp(HtmlElement):
    """
    Parenthesis for ruby annotation text
    """

    allowed_contexts = {"_ruby": None}


class Rt(HtmlElement):
    """
    Ruby annotation text
    """

    allowed_contexts = {"_ruby": None}


class Ruby(HtmlElement):
    """
    Ruby annotation(s)
    """

    element_categories = {"flow": None, "palpable": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class S(HtmlElement):
    """
    Inaccurate text
    """

    element_categories = {"flow": None, "palpable": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Samp(HtmlElement):
    """
    Computer output
    """

    element_categories = {"flow": None, "palpable": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Script(HtmlElement):
    """
    Embedded script
    """

    element_attributes = {
        "async": v.attribute_bool,
        "crossorigin": {"anonymous", "use-credentials"},
        "defer": v.attribute_bool,
        "integrity": v.attribute_str,
        "nomodule": v.attribute_bool,
        "referrerpolicy": v.attribute_str,
        "src": v.attribute_str,
        "type": v.attribute_str,
    }
    element_categories = {
        "flow": None,
        "metadata": None,
        "phrasing": None,
        "script-supporting": None,
    }
    allowed_contexts = {"_head": None, "phrasing": None, "script-supporting": None}


class Section(HtmlElement):
    """
    Generic document or application section
    """

    element_categories = {"flow": None, "palpable": None, "sectioning": None}
    allowed_contexts = {"flow": None}


class Select(HtmlElement):
    """
    List box control
    """

    element_attributes = {
        "autocomplete": v.attribute_str,
        "disabled": v.attribute_bool,
        "form": v.attribute_str,
        "multiple": v.attribute_bool,
        "name": v.attribute_str,
        "required": v.attribute_bool,
        "size": v.attribute_int_gt_zero,
    }
    element_categories = {
        "autocapitalize-inheriting": None,
        "flow": None,
        "form-associated": None,
        "interactive": None,
        "labelable": None,
        "listed": None,
        "palpable": None,
        "phrasing": None,
        "resettable": None,
        "submittable": None,
    }
    allowed_contexts = {"phrasing": None}


class Slot(HtmlElement):
    """
    Shadow tree slot
    """

    element_attributes = {"name": v.attribute_str}
    element_categories = {"flow": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Small(HtmlElement):
    """
    Side comment
    """

    element_categories = {"flow": None, "palpable": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Source(HtmlElement):
    """
    Image source for img or media source for video or audio
    """

    is_empty = True
    element_attributes = {
        "height": v.attribute_int_ge_zero,
        "media": v.attribute_str,
        "sizes": v.attribute_str,
        "src": v.attribute_str,
        "srcset": v.attribute_str,
        "type": v.attribute_str,
        "width": v.attribute_int_ge_zero,
    }
    allowed_contexts = {"_audio": None, "_picture": None, "_video": None}


class Span(HtmlElement):
    """
    Generic phrasing container
    """

    element_categories = {"flow": None, "palpable": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Strong(HtmlElement):
    """
    Importance
    """

    element_categories = {"flow": None, "palpable": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Style(HtmlElement):
    """
    Embedded styling information
    """

    element_attributes = {"media": v.attribute_str}
    element_categories = {"metadata": None}
    allowed_contexts = {"_head": None, "_noscript": None}


class Sub(HtmlElement):
    """
    Subscript
    """

    element_categories = {"flow": None, "palpable": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Summary(HtmlElement):
    """
    Caption for details
    """

    allowed_contexts = {"_details": None}


class Sup(HtmlElement):
    """
    Superscript
    """

    element_categories = {"flow": None, "palpable": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Table(HtmlElement):
    """
    Table
    """

    element_categories = {"flow": None, "palpable": None}
    allowed_contexts = {"flow": None}


class Tbody(HtmlElement):
    """
    Group of rows in a table
    """

    allowed_contexts = {"_table": None}


class Td(HtmlElement):
    """
    Table cell
    """

    element_attributes = {
        "colspan": v.attribute_int_gt_zero,
        "headers": v.attribute_unique_set,
        "rowspan": v.attribute_int_ge_zero,
    }
    element_categories = {"sectioning-root": None}
    allowed_contexts = {"_tr": None}


class Template(HtmlElement):
    """
    Template
    """

    is_empty = True
    element_categories = {
        "flow": None,
        "metadata": None,
        "phrasing": None,
        "script-supporting": None,
    }
    allowed_contexts = {
        "_colgroup": None,
        "metadata": None,
        "phrasing": None,
        "script-supporting": None,
    }


class Textarea(HtmlElement):
    """
    Multiline text controls
    """

    element_attributes = {
        "autocomplete": v.attribute_str,
        "cols": v.attribute_int_gt_zero,
        "dirname": v.attribute_str,
        "disabled": v.attribute_bool,
        "form": v.attribute_str,
        "maxlength": v.attribute_int_ge_zero,
        "minlength": v.attribute_int_ge_zero,
        "name": v.attribute_str,
        "placeholder": v.attribute_str,
        "readonly": v.attribute_bool,
        "required": v.attribute_bool,
        "rows": v.attribute_int_gt_zero,
        "wrap": {"soft", "hard"},
    }
    element_categories = {
        "autocapitalize-inheriting": None,
        "flow": None,
        "form-associated": None,
        "interactive": None,
        "labelable": None,
        "listed": None,
        "palpable": None,
        "phrasing": None,
        "resettable": None,
        "submittable": None,
    }
    allowed_contexts = {"phrasing": None}


class Tfoot(HtmlElement):
    """
    Group of footer rows in a table
    """

    allowed_contexts = {"_table": None}


class Th(HtmlElement):
    """
    Table header cell
    """

    element_attributes = {
        "abbr": v.attribute_str,
        "colspan": v.attribute_int_gt_zero,
        "headers": v.attribute_unique_set,
        "rowspan": v.attribute_int_ge_zero,
        "scope": {"row", "col", "rowgroup", "colgroup"},
    }
    allowed_contexts = {"_tr": None}


class Thead(HtmlElement):
    """
    Group of heading rows in a table
    """

    allowed_contexts = {"_table": None}


class Time(HtmlElement):
    """
    Machine-readable equivalent of date- or time-related data
    """

    element_attributes = {"datetime": v.attribute_str}
    element_categories = {"flow": None, "palpable": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Title(HtmlElement):
    """
    Document title
    """

    element_categories = {"metadata": None}
    allowed_contexts = {"_head": None}


class Tr(HtmlElement):
    """
    Table row
    """

    allowed_contexts = {"_table": None, "_tbody": None, "_tfoot": None, "_thead": None}


class Track(HtmlElement):
    """
    Timed text track
    """

    is_empty = True
    element_attributes = {
        "default": v.attribute_bool,
        "kind": {"subtitles", "captions", "descriptions", "chapters", "metadata"},
        "label": v.attribute_str,
        "src": v.attribute_str,
        "srclang": v.attribute_str,
    }
    allowed_contexts = {"_audio": None, "_video": None}


class U(HtmlElement):
    """
    Unarticulated annotation
    """

    element_categories = {"flow": None, "palpable": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Ul(HtmlElement):
    """
    List
    """

    element_categories: _T_categories_dict = {
        "flow": None,
        "palpable": lambda x: ("li" in (child.name for child in x)),
    }
    allowed_contexts = {"flow": None}


class Var(HtmlElement):
    """
    Variable
    """

    element_categories = {"flow": None, "palpable": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}


class Video(HtmlElement):
    """
    Video player
    """

    element_attributes = {
        "autoplay": v.attribute_bool,
        "controls": v.attribute_bool,
        "crossorigin": {"anonymous", "use-credentials"},
        "height": v.attribute_int_ge_zero,
        "loop": v.attribute_bool,
        "muted": v.attribute_bool,
        "playsinline": v.attribute_bool,
        "poster": v.attribute_str,
        "preload": {"none", "metadata", "auto"},
        "src": v.attribute_str,
        "width": v.attribute_int_ge_zero,
    }
    element_categories: _T_categories_dict = {
        "embedded": None,
        "flow": None,
        "interactive": lambda x: (x["controls"] is not False),
        "palpable": None,
        "phrasing": None,
    }
    allowed_contexts = {"phrasing": None}


class Wbr(HtmlElement):
    """
    Line breaking opportunity
    """

    is_empty = True
    element_categories = {"flow": None, "phrasing": None}
    allowed_contexts = {"phrasing": None}
