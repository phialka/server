from fastapi import APIRouter

from controllers import files



files_router = APIRouter(
    prefix = "/file",
    tags = ["file"]
)


@files_router.get("/{file_hash}")
async def download_file(file_hash: str):
    return await files.get_file(file_hash)