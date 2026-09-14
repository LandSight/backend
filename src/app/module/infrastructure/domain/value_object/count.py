"""Count value object for the number of objects in a buffer."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class Count(BaseValueObject[int]):
    """Number of objects in a buffer zone.

    Invariants:
    - Must be a non-negative integer (>= 0)
    """

    _MIN_VALUE = 0

    @override
    def _normalize(self, value: int) -> int:
        return int(value)

    @override
    def _validate(self) -> None:
        if self._value < self._MIN_VALUE:
            message = f"Count must be at least {self._MIN_VALUE}, got {self._value}."
            raise ValidationError(message)


__all__ = ("Count",)
