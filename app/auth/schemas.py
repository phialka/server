from uuid import UUID

from pydantic import BaseModel



class AuthData(BaseModel):
    user_id: UUID
    login: str
    password_hash: str



class AuthDataBasic(BaseModel):
        """
        scheme for validating user login request data
        """
        username: str
        userpass: str



class AuthDataRefresh(BaseModel):
        """
        scheme for validating user login request data
        """
        refresh_token: str



class TokenSet(BaseModel):
        """
        scheme for validating user login request data
        """
        token: str
        refresh: str
