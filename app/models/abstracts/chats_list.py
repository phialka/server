from abc import ABCMeta, abstractmethod
from typing import Optional

from pydantic import BaseModel



class AbsChatsList(BaseModel):
    __metaclass__ = ABCMeta

    id: int
    owner_id: int
    conversation_ids: Optional[set[int]]
    chat_ids: Optional[set[int]]