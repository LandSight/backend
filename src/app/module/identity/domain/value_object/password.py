"""Password value object."""

import re
import string
from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class Password(BaseValueObject[str]):
    """Value object for a plain-text password.

    Validates password strength requirements.
    """

    _MIN_LENGTH = 8
    _MAX_LENGTH = 128

    _SPECIAL_CHARS = "!@#$%^&*(),.\"':;{}|<>`~-_=+[]\\/?"

    _UPPERCASE = re.compile(r"[A-Z]")
    _LOWERCASE = re.compile(r"[a-z]")
    _DIGIT = re.compile(r"\d")
    _SPECIAL = re.compile(rf"[{re.escape(_SPECIAL_CHARS)}]")
    _ALLOWED_CHARS = frozenset(string.ascii_letters + string.digits + _SPECIAL_CHARS)

    @override
    def _normalize(self, value: str) -> str:
        return value

    @override
    def _validate(self) -> None:
        if not (self._MIN_LENGTH <= len(self._value) <= self._MAX_LENGTH):
            message = (
                f"Password must be between {self._MIN_LENGTH} and "
                f"{self._MAX_LENGTH} characters long, got {len(self._value)}."
            )
            raise ValidationError(message)

        if not set(self._value).issubset(self._ALLOWED_CHARS):
            message = "Password must contain only ASCII printable characters and no whitespace."
            raise ValidationError(message)

        if not self._UPPERCASE.search(self._value):
            message = "Password must contain at least one uppercase letter."
            raise ValidationError(message)

        if not self._LOWERCASE.search(self._value):
            message = "Password must contain at least one lowercase letter."
            raise ValidationError(message)

        if not self._DIGIT.search(self._value):
            message = "Password must contain at least one digit."
            raise ValidationError(message)

        if not self._SPECIAL.search(self._value):
            message = "Password must contain at least one special character."
            raise ValidationError(message)


__all__ = ("Password",)
