"""Parcel analysis response DTO."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


# NOTE: Temporary cross-module coupling (MVP).
#
# To avoid duplicating the metric models, the Analysis aggregate currently
# reuses the *interface-level* result DTOs of the metric modules
# (``TopographyMetricsResult``, ``InfrastructureMetricsResult``,
# ``ClimateMetricsResult``). These are framework-agnostic interchange contracts,
# not domain internals, but they still couple Analysis to other modules.
#
# When the Analysis module evolves into full scoring/assessment it should own
# its own output model (or consume metrics via a shared contract) instead of
# referencing other modules' DTOs directly.


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.climate.interface.internal.dto import ClimateMetricsResult
    from app.module.infrastructure.interface.internal.dto import InfrastructureMetricsResult
    from app.module.topography.interface.internal.dto import TopographyMetricsResult


@dataclass(frozen=True, slots=True)
class ParcelAnalysisResponse:
    """Aggregated metrics of a parcel across all metric modules.

    Attributes
    ----------
    parcel_id : UUID
        ID of the parcel.
    topography : TopographyMetricsResult
        Topography metrics.
    infrastructure : InfrastructureMetricsResult
        Infrastructure metrics (per category).
    climate : ClimateMetricsResult
        Climate metrics.
    """

    parcel_id: UUID
    topography: TopographyMetricsResult
    infrastructure: InfrastructureMetricsResult
    climate: ClimateMetricsResult


__all__ = ("ParcelAnalysisResponse",)
