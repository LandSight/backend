"""Slope value object in degrees."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class Slope(BaseValueObject[float]):
    """Slope value object in degrees.

    Invariants:
    - Must be in range [0, 90]
    """

    _MIN_VALUE = 0
    _MAX_VALUE = 90

    @override
    def _normalize(self, value: float) -> float:
        return round(value, 2)

    @override
    def _validate(self) -> None:
        if not (self._MIN_VALUE <= self._value <= self._MAX_VALUE):
            message = f"Slope must be between {self._MIN_VALUE} and {self._MAX_VALUE} degrees, got {self._value}."
            raise ValidationError(message)


__all__ = ("Slope",)
