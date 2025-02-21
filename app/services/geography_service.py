import logging
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.models import Geography
from app.schemas import BaseCreateSchema
from app.utilities.app_exceptions import SQLProcessException, ServerProcessException

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class GeographyService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_geographys(self):
        """
        Get all geographies\n
        ดึงข้อมูลภูมิศาสตร์ทั้งหมด\n
        """

        try:
            stmp = select(Geography)
            result = await self.session.execute(stmp)
            geographies = result.scalars().all()

            return geographies
        
        except SQLAlchemyError as e:
            logger.error("SQLAlchemy error: %s", e)
            raise SQLProcessException(
                event=e,
                message="เกิดข้อผิดพลาดในการดึงข้อมูลผู้ใช้",
            )
        
        except Exception as e:
            logger.error("Unknown error: %s", e)
            raise ServerProcessException(message="เกิดข้อผิดพลาดที่ไม่รู้จัก")
    
    async def get_geography_by_id(self, geography_id: str):
        """
        Get geography by id\n
        ดึงข้อมูลภูมิศาสตร์โดยใช้ ID\n
        """

        try:
            stmp = select(Geography).where(Geography.code == geography_id)
            result = await self.session.execute(stmp)
            geography = result.scalars().first()

            return geography
        
        except SQLAlchemyError as e:
            logger.error("SQLAlchemy error: %s", e)
            raise SQLProcessException(
                event=e,
                message="เกิดข้อผิดพลาดในการดึงข้อมูลผู้ใช้",
            )
        
        except Exception as e:
            logger.error("Unknown error: %s", e)
            raise ServerProcessException(message="เกิดข้อผิดพลาดที่ไม่รู้จัก")
    
    async def create_geography(self, geography: BaseCreateSchema):
        """
        Create new geography\n
        สร้างข้อมูลภูมิศาสตร์ใหม่\n
        :param geography: BaseGeoSchema\n
        """

        try:
            new_geography = Geography(
                name_th=geography.name_th,
                name_en=geography.name_en
            )

            self.session.add(new_geography)
            await self.session.commit()
            self.session.refresh(new_geography)

            return new_geography
        
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error("SQLAlchemy error: %s", e)
            raise SQLProcessException(
                event=e,
                message="เกิดข้อผิดพลาดในการดึงข้อมูลผู้ใช้",
            )
        
        except Exception as e:
            await self.session.rollback()
            logger.error("Unknown error: %s", e)
            raise ServerProcessException(message="เกิดข้อผิดพลาดที่ไม่รู้จัก")
            
    
    def update_geography(self, geography_id: str, geography: BaseCreateSchema):

        try:
            stmp = select(Geography).where(Geography.id == geography_id)
            result = self.session.execute(stmp)
            current_geography = result.scalars().first()

            current_geography.name_th = geography.name_th
            current_geography.name_en = geography.name_en

            self.session.commit()
            self.session.refresh(current_geography)

            return current_geography
        
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error("SQLAlchemy error: %s", e)
            raise SQLProcessException(
                event=e,
                message="เกิดข้อผิดพลาดในการดึงข้อมูลผู้ใช้",
            )
        
        except Exception as e:
            self.session.rollback()
            logger.error("Unknown error: %s", e)
            raise ServerProcessException(message="เกิดข้อผิดพลาดที่ไม่รู้จัก")
    
    def delete_geography(self, geography_id: str):
        """
        Delete geography by id\n
        ลบข้อมูลภูมิศาสตร์โดยใช้ ID\n
        
        """
        try:
            stmp = select(Geography).where(Geography.id == geography_id)
            result = self.session.execute(stmp)
            current_geography = result.scalars().first()

            self.session.delete(current_geography)
            self.session.commit()
            self.session.refresh(current_geography)

            return current_geography
        
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error("SQLAlchemy error: %s", e)
            raise SQLProcessException(
                event=e,
                message="เกิดข้อผิดพลาดในการดึงข้อมูลผู้ใช้",
            )
        
        except Exception as e:
            self.session.rollback()
            logger.error("Unknown error: %s", e)
            raise ServerProcessException(message="เกิดข้อผิดพลาดที่ไม่รู้จัก")
