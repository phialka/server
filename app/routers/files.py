from fastapi import APIRouter

from controllers.files_logic import Storage


files_router = APIRouter(
    prefix = "/file",
    tags = ["file"]
)


@files_router.get("/{file_hash}", include_in_schema=False)
async def download_file(file_hash: str):
    return await Storage.download_file(file_hash)