from fastapi import APIRouter, Response, Depends, Cookie, Request
from utils.fastapi_jwt_auth import auth_scheme

from auth.schemas import AuthDataBasic, AuthDataRefresh, TokenSet
from auth.use_caces import AuthUseCases
from auth.adapters import SQLAuthDataRepo, JWTManager



import config



login_routers = APIRouter(
    prefix = "/auth",
    tags = ["auth"]
)

auth_routers =APIRouter(
    prefix = "/auth",
    tags = ["auth"],
    dependencies=[Depends(auth_scheme)]
)



auth_uc = AuthUseCases(
    repo=SQLAuthDataRepo(), 
    jwt_manager=JWTManager(
        key = config.JWT_SECRET_KEY, 
        access_ttl=config.JWT_ACCESS_TTL, 
        refersh_ttl=config.JWT_REFRESH_TTL
        )
    )



@login_routers.post(
        "", 
        summary = 'Получить JWT токен по логину и паролю'
        )
async def login(data: AuthDataBasic, res: Response):
    access, refresh = await auth_uc.get_jwt_by_logpass(data.username, data.password)
    res.set_cookie(
        key='access_token',
        value=access,
        secure=False,
        httponly=True,
        path='/'
    )
    res.set_cookie(
        key='refresh_token',
        value=refresh,
        secure=False,
        httponly=True,
        path='/auth/refresh'
    )
    res.set_cookie(
        key='refresh_token',
        value=refresh,
        secure=False,
        httponly=True,
        path='/auth/logout'
    )

    return



@auth_routers.get(
        "/refresh", 
        summary = 'Получить JWT токен по refresh-токену'
        )
async def refresh_login(requeset: Request, res: Response):
    refresh_token: str = requeset.cookies.get('refresh_token')
    print('\n\n\n' + refresh_token + '\n\n\n')
    access, refresh = await auth_uc.refresh_jwt(refresh_token)
    res.set_cookie(
        key='access_token',
        value=access,
        secure=False,
        httponly=True,
        path='/'
    )
    res.set_cookie(
        key='refresh_token',
        value=refresh,
        secure=False,
        httponly=True,
        path='/auth/refresh'
    )
    res.set_cookie(
        key='refresh_token',
        value=refresh,
        secure=False,
        httponly=True,
        path='/auth/logout'
    )
    return



@auth_routers.delete(
    "/logout",
    summary='Завершить сессию'
)
async def logout(requeset: Request, res: Response):
    access_token: str = requeset.cookies.get('access_token')
    refresh_token: str = requeset.cookies.get('refresh_token')
    res.set_cookie(
        key='access_token',
        value=access_token,
        expires=0,
        secure=False,
        httponly=True,
        path='/'
    )
    res.set_cookie(
        key='refresh_token',
        value=refresh_token,
        expires=0,
        secure=False,
        httponly=True,
        path='/auth/refresh'
    )
    res.set_cookie(
        key='refresh_token',
        value=refresh_token,
        expires=0,
        secure=False,
        httponly=True,
        path='/auth/logout'
    )
    return