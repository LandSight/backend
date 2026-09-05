"""Local UTM projection helpers for metric geometry operations.

Reprojects lon/lat (EPSG:4326) Shapely geometries into a local Universal
Transverse Mercator (UTM) zone so buffers, distances and areas are computed in
physical meters. The UTM zone is chosen automatically from a geometry's
centroid, keeping calculations correct across a wide range of longitudes and
delegating all coordinate math to ``pyproj``.
"""

from __future__ import annotations

from pyproj import Transformer
from shapely.geometry import Point as ShapelyPoint, Polygon as ShapelyPolygon
from shapely.ops import transform


WGS84_EPSG = "EPSG:4326"

# UTM zone width in degrees.
_UTM_ZONE_WIDTH = 6.0
# Longitude offset used to compute the UTM zone number.
_UTM_LON_OFFSET = 180.0
# EPSG code bases for northern/southern hemisphere UTM zones.
_UTM_NORTH_EPSG_BASE = 32600
_UTM_SOUTH_EPSG_BASE = 32700

# Supported geometry types (runtime accepts any Shapely geometry).
ShapelyGeometry = ShapelyPoint | ShapelyPolygon


def utm_epsg(lon: float, lat: float) -> int:
    """Return the UTM zone EPSG code covering the given longitude/latitude.

    Parameters
    ----------
    lon : float
        Longitude in degrees.
    lat : float
        Latitude in degrees.

    Returns
    -------
    int
        EPSG code of the UTM zone covering the coordinates.
    """
    zone = int((lon + _UTM_LON_OFFSET) / _UTM_ZONE_WIDTH) + 1
    base = _UTM_NORTH_EPSG_BASE if lat >= 0 else _UTM_SOUTH_EPSG_BASE
    return base + zone


def reproject_to(geometry: ShapelyGeometry, epsg: int) -> ShapelyGeometry:
    """Reproject a lon/lat geometry into the given UTM zone (meters)."""
    transformer = Transformer.from_crs(WGS84_EPSG, f"EPSG:{epsg}", always_xy=True)
    return transform(transformer.transform, geometry)


def to_local_utm(geometry: ShapelyGeometry) -> tuple[ShapelyGeometry, int]:
    """Reproject a lon/lat geometry into a local UTM zone from its centroid.

    Returns a ``(projected_geometry, epsg)`` pair so callers can reuse the same
    zone (``epsg``) for related geometries via :func:`reproject_to`.
    """
    epsg = utm_epsg(geometry.centroid.x, geometry.centroid.y)
    return reproject_to(geometry, epsg), epsg


def to_wgs84(geometry: ShapelyGeometry, epsg: int) -> ShapelyGeometry:
    """Reproject a UTM-meter geometry back to lon/lat (EPSG:4326)."""
    transformer = Transformer.from_crs(f"EPSG:{epsg}", WGS84_EPSG, always_xy=True)
    return transform(transformer.transform, geometry)


__all__ = ("reproject_to", "to_local_utm", "to_wgs84", "utm_epsg")
