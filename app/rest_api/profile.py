from uuid import UUID

from fastapi import APIRouter, UploadFile, Response, status, Depends, Request
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT

from entities import User
from use_cases.profile_usecases import ProfileUseCases
from use_cases.files_usecases import FileUseCases
from adapters.file_repo import SQLFileRepo
from adapters.file_storage import SystemFileStorage
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



file_uc = FileUseCases(SQLFileRepo(), SystemFileStorage(config.FILE_STORAGE))
uc = ProfileUseCases(SQLUserRepo(), SQLAuthDataRepo(), file_uc)



@register_routers.post(
        "", 
        summary = 'Создать профиль',
        response_model = User
        )
async def register(user: UserCreate):
    user = await uc.register(user.name, user.login, user.password, user.tag, user.description, user.birthdate)
    return user


