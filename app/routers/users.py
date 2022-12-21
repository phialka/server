from fastapi import APIRouter,  Depends
from typing import Union

from auth import JWTAuth
import schemas

users_router = APIRouter(
    prefix = "/users",
    tags = ["users"],
    dependencies = [Depends(JWTAuth.auth_scheme)]
)


@users_router.get("/search")
async def search_users(string: str, offset: Union[int, None] = None, count: Union[int, None] = None):
    return {'status':'OK'}


@users_router.get("/get-id")
async def get_userid(username: str):
    return {'status':'OK'}


@users_router.get("/{user_id}")
async def get_user(user_id: int):
    return {'user_id':user_id}