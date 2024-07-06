from uuid import UUID

from fastapi import APIRouter, UploadFile, Response, status, Depends, Request

from use_cases.authentification_usecases import AuthUseCases
from adapters.auth_data_repo import SQLAuthDataRepo
from adapters.jwt_manager import FastAPIBasedJWTManager
from .schemas.auth import Login, RefreshLogin, LoginSuccess, RefreshLoginSuccess

import config


auth_routers = APIRouter(
    prefix = "/auth",
    tags = ["auth"]
)



uc = AuthUseCases(repo=SQLAuthDataRepo(), jwt_manager=FastAPIBasedJWTManager('super_secret'))



@auth_routers.post(
        "", 
        summary = 'Получить JWT токен по логину и паролю',
        response_model = LoginSuccess
        )
async def login(data: Login):
    access, refresh = await uc.get_jwt_by_logpass(data.username, data.userpass)

    return LoginSuccess(token=access, refresh=refresh)



@auth_routers.post(
        "/refresh", 
        summary = 'Получить JWT токен по refresh-токену',
        response_model = LoginSuccess
        )
async def refresh_login(data: RefreshLogin):
    access, refresh = await uc.refresh_jwt(data.refresh_token)
    return LoginSuccess(token=access, refresh=refresh)