from uuid import UUID
from typing import Optional

from fastapi import APIRouter, UploadFile, Response, status, Depends, Request, WebSocket, Cookie
from utils.fastapi_jwt_auth import auth_scheme, get_user_id

from messages.schemas import Message, MessageUpdate
from messages.use_cases import MessageUseCases
from messages.adapters import SQLMessageRepo

from files.adapters import SQLFileRepo, SystemFileStorage

import config



message_routers = APIRouter(
    prefix = "",
    tags = ["messages"],
    dependencies=[Depends(auth_scheme)]
)



message_uc = MessageUseCases(
        msg_repo=SQLMessageRepo(),
        file_repo=SQLFileRepo(),
        file_storage=SystemFileStorage(
            path=config.FILE_STORAGE
        )
    )



@message_routers.get(
        "/messages/getWS", 
        summary = 'Получить веб-сокет для приёма новых сообщений'
        )
async def get_message_ws(req: Request, user_id: str = Depends(get_user_id), cookie: str = Depends(auth_scheme)):
    return f'ws://{req.base_url.hostname}/messages/ws?token={cookie}'



@message_routers.get(
        "/messages/{message_id}", 
        summary = 'Получить сообщение по ID',
        response_model = Message
        )
async def get_message_by_id(message_id: UUID, user_id: str = Depends(get_user_id)):
    return await message_uc.get_message_by_id(requester_id=user_id, message_id=message_id)



@message_routers.delete(
        "/messages/{message_id}", 
        summary = 'Удалить сообщение по ID'
        )
async def delete_message_by_id(message_id: UUID, user_id: str = Depends(get_user_id)):
    await message_uc.delete_message(requester_id=user_id, message_id=message_id)

    return



@message_routers.patch(
        "/messages/{message_id}", 
        summary = 'Редактировать сообщение по ID'
        )
async def edit_message_by_id(message_id: UUID, msg_data: MessageUpdate, user_id: str = Depends(get_user_id)):
    await message_uc.edit_message(requester_id=user_id, message_id=message_id, content=msg_data.content)
