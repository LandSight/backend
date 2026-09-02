"""Elongation index value object."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class ElongationIndex(BaseValueObject[float]):
    """Elongation index value object (width/length).

    Measures how elongated a shape is using the minimum bounding rectangle.
    A perfect square or circle has elongation ≈ 1.0.
    Lower values indicate more elongated shapes.

    Invariants:
    - Must be in range [0, 1] (width <= length by definition)
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
            message = f"Elongation index must be between {self._MIN_VALUE} and {self._MAX_VALUE}, got {self._value}."
            raise ValidationError(message)


__all__ = ("ElongationIndex",)
