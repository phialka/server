from abc import ABCMeta, abstractmethod
from typing import Optional

from pydantic import BaseModel



class AbsConversationFile(BaseModel):
    __metaclass__ = ABCMeta

    id: int
    file_id: int
    conversation_id: int