from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from utils.openapi_documentation import CustomServerAPI
from database.tables import connect_database, disconnect_database
from rest_api import profile_routers, auth_routers, register_routers, files_router, users_routers, server_routers, channel_routers, private_chat_routers, message_routers

from rest_api.exception_handlers import *
import config



@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_database()

    yield

    await disconnect_database()



app = FastAPI(lifespan=lifespan)
app.openapi = CustomServerAPI(app).get_openapi()



app.include_router(auth_routers)
app.include_router(register_routers)
app.include_router(profile_routers)
app.include_router(users_routers)
app.include_router(server_routers)
app.include_router(channel_routers)
app.include_router(private_chat_routers)
app.include_router(message_routers)
app.include_router(files_router)



app.add_exception_handler(AuthError, auth_error_exception_handler)
app.add_exception_handler(NotAuth, not_auth_exception_handler)
app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.add_exception_handler(AccessDeniedException, access_denied_exception_handler)
app.add_exception_handler(IncorrectValueException, incorrect_value_exception_handler)



@app.get("/domain", tags=["domain"])
async def mainpage():
    return {"name": config.SERVER_NAME, "status": "working"}



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host=config.HOST, port=config.PORT)
