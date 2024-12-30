from typing import List
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from src.models.base import SQLModel
class SubDistricts(SQLModel):
    __tablename__ = "sub_district_geography"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name_th: Mapped[str] = mapped_column(String(255), nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)
    district_id: Mapped[int] = mapped_column(Integer, ForeignKey("district_geography.id"), nullable=False)
    province_id: Mapped[int] = mapped_column(Integer, ForeignKey("province_geography.id"), nullable=False)

    # Relationships
    district: Mapped["Districts"] = relationship("Districts", back_populates="sub_districts")
    province: Mapped["Provinces"] = relationship("Provinces", back_populates="sub_districts")