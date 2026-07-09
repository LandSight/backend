"""User entity."""

from typing import TYPE_CHECKING, override

from app.module.identity.domain.value_object import UserId
from app.module.shared.domain.entity import BaseEntity


if TYPE_CHECKING:
    from app.module.identity.domain.value_object import (
        HashedPassword,
        Username,
    )


class User(BaseEntity[UserId]):
    """User entity.

    Represents a registered user in the system.
    """

    def __init__(
        self,
        id: UserId,
        username: Username,
        hashed_password: HashedPassword,
    ) -> None:
        self._username: Username = username
        self._hashed_password: HashedPassword = hashed_password

        super().__init__(id)

    @override
    def _validate(self) -> None:
        pass

    @property
    def username(self) -> Username:
        """Username of the user."""
        return self._username

    @property
    def hashed_password(self) -> HashedPassword:
        """Hashed password of the user."""
        return self._hashed_password


__all__ = ("User",)
