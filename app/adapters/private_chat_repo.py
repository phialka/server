from entities import PrivateChat, User, File
from use_cases.datamodels.filters import PrivateChatFilter
from use_cases.abstracts import PrivateChatRepo

from typing import Optional
from uuid import uuid4

from database import tables



class SQLPrivateChatRepo(PrivateChatRepo):

    def __init__(self) -> None:
        self.__chat_table = tables.PrivateChat
        self.__member_table = tables.PrivateChatMember


    def __serialize_filter(self, filter: PrivateChatFilter):
        """
        Amazing filter serialization from data model to ORMAR style
        """
        chat_query = None
        member_query = None

        def __without_none(somthing, query, operation = lambda a, b: a and b):
            if query:
                query = operation(somthing, query)
            else:
                query = somthing
            return query

        if filter.chat_id:
            chat_query = __without_none(self.__chat_table.id == filter.chat_id, chat_query)
        if filter.member_ids:
            or_set = None
            for usr_id in filter.member_ids:
                or_set = __without_none(self.__member_table.user.id == usr_id, or_set, lambda a, b: a and b)
            member_query = __without_none(or_set, member_query)

        return chat_query, member_query
    

    async def save(self, chat: PrivateChat) -> bool:
        await self.__chat_table.objects.create(id = chat.chat_id)
        for user in chat.members:
            await self.__member_table.objects.create(
                id = uuid4(),
                private_chat = chat.chat_id,
                user = user.user_id
            )


    async def get(self, filter: Optional[PrivateChatFilter] = None) -> list[PrivateChat]:
        chat_f, member_f = self.__serialize_filter(filter)
        chat_list = []
        if chat_f:
            chats = await self.__chat_table.objects.select_related([self.__chat_table.privatechatmembers, self.__chat_table.privatechatmembers.user, self.__chat_table.privatechatmembers.user.photo]).all(chat_f)
            for chat in chats:
                chat_list.append(
                    PrivateChat(
                        chat_id = chat.id,
                        members = [
                            User(
                                user_id = m.user.id,
                                name = m.user.name,
                                description = m.user.description,
                                tag = m.user.tag,
                                birthdate = m.user.birthdate,
                                photo = None if not m.user.photo else File(
                                    file_id = m.user.photo.id,
                                    download_id = m.user.photo.download_id,
                                    size = m.user.photo.size,
                                    hash = m.user.photo.hash,
                                    mime_type = m.user.photo.mime_type,
                                    upload_at = m.user.photo.upload_at
                                )
                            )
                            for m in chat.privatechatmembers
                        ]
                    )
                )
            return chat_list
        if member_f:
            members = await self.__member_table.objects.all(member_f)
            for member in members:
                chat = await self.__chat_table.objects.select_related([self.__chat_table.privatechatmembers, self.__chat_table.privatechatmembers.user, self.__chat_table.privatechatmembers.user.photo]).get(self.__chat_table.id == member.private_chat.id)
                chat_list.append(
                    PrivateChat(
                        chat_id = chat.id,
                        members = [
                            User(
                                user_id = m.user.id,
                                name = m.user.name,
                                description = m.user.description,
                                tag = m.user.tag,
                                birthdate = m.user.birthdate,
                                photo = None if not m.user.photo else File(
                                    file_id = m.user.photo.id,
                                    download_id = m.user.photo.download_id,
                                    size = m.user.photo.size,
                                    hash = m.user.photo.hash,
                                    mime_type = m.user.photo.mime_type,
                                    upload_at = m.user.photo.upload_at
                                )
                            )
                            for m in chat.privatechatmembers
                        ]
                    )
                )
            for chat in chat_list:
                if [c.chat_id for c in chat_list].count(chat.chat_id) > 1:
                    chat_list.remove(chat)
            return chat_list


    async def update(self, filter: Optional[PrivateChatFilter] = None, **kwargs) -> int:
        pass


    async def delete(self, filter: Optional[PrivateChatFilter] = None) -> int:
        chats = await self.get(filter=filter)
        for chat in chats:
            await self.__chat_table.objects.delete(self.__chat_table.id == chat.chat_id)
        return len(chats)
