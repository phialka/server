from fastapi import APIRouter, Depends, Header
from fastapi.security import HTTPBearer
import schemas
from controllers import auth_logic
from auth import JWTAuth



auth_router = APIRouter(
    prefix = "/auth",
    tags = ["authentification"]
)


@auth_router.post("/login")
async def login(login: schemas.UserLogin):
    return await auth_logic.login_user(login)


@auth_router.post("/refresh-login")
async def refresh_login(refresh: str = Depends(HTTPBearer(scheme_name="JWT refresh token")), authorize: JWTAuth = Depends()):
    authorize.jwt_refresh_token_required()
    user_id = authorize.get_jwt_subject()
    return {"access": authorize.create_access_token(user_id)}