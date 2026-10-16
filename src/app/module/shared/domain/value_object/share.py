"""Share value object: a part of a whole as a fraction."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object.base import BaseValueObject


class Share(BaseValueObject[float]):
    """Part of a whole as a fraction in ``[0, 1]`` (``0.25`` is a quarter).

    Invariants:
    - Must be within [0, 1]
    """

    _MIN_VALUE = 0.0
    _MAX_VALUE = 1.0
    _DECIMAL_PLACES = 4

    @override
    def _normalize(self, value: float) -> float:
        return round(float(value), self._DECIMAL_PLACES)

    @override
    def _validate(self) -> None:
        if not self._MIN_VALUE <= self._value <= self._MAX_VALUE:
            message = f"Share must be within [{self._MIN_VALUE}, {self._MAX_VALUE}], got {self._value}."
            raise ValidationError(message)


__all__ = ("Share",)
