from dotenv import dotenv_values

__values = dotenv_values(".env")
SERVER_NAME = __values["SERVER_NAME"]
DATABASE_URL = __values["DATABASE_URL"]
JWT_SECRET_KEY = __values["JWT_SECRET_KEY"]
FILE_STORAGE=__values["FILE_STORAGE"]
HOST=__values["HOST"]
PORT=int(__values["PORT"])