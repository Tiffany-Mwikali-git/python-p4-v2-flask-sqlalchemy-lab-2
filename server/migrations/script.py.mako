"""make item fields nullable"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = 'xxxxxx'   # auto-generated
down_revision = 'previous_revision'  # auto-generated
branch_labels = None
depends_on = None


def upgrade():
    # Alter columns to allow NULL
    with op.batch_alter_table('items') as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.String(),
               nullable=True)
        batch_op.alter_column('price',
               existing_type=sa.Float(),
               nullable=True)


def downgrade():
    # Revert to NOT NULL (old state)
    with op.batch_alter_table('items') as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.String(),
               nullable=False)
        batch_op.alter_column('price',
               existing_type=sa.Float(),
               nullable=False)
