from sqlalchemy import Integer, Float, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List

from app.models.base import SQLModel

class SoilGeography(SQLModel):

    __tablename__ = "SoilGeography"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subdistrict_id: Mapped[int] = mapped_column(Integer, ForeignKey("SubDistrict.code"), nullable=False)
    soil_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("SoilType.id"), nullable=False)
    fertility_top: Mapped[float] = mapped_column(Float, nullable=True)
    ph_top: Mapped[float] = mapped_column(Float, nullable=True)
    ph_low: Mapped[float] = mapped_column(Float, nullable=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    rubber_farms: Mapped[List["RubberFarm"]] = relationship("RubberFarm", back_populates="soil")
    sub_district: Mapped["SubDistrict"] = relationship("SubDistrict", back_populates="soil_geographies")
    soil_type: Mapped["SoilType"] = relationship("SoilType", back_populates="soil_geographies")
