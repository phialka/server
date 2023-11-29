from abc import ABCMeta, abstractmethod
from typing import Optional

from pydantic import BaseModel



class AbsAuth(BaseModel):
    __metaclass__ = ABCMeta

    id: int
    user_id: int
    username: str
    userpass: str

    @abstractmethod
    async def get(cls, username: str) -> list["AbsAuth"]:
        "Get Auth"

    @abstractmethod
    async def add(
            cls, user_id: int, username: str, userpass: int) -> int:
        "Add Auth"

    @abstractmethod
    async def update(cls, auth_id: int, username: Optional[str] = None, userpass: Optional[str] = None) -> int:
        "Update Auth"

    @abstractmethod
    async def delete(cls, auth_id: Optional[int] = None, user_id: Optional[int] = None) -> int:
        "Delete Auth"