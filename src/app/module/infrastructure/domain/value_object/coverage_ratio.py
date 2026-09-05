"""Coverage ratio value object."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class CoverageRatio(BaseValueObject[float]):
    """Fraction of the buffer zone covered by objects.

    Invariants:
    - Must be in range [0, 1]
    """

    _MIN_VALUE = 0.0
    _MAX_VALUE = 1.0
    _DECIMAL_PLACES = 4

    @override
    def _normalize(self, value: float) -> float:
        return round(value, self._DECIMAL_PLACES)

    @override
    def _validate(self) -> None:
        if not (self._MIN_VALUE <= self._value <= self._MAX_VALUE):
            message = f"CoverageRatio must be between {self._MIN_VALUE} and {self._MAX_VALUE}, got {self._value}."
            raise ValidationError(message)


__all__ = ("CoverageRatio",)
