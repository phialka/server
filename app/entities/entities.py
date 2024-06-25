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


class Server(BaseModel):
    server_id: UUID
    owner_id: UUID
    title: str
    description: Optional[str] = None
    logo: Optional[File] = None
    created_at: datetime


class Channel(BaseModel):
    cnannel_id: UUID
    server_id: UUID
    title: str
    description: Optional[str] = None
    logo: Optional[File] = None
    created_at: datetime


class PrivateChat(BaseModel):
    chat_id: UUID
    members: list[User]


class Attachment(BaseModel):
    attach_type: str
    file: File


class Message(BaseModel):
    message_id: UUID
    author_id: UUID
    content: Optional[str] = None
    attachments: Optional[list[Attachment]] = None
    reply_message_id: Optional[UUID] = None
    updated_at: Optional[date] = None
    created_at: datetime


class ChannelMessage(Message):
    sequence: int


class PrivateMessage(Message):
    sequence: int