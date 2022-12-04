from fastapi import APIRouter
import schemas


channels_router = APIRouter(
    prefix = "/channels",
    tags = ["channels"]
)


@channels_router.get("/")
async def get_list(count: int, offset:int):
    return {'status':'OK'}


@channels_router.post("/")
async def create_channel(title: str, description: str, photo: UploadFile):
    return {'status':'OK'}


@channels_router.get("/{channel_id}")
async def get_info_channel(channel_id: int):
    return {'channel_id':'channel_id'}


@channels_router.patch("/{channel_id}")
async def edit_info_channel(channel_id: int, title: str, description: str, photo: UploadFile):
    return {'channel_id':'channel_id'}


@channels_router.delete("/{channel_id}")
async def delete_channel(channel_id: int):
    return {'channel_id':'channel_id'}


@channels_router.patch("/{channel_id}/join")
async def join_channel(channel_id: int):
    return {'channel_id':'channel_id'}


@channels_router.patch("/{channel_id}/leave")
async def leave_channel(channel_id: int):
    return {'channel_id':'channel_id'}


@channels_router.get("/{channel_id}/posts")
async def get_posts(channel_id: int, post_id: int, newer_than: str, count: int):
    return {'channel_id':'channel_id'}


@channels_router.post("/{channel_id}/posts")
async def create_posts(channel_id: int, info: schemas.PostContent):
    return {'channel_id':'channel_id'}


@channels_router.delete("/{channel_id}/posts")
async def delete_posts(channel_id: int, post_ids: int, user_id: int):
    return {'channel_id':'channel_id'}


@channels_router.patch("/{channel_id}/posts/{post_id}")
async def edit_posts(channel_id: int, post_id: int, info: schemas.PostContent):
    return {'post_id':'post_id'}


@channels_router.get("/{channel_id}/members")
async def get_members(channel_id: int, count: int, offset: int):
    return {'channel_id':'channel_id'}


@channels_router.patch("/{channel_id}/members")
async def invite_users(channel_id: int, user_ids: int):
    return {'channel_id':'channel_id'}


@channels_router.get("/{channel_id}/my_role")
async def get_role(channel_id: int):
    return {'channel_id':'channel_id'}


@channels_router.get("/{channel_id}/roles")
async def get_list_roles(channel_id: int):
    return {'channel_id':'channel_id'}


@channels_router.post("/{channel_id}/roles")
async def create_roles(channel_id: int, info: schemas.ChannelRole):
    return {'channel_id':'channel_id'}


@channels_router.patch("/{channel_id}/roles")
async def change_roles(channel_id: int, user_id: int, role_id: int):
    return {'channel_id':'channel_id'}
