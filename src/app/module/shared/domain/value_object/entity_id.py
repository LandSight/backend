from typing import override
from uuid import UUID

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object.base import BaseValueObject


class EntityIdUUID6ValueObject(BaseValueObject[UUID]):
    """Entity ID value object using UUID6."""

    _UUID_VERSION = 6

    @override
    def _normalize(self, value: UUID) -> UUID:
        return value

    @override
    def _validate(self) -> None:
        if self._value.version != self._UUID_VERSION:
            message = f"Invalid UUID version: {self._value.version}"
            raise ValidationError(message)


__all__ = ("EntityIdUUID6ValueObject",)
