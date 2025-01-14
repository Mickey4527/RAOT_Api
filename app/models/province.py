from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import List

from app.models.base import SQLModel

class Province(SQLModel):
    __tablename__ = "Province"

    code: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name_th: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    name_en: Mapped[str] = mapped_column(String(255), nullable=True, unique=True)
    geography_id: Mapped[int] = mapped_column(Integer, ForeignKey("Geography.code"), nullable=False)

    # Relationships
    geography: Mapped["Geography"] = relationship("Geography", back_populates="provinces") # type: ignore
    districts: Mapped[List["District"]] = relationship("District", back_populates="province") # type: ignore
    weather_geographies: Mapped["WeatherGeography"] = relationship("WeatherGeography", back_populates="province") # type: ignore
