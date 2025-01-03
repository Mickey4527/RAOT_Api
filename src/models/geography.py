from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import List

from src.models.base import SQLModel

class Geography(SQLModel):
    __tablename__ = "geography"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name_th: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    name_en: Mapped[str] = mapped_column(String(255), nullable=True, unique=True)

    # Relationships
    province: Mapped[List["Province"]] = relationship("Province", back_populates="geography")

    