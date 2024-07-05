from typing import BinaryIO
from uuid import UUID, uuid4
from hashlib import md5
from datetime import datetime
from typing import Optional

from entities import PrivateChat, User
from .datamodels.filters import PrivateChatFilter
from .abstracts import PrivateChatRepo
from .exceptions import UserAlreadyExist, UserTagAlreadyExist, ForbiddenError



class PrivateChatUseCases():
    def __init__(self, chat_repo: PrivateChatRepo) -> None:
        self.__chat_repo: PrivateChatRepo = chat_repo

    
    def __hash(self, string: str) -> str:
        return md5(string.encode()).hexdigest()
    

    # async def __check_requester_is_owner(self, requester_id: UUID, channel_id: UUID) -> None:
    #     channel = await self.get_channel_by_id(channel_id)
    #     servers = await self.__server_repo.get(filter=ServerFilter(server_id=channel.server_id))

    #     if servers[0].owner_id != requester_id:
    #         raise ForbiddenError()


    async def create_chat(self, members: list[User]):
        chat = PrivateChat(
            chat_id = uuid4(),
            members = members
        )

        await self.__chat_repo.save(chat)

        return


    async def get_chat_by_id(self, requester_id: UUID, chat_id: UUID) -> PrivateChat:
        chats = await self.__chat_repo.get(filter=PrivateChatFilter(chat_id=chat_id))

        if len(chats) == 0:
            raise

        chat = chats[0]

        if requester_id not in [m.user_id for m in chat.members]:
            raise

        return chat
    

    async def delete_chat(self, requester_id: UUID, chat_id: UUID):
        chat = await self.get_chat_by_id(requester_id, chat_id)
        await self.__chat_repo.delete(filter=PrivateChatFilter(chat_id=chat.chat_id))

        return


    async def get_chats_by_member(self, user_id: UUID) -> list[PrivateChat]:
        chats = await self.__chat_repo.get(filter=PrivateChatFilter(member_ids=[user_id]))

        return chats
    

    
