import config
import databases
import sqlalchemy
import ormar

from typing import Optional
import pydantic

database = databases.Database(config.DATABASE_URL)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"
    id: int = ormar.Integer(primary_key=True)
    username: str = ormar.String(max_length=100)
    userpass: str = ormar.String(max_length=100)


class UserInfo(ormar.Model):
    class Meta(BaseMeta):
        tablename = "user_info"
    id: int = ormar.Integer(primary_key=True)
    user_id: User = ormar.ForeignKey(User)
    info: pydantic.Json = ormar.JSON()


class UserSettings(ormar.Model):
    class Meta(BaseMeta):
        tablename = "user_settings"
    id: int = ormar.Integer(primary_key=True)
    user_id: User = ormar.ForeignKey(User)
    settings: pydantic.Json = ormar.JSON()


class Message(ormar.Model):
    class Meta(BaseMeta):
        tablename = "messages"
    id: int = ormar.Integer(primary_key=True)
    content: str = ormar.String()
    created_at: int = ormar.Integer()
    updated_at: int = ormar.Integer()


class Attachment(ormar.Model):
    class Meta(BaseMeta):
        tablename = "attachments"
    id: int = ormar.Integer(primary_key=True)
    message_id: Message = ormar.ForeignKey(Message)
    files: pydantic.Json = ormar.JSON()


class Replice(ormar.Model):
    class Meta(BaseMeta):
        tablename = "replices"
    id: int = ormar.Integer(primary_key=True)
    message_id: Message = ormar.ForeignKey(Message)
    reply_message_id: Message = ormar.ForeignKey(Message)


class Forwarded(ormar.Model):
    class Meta(BaseMeta):
        tablename = "forwardes"
    id: int = ormar.Integer(primary_key=True)
    message_id: Message = ormar.ForeignKey(Message)
    forwarded_message_id: Message = ormar.ForeignKey(Message)


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
    description: str = ormar.String()


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
    sender_id: User = ormar.ForeignKey(User)
    recipient_id: User = ormar.ForeignKey(User)

      
class Conversation(ormar.Model):
    class Meta(BaseMeta):
        tablename = "conversations"
    id: int = ormar.Integer(primary_key=True)
    type: str = ormar.String(max_length=100)
    settings: pydantic.Json = ormar.JSON()
    owner_id: User = ormar.ForeignKey(User)
    created_at: int = ormar.Integer()
    updated_at: int = ormar.Integer()


class ConversationUser(ormar.Model):
    class Meta(BaseMeta):
        tablename = "conversation_users"
    id: int = ormar.Integer(primary_key=True)
    conversation_id: Conversation = ormar.ForeignKey(Conversation)
    user_id: User = ormar.ForeignKey(User)


class Permission(ormar.Model):
    class Meta(BaseMeta):
        tablename = "permissions"
    id: int = ormar.Integer(primary_key=True)
    key: str = ormar.String(max_length=100)
    descriprion: str = ormar.String(max_length=2000)


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


class ConversationUserRole(ormar.Model):
    class Meta(BaseMeta):
        tablename = "converastion_user_roles"
    id: int = ormar.Integer(primary_key=True)
    conversation_id: Conversation = ormar.ForeignKey(Conversation)
    role_id: ConversationRole = ormar.ForeignKey(ConversationRole)
    user_id: User = ormar.ForeignKey(User)


engine = sqlalchemy.create_engine(config.DATABASE_URL)
metadata.create_all(engine)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       