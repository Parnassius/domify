# pylint: disable=too-many-lines

from . import attribute_validators as v
from .base_element import BaseElement
from .base_element import RawTextNode as RawTextNode  # pylint: disable=unused-import
from .base_element import TextNode as TextNode  # pylint: disable=unused-import
from .base_element import _T_attributes_dict

# begin automatic


class HtmlElement(BaseElement):
    """
    Base class for html elements, contains global attributes.
    """

    global_attributes: _T_attributes_dict = {
        "accesskey": lambda x: v.unique_set_validator(x)
        and max(len(t) for t in str(x).split()) <= 1,
        "autocapitalize": {"on", "off", "none", "sentences", "words", "characters"},
        "autofocus": v.bool_validator,
        "class": v.str_validator,
        "contenteditable": {"true", "false"},
        "dir": {"ltr", "rtl", "auto"},
        "draggable": {"true", "false"},
        "enterkeyhint": {"enter", "done", "go", "next", "previous", "search", "send"},
        "hidden": v.bool_validator,
        "id": v.str_validator,
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
        "is": v.str_validator,
        "itemid": v.str_validator,
        "itemprop": v.unique_set_validator,
        "itemref": v.unique_set_validator,
        "itemscope": v.bool_validator,
        "itemtype": v.unique_set_validator,
        "lang": v.str_validator,
        "nonce": v.str_validator,
        "slot": v.str_validator,
        "spellcheck": {"true", "false"},
        "style": v.str_validator,
        "tabindex": v.int_validator,
        "title": v.str_validator,
        "translate": {"yes", "no"},
        "onauxclick": v.str_validator,
        "onblur": v.str_validator,
        "oncancel": v.str_validator,
        "oncanplay": v.str_validator,
        "oncanplaythrough": v.str_validator,
        "onchange": v.str_validator,
        "onclick": v.str_validator,
        "onclose": v.str_validator,
        "oncontextlost": v.str_validator,
        "oncontextmenu": v.str_validator,
        "oncontextrestored": v.str_validator,
        "oncopy": v.str_validator,
        "oncuechange": v.str_validator,
        "oncut": v.str_validator,
        "ondblclick": v.str_validator,
        "ondrag": v.str_validator,
        "ondragend": v.str_validator,
        "ondragenter": v.str_validator,
        "ondragleave": v.str_validator,
        "ondragover": v.str_validator,
        "ondragstart": v.str_validator,
        "ondrop": v.str_validator,
        "ondurationchange": v.str_validator,
        "onemptied": v.str_validator,
        "onended": v.str_validator,
        "onerror": v.str_validator,
        "onfocus": v.str_validator,
        "onformdata": v.str_validator,
        "oninput": v.str_validator,
        "oninvalid": v.str_validator,
        "onkeydown": v.str_validator,
        "onkeypress": v.str_validator,
        "onkeyup": v.str_validator,
        "onload": v.str_validator,
        "onloadeddata": v.str_validator,
        "onloadedmetadata": v.str_validator,
        "onloadstart": v.str_validator,
        "onmousedown": v.str_validator,
        "onmouseenter": v.str_validator,
        "onmouseleave": v.str_validator,
        "onmousemove": v.str_validator,
        "onmouseout": v.str_validator,
        "onmouseover": v.str_validator,
        "onmouseup": v.str_validator,
        "onpaste": v.str_validator,
        "onpause": v.str_validator,
        "onplay": v.str_validator,
        "onplaying": v.str_validator,
        "onprogress": v.str_validator,
        "onratechange": v.str_validator,
        "onreset": v.str_validator,
        "onresize": v.str_validator,
        "onscroll": v.str_validator,
        "onsecuritypolicyviolation": v.str_validator,
        "onseeked": v.str_validator,
        "onseeking": v.str_validator,
        "onselect": v.str_validator,
        "onslotchange": v.str_validator,
        "onstalled": v.str_validator,
        "onsubmit": v.str_validator,
        "onsuspend": v.str_validator,
        "ontimeupdate": v.str_validator,
        "ontoggle": v.str_validator,
        "onvolumechange": v.str_validator,
        "onwaiting": v.str_validator,
        "onwheel": v.str_validator,
    }


