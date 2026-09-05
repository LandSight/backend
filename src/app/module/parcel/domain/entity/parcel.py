"""Parcel entity representing a land plot."""

from typing import TYPE_CHECKING, override

from app.module.parcel.domain.value_object import (
    OwnerId,
    ParcelId,
    ParcelName,
)
from app.module.shared.domain.entity import BaseEntity


if TYPE_CHECKING:
    from app.module.shared.domain.value_object import Polygon


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
    owner_id : OwnerId
        ID of the user who owns this parcel.
    """

    def __init__(
        self,
        id: ParcelId,
        name: ParcelName,
        polygon: Polygon,
        owner_id: OwnerId,
    ) -> None:
        self._name: ParcelName = name
        self._polygon: Polygon = polygon
        self._owner_id: OwnerId = owner_id

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

    @property
    def owner_id(self) -> OwnerId:
        """ID of the user who owns this parcel."""
        return self._owner_id


__all__ = ("Parcel",)
