from __future__ import annotations

import logging

from django.conf import settings

from .settings import DEFAULT_SETTINGS

pytest_plugins = []  # type: ignore


def pytest_configure(config):
    logging.disable(logging.CRITICAL)

    settings.configure(**DEFAULT_SETTINGS, **TEST_SETTINGS)


TEST_SETTINGS = {
    # add any test settings specific to `django-simple-nav` here
}
