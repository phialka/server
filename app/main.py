import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from routers import profile, users, channels, chats, files
from dbmodels import database, tables_init
import config
from auth import JWTAuth
from openapi_documentation import CustomServerAPI

import controllers

app = FastAPI()
app.openapi = CustomServerAPI(app).get_openapi()
app.state.database = database


app.include_router(profile.profile_router)
app.include_router(users.users_router)
app.include_router(channels.channels_router)
app.include_router(chats.chats_router)
app.include_router(files.files_router)


@app.on_event("startup")
async def start():
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()
    tables_init()
    #controllers.files.create_storage()


@app.on_event("shutdown")
async def stop():
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


@app.get("/")
async def mainpage():
    return {"name": "Phialka_API", "version": 1.0, "status": "working"}



# exception handler for jwtauth
@app.exception_handler(JWTAuth.auth_exeption)
def authjwt_exception_handler(request: Request, exc: JWTAuth.auth_exeption):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host=config.HOST, port=config.PORT)

