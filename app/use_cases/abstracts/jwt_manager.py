from abc import ABC, abstractmethod
from typing import Optional



class IJWTManager(ABC):
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
        pass

    @abstractmethod
    def is_access_token(self, token: str) -> bool:
        pass

    @abstractmethod
    def is_refresh_token(self, token: str) -> bool:
        pass
