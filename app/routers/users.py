from fastapi import APIRouter,  Depends
from typing import Union, List

from auth import JWTAuth
from schemas import UserList, User
from controllers.users_logic import ServerUser, UList

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


@users_router.get("/user-lists", response_model=List[UserList.View])
async def get_userlists(authorize: JWTAuth = Depends()):
    authorize.jwt_required()
    return await ServerUser(authorize.get_jwt_subject()).get_userlists()


@users_router.get("/{user_id}")
async def get_user(user_id: int, authorize: JWTAuth = Depends()):
    authorize.jwt_required()
    observer = ServerUser(authorize.get_jwt_subject())
    pass


@users_router.post("/user-lists", response_model=UserList.View)
async def create_userlists(userlist: UserList.Create, authorize: JWTAuth = Depends()):
    authorize.jwt_required()
    ulist = await (await UList().create(authorize.get_jwt_subject(), userlist)).create_view()
    return ulist.view


@users_router.get("/user-lists/{list_id}/users", response_model=List[User.View])                         #
async def get_users_from_userlist(list_id: int, authorize: JWTAuth = Depends()):
    authorize.jwt_required()
    list = await UList(id=list_id).create_users_view()
    return list.users_view


@users_router.post("/user-lists/{list_id}/users")
async def addusers_into_userlist(list_id: int, user_id: int):
    return {'list_id':list_id, 'user_id':user_id}


@users_router.delete("/user-lists/{list_id}/users")
async def deleteusers_from_userlist(list_id: int, user_id: int):
    return {'list_id':list_id, 'user_id':user_id}
