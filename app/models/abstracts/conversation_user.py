from abc import ABCMeta, abstractmethod
from typing import Optional, Union

from pydantic import BaseModel



class AbsConversationUser(BaseModel):
    __metaclass__ = ABCMeta

    id: int
    user_id: int
    conversation_id: int
    role_id: int