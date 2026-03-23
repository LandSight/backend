from typing import Self
from uuid import UUID, uuid6

from app.shared.domain.error import InvalidEntityIdError
from app.shared.domain.value_object.base import BaseValueObject


class BaseEntityIdValueObject(BaseValueObject[UUID]):
    """Base entity ID value object."""

    _UUID_VERSION = 6

    def _normalize(self, value: UUID) -> UUID:
        return value

    def _validate(self) -> None:
        if self._value.version != self._UUID_VERSION:
            message = f"Invalid UUID version: {self._value.version}, expected {self._UUID_VERSION}"
            raise InvalidEntityIdError(message)

    @classmethod
    def default(cls) -> Self:
        """Return a default entity ID value object."""
        return cls(uuid6())
