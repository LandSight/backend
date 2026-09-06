"""Bioclimatic variable enum for the WorldClim 2.1 dataset."""

from __future__ import annotations

from enum import Enum


class ClimateVariable(Enum):
    """A single bioclimatic variable used by the Climate module."""

    MEAN_ANNUAL_TEMPERATURE = "BIO1"
    TEMPERATURE_SEASONALITY = "BIO4"
    MAX_TEMPERATURE_WARMEST_MONTH = "BIO5"
    MIN_TEMPERATURE_COLDEST_MONTH = "BIO6"
    ANNUAL_PRECIPITATION = "BIO12"
    PRECIPITATION_WETTEST_MONTH = "BIO13"
    PRECIPITATION_DRIEST_MONTH = "BIO14"
    PRECIPITATION_SEASONALITY = "BIO15"


__all__ = ("ClimateVariable",)
