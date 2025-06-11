from __future__ import annotations

from typing import cast

from django.utils.module_loading import import_string
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
            raise TemplateRuntimeError(str(err)) from err

    try:
        if template_name is None:
            template_name = cast(Nav, nav).template_name
        if template_name is None:
            raise TemplateRuntimeError("Navigation object has no template")
        request = context['request']
        new_context = {
            'request': request,
            **cast(Nav, nav).get_context_data(request)
        }
    except Exception as err:
        raise TemplateRuntimeError(str(err)) from err

    return loader.load(context.environment, template_name).render(new_context)
