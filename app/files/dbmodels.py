from uuid import UUID
from datetime import datetime

import ormar

from database import database, metadata



class File(ormar.Model):
    """
    Database model for file object
    """
    ormar_config = ormar.OrmarConfig(
        metadata = metadata,
        database = database,
        tablename = "files"
    )

    id: UUID = ormar.UUID(primary_key=True)
    download_id: UUID = ormar.UUID()
    hash: str = ormar.String(max_length=200)
    mime_type: str = ormar.String(max_length=100)
    size: int = ormar.Integer()
    upload_at: datetime = ormar.DateTime(timezone=False)
