"""add analyses table

Revision ID: 002_analyses
Revises: 001_initial
Create Date: 2026-07-14

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "002_analyses"
down_revision: Union[str, None] = "001_initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "analyses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("information_id", sa.Integer(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("key_topics", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("relevance_score", sa.Float(), nullable=False),
        sa.Column("commercial_potential", sa.String(length=20), nullable=False),
        sa.Column("analyzed_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("raw_response", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(["information_id"], ["information.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("information_id"),
    )
    op.create_index("ix_analyses_information_id", "analyses", ["information_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_analyses_information_id", table_name="analyses")
    op.drop_table("analyses")
