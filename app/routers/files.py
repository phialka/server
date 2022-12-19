from fastapi import APIRouter

from controllers import files_logic



files_router = APIRouter(
    prefix = "/file",
    tags = ["file"]
)


@files_router.get("/{file_hash}")
async def download_file(file_hash: str):
    return await files_logic.get_file(file_hash)