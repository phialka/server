from abc import ABC, abstractmethod
from typing import Optional, Union
from datetime import date
from uuid import UUID
from pydantic import BaseModel

from messages.schemas import Message



class AttachmentFilter(BaseModel):
    message_id: Optional[UUID] = None



class MessageFilter(BaseModel):
    message_id: Optional[UUID] = None
    author_id: Optional[UUID] = None
    reply_message_id: Optional[UUID] = None



class MessageRepo(ABC):
    """
    Abstract repo for message objects
    """

    @abstractmethod
    async def save(self, message: Message) -> bool:
        pass

    @abstractmethod
    async def get(self, filter: Optional[MessageFilter] = None) -> list[Message]:
        pass

    @abstractmethod
    async def update(self, filter: Optional[MessageFilter] = None, **kwargs) -> int:
        pass

    @abstractmethod
    async def delete(self, filter: Optional[MessageFilter] = None) -> int:
        pass
