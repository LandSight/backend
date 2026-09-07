"""Climate metrics provider port."""

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

    from app.module.climate.interface.internal.dto import ClimateMetricsResult


class ClimateProvider(ABC):
    """Port for calculating a parcel's climate metrics.

    The owning module resolves the parcel and enforces access, so Analysis never
    re-implements ownership rules.

    MVP: always triggers recalculation. Later this should read the stored snapshot
    when available and only recalculate when missing.

    Implementations:
    - :class:`app.module.analysis.infrastructure.provider.climate_provider.ClimateProviderImpl`
    """

    @abstractmethod
    async def calculate_parcel_metrics(self, parcel_id: UUID, user_id: UUID) -> ClimateMetricsResult:
        """Return the parcel's climate metrics for an authorized user.

        Parameters
        ----------
        parcel_id : UUID
            ID of the parcel.
        user_id : UUID
            ID of the user performing the request.

        Returns
        -------
        ClimateMetricsResult
            The parcel's climate metrics.

        Raises
        ------
        app.module.climate.application.error.ClimateMetricsNotFoundError
            If no metrics have been calculated for the parcel.
        """
        raise NotImplementedError


__all__ = ("ClimateProvider",)
