from fastapi import HTTPException, status, UploadFile
from fastapi.responses import JSONResponse

from dbmodels import *
import schemas
from auth import JWTAuth
from controllers.files_logic import Storage


@database.transaction()
async def reg_profile(reg: schemas.UserRegistration) -> None:
    #if such user already exists
    if await User.objects.get_or_none(username=reg.username):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="such user already exist")

    user = await User.objects.create(username=reg.username, userpass=reg.userpass)
    userinfo = UserInfoField(name = reg.name, shortname = reg.shortname, description = reg.description, email = reg.email)
    await UserInfo.objects.create(user_id=user, info=userinfo.dict())
    return


async def set_profile_photo(user_id: int, photo: UploadFile):
    old_uinfo = await UserInfo.objects.get_or_none(user_id=user_id)
    if not old_uinfo:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="user not exists")
    info = old_uinfo.prepared_info
    new_photo = await Storage.save_to_server(photo)
    info.photo = new_photo.info
    await UserInfo.objects.filter(UserInfo.user_id.id == user_id).update(info=info.dict())
    return info.photo
    


async def get_profile(user_id):
    uinfo = await UserInfo.objects.get_or_none(user_id=user_id)
    return uinfo.prepared_info