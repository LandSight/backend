from functools import cache

from app.platform.config.models import AppConfig, AuthConfig, DatabaseConfig, LoggingConfig, S3Config


@cache
def load_app_config() -> AppConfig:
    """Load full application configuration.

    Returns
    -------
    AppConfig
        App configuration populated from the environment.
    """
    return AppConfig()


@cache
def load_logging_config() -> LoggingConfig:
    """Load logging settings from environment variables.

    Returns
    -------
    LoggingConfig
        Logging configuration populated from the environment.
    """
    return load_app_config().logging


def load_database_config() -> DatabaseConfig:
    """Load database settings from environment variables.

    Returns
    -------
    DatabaseConfig
        Database configuration populated from the environment.
    """
    return load_app_config().database


def load_auth_config() -> AuthConfig:
    """Load authentication settings from environment variables.

    Returns
    -------
    AuthConfig
        Authentication configuration populated from the environment.
    """
    return load_app_config().auth


def load_s3_config() -> S3Config:
    """Load S3 storage settings from environment variables.

    Returns
    -------
    S3Config
        S3 configuration populated from the environment.
    """
    return load_app_config().s3


__all__ = (
    "load_app_config",
    "load_auth_config",
    "load_database_config",
    "load_logging_config",
    "load_s3_config",
)