class A(HtmlElement):
    """
    Hyperlink
    """

    element_attributes = {
        "download": v.str_validator,
        "href": v.str_validator,
        "hreflang": v.str_validator,
        "ping": v.str_validator,
        "referrerpolicy": v.str_validator,
        "rel": v.unique_set_validator,
        "target": v.str_validator,
        "type": v.str_validator,
    }


class Abbr(HtmlElement):
    """
    Abbreviation
    """


class Address(HtmlElement):
    """
    Contact information for a page or article element
    """


class Area(HtmlElement):
    """
    Hyperlink or dead area on an image map
    """

    is_empty = True
    element_attributes = {
        "alt": v.str_validator,
        "coords": v.str_validator,
        "download": v.str_validator,
        "href": v.str_validator,
        "ping": v.str_validator,
        "referrerpolicy": v.str_validator,
        "rel": v.unique_set_validator,
        "shape": {"circle", "default", "poly", "rect"},
        "target": v.str_validator,
    }


class Article(HtmlElement):
    """
    Self-contained syndicatable or reusable composition
    """


class Aside(HtmlElement):
    """
    Sidebar for tangentially related content
    """


class Audio(HtmlElement):
    """
    Audio player
    """

    element_attributes = {
        "autoplay": v.bool_validator,
        "controls": v.bool_validator,
        "crossorigin": {"anonymous", "use-credentials"},
        "loop": v.bool_validator,
        "muted": v.bool_validator,
        "preload": {"none", "metadata", "auto"},
        "src": v.str_validator,
    }


class B(HtmlElement):
    """
    Keywords
    """


class Base(HtmlElement):
    """
    Base URL and default target browsing context for hyperlinks and forms
    """

    is_empty = True
    element_attributes = {"href": v.str_validator, "target": v.str_validator}


class Bdi(HtmlElement):
    """
    Text directionality isolation
    """


class Bdo(HtmlElement):
    """
    Text directionality formatting
    """


class Blockquote(HtmlElement):
    """
    A section quoted from another source
    """

    element_attributes = {"cite": v.str_validator}


class Body(HtmlElement):
    """
    Document body
    """

    element_attributes = {
        "onafterprint": v.str_validator,
        "onbeforeprint": v.str_validator,
        "onbeforeunload": v.str_validator,
        "onhashchange": v.str_validator,
        "onlanguagechange": v.str_validator,
        "onmessage": v.str_validator,
        "onmessageerror": v.str_validator,
        "onoffline": v.str_validator,
        "ononline": v.str_validator,
        "onpagehide": v.str_validator,
        "onpageshow": v.str_validator,
        "onpopstate": v.str_validator,
        "onrejectionhandled": v.str_validator,
        "onstorage": v.str_validator,
        "onunhandledrejection": v.str_validator,
        "onunload": v.str_validator,
    }


class Br(HtmlElement):
    """
    Line break, e.g. in poem or postal address
    """

    is_empty = True


class Button(HtmlElement):
    """
    Button control
    """

    element_attributes = {
        "disabled": v.bool_validator,
        "form": v.str_validator,
        "formaction": v.str_validator,
        "formenctype": {
            "application/x-www-form-urlencoded",
            "multipart/form-data",
            "text/plain",
        },
        "formmethod": {"GET", "POST", "dialog"},
        "formnovalidate": v.bool_validator,
        "formtarget": v.str_validator,
        "name": v.str_validator,
        "type": {"submit", "reset", "button"},
        "value": v.str_validator,
    }


class Canvas(HtmlElement):
    """
    Scriptable bitmap canvas
    """

    element_attributes = {
        "height": v.int_ge_zero_validator,
        "width": v.int_ge_zero_validator,
    }


