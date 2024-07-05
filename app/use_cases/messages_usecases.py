from typing import BinaryIO
from uuid import UUID, uuid4
from hashlib import md5
from datetime import datetime
from typing import Optional

from entities import PrivateChat, Message, PrivateMessage, ChannelMessage, Attachment
from .datamodels.filters import MessageFilter, ChannelMessageFilter, PrivateMessageFilter, PrivateChatFilter
from .datamodels.creation_data import AttachmentCreate, MessageCerate


from .abstracts import PrivateChatRepo, MessageRepo, ChannelMessageRepo, PrivateMessageRepo, UserRepo, AuthDataRepo, FileRepo, ChannelRepo, ServerRepo, FileStorage
from use_cases.private_chat_usecases import PrivateChatUseCases
from use_cases.user_usecases import UserUseCases
from use_cases.files_usecases import FileUseCases
from use_cases.channel_usecases import ChannelUseCases
from .exceptions import UserAlreadyExist, UserTagAlreadyExist, ForbiddenError



class MessageUseCases():
    def __init__(
            self, 
            chat_repo: PrivateChatRepo, 
            msg_repo: MessageRepo, 
            chat_msg_repo: PrivateMessageRepo, 
            channel_msg_repo: ChannelMessageRepo,
            user_repo: UserRepo,
            auth_repo: AuthDataRepo,
            file_repo: FileRepo,
            channel_repo: ChannelRepo,
            server_repo: ServerRepo,
            file_storage: FileStorage
            ) -> None:
        self.__chat_repo: PrivateChatRepo = chat_repo
        self.__msg_repo: MessageRepo = msg_repo
        self.__chat_msg_repo: PrivateMessageRepo = chat_msg_repo
        self.__channel_msg_repo: ChannelMessageRepo = channel_msg_repo

        self.__user_uc: UserUseCases = UserUseCases(user_repo=user_repo, auth_repo=auth_repo)
        self.__chat_uc: PrivateChatUseCases = PrivateChatUseCases(chat_repo=self.__chat_repo)
        self.__file_uc: FileUseCases = FileUseCases(file_repo=file_repo, file_storage=file_storage)
        self.__channel_uc: ChannelUseCases = ChannelUseCases(file_uc=self.__file_uc, channel_repo=channel_repo, server_repo=server_repo)


    def __hash(self, string: str) -> str:
        return md5(string.encode()).hexdigest()


    async def __get_or_create_private_chat(self, requester_id: UUID, user_id: UUID):
        chats = await self.__chat_repo.get(filter=PrivateChatFilter(member_ids=[requester_id, user_id]))
        if len(chats) == 0:
            requester = await self.__user_uc.get_user_by_id(requester_id)
            user = await self.__user_uc.get_user_by_id(user_id)
            chat = await self.__chat_uc.create_chat(requester, user)
            return chat
        return chats[0]
    

    async def __create_attachment(self, attach_data: AttachmentCreate, message_id: UUID) -> Attachment:
        attach = Attachment(
            message_id = message_id,
            attach_type = attach_data.attach_type,
            file = await self.__file_uc.get_file_by_id(attach_data.file_id)
        )

        return attach
    

    async def __get_last_chat_sequence(self, chat_id: UUID) -> int:
        msgs = await self.__chat_msg_repo.get(filter=PrivateMessageFilter(chat_id=chat_id))

        return len(msgs) - 1
    

    async def __get_last_channel_sequence(self, channel_id: UUID) -> int:
        msgs = await self.__channel_msg_repo.get(filter=ChannelMessageFilter(channel_id=channel_id))

        return len(msgs) - 1


    async def __create_message(self, msg_data: MessageCerate, author_id: UUID) -> Message:
        message_id = uuid4()
        msg = Message(
            message_id = message_id,
            author_id = author_id,
            content = msg_data.content,
            reply_message_id = None,
            updated_at = None,
            created_at = datetime.now(),
            attachments = [
                await self.__create_attachment(adata, message_id)
                for adata in msg_data.attachments
            ]
        ) 

        return msg


    async def create_private_message(
            self, 
            requester_id: UUID, 
            recipient_id: UUID, 
            msg_data: MessageCerate
            ) -> PrivateMessage:
        
        msg = await self.__create_message(msg_data=msg_data, author_id=requester_id)

        await self.__msg_repo.save(msg)

        chat = await self.__get_or_create_private_chat(requester_id, recipient_id)

        private_msg = PrivateMessage(
            message = msg,
            chat_id = chat.chat_id,
            sequence = await self.__get_last_chat_sequence(chat_id=chat.chat_id)
        )

        await self.__chat_msg_repo.save(private_msg)

        return private_msg


    async def create_channel_message(
            self,
            requester_id: UUID,
            channel_id: UUID,
            msg_data: MessageCerate
            ) -> ChannelMessage:
        
        channel = await self.__channel_uc.get_channel_by_id(channel_id=channel_id)

        msg = await self.__create_message(msg_data=msg_data, author_id=requester_id)

        await self.__msg_repo.save(msg)

        channel_msg = ChannelMessage(
            message = msg,
            channel_id = channel_id,
            sequence = await self.__get_last_channel_sequence(channel_id)
        )

        await self.__channel_msg_repo.save(channel_msg)

        return channel_msg


    async def get_channel_messages(self, requester_id: UUID, channel_id: UUID, sequence_min: int, count: min) -> list[ChannelMessage]:
        
        channel = await self.__channel_uc.get_channel_by_id(channel_id=channel_id)

        msgs = await self.__channel_msg_repo.get(filter=ChannelMessageFilter(channel_id=channel_id, sequence_min=sequence_min))

        return msgs[0:count]


    async def get_private_chat_messages(self, requester_id: UUID, chat_id: UUID, sequence_min: int, count: int) -> list[PrivateMessage]:
        chat = await self.__chat_uc.get_chat_by_id(requester_id=requester_id, chat_id=chat_id)

        msgs = await self.__chat_msg_repo.get(filter=PrivateMessageFilter(chat_id=chat_id, sequence_min=sequence_min))

        return msgs[0:count]


    async def get_message_by_id(self, requester_id: UUID, message_id: UUID) -> Message:
        msgs = await self.__msg_repo.get(filter=MessageFilter(message_id=message_id))

        if len(msgs) == 0:
            raise

        return msgs[0]


    async def edit_message(self, requester_id: UUID, message_id: UUID, content: str) -> None:
        msgs = await self.__msg_repo.get(filter=MessageFilter(message_id=message_id))
        
        if len(msgs) == 0:
            raise

        if msgs[0].author_id != requester_id:
            raise ForbiddenError()
        
        await self.__msg_repo.update(filter=MessageFilter(message_id=message_id), content=content)

        return


    async def delete_message(self, requester_id: UUID, message_id: UUID) -> None:
        msgs = await self.__msg_repo.get(filter=MessageFilter(message_id=message_id))
        
        if len(msgs) == 0:
            raise

        if msgs[0].author_id != requester_id:
            raise ForbiddenError()
        
        await self.__msg_repo.delete(filter=MessageFilter(message_id=message_id))

        return

