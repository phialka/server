import os
import itertools
from typing import BinaryIO

from PIL import Image



class Storage():
    def __init__(self, storage_directory: str) -> None:
        self.__directory = storage_directory


    @classmethod
    async def create_storage(cls, path: str) -> 'Storage':
        """
        Creates a directory for storing files on the server.
        """
        def create(path, echo):
            if not os.path.isdir(path):
                os.mkdir(path)
            if echo:
                return path
            
        create(path, False)

        return Storage(path)


    async def save_file(self, file: BinaryIO, save_as: str) -> bool:
        """
        Save the file in the storage
        """
        with open(f'{self.__directory}/{save_as}', 'wb') as file_in_storage:
            file_in_storage.write(file.read())
        
        return True


    async def get_file_path(self, file_name: str) -> str:
        """
        Get a file path by file name from the storage
        """
        fullpath = f'{self.__directory}/{file_name}'

        if os.path.exists(fullpath):
            return fullpath
        else:
            raise FileNotFoundError


    async def get_file(self, file_name: str) -> bytes:
        """
        Get a file by name from the storage
        """
        fullpath = f'{self.__directory}/{file_name}'

        if os.path.exists(fullpath):
            with open(f'{self.__directory}/{file_name}', 'rb') as file_in_storage:
                return file_in_storage.read()
        else:
            raise FileNotFoundError


    async def delete_file(self, file_name: str) -> bool:
        """
        Delete a file with the specified name from the storage
        """
        fullpath = f'{self.__directory}/{file_name}'

        if os.path.exists(fullpath):
            os.remove(fullpath)
        else:
            raise FileNotFoundError
        

