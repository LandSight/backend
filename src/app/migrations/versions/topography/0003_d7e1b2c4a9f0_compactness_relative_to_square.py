"""Rescale the compactness index relative to a square.

The index used to be the raw Polsby-Popper score (4πA/P²), where a square
scored π/4 ≈ 0.785. It is now divided by π/4 and capped at 1.0, so a square
scores 1.0.

Revision ID: d7e1b2c4a9f0
Revises: c3f0a9d1e2b4
Create Date: 2026-10-09 16:00:00.000000

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op


if TYPE_CHECKING:
    from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "d7e1b2c4a9f0"
down_revision: str | Sequence[str] | None = "c3f0a9d1e2b4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        "UPDATE topography.metrics SET compactness_index = ROUND(LEAST(compactness_index / (pi() / 4), 1)::numeric, 4)"
    )
    op.alter_column(
        "metrics",
        "compactness_index",
        existing_type=sa.Float(),
        existing_nullable=False,
        comment="Compactness index relative to a square (1 = square), dimensionless",
        existing_comment="Compactness index (4πA/P²), dimensionless",
        schema="topography",
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Values capped at 1.0 cannot be restored exactly; they map back to a square.
    op.execute("UPDATE topography.metrics SET compactness_index = ROUND((compactness_index * pi() / 4)::numeric, 4)")
    op.alter_column(
        "metrics",
        "compactness_index",
        existing_type=sa.Float(),
        existing_nullable=False,
        comment="Compactness index (4πA/P²), dimensionless",
        existing_comment="Compactness index relative to a square (1 = square), dimensionless",
        schema="topography",
    )
