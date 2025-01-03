from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import List

from src.models.base import SQLModel

class Province(SQLModel):
    __tablename__ = "province_geography"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    name_th: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    name_en: Mapped[str] = mapped_column(String(255), nullable=True, unique=True)
    geography_id: Mapped[int] = mapped_column(Integer, ForeignKey("geography.id"), nullable=False)

    # Relationships
    district: Mapped[List["District"]] = relationship("District", back_populates="province")
    sub_district: Mapped[List["SubDistrict"]] = relationship("SubDistrict", back_populates="province")
    geography: Mapped["Geography"] = relationship("Geography", back_populates="province")
    