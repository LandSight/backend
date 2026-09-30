"""Coordinate helpers for converting raw geometries into domain value objects."""

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from collections.abc import Iterable

    from app.module.shared.domain.value_object import GeoPoint


def dedupe_consecutive(points: Iterable[GeoPoint]) -> list[GeoPoint]:
    """Drop consecutive duplicate points from a coordinate sequence.

    Raw geometries (OSM imports, reprojected buffers) may repeat a vertex, which
    would create a zero-length edge that the domain ``Polygon``/``LineString``
    value objects reject. Removing the repeats keeps the domain invariant while
    accepting imperfect source data.
    """
    deduped: list[GeoPoint] = []
    for point in points:
        if not deduped or deduped[-1] != point:
            deduped.append(point)
    return deduped


__all__ = ("dedupe_consecutive",)
