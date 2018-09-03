"""empty message

Revision ID: 897066fb86bb
Revises: 3cd9e9b6f3f1
Create Date: 2018-08-31 22:07:54.099654

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '897066fb86bb'
down_revision = '3cd9e9b6f3f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('wushu_teams', sa.Column('city', sa.String(length=20), nullable=False))
    op.add_column('wushu_teams', sa.Column('country', sa.String(length=20), nullable=False))
    op.add_column('wushu_teams', sa.Column('detail_address', sa.String(length=40), nullable=False))
    op.add_column('wushu_teams', sa.Column('en_name', sa.String(length=20), nullable=False))
    op.add_column('wushu_teams', sa.Column('pemail', sa.String(length=20), nullable=False))
    op.add_column('wushu_teams', sa.Column('pid', sa.Integer(), nullable=False))
    op.add_column('wushu_teams', sa.Column('pname', sa.String(length=20), nullable=False))
    op.add_column('wushu_teams', sa.Column('province', sa.String(length=20), nullable=False))
    op.add_column('wushu_teams', sa.Column('ptelephone', sa.String(length=20), nullable=False))
    op.add_column('wushu_teams', sa.Column('pwx', sa.String(length=30), nullable=False))
    op.add_column('wushu_teams', sa.Column('short_name', sa.String(length=20), nullable=False))
    op.add_column('wushu_teams', sa.Column('state', sa.String(length=20), nullable=False))
    op.drop_column('wushu_teams', 'owner_name')
    op.drop_column('wushu_teams', 'owner_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('wushu_teams', sa.Column('owner_id', mysql.VARCHAR(collation='utf8_bin', length=20), nullable=False))
    op.add_column('wushu_teams', sa.Column('owner_name', mysql.VARCHAR(collation='utf8_bin', length=20), nullable=False))
    op.drop_column('wushu_teams', 'state')
    op.drop_column('wushu_teams', 'short_name')
    op.drop_column('wushu_teams', 'pwx')
    op.drop_column('wushu_teams', 'ptelephone')
    op.drop_column('wushu_teams', 'province')
    op.drop_column('wushu_teams', 'pname')
    op.drop_column('wushu_teams', 'pid')
    op.drop_column('wushu_teams', 'pemail')
    op.drop_column('wushu_teams', 'en_name')
    op.drop_column('wushu_teams', 'detail_address')
    op.drop_column('wushu_teams', 'country')
    op.drop_column('wushu_teams', 'city')
    # ### end Alembic commands ###
