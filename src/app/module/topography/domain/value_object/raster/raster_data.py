"""Raster data value object."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.value_object import BaseValueObject

from .raster_data_array import RasterDataArray
from .raster_resolution import RasterResolution


class RasterData(BaseValueObject[tuple[RasterDataArray, RasterResolution]]):
    """
    Raster data with its spatial resolution.

    Composes two Value Objects: RasterDataArray and Resolution.
    """

    @override
    def _normalize(self, value: tuple[RasterDataArray, RasterResolution]) -> tuple[RasterDataArray, RasterResolution]:
        return value

    @property
    def array(self) -> RasterDataArray:
        """Raster data array."""
        return self._value[0]

    @property
    def resolution(self) -> RasterResolution:
        """Spatial resolution."""
        return self._value[1]


__all__ = ("RasterData",)
