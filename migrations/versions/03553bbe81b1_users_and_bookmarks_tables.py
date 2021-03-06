"""users and bookmarks tables

Revision ID: 03553bbe81b1
Revises: 
Create Date: 2018-04-25 01:50:06.291561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03553bbe81b1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('lastBookViewed', sa.String(length=64), nullable=True),
    sa.Column('lastChapterViewed', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('bookmark',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('book', sa.String(length=64), nullable=True),
    sa.Column('chapter', sa.String(length=64), nullable=True),
    sa.Column('verses', sa.String(length=64), nullable=True),
    sa.Column('version', sa.String(length=64), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bookmark_timestamp'), 'bookmark', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_bookmark_timestamp'), table_name='bookmark')
    op.drop_table('bookmark')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
