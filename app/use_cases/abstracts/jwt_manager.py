from abc import ABC, abstractmethod
from typing import Optional


class JWTManager(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def create_access_token(self, subject: str, exp_time: int, headers: Optional[dict] = {}, payload: Optional[dict] = {}) -> str:
        pass

    @abstractmethod
    def create_refresh_token(self, subject: str, exp_time: int, headers: Optional[dict] = {}, payload: Optional[dict] = {}) -> str:
        pass

    @abstractmethod
    def get_jwt_subject(self, token: str) -> str:
        pass


