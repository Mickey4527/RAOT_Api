from sqlalchemy import Index, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import List

from app.models.base import SQLModel

class District(SQLModel):
    __tablename__ = "District"

    code: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name_th: Mapped[str] = mapped_column(String(255), nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), nullable=True)
    province_id: Mapped[int] = mapped_column(Integer, ForeignKey("Province.code"), nullable=False)

     # Indexes
    __table_args__ = (
        Index("idx_district_name_th", "name_th"),
        Index("idx_district_name_en", "name_en"),
    )

    # Relationships
    province: Mapped["Province"] = relationship("Province", back_populates="districts")
    sub_districts: Mapped[List["SubDistrict"]] = relationship("SubDistrict", back_populates="districts")
