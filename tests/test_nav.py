from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.utils.module_loading import import_string
from model_bakery import baker

from django_simple_nav.nav import Nav
from django_simple_nav.nav import NavGroup
from django_simple_nav.nav import NavItem

pytestmark = pytest.mark.django_db


class TestNav(Nav):
    items = [
        NavItem(title="Relative URL", url="/relative-url"),
        NavItem(title="Absolute URL", url="https://example.com/absolute-url"),
        NavGroup(
            title="Group",
            url="/group",
            items=[
                NavItem(title="Relative URL", url="/relative-url"),
                NavItem(title="Absolute URL", url="https://example.com/absolute-url"),
            ],
        ),
        NavItem(
            title="is_authenticated Item", url="#", permissions=["is_authenticated"]
        ),
        NavItem(title="is_staff Item", url="#", permissions=["is_staff"]),
        NavItem(title="is_superuser Item", url="#", permissions=["is_superuser"]),
        NavGroup(
            title="is_authenticated Group",
            permissions=["is_authenticated"],
            items=[NavItem(title="Test Item", url="#")],
        ),
        NavGroup(
            title="is_staff Group",
            permissions=["is_staff"],
            items=[NavItem(title="Test Item", url="#")],
        ),
        NavGroup(
            title="is_superuser Group",
            permissions=["is_superuser"],
            items=[NavItem(title="Test Item", url="#")],
        ),
    ]
    template_name = "tests/test_nav.html"


@pytest.fixture
def req():
    return HttpRequest()


@pytest.fixture
def user():
    return baker.make(get_user_model())


def test_dotted_path_loading():
    nav = import_string("tests.test_nav.TestNav")

    assert len(nav.items) == 9
    assert nav.template_name == "tests/test_nav.html"


def test_nav_render(req, user):
    req.user = user
    rendered_template = TestNav.render(req)

    assert "Relative URL" in rendered_template
    assert "/relative-url" in rendered_template
    assert "Absolute URL" in rendered_template
    assert "https://example.com/absolute-url" in rendered_template
    assert "Group" in rendered_template


def test_dotted_path_rendering(req, user):
    req.user = user
    nav = import_string("tests.test_nav.TestNav")

    assert nav.render(req)
