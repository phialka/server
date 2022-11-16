import uvicorn
from fastapi import FastAPI
from routers import profile, users, channels
from dbmodels import database

app = FastAPI(title='Phialka')
app.state.database = database


app.include_router(profile.profile_router)
app.include_router(users.users_router)
app.include_router(channels.channels_router)


@app.on_event("startup")
async def start():
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def stop():
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


@app.get("/")
async def mainpage():
    return {"name": "Phialka_API", "version": 1.0, "status": "working"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

