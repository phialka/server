from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


from private_chats.schemas import PrivateChat, PrivateMessage



class PrivateChatFilter(BaseModel):
    chat_id: Optional[UUID] = None
    member_ids: Optional[list[UUID]] = None



class PrivateMessageFilter(BaseModel):
    chat_id: Optional[UUID] = None
    sequence_min: Optional[int] = None



class PrivateChatRepo(ABC):
    """
    Abstract repo for private chat objects
    """

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



class PrivateMessageRepo(ABC):
    """
    Abstract repo for private message objects
    """

    @abstractmethod
    async def save(self, message: PrivateMessage) -> bool:
        pass

    @abstractmethod
    async def get(self, filter: Optional[PrivateMessageFilter] = None) -> list[PrivateMessage]:
        pass

    @abstractmethod
    async def update(self, filter: Optional[PrivateMessageFilter] = None, **kwargs) -> int:
        pass

    @abstractmethod
    async def delete(self, filter: Optional[PrivateMessageFilter] = None) -> int:
        pass
