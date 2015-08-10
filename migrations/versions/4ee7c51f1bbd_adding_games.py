"""adding games

Revision ID: 4ee7c51f1bbd
Revises: 58404d0b7e55
Create Date: 2015-08-05 10:28:03.266280

"""

# revision identifiers, used by Alembic.
revision = '4ee7c51f1bbd'
down_revision = '58404d0b7e55'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('games',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('board_state', sa.String(length=128), nullable=True),
    sa.Column('player_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('last_played', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['player_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_games_created_at'), 'games', ['created_at'], unique=False)
    op.create_index(op.f('ix_games_last_played'), 'games', ['last_played'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_games_last_played'), table_name='games')
    op.drop_index(op.f('ix_games_created_at'), table_name='games')
    op.drop_table('games')
    ### end Alembic commands ###