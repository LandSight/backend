"""Interpretation ID value object."""

from __future__ import annotations

from app.module.shared.domain.value_object import EntityIdUUID6ValueObject


class InterpretationId(EntityIdUUID6ValueObject):
    """Interpretation report ID value object using UUID6."""


__all__ = ("InterpretationId",)
