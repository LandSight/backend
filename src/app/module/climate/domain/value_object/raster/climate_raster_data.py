"""Climate raster data value object."""

from __future__ import annotations

from collections.abc import Mapping
from typing import override

from app.module.climate.domain.value_object.raster.climate_variable import ClimateVariable
from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseValueObject, RasterDataArray


class ClimateRasterData(BaseValueObject[Mapping[ClimateVariable, RasterDataArray]]):
    """Raster arrays for each of the 8 bioclimatic variables.

    Maps a :class:`ClimateVariable` to its :class:`RasterDataArray` sampled over
    the parcel's bounding box (NaN-filled for masked pixels). Reuses the shared
    raster array value object for 2D/shape validation.
    """

    _EXPECTED_VARIABLES = len(ClimateVariable)

    @override
    def _normalize(
        self,
        value: Mapping[ClimateVariable, RasterDataArray],
    ) -> Mapping[ClimateVariable, RasterDataArray]:
        return dict(value)

    @override
    def _validate(self) -> None:
        if len(self._value) != self._EXPECTED_VARIABLES:
            message = f"Expected {self._EXPECTED_VARIABLES} climate variables, got {len(self._value)}."
            raise ValidationError(message)

        expected_shape: tuple[int, int] | None = None
        for variable, array in self._value.items():
            if expected_shape is None:
                expected_shape = array.shape
            elif array.shape != expected_shape:
                message = (
                    f"{variable.value}: shape {array.shape} does not match the "
                    f"expected {expected_shape} shared across variables."
                )
                raise ValidationError(message)

    def get(self, variable: ClimateVariable) -> RasterDataArray:
        """Return the raster array for the given variable."""
        return self._value[variable]

    @property
    def variables(self) -> Mapping[ClimateVariable, RasterDataArray]:
        """All variable arrays keyed by :class:`ClimateVariable`."""
        return self._value


__all__ = ("ClimateRasterData",)
