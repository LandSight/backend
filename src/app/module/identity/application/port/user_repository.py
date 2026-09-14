"""User repository port."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.identity.domain.entity.user import User
    from app.module.identity.domain.value_object import (
        UserId,
        Username,
    )


class UserRepository(ABC):
    """Port for user persistence.

    Implementations:
    - :class:`app.module.identity.infrastructure.repository.postgres_user_repository.PostgresUserRepository`
    """

    @abstractmethod
    async def save(self, user: User) -> None:
        """Persist a user.

        Parameters
        ----------
        user : User
            User entity to save.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: UserId) -> User | None:
        """Retrieve a user by their ID.

        Parameters
        ----------
        user_id : UserId
            User identifier.

        Returns
        -------
        User | None
            The user if found, ``None`` otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_username(self, username: Username) -> User | None:
        """Retrieve a user by their username.

        Parameters
        ----------
        username : Username
            Username to look up.

        Returns
        -------
        User | None
            The user if found, ``None`` otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user_id: UserId) -> None:
        """Delete a user by their ID.

        Parameters
        ----------
        user_id : UserId
            User identifier.
        """
        raise NotImplementedError


__all__ = ("UserRepository",)
