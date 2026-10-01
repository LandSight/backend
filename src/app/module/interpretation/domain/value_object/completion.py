"""Completion value object."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.value_object import BaseValueObject


class Completion(BaseValueObject[str]):
    """A raw answer returned by the model.

    An empty completion is allowed: the caller treats it as a generation
    failure and falls back to safe text.
    """

    @override
    def _normalize(self, value: str) -> str:
        return value

    @override
    def _validate(self) -> None:
        """Allow any completion, including an empty one."""


__all__ = ("Completion",)
