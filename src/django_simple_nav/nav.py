from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from django_simple_nav.exceptions import ReadOnlyProperty
from django_simple_nav.permissions import check_item_permissions


@dataclass(frozen=True)
class Nav:
    template_name: str
    items: list[NavGroup | NavItem]

    @classmethod
    def render_from_request(cls, request: HttpRequest) -> str:
        items = [
            _RenderedNavItem(item, request)
            for item in cls.items
            if check_item_permissions(item, request.user)  # type: ignore[arg-type]
        ]
        return render_to_string(
            template_name=cls.template_name,
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
class _RenderedNavItem:
    item: NavItem | NavGroup
    request: HttpRequest

    @property
    def title(self) -> str:
        return self.item.title

    @title.setter
    def title(self, _: str) -> None:
        raise ReadOnlyProperty("title")

    @property
    def items(self) -> list[NavGroup | NavItem] | None:
        if not isinstance(self.item, NavGroup):
            return None
        return self.item.items

    @items.setter
    def items(self, _: list[NavGroup | NavItem]) -> None:
        raise ReadOnlyProperty("items")

    @property
    def url(self) -> str | None:
        return self.item.url

    @url.setter
    def url(self, _: str) -> None:
        raise ReadOnlyProperty("url")

    @property
    def href(self) -> str:
        if not self.item.url:
            return "#"
        try:
            href = reverse(self.item.url)
        except NoReverseMatch:
            href = self.item.url
        return href

    @href.setter
    def href(self, _: str) -> None:
        raise ReadOnlyProperty("href")

    @property
    def active(self) -> bool:
        if not self.item.url:
            return False
        return (
            self.request.path.startswith(self.item.url)
            and self.item.url != "/"
            or self.request.path == self.item.url
        )

    @active.setter
    def active(self, _: bool) -> None:
        raise ReadOnlyProperty("active")
