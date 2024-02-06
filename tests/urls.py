from __future__ import annotations

from django.urls import path


def fake_view(request):
    pass


urlpatterns = [
    path("fake-view/", fake_view, name="fake-view"),
]
