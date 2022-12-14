import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from routers import profile, users, channels, chats
from dbmodels import database
import config
from auth import JWTAuth

app = FastAPI()
app.state.database = database


app.include_router(profile.profile_router)
app.include_router(users.users_router)
app.include_router(channels.channels_router)
app.include_router(chats.chats_router)


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



# exception handler for jwtauth
@app.exception_handler(JWTAuth.auth_exeption)
def authjwt_exception_handler(request: Request, exc: JWTAuth.auth_exeption):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=config.SERVER_NAME,
        version="alpha",
        description="Phialka server",
        routes=app.routes,
    )

    # Custom documentation fastapi-jwt-auth
    headers = {
        "name": "Authorization",
        "in": "header",
        "required": True,
        "schema": {
            "title": "Authorization",
            "type": "string"
        },
    }

    # Get routes from index 4 because before that fastapi define router for /openapi.json, /redoc, /docs, etc
    # Get all router where operation_id is authorize
    router_authorize = [route for route in app.routes[4:] if route.operation_id == "authorize"]

    for route in router_authorize:
        method = list(route.methods)[0].lower()
        try:
            # If the router has another parameter
            openapi_schema["paths"][route.path][method]['parameters'].append(headers)
        except Exception:
            # If the router doesn't have a parameter
            openapi_schema["paths"][route.path][method].update({"parameters":[headers]})

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

