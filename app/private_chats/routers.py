from uuid import UUID
from typing import Optional

from fastapi import APIRouter, UploadFile, Response, status, Depends, Request
from fastapi.security import HTTPBearer
from utils.fastapi_jwt_auth import auth_scheme, get_user_id

from private_chats.schemas import PrivateChat, PrivateMessage
from private_chats.use_cases import PrivateChatUseCases
from private_chats.adapters import SQLPrivateChatRepo, SQLPrivateMessageRepo

from messages.schemas import MessageCerate
from messages.adapters import SQLMessageRepo
from messages.routers import message_uc

from auth.adapters import SQLAuthDataRepo

from files.adapters import SQLFileRepo, SystemFileStorage

from users.adapters import SQLUserRepo
from users.routers import users_routers

import config



private_chat_routers = APIRouter(
    prefix = "/private",
    tags = ["private"],
    dependencies=[Depends(auth_scheme)]
)



chat_uc = PrivateChatUseCases(
        chat_repo=SQLPrivateChatRepo(),
        private_msg_repo=SQLPrivateMessageRepo(),
        user_repo=SQLUserRepo(),
        auth_repo=SQLAuthDataRepo(),
        file_repo=SQLFileRepo(),
        file_storage=SystemFileStorage(
            path=config.FILE_STORAGE
        ),
        message_uc=message_uc
    )



@private_chat_routers.get(
        "", 
        summary = 'Получить список своих приватных чатов',
        response_model = list[PrivateChat]
        )
async def get_my_chats(user_id: str = Depends(get_user_id)):
    chats = await chat_uc.get_chats_by_member(user_id=user_id)

    return chats



@private_chat_routers.get(
        "/{chat_id}", 
        summary = 'Получить информацию о приватном чате',
        response_model = PrivateChat
        )
async def get_chat_by_id(chat_id: UUID, user_id: str = Depends(get_user_id)):
    chat = await chat_uc.get_chat_by_id(user_id, chat_id)

    return chat



@private_chat_routers.delete(
        "/{chat_id}", 
        summary = 'Удалить приватный чат'
        )
async def delete_chat_by_id(chat_id: UUID, user_id: str = Depends(get_user_id)):
    await chat_uc.delete_chat(requester_id=user_id, chat_id=chat_id)

    return 



@users_routers.post(
        "/{user_id}/sendMessage", 
        summary = 'Отправить сообщение пользователю',
        tags=['messages']
        )
async def send_message_to_user(user_id: UUID, msg: MessageCerate, requester_id: str = Depends(get_user_id)):
    await chat_uc.create_private_message(requester_id=requester_id, recipient_id=user_id, msg_data=msg)

    return



@private_chat_routers.get(
        "/private/{chat_id}/messages", 
        summary = 'Получить сообщения из приватного чата',
        response_model = list[PrivateMessage],
        tags=['messages']
        )
async def get_messages_from_chat(chat_id: UUID, sequence: int, count: Optional[int] = 10, user_id: str = Depends(get_user_id)):
    return await chat_uc.get_private_chat_messages(requester_id=user_id, chat_id=chat_id, sequence_min=sequence, count=count)
