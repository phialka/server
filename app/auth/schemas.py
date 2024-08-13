from uuid import UUID

from pydantic import BaseModel



class AuthData(BaseModel):
    user_id: UUID
    username: str
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
        refresh: str



class TokenSet(BaseModel):
        """
        scheme for validating user login request data
        """
        access: str
        refresh: str
