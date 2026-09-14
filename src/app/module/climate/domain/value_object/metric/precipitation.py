"""Precipitation value object in millimetres."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class Precipitation(BaseValueObject[float]):
    """Precipitation value object in millimetres.

    Invariants:
    - Must be non-negative.
    - Upper bound chosen to cover extreme global annual totals.
    """

    _MIN_VALUE = 0.0
    _MAX_VALUE = 20000.0

    @override
    def _normalize(self, value: float) -> float:
        return round(float(value), 2)

    @override
    def _validate(self) -> None:
        if not (self._MIN_VALUE <= self._value <= self._MAX_VALUE):
            message = f"Precipitation must be between {self._MIN_VALUE} and {self._MAX_VALUE} mm, got {self._value}."
            raise ValidationError(message)


__all__ = ("Precipitation",)
