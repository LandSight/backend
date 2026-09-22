"""City tier value object for a major settlement."""

from __future__ import annotations

from enum import StrEnum


class CityTier(StrEnum):
    """Tier of a settlement relative to the administrative hierarchy.

    The tier is a domain concept and is intentionally source-agnostic: mapping
    raw data source attributes (e.g. OpenStreetMap tags) onto it is the
    responsibility of the data source adapter.
    """

    REGIONAL_CENTER = "regional_center"
    DISTRICT_CENTER = "district_center"
    LOCAL_TOWN = "local_town"
    UNKNOWN = "unknown"


__all__ = ("CityTier",)
