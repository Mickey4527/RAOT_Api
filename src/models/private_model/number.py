from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import List

from src.models.base import SQLModel

class NumberTest(SQLModel):

    __tablename__ = "NumberTest"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    price: Mapped[int] = mapped_column(Integer, nullable=False)