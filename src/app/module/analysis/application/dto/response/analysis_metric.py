"""Analysis metric reference response DTO."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class AnalysisMetricResponse:
    """Response DTO for a single analysis metric reference.

    Attributes
    ----------
    module : str
        Metric module the snapshot belongs to (e.g. ``infrastructure``).
    category : str | None
        Infrastructure category; ``None`` for single-metric modules.
    metrics_id : UUID
        ID of the persisted metrics snapshot.
    """

    module: str
    category: str | None
    metrics_id: UUID


__all__ = ("AnalysisMetricResponse",)
