from typing import Annotated, Any
from uuid import UUID

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends

from auth.adapters import JWTManager

import config



auth_scheme = HTTPBearer(scheme_name='JWT')
jwt_manager = JWTManager(
    key = config.JWT_SECRET_KEY,
    access_ttl=config.JWT_ACCESS_TTL,
    refersh_ttl=config.JWT_REFRESH_TTL
)



def get_user_id(token: Annotated[HTTPAuthorizationCredentials, Depends(auth_scheme)]) -> UUID:
    token_string = token.credentials
    return UUID(jwt_manager.get_jwt_subject(token_string))
