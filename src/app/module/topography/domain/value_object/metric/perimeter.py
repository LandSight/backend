"""Perimeter value object in meters."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class Perimeter(BaseValueObject[float]):
    """Perimeter value object in meters.

    Invariants:
    - Must be non-negative (>= 0)
    """

    _DECIMAL_PLACES = 2

    @override
    def _normalize(self, value: float) -> float:
        return round(value, self._DECIMAL_PLACES)

    @override
    def _validate(self) -> None:
        if self._value < 0:
            message = f"Perimeter must be non-negative, got {self._value}."
            raise ValidationError(message)


__all__ = ("Perimeter",)
