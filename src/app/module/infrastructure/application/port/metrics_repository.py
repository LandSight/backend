"""Metrics repository port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.infrastructure.domain.entity import InfrastructureMetrics
    from app.module.infrastructure.domain.value_object import Category, ParcelId


class MetricsRepository(ABC):
    """Port for infrastructure metrics persistence.

    Implementations dispatch to the per-category tables (e.g.
    ``parcel_school_metrics``) based on the concrete entity type.

    Implementations:
    - :class:`app.module.infrastructure.infrastructure.repository.postgres_metrics_repository.PostgresMetricsRepository`
    """

    @abstractmethod
    async def save(self, metrics: InfrastructureMetrics) -> None:
        """Persist infrastructure metrics.

        Parameters
        ----------
        metrics : InfrastructureMetrics
            Infrastructure metrics entity to save.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_parcel_id_and_category(
        self,
        parcel_id: ParcelId,
        category: Category,
    ) -> InfrastructureMetrics | None:
        """Retrieve infrastructure metrics by parcel ID and category.

        Parameters
        ----------
        parcel_id : ParcelId
            Parcel identifier.
        category : Category
            Infrastructure category.

        Returns
        -------
        InfrastructureMetrics | None
            The metrics if found, ``None`` otherwise.
        """
        raise NotImplementedError


__all__ = ("MetricsRepository",)
