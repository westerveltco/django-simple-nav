from __future__ import annotations

from django.contrib.auth.models import AnonymousUser
from django.template import Context
from django.template import Template


def test_django_simple_nav_templatetag(req, count_anchors):
    template = Template(
        "{% load django_simple_nav %} {% django_simple_nav 'tests.navs.DummyNav' %}"
    )
    req.user = AnonymousUser()

    rendered_template = template.render(Context({"request": req}))

    assert count_anchors(rendered_template) == 7


def test_templatetag_with_template_name(req):
    template = Template(
        "{% load django_simple_nav %} {% django_simple_nav 'tests.navs.DummyNav' 'tests/alternate.html' %}"
    )
    req.user = AnonymousUser()

    rendered_template = template.render(Context({"request": req}))

    assert "This is an alternate template." in rendered_template
