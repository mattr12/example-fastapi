"""add foreign key to posts table

Revision ID: 8b6d2520c9dc
Revises: 1f6124e61e26
Create Date: 2022-06-05 19:45:04.002645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8b6d2520c9dc"
down_revision = "1f6124e61e26"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("user_id", sa.Integer, nullable=False))
    op.create_foreign_key(
        "post_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["user_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "user_id")
