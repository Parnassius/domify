# Changelog

## [Unreleased]

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
