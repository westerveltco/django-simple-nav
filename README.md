# django-simple-nav

[![PyPI](https://img.shields.io/pypi/v/django-simple-nav)](https://pypi.org/project/django-simple-nav/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-simple-nav)
![Django Version](https://img.shields.io/badge/django-3.2%20%7C%204.2%20%7C%205.0-%2344B78B?labelColor=%23092E20)
<!-- https://shields.io/badges -->
<!-- django-3.2 | 4.2 | 5.0-#44B78B -->
<!-- labelColor=%23092E20 -->

`django-simple-nav` is a Python/Django application designed to simplify the integration of navigation and menu bars in your Django projects. With a straightforward API and customizable options, you can easily add and manage navigational elements in your web applications.

## Requirements

- Python 3.8, 3.9, 3.10, 3.11, 3.12
- Django 3.2, 4.2, 5.0

## Getting Started

1. Install the package from PyPI:

   ```bash
   python -m pip install django-simple-nav
   ```

2. **Add to Installed Apps**:

   After installation, add `django_simple_nav` to your `INSTALLED_APPS` in your Django settings:

   ```python
   INSTALLED_APPS = [
       ...,
       "django_simple_nav",
       ...,
   ]
   ```

## Usage

1. **Create a navigation definition**:

   Define your navigation structure in a Python file. Here's an example configuration:

   ```python
   from django_simple_nav.nav import Nav
   from django_simple_nav.nav import NavGroup
   from django_simple_nav.nav import NavItem


   class MainNav(Nav):
       template_name = "main_nav.html"
       items = [
           NavItem(title="Relative URL", url="/relative-url"),
           NavItem(title="Absolute URL", url="https://example.com/absolute-url"),
           NavItem(title="Internal Django URL by Name", url="fake-view"),
           NavGroup(
               title="Group",
               url="/group",
               items=[
                   NavItem(title="Relative URL", url="/relative-url"),
                   NavItem(title="Absolute URL", url="https://example.com/absolute-url"),
                   NavItem(title="Internal Django URL by Name", url="fake-view"),
               ],
           ),
           NavItem(
               title="is_authenticated Item", url="#", permissions=["is_authenticated"]
           ),
           NavItem(title="is_staff Item", url="#", permissions=["is_staff"]),
           NavItem(title="is_superuser Item", url="#", permissions=["is_superuser"]),
           NavItem(
               title="myapp.django_perm Item", url="#", permissions=["myapp.django_perm"]
           ),
       ]
   ```

2. **Integrate Navigation in Templates**:

   Use the `django_simple_nav` template tag in your Django templates where you want to display the navigation.

   For example:

   ```html
   {% load django_simple_nav %}
   ...
   <nav>
       {% django_simple_nav 'path.to.MainNav' %}
   </nav>
   ...
   ```

After configuring your navigation, you can use it across your Django project by calling the `django_simple_nav` template tag in your templates.
This tag dynamically renders navigation based on your defined structure, ensuring a consistent and flexible navigation experience throughout your application.

## Documentation

Please refer to the [documentation](https://django-simple-nav.westervelt.dev/) for more information.

## License

`django-simple-nav` is licensed under the MIT license. See the [`LICENSE`](LICENSE) file for more information.
