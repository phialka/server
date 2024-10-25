from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, date

from files.schemas import File



class AttachmentCreate(BaseModel):
    attach_type: str
    file_id: UUID



class MessageCreate(BaseModel):
    content: Optional[str] = None
    reply_message_id: Optional[UUID] = None
    attachments: Optional[list[AttachmentCreate]] = None



class MessageUpdate(BaseModel):
    content: Optional[str] = None



class Attachment(BaseModel):
    '''
    Dataclass with attachment data

    attach types:
    - file
    - media
    '''
    message_id: UUID
    attach_type: str
    file: File



class Message(BaseModel):
    '''
    Datamodel with message data

    Message is independent entity.
    In future message can be a part of a channel message or a private message.
    '''
    message_id: UUID
    author_id: UUID
    content: Optional[str] = None
    attachments: Optional[list[Attachment]] = None
    reply_message_id: Optional[UUID] = None
    updated_at: Optional[date] = None
    created_at: datetime
