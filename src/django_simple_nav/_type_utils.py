from __future__ import annotations

import sys
from typing import Protocol

from django.http import HttpRequest
from django.template.context import Context
from django.utils.safestring import SafeString

if sys.version_info >= (3, 12):
    from typing import override as typing_override
else:  # pragma: no cover
    from typing_extensions import (
        override as typing_override,  # pyright: ignore[reportUnreachable]
    )

override = typing_override


# https://github.com/typeddjango/django-stubs/blob/b6e8ea9b4279ece87d14e38226c265e4f0aadccd/django-stubs/template/backends/base.pyi#L22-L28
class EngineTemplate(Protocol):
    def render(
        self,
        context: Context | dict[str, object] | None = ...,
        request: HttpRequest | None = ...,
    ) -> SafeString: ...
