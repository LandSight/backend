"""Legal basis value object."""

from __future__ import annotations

from typing import ClassVar, override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class LegalBasis(BaseValueObject[str]):
    """Short reference to the rule that defines a zone, e.g. a Water Code article.

    It is a citation shown in reports, not the text of the rule.

    Invariants:
    - 1 to 256 characters after trimming
    """

    MAX_LENGTH: ClassVar[int] = 256

    @override
    def _normalize(self, value: str) -> str:
        return " ".join(value.split())

    @override
    def _validate(self) -> None:
        if not self._value:
            message = "Legal basis must not be empty."
            raise ValidationError(message)
        if len(self._value) > self.MAX_LENGTH:
            message = f"Legal basis must be at most {self.MAX_LENGTH} characters, got {len(self._value)}."
            raise ValidationError(message)


__all__ = ("LegalBasis",)
