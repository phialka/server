from fastapi import APIRouter,  Depends
from typing import Union

from auth import JWTAuth
from schemas import UserList
from controllers.users_logic import ServerUser

users_router = APIRouter(
    prefix = "/users",
    tags = ["users"],
    dependencies = [Depends(JWTAuth.auth_scheme)]
)


@users_router.get("/search")
async def search_users(string: str, offset: Union[int, None] = None, count: Union[int, None] = None):
    return {'status':'OK'}


@users_router.get("/get-id")
async def get_userid(username: str, authorize: JWTAuth = Depends()):
    authorize.jwt_required()
    pass


@users_router.get("/{user_id}")
async def get_user(user_id: int):
    return {'user_id':user_id}


@users_router.get("/user-lists")
async def get_userlists():
    return {'status':'OK'}


@users_router.post("/user-lists")
async def create_userlists(userlist: UserList.Create):
    return {'status':'OK'}


@users_router.get("/user-lists/{list_id}")
async def get_this_userlist(list_id: int):
    return {'list_id':list_id}


@users_router.get("/user-lists/{list_id}/users")
async def getusers_from_userlist(list_id: int):
    return {'list_id':list_id}


@users_router.post("/user-lists/{list_id}/users")
async def addusers_into_userlist(list_id: int, user_id: int):
    return {'list_id':list_id, 'user_id':user_id}


@users_router.delete("/user-lists/{list_id}/users")
async def deleteusers_from_userlist(list_id: int, user_id: int):
    return {'list_id':list_id, 'user_id':user_id}
