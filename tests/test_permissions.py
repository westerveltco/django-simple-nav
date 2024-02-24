from __future__ import annotations

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import override_settings
from model_bakery import baker

from django_simple_nav.nav import NavGroup
from django_simple_nav.nav import NavItem
from django_simple_nav.permissions import check_item_permissions
from django_simple_nav.permissions import user_has_perm

pytestmark = pytest.mark.django_db


def test_check_anonymous_user_has_perm():
    user = AnonymousUser()

    assert not user_has_perm(user, "is_authenticated")


def test_check_authenticated_user_has_perm():
    user = baker.make(get_user_model())

    assert user_has_perm(user, "is_authenticated")


def test_check_staff_user_has_perm():
    user = baker.make(get_user_model(), is_staff=True)

    assert user_has_perm(user, "is_staff")


def test_check_superuser_user_has_perm():
    user = baker.make(get_user_model(), is_superuser=True)

    assert user_has_perm(user, "is_superuser")


def test_check_auth_permission_user_has_perm():
    user = baker.make(get_user_model())

    dummy_perm = baker.make(
        "auth.Permission",
        codename="dummy_perm",
        name="Dummy Permission",
        content_type=baker.make("contenttypes.ContentType", app_label="tests"),
    )

    user.user_permissions.add(dummy_perm)

    assert user_has_perm(user, "tests.dummy_perm")


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
        (NavGroup("Test", [], "/test"), True),
        (NavGroup("Test", [], "/test", permissions=["is_authenticated"]), False),
        (NavGroup("Test", [], "/test", permissions=["is_staff"]), False),
        (NavGroup("Test", [], "/test", permissions=["is_superuser"]), False),
        (NavGroup("Test", [], "/test", permissions=["tests.dummy_perm"]), False),
        # nav group with no url and items with perms
        (NavGroup("Test", [NavItem("Test", "/test")]), True),
        (
            NavGroup(
                "Test",
                [NavItem("Test", "/test", permissions=["is_authenticated"])],
            ),
            False,
        ),
        (NavGroup("Test", [NavItem("Test", "/test", permissions=["is_staff"])]), False),
        (
            NavGroup("Test", [NavItem("Test", "/test", permissions=["is_superuser"])]),
            False,
        ),
        (
            NavGroup(
                "Test", [NavItem("Test", "/test", permissions=["tests.dummy_perm"])]
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

    assert check_item_permissions(item, req) == expected


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
        (NavGroup("Test", [], "/test"), True),
        (NavGroup("Test", [], "/test", permissions=["is_authenticated"]), True),
        (NavGroup("Test", [], "/test", permissions=["is_staff"]), False),
        (NavGroup("Test", [], "/test", permissions=["is_superuser"]), False),
        (NavGroup("Test", [], "/test", permissions=["tests.dummy_perm"]), False),
        # nav group with no url and items with perms
        (NavGroup("Test", [NavItem("Test", "/test")], "/test"), True),
        (
            NavGroup(
                "Test",
                [NavItem("Test", "/test", permissions=["is_authenticated"])],
            ),
            True,
        ),
        (NavGroup("Test", [NavItem("Test", "/test", permissions=["is_staff"])]), False),
        (
            NavGroup("Test", [NavItem("Test", "/test", permissions=["is_superuser"])]),
            False,
        ),
        (
            NavGroup(
                "Test", [NavItem("Test", "/test", permissions=["tests.dummy_perm"])]
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

    assert check_item_permissions(item, req) == expected


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
        (NavGroup("Test", [], "/test"), True),
        (NavGroup("Test", [], "/test", permissions=["is_authenticated"]), True),
        (NavGroup("Test", [], "/test", permissions=["is_staff"]), True),
        (NavGroup("Test", [], "/test", permissions=["is_superuser"]), False),
        (NavGroup("Test", [], "/test", permissions=["tests.dummy_perm"]), False),
        # nav group with no url and items with perms
        (NavGroup("Test", [NavItem("Test", "/test")]), True),
        (
            NavGroup(
                "Test",
                [NavItem("Test", "/test", permissions=["is_authenticated"])],
            ),
            True,
        ),
        (NavGroup("Test", [NavItem("Test", "/test", permissions=["is_staff"])]), True),
        (
            NavGroup("Test", [NavItem("Test", "/test", permissions=["is_superuser"])]),
            False,
        ),
        (
            NavGroup(
                "Test", [NavItem("Test", "/test", permissions=["tests.dummy_perm"])]
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

    assert check_item_permissions(item, req) == expected


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
        (NavGroup("Test", [], "/test"), True),
        (NavGroup("Test", [], "/test", permissions=["is_authenticated"]), True),
        (NavGroup("Test", [], "/test", permissions=["is_staff"]), True),
        (NavGroup("Test", [], "/test", permissions=["is_superuser"]), True),
        (NavGroup("Test", [], "/test", permissions=["tests.dummy_perm"]), True),
        # nav group with no url and items with perms
        (NavGroup("Test", [NavItem("Test", "/test")], "/test"), True),
        (
            NavGroup(
                "Test",
                [NavItem("Test", "/test", permissions=["is_authenticated"])],
            ),
            True,
        ),
        (NavGroup("Test", [NavItem("Test", "/test", permissions=["is_staff"])]), True),
        (
            NavGroup("Test", [NavItem("Test", "/test", permissions=["is_superuser"])]),
            True,
        ),
        (
            NavGroup(
                "Test", [NavItem("Test", "/test", permissions=["tests.dummy_perm"])]
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

    assert check_item_permissions(item, req) == expected


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
        (NavGroup("Test", [], "/test"), True),
        (NavGroup("Test", [], "/test", permissions=["is_authenticated"]), True),
        (NavGroup("Test", [], "/test", permissions=["is_staff"]), False),
        (NavGroup("Test", [], "/test", permissions=["is_superuser"]), False),
        (NavGroup("Test", [], "/test", permissions=["tests.dummy_perm"]), True),
        # nav group with no url and items with perms
        (NavGroup("Test", [NavItem("Test", "/test")], "/test"), True),
        (
            NavGroup(
                "Test",
                [NavItem("Test", "/test", permissions=["is_authenticated"])],
            ),
            True,
        ),
        (NavGroup("Test", [NavItem("Test", "/test", permissions=["is_staff"])]), False),
        (
            NavGroup("Test", [NavItem("Test", "/test", permissions=["is_superuser"])]),
            False,
        ),
        (
            NavGroup(
                "Test", [NavItem("Test", "/test", permissions=["tests.dummy_perm"])]
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

    assert check_item_permissions(item, req) == expected


@override_settings(
    INSTALLED_APPS=[
        app for app in settings.INSTALLED_APPS if app != "django.contrib.auth"
    ]
)
def test_check_item_permissions_no_contrib_auth(req, caplog):
    item = NavItem("Test", "/test", permissions=["is_authenticated"])

    with caplog.at_level("WARNING"):
        assert check_item_permissions(item, req) is True

    assert "The 'django.contrib.auth' app is not installed" in caplog.text
