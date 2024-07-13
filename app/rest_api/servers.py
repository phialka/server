from uuid import UUID
from typing import Optional

from fastapi import APIRouter, UploadFile, Response, status, Depends, Request
from fastapi.security import HTTPBearer
from .security.jwt_auth import auth_scheme, get_user_id

from entities import Server, File, Channel, User
from use_cases.server_usecases import ServerUseCases
from use_cases.files_usecases import FileUseCases
from use_cases.user_usecases import UserUseCases

from adapters.file_repo import SQLFileRepo
from adapters.file_storage import SystemFileStorage
from adapters.server_repo import SQLServerRepo
from adapters.channel_repo import SQLChannelRepo
from adapters.user_repo import SQLUserRepo
from adapters.auth_data_repo import SQLAuthDataRepo
from adapters.server_member_repo import SQLServerMemberRepo

from .schemas.servers import ServerCreate, ServerUpdate, UserInvite


import config



server_routers = APIRouter(
    prefix = "/servers",
    tags = ["servers"],
    dependencies=[Depends(auth_scheme)]
)



server_repo = SQLServerRepo()
file_repo = SQLFileRepo()
channel_repo = SQLChannelRepo()
member_repo = SQLServerMemberRepo()
file_storage = SystemFileStorage(config.FILE_STORAGE)


file_uc = FileUseCases(file_repo, file_storage)
user_uc = UserUseCases(SQLUserRepo(), SQLAuthDataRepo())
server_uc = ServerUseCases(server_repo, member_repo, channel_repo, user_uc, file_uc)



@server_routers.post(
        "", 
        summary = 'Создать сервер'
        )
async def create_server(data: ServerCreate, user_id: str = Depends(get_user_id)):
    await server_uc.create_server(owner_id=user_id, title=data.title, description=data.description)

    return



@server_routers.get(
        "", 
        summary = 'Получить список серверов, в которых состоит текущий пользователь',
        response_model = list[Server]
        )
async def get_my_servers(user_id: str = Depends(get_user_id)):
    return await server_uc.get_user_servers(user_id=user_id)



@server_routers.get(
        "/search", 
        summary = 'Поиск серверов по запросу',
        response_model = list[Server]
        )
async def search_server(prompt: str, offset: Optional[int] = 0, count: Optional[int] = 10, user_id: str = Depends(get_user_id)):
    return await server_uc.search_servers_by_prompt(prompt=prompt, count=count, offset=offset)



@server_routers.patch(
        "/{server_id}", 
        summary = 'Редактировать сервер'
        )
async def edit_server(data: ServerUpdate, server_id: UUID, user_id: str = Depends(get_user_id)):
    await server_uc.edit_server(
        server_id=server_id, 
        requester_id=user_id, 
        new_title=data.title, 
        new_description=data.description
        )
    
    return



@server_routers.delete(
        "/{server_id}", 
        summary = 'Удалить сервер'
        )
async def delete_server(server_id: UUID, user_id: str = Depends(get_user_id)):
    return await server_uc.delete_server(requester_id=user_id, server_id=server_id)



@server_routers.get(
        "/{server_id}", 
        summary = 'Получить информацию о сервере',
        response_model = Server
        )
async def get_server_info(server_id: UUID, user_id: str = Depends(get_user_id)):
    return await server_uc.get_server_by_id(server_id=server_id)



@server_routers.put(
        "/{server_id}/logo", 
        summary = 'Установить логотип сервера',
        response_model = File
        )
async def set_server_logo(server_id: UUID, logo: UploadFile, user_id: str = Depends(get_user_id)):
    await server_uc.set_server_logo(server_id, requester_id=user_id, logo=logo.file)

    return



@server_routers.delete(
        "/{server_id}/logo", 
        summary = 'Удалить логотип сервера'
        )
async def delete_server_logo(server_id: UUID, user_id: str = Depends(get_user_id)):
    return await server_uc.delete_server_logo(server_id=server_id, requester_id=user_id)



@server_routers.get(
        "/{server_id}/getChannels", 
        summary = 'Получить список текстовых каналов на сервере',
        response_model = list[Channel]
        )
async def get_server_channels(server_id: UUID, user_id: str = Depends(get_user_id)):
    return await server_uc.get_channels(server_id)



@server_routers.get(
        "/{server_id}/getMembers", 
        summary = 'Получить список пользователей сервера',
        response_model = list[User]
        )
async def get_server_members(server_id: UUID, user_id: str = Depends(get_user_id)):
    return await server_uc.get_server_members(server_id)



@server_routers.post(
        "/{server_id}/join", 
        summary = 'Присоединиться к серверу'
        )
async def join_to_channel(server_id: UUID, user_id: str = Depends(get_user_id)):
    await server_uc.user_join_to_server(requester_id=user_id, server_id=server_id)
    return



@server_routers.post(
        "/{server_id}/invite", 
        summary = 'Пригласить пользователя на сервер'
        )
async def invite_user_to_channel(server_id: UUID, user: UserInvite, user_id: str = Depends(get_user_id)):
    await server_uc.invite_user_to_server(requester_id=user_id, user_id=user.user_id, server_id=server_id)
    return
