from pydantic import BaseModel
from uuid import UUID

from users.schemas import User
from messages.schemas import Message



class PrivateChat(BaseModel):
    '''
    Dataclass with private chat data

    *there can be only two members
    '''
    chat_id: UUID
    members: list[User]



class PrivateMessage(BaseModel):
    '''
    Dataclass with channel message data

    *sequence is a serial number of the message in the private chat
    '''
    message: Message
    chat_id: UUID
    sequence: int
