from __future__ import annotations

import pytest

from django_simple_nav.conf import app_settings


def test_app_settings():
    # stub test until `django-simple-nav` requires custom app settings
    with pytest.raises(AttributeError):
        assert app_settings.foo
