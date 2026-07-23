"""Raster data array value object."""

from __future__ import annotations

from typing import override

import numpy as np

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class RasterDataArray(BaseValueObject[np.ndarray]):
    """2D raster data array."""

    _EXPECTED_DIMENSIONS = 2
    _MIN_DIMENSION = 1
    _MIN_PIXELS = 4

    @override
    def _normalize(self, value: np.ndarray) -> np.ndarray:
        return value

    @override
    def _validate(self) -> None:
        if self._value.ndim != self._EXPECTED_DIMENSIONS:
            message = f"Raster must be {self._EXPECTED_DIMENSIONS}D, got {self._value.ndim}D"
            raise ValidationError(message)

        h, w = self._value.shape
        if h < self._MIN_DIMENSION or w < self._MIN_DIMENSION:
            message = f"Dimensions must be >= {self._MIN_DIMENSION}, got {h}x{w}"
            raise ValidationError(message)

        if h * w < self._MIN_PIXELS:
            message = f"Raster must have at least {self._MIN_PIXELS} pixels for metric calculations, got {h * w}"
            raise ValidationError(message)

    @property
    def height(self) -> int:
        """Number of rows in the raster."""
        return self._value.shape[0]

    @property
    def width(self) -> int:
        """Number of columns in the raster."""
        return self._value.shape[1]

    @property
    def shape(self) -> tuple[int, int]:
        """Raster shape as (height, width)."""
        return self._value.shape

    @property
    def total_pixels(self) -> int:
        """Total number of pixels."""
        return self.height * self.width

    @property
    def dtype(self) -> np.dtype:
        """Data type of the array."""
        return self._value.dtype


__all__ = ("RasterDataArray",)
