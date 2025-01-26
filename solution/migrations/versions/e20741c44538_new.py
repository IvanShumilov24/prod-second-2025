"""new

Revision ID: e20741c44538
Revises: 
Create Date: 2025-01-24 20:30:10.835946

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e20741c44538'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('business',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_business_id'), 'business', ['id'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('surname', sa.String(length=120), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('avatar_url', sa.String(length=350), nullable=False),
    sa.Column('other', sa.JSON(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_table('promo',
    sa.Column('description', sa.String(length=300), nullable=False),
    sa.Column('image_url', sa.String(length=350), nullable=False),
    sa.Column('target', sa.JSON(), nullable=False),
    sa.Column('max_count', sa.Integer(), nullable=False),
    sa.Column('active_from', sa.Date(), nullable=True),
    sa.Column('active_until', sa.Date(), nullable=True),
    sa.Column('mode', sa.Enum('COMMON', 'UNIQUE', name='mode'), nullable=False),
    sa.Column('promo_common', sa.String(), nullable=False),
    sa.Column('promo_unique', sa.JSON(), nullable=False),
    sa.Column('promo_id', sa.UUID(), nullable=False),
    sa.Column('company_id', sa.UUID(), nullable=False),
    sa.Column('company_name', sa.String(length=50), nullable=False),
    sa.Column('like_count', sa.Integer(), nullable=False),
    sa.Column('used_count', sa.Integer(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['business.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['company_name'], ['business.name'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('promo_id')
    )
    op.create_index(op.f('ix_promo_promo_id'), 'promo', ['promo_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_promo_promo_id'), table_name='promo')
    op.drop_table('promo')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_business_id'), table_name='business')
    op.drop_table('business')
    # ### end Alembic commands ###
