from fastapi import APIRouter, UploadFile, Depends, Form
import schemas
from controllers import profile_logic
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


@profile_router.get("/")
async def get_profile_info(authorize: JWTAuth = Depends()):
    authorize.jwt_required()
    return await profile_logic.get_profile(authorize.get_jwt_subject())


@unauth_router.post("/", status_code=201)
async def register(user: schemas.UserRegistration):
    return await profile_logic.reg_profile(user)
    

@profile_router.patch("/")
async def edit_profile_info(info: schemas.UserRegistration):
    return {'status':'OK'}


@profile_router.put("/reset-password")
async def reset_password(reset: schemas.UserReset, authorize: JWTAuth = Depends()):
    authorize.jwt_required()
    return {'status':'OK'}


@profile_router.get("/check-username")
async def check_username():
    return {'status':'OK'}


@profile_router.get("/privacy-options")
async def get_privacy():
    return {'status':'OK'}


@profile_router.patch("/privacy-options")
async def edit_privacy(options: schemas.PrivacyOptions):
    return {'status':'OK'}


@profile_router.put("/photo")
async def edit_profile_photo(photo: UploadFile, authorize: JWTAuth = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    return await profile_logic.set_profile_photo(user_id, photo)


@profile_router.get("/user-lists")
async def get_userlists():
    return {'status':'OK'}


@profile_router.post("/user-lists")
async def create_userlists(userlist: schemas.NewUserlist):
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


