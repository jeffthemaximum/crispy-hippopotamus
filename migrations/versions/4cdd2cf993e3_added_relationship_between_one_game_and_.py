"""added relationship between one game and many posts

Revision ID: 4cdd2cf993e3
Revises: c14b486d082
Create Date: 2015-08-11 14:25:12.626691

"""

# revision identifiers, used by Alembic.
revision = '4cdd2cf993e3'
down_revision = 'c14b486d082'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('game_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'posts', 'users', ['game_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.drop_column('posts', 'game_id')
    ### end Alembic commands ###
