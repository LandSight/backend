from __future__ import annotations

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


def get_logger(logger: str | None = None) -> logging.Logger:
    """Return a configured logger.

    Parameters
    ----------
    logger : str | None, optional
        Logger name to retrieve. If ``None``, the root logger is returned.

    Returns
    -------
    logging.Logger
        The requested logger instance.
    """
    return logging.getLogger(logger)


__all__ = (
    "configure_logging",
    "get_logger",
)
