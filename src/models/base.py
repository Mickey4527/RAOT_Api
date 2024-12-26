from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

class Base(AsyncAttrs, DeclarativeBase):
    pass

class SQLModel(Base):

    __abstract__ = True
    
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())