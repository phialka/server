from fastapi import APIRouter

from auth.schemas import AuthDataBasic, AuthDataRefresh, TokenSet
from auth.use_caces import AuthUseCases
from auth.adapters import SQLAuthDataRepo, JWTManager



import config



auth_routers = APIRouter(
    prefix = "/auth",
    tags = ["auth"]
)



auth_uc = AuthUseCases(
    repo=SQLAuthDataRepo(), 
    jwt_manager=JWTManager(
        key = config.JWT_SECRET_KEY, 
        access_ttl=config.JWT_ACCESS_TTL, 
        refersh_ttl=config.JWT_REFRESH_TTL
        )
    )



@auth_routers.post(
        "", 
        summary = 'Получить JWT токен по логину и паролю',
        response_model = TokenSet
        )
async def login(data: AuthDataBasic):
    access, refresh = await auth_uc.get_jwt_by_logpass(data.username, data.userpass)

    return TokenSet(token=access, refresh=refresh)



@auth_routers.post(
        "/refresh", 
        summary = 'Получить JWT токен по refresh-токену',
        response_model = TokenSet
        )
async def refresh_login(data: AuthDataRefresh):
    access, refresh = await auth_uc.refresh_jwt(data.refresh_token)
    return TokenSet(token=access, refresh=refresh)
