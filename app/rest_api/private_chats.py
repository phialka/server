from uuid import UUID
from typing import Optional

from fastapi import APIRouter, UploadFile, Response, status, Depends, Request
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT

from entities import PrivateChat, User
from use_cases.private_chat_usecases import PrivateChatUseCases
from adapters.private_chat_repo import SQLPrivateChatRepo

from .schemas.channels import ChannelCreate, ChannelUpdate


import config



private_chat_routers = APIRouter(
    prefix = "/private",
    tags = ["private"],
    dependencies=[Depends(HTTPBearer(scheme_name='JWT'))]
)


chat_repo = SQLPrivateChatRepo()
chat_uc = PrivateChatUseCases(chat_repo)



@private_chat_routers.get(
        "", 
        summary = 'Получить список своих приватных чатов',
        response_model = list[PrivateChat]
        )
async def get_my_chats(auth: AuthJWT = Depends()):
    auth.jwt_required()
    user_id = UUID(auth.get_jwt_subject())

    chats = await chat_uc.get_chats_by_member(user_id=user_id)

    return chats



@private_chat_routers.get(
        "/{chat_id}", 
        summary = 'Получить информацию о приватном чате',
        response_model = PrivateChat
        )
async def get_chat_by_id(chat_id: UUID, auth: AuthJWT = Depends()):
    auth.jwt_required()
    user_id = UUID(auth.get_jwt_subject())

    chat = await chat_uc.get_chat_by_id(user_id, chat_id)

    return chat



@private_chat_routers.delete(
        "/{chat_id}", 
        summary = 'Удалить приватный чат'
        )
async def delete_chat_by_id(chat_id: UUID, auth: AuthJWT = Depends()):
    auth.jwt_required()
    user_id = UUID(auth.get_jwt_subject())

    await chat_uc.delete_chat(requester_id=user_id, chat_id=chat_id)

    return 

