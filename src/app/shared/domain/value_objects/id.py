import uuid
from typing import Final

from app.shared.domain.errors import InvalidUUIDTypeError, InvalidUUIDVersionError
from app.shared.domain.value_objects.base import BaseValueObject


class EntityIdValueObject(BaseValueObject[uuid.UUID]):
    """Entity ID value object."""

    _UUID_VERSION: Final[int] = 6

    @staticmethod
    def default() -> EntityIdValueObject:
        """Return default entity ID."""
        return EntityIdValueObject(uuid.uuid6())

    def _normalize(self, value: uuid.UUID) -> uuid.UUID:
        return value

    def _validate(self) -> None:
        if not isinstance(self._value, uuid.UUID):
            raise InvalidUUIDTypeError(self._value)
        elif self._value.version != self._UUID_VERSION:
            raise InvalidUUIDVersionError(self._value.version)
