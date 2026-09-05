"""Abstract base entity for infrastructure metrics."""

from __future__ import annotations

from abc import ABC
from typing import override

from app.module.infrastructure.domain.value_object import (
    Buffer,
    InfrastructureMetricsId,
    ParcelId,
)
from app.module.shared.domain.entity import BaseEntity


class InfrastructureMetrics(BaseEntity[InfrastructureMetricsId], ABC):
    """Abstract base for infrastructure metrics of a single category.

    Concrete subclasses map to a dedicated table per category
    (e.g. ``parcel_school_metrics``).

    Attributes
    ----------
    id : InfrastructureMetricsId
        Unique identifier for this metrics record.
    parcel_id : ParcelId
        ID of the parcel these metrics belong to.
    buffer : Buffer
        Buffer radius in meters around the parcel boundary.
    """

    def __init__(
        self,
        id: InfrastructureMetricsId,
        parcel_id: ParcelId,
        buffer: Buffer,
    ) -> None:
        self._parcel_id: ParcelId = parcel_id
        self._buffer: Buffer = buffer

        super().__init__(id)

    @property
    def parcel_id(self) -> ParcelId:
        """ID of the parcel these metrics belong to."""
        return self._parcel_id

    @property
    def buffer(self) -> Buffer:
        """Buffer radius in meters around the parcel boundary."""
        return self._buffer

    @override
    def _validate(self) -> None:
        """Validate the entity's state.

        Per-field invariants are enforced by the wrapped value objects, so this
        entity adds no further checks of its own.
        """
        pass


__all__ = ("InfrastructureMetrics",)
