"""Density value object."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class Density(BaseValueObject[float]):
    """Quantity per unit area (e.g. kilometres of road per square kilometre).

    The unit is defined by the metric the value belongs to and is not part of
    the value object.

    Invariants:
    - Must be non-negative (>= 0)
    """

    _DECIMAL_PLACES = 4

    @override
    def _normalize(self, value: float) -> float:
        return round(value, self._DECIMAL_PLACES)

    @override
    def _validate(self) -> None:
        if self._value < 0:
            message = f"Density must be non-negative, got {self._value}."
            raise ValidationError(message)


__all__ = ("Density",)
