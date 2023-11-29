from typing import Optional
import time

from models.abstracts.auth import AbsAuth
import models.database.dbtables as tables



class DBAuth(AbsAuth):
    @classmethod
    async def get(cls, username: str) -> list["AbsAuth"]:
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