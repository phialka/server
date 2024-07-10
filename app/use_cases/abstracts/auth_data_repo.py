from abc import ABC, abstractmethod
from entities import AuthData
from ..datamodels.filters import AuthDataFilter
from typing import Optional

from pydantic import BaseModel



class AuthDataRepo(ABC):
    """
    Abstract repo for user auth data
    """

    @abstractmethod
    async def save(self, data: AuthData) -> bool:
        pass

    @abstractmethod
    async def get(self, filter: Optional[AuthDataFilter] = None) -> list[AuthData]:
        pass

    @abstractmethod
    async def update(self, 
                    filter: Optional[AuthDataFilter] = None,
                    new_password: Optional[str] = None
                    ) -> int:
        pass

    @abstractmethod
    async def delete(self, filter: Optional[AuthDataFilter] = None) -> int:
        pass