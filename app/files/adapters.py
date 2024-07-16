from typing import BinaryIO, Optional
from uuid import UUID

from files.schemas import File
from files.abstracts import FileRepo, FileFilter, FileStorage
from files.dbmodels import File as DBFile

from utils.file_storage import Storage



class SQLFileRepo(FileRepo):

    def __init__(self) -> None:
        self.__table = DBFile


    async def save(self, file: File) -> bool:
        await self.__table.objects.create(
            id = file.file_id,
            download_id  = file.download_id,
            hash = file.hash,
            mime_type = file.mime_type,
            size = file.size,
            upload_at = file.upload_at
        )

        return True


    async def get(self, filter: FileFilter) -> list[File]:
        if filter.file_id:
            files = await self.__table.objects.all(self.__table.id == filter.file_id)
            files = [File(
                file_id=f.id,
                download_id=f.download_id,
                size=f.size,
                hash=f.hash,
                mime_type=f.mime_type,
                upload_at=f.upload_at
                ) for f in files]
        else:
            files = []

        return files


    async def update(self, filter: Optional[FileFilter] = None, **kwargs) -> int:
        pass


    async def delete(self, filter: Optional[FileFilter] = None) -> int:
        if filter.file_id:
            files_count = await self.__table.objects.delete(self.__table.id == filter.file_id)
        else:
            files_count = 0
        return files_count



# class JsonFileRepo(FileRepo):
#     pass



class SystemFileStorage(FileStorage):

    def __init__(self, path: str) -> None:
        self.__storage = Storage(path)


    async def save(self, bin_file: BinaryIO, save_as: str) -> UUID:
        return await self.__storage.save_file(bin_file, save_as)


    async def get(self, download_id: UUID) -> bytes:
        return await self.__storage.get_file(download_id)
