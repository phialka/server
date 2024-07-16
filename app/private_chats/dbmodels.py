from uuid import UUID

import ormar

from database import database, metadata
from messages.dbmodels import Message
from users.dbmodels import User



class PrivateChat(ormar.Model):
    """
    Database model for private chat
    """
    ormar_config = ormar.OrmarConfig(
        metadata = metadata,
        database = database,
        tablename = "private_chats"
    )

    id: UUID = ormar.UUID(primary_key=True)



class PrivateChatMember(ormar.Model):
    """
    Database model for private chat member
    """
    ormar_config = ormar.OrmarConfig(
        metadata = metadata,
        database = database,
        tablename = "private_chat_members"
    )

    id: UUID = ormar.UUID(primary_key=True)
    private_chat: PrivateChat = ormar.ForeignKey(PrivateChat, ondelete=ormar.ReferentialAction.CASCADE)
    user: User = ormar.ForeignKey(User, ondelete=ormar.ReferentialAction.CASCADE)



class PrivateMessage(ormar.Model):
    """
    Database model for private chat message
    """
    ormar_config = ormar.OrmarConfig(
        metadata = metadata,
        database = database,
        tablename = "private_messages"
    )

    id: UUID = ormar.UUID(primary_key=True)
    private_chat: PrivateChat = ormar.ForeignKey(PrivateChat, ondelete=ormar.ReferentialAction.CASCADE)
    message: Message = ormar.ForeignKey(Message, ondelete=ormar.ReferentialAction.CASCADE)
    was_viewed: bool = ormar.Boolean(default=False)
    sequence: int = ormar.Integer()
