"""adjust name colunm rubber farm

Revision ID: cb08b0a7d01e
Revises: 0e8bf6da4832
Create Date: 2025-03-05 16:18:00.521350

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb08b0a7d01e'
down_revision: Union[str, None] = '0e8bf6da4832'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('RubberFarm', sa.Column('citizen_id', sa.String(length=13), nullable=True))
    op.drop_column('RubberFarm', 'citzen_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uq_user_role', 'UserRole', type_='unique')
    op.add_column('RubberFarm', sa.Column('citzen_id', sa.VARCHAR(length=13), autoincrement=False, nullable=True))
    op.drop_column('RubberFarm', 'citizen_id')
    # ### end Alembic commands ###
