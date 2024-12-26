from src.models.base import SQLModel
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from typing import List
import uuid


class Provinces(SQLModel):
    __tablename__ = "provinces"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name_th: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    name_en: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    # Relationships
    districts: Mapped[List["Districts"]] = relationship("Districts", back_populates="province")
    sub_districts: Mapped[List["SubDistricts"]] = relationship("SubDistricts", back_populates="province")
    