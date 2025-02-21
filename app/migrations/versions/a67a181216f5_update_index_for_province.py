"""update index for province

Revision ID: a67a181216f5
Revises: 
Create Date: 2025-02-08 05:24:49.292445

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a67a181216f5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Geography',
    sa.Column('code', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name_th', sa.String(length=255), nullable=False),
    sa.Column('name_en', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('code'),
    sa.UniqueConstraint('name_en'),
    sa.UniqueConstraint('name_th')
    )
    op.create_table('SoilType',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Province',
    sa.Column('code', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name_th', sa.String(length=255), nullable=False),
    sa.Column('name_en', sa.String(length=255), nullable=True),
    sa.Column('geography_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['geography_id'], ['Geography.code'], ),
    sa.PrimaryKeyConstraint('code'),
    sa.UniqueConstraint('name_en'),
    sa.UniqueConstraint('name_th')
    )
    op.create_index('idx_province_name_en', 'Province', ['name_en'], unique=False)
    op.create_index('idx_province_name_th', 'Province', ['name_th'], unique=False)
    op.create_table('District',
    sa.Column('code', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name_th', sa.String(length=255), nullable=False),
    sa.Column('name_en', sa.String(length=255), nullable=True),
    sa.Column('province_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['province_id'], ['Province.code'], ),
    sa.PrimaryKeyConstraint('code')
    )
    op.create_index('idx_district_name_en', 'District', ['name_en'], unique=False)
    op.create_index('idx_district_name_th', 'District', ['name_th'], unique=False)
    op.create_table('WeatherGeography',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('province_id', sa.Integer(), nullable=False),
    sa.Column('rainfall_mm', sa.Float(), nullable=True),
    sa.Column('average_temperature', sa.Float(), nullable=True),
    sa.Column('average_humidity', sa.Float(), nullable=True),
    sa.Column('rainy_day_count', sa.Integer(), nullable=True),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['province_id'], ['Province.code'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('SubDistrict',
    sa.Column('code', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name_th', sa.String(length=255), nullable=False),
    sa.Column('name_en', sa.String(length=255), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('zip_code', sa.Integer(), nullable=False),
    sa.Column('district_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['district_id'], ['District.code'], ),
    sa.PrimaryKeyConstraint('code')
    )
    op.create_table('SoilGeography',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('subdistrict_id', sa.Integer(), nullable=False),
    sa.Column('soil_type_id', sa.Integer(), nullable=False),
    sa.Column('fertility_top', sa.Float(), nullable=True),
    sa.Column('ph_top', sa.Float(), nullable=True),
    sa.Column('ph_low', sa.Float(), nullable=True),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['soil_type_id'], ['SoilType.id'], ),
    sa.ForeignKeyConstraint(['subdistrict_id'], ['SubDistrict.code'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('SoilGeography')
    op.drop_table('SubDistrict')
    op.drop_table('WeatherGeography')
    op.drop_index('idx_district_name_th', table_name='District')
    op.drop_index('idx_district_name_en', table_name='District')
    op.drop_table('District')
    op.drop_index('idx_province_name_th', table_name='Province')
    op.drop_index('idx_province_name_en', table_name='Province')
    op.drop_table('Province')
    op.drop_table('SoilType')
    op.drop_table('Geography')
    # ### end Alembic commands ###
