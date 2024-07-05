from abc import ABC, abstractmethod
from entities import ServerMember, User, File
from use_cases.datamodels.filters import ServerMemberFilter

from typing import Optional
from datetime import date
from uuid import uuid4

from database import tables



class SQLServerMemberRepo(ABC):
    def __init__(self) -> None:
        self.__table = tables.ServerMember


    def __serialize_filter(self, filter: ServerMemberFilter):
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

        if filter.server_id:
            query = __without_none(self.__table.server.id == filter.server_id)
        if filter.user_id:
            query = __without_none(self.__table.user.id == filter.user_id)

        return query


    async def save(self, member: ServerMember) -> bool:
        member = await self.__table.objects.create(
            id = uuid4(),
            server = member.server_id,
            user = member.user.user_id
        )

        return True


    async def get(self, filter: Optional[ServerMemberFilter] = None) -> list[ServerMember]:
        if filter:
            members = await self.__table.objects.select_related(['user', 'user__photo']).all(self.__serialize_filter(filter))
        else:
            members = await self.__table.objects.select_related(['user', 'user__photo']).all()
        members = [ServerMember(
            server_id=m.server.id, 
            user=User(
                user_id=m.user.id,
                name=m.user.name,
                description=m.user.description,
                tag=m.user.tag,
                birthdate=m.user.birthdate,
                photo=None if not m.user.photo else File(
                    file_id=m.user.photo.id,
                    download_id=m.user.photo.download_id,
                    size=m.user.photo.size,
                    hash=m.user.photo.hash,
                    mime_type=m.user.photo.hash,
                    upload_at=m.user.photo.upload_at
            ))) for m in members]
        return members


    async def update(self, filter: Optional[ServerMemberFilter] = None, **kwargs) -> int:
        pass


    async def delete(self, filter: Optional[ServerMemberFilter] = None) -> int:
        if filter:
            return await self.__table.objects.filter(self.__serialize_filter(filter)).delete()
        else:
            return await self.__table.objects.delete(each=True)