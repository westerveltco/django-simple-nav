from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any

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

    def get_context_data(self, request: HttpRequest) -> dict[str, Any]:
        items = [
            RenderedNavItem(item, request)
            for item in self.items
            if check_item_permissions(item, request)
        ]
        return {"items": items}

    def render(self, request: HttpRequest, template_name: str | None = None) -> str:
        context = self.get_context_data(request)
        context["request"] = request
        return render_to_string(
            template_name=template_name or self.template_name,
            context=context,
            request=request,
        )


@dataclass(frozen=True)
class NavGroup:
    title: str
    items: list[NavGroup | NavItem]
    url: str | None = None
    permissions: list[str] = field(default_factory=list)
    extra_context: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class NavItem:
    title: str
    url: str
    permissions: list[str] = field(default_factory=list)
    extra_context: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RenderedNavItem:
    item: NavItem | NavGroup
    request: HttpRequest

    def __getattr__(self, name: str) -> Any:
        if name == "extra_context":
            return self.item.extra_context
        elif hasattr(self.item, name):
            return getattr(self.item, name)
        else:
            try:
                return self.item.extra_context[name]
            except KeyError as err:
                msg = f"{self.item!r} object has no attribute {name!r}"
                raise AttributeError(msg) from err

    @property
    def title(self) -> str:
        return mark_safe(self.item.title)

    @property
    def items(self) -> list[RenderedNavItem] | None:
        if not isinstance(self.item, NavGroup):
            return None
        return [RenderedNavItem(item, self.request) for item in self.item.items]

    @property
    def url(self) -> str | None:
        if not self.item.url:
            return None
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
