"""Bcrypt password hasher implementation."""

from typing import override

import bcrypt

from app.module.identity.application.port import PasswordHasher


class BcryptPasswordHasher(PasswordHasher):
    """Hash and verify passwords using bcrypt."""

    @override
    def hash(self, password: str) -> str:
        """See :class:`app.module.identity.application.port.PasswordHasher.hash`."""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @override
    def verify(self, password: str, hashed: str) -> bool:
        """See :class:`app.module.identity.application.port.PasswordHasher.verify`."""
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


__all__ = ("BcryptPasswordHasher",)
