from use_cases.abstracts import AuthDataRepo
from entities import AuthData, AuthDataFilter
from database import tables



class SQLAuthDataRepo(AuthDataRepo):

    def __init__(self) -> None:
        self.__table = tables.AuthData


    async def save(self, data: AuthData) -> bool:
        await self.__table.objects.create(
            user_id = data.user_id,
            login = data.login,
            pass_hash = data.password_hash
        )

        return True


    async def get(self, filter: AuthDataFilter) -> list[AuthData]:
        if filter.login:
            auth_data = await self.__table.objects.all(self.__table.login == filter.login)
            auth_data = [AuthData(
                user_id=ad.user_id.id,
                login=ad.login,
                password_hash=ad.pass_hash
                ) for ad in auth_data]
        else:
            auth_data = []

        return auth_data


    async def update(self, filter: AuthDataFilter, **kwargs) -> int:
        pass


    async def delete(self, filter: AuthDataFilter) -> int:
        if filter.login:
            count = await self.__table.objects.delete(self.__table.login == filter.login)
        else:
            count = 0
        return count




# class JsonAuthDataRepo(AuthDataRepo):
#     pass