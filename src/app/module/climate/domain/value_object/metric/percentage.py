"""Percentage / coefficient-of-variation value object."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class Percentage(BaseValueObject[float]):
    """Percentage or coefficient-of-variation value.

    Invariants:
    - Must be non-negative.
    - A CV may exceed 100 % in extremely seasonal climates, so the upper bound
      is deliberately generous.
    """

    _MIN_VALUE = 0.0
    _MAX_VALUE = 1000.0

    @override
    def _normalize(self, value: float) -> float:
        return round(float(value), 2)

    @override
    def _validate(self) -> None:
        if not (self._MIN_VALUE <= self._value <= self._MAX_VALUE):
            message = f"Percentage must be between {self._MIN_VALUE} and {self._MAX_VALUE} %, got {self._value}."
            raise ValidationError(message)


__all__ = ("Percentage",)
