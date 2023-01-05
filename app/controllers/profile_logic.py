from typing import List, Optional
import time

from fastapi import HTTPException, status, UploadFile
from fastapi.responses import JSONResponse

from dbmodels import *
import schemas
from auth import JWTAuth
from controllers.files_logic import Storage, SavedFile



class UList():
    def __init__(self, ) -> None:
        self.__dbuserlist: UserList
        self.__dbusers: List[ServerUser]     
        self.__view: schemas.UserList.View

    @property
    def view(self):
        return self.__view 

    async def _create_view(self):
        self.__view = schemas.UserList.View(
            id = self.__dbuserlist.id,
            title = self.__dbuserlist.title,
            settings = schemas.UserList.View.Settings(
                ban_messages = self.__dbuserlist.settings_.ban_messages,
                notification_settings= self.__dbuserlist.settings_.notifications
            )
        )
        return self

    async def create(self, owner_id, schema: schemas.UserList.Create):
        settings = UserList.Settings(ban_messages=schema.ban, notifications=schema.notification_settings)
        self.__dbuserlist = await UserList.objects.create(owner_id=owner_id, title=schema.title, settings=settings.json())
        return self._create_view()



class ServerUser():
    def __init__(self, id: Optional[int]) -> None:
        id: int
        if id:
            self.id = id
        self.__dbuser: User
        self.__dbinfo: UserInfo
        self.__dbsettings: UserSettings

        self.__info: UserInfo.Info
        self.__settings: UserSettings.Settings

        self.__view: schemas.User.View

    @property
    async def view(self):
        await self.__init_user()
        await self.__init_info()
        return (await self.__create_view()).__view

    async def __init_user(self):
        self.__dbuser = await User.objects.filter(User.id == self.id).get_or_none()
        self.id = self.__dbuser.id
    
    async def __init_info(self):
        self.__dbinfo = await UserInfo.objects.filter(UserInfo.user_id.id == self.id).get_or_none()
        self.__info = self.__dbinfo.info_

    async def __init_settings(self):
        self.__dbsettings = await UserSettings.objects.filter(UserSettings.user_id.id == self.id).get_or_none()
        self.__settings = self.__dbsettings.settings_

    async def __update_info(self, **kwargs):
        self.__info = UserInfo.Info(**{arg[0]:arg[1] for arg in self.__info.dict().items() if arg[0] not in kwargs}, **kwargs)


    async def __create_view(self):
        if self.__info.photo_file_id:
            photo = await SavedFile(self.__info.photo_file_id).view
        else:
            photo = None

        self.__view = schemas.User.View(
            id = self.id,
            name = self.__info.name,
            shortname = self.__info.shortname,
            descriptiion = self.__info.description,
            photo = photo,
            last_time = self.__info.last_visit
        )
        return self

    
    async def create(self, reg: schemas.User.Registration):
        @database.transaction()
        async def creating_transaction():
            #if such user already exists
            if await User.objects.filter(username=reg.username).exists():
                raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="such user already exist")

            #create user
            self.__dbuser = await User.objects.create(username=reg.username, userpass=reg.userpass)
            self.id = self.__dbuser.id

            #create userinfo
            self.__info =  UserInfo.Info(name = reg.name, shortname = reg.shortname, description = reg.description, email = reg.email, last_visit=time.time())
            self.__dbinfo = await UserInfo.objects.create(user_id=self.__dbuser, info=self.__info.json())

            #create usersettings
            self.__settings = UserSettings.Settings(privacy_settings=UserSettings.Settings.PrivacySettings())
            self.__dbsettings = await UserSettings.objects.create(user_id=self.__dbuser, settings=self.__settings.json())

            #create contacts and blacklist
            contacts_settings = UserList.Settings(contacts=True, notifications=UserList.Settings.NotificationSettings())
            blacklist_settings = UserList.Settings(black_list=True, notifications=UserList.Settings.NotificationSettings())
            await UserList.objects.create(owner_id=self.__dbuser, title="Contacts", settings=contacts_settings.json())
            await UserList.objects.create(owner_id=self.__dbuser, title="Blacklist", settings=blacklist_settings.json())
        await creating_transaction()
        return self


    async def set_photo(self, photo: UploadFile):
        await self.__init_info()
        file = await (await SavedFile().save(photo)).view
        await self.__update_info(photo_file_id = file.file_id)
        await UserInfo.objects.filter(UserInfo.user_id.id == self.id).update(info = self.__info.json())
        return file


    async def _get_user_settings(self, user_id):
        self.id = user_id
        uset = await UserSettings.objects.get_or_none(user_id=self.id)
        self.settings = uset.settings_
        return self


    async def _get_userlists(self) -> List[UList]:
        return await UserList.objects.filter(owner_id = self.id).exclude_fields("owner_id").all()

    
    async def create_conversation_list(self, list_schema: schemas.ConversationList.Create):
        notify_settings = UserList.Settings.NotificationSettings(**list_schema.notifications)
        await UserList.objects.create(owner_id=self.id, title=list_schema.title, notify_settings=notify_settings.json())


    async def edit_profile_info(self, info: schemas.User.EditInfo):
        old_uinfo = await UserInfo.objects.get_or_none(user_id=self.id)
        old_info = old_uinfo.info_.dict()

        for key in info.dict().keys():
            if info.dict()[key]!=None:
                old_info[key] = info.dict()[key]
        
        await UserInfo.objects.filter(UserInfo.user_id.id == self.id).update(info=old_info)
        return old_info



class UserController():

    @classmethod
    async def check_username_isfree(cls, username: str) -> bool:
        if await User.objects.filter(username=username).exists():
            return False
        else:
            return True
