"""Add Artist to Songs Table

Revision ID: 767924ae0783
Revises: a6887fce3299
Create Date: 2018-09-30 21:35:18.711330

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '767924ae0783'
down_revision = 'a6887fce3299'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('songs', sa.Column('artist', sa.String(length=128), nullable=False))
    op.add_column('songs', sa.Column('title', sa.String(length=128), nullable=False))
    op.drop_constraint('songs_name_key', 'songs', type_='unique')
    op.drop_column('songs', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('songs', sa.Column('name', sa.VARCHAR(length=128), autoincrement=False, nullable=False))
    op.create_unique_constraint('songs_name_key', 'songs', ['name'])
    op.drop_column('songs', 'title')
    op.drop_column('songs', 'artist')
    # ### end Alembic commands ###
