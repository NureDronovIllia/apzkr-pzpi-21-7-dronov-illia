"""alter vehicle table

Revision ID: c67b0ac39e22
Revises: a739a694a76f
Create Date: 2024-05-26 09:25:49.206861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c67b0ac39e22'
down_revision = 'a739a694a76f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vehicles', sa.Column('current_fuel_lvl', sa.Float(), nullable=False))
    op.add_column('vehicles', sa.Column('max_fuel_lvl', sa.Float(), nullable=False))
    op.drop_column('vehicles', 'fuel_level')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vehicles', sa.Column('fuel_level', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.drop_column('vehicles', 'max_fuel_lvl')
    op.drop_column('vehicles', 'current_fuel_lvl')
    # ### end Alembic commands ###