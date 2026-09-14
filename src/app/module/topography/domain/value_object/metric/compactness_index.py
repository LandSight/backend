"""Compactness index value object."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class CompactnessIndex(BaseValueObject[float]):
    """Compactness index value object (4πA/P²).

    Measures how compact a shape is. A perfect circle has compactness = 1.0.
    Lower values indicate more irregular shapes.

    Invariants:
    - Must be in range [0, 1] (by the isoperimetric inequality)
    """

    _DECIMAL_PLACES = 4
    _MIN_VALUE = 0.0
    _MAX_VALUE = 1.0

    @override
    def _normalize(self, value: float) -> float:
        return round(value, self._DECIMAL_PLACES)

    @override
    def _validate(self) -> None:
        if not (self._MIN_VALUE <= self._value <= self._MAX_VALUE):
            message = f"Compactness index must be between {self._MIN_VALUE} and {self._MAX_VALUE}, got {self._value}."
            raise ValidationError(message)


__all__ = ("CompactnessIndex",)
