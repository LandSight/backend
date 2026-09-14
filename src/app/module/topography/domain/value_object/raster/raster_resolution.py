"""Raster data resolution value object."""

from __future__ import annotations

from typing import override

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class RasterResolution(BaseValueObject[float]):
    """
    Spatial resolution in meters per pixel.

    Validates that resolution is positive and rounds to 6 decimal places.
    """

    _MIN_VALUE = 0.0

    @override
    def _normalize(self, value: float) -> float:
        return round(float(value), 6)

    @override
    def _validate(self) -> None:
        if self._value <= self._MIN_VALUE:
            message = "Resolution must be positive."
            raise ValidationError(message)


__all__ = ("RasterResolution",)
