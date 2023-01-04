from typing import Union, List, Optional
from pydantic import BaseModel, EmailStr
from dbmodels import NotificationSettings


class Photo(BaseModel):
    file_id: int
    byte_syze: int
    media_type: str
    width: int
    height: int
    url: str
    upload_at: int


class User():
    class Registration(BaseModel):
        """
        scheme for validating user registration request data
        """
        username: str
        userpass: str
        name: str
        description: Optional[str]
        shortname: str
        email: Optional[EmailStr]


    class Login(BaseModel):
        """
        scheme for validating user login request data
        """
        username: str
        userpass: str


    class Reset(BaseModel):
        userpass: str
        new_pass: str


    class EditInfo(BaseModel):
        name: Optional[str]
        description: Optional[str]
        shortname: Optional[str]
        email: Optional[EmailStr]


    class PrivacyOptions(BaseModel):
        can_found: int
        last_visit: int
        audio_call: int
        video_call: int
        forwarding: int
    

    class Info(BaseModel):
        """
        The UserInfo object in the api view (response model)
        """
        id: int
        name: str
        shortname: str
        descriptiion: str
        photo: Photo
        last_time: str

    

class UserList(BaseModel):
    class Create(BaseModel):
        title: str
        ban: bool = False
        notification_settings: NotificationSettings
        user_ids: Union[None, List[int]]


    class View(BaseModel):
        """
        The UserList object in the api view (response model)
        """
        class Settings(BaseModel):
            ban_messages: bool
            notification_settings: NotificationSettings
        id: int
        title: str
        settings: Settings

        
class ConversationList(BaseModel):
    class Create(BaseModel):
        title: str
        notification_settings: NotificationSettings
        conversation_ids: Union[None, List[int]]


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
    attachments: Union[List[str], None] = None
    upload_time: str
        
        
class ChannelRole(BaseModel):
    id: int
    title: str
    name_color: str
    posts_permissions: int
    decoration_permissions: int
    join_permissions: int
    roling_permissions: Union[List[str], None] = None
        
        
class PostContent(BaseModel):
    text: str
    attachments: str
        

class ChannelRole(BaseModel):
    title: str
    name_color: str
    posts_permissions: int
    decoration_permissions: int
    join_permissions: int
    roling_permissions: Union[List[str], None] = None
    items: int



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
    roling_permissions: List[int]
