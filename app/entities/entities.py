from typing import Union, Optional
from pydantic import BaseModel, ByteSize
from uuid import UUID
from datetime import datetime, date



class File(BaseModel):
    file_id: UUID
    download_id: UUID
    size: ByteSize
    hash: str
    mime_type: str
    upload_at: datetime



class FileFilter(BaseModel):
    file_id: Optional[UUID] = None
    download_id: Optional[UUID] = None



class AuthData(BaseModel):
    user_id: UUID
    login: str
    password_hash: str



class AuthDataFilter(BaseModel):
    login: Optional[str] = None



class User(BaseModel):
    user_id: UUID
    name: str
    description: Optional[str] = None
    tag: str
    birthdate: Optional[date] = None
    photo: Optional[File] = None



class UserFilter(BaseModel):
    user_id: Optional[UUID] = None
    tag: Optional[str] = None
    name: Optional[str] = None