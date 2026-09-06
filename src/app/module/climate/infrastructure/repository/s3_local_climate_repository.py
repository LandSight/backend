"""S3-backed local climate repository implementation.

Reads the 8 Cloud Optimized GeoTIFF (COG) bioclimatic variables (WorldClim
2.1) from an S3-compatible object store (MinIO, AWS S3, etc.) and performs a
``windowed read`` of the required sub-region for a requested bounding box.

Each variable is stored under its own object key (see
:class:`~app.module.climate.domain.value_object.raster.ClimateVariable`).
If the requested bounding box is not fully covered by the stored COGs,
``get_climate_data`` returns ``None`` so callers can report that no data is
available for the requested area.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, override

import numpy as np
import rasterio
import rasterio.windows

from app.module.climate.application.port import LocalClimateRepository
from app.module.climate.domain.value_object.raster import ClimateRasterData, ClimateVariable
from app.module.climate.infrastructure.climate_variable_spec import CLIMATE_VARIABLE_SPECS
from app.module.shared.domain.value_object import BoundingBox, RasterDataArray
from app.platform.logging import get_logger
from app.platform.storage.repository import S3GeoRepository


if TYPE_CHECKING:
    from botocore.client import BaseClient as BotoClient
    from rasterio.session import AWSSession

    from app.platform.config.models import S3Config


logger = get_logger("app.climate.infrastructure.repository.s3_local_climate_repository")


class S3LocalClimateRepository(S3GeoRepository, LocalClimateRepository):
    """Local climate repository backed by S3-compatible geo-object storage.

    Reads the 8 pre-loaded WorldClim 2.1 COGs stored under fixed object keys.
    Inherits from :class:`S3GeoRepository` and from
    :class:`LocalClimateRepository` for the domain port.
    """

    def __init__(self, aws_session: AWSSession, s3_client: BotoClient, s3_config: S3Config) -> None:
        S3GeoRepository.__init__(self, aws_session, s3_client, s3_config)
        self._logger = logger

    def _get_s3_uri(self, key: str) -> str:
        """Build S3 URI from bucket and key."""
        return f"s3://{self._s3_config.climate_bucket}/{key}"

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
    async def exists(self, bounds: BoundingBox) -> bool:
        """Check whether climate data is available for the requested bounds.

        Returns ``True`` only when all 8 COG objects are present in S3 AND the
        requested bounds are fully inside their (shared) coverage.

        Parameters
        ----------
        bounds : BoundingBox
            Bounding box for the area of interest.

        Returns
        -------
        bool
            True if climate data is available for the requested bounds, False otherwise.
        """
        # 1) All 8 COG objects must exist in the bucket.
        for spec in CLIMATE_VARIABLE_SPECS.values():
            try:
                self._s3_client.head_object(
                    Bucket=self._s3_config.climate_bucket,
                    Key=spec.object_key,
                )
            except self._s3_client.exceptions.ClientError:
                self._logger.warning(
                    "Climate COG not found in S3: %s",
                    self._get_s3_uri(spec.object_key),
                )
                return False

        # 2) The requested bounds must be fully inside the (shared) coverage.
        reference_variable = ClimateVariable.MEAN_ANNUAL_TEMPERATURE
        s3_uri = self._get_s3_uri(CLIMATE_VARIABLE_SPECS[reference_variable].object_key)
        try:
            with rasterio.Env(**self._rasterio_env_options()), rasterio.open(s3_uri) as src:
                coverage = self._coverage_bounds(src)
        except rasterio.errors.RasterioIOError as exc:
            self._logger.warning("Climate COG could not be opened from S3: %s (%s)", s3_uri, exc, exc_info=True)
            return False

        if not self._covers(coverage, bounds):
            self._logger.warning("Requested bounds %s are outside climate coverage %s", bounds, coverage)
            return False

        return True

    @override
    async def get_climate_data(self, bounds: BoundingBox) -> ClimateRasterData | None:
        """Retrieve raster sub-regions for all climate variables from S3 COGs.

        Parameters
        ----------
        bounds : BoundingBox
            Bounding box for the area of interest.

        Returns
        -------
        ClimateRasterData | None
            Raster arrays keyed by variable, or ``None`` if the requested
            bounds are not fully covered by the stored COGs.
        """
        arrays: dict[ClimateVariable, RasterDataArray] = {}

        for spec in CLIMATE_VARIABLE_SPECS.values():
            s3_uri = self._get_s3_uri(spec.object_key)

            try:
                with rasterio.Env(**self._rasterio_env_options()), rasterio.open(s3_uri) as src:
                    if self._is_out_of_coverage(src, bounds):
                        return None
                    arrays[spec.variable] = RasterDataArray(self._read_window(src, bounds))
            except rasterio.errors.RasterioIOError as exc:
                self._logger.warning("Climate COG could not be opened from S3: %s (%s)", s3_uri, exc, exc_info=True)
                return None

        return ClimateRasterData(arrays)

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
            Extent covered by the climate COGs.
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
        """Return True if the requested bounds are outside the raster coverage."""
        coverage = self._coverage_bounds(src)
        if self._covers(coverage, bounds):
            return False
        self._logger.debug("Requested bounds %s are outside climate coverage %s", bounds, coverage)
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


__all__ = ("S3LocalClimateRepository",)
