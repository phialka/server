from typing import BinaryIO
from uuid import UUID, uuid4
from hashlib import md5
from datetime import datetime
from typing import Optional

from entities import User, AuthData
from .datamodels.filters import UserFilter
from .abstracts import UserRepo, AuthDataRepo
from .exceptions import UserNotFoundError, ForbiddenError

import config



class UserUseCases():
    def __init__(self, user_repo: UserRepo, auth_repo: AuthDataRepo) -> None:
        self.__user_repo: UserRepo = user_repo
        self.__auth_repo: AuthDataRepo = auth_repo



    async def get_user_by_id(self, user_id: UUID) -> User:
        users = await self.__user_repo.get(UserFilter(user_id=user_id))
        if len(users) == 0:
            raise UserNotFoundError
        else:
            return users[0]
        

    async def search_user_by_prompt(self, prompt: str) -> list[User]:
        if prompt.startswith(config.USER_TAG_PREFIX):
            filter = UserFilter(tag_search_prompt=prompt.removeprefix(config.USER_TAG_PREFIX))
        else:
            filter = UserFilter(name_search_prompt=prompt)

        return await self.__user_repo.get(filter=filter)
        


