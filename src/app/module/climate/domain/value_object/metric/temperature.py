"""Temperature value object in degrees Celsius."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class Temperature(BaseValueObject[float]):
    """Temperature value object in degrees Celsius.

    Invariants:
    - Must be in range [-100, 60] °C (Earth's extreme surface range).
    """

    _MIN_VALUE = -100.0
    _MAX_VALUE = 60.0

    @override
    def _normalize(self, value: float) -> float:
        return round(float(value), 2)

    @override
    def _validate(self) -> None:
        if not (self._MIN_VALUE <= self._value <= self._MAX_VALUE):
            message = f"Temperature must be between {self._MIN_VALUE} and {self._MAX_VALUE} °C, got {self._value}."
            raise ValidationError(message)


__all__ = ("Temperature",)
