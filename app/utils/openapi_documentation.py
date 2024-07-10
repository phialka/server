from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI

import config

class CustomServerAPI():
    def __init__(self, app: FastAPI):
        self.app = app

    def get_openapi(self):
        def custom_openapi():
            if self.app.openapi_schema:
                return self.app.openapi_schema

            openapi_schema = get_openapi(
                title=config.SERVER_NAME,
                version="MVP v1.0",
                description="Phialka server REST API",
                routes=self.app.routes,
            )

            self.app.openapi_schema = openapi_schema
            return self.app.openapi_schema
        return custom_openapi