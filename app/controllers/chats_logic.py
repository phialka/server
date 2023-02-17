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
    def __init__(self, id: Optional[int] = None) -> None:
        """
        Provides the ability to work correctly with an entity from the database, as well as converting it to a view for display in the API
        """
        self.id: int
        self.__dbattachment: Attachment

        self.__view: schemas.Attachment.View

        if id:
            self.id = id

    @property
    def view(self) -> schemas.Attachment.View:
        return self.__view 

    async def __load_from_db(self):
        self.__dbattachment = await Attachment.objects.filter(Attachment.id == self.id).get()

    async def create_view(self):
        await self.__load_from_db()
        self.__view = schemas.Attachment.View(
            type=self.__dbattachment.type,
            file=(await SavedFile(self.__dbattachment.file).create_view()).view
        )
        return self

    async def create(self, msg_id, schema: schemas.Attachment.Create):
        self.__dbattachment = await Attachment.objects.create(message_id=msg_id, file=schema.file_id, type=schema.type)
        self.id = self.__dbattachment.id
        return self



class MsgReaction():
    def __init__(self, id: Optional[int] = None) -> None:
        self.id: int
        if id:
            self.id = id



class ChatMessage():
    def __init__(self, id: Optional[int] = None) -> None:
        """
        Provides the ability to work correctly with an entity from the database, as well as converting it to a view for display in the API
        """
        self.id: int
        self.__dbmessage: Message

        self.owner: ServerUser
        self.__attachments: List[MsgAttachment] = list()
        self.__reply_id: int = None
        self.__forwarded_ids: List[int] = list() 
        self.__answers: List[ChatMessage] = list()
        self.__reactions: List[MsgReaction] = list()

        self.__view: schemas.Message.View

        if id:
            self.id = id

    @property
    def view(self) -> schemas.Message.View:
        return self.__view 

    async def __load_from_db(self):
        self.__dbmessage = await Message.objects.filter(Message.id == self.id).get()

    async def __load_attachments(self):
        self.__attachments = [
            await MsgAttachment(attach.id).create_view() for attach in await Attachment.objects.filter(Attachment.message_id.id == self.id).all()
            ]

    async def __load_reply(self):
        dbreply = await Replice.objects.filter(Replice.message_id.id == self.id).get_or_none()
        if dbreply:
            self.__reply_id = dbreply.reply_message_id.id

    async def __load_forwardes(self):
        dbforwards = await Forwarded.objects.filter(Replice.message_id.id == self.id).all()
        if dbforwards:
            self.__forwarded_ids = [forward.id for forward in dbforwards]

    async def __load_queue(self):
        queue = await MessageQueue.objects.filter(MessageQueue.message_id.id == self.id).first()
        self.owner = ServerUser(queue.sender_id.id)

    async def create_view(self):
        await self.__load_from_db()
        await self.__load_attachments()
        await self.__load_reply()
        await self.__load_forwardes()
        await self.__load_queue()

        self.__view = schemas.Message.View(
            message_id=self.id,
            user_id=self.owner.id,
            text=self.__dbmessage.content,
            attachments=[attach.view for attach in self.__attachments],
            reply_to=self.__reply_id,
            forward_messages=self.__forwarded_ids,
            reactions=None,
            views=None,
            created_at=self.__dbmessage.created_at
        )
        return self



class MessageController():
    def __init__(self, subject_id: Optional[int]=None) -> None:
        """
        Provides methods for interacting with entities on behalf of the specified user. Initialized with a specific user id
        """
        self._subject: int
        self.__message_id: int
        self.__message: ChatMessage
        if subject_id:
            self._subject = subject_id

    @property
    def message(self) -> ChatMessage:
        return self.__message


    async def create_message(self, schema: schemas.Message.Create) -> int:
        if not (schema.user_ids or schema.chat_ids):
            raise HTTPException(status_code=400, detail="one of the parameters must be present: user_ids or chat_ids")
        if not (schema.text or schema.attachments or schema.forward_messages):
            raise HTTPException(status_code=400, detail="the message has no content")

        database.transaction()
        async def creating_transaction():
            acttime = time.time()
            message = await Message.objects.create(content=schema.text, updated_at=acttime, created_at=acttime)
            if schema.attachments:
                for attach in schema.attachments:
                    await MsgAttachment().create(msg_id=message.id, schema=schemas.Attachment.Create(**attach.dict()))
            if schema.forward_messages:
                for forward in schema.forward_messages:
                    await Forwarded.objects.create(forwarded_message_id=forward, message_id=message.id)
            if schema.reply_to:
                await Replice.objects.create(message_id=message.id, reply_message_id=schema.reply_to)

            if schema.user_ids:
                for user_id in schema.user_ids:
                    await MessageQueue.objects.create(message_id=message.id, sender_id=self._subject, recipient_id=user_id, conversation_id=None)
            if schema.chat_ids:
                for chat_id in schema.chat_ids:
                    await MessageQueue.objects.create(message_id=message.id, sender_id=self._subject, recipient_id=None, conversation_id=chat_id)
            
            return message.id
        return await creating_transaction()


    async def get_message_byid(self, message_id):
        try:
            return await ChatMessage(message_id).create_view()
        except dbexceptions.NoMatch:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'message with id {message_id} not exists')

    
    async def get_user_messages(self, newer: int, count: int) -> List[ChatMessage]:
        queue = await MessageQueue.objects.filter(
            (MessageQueue.recipient_id.id == self._subject) & (MessageQueue.message_id.created_at >= newer)
            ).limit(count).all()
        return [await ChatMessage(q.message_id.id).create_view() for q in queue]

    
    async def get_chat_messages(self, chat_id: int, newer: int, count: int):
        queue = await MessageQueue.objects.filter(
            (MessageQueue.conversation_id.id == chat_id) & (MessageQueue.message_id.created_at >= newer)
            ).limit(count).all()
        return [await ChatMessage(q.message_id.id).create_view() for q in queue]




class Chat():
    def __init__(self, id:Optional[int]=None) -> None:
        """
        Provides the ability to work correctly with an entity from the database, as well as converting it to a view for display in the API
        """
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
            chat_id=self.id,
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

    async def get_messages(self, count: int, offset: int):
        pass




class ChatController():
    def __init__(self, subject_id: Optional[int]=None) -> None:
        """
        Provides methods for interacting with entities on behalf of the specified user. Initialized with a specific user id
        """
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

    async def get_user_chats(self, count: int, offset: int):
        db_chatusers = await ConversationUser.objects.filter(ConversationUser.user_id.id == self._subject).limit(count).offset(offset).all()
        return [await Chat(user.conversation_id.id).create_view() for user in db_chatusers]
    

    async def get_chat(self, chat_id):
        chat = await Chat(chat_id).create_view()
        return chat
    

    async def get_chat_members(self, chat_id: int, count: int, offset: int) -> List[schemas.User.View]:
        members = await Chat(chat_id).get_members(count, offset)
        return [member.view for member in members]


    async def add_chat_members(self, chat_id, user_ids: List[int]):
        return await Chat(chat_id).add_members(user_ids)