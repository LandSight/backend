"""Add interpretation generation status.

Tracks the report generation lifecycle so clients can show whether the report
is ordered, being generated, completed or failed. Existing rows hold finished
reports, so the column defaults to ``completed``.

Revision ID: a9b8c7d6e5f4
Revises: b1c2d3e4f5a6
Create Date: 2026-10-05 08:00:00.000000

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op


if TYPE_CHECKING:
    from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "a9b8c7d6e5f4"
down_revision: str | Sequence[str] | None = "b1c2d3e4f5a6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "interpretations",
        sa.Column(
            "status",
            sa.String(length=16),
            server_default="completed",
            nullable=False,
            comment="Report generation status: ordered/running/completed/failed",
        ),
        schema="interpretation",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("interpretations", "status", schema="interpretation")


__all__ = ("down_revision", "downgrade", "revision", "upgrade")
