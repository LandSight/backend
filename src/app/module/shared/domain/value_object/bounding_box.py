"""Bounding box value object."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import InvariantViolationError
from app.module.shared.domain.value_object import BaseValueObject
from app.module.shared.domain.value_object.latitude import Latitude
from app.module.shared.domain.value_object.longitude import Longitude


class BoundingBox(BaseValueObject[tuple[Latitude, Longitude, Latitude, Longitude]]):
    """Bounding box value object.

    Order: (min_lat, min_lon, max_lat, max_lon).

    Invariants:
    - min_lat < max_lat
    - min_lon < max_lon
    - All values validated by Latitude/Longitude VOs
    """

    @override
    def _normalize(
        self,
        value: tuple[Latitude, Longitude, Latitude, Longitude],
    ) -> tuple[Latitude, Longitude, Latitude, Longitude]:
        return value

    @override
    def _validate(self) -> None:
        min_lat, min_lon, max_lat, max_lon = self._value

        if min_lat.unwrap() >= max_lat.unwrap():
            message = f"min_lat ({min_lat.unwrap()}) must be less than max_lat ({max_lat.unwrap()})."
            raise InvariantViolationError(message)

        if min_lon.unwrap() >= max_lon.unwrap():
            message = f"min_lon ({min_lon.unwrap()}) must be less than max_lon ({max_lon.unwrap()})."
            raise InvariantViolationError(message)

    @property
    def min_lat(self) -> Latitude:
        """Minimum latitude (south)."""
        return self._value[0]

    @property
    def min_lon(self) -> Longitude:
        """Minimum longitude (west)."""
        return self._value[1]

    @property
    def max_lat(self) -> Latitude:
        """Maximum latitude (north)."""
        return self._value[2]

    @property
    def max_lon(self) -> Longitude:
        """Maximum longitude (east)."""
        return self._value[3]

    def to_float_tuple(self) -> tuple[float, float, float, float]:
        """Return bounds as (min_lat, min_lon, max_lat, max_lon) floats."""
        return (
            self.min_lat.unwrap(),
            self.min_lon.unwrap(),
            self.max_lat.unwrap(),
            self.max_lon.unwrap(),
        )

    @classmethod
    def from_float(
        cls,
        min_lat: float,
        min_lon: float,
        max_lat: float,
        max_lon: float,
    ) -> BoundingBox:
        """Create a BoundingBox from raw float values.

        Parameters
        ----------
        min_lat : float
            Minimum latitude (south).
        min_lon : float
            Minimum longitude (west).
        max_lat : float
            Maximum latitude (north).
        max_lon : float
            Maximum longitude (east).

        Returns
        -------
        BoundingBox
        """
        return cls(
            (
                Latitude(min_lat),
                Longitude(min_lon),
                Latitude(max_lat),
                Longitude(max_lon),
            )
        )


__all__ = ("BoundingBox",)
