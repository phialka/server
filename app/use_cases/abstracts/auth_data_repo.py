from abc import ABC, abstractmethod
from entities import AuthData, AuthDataFilter



class AuthDataRepo(ABC):

    @abstractmethod
    async def save(self, data: AuthData) -> bool:
        pass

    @abstractmethod
    async def get(self, filter: AuthDataFilter) -> list[AuthData]:
        pass

    @abstractmethod
    async def update(self, filter: AuthDataFilter, **kwargs) -> int:
        pass

    @abstractmethod
    async def delete(self, filter: AuthDataFilter) -> int:
        pass