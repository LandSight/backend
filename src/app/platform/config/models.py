import typing

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.platform.constants import ENV_FILE


class BaseConfig(BaseSettings):
    """Base settings for the application.

    Notes
    -----
    Configuration is loaded from environment variables and the project-level `.env`
    file specified by `ENV_FILE`. Unknown variables are ignored. Nested settings
    can be provided using the `__` delimiter.
    """

    model_config = SettingsConfigDict(
        extra="ignore",
        env_nested_delimiter="__",
        env_file=ENV_FILE,
    )


class LoggingConfig(BaseConfig):
    """Logging configuration.

    Notes
    -----
    All environment variables for this section must be prefixed with `LOGGING_`.

    Attributes
    ----------
    level : {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        Logging level. Can be overridden via the `LOGGING_LEVEL` environment
        variable.
    formatter : {"pretty"}
        Formatter name. Can be overridden via the `LOGGING_FORMATTER`
        environment variable.

    """

    model_config = SettingsConfigDict(
        env_prefix="LOGGING_",
    )
    level: typing.Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    formatter: typing.Literal["pretty"] = "pretty"


class DatabaseConfig(BaseConfig):
    """Database configuration.

    Notes
    -----
    All environment variables for this section must be prefixed with `DATABASE_`.

    Attributes
    ----------
    url : str
        Database URL. Example: ``postgresql+asyncpg://user:pass@localhost:5432/db``.
    echo : bool
        Enable SQL echo for debugging.
    pool_size : int
        Connection pool size.
    max_overflow : int
        Maximum overflow connections.
    """

    model_config = SettingsConfigDict(
        env_prefix="DATABASE_",
    )
    url: str = "postgresql+asyncpg://landsight:landsight@localhost:5432/landsight"
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10
