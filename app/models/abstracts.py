from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Optional, Union

from pydantic import BaseModel
from enum import Enum



class AbsUser(BaseModel):
    __metaclass__ = ABCMeta

    id: int
    name: str
    shortname: str
    description: Optional[str]
    photo_id: Optional[int]
    last_time: int
    created_at: int

    @abstractmethod
    async def get(cls, user_id: int) -> list["AbsUser"]:
        "Get User"

    @abstractmethod
    async def add(cls, name: str, shortname: str,  photo_id: Optional[int] = None, description: Optional[str] = None) -> int:
        "Add User"

    @abstractmethod
    async def update(
            cls, 
            id: int,
            name: Optional[str] = None, 
            shortname: Optional[str] = None,  
            photo_id: Optional[int] = None, 
            description: Optional[str] = None,
            last_time: Optional[int] = None
            ) -> int:
        "Update User"

    @abstractmethod
    async def delete(cls, user_id: int) -> int:
        "Delete User"



class AbsAuth(BaseModel):
    __metaclass__ = ABCMeta

    id: int
    user_id: int
    username: str
    userpass: str

    @abstractmethod
    async def get(cls, username: str) -> list["AbsAuth"]:
        "Get Auth"

    @abstractmethod
    async def add(
            cls, user_id: int, username: str, userpass: int) -> int:
        "Add Auth"

    @abstractmethod
    async def update(cls, auth_id: int, username: Optional[str] = None, userpass: Optional[str] = None) -> int:
        "Update Auth"

    @abstractmethod
    async def delete(cls, auth_id: Optional[int] = None, user_id: Optional[int] = None) -> int:
        "Delete Auth"



class AbsFile(BaseModel):
    __metaclass__ = ABCMeta

    class PhotoTI(BaseModel):
        width: int
        height: int

    class VideoTI(BaseModel):
        width: int
        height: int
        duration: int

    class AudioTI(BaseModel):
        duration: int
    

    id: int
    hash: str
    size: int
    type: str
    location: str
    title: str
    type_info: Union[PhotoTI, VideoTI, AudioTI, None]



class AbsConversation(BaseModel):
    __metaclass__ = ABCMeta

    id: int
    title: str
    icon_file_id: Optional[int]
    description: Optional[str]
    owner_id: int
    users_count: int
    created_at: int



class AbsConversationFile(BaseModel):
    __metaclass__ = ABCMeta

    id: int
    file_id: int
    conversation_id: int



class AbsConversationUser(BaseModel):
    __metaclass__ = ABCMeta

    id: int
    user_id: int
    conversation_id: int
    role_id: int



class AbsRole(BaseModel):
    __metaclass__ = ABCMeta

    class Permissions(Enum):
        TEXT_MESSAGES = 1
        VOICE_MESSAGES = 2

    id: int
    role_id: int
    title: str
    description: str
    permissions: set[Permissions]



class AbsDialog(BaseModel):
    __metaclass__ = ABCMeta

    id: int
    user_ids: set[int]



class AbsDialogFile(BaseModel):
    __metaclass__ = ABCMeta

    id: int
    file_id: int
    dialog_id: int



class AbsMessage(BaseModel):
    __metaclass__ = ABCMeta

    id: int
    type: str
    dialog_id: Optional[int]
    conversation_id: Optional[int]
    author_id: int
    content: Optional[str]
    attach_files: Optional[list[int]]
    forwarded_messages: Optional[list[int]]
    answer_to: Optional[int]
    created_at: int
    updated_at: int



class AbsBlackList(BaseModel):
    __metaclass__ = ABCMeta

    id: int
    owner_id: int
    user_ids: Optional[set[int]]



class AbsContacts(BaseModel):
    __metaclass__ = ABCMeta

    id: int
    owner_id: int
    user_ids: Optional[set[int]]



class AbsChatsList(BaseModel):
    __metaclass__ = ABCMeta

    id: int
    owner_id: int
    conversation_ids: Optional[set[int]]
    chat_ids: Optional[set[int]]