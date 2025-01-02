from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import List

from src.models.base import SQLModel

class Provinces(SQLModel):
    __tablename__ = "province_geography"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(5), nullable=False, unique=True)
    name_th: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    name_en: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    geography_id: Mapped[int] = mapped_column(Integer, ForeignKey("geography.id"), nullable=False)

    # Relationships
    districts: Mapped[List["Districts"]] = relationship("Districts", back_populates="province")
    sub_districts: Mapped[List["SubDistricts"]] = relationship("SubDistricts", back_populates="province")
    geography: Mapped["Geography"] = relationship("Geography", back_populates="province")


    