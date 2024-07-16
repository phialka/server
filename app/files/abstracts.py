from abc import ABC, abstractmethod
from typing import BinaryIO, Optional
from uuid import UUID
from pydantic import BaseModel

from files.schemas import File



class FileFilter(BaseModel):
    file_id: Optional[UUID] = None
    download_id: Optional[UUID] = None



class FileRepo(ABC):
    """
    Abstract repo for file objects
    """

    @abstractmethod
    async def save(self, file: File) -> bool:
        pass

    @abstractmethod
    async def get(self, filter: FileFilter) -> list[File]:
        pass

    @abstractmethod
    async def update(self, filter: FileFilter, **kwargs) -> int:
        pass

    @abstractmethod
    async def delete(self, filter: FileFilter) -> int:
        pass



class FileStorage(ABC):
    """
    Abstract file storage
    """

    @abstractmethod
    async def save(self, bin_file: BinaryIO, save_as: str) -> UUID:
        pass

    @abstractmethod
    async def get(self, download_id: UUID) -> bytes:
        pass

