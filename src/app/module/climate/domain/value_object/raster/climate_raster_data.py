"""Climate raster data value object."""

from __future__ import annotations

from collections.abc import Mapping
from typing import override

import numpy as np

from app.module.climate.domain.value_object.raster.climate_variable import ClimateVariable
from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject


class ClimateRasterData(BaseValueObject[Mapping[ClimateVariable, np.ndarray]]):
    """Raster arrays for each of the 8 bioclimatic variables.

    Maps a :class:`ClimateVariable` to its 2D NumPy array sampled over the
    parcel's bounding box (NaN-filled for masked pixels).
    """

    _EXPECTED_VARIABLES = len(ClimateVariable)
    _EXPECTED_DIMENSIONS = 2
    _MIN_PIXELS = 4

    @override
    def _normalize(
        self,
        value: Mapping[ClimateVariable, np.ndarray],
    ) -> Mapping[ClimateVariable, np.ndarray]:
        return dict(value)

    @override
    def _validate(self) -> None:
        if len(self._value) != self._EXPECTED_VARIABLES:
            message = f"Expected {self._EXPECTED_VARIABLES} climate variables, got {len(self._value)}."
            raise ValidationError(message)

        expected_shape: tuple[int, int] | None = None
        for variable, array in self._value.items():
            if array.ndim != self._EXPECTED_DIMENSIONS:
                message = f"{variable.code}: raster must be 2D, got {array.ndim}D."
                raise ValidationError(message)
            if expected_shape is None:
                expected_shape = array.shape
            elif array.shape != expected_shape:
                message = (
                    f"{variable.code}: shape {array.shape} does not match the "
                    f"expected {expected_shape} shared across variables."
                )
                raise ValidationError(message)

            if expected_shape[0] * expected_shape[1] < self._MIN_PIXELS:
                message = (
                    f"{variable.code}: raster must have at least {self._MIN_PIXELS} "
                    f"pixels, got {expected_shape[0] * expected_shape[1]}."
                )
                raise ValidationError(message)

    def get(self, variable: ClimateVariable) -> np.ndarray:
        """Return the raster array for the given variable."""
        return self._value[variable]

    @property
    def variables(self) -> Mapping[ClimateVariable, np.ndarray]:
        """All variable arrays keyed by :class:`ClimateVariable`."""
        return self._value


__all__ = ("ClimateRasterData",)
