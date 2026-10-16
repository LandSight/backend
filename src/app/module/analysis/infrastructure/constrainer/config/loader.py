"""Typed loader for the packaged constraint policy."""

from __future__ import annotations

from importlib.resources import files

import pydantic
import yaml

from app.module.analysis.infrastructure.constrainer.config.models import ConstraintsConfig
from app.module.shared.domain.error import ValidationError


_CONFIG_PACKAGE = "app.module.analysis.infrastructure.constrainer.config"
_CONFIG_FILE = "constraints.yaml"


def load_constraints_config() -> ConstraintsConfig:
    """Load and validate the packaged constraint policy.

    Raises
    ------
    ValidationError
        If the document is missing or malformed.
    """
    resource = files(_CONFIG_PACKAGE).joinpath(_CONFIG_FILE)
    try:
        with resource.open("r", encoding="utf-8") as handle:
            raw = yaml.safe_load(handle)
    except FileNotFoundError as exc:
        message = f"Missing configuration file '{_CONFIG_FILE}'."
        raise ValidationError(message) from exc
    try:
        return ConstraintsConfig.model_validate(raw)
    except pydantic.ValidationError as exc:
        message = f"Invalid constraint policy: {exc}"
        raise ValidationError(message) from exc


__all__ = ("load_constraints_config",)
