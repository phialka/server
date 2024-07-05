from use_cases.abstracts import ChannelRepo
from entities import Channel, File
from use_cases.datamodels.filters import ChannelFilter

from typing import Optional
from datetime import date

from database import tables



class SQLChannelRepo(ChannelRepo):

    def __init__(self) -> None:
        self.__table = tables.Channel


    def __serialize_filter(self, filter: ChannelFilter):
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

        if filter.channel_id:
            query = __without_none(self.__table.id == filter.channel_id)
        if filter.server_id:
            query = __without_none(self.__table.server.id == filter.server_id)

        return query


    async def save(self, channel: Channel) -> bool:
        await self.__table.objects.create(
            id = channel.channel_id,
            server = channel.server_id,
            title = channel.title,
            description = channel.description,
            created_at = channel.created_at,
            logo = None if not channel.logo else channel.logo.file_id
        )

        return True


    async def get(self, filter: Optional[ChannelFilter] = None) -> list[Channel]:
        if filter:
            channels = await self.__table.objects.select_related('logo').all(self.__serialize_filter(filter))
        else:
            channels = await self.__table.objects.select_related('logo').all()
        channels = [Channel(
            channel_id = c.id,
            server_id = c.server.id,
            title = c.title,
            description = c.description,
            created_at = c.created_at,
            logo = None if not c.logo else File(
                file_id = c.logo.id,
                download_id = c.logo.download_id,
                size = c.logo.size,
                hash = c.logo.hash,
                mime_type = c.logo.mime_type,
                upload_at = c.logo.upload_at
            ))
            for c in channels
        ]
        return channels


    async def update(self, filter: Optional[ChannelFilter] = None, **kwargs) -> int:
        if 'channel_id' in kwargs:
            raise
        if 'logo' in kwargs:
            kwargs['logo'] = None if not kwargs['logo'] else kwargs['logo'].file_id
            
        if not filter:
            return await self.__table.objects.update(each=True, **kwargs)
        if filter:
            return await self.__table.objects.filter(self.__serialize_filter(filter)).update(**kwargs)


    async def delete(self, filter: Optional[ChannelFilter] = None) -> int:
        if filter:
            return await self.__table.objects.filter(self.__serialize_filter(filter)).delete()
        else:
            return await self.__table.objects.delete(each=True)
