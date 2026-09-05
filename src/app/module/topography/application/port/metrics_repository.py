"""Metrics repository port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.topography.domain.entity.topography_metrics import TopographyMetrics
    from app.module.topography.domain.value_object.metric import ParcelId, TopographyMetricsId


class MetricsRepository(ABC):
    """Port for topography metrics persistence.

    Implementations:
    - :class:`app.module.topography.infrastructure.repository.postgres_metrics_repository.PostgresMetricsRepository`
    """

    @abstractmethod
    async def save(self, metrics: TopographyMetrics) -> TopographyMetrics:
        """Persist topography metrics and return the persisted entity.

        Parameters
        ----------
        metrics : TopographyMetrics
            Topography metrics entity to save.

        Returns
        -------
        TopographyMetrics
            The persisted entity.
        """
        raise NotImplementedError

    @abstractmethod
    async def get(self, metrics_id: TopographyMetricsId) -> TopographyMetrics | None:
        """Retrieve topography metrics by their ID.

        Parameters
        ----------
        metrics_id : TopographyMetricsId
            Metrics identifier.

        Returns
        -------
        TopographyMetrics | None
            The metrics if found, ``None`` otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_parcel_metrics(self, parcel_id: ParcelId) -> TopographyMetrics | None:
        """Retrieve the current topography metrics for a parcel.

        MVP keeps a single metrics snapshot per parcel, overwritten on each
        recalculation.

        Parameters
        ----------
        parcel_id : ParcelId
            Parcel identifier.

        Returns
        -------
        TopographyMetrics | None
            The current metrics if any exist, ``None`` otherwise.
        """
        raise NotImplementedError


__all__ = ("MetricsRepository",)
