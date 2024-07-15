from __future__ import annotations

import logging
import sys
from dataclasses import dataclass
from dataclasses import field
from typing import Callable
from typing import cast

from django.apps import apps
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.safestring import mark_safe

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override  # pyright: ignore[reportUnreachable]

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Nav:
    template_name: str | None = field(init=False, default=None)
    items: list[NavGroup | NavItem] | None = field(init=False, default=None)

    def get_template_name(self) -> str:
        if self.template_name is not None:
            return self.template_name

        msg = f"{self.__class__!r} must define 'template_name' or override 'get_template_name()'"
        raise ImproperlyConfigured(msg % self.__class__.__name__)

    def get_items(self, request: HttpRequest) -> list[NavGroup | NavItem]:
        if self.items is not None:
            return [item for item in self.items if item.check_permissions(request)]

        msg = f"{self.__class__!r} must define 'items' or override 'get_items()'"
        raise ImproperlyConfigured(msg)

    def get_items_context_data(self, request: HttpRequest) -> list[dict[str, object]]:
        items = self.get_items(request)
        context = [item.get_context_data(request) for item in items]
        return context

    def get_context_data(self, request: HttpRequest) -> dict[str, object]:
        return {
            "items": self.get_items_context_data(request),
            "request": request,
        }

    def render(self, request: HttpRequest, template_name: str | None = None) -> str:
        context = self.get_context_data(request)
        return render_to_string(
            template_name=template_name or self.get_template_name(),
            context=context,
            request=request,
        )


@dataclass(frozen=True)
class NavItem:
    title: str
    url: str | None = None
    permissions: list[str | Callable[[HttpRequest], bool]] = field(default_factory=list)
    extra_context: dict[str, object] = field(default_factory=dict)

    def get_context_data(self, request: HttpRequest) -> dict[str, object]:
        context = {
            "title": self.get_title(),
            "url": self.get_url(),
            "active": self.get_active(request),
            # this needs to be set to shadow the built-in `items()` of the dict
            # returned by this method for `NavItem`. otherwise when looping through
            # the items in a `Nav`, calling `{% if item.items %}` will resolve to `True`.
            # this is a consequence of getting rid of `RenderedNavItem` from earlier versions
            # of `django-simple-nav` which was done to slightly simplfy the library. though
            # given this hack, maybe that wasn't really worth it? idk... i guess it could
            # have been called `children` or `subnav`, but i started with `items` and
            # i'd rather have API consistency and this hack.
            "items": None,
        }
        # filter out any items in `extra_context` that may be shadowing the
        # above `context` dict
        extra_context = {
            key: value
            for key, value in self.extra_context.copy().items()
            if context.get(key) is None
        }
        return {
            **context,
            **extra_context,
        }

    def get_title(self) -> str:
        return mark_safe(self.title)

    def get_url(self) -> str:
        url: str | None

        try:
            url = reverse(self.url)
        except NoReverseMatch:
            url = self.url

        if url is not None:
            return url

        msg = f"{self.__class__!r} must define 'url' or override 'get_url()'"
        raise ImproperlyConfigured(msg)

    def get_active(self, request: HttpRequest) -> bool:
        try:
            url = self.get_url()
        except ImproperlyConfigured:
            url = None

        if not url:
            return False

        return request.path.startswith(url) and url != "/" or request.path == url

    def check_permissions(self, request: HttpRequest) -> bool:
        if not apps.is_installed("django.contrib.auth"):
            logger.warning(
                "The 'django.contrib.auth' app is not installed, so permissions will not be checked."
            )
            return True

        if not hasattr(request, "user"):
            # if no user attached to request, we assume that the user is not authenticated
            # and we should hide if *any* permissions are set
            return not self.permissions

        # explicitly cast to AbstractUser to make static type checkers happy
        # `django-stubs` types `request.user` as `django.contrib.auth.base_user.AbstractBaseUser`
        # as opposed to `django.contrib.auth.models.AbstractUser` or `django.contrib.auth.models.User`
        # so any type checkers will complain if this is not casted
        user = cast(AbstractUser, request.user)

        has_perm = False

        if not self.permissions:
            has_perm = True

        for idx, perm in enumerate(self.permissions):
            if getattr(user, "is_superuser", False):
                has_perm = True
                break
            elif perm in ["is_authenticated", "is_staff"]:
                has_perm = getattr(user, perm, False)
            elif callable(perm):
                cast(Callable[[HttpRequest], bool], perm)
                has_perm = perm(request)
            else:
                has_perm = user.has_perm(perm)

            if not idx == len(self.permissions) - 1:
                continue

        if isinstance(self, NavGroup) and hasattr(self, "items"):
            sub_items = [
                sub_item
                for sub_item in self.items
                if sub_item.check_permissions(request) is not False
            ]
            if not sub_items and not self.url:
                has_perm = False

        return has_perm


@dataclass(frozen=True)
class NavGroup(NavItem):
    items: list[NavGroup | NavItem] = field(default_factory=list)

    @override
    def get_context_data(self, request: HttpRequest) -> dict[str, object]:
        context = super().get_context_data(request)
        context["items"] = [item.get_context_data(request) for item in self.items]
        return context

    @override
    def get_url(self) -> str:
        try:
            url = super().get_url()
        except ImproperlyConfigured:
            return ""
        return url
