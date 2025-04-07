from uuid import UUID
from typing import Optional

from fastapi import APIRouter, UploadFile, Depends
from utils.fastapi_jwt_auth import auth_scheme, get_user_id

from servers.schemas import Server, ServerCreate, ServerUpdate, UserInvite
from servers.use_cases import ServerUseCases
from servers.adapters import SQLServerRepo, SQLServerMemberRepo

from users.schemas import User
from users.adapters import SQLUserRepo

from auth.adapters import SQLAuthDataRepo

from files.schemas import File
from files.adapters import SQLFileRepo, SystemFileStorage


import config



server_routers = APIRouter(
    prefix = "/servers",
    tags = ["servers"],
    dependencies=[Depends(auth_scheme)]
)



server_uc = ServerUseCases(
        server_repo=SQLServerRepo(),
        member_repo=SQLServerMemberRepo(),
        user_repo=SQLUserRepo(),
        auth_repo=SQLAuthDataRepo(),
        file_repo=SQLFileRepo(),
        file_storage=SystemFileStorage(
            path=config.FILE_STORAGE
        )
    )



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
        summary = 'Установить логотип сервера'
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
