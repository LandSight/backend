"""Semantic version value object."""

from __future__ import annotations

import re
from typing import Final, override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object.base import BaseValueObject


_PATTERN: Final = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


class SemanticVersion(BaseValueObject[str]):
    """Version in the ``MAJOR.MINOR.PATCH`` form of Semantic Versioning.

    Invariants:
    - Three dot-separated non-negative integers without leading zeros
    """

    @override
    def _normalize(self, value: str) -> str:
        return value.strip()

    @override
    def _validate(self) -> None:
        if not _PATTERN.match(self._value):
            message = f"Version must be MAJOR.MINOR.PATCH, got '{self._value}'."
            raise ValidationError(message)


__all__ = ("SemanticVersion",)
