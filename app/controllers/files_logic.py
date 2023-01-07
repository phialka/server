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
import schemas


class SavedFile():
    def __init__(self, id: Optional[int] = None) -> None:
        self.id: int
        if id:
            self.id = id
        self.__file: BinaryIO
        self.__hash: str
        self.__info: File.Info

        self.__dbfile: File

        self.__view: Union[schemas.Photo, schemas.Video, schemas.Audio]

    @property
    def file(self) -> BinaryIO:
        return self.__file

    @property
    def dbfile(self):
        return self.__dbfile

    @property
    def view(self):
        return self.__view


    async def __init_file(self):
        self.__dbfile = await File.objects.filter(File.id == self.id).get_or_none()
        self.__info = self.__dbfile.info_

    
    async def create_view(self):
        await self.__init_file()
        filedata = schemas.File(
            file_id=self.__dbfile.id,
            byte_syze=self.__info.size,
            media_type=self.__info.type,
            url=self.__info.url,
            upload_at=self.__info.upload_at
        )
        mimetype = filedata.media_type.split("/")
        if mimetype[0] == "image":
            self.__view = schemas.Photo(
                **filedata.dict(),
                width=self.__info.type_info.width,
                height=self.__info.type_info.height
            )
        else:
            self.__view = schemas.File(**filedata.dict())
        return self


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


    async def __create_typeinfo(self, file: UploadFile) -> Union[PhotoTypeInfo, VideoTypeInfo, AudioTypeInfo, None]:
        """
        Creates a type_info object specific to files of different types.
        """
        mimetype = (file.content_type).split("/")

        if mimetype[0] == "image":
            image = Image.open(self.file)
            width, height = image.size
            return PhotoTypeInfo(width=width, height=height)
        return None

    
    async def __create_info(self, file: UploadFile) -> File.Info:
        info = File.Info(
            type = file.content_type,
            title = file.filename,
            size = await self.__get_filesize(),
            upload_at = time.time(),
            type_info = await self.__create_typeinfo(file),
            url = f"http://{config.HOST}:{config.PORT}/file/{self.__hash}"
        )
        return info


    async def save(self, file: UploadFile):
        self.__file = file.file
        self.__hash = await self.__calculate_hash()

        file_already_saved = await File.objects.get_or_none(hash = self.__hash)
        if file_already_saved:
            self.__dbfile = file_already_saved
            self.id = self.__dbfile.id
            self.__info = self.__dbfile.info_
            return self
        
        info = await self.__create_info(file)
        path = f'{config.FILE_STORAGE}\{self.__hash[0:2]}\{self.__hash[2:4]}'
        self.__dbfile = await File.objects.create(hash=self.__hash, info=info.json(), path=path)
        self.id = self.__dbfile.id
        
        with open(f"{path}\{self.__hash}", "wb") as new_file:
            self.file.seek(0,0)
            new_file.write(self.file.read())
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
        return await SavedFile().save(file)
    

    @classmethod
    async def download_file(cls, file_hash: str) -> Response:
        """
        Returns the Response object with the uploaded file
        """
        file = await File.objects.get_or_none(hash=file_hash)
        with open(f"{file.path}\{file.hash}", "rb") as data:
            return Response(content=data.read(), media_type=file.info["type"], status_code=200)

