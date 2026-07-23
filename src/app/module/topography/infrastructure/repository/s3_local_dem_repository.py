"""S3-backed local DEM repository implementation.

Stores and retrieves DEM rasters as Cloud Optimized GeoTIFFs (COGs)
in an S3-compatible object store (MinIO, AWS S3, etc.).
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, override

import rasterio

from app.module.topography.application.port.local_dem_repository import LocalDemRepository
from app.module.topography.domain.value_object.raster import RasterData
from app.module.topography.domain.value_object.raster.raster_data_array import RasterDataArray
from app.module.topography.domain.value_object.raster.raster_resolution import RasterResolution
from app.platform.logging import get_logger
from app.platform.storage.repository import S3GeoRepository


if TYPE_CHECKING:
    from botocore.client import BaseClient
    from rasterio.session import AWSSession

    from app.module.shared.domain.value_object import BoundingBox
    from app.platform.config.models import S3Config


logger = get_logger("app.topography.infrastructure.repository.s3_local_dem_repository")


class S3LocalDemRepository(S3GeoRepository, LocalDemRepository):
    """Local DEM repository backed by S3-compatible geo-object storage.

    Stores DEM rasters as Cloud Optimized GeoTIFFs (COGs) keyed by
    a tile identifier derived from the bounding box coordinates.

    Inherits from :class:`S3GeoRepository` and
    from :class:`LocalDemRepository` for the domain port.
    """

    _TILE_PRECISION: int = 2

    def __init__(self, aws_session: AWSSession, s3_client: BaseClient, s3_config: S3Config) -> None:
        S3GeoRepository.__init__(self, aws_session, s3_client, s3_config)
        self._logger = logger

    def _get_s3_uri(self, key: str) -> str:
        """Build S3 URI from bucket and key."""
        return f"s3://{self._bucket}/{key}"

    @override
    async def get_elevation_raster(self, bounds: BoundingBox) -> RasterData | None:
        """Retrieve a DEM raster from S3 for the given bounding box.

        Uses rasterio to read the Cloud Optimized GeoTIFF directly from S3.

        Parameters
        ----------
        bounds : BoundingBox
            Bounding box for the area of interest.

        Returns
        -------
        RasterData | None
            Raster data with elevation array and resolution, or ``None`` if not cached.
        """
        key = self._build_key(bounds)
        s3_uri = self._get_s3_uri(key)

        self._logger.debug("Checking S3 for DEM raster: %s", s3_uri)

        try:
            with rasterio.Env(session=self._aws_session), rasterio.open(s3_uri) as src:
                # Read with masking to handle nodata
                data = src.read(1, masked=True)

                # Calculate resolution in meters from transform
                resolution = self._calculate_resolution_in_meters(
                    transform=src.transform,
                    bounds=bounds,
                )

                self._logger.debug(
                    "DEM raster found in S3: %s (shape=%s, resolution=%sm)",
                    s3_uri,
                    data.shape,
                    resolution,
                )

                # Create RasterData VO
                return RasterData((RasterDataArray(data), RasterResolution(resolution)))

        except rasterio.errors.RasterioIOError:
            self._logger.debug("DEM raster not found in S3: %s", s3_uri)
            return None

    @override
    async def save_elevation_raster(
        self,
        bounds: BoundingBox,
        raster: RasterData,
    ) -> None:
        """Save a DEM raster to S3 as a Cloud Optimized GeoTIFF.

        Uses rasterio to write the COG directly to S3.

        Parameters
        ----------
        bounds : BoundingBox
            Bounding box for the area of interest.
        raster : RasterData
            Raster data containing elevation array and resolution.
        """
        key = self._build_key(bounds)
        s3_uri = self._get_s3_uri(key)

        # Извлекаем данные из RasterData
        elevation = raster.array._value
        resolution = raster.resolution._value

        self._logger.info(
            "Saving DEM raster to S3: %s (shape=%s, resolution=%sm)",
            s3_uri,
            elevation.shape,
            resolution,
        )

        # Compute geotransform from bounds and array shape
        min_lon, max_lon = bounds.min_lon.unwrap(), bounds.max_lon.unwrap()
        min_lat, max_lat = bounds.min_lat.unwrap(), bounds.max_lat.unwrap()

        height, width = elevation.shape
        res_x = resolution if resolution else (max_lon - min_lon) / width
        res_y = resolution if resolution else (max_lat - min_lat) / height

        transform = rasterio.Affine(res_x, 0.0, min_lon, 0.0, -res_y, max_lat)

        profile = {
            "driver": "COG",
            "height": height,
            "width": width,
            "count": 1,
            "dtype": elevation.dtype,
            "crs": "EPSG:4326",
            "transform": transform,
            "compress": "DEFLATE",
            "blockxsize": 256,
            "blockysize": 256,
            "tiled": True,
            "interleave": "pixel",
            "nodata": -9999,
        }

        with rasterio.Env(session=self._aws_session), rasterio.open(s3_uri, "w", **profile) as dst:
            dst.write(elevation, 1)

        self._logger.info("DEM raster saved to S3: %s", s3_uri)

    @override
    async def exists(self, bounds: BoundingBox) -> bool:
        """Check if a DEM raster exists in S3.

        Parameters
        ----------
        bounds : BoundingBox
            Bounding box for the area of interest.

        Returns
        -------
        bool
            True if cached, False otherwise.
        """
        key = self._build_key(bounds)
        try:
            self._s3_client.head_object(Bucket=self._bucket, Key=key)
        except self._s3_client.exceptions.ClientError:
            return False
        else:
            return True

    def _build_key(self, bounds: BoundingBox) -> str:
        """Build an S3 object key from bounding box coordinates.

        Uses a tile-grid approach: rounds coordinates to ``_TILE_PRECISION``
        decimal places so that overlapping or nearby queries map to the same key.

        Parameters
        ----------
        bounds : BoundingBox
            Bounding box for the area of interest.

        Returns
        -------
        str
            S3 object key (e.g., ``dem/59.90_30.20_60.10_30.50.tif``).
        """
        min_lat = round(bounds.min_lat.unwrap(), self._TILE_PRECISION)
        min_lon = round(bounds.min_lon.unwrap(), self._TILE_PRECISION)
        max_lat = round(bounds.max_lat.unwrap(), self._TILE_PRECISION)
        max_lon = round(bounds.max_lon.unwrap(), self._TILE_PRECISION)
        return f"dem/{min_lat}_{min_lon}_{max_lat}_{max_lon}.tif"

    def _calculate_resolution_in_meters(
        self,
        transform: rasterio.Affine,
        bounds: BoundingBox,
    ) -> float:
        """Calculate spatial resolution in meters from geotransform.

        Parameters
        ----------
        transform : rasterio.Affine
            Affine transform from the raster dataset containing pixel
            resolution in degrees.
        bounds : BoundingBox
            Bounding box for the area of interest.

        Returns
        -------
        float
            Spatial resolution in meters per pixel.
        """
        # Resolution in degrees
        res_x_deg = abs(transform.a)
        res_y_deg = abs(transform.e)
        avg_res_deg = (res_x_deg + res_y_deg) / 2

        # Central latitude for conversion
        center_lat = (bounds.min_lat.unwrap() + bounds.max_lat.unwrap()) / 2
        lat_rad = math.radians(center_lat)

        # Convert degrees to meters
        meters_per_degree: float = 111320.0
        resolution_meters = avg_res_deg * meters_per_degree * math.cos(lat_rad)

        return resolution_meters


__all__ = ("S3LocalDemRepository",)
