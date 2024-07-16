from abc import ABC, abstractmethod
from typing import Optional
from datetime import date
from pydantic import BaseModel
from uuid import UUID

from servers.schemas import Server, ServerMember



class ServerFilter(BaseModel):
    server_id: Optional[UUID] = None
    owner_id: Optional[UUID] = None
    title_search_prompt: Optional[str] = None
    description_search_prompt: Optional[str] = None



class ServerMemberFilter(BaseModel):
    server_id: Optional[UUID] = None
    user_id: Optional[UUID] = None



class ServerRepo(ABC):
    """
    Abstract repo for server objects
    """

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



class ServerMemberRepo(ABC):
    """
    Abstract repo for server member objects
    """

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
