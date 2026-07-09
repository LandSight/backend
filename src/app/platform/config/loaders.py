from functools import cache

from app.platform.config.models import AuthConfig, DatabaseConfig, LoggingConfig


@cache
def load_logging_config() -> LoggingConfig:
    """Load logging settings from environment variables.

    Returns
    -------
    LoggingConfig
        Logging configuration populated from the environment.
    """
    return LoggingConfig()


@cache
def load_database_config() -> DatabaseConfig:
    """Load database settings from environment variables.

    Returns
    -------
    DatabaseConfig
        Database configuration populated from the environment.
    """
    return DatabaseConfig()


@cache
def load_auth_config() -> AuthConfig:
    """Load authentication settings from environment variables.

    Returns
    -------
    AuthConfig
        Authentication configuration populated from the environment.
    """
    return AuthConfig()
