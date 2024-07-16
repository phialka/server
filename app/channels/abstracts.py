from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from channels.schemas import Channel, ChannelMessage



class ChannelFilter(BaseModel):
    channel_id: Optional[UUID] = None
    server_id: Optional[UUID] = None



class ChannelMessageFilter(BaseModel):
    channel_id: Optional[UUID] = None
    sequence_min: Optional[int] = None



class ChannelRepo(ABC):
    """
    Abstract repo for channel objects
    """

    @abstractmethod
    async def save(self, channel: Channel) -> bool:
        pass


    @abstractmethod
    async def get(self, filter: Optional[ChannelFilter] = None) -> list[Channel]:
        pass


    @abstractmethod
    async def update(self, filter: Optional[ChannelFilter] = None, **kwargs) -> int:
        pass


    @abstractmethod
    async def delete(self, filter: Optional[ChannelFilter] = None) -> int:
        pass



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
