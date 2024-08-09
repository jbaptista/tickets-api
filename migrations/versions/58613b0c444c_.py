"""empty message

Revision ID: 58613b0c444c
Revises: 89d70a2075e6
Create Date: 2024-08-08 20:40:59.491009

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '58613b0c444c'
down_revision: Union[str, None] = '89d70a2075e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tickets', sa.Column('category_id', sa.BigInteger().with_variant(sa.INTEGER(), 'sqlite'), nullable=False))
    op.add_column('tickets', sa.Column('subcategory_id', sa.BigInteger().with_variant(sa.INTEGER(), 'sqlite'), nullable=False))
    op.create_foreign_key(None, 'tickets', 'categories', ['category_id'], ['id'])
    op.create_foreign_key(None, 'tickets', 'categories', ['subcategory_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tickets', type_='foreignkey')
    op.drop_constraint(None, 'tickets', type_='foreignkey')
    op.drop_column('tickets', 'subcategory_id')
    op.drop_column('tickets', 'category_id')
    # ### end Alembic commands ###