"""Drop slope_distribution from topography metrics.

Revision ID: c3f0a9d1e2b4
Revises: 674e5b6df11e
Create Date: 2026-09-13 12:30:00.000000

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


if TYPE_CHECKING:
    from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "c3f0a9d1e2b4"
down_revision: str | Sequence[str] | None = "674e5b6df11e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("metrics", "slope_distribution", schema="topography")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "metrics",
        sa.Column(
            "slope_distribution",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
            comment="Slope histogram bins (10 bins, 0-90°) as JSON array",
        ),
        schema="topography",
    )
    op.alter_column("metrics", "slope_distribution", server_default=None, schema="topography")
