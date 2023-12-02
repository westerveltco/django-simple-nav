from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch


@dataclass
class Nav:
    items: list[NavGroup | NavItem]
    template_name: str

    def _get_url(self, url: str) -> str:
        try:
            return reverse(url)
        except NoReverseMatch:
            return url

    @classmethod
    def render(cls, request: HttpRequest) -> str:
        items = [
            item for item in cls.items if cls._check_item_visibility(request, item)
        ]
        return render_to_string(
            template_name=cls.template_name,
            context={"items": items},
        )

    @classmethod
    def _check_item_visibility(
        cls, request: HttpRequest, item: NavGroup | NavItem
    ) -> bool:
        if isinstance(item, NavItem):
            for idx, perm in enumerate(item.permissions):
                user_perm = getattr(request.user, perm, False)
                if not user_perm:
                    return False
                if not idx == len(item.permissions) - 1:
                    continue
        elif isinstance(item, NavGroup):
            sub_items = [
                sub_item
                for sub_item in item.items
                if cls._check_item_visibility(request, sub_item)
            ]
            if not sub_items:
                return False

        return True

    @staticmethod
    def _check_item_active(request: HttpRequest, url: str) -> bool:
        return request.path.startswith(url) and url != "/" or request.path == url


@dataclass
class NavGroup:
    title: str
    items: list[NavGroup | NavItem]
    url: str | None = None
    permissions: list[str] = field(default_factory=list)
    active: bool = False


@dataclass
class NavItem:
    title: str
    url: str
    permissions: list[str] = field(default_factory=list)
    active: bool = False
