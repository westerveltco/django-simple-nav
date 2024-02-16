from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.safestring import mark_safe

from django_simple_nav.permissions import check_item_permissions


@dataclass(frozen=True)
class Nav:
    template_name: str = field(init=False)
    items: list[NavGroup | NavItem] = field(init=False)

    @classmethod
    def render_from_request(
        cls, request: HttpRequest, template_name: str | None = None
    ) -> str:
        items = [
            RenderedNavItem(item, request)
            for item in cls.items
            if check_item_permissions(item, request.user)  # type: ignore[arg-type]
        ]
        return render_to_string(
            template_name=template_name or cls.template_name,
            context={"items": items},
        )


@dataclass(frozen=True)
class NavGroup:
    title: str
    items: list[NavGroup | NavItem]
    url: str | None = None
    permissions: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class NavItem:
    title: str
    url: str
    permissions: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class RenderedNavItem:
    item: NavItem | NavGroup
    request: HttpRequest

    @property
    def title(self) -> str:
        return mark_safe(self.item.title)

    @property
    def items(self) -> list[NavGroup | NavItem] | None:
        if not isinstance(self.item, NavGroup):
            return None
        return self.item.items

    @property
    def url(self) -> str:
        if not self.item.url:
            return "#"
        try:
            url = reverse(self.item.url)
        except NoReverseMatch:
            url = self.item.url
        return url

    @property
    def active(self) -> bool:
        if not self.item.url:
            return False
        return (
            self.request.path.startswith(self.item.url)
            and self.item.url != "/"
            or self.request.path == self.item.url
        )
