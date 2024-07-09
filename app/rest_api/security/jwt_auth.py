from typing import Annotated, Any

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends

from adapters.jwt_manager import JWTManager

import config



auth_scheme = HTTPBearer(scheme_name='JWT')
jwt_manager = JWTManager(
    key = config.JWT_SECRET_KEY
)



def get_user_id(token: Annotated[HTTPAuthorizationCredentials, Depends(auth_scheme)]) -> str:
    token_string = token.credentials
    return jwt_manager.get_jwt_subject(token_string)
