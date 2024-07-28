from typing import BinaryIO
from uuid import UUID, uuid4
from hashlib import md5
from datetime import datetime
from typing import Optional

from channels.schemas import Channel, ChannelMessage
from servers.schemas import Server
from messages.schemas import MessageCerate

from channels.abstracts import ChannelFilter, ChannelRepo, ChannelMessageRepo, ChannelMessageFilter
from servers.abstracts import ServerRepo, ServerFilter, ServerMemberRepo
from files.abstracts import FileRepo, FileStorage
from users.abstracts import UserRepo
from auth.abstracts import AuthDataRepo
from messages.abstracts import MessageRepo

from files.use_cases import FileUseCases
from servers.use_cases import ServerUseCases
from messages.use_cases import MessageUseCases
from users.use_caces import UserUseCases

from exceptions import NotFoundException, AccessDeniedException, IncorrectValueException, ReceiverClosed



class ChannelUseCases():
    def __init__(
            self, 
            channel_repo: ChannelRepo, 
            file_repo: FileRepo,
            file_storage: FileStorage,
            server_repo: ServerRepo,
            member_repo: ServerMemberRepo,
            user_repo: UserRepo,
            auth_repo: AuthDataRepo,
            channel_msg_repo: ChannelMessageRepo,
            messages_uc: MessageUseCases
            ) -> None:
        self.__channel_repo: ChannelRepo = channel_repo
        self.__channel_msg_repo: ChannelMessageRepo = channel_msg_repo

        self.__file_uc: FileUseCases = FileUseCases(file_repo, file_storage)
        self.__user_uc: UserUseCases = UserUseCases(
            user_repo=user_repo, 
            auth_repo=auth_repo,
            file_repo=file_repo,
            file_storage=file_storage
            )
        self.__msg_uc: MessageUseCases = messages_uc
        self.__server_uc = ServerUseCases(
            server_repo=server_repo,
            member_repo=member_repo,
            user_repo=user_repo,
            auth_repo=auth_repo,
            file_repo=file_repo,
            file_storage=file_storage
        )
    

    def __hash(self, string: str):
        return md5(string.encode()).hexdigest()
    

    async def _get_last_channel_sequence(self, channel_id: UUID) -> int:
        msgs = await self.__channel_msg_repo.get(filter=ChannelMessageFilter(channel_id=channel_id))

        return len(msgs)


    async def __check_requester_is_owner(self, requester_id: UUID, channel_id: UUID) -> None:
        channel = await self.get_channel_by_id(channel_id)
        server = await self.__server_uc.get_server_by_id(server_id=channel.server_id)

        if server.owner_id != requester_id:
            raise AccessDeniedException(msg='You dont have permission for this action. You are not the server owner')


    async def create_channel(self, requester_id: UUID, server_id: UUID, title: str, description: Optional[str] = None) -> Channel:
        server = await self.__server_uc.get_server_by_id(server_id=server_id)

        if server.owner_id != requester_id:
            raise AccessDeniedException(msg='You dont have permission for channel creation. You are not the server owner')

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
            raise NotFoundException(msg='Channel not found')
        
        return channels[0]
    

    async def edit_channel(self, channel_id: UUID, requester_id: UUID, new_title: Optional[str] = None, new_description: Optional[str] = None) -> Channel:
        await self.__check_requester_is_owner(requester_id=requester_id, channel_id=channel_id)
        channel = await self.get_channel_by_id(channel_id=channel_id)

        fields_to_update = dict()
        if new_title:
            fields_to_update['title'] = new_title
        if new_description:
            fields_to_update['description'] = new_description

        if len(fields_to_update) == 0:
            raise IncorrectValueException(msg='There are no fields to update')

        await self.__channel_repo.update(filter=ChannelFilter(channel_id=channel_id), **fields_to_update)
        return await self.get_channel_by_id(channel_id)


    async def delete_channel(self, requester_id: UUID, channel_id: UUID) -> bool:
        await self.__check_requester_is_owner(requester_id=requester_id, channel_id=channel_id)
        channel = await self.get_channel_by_id(channel_id=channel_id)
        
        await self.__channel_repo.delete(filter=ChannelFilter(channel_id=channel_id))

        return True
    

    async def set_channel_logo(self, channel_id: UUID, requester_id: UUID, logo: BinaryIO):
        await self.__check_requester_is_owner(requester_id=requester_id, channel_id=channel_id)
        channel = await self.get_channel_by_id(channel_id=channel_id)
        
        channel_logo = await self.__file_uc.upload_file(logo)

        await self.__channel_repo.update(filter=ChannelFilter(channel_id=channel_id), logo=channel_logo)

        return channel_logo


    async def delete_channel_logo(self, channel_id: UUID, requester_id: UUID):
        await self.__check_requester_is_owner(requester_id=requester_id, channel_id=channel_id)
        channel = await self.get_channel_by_id(channel_id=channel_id)
        
        await self.__channel_repo.update(filter=ChannelFilter(channel_id=channel_id), logo=None)

        return True
    
    
    async def get_channels_by_server_id(self, requester_id: UUID, server_id: UUID) -> list[Channel]:
        if requester_id not in [m.user_id for m in await self.__server_uc.get_server_members(server_id=server_id)]:
            raise AccessDeniedException(msg='You dont have permission to get channels from this server. You are not server member')
        
        channels = await self.__channel_repo.get(filter=ChannelFilter(server_id=server_id))
        return channels


    async def create_channel_message(
            self,
            requester_id: UUID,
            channel_id: UUID,
            msg_data: MessageCerate
            ) -> ChannelMessage:
        
        requester = await self.__user_uc.get_user_by_id(user_id=requester_id)
        channel = await self.get_channel_by_id(channel_id=channel_id)

        msg = await self.__msg_uc.create_message(msg_data=msg_data, author_id=requester_id)

        channel_msg = ChannelMessage(
            message = msg,
            channel_id = channel_id,
            sequence = await self._get_last_channel_sequence(channel_id)
        )

        await self.__channel_msg_repo.save(channel_msg)

        member_ids = [m.user_id for m in await self.__server_uc.get_server_members(server_id=channel.server_id, count=100000)]
        
        for rec in self.__msg_uc.user_msg_reseivers:
            if rec.user_id in member_ids:
                await rec.send_message(msg=channel_msg)
                
        return channel_msg


    async def get_channel_messages(self, requester_id: UUID, channel_id: UUID, sequence_min: int, count: Optional[int] = 50) -> list[ChannelMessage]:
        
        channel = await self.get_channel_by_id(channel_id=channel_id)

        msgs = await self.__channel_msg_repo.get(filter=ChannelMessageFilter(channel_id=channel_id, sequence_min=sequence_min))

        return msgs[0:count]
