from abc import ABC, abstractmethod
from uuid import UUID
from typing import BinaryIO



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
