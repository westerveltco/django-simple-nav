# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project attempts to adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
## [${version}]
### Added - for new features
### Changed - for changes in existing functionality
### Deprecated - for soon-to-be removed features
### Removed - for now removed features
### Fixed - for any bug fixes
### Security - in case of vulnerabilities
[${version}]: https://github.com/westerveltco/django-simple-nav/releases/tag/v${version}
-->

## [Unreleased]

## [0.5.0]

### Added

- An number of examples have been added to a new `example` directory. These examples are intended to demonstrate various ways how to use `django-simple-nav` in a Django project and include basic usage and usage with some popular CSS frameworks.

### Changed

- `check_item_permission` now takes a `request` argument instead of a `user` argument.

### Fixed

- `check_item_permission` now explicitly checks if `django.contrib.auth` is installed before attempting to check if a user has a permission. If it is not, it will return `True` by default and log a warning.
- The `request` object is now passed to `render_to_string` when rendering the navigation template, so that the `request` object is available in the template context. This allows for nesting the `django_simple_nav` template tag within another `django_simple_nav` template tag, and having the `request` object available in the nested template.

## [0.4.0]

### Added

- The `Nav` class now has two new methods: `get_context_data` and `render`. These methods are used to render the navigation to a template. These new methods give greater flexibility for customizing the rendering of the navigation, as they can be overridden when defining a new `Nav`.
  - `Nav.get_context_data` method takes a Django `HttpRequest` object and returns a dictionary of context data that can be used to render the navigation to a template.
  - `Nav.render` method takes a Django `HttpRequest` object and an optional template name and renders the navigation to a template, returning the rendered template as a string.

### Removed

- `Nav.render_from_request` method has been removed. This was only used within the template tag to render a `Nav` template from an `HttpRequest` object. It has been removed in favor of the new `Nav.get_context_data` and `Nav.render` methods.

## [0.3.0]

### Added

- `NavGroup` and `NavItem` now has a new `extra_context` attribute. This allows for passing additional context to the template when rendering the navigation, either via the extra attribute (`item.foo`) or the `extra_context` attribute itself (`item.extra_context.foo`).

### Changed

- Now using v2024.13 of `django-twc-package`.

### Fixed

- `RenderedNavItem.items` property now correctly returns a list of `RenderedNavItem` objects, rather than a list of `NavItem` objects. This fixes a bug where the properties that should be available (e.g. `active`, `url`, etc.) were not available when iterating over the `RenderedNavItem.items` list if the item was a `NavGroup` object with child items.

## [0.2.0]

### Added

- The `django_simple_nav` template tag can now take an instance of a `Nav` class, in addition to a `Nav` dotted path string. This should give greater flexibility for rendering a `Nav`, as it can now be overridden on a per-view/template basis.

### Changed

- Now using [`django-twc-package`](https://github.com/westerveltco/django-twc-package) template for repository and package structure.

## [0.1.0]

Initial release! 🎉

### Added

- A group of navigation classes -- `Nav`, `NavGroup`, and `NavItem` -- that can be used together to build a simple navigation structure.
  - `Nav` is the main container for a navigation structure.
  - `NavGroup` is a container for a group of `NavItem` objects.
  - `NavItem` is a single navigation item.
- A `django_simple_nav` template tag that renders a `Nav` object to a template. The template tag takes a string represented the dotted path to a `Nav` object and renders it to the template.
- Navigation item urls can be either a URL string (e.g. `https://example.com/about/` or `/about/`) or a Django URL name (e.g. `about-view`). When rendering out to the template, the template tag will resolve the URL name to the actual URL.
- Navigation items also can take a list of permissions to control the visibility of the item. The permissions can be user attributes (e.g. `is_staff`, `is_superuser`, etc.) or a specific permission (e.g. `auth.add_user`).
- Navigation items are marked as `active` if the current request path matches the item's URL. This is can be useful for highlighting the current page in the navigation.
- A `Nav` object's template can either be set as a class attribute (`template_name`) or passed in as a keyword argument when rendering the template tag. This allows for easy customization of the navigation structure on a per-template or per-view basis.
- Initial documentation.
- Initial tests.
- Initial CI/CD (GitHub Actions).

### New Contributors

- Josh Thomas <josh@joshthomas.dev> (maintainer)
- Jeff Triplett [@jefftriplett](https://github.com/jefftriplett)

[unreleased]: https://github.com/westerveltco/django-simple-nav/compare/v0.5.0...HEAD
[0.1.0]: https://github.com/westerveltco/django-simple-nav/releases/tag/v0.1.0
[0.2.0]: https://github.com/westerveltco/django-simple-nav/releases/tag/v0.2.0
[0.3.0]: https://github.com/westerveltco/django-simple-nav/releases/tag/v0.3.0
[0.4.0]: https://github.com/westerveltco/django-simple-nav/releases/tag/v0.4.0
[0.5.0]: https://github.com/westerveltco/django-simple-nav/releases/tag/v0.5.0
