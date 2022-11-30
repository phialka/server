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

        
   
class Server(ormar.Model):
    class Meta(BaseMeta):
        tablename = "server"
    id: int = ormar.Integer(primary_key=True)
    ip: int = ormar.Integer()
    port: int = ormar.Integer()
        

class ServerDataDistribution(ormar.Model):
    class Meta(BaseMeta):
        tablename = "server_data_distribution"
    id: int = ormar.Integer(primary_key=True)
    server_id: Server = ormar.ForeignKey(Server)
    conversation_id: = Conversation = ormar.ForeignKey(Conversation)
        
        
engine = sqlalchemy.create_engine(config.DATABASE_URL)
metadata.create_all(engine)


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
