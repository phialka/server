from uuid import UUID
from typing import Optional
import asyncio

from fastapi import APIRouter, UploadFile, Response, status, Depends, Request, WebSocket
from fastapi.websockets import WebSocketState
from starlette.endpoints import WebSocketEndpoint
from utils.fastapi_jwt_auth import auth_scheme, get_user_id

from messages.schemas import Message, MessageUpdate
from messages.use_cases import MessageUseCases
from messages.adapters import SQLMessageRepo

from users.adapters import SQLUserRepo, UserMsgWebSocket

from auth.adapters import SQLAuthDataRepo

from files.adapters import SQLFileRepo, SystemFileStorage
from channels.routers import channel_uc
from servers.routers import server_uc
from messages.routers import message_uc

import config



message_ws_router = APIRouter(
    prefix = ""
)



@message_ws_router.websocket(
        "/messages/ws"
        )
async def get_message_ws(ws: WebSocket, token: str):
    user_id = get_user_id(token)
    await ws.accept()
    user_ws = UserMsgWebSocket(user_id=user_id, ws=ws)
    message_uc.add_user_msg_receiver(user_ws)

    while True:
        if ws.application_state == WebSocketState.DISCONNECTED:
            message_uc.delete_user_msg_receiver(user_id=user_id)
            return
        await asyncio.sleep(0.01)
