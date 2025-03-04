from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List

from app.models.base import SQLModel

class RubberType(SQLModel):

    __tablename__ = "RubberType"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name_th: Mapped[str] = mapped_column(String, nullable=False)
    name_en: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)

    # relationship
    rubber_farms: Mapped[List["RubberFarm"]] = relationship("RubberFarm", back_populates="rubber_type")