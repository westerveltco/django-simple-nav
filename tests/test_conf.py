from __future__ import annotations

import pytest
from django.conf import settings

from simple_nav.conf import SIMPLE_NAV_SETTINGS_NAME
from simple_nav.conf import app_settings


def test_default_settings():
    user_settings = getattr(settings, SIMPLE_NAV_SETTINGS_NAME, {})

    assert user_settings == {}


def test_app_settings():
    # temporary until app actually has settings
    with pytest.raises(AttributeError):
        app_settings.FOO  # noqa: B018
