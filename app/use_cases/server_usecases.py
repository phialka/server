from typing import BinaryIO
from uuid import UUID, uuid4
from hashlib import md5
from datetime import datetime
from typing import Optional

from entities import User, UserFilter, AuthData, File
from .abstracts import UserRepo, AuthDataRepo
from .exceptions import UserAlreadyExist, UserTagAlreadyExist, ForbiddenError

from use_cases.files_usecases import FileUseCases



class ServerUseCases():
    def __init__(self, user_repo: UserRepo, auth_repo: AuthDataRepo, file_uc: FileUseCases) -> None:
        self.__user_repo: UserRepo = user_repo
        self.__auth_repo: AuthDataRepo = auth_repo
        self.__file_uc: FileUseCases = file_uc

    
    def __hash(self, string: str):
        return md5(string.encode()).hexdigest()


    