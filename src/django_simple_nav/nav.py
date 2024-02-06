from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from django_simple_nav.permissions import check_item_permissions


@dataclass
class Nav:
    template_name: str
    items: list[NavGroup | NavItem]

    @classmethod
    def render_from_request(cls, request: HttpRequest) -> str:
        items = [
            item
            for item in cls.items
            if check_item_permissions(item, request.user)  # type: ignore[arg-type]
        ]
        for item in items:
            if item.url:
                item.url = item.get_url()
                item.active = item.is_active(request)
            if hasattr(item, "items"):
                for sub_item in item.items:
                    sub_item.url = sub_item.get_url()
                    item.active = item.is_active(request)
        return render_to_string(
            template_name=cls.template_name,
            context={"items": items},
        )


@dataclass
class NavGroup:
    title: str
    items: list[NavGroup | NavItem]
    url: str | None = None
    permissions: list[str] = field(default_factory=list)
    active: bool | None = None

    def get_url(self) -> str | None:
        if not self.url:
            return None
        return _get_url(self.url)

    def is_active(self, request: HttpRequest) -> bool | None:
        if not self.url:
            return None
        return _check_item_active(request, self.url)


@dataclass
class NavItem:
    title: str
    url: str
    permissions: list[str] = field(default_factory=list)
    active: bool | None = None

    def get_url(self) -> str:
        return _get_url(self.url)

    def is_active(self, request: HttpRequest) -> bool:
        return _check_item_active(request, self.url)


def _get_url(url: str) -> str:
    try:
        url = reverse(url)
    except NoReverseMatch:
        url = url
    return url


def _check_item_active(request: HttpRequest, url: str) -> bool:
    return request.path.startswith(url) and url != "/" or request.path == url
