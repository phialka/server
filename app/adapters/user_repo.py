from use_cases.abstracts import UserRepo
from entities import User, UserFilter, File
from database import tables



class SQLUserRepo(UserRepo):

    def __init__(self) -> None:
        self.__table = tables.User


    async def save(self, user: User) -> bool:
        await self.__table.objects.create(
            id = user.user_id,
            name = user.name,
            description = user.description,
            tag = user.tag,
            birthdate = user.birthdate,
            photo = None if not user.photo else user.photo.file_id
        )

        return True


    async def get(self, filter: UserFilter) -> list[User]:
        if filter.user_id:
            users = await self.__table.objects.all(self.__table.id == filter.user_id)
            users = [User(
                user_id=u.id,
                name=u.name,
                description=u.description,
                tag=u.tag,
                birthdate=u.birthdate,
                photo=None if not u.photo else File(
                    file_id=u.photo.id,
                    download_id=u.photo.download_id,
                    size=u.photo.size,
                    hash=u.photo.hash,
                    mime_type=u.photo.hash,
                    upload_at=u.photo.upload_at
                ))
                for u in users
            ]
            return users
        else:
            return []


    async def update(self, filter: UserFilter, **kwargs) -> int:
        pass


    async def delete(self, filter: UserFilter) -> int:
        if filter.user_id:
            count = await self.__table.objects.delete(self.__table.id == filter.user_id)
        else:
            return 0