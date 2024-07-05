from typing import Union, Optional
from pydantic import BaseModel, ByteSize
from uuid import UUID
from datetime import datetime, date



class File(BaseModel):
    '''
    Datamodel with file data
    '''
    file_id: UUID
    download_id: UUID
    size: ByteSize
    hash: str
    mime_type: str
    upload_at: datetime



class AuthData(BaseModel):
    user_id: UUID
    login: str
    password_hash: str



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



class PrivateChat(BaseModel):
    '''
    Dataclass with private chat data

    *there can be only two members
    '''
    chat_id: UUID
    members: list[User]



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



class ChannelMessage(BaseModel):
    '''
    Dataclass with channel message data

    *sequence is a serial number of the message in the text channel
    '''
    message: Message
    channel_id: UUID
    sequence: int



class PrivateMessage(BaseModel):
    '''
    Dataclass with channel message data

    *sequence is a serial number of the message in the private chat
    '''
    message: Message
    chat_id: UUID
    sequence: int
