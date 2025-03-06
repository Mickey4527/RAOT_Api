import logging
from sqlalchemy import String, cast, desc, distinct
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, CompileError, IntegrityError
from sqlalchemy.orm import joinedload

from app.models import Province, District
from app.models.rubberfarm import RubberFarm
from app.models.subdistrict import SubDistrict
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
    
    def _filter_districts_with_rubber_farms(self, province):
        """Filter districts and subdistricts that have rubber farms"""
        
        filtered_districts = []
        for district in province.districts:
            filtered_subdistricts = [
                sub for sub in district.sub_districts
                if any(farm.subdistrict_id == sub.code for farm in sub.rubber_farms)
            ]
            if filtered_subdistricts:
                district.sub_districts = filtered_subdistricts
                filtered_districts.append(district)
        return filtered_districts

    async def get_provinces_with_rubber_farms(self, query: QueryGeoSchema):
        """
        Get provinces with rubber farms and their districts/subdistricts if detailed view is requested
        
        Args:
            query: QueryGeoSchema - Query parameters for filtering and language selection
        
        Returns:
            List[Province]: List of provinces with rubber farms and optional district details
        """
        try:
            # First, get just the provinces that have rubber farms without loading all related data
            # This uses a subquery approach instead of eager loading everything
            province_ids_stmt = (
                select(distinct(Province.code))
                .join(District, District.province_id == Province.code)
                .join(SubDistrict, SubDistrict.district_id == District.code)
                .join(RubberFarm, RubberFarm.subdistrict_id == SubDistrict.code)
            )
            
            if query.code:
                province_ids_stmt = province_ids_stmt.where(Province.code == query.code)
                
            # Execute just to get province IDs - much more efficient
            province_ids_result = await self.session.execute(province_ids_stmt)
            province_ids = [row[0] for row in province_ids_result.all()]
            
            if not province_ids:
                raise ResourceNotFoundException(message=self.t.get("NotFound"))
            
            # Now get the actual provinces
            provinces_stmt = (
                select(Province)
                .where(Province.code.in_(province_ids))
            )
            
            # Only load detailed district data if requested
            if query.detail:
                # Use selective loading to avoid loading all farms
                provinces_stmt = provinces_stmt.options(
                    joinedload(Province.districts)
                    .joinedload(District.sub_districts)
                )
            
            provinces_result = await self.session.execute(provinces_stmt)
            provinces = provinces_result.unique().scalars().all()
            
            # If detail is requested, we need to filter districts/subdistricts with rubber farms
            if query.detail:
                for province in provinces:
                    # For each province, find districts with rubber farms
                    district_ids_stmt = (
                        select(distinct(District.code))
                        .join(SubDistrict, SubDistrict.district_id == District.code)
                        .join(RubberFarm, RubberFarm.subdistrict_id == SubDistrict.code)
                        .where(District.province_id == province.code)
                    )
                    
                    district_ids_result = await self.session.execute(district_ids_stmt)
                    district_ids = [row[0] for row in district_ids_result.all()]
                    
                    # Filter districts that have rubber farms
                    province.districts = [d for d in province.districts if d.code in district_ids]
                    
                    # For each district, find subdistricts with rubber farms
                    for district in province.districts:
                        subdistrict_ids_stmt = (
                            select(distinct(SubDistrict.code))
                            .join(RubberFarm, RubberFarm.subdistrict_id == SubDistrict.code)
                            .where(SubDistrict.district_id == district.code)
                        )
                        
                        subdistrict_ids_result = await self.session.execute(subdistrict_ids_stmt)
                        subdistrict_ids = [row[0] for row in subdistrict_ids_result.all()]
                        
                        # Filter subdistricts that have rubber farms
                        district.sub_districts = [sd for sd in district.sub_districts 
                                                 if sd.code in subdistrict_ids]
            
            # Apply names according to language selection
            provinces = self._apply_names(provinces, query)
            if query.detail:
                provinces = self._apply_district_details(provinces, query)
            
            return provinces

        except ResourceNotFoundException as e:
            logger.warning("No provinces with rubber farms found")
            raise e
        except SQLAlchemyError as e:
            logger.error(f"Database error: {str(e)}", exc_info=True)
            raise SQLProcessException(
                event=e,
                message=self.t.get("SQLServerQueryError")
            )
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            raise ServerProcessException(
                message=self.t.get("InternalServerError")
            )

