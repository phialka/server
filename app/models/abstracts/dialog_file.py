from abc import ABCMeta, abstractmethod
from typing import Optional, Union

from pydantic import BaseModel
from enum import Enum



class AbsDialogFile(BaseModel):
    __metaclass__ = ABCMeta

    id: int
    file_id: int
    dialog_id: int