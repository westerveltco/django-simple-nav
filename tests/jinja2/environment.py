"""Sets up a reasonably minimal Jinja2 environment for testing"""

from __future__ import annotations

from jinja2 import Environment
from jinja2 import FileSystemLoader

from django_simple_nav.jinja2.django_simple_nav import django_simple_nav

environment = Environment(loader=FileSystemLoader("tests/templates/tests/jinja2/"))
environment.globals.update({"django_simple_nav": django_simple_nav})
