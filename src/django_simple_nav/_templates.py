from __future__ import annotations

import logging

from django.core.exceptions import ImproperlyConfigured
from django.template import engines
from django.template.backends.base import BaseEngine

from django_simple_nav.conf import app_settings

logger = logging.getLogger(__name__)


def get_template_engine(using: str | None = None) -> BaseEngine:
    if template_backend := app_settings.TEMPLATE_BACKEND:
        # https://github.com/django/django/blob/082fe2b5a83571dec4aa97580af0fe8cf2a5214e/django/template/utils.py#L33-L42
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

        # https://github.com/django/django/blob/082fe2b5a83571dec4aa97580af0fe8cf2a5214e/django/template/loader.py#L65-L66
        engine = all_engines[0] if using is None else engines[using]

    return engine
