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
