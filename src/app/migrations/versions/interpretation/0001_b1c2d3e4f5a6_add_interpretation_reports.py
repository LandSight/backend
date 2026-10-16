"""Add interpretation reports.

The report stores only the generated text (summary and per-aspect
explanations) and the model that produced it. Scores, weights and evaluation
metadata are recomputed from the current evaluation when the report is read, so
they are not duplicated here.

Revision ID: b1c2d3e4f5a6
Revises:
Create Date: 2026-09-30 08:20:00.000000

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


if TYPE_CHECKING:
    from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "b1c2d3e4f5a6"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "interpretations",
        sa.Column("analysis_id", sa.UUID(), nullable=False, comment="ID of the analysis the report belongs to"),
        sa.Column("model", sa.String(length=128), nullable=False, comment="Model that generated the report"),
        sa.Column("summary", sa.Text(), nullable=False, comment="Combined top-aspects summary"),
        sa.Column(
            "aspect_explanations",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            comment="Explanation text keyed by aspect key",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["analysis_id"],
            ["analysis.analyses.id"],
            name=op.f("fk_interpretations_analysis_id_analyses"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_interpretations")),
        schema="interpretation",
    )
    op.create_index(
        "ix_interpretations_analysis_id",
        "interpretations",
        ["analysis_id"],
        unique=True,
        schema="interpretation",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_interpretations_analysis_id", table_name="interpretations", schema="interpretation")
    op.drop_table("interpretations", schema="interpretation")
