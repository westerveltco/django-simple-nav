from __future__ import annotations

import sys
from dataclasses import dataclass

from django.conf import settings

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override  # pyright: ignore[reportUnreachable]

DJANGO_SIMPLE_NAV_SETTINGS_NAME = "DJANGO_SIMPLE_NAV"


@dataclass(frozen=True)
class AppSettings:
    TEMPLATE_BACKEND: str = "django.template.backends.django.DjangoTemplates"

    @override
    def __getattribute__(self, __name: str) -> object:
        user_settings = getattr(settings, DJANGO_SIMPLE_NAV_SETTINGS_NAME, {})
        return user_settings.get(__name, super().__getattribute__(__name))  # pyright: ignore[reportAny]


app_settings = AppSettings()
