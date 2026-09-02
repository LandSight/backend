"""S3-backed local DEM repository implementation.

Stores a single Cloud Optimized GeoTIFF (COG) covering a whole region in
an S3-compatible object store (MinIO, AWS S3, etc.) and reads only the
required sub-region (``windowed read``) for a requested bounding box.

If the requested bounding box is not fully covered by the stored COG,
``get_elevation_raster`` returns ``None`` so callers can report that no
data is available for the requested area.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, override

import numpy as np
import rasterio
import rasterio.windows

from app.module.shared.domain.value_object import BoundingBox
from app.module.topography.application.port.local_dem_repository import LocalDemRepository
from app.module.topography.domain.value_object.raster import RasterData
from app.module.topography.domain.value_object.raster.raster_data_array import RasterDataArray
from app.module.topography.domain.value_object.raster.raster_resolution import RasterResolution
from app.platform.logging import get_logger
from app.platform.storage.repository import S3GeoRepository


if TYPE_CHECKING:
    from botocore.client import BaseClient as BotoClient
    from rasterio.session import AWSSession

    from app.platform.config.models import S3Config


logger = get_logger("app.topography.infrastructure.repository.s3_local_dem_repository")


class S3LocalDemRepository(S3GeoRepository, LocalDemRepository):
    """Local DEM repository backed by S3-compatible geo-object storage.

    Reads a single pre-loaded Cloud Optimized GeoTIFF (COG) stored under a
    fixed object key. For a requested bounding box it:

    1. opens the COG and obtains its full coverage extent;
    2. checks that the requested bounds are fully inside the coverage;
    3. performs a ``windowed read`` to load only the required sub-region.

    Inherits from :class:`S3GeoRepository` and from
    :class:`LocalDemRepository` for the domain port.
    """

    #: S3 object key of the single DEM COG covering the whole region.
    _DEM_KEY: str = "leningrad_oblast_dem_cog.tif"

    def __init__(self, aws_session: AWSSession, s3_client: BotoClient, s3_config: S3Config) -> None:
        S3GeoRepository.__init__(self, aws_session, s3_client, s3_config)
        self._logger = logger

    def _get_s3_uri(self, key: str) -> str:
        """Build S3 URI from bucket and key."""
        return f"s3://{self._s3_config.dem_bucket}/{key}"

    def _rasterio_env_options(self) -> dict[str, object]:
        """Build ``rasterio.Env`` kwargs targeting the configured S3 endpoint.

        For S3-compatible stores such as MinIO, GDAL must be told which endpoint
        to use (``AWS_S3_ENDPOINT``) and which signature version to apply.
        """
        options: dict[str, object] = {
            "session": self._aws_session,
            "AWS_S3_SIGNATURE_VERSION": "s3v4",
            # MinIO is an S3-compatible store that expects path-style addressing,
            # so disable GDAL's default virtual-hosted style.
            "AWS_VIRTUAL_HOSTING": "FALSE",
        }
        if self._s3_config.endpoint:
            options["AWS_S3_ENDPOINT"] = self._s3_config.endpoint
            options["AWS_S3_USE_HTTPS"] = "YES" if self._s3_config.secure else "NO"
        return options

    @override
    async def get_elevation_raster(self, bounds: BoundingBox) -> RasterData | None:
        """Retrieve a DEM sub-region from the S3 COG for the given bounding box.

        Parameters
        ----------
        bounds : BoundingBox
            Bounding box for the area of interest.

        Returns
        -------
        RasterData | None
            Raster data with elevation array and resolution, or ``None`` if the
            requested bounds are not fully covered by the stored COG.
        """
        s3_uri = self._get_s3_uri(self._DEM_KEY)

        try:
            with rasterio.Env(**self._rasterio_env_options()), rasterio.open(s3_uri) as src:
                if self._is_out_of_coverage(src, bounds):
                    return None

                elevation = self._read_window(src, bounds)
                resolution = self._calculate_resolution_in_meters(transform=src.transform, bounds=bounds)

                return RasterData((RasterDataArray(elevation), RasterResolution(resolution)))

        except rasterio.errors.RasterioIOError as exc:
            self._logger.warning("DEM COG could not be opened from S3: %s (%s)", s3_uri, exc, exc_info=True)
            return None

    @override
    async def save_elevation_raster(
        self,
        bounds: BoundingBox,
        raster: RasterData,
    ) -> None:
        """Save a DEM raster to S3 as a Cloud Optimized GeoTIFF.

        Note
        ----
        Writes under the fixed COG object key. This overwrites the whole-region
        COG and is intended for initializing the store rather than per-query caching.

        Parameters
        ----------
        bounds : BoundingBox
            Bounding box for the area of interest.
        raster : RasterData
            Raster data containing elevation array and resolution.
        """
        s3_uri = self._get_s3_uri(self._DEM_KEY)

        elevation = raster.array._value
        resolution = raster.resolution._value

        self._logger.info(
            "Saving DEM raster to S3: %s (shape=%s, resolution=%sm)",
            s3_uri,
            elevation.shape,
            resolution,
        )

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

        with rasterio.Env(**self._rasterio_env_options()), rasterio.open(s3_uri, "w", **profile) as dst:
            dst.write(elevation, 1)

        self._logger.info("DEM raster saved to S3: %s", s3_uri)

    @override
    async def exists(self, bounds: BoundingBox) -> bool:
        """Check whether DEM data is available for the requested bounds.

        Returns ``True`` only when the single COG object is present in S3 AND the
        requested bounds are fully inside its coverage. When data is unavailable,
        logs the specific reason (missing object vs. out-of-coverage) so the cause
        is visible in the application logs.

        Parameters
        ----------
        bounds : BoundingBox
            Bounding box for the area of interest.

        Returns
        -------
        bool
            True if DEM data is available for the requested bounds, False otherwise.
        """
        s3_uri = self._get_s3_uri(self._DEM_KEY)

        # 1) The COG object must exist in the bucket.
        try:
            self._s3_client.head_object(Bucket=self._s3_config.dem_bucket, Key=self._DEM_KEY)
        except self._s3_client.exceptions.ClientError:
            self._logger.warning("DEM COG not found in S3: %s", s3_uri)
            return False

        # 2) The requested bounds must be fully inside the COG coverage.
        try:
            with rasterio.Env(**self._rasterio_env_options()), rasterio.open(s3_uri) as src:
                coverage = self._coverage_bounds(src)
        except rasterio.errors.RasterioIOError as exc:
            self._logger.warning("DEM COG could not be opened from S3: %s (%s)", s3_uri, exc, exc_info=True)
            return False

        if not self._covers(coverage, bounds):
            self._logger.warning(
                "Requested bounds %s are outside DEM coverage %s",
                bounds,
                coverage,
            )
            return False

        return True

    @staticmethod
    def _coverage_bounds(src: rasterio.io.DatasetReader) -> BoundingBox:
        """Return the full coverage extent of a raster dataset as a bounding box.

        Parameters
        ----------
        src : rasterio.io.DatasetReader
            Open raster dataset.

        Returns
        -------
        BoundingBox
            Coverage in ``(min_lat, min_lon, max_lat, max_lon)`` order.
        """
        return BoundingBox.from_float(
            min_lat=src.bounds.bottom,
            min_lon=src.bounds.left,
            max_lat=src.bounds.top,
            max_lon=src.bounds.right,
        )

    @staticmethod
    def _covers(coverage: BoundingBox, requested: BoundingBox) -> bool:
        """Check that ``requested`` bounds are fully inside ``coverage``.

        Parameters
        ----------
        coverage : BoundingBox
            Extent covered by the DEM.
        requested : BoundingBox
            Area of interest.

        Returns
        -------
        bool
            True if the requested bounds are fully contained in the coverage.
        """
        return (
            requested.min_lon.unwrap() >= coverage.min_lon.unwrap()
            and requested.min_lat.unwrap() >= coverage.min_lat.unwrap()
            and requested.max_lon.unwrap() <= coverage.max_lon.unwrap()
            and requested.max_lat.unwrap() <= coverage.max_lat.unwrap()
        )

    def _is_out_of_coverage(self, src: rasterio.io.DatasetReader, bounds: BoundingBox) -> bool:
        """Return True if the requested bounds are outside the DEM coverage."""
        coverage = self._coverage_bounds(src)
        if self._covers(coverage, bounds):
            return False
        self._logger.debug("Requested bounds %s are outside DEM coverage %s", bounds, coverage)
        return True

    @staticmethod
    def _read_window(src: rasterio.io.DatasetReader, bounds: BoundingBox) -> np.ndarray:
        """Read the requested sub-region from the COG as a NaN-filled array."""
        window = rasterio.windows.from_bounds(
            left=bounds.min_lon.unwrap(),
            bottom=bounds.min_lat.unwrap(),
            right=bounds.max_lon.unwrap(),
            top=bounds.max_lat.unwrap(),
            transform=src.transform,
        )
        data = src.read(1, window=window, masked=True)
        return data.filled(np.nan)

    @staticmethod
    def _calculate_resolution_in_meters(
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
