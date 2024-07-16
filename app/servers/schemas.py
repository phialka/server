from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from files.schemas import File
from users.schemas import User



class Server(BaseModel):
    '''
    Datamodel with server data
    '''
    server_id: UUID
    owner_id: UUID
    title: str
    description: Optional[str] = None
    logo: Optional[File] = None
    created_at: datetime



class ServerMember(BaseModel):
    '''
    Datamodel with server member data
    '''
    server_id: UUID
    user: User



class ServerCreate(BaseModel):
    title: str
    description: Optional[str] = None



class ServerUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None



class UserInvite(BaseModel):
    user_id: UUID
