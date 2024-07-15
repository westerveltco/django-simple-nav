from __future__ import annotations

import sys
from typing import Protocol

from django.http import HttpRequest
from django.template.context import Context
from django.utils.safestring import SafeString

if sys.version_info >= (3, 12):
    from typing import override as typing_override
else:
    from typing_extensions import (
        override as typing_override,  # pyright: ignore[reportUnreachable]
    )

override = typing_override


class EngineTemplate(Protocol):
    def render(
        self,
        context: Context | dict[str, object] | None = ...,
        request: HttpRequest | None = ...,
    ) -> SafeString: ...
