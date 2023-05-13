"""Create access_token

Revision ID: b04e3f3aa4ac
Revises: 260bbf04d79d
Create Date: 2023-05-05 11:50:47.380039

"""
import fastapi_users_db_sqlalchemy
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b04e3f3aa4ac'
down_revision = '260bbf04d79d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accesstoken',
    sa.Column('token', sa.String(length=43), nullable=False),
    sa.Column('created_at', fastapi_users_db_sqlalchemy.generics.TIMESTAMPAware(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('token')
    )
    op.create_index(op.f('ix_accesstoken_created_at'), 'accesstoken', ['created_at'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_accesstoken_created_at'), table_name='accesstoken')
    op.drop_table('accesstoken')
    # ### end Alembic commands ###