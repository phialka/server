from fastapi import APIRouter, UploadFile

from controllers.files_logic import Storage


files_router = APIRouter(
    prefix = "/file",
    tags = ["file"]
)


@files_router.get("/{file_hash}", include_in_schema=False)
async def download_file(file_hash: str):
    return await Storage.download_file(file_hash)


@files_router.post("/")
async def upload_to_server(file: UploadFile):
    saved = await Storage.save_to_server(file)
    return saved.id


@files_router.get("/")
async def get_link_byid(file_id: int):
    return await Storage.get_link(file_id)