from abc import ABC, abstractmethod
from entities import Server, ServerFilter

from typing import Optional
from datetime import date



class ServerRepo(ABC):

    @abstractmethod
    async def save(self, server: Server) -> bool:
        pass

    @abstractmethod
    async def get(self, filter: Optional[ServerFilter] = None) -> list[Server]:
        pass

    @abstractmethod
    async def update(self, filter: Optional[ServerFilter] = None, **kwargs) -> int:
        pass

    @abstractmethod
    async def delete(self, filter: Optional[ServerFilter] = None) -> int:
        pass