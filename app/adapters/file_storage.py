from typing import BinaryIO
from uuid import UUID

from use_cases.abstracts import FileStorage
from utils.file_storage import Storage



class SystemFileStorage(FileStorage):

    def __init__(self, path: str) -> None:
        self.__storage = Storage(path)


    async def save(self, bin_file: BinaryIO, save_as: str) -> UUID:
        return await self.__storage.save_file(bin_file, save_as)


    async def get(self, download_id: UUID) -> bytes:
        return await self.__storage.get_file(download_id)
