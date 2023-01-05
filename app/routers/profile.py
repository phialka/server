from fastapi import APIRouter, UploadFile, Depends, Form
from schemas import User, UserList
from controllers.profile_logic import UserController, ServerUser
from controllers.files_logic import Storage
from auth import JWTAuth

profile_router = APIRouter(
    prefix = "/profile",
    tags = ["profile"],
    dependencies = [Depends(JWTAuth.auth_scheme)]
)

unauth_router = APIRouter(
    prefix = "/profile",
    tags = ["profile"]
)


@profile_router.get("/", response_model=User.View)
async def get_profile_info(authorize: JWTAuth = Depends()):
    authorize.jwt_required()
    return await ServerUser(authorize.get_jwt_subject()).view
    


@unauth_router.post("/", status_code=201)
async def register(reg: User.Registration):
    user = await ServerUser().create(reg)
    return await user.view
    

@profile_router.patch("/")
async def edit_profile_info(info: User.EditInfo, authorize: JWTAuth = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    new_user = await ServerUser(user_id).edit_info(info)
    return await new_user.view


@profile_router.put("/reset-password")
async def reset_password(reset: User.Reset, authorize: JWTAuth = Depends()):
    authorize.jwt_required()
    return {'status':'OK'}


@unauth_router.get("/check-username")
async def check_username(username: str):
    return await UserController.check_username_isfree(username)


@profile_router.get("/privacy-options", response_model=User.PrivacyOptions)
async def get_privacy(authorize: JWTAuth = Depends()):
    user_id = authorize.get_jwt_subject()
    return await ServerUser(user_id).privacy_options


@profile_router.patch("/privacy-options")
async def edit_privacy(options: User.EditSettings, authorize: JWTAuth = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    new_user = await ServerUser(user_id).edit_privacy_settings(options)
    return await new_user.privacy_options


@profile_router.put("/photo")
async def edit_profile_photo(photo: UploadFile, authorize: JWTAuth = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    return await ServerUser(user_id).set_photo(photo)


@profile_router.get("/user-lists")
async def get_userlists():
    return {'status':'OK'}


@profile_router.post("/user-lists")
async def create_userlists(userlist: UserList.Create):
    return {'status':'OK'}


@profile_router.get("/user-lists/{list_id}")
async def get_this_userlist(list_id: int):
    return {'list_id':list_id}


@profile_router.get("/user-lists/{list_id}/users")
async def getusers_from_userlist(list_id: int):
    return {'list_id':list_id}


@profile_router.post("/user-lists/{list_id}/users")
async def addusers_into_userlist(list_id: int, user_id: int):
    return {'list_id':list_id, 'user_id':user_id}


@profile_router.delete("/user-lists/{list_id}/users")
async def deleteusers_from_userlist(list_id: int, user_id: int):
    return {'list_id':list_id, 'user_id':user_id}


