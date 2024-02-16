from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from model_bakery import baker

from django_simple_nav.nav import NavGroup
from django_simple_nav.nav import NavItem
from django_simple_nav.permissions import check_item_permissions
from django_simple_nav.permissions import user_has_perm

pytestmark = pytest.mark.django_db


def test_check_anonymous_user_has_perm():
    user = AnonymousUser()

    assert user_has_perm(user, "is_authenticated") is False


def test_check_authenticated_user_has_perm():
    user = baker.make(get_user_model())

    assert user_has_perm(user, "is_authenticated") is True


def test_check_staff_user_has_perm():
    user = baker.make(get_user_model(), is_staff=True)

    assert user_has_perm(user, "is_staff") is True


def test_check_superuser_user_has_perm():
    user = baker.make(get_user_model(), is_superuser=True)

    assert user_has_perm(user, "is_superuser") is True


@pytest.mark.parametrize(
    "item,expected",
    [
        (NavItem("Test", "/test"), True),
        (NavItem("Test", "/test", permissions=["is_authenticated"]), False),
        (NavItem("Test", "/test", permissions=["is_staff"]), False),
        (NavItem("Test", "/test", permissions=["is_superuser"]), False),
        (NavGroup("Test", [], "/test"), True),
        (NavGroup("Test", [], "/test", permissions=["is_authenticated"]), False),
        (NavGroup("Test", [], "/test", permissions=["is_staff"]), False),
        (NavGroup("Test", [], "/test", permissions=["is_superuser"]), False),
        (NavGroup("Test", [NavItem("Test", "/test")], "/test"), True),
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
                "Test",
                [NavItem("Test", "/test")],
                "/test",
                permissions=["is_authenticated"],
            ),
            False,
        ),
        (
            NavGroup(
                "Test", [NavItem("Test", "/test")], "/test", permissions=["is_staff"]
            ),
            False,
        ),
        (
            NavGroup(
                "Test",
                [NavItem("Test", "/test")],
                "/test",
                permissions=["is_superuser"],
            ),
            False,
        ),
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
def test_check_item_permissions_anonymous(item, expected):
    user = AnonymousUser()

    assert check_item_permissions(item, user) is expected


@pytest.mark.parametrize(
    "item,expected",
    [
        (NavItem("Test", "/test"), True),
        (NavItem("Test", "/test", permissions=["is_authenticated"]), True),
        (NavItem("Test", "/test", permissions=["is_staff"]), False),
        (NavItem("Test", "/test", permissions=["is_superuser"]), False),
        (NavGroup("Test", [], "/test"), True),
        (NavGroup("Test", [], "/test", permissions=["is_authenticated"]), True),
        (NavGroup("Test", [], "/test", permissions=["is_staff"]), False),
        (NavGroup("Test", [], "/test", permissions=["is_superuser"]), False),
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
                "Test",
                [NavItem("Test", "/test")],
                "/test",
                permissions=["is_authenticated"],
            ),
            True,
        ),
        (
            NavGroup(
                "Test", [NavItem("Test", "/test")], "/test", permissions=["is_staff"]
            ),
            False,
        ),
        (
            NavGroup(
                "Test",
                [NavItem("Test", "/test")],
                "/test",
                permissions=["is_superuser"],
            ),
            False,
        ),
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
def test_check_item_permissions_is_authenticated(item, expected):
    user = baker.make(get_user_model())

    assert check_item_permissions(item, user) is expected


@pytest.mark.parametrize(
    "item,expected",
    [
        (NavItem("Test", "/test"), True),
        (NavItem("Test", "/test", permissions=["is_authenticated"]), True),
        (NavItem("Test", "/test", permissions=["is_staff"]), True),
        (NavItem("Test", "/test", permissions=["is_superuser"]), False),
        (NavGroup("Test", [], "/test"), True),
        (NavGroup("Test", [], "/test", permissions=["is_authenticated"]), True),
        (NavGroup("Test", [], "/test", permissions=["is_staff"]), True),
        (NavGroup("Test", [], "/test", permissions=["is_superuser"]), False),
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
                "Test",
                [NavItem("Test", "/test")],
                "/test",
                permissions=["is_authenticated"],
            ),
            True,
        ),
        (
            NavGroup(
                "Test", [NavItem("Test", "/test")], "/test", permissions=["is_staff"]
            ),
            True,
        ),
        (
            NavGroup(
                "Test",
                [NavItem("Test", "/test")],
                "/test",
                permissions=["is_superuser"],
            ),
            False,
        ),
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
def test_check_item_permissions_is_staff(item, expected):
    user = baker.make(get_user_model(), is_staff=True)

    assert check_item_permissions(item, user) is expected


@pytest.mark.parametrize(
    "item,expected",
    [
        (NavItem("Test", "/test"), True),
        (NavItem("Test", "/test", permissions=["is_authenticated"]), True),
        (NavItem("Test", "/test", permissions=["is_staff"]), True),
        (NavItem("Test", "/test", permissions=["is_superuser"]), True),
        (NavGroup("Test", [], "/test"), True),
        (NavGroup("Test", [], "/test", permissions=["is_authenticated"]), True),
        (NavGroup("Test", [], "/test", permissions=["is_staff"]), True),
        (NavGroup("Test", [], "/test", permissions=["is_superuser"]), True),
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
                "Test",
                [NavItem("Test", "/test")],
                "/test",
                permissions=["is_authenticated"],
            ),
            True,
        ),
        (
            NavGroup(
                "Test", [NavItem("Test", "/test")], "/test", permissions=["is_staff"]
            ),
            True,
        ),
        (
            NavGroup(
                "Test",
                [NavItem("Test", "/test")],
                "/test",
                permissions=["is_superuser"],
            ),
            True,
        ),
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
def test_check_item_permissions_is_superuser(item, expected):
    user = baker.make(get_user_model(), is_superuser=True)

    assert check_item_permissions(item, user) is expected
