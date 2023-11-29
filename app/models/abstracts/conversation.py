from abc import ABCMeta, abstractmethod
from typing import Optional, Union

from pydantic import BaseModel



class AbsConversation(BaseModel):
    __metaclass__ = ABCMeta

    id: int
    title: str
    icon_file_id: Optional[int]
    description: Optional[str]
    owner_id: int
    users_count: int # derived field
    created_at: int