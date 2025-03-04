import logging
from sqlalchemy import String, cast, desc
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, CompileError, IntegrityError
from sqlalchemy.orm import joinedload

from app.models import Province, District
from app.schemas import QueryGeoSchema, ProvinceCreateSchema
from app.utilities.app_exceptions import DuplicateResourceException, ResourceNotFoundException, SQLProcessException, ServerProcessException
from app.I18n.load_laguage import get_lang_content

logger = logging.getLogger(__name__)
class ProvinceService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.t = get_lang_content().get("ErrorMessage")


    async def get_provinces(self, query: QueryGeoSchema) -> list:
        """
            เรียกข้อมูลจังหวัดจากฐานข้อมูลตามเงื่อนไขที่กำหนด \n
            Retrieve provinces from the database based on the query parameters.

            #### Parameters
                session: AsyncSession => The database session object.
                query: QueryGeographySchema => The query parameters.

            #### Returns
                List[Province] => List of Province instances.

        """

        try:

            stmp = select(Province)
            stmp = self._apply_filters(stmp=stmp, query=query)
            result = await self.session.execute(stmp)

            provinces = result.unique().scalars().all()
            provinces = self._apply_names(provinces, query)
                        
            if query.detail:
                provinces = self._apply_district_details(provinces, query)

            return provinces
        
        except SQLAlchemyError as e:
            raise SQLProcessException(
                event=e,
                message=self.t.get("SQLServerQueryError"),
            )
        
        except Exception as e:
            raise ServerProcessException(message=self.t.get("InternalServerError"))
        
        
        
    async def create_province(self, province: ProvinceCreateSchema):
        """
            สร้างข้อมูลจังหวัดใหม่ \n
            Create a new province in the database.

        """

        try:

            existing_province = await self._get_province_by_code(province.code)

            if existing_province:
                return DuplicateResourceException(message=self.t.get("Conflict"))
            
            new_province = self._populate_sub_district_fields(Province(), province)
            self.session.add(new_province)
            await self.session.commit()
            self.session.refresh(new_province)

            return new_province
        
        except DuplicateResourceException as e:
            await self.session.rollback()
            raise e
        
        except SQLAlchemyError as e:
            await self.session.rollback()

            raise SQLProcessException(
                event=e,
                message=self.t.get("SQLServerQueryError"),
            )
        
        except Exception as e:
            await self.session.rollback()
            raise ServerProcessException(message=self.t.get("InternalServerError"))
        


    async def update_province(self, province: ProvinceCreateSchema, code: int):
        """
            อัพเดทข้อมูลจังหวัด \n
            Update province data.
        """

        try:
            existing_province = await self._get_province_by_code(code)

            if not existing_province:
                raise ResourceNotFoundException(message=self.t.get("NotFound"))
            
            self._populate_sub_district_fields(existing_province, province)
            await self.session.commit()
            await self.session.refresh(existing_province)

            return existing_province
        
        except ResourceNotFoundException as e:
            self.session.rollback()
            raise e
        
        except SQLAlchemyError as e:

            raise SQLProcessException(
                event=e,
                message=self.t.get("SQLServerQueryError"),
            )
        
        except Exception as e:
            await self.session.rollback()
            raise ServerProcessException(message=self.t.get("InternalServerError"))
        

    async def delete_province(self, code: int):
        """
            ลบข้อมูลจังหวัด \n
            Delete province data.
        """

        try:
            existing_province = await self._get_province_by_code(code)

            if not existing_province:
                raise ResourceNotFoundException(message=self.t.get("NotFound"))

            self.session.delete(existing_province)
            await self.session.commit()

            return True
        
        except ResourceNotFoundException as e:
            await self.session.rollback()
            logger.warning(f"Province with code {code} not found.")
            raise e
        
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"SQL error while deleting province {code}: {e}")
            raise SQLProcessException(
                event=e,
                message=self.t.get("SQLServerQueryError"),
            )
        
        except Exception as e:
            await self.session.rollback()
            logger.critical(f"Unexpected error in delete_province: {e}", exc_info=True)
            raise ServerProcessException(message=self.t.get("InternalServerError"))
        

    def _apply_filters(self, stmp, query):

        """
        Apply query filters to the SQLAlchemy statement.\n
        นำเงื่อนไขการค้นหามาใช้กับคำสั่ง SQLAlchemy

        """

        if query.code:
            stmp = stmp.where(Province.code == query.code)

        if query.detail:
            stmp = stmp.options(
                joinedload(Province.districts).joinedload(District.sub_districts)
            )

        if query.limit:
            stmp = stmp.limit(query.limit)

        if query.offset:
            stmp = stmp.offset(query.offset)

        if query.search:
            stmp = stmp.filter(
                Province.name_th.ilike(f"%{query.search}%") |
                Province.name_en.ilike(f"%{query.search}%") |
                cast(Province.code, String).ilike(f"%{query.search}%")
            )

        if query.order_by_desc:
            stmp = stmp.order_by(desc(query.order_by))

        return stmp


    def _apply_names(self, provinces, query):
        """
        Apply name translations to provinces based on query type.\n
        นำข้อมูลชื่อจังหวัดมาแปลเป็นภาษาที่ต้องการ
        """
        for province in provinces:
            province.name = province.name_en if query.type == "en" else province.name_th
        return provinces


    def _apply_district_details(self, provinces, query):
        """
        Apply name translations to districts and sub-districts.\n
        นำข้อมูลชื่ออำเภอและตำบลมาแปลเป็นภาษาที่ต้องการ
        """
        for province in provinces:
            for district in province.districts:
                district.name = district.name_en if query.type == "en" else district.name_th
                for sub_district in district.sub_districts:
                    sub_district.name = sub_district.name_en if query.type == "en" else sub_district.name_th
        return provinces


    async def _get_province_by_code(self, code: int):
        
        stmp = select(Province).where(Province.code == code)
        result = await self.session.execute(stmp)
        result = result.scalars().first()
        
        return result
    
    def _populate_sub_district_fields(
            self, province: Province, data: ProvinceCreateSchema
        ) -> Province:
        
        """
        Populate fields of a Province instance with data from ProvinceSchema.\n
        นำข้อมูลจังหวัดจาก ProvinceSchema มาเติมใน Province instance
        """
        province.name_th = data.name_th
        province.name_en = data.name_en
        province.code = data.code
        province.geography_id = data.geography_id

        return province
