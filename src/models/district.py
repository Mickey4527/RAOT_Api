from src.models.base import SQLModel
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from typing import List
import uuid

class Districts(SQLModel):
    __tablename__ = "districts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name_th: Mapped[str] = mapped_column(String(255), nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)
    province_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("provinces.id"), nullable=False)

    province: Mapped["Provinces"] = relationship("Provinces", back_populates="districts")
    sub_districts: Mapped[List["SubDistricts"]] = relationship("SubDistricts", back_populates="district")