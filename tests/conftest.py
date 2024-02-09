from __future__ import annotations

import logging

from django.conf import settings

pytest_plugins = []  # type: ignore


def pytest_configure(_):
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
        "django_simple_nav",
    ],
    "LOGGING_CONFIG": None,
    "PASSWORD_HASHERS": [
        "django.contrib.auth.hashers.MD5PasswordHasher",
    ],
}
