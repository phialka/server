from abc import ABC, abstractmethod
from entities import AuthData, AuthDataFilter
from typing import Optional

from pydantic import BaseModel



class AuthDataRepo(ABC):

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