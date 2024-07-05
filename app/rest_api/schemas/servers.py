from pydantic import BaseModel
from datetime import date
from typing import Optional
from uuid import UUID



class ServerCreate(BaseModel):
    title: str
    description: Optional[str] = None



class ServerUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class UserInvite(BaseModel):
    user_id: UUID