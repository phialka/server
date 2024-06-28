from abc import ABC, abstractmethod
from entities import Message, ChannelMessage, PrivateMessage, MessageFilter

from typing import Optional, Union
from datetime import date



class ChannelMessageRepo(ABC):

    @abstractmethod
    async def save(self, message: ChannelMessage) -> bool:
        pass

    @abstractmethod
    async def get(self, filter: Optional[ChannelMessageFilter] = None) -> list[ChannelMessage]:
        pass

    @abstractmethod
    async def update(self, filter: Optional[MessageFilter] = None, **kwargs) -> int:
        pass

    @abstractmethod
    async def delete(self, filter: Optional[MessageFilter] = None) -> int:
        pass
