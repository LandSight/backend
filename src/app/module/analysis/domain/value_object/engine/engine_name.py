"""Engine name value object."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class EngineName(BaseValueObject[str]):
    """Value object for a scoring engine display name.

    Rules:
    - Length: 1-64 characters
    - No leading/trailing whitespace
    - Normalized: stripped (case-sensitive for display)
    """

    _MIN_LENGTH = 1
    _MAX_LENGTH = 64

    @override
    def _normalize(self, value: str) -> str:
        return value.strip()

    @override
    def _validate(self) -> None:
        if not (self._MIN_LENGTH <= len(self._value) <= self._MAX_LENGTH):
            message = (
                f"Engine name must be between {self._MIN_LENGTH} and "
                f"{self._MAX_LENGTH} characters long, got {len(self._value)}."
            )
            raise ValidationError(message)


__all__ = ("EngineName",)
