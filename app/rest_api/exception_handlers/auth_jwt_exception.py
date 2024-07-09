from fastapi import Request, status
from fastapi.responses import JSONResponse

from use_cases.exceptions import AuthError, NotAuth




def auth_error_exception_handler(request: Request, exc: AuthError):
    """
    Handler for error of JWT authorization
    """
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": exc.msg}
    )



def not_auth_exception_handler(request: Request, exc: NotAuth):
    """
    Handler for error of JWT authorization
    """
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.msg}
    )