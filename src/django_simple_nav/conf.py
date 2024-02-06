from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from django.conf import settings

DJANGO_SIMPLE_NAV_SETTINGS_NAME = "DJANGO_SIMPLE_NAV"


@dataclass(frozen=True)
class AppSettings:
    def __getattribute__(self, __name: str) -> Any:
        user_settings = getattr(settings, DJANGO_SIMPLE_NAV_SETTINGS_NAME, {})
        return user_settings.get(__name, super().__getattribute__(__name))


app_settings = AppSettings()
