from typing import Any, Dict

from use_cases.exceptions import IncorrectValueException

from fastapi import Request, status
from fastapi.responses import JSONResponse



def incorrect_value_exception_handler(request: Request, exc: IncorrectValueException):
    """
    Handler for error of JWT authorization
    """
    return JSONResponse(
        status_code = status.HTTP_409_CONFLICT,
        content = {"detail": exc.msg}
    )
