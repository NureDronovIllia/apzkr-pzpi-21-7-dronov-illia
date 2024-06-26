"""alter user table

Revision ID: a739a694a76f
Revises: 1bf065718edb
Create Date: 2024-05-25 06:29:59.452985

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a739a694a76f'
down_revision = '1bf065718edb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('birth_date', sa.String(length=10), nullable=False))
    op.drop_column('users', 'birth_data')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('birth_data', sa.VARCHAR(length=10), autoincrement=False, nullable=False))
    op.drop_column('users', 'birth_date')
    # ### end Alembic commands ###
