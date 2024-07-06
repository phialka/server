from typing import Any, Dict

from use_cases.exceptions import AccessDeniedException

from fastapi import Request, status
from fastapi.responses import JSONResponse



def access_denied_exception_handler(request: Request, exc: AccessDeniedException):
    
    return JSONResponse(
        status_code = status.HTTP_403_FORBIDDEN,
        content = {"detail": exc.msg}
    )
