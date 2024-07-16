from typing import BinaryIO
from uuid import UUID, uuid4
from hashlib import md5
from datetime import datetime
from mimetypes import guess_type

from files.schemas import File
from files.abstracts import FileRepo, FileStorage, FileFilter
from exceptions import NotFoundException



class FileUseCases():
    def __init__(self, file_repo: FileRepo, file_storage: FileStorage) -> None:
        self.__repo: FileRepo = file_repo
        self.__storage: FileStorage = file_storage


    async def upload_file(self, bin_file: BinaryIO) -> File:
        byte_size = bin_file.seek(0, 2)
        bin_file.seek(0)

        download_id = uuid4()
        await self.__storage.save(bin_file, download_id)

        file = File(
            file_id = uuid4(),
            download_id = download_id,
            size = byte_size,
            hash = md5(bin_file.read()).hexdigest(),
            mime_type = 'unknown',
            upload_at = datetime.now()
        )

        await self.__repo.save(file)

        return file


    async def get_file_by_id(self, file_id: UUID) -> File:
        files = await self.__repo.get(
            filter = FileFilter(file_id=file_id)
            )

        if len(files)<1:
            raise NotFoundException(msg='File not found')
        return files[0]


    async def download_file_by_download_id(self, download_id: UUID) -> bytes:
        try:
            file_bytes = await self.__storage.get(download_id)
        except FileNotFoundError:
            raise NotFoundException(msg='File not found')
        return file_bytes
