from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, func

from src.models import NumberTest
from src.schemas import TestSchema

class PrivateService:

    @staticmethod
    async def get_private(session: AsyncSession):
        stmp = select(NumberTest)
        result = await session.execute(stmp)
        privates = result.scalars().all()

        return privates
    
    @staticmethod
    async def add_private(session: AsyncSession):

        for i in range(1, 1000000):
            private = NumberTest(
                price=i
            )
            
            session.add(private)
            await session.commit()
            session.refresh(private)

        return True
    
    """
        Avg test function
    """
    @staticmethod
    async def avg_test(session: AsyncSession):
        stmt = select(func.round(func.avg(NumberTest.price), 2))
        result = await session.execute(stmt)

        return result.scalar_one()
    
    @staticmethod
    async def count_test(session: AsyncSession):
        stmt = select(func.count(NumberTest.price))
        result = await session.execute(stmt)

        return result.scalar_one()
