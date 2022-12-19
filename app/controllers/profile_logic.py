from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from dbmodels import *
import schemas
from auth import JWTAuth


@database.transaction()
async def reg_profile(reg: schemas.UserRegistration) -> JSONResponse:
    #if such user already exists
    if await User.objects.get_or_none(username=reg.username):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="such user already exist")

    user = await User.objects.create(username=reg.username, userpass=reg.userpass)
    userinfo = {"name": reg.name, "shortname": reg.shortname, "description": reg.description, "email": reg.email}
    await UserInfo.objects.create(user_id=user, info=userinfo)
    return JSONResponse(status_code=status.HTTP_201_CREATED)


async def login_user(user: schemas.UserLogin) -> dict:
    user_in_db = await User.objects.get_or_none(username=user.username)
    if not user_in_db:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="no such user was found")
    if user.userpass != user_in_db.userpass:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="incorrect password")
    
    auth = JWTAuth()
    return {"access":auth.create_access_token(user_in_db.id), "refresh":auth.create_refresh_token(user_in_db.id)}


async def get_info():
    info = await UserInfo.objects.get(user_id=1)
    return info.info