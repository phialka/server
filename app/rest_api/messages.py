from uuid import UUID
from typing import Optional

from fastapi import APIRouter, UploadFile, Response, status, Depends, Request
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT

from entities import Message, PrivateMessage, ChannelMessage
from use_cases.datamodels.creation_data import MessageCerate
from use_cases.messages_usecases import MessageUseCases

from adapters.private_chat_repo import SQLPrivateChatRepo
from adapters.message_repo import SQLMessageRepo, SQLChannelMessageRepo, SQLPrivateMessageRepo
from adapters.user_repo import SQLUserRepo
from adapters.auth_data_repo import SQLAuthDataRepo
from adapters.channel_repo import SQLChannelRepo
from adapters.server_repo import SQLServerRepo
from adapters.file_repo import SQLFileRepo
from adapters.file_storage import SystemFileStorage

from .schemas.channels import ChannelCreate, ChannelUpdate


import config



message_routers = APIRouter(
    prefix = "",
    tags = ["messages"],
    dependencies=[Depends(HTTPBearer(scheme_name='JWT'))]
)



message_uc = MessageUseCases(
    channel_repo = SQLChannelRepo(),
    msg_repo = SQLMessageRepo(),
    channel_msg_repo = SQLChannelMessageRepo(),
    chat_msg_repo = SQLPrivateMessageRepo(),
    user_repo = SQLUserRepo(),
    auth_repo = SQLAuthDataRepo(),
    file_repo = SQLFileRepo(),
    chat_repo = SQLPrivateChatRepo(),
    server_repo = SQLServerRepo(),
    file_storage = SystemFileStorage(config.FILE_STORAGE)
)



@message_routers.get(
        "/messages/{message_id}", 
        summary = 'Получить сообщение по ID',
        response_model = Message
        )
async def get_message_by_id(message_id: UUID, auth: AuthJWT = Depends()):
    auth.jwt_required()
    user_id = UUID(auth.get_jwt_subject())

    return await message_uc.get_message_by_id(requester_id=user_id, message_id=message_id)



@message_routers.delete(
        "/messages/{message_id}", 
        summary = 'Удвлить сообщение по ID'
        )
async def delete_message_by_id(message_id: UUID, auth: AuthJWT = Depends()):
    auth.jwt_required()
    user_id = UUID(auth.get_jwt_subject())

    pass


@message_routers.post(
        "/users/{user_id}/sendMessage", 
        summary = 'Отправить сообщение пользователю',
        tags=['users']
        )
async def send_message_to_user(user_id: UUID, msg: MessageCerate, auth: AuthJWT = Depends()):
    auth.jwt_required()
    requester_id = UUID(auth.get_jwt_subject())

    await message_uc.create_private_message(requester_id=requester_id, recipient_id=user_id, msg_data=msg)

    return



@message_routers.post(
        "/channels/{channel_id}/sendMessage", 
        summary = 'Отправить сообщение в текстовый канал',
        tags=['channels']
        )
async def send_message_to_channel(channel_id: UUID, msg: MessageCerate, auth: AuthJWT = Depends()):
    auth.jwt_required()
    requester_id = UUID(auth.get_jwt_subject())

    await message_uc.create_channel_message(requester_id=requester_id, channel_id=channel_id, msg_data=msg)

    return



@message_routers.get(
        "/private/{chat_id}/messages", 
        summary = 'Получить сообщения из приватного чата',
        response_model = list[Message],
        tags=['private']
        )
async def get_message_from_chat(chat_id: UUID, sequence: int, count: Optional[int] = 10, auth: AuthJWT = Depends()):
    auth.jwt_required()
    user_id = UUID(auth.get_jwt_subject())

    return await message_uc.get_private_chat_messages(requester_id=user_id, chat_id=chat_id, sequence_min=sequence, count=count)
