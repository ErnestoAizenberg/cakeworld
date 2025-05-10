"""added lst_var_request

Revision ID: cec73a2546fb
Revises: e5927ac6ea44
Create Date: 2025-02-28 13:42:50.066128

"""

import sqlalchemy as sa

from alembic import op

revision = "cec73a2546fb"
down_revision = "e5927ac6ea44"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(
            sa.Column("last_verification_request", sa.DateTime(), nullable=True)
        )


def downgrade():
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("last_verification_request")
