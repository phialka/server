import os
from dotenv import dotenv_values
import json

if os.path.exists('.env'):
    __values = dotenv_values(".env")
else:
    __values = os.environ


SERVER_NAME = __values["SERVER_NAME"]
DATABASE_URL = __values["DATABASE_URL"]
JSON_DB_PATH = __values["JSON_DB_PATH"]
JWT_SECRET_KEY = __values["JWT_SECRET_KEY"]
FILE_STORAGE=__values["FILE_STORAGE"]
HOST=__values["HOST"]
PORT=int(__values["PORT"])
USER_TAG_PREFIX=__values["USER_TAG_PREFIX"]
JWT_ACCESS_TTL=int(__values["JWT_ACCESS_TTL"])
JWT_REFRESH_TTL=int(__values["JWT_REFRESH_TTL"])
ALLOW_ORIGINS=json.loads(__values["ALLOW_ORIGINS"])
