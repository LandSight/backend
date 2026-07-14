"""Logging configuration for the application.

Uses Python's ``logging.config.dictConfig`` under the hood.
Configuration is driven by :class:`LoggingConfig` from the settings.
"""

from __future__ import annotations

import logging
import logging.config
import typing


if typing.TYPE_CHECKING:
    from app.platform.config.models import LoggingConfig


def _build_dict_config(config: LoggingConfig) -> dict[str, typing.Any]:
    """Convert *LoggingConfig* into the dictionary expected by ``logging.config.dictConfig``.

    Parameters
    ----------
    config : LoggingConfig
        Logging configuration.
    """
    return {
        "version": 1,
        "disable_existing_loggers": True,
        "filters": {},
        "formatters": {
            "pretty": {
                "()": "logging.Formatter",
                "format": "[%(asctime)s] [%(levelname)-8s] %(message)s [%(name)s] [%(filename)s:%(funcName)s:%(lineno)d]",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "brief": {
                "()": "logging.Formatter",
                "format": "[%(asctime)s] [%(levelname)-8s] %(message)s",
                "datefmt": "%H:%M:%S",
            },
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "formatter": config.formatter,
                "stream": "ext://sys.stdout",
            },
        },
        "root": {
            "level": config.level,
            "handlers": ["stdout"],
        },
        "loggers": {
            # Application loggers — must be declared explicitly because
            # disable_existing_loggers=True prevents runtime logger creation.
            "app": {
                "level": config.level,
                "handlers": ["stdout"],
                "propagate": False,
            },
            "app.http.access": {
                "level": config.level,
                "handlers": ["stdout"],
                "propagate": False,
            },
            "app.interface.http.exception_handlers": {
                "level": config.level,
                "handlers": ["stdout"],
                "propagate": False,
            },
            "app.identity.use_case": {
                "level": config.level,
                "handlers": ["stdout"],
                "propagate": False,
            },
            "app.platform.database.session": {
                "level": config.level,
                "handlers": ["stdout"],
                "propagate": False,
            },
        },
    }


def configure_logging(config: LoggingConfig) -> None:
    """Configure logging based on the provided settings.

    Parameters
    ----------
    config : LoggingConfig
        Logging configuration.
    """
    logging.config.dictConfig(_build_dict_config(config))


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
