"""Buffer radius value object in meters."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class Buffer(BaseValueObject[int]):
    """Buffer radius in meters around the parcel boundary.

    Invariants:
    - Must be a positive integer within [1, 10000]
    """

    _MIN_VALUE = 1
    _MAX_VALUE = 10000

    @override
    def _normalize(self, value: int) -> int:
        return int(value)

    @override
    def _validate(self) -> None:
        if not (self._MIN_VALUE <= self._value <= self._MAX_VALUE):
            message = f"Buffer must be between {self._MIN_VALUE} and {self._MAX_VALUE} meters, got {self._value}."
            raise ValidationError(message)


__all__ = ("Buffer",)
