import logging
import pandas as pd

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from importlib import import_module

class FileService:

    def __init__(self, session: AsyncSession):
        self.session = session

    import logging
import pandas as pd
from importlib import import_module
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

class FileService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def import_csv_files(self, csv_files_import: list):
        """
        Import multiple CSV files into their respective database tables.

        Args:
            csv_files_import (list): List of dictionaries with 'model' and 'file' keys.

        Returns:
            None
        """
        total_imported_records = 0  # นับจำนวน record ที่นำเข้าได้

        try:
            for entry in csv_files_import:
                model_name = entry['model']
                file_path = entry['file']

                try:
                    # นำเข้า Model แบบไดนามิก
                    module_path = f"app.models.{model_name.lower()}"
                    model_module = import_module(module_path)
                    model_class = getattr(model_module, model_name)

                    # อ่านไฟล์ CSV
                    data = pd.read_csv(file_path, encoding='utf-8')
                    records = data.to_dict(orient='records')

                    if not records:
                        logging.warning(f"CSV file {file_path} is empty. Skipping.")
                        continue

                    logging.info(f"Importing {len(records)} records into {model_name} table.")

                    # ใช้ bulk_insert_mappings เพื่อเพิ่มประสิทธิภาพ
                    await self.session.execute(model_class.__table__.insert(), records)

                    total_imported_records += len(records)

                except pd.errors.EmptyDataError:
                    logging.error(f"The CSV file {file_path} is empty or invalid. Skipping.")

                except SQLAlchemyError as db_error:
                    logging.error(f"Database error occurred for {model_name}: {db_error}")
                    await self.session.rollback()

                except Exception as e:
                    logging.error(f"Unexpected error for {model_name}: {e}")
                    await self.session.rollback()

            # ถ้าไม่มีข้อผิดพลาดร้ายแรง ให้ commit
            if total_imported_records > 0:
                await self.session.commit()
                logging.info(f"Successfully imported {total_imported_records} records in total.")
            else:
                logging.warning("No valid records imported. Nothing to commit.")

        except SQLAlchemyError as e:
            logging.error(f"Transaction failed: {e}")
            await self.session.rollback()
