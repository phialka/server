from typing import Optional
import time

from models.abstracts.user import AbsUser
import models.database.dbtables as tables
from models.filter import ConditionTreeNode, PostgreConditionTranslator


class DBUser(AbsUser):

    _condition_translator = PostgreConditionTranslator
    _fields_display = {
        AbsUser._F.id.content : tables.User.id,
        AbsUser._F.name.content : tables.User.name,
        AbsUser._F.shortname.content : tables.User.shortname,
        AbsUser._F.description.content : tables.User.description,
        AbsUser._F.photo_id.content : tables.User.photo_file_id.id,
        AbsUser._F.last_time.content : tables.User.last_visit,
        AbsUser._F.created_at.content : tables.User.created_at
    }

    @classmethod
    def __from_dbmodel(cls, model: tables.User) -> "AbsUser":
        return cls(
            id = model.id, 
            name = model.name, 
            shortname = model.shortname,
            description = model.description,
            photo_id = [file.id if file!=None else None for file in (model.photo_file_id, )][0],
            last_time = model.last_visit,
            created_at = model.created_at
            )


    @classmethod
    async def get(cls, filter: ConditionTreeNode = None) -> list["AbsUser"]:
        if type(filter) == type(None):
            targets = await tables.User.objects.all()
        else: 
            targets = await tables.User.objects.all(cls._condition_translator.build_condition(filter, cls._fields_display))
        return [cls.__from_dbmodel(usr) for usr in targets]


    @classmethod
    async def add(cls, name: str, shortname: str,  photo_id: Optional[int] = None, description: Optional[str] = None) -> int:
        usr = await tables.User.objects.create(
            photo_file_id = photo_id,
            last_visit = time.time(),
            created_at = time.time(),
            settings = {},
            info = tables.User.Info(
                name = name,
                shortname = shortname,
                description = description,
                photo_file_id = photo_id,
            ).dict()
        )
        return usr.id
    

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

        jsf_now = await tables.User.objects.get(id=id)
        inf = cls._json_field_upd(jsf_now.info_.dict(), name=name, shortname=shortname, description=description)
        kwargset = {itm[0]:itm[1] for itm in {
            "info": inf,
            "photo_file_id": photo_id,
            "last_visit": last_time
            }.items() if itm[1]!=None}
        
        upd_usr = await tables.User.objects.filter(id=id).update(**kwargset)
        return upd_usr

    
    @classmethod
    async def delete(cls, filter: ConditionTreeNode) -> int:
        # response = await tables.User.objects.filter(id=user_id).delete()
        # return response
        pass
