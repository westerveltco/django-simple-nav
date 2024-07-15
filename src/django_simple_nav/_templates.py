from __future__ import annotations

import logging
from typing import Protocol

from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest
from django.template import engines
from django.template.backends.base import BaseEngine
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
    engine = get_engine(using)
    return engine.from_string(template_code)


def get_engine(using: str | None = None) -> BaseEngine:
    if app_settings.TEMPLATE_BACKEND is None:
        num_of_engines = len(engines.all())

        if num_of_engines == 0:
            msg = "No `BACKEND` found for a template engine. Please configure at least one in your `TEMPLATES` setting or set `DJANGO_SIMPLE_NAV['TEMPLATE_BACKEND']`."
            raise ImproperlyConfigured(msg)

        if num_of_engines > 1:
            msg = "Multiple `BACKEND` defined for a template engine. Will proceed with first defined in list, otherwise set `DJANGO_SIMPLE_NAV['TEMPLATE_BACKEND']` to specify which one to use."
            logger.warning(msg)

        engine = engines.all()[0] if using is None else engines[using]
    else:
        try:
            backend_alias = app_settings.TEMPLATE_BACKEND.rsplit(".", 2)[-2]
        except Exception as err:
            msg = f"Invalid `TEMPLATE_BACKEND` for a template engine: {app_settings.TEMPLATE_BACKEND}. Check your `DJANGO_SIMPLE_NAV['TEMPLATE_BACKEND']` setting."
            raise ImproperlyConfigured(msg) from err

        engine = engines[backend_alias]

    return engine
