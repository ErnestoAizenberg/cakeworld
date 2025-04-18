"""notification model has added

Revision ID: 41361c17d06a
Revises: 0d8dc99933f1
Create Date: 2025-03-12 14:25:07.939628

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "41361c17d06a"
down_revision: Union[str, None] = "0d8dc99933f1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("android_metadata")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table("android_metadata", sa.Column("locale", sa.TEXT(), nullable=True))
    # ### end Alembic commands ###
