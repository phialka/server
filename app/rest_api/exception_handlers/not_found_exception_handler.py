from typing import Any, Dict

from use_cases.exceptions import NotFoundException

from fastapi import Request, status
from fastapi.responses import JSONResponse



def not_found_exception_handler(request: Request, exc: NotFoundException):
    """
    Handler for error of JWT authorization
    """
    return JSONResponse(
        status_code = status.HTTP_404_NOT_FOUND,
        content = {"detail": exc.msg}
    )
