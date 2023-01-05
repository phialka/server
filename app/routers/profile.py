from fastapi import APIRouter, UploadFile, Depends, Form
from schemas import User, Photo
from controllers.users_logic import UserController, ServerUser
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
    


@unauth_router.post("/", response_model=User.View, status_code=201)
async def register(reg: User.Registration):
    user = await ServerUser().create(reg)
    return await user.view
    

@profile_router.patch("/", response_model=User.View)
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


@profile_router.patch("/privacy-options", response_model=User.PrivacyOptions)
async def edit_privacy(options: User.EditSettings, authorize: JWTAuth = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    new_user = await ServerUser(user_id).edit_privacy_settings(options)
    return await new_user.privacy_options


@profile_router.put("/photo", response_model=Photo)
async def edit_profile_photo(photo: UploadFile, authorize: JWTAuth = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    return await ServerUser(user_id).set_photo(photo)


