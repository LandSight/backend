"""Static restriction policy."""

from __future__ import annotations

from typing import Final


# Positional tolerance of the overlap test, in meters. A zone counts as
# overlapping only when it reaches deeper than this into the parcel: OSM
# objects and hand-drawn parcels are a few meters off, and buffer widths
# derived from OSM are approximations, so a zone that merely grazes the
# boundary is noise, not a restriction.
POSITIONAL_TOLERANCE_M: Final[float] = 3.0


__all__ = ("POSITIONAL_TOLERANCE_M",)
