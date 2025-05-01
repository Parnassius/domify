# Changelog

## [Unreleased]

## [0.4.6] - 2025-05-01
### Changed
- Bump the minimum Python version to 3.9.

### HTML spec
- Add the `oncommand` global attribute.
- Add the `command` and `commandfor` attributes to the `button` element.
- Add the `closedby` attribute to the `dialog` element.
- Add the `alpha` and `colorspace` attributes to the `input` element.
- Add the `shadowrootcustomelementregistry` attribute to the `template` element.

## [0.4.5] - 2024-09-30
### Changed
- Bump the minimum Python version to 3.8.

### HTML spec
- Add the `autocorrect`, `writingsuggestions`, `onbeforeinput`, `onpagereveal` and
`onpageswap` global attributes.
- Add the empty string value to the `spellcheck` global attribute.
- Add the `shadowrootclonable` and `shadowrootserializable` attributes to the `template`
element.

## [0.4.4] - 2024-01-01
### HTML spec
- Add the `name` attribute to the `details` element.
- Add the `shadowrootmode` and `shadowrootdelegatesfocus` to the `template` element.
- Add the `onpagereveal` attribute to the `body` element.

## [0.4.3] - 2023-08-05
### HTML spec
- Remove the incorrect attributes `height`, `media` and `width` attributes from
`picture` elements.

## [0.4.2] - 2023-05-27
### HTML spec
- Add the `fetchpriority` attribute to the `img`, `link` and `script` elements.
- Add the `plaintext-only` value to the `contenteditable` global attribute.
- Add the `search` element.
- Replace the `popoverhidetarget`, `popovershowtarget` and `popovertoggletarget`
attributes of the `button` and `input` elements with `popovertarget` and
`popovertargetaction`.

## [0.4.1] - 2023-02-03
### HTML spec
- Add the `popover` and `onbeforetoggle` global attributes.
- Add the `popoverhidetarget`, `popovershowtarget` and `popovertoggletarget` attributes
to `button` and `input` elements.
- Add the `dir` attribute to `bdo` elements.
- Add the `height` attribute to `picture` elements.

## [0.4.0] - 2022-12-10
### Added
- Explicitly support Python 3.11.
### Changed
- Bump the minimum Python version from 3.7.0 to 3.7.2.
### HTML spec
- Add the `onscrollend` global attribute.
- Update the allowed values of the `hidden` global attribute.

## [0.3.0] - 2022-05-05
### Changed
- Remove upper bound on `typing-extensions`.
### HTML spec
- Add the `blocking` attribute to `link`, `script` and `style` elements.
- Add the `inert` and `onbeforematch` global attributes.
- Update the allowed values of the `sandbox` attributes of `iframe` elements.
- Remove the deprecated `param` element.

## [0.2.0] - 2021-12-09
### Added
- Automatically prepend a `DOCTYPE` declaration to `<html>` elements. This behaviour can
be overridden using the `_prepend_doctype` keyword argument.
### Changed
- Elements can be subscripted using slices, returning (or replacing/deleting) a slice of
their children.
- Attribute validators follow a different naming scheme (for example
`attribute_validators.bool_validator` is now `validators.attribute_bool`).

## [0.1.1] - 2021-11-09
### Added
- Treat `BaseElement` as a simple container, omitting the start and end tags when
rendering.
- Implement `BaseElement.insert()` to add children at a given position.
### Removed
- `BaseElement.children` and `BaseElement.attributes` are no longer public.

## [0.1.0] - 2021-11-08
- Initial release
