"""clean classes

Revision ID: 56438119988a
Revises: ce06270c1263
Create Date: 2020-03-25 17:19:07.082724

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '56438119988a'
down_revision = 'ce06270c1263'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('steaktopping_steak_id_fkey', 'steaktopping', type_='foreignkey')
    op.drop_column('steaktopping', 'large_price')
    op.drop_column('steaktopping', 'steak_id')
    op.drop_column('steaktopping', 'small_price')
    op.drop_constraint('topping_pizza_id_fkey', 'topping', type_='foreignkey')
    op.drop_column('topping', 'pizza_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('topping', sa.Column('pizza_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('topping_pizza_id_fkey', 'topping', 'pizza', ['pizza_id'], ['id'])
    op.add_column('steaktopping', sa.Column('small_price', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('steaktopping', sa.Column('steak_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('steaktopping', sa.Column('large_price', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.create_foreign_key('steaktopping_steak_id_fkey', 'steaktopping', 'sub', ['steak_id'], ['id'])
    # ### end Alembic commands ###