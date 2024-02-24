from __future__ import annotations

from django import template
from django.utils.module_loading import import_string

register = template.Library()


@register.tag(name="django_simple_nav")
def do_django_simple_nav(parser, token):
    try:
        _, args = token.contents.split(None, 1)
    except ValueError as err:
        raise template.TemplateSyntaxError(
            f"{token.contents.split()[0]} tag requires arguments"
        ) from err

    args = args.split()
    nav = args[0]
    template_name = args[1] if len(args) > 1 else None

    return DjangoSimpleNavNode(nav, template_name)


class DjangoSimpleNavNode(template.Node):
    def __init__(self, nav, template_name):
        self.nav = template.Variable(nav)
        self.template_name = template.Variable(template_name) if template_name else None

    def render(self, context):
        try:
            nav = self.nav.resolve(context)
            template_name = (
                self.template_name.resolve(context) if self.template_name else None
            )
        except template.VariableDoesNotExist as err:
            raise template.TemplateSyntaxError(
                f"Variable does not exist: {err}"
            ) from err

        if isinstance(nav, str):
            try:
                nav_instance = import_string(nav)()
            except ImportError as err:
                raise template.TemplateSyntaxError(f"Failed to import: {nav}") from err
        else:
            nav_instance = nav

        if not hasattr(nav_instance, "render"):
            raise template.TemplateSyntaxError(
                "The object does not have a 'render' method."
            )

        return nav_instance.render(context["request"], template_name)
