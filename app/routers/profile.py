from fastapi import APIRouter, UploadFile, Depends
import schemas
from controllers import profile_funcs
from auth import JWTAuth

profile_router = APIRouter(
    prefix = "/profile",
    tags = ["profile"]
)


@profile_router.get("/")
async def get_profile_info():
    info = await profile_funcs.get_info()
    return info


@profile_router.post("/")
async def register(info: schemas.RegistrationInfo):
    await profile_funcs.reg_profile(info)
    return {'status':'OK'}


@profile_router.patch("/")
async def edit_profile_info(info: schemas.RegistrationInfo):
    return {'status':'OK'}


@profile_router.post("/login")
async def login(info: schemas.UserLogin, Authorize: JWTAuth = Depends()):
    return {'status':'OK'}


@profile_router.post("/refresh-login")
async def refresh_login(Authorize: JWTAuth = Depends()):
    Authorize.jwt_refresh_token_required()
    return {'status':'OK'}


@profile_router.get("/checkUsername")
async def check_username():
    return {'status':'OK'}


@profile_router.get("/privacy_options")
async def get_privacy():
    return {'status':'OK'}


@profile_router.patch("/privacy_options")
async def edit_privacy(options: schemas.PrivacyOptions):
    return {'status':'OK'}


@profile_router.put("/photo")
async def edit_profile_photo(photo: UploadFile):
    return {'name':photo.filename, 'type':photo.content_type}


@profile_router.get("/user_lists")
async def get_userlists():
    return {'status':'OK'}


@profile_router.post("/user_lists")
async def create_userlists(userlist: schemas.NewUserlist):
    return {'status':'OK'}


@profile_router.get("/user_lists/{list_id}")
async def get_this_userlist(list_id: int):
    return {'list_id':list_id}


@profile_router.get("/user_lists/{list_id}/users")
async def getusers_from_userlist(list_id: int):
    return {'list_id':list_id}


@profile_router.post("/user_lists/{list_id}/users")
async def addusers_into_userlist(list_id: int, user_id: int):
    return {'list_id':list_id, 'user_id':user_id}


@profile_router.delete("/user_lists/{list_id}/users")
async def deleteusers_from_userlist(list_id: int, user_id: int):
    return {'list_id':list_id, 'user_id':user_id}


