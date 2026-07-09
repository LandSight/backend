from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class HashedAuthenticationKey(BaseValueObject[str]):
    """Value object for a hashed authentication key."""

    @override
    def _normalize(self, value: str) -> str:
        return value

    @override
    def _validate(self) -> None:
        if not self._value:
            message = "Hashed authentication key must not be empty."
            raise ValidationError(message)


__all__ = ("HashedAuthenticationKey",)
