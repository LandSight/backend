"""Internal DTOs for the Analysis module."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


# NOTE: Temporary cross-module coupling (MVP).
#
# The aggregate reuses the metric modules' interface-level result DTOs to avoid
# duplicating the metric models. See
# ``app.module.analysis.application.dto.response.parcel_analysis`` for details.


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.climate.interface.internal.dto import ClimateMetricsResult
    from app.module.infrastructure.interface.internal.dto import InfrastructureMetricsResult
    from app.module.topography.interface.internal.dto import TopographyMetricsResult


@dataclass(frozen=True, slots=True)
class AnalyzeParcelInput:
    """Input for aggregating a parcel's metrics."""

    parcel_id: UUID
    current_user_id: UUID


@dataclass(frozen=True, slots=True)
class ParcelAnalysisResult:
    """Result of aggregating a parcel's metrics."""

    parcel_id: UUID
    topography: TopographyMetricsResult
    infrastructure: InfrastructureMetricsResult
    climate: ClimateMetricsResult


__all__ = (
    "AnalyzeParcelInput",
    "ParcelAnalysisResult",
)
