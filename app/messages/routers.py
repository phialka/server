from uuid import UUID
from typing import Optional

from fastapi import APIRouter, UploadFile, Response, status, Depends, Request, WebSocket
from utils.fastapi_jwt_auth import auth_scheme, get_user_id

from messages.schemas import Message, MessageUpdate
from messages.use_cases import MessageUseCases
from messages.adapters import SQLMessageRepo

from users.adapters import SQLUserRepo, UserMsgWebSocket

from auth.adapters import SQLAuthDataRepo

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



@message_routers.websocket(
        "/messages/ws"
        )
async def get_message_ws(ws: WebSocket, user_id: str = Depends(get_user_id)):
    await ws.accept()
    rec = UserMsgWebSocket(user_id=user_id, ws=ws)
    return await message_uc.add_user_msg_receiver(rec)



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
