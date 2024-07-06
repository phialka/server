from typing import Any, Dict

from use_cases.exceptions import AlreadyExistsException

from fastapi import Request, status
from fastapi.responses import JSONResponse



def already_exists_exception_handler(request: Request, exc: AlreadyExistsException):
    """
    Handler for error of JWT authorization
    """
    return JSONResponse(
        status_code = status.HTTP_409_CONFLICT,
        content = {"detail": exc.msg}
    )
