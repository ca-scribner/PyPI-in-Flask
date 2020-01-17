"""add auditing table

Revision ID: 6e1714c55a2b
Revises: f45ade69ae86
Create Date: 2020-01-11 15:55:36.206213

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e1714c55a2b'
down_revision = 'f45ade69ae86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('auditing',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_auditing_created_date'), 'auditing', ['created_date'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_auditing_created_date'), table_name='auditing')
    op.drop_table('auditing')
    # ### end Alembic commands ###