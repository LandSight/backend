from typing import override

from app.module.shared.domain.value_object.base import BaseValueObject


class HashedPassword(BaseValueObject[str]):
    """Value object for a hashed password."""

    @override
    def _normalize(self, value: str) -> str:
        return value

    @override
    def _validate(self) -> None:
        pass
