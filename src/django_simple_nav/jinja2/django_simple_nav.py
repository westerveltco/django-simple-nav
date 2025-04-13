from __future__ import annotations

from typing import cast

from django.utils.module_loading import import_string
from jinja2 import Template
from jinja2 import TemplateRuntimeError
from jinja2 import pass_context
from jinja2.runtime import Context

from django_simple_nav.nav import Nav


@pass_context
def django_simple_nav(
    context: Context, nav: str | Nav, template_name: str | None = None
) -> str:
    """Jinja binding for `django_simple_nav`"""
    if (loader := context.environment.loader) is None:
        raise TemplateRuntimeError("No template loader in Jinja2 environment")

    if type(nav) is str:
        try:
            nav = import_string(nav)()
        except ImportError as err:
            msg = f"Variable does not exist: {err}"
            raise TemplateRuntimeError(msg) from err

    if template_name is None:
        template_name = cast(Nav, nav).template_name
    if template_name is None:
        raise TemplateRuntimeError("Navigation object has no template")

    template: Template = loader.load(context.environment, template_name)
    return template.render(items=cast(Nav, nav).items)
