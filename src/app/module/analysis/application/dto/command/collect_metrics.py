"""Collect analysis metrics command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.analysis.domain.value_object import MetricType


@dataclass(frozen=True, slots=True)
class CollectMetricsCommand:
    """Command for one metrics-calculation phase of an analysis.

    Attributes
    ----------
    analysis_id : UUID
        ID of the analysis being processed.
    current_user_id : UUID
        ID of the user who requested the analysis.
    metric_type : MetricType
        Which metric module to calculate.
    """

    analysis_id: UUID
    current_user_id: UUID
    metric_type: MetricType


__all__ = ("CollectMetricsCommand",)
