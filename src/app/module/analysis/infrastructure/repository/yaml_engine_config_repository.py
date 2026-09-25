"""YAML-backed engine configuration repository."""

from __future__ import annotations

from importlib.resources import files
from typing import TYPE_CHECKING, Any, cast

import yaml

from app.module.analysis.domain.value_object import (
    AnalysisKey,
    AnalysisType,
    Hierarchy,
    HierarchyNode,
    Weight,
)
from app.module.analysis.infrastructure.fuzzy import build_fuzzy_function
from app.module.analysis.infrastructure.ports import EngineConfigRepository, FuzzyFunction
from app.module.shared.domain.error import ValidationError


if TYPE_CHECKING:
    from collections.abc import Mapping


_CONFIG_PACKAGE = "app.module.analysis.infrastructure.config"


class YamlEngineConfigRepository(EngineConfigRepository):
    """Reads the engine configuration from packaged YAML documents.

    Both the hierarchy and the fuzzy functions are read through the same private
    YAML accessor, which resolves the document for the requested analysis type.
    """

    def get_hierarchy(self, analysis_type: AnalysisType) -> Hierarchy:
        """See :class:`app.module.analysis.infrastructure.ports.EngineConfigRepository.get_hierarchy`."""
        raw = self._read_document("hierarchy", analysis_type)
        roots = tuple(
            self._parse_node(cast("dict[str, Any]", item)) for item in cast("list[Any]", raw.get("clusters", []))
        )
        return Hierarchy(
            analysis_type=analysis_type,
            model_version=str(raw.get("model_version", "unknown")),
            roots=roots,
        )

    def get_fuzzy_functions(self, analysis_type: AnalysisType) -> Mapping[str, FuzzyFunction]:
        """See :class:`app.module.analysis.infrastructure.ports.EngineConfigRepository.get_fuzzy_functions`."""
        raw = self._read_document("fuzzy_functions", analysis_type)
        functions = cast("Mapping[str, Any]", raw.get("functions", {}))
        if not functions:
            message = f"No fuzzy functions configured for analysis type '{analysis_type}'."
            raise ValidationError(message)
        return {
            str(key): self._parse_function(str(key), cast("Mapping[str, Any]", data)) for key, data in functions.items()
        }

    @staticmethod
    def _read_document(base_name: str, analysis_type: AnalysisType) -> dict[str, Any]:
        """Read a packaged YAML document, specialising by analysis type."""
        package = files(_CONFIG_PACKAGE)
        specialised = package.joinpath(f"{base_name}.{analysis_type.value}.yaml")
        resource = specialised if specialised.is_file() else package.joinpath(f"{base_name}.yaml")
        try:
            with resource.open("r", encoding="utf-8") as handle:
                raw = yaml.safe_load(handle)
        except FileNotFoundError as exc:
            message = f"Missing configuration file '{base_name}' for analysis type '{analysis_type}'."
            raise ValidationError(message) from exc
        if not isinstance(raw, dict):
            message = f"Configuration '{base_name}' must be a YAML mapping."
            raise ValidationError(message)
        declared = str(raw.get("analysis_type", "")).lower()
        if declared != analysis_type.value:
            message = f"Configuration declares analysis type '{declared}', expected '{analysis_type.value}'."
            raise ValidationError(message)
        return cast("dict[str, Any]", raw)

    def _parse_node(self, raw: dict[str, Any]) -> HierarchyNode:
        """Parse one hierarchy node, recursing into its components."""
        components = tuple(
            self._parse_node(cast("dict[str, Any]", item)) for item in cast("list[Any]", raw.get("components", []))
        )
        return HierarchyNode(
            key=AnalysisKey(str(raw["key"])),
            weight=self._parse_weight(raw["weight"]),
            components=components,
        )

    @staticmethod
    def _parse_weight(raw: object) -> Weight:
        """Parse a node weight and wrap it in its value object."""
        try:
            return Weight(cast("float", raw))
        except (TypeError, ValueError) as exc:
            message = f"Invalid weight value: {raw!r}."
            raise ValidationError(message) from exc

    @staticmethod
    def _parse_function(key: str, raw: Mapping[str, Any]) -> FuzzyFunction:
        """Parse and validate one fuzzy function definition."""
        params_raw = cast("Mapping[str, Any]", raw.get("params", {}))
        try:
            params = {str(name): float(value) for name, value in params_raw.items()}
            return build_fuzzy_function(str(raw["type"]), params, str(raw.get("unit", "")))
        except (TypeError, KeyError, ValueError, ValidationError) as exc:
            message = f"Invalid fuzzy function '{key}': {exc}."
            raise ValidationError(message) from exc


__all__ = ("YamlEngineConfigRepository",)
