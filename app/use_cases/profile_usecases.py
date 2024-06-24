from typing import BinaryIO
from uuid import UUID, uuid4
from hashlib import md5
from datetime import datetime
from mimetypes import guess_type

from entities import User, UserFilter, AuthData
from .abstracts import UserRepo, AuthDataRepo



class ProfileUseCases():
    def __init__(self, user_repo: UserRepo, auth_repo: AuthDataRepo) -> None:
        self.__user_repo: UserRepo = user_repo
        self.__auth_repo: AuthDataRepo = auth_repo

    
    def __hash(self, string: str):
        return md5(string.encode()).hexdigest()


    async def register(self, name: str, login: str, password: str) -> User:
        user_id = uuid4()
        user = User(
            name=name,
            user_id=user_id,
            tag='super_tag'
            )
        
        await self.__user_repo.save(user)

        auth_data = AuthData(
            user_id=user_id,
            login=login,
            password_hash=self.__hash(password)
            )
        
        await self.__auth_repo.save(auth_data)

        return user