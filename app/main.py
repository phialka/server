from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from auth.routers import auth_routers
from users.routers import users_routers, profile_routers, register_routers
from private_chats.routers import private_chat_routers
from servers.routers import server_routers
from channels.routers import channel_routers
from messages.routers import message_routers
from messages.websockets import message_ws_router
from files.routers import files_router

from utils.openapi_documentation import CustomServerAPI
from utils.fastapi_exceptions_handler import set_exception_handlers
from utils.file_storage import Storage
from database import connect_database, disconnect_database

from exceptions import *

import config



@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_database()
    await Storage.create_storage(config.FILE_STORAGE)

    yield

    await disconnect_database()



app = FastAPI(lifespan=lifespan)
app.openapi = CustomServerAPI(app).get_openapi()



app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



app.include_router(auth_routers)
app.include_router(register_routers)
app.include_router(profile_routers)
app.include_router(users_routers)
app.include_router(private_chat_routers)
app.include_router(server_routers)
app.include_router(channel_routers)
app.include_router(message_routers)
app.include_router(message_ws_router)
app.include_router(files_router)



set_exception_handlers(app=app)



@app.get("/domain", tags=["domain"])
async def mainpage():
    return {"name": config.SERVER_NAME, "status": "working"}



if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        reload=True, 
        host=config.HOST, 
        port=config.PORT
        )
