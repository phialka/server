from typing import BinaryIO
from uuid import UUID, uuid4
from hashlib import md5
from datetime import datetime
from typing import Optional

from private_chats.schemas import PrivateChat, PrivateMessage
from messages.schemas import Message, MessageCreate
from users.schemas import User

from private_chats.abstracts import PrivateChatRepo, PrivateChatFilter, PrivateMessageRepo, PrivateMessageFilter
from users.abstracts import UserRepo
from auth.abstracts import AuthDataRepo
from messages.abstracts import MessageRepo
from files.abstracts import FileRepo, FileStorage
from exceptions import NotFoundException, AccessDeniedException, ReceiverClosed

from users.use_caces import UserUseCases
from messages.use_cases import MessageUseCases



class PrivateChatUseCases():
    def __init__(
            self, 
            chat_repo: PrivateChatRepo,
            private_msg_repo: PrivateMessageRepo,
            user_repo: UserRepo,
            auth_repo: AuthDataRepo,
            file_repo: FileRepo,
            file_storage: FileStorage,
            message_uc: MessageUseCases
            ) -> None:
        self.__chat_repo: PrivateChatRepo = chat_repo
        self.__chat_msg_repo: PrivateMessageRepo = private_msg_repo
        self.__user_uc: UserUseCases = UserUseCases(
            user_repo=user_repo, 
            auth_repo=auth_repo,
            file_repo=file_repo,
            file_storage=file_storage
            )
        self.__msg_uc: MessageUseCases = message_uc

    
    def __hash(self, string: str) -> str:
        return md5(string.encode()).hexdigest()
    

    async def __get_or_create_private_chat(self, requester_id: UUID, user_id: UUID) -> PrivateChat:
        chats = await self.__chat_repo.get(filter=PrivateChatFilter(member_ids=[requester_id, user_id]))
        if len(chats) == 0:
            requester = await self.__user_uc.get_user_by_id(requester_id)
            user = await self.__user_uc.get_user_by_id(user_id)
            chat = await self.create_chat([requester, user])
            return chat
        return chats[0]
    

    async def __get_last_chat_sequence(self, chat_id: UUID) -> int:
        msgs = await self.__chat_msg_repo.get(filter=PrivateMessageFilter(chat_id=chat_id))

        return len(msgs) - 1
    

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
    

    async def create_private_message(
            self, 
            requester_id: UUID, 
            recipient_id: UUID, 
            msg_data: MessageCreate
            ) -> PrivateMessage:
        
        requester = await self.__user_uc.get_user_by_id(user_id=requester_id)
        recipient = await self.__user_uc.get_user_by_id(user_id=recipient_id)

        msg = await self.__msg_uc.create_message(msg_data=msg_data, author_id=requester_id)

        chat = await self.__get_or_create_private_chat(requester_id, recipient_id)

        private_msg = PrivateMessage(
            message = msg,
            chat_id = chat.chat_id,
            sequence = await self.__get_last_chat_sequence(chat_id=chat.chat_id)
        )

        await self.__chat_msg_repo.save(private_msg)

        recs = self.__msg_uc.user_msg_reseivers
        for r in recs:
            if (r.user_id == recipient_id) or (r.user_id == requester_id):
                try:
                    await r.send_message(msg=private_msg)
                except ReceiverClosed:
                    self.__msg_uc.delete_user_msg_receiver(user_id=r.user_id)

        return private_msg


    async def get_private_chat_messages(self, requester_id: UUID, chat_id: UUID, sequence_min: int, count: Optional[int] = 50) -> list[PrivateMessage]:
        chat = await self.get_chat_by_id(requester_id=requester_id, chat_id=chat_id)

        if requester_id not in [m.user_id for m in chat.members]:
            raise AccessDeniedException(msg='You dont have permission to access this chat. You are not chat member')

        msgs = await self.__chat_msg_repo.get(filter=PrivateMessageFilter(chat_id=chat_id, sequence_min=sequence_min))

        return msgs[0:count]
