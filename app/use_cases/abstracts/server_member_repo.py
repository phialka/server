from abc import ABC, abstractmethod
from entities import ServerMember
from ..datamodels.filters import ServerMemberFilter

from typing import Optional
from datetime import date



class ServerMemberRepo(ABC):

    @abstractmethod
    async def save(self, member: ServerMember) -> bool:
        pass

    @abstractmethod
    async def get(self, filter: Optional[ServerMemberFilter] = None) -> list[ServerMember]:
        pass

    @abstractmethod
    async def update(self, filter: Optional[ServerMemberFilter] = None, **kwargs) -> int:
        pass

    @abstractmethod
    async def delete(self, filter: Optional[ServerMemberFilter] = None) -> int:
        pass