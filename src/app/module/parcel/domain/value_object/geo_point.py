"""Geographic point value object."""

from __future__ import annotations

from dataclasses import dataclass
from typing import override

from app.module.parcel.domain.value_object.latitude import Latitude
from app.module.parcel.domain.value_object.longitude import Longitude
from app.module.shared.domain.value_object import BaseValueObject


@dataclass(frozen=True, slots=True)
class _GeoPointCoords:
    """Internal immutable container for lat/lon."""

    lat: Latitude
    lon: Longitude


class GeoPoint(BaseValueObject[_GeoPointCoords]):
    """Geographic point value object."""

    @property
    def latitude(self) -> Latitude:
        """Latitude of geographic point."""
        return self._value.lat

    @property
    def longitude(self) -> Longitude:
        """Longitude of geographic point."""
        return self._value.lon

    @override
    def _normalize(self, value: tuple[float, float] | _GeoPointCoords) -> _GeoPointCoords:
        if isinstance(value, _GeoPointCoords):
            return value

        lat_val, lon_val = value
        return _GeoPointCoords(
            lat=Latitude(lat_val),
            lon=Longitude(lon_val),
        )

    @override
    def _validate(self) -> None:
        pass

    def to_tuple(self) -> tuple[float, float]:
        """Return (lat, lon) as floats."""
        return (self._value.lat.unwrap(), self._value.lon.unwrap())


__all__ = ("GeoPoint",)
