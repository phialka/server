from typing import BinaryIO
from uuid import UUID, uuid4
from hashlib import md5
from datetime import datetime
from typing import Optional

from messages.schemas import Message, Attachment, MessageCerate, AttachmentCreate

from messages.abstracts import MessageRepo, MessageFilter
from files.abstracts import FileRepo, FileStorage
from auth.abstracts import AuthDataRepo
from users.abstracts import UserRepo, UserMsgReceiver

from users.use_caces import UserUseCases
from files.use_cases import FileUseCases

from exceptions import NotFoundException, AccessDeniedException



class MessageUseCases():
    def __init__(
            self, 
            msg_repo: MessageRepo, 
            file_repo: FileRepo,
            file_storage: FileStorage
            ) -> None:
        self.__msg_repo: MessageRepo = msg_repo
        self.__file_uc: FileUseCases = FileUseCases(file_repo=file_repo, file_storage=file_storage)

        self.__user_msg_receivers: list[UserMsgReceiver] = []


    def __hash(self, string: str) -> str:
        return md5(string.encode()).hexdigest()
    

    async def __create_attachment(self, attach_data: AttachmentCreate, message_id: UUID) -> Attachment:
        attach = Attachment(
            message_id = message_id,
            attach_type = attach_data.attach_type,
            file = await self.__file_uc.get_file_by_id(attach_data.file_id)
        )

        return attach
    

    @property
    def user_msg_reseivers(self):
        return self.__user_msg_receivers


    def add_user_msg_receiver(self, rec: UserMsgReceiver):
        self.__user_msg_receivers.append(rec)


    def delete_user_msg_receiver(self, user_id: UUID):
        self.__user_msg_receivers = [rec for rec in self.__user_msg_receivers if rec.user_id != user_id]


    async def create_message(self, msg_data: MessageCerate, author_id: UUID) -> Message:
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

        await self.__msg_repo.save(message=msg)

        return msg
    

    async def get_message_by_id(self, requester_id: UUID, message_id: UUID) -> Message:
        msgs = await self.__msg_repo.get(filter=MessageFilter(message_id=message_id))

        if len(msgs) == 0:
            raise NotFoundException(msg='Message not found')

        return msgs[0]


    async def edit_message(self, requester_id: UUID, message_id: UUID, content: str) -> None:
        msg = await self.get_message_by_id(requester_id=requester_id, message_id=message_id)

        if msg.author_id != requester_id:
            raise AccessDeniedException(msg='You dont have permission to edit this message')
        
        await self.__msg_repo.update(filter=MessageFilter(message_id=message_id), content=content)

        return


    async def delete_message(self, requester_id: UUID, message_id: UUID) -> None:
        msg = await self.get_message_by_id(requester_id=requester_id, message_id=message_id)

        if msg.author_id != requester_id:
            raise AccessDeniedException(msg='You dont have permission to edit this message')
        
        await self.__msg_repo.delete(filter=MessageFilter(message_id=message_id))

        return
