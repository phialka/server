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


class Conversations(ormar.Model):
    class Meta(BaseMeta):
        tablename = "conversations"
    id: int = ormar.Integer(primary_key=True)
    type: str = ormar.String(max_length=100)
    settings: pydantic.Json = ormar.JSON()
    owner_id: int = ormar.Integer()
    created_at: int = ormar.Integer()
    updated_at: int = ormar.Integer()


class ConversationUsers(ormar.Model):
    class Meta(BaseMeta):
        tablename = "conversation_users"
    id: int = ormar.Integer(primary_key=True)
    conversation_id: int = ormar.Integer()
    user_id: int = ormar.Integer()


class Permissions(ormar.Model):
    class Meta(BaseMeta):
        tablename = "permissions"
    id: int = ormar.Integer(primary_key=True)
    key: str = ormar.String(max_length=100)
    descriprion: str = ormar.String(max_length=2000)


class ConversationRoles(ormar.Model):
    class Meta(BaseMeta):
        tablename = "conversation_roles"
    id: int = ormar.Integer(primary_key=True)
    role: str = ormar.String(max_length=100)


class RolePermissions(ormar.Model):
    class Meta(BaseMeta):
        tablename = "role_permissions"
    id: int = ormar.Integer(primary_key=True)
    role_id: int = ormar.Integer()
    permission_id: int = ormar.Integer()
    value: bool = ormar.Boolean()


class ConversationUserRoles(ormar.Model):
    class Meta(BaseMeta):
        tablename = "converastion_user_role"
    id: int = ormar.Integer(primary_key=True)
    conversation_id: int = ormar.Integer()
    role_id: int = ormar.Integer()
    user_id: int = ormar.Integer()


engine = sqlalchemy.create_engine(config.DATABASE_URL)
metadata.create_all(engine)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       