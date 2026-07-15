"""Password hasher port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.identity.domain.value_object import HashedPassword, Password


class PasswordHasher(ABC):
    """Port for password hashing.

    Operates on domain :class:`~app.module.identity.domain.value_object.password.Password`
    and :class:`~app.module.identity.domain.value_object.hashed_password.HashedPassword`
    value objects.

    Implementations:
    - :class:`app.module.identity.infrastructure.security.bcrypt_password_hasher.BcryptPasswordHasher`
    """

    @abstractmethod
    def hash(self, password: Password) -> HashedPassword:
        """Hash a password.

        Parameters
        ----------
        password : Password
            Domain password value object.

        Returns
        -------
        HashedPassword
            Hashed password value object.
        """
        raise NotImplementedError

    @abstractmethod
    def verify(self, password: Password, hashed: HashedPassword) -> bool:
        """Verify a password against a hash.

        Parameters
        ----------
        password : Password
            Domain password value object to verify.
        hashed : HashedPassword
            Domain hashed password value object to verify against.

        Returns
        -------
        bool
            ``True`` if the password matches the hash.
        """
        raise NotImplementedError


__all__ = ("PasswordHasher",)
