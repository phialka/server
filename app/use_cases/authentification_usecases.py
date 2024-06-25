from entities import AuthData, AuthDataFilter
from .abstracts import AuthDataRepo, JWTManager
from .exceptions import UncorerctLogin, UncorrectPassword
from hashlib import md5



class AuthUseCases():
    def __init__(self, repo: AuthDataRepo, jwt_manager: JWTManager) -> None:
        self.__repo: AuthDataRepo = repo
        self.__jwt_manager: JWTManager = jwt_manager


    def __hash(self, string: str):
        return md5(string.encode()).hexdigest()
    

    async def get_jwt_by_logpass(self, login: str, password: str) -> list[str]:
        auth_data = await self.__repo.get(filter=AuthDataFilter(login=login))

        if len(auth_data) == 0:
            raise UncorerctLogin()
        else:
            auth_data = auth_data[0]
        
        if auth_data.password_hash != self.__hash(password):
            raise UncorrectPassword()
        
        user_id = auth_data.user_id
        access_t = self.__jwt_manager.create_access_token(subject=user_id.hex, exp_time=300)
        refresh_t = self.__jwt_manager.create_refresh_token(subject=user_id.hex, exp_time=3000)

        return access_t, refresh_t
        


    async def refresh_jwt(self, refresh_token: str) -> list[str]:
        user_id = self.__jwt_manager.get_jwt_subject(refresh_token)

        access_t = self.__jwt_manager.create_access_token(subject=user_id, exp_time=300)
        refresh_t = self.__jwt_manager.create_refresh_token(subject=user_id, exp_time=3000)

        return access_t, refresh_t

    
    


