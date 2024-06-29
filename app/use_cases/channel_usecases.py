from typing import BinaryIO
from uuid import UUID, uuid4
from hashlib import md5
from datetime import datetime
from typing import Optional

from entities import Channel, ChannelFilter, ServerFilter
from .abstracts import ChannelRepo, ServerRepo
from .exceptions import UserAlreadyExist, UserTagAlreadyExist, ForbiddenError

from use_cases.files_usecases import FileUseCases



class ChannelUseCases():
    def __init__(self, channel_repo: ChannelRepo, server_repo: ServerRepo, file_uc: FileUseCases) -> None:
        self.__server_repo: ServerRepo = server_repo
        self.__channel_repo: ChannelRepo = channel_repo
        self.__file_uc: FileUseCases = file_uc

    
    def __hash(self, string: str):
        return md5(string.encode()).hexdigest()
    

    async def __check_requester_is_owner(self, requester_id: UUID, channel_id: UUID) -> None:
        channel = await self.get_channel_by_id(channel_id)
        servers = await self.__server_repo.get(filter=ServerFilter(server_id=channel.server_id))

        if servers[0].owner_id != requester_id:
            raise ForbiddenError()


    async def create_channel(self, requester_id: UUID, server_id: UUID, title: str, description: Optional[str] = None) -> Channel:
        servers = await self.__server_repo.get(filter=ServerFilter(server_id=server_id))

        if len(servers) == 0:
            raise

        if servers[0].owner_id != requester_id:
            raise ForbiddenError()

        channel = Channel(
            channel_id = uuid4(),
            server_id = server_id,
            title = title,
            description = description,
            logo = None,
            created_at = datetime.now()
        )

        await self.__channel_repo.save(channel)

        return channel
    

    async def get_channel_by_id(self, channel_id: UUID) -> Channel:
        channels = await self.__channel_repo.get(filter=ChannelFilter(channel_id=channel_id))

        if len(channels) == 0:
            raise
        
        return channels[0]
    

    async def edit_channel(self, channel_id: UUID, requester_id: UUID, new_title: Optional[str] = None, new_description: Optional[str] = None) -> Channel:
        await self.__check_requester_is_owner(requester_id=requester_id, channel_id=channel_id)

        fields_to_update = dict()
        if new_title:
            fields_to_update['title'] = new_title
        if new_description:
            fields_to_update['description'] = new_description

        if len(fields_to_update) == 0:
            raise

        await self.__channel_repo.update(filter=ChannelFilter(channel_id=channel_id), **fields_to_update)
        return await self.get_channel_by_id(channel_id)


    async def delete_channel(self, requester_id: UUID, channel_id: UUID) -> bool:
        await self.__check_requester_is_owner(requester_id=requester_id, channel_id=channel_id)
        
        await self.__channel_repo.delete(filter=ChannelFilter(channel_id=channel_id))

        return True
    

    async def set_channel_logo(self, channel_id: UUID, requester_id: UUID, logo: BinaryIO):
        await self.__check_requester_is_owner(requester_id=requester_id, channel_id=channel_id)
        
        channel_logo = await self.__file_uc.upload_file(logo)

        await self.__channel_repo.update(filter=ChannelFilter(channel_id=channel_id), logo=channel_logo)

        return channel_logo


    async def delete_channel_logo(self, channel_id: UUID, requester_id: UUID):
        await self.__check_requester_is_owner(requester_id=requester_id, channel_id=channel_id)
        
        await self.__channel_repo.update(filter=ChannelFilter(channel_id=channel_id), logo=None)

        return True
