import logging
import pandas as pd

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from importlib import import_module

class FileService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def import_csv_files(self, csv_files_import: list):
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
                    module_path = f"app.models.{model_name.lower()}"
                    model_module = import_module(module_path)
                    model_class = getattr(model_module, model_name)

                    data = pd.read_csv(file_path)
                    records = data.to_dict(orient='records')

                    logging.info(f"Importing {len(records)} records into {model_name} table.")
                    
                    for record in records:
                        obj = model_class(**record)
                        self.session.add(obj)

                except pd.errors.EmptyDataError:
                    logging.error(f"The CSV file {file_path} is invalid or empty.")

                except SQLAlchemyError as db_error:
                    logging.error(f"Database error occurred for {model_name}: {db_error}")

                    await self.session.rollback()
                except Exception as e:

                    logging.error(f"An unexpected error occurred for {model_name}: {e}")
                    await self.session.rollback()
                    
            logging.info(f"Successfully imported {len(records)} records into {model_name} table.")
            await self.session.commit()

        except SQLAlchemyError as e:
            logging.error(f"Transaction failed: {e}")
            await self.session.rollback()