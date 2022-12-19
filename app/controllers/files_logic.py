import hashlib
import time
import os
import itertools

from starlette.responses import Response
from fastapi import UploadFile

from dbmodels import *
import config



#creates a directory for storing files on the server
def create_storage() -> None:
    def create(path, echo):
        if not os.path.isdir(path):
            os.mkdir(path)
        if echo:
            return path
    create(config.FILE_STORAGE, False)
    duos = [d[0]+d[1] for d in itertools.product('0123456789abcdef', repeat=2)]
    first_level = [create(f"{config.FILE_STORAGE}\{sub}", True) for sub in duos]
    second_level = [[create(f"{path}\{sub}", False) for sub in duos] for path in first_level]


#calculates the hash sum of the file to verify uniqueness
async def calculate_hash(file) -> str:
    hash = hashlib.md5()
    hash.update(file.read())
    return hash.hexdigest()


#saves the uploaded file to the storage, registers it in the database
#returns file id
async def save_to_server(file: UploadFile) -> File:
    md5hash = await calculate_hash(file.file)

    file_already_saved = await File.objects.get_or_none(hash=md5hash)
    if file_already_saved:
        return file_already_saved

    path = f'{config.FILE_STORAGE}\{md5hash[0:2]}\{md5hash[2:4]}'

    with open(f"{path}\{md5hash}", "wb") as new_file:
        file.file.seek(0,0)
        new_file.write(file.file.read())

    info = { 
        "type": file.content_type,
        "title": file.filename,
        "size": os.path.getsize(f"{path}\{md5hash}"),
        "upload_at": time.time(),
        "url": f"http://{config.HOST}:{config.PORT}/file/{md5hash}"
    }
    return await File.objects.create(hash=md5hash, info=info, path=path)


#returns the Response object with the uploaded file
async def get_file(file_hash) -> Response:
    file = await File.objects.get_or_none(hash=file_hash)
    with open(f"{file.path}\{file.hash}", "rb") as data:
        return Response(content=data.read(), media_type=file.info["type"], status_code=200)





