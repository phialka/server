from typing import Optional
from uuid import UUID
from datetime import date

from pydantic import BaseModel

from files.schemas import File



class UserCreate(BaseModel):
    name: str
    description: Optional[str] = None
    birthdate: Optional[date] = None
    tag: Optional[str] = None
    login: str
    password: str



class UserUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    birthdate: Optional[date] = None
    tag: Optional[str] = None



class User(BaseModel):
    '''
    Datamodel with user profile data
    '''
    user_id: UUID
    name: str
    description: Optional[str] = None
    tag: str
    birthdate: Optional[date] = None
    photo: Optional[File] = None
