from __future__ import annotations

import logging
from dataclasses import dataclass
from dataclasses import field
from typing import cast

from django.apps import apps
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.safestring import mark_safe

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

    def get_items(self, request: HttpRequest) -> list[dict[str, object]]:
        if self.items is not None:
            items = [item.render(request) for item in self.items]
            print(f"{items=}")
            print(f"{len(items)=}")
            none_items = [item for item in items if item is not None]
            print(f"{none_items=}")
            print(f"{len(none_items)=}")
            return none_items

        msg = f"{self.__class__!r} must define 'items' or override 'get_items()'"
        raise ImproperlyConfigured(msg)

    def get_context_data(self, request: HttpRequest) -> dict[str, object]:
        items = self.get_items(request)
        print(f"get_context_data: {items=}")
        return {
            "items": items,
            "request": request,
        }

    def render(self, request: HttpRequest, template_name: str | None = None) -> str:
        context = self.get_context_data(request)
        print(f"render: {context=}")
        return render_to_string(
            template_name=template_name or self.get_template_name(),
            context=context,
            request=request,
        )


@dataclass(frozen=True)
class NavItem:
    title: str
    url: str
    permissions: list[str] = field(default_factory=list)
    extra_context: dict[str, object] = field(default_factory=dict)

    def render(self, request: HttpRequest) -> dict[str, object] | None:
        if not self.check_permissions(request):
            print(f"{self.__class__!r} failed permissions")
            print(f"{self.title=}")
            print(f"{self.url=}")
            print(f"{self.permissions=}")
            print(f"{self.extra_context=}")
            return None

        # item.items returns the dictionary, not the list of NavItems, even on this
        return {
            "title": self.get_title(),
            "url": self.get_url(),
            "active": self.get_active(request),
            **self.extra_context,
        }

    def check_permissions(self, request: HttpRequest) -> bool:
        if not apps.is_installed("django.contrib.auth"):
            logger.warning(
                "The 'django.contrib.auth' app is not installed, so permissions will not be checked."
            )
            return True

        if not self.permissions:
            return True

        if hasattr(request, "user") and isinstance(request.user, AnonymousUser):
            return False

        has_perm = False

        user = cast(AbstractUser, request.user)

        for perm in self.permissions:
            if perm in ["is_authenticated", "is_staff", "is_superuser"]:
                has_perm = getattr(user, perm, False)
            else:
                has_perm = user.has_perm(perm)

            if has_perm:
                break

        return has_perm

    def get_title(self) -> str:
        return mark_safe(self.title)

    def get_url(self) -> str | None:
        try:
            url = reverse(self.url)
        except NoReverseMatch:
            url = self.url
        return url

    def get_active(self, request: HttpRequest) -> bool:
        url = self.get_url()
        if url is None:
            return False
        return request.path.startswith(url) and url != "/" or request.path == url


@dataclass(frozen=True)
class NavGroup(NavItem):
    url: str = "#"
    items: list[NavGroup | NavItem] = field(default_factory=list)

    def render(self, request: HttpRequest) -> dict[str, object] | None:
        context = super().render(request)
        if context is None:
            return None
        items = [item.render(request) for item in self.items]
        context["items"] = [item for item in items if item is not None]
        return context

    def get_url(self) -> str | None:
        url = super().get_url()
        if url == "#":
            return None
        return url
