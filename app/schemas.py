from typing import Union
from pydantic import BaseModel


class RegistrationInfo(BaseModel):
    nickname: str
    name: str
    description: Union[str, None] = None
    email: Union[str, None] = None
    username: str
    userpass: str


class PrivacyOptions(BaseModel):
    can_found: int
    last_visit: int
    audio_call: int
    video_call: int
    forwarding: int


class NewUserlist(BaseModel):
    title: str
    ban: bool
    ignore: bool
    user_ids: Union[None, list[int]]


class Photo(BaseModel):
    file_id: int
    owner_id: int
    byte_syze: int
    media_type: str
    width: int
    height: int
    download_url: str
    previev_50px: str
    previev_100px: str
    previev_200px: str
    upload_time: int


class ChatCreate(BaseModel):
    user_ids: list[int]
    title: str
    description: str
    photo: Photo


class Attachment(BaseModel):
    type: str
    file_id: int


class MessageCreate(BaseModel):
    user_ids: list[int]
    chat_ids: list[int]
    text: str
    attachments: list[Attachment]
    reply_to: int
    forward_messages: list[int]


class MessageSearchQuery(BaseModel):
    text: str
    data: int
    chat_id: int
    author_id: int


class ChatRole(BaseModel):
    id: int
    title: str
    name_color: int
    messages_permissions: int
    decoration_permissions: int
    join_permissions: int
    roling_permissions: list[int]
