"""Climate metrics response DTO."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import datetime
    from uuid import UUID


@dataclass(frozen=True, slots=True)
class ClimateMetricsResponse:
    """Response DTO for climate metrics.

    Attributes
    ----------
    id : UUID
        Climate metrics identifier.
    parcel_id : UUID
        ID of the parcel these metrics belong to.
    mean_annual_temperature : float
        Mean annual temperature (BIO1) in °C.
    annual_precipitation : float
        Annual precipitation (BIO12) in mm.
    temperature_seasonality : float
        Temperature seasonality (BIO4) in °C.
    precipitation_seasonality : float
        Precipitation seasonality (BIO15), coefficient of variation in %.
    max_temperature_warmest_month : float
        Max temperature of the warmest month (BIO5) in °C.
    min_temperature_coldest_month : float
        Min temperature of the coldest month (BIO6) in °C.
    precipitation_wettest_month : float
        Precipitation of the wettest month (BIO13) in mm.
    precipitation_driest_month : float
        Precipitation of the driest month (BIO14) in mm.
    created_at : datetime | None
        When these metrics were created (UTC).
    """

    id: UUID
    parcel_id: UUID
    created_at: datetime.datetime | None
    mean_annual_temperature: float
    annual_precipitation: float
    temperature_seasonality: float
    precipitation_seasonality: float
    max_temperature_warmest_month: float
    min_temperature_coldest_month: float
    precipitation_wettest_month: float
    precipitation_driest_month: float


__all__ = ("ClimateMetricsResponse",)
