"""Contribution value object."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class Contribution(BaseValueObject[float]):
    """Weighted contribution of a node or metric to its parent.

    Invariants:
    - Must not be negative
    """

    @override
    def _normalize(self, value: float) -> float:
        return round(float(value), 4)

    @override
    def _validate(self) -> None:
        if self._value < 0:
            message = f"Contribution must not be negative, got {self._value}."
            raise ValidationError(message)


__all__ = ("Contribution",)
