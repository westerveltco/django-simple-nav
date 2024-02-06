from __future__ import annotations

from django import template
from django.template import Context
from django.utils.module_loading import import_string

register = template.Library()


@register.simple_tag(takes_context=True)
def django_simple_nav(context: Context, nav_path: str) -> str:
    nav = import_string(nav_path)
    return nav.render_from_request(request=context["request"])
