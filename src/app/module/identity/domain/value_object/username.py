import re
from typing import ClassVar, override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class Username(BaseValueObject[str]):
    """Value object for a username."""

    _MIN_LENGTH = 3
    _MAX_LENGTH = 16
    _SPECIAL: ClassVar[str] = "_"
    _PATTERN: ClassVar[re.Pattern] = re.compile(
        rf"^[A-Za-z][A-Za-z0-9{re.escape(_SPECIAL)}]{{{_MIN_LENGTH - 1},{_MAX_LENGTH - 1}}}$"
    )

    @override
    def _normalize(self, value: str) -> str:
        return value.lower()

    @override
    def _validate(self) -> None:
        if not (self._MIN_LENGTH <= len(self._value) <= self._MAX_LENGTH):
            message = (
                f"Username must be between {self._MIN_LENGTH} and {self._MAX_LENGTH} "
                f"characters long, got {len(self._value)}."
            )
            raise ValidationError(message)

        if not self._PATTERN.match(self._value):
            allowed = f"alphanumeric and '{self._SPECIAL}'"
            message = f"Username must start with a letter and contain only {allowed} characters."
            raise ValidationError(message)


__all__ = ("Username",)
