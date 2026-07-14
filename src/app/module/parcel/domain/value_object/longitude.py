"""Longitude value object."""

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class Longitude(BaseValueObject[float]):
    """Latitude value object (-180 to 180)."""

    _MIN_VALUE = -180
    _MAX_VALUE = 180

    @override
    def _normalize(self, value: float) -> float:
        return value

    @override
    def _validate(self) -> None:
        if not (self._MIN_VALUE <= self._value <= self._MAX_VALUE):
            message = f"Longitude must be between {self._MIN_VALUE} and {self._MAX_VALUE}, got {self._value}"
            raise ValidationError(message)


__all__ = ("Longitude",)
