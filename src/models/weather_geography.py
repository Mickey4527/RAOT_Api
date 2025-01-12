from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List

from src.models.base import SQLModel


class WeatherGeography(SQLModel):

    __tablename__ = "WeatherGeography"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    province_id: Mapped[int] = mapped_column(Integer, ForeignKey("Province.code"), nullable=False)
    rainfall_mm: Mapped[float] = mapped_column(Float, nullable=True)
    average_temperature: Mapped[float] = mapped_column(Float, nullable=True)
    average_humidity: Mapped[float] = mapped_column(Float, nullable=True)
    rainy_day_count: Mapped[int] = mapped_column(Integer, nullable=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)

    rubber_farms: Mapped["RubberFarm"] = relationship("RubberFarm", back_populates="weather")
    province: Mapped[List["Province"]] = relationship("Province", back_populates="weather_geographies")