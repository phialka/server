from typing import Optional, Union, List

import databases
import sqlalchemy
import ormar
import pydantic

try:
    import config
except: 
    import app.config as config


#default value
_database_url = config.DATABASE_URL



class BaseMeta(ormar.ModelMeta):
    metadata = sqlalchemy.MetaData()
    database = databases.Database(_database_url)
    
    @classmethod
    def change_db(cls, db_url: str) -> None:
        """
        Use to change database
        Don't use it without adapter 
        """
        cls.database = databases.Database(db_url)



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

    id: int = ormar.Integer(primary_key=True)
    hash: str = ormar.String(max_length=34)
    mime_type: str = ormar.String(max_length=50)
    size: int = ormar.Integer()
    type_info: Optional[pydantic.Json[PhotoTypeInfo, VideoTypeInfo, AudioTypeInfo]] = ormar.JSON()
    location: str = ormar.String(max_length=100)

    @property
    def main_type(self):
        return self.mime_type.split("/")[0]

    @property
    def type_info_(self) -> PhotoTypeInfo|VideoTypeInfo|AudioTypeInfo|None:
        """presrnts json-field 'type_info' as dict"""
        if self.type_info != None:
            if self.main_type == "image":
                return PhotoTypeInfo(**self.type_info)
            elif self.main_type == "video":
                return VideoTypeInfo(**self.type_info)
            elif self.main_type == "audio":
                return AudioTypeInfo(**self.type_info)
        return None



class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"

    class Info(pydantic.BaseModel):
        name: str
        shortname: str
        description: Optional[str]

    class Settings(pydantic.BaseModel):
        online_display: str = "all"
        profile_photo_display: str = "all"
        personal_messages_resend: str = "all"
        can_write: str = "all"
        mentions: str = "all"
        add_to_chats: str = "all"
        add_to_channels: str = "all"
        can_find: str = "all"

    id: int = ormar.Integer(primary_key=True)
    info: pydantic.Json[Info] = ormar.JSON()
    settings: pydantic.Json = ormar.JSON()
    photo_file_id: File = ormar.ForeignKey(File)
    last_visit: int = ormar.Integer()
    created_at: int = ormar.Integer()

    @property
    def info_(self) -> Info:
        """presrnts json-field 'info' as dict"""
        return User.Info(**self.info)



class Auth(ormar.Model):
    class Meta(BaseMeta):
        tablename = "auth"
    id: int = ormar.Integer(primary_key=True)
    user_id: User = ormar.ForeignKey(User)
    username: str = ormar.String(max_length=100, unique=True)
    userpass: str = ormar.String(max_length=100)



class UserBlacklist(ormar.Model):
    class Meta(BaseMeta):
        tablename = "blacklist"

    id: int = ormar.Integer(primary_key=True)
    owner_id: User = ormar.ForeignKey(User, related_name="blacklist")
    banned_user: User = ormar.ForeignKey(User, related_name="banned_from")



class Contact(ormar.Model):
    class Meta(BaseMeta):
        tablename = "contacts"

    id: int = ormar.Integer(primary_key=True)
    owner_id: User = ormar.ForeignKey(User, related_name="contacts")
    contact_user: User = ormar.ForeignKey(User, related_name="into_contacts")



class UserList(ormar.Model):
    class Meta(BaseMeta):
        tablename = "user_lists"

    class Settings(pydantic.BaseModel):
        notify_messages: bool = True
        notify_reactions: bool = True
        notify_answers: bool = True

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
    list_id: UserList = ormar.ForeignKey(UserList, related_name="rows")
    user_id: User = ormar.ForeignKey(User)



class Conversation(ormar.Model):
    class Meta(BaseMeta):
        tablename = "conversations"

    class Settings(pydantic.BaseModel):
        pass 
    
    id: int = ormar.Integer(primary_key=True)
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
    settings: pydantic.Json = ormar.JSON()



class ConversationInList(ormar.Model):
    class Meta(BaseMeta):
        tablename = "conversations_in_lists"
    id: int = ormar.Integer(primary_key=True)
    list_id: ConversationList = ormar.ForeignKey(ConversationList)
    conversation_id: Conversation = ormar.ForeignKey(Conversation)
    user_id: User = ormar.ForeignKey(User, related_name="in_lists")



class Server(ormar.Model):
    class Meta(BaseMeta):
        tablename = "servers"
    id: int = ormar.Integer(primary_key=True)
    ip: int = ormar.Integer()
    port: int = ormar.Integer()
    title: str = ormar.String(max_length=100)
    description: str = ormar.String(max_length=100)



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
    conversation_id: Conversation = ormar.ForeignKey(Conversation)
    destination_user: User = ormar.ForeignKey(User, related_name="dst_user")
    user_id: User = ormar.ForeignKey(User, related_name="msg_author")
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
    message_id: Message = ormar.ForeignKey(Message, related_name="forwardes")
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
    role_name: str = ormar.String(max_length=100)



class RolePermission(ormar.Model):
    class Meta(BaseMeta):
        tablename = "role_permissions"
    id: int = ormar.Integer(primary_key=True)
    role_id: ConversationRole = ormar.ForeignKey(ConversationRole)
    permission_id: Permission = ormar.ForeignKey(Permission)
    value: bool = ormar.Boolean()



class ConversationUser(ormar.Model):
    class Meta(BaseMeta):
        tablename = "converastion_user"
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



async def connect_database(database_url: Optional[str] = None):
    if database_url:
        BaseMeta.change_db(database_url)

    engine = sqlalchemy.create_engine(database_url or _database_url)
    BaseMeta.metadata.create_all(engine)

    database_ = BaseMeta.database
    if not database_.is_connected:
        await database_.connect()



async def disconnect_database():
    if BaseMeta.database.is_connected:
        await BaseMeta.database.disconnect()







# class DatabaseSchemed():
#     def __init__(self, db_url, database) -> None:
#         self.db: databases.Database = database
#         self.db_url = db_url

#         self.users = User
#         self.auth = Auth
    

#     async def connect_database(database_url: Optional[str] = None):
#         if database_url:
#             BaseMeta.change_db(database_url)
 
#         engine = sqlalchemy.create_engine(database_url or _database_url)
#         BaseMeta.metadata.create_all(engine)

#         database_ = BaseMeta.database
#         if not database_.is_connected:
#             await database_.connect()


#     async def disconnect_database(database):
#         if database.is_connected:
#             await database.disconnect()

    
#     @classmethod
#     async def getdb(cls, db_url) -> None:
#         await cls.connect_database(db_url)
#         return cls(db_url, BaseMeta.database)



