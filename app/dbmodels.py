from typing import Optional, Union, List
import json

import databases
import sqlalchemy
import ormar
import pydantic

import config


database = databases.Database(config.DATABASE_URL)
metadata = sqlalchemy.MetaData()

class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class PhotoTypeInfo(pydantic.BaseModel):
    width: int
    height: int

class VideoTypeInfo(pydantic.BaseModel):
    width: int
    height: int
    duration: int

class AudioTypeInfo(pydantic.BaseModel):
    duration: int


class File(ormar.Model):
    class Meta(BaseMeta):
        tablename = "files"

    class Info(pydantic.BaseModel):
        type: str
        title: str
        size: int
        upload_at: int
        type_info: Union[PhotoTypeInfo, VideoTypeInfo, AudioTypeInfo, None]
        url: str

    id: int = ormar.Integer(primary_key=True)
    hash: str = ormar.String(max_length=34)
    info: pydantic.Json[Info] = ormar.JSON()
    path: str = ormar.String(max_length=100)

    @property
    def info_(self) -> Info:
        return File.Info(**self.info)



class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"
    id: int = ormar.Integer(primary_key=True)
    username: str = ormar.String(max_length=100, unique=True)
    userpass: str = ormar.String(max_length=100)


class UserInfo(ormar.Model):
    class Meta(BaseMeta):
        tablename = "user_info"

    class Info(pydantic.BaseModel):
        name: str
        shortname: str
        description: Optional[str]
        email: Optional[pydantic.EmailStr]
        photo_file_id: Optional[int]
        last_visit: int

    id: int = ormar.Integer(primary_key=True)
    user_id: User = ormar.ForeignKey(User)
    info: pydantic.Json[Info] = ormar.JSON()

    @property
    def info_(self) -> Info:
        return UserInfo.Info(**self.info)



class UserSettings(ormar.Model):
    class Meta(BaseMeta):
        tablename = "user_settings"

    class Settings(pydantic.BaseModel):
        class PrivacySettings(pydantic.BaseModel):
            online_display: str = "all"
            profile_photo_display: str = "all"
            personal_messages_resend: str = "all"
            can_write: str = "all"
            mentions: str = "all"
            add_to_chats: str = "all"
            add_to_channels: str = "all"
            can_find: str = "all"

        privacy_settings: PrivacySettings

    id: int = ormar.Integer(primary_key=True)
    user_id: User = ormar.ForeignKey(User)
    settings: pydantic.Json = ormar.JSON()

    @property
    def settings_(self) -> Settings:
        return UserSettings.Settings(**self.settings)



class UserList(ormar.Model):
    class Meta(BaseMeta):
        tablename = "user_lists"

    class Settings(pydantic.BaseModel):
        class NotificationSettings(pydantic.BaseModel):
            messages: bool = True
            references: bool = True
            reactions: bool = True
            answers: bool = True

        contacts: bool = False
        black_list: bool = False
        ban_messages: bool = False
        notifications: NotificationSettings

    id: int = ormar.Integer(primary_key=True)
    owner_id: User = ormar.ForeignKey(User)
    title: str = ormar.String(max_length=100)
    settings: pydantic.Json = ormar.JSON()

    @property
    def settings_(self) -> Settings:
        return UserList.Settings(**self.settings)



