from fastapi import Request, Response
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from fastapi.security import HTTPBearer

import config

#class-adapter for authorization using JWT
class JWTAuth():
    auth_mainclass = AuthJWT
    auth_exeption = AuthJWTException
    auth_scheme = HTTPBearer(scheme_name='JWT access token')

    def __init__(self, req: Request = None, res: Response = None):
        self.auth = AuthJWT(req, res)

    @classmethod
    def load_settings(cls, settings: BaseModel):
        cls.auth_mainclass.load_config(settings)

    def get_jwt_subject(self):
        return self.auth.get_jwt_subject()

    def jwt_required(self):
        self.auth.jwt_required()

    def jwt_refresh_token_required(self):
        self.auth.jwt_refresh_token_required()

    def create_access_token(self, subject):
        return self.auth.create_access_token(subject=subject)

    def create_refresh_token(self, subject):
        return self.auth.create_refresh_token(subject=subject)


class Settings(BaseModel):
        authjwt_secret_key: str = config.JWT_SECRET_KEY

JWTAuth.load_settings(Settings)
