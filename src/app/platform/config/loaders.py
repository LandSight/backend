from functools import cache

from app.platform.config.models import LoggingConfig


@cache
def load_logging_config() -> LoggingConfig:
    """Load logging settings from environment variables.

    Returns
    -------
    LoggingConfig
        Logging configuration populated from the environment.
    """
    return LoggingConfig()
