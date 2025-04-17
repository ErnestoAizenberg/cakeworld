"""added storin image paths for User, Chat, Post, Message

Revision ID: e5927ac6ea44
Revises: 29cbdb49eb44
Create Date: 2025-02-26 19:26:12.851708

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e5927ac6ea44"
down_revision: Union[str, None] = "29cbdb49eb44"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "chats", sa.Column("avatar_path", sa.String(length=256), nullable=True)
    )
    op.add_column("messages", sa.Column("images", sa.JSON(), nullable=True))
    op.add_column("posts", sa.Column("images", sa.JSON(), nullable=True))
    op.add_column(
        "users", sa.Column("avatar_path", sa.String(length=256), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "avatar_path")
    op.drop_column("posts", "images")
    op.drop_column("messages", "images")
    op.drop_column("chats", "avatar_path")
    # ### end Alembic commands ###
