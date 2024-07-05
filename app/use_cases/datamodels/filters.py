'''
Filters are dataclasses that are used in entity repositories
'''

from typing import Union, Optional
from pydantic import BaseModel, ByteSize
from uuid import UUID
from datetime import datetime, date



class FileFilter(BaseModel):
    file_id: Optional[UUID] = None
    download_id: Optional[UUID] = None



class AuthDataFilter(BaseModel):
    login: Optional[str] = None



class UserFilter(BaseModel):
    user_id: Optional[UUID] = None
    tag: Optional[str] = None
    name: Optional[str] = None
    tag_search_prompt: Optional[str] = None
    name_search_prompt: Optional[str] = None



class ServerFilter(BaseModel):
    server_id: Optional[UUID] = None
    owner_id: Optional[UUID] = None
    title_search_prompt: Optional[str] = None
    description_search_prompt: Optional[str] = None



class ServerMemberFilter(BaseModel):
    server_id: Optional[UUID] = None
    user_id: Optional[UUID] = None



class ChannelFilter(BaseModel):
    channel_id: Optional[UUID] = None
    server_id: Optional[UUID] = None



class PrivateChatFilter(BaseModel):
    chat_id: Optional[UUID] = None
    member_ids: Optional[list[UUID]] = None



class AttachmentFilter(BaseModel):
    message_id: Optional[UUID] = None



class MessageFilter(BaseModel):
    message_id: Optional[UUID] = None
    author_id: Optional[UUID] = None
    reply_message_id: Optional[UUID] = None



class ChannelMessageFilter(BaseModel):
    channel_id: Optional[UUID] = None
    sequence_min: Optional[int] = None



class PrivateMessageFilter(BaseModel):
    chat_id: Optional[UUID] = None
    sequence_min: Optional[int] = None
