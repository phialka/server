from fastapi import HTTPException, status
from dbmodels import *
import schemas
from auth import JWTAuth



async def login_user(user: schemas.User.Login) -> dict:
    """
    Creates an access/refresh_token pair for the specified user. 
    The token contains the user ID.
    Returns a dictionary.
    """
    user_in_db = await User.objects.get_or_none(username=user.username)
    if not user_in_db:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="no such user was found")
    if user.userpass != user_in_db.userpass:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="incorrect password")
    
    authorize = JWTAuth()
    return {"access":authorize.create_access_token(user_in_db.id), "refresh":authorize.create_refresh_token(user_in_db.id)}
