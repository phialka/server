from use_cases.abstracts import UserRepo
from entities import User, UserFilter, File
from database import tables

from typing import Optional



class SQLUserRepo(UserRepo):

    def __init__(self) -> None:
        self.__table = tables.User


    def __serialize_filter(self, filter: UserFilter):
        """
        Amazing filter serialization from data model to ORMAR style
        """
        query = None

        def __without_none(somthing):
            if query:
                query = query and somthing
            else:
                query = somthing
            
        if filter.user_id:
            query = __without_none(self.__table.id == filter.user_id)
        if filter.name:
            query = __without_none(self.__table.name == filter.name)
        if filter.tag:
            query = __without_none(self.__table.tag == filter.tag)

        return query



    async def save(self, user: User) -> bool:
        await self.__table.objects.create(
            id = user.user_id,
            name = user.name,
            description = user.description,
            tag = user.tag,
            birthdate = user.birthdate,
            photo = None if not user.photo else user.photo.file_id
        )

        return True


    async def get(self, filter: Optional[UserFilter] = None) -> list[User]:
        if filter:
            users = await self.__table.objects.all(self.__serialize_filter(filter))
        else:
            users = await self.__table.objects.all()
        users = [User(
            user_id=u.id,
            name=u.name,
            description=u.description,
            tag=u.tag,
            birthdate=u.birthdate,
            photo=None if not u.photo else File(
                file_id=u.photo.id,
                download_id=u.photo.download_id,
                size=u.photo.size,
                hash=u.photo.hash,
                mime_type=u.photo.hash,
                upload_at=u.photo.upload_at
            ))
            for u in users
        ]
        return users



    async def update(self, filter: UserFilter, **kwargs) -> int:
        pass


    async def delete(self, filter: UserFilter) -> int:
        return await self.__table.objects.delete(self.__serialize_filter(filter))
