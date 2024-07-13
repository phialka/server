from typing import BinaryIO
from uuid import UUID, uuid4
from hashlib import md5
from datetime import datetime
from typing import Optional

from entities import Server, ServerMember, User, Channel
from .datamodels.filters import ServerFilter, ServerMemberFilter, ChannelFilter, UserFilter
from .abstracts import ServerRepo, ServerMemberRepo, ChannelRepo
from .exceptions import NotFoundException, AccessDeniedException

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
            raise NotFoundException(msg='Server not found')
        
        return servers[0]
    

    async def edit_server(self, server_id: UUID, requester_id: UUID, new_title: Optional[str] = None, new_description: Optional[str] = None) -> None:
        server_before_edit = await self.get_server_by_id(server_id)

        if requester_id != server_before_edit.owner_id:
            raise AccessDeniedException(msg='You dont have permission to edit this server')

        fields_to_update = dict()
        if new_title:
            fields_to_update['title'] = new_title
        if new_description:
            fields_to_update['description'] = new_description
        if len(fields_to_update) == 0:
            raise

        await self.__server_repo.update(filter=ServerFilter(server_id=server_id), **fields_to_update)
        return


    async def delete_server(self, requester_id: UUID, server_id: UUID) -> None:
        server = await self.get_server_by_id(server_id)

        if requester_id != server.owner_id:
            raise AccessDeniedException(msg='You dont have permission to delete this server')
        
        await self.__server_repo.delete(filter=ServerFilter(server_id=server_id))

        return
    

    async def set_server_logo(self, server_id: UUID, requester_id: UUID, logo: BinaryIO) -> None:
        server = await self.get_server_by_id(server_id)

        if requester_id != server.owner_id:
            raise AccessDeniedException(msg='You dont have permission to edit this server')
        
        server_logo = await self.__file_uc.upload_file(logo)

        await self.__server_repo.update(filter=ServerFilter(server_id=server_id), logo=server_logo)

        return 


    async def delete_server_logo(self, server_id: UUID, requester_id: UUID) -> None:
        server = await self.get_server_by_id(server_id)

        if requester_id != server.owner_id:
            raise AccessDeniedException(msg='You dont have permission to edit this server')
        
        await self.__server_repo.update(filter=ServerFilter(server_id=server_id), logo=None)

        return


    async def get_server_members(self, server_id: UUID, count: Optional[int] = 50, offset: Optional[int] = 0) -> list[User]:
        members = await self.__member_repo.get(filter=ServerMemberFilter(server_id=server_id))
        return [m.user for m in members][offset:offset+count]


    async def get_channels(self, requester_id: UUID, server_id: UUID) -> list[Channel]:
        if requester_id not in [m.user_id for m in await self.get_server_members(server_id=server_id)]:
            raise AccessDeniedException(msg='You dont have permission to get channels from this server. You are not server member')
        
        channels = await self.__channel_repo.get(filter=ChannelFilter(server_id=server_id))
        return channels


    async def get_user_servers(self, user_id: UUID) -> list[Server]:
        user = await self.__user_uc.get_user_by_id(user_id=user_id)

        members = await self.__member_repo.get(filter=ServerMemberFilter(user_id=user_id))

        server_ids = [m.server_id for m in members]

        servers = []
        for server_id in server_ids:
            servers.append(await self.get_server_by_id(server_id=server_id))

        return servers


    async def search_servers_by_prompt(self, prompt: str, count: Optional[int] = 10, offset: Optional[int] = None) -> list[Server]:
        servers = await self.__server_repo.get(filter=ServerFilter(title_search_prompt=prompt))

        return servers[offset:offset+count]
    

    async def user_join_to_server(self, requester_id: UUID, server_id: UUID) -> None:
        user = await self.__user_uc.get_user_by_id(user_id=requester_id)
        server = await self.get_server_by_id(server_id=server_id)

        new_member = ServerMember(server_id=server_id, user=user)

        await self.__member_repo.save(new_member)

        return
    

    async def invite_user_to_server(self, requester_id: UUID, user_id: UUID, server_id: UUID) -> None:
        user = await self.__user_uc.get_user_by_id(user_id=user_id)
        server = await self.get_server_by_id(server_id=server_id)

        server_members_like_requester = await self.__member_repo.get(filter=ServerMemberFilter(user_id=requester_id))

        if len(server_members_like_requester) == 0:
            raise AccessDeniedException(msg='You dont have permission to invite users to this server. You are not server member')

        new_member = ServerMember(server_id=server_id, user=user)

        await self.__member_repo.save(new_member)

        return
