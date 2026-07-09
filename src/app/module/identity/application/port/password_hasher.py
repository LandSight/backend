"""Password hasher port."""

from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    """Port for password hashing.

    Implementations:
    - :class:`app.module.identity.infrastructure.auth.password_hasher.BcryptPasswordHasher`
    """

    @abstractmethod
    def hash(self, password: str) -> str:
        """Hash a plain-text password.

        Parameters
        ----------
        password : str
            Plain-text password.

        Returns
        -------
        str
            Hashed password.
        """
        raise NotImplementedError

    @abstractmethod
    def verify(self, password: str, hashed: str) -> bool:
        """Verify a plain-text password against a hash.

        Parameters
        ----------
        password : str
            Plain-text password to verify.
        hashed : str
            Stored hash to verify against.

        Returns
        -------
        bool
            ``True`` if the password matches the hash.
        """
        raise NotImplementedError


__all__ = ("PasswordHasher",)
