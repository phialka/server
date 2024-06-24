from abc import ABC, abstractmethod
from entities import User, UserFilter



class UserRepo(ABC):

    @abstractmethod
    async def save(self, user: User) -> bool:
        pass

    @abstractmethod
    async def get(self, filter: UserFilter) -> list[User]:
        pass

    @abstractmethod
    async def update(self, filter: UserFilter, **kwargs) -> int:
        pass

    @abstractmethod
    async def delete(self, filter: UserFilter) -> int:
        pass
