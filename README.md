# domify

HTML generator using pure Python.

[![PyPI](https://img.shields.io/pypi/v/domify)](https://pypi.org/project/domify/)
[![PyPI - Status](https://img.shields.io/pypi/status/dominate)](https://pypi.org/project/domify/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/domify)](https://pypi.org/project/domify/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests status](https://img.shields.io/github/workflow/status/Parnassius/domify/main/main?event=push&label=tests)](https://github.com/Parnassius/domify/actions?query=workflow%3Amain)
[![Codecov](https://img.shields.io/codecov/c/gh/Parnassius/dominate/main?token=RYDAXOWCUS)](https://codecov.io/gh/Parnassius/dominate)
[![PyPI - License](https://img.shields.io/pypi/l/domify)](https://github.com/Parnassius/domify/blob/main/LICENSE)

Simple example:
```python
from domify import html_elements as e

html = e.Html(lang="en")
with html:
    with e.Head():
        e.Meta(charset="utf-8")
        e.Title("Example page")

    with e.Body():
        e.H1("Hello world")
        e.P("Lorem ipsum ", e.I("dolor sit amet"))

print(str(html))
```

HTML output (formatted for legibility):
```html
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Example page</title>
  </head>
  <body>
    <h1>Hello world</h1>
    <p>Lorem ipsum <i>dolor sit amet</i></p>
  </body>
</html>
```

Note: every example on this page assumes domify has already been imported:
```python
from domify import html_elements as e
```

`domify.html_elements` contains a class for each HTML element, with the first letter
converted to uppercase:
```python
p = e.P("Lorem ipsum dolor sit amet")
print(str(p))
```
```html
<p>Lorem ipsum dolor sit amet</p>
```

You can pass strings or additional elements as positional arguments, and they will be
treated as children:
```python
p = e.P("Lorem ipsum dolor sit amet", e.Br(), "consectetur adipiscing elit.")
print(str(p))
```
```html
<p>
  Lorem ipsum dolor sit amet
  <br>
  consectetur adipiscing elit.
</p>
```

Attributes can be passed as keyword arguments, optionally appending an underscore to
attributes which are reserved keywords in python (for example `class`). Integers and
floats are automatically converted to strings, while additional underscores are replaced
with dashes (especially useful for `data` and `aria` attributes):
```python
btn = e.Button("Click!", type="submit", class_="someclass", data_order=155)
print(str(btn))
```
```html
<button type="submit" class="someclass" data-order="155">Click!</button>
```

HTML5 boolean attributes accept a boolean value instead:
```python
text_input = e.Input(type="text", required=True, disabled=False)
print(str(text_input))
```
```html
<input type="text" required>
```

Attributes can be added or modified by subscripting an element object:
```python
html = e.Html()
html["lang"] = "en"
print(str(html))
```
```html
<html lang="en"></html>
```

Children can be modified (but not added) by subscripting as well:
```python
p = e.P("Text node 1", e.Br(), "Text node 2")
p[0] = "Text node 3"
p[1] = t.Hr()
print(str(p))
```
```html
<p>
  Text node 3
  <hr>
  Text node 2
</p>
```

The `del` keyword can be used to delete both attributes and children:
```python
div = e.Div("foo", e.Br(), "bar", id="someid", class_="someclass")
del div["class"]
del div[1]
print(str(div))
```
```html
<div id="someid">foobar</div>
```

`add_class` and `remove_class` can be used to manage classes:
```python
div = e.Div(class_="some-class some-other-class")
div.remove_class("some-class")
div.add_class("third-class")
print(str(div))
```
```html
<div class="some-other-class third-class"></div>
```

Children can be added using the `add` method, which return the newly added element:
```python
p = e.P()
span = p.add(e.Span())
span.add("First line")
span.add(e.Br())
span.add("Second line")
print(str(p))
```
```html
<p>
  <span>
    First line
    <br>
    Second line
  </span>
</p>
```

Context managers can be used to add child elements too:
```python
with e.Select() as select:
    e.Option("Option 1", value=1)
    e.Option("Option 2", value=2)
    e.Option("Option 3", value=3)
print(str(select))
```
```html
<select>
  <option value="1">Option 1</option>
  <option value="2">Option 2</option>
  <option value="3">Option 3</option>
</select>
```

The `+` operator can be used to concatenate multiple elements and/or strings:
```python
username = "Username: " + e.Input(type="text", name="username")
password = "Password: " + e.Input(type="password", name="password")
login_form = e.Label(username) + e.Label(password)
login_form += e.Button("Login", type="submit")
print(str(login_form))
```
```html
<label>Username: <input type="text" name="username"></label>
<label>Password: <input type="password" name="password"></label>
<button type="submit">Login</button>
```

Text nodes can be created using `TextNode` (this is usually not required, since strings
are automatically coverted):
```python
with e.P() as p:
    e.TextNode("Lorem ipsum")
print(str(p))
```
```html
<p>Lorem ipsum</p>
```

`RawTextNode` can be used to add strings without escaping:
```python
with e.P() as p:
    e.TextNode("<i>TextNode</i>")
    e.Br()
    e.RawTextNode("<i>RawTextNode</i>")
print(str(p))
```
```html
<p>
  &lt;i&gt;TextNode&lt;/i&gt;
  <br>
  <i>RawTextNode</i>
</p>
```
