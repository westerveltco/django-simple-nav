from __future__ import annotations

import os
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
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        },
    },
    INSTALLED_APPS=[
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django_simple_nav",
    ],
    LOGGING={
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
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
                "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            },
        },
    },
    MIDDLEWARE=[
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
    ],
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


def demo(request, template_name):
    return render(request, template_name)


def permissions(request):
    perm = request.GET.get("permission", None)
    if perm:
        request.user = type(
            "User", (), {"is_authenticated": True, "has_perm": lambda p: p == perm}
        )
        if perm in ["is_staff", "is_superuser"]:
            setattr(request.user, perm, True)
    return demo(request, "permissions.html")


urlpatterns = [
    path("", demo, {"template_name": "base.html"}),
    path("basic/", demo, {"template_name": "basic.html"}),
    path("permissions/", permissions),
    path("extra-context/", demo, {"template_name": "extra_context.html"}),
    path("nested/", demo, {"template_name": "nested.html"}),
    path("tailwind/", demo, {"template_name": "tailwind.html"}),
    path("bootstrap4/", demo, {"template_name": "bootstrap4.html"}),
    path("bootstrap5/", demo, {"template_name": "bootstrap5.html"}),
    path("picocss/", demo, {"template_name": "picocss.html"}),
]

app = get_wsgi_application()


if __name__ == "__main__":
    from django.contrib.auth.models import Permission
    from django.core.management import call_command

    call_command("migrate")
    Permission.objects.update_or_create(
        codename="demo_permission",
        name="Demo Permission",
        content_type_id=1,
    )
    call_command("runserver")
