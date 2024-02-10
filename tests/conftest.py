from __future__ import annotations

import logging
from html.parser import HTMLParser

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


@pytest.fixture
def count_anchors():
    class AnchorParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.anchors = []

        def handle_starttag(self, tag, attrs):
            if tag == "a":
                self.anchors.append(attrs[0][1])

    def count_anchors(html: str) -> int:
        parser = AnchorParser()
        parser.feed(html)
        return len(parser.anchors)

    return count_anchors
