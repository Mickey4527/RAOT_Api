from typing import Optional
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.models.base import SQLModel

class RubberFarm(SQLModel):
    __tablename__ = "RubberFarm"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    soil_id: Mapped[int] = mapped_column(Integer, ForeignKey("SoilGeography.id"), nullable=False)
    weather_id: Mapped[int] = mapped_column(Integer, ForeignKey("WeatherGeography.id"), nullable=False)
    subdistrict_id: Mapped[int] = mapped_column(Integer, ForeignKey("SubDistrict.code"), nullable=False)
    rubber_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("RubberType.id"), nullable=False)
    rubber_area: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    rubber_tree_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    rubber_tree_age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    dry_rubber_content: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Relationships
    soil: Mapped["SoilGeography"] = relationship("SoilGeography", back_populates="rubber_farms")
    weather: Mapped["WeatherGeography"] = relationship("WeatherGeography", back_populates="rubber_farms")
    sub_district: Mapped["SubDistrict"] = relationship("SubDistrict", back_populates="rubber_farms")
    rubber_type: Mapped["RubberType"] = relationship("RubberType", back_populates="rubber_farms")
