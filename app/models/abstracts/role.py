from abc import ABCMeta, abstractmethod
from typing import Optional, Union

from pydantic import BaseModel
from enum import Enum


class AbsRole(BaseModel):
    __metaclass__ = ABCMeta

    class Permissions(Enum):
        TEXT_MESSAGES = 1
        VOICE_MESSAGES = 2

    id: int
    role_id: int
    title: str
    description: str
    permissions: set[Permissions]