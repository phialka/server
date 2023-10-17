from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Optional

from pydantic import BaseModel



class AbsUser(BaseModel):
    __metaclass__ = ABCMeta

    id: int
    name: str
    shortname: str
    description: Optional[str]
    photo_id: Optional[int]
    last_time: int
    created_at: int

    @abstractmethod
    async def get(cls, user_id: int) -> list["AbsUser"]:
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
    async def delete(cls, user_id: int) -> int:
        "Delete User"



class AbsAuth(BaseModel):
    __metaclass__ = ABCMeta

    id: int
    user_id: int
    username: str
    userpass: str

    @abstractmethod
    async def get(cls, user_id: int) -> list["AbsAuth"]:
        "Get Auth"

    @abstractmethod
    async def add(
            cls, user_id: int, username: str, userpass: int) -> "AbsAuth":
        "Add Auth"

    @abstractmethod
    async def update(cls) -> int:
        "Update Auth"

    @abstractmethod
    async def delete(cls, auth_id: Optional[int] = None, user_id: Optional[int] = None) -> int:
        "Delete Auth"