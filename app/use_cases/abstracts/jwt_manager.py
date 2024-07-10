from abc import ABC, abstractmethod
from typing import Optional



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
