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

_database = databases.Database(_database_url)
_metadata = sqlalchemy.MetaData()

base_ormar_config = ormar.OrmarConfig(
    metadata = _metadata,
    database = _database
)



def __change_db(url: str):
    _database = databases.Database(url)



class File(ormar.Model):
    ormar_config = ormar.OrmarConfig(
        metadata = _metadata,
        database = _database,
        tablename = "files"
    )

    id: UUID = ormar.UUID(primary_key=True)
    download_id: UUID = ormar.UUID()
    hash: str = ormar.String(max_length=200)
    mime_type: str = ormar.String(max_length=100)
    size: int = ormar.Integer()
    upload_at: datetime = ormar.DateTime(timezone=False)



class User(ormar.Model):
    ormar_config = ormar.OrmarConfig(
        metadata = _metadata,
        database = _database,
        tablename = "users"
    )

    id: UUID = ormar.UUID(primary_key=True)
    name: str = ormar.String(max_length=40)
    description: Optional[str] = ormar.String(max_length=100, nullable=True)
    tag: str = ormar.String(max_length=30)
    birthdate: Optional[date] = ormar.Date(nullable=True)
    photo: File = ormar.ForeignKey(File, nullable=True, ondelete=ormar.ReferentialAction.SET_NULL)



class AuthData(ormar.Model):
    ormar_config = ormar.OrmarConfig(
        metadata = _metadata,
        database = _database,
        tablename = "auth_data"
    )

    user_id: User = ormar.ForeignKey(User, ondelete=ormar.ReferentialAction.CASCADE)
    login: UUID = ormar.String(max_length=200, primary_key=True)
    pass_hash: str = ormar.String(max_length=200)



class Server(ormar.Model):
    ormar_config = ormar.OrmarConfig(
        metadata = _metadata,
        database = _database,
        tablename = "servers"
    )

    id: UUID = ormar.UUID(primary_key=True)
    owner: User = ormar.ForeignKey(User, ondelete=ormar.ReferentialAction.CASCADE)
    title: str = ormar.String(max_length=40)
    description: Optional[str] = ormar.String(max_length=100, nullable=True)
    created_at: Optional[datetime] = ormar.DateTime()
    logo: File = ormar.ForeignKey(File, nullable=True, ondelete=ormar.ReferentialAction.SET_NULL)



class Channel(ormar.Model):
    ormar_config = ormar.OrmarConfig(
        metadata = _metadata,
        database = _database,
        tablename = "channels"
    )

    id: UUID = ormar.UUID(primary_key=True)
    server: Server = ormar.ForeignKey(Server, ondelete=ormar.ReferentialAction.CASCADE)
    title: str = ormar.String(max_length=40)
    description: Optional[str] = ormar.String(max_length=100, nullable=True)
    created_at: Optional[datetime] = ormar.DateTime()
    logo: File = ormar.ForeignKey(File, nullable=True, ondelete=ormar.ReferentialAction.SET_NULL)



class PrivateChat(ormar.Model):
    ormar_config = ormar.OrmarConfig(
        metadata = _metadata,
        database = _database,
        tablename = "private_chats"
    )

    id: UUID = ormar.UUID(primary_key=True)



class ServerMember(ormar.Model):
    ormar_config = ormar.OrmarConfig(
        metadata = _metadata,
        database = _database,
        tablename = "server_members"
    )

    id: UUID = ormar.UUID(primary_key=True)
    server: Server = ormar.ForeignKey(Server, ondelete=ormar.ReferentialAction.CASCADE)
    user: User = ormar.ForeignKey(User, ondelete=ormar.ReferentialAction.CASCADE)



class PrivateChatMember(ormar.Model):
    ormar_config = ormar.OrmarConfig(
        metadata = _metadata,
        database = _database,
        tablename = "private_chat_members"
    )

    id: UUID = ormar.UUID(primary_key=True)
    private_chat: PrivateChat = ormar.ForeignKey(PrivateChat, ondelete=ormar.ReferentialAction.CASCADE)
    user: User = ormar.ForeignKey(User, ondelete=ormar.ReferentialAction.CASCADE)



class Message(ormar.Model):
    ormar_config = ormar.OrmarConfig(
        metadata = _metadata,
        database = _database,
        tablename = "messages"
    )

    id: UUID = ormar.UUID(primary_key=True)
    author: User = ormar.ForeignKey(User, ondelete=ormar.ReferentialAction.SET_NULL, nullable=True)
    content: str = ormar.Text(nullable=True)
    created_at: Optional[datetime] = ormar.DateTime()
    updated_at: Optional[datetime] = ormar.DateTime(nullable=True)



class Attachment(ormar.Model):
    ormar_config = ormar.OrmarConfig(
        metadata = _metadata,
        database = _database,
        tablename = "attachments"
    )

    id: UUID = ormar.UUID(primary_key=True)
    file: File = ormar.ForeignKey(File, ondelete=ormar.ReferentialAction.CASCADE)
    message: Message = ormar.ForeignKey(Message, ondelete=ormar.ReferentialAction.CASCADE)
    attach_type: str = ormar.String(max_length=40)



class ChannelMessage(ormar.Model):
    ormar_config = ormar.OrmarConfig(
        metadata = _metadata,
        database = _database,
        tablename = "channel_messages"
    )

    id: UUID = ormar.UUID(primary_key=True)
    channel: Channel = ormar.ForeignKey(Channel, ondelete=ormar.ReferentialAction.CASCADE)
    message: Message = ormar.ForeignKey(Message, ondelete=ormar.ReferentialAction.CASCADE)
    was_viewed: bool = ormar.Boolean(default=False)
    sequence: int = ormar.Integer()



class PrivateMessage(ormar.Model):
    ormar_config = ormar.OrmarConfig(
        metadata = _metadata,
        database = _database,
        tablename = "private_messages"
    )

    id: UUID = ormar.UUID(primary_key=True)
    private_chat: PrivateChat = ormar.ForeignKey(PrivateChat, ondelete=ormar.ReferentialAction.CASCADE)
    message: Message = ormar.ForeignKey(Message, ondelete=ormar.ReferentialAction.CASCADE)
    was_viewed: bool = ormar.Boolean(default=False)
    sequence: int = ormar.Integer()



async def connect_database(database_url: Optional[str] = None):
    if database_url:
        __change_db(database_url)
    engine = sqlalchemy.create_engine(database_url or _database_url)
    print('> engine create')
    base_ormar_config.metadata.create_all(engine)

    print('> all create')
    database_ = base_ormar_config.database
    if not database_.is_connected:
        await database_.connect()
        print('> connected')



async def disconnect_database():
    if base_ormar_config.database.is_connected:
        await base_ormar_config.database.disconnect()


