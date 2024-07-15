from __future__ import annotations

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.test import override_settings
from model_bakery import baker

from django_simple_nav.nav import NavGroup
from django_simple_nav.nav import NavItem

pytestmark = pytest.mark.django_db


# anonymous user
@pytest.mark.parametrize(
    "item,expected",
    [
        # nav item
        (NavItem("Test", "/test"), True),
        (NavItem("Test", "/test", permissions=["is_authenticated"]), False),
        (NavItem("Test", "/test", permissions=["is_staff"]), False),
        (NavItem("Test", "/test", permissions=["is_superuser"]), False),
        (NavItem("Test", "/test", permissions=["tests.dummy_perm"]), False),
        # nav group with url
        (NavGroup("Test", "/test", items=[]), True),
        (NavGroup("Test", "/test", items=[], permissions=["is_authenticated"]), False),
        (NavGroup("Test", "/test", items=[], permissions=["is_staff"]), False),
        (NavGroup("Test", "/test", items=[], permissions=["is_superuser"]), False),
        (NavGroup("Test", "/test", items=[], permissions=["tests.dummy_perm"]), False),
        # nav group with no url and items with perms
        (NavGroup("Test", items=[NavItem("Test", "/test")]), True),
        (
            NavGroup(
                "Test",
                items=[NavItem("Test", "/test", permissions=["is_authenticated"])],
            ),
            False,
        ),
        (
            NavGroup(
                "Test", items=[NavItem("Test", "/test", permissions=["is_staff"])]
            ),
            False,
        ),
        (
            NavGroup(
                "Test", items=[NavItem("Test", "/test", permissions=["is_superuser"])]
            ),
            False,
        ),
        (
            NavGroup(
                "Test",
                items=[NavItem("Test", "/test", permissions=["tests.dummy_perm"])],
            ),
            False,
        ),
        # multiple perms
        (NavItem("Test", "/test", permissions=["is_authenticated", "is_staff"]), False),
        (
            NavItem(
                "Test",
                "/test",
                permissions=["is_authenticated", "is_staff", "is_superuser"],
            ),
            False,
        ),
    ],
)
def test_check_item_permissions_anonymous(item, expected, req):
    req.user = AnonymousUser()

    assert item.check_permissions(req) == expected


# authenticated user
@pytest.mark.parametrize(
    "item,expected",
    [
        # nav item
        (NavItem("Test", "/test"), True),
        (NavItem("Test", "/test", permissions=["is_authenticated"]), True),
        (NavItem("Test", "/test", permissions=["is_staff"]), False),
        (NavItem("Test", "/test", permissions=["is_superuser"]), False),
        (NavItem("Test", "/test", permissions=["tests.dummy_perm"]), False),
        # nav group with url
        (NavGroup("Test", "/test", items=[]), True),
        (NavGroup("Test", "/test", items=[], permissions=["is_authenticated"]), True),
        (NavGroup("Test", "/test", items=[], permissions=["is_staff"]), False),
        (NavGroup("Test", "/test", items=[], permissions=["is_superuser"]), False),
        (NavGroup("Test", "/test", items=[], permissions=["tests.dummy_perm"]), False),
        # nav group with no url and items with perms
        (NavGroup("Test", items=[NavItem("Test", "/test")]), True),
        (
            NavGroup(
                "Test",
                items=[NavItem("Test", "/test", permissions=["is_authenticated"])],
            ),
            True,
        ),
        (
            NavGroup(
                "Test", items=[NavItem("Test", "/test", permissions=["is_staff"])]
            ),
            False,
        ),
        (
            NavGroup(
                "Test", items=[NavItem("Test", "/test", permissions=["is_superuser"])]
            ),
            False,
        ),
        (
            NavGroup(
                "Test",
                items=[NavItem("Test", "/test", permissions=["tests.dummy_perm"])],
            ),
            False,
        ),
        # multiple perms
        (NavItem("Test", "/test", permissions=["is_authenticated", "is_staff"]), False),
        (
            NavItem(
                "Test",
                "/test",
                permissions=["is_authenticated", "is_staff", "is_superuser"],
            ),
            False,
        ),
    ],
)
def test_check_item_permissions_is_authenticated(item, expected, req):
    req.user = baker.make(get_user_model())

    assert item.check_permissions(req) == expected


