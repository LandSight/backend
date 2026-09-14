"""Local DEM repository port."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.module.shared.domain.value_object import BoundingBox
    from app.module.topography.domain.value_object.raster import RasterData


class LocalDemRepository(ABC):
    """Port for accessing locally cached DEM raster data.

    Provides access to previously downloaded and cached DEM tiles
    stored in the local file system or database.

    Implementations:
    - :class:`app.module.topography.infrastructure.dem.local_dem_repository.LocalDemRepository`
    """

    @abstractmethod
    async def get_elevation_raster(self, bounds: BoundingBox) -> RasterData | None:
        """Retrieve locally cached DEM raster for the given bounding box.

        Parameters
        ----------
        bounds : BoundingBox
            Bounding box for the area of interest.

        Returns
        -------
        RasterData | None
            Raster data with elevation array and resolution, or ``None`` if not cached.
        """
        raise NotImplementedError

    @abstractmethod
    async def save_elevation_raster(
        self,
        bounds: BoundingBox,
        raster: RasterData,
    ) -> None:
        """Cache a DEM raster locally.

        Parameters
        ----------
        bounds : BoundingBox
            Bounding box for the area of interest.
        raster : RasterData
            Raster data containing elevation array and resolution.
        """
        raise NotImplementedError

    @abstractmethod
    async def exists(self, bounds: BoundingBox) -> bool:
        """Check if a DEM raster exists in the cache.

        Parameters
        ----------
        bounds : BoundingBox
            Bounding box for the area of interest.

        Returns
        -------
        bool
            True if cached, False otherwise.
        """
        raise NotImplementedError


__all__ = ("LocalDemRepository",)
