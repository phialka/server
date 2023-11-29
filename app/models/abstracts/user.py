from abc import ABCMeta, abstractmethod
from typing import Optional

from pydantic import BaseModel

from models.filter import ConditionTreeNode



class AbsUser(BaseModel):
    __metaclass__ = ABCMeta

    id: int
    name: str
    shortname: str
    description: Optional[str]
    photo_id: Optional[int]
    last_time: int
    created_at: int

    _F = ConditionTreeNode.create_accessor(__annotations__)

    @abstractmethod
    async def get(cls, filter: ConditionTreeNode) -> list["AbsUser"]:
        "Get User"

    @abstractmethod
    async def add(cls, name: str, shortname: str,  photo_id: Optional[int] = None, description: Optional[str] = None) -> int:
        "Add User"

    @abstractmethod
    async def update(
            cls, 
            id: int,
            name: Optional[str] = None, 
            shortname: Optional[str] = None,  
            photo_id: Optional[int] = None, 
            description: Optional[str] = None,
            last_time: Optional[int] = None
            ) -> int:
        "Update User"

    @abstractmethod
    async def delete(cls, filter: ConditionTreeNode) -> int:
        "Delete User"