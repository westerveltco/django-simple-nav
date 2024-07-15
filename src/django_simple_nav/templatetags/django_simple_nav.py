from __future__ import annotations

import sys

from django import template
from django.http import HttpRequest
from django.template.base import Parser
from django.template.base import Token
from django.template.context import Context
from django.utils.module_loading import import_string

from django_simple_nav.nav import Nav

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override  # pyright: ignore[reportUnreachable]
register = template.Library()


@register.tag(name="django_simple_nav")
def do_django_simple_nav(parser: Parser, token: Token) -> DjangoSimpleNavNode:
    try:
        args = token.split_contents()[1:]
        if len(args) == 0:
            raise ValueError
    except ValueError as err:
        raise template.TemplateSyntaxError(
            f"{token.contents.split()[0]} tag requires arguments"
        ) from err

    nav = args[0]
    template_name = args[1] if len(args) > 1 else None

    return DjangoSimpleNavNode(nav, template_name)


class DjangoSimpleNavNode(template.Node):
    def __init__(self, nav: str, template_name: str | None) -> None:
        self.nav = template.Variable(nav)
        self.template_name = template.Variable(template_name) if template_name else None

    @override
    def render(self, context: Context) -> str:
        nav = self.get_nav(context)
        template_name = self.get_template_name(context)
        request = self.get_request(context)

        return nav.render(request, template_name)

    def get_nav(self, context: Context) -> Nav:
        try:
            nav: str | Nav = self.nav.resolve(context)
        except template.VariableDoesNotExist as err:
            raise template.TemplateSyntaxError(
                f"Variable does not exist: {err}"
            ) from err

        if isinstance(nav, str):
            try:
                nav_instance: Nav = import_string(nav)()
            except ImportError as err:
                raise template.TemplateSyntaxError(f"Failed to import: {nav}") from err
        else:
            nav_instance = nav

        if not hasattr(nav_instance, "render"):
            raise template.TemplateSyntaxError(
                "The object does not have a 'render' method."
            )

        return nav_instance

    def get_template_name(self, context: Context) -> str | None:
        try:
            template_name = (
                self.template_name.resolve(context) if self.template_name else None
            )
        except template.VariableDoesNotExist as err:
            raise template.TemplateSyntaxError(
                f"Variable does not exist: {err}"
            ) from err

        return template_name

    def get_request(self, context: Context) -> HttpRequest:
        request = context.get("request", None)

        if not request:
            raise template.TemplateSyntaxError(
                f"`request` not found in template context: {context}"
            )
        elif not isinstance(request, HttpRequest):
            raise template.TemplateSyntaxError(
                f"`request` not a valid `HttpRequest`: {request}"
            )

        return request
