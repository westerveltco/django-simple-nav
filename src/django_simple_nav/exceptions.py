from __future__ import annotations


class ReadOnlyProperty(Exception):
    """Raised when trying to set a read-only property."""

    def __init__(self, field: str) -> None:
        super().__init__(f"{field} is read-only")
