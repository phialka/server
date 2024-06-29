from abc import ABC, abstractmethod
from entities import Channel, ChannelFilter

from typing import Optional
from datetime import date



class ChannelRepo(ABC):

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
