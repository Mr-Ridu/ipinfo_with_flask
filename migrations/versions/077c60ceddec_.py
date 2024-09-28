"""empty message

Revision ID: 077c60ceddec
Revises: 
Create Date: 2024-09-28 01:01:03.151516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '077c60ceddec'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('visitor_ip',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ip_address', sa.String(length=100), nullable=False),
    sa.Column('visit_time', sa.DateTime(), nullable=True),
    sa.Column('visit_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('ip_address')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('visitor_ip')
    # ### end Alembic commands ###