from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, UploadFile, Response, status, Depends, Request
from fastapi.responses import FileResponse
from .security.jwt_auth import auth_scheme, get_user_id

from entities import File
from use_cases.files_usecases import FileUseCases

from adapters.file_repo import SQLFileRepo
from adapters.file_storage import SystemFileStorage

import config


files_router = APIRouter(
    prefix = "/files",
    tags = ["files"],
    dependencies=[Depends(auth_scheme)]
)



uc = FileUseCases(SQLFileRepo(), SystemFileStorage(config.FILE_STORAGE))



@files_router.post(
        "", 
        summary = 'Загрузить файл на сервер',
        response_model = File
        )
async def upload_file_to_server(file: UploadFile, user_id: str = Depends(get_user_id)):
    return await uc.upload_file(file.file)



@files_router.get(
        "/{file_id}", 
        summary = 'Получить информацию о файле по file_id',
        response_model = File,
        include_in_schema=True
        )
async def get_file_info(file_id: UUID, user_id: str = Depends(get_user_id)):
    return await uc.get_file_by_id(file_id)



@files_router.get(
        "/download/{download_id}",
        summary = 'Скачать файл по его download_id',
        response_class = FileResponse,
        responses = {
            status.HTTP_200_OK: {
                'content': {'application/octet-stream': {}}
            },
            status.HTTP_404_NOT_FOUND: {}
        }
        )
async def get_file(download_id: UUID, user_id: str = Depends(get_user_id)):
    file_bytes = await uc.download_file_by_download_id(download_id)

    return Response(content=file_bytes, status_code=200)
