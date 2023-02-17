from typing import Union, List, Optional
from pydantic import BaseModel, EmailStr


class File(BaseModel):
    file_id: int
    byte_syze: int
    media_type: str
    url: str
    upload_at: int

class Photo(File):
    width: int
    height: int
        
class Video(File):
    width: int
    height: int
    duration: int

class Audio(File):
    duration: int


class NotificationSettings(BaseModel):
            messages: bool = True
            references: bool = True
            reactions: bool = True
            answers: bool = True


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
        """
        scheme for validating user request for editing profile info
        """
        name: Optional[str]
        description: Optional[str]
        shortname: Optional[str]
        email: Optional[EmailStr]

    
    class EditSettings(BaseModel):
        """
        scheme for validating user request for editing profile info
        """
        online_display: Optional[str]
        profile_photo_display: Optional[str]
        personal_messages_resend: Optional[str]
        can_write: Optional[str]
        mentions: Optional[str]
        add_to_chats: Optional[str]
        add_to_channels: Optional[str]
        can_find: Optional[str]


    class PrivacyOptions(BaseModel):
        """
        The User's PrivacyOptions object in the api view (response model)
        """
        online_display: str
        profile_photo_display: str
        personal_messages_resend: str
        can_write: str
        mentions: str
        add_to_chats: str 
        add_to_channels: str 
        can_find: str 
    

    class View(BaseModel):
        """
        The UserInfo object in the api view (response model)
        """
        id: int
        name: str
        shortname: str
        descriptiion: Optional[str]
        photo: Optional[Photo]
        last_time: int



class Search():
    class Users(BaseModel):
        """
        List of users who meet the search criteria (response model)
        """
    


class UserList(BaseModel):
    class Create(BaseModel):
        title: str
        ban: bool = False
        notification_settings: NotificationSettings
        user_ids: Optional[List[int]]


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



class Attachment():
    class Create(BaseModel):
        type: str
        file_id: int


    class View(BaseModel):
        type: str
        file: Union[Photo, Video, Audio]



class Reaction():
    class SingleView(BaseModel):
        badge: int
        user_id: int


    class ManyView(BaseModel):
        badge: int
        count: int



class Message():
    class Create(BaseModel):
        user_ids: Optional[List[int]]
        chat_ids: Optional[List[int]]
        text: Optional[str]
        attachments: Optional[List[Attachment.Create]]
        reply_to: Optional[int]
        forward_messages: Optional[List[int]]


    class View(BaseModel):
        message_id: int
        user_id: int
        text: Optional[str]
        attachments: Optional[List[Attachment.View]]
        reply_to: Optional[int]
        forward_messages: Optional[List[int]]
        reactions: Union[None, List[Reaction.SingleView], List[Reaction.ManyView]]
        views: Union[None, List[int], int]
        created_at: int



class Chat():
    class Create(BaseModel):
        user_ids: List[int]
        title: str
        description: Optional[str]
        photo_id: Optional[int]

    class View(BaseModel):
        chat_id: int
        title: str
        description: Optional[str]
        photo: Optional[Photo]
        users_count: int



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
