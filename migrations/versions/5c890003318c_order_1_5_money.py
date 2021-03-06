"""Order 1.5 - money

Revision ID: 5c890003318c
Revises: 1f4115e706fa
Create Date: 2020-03-25 15:23:17.117653

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c890003318c'
down_revision = '1f4115e706fa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('money', sa.String(length=128), nullable=False))
    op.drop_column('item', 'price')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('price', sa.VARCHAR(length=128), autoincrement=False, nullable=False))
    op.drop_column('item', 'money')
    # ### end Alembic commands ###
