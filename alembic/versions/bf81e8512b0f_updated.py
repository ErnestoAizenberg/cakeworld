"""updated

Revision ID: bf81e8512b0f
Revises: cec73a2546fb
Create Date: 2025-03-01 13:17:08.042113

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "bf81e8512b0f"
down_revision: Union[str, None] = "cec73a2546fb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("android_metadata")
    with op.batch_alter_table("chats", schema=None) as batch_op:
        batch_op.add_column(sa.Column("is_private", sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("chats", schema=None) as batch_op:
        batch_op.drop_column("is_private")

    op.create_table("android_metadata", sa.Column("locale", sa.TEXT(), nullable=True))
    # ### end Alembic commands ###
