import uuid
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import SQLModel

class Module(SQLModel):
    """
    ตารางเก็บข้อมูลโมดูล \n
    Table for storing module data

    #### Description
        ตารางเก็บข้อมูลโมดูลที่ใช้ในการกำหนดสิทธิ์การใช้งาน \n
        A table for storing module data used to define access rights

    """
    __tablename__ = "Module"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    role_permissions = relationship("RolePermission", back_populates="module")
    permissions = relationship("Permission", back_populates="module")  # type: ignore

