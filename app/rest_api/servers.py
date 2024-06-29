from uuid import UUID
from typing import Optional

from fastapi import APIRouter, UploadFile, Response, status, Depends, Request
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT

from entities import Server, File, Channel, User
from use_cases.server_usecases import ServerUseCases
from use_cases.files_usecases import FileUseCases
from adapters.file_repo import SQLFileRepo
from adapters.file_storage import SystemFileStorage
from adapters.server_repo import SQLServerRepo
from adapters.channel_repo import SQLChannelRepo
from adapters.server_member_repo import SQLServerMemberRepo

from .schemas.servers import ServerCreate, ServerUpdate


import config



server_routers = APIRouter(
    prefix = "/servers",
    tags = ["servers"],
    dependencies=[Depends(HTTPBearer(scheme_name='JWT'))]
)



server_repo = SQLServerRepo()
file_repo = SQLFileRepo()
channel_repo = SQLChannelRepo()
member_repo = SQLServerMemberRepo()
file_storage = SystemFileStorage(config.FILE_STORAGE)


file_uc = FileUseCases(file_repo, file_storage)
server_uc = ServerUseCases(server_repo, member_repo, channel_repo, file_uc)



@server_routers.post(
        "", 
        summary = 'Создать сервер',
        response_model = Server
        )
async def create_server(data: ServerCreate, auth: AuthJWT = Depends()):
    auth.jwt_required()
    user_id = auth.get_jwt_subject()

    return await server_uc.create_server(owner_id=user_id, title=data.title, description=data.description)



@server_routers.patch(
        "/{server_id}", 
        summary = 'Редактировать сервер',
        response_model = Server
        )
async def edit_server(data: ServerUpdate, server_id: UUID, auth: AuthJWT = Depends()):
    auth.jwt_required()
    user_id = UUID(auth.get_jwt_subject())

    return await server_uc.edit_server(
        server_id=server_id, 
        requester_id=user_id, 
        new_title=data.title, 
        new_description=data.description
        )



@server_routers.delete(
        "/{server_id}", 
        summary = 'Удалить сервер'
        )
async def delete_server(server_id: UUID, auth: AuthJWT = Depends()):
    auth.jwt_required()
    user_id = UUID(auth.get_jwt_subject())

    return await server_uc.delete_server(requester_id=user_id, server_id=server_id)



@server_routers.get(
        "/{server_id}", 
        summary = 'Получить информацию о сервере',
        response_model = Server
        )
async def get_server_info(server_id: UUID, auth: AuthJWT = Depends()):
    auth.jwt_required()

    return await server_uc.get_server_by_id(server_id=server_id)



@server_routers.put(
        "/{server_id}/logo", 
        summary = 'Установить логотип сервера',
        response_model = File
        )
async def set_server_logo(server_id: UUID, logo: UploadFile, auth: AuthJWT = Depends()):
    auth.jwt_required()
    user_id = UUID(auth.get_jwt_subject())

    return await server_uc.set_server_logo(server_id, requester_id=user_id, logo=logo.file)



@server_routers.delete(
        "/{server_id}/logo", 
        summary = 'Удалить логотип сервера'
        )
async def set_server_logo(server_id: UUID, auth: AuthJWT = Depends()):
    auth.jwt_required()
    user_id = UUID(auth.get_jwt_subject())

    return await server_uc.delete_server_logo(server_id=server_id, requester_id=user_id)



@server_routers.get(
        "/{server_id}/getChannels", 
        summary = 'Получить список текстовых каналов на сервере',
        response_model = list[Channel]
        )
async def get_server_channels(server_id: UUID, auth: AuthJWT = Depends()):
    auth.jwt_required()

    return await server_uc.get_channels(server_id)



@server_routers.get(
        "/{server_id}/getMembers", 
        summary = 'Получить список пользователей сервера',
        response_model = list[User]
        )
async def get_server_members(server_id: UUID, auth: AuthJWT = Depends()):
    auth.jwt_required()

    return await server_uc.get_server_members(server_id)
