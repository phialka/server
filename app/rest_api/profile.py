from uuid import UUID

from fastapi import APIRouter, UploadFile, Response, status, Depends, Request
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT

from entities import User
from use_cases.profile_usecases import ProfileUseCases
from adapters.file_repo import SQLFileRepo
from adapters.auth_data_repo import SQLAuthDataRepo
from adapters.user_repo import SQLUserRepo
from .schemas.profile import UserCreate

import config


profile_routers = APIRouter(
    prefix = "/profile",
    tags = ["profile"],
    dependencies=[Depends(HTTPBearer(scheme_name='JWT'))]
)


register_routers = APIRouter(
    prefix = "/profile",
    tags = ["profile"]
)


uc = ProfileUseCases(SQLUserRepo(), SQLAuthDataRepo())



@register_routers.post(
        "", 
        summary = 'Создать профиль',
        response_model = User
        )
async def register(user: UserCreate):
    user = await uc.register(user.name, user.login, user.password)
    return user


