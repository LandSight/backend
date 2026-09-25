"""Fuzzy function builder."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.module.analysis.infrastructure.fuzzy.s_shaped import SShaped
from app.module.analysis.infrastructure.fuzzy.trapezoidal import Trapezoidal
from app.module.analysis.infrastructure.fuzzy.z_shaped import ZShaped
from app.module.shared.domain.error import ValidationError


if TYPE_CHECKING:
    from collections.abc import Mapping

    from app.module.analysis.infrastructure.ports import FuzzyFunction


def build_fuzzy_function(function_type: str, params: Mapping[str, float], unit: str = "") -> FuzzyFunction:
    """Build a fuzzy function from its configured type and parameters.

    Parameters
    ----------
    function_type : str
        One of ``z_shaped``, ``s_shaped`` or ``trapezoidal``.
    params : Mapping[str, float]
        Constructor parameters of the function.
    unit : str
        Unit of the raw metric.

    Returns
    -------
    FuzzyFunction
        The constructed function.

    Raises
    ------
    ValidationError
        If the function type is unknown or its parameters are invalid.
    """
    values = dict(params)
    match function_type:
        case "z_shaped":
            return ZShaped(
                unit=unit,
                optimal_max=values["optimal_max"],
                acceptable_max=values["acceptable_max"],
            )
        case "s_shaped":
            return SShaped(unit=unit, minimum=values["min"], maximum=values["max"])
        case "trapezoidal":
            return Trapezoidal(
                unit=unit,
                low=values["low"],
                optimal_min=values["optimal_min"],
                optimal_max=values["optimal_max"],
                high=values["high"],
            )
        case _:
            message = f"Unknown fuzzy function type: '{function_type}'."
            raise ValidationError(message)


__all__ = ("build_fuzzy_function",)
