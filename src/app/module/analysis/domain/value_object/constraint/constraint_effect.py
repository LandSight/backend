"""Constraint effect value object."""

from __future__ import annotations

from enum import StrEnum


class ConstraintEffect(StrEnum):
    """What an applied constraint does to the score.

    ``PROHIBIT`` bars the scenario on the parcel and zeroes the total score;
    ``PENALTY`` multiplies the score by a factor below one.
    """

    PROHIBIT = "prohibit"
    PENALTY = "penalty"


__all__ = ("ConstraintEffect",)
