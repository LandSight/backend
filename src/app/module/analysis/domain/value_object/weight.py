"""Weight value object."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class Weight(BaseValueObject[float]):
    """Relative weight of a hierarchy node or metric.

    Invariants:
    - Must be strictly positive
    """

    @override
    def _normalize(self, value: float) -> float:
        return round(float(value), 6)

    @override
    def _validate(self) -> None:
        if self._value <= 0:
            message = f"Weight must be positive, got {self._value}."
            raise ValidationError(message)


__all__ = ("Weight",)
