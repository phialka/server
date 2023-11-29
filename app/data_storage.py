from abc import ABCMeta, abstractmethod
from enum import Enum

from models.abstracts import *
from models.database import dbtables
from models.database import *
from models.json_db import *
import config
# from models.db_type import DBType


class DBType(Enum):
    JSON = 1
    POSTGRE = 2



class DataStorage():
    __metaclass__ = ABCMeta

    type: DBType
    users: AbsUser
    auth: AbsAuth

    @abstractmethod
    async def getStorage(cls):
        "Return DataStorage object"



class DBDataStorage(DataStorage):
    database_url = config.DATABASE_URL

    @classmethod
    async def getStorage(cls):
        """
        """
        await dbtables.connect_database(cls.database_url)
        obj = cls()
        obj.users = DBUser
        obj.auth = DBAuth
        return obj




class JsonDataStorage(DataStorage):
    storage_path = config.JSON_DB_PATH

    @classmethod
    async def getStorage(cls):
        """
        """
        obj = cls()
        obj.users = FDBUser.set_db(cls.storage_path + "users.json")
        return obj



async def getDataStorage(type: DBType) -> DataStorage:
    type_classes = {
        DBType.POSTGRE : DBDataStorage,
        DBType.JSON : JsonDataStorage
    }

    storage = await type_classes[type].getStorage()
    storage.type = type
    return storage