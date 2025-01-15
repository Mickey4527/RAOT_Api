from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List

from app.models.base import SQLModel

class SoilType(SQLModel):

    __tablename__ = "SoilType"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)

    # Relationships
    soil_geographies: Mapped[List["SoilGeography"]] = relationship("SoilGeography", back_populates="soil_type")
