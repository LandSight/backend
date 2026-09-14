"""Local climate repository port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.climate.domain.value_object.raster import ClimateRasterData
    from app.module.shared.domain.value_object import BoundingBox


class LocalClimateRepository(ABC):
    """Port for accessing locally stored WorldClim 2.1 COG rasters.

    Provides access to the 8 bioclimatic COGs pre-loaded into S3-compatible
    object storage. Each variable is read as a sub-region (windowed read) for
    a requested bounding box.

    Implementations:
    - :class:`app.module.climate.infrastructure.repository.s3_local_climate_repository.S3LocalClimateRepository`
    """

    @abstractmethod
    async def exists(self, bounds: BoundingBox) -> bool:
        """Check whether climate data is available for the requested bounds.

        Parameters
        ----------
        bounds : BoundingBox
            Bounding box for the area of interest.

        Returns
        -------
        bool
            True if all 8 COGs are present and fully cover the bounds.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_climate_data(self, bounds: BoundingBox) -> ClimateRasterData | None:
        """Retrieve raster arrays for all 8 climate variables for the bounds.

        Parameters
        ----------
        bounds : BoundingBox
            Bounding box for the area of interest.

        Returns
        -------
        ClimateRasterData | None
            Raster arrays keyed by variable, or ``None`` if not fully covered.
        """
        raise NotImplementedError


__all__ = ("LocalClimateRepository",)
