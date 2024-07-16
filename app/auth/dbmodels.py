from uuid import UUID

import ormar

from database import database, metadata
from users.dbmodels import User



class AuthData(ormar.Model):
    """
    Database model for user auth data
    """
    ormar_config = ormar.OrmarConfig(
        metadata = metadata,
        database = database,
        tablename = "auth_data"
    )

    user_id: User = ormar.ForeignKey(User, ondelete=ormar.ReferentialAction.CASCADE)
    login: UUID = ormar.String(max_length=200, primary_key=True)
    pass_hash: str = ormar.String(max_length=200)
