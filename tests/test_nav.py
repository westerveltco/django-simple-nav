from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.module_loading import import_string
from model_bakery import baker

from .navs import DummyNav

pytestmark = pytest.mark.django_db


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
        (get_user_model(), 10),
    ],
)
def test_nav_render(user, expected_count, req, count_anchors):
    if not isinstance(user, AnonymousUser):
        user = baker.make(user)

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
        ("is_superuser", 16),
        ("tests.dummy_perm", 13),
    ],
)
def test_nav_render_with_permissions(req, count_anchors, permission, expected_count):
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
