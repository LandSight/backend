"""Parcel entity representing a land plot."""

from typing import override

from app.module.parcel.domain.value_object import ParcelId, ParcelName, Polygon
from app.module.shared.domain.entity import BaseEntity


class Parcel(BaseEntity[ParcelId]):
    """Land parcel entity.

    Attributes
    ----------
    id : ParcelId
        Unique identifier for the parcel.
    name : ParcelName
        Human-readable name of the parcel.
    polygon : Polygon
        Geographic boundary of the parcel.
    """

    def __init__(
        self,
        id: ParcelId,
        name: ParcelName,
        polygon: Polygon,
    ) -> None:
        self._name: ParcelName = name
        self._polygon: Polygon = polygon

        super().__init__(id)

    @override
    def _validate(self) -> None:
        pass

    @property
    def name(self) -> ParcelName:
        """Name of the parcel."""
        return self._name

    @property
    def polygon(self) -> Polygon:
        """Geographic boundary of the parcel."""
        return self._polygon


__all__ = ("Parcel",)
