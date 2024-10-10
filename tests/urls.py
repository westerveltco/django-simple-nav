from __future__ import annotations

from django.urls import path


def home(request): ...


def fake_view(request): ...


urlpatterns = [
    path("fake-view/", fake_view, name="fake-view"),
    path("", home, name="home"),
]
