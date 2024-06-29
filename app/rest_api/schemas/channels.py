from pydantic import BaseModel
from datetime import date
from typing import Optional

from uuid import UUID



class ChannelCreate(BaseModel):
    server_id: UUID
    title: str
    description: Optional[str] = None



class ChannelUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
