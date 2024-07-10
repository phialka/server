from abc import ABC, abstractmethod
from entities import User, File
from ..datamodels.filters import UserFilter

from typing import Optional
from datetime import date



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
