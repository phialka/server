from uuid import UUID
from typing import Optional

from fastapi import APIRouter, UploadFile, Depends
from utils.fastapi_jwt_auth import auth_scheme, get_user_id

from channels.schemas import Channel, ChannelCreate, ChannelUpdate, ChannelMessage
from channels.use_cases import ChannelUseCases
from channels.adapters import SQLChannelRepo, SQLChannelMessageRepo

from files.adapters import SQLFileRepo, SystemFileStorage
from users.adapters import SQLUserRepo
from auth.adapters import SQLAuthDataRepo

from messages.schemas import MessageCerate
from messages.adapters import SQLMessageRepo

from servers.adapters import SQLServerRepo, SQLServerMemberRepo
from servers.routers import server_routers

import config



channel_routers = APIRouter(
    prefix = "/channels",
    tags = ["channels"],
    dependencies=[Depends(auth_scheme)]
)



channel_uc = ChannelUseCases(
        channel_repo=SQLChannelRepo(),
        channel_msg_repo=SQLChannelMessageRepo(),
        file_repo=SQLFileRepo(),
        file_storage=SystemFileStorage(
            path=config.FILE_STORAGE
        ),
        server_repo=SQLServerRepo(),
        member_repo=SQLServerMemberRepo(),
        user_repo=SQLUserRepo(),
        auth_repo=SQLAuthDataRepo(),
        msg_repo=SQLMessageRepo()
    )



@channel_routers.post(
        "", 
        summary = 'Создать текстовый канал'
        )
async def create_channel(data: ChannelCreate, user_id: str = Depends(get_user_id)):
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
async def edit_channel(data: ChannelUpdate, channel_id: UUID, user_id: str = Depends(get_user_id)):
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
async def delete_channel(channel_id: UUID, user_id: str = Depends(get_user_id)):
    return await channel_uc.delete_channel(
        requester_id = user_id,
        channel_id = channel_id
    )



@channel_routers.get(
        "/{channel_id}", 
        summary = 'Получить информацию о текстовом канале',
        response_model = Channel
        )
async def get_channel_info(channel_id: UUID, user_id: str = Depends(get_user_id)):
    return await channel_uc.get_channel_by_id(channel_id=channel_id)



@channel_routers.put(
        "/{channel_id}/logo", 
        summary = 'Установить логотип канала'
        )
async def set_channel_logo(channel_id: UUID, logo: UploadFile, user_id: str = Depends(get_user_id)):
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
async def delete_channel_logo(channel_id: UUID, user_id: str = Depends(get_user_id)):
    return await channel_uc.delete_channel_logo(
        channel_id = channel_id,
        requester_id=  user_id
    )



@channel_routers.post(
        "/{channel_id}/sendMessage", 
        summary = 'Отправить сообщение в текстовый канал',
        tags=['messages']
        )
async def send_message_to_channel(channel_id: UUID, msg: MessageCerate, requester_id: str = Depends(get_user_id)):
    await channel_uc.create_channel_message(requester_id=requester_id, channel_id=channel_id, msg_data=msg)

    return



@channel_routers.get(
        "/{channel_id}/messages", 
        summary = 'Получить сообщения из текстового канала',
        response_model = list[ChannelMessage],
        tags=['messages']
        )
async def get_messages_from_chat(channel_id: UUID, sequence: int, count: Optional[int] = 10, user_id: str = Depends(get_user_id)):
    return await channel_uc.get_channel_messages(requester_id=user_id, channel_id=channel_id, sequence_min=sequence, count=count)



@server_routers.get(
        "/{server_id}/getChannels", 
        summary = 'Получить список текстовых каналов на сервере',
        response_model = list[Channel]
        )
async def get_server_channels(server_id: UUID, user_id: str = Depends(get_user_id)):
    return await channel_uc.get_channels_by_server_id(requester_id=user_id, server_id=server_id)
