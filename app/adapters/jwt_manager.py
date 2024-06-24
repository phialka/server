from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel

from typing import Optional

from use_cases.abstracts import JWTManager

import config



class FastAPIBasedJWTManager(JWTManager):
    def __init__(self, secret: str) -> None:
        AuthJWT.load_config(lambda:[('authjwt_secret_key', secret)])
        self.__magic_tool: AuthJWT = AuthJWT()

    def create_access_token(self, subject: str, exp_time: int, headers: Optional[dict] = {}, payload: Optional[dict] = {}) -> str:
        return self.__magic_tool.create_access_token(subject=subject, expires_time=exp_time, headers=headers, user_claims=payload)


    def create_refresh_token(self, subject: str, exp_time: int, headers: Optional[dict] = {}, payload: Optional[dict] = {}) -> str:
        return self.__magic_tool.create_refresh_token(subject=subject, expires_time=exp_time, headers=headers, user_claims=payload)


    def get_jwt_subject(self, token: str) -> str:
        self.__magic_tool._token = token
        return self.__magic_tool.get_jwt_subject()


