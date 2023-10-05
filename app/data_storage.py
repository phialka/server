from abc import ABCMeta, abstractmethod, abstractproperty
import time
from typing import Optional
from pydantic import BaseModel

import pysondb

import dbmodels



class AbsUser(BaseModel):
    __metaclass__ = ABCMeta

    id: int
    name: str
    shortname: str
    description: Optional[str]
    photo_id: Optional[int]
    last_time: int
    created_at: int

    @abstractmethod
    async def get(cls, user_id: int) -> list["AbsUser"]:
        "Get User"

    @abstractmethod
    async def add(cls, name: str, shortname: str,  photo_id: Optional[int] = None, description: Optional[str] = None) -> "AbsUser":
        "Add User"

    @abstractmethod
    async def update(
            cls, 
            id: int,
            name: Optional[str] = None, 
            shortname: Optional[str] = None,  
            photo_id: Optional[int] = None, 
            description: Optional[str] = None,
            last_time: Optional[int] = None
            ) -> int:
        "Update User"

    @abstractmethod
    async def delete(cls, user_id: int) -> int:
        "Delete User"



class DBUser(AbsUser):
    @classmethod
    def __from_dbmodel(cls, model: dbmodels.User) -> "AbsUser":
        return cls(
            id = model.id, 
            name = model.info_.name, 
            shortname = model.info_.shortname,
            description = model.info_.description,
            photo_id = [file.id if file!=None else None for file in (model.photo_file_id, )][0],
            last_time = model.last_visit,
            created_at = model.created_at
            )


    @classmethod
    async def get(cls, user_id: int) -> list["AbsUser"]:
        response = await dbmodels.User.objects.all(id=user_id)
        return [cls.__from_dbmodel(usr) for usr in response]


    @classmethod
    async def add(cls, name: str, shortname: str,  photo_id: Optional[int] = None, description: Optional[str] = None) -> "AbsUser":
        usr = await dbmodels.User.objects.create(
            photo_file_id = photo_id,
            last_visit = time.time(),
            created_at = time.time(),
            settings = {},
            info = dbmodels.User.Info(
                name = name,
                shortname = shortname,
                description = description,
                photo_file_id = photo_id,
            ).dict()
        )
        return [cls.__from_dbmodel(usr)]


    @classmethod
    async def update(
            cls, 
            id: int,
            name: Optional[str] = None, 
            shortname: Optional[str] = None,  
            photo_id: Optional[int] = None, 
            description: Optional[str] = None,
            last_time: Optional[int] = None
            ) -> int:

        jsf_now = await dbmodels.User.objects.get(id=id)
        inf = cls._json_field_upd(jsf_now.info_.dict(), name=name, shortname=shortname, description=description)
        kwargset = {itm[0]:itm[1] for itm in {
            "info": inf,
            "photo_file_id": photo_id,
            "last_visit": last_time
            }.items() if itm[1]!=None}
        
        upd_usr = await dbmodels.User.objects.filter(id=id).update(**kwargset)
        return upd_usr

    
    @classmethod
    async def delete(cls, user_id: int) -> int:
        response = await dbmodels.User.objects.filter(id=user_id).delete()
        return response
    


class FDBUser(AbsUser):
    
    _db: pysondb.getDb

    @classmethod
    def set_db(cls, path: str):
        """
        
        """
        cls._db = pysondb.getDb(path)
        return cls

    @classmethod
    async def get(cls, user_id: int) -> list["AbsUser"]:
        return [cls(**u) for u in cls._db.getBy({"id": user_id})]


    @classmethod
    async def add(cls, name: str, shortname: str,  photo_id: Optional[int] = None, description: Optional[str] = None) -> "AbsUser":
        id = cls._db.add({
            "name": name,
            "shortname": shortname,
            "photo_id": photo_id,
            "description": description,
            "last_time": time.time(),
            "created_at": time.time()
        })
        return await cls.get(id)


    @classmethod
    async def update(
            cls, 
            id: int,
            name: Optional[str] = None, 
            shortname: Optional[str] = None,  
            photo_id: Optional[int] = None, 
            description: Optional[str] = None,
            last_time: Optional[int] = None
            ) -> int:
        pass

    
    @classmethod
    async def delete(cls, user_id: int) -> int:
        pass



class AbsAuth(BaseModel):
    __metaclass__ = ABCMeta

    id: int
    user_id: int
    username: str
    userpass: str

    @abstractmethod
    async def get(cls, user_id: int) -> list["AbsAuth"]:
        "Get Auth"

    @abstractmethod
    async def add(
            cls, user_id: int, username: str, userpass: int) -> "AbsAuth":
        "Add Auth"

    @abstractmethod
    async def update(cls) -> int:
        "Update Auth"

    @abstractmethod
    async def delete(cls, auth_id: Optional[int] = None, user_id: Optional[int] = None) -> int:
        "Delete Auth"




class DataStorage():
    file_storage_path = "jsondb/"
    database_url = "postgresql://postgres:toor@127.0.0.1:5432/phidb"

    def __init__(self, db_type: str, users: AbsUser) -> None:
        self.type: str = db_type
        self.users: AbsUser = users


    @classmethod
    async def getStorage(cls, type: str):
        """
        """
        if type == "postgre":
            await dbmodels.connect_database(cls.database_url)
            return cls(
                db_type = type,
                users = DBUser
            )

        if type == "json":
            return cls(
                db_type = type,
                users = FDBUser.set_db(cls.file_storage_path + "users.json")
            )

