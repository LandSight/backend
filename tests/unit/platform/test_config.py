import typing

import pytest

from app.platform.config.loaders import load_logging_config


class TestLoggingConfigLoader:
    """Test the logging configuration loader."""

    @staticmethod
    @pytest.fixture(autouse=True)
    def clear_cache_config_loaders() -> typing.Generator:
        """Clear the cache of config loaders."""
        load_logging_config.cache_clear()
        yield None
        load_logging_config.cache_clear()

    @staticmethod
    def test_load_logging_config_reads_env(monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that the logging configuration is loaded from environment variables."""
        monkeypatch.setenv("LOGGING_LEVEL", "CRITICAL")
        monkeypatch.setenv("LOGGING_FORMATTER", "pretty")

        logging_config = load_logging_config()

        assert logging_config.level == "CRITICAL"
        assert logging_config.formatter == "pretty"

    @staticmethod
    def test_load_logging_config_returns_cached_instance() -> None:
        """Test that the logging configuration is cached."""
        logging_config = load_logging_config()

        logging_config_cached = load_logging_config()

        load_logging_config.cache_clear()

        logging_config_no_cached = load_logging_config()

        assert logging_config is logging_config_cached
        assert logging_config is not logging_config_no_cached
