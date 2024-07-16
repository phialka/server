from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from .schemas import User



class UserFilter(BaseModel):
    user_id: Optional[UUID] = None
    tag: Optional[str] = None
    name: Optional[str] = None
    tag_search_prompt: Optional[str] = None
    name_search_prompt: Optional[str] = None



class UserRepo(ABC):
    """
    Abstract repo for user objects
    """

    @abstractmethod
    async def save(self, user: User) -> bool:
        pass

    @abstractmethod
    async def get(self, filter: Optional[UserFilter] = None) -> list[User]:
        pass

    @abstractmethod
    async def update(self, filter: Optional[UserFilter] = None, **kwargs) -> int:
        pass

    @abstractmethod
    async def delete(self, filter: Optional[UserFilter] = None) -> int:
        pass
