# Changelog

## [Unreleased]
### Changed
- Elements can be subscripted using slices, returning (or replacing/deleting) a slice of
its children.

## [0.1.1] - 2021-11-09
### Added
- Treat `BaseElement` as a simple container, omitting the start and end tags when
rendering.
- Implement `BaseElement.insert()` to add children at a given position.
### Removed
- `BaseElement.children` and `BaseElement.attributes` are no longer public.

## [0.1.0] - 2021-11-08
- Initial release