# staff user
@pytest.mark.parametrize(
    "item,expected",
    [
        # nav item
        (NavItem("Test", "/test"), True),
        (NavItem("Test", "/test", permissions=["is_authenticated"]), True),
        (NavItem("Test", "/test", permissions=["is_staff"]), True),
        (NavItem("Test", "/test", permissions=["is_superuser"]), False),
        (NavItem("Test", "/test", permissions=["tests.dummy_perm"]), False),
        # nav group with url
        (NavGroup("Test", "/test", items=[]), True),
        (NavGroup("Test", "/test", items=[], permissions=["is_authenticated"]), True),
        (NavGroup("Test", "/test", items=[], permissions=["is_staff"]), True),
        (NavGroup("Test", "/test", items=[], permissions=["is_superuser"]), False),
        (NavGroup("Test", "/test", items=[], permissions=["tests.dummy_perm"]), False),
        # nav group with no url and items with perms
        (NavGroup("Test", items=[NavItem("Test", "/test")]), True),
        (
            NavGroup(
                "Test",
                items=[NavItem("Test", "/test", permissions=["is_authenticated"])],
            ),
            True,
        ),
        (
            NavGroup(
                "Test", items=[NavItem("Test", "/test", permissions=["is_staff"])]
            ),
            True,
        ),
        (
            NavGroup(
                "Test", items=[NavItem("Test", "/test", permissions=["is_superuser"])]
            ),
            False,
        ),
        (
            NavGroup(
                "Test",
                items=[NavItem("Test", "/test", permissions=["tests.dummy_perm"])],
            ),
            False,
        ),
        # multiple perms
        (NavItem("Test", "/test", permissions=["is_authenticated", "is_staff"]), True),
        (
            NavItem(
                "Test",
                "/test",
                permissions=["is_authenticated", "is_staff", "is_superuser"],
            ),
            False,
        ),
    ],
)
def test_check_item_permissions_is_staff(item, expected, req):
    req.user = baker.make(get_user_model(), is_staff=True)

    assert item.check_permissions(req) == expected


# superuser
@pytest.mark.parametrize(
    "item,expected",
    [
        # nav item
        (NavItem("Test", "/test"), True),
        (NavItem("Test", "/test", permissions=["is_authenticated"]), True),
        (NavItem("Test", "/test", permissions=["is_staff"]), True),
        (NavItem("Test", "/test", permissions=["is_superuser"]), True),
        (NavItem("Test", "/test", permissions=["tests.dummy_perm"]), True),
        # nav group with url
        (NavGroup("Test", "/test", items=[]), True),
        (NavGroup("Test", "/test", items=[], permissions=["is_authenticated"]), True),
        (NavGroup("Test", "/test", items=[], permissions=["is_staff"]), True),
        (NavGroup("Test", "/test", items=[], permissions=["is_superuser"]), True),
        (NavGroup("Test", "/test", items=[], permissions=["tests.dummy_perm"]), True),
        # nav group with no url and items with perms
        (NavGroup("Test", items=[NavItem("Test", "/test")]), True),
        (
            NavGroup(
                "Test",
                items=[NavItem("Test", "/test", permissions=["is_authenticated"])],
            ),
            True,
        ),
        (
            NavGroup(
                "Test", items=[NavItem("Test", "/test", permissions=["is_staff"])]
            ),
            True,
        ),
        (
            NavGroup(
                "Test", items=[NavItem("Test", "/test", permissions=["is_superuser"])]
            ),
            True,
        ),
        (
            NavGroup(
                "Test",
                items=[NavItem("Test", "/test", permissions=["tests.dummy_perm"])],
            ),
            True,
        ),
        # multiple perms
        (NavItem("Test", "/test", permissions=["is_authenticated", "is_staff"]), True),
        (
            NavItem(
                "Test",
                "/test",
                permissions=["is_authenticated", "is_staff", "is_superuser"],
            ),
            True,
        ),
    ],
)
def test_check_item_permissions_is_superuser(item, expected, req):
    req.user = baker.make(get_user_model(), is_superuser=True)

    assert item.check_permissions(req) == expected


