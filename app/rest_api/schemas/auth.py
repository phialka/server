from pydantic import BaseModel
from uuid import UUID


#==================== REQUESTS SCHEMAS ====================

class Login(BaseModel):
        """
        scheme for validating user login request data
        """
        username: str
        userpass: str



class RefreshLogin(BaseModel):
        """
        scheme for validating user login request data
        """
        refresh_token: str



#==================== RESPONSE SCHEMAS ====================



class LoginSuccess(BaseModel):
        """
        scheme for validating user login request data
        """
        token: str
        refresh: str
        


class RefreshLoginSuccess(BaseModel):
        """
        scheme for validating user login request data
        """
        token: str
        refresh: str