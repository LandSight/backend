import typing

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.platform.constants import ENV_FILE


class BaseConfig(BaseSettings):
    """Base settings for the application.

    Notes
    -----
    Configuration is loaded from environment variables and the project-level ``.env``
    file specified by ``ENV_FILE``. Unknown variables are ignored. Nested settings
    can be provided using the ``__`` delimiter.
    """

    model_config = SettingsConfigDict(
        extra="ignore",
        env_nested_delimiter="__",
        env_file=ENV_FILE,
    )


class LoggingConfig(BaseConfig):
    """Logging configuration.

    Attributes
    ----------
    level : {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        Logging level. Can be overridden via the ``LOGGING_LEVEL`` environment
        variable.
    formatter : {"pretty"}
        Formatter name. Can be overridden via the ``LOGGING_FORMATTER``
        environment variable.
    """

    model_config = SettingsConfigDict(
        env_prefix="LOGGING_",
    )
    level: typing.Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    formatter: typing.Literal["pretty"] = "pretty"


class DatabaseConfig(BaseConfig):
    """Database configuration.

    Attributes
    ----------
    name : str
        Database name.
    host : str
        Database host.
    port : int
        Database port.
    username : str
        Database user.
    password : str
        Database password.
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
    name: str = Field(
        default="landsight",
        description="Database name",
        min_length=1,
    )
    host: str = Field(
        default="localhost",
        description="Database host",
        min_length=1,
    )
    port: int = Field(
        default=5432,
        description="Database port",
        ge=1,
        le=65535,
    )
    username: str = Field(
        default="landsight",
        description="Database username",
        min_length=1,
    )
    password: SecretStr = Field(
        default=SecretStr("landsight"),
        description="Database password",
    )

    echo: bool = Field(
        default=False,
        description="Enable SQL echo for debugging",
    )
    pool_size: int = Field(
        default=5,
        description="Connection pool size",
        ge=1,
    )
    max_overflow: int = Field(
        default=10,
        description="Maximum overflow connections",
        ge=0,
    )
    engine: str = Field(
        default="postgresql",
        description="Database engine",
        frozen=True,
    )
    driver: str = Field(
        default="asyncpg",
        description="Database driver",
        frozen=True,
    )

    def get_url(self) -> str:
        """Build a full async database URL from connection parameters.

        Returns
        -------
        str
            Database URL in the form
            ``engine+driver://user:pass@host:port/name``.
        """
        return f"{self.engine}+{self.driver}://{self.username}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}"


class AuthConfig(BaseConfig):
    """Authentication configuration.

    Attributes
    ----------
    secret_key : str
        Secret key for JWT signing.
    algorithm : str
        JWT signing algorithm.
    access_token_expire_minutes : int
        Access token lifetime in minutes.
    refresh_token_expire_days : int
        Refresh token lifetime in days.
    """

    model_config = SettingsConfigDict(
        env_prefix="AUTH_",
    )
    secret_key: SecretStr = Field(
        default=SecretStr("dev-secret-key-do-not-use-in-production"),
        description="Secret key for JWT signing",
        min_length=32,
    )
    algorithm: str = Field(
        default="HS256",
        description="JWT signing algorithm",
        pattern=r"^(HS256|HS384|HS512|RS256|RS384|RS512|ES256|ES384|ES512)$",
    )
    access_token_expire_minutes: int = Field(
        default=30,
        description="Access token lifetime in minutes",
        ge=1,
        le=1440,
    )
    refresh_token_expire_days: int = Field(
        default=7,
        description="Refresh token lifetime in days",
        ge=1,
        le=30,
    )


class S3Config(BaseConfig):
    """S3-compatible storage configuration for geospatial rasters.

    Attributes
    ----------
    endpoint : str
        S3 endpoint URL (e.g., http://localhost:9000 for MinIO).
    bucket : str
        Bucket name for raster storage.
    access_key : str
        S3 access key.
    secret_key : SecretStr
        S3 secret key.
    secure : bool
        Use HTTPS (False for local MinIO).
    region : str
        S3 region (us-east-1 by default).
    """

    model_config = SettingsConfigDict(
        env_prefix="S3_",
    )
    endpoint: str = Field(
        default="http://localhost:9000",
        description="S3 endpoint URL",
        min_length=1,
    )
    dem_bucket: str = Field(
        default="landsight-dem",
        description="Bucket name for dem storage",
        min_length=1,
    )
    access_key: str = Field(
        default="admin",
        description="S3 access key",
        min_length=1,
    )
    secret_key: SecretStr = Field(
        default=SecretStr("password123"),
        description="S3 secret key",
    )
    secure: bool = Field(
        default=False,
        description="Use HTTPS",
    )
    region: str = Field(
        default="us-east-1",
        description="S3 region",
        min_length=1,
    )

    def get_endpoint_url(self) -> str:
        """Get endpoint URL without protocol."""
        return self.endpoint.replace("http://", "").replace("https://", "")


class AppConfig(BaseConfig):
    """Application configuration — root config."""

    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    auth: AuthConfig = Field(default_factory=AuthConfig)
    s3: S3Config = Field(default_factory=S3Config)
