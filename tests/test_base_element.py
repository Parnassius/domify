from __future__ import annotations

import asyncio

import pytest

from domify import exc
from domify import html_elements as e
from domify.base_element import BaseElement


def test_base():
    assert str(e.Div()) == "<div></div>"
    assert str(e.Br()) == "<br>"

    assert str(BaseElement()) == ""

    assert str(e.Div(e.TextNode("<foobar>"))) == "<div>&lt;foobar&gt;</div>"
    assert str(e.Div(e.RawTextNode("<foobar>"))) == "<div><foobar></div>"


def test_attributes():
    assert str(e.Div(id="main")) == '<div id="main"></div>'
    assert (
        str(e.Div(class_="class1", data_foo="bar"))
        == '<div class="class1" data-foo="bar"></div>'
    )
    assert (
        str(e.Div(title=82, data_foo=1, data_bar=5.5))
        == '<div title="82" data-foo="1" data-bar="5.5"></div>'
    )
    assert (
        str(e.Input(type_="checkbox", checked=False, tabindex=-1))
        == '<input type="checkbox" tabindex="-1">'
    )
    assert (
        str(e.Input(type_="checkbox", checked=True, name=None))
        == '<input type="checkbox" checked>'
    )
    assert (
        str(e.Img(src="foobar", width=50, height=15))
        == '<img src="foobar" width="50" height="15">'
    )
    assert (
        str(e.Progress(max=50, value=2.5))
        == '<progress max="50" value="2.5"></progress>'
    )
    assert str(e.Link(rel="prefetch preload")) == '<link rel="prefetch preload">'
    assert str(e.Form(accept_charset="UTF-8")) == '<form accept-charset="UTF-8"></form>'
    assert str(e.Div(hidden=True)) == "<div hidden></div>"
    assert str(e.Div(hidden="hidden")) == '<div hidden="hidden"></div>'

    # Invalid attributes
    with pytest.warns(exc.InvalidAttributeWarning):
        e.Div(href="foo.html")
    with pytest.warns(exc.InvalidAttributeWarning):
        e.Br(for_="bar")

    # Invalid attribute values
    with pytest.warns(exc.InvalidAttributeValueWarning):
        e.Div(translate="foobar")
    with pytest.warns(exc.InvalidAttributeValueWarning):
        e.Div(hidden=14)
    with pytest.warns(exc.InvalidAttributeValueWarning):
        e.Input(type_="number", step=-1)
    with pytest.warns(exc.InvalidAttributeValueWarning):
        e.Img(src="foobar", width="50", height=15)
    with pytest.warns(exc.InvalidAttributeValueWarning):
        e.Img(src="foobar", width=50, height=15.5)
    with pytest.warns(exc.InvalidAttributeValueWarning):
        e.Input(size=0)
    with pytest.warns(exc.InvalidAttributeValueWarning):
        e.Link(rel=True)
    with pytest.warns(exc.InvalidAttributeValueWarning):
        e.Link(href=True)
    with pytest.warns(exc.InvalidAttributeValueWarning):
        e.Link(rel="prefetch preload prefetch")
    with pytest.warns(exc.InvalidAttributeValueWarning):
        e.A(accesskey="Ff g")
    with pytest.warns(exc.InvalidAttributeValueWarning):
        e.Iframe(sandbox="allow-forms allow-foobar")


def test_add_remove_class():
    d = e.Div()
    d.add_class("foo")
    assert d.get_classes() == ["foo"]
    d.add_class("bar", "baz")
    assert d.get_classes() == ["foo", "bar", "baz"]
    d.add_class("bar")
    assert d.get_classes() == ["foo", "bar", "baz"]
    d.add_class("foo", "qux")
    assert d.get_classes() == ["foo", "bar", "baz", "qux"]
    d.add_class("foo")
    assert d.get_classes() == ["foo", "bar", "baz", "qux"]
    d.add_class("bar", "quux", "quux")
    assert d.get_classes() == ["foo", "bar", "baz", "qux", "quux"]

    d.remove_class("bar")
    assert d.get_classes() == ["foo", "baz", "qux", "quux"]
    d.remove_class("foo", "qux")
    assert d.get_classes() == ["baz", "quux"]
    with pytest.raises(ValueError, match=r"not in list$"):
        d.remove_class("bar")
    with pytest.raises(ValueError, match=r"not in list$"):
        d.remove_class("quux", "quux")


def test_children():
    assert str(e.Div(e.Div())) == "<div><div></div></div>"
    assert str(e.Div("foo")) == "<div>foo</div>"
    assert str(e.Div("foo", e.Br(), "bar")) == "<div>foo<br>bar</div>"
    assert str(e.Div(44)) == "<div>44</div>"

    # Children in empty elements
    with pytest.raises(exc.EmptyElementChildrenError):
        e.Br("foo")
    with pytest.raises(exc.EmptyElementChildrenError):
        e.Br(e.Span())


def test_add_children():
    d = e.Div()
    d.add(e.Span())
    assert str(d) == "<div><span></span></div>"

    d = e.Div()
    d.add("foobar")
    assert str(d) == "<div>foobar</div>"


def test_insert_children():
    d = e.Div("foo", e.Br(), "bar")
    d.insert(2, "baz" + e.Br())
    assert str(d) == "<div>foo<br>baz<br>bar</div>"


