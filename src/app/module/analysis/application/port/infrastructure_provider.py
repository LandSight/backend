"""Infrastructure metrics provider port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


# NOTE: Temporary cross-module coupling (MVP).
#
# The provider return type is the other module's interface-level result DTO to
# avoid duplicating the metric model. See
# ``app.module.analysis.application.dto.response.parcel_analysis`` for details.


if TYPE_CHECKING:
    from uuid import UUID

    from app.module.infrastructure.interface.internal.dto import InfrastructureMetricsResult


class InfrastructureProvider(ABC):
    """Port for calculating a parcel's infrastructure metrics.

    The owning module resolves the parcel and enforces access, so Analysis never
    re-implements ownership rules.

    MVP: always triggers recalculation with explicit categories. Later this should
    read the stored snapshot when available and only recalculate when missing.

    Implementations:
    - :class:`app.module.analysis.infrastructure.provider.infrastructure_provider.InfrastructureProviderImpl`
    """

    @abstractmethod
    async def calculate_parcel_metrics(
        self,
        parcel_id: UUID,
        user_id: UUID,
        categories: list[tuple[str, int]],
    ) -> InfrastructureMetricsResult:
        """Return the parcel's infrastructure metrics for an authorized user.

        Parameters
        ----------
        parcel_id : UUID
            ID of the parcel.
        user_id : UUID
            ID of the user performing the request.
        categories : list[tuple[str, int]]
            Requested ``(category, buffer_meters)`` pairs.

        Returns
        -------
        InfrastructureMetricsResult
            The parcel's infrastructure metrics (per category).
        """
        raise NotImplementedError


__all__ = ("InfrastructureProvider",)