class Caption(HtmlElement):
    """
    Table caption
    """


class Cite(HtmlElement):
    """
    Title of a work
    """


class Code(HtmlElement):
    """
    Computer code
    """


class Col(HtmlElement):
    """
    Table column
    """

    is_empty = True
    element_attributes = {"span": v.int_gt_zero_validator}


class Colgroup(HtmlElement):
    """
    Group of columns in a table
    """

    element_attributes = {"span": v.int_gt_zero_validator}


class Data(HtmlElement):
    """
    Machine-readable equivalent
    """

    element_attributes = {"value": v.str_validator}


class Datalist(HtmlElement):
    """
    Container for options for combo box control
    """


class Dd(HtmlElement):
    """
    Content for corresponding dt element(s)
    """


class Del(HtmlElement):
    """
    A removal from the document
    """

    element_attributes = {"cite": v.str_validator, "datetime": v.str_validator}


class Details(HtmlElement):
    """
    Disclosure control for hiding details
    """

    element_attributes = {"open": v.bool_validator}


class Dfn(HtmlElement):
    """
    Defining instance
    """


class Dialog(HtmlElement):
    """
    Dialog box or window
    """

    element_attributes = {"open": v.bool_validator}


class Div(HtmlElement):
    """
    Generic flow container, or container for name-value groups in dl elements
    """


class Dl(HtmlElement):
    """
    Association list consisting of zero or more name-value groups
    """


class Dt(HtmlElement):
    """
    Legend for corresponding dd element(s)
    """


class Em(HtmlElement):
    """
    Stress emphasis
    """


class Embed(HtmlElement):
    """
    Plugin
    """

    is_empty = True
    element_attributes = {
        "height": v.int_ge_zero_validator,
        "src": v.str_validator,
        "type": v.str_validator,
        "width": v.int_ge_zero_validator,
    }
    any_attribute = True


class Fieldset(HtmlElement):
    """
    Group of form controls
    """

    element_attributes = {
        "disabled": v.bool_validator,
        "form": v.str_validator,
        "name": v.str_validator,
    }


class Figcaption(HtmlElement):
    """
    Caption for figure
    """


class Figure(HtmlElement):
    """
    Figure with optional caption
    """


class Footer(HtmlElement):
    """
    Footer for a page or section
    """


class Form(HtmlElement):
    """
    User-submittable form
    """

    element_attributes: _T_attributes_dict = {
        "accept-charset": lambda x: str(x).upper() == "UTF-8",
        "action": v.str_validator,
        "autocomplete": {"on", "off"},
        "enctype": {
            "application/x-www-form-urlencoded",
            "multipart/form-data",
            "text/plain",
        },
        "method": {"GET", "POST", "dialog"},
        "name": v.str_validator,
        "novalidate": v.bool_validator,
        "target": v.str_validator,
    }


class H1(HtmlElement):
    """
    Section heading
    """


class H2(HtmlElement):
    """
    Section heading
    """


class H3(HtmlElement):
    """
    Section heading
    """


class H4(HtmlElement):
    """
    Section heading
    """


class H5(HtmlElement):
    """
    Section heading
    """


class H6(HtmlElement):
    """
    Section heading
    """


class Head(HtmlElement):
    """
    Container for document metadata
    """


class Header(HtmlElement):
    """
    Introductory or navigational aids for a page or section
    """


class Hgroup(HtmlElement):
    """
    heading group
    """


class Hr(HtmlElement):
    """
    Thematic break
    """

    is_empty = True


class Html(HtmlElement):
    """
    Root element
    """


class I(HtmlElement):
    """
    Alternate voice
    """


