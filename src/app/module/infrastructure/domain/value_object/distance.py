"""Distance value object in meters."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class Distance(BaseValueObject[float]):
    """Distance between objects, in meters.

    Invariants:
    - Must be a non-negative number (>= 0)
    """

    _MIN_VALUE = 0.0

    @override
    def _normalize(self, value: float) -> float:
        return round(value, 2)

    @override
    def _validate(self) -> None:
        if self._value < self._MIN_VALUE:
            message = f"Distance must be at least {self._MIN_VALUE}, got {self._value}."
            raise ValidationError(message)


__all__ = ("Distance",)
