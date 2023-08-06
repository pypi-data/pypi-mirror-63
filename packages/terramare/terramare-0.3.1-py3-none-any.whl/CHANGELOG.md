# Changelog

This file documents all notable changes to the project.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Commit messages and changelog entries should follow the [Conventional Commits](https://www.conventionalcommits.org) specification.

## [Unreleased]

## [0.3.1] - 2020-03-16

### Changed

- chore: Specify license in package metadata

## [0.3.0] - 2020-03-15

### Added

- feat: Add `deserialize_into` keyword arguments:
  - `handle_exception_types`, allowing `terramare` to catch and handle custom exceptions, e.g.
    those raised by additional validation on a class;
  - `handle_reentrancy`, controlling how `terramare` handles deserialzation targets that themselves
    call into `terramare`.
- feat: Add support for variadic tuples
- feat: Add support for `functools.partial`
- docs: Usage guide

### Changed

- refactor: Extract common deserializer logic into "deserializer combinators" and use throughout.
- improvement: Improve class deserialization error messages

### Fixed

- docs: Document public API only

### Removed

- refactor!: Remove `create_deserializer` and `create_deserializer_factory` functions from public API

## [0.2.0] - 2020-02-09

### Added

- test: Test for simple forward reference type
- feat: Deserialize enum types
- feat: Optionally coerce strings to `int`, `float`, or `bool` where the latter are required
- feat: Deserialize `Set`, `FrozenSet`, `Iterable` and `Iterator` types

### Changed

- chore(infra): Enable linters in vscode
- improvement: Improve handling of forward references
- improvement: Improve error messages
- feat: Create class deserializers in more situations

### Fixed

- fix: Fix `AttributeError` on querying description of `Any` deserializer
- fix: Fix type name in `ClassDeserializerFactoryError`
- fix: Fix inadvertantly persisting state between `CachingDeserializerFactory` instances
- fix: Raise correct error when re-raising `InternalDeserializationError`

## [0.1.0] - 2019-10-11

### Added

- Initial version

[Unreleased]: https://gitlab.com/tomwatson1024/terramare/compare/0.2.0...master
[0.2.0]: https://gitlab.com/tomwatson1024/terramare/compare/0.1.0...0.2.0
[0.1.0]: https://gitlab.com/tomwatson1024/terramare/-/tags/0.1.0
