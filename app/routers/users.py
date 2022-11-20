from fastapi import APIRouter
import schemas
from typing import Union



users_router = APIRouter(
    prefix = "/users",
    tags = ["users"]
)


@users_router.get("/search")
async def search_users(string: str, offset: Union[int, None] = None, count: Union[int, None] = None):
    return {'status':'OK'}


@users_router.get("/getID")
async def get_userid(username: str):
    return {'status':'OK'}


@users_router.get("/{user_id}")
async def get_user(user_id: int):
    return {'user_id':user_id}