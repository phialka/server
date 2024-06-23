from use_cases.abstracts import FileRepo
from entities import File, FileFilter
from database import tables



class SQLFileRepo(FileRepo):

    def __init__(self) -> None:
        self.__table = tables.Files


    async def save(self, file: File) -> bool:
        await self.__table.objects.create(
            id = file.file_id,
            download_id  = file.download_id,
            hash = file.hash,
            mime_type = file.mime_type,
            size = file.size,
            upload_at = file.upload_at
    )


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


    async def update(self, filter: FileFilter, **kwargs) -> int:
        pass


    async def delete(self, filter: FileFilter) -> int:
        if filter.file_id:
            files_count = await self.__table.objects.delete(self.__table.id == filter.file_id)
        else:
            files_count = 0
        return files_count




# class JsonFileRepo(FileRepo):
#     pass