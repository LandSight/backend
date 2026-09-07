"""Topography metrics provider port."""

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

    from app.module.topography.interface.internal.dto import TopographyMetricsResult


class TopographyProvider(ABC):
    """Port for calculating a parcel's topography metrics.

    The owning module resolves the parcel and enforces access, so Analysis never
    re-implements ownership rules.

    MVP: always triggers recalculation. Later this should read the stored snapshot
    when available and only recalculate when missing.

    Implementations:
    - :class:`app.module.analysis.infrastructure.provider.topography_provider.TopographyProviderImpl`
    """

    @abstractmethod
    async def calculate_parcel_metrics(self, parcel_id: UUID, user_id: UUID) -> TopographyMetricsResult:
        """Return the parcel's topography metrics for an authorized user.

        Parameters
        ----------
        parcel_id : UUID
            ID of the parcel.
        user_id : UUID
            ID of the user performing the request.

        Returns
        -------
        TopographyMetricsResult
            The parcel's topography metrics.

        Raises
        ------
        app.module.topography.application.error.TopographyMetricsNotFoundError
            If no metrics have been calculated for the parcel.
        """
        raise NotImplementedError


__all__ = ("TopographyProvider",)
