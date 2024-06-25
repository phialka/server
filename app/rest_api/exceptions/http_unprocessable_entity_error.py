from typing import Any, Dict
from fastapi import Request
from fastapi.responses import JSONResponse



class HTTPUnprocessableEntity(Exception):
    def __init__(self, message: str|None = None) -> None:
        self.status_code = 422
        self.message = message



def http_unprocessable_entity_exception_handler(request: Request, exc: HTTPUnprocessableEntity):
    """
    Handler for error of JWT authorization
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )
