"""add user table

Revision ID: 1f6124e61e26
Revises: 46f3a9a220a4
Create Date: 2022-06-05 19:37:00.104430

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1f6124e61e26"
down_revision = "46f3a9a220a4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, nullable=False, primary_key=True),
        sa.Column("email", sa.String, nullable=False, unique=True),
        sa.Column("password", sa.String, nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("users")
