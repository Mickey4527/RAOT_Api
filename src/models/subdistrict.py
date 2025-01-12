from typing import List
from sqlalchemy import Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from src.models.base import SQLModel

class SubDistrict(SQLModel):

    __tablename__ = "SubDistrict"

    code: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name_th: Mapped[str] = mapped_column(String(255), nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    zip_code: Mapped[int] = mapped_column(Integer, nullable=False)
    district_id: Mapped[int] = mapped_column(Integer, ForeignKey("District.code"), nullable=False)

    # Relationships
    districts: Mapped["District"] = relationship("District", back_populates="sub_districts")
    soil_geographies: Mapped[List["SoilGeography"]] = relationship("SoilGeography", back_populates="sub_district")
    rubber_farms: Mapped[List["RubberFarm"]] = relationship("RubberFarm", back_populates="sub_district")