"""Parcel name value object."""

from __future__ import annotations

import re
from typing import ClassVar, override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class ParcelName(BaseValueObject[str]):
    """Value object for a parcel name.

    Rules:
    - Length: 3-64 characters
    - Allowed: letters, digits, spaces, hyphens, underscores
    - Must start with a letter
    - No leading/trailing whitespace
    - Normalized: stripped and lowercased
    """

    _MIN_LENGTH = 3
    _MAX_LENGTH = 64
    _SPECIAL_CHARS: ClassVar[str] = " _-"
    _PATTERN: ClassVar[re.Pattern] = re.compile(
        rf"^[A-Za-z][A-Za-z0-9{re.escape(_SPECIAL_CHARS)}]{{{_MIN_LENGTH - 1},{_MAX_LENGTH - 1}}}$"
    )

    @override
    def _normalize(self, value: str) -> str:
        return value.strip().lower()

    @override
    def _validate(self) -> None:
        if not (self._MIN_LENGTH <= len(self._value) <= self._MAX_LENGTH):
            message = (
                f"Parcel name must be between {self._MIN_LENGTH} and {self._MAX_LENGTH} "
                f"characters long, got {len(self._value)}."
            )
            raise ValidationError(message)

        if not self._PATTERN.match(self._value):
            allowed = "alphanumeric, spaces, hyphens, and underscores"
            message = f"Parcel name must start with a letter and contain only {allowed} characters."
            raise ValidationError(message)


__all__ = ("ParcelName",)
