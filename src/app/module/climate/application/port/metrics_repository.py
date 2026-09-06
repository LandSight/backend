"""Metrics repository port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.climate.domain.entity.climate_metrics import ClimateMetrics
    from app.module.climate.domain.value_object.metric import ClimateMetricsId, ParcelId


class MetricsRepository(ABC):
    """Port for climate metrics persistence.

    Implementations:
    - :class:`app.module.climate.infrastructure.repository.postgres_metrics_repository.PostgresMetricsRepository`
    """

    @abstractmethod
    async def save(self, metrics: ClimateMetrics) -> ClimateMetrics:
        """Persist climate metrics and return the persisted entity.

        Parameters
        ----------
        metrics : ClimateMetrics
            Climate metrics entity to save.

        Returns
        -------
        ClimateMetrics
            The persisted entity.
        """
        raise NotImplementedError

    @abstractmethod
    async def get(self, metrics_id: ClimateMetricsId) -> ClimateMetrics | None:
        """Retrieve climate metrics by their ID.

        Parameters
        ----------
        metrics_id : ClimateMetricsId
            Metrics identifier.

        Returns
        -------
        ClimateMetrics | None
            The metrics if found, ``None`` otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_parcel_metrics(self, parcel_id: ParcelId) -> ClimateMetrics | None:
        """Retrieve the current climate metrics for a parcel.

        MVP keeps a single metrics snapshot per parcel, overwritten on each
        recalculation.

        Parameters
        ----------
        parcel_id : ParcelId
            Parcel identifier.

        Returns
        -------
        ClimateMetrics | None
            The current metrics if any exist, ``None`` otherwise.
        """
        raise NotImplementedError


__all__ = ("MetricsRepository",)
