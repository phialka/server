from abc import ABC, abstractmethod
from entities import PrivateChat, PrivateChatFilter

from typing import Optional



class PrivateChatRepo(ABC):

    @abstractmethod
    async def save(self, chat: PrivateChat) -> bool:
        pass


    @abstractmethod
    async def get(self, filter: Optional[PrivateChatFilter] = None) -> list[PrivateChat]:
        pass


    @abstractmethod
    async def update(self, filter: Optional[PrivateChatFilter] = None, **kwargs) -> int:
        pass


    @abstractmethod
    async def delete(self, filter: Optional[PrivateChatFilter] = None) -> int:
        pass
