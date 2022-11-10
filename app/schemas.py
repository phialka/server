from typing import Union
from pydantic import BaseModel



class RegistrationInfo(BaseModel):
    nickname: str
    name: str
    description: Union[str, None] = None
    email: Union[str, None] = None
    username: str
    userpass: str


class PrivacyOptions(BaseModel):
    can_found: int
    last_visit: int
    audio_call: int
    video_call: int
    forwarding: int


class UserlistIn(BaseModel):
    title: str
    ban: bool
    ignore: bool
    user_ids: Union[None, list[int]]