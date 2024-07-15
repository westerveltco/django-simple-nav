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


def get_template_engine(using: str | None = None) -> BaseEngine:
    if template_backend := app_settings.TEMPLATE_BACKEND:
        try:
            backend_alias = template_backend.rsplit(".", 2)[-2]
        except Exception as err:
            msg = f"Invalid `TEMPLATE_BACKEND` for a template engine: {app_settings.TEMPLATE_BACKEND}. Check your `DJANGO_SIMPLE_NAV['TEMPLATE_BACKEND']` setting."
            raise ImproperlyConfigured(msg) from err

        engine = engines[backend_alias]
    else:
        all_engines = engines.all()
        num_of_engines = len(all_engines)

        if num_of_engines == 0:
            msg = "No `BACKEND` found for a template engine. Please configure at least one in your `TEMPLATES` setting or set `DJANGO_SIMPLE_NAV['TEMPLATE_BACKEND']`."
            raise ImproperlyConfigured(msg)

        if num_of_engines > 1:
            msg = "Multiple `BACKEND` defined for a template engine. Will proceed with first defined in list, otherwise set `DJANGO_SIMPLE_NAV['TEMPLATE_BACKEND']` to specify which one to use."
            logger.warning(msg)

        engine = all_engines[0] if using is None else engines[using]

    return engine
