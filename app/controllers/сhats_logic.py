from typing import List, Optional, Dict
import time

from fastapi import HTTPException, status, UploadFile
from fastapi.responses import JSONResponse
import ormar.exceptions as dbexceptions

from dbmodels import *
import schemas
from auth import JWTAuth
from controllers.files_logic import Storage, SavedFile
from controllers.users_logic import ServerUser


class PermissionController():
    standard_permissions = [
            Permission(
                key="WRITE_MESSAGES", 
                description="Adding messages to a chat/channel"),
            Permission(
                key="EDIT_MESSAGES", 
                description="Editing other people's messages"),
            Permission(
                key="DELETE_MESSAGES", 
                description="Deleting other people's messages"),
            Permission(
                key="EDIT_CONVERSATION_INFO", 
                description="Changing Chat/Channel information"),
            Permission(
                key="EDIT_CONVERSATION_SETTINGS", 
                description="Changing Chat/Channel settings")
        ]
    
    permission_ids = {}

    standard_roles_permission = {
        "ChatOwner": {
            "WRITE_MESSAGES": True,
            "EDIT_MESSAGES": True,
            "DELETE_MESSAGES": True,
            "EDIT_CONVERSATION_INFO": True,
            "EDIT_CONVERSATION_SETTINGS": True
        },
        "ChatUser": {
            "WRITE_MESSAGES": True,
            "EDIT_MESSAGES": False,
            "DELETE_MESSAGES": False,
            "EDIT_CONVERSATION_INFO": False,
            "EDIT_CONVERSATION_SETTINGS": False
        },
        "ChannelOwner": {
            "WRITE_MESSAGES": True,
            "EDIT_MESSAGES": True,
            "DELETE_MESSAGES": True,
            "EDIT_CONVERSATION_INFO": True,
            "EDIT_CONVERSATION_SETTINGS": True
        },
        "ChannelUser": {
            "WRITE_MESSAGES": False,
            "EDIT_MESSAGES": False,
            "DELETE_MESSAGES": False,
            "EDIT_CONVERSATION_INFO": False,
            "EDIT_CONVERSATION_SETTINGS": False
        }
    }

    role_ids = []


    @classmethod
    async def __init_standard_permissions(cls):
        await Permission.objects.delete(each=True)
        for permission in cls.standard_permissions:
            perm_id = await Permission.objects.create(key=permission.key, description=permission.description)
            cls.permission_ids[permission.key] = perm_id

    @classmethod
    async def __init_standard_roles(cls):
        for role in cls.standard_roles_permission.items():
            role_id = await ConversationRole.objects.create(role=role[0])
            for permission in role[1].items():
                await RolePermission.objects.create(role_id=role_id, permission_id=cls.permission_ids[permission[0]], value=permission[1])

    @classmethod
    async def init_standard(cls):
        @database.transaction()
        async def creating_transaction():
            if await Permission.objects.count() != len(cls.standard_permissions):
                await cls.__init_standard_permissions()
                await cls.__init_standard_roles()
        await creating_transaction()

    @classmethod
    async def load_role_ids(cls):
        cls.role_ids = {role.role:role.id for role in (await ConversationRole.objects.all())}



class MsgAttachment():
    def __init__(self, id: Optional[int] = None, message: 'ChatMessage' = None) -> None:
        self.id: int
        self.__dbattachment: Attachment

        self.__message: ChatMessage

        self.__view: schemas.Attachment.View

        if message:
            self.__message = message
        if id:
            self.id = id


    async def create(self, schema: schemas.Attachment.Create):
        self.__dbattachment = await Attachment.objects.create(message_id=self.__message, file=schema.file_id, type=schema.type)
        return self



class MsgReaction():
    def __init__(self, id: Optional[int] = None) -> None:
        self.id: int
        if id:
            self.id = id



class ChatMessage():
    def __init__(self, dbmessage: Optional[Message] = None, id: Optional[int] = None) -> None:
        self.id: int
        self.__dbmessage: Message

        self.__attachments: List[MsgAttachment] = list()
        self.__reply: ChatMessage
        self.__forwarded: List[ChatMessage] = list()
        self.__answers: List[ChatMessage] = list()
        self.__reactions: List[MsgReaction] = list()

        self.__view: schemas.Message.View

        if dbmessage:
            self.__dbmessage = dbmessage
        if id:
            self.id = id

    
    async def create(self, schema: schemas.Message.Create):
        pass



class Chat():
    def __init__(self, id:Optional[int]=None) -> None:
        self.id: int
        self.__dbchat: Conversation

        self.__view: schemas.Chat.View

        self.__subject: ServerUser

        if id:
            self.id = id

    @property
    def view(self) -> schemas.Chat.View:
        return self.__view 


    async def __load_from_db(self):
        try:
            self.__dbchat = await Conversation.objects.filter(Conversation.id==self.id).get()
        except dbexceptions.NoMatch:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="such chat not exists")


    async def create_view(self) -> 'Chat':
        await self.__load_from_db()
        photo = None
        if self.__dbchat.photo_id:
            pass
        self.__view = schemas.Chat.View(
            title = self.__dbchat.title,
            description = self.__dbchat.description,
            photo = photo,
            users_count = await ConversationUser.objects.filter(ConversationUser.conversation_id.id == self.id).count()
        )
        return self
    

    async def get_members(self, count, offset) -> List[ServerUser]:
        members = list()
        dbmembers = await ConversationUser.objects.filter(ConversationUser.conversation_id.id==self.id).limit(count).offset(offset).all()
        for dbmember in dbmembers:
            member = await ServerUser(dbmember.id).create_view()
            members.append(member)
        return members


    async def add_members(self, user_ids: List[int]):
        for uid in user_ids:
            await ConversationUser.objects.create(conversation_id=self.id, user_id=uid, role_id=PermissionController.role_ids['ChatUser'])
        return True




class ChatController():
    def __init__(self, subject_id: Optional[int]=None) -> None:
        self._subject: int
        self.__chat_id: int
        self.__chat: Chat
        if subject_id:
            self._subject = subject_id

    @property
    def chat(self) -> Chat:
        return self.__chat


    async def create_chat(self, schema: schemas.Chat.Create) -> int:
        acttime = time.time()
        chat = await Conversation.objects.create(
            type="chat", 
            settings={}, 
            owner_id=self._subject, 
            created_at=acttime, 
            updated_at=acttime,
            title=schema.title,
            description=schema.description,
            photo_id=schema.photo_id
            )

        await ConversationUser.objects.create(
            user_id=self._subject,
            conversation_id=chat.id,
            role_id= (await ConversationRole.objects.filter(ConversationRole.role=="ChatOwner").get()).id)

        for user_id in schema.user_ids:
            await ConversationUser.objects.create(
                user_id=user_id,
                conversation_id=chat.id,
                role_id=(await ConversationRole.objects.filter(ConversationRole.role=="ChatUser").get()).id)

        self.__chat_id = chat.id
        return chat.id


    async def get_chat(self, chat_id):
        chat = await Chat(chat_id).create_view()
        return chat
    
    async def get_chat_members(self, chat_id: int, count: int, offset: int) -> List[schemas.User.View]:
        members = await Chat(chat_id).get_members(count, offset)
        return [member.view for member in members]

    async def add_chat_members(self, chat_id, user_ids: List[int]):
        return await Chat(chat_id).add_members(user_ids)