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
    version = request.GET.get("version", "")
    template = f"{template_name.split('.')[0]}{version}.html"
    return render(request, template)


urlpatterns = [
    path("", demo, {"template_name": "base.html"}),
    path("tailwind/", demo, {"template_name": "tailwind.html"}),
    path("bootstrap/", demo, {"template_name": "bootstrap.html"}),
]

app = get_wsgi_application()


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
