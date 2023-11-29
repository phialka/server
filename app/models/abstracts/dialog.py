from abc import ABCMeta, abstractmethod
from typing import Optional, Union

from pydantic import BaseModel
from enum import Enum



class AbsDialog(BaseModel):
    __metaclass__ = ABCMeta

    id: int
    user_ids: set[int]