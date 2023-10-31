from typing import Optional
import time

import models.abstracts as abs
import models.database.dbtables as tables



class DBUser(abs.AbsUser):
    @classmethod
    def __from_dbmodel(cls, model: tables.User) -> "abs.AbsUser":
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
    async def get(cls, user_id: int) -> list["abs.AbsUser"]:
        response = await tables.User.objects.all(id=user_id)
        return [cls.__from_dbmodel(usr) for usr in response]


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
    async def delete(cls, user_id: int) -> int:
        response = await tables.User.objects.filter(id=user_id).delete()
        return response



class DBAuth(abs.AbsAuth):
    @classmethod
    async def get(cls, username: str) -> list["abs.AbsAuth"]:
        auths = await tables.Auth.objects.all(username=username)
        return [cls(**a.dict(exclude={"user_id"}), user_id=a.user_id.id) for a in auths]


    @classmethod
    async def add(
            cls, user_id: int, username: str, userpass: int) -> int:
        new_auth = await tables.Auth.objects.create(user_id=user_id, username=username, userpass=userpass)
        return new_auth.id

    @classmethod
    async def update(cls, auth_id: int, username: Optional[str] = None, userpass: Optional[str] = None) -> int:
        args = {i[0]:i[1] for i in {"username":username, "userpass": userpass}.items() if i[1]!=None}
        upd_count = await tables.Auth.objects.filter(id=auth_id).update(**args)
        return upd_count


    @classmethod
    async def delete(cls, auth_id: Optional[int] = None, user_id: Optional[int] = None) -> int:
        args = {i[0]:i[1] for i in {"id":auth_id, "user_id": user_id}.items() if i[1]!=None}
        del_count = await tables.Auth.objects.filter(id=auth_id).delete(**args)
        return del_count