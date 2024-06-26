"""modify nodes again

Revision ID: c2e7c1a3fc49
Revises: 00ff28485e61
Create Date: 2024-06-14 16:16:38.453579

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c2e7c1a3fc49"
down_revision: Union[str, None] = "00ff28485e61"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "nodes", sa.Column("character_name", sa.String(length=40), nullable=False)
    )
    op.drop_column("nodes", "charachter_name")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "nodes",
        sa.Column(
            "charachter_name", sa.VARCHAR(length=40), autoincrement=False, nullable=False
        ),
    )
    op.drop_column("nodes", "character_name")
    # ### end Alembic commands ###
