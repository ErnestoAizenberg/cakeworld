"""color to category

Revision ID: 6017a83958a7
Revises: abfdbc6d210f
Create Date: 2024-04-05 00:11:51.286974

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6017a83958a7"
down_revision: Union[str, None] = "abfdbc6d210f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("categories", schema=None) as batch_op:
        batch_op.add_column(sa.Column("color", sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("categories", schema=None) as batch_op:
        batch_op.drop_column("color")

    # ### end Alembic commands ###
