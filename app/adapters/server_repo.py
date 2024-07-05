from use_cases.abstracts import ServerRepo
from entities import Server, File
from use_cases.datamodels.filters import ServerFilter

from typing import Optional
from datetime import date

from database import tables



class SQLServerRepo(ServerRepo):

    def __init__(self) -> None:
        self.__table = tables.Server


    def __serialize_filter(self, filter: ServerFilter):
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
            query = __without_none(self.__table.id == filter.server_id)
        if filter.owner_id:
            query = __without_none(self.__table.owner.id == filter.owner_id)
        if filter.title_search_prompt:
            query = __without_none(self.__table.title.icontains(filter.title_search_prompt))
        if filter.description_search_prompt:
            query = __without_none(self.__table.description.icontains(filter.description_search_prompt))

        return query


    async def save(self, server: Server) -> bool:
        await self.__table.objects.create(
            id = server.server_id,
            owner = server.owner_id,
            title = server.title,
            description = server.description,
            created_at = server.created_at,
            logo = None if not server.logo else server.logo.file_id
        )

        return True


    async def get(self, filter: Optional[ServerFilter] = None) -> list[Server]:
        if filter:
            servers = await self.__table.objects.select_related('logo').all(self.__serialize_filter(filter))
        else:
            servers = await self.__table.objects.select_related('logo').all()
        servers = [Server(
            server_id = s.id,
            owner_id = s.owner.id,
            title = s.title,
            description = s.description,
            created_at = s.created_at,
            logo = None if not s.logo else File(
                file_id = s.logo.id,
                download_id = s.logo.download_id,
                size = s.logo.size,
                hash = s.logo.hash,
                mime_type = s.logo.mime_type,
                upload_at = s.logo.upload_at
            ))
            for s in servers
        ]
        return servers


    async def update(self, filter: Optional[ServerFilter] = None, **kwargs) -> int:
        if 'server_id' in kwargs:
            raise
        if 'logo' in kwargs:
            kwargs['logo'] = None if not kwargs['logo'] else kwargs['logo'].file_id
            
        if not filter:
            return await self.__table.objects.update(each=True, **kwargs)
        if filter:
            return await self.__table.objects.filter(self.__serialize_filter(filter)).update(**kwargs)


    async def delete(self, filter: Optional[ServerFilter] = None) -> int:
        if filter:
            return await self.__table.objects.filter(self.__serialize_filter(filter)).delete()
        else:
            return await self.__table.objects.delete(each=True)
