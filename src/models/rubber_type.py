from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List

from src.models.base import SQLModel


class RubberType(SQLModel):

    __tablename__ = "RubberType"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)

    # relationship
    rubber_farms: Mapped[List["RubberFarm"]] = relationship("RubberFarm", back_populates="rubber_type")
