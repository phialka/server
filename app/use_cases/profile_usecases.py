from typing import BinaryIO
from uuid import UUID, uuid4
from hashlib import md5
from datetime import date
from typing import Optional

from entities import User, AuthData, File
from .datamodels.filters import UserFilter
from .abstracts import UserRepo, AuthDataRepo
from .exceptions import AlreadyExistsException, NotFoundException, AccessDeniedException

from use_cases.files_usecases import FileUseCases



class ProfileUseCases():
    def __init__(self, user_repo: UserRepo, auth_repo: AuthDataRepo, file_uc: FileUseCases) -> None:
        self.__user_repo: UserRepo = user_repo
        self.__auth_repo: AuthDataRepo = auth_repo
        self.__file_uc: FileUseCases = file_uc

    
    def __hash(self, string: str):
        return md5(string.encode()).hexdigest()
    

    async def __check_user_exist(self, user_id: UUID):
        users = await self.__user_repo.get(filter=UserFilter(user_id=user_id))

        if len(users) == 0:
            raise NotFoundException(msg='User not found')


    async def register(self, name: str, login: str, password: str, tag: Optional[str] = None, description: Optional[str] = None, birthdate: Optional[str] = None) -> User:
        '''
        Register user on server
        '''

        #check login is free
        exist_auth = await self.__auth_repo.get()
        if any([ad.login == login for ad in exist_auth]):
            raise AlreadyExistsException(msg='Current login already involved')
        
        #check tag is free
        exist_users = await self.__user_repo.get()
        if tag:
            if any([u.tag == tag for u in exist_users]):
                raise AlreadyExistsException(msg='Current user tag already involved')
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


    async def update_profile(
            self, 
            user_id: UUID, 
            requester_id: UUID, 
            new_name: Optional[str] = None,
            new_description: Optional[str] = None,
            new_tag: Optional[str] = None,
            new_birthdate: Optional[date] = None
            ) -> User:
        '''
        Update user profile\n
        It can do only profile owner
        '''
        if requester_id != user_id:
            raise AccessDeniedException(msg='You dont have permission to update this profile')
        
        await self.__check_user_exist(user_id=user_id)

        fields_to_update = dict()
        if new_name:
            fields_to_update['name'] = new_name
        if new_description:
            fields_to_update['description'] = new_description
        if new_tag:
            fields_to_update['tag'] = new_tag
        if new_birthdate:
            fields_to_update['birthdate'] = new_birthdate
        if len(fields_to_update) == 0:
            raise

        await self.__user_repo.update(filter=UserFilter(user_id=user_id), **fields_to_update)
        return (await self.__user_repo.get(filter=UserFilter(user_id=user_id)))[0]


    async def set_profile_photo(self, photo: BinaryIO, user_id: UUID, requester_id: UUID) -> File:
        if requester_id != user_id:
            raise AccessDeniedException(msg='You dont have permission to update this profile')
        
        await self.__check_user_exist(user_id=user_id)
        
        profile_photo = await self.__file_uc.upload_file(photo)

        await self.__user_repo.update(filter=UserFilter(user_id=user_id), photo=profile_photo)
        
        return profile_photo
    

    async def delete_profile_photo(self, user_id: UUID, requester_id: UUID) -> bool:
        if requester_id != user_id:
            raise AccessDeniedException(msg='You dont have permission to update this profile')
        
        await self.__check_user_exist(user_id=user_id)

        await self.__user_repo.update(filter=UserFilter(user_id=user_id), photo=None)
        
        return True
    

    async def delete_profile(self, user_id: UUID, requester_id: UUID) -> bool:
        if requester_id != user_id:
            raise AccessDeniedException(msg='You dont have permission to delete this profile')
        
        await self.__check_user_exist(user_id=user_id)

        await self.__user_repo.delete(filter=UserFilter(user_id=user_id))
        
        return True