class Iframe(HtmlElement):
    """
    Nested browsing context
    """

    is_empty = True
    element_attributes: _T_attributes_dict = {
        "allow": v.str_validator,
        "allowfullscreen": v.bool_validator,
        "height": v.int_ge_zero_validator,
        "loading": {"lazy", "eager"},
        "name": v.str_validator,
        "referrerpolicy": v.str_validator,
        "sandbox": lambda x: v.unique_set_validator(str(x).lower())
        and set(str(x).lower().split())
        <= {
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
        },
        "src": v.str_validator,
        "srcdoc": v.str_validator,
        "width": v.int_ge_zero_validator,
    }


class Img(HtmlElement):
    """
    Image
    """

    is_empty = True
    element_attributes = {
        "alt": v.str_validator,
        "crossorigin": {"anonymous", "use-credentials"},
        "decoding": {"sync", "async", "auto"},
        "height": v.int_ge_zero_validator,
        "ismap": v.bool_validator,
        "loading": {"lazy", "eager"},
        "referrerpolicy": v.str_validator,
        "sizes": v.str_validator,
        "src": v.str_validator,
        "srcset": v.str_validator,
        "usemap": v.str_validator,
        "width": v.int_ge_zero_validator,
    }


class Input(HtmlElement):
    """
    Form control
    """

    is_empty = True
    element_attributes: _T_attributes_dict = {
        "accept": v.str_validator,
        "alt": v.str_validator,
        "autocomplete": v.str_validator,
        "checked": v.bool_validator,
        "dirname": v.str_validator,
        "disabled": v.bool_validator,
        "form": v.str_validator,
        "formaction": v.str_validator,
        "formenctype": {
            "application/x-www-form-urlencoded",
            "multipart/form-data",
            "text/plain",
        },
        "formmethod": {"GET", "POST", "dialog"},
        "formnovalidate": v.bool_validator,
        "formtarget": v.str_validator,
        "height": v.int_ge_zero_validator,
        "list": v.str_validator,
        "max": v.str_validator,
        "maxlength": v.int_ge_zero_validator,
        "min": v.str_validator,
        "minlength": v.int_ge_zero_validator,
        "multiple": v.bool_validator,
        "name": v.str_validator,
        "pattern": v.str_validator,
        "placeholder": v.str_validator,
        "readonly": v.bool_validator,
        "required": v.bool_validator,
        "size": v.int_gt_zero_validator,
        "src": v.str_validator,
        "step": lambda x: v.float_gt_zero_validator(x) or x in {"any"},
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
        "value": v.str_validator,
        "width": v.int_ge_zero_validator,
    }


class Ins(HtmlElement):
    """
    An addition to the document
    """

    element_attributes = {"cite": v.str_validator, "datetime": v.str_validator}


class Kbd(HtmlElement):
    """
    User input
    """


class Label(HtmlElement):
    """
    Caption for a form control
    """

    element_attributes = {"for": v.str_validator}


class Legend(HtmlElement):
    """
    Caption for fieldset
    """


class Li(HtmlElement):
    """
    List item
    """

    element_attributes = {"value": v.int_validator}


class Link(HtmlElement):
    """
    Link metadata
    """

    is_empty = True
    element_attributes = {
        "as": v.str_validator,
        "color": v.str_validator,
        "crossorigin": {"anonymous", "use-credentials"},
        "disabled": v.bool_validator,
        "href": v.str_validator,
        "hreflang": v.str_validator,
        "imagesizes": v.str_validator,
        "imagesrcset": v.str_validator,
        "integrity": v.str_validator,
        "media": v.str_validator,
        "referrerpolicy": v.str_validator,
        "rel": v.unique_set_validator,
        "sizes": v.str_validator,
        "type": v.str_validator,
    }


class Main(HtmlElement):
    """
    Container for the dominant contents of the document
    """


class Map(HtmlElement):
    """
    Image map
    """

    element_attributes = {"name": v.str_validator}


class Mark(HtmlElement):
    """
    Highlight
    """


class Menu(HtmlElement):
    """
    Menu of commands
    """


