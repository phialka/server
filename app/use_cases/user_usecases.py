from typing import BinaryIO
from uuid import UUID, uuid4
from hashlib import md5
from datetime import datetime
from typing import Optional

from entities import User, UserFilter, AuthData
from .abstracts import UserRepo, AuthDataRepo
from .exceptions import UserNotFoundError, ForbiddenError



class UserUseCases():
    def __init__(self, user_repo: UserRepo, auth_repo: AuthDataRepo) -> None:
        self.__user_repo: UserRepo = user_repo
        self.__auth_repo: AuthDataRepo = auth_repo



    async def get_user_by_id(self, user_id: UUID):
        users = await self.__user_repo.get(UserFilter(user_id=user_id))
        if len(users) == 0:
            raise UserNotFoundError
        else:
            return users[0]


