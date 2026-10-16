"""Analysis evaluation ID value object."""

from __future__ import annotations

from app.module.shared.domain.value_object import EntityIdUUID6ValueObject


class AnalysisEvaluationId(EntityIdUUID6ValueObject):
    """Analysis evaluation ID value object using UUID6."""


__all__ = ("AnalysisEvaluationId",)
