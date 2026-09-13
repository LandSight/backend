"""Reference to a metrics snapshot used by an analysis."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.analysis.domain.value_object.metric_type import MetricType


@dataclass(frozen=True, slots=True)
class AnalysisMetricRef:
    """Weak reference to a persisted metrics snapshot.

    Attributes
    ----------
    metric_type : MetricType
        Module the snapshot belongs to.
    metric_id : UUID
        ID of the metrics snapshot.
    category : str | None
        Infrastructure category; ``None`` for single-metric modules.
    """

    metric_type: MetricType
    metric_id: UUID
    category: str | None = None


__all__ = ("AnalysisMetricRef",)
