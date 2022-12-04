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


class UserlistIn(BaseModel):
    title: str
    ban: bool
    ignore: bool
    user_ids: Union[None, list[int]]
        
        
class Channel(BaseModel):
    id: int
    author_id: int
    title: str
    description: str
    members_count: int
    photo: Photo
    create_time: str
        
        
class Post(BaseModel):
    post_id: str
    author_id: int
    channel_id: int
    text: str
    attachments: array
    upload_time: str
        
        
class Channel_Role(BaseModel):
    id: int
    title: str
    name_color: str
    posts_permissions: int
    decoration_permissions: int
    join_permissions: int
    roling_permissions: array
        
        
class User(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    photo: Photo
    last_time: str

        
class PostContent(BaseModel):
    text: str
    attachments: str
        

class ChannelRole(BaseModel):
    title: str
    name_color: str
    posts_permissions: int
    decoration_permissions: int
    join_permissions: int
    roling_permissions: array
    items: int
