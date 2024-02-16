from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.module_loading import import_string
from model_bakery import baker

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
    rendered_template = DummyNav.render_from_request(req)

    assert count_anchors(rendered_template) == expected_count


def test_dotted_path_rendering(req):
    req.user = baker.make(get_user_model())
    nav = import_string("tests.navs.DummyNav")

    assert nav.render_from_request(req)


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
    rendered_template = DummyNav.render_from_request(req)

    assert count_anchors(rendered_template) == expected_count


def test_nav_render_from_request_with_template_name(req):
    req.user = AnonymousUser()

    rendered_template = DummyNav.render_from_request(req, "tests/alternate.html")

    assert "This is an alternate template." in rendered_template
