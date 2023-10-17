from enum import Enum
from abc import ABCMeta, abstractmethod

from models import abstracts as abs
from models.database import dbtables
from models.database.dbmodels import *
from models.fdbmodels import *


class DBType(Enum):
    JSON = 1
    POSTGRE = 2



class DataStorage():
    __metaclass__ = ABCMeta

    type: DBType
    users: abs.AbsUser
    auth: abs.AbsAuth

    @abstractmethod
    async def getStorage(cls):
        "Return DataStorage object"



class DBDataStorage(DataStorage):
    database_url = "postgresql://postgres:toor@127.0.0.1:5432/phidb"

    @classmethod
    async def getStorage(cls):
        """
        """
        await dbtables.connect_database(cls.database_url)
        obj = cls()
        obj.users = DBUser
        return obj




class JsonDataStorage(DataStorage):
    storage_path = "jsondb/"

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