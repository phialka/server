from dbmodels import *
import schemas



@database.transaction()
async def reg_profile(reg_info: schemas.RegistrationInfo):
    user = await User.objects.create(username=reg_info.username, userpass=reg_info.userpass)
    userinfo = {"nickname": reg_info.nickname, "name": reg_info.name, "description": reg_info.description, "email": reg_info.email}
    await UserInfo.objects.create(user_id=user, info=userinfo)

async def get_info():
    info = await UserInfo.objects.get(user_id=1)
    return info.info