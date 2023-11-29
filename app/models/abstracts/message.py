from abc import ABCMeta, abstractmethod
from typing import Optional

from pydantic import BaseModel



class AbsMessage(BaseModel):
    __metaclass__ = ABCMeta

    id: int
    type: str
    dialog_id: Optional[int]
    conversation_id: Optional[int]
    author_id: int
    content: Optional[str]
    attach_files: Optional[list[int]]
    forwarded_messages: Optional[list[int]]
    answer_to: Optional[int]
    created_at: int
    updated_at: int
