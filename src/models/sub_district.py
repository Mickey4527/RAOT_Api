from src.models.base import SQLModel
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


from typing import List
import uuid
from datetime import datetime


class SubDistricts(SQLModel):
    __tablename__ = "sub_districts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name_th: Mapped[str] = mapped_column(String(255), nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)
    province_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("provinces.id"), nullable=False)
    district_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("districts.id"), nullable=False)

    province: Mapped["Provinces"] = relationship("Provinces", back_populates="sub_districts")
    district: Mapped["Districts"] = relationship("Districts", back_populates="sub_districts")
