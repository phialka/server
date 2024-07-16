from typing import Optional
from uuid import UUID
from datetime import datetime

import ormar

from database import database, metadata
from files.dbmodels import File
from users.dbmodels import User



class Message(ormar.Model):
    """
    Database model for message
    """
    ormar_config = ormar.OrmarConfig(
        metadata = metadata,
        database = database,
        tablename = "messages"
    )

    id: UUID = ormar.UUID(primary_key=True)
    author: User = ormar.ForeignKey(User, ondelete=ormar.ReferentialAction.SET_NULL, nullable=True)
    content: str = ormar.Text(nullable=True)
    created_at: Optional[datetime] = ormar.DateTime()
    updated_at: Optional[datetime] = ormar.DateTime(nullable=True)



class Attachment(ormar.Model):
    """
    Database model for message attachment
    """
    ormar_config = ormar.OrmarConfig(
        metadata = metadata,
        database = database,
        tablename = "attachments"
    )

    id: UUID = ormar.UUID(primary_key=True)
    file: File = ormar.ForeignKey(File, ondelete=ormar.ReferentialAction.CASCADE)
    message: Message = ormar.ForeignKey(Message, ondelete=ormar.ReferentialAction.CASCADE)
    attach_type: str = ormar.String(max_length=40)
