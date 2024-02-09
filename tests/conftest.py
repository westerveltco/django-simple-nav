from __future__ import annotations

import logging
from html.parser import HTMLParser

import pytest
from django.conf import settings
from django.http import HttpRequest

pytest_plugins = []  # type: ignore


def pytest_configure(config):
    logging.disable(logging.CRITICAL)

    settings.configure(**TEST_SETTINGS)


TEST_SETTINGS = {
    "ALLOWED_HOSTS": ["*"],
    "DEBUG": False,
    "CACHES": {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    },
    "DATABASES": {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        },
    },
    "EMAIL_BACKEND": "django.core.mail.backends.locmem.EmailBackend",
    "INSTALLED_APPS": [
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django_simple_nav",
        "tests",
    ],
    "LOGGING_CONFIG": None,
    "PASSWORD_HASHERS": [
        "django.contrib.auth.hashers.MD5PasswordHasher",
    ],
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
