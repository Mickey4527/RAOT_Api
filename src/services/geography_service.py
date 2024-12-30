from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from src.models import Geography

class GeographyService:
    @staticmethod
    def get_geography(session: Session):
        stmp = select(Geography)
        result = session.execute(stmp)
        geographies = result.scalars().all()

        return geographies
    
    @staticmethod
    def get_geography_by_id(session: Session, geography_id: str):
        stmp = select(Geography).where(Geography.id == geography_id)
        result = session.execute(stmp)
        geography = result.scalars().first()

        return geography
    
    @staticmethod
    def create_geography(session: Session, geography):
        new_geography = Geography(
            name_th=geography.name_th,
            name_en=geography.name_en
        )

        session.add(new_geography)
        session.commit()
        session.refresh(new_geography)

        return new_geography
    
    @staticmethod
    def update_geography(session: Session, geography_id: str, geography):
        stmp = select(Geography).where(Geography.id == geography_id)
        result = session.execute(stmp)
        current_geography = result.scalars().first()

        current_geography.name_th = geography.name_th
        current_geography.name_en = geography.name_en

        session.commit()
        session.refresh(current_geography)

        return current_geography
    
    @staticmethod
    def delete_geography(session: Session, geography_id: str):
        stmp = select(Geography).where(Geography.id == geography_id)
        result = session.execute(stmp)
        current_geography = result.scalars().first()

        session.delete(current_geography)
        session.commit()
        session.refresh(current_geography)

        return current_geography
    
    # @staticmethod
    # def get_provinces_by_geography(session: Session, geography_id: str):
    #     stmp = select(Geography).where(Geography.id == geography_id)
    #     result = session.execute(stmp)
    #     geography = result.scalars().first()

    #     return geography.province