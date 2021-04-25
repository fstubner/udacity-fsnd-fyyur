"""Shows table and associated relationships

Revision ID: 784eec396fd2
Revises: a6ddc3434eb2
Create Date: 2021-04-26 00:08:31.312702

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '784eec396fd2'
down_revision = 'a6ddc3434eb2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shows',
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['venue_id'], ['venues.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('venue_id', 'artist_id')
    )
    op.add_column('artists', sa.Column('looking_for_venues', sa.Boolean(), nullable=False))
    op.add_column('artists', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    op.add_column('artists', sa.Column('website_link', sa.String(length=120), nullable=True))
    op.alter_column('artists', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('artists', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('artists', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('artists', 'state',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.add_column('venues', sa.Column('genres', sa.String(length=120), nullable=False))
    op.add_column('venues', sa.Column('looking_for_talent', sa.Boolean(), nullable=False))
    op.add_column('venues', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    op.add_column('venues', sa.Column('website_link', sa.String(length=120), nullable=True))
    op.alter_column('venues', 'address',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('venues', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('venues', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('venues', 'state',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venues', 'state',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('venues', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('venues', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('venues', 'address',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.drop_column('venues', 'website_link')
    op.drop_column('venues', 'seeking_description')
    op.drop_column('venues', 'looking_for_talent')
    op.drop_column('venues', 'genres')
    op.alter_column('artists', 'state',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('artists', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('artists', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('artists', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.drop_column('artists', 'website_link')
    op.drop_column('artists', 'seeking_description')
    op.drop_column('artists', 'looking_for_venues')
    op.drop_table('shows')
    # ### end Alembic commands ###
