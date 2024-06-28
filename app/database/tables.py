from typing import Optional, Union, List
from uuid import UUID
from datetime import datetime, date

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



class File(ormar.Model):
    class Meta(BaseMeta):
        tablename = "files"

    id: UUID = ormar.UUID(primary_key=True)
    download_id: UUID = ormar.UUID()
    hash: str = ormar.String(max_length=200)
    mime_type: str = ormar.String(max_length=100)
    size: int = ormar.Integer()
    upload_at: datetime = ormar.DateTime(timezone=False)



class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"

    id: UUID = ormar.UUID(primary_key=True)
    name: str = ormar.String(max_length=40)
    description: Optional[str] = ormar.String(max_length=100, nullable=True)
    tag: str = ormar.String(max_length=30)
    birthdate: Optional[date] = ormar.Date(nullable=True)
    photo: File = ormar.ForeignKey(File, nullable=True, ondelete=ormar.ReferentialAction.SET_NULL)



class AuthData(ormar.Model):
    class Meta(BaseMeta):
        tablename = "auth_data"

    user_id: User = ormar.ForeignKey(User, ondelete=ormar.ReferentialAction.CASCADE)
    login: UUID = ormar.String(max_length=200, primary_key=True)
    pass_hash: str = ormar.String(max_length=200)



class Server(ormar.Model):
    class Meta(BaseMeta):
        tablename = "servers"

    id: UUID = ormar.UUID(primary_key=True)
    owner: User = ormar.ForeignKey(User, ondelete=ormar.ReferentialAction.CASCADE)
    title: str = ormar.String(max_length=40)
    description: Optional[str] = ormar.String(max_length=100, nullable=True)
    created_at: Optional[datetime] = ormar.DateTime()
    logo: File = ormar.ForeignKey(File, nullable=True, ondelete=ormar.ReferentialAction.SET_NULL)



class Channel(ormar.Model):
    class Meta(BaseMeta):
        tablename = "channels"

    id: UUID = ormar.UUID(primary_key=True)
    server: Server = ormar.ForeignKey(Server, ondelete=ormar.ReferentialAction.CASCADE)
    title: str = ormar.String(max_length=40)
    description: Optional[str] = ormar.String(max_length=100, nullable=True)
    created_at: Optional[datetime] = ormar.DateTime()
    logo: File = ormar.ForeignKey(File, nullable=True, ondelete=ormar.ReferentialAction.SET_NULL)



class PrivateChat(ormar.Model):
    class Meta(BaseMeta):
        tablename = "private_chat"

    id: UUID = ormar.UUID(primary_key=True)



class ServerMember(ormar.Model):
    class Meta(BaseMeta):
        tablename = "server_members"

    id: UUID = ormar.UUID(primary_key=True)
    server: Server = ormar.ForeignKey(Server, ondelete=ormar.ReferentialAction.CASCADE)
    user: User = ormar.ForeignKey(User, ondelete=ormar.ReferentialAction.CASCADE)



class PrivateChatMember(ormar.Model):
    class Meta(BaseMeta):
        tablename = "private_chat_members"

    id: UUID = ormar.UUID(primary_key=True)
    private_chat: PrivateChat = ormar.ForeignKey(Server, ondelete=ormar.ReferentialAction.CASCADE)
    user: User = ormar.ForeignKey(User, ondelete=ormar.ReferentialAction.CASCADE)



class Message(ormar.Model):
    class Meta(BaseMeta):
        tablename = "messages"

    id: UUID = ormar.UUID(primary_key=True)
    author: User = ormar.ForeignKey(User, ondelete=ormar.ReferentialAction.SET_NULL, nullable=True)
    content: str = ormar.Text()
    created_at: Optional[datetime] = ormar.DateTime()
    updated_at: Optional[datetime] = ormar.DateTime()



class Attachment(ormar.Model):
    class Meta(BaseMeta):
        tablename = "attachments"

    id: UUID = ormar.UUID(primary_key=True)
    file: File = ormar.ForeignKey(File, ondelete=ormar.ReferentialAction.CASCADE)
    message: Message = ormar.ForeignKey(Message, ondelete=ormar.ReferentialAction.CASCADE)
    attach_type: str = ormar.String(max_length=40)



class ChannelMessage(ormar.Model):
    class Meta(BaseMeta):
        tablename = "channel_messages"

    id: UUID = ormar.UUID(primary_key=True)
    channel: Channel = ormar.ForeignKey(Channel, ondelete=ormar.ReferentialAction.CASCADE)
    message: Message = ormar.ForeignKey(Message, ondelete=ormar.ReferentialAction.CASCADE)
    was_viewed: bool = ormar.Boolean(default=False)
    sequence: int = ormar.Integer(autoincrement=True)



class PrivateMessage(ormar.Model):
    class Meta(BaseMeta):
        tablename = "channel_messages"

    id: UUID = ormar.UUID(primary_key=True)
    private_chat: PrivateChat = ormar.ForeignKey(PrivateChat, ondelete=ormar.ReferentialAction.CASCADE)
    message: Message = ormar.ForeignKey(Message, ondelete=ormar.ReferentialAction.CASCADE)
    was_viewed: bool = ormar.Boolean(default=False)
    sequence: int = ormar.Integer(autoincrement=True)



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


