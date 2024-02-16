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

[unreleased]: https://github.com/westerveltco/django-simple-nav/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/westerveltco/django-simple-nav/releases/tag/v0.1.0
