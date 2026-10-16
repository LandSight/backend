"""Compactness index value object."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class CompactnessIndex(BaseValueObject[float]):
    """Compactness index value object, relative to a square.

    The Polsby-Popper score (4πA/P²) divided by that of a square (π/4) and
    capped at 1.0. A square has compactness = 1.0, a 1:2 rectangle about 0.89;
    lower values indicate more elongated or irregular shapes.

    Invariants:
    - Must be in range [0, 1]
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
