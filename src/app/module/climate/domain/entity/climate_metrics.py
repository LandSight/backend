"""Climate metrics entity."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from app.module.climate.domain.value_object.metric import (
    ClimateMetricsId,
    ParcelId,
    Percentage,
    Precipitation,
    Temperature,
)
from app.module.shared.domain.entity import BaseEntity


if TYPE_CHECKING:
    import datetime


class ClimateMetrics(BaseEntity[ClimateMetricsId]):
    """Climate metrics entity for a parcel.

    Stores the 8 bioclimatic metrics computed from WorldClim 2.1 data.
    Temperature values are returned in °C (converted from the raw °C x 10 /
    °C x 100 stored values).

    Attributes
    ----------
    id : ClimateMetricsId
        Unique identifier for this metrics record.
    parcel_id : ParcelId
        ID of the parcel these metrics belong to.
    mean_annual_temperature : Temperature
        Mean annual temperature (BIO1) in °C.
    annual_precipitation : Precipitation
        Annual precipitation (BIO12) in mm.
    temperature_seasonality : Temperature
        Temperature seasonality (BIO4) in °C (std dev of monthly means).
    precipitation_seasonality : Percentage
        Precipitation seasonality (BIO15), coefficient of variation in %.
    max_temperature_warmest_month : Temperature
        Max temperature of the warmest month (BIO5) in °C.
    min_temperature_coldest_month : Temperature
        Min temperature of the coldest month (BIO6) in °C.
    precipitation_wettest_month : Precipitation
        Precipitation of the wettest month (BIO13) in mm.
    precipitation_driest_month : Precipitation
        Precipitation of the driest month (BIO14) in mm.
    created_at : datetime | None
        When these metrics were created (UTC); ``None`` if not yet persisted.
    """

    def __init__(  # noqa: PLR0913
        self,
        id: ClimateMetricsId,
        parcel_id: ParcelId,
        mean_annual_temperature: Temperature,
        annual_precipitation: Precipitation,
        temperature_seasonality: Temperature,
        precipitation_seasonality: Percentage,
        max_temperature_warmest_month: Temperature,
        min_temperature_coldest_month: Temperature,
        precipitation_wettest_month: Precipitation,
        precipitation_driest_month: Precipitation,
        created_at: datetime.datetime | None = None,
    ) -> None:
        self._parcel_id: ParcelId = parcel_id
        self._mean_annual_temperature: Temperature = mean_annual_temperature
        self._annual_precipitation: Precipitation = annual_precipitation
        self._temperature_seasonality: Temperature = temperature_seasonality
        self._precipitation_seasonality: Percentage = precipitation_seasonality
        self._max_temperature_warmest_month: Temperature = max_temperature_warmest_month
        self._min_temperature_coldest_month: Temperature = min_temperature_coldest_month
        self._precipitation_wettest_month: Precipitation = precipitation_wettest_month
        self._precipitation_driest_month: Precipitation = precipitation_driest_month
        self._created_at: datetime.datetime | None = created_at

        super().__init__(id)

    @override
    def _validate(self) -> None:
        return None

    @property
    def parcel_id(self) -> ParcelId:
        """ID of the parcel these metrics belong to."""
        return self._parcel_id

    @property
    def mean_annual_temperature(self) -> Temperature:
        """Mean annual temperature (BIO1) in °C."""
        return self._mean_annual_temperature

    @property
    def annual_precipitation(self) -> Precipitation:
        """Annual precipitation (BIO12) in mm."""
        return self._annual_precipitation

    @property
    def temperature_seasonality(self) -> Temperature:
        """Temperature seasonality (BIO4) in °C."""
        return self._temperature_seasonality

    @property
    def precipitation_seasonality(self) -> Percentage:
        """Precipitation seasonality (BIO15) in %."""
        return self._precipitation_seasonality

    @property
    def max_temperature_warmest_month(self) -> Temperature:
        """Max temperature of the warmest month (BIO5) in °C."""
        return self._max_temperature_warmest_month

    @property
    def min_temperature_coldest_month(self) -> Temperature:
        """Min temperature of the coldest month (BIO6) in °C."""
        return self._min_temperature_coldest_month

    @property
    def precipitation_wettest_month(self) -> Precipitation:
        """Precipitation of the wettest month (BIO13) in mm."""
        return self._precipitation_wettest_month

    @property
    def precipitation_driest_month(self) -> Precipitation:
        """Precipitation of the driest month (BIO14) in mm."""
        return self._precipitation_driest_month

    @property
    def created_at(self) -> datetime.datetime | None:
        """When these metrics were created (UTC)."""
        return self._created_at


__all__ = ("ClimateMetrics",)
