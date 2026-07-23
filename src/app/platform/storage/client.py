"""S3 session factories.

Provides factories for creating:
- ``BotoSession`` from application config
- ``AWSSession`` for rasterio S3 access from a ``BotoSession``
"""

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from boto3 import Session as BotoSession
    from botocore.client import BaseClient


def create_s3_boto_client(boto_session: BotoSession) -> BaseClient:
    """Create a boto3 S3 client from a session.

    Parameters
    ----------
    boto_session : BotoSession
        Pre-configured boto3 session.

    Returns
    -------
    BaseClient
        Boto3 S3 client.
    """
    return boto_session.client("s3")


__all__ = ("create_s3_boto_client",)
