"""NumPy-based climate metrics service implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

import numpy as np

from app.module.climate.application.port import ClimateMetricsService
from app.module.climate.domain.value_object.metric import Percentage, Precipitation, Temperature
from app.module.climate.domain.value_object.raster.climate_variable import ClimateVariable
from app.module.climate.infrastructure.climate_variable_spec import CLIMATE_VARIABLE_SPECS


if TYPE_CHECKING:
    from app.module.climate.domain.value_object.raster import ClimateRasterData


class NumpyClimateMetricsService(ClimateMetricsService):
    """NumPy-based implementation of the climate metrics service.

    Averages each variable's pixels over the parcel extent and applies the
    variable-specific unit conversion (WorldClim stores temperature-derived
    variables scaled by 10 or 100).
    """

    @override
    def calculate_mean_annual_temperature(self, data: ClimateRasterData) -> Temperature:
        """See :class:`app.module.climate.application.port.ClimateMetricsService.calculate_mean_annual_temperature`."""
        return Temperature(self._mean(data, ClimateVariable.MEAN_ANNUAL_TEMPERATURE))

    @override
    def calculate_annual_precipitation(self, data: ClimateRasterData) -> Precipitation:
        """See :class:`app.module.climate.application.port.ClimateMetricsService.calculate_annual_precipitation`."""
        return Precipitation(self._mean(data, ClimateVariable.ANNUAL_PRECIPITATION))

    @override
    def calculate_temperature_seasonality(self, data: ClimateRasterData) -> Temperature:
        """See :class:`app.module.climate.application.port.ClimateMetricsService.calculate_temperature_seasonality`."""
        return Temperature(self._mean(data, ClimateVariable.TEMPERATURE_SEASONALITY))

    @override
    def calculate_precipitation_seasonality(self, data: ClimateRasterData) -> Percentage:
        """See :class:`app.module.climate.application.port.ClimateMetricsService.calculate_precipitation_seasonality`."""
        return Percentage(self._mean(data, ClimateVariable.PRECIPITATION_SEASONALITY))

    @override
    def calculate_max_temperature_warmest_month(self, data: ClimateRasterData) -> Temperature:
        """See :class:`app.module.climate.application.port.ClimateMetricsService.calculate_max_temperature_warmest_month`."""
        return Temperature(self._mean(data, ClimateVariable.MAX_TEMPERATURE_WARMEST_MONTH))

    @override
    def calculate_min_temperature_coldest_month(self, data: ClimateRasterData) -> Temperature:
        """See :class:`app.module.climate.application.port.ClimateMetricsService.calculate_min_temperature_coldest_month`."""
        return Temperature(self._mean(data, ClimateVariable.MIN_TEMPERATURE_COLDEST_MONTH))

    @override
    def calculate_precipitation_wettest_month(self, data: ClimateRasterData) -> Precipitation:
        """See :class:`app.module.climate.application.port.ClimateMetricsService.calculate_precipitation_wettest_month`."""
        return Precipitation(self._mean(data, ClimateVariable.PRECIPITATION_WETTEST_MONTH))

    @override
    def calculate_precipitation_driest_month(self, data: ClimateRasterData) -> Precipitation:
        """See :class:`app.module.climate.application.port.ClimateMetricsService.calculate_precipitation_driest_month`."""
        return Precipitation(self._mean(data, ClimateVariable.PRECIPITATION_DRIEST_MONTH))

    @staticmethod
    def _mean(data: ClimateRasterData, variable: ClimateVariable) -> float:
        """Compute the mean of a variable's pixels, applying its unit scale.

        Parameters
        ----------
        data : ClimateRasterData
            Raster arrays for all climate variables.
        variable : ClimateVariable
            The variable to average.

        Returns
        -------
        float
            Mean value converted to the variable's physical unit.
        """
        array = data.get(variable)
        scale = CLIMATE_VARIABLE_SPECS[variable].scale
        raw_mean = float(np.nanmean(array._value))
        return round(raw_mean / scale, 2)


__all__ = ("NumpyClimateMetricsService",)
