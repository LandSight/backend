"""Domain event emitted when an analysis is deleted."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from app.module.analysis.domain.value_object import AnalysisMetricRef, MetricType


if TYPE_CHECKING:
    from collections.abc import Mapping

    from app.module.analysis.domain.value_object import AnalysisId


ANALYSIS_DELETED_EVENT = "analysis.analysis_deleted"


@dataclass(frozen=True, slots=True)
class AnalysisDeletedEvent:
    """Metric references owned by a deleted analysis.

    The payload is self-contained: the analysis row (and therefore its metric
    references) is already gone by the time a handler runs, so the references
    are captured here.

    Attributes
    ----------
    analysis_id : AnalysisId
        ID of the deleted analysis.
    metrics : tuple[AnalysisMetricRef, ...]
        Metric snapshots the analysis referenced.
    """

    analysis_id: AnalysisId
    metrics: tuple[AnalysisMetricRef, ...]

    def to_payload(self) -> dict[str, object]:
        """Serialize the event into a JSON-compatible payload."""
        return {
            "analysis_id": str(self.analysis_id.unwrap()),
            "metrics": [
                {
                    "metric_type": ref.metric_type.value,
                    "metrics_id": str(ref.metric_id),
                    "category": ref.category,
                }
                for ref in self.metrics
            ],
        }


def metric_refs_from_payload(payload: Mapping[str, object]) -> tuple[AnalysisMetricRef, ...]:
    """Deserialize metric references from an ``AnalysisDeleted`` payload.

    Parameters
    ----------
    payload : Mapping[str, object]
        Event payload produced by :meth:`AnalysisDeletedEvent.to_payload`.

    Returns
    -------
    tuple[AnalysisMetricRef, ...]
        Metric references to clean up.

    Raises
    ------
    TypeError
        If the payload is malformed.
    """
    metrics = payload.get("metrics")
    if not isinstance(metrics, list):
        message = "AnalysisDeleted payload must contain a 'metrics' list."
        raise TypeError(message)

    refs: list[AnalysisMetricRef] = []
    for item in metrics:
        if not isinstance(item, dict):
            message = "Each metric reference in the payload must be an object."
            raise TypeError(message)
        metric_type = item.get("metric_type")
        metrics_id = item.get("metrics_id")
        if metric_type is None or metrics_id is None:
            message = "Each metric reference must contain 'metric_type' and 'metrics_id'."
            raise TypeError(message)
        category = item.get("category")
        refs.append(
            AnalysisMetricRef(
                metric_type=MetricType(str(metric_type)),
                metric_id=UUID(str(metrics_id)),
                category=str(category) if category is not None else None,
            )
        )
    return tuple(refs)


__all__ = ("ANALYSIS_DELETED_EVENT", "AnalysisDeletedEvent", "metric_refs_from_payload")
