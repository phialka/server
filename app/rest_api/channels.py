from uuid import UUID
from typing import Optional

from fastapi import APIRouter, UploadFile, Response, status, Depends, Request
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT

from entities import Channel, User, File
from use_cases.files_usecases import FileUseCases
from use_cases.channel_usecases import ChannelUseCases
from adapters.file_repo import SQLFileRepo
from adapters.file_storage import SystemFileStorage
from adapters.channel_repo import SQLChannelRepo
from adapters.server_repo import SQLServerRepo

from .schemas.channels import ChannelCreate, ChannelUpdate


import config



channel_routers = APIRouter(
    prefix = "/channels",
    tags = ["channels"],
    dependencies=[Depends(HTTPBearer(scheme_name='JWT'))]
)



file_repo = SQLFileRepo()
channel_repo = SQLChannelRepo()
server_repo = SQLServerRepo()
file_storage = SystemFileStorage(config.FILE_STORAGE)


file_uc = FileUseCases(file_repo, file_storage)
channel_uc = ChannelUseCases(channel_repo=channel_repo, server_repo=server_repo, file_uc=file_uc)



@channel_routers.post(
        "", 
        summary = 'Создать текстовый канал'
        )
async def create_channel(data: ChannelCreate, auth: AuthJWT = Depends()):
    auth.jwt_required()
    user_id = UUID(auth.get_jwt_subject())

    await channel_uc.create_channel(
        requester_id = user_id,
        server_id = data.server_id,
        title = data.title,
        description = data.description
    )

    return



@channel_routers.patch(
        "/{channel_id}", 
        summary = 'Редактировать текстовый канал'
        )
async def edit_channel(data: ChannelUpdate, channel_id: UUID, auth: AuthJWT = Depends()):
    auth.jwt_required()
    user_id = UUID(auth.get_jwt_subject())

    await channel_uc.edit_channel(
        channel_id = channel_id,
        requester_id = user_id,
        new_title=  data.title,
        new_description = data.description
    )

    return



@channel_routers.delete(
        "/{channel_id}", 
        summary = 'Удалить текстовый канал'
        )
async def delete_channel(channel_id: UUID, auth: AuthJWT = Depends()):
    auth.jwt_required()
    user_id = UUID(auth.get_jwt_subject())

    return await channel_uc.delete_channel(
        requester_id = user_id,
        channel_id = channel_id
    )



@channel_routers.get(
        "/{channel_id}", 
        summary = 'Получить информацию о текстовом канале',
        response_model = Channel
        )
async def get_channel_info(channel_id: UUID, auth: AuthJWT = Depends()):
    auth.jwt_required()

    return await channel_uc.get_channel_by_id(channel_id=channel_id)



@channel_routers.put(
        "/{channel_id}/logo", 
        summary = 'Установить логотип канала'
        )
async def set_channel_logo(channel_id: UUID, logo: UploadFile, auth: AuthJWT = Depends()):
    auth.jwt_required()
    user_id = UUID(auth.get_jwt_subject())

    await channel_uc.set_channel_logo(
        channel_id = channel_id,
        requester_id = user_id,
        logo = logo.file
    )

    return



@channel_routers.delete(
        "/{channel_id}/logo", 
        summary = 'Удалить логотип канала'
        )
async def delete_channel_logo(channel_id: UUID, auth: AuthJWT = Depends()):
    auth.jwt_required()
    user_id = UUID(auth.get_jwt_subject())

    return await channel_uc.delete_channel_logo(
        channel_id = channel_id,
        requester_id=  user_id
    )




