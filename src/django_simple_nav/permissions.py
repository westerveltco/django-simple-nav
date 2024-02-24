from __future__ import annotations

import logging
from typing import TYPE_CHECKING
from typing import Protocol
from typing import cast

from django.apps import apps
from django.http import HttpRequest

if TYPE_CHECKING:
    from django_simple_nav.nav import NavGroup
    from django_simple_nav.nav import NavItem

logger = logging.getLogger(__name__)


class User(Protocol):
    is_authenticated: bool
    is_staff: bool
    is_superuser: bool

    def has_perm(self, perm: str) -> bool:
        ...  # pragma: no cover


def check_item_permissions(item: NavGroup | NavItem, request: HttpRequest) -> bool:
    if not apps.is_installed("django.contrib.auth"):
        logger.warning(
            "The 'django.contrib.auth' app is not installed, so no permissions will be checked."
        )
        return True

    user = cast(User, request.user)

    for idx, perm in enumerate(item.permissions):
        if not hasattr(request, "user"):
            return False

        user = cast(User, request.user)

        user_perm = user_has_perm(user, perm)

        if not user_perm:
            return False

        if not idx == len(item.permissions) - 1:
            continue

    if hasattr(item, "items"):
        sub_items = [
            sub_item
            for sub_item in item.items
            if check_item_permissions(sub_item, request)
        ]
        if not sub_items and not item.url:
            return False

    return True


def user_has_perm(user: User, perm: str) -> bool:
    """Check if the user has a certain auth attribute or permission."""

    has_perm = False

    if perm in ["is_authenticated", "is_staff", "is_superuser"]:
        is_superuser = getattr(user, "is_superuser", False)
        if is_superuser:
            has_perm = True
        else:
            has_perm = getattr(user, perm, False)
    elif user.has_perm(perm):
        has_perm = True

    return has_perm
