"""Analysis key value object."""

from __future__ import annotations

import re
from typing import ClassVar, override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class AnalysisKey(BaseValueObject[str]):
    """Key of a hierarchy node or a metric.

    Invariants:
    - 1-64 characters
    - Allowed: letters, digits, underscores, colons, dashes and dots
    - No leading/trailing whitespace
    """

    _MAX_LENGTH = 64
    _PATTERN: ClassVar[re.Pattern[str]] = re.compile(r"^[A-Za-z0-9_:.-]+$")

    @override
    def _normalize(self, value: str) -> str:
        return value.strip()

    @override
    def _validate(self) -> None:
        if not self._value:
            message = "Analysis key must not be empty."
            raise ValidationError(message)
        if len(self._value) > self._MAX_LENGTH:
            message = f"Analysis key must be at most {self._MAX_LENGTH} characters long, got {len(self._value)}."
            raise ValidationError(message)
        if not self._PATTERN.match(self._value):
            message = f"Analysis key '{self._value}' contains unsupported characters."
            raise ValidationError(message)


__all__ = ("AnalysisKey",)