# user with specific auth.Permission
@pytest.mark.parametrize(
    "item,expected",
    [
        # nav item
        (NavItem("Test", "/test"), True),
        (NavItem("Test", "/test", permissions=["is_authenticated"]), True),
        (NavItem("Test", "/test", permissions=["is_staff"]), False),
        (NavItem("Test", "/test", permissions=["is_superuser"]), False),
        (NavItem("Test", "/test", permissions=["tests.dummy_perm"]), True),
        # nav group with url
        (NavGroup("Test", "/test", items=[]), True),
        (NavGroup("Test", "/test", items=[], permissions=["is_authenticated"]), True),
        (NavGroup("Test", "/test", items=[], permissions=["is_staff"]), False),
        (NavGroup("Test", "/test", items=[], permissions=["is_superuser"]), False),
        (NavGroup("Test", "/test", items=[], permissions=["tests.dummy_perm"]), True),
        # nav group with no url and items with perms
        (NavGroup("Test", items=[NavItem("Test", "/test")]), True),
        (
            NavGroup(
                "Test",
                items=[NavItem("Test", "/test", permissions=["is_authenticated"])],
            ),
            True,
        ),
        (
            NavGroup(
                "Test", items=[NavItem("Test", "/test", permissions=["is_staff"])]
            ),
            False,
        ),
        (
            NavGroup(
                "Test", items=[NavItem("Test", "/test", permissions=["is_superuser"])]
            ),
            False,
        ),
        (
            NavGroup(
                "Test",
                items=[NavItem("Test", "/test", permissions=["tests.dummy_perm"])],
            ),
            True,
        ),
        # multiple perms
        (NavItem("Test", "/test", permissions=["is_authenticated", "is_staff"]), False),
        (
            NavItem(
                "Test",
                "/test",
                permissions=["is_authenticated", "is_staff", "is_superuser"],
            ),
            False,
        ),
    ],
)
def test_check_item_permissions_auth_permission(item, expected, req):
    user = baker.make(get_user_model())

    dummy_perm = baker.make(
        "auth.Permission",
        codename="dummy_perm",
        name="Dummy Permission",
        content_type=baker.make("contenttypes.ContentType", app_label="tests"),
    )

    user.user_permissions.add(dummy_perm)

    req.user = user

    assert item.check_permissions(req) == expected


@override_settings(
    INSTALLED_APPS=[
        app for app in settings.INSTALLED_APPS if app != "django.contrib.auth"
    ]
)
def test_check_item_permissions_no_contrib_auth(req, caplog):
    item = NavItem("Test", "/test", permissions=["is_authenticated"])

    with caplog.at_level("WARNING"):
        assert item.check_permissions(req) is True

    assert "The 'django.contrib.auth' app is not installed" in caplog.text


def test_item_permissions_with_callable(req):
    def dummy_check(request: HttpRequest) -> bool:
        return True

    item = NavItem("Test", "/test", permissions=[dummy_check])

    req.user = AnonymousUser()

    assert item.check_permissions(req)


def test_item_permissions_with_callable_and_user(req):
    def check_is_authenticated(request: HttpRequest) -> bool:
        return request.user.is_authenticated

    item = NavItem("Test", "/test", permissions=[check_is_authenticated])

    req.user = AnonymousUser()

    assert not item.check_permissions(req)

    req.user = baker.make(get_user_model())

    assert item.check_permissions(req)
