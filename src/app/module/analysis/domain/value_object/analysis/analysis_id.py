"""Analysis ID value object."""

from __future__ import annotations

from app.module.shared.domain.value_object import EntityIdUUID6ValueObject


class AnalysisId(EntityIdUUID6ValueObject):
    """Analysis ID value object using UUID6."""


__all__ = ("AnalysisId",)
