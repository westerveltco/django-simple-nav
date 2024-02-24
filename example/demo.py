from __future__ import annotations

import secrets
import sys
from pathlib import Path

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.shortcuts import render
from django.urls import path

BASE_DIR = Path(__file__).parent

settings.configure(
    ALLOWED_HOSTS="*",
    INSTALLED_APPS=[
        "django_simple_nav",
    ],
    LOGGING={
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "plain_console": {
                "format": "%(levelname)s %(message)s",
            },
            "verbose": {
                "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
            },
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "verbose",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["stdout"],
                "level": "DEBUG",
            },
            "default": {
                "handlers": ["stdout"],
                "level": "DEBUG",
            },
        },
    },
    ROOT_URLCONF=__name__,
    SECRET_KEY=secrets.token_hex(32),
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [BASE_DIR / "templates"],
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.request",
                ],
            },
        }
    ],
)


urlpatterns = [
    path("", lambda request: render(request, "base.html")),
    path("tailwind/", lambda request: render(request, "tailwind.html")),
    path("bootstrap4/", lambda request: render(request, "bootstrap4.html")),
    path("bootstrap5/", lambda request: render(request, "bootstrap5.html")),
]

app = get_wsgi_application()


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
