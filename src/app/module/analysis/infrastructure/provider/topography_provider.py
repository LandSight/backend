"""Topography provider implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.port import TopographyProvider
from app.module.topography.interface.internal.dto import CalculateMetricsInput


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.topography.interface.internal.dto import TopographyMetricsResult
    from app.module.topography.interface.internal.port import TopographyInternalAPI


class TopographyProviderImpl(TopographyProvider):
    """Topography metrics provider backed by the module's Internal API.

    MVP: always recalculates via ``calculate_metrics``. Later this should read
    the stored snapshot and only recalculate when missing.
    """

    def __init__(self, topography_api: TopographyInternalAPI) -> None:
        self._topography_api = topography_api

    @override
    async def calculate_parcel_metrics(self, parcel_id: UUID, user_id: UUID) -> TopographyMetricsResult:
        """See :class:`app.module.analysis.application.port.TopographyProvider.calculate_parcel_metrics`."""
        return await self._topography_api.calculate_metrics(
            CalculateMetricsInput(parcel_id=parcel_id, current_user_id=user_id),
        )


__all__ = ("TopographyProviderImpl",)
