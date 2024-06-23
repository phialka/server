from uuid import UUID

from fastapi import APIRouter, UploadFile, Response
from fastapi.responses import FileResponse

from entities import File
from use_cases.files_usecases import FileUseCases
from adapters.file_repo import SQLFileRepo
from adapters.file_storage import SystemFileStorage

import config


files_router = APIRouter(
    prefix = "/files",
    tags = ["files"]
)



uc = FileUseCases(SQLFileRepo(), SystemFileStorage(config.FILE_STORAGE))



@files_router.post(
        "", 
        summary = 'Загрузить файл на сервер',
        response_model = File
        )
async def upload_file_to_server(file: UploadFile):
    return await uc.upload_file(file.file)



@files_router.get(
        "/{file_id}", 
        summary = 'Получить информацию о файле по file_id',
        response_model = File,
        include_in_schema=True
        )
async def get_file_info(file_id: UUID):
    return await uc.get_file_by_id(file_id)



@files_router.get(
        "/download/{download_id}",
        summary = 'Скачать файл по его download_id',
        )
async def get_file(download_id: UUID):
    file_path = await uc.download_file_by_download_id(download_id)
    with open(file_path, 'rb') as f:
        return Response(content=f.read(), status_code=200)
