"""Latitude value object."""

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class Latitude(BaseValueObject[float]):
    """Latitude value object (-90 to 90)."""

    _MIN_VALUE = -90
    _MAX_VALUE = 90

    @override
    def _normalize(self, value: float) -> float:
        return value

    @override
    def _validate(self) -> None:
        if not (self._MIN_VALUE <= self._value <= self._MAX_VALUE):
            message = f"Latitude must be between {self._MIN_VALUE} and {self._MAX_VALUE}, got {self._value}"
            raise ValidationError(message)


__all__ = ("Latitude",)
