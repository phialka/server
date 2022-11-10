from fastapi import APIRouter
import schemas



users_router = APIRouter(
    prefix = "/users",
    tags = ["users"]
)


@users_router.get("/search")
async def search_users():
    return {'status':'OK'}


@users_router.get("/getID")
async def get_userid():
    return {'status':'OK'}


@users_router.get("/{user_id}")
async def get_user(user_id: int):
    return {'user_id':user_id}