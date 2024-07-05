from use_cases.abstracts import AuthDataRepo
from entities import AuthData
from use_cases.datamodels.filters import AuthDataFilter

from database import tables
from typing import Optional



class SQLAuthDataRepo(AuthDataRepo):

    def __init__(self) -> None:
        self.__table = tables.AuthData


    def __serialize_filter(self, filter: AuthDataFilter):
        """
        Amazing filter serialization from data model to ORMAR style
        """
        return self.__table.login == filter.login


    async def save(self, data: AuthData) -> bool:
        await self.__table.objects.create(
            user_id = data.user_id,
            login = data.login,
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
                login=ad.login,
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