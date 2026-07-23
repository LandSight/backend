"""Abstract base repository for S3-backed storage.

Provides common S3 operations (upload, download, exists) using a shared
``boto3.Session``. All S3-based repositories should inherit from this
class to avoid duplicating S3 interaction logic.
"""

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from botocore.client import BaseClient
    from rasterio.session import AWSSession

    from app.platform.config.models import S3Config


class S3Repository:
    """Base repository for S3-compatible object storage.

    Parameters
    ----------
    s3_boto_client : BaseClient
        Pre-configured boto3 S3 client (created once at application startup).
    s3_config : S3Config
        S3-compatible storage configuration.
    """

    def __init__(self, s3_boto_client: BaseClient, s3_config: S3Config) -> None:
        self._s3_boto_client = s3_boto_client
        self._bucket = s3_config.bucket


class S3GeoRepository(S3Repository):
    """Base repository for S3-compatible geo-object storage.

    Parameters
    ----------
    aws_session : AWSSession
        Pre-configured aws session for rasterio.
    s3_boto_client : BaseClient
            Pre-configured boto3 S3 client (created once at application startup).
    s3_config : S3Config
        S3-compatible storage configuration.
    """

    def __init__(self, aws_session: AWSSession, s3_boto_client: BaseClient, s3_config: S3Config) -> None:
        super().__init__(s3_boto_client, s3_config)
        self._aws_session = aws_session


__all__ = (
    "S3GeoRepository",
    "S3Repository",
)
