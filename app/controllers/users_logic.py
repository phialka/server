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

        self.__users: List[ServerUser]   

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
        self.__privacy_options_view: schemas.User.PrivacyOptions

    @property
    async def view(self):
        await self.__init_user()
        await self.__init_info()
        return (await self.__create_view()).__view

    @property
    async def privacy_options(self):
        await self.__init_user()
        await self.__init_settings()
        return (await self.__create_privacy_options_view()).__privacy_options_view

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
        separate_kwargs = {karg[0]:karg[1] for karg in kwargs.items() if karg[1] != None}
        self.__info = UserInfo.Info(
            **{arg[0]:arg[1] for arg in self.__info.dict().items() if arg[0] not in separate_kwargs}, 
            **separate_kwargs #a dubious decision. it will not allow assigning the value None to some parameters
            )
    
    async def __update_privacy_settings(self, **kwargs):
        def separator(unsep_dict: dict):
           return {karg[0]:karg[1] for karg in unsep_dict.items() if karg[1] != None}
        
        separate_kwargs = separator(kwargs)
        self.__settings = UserSettings.Settings(
            privacy_settings = UserSettings.Settings.PrivacySettings(
                **{arg[0]:arg[1] for arg in self.__settings.dict().items() if arg[0] not in separate_kwargs}, 
                **separate_kwargs #a dubious decision. it will not allow assigning the value None to some parameters
            ))

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

    async def __create_privacy_options_view(self):
        self.__privacy_options_view = schemas.User.PrivacyOptions(
            online_display = self.__settings.privacy_settings.online_display,
            profile_photo_display = self.__settings.privacy_settings.profile_photo_display,
            personal_messages_resend = self.__settings.privacy_settings.personal_messages_resend,
            can_write = self.__settings.privacy_settings.can_write,
            mentions = self.__settings.privacy_settings.mentions,
            add_to_chats = self.__settings.privacy_settings.add_to_chats,
            add_to_channels = self.__settings.privacy_settings.add_to_channels,
            can_find = self.__settings.privacy_settings.can_find
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


    async def edit_info(self, new_info: schemas.User.EditInfo):
        await self.__init_info()
        await self.__update_info(**new_info.dict())
        await UserInfo.objects.filter(UserInfo.user_id.id == self.__dbinfo.user_id).update(info = self.__info.json())
        return self


    async def edit_privacy_settings(self, new_settings: schemas.User.EditSettings):
        await self.__init_settings()
        await self.__update_privacy_settings(**new_settings.dict())
        await UserSettings.objects.filter(UserSettings.user_id.id == self.__dbsettings.user_id).update(settings = self.__settings.json())
        return self


    async def set_photo(self, photo: UploadFile):
        await self.__init_info()
        file = await (await SavedFile().save(photo)).view
        await self.__update_info(photo_file_id = file.file_id)
        await UserInfo.objects.filter(UserInfo.user_id.id == self.id).update(info = self.__info.json())
        return file



class UserController():

    @classmethod
    async def check_username_isfree(cls, username: str) -> bool:
        if await User.objects.filter(username=username).exists():
            return False
        else:
            return True