class Meta(HtmlElement):
    """
    Text metadata
    """

    is_empty = True
    element_attributes = {
        "charset": {"utf-8"},
        "content": v.str_validator,
        "http-equiv": {
            "content-type",
            "default-style",
            "refresh",
            "x-ua-compatible",
            "content-security-policy",
        },
        "media": v.str_validator,
        "name": v.str_validator,
    }


class Meter(HtmlElement):
    """
    Gauge
    """

    element_attributes = {
        "high": v.float_validator,
        "low": v.float_validator,
        "max": v.float_validator,
        "min": v.float_validator,
        "optimum": v.float_validator,
        "value": v.float_validator,
    }


class Nav(HtmlElement):
    """
    Section with navigational links
    """


class Noscript(HtmlElement):
    """
    Fallback content for script
    """


class Object(HtmlElement):
    """
    Image, nested browsing context, or plugin
    """

    element_attributes = {
        "data": v.str_validator,
        "form": v.str_validator,
        "height": v.int_ge_zero_validator,
        "name": v.str_validator,
        "type": v.str_validator,
        "width": v.int_ge_zero_validator,
    }


class Ol(HtmlElement):
    """
    Ordered list
    """

    element_attributes = {
        "reversed": v.bool_validator,
        "start": v.int_validator,
        "type": {"1", "a", "A", "i", "I"},
    }


class Optgroup(HtmlElement):
    """
    Group of options in a list box
    """

    element_attributes = {"disabled": v.bool_validator, "label": v.str_validator}


class Option(HtmlElement):
    """
    Option in a list box or combo box control
    """

    element_attributes = {
        "disabled": v.bool_validator,
        "label": v.str_validator,
        "selected": v.bool_validator,
        "value": v.str_validator,
    }


class Output(HtmlElement):
    """
    Calculated output value
    """

    element_attributes = {
        "for": v.unique_set_validator,
        "form": v.str_validator,
        "name": v.str_validator,
    }


class P(HtmlElement):
    """
    Paragraph
    """


class Param(HtmlElement):
    """
    Parameter for object
    """

    is_empty = True
    element_attributes = {"name": v.str_validator, "value": v.str_validator}


class Picture(HtmlElement):
    """
    Image
    """

    element_attributes = {"media": v.str_validator, "width": v.int_ge_zero_validator}


class Pre(HtmlElement):
    """
    Block of preformatted text
    """


class Progress(HtmlElement):
    """
    Progress bar
    """

    element_attributes = {"max": v.float_validator, "value": v.float_validator}


class Q(HtmlElement):
    """
    Quotation
    """

    element_attributes = {"cite": v.str_validator}


class Rp(HtmlElement):
    """
    Parenthesis for ruby annotation text
    """


class Rt(HtmlElement):
    """
    Ruby annotation text
    """


class Ruby(HtmlElement):
    """
    Ruby annotation(s)
    """


class S(HtmlElement):
    """
    Inaccurate text
    """


class Samp(HtmlElement):
    """
    Computer output
    """


class Script(HtmlElement):
    """
    Embedded script
    """

    element_attributes = {
        "async": v.bool_validator,
        "crossorigin": {"anonymous", "use-credentials"},
        "defer": v.bool_validator,
        "integrity": v.str_validator,
        "nomodule": v.bool_validator,
        "referrerpolicy": v.str_validator,
        "src": v.str_validator,
        "type": v.str_validator,
    }


class Section(HtmlElement):
    """
    Generic document or application section
    """


class Select(HtmlElement):
    """
    List box control
    """

    element_attributes = {
        "autocomplete": v.str_validator,
        "disabled": v.bool_validator,
        "form": v.str_validator,
        "multiple": v.bool_validator,
        "name": v.str_validator,
        "required": v.bool_validator,
        "size": v.int_gt_zero_validator,
    }


class Slot(HtmlElement):
    """
    Shadow tree slot
    """

    element_attributes = {"name": v.str_validator}