def test_setitem():
    d: BaseElement = e.Div()
    d["class"] = "foo"
    assert str(d) == '<div class="foo"></div>'
    d = e.Br()
    d["data-foo"] = "bar"
    assert str(d) == '<br data-foo="bar">'

    d = e.Div(e.Span())
    d[0] = e.P()
    assert str(d) == "<div><p></p></div>"
    d = e.Div(e.P())
    d[0] = e.Br()
    assert str(d) == "<div><br></div>"

    d = e.Div(e.H1(), e.H2(), e.H3())
    d[1:] = [e.Span()]
    assert str(d) == "<div><h1></h1><span></span></div>"
    d = e.Div(e.H1(), e.H2(), e.H3())
    d[0:1] = [e.Span(), e.Div(), e.P()]
    assert str(d) == "<div><span></span><div></div><p></p><h2></h2><h3></h3></div>"
    with e.Div(e.H1(), e.H2(), e.H3(), e.H4(), e.H5()) as d:
        d[::2] = [e.Span()] * 3
    assert (
        str(d) == "<div><span></span><h2></h2><span></span><h4></h4><span></span></div>"
    )


def test_getitem():
    d: BaseElement = e.Div(class_="foo")
    assert d["class"] == "foo"
    d = e.Br(data_foo="bar")
    assert d["data-foo"] == "bar"

    d = e.Div(e.Span())
    assert isinstance(d[0], e.Span)
    d = e.Div(e.Br())
    assert isinstance(d[0], e.Br)

    d = e.Div(e.H1(), e.H2(), e.H3())
    assert [str(x) for x in d[:2]] == ["<h1></h1>", "<h2></h2>"]
    d = e.Div(e.H1(), e.H2(), e.H3())
    assert [str(x) for x in d[::2]] == ["<h1></h1>", "<h3></h3>"]


def test_delitem():
    d: BaseElement = e.Div(class_="foo")
    del d["class"]
    assert str(d) == "<div></div>"
    d = e.Br(data_foo="bar", data_baz="qux")
    del d["data-foo"]
    assert str(d) == '<br data-baz="qux">'

    d = e.Div(e.Span(), e.P())
    del d[0]
    assert str(d) == "<div><p></p></div>"
    d = e.Div(e.Br(), "foo", e.Br())
    del d[1]
    assert str(d) == "<div><br><br></div>"

    d = e.Div(e.H1(), e.H2(), e.H3())
    del d[:2]
    assert [str(x) for x in d] == ["<h3></h3>"]
    d = e.Div(e.H1(), e.H2(), e.H3())
    del d[::2]
    assert [str(x) for x in d] == ["<h2></h2>"]


def test_add():
    assert str(e.Div() + e.Div()) == "<div></div><div></div>"
    assert str(e.Div("foo") + "bar") == "<div>foo</div>bar"
    assert str("foo" + e.Div(class_="bar")) == 'foo<div class="bar"></div>'
    assert (
        str(e.Div("foo") + "bar" + e.Div(data_baz="qux"))
        == '<div>foo</div>bar<div data-baz="qux"></div>'
    )


def test_context_manager():
    with e.Div() as d:
        e.Span()
    assert str(d) == "<div><span></span></div>"

    with e.Div() as d:
        e.TextNode("foo")
    assert str(d) == "<div>foo</div>"

    with e.Div() as d:
        d.add(e.Div())
    assert str(d) == "<div><div></div></div>"

    with e.Div() as d:
        e.Div(e.P("foobar", e.Strong("baz")))
    assert str(d) == "<div><div><p>foobar<strong>baz</strong></p></div></div>"

    with e.Div(e.H1("title")) as d, e.P(), e.Span():
        e.B("foo", e.Br(), "bar")
    assert str(d) == "<div><h1>title</h1><p><span><b>foo<br>bar</b></span></p></div>"

    s: BaseElement
    with e.Div(e.H1()) as d, e.P() as p:
        with e.Span() as s, e.B():
            e.TextNode("foo")
            e.Br()
            e.RawTextNode("<bar>")
            d[0].add("t")
            p["id"] = "baz"
        s = e.Hr() + s
    assert (
        str(d)
        == '<div><h1>t</h1><p id="baz"><hr><span><b>foo<br><bar></b></span></p></div>'
    )


def test_prepend_doctype():
    assert str(e.Html()) == "<!DOCTYPE html><html></html>"
    assert str(e.Html(_prepend_doctype=True)) == "<!DOCTYPE html><html></html>"
    assert str(e.Html(_prepend_doctype=False)) == "<html></html>"

    assert str(e.P()) == "<p></p>"
    assert str(e.P(_prepend_doctype=True)) == "<!DOCTYPE html><p></p>"
    assert str(e.P(_prepend_doctype=False)) == "<p></p>"


def test_asyncio():
    async def main() -> None:
        async def task1() -> None:
            with e.Div() as divs:
                e.Div()
                await asyncio.sleep(1)
                with e.Div():
                    e.Div()
                    await asyncio.sleep(1)
                    e.Div()

            assert (
                str(divs) == "<div><div></div><div><div></div><div></div></div></div>"
            )

        async def task2() -> None:
            with e.Span() as spans:
                e.Span()
                await asyncio.sleep(0.7)
                with e.Span():
                    e.Span()
                    await asyncio.sleep(0.7)
                    e.Span()

            assert (
                str(spans)
                == "<span><span></span><span><span></span><span></span></span></span>"
            )

        await asyncio.gather(task1(), task2())

    # Random elements without context manager
    e.Div(e.Span(e.I()))
    asyncio.run(main())

    # Random elements with context manager
    with e.Div(), e.Span():
        e.I()
    asyncio.run(main())
