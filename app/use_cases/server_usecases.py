from typing import BinaryIO
from uuid import UUID, uuid4
from hashlib import md5
from datetime import datetime
from typing import Optional

from entities import Server, ServerFilter, ServerMember, ServerMemberFilter, User, Channel, ChannelFilter, UserFilter
from .abstracts import ServerRepo, ServerMemberRepo, ChannelRepo
from .exceptions import UserAlreadyExist, UserTagAlreadyExist, ForbiddenError

from use_cases.files_usecases import FileUseCases
from use_cases.user_usecases import UserUseCases



class ServerUseCases():
    def __init__(self, server_repo: ServerRepo, member_repo: ServerMemberRepo, channel_repo: ChannelRepo, user_uc: UserUseCases, file_uc: FileUseCases) -> None:
        self.__server_repo: ServerRepo = server_repo
        self.__member_repo: ServerMemberRepo = member_repo
        self.__channel_repo: ChannelRepo = channel_repo
        self.__user_uc: UserUseCases = user_uc
        self.__file_uc: FileUseCases = file_uc

    
    def __hash(self, string: str):
        return md5(string.encode()).hexdigest()


    async def create_server(self, owner_id: UUID, title: str, description: Optional[str] = None) -> Server:
        owner = await self.__user_uc.get_user_by_id(owner_id)

        server = Server(
            server_id = uuid4(),
            owner_id = owner_id,
            title = title,
            description = description,
            logo = None,
            created_at = datetime.now()
        )

        await self.__server_repo.save(server)
        await self.__member_repo.save(ServerMember(server_id=server.server_id, user=owner))

        return server
    

    async def get_server_by_id(self, server_id: UUID) -> Server:
        servers = await self.__server_repo.get(filter=ServerFilter(server_id=server_id))

        if len(servers) == 0:
            raise
        
        return servers[0]
    

    async def edit_server(self, server_id: UUID, requester_id: UUID, new_title: Optional[str] = None, new_description: Optional[str] = None) -> Server:
        server_before_edit = await self.get_server_by_id(server_id)

        if requester_id != server_before_edit.owner_id:
            raise ForbiddenError()
        else:
            fields_to_update = dict()
            if new_title:
                fields_to_update['title'] = new_title
            if new_description:
                fields_to_update['description'] = new_description
            if len(fields_to_update) == 0:
                raise

        await self.__server_repo.update(filter=ServerFilter(server_id=server_id), **fields_to_update)
        return await self.get_server_by_id(server_id)


    async def delete_server(self, requester_id: UUID, server_id: UUID) -> bool:
        server = await self.get_server_by_id(server_id)

        if requester_id != server.owner_id:
            raise ForbiddenError()
        
        await self.__server_repo.delete(filter=ServerFilter(server_id=server_id))

        return True
    

    async def set_server_logo(self, server_id: UUID, requester_id: UUID, logo: BinaryIO):
        server = await self.get_server_by_id(server_id)

        if requester_id != server.owner_id:
            raise ForbiddenError()
        
        server_logo = await self.__file_uc.upload_file(logo)

        await self.__server_repo.update(filter=ServerFilter(server_id=server_id), logo=server_logo)

        return server_logo


    async def delete_server_logo(self, server_id: UUID, requester_id: UUID):
        server = await self.get_server_by_id(server_id)

        if requester_id != server.owner_id:
            raise ForbiddenError()
        
        await self.__server_repo.update(filter=ServerFilter(server_id=server_id), logo=None)

        return True


    async def get_server_members(self, server_id: UUID, count: Optional[int] = 100, offset: Optional[int] = 0) -> list[User]:
        members = await self.__member_repo.get(filter=ServerMemberFilter(server_id=server_id))
        return [m.user for m in members]


    async def get_channels(self, server_id: UUID) -> list[Channel]:
        channels = await self.__channel_repo.get(filter=ChannelFilter(server_id=server_id))
        return channels