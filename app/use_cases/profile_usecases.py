from typing import BinaryIO
from uuid import UUID, uuid4
from hashlib import md5
from datetime import datetime
from typing import Optional

from entities import User, UserFilter, AuthData, File
from .abstracts import UserRepo, AuthDataRepo
from .exceptions import UserAlreadyExist, UserTagAlreadyExist, ForbiddenError

from use_cases.files_usecases import FileUseCases



class ProfileUseCases():
    def __init__(self, user_repo: UserRepo, auth_repo: AuthDataRepo, file_uc: FileUseCases) -> None:
        self.__user_repo: UserRepo = user_repo
        self.__auth_repo: AuthDataRepo = auth_repo
        self.__file_uc: FileUseCases = file_uc

    
    def __hash(self, string: str):
        return md5(string.encode()).hexdigest()


    async def register(self, name: str, login: str, password: str, tag: Optional[str] = None, description: Optional[str] = None, birthdate: Optional[str] = None) -> User:

        #check login is free
        exist_auth = await self.__auth_repo.get()
        if any([ad.login == login for ad in exist_auth]):
            raise UserAlreadyExist()
        
        #check tag is free
        exist_users = await self.__user_repo.get()
        if tag:
            if any([u.tag == tag for u in exist_users]):
                raise UserTagAlreadyExist()
        else:
            auto_tags_numbers = sorted([int(u.tag.split('r')[1]) for u in exist_users if u.tag.startswith('usr')])
            tag = 'usr'+str(auto_tags_numbers[0]+1) if len(auto_tags_numbers)!=0 else 'usr1'
        
        user_id = uuid4()
        user = User(
            name=name,
            user_id=user_id,
            tag=tag,
            description=description,
            birthdate=birthdate
            )
        
        await self.__user_repo.save(user)

        auth_data = AuthData(
            user_id=user_id,
            login=login,
            password_hash=self.__hash(password)
            )
        
        await self.__auth_repo.save(auth_data)

        return user


    # async def update_profile(self, user_id: UUID, requester_id: UUID) -> User:
    #     if requester_id != user_id:
    #         raise ForbiddenError()
    #     else:
    #         pass


    # async def set_profile_photo(self, photo: BinaryIO, user_id: UUID, requester_id: UUID) -> File:
    #     if requester_id != user_id:
    #         raise ForbiddenError()
    #     photo = await self.__file_uc.upload_file(photo)
        
    #     return photo