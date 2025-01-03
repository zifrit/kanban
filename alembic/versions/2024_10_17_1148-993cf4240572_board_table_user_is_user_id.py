"""board table user_is > user_id

Revision ID: 993cf4240572
Revises: ebb0606fa7fd
Create Date: 2024-10-17 11:48:16.768993

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "993cf4240572"
down_revision: Union[str, None] = "ebb0606fa7fd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("board", sa.Column("user_id", sa.Integer(), nullable=False))
    op.drop_constraint("board_user_is_fkey", "board", type_="foreignkey")
    op.create_foreign_key(None, "board", "users", ["user_id"], ["id"])
    op.drop_column("board", "user_is")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "board",
        sa.Column(
            "user_is", sa.INTEGER(), autoincrement=False, nullable=False
        ),
    )
    op.drop_constraint(None, "board", type_="foreignkey")
    op.create_foreign_key(
        "board_user_is_fkey", "board", "users", ["user_is"], ["id"]
    )
    op.drop_column("board", "user_id")
    # ### end Alembic commands ###
