from abc import ABC, abstractmethod
from uuid import UUID
from typing import BinaryIO
from entities import File



class FileStorage(ABC):

    @abstractmethod
    async def save(bin_file: BinaryIO, save_as: str) -> UUID:
        pass

    @abstractmethod
    async def get(download_id: UUID) -> str:
        pass
