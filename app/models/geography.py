from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import List

from app.models.base import SQLModel

class Geography(SQLModel):
    __tablename__ = "Geography"

    code: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name_th: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    name_en: Mapped[str] = mapped_column(String(255), nullable=True, unique=True)

    # Relationships
    provinces: Mapped[List["Province"]] = relationship("Province", back_populates="geography") # type: ignore
