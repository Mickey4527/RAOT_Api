from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from importlib import import_module

class DataService:

    @staticmethod
    async def import_csv_files(session: AsyncSession, csv_files_import: list):
        """
        Import multiple CSV files into their respective database tables.

        Args:
            session (AsyncSession): SQLAlchemy AsyncSession instance.
            csv_files_import (list): List of dictionaries with 'model' and 'file' keys.

        Returns:
            None
        """
        
        try:
            for entry in csv_files_import:
                model_name = entry['model']
                file_path = entry['file']

                try:
                    module_path = f"src.models.{model_name.lower()}"
                    model_module = import_module(module_path)
                    model_class = getattr(model_module, model_name)

                    data = pd.read_csv(file_path)
                    records = data.to_dict(orient='records')

                    logger.info(f"Importing data from {file_path} into {model_name} table...")

                    for record in records:
                        obj = model_class(**record)
                        session.add(obj)

                    logger.success(f"Successfully imported {len(records)} records into {model_name} table.")
                    await session.commit()

                except FileNotFoundError:
                    logger.error(f"CSV file not found: {file_path}")
                except SQLAlchemyError as db_error:
                    logger.error(f"Database error occurred for {model_name}: {db_error}")
                    await session.rollback()
                except Exception as e:
                    logger.error(f"An unexpected error occurred for {model_name}: {e}")
                    await session.rollback()

        except SQLAlchemyError as e:
            logger.error(f"Transaction failed: {e}")
            await session.rollback()