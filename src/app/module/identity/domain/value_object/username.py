from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class Username(BaseValueObject[str]):
    """Value object for a username."""

    _MIN_LENGTH = 3
    _MAX_LENGTH = 16

    @override
    def _normalize(self, value: str) -> str:
        return value.lower()

    @override
    def _validate(self) -> None:
        if not (self._MIN_LENGTH <= len(self._value) <= self._MAX_LENGTH):
            message = f"Username must be between {self._MIN_LENGTH} and {self._MAX_LENGTH} characters long."
            raise ValidationError(message)
        if not self._value.isalnum():
            message = "Username must contain only alphanumeric characters."
            raise ValidationError(message)
        if not self._value[0].isalpha():
            message = "Username must start with a letter or underscore."
            raise ValidationError(message)


__all__ = ("Username",)
