"""Bcrypt password hasher implementation."""

from __future__ import annotations

from typing import override

import bcrypt

from app.module.identity.application.port import PasswordHasher
from app.module.identity.domain.value_object import HashedPassword, Password


class BcryptPasswordHasher(PasswordHasher):
    """Hash and verify passwords using bcrypt."""

    @override
    def hash(self, password: Password) -> HashedPassword:
        """See :class:`app.module.identity.application.port.PasswordHasher.hash`."""
        hashed = bcrypt.hashpw(password.unwrap().encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        return HashedPassword(hashed)

    @override
    def verify(self, password: Password, hashed: HashedPassword) -> bool:
        """See :class:`app.module.identity.application.port.PasswordHasher.verify`."""
        return bcrypt.checkpw(password.unwrap().encode("utf-8"), hashed.unwrap().encode("utf-8"))


__all__ = ("BcryptPasswordHasher",)
