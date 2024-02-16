from __future__ import annotations

import logging

import pytest
from django.conf import settings
from django.http import HttpRequest

from .settings import DEFAULT_SETTINGS

pytest_plugins = []  # type: ignore


def pytest_configure(config):
    logging.disable(logging.CRITICAL)

    settings.configure(**DEFAULT_SETTINGS, **TEST_SETTINGS)


TEST_SETTINGS = {
    "INSTALLED_APPS": [
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django_simple_nav",
        "tests",
    ],
    "ROOT_URLCONF": "tests.urls",
    "TEMPLATES": [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "APP_DIRS": True,
        }
    ],
}


@pytest.fixture
def req():
    return HttpRequest()
