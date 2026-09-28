"""Scoring engine value object."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from app.module.shared.domain.error import ValidationError
from app.module.shared.domain.value_object import BaseCompositeValueObject


if TYPE_CHECKING:
    from app.module.analysis.domain.value_object.analysis_engine import AnalysisEngine
    from app.module.analysis.domain.value_object.engine_description import EngineDescription
    from app.module.analysis.domain.value_object.engine_name import EngineName


@dataclass(frozen=True, slots=True)
class Engine(BaseCompositeValueObject):
    """Catalog descriptor of a scoring engine.

    An engine is the algorithm a client selects to turn collected metrics into a
    score; the version pins the model configuration used for evaluations.

    Attributes
    ----------
    key : AnalysisEngine
        Engine identifier.
    name : EngineName
        Display name shown to clients.
    description : EngineDescription
        Human-readable description of the engine.
    version : str
        Version of the engine model used for evaluations.
    """

    key: AnalysisEngine
    name: EngineName
    description: EngineDescription
    version: str

    def _validate(self) -> None:
        if not self.version:
            message = f"Engine '{self.key}' must carry a version."
            raise ValidationError(message)


__all__ = ("Engine",)
