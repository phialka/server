from typing import Optional, Union, List
from uuid import UUID
from datetime import datetime

import databases
import sqlalchemy
import ormar
import pydantic

try:
    import config
except: 
    import app.config as config


#default value
_database_url = config.DATABASE_URL



class BaseMeta(ormar.ModelMeta):
    metadata = sqlalchemy.MetaData()
    database = databases.Database(_database_url)
    
    @classmethod
    def change_db(cls, db_url: str) -> None:
        """
        Use to change database
        Don't use it without adapter 
        """
        cls.database = databases.Database(db_url)



class Files(ormar.Model):
    class Meta(BaseMeta):
        tablename = "files"

    id: UUID = ormar.UUID(primary_key=True)
    download_id: UUID = ormar.UUID()
    hash: str = ormar.String(max_length=200)
    mime_type: str = ormar.String(max_length=100)
    size: int = ormar.Integer()
    upload_at: datetime = ormar.DateTime(timezone=False)



async def connect_database(database_url: Optional[str] = None):
    if database_url:
        BaseMeta.change_db(database_url)

    engine = sqlalchemy.create_engine(database_url or _database_url)
    BaseMeta.metadata.create_all(engine)

    database_ = BaseMeta.database
    if not database_.is_connected:
        await database_.connect()



async def disconnect_database():
    if BaseMeta.database.is_connected:
        await BaseMeta.database.disconnect()


