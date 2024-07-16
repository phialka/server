from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from exceptions import AccessDeniedException, AlreadyExistsException, AuthError, NotAuth, IncorrectValueException, NotFoundException



def set_exception_handlers(app: FastAPI):

    @app.exception_handler(AccessDeniedException)
    async def access_denied_exception_handler(request: Request, exc: AccessDeniedException):
        
        return JSONResponse(
            status_code = status.HTTP_403_FORBIDDEN,
            content = {"detail": exc.msg}
        )


    @app.exception_handler(AlreadyExistsException)
    async def already_exists_exception_handler(request: Request, exc: AlreadyExistsException):
        """
        Handler for error of JWT authorization
        """
        return JSONResponse(
            status_code = status.HTTP_409_CONFLICT,
            content = {"detail": exc.msg}
        )

    @app.exception_handler(AuthError)
    async def auth_error_exception_handler(request: Request, exc: AuthError):
        """
        Handler for error of JWT authorization
        """
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": exc.msg}
        )


    @app.exception_handler(NotAuth)
    async def not_auth_exception_handler(request: Request, exc: NotAuth):
        """
        Handler for error of JWT authorization
        """
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": exc.msg}
        )


    @app.exception_handler(IncorrectValueException)
    async def incorrect_value_exception_handler(request: Request, exc: IncorrectValueException):
        """
        Handler for error of JWT authorization
        """
        return JSONResponse(
            status_code = status.HTTP_409_CONFLICT,
            content = {"detail": exc.msg}
        )

    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(request: Request, exc: NotFoundException):
        """
        Handler for error of JWT authorization
        """
        return JSONResponse(
            status_code = status.HTTP_404_NOT_FOUND,
            content = {"detail": exc.msg}
        )
