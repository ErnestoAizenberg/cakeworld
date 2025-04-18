"""created to post with MSC time

Revision ID: efb40236c539
Revises: bf81e8512b0f
Create Date: 2025-03-05 13:47:11.975367

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "efb40236c539"
down_revision: Union[str, None] = "bf81e8512b0f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("android_metadata")
    with op.batch_alter_table("posts", schema=None) as batch_op:
        batch_op.add_column(sa.Column("created", sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("posts", schema=None) as batch_op:
        batch_op.drop_column("created")

    op.create_table("android_metadata", sa.Column("locale", sa.TEXT(), nullable=True))
    # ### end Alembic commands ###
