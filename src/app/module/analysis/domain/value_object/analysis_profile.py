"""Analysis profile value object."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from app.module.shared.domain.value_object import BaseCompositeValueObject


if TYPE_CHECKING:
    from app.module.analysis.domain.value_object.analysis_profile_description import AnalysisProfileDescription
    from app.module.analysis.domain.value_object.analysis_profile_name import AnalysisProfileName
    from app.module.analysis.domain.value_object.analysis_type import AnalysisType


@dataclass(frozen=True, slots=True)
class AnalysisProfile(BaseCompositeValueObject):
    """Catalog descriptor of an analysis profile.

    A profile is the domain concept a client selects to evaluate a parcel; the
    scoring hierarchy and collection parameters are resolved from it.

    Attributes
    ----------
    key : AnalysisType
        Profile identifier.
    name : AnalysisProfileName
        Display name shown to clients.
    description : AnalysisProfileDescription
        Human-readable description of what the profile evaluates.
    """

    key: AnalysisType
    name: AnalysisProfileName
    description: AnalysisProfileDescription

    def _validate(self) -> None:
        """Validate the profile descriptor."""


__all__ = ("AnalysisProfile",)
