from typing import Optional
import time

import pysondb

import models.abstracts as abs



class FDBUser(abs.AbsUser):
    
    _db: pysondb.getDb

    @classmethod
    def set_db(cls, path: str):
        """
        """
        cls._db = pysondb.getDb(path)
        return cls


    @classmethod
    async def get(cls, user_id: int) -> list["abs.AbsUser"]:
        return [cls(**u) for u in cls._db.getBy({"id": user_id})]


    @classmethod
    async def add(cls, name: str, shortname: str,  photo_id: Optional[int] = None, description: Optional[str] = None) -> int:
        id = cls._db.add({
            "name": name,
            "shortname": shortname,
            "photo_id": photo_id,
            "description": description,
            "last_time": time.time(),
            "created_at": time.time()
        })
        return id


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


