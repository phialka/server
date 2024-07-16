from typing import Optional, Union
from uuid import uuid4, UUID

from messages.schemas import Message, MessageCerate, Attachment, AttachmentCreate
from messages.abstracts import MessageRepo, MessageFilter
from messages.dbmodels import Message as DBMessage, Attachment as DBAttachment

from files.schemas import File



class SQLMessageRepo(MessageRepo):

    def __init__(self) -> None:
        self.__table = DBMessage
        self.__attach_table = DBAttachment


    def __serialize_filter(self, filter: MessageFilter):
        """
        Amazing filter serialization from data model to ORMAR style
        """
        query = None

        def __without_none(somthing, query, operation = lambda a, b: a and b):
            if query:
                query = operation(somthing, query)
            else:
                query = somthing
            return query

        if filter.message_id:
            query = __without_none(self.__table.id == filter.message_id, query)
        if filter.author_id:
            query = __without_none(self.__table.author.id == filter.author_id, query)

        return query


    async def __save_attachment(self, attachment: Attachment) -> bool:
        await self.__attach_table.objects.create(
            id = uuid4(),
            file = attachment.file.file_id,
            message = attachment.message_id,
            attach_type = attachment.attach_type
        )

        return True
    

    async def __get_message_attachments(self, message_id: UUID) -> list[Attachment]:
        query_set = self.__attach_table.objects.select_related(self.__attach_table.file)
        query_set = query_set.filter(self.__attach_table.message.id == message_id)
        
        attachments_raw = await query_set.all()

        return [
            Attachment(
                message_id = a.message.id,
                attach_type = a.attach_type,
                file = File(
                    file_id = a.file.id,
                    download_id = a.file.download_id,
                    size = a.file.size,
                    hash = a.file.hash,
                    mime_type = a.file.mime_type,
                    upload_at = a.file.upload_at
                )
            )
            for a in attachments_raw
        ]


    async def save(self, message: Message) -> bool:

        await self.__table.objects.create(
            id = message.message_id,
            author = message.author_id,
            content = message.content,
            created_at = message.created_at,
            updated_at = message.updated_at
        )

        for attach in message.attachments:
            await self.__save_attachment(attach)

        return True


    async def get(self, filter: Optional[MessageFilter] = None) -> list[Message]:
        query_set = self.__table.objects

        if filter:
            query_set = query_set.filter(self.__serialize_filter(filter))
        
        messages_raw = await query_set.all()

        return [
            Message(
                message_id = msg.id,
                author_id = msg.author.id,
                content = msg.content,
                reply_message_id = None,
                created_at = msg.created_at,
                updated_at = msg.updated_at,
                attachments = await self.__get_message_attachments(msg.id)
            )
            for msg in messages_raw
        ]


    async def update(self, filter: Optional[MessageFilter] = None, **kwargs) -> int:
        if 'message_id' in kwargs:
            raise
        if 'created_at' in kwargs:
            raise
        if 'author_id' in kwargs:
            raise

        if not filter:
            return await self.__table.objects.update(each=True, **kwargs)
        if filter:
            return await self.__table.objects.filter(self.__serialize_filter(filter)).update(**kwargs)


    async def delete(self, filter: Optional[MessageFilter] = None) -> int:
        if not filter:
            return await self.__table.objects.delete(each=True)
        else:
            return await self.__table.objects.filter(self.__serialize_filter(filter)).delete()
