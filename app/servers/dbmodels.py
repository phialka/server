from typing import Optional
from uuid import UUID
from datetime import datetime

import ormar

from database import database, metadata
from users.dbmodels import User
from files.dbmodels import File



class Server(ormar.Model):
    """
    Database model for sever
    """
    ormar_config = ormar.OrmarConfig(
        metadata = metadata,
        database = database,
        tablename = "servers"
    )

    id: UUID = ormar.UUID(primary_key=True)
    owner: User = ormar.ForeignKey(User, ondelete=ormar.ReferentialAction.CASCADE)
    title: str = ormar.String(max_length=40)
    description: Optional[str] = ormar.String(max_length=100, nullable=True)
    created_at: Optional[datetime] = ormar.DateTime()
    logo: File = ormar.ForeignKey(File, nullable=True, ondelete=ormar.ReferentialAction.SET_NULL)



class ServerMember(ormar.Model):
    """
    Database model for server member
    """
    ormar_config = ormar.OrmarConfig(
        metadata = metadata,
        database = database,
        tablename = "server_members"
    )

    id: UUID = ormar.UUID(primary_key=True)
    server: Server = ormar.ForeignKey(Server, ondelete=ormar.ReferentialAction.CASCADE)
    user: User = ormar.ForeignKey(User, ondelete=ormar.ReferentialAction.CASCADE)
