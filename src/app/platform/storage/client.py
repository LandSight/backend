"""S3 session factories.

Provides factories for creating:
- ``BotoSession`` from application config
- ``AWSSession`` for rasterio S3 access from a ``BotoSession``
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from botocore.config import Config


if TYPE_CHECKING:
    from boto3 import Session as BotoSession
    from botocore.client import BaseClient

    from app.platform.config.models import S3Config


def create_s3_boto_client(boto_session: BotoSession, s3_config: S3Config) -> BaseClient:
    """Create a boto3 S3 client from a session.

    Parameters
    ----------
    boto_session : BotoSession
        Pre-configured boto3 session.
    s3_config : S3Config
        S3 configuration with the endpoint URL.

    Returns
    -------
    BaseClient
        Boto3 S3 client.
    """
    return boto_session.client(
        "s3",
        endpoint_url=s3_config.endpoint,
        config=Config(
            signature_version="s3v4",
            s3={"addressing_style": "path"},
        ),
    )


__all__ = ("create_s3_boto_client",)
