from typing import Optional

from users.schemas import User
from users.abstracts import UserRepo, UserFilter
from users.dbmodels import User as DBUser

from files.schemas import File



class SQLUserRepo(UserRepo):

    def __init__(self) -> None:
        self.__table = DBUser


    def __serialize_filter(self, filter: UserFilter):
        """
        Amazing filter serialization from data model to ORMAR style
        """
        query = None

        def __without_none(somthing, query = query):
            if query:
                query = somthing and query
            else:
                query = somthing
            return query
            
        if filter.user_id:
            query = __without_none(self.__table.id == filter.user_id)
        if filter.name:
            query = __without_none(self.__table.name == filter.name)
        if filter.tag:
            query = __without_none(self.__table.tag == filter.tag)
        if filter.name_search_prompt:
            query = __without_none(self.__table.name.icontains(filter.name_search_prompt))
        if filter.tag_search_prompt:
            query = __without_none(self.__table.tag.icontains(filter.tag_search_prompt))

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
            users = await self.__table.objects.select_related('photo').all(self.__serialize_filter(filter))
        else:
            users = await self.__table.objects.select_related('photo').all()
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


    async def update(self, filter: Optional[UserFilter] = None, **kwargs) -> int:
        if 'user_id' in kwargs:
            raise
        if 'photo' in kwargs:
            kwargs['photo'] = None if not kwargs['photo'] else kwargs['photo'].file_id
            
        if not filter:
            return await self.__table.objects.update(each=True, **kwargs)
        if filter:
            return await self.__table.objects.filter(self.__serialize_filter(filter)).update(**kwargs)


    async def delete(self, filter: Optional[UserFilter] = None) -> int:
        if filter:
            return await self.__table.objects.filter(self.__serialize_filter(filter)).delete()
        else:
            return await self.__table.objects.delete(each=True)
