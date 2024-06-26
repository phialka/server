from uuid import UUID

from fastapi import APIRouter, UploadFile, Response, status, Depends, Request
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT

from entities import User, File
from use_cases.profile_usecases import ProfileUseCases
from use_cases.files_usecases import FileUseCases
from use_cases.user_usecases import UserUseCases
from adapters.file_repo import SQLFileRepo
from adapters.file_storage import SystemFileStorage
from adapters.auth_data_repo import SQLAuthDataRepo
from adapters.user_repo import SQLUserRepo
from .schemas.profile import UserCreate, UserUpdate

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

file_repo = SQLFileRepo()
file_storage = SystemFileStorage(config.FILE_STORAGE)
auth_repo = SQLAuthDataRepo()
user_repo = SQLUserRepo()

file_uc = FileUseCases(file_repo, file_storage)
user_uc = UserUseCases(user_repo, auth_repo)
uc = ProfileUseCases(user_repo, auth_repo, file_uc)



@register_routers.post(
        "", 
        summary = 'Создать профиль',
        response_model = User
        )
async def register(user: UserCreate):
    user = await uc.register(user.name, user.login, user.password, user.tag, user.description, user.birthdate)
    return user



@profile_routers.delete(
        "", 
        summary = 'Удалить профиль'
        )
async def delete_profile(auth: AuthJWT = Depends()):
    auth.jwt_required()
    user_id = auth.get_jwt_subject()

    await uc.delete_profile(user_id=user_id, requester_id=user_id)

    return



@profile_routers.get(
        "", 
        summary = 'Получить данные своего профиля',
        response_model = User
        )
async def get_profile(auth: AuthJWT = Depends()):
    auth.jwt_required()
    user_id = auth.get_jwt_subject()
    return await user_uc.get_user_by_id(user_id)
    


@profile_routers.patch(
        "", 
        summary = 'Редактировать свой профиль',
        response_model = User
        )
async def edit_profile(data: UserUpdate, auth: AuthJWT = Depends()):
    auth.jwt_required()
    user_id = auth.get_jwt_subject()
    user = await uc.update_profile(
        user_id = user_id,
        requester_id = user_id,
        new_name = data.name,
        new_description = data.description,
        new_tag = data.tag,
        new_birthdate = data.birthdate
        )
    
    return user



@profile_routers.put(
        "/photo", 
        summary = 'Установить фото профиля',
        response_model = File
        )
async def set_profile_photo(photo: UploadFile, auth: AuthJWT = Depends()):
    auth.jwt_required()
    user_id = auth.get_jwt_subject()
    
    profile_photo = await uc.set_profile_photo(photo=photo.file, user_id=user_id, requester_id=user_id)
    
    return profile_photo



@profile_routers.delete(
        "/photo", 
        summary = 'Удалить фото профиля'
        )
async def delete_profile_photo(auth: AuthJWT = Depends()):
    auth.jwt_required()
    user_id = auth.get_jwt_subject()

    await uc.delete_profile_photo(user_id=user_id, requester_id=user_id)

    return