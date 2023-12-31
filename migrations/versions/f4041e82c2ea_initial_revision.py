"""Initial revision

Revision ID: f4041e82c2ea
Revises: 
Create Date: 2023-09-03 17:35:15.393103

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4041e82c2ea'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    op.create_table(
        'users',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_set_id', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('is_superuser', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('published_landmarks', sa.ARRAY(sa.String()), nullable=True),
        sa.Column('favorite_landmarks', sa.ARRAY(sa.String()), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    
        
    op.create_table('landmarks',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('rating', sa.Float(), nullable=False),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('coordinates',sa.ARRAY(sa.Float()), nullable=False),
        sa.Column('categories', sa.ARRAY(sa.String()), nullable=False),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('time', sa.String(), nullable=False),
        sa.Column('img', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_landmarks_id'), 'landmarks', ['id'], unique=False)
    
    op.create_table(
        'published_landmarks',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('landmark_id', sa.String(), sa.ForeignKey('landmarks.id'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'favorite_landmarks',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('landmark_id', sa.String(), sa.ForeignKey('landmarks.id'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    
    op.create_table(
        'refresh_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('refresh_token', sa.String(), nullable=False),
        sa.Column('expires_at', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('user_id', sa.String(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('published_landmarks')
    op.drop_table('favorite_landmarks')
    op.drop_table('refresh_tokens')
    op.drop_table('users')
    op.drop_index(op.f('ix_landmarks_id'), table_name='landmarks')
    op.drop_table('landmarks')

    # ### end Alembic commands ###
