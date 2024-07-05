from abc import ABC, abstractmethod
from entities import File
from ..datamodels.filters import FileFilter



class FileRepo(ABC):

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