class UserInList(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users_in_lists"
    id: int = ormar.Integer(primary_key=True)
    list_id: UserList = ormar.ForeignKey(UserList)
    user_id: User = ormar.ForeignKey(User)



class Conversation(ormar.Model):
    class Meta(BaseMeta):
        tablename = "conversations"

    class Settings(pydantic.BaseModel):
        pass 
    
    id: int = ormar.Integer(primary_key=True)
    type: str = ormar.String(max_length=10)
    title: str = ormar.String(max_length=100)
    description: str = ormar.String(max_length=100)
    photo_id: File = ormar.ForeignKey(File)
    settings: pydantic.Json = ormar.JSON()
    owner_id: User = ormar.ForeignKey(User)
    created_at: int = ormar.Integer()
    updated_at: int = ormar.Integer()



class ConversationList(ormar.Model):
    class Meta(BaseMeta):
        tablename = "conversations_lists"
    id: int = ormar.Integer(primary_key=True)
    owner_id: User = ormar.ForeignKey(User)
    title: str = ormar.String(max_length=100)
    notify_settings: pydantic.Json = ormar.JSON()



class ConversationInList(ormar.Model):
    class Meta(BaseMeta):
        tablename = "conversations_in_lists"
    id: int = ormar.Integer(primary_key=True)
    list_id: ConversationList = ormar.ForeignKey(ConversationList)
    conversation_id: Conversation = ormar.ForeignKey(Conversation)



class Server(ormar.Model):
    class Meta(BaseMeta):
        tablename = "servers"
    id: int = ormar.Integer(primary_key=True)
    ip: int = ormar.Integer()
    port: int = ormar.Integer()



class ServerDataDistribution(ormar.Model):
    class Meta(BaseMeta):
        tablename = "server_data_distribution"
    id: int = ormar.Integer(primary_key=True)
    server_id: Server = ormar.ForeignKey(Server)
    conversation_id: Conversation = ormar.ForeignKey(Conversation)
        

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
class Message(ormar.Model):
    class Meta(BaseMeta):
        tablename = "messages"
    id: int = ormar.Integer(primary_key=True)
    content: str = ormar.String(max_length=1000)
    created_at: int = ormar.Integer()
    updated_at: int = ormar.Integer()



class Attachment(ormar.Model):
    class Meta(BaseMeta):
        tablename = "attachments"
    id: int = ormar.Integer(primary_key=True)
    message_id: Message = ormar.ForeignKey(Message)
    file: File = ormar.ForeignKey(File)
    type: str = ormar.String(max_length=20)



class Replice(ormar.Model):
    class Meta(BaseMeta):
        tablename = "replices"
    id: int = ormar.Integer(primary_key=True)
    message_id: Message = ormar.ForeignKey(Message, related_name="answers")
    reply_message_id: Message = ormar.ForeignKey(Message, related_name="quote")



class Forwarded(ormar.Model):
    class Meta(BaseMeta):
        tablename = "forwardes"
    id: int = ormar.Integer(primary_key=True)
    message_id: Message = ormar.ForeignKey(Message, related_name="forwarded")
    forwarded_message_id: Message = ormar.ForeignKey(Message, related_name="be_forwarded")



class View(ormar.Model):
    class Meta(BaseMeta):
        tablename = "views"
    id: int = ormar.Integer(primary_key=True)
    message_id: Message = ormar.ForeignKey(Message)
    user_id: User = ormar.ForeignKey(User)



class Reaction(ormar.Model):
    class Meta(BaseMeta):
        tablename = "reactions"
    id: int = ormar.Integer(primary_key=True)
    badge: int = ormar.Integer()
    description: str = ormar.String(max_length=50)



class MessageReaction(ormar.Model):
    class Meta(BaseMeta):
        tablename = "message_reactions"
    id: int = ormar.Integer(primary_key=True)
    message_id: Message = ormar.ForeignKey(Message)
    user_id: User = ormar.ForeignKey(User)
    reaction_id: Reaction = ormar.ForeignKey(Reaction)



class MessageQueue(ormar.Model):
    class Meta(BaseMeta):
        tablename = "message_queues"
    id: int = ormar.Integer(primary_key=True)
    conversation_id: Conversation = ormar.ForeignKey(Conversation)
    message_id: Message = ormar.ForeignKey(Message)
    sender_id: User = ormar.ForeignKey(User, related_name="sender_user")
    recipient_id: User = ormar.ForeignKey(User, related_name="recipient_user")



class Permission(ormar.Model):
    class Meta(BaseMeta):
        tablename = "permissions"
    id: int = ormar.Integer(primary_key=True)
    key: str = ormar.String(max_length=100)
    description: str = ormar.String(max_length=2000)



class ConversationRole(ormar.Model):
    class Meta(BaseMeta):
        tablename = "conversation_roles"
    id: int = ormar.Integer(primary_key=True)
    role: str = ormar.String(max_length=100)



class RolePermission(ormar.Model):
    class Meta(BaseMeta):
        tablename = "role_permissions"
    id: int = ormar.Integer(primary_key=True)
    role_id: ConversationRole = ormar.ForeignKey(ConversationRole)
    permission_id: Permission = ormar.ForeignKey(Permission)
    value: bool = ormar.Boolean()



class ConversationUser(ormar.Model):
    class Meta(BaseMeta):
        tablename = "converastion_user_roles"
    id: int = ormar.Integer(primary_key=True)
    conversation_id: Conversation = ormar.ForeignKey(Conversation)
    role_id: ConversationRole = ormar.ForeignKey(ConversationRole)
    user_id: User = ormar.ForeignKey(User)



class ConversationsFile(ormar.Model):
    class Meta(BaseMeta):
        tablename = "conversations_files"
    id: int = ormar.Integer(primary_key=True)
    file_id: File = ormar.ForeignKey(File)
    conversation_id: Conversation = ormar.ForeignKey(Conversation)



def tables_init():
    engine = sqlalchemy.create_engine(config.DATABASE_URL)
    metadata.create_all(engine)
