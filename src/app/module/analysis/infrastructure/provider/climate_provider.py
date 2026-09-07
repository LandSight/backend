"""Climate provider implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.port import ClimateProvider
from app.module.climate.interface.internal.dto import CalculateMetricsInput


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.climate.interface.internal.dto import ClimateMetricsResult
    from app.module.climate.interface.internal.port import ClimateInternalAPI


class ClimateProviderImpl(ClimateProvider):
    """Climate metrics provider backed by the module's Internal API.

    MVP: always recalculates via ``calculate_metrics``. Later this should read
    the stored snapshot and only recalculate when missing.
    """

    def __init__(self, climate_api: ClimateInternalAPI) -> None:
        self._climate_api = climate_api

    @override
    async def calculate_parcel_metrics(self, parcel_id: UUID, user_id: UUID) -> ClimateMetricsResult:
        """See :class:`app.module.analysis.application.port.ClimateProvider.calculate_parcel_metrics`."""
        return await self._climate_api.calculate_metrics(
            CalculateMetricsInput(parcel_id=parcel_id, current_user_id=user_id),
        )


__all__ = ("ClimateProviderImpl",)
