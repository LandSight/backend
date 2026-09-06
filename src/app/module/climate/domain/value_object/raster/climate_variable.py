"""Bioclimatic variable enum for the WorldClim 2.1 dataset."""

from __future__ import annotations

from enum import Enum


class ClimateVariable(Enum):
    """A single WorldClim 2.1 bioclimatic variable.

    Encapsulates the S3 object key, the unit conversion factor applied to raw
    stored values, and the unit label.

    WorldClim stores temperature-derived variables scaled by a factor of 10 or
    100 (e.g. ``degC x 10``). The ``scale`` attribute is the divisor applied
    when converting a raw pixel value to its physical unit.
    """

    MEAN_ANNUAL_TEMPERATURE = ("bio_1.tif", "BIO1", 10, "°C")
    TEMPERATURE_SEASONALITY = ("bio_4.tif", "BIO4", 100, "°C")
    MAX_TEMPERATURE_WARMEST_MONTH = ("bio_5.tif", "BIO5", 10, "°C")
    MIN_TEMPERATURE_COLDEST_MONTH = ("bio_6.tif", "BIO6", 10, "°C")
    ANNUAL_PRECIPITATION = ("bio_12.tif", "BIO12", 1, "mm")
    PRECIPITATION_WETTEST_MONTH = ("bio_13.tif", "BIO13", 1, "mm")
    PRECIPITATION_DRIEST_MONTH = ("bio_14.tif", "BIO14", 1, "mm")
    PRECIPITATION_SEASONALITY = ("bio_15.tif", "BIO15", 1, "%")

    def __init__(self, object_key: str, code: str, scale: int, unit: str) -> None:
        self._object_key = object_key
        self._code = code
        self._scale = scale
        self._unit = unit

    @property
    def object_key(self) -> str:
        """S3 object key of the COG file for this variable."""
        return self._object_key

    @property
    def code(self) -> str:
        """WorldClim variable code (e.g. ``BIO1``)."""
        return self._code

    @property
    def scale(self) -> int:
        """Divisor applied to convert raw stored values to physical units."""
        return self._scale

    @property
    def unit(self) -> str:
        """Physical unit of the converted value."""
        return self._unit


__all__ = ("ClimateVariable",)
