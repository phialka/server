from entities import ChannelMessage, PrivateMessage, Message, Attachment, File
from use_cases.datamodels.filters import MessageFilter, ChannelMessageFilter, PrivateMessageFilter
from use_cases.abstracts import MessageRepo, ChannelMessageRepo, PrivateMessageRepo

from typing import Optional, Union
from datetime import date
from uuid import uuid4, UUID

from database import tables



class SQLChannelMessageRepo(ChannelMessageRepo):

    def __init__(self) -> None:
        self.__table = tables.ChannelMessage
        self.__msg_repo = SQLMessageRepo()


    def __serialize_filter(self, filter: ChannelMessageFilter):
        """
        Amazing filter serialization from data model to ORMAR style
        """
        query = None

        def __without_none(somthing, query, operation = lambda a, b: a & b):
            if query:
                query = operation(somthing, query)
            else:
                query = somthing
            return query

        if filter.channel_id:
            query = __without_none(self.__table.channel.id == filter.channel_id, query)
        if filter.sequence_min:
            query = __without_none(self.__table.sequence >= filter.sequence_min, query)

        return query


    async def save(self, message: ChannelMessage) -> bool:
        await self.__table.objects.create(
            id = uuid4(),
            channel = message.channel_id,
            message = message.message.message_id,
            was_viewed = False,
            sequence = message.sequence
        )


    async def get(self, filter: Optional[ChannelMessageFilter] = None) -> list[ChannelMessage]:
        query_set = self.__table.objects

        if filter:
            channel_msgs_raw = await query_set.all(self.__serialize_filter(filter))
        else:
            channel_msgs_raw = await query_set.all()

        messages = [
            ChannelMessage(
                channel_id = msg.channel.id,
                sequence = msg.sequence,
                message = (await self.__msg_repo.get(filter=MessageFilter(message_id=msg.message.id)))[0]
            )
            for msg in channel_msgs_raw
        ]

        return messages


    async def update(self, filter: Optional[ChannelMessageFilter] = None, **kwargs) -> int:
        pass


    async def delete(self, filter: Optional[ChannelMessageFilter] = None) -> int:
        if filter:
            count = await self.__table.objects.delete(self.__serialize_filter(filter))
        else:
            count = await self.__table.objects.delete(each=True)

        return count



class SQLPrivateMessageRepo(PrivateMessageRepo):

    def __init__(self) -> None:
        self.__table = tables.PrivateMessage
        self.__msg_repo = SQLMessageRepo()


    def __serialize_filter(self, filter: PrivateMessageFilter):
        """
        Amazing filter serialization from data model to ORMAR style
        """
        query = None

        def __without_none(somthing, query, operation = lambda a, b: a & b):
            if query:
                query = operation(somthing, query)
            else:
                query = somthing
            return query

        if filter.chat_id:
            query = __without_none(self.__table.private_chat.id == filter.chat_id, query)
        if filter.sequence_min:
            query = __without_none(self.__table.sequence >= filter.sequence_min, query)

        return query


    async def save(self, message: PrivateMessage) -> bool:
        await self.__table.objects.create(
            id = uuid4(),
            private_chat = message.chat_id,
            message = message.message.message_id,
            was_viewed = False,
            sequence = message.sequence
        )


    async def get(self, filter: Optional[PrivateMessageFilter] = None) -> list[PrivateMessage]:
        query_set = self.__table.objects

        if filter:
            private_msgs_raw = await query_set.all(self.__serialize_filter(filter))
        else:
            private_msgs_raw = await query_set.all()

        messages = [
            PrivateMessage(
                chat_id = msg.private_chat.id,
                sequence = msg.sequence,
                message = (await self.__msg_repo.get(filter=MessageFilter(message_id=msg.message.id)))[0]
            )
            for msg in private_msgs_raw
        ]

        return messages


    async def update(self, filter: Optional[PrivateMessageFilter] = None, **kwargs) -> int:
        pass


    async def delete(self, filter: Optional[PrivateMessageFilter] = None) -> int:
        if filter:
            private_msgs_raw = await self.__table.objects.delete(self.__serialize_filter(filter))
        else:
            private_msgs_raw = await self.__table.objects.delete(each=True)



class SQLMessageRepo(MessageRepo):

    def __init__(self) -> None:
        self.__table = tables.Message
        self.__attach_table = tables.Attachment


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
        pass


    async def delete(self, filter: Optional[MessageFilter] = None) -> int:
        pass
