"""Typed loader for the packaged HMCDA engine configuration."""

from __future__ import annotations

from importlib.resources import files

import pydantic
import yaml

from app.module.analysis.infrastructure.scorer.hmcda.config.models import EngineConfig
from app.module.shared.domain.error import ValidationError


_CONFIG_PACKAGE = "app.module.analysis.infrastructure.scorer.hmcda.config"
_CONFIG_NAME = "engine"


def load_engine_config() -> EngineConfig:
    """Load and validate the packaged HMCDA engine configuration.

    Returns
    -------
    EngineConfig
        The validated configuration with profiles keyed by analysis type.

    Raises
    ------
    ValidationError
        If the document is missing or malformed.
    """
    raw = _read_document(_CONFIG_NAME)
    try:
        return EngineConfig.model_validate(raw)
    except pydantic.ValidationError as exc:
        message = f"Invalid HMCDA engine configuration: {exc}"
        raise ValidationError(message) from exc


def _read_document(base_name: str) -> object:
    """Read a packaged YAML document."""
    resource = files(_CONFIG_PACKAGE).joinpath(f"{base_name}.yaml")
    try:
        with resource.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle)
    except FileNotFoundError as exc:
        message = f"Missing configuration file '{base_name}.yaml'."
        raise ValidationError(message) from exc


__all__ = ("load_engine_config",)
