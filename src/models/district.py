from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import List

from src.models.base import SQLModel

class District(SQLModel):
    __tablename__ = "district_geography"

    code: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name_th: Mapped[str] = mapped_column(String(255), nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), nullable=True)
    province_id: Mapped[int] = mapped_column(Integer, ForeignKey("province_geography.id"), nullable=False)

    # Relationships
    province: Mapped["Province"] = relationship("Province", back_populates="districts")
    sub_districts: Mapped[List["SubDistrict"]] = relationship("SubDistrict", back_populates="districts")