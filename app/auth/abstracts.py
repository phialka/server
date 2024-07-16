from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel

from .schemas import AuthData



class AuthDataFilter(BaseModel):
    login: Optional[str] = None



class AuthDataRepo(ABC):
    """
    Abstract repo for user auth data
    """

    @abstractmethod
    async def save(self, data: AuthData) -> bool:
        pass

    @abstractmethod
    async def get(self, filter: Optional[AuthDataFilter] = None) -> list[AuthData]:
        pass

    @abstractmethod
    async def update(self, 
                    filter: Optional[AuthDataFilter] = None,
                    new_password: Optional[str] = None
                    ) -> int:
        pass

    @abstractmethod
    async def delete(self, filter: Optional[AuthDataFilter] = None) -> int:
        pass



class IJWTManager(ABC):
    """
    Abstract class for work with JWT
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def create_access_token(self, sub: str) -> bytes:
        pass

    @abstractmethod
    def create_refresh_token(self, sub: str) -> bytes:
        pass

    @abstractmethod
    def get_jwt_subject(self, token: str) -> str:
        """
        Get subject which encoded in token

        If token expired or invalid, raises exception
        """
        pass

    @abstractmethod
    def is_access_token(self, token: str) -> bool:
        """
        Check whether the token is an access token
        """

    @abstractmethod
    def is_refresh_token(self, token: str) -> bool:
        """
        Check whether the token is a refresh token
        """
        pass
