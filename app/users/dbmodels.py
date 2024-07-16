from typing import Optional
from uuid import UUID
from datetime import date

import ormar

from database import database, metadata
from files.dbmodels import File



class User(ormar.Model):
    """
    Database model for user
    """
    ormar_config = ormar.OrmarConfig(
        metadata = metadata,
        database = database,
        tablename = "users"
    )

    id: UUID = ormar.UUID(primary_key=True)
    name: str = ormar.String(max_length=40)
    description: Optional[str] = ormar.String(max_length=100, nullable=True)
    tag: str = ormar.String(max_length=30)
    birthdate: Optional[date] = ormar.Date(nullable=True)
    photo: File = ormar.ForeignKey(File, nullable=True, ondelete=ormar.ReferentialAction.SET_NULL)
