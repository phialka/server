import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from routers import channels, authentification
import config
from auth import JWTAuth
from openapi_documentation import CustomServerAPI

#from controllers.files_logic import Storage
#from controllers.chats_logic import PermissionController

app = FastAPI()
app.openapi = CustomServerAPI(app).get_openapi()



app.include_router(authentification.auth_router)
#app.include_router(profile.profile_router)
#app.include_router(profile.unauth_router)
#app.include_router(users.users_router)
app.include_router(channels.channels_router)
#app.include_router(chats.chats_router)
#app.include_router(files.files_router)


@app.on_event("startup")
async def start():
    pass
    #Storage.create_storage()
    #await PermissionController.init_standard()
    #await PermissionController.load_role_ids()


@app.on_event("shutdown")
async def stop():
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


@app.get("/", tags=["server"])
async def mainpage():
    return {"name": config.SERVER_NAME, "status": "working"}



# exception handler for jwtauth
@app.exception_handler(JWTAuth.auth_exeption)
def authjwt_exception_handler(request: Request, exc: JWTAuth.auth_exeption):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host=config.HOST, port=config.PORT)

