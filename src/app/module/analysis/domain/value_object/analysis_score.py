"""Analysis score value object."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class AnalysisScore(BaseValueObject[float]):
    """Final analysis score.

    Invariants:
    - Must be in range [0, 10]
    """

    _MIN_VALUE = 0.0
    _MAX_VALUE = 10.0

    @property
    def scale(self) -> str:
        """Score scale derived from the valid value bounds."""
        return f"{self._MIN_VALUE:g}-{self._MAX_VALUE:g}"

    @override
    def _normalize(self, value: float) -> float:
        return round(float(value), 2)

    @override
    def _validate(self) -> None:
        if not (self._MIN_VALUE <= self._value <= self._MAX_VALUE):
            message = f"Analysis score must be between {self._MIN_VALUE} and {self._MAX_VALUE}, got {self._value}."
            raise ValidationError(message)


__all__ = ("AnalysisScore",)
