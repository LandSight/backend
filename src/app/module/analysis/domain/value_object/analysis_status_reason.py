"""Analysis status reason value object."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class AnalysisStatusReason(BaseValueObject[str]):
    """Value object for a human-readable analysis status explanation.

    Rules:
    - Must not be empty
    - Normalized: stripped and truncated to 512 characters, because the text
      usually comes from a system error and recording a failure must not fail
    """

    _MAX_LENGTH = 512
    _DEFAULT_FAILURE = "Analysis failed."

    @classmethod
    def from_error(cls, error: Exception) -> AnalysisStatusReason:
        """Build a reason from an error, falling back to a generic message."""
        return cls(str(error).strip() or cls._DEFAULT_FAILURE)

    @override
    def _normalize(self, value: str) -> str:
        return value.strip()[: self._MAX_LENGTH]

    @override
    def _validate(self) -> None:
        if not self._value:
            message = "Analysis status reason must not be empty."
            raise ValidationError(message)


__all__ = ("AnalysisStatusReason",)
