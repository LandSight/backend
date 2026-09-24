"""Spatial reference system identifiers used across the application."""

from __future__ import annotations

from enum import IntEnum


class Srid(IntEnum):
    """Spatial reference system identifiers (EPSG codes).

    The value is the numeric EPSG code usable directly in PostGIS/GeoAlchemy
    calls, while :meth:`to_epsg` returns the ``EPSG:<code>`` string expected by
    ``pyproj`` and similar libraries.
    """

    WGS84 = 4326
    WEB_MERCATOR = 3857

    def to_epsg(self) -> str:
        """Return the reference system as an ``EPSG:<code>`` string."""
        return f"EPSG:{self.value}"


__all__ = ("Srid",)
