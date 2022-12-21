from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from dbmodels import *
import schemas
from auth import JWTAuth


@database.transaction()
async def reg_profile(reg: schemas.UserRegistration) -> None:
    #if such user already exists
    if await User.objects.get_or_none(username=reg.username):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="such user already exist")

    user = await User.objects.create(username=reg.username, userpass=reg.userpass)
    userinfo = {"name": reg.name, "shortname": reg.shortname, "description": reg.description, "email": reg.email}
    await UserInfo.objects.create(user_id=user, info=userinfo)
    return


async def get_profile(user_id):
    info = await UserInfo.objects.get(user_id=user_id)
    return {
        "id": user_id,
        "name": info.info["name"],
        "shortname": info.info["shortname"],
        "descriptiion": info.info["description"],
    }