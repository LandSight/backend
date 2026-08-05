"""Infrastructure object category value object."""

from __future__ import annotations

from enum import StrEnum


class Category(StrEnum):
    """Category of infrastructure objects."""

    SCHOOLS = "schools"
    HOSPITALS = "hospitals"
    SHOPS = "shops"
    TRANSIT_STOPS = "transit_stops"


__all__ = ("Category",)
