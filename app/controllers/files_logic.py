import hashlib
import time
import os
import itertools
from typing import BinaryIO

from starlette.responses import Response
from fastapi import UploadFile
from PIL import Image

from dbmodels import *
import config



class SavedFile():
    def __init__(self, file: UploadFile) -> None:
        self.__type: str = file.content_type
        self.__name = file.filename
        self.__file: BinaryIO = file.file
        self.file_in_db: File
        self.__size: int 
        self.__hash: str 
        self.__info: FileInfoField
    
    @property
    def type(self) -> str:
        return self.__type

    @property
    def name(self) -> str:
        return self.__name

    @property
    def file(self) -> BinaryIO:
        return self.__file

    @property
    def size(self) -> int:
        return self.__size

    @property
    def hash(self) -> str:
        return self.__hash

    @property
    def info(self) -> FileInfoField:
        return self.__info


    async def __calculate_hash(self) -> str:
        """
        Calculates the hash sum of the file to verify uniqueness.
        """
        hash = hashlib.md5()
        hash.update(self.file.read())
        return hash.hexdigest()


    async def __get_filesize(self) -> int:
        """
        Returns the file size in bytes.
        """
        self.file.seek(0, 2)
        size = self.file.tell()
        self.file.seek(0, 0)
        return size


    async def __create_typeinfo(self) -> Union[PhotoTypeInfo, VideoTypeInfo, AudioTypeInfo, None]:
        """
        Creates a type_info object specific to files of different types.
        """
        mimetype = (self.type).split("/")

        if mimetype[0] == "image":
            image = Image.open(self.file)
            width, height = image.size
            return PhotoTypeInfo(width=width, height=height)
        return None

    
    async def __create_info(self) -> FileInfoField:
        info = FileInfoField(
            type = self.type,
            title = self.name,
            size = self.size,
            upload_at = time.time(),
            type_info = await self.__create_typeinfo(),
            url = f"http://{config.HOST}:{config.PORT}/file/{self.hash}"
        )
        return info


    async def save(self):
        self.__hash = await self.__calculate_hash()

        file_already_saved = await File.objects.get_or_none(hash=self.hash)
        if file_already_saved:
            self.file_in_db = file_already_saved
            self.__info = file_already_saved.prepared_info
            self.__size = self.info.size
            return self

        self.__size = await self.__get_filesize()
        self.__info = await self.__create_info()

        path = f'{config.FILE_STORAGE}\{self.hash[0:2]}\{self.hash[2:4]}'
        with open(f"{path}\{self.hash}", "wb") as new_file:
            self.file.seek(0,0)
            new_file.write(self.file.read())
        self.file_in_db = await File.objects.create(hash=self.hash, info=self.info.json(), path=path)
        return self



class Storage():
    def __init__(self) -> None:
        pass

    @classmethod
    def create_storage(cls) -> None:
        """
        Creates a directory for storing files on the server.
        """
        def create(path, echo):
            if not os.path.isdir(path):
                os.mkdir(path)
            if echo:
                return path
        create(config.FILE_STORAGE, False)
        duos = [d[0]+d[1] for d in itertools.product('0123456789abcdef', repeat=2)]
        first_level = [create(f"{config.FILE_STORAGE}\{sub}", True) for sub in duos]
        second_level = [[create(f"{path}\{sub}", False) for sub in duos] for path in first_level]


    @classmethod
    async def save_to_server(cls, file: UploadFile) -> SavedFile:
        """
        Saves the uploaded file to the storage, registers it in the database
        """
        sfile = SavedFile(file)
        return await sfile.save()
    

    @classmethod
    async def get_file(cls, file_hash: str) -> Response:
        """
        Returns the Response object with the uploaded file
        """
        file = await File.objects.get_or_none(hash=file_hash)
        with open(f"{file.path}\{file.hash}", "rb") as data:
            return Response(content=data.read(), media_type=file.info["type"], status_code=200)

