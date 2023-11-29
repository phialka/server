from typing import Optional
import time

import pysondb

from models.abstracts.user import AbsUser
from models.filter import ConditionTreeNode, JsondbConditionTranslator



class FDBUser(AbsUser):
    
    _db: pysondb.getDb
    _condition_translator = JsondbConditionTranslator

    @classmethod
    def set_db(cls, path: str):
        """
        """
        cls._db = pysondb.getDb(path)
        return cls
    

    @classmethod
    def _get_all_models(cls):
        return cls._db.getAll()


    @classmethod
    async def get(cls, filter: ConditionTreeNode = None) -> list["AbsUser"]:
        if type(filter) == type(None):
            targets = cls._get_all_models()
        else: 
            targets = cls._condition_translator.build_condition(filter, cls._get_all_models())
        return [cls(**u) for u in targets]


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
            filter: ConditionTreeNode,
            name: Optional[str] = None, 
            shortname: Optional[str] = None,  
            photo_id: Optional[int] = None, 
            description: Optional[str] = None,
            last_time: Optional[int] = None
            ) -> int:
        target_ids = [obj['id'] for obj in cls._get_query_targets(filter)]
        
        for id in target_ids:
            cls._db.updateById(id, )

    
    @classmethod
    async def delete(cls, filter: ConditionTreeNode) -> int:
        target_ids = [obj['id'] for obj in cls._get_query_targets(filter)]
        for id in target_ids:
            cls._db.deleteById(id)
        return len(target_ids)


