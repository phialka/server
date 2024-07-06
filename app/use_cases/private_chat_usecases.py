from typing import BinaryIO
from uuid import UUID, uuid4
from hashlib import md5
from datetime import datetime
from typing import Optional

from entities import PrivateChat, User
from .datamodels.filters import PrivateChatFilter
from .abstracts import PrivateChatRepo
from .exceptions import NotFoundException, AccessDeniedException



class PrivateChatUseCases():
    def __init__(self, chat_repo: PrivateChatRepo) -> None:
        self.__chat_repo: PrivateChatRepo = chat_repo

    
    def __hash(self, string: str) -> str:
        return md5(string.encode()).hexdigest()
    

    async def create_chat(self, members: list[User]) -> PrivateChat:
        chat = PrivateChat(
            chat_id = uuid4(),
            members = members
        )

        await self.__chat_repo.save(chat)

        return chat


    async def get_chat_by_id(self, requester_id: UUID, chat_id: UUID) -> PrivateChat:
        chats = await self.__chat_repo.get(filter=PrivateChatFilter(chat_id=chat_id))

        if len(chats) == 0:
            raise NotFoundException(msg='Private chat not found')

        chat = chats[0]

        if requester_id not in [m.user_id for m in chat.members]:
            raise AccessDeniedException(msg='You dont have permission access to this chat. You are not the chat member')

        return chat
    

    async def delete_chat(self, requester_id: UUID, chat_id: UUID):
        chat = await self.get_chat_by_id(requester_id, chat_id)

        await self.__chat_repo.delete(filter=PrivateChatFilter(chat_id=chat.chat_id))

        return


    async def get_chats_by_member(self, requester_id: UUID, user_id: UUID) -> list[PrivateChat]:
        if requester_id != user_id:
            raise AccessDeniedException(msg='You dont have permission access to this chats. You are not the chats member')
        
        chats = await self.__chat_repo.get(filter=PrivateChatFilter(member_ids=[user_id]))

        return chats
