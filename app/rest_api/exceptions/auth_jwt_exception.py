from fastapi import Request
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse



def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    """
    Handler for error of JWT authorization
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )