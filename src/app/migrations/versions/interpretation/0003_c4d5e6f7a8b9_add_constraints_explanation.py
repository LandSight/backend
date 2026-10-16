"""Add interpretation restrictions explanation.

Stores the generated explanation of the restriction zones that barred the
scenario or lowered the score. Existing reports were generated without it, so
the column defaults to an empty text.

Revision ID: c4d5e6f7a8b9
Revises: a9b8c7d6e5f4
Create Date: 2026-10-16 08:00:00.000000

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op


if TYPE_CHECKING:
    from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "c4d5e6f7a8b9"
down_revision: str | Sequence[str] | None = "a9b8c7d6e5f4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "interpretations",
        sa.Column(
            "constraints_explanation",
            sa.Text(),
            server_default="",
            nullable=False,
            comment="Explanation of the restriction zones that lowered the score",
        ),
        schema="interpretation",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("interpretations", "constraints_explanation", schema="interpretation")


__all__ = ("down_revision", "downgrade", "revision", "upgrade")
