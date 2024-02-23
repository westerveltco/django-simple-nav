from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.module_loading import import_string
from model_bakery import baker

from django_simple_nav.nav import NavGroup
from django_simple_nav.nav import NavItem
from django_simple_nav.nav import RenderedNavItem
from tests.navs import DummyNav
from tests.utils import count_anchors

pytestmark = pytest.mark.django_db


def test_init():
    nav = DummyNav

    assert nav.template_name == "tests/dummy_nav.html"
    assert len(nav.items) == 12

    for item in nav.items:
        assert item.title


@pytest.mark.parametrize(
    "nav, template_name, expected_count",
    [
        ("tests.navs.DummyNav", "tests/dummy_nav.html", 12),
    ],
)
def test_dotted_path_loading(nav, template_name, expected_count):
    nav = import_string(nav)

    assert nav.template_name == template_name
    assert len(nav.items) == expected_count


@pytest.mark.parametrize(
    "user, expected_count",
    [
        (AnonymousUser(), 7),
        (None, 10),
    ],
)
def test_nav_render(user, expected_count, req):
    if not isinstance(user, AnonymousUser):
        user = baker.make(get_user_model())

    req.user = user

    rendered_template = DummyNav().render(req)

    assert count_anchors(rendered_template) == expected_count


def test_dotted_path_nav_render(req):
    req.user = baker.make(get_user_model())

    nav = import_string("tests.navs.DummyNav")

    assert nav().render(req)


@pytest.mark.parametrize(
    "permission, expected_count",
    [
        ("", 10),  # regular authenticated user
        ("is_staff", 13),
        ("is_superuser", 19),
        ("tests.dummy_perm", 13),
    ],
)
def test_nav_render_with_permissions(req, permission, expected_count):
    user = baker.make(get_user_model())

    if permission == "tests.dummy_perm":
        dummy_perm = baker.make(
            "auth.Permission",
            codename="dummy_perm",
            name="Dummy Permission",
            content_type=baker.make("contenttypes.ContentType", app_label="tests"),
        )
        user.user_permissions.add(dummy_perm)
    else:
        setattr(user, permission, True)

    user.save()

    req.user = user
    rendered_template = DummyNav().render(req)

    assert count_anchors(rendered_template) == expected_count


def test_nav_render_with_template_name(req):
    req.user = AnonymousUser()

    rendered_template = DummyNav().render(req, "tests/alternate.html")

    assert "This is an alternate template." in rendered_template


def test_extra_context(req):
    item = NavItem(
        title="Test",
        url="/test/",
        extra_context={"foo": "bar"},
    )

    rendered_item = RenderedNavItem(item, req)

    assert rendered_item.foo == "bar"


def test_extra_context_with_no_extra_context(req):
    item = NavItem(
        title="Test",
        url="/test/",
    )

    rendered_item = RenderedNavItem(item, req)

    with pytest.raises(AttributeError):
        assert rendered_item.foo == "bar"


def test_extra_context_shadowing(req):
    item = NavItem(
        title="Test",
        url="/test/",
        extra_context={"title": "Shadowed"},
    )

    rendered_item = RenderedNavItem(item, req)

    assert rendered_item.title == "Test"


def test_extra_context_iteration(req):
    item = NavItem(
        title="Test",
        url="/test/",
        extra_context={"foo": "bar", "baz": "qux"},
    )

    rendered_item = RenderedNavItem(item, req)

    assert rendered_item.extra_context == {"foo": "bar", "baz": "qux"}
    for key, value in rendered_item.extra_context.items():
        assert getattr(rendered_item, key) == value


def test_extra_context_builtins(req):
    item = NavGroup(
        title="Test",
        items=[
            NavItem(
                title="Test",
                url="/test/",
                permissions=["is_staff"],
                extra_context={"foo": "bar"},
            ),
        ],
        url="/test/",
        permissions=["is_staff"],
        extra_context={"baz": "qux"},
    )

    rendered_item = RenderedNavItem(item, req)

    assert rendered_item.title == "Test"
    assert rendered_item.url == "/test/"
    assert rendered_item.permissions == ["is_staff"]
    assert rendered_item.extra_context == {"baz": "qux"}
    assert rendered_item.baz == "qux"

    assert rendered_item.items is not None
    assert len(rendered_item.items) == 1

    rendered_group_item = rendered_item.items[0]

    assert rendered_group_item.title == "Test"
    assert rendered_group_item.url == "/test/"
    assert rendered_group_item.permissions == ["is_staff"]
    assert rendered_group_item.extra_context == {"foo": "bar"}
    assert rendered_group_item.foo == "bar"


def test_get_context_data(req):
    req.user = baker.make(get_user_model())

    context = DummyNav().get_context_data(req)

    assert context["items"]


def test_get_context_data_override(req):
    class OverrideNav(DummyNav):
        def get_context_data(self, request):
            return {"foo": "bar"}

    req.user = baker.make(get_user_model())

    context = OverrideNav().get_context_data(req)

    assert context["foo"] == "bar"


def test_get_context_data_override_render(req):
    class OverrideNav(DummyNav):
        def get_context_data(self, request):
            return {"foo": "bar"}

    req.user = baker.make(get_user_model())

    rendered_template = OverrideNav().render(req)

    assert count_anchors(rendered_template) == 0


def test_rendered_nav_item_active(req):
    item = NavItem(title="Test", url="/test/")
    rendered_item = RenderedNavItem(item, req)

    assert rendered_item.active is False

    req.path = "/test/"
    rendered_item = RenderedNavItem(item, req)

    assert rendered_item.active is True


def test_rendered_nav_item_active_no_url(req):
    item = NavGroup(title="Test", items=[NavItem(title="Test", url="/test/")])

    rendered_item = RenderedNavItem(item, req)

    assert rendered_item.active is False
