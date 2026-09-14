"""S3 session factories.

Provides factories for creating:
- ``BotoSession`` from application config
- ``AWSSession`` for rasterio S3 access from a ``BotoSession``
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from boto3 import Session as BotoSession
from rasterio.session import AWSSession


if TYPE_CHECKING:
    from app.platform.config.models import S3Config


def create_boto_session(s3_config: S3Config) -> BotoSession:
    """Create a pre-configured boto3 session from S3 configuration.

    Parameters
    ----------
    s3_config : S3Config
        S3-compatible storage configuration.

    Returns
    -------
    BotoSession
        Pre-configured boto3 session.
    """
    return BotoSession(
        aws_access_key_id=s3_config.access_key,
        aws_secret_access_key=s3_config.secret_key.get_secret_value(),
        region_name=s3_config.region,
    )


def create_aws_session(boto_session: BotoSession) -> AWSSession:
    """Create a rasterio AWSSession from a boto3 session.

    Parameters
    ----------
    boto_session : BotoSession
        Pre-configured boto3 session.

    Returns
    -------
    AWSSession
        Rasterio AWS session wrapping the boto3 session.
    """
    return AWSSession(boto_session)


__all__ = (
    "create_aws_session",
    "create_boto_session",
)