class Small(HtmlElement):
    """
    Side comment
    """


class Source(HtmlElement):
    """
    Image source for img or media source for video or audio
    """

    is_empty = True
    element_attributes = {
        "height": v.int_ge_zero_validator,
        "media": v.str_validator,
        "sizes": v.str_validator,
        "src": v.str_validator,
        "srcset": v.str_validator,
        "type": v.str_validator,
        "width": v.int_ge_zero_validator,
    }


class Span(HtmlElement):
    """
    Generic phrasing container
    """


class Strong(HtmlElement):
    """
    Importance
    """


class Style(HtmlElement):
    """
    Embedded styling information
    """

    element_attributes = {"media": v.str_validator}


class Sub(HtmlElement):
    """
    Subscript
    """


class Summary(HtmlElement):
    """
    Caption for details
    """


class Sup(HtmlElement):
    """
    Superscript
    """


class Table(HtmlElement):
    """
    Table
    """


class Tbody(HtmlElement):
    """
    Group of rows in a table
    """


class Td(HtmlElement):
    """
    Table cell
    """

    element_attributes = {
        "colspan": v.int_gt_zero_validator,
        "headers": v.unique_set_validator,
        "rowspan": v.int_ge_zero_validator,
    }


class Template(HtmlElement):
    """
    Template
    """

    is_empty = True


class Textarea(HtmlElement):
    """
    Multiline text controls
    """

    element_attributes = {
        "autocomplete": v.str_validator,
        "cols": v.int_gt_zero_validator,
        "dirname": v.str_validator,
        "disabled": v.bool_validator,
        "form": v.str_validator,
        "maxlength": v.int_ge_zero_validator,
        "minlength": v.int_ge_zero_validator,
        "name": v.str_validator,
        "placeholder": v.str_validator,
        "readonly": v.bool_validator,
        "required": v.bool_validator,
        "rows": v.int_gt_zero_validator,
        "wrap": {"soft", "hard"},
    }


class Tfoot(HtmlElement):
    """
    Group of footer rows in a table
    """


class Th(HtmlElement):
    """
    Table header cell
    """

    element_attributes = {
        "abbr": v.str_validator,
        "colspan": v.int_gt_zero_validator,
        "headers": v.unique_set_validator,
        "rowspan": v.int_ge_zero_validator,
        "scope": {"row", "col", "rowgroup", "colgroup"},
    }


class Thead(HtmlElement):
    """
    Group of heading rows in a table
    """


class Time(HtmlElement):
    """
    Machine-readable equivalent of date- or time-related data
    """

    element_attributes = {"datetime": v.str_validator}


class Title(HtmlElement):
    """
    Document title
    """


class Tr(HtmlElement):
    """
    Table row
    """


class Track(HtmlElement):
    """
    Timed text track
    """

    is_empty = True
    element_attributes = {
        "default": v.bool_validator,
        "kind": {"subtitles", "captions", "descriptions", "chapters", "metadata"},
        "label": v.str_validator,
        "src": v.str_validator,
        "srclang": v.str_validator,
    }


class U(HtmlElement):
    """
    Unarticulated annotation
    """


class Ul(HtmlElement):
    """
    List
    """


class Var(HtmlElement):
    """
    Variable
    """


class Video(HtmlElement):
    """
    Video player
    """

    element_attributes = {
        "autoplay": v.bool_validator,
        "controls": v.bool_validator,
        "crossorigin": {"anonymous", "use-credentials"},
        "height": v.int_ge_zero_validator,
        "loop": v.bool_validator,
        "muted": v.bool_validator,
        "playsinline": v.bool_validator,
        "poster": v.str_validator,
        "preload": {"none", "metadata", "auto"},
        "src": v.str_validator,
        "width": v.int_ge_zero_validator,
    }


class Wbr(HtmlElement):
    """
    Line breaking opportunity
    """

    is_empty = True
