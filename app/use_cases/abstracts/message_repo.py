from abc import ABC, abstractmethod
from entities import ChannelMessage, PrivateMessage, Message
from ..datamodels.filters import MessageFilter, ChannelMessageFilter, PrivateMessageFilter

from typing import Optional, Union
from datetime import date



class ChannelMessageRepo(ABC):
    """
    Abstract repo for channel message objects
    """

    @abstractmethod
    async def save(self, message: ChannelMessage) -> bool:
        pass

    @abstractmethod
    async def get(self, filter: Optional[ChannelMessageFilter] = None) -> list[ChannelMessage]:
        pass

    @abstractmethod
    async def update(self, filter: Optional[ChannelMessageFilter] = None, **kwargs) -> int:
        pass

    @abstractmethod
    async def delete(self, filter: Optional[ChannelMessageFilter] = None) -> int:
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
