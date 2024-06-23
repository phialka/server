import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from utils.openapi_documentation import CustomServerAPI
from database.tables import connect_database, disconnect_database
from rest_api import files_router
import config



app = FastAPI()
app.openapi = CustomServerAPI(app).get_openapi()



app.include_router(files_router)



@app.on_event("startup")
async def start():
    await connect_database()



@app.on_event("shutdown")
async def stop():
    await disconnect_database()



@app.get("/domain", tags=["domain"])
async def mainpage():
    return {"name": config.SERVER_NAME, "status": "working"}



# # exception handler for jwtauth
# @app.exception_handler(JWTAuth.auth_exeption)
# def authjwt_exception_handler(request: Request, exc: JWTAuth.auth_exeption):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"detail": exc.message}
#     )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host=config.HOST, port=config.PORT)

