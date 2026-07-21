"""Geographic point value object."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.value_object import BaseValueObject, Latitude, Longitude


class GeoPoint(BaseValueObject[tuple[Latitude, Longitude]]):
    """Geographic point value object."""

    @property
    def latitude(self) -> Latitude:
        """Latitude of geographic point."""
        return self._value[0]

    @property
    def longitude(self) -> Longitude:
        """Longitude of geographic point."""
        return self._value[1]

    @override
    def _normalize(self, value: tuple[Latitude, Longitude]) -> tuple[Latitude, Longitude]:
        return value

    @override
    def _validate(self) -> None:
        pass

    @classmethod
    def create(cls, lat: float, lon: float) -> GeoPoint:
        """Create a GeoPoint from raw latitude and longitude values."""
        return cls((Latitude(lat), Longitude(lon)))

    def to_tuple(self) -> tuple[float, float]:
        """Return (lat, lon) as floats."""
        return (self.latitude.unwrap(), self.longitude.unwrap())


__all__ = ("GeoPoint",)
