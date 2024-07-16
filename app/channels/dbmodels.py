from typing import Optional
from uuid import UUID
from datetime import datetime

import ormar

from database import database, metadata
from files.dbmodels import File
from servers.dbmodels import Server
from messages.dbmodels import Message



class Channel(ormar.Model):
    """
    Database model for text channel
    """
    ormar_config = ormar.OrmarConfig(
        metadata = metadata,
        database = database,
        tablename = "channels"
    )

    id: UUID = ormar.UUID(primary_key=True)
    server: Server = ormar.ForeignKey(Server, ondelete=ormar.ReferentialAction.CASCADE)
    title: str = ormar.String(max_length=40)
    description: Optional[str] = ormar.String(max_length=100, nullable=True)
    created_at: Optional[datetime] = ormar.DateTime()
    logo: File = ormar.ForeignKey(File, nullable=True, ondelete=ormar.ReferentialAction.SET_NULL)



class ChannelMessage(ormar.Model):
    """
    Database model for tex channel message
    """
    ormar_config = ormar.OrmarConfig(
        metadata = metadata,
        database = database,
        tablename = "channel_messages"
    )

    id: UUID = ormar.UUID(primary_key=True)
    channel: Channel = ormar.ForeignKey(Channel, ondelete=ormar.ReferentialAction.CASCADE)
    message: Message = ormar.ForeignKey(Message, ondelete=ormar.ReferentialAction.CASCADE)
    was_viewed: bool = ormar.Boolean(default=False)
    sequence: int = ormar.Integer()
