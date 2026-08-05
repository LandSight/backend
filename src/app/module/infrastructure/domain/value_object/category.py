"""Infrastructure object category value object."""

from __future__ import annotations

from enum import StrEnum


class Category(StrEnum):
    """Category of infrastructure objects."""

    SCHOOL = "school"
    HOSPITAL = "hospital"
    SHOP = "shop"
    TRANSIT_STOP = "transit_stop"
    WATER_BODY = "water_body"


__all__ = ("Category",)
