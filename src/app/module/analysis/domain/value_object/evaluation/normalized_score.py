"""Normalized score value object."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class NormalizedScore(BaseValueObject[float]):
    """A value normalized to the closed range ``[0, 1]``.

    Used both for normalized metric readings and for aggregated group scores.

    Invariants:
    - Must be in range [0, 1]
    """

    _MIN_VALUE = 0.0
    _MAX_VALUE = 1.0

    @override
    def _normalize(self, value: float) -> float:
        return round(float(value), 4)

    @override
    def _validate(self) -> None:
        if not (self._MIN_VALUE <= self._value <= self._MAX_VALUE):
            message = f"Normalized score must be between {self._MIN_VALUE} and {self._MAX_VALUE}, got {self._value}."
            raise ValidationError(message)


__all__ = ("NormalizedScore",)
