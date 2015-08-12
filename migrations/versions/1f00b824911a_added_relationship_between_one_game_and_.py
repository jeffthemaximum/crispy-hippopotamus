"""added relationship between one game and many posts

Revision ID: 1f00b824911a
Revises: 5833d5971a5e
Create Date: 2015-08-11 14:32:42.517486

"""

# revision identifiers, used by Alembic.
revision = '1f00b824911a'
down_revision = '5833d5971a5e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'posts_game_id_fkey', 'posts', type_='foreignkey')
    op.create_foreign_key(None, 'posts', 'games', ['game_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.create_foreign_key(u'posts_game_id_fkey', 'posts', 'users', ['game_id'], ['id'])
    ### end Alembic commands ###