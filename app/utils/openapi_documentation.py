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
                version="alpha",
                description="Phialka server",
                routes=self.app.routes,
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
            router_authorize = [route for route in self.app.routes[4:] if route.operation_id == "authorize"]

            for route in router_authorize:
                method = list(route.methods)[0].lower()
                try:
                    # If the router has another parameter
                    openapi_schema["paths"][route.path][method]['parameters'].append(headers)
                except Exception:
                    # If the router doesn't have a parameter
                    openapi_schema["paths"][route.path][method].update({"parameters":[headers]})

            self.app.openapi_schema = openapi_schema
            return self.app.openapi_schema
        return custom_openapi