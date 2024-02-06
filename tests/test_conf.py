from __future__ import annotations

import pytest
from django.conf import settings

from django_simple_nav.conf import DJANGO_SIMPLE_NAV_SETTINGS_NAME
from django_simple_nav.conf import app_settings


def test_default_settings():
    user_settings = getattr(settings, DJANGO_SIMPLE_NAV_SETTINGS_NAME, {})

    assert user_settings == {}


def test_app_settings():
    # temporary until app actually has settings
    with pytest.raises(AttributeError):
        app_settings.FOO  # noqa: B018
