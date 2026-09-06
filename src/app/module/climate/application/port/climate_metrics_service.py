"""Climate metrics service port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.climate.domain.value_object.metric import (
        Percentage,
        Precipitation,
        Temperature,
    )
    from app.module.climate.domain.value_object.raster import ClimateRasterData


class ClimateMetricsService(ABC):
    """Port for computing climate metrics from WorldClim raster data.

    Each method averages the relevant variable's pixels over the parcel extent
    and applies the variable-specific unit conversion (e.g. °C x 10 to °C).

    Implementations:
    - :class:`app.module.climate.infrastructure.climate.numpy_climate_metrics_service.NumpyClimateMetricsService`
    """

    @abstractmethod
    def calculate_mean_annual_temperature(self, data: ClimateRasterData) -> Temperature:
        """Calculate the mean annual temperature (BIO1) in °C."""
        raise NotImplementedError

    @abstractmethod
    def calculate_annual_precipitation(self, data: ClimateRasterData) -> Precipitation:
        """Calculate the annual precipitation (BIO12) in mm."""
        raise NotImplementedError

    @abstractmethod
    def calculate_temperature_seasonality(self, data: ClimateRasterData) -> Temperature:
        """Calculate the temperature seasonality (BIO4) in °C."""
        raise NotImplementedError

    @abstractmethod
    def calculate_precipitation_seasonality(self, data: ClimateRasterData) -> Percentage:
        """Calculate the precipitation seasonality (BIO15) in %."""
        raise NotImplementedError

    @abstractmethod
    def calculate_max_temperature_warmest_month(self, data: ClimateRasterData) -> Temperature:
        """Calculate the max temperature of the warmest month (BIO5) in °C."""
        raise NotImplementedError

    @abstractmethod
    def calculate_min_temperature_coldest_month(self, data: ClimateRasterData) -> Temperature:
        """Calculate the min temperature of the coldest month (BIO6) in °C."""
        raise NotImplementedError

    @abstractmethod
    def calculate_precipitation_wettest_month(self, data: ClimateRasterData) -> Precipitation:
        """Calculate the precipitation of the wettest month (BIO13) in mm."""
        raise NotImplementedError

    @abstractmethod
    def calculate_precipitation_driest_month(self, data: ClimateRasterData) -> Precipitation:
        """Calculate the precipitation of the driest month (BIO14) in mm."""
        raise NotImplementedError


__all__ = ("ClimateMetricsService",)
