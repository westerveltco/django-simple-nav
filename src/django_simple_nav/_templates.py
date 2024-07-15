from __future__ import annotations

import logging
from typing import Protocol

from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest
from django.template import engines
from django.template.context import Context
from django.utils.safestring import SafeString

from django_simple_nav.conf import app_settings

logger = logging.getLogger(__name__)


class EngineTemplate(Protocol):
    def render(
        self,
        context: Context | dict[str, object] | None = ...,
        request: HttpRequest | None = ...,
    ) -> SafeString: ...


def from_string(template_code: str, using: str | None = None) -> EngineTemplate:
    if app_settings.TEMPLATE_BACKEND is None:
        try:
            engine = engines.all()[0]
        except IndexError as err:
            msg = "No `BACKEND` found for a template engine. Please configure at least one in your TEMPLATES setting or set DJANGO_SIMPLE_NAV['TEMPLATE_BACKEND']"
            raise ImproperlyConfigured(msg) from err
    else:
        try:
            backend_alias = app_settings.TEMPLATE_BACKEND.rsplit(".", 2)[-2]
        except Exception as err:
            msg = f"Invalid TEMPLATE_BACKEND for a template engine: {app_settings.TEMPLATE_BACKEND}. Check your DJANGO_SIMPLE_NAV['TEMPLATE_BACKEND'] setting."
            raise ImproperlyConfigured(msg) from err
        engine = engines[backend_alias]
    return engine.from_string(template_code)
