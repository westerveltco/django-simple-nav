from __future__ import annotations

import logging

from django.conf import settings

pytest_plugins = []  # type: ignore


# Settings fixtures to bootstrap our tests
def pytest_configure(config):
    logging.disable(logging.CRITICAL)

    settings.configure(
        ALLOWED_HOSTS=["*"],
        CACHES={
            "default": {
                "BACKEND": "django.core.cache.backends.dummy.DummyCache",
            }
        },
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            },
        },
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        INSTALLED_APPS=[
            "simple_nav",
        ],
        LOGGING_CONFIG=None,
        PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"],
        SECRET_KEY="NOTASECRET",
        USE_TZ=True,
    )
