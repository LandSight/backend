"""Prompt value object."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class Prompt(BaseValueObject[str]):
    """A fully rendered prompt sent to the model.

    Rules:
    - Length: 1-32000 characters
    - No leading/trailing whitespace
    - Normalized: stripped
    """

    _MIN_LENGTH = 1
    _MAX_LENGTH = 32000

    @override
    def _normalize(self, value: str) -> str:
        return value.strip()

    @override
    def _validate(self) -> None:
        if not (self._MIN_LENGTH <= len(self._value) <= self._MAX_LENGTH):
            message = (
                f"Prompt must be between {self._MIN_LENGTH} and {self._MAX_LENGTH} "
                f"characters long, got {len(self._value)}."
            )
            raise ValidationError(message)


__all__ = ("Prompt",)
