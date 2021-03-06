"""Order 2.0 - total

Revision ID: c1b0cd8fec06
Revises: 5c890003318c
Create Date: 2020-03-25 15:48:10.073729

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c1b0cd8fec06'
down_revision = '5c890003318c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('final', sa.String(length=128), nullable=False))
    op.drop_column('order', 'total')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('total', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.drop_column('order', 'final')
    # ### end Alembic commands ###
