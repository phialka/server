"""
REST api routers based on fastapi
"""
from .files import files_router
from .profile import profile_routers, register_routers
from .authentification import auth_routers
from .users import users_routers
from .servers import server_routers
from .channels import channel_routers
from .private_chats import private_chat_routers
from .messages import message_routers