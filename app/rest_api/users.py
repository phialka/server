from uuid import UUID
from typing import Optional

from fastapi import APIRouter, UploadFile, Response, status, Depends, Request
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT

from entities import User, File
from use_cases.user_usecases import UserUseCases
from adapters.auth_data_repo import SQLAuthDataRepo
from adapters.user_repo import SQLUserRepo


import config



users_routers = APIRouter(
    prefix = "/users",
    tags = ["users"],
    dependencies=[Depends(HTTPBearer(scheme_name='JWT'))]
)



auth_repo = SQLAuthDataRepo()
user_repo = SQLUserRepo()


uc = UserUseCases(user_repo, auth_repo)


@users_routers.get(
        "/search", 
        summary = 'Найти пользователя по запросу',
        response_model = list[User]
        )
async def get_users_by_query(prompt: str, count: Optional[int] = 10, offset: Optional[int] = 0, auth: AuthJWT = Depends()):
    auth.jwt_required()
    users = await uc.search_user_by_prompt(prompt)
    return users



@users_routers.get(
        "/{user_id}", 
        summary = 'Получить профиль пользователя по его user_id',
        response_model = User
        )
async def get_user_by_id(user_id: UUID, auth: AuthJWT = Depends()):
    auth.jwt_required()
    user = await uc.get_user_by_id(user_id=user_id)
    return user





