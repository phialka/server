'''
'Creation data' dataclasses describe a data which need to create entity
'''

from typing import Union, Optional
from pydantic import BaseModel, ByteSize
from uuid import UUID
from datetime import datetime, date



class AttachmentCreate(BaseModel):
    attach_type: str
    file_id: UUID



class MessageCerate(BaseModel):
    content: Optional[str]
    reply_message_id: Optional[UUID]
    attachments: Optional[list[AttachmentCreate]]
