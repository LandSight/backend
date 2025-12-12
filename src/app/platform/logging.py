import logging
import logging.config
import typing


if typing.TYPE_CHECKING:
    from app.platform.config import LoggingConfig


def configure_logging(config: LoggingConfig) -> None:
    """Configure logging based on the provided settings.

    Parameters
    ----------
    config : LoggingConfig
        Logging configuration.
    """
    dict_config = {
        "version": 1,
        "disable_existing_loggers": True,
        "filters": {},
        "formatters": {
            "pretty": {
                "()": "logging.Formatter",
                "format": "[%(asctime)s] [%(levelname)-8s] %(message)s [%(name)s] [%(filename)s:%(funcName)s:%(lineno)d]",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "formatter": config.formatter,
                "stream": "ext://sys.stdout",
            }
        },
        "root": {
            "level": config.level,
            "handlers": ["stdout"],
        },
        "loggers": {},
    }
    logging.config.dictConfig(dict_config)


__all__ = ("configure_logging",)
