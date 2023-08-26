import dbmodels
import time
from pydantic import BaseModel
from typing import Optional, Union



async def connect():
    database_ = dbmodels.database
    if not database_.is_connected:
        await database_.connect()
    dbmodels.tables_init()




class DataEntity(BaseModel):
    @classmethod
    def __from_dbmodel(cls, model: dbmodels.ormar.Model) -> "DataEntity":
        pass   

    @classmethod
    def __json_field_upd(cls, field: dict, **kwargs) -> dict:
        return {itm[0]:itm[1] if itm[0] not in kwargs or kwargs[itm[0]]==None else kwargs[itm[0]] for itm in field.items()}


    @classmethod
    async def get(cls, *args, **kwargs) -> list["DataEntity"]:
        pass


    @classmethod
    async def add(cls, *args, **kwargs) -> "DataEntity":
        pass


    @classmethod
    async def update(cls, *args, **kwargs) -> int:
        pass
    

    @classmethod
    async def delete(cls, *args, **kwargs) -> int:
        pass



class Auth(DataEntity):
    id: int
    user_id: int
    username: str
    userpass: str

    @classmethod
    def __from_dbmodel(cls, model: dbmodels.Auth) -> "Auth":
        return cls(
            id = model.id,
            user_id = model.user_id.id,
            username = model.username,
            userpass = model.userpass
            )


    @classmethod
    async def get(cls, user_id: int) -> list["Auth"]:
        response = await dbmodels.Auth.objects.all(user_id=user_id)
        return [cls.__from_dbmodel(auth) for auth in response]


    @classmethod
    async def add(
            cls, 
            user_id: int,
            username: str,
            userpass: int
            ) -> "Auth":
        auth = await dbmodels.Auth.objects.create(
            user_id = user_id,
            username = username,
            userpass = userpass
        )
        return cls.__from_dbmodel(auth)


    @classmethod
    async def update(cls) -> int:
        pass

    
    @classmethod
    async def delete(cls, auth_id: Optional[int] = None, user_id: Optional[int] = None) -> int:
        kwargset = {itm[0]:itm[1] for itm in {
            "id": auth_id, 
            "user_id": user_id}.items() if itm[1]!=None}
        response = await dbmodels.Auth.objects.filter(**kwargset).delete()
        return response



class User(DataEntity):
    id: int
    name: str
    shortname: str
    description: Optional[str]
    photo_id: Optional[int]
    last_time: int
    created_at: int


    @classmethod
    def __from_dbmodel(cls, model: dbmodels.User) -> "User":
        return cls(
            id = model.id, 
            name = model.info_.name, 
            shortname = model.info_.shortname,
            description = model.info_.description,
            photo_id = model.photo_file_id,
            last_time = model.last_visit,
            created_at = model.created_at
            )


    @classmethod
    async def get(cls, user_id: int) -> list["User"]:
        response = await dbmodels.User.objects.all(id=user_id)
        return [cls.__from_dbmodel(usr) for usr in response]


    @classmethod
    async def add(cls, name: str, shortname: str,  photo_id: Optional[int] = None, description: Optional[str] = None) -> "User":
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
        return cls.__from_dbmodel(usr)


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
        inf = cls.__json_field_upd(jsf_now.info_.dict(), name=name, shortname=shortname, description=description)
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





class File(DataEntity):
    class PhotoTypeInfo(BaseModel):
        width: int
        height: int

    class VideoTypeInfo(BaseModel):
        width: int
        height: int
        duration: int

    class AudioTypeInfo(BaseModel):
        duration: int

    id: int
    hash: str
    type: str
    size: int
    type_info: Optional[dict]
    location: str

    @classmethod
    def __from_dbmodel(cls, model: dbmodels.File) -> "File":
        return cls(
            id = model.id,
            hash = model.hash,
            type = model.mime_type,
            size = model.size,
            location = model.location,
            type_info = model.type_info_
            )


    @classmethod
    async def get(cls, file_id: int) -> list["File"]:
        response = await dbmodels.File.objects.all(id=file_id)
        return [cls.__from_dbmodel(file) for file in response]


    @classmethod
    async def add(
            cls, 
            hash: str,
            type: str,
            size: int,
            location: str,
            type_info: Optional[dict] = None
            ) -> "File":
        main_type = type.split("/")[0]
        tp_info = None
        if type_info != None:
            if main_type == "image":
                tp_info = cls.PhotoTypeInfo(**type_info).dict()
            elif main_type == "video":
                tp_info = cls.PhotoTypeInfo(**type_info).dict()
            elif main_type == "audio":
                tp_info = cls.PhotoTypeInfo(**type_info).dict()
        file = await dbmodels.File.objects.create(
            hash = hash,
            mime_type = type,
            size = size,
            type_info = tp_info,
            location = location
        )
        return cls.__from_dbmodel(file)


    @classmethod
    async def update(cls) -> int:
        pass

    
    @classmethod
    async def delete(cls, file_id: int) -> int:
        response = await dbmodels.File.objects.filter(id=file_id).delete()
        return response
    


