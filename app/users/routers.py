from uuid import UUID
from typing import Optional

from fastapi import APIRouter, UploadFile, Response, status, Depends, Request
from fastapi.security import HTTPBearer
from utils.fastapi_jwt_auth import auth_scheme, get_user_id

from users.schemas import User, UserUpdate, UserCreate
from users.use_caces import UserUseCases
from users.adapters import SQLUserRepo

from files.adapters import SQLFileRepo, SystemFileStorage

from auth.adapters import SQLAuthDataRepo

import config



register_routers = APIRouter(
    prefix = "/profile",
    tags = ["profile"]
)

users_routers = APIRouter(
    prefix = "/users",
    tags = ["users"],
    dependencies=[Depends(auth_scheme)]
)

profile_routers = APIRouter(
    prefix = "/profile",
    tags = ["profile"],
    dependencies=[Depends(auth_scheme)]
)



file_repo = SQLFileRepo()
file_storage = SystemFileStorage(config.FILE_STORAGE)
auth_repo = SQLAuthDataRepo()
user_repo = SQLUserRepo()

user_uc = UserUseCases(
    user_repo=user_repo,
    auth_repo=auth_repo,
    file_repo=file_repo,
    file_storage=file_storage
    )



@register_routers.post(
        "", 
        summary = 'Создать профиль'
        )
async def register(user: UserCreate):
    await user_uc.register_user(user.name, user.username, user.password, user.tag, user.description, user.birthdate)
    return



@profile_routers.delete(
        "", 
        summary = 'Удалить профиль'
        )
async def delete_profile(user_id: str = Depends(get_user_id)):
    await user_uc.delete_profile(user_id=user_id, requester_id=user_id)

    return



@profile_routers.get(
        "", 
        summary = 'Получить данные своего профиля',
        response_model = User
        )
async def get_profile(user_id: str = Depends(get_user_id)):
    return await user_uc.get_user_by_id(user_id)
    


@profile_routers.patch(
        "", 
        summary = 'Редактировать свой профиль'
        )
async def edit_profile(data: UserUpdate, user_id: str = Depends(get_user_id)):
    await user_uc.update_user_profile(
        user_id = user_id,
        requester_id = user_id,
        new_name = data.name,
        new_description = data.description,
        new_tag = data.tag,
        new_birthdate = data.birthdate
        )
    
    return



@profile_routers.put(
        "/photo", 
        summary = 'Установить фото профиля'
        )
async def set_profile_photo(photo: UploadFile, user_id: str = Depends(get_user_id)):
    
    await user_uc.set_profile_photo(photo=photo.file, user_id=user_id, requester_id=user_id)
    
    return



@profile_routers.delete(
        "/photo", 
        summary = 'Удалить фото профиля'
        )
async def delete_profile_photo(user_id: str = Depends(get_user_id)):
    await user_uc.delete_profile_photo(user_id=user_id, requester_id=user_id)

    return



@users_routers.get(
        "/search", 
        summary = 'Найти пользователя по запросу',
        response_model = list[User]
        )
async def get_users_by_query(prompt: str, count: Optional[int] = 10, offset: Optional[int] = 0, user_id: str = Depends(get_user_id)):
    users = await user_uc.search_user_by_prompt(prompt)
    return users



@users_routers.get(
        "/{user_id}", 
        summary = 'Получить профиль пользователя по его user_id',
        response_model = User
        )
async def get_user_by_id(user_id: UUID, requester_id: str = Depends(get_user_id)):
    user = await user_uc.get_user_by_id(user_id=user_id)
    return user
