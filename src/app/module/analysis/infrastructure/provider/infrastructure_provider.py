"""Infrastructure provider implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.analysis.application.port import InfrastructureProvider
from app.module.infrastructure.interface.internal.dto import (
    CalculateMetricsInput,
    CategoryRequestInput,
)


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.infrastructure.interface.internal.dto import InfrastructureMetricsResult
    from app.module.infrastructure.interface.internal.port import InfrastructureInternalAPI


class InfrastructureProviderImpl(InfrastructureProvider):
    """Infrastructure metrics provider backed by the module's Internal API.

    MVP: always recalculates via ``calculate_metrics`` (default categories).
    Later this should read the stored snapshot and only recalculate when missing.
    """

    def __init__(self, infrastructure_api: InfrastructureInternalAPI) -> None:
        self._infrastructure_api = infrastructure_api

    @override
    async def calculate_parcel_metrics(
        self,
        parcel_id: UUID,
        user_id: UUID,
        categories: list[tuple[str, int]],
    ) -> InfrastructureMetricsResult:
        """See :class:`app.module.analysis.application.port.InfrastructureProvider.calculate_parcel_metrics`."""
        return await self._infrastructure_api.calculate_metrics(
            CalculateMetricsInput(
                parcel_id=parcel_id,
                current_user_id=user_id,
                categories=[CategoryRequestInput(category=category, buffer=buffer) for category, buffer in categories],
            ),
        )


__all__ = ("InfrastructureProviderImpl",)
