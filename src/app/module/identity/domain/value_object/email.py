import re
from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class Email(BaseValueObject[str]):
    """Value object for an email address."""

    _PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    @override
    def _normalize(self, value: str) -> str:
        return value.lower().strip()

    @override
    def _validate(self) -> None:
        if not self._value:
            message = "Email must not be empty."
            raise ValidationError(message)
        if not self._PATTERN.match(self._value):
            message = f"Invalid email format: {self._value}"
            raise ValidationError(message)


__all__ = ("Email",)
