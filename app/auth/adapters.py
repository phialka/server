from typing import Literal, Optional
from datetime import timedelta, datetime, timezone
import jwt
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError

from auth.schemas import AuthData
from auth.abstracts import AuthDataRepo, IJWTManager, AuthDataFilter
from auth.dbmodels import AuthData as DBAuthData

from exceptions import AuthError



class SQLAuthDataRepo(AuthDataRepo):

    def __init__(self) -> None:
        self.__table = DBAuthData


    def __serialize_filter(self, filter: AuthDataFilter):
        """
        Amazing filter serialization from data model to ORMAR style
        """
        return self.__table.login == filter.login


    async def save(self, data: AuthData) -> bool:
        await self.__table.objects.create(
            user_id = data.user_id,
            login = data.username,
            pass_hash = data.password_hash
        )

        return True


    async def get(self, filter: Optional[AuthDataFilter] = None) -> list[AuthData]:
        if filter:
            auth_data = await self.__table.objects.all(self.__serialize_filter(filter))
        else:
            auth_data = await self.__table.objects.all()
        auth_data = [AuthData(
                user_id=ad.user_id.id,
                username=ad.login,
                password_hash=ad.pass_hash
                ) for ad in auth_data]

        return auth_data


    async def update(self, filter: AuthDataFilter, **kwargs) -> int:
        pass


    async def delete(self, filter: AuthDataFilter) -> int:
        count = await self.__table.objects.delete(self.__serialize_filter(filter))
        return count



# class JsonAuthDataRepo(AuthDataRepo):
#     pass



class JWTManager(IJWTManager):
    def __init__(self, key: str, access_ttl: Optional[int] = 300, refersh_ttl: Optional[int] = 3000) -> None:
        self.__secret_key = key
        self.__access_ttl = timedelta(seconds=access_ttl)
        self.__refresh_ttl = timedelta(seconds=refersh_ttl)

    
    def __create_token(self, subj: str, exp_time: datetime, type: Literal['access', 'refresh']) -> bytes:
        token = jwt.encode(
            payload = {
                'sub': subj,
                'exp': exp_time,
                'type': type
                },
            key = self.__secret_key
        )

        return token


    def __decode_token(self, token: bytes) -> dict:
        try:
            decode = jwt.decode(
                jwt = token,
                key = self.__secret_key
            )
        except ExpiredSignatureError:
            raise AuthError(msg='Signature has expired')
        except InvalidSignatureError:
            raise AuthError(msg='Invalid signature')

        return decode
    

    def create_access_token(self, sub: str) -> bytes:
        token = self.__create_token(
            subj = sub, 
            exp_time = datetime.now(tz=timezone.utc) + self.__access_ttl,
            type = 'access'
            )
    
        return token
    

    def create_refresh_token(self, sub: str) -> bytes:
        token = self.__create_token(
            subj = sub, 
            exp_time = datetime.now(tz=timezone.utc) + self.__refresh_ttl,
            type = 'refresh'
            )
    
        return token


    def get_jwt_subject(self, token: bytes) -> str:
        payload = self.__decode_token(token=token)
        
        return payload['sub']
    

    def is_refresh_token(self, token: str) -> bool:
        payload = self.__decode_token(token=token)
        return payload['type'] == 'refresh'
    

    def is_access_token(self, token: str) -> bool:
        payload = self.__decode_token(token=token)
        return payload['type'] == 'access'
