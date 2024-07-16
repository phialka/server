from typing import Union, Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, date

from files.schemas import File
from messages.schemas import Message


class Channel(BaseModel):
    '''
    Datamodel with test channel data
    '''
    channel_id: UUID
    server_id: UUID
    title: str
    description: Optional[str] = None
    logo: Optional[File] = None
    created_at: datetime



class ChannelMessage(BaseModel):
    '''
    Dataclass with channel message data

    *sequence is a serial number of the message in the text channel
    '''
    message: Message
    channel_id: UUID
    sequence: int



class ChannelCreate(BaseModel):
    server_id: UUID
    title: str
    description: Optional[str] = None



class ChannelUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